# PORT NOTES · STATE — the v16 transmitter log and `game_state.gd`, transcribed

**Unit 0.8b-spec (CLOUD-OK).** This is the implementation checklist for the
rest of 0.8b: every field `game_state.gd` owns, its type, its default, whether
it rides in the v16 save, who writes it from outside, and every signal with
its emitters and listeners. Source of truth: `scripts/game_state.gd` at the
commit this file landed in (777 lines). Where these notes and that file
disagree, THE CODE IS THE INTENT (PORT-BRIEF law); fix the notes.

UE home per `docs/packet/portbrief/UE5-MIGRATION-MAP.md`: the autoload is
`URestorationState : UGameInstanceSubsystem`; the JSON log becomes
`URestorationSaveGame : USaveGame`; signals become multicast delegates with
the same names. Both already exist from 0.8a
(`ue/Restoration/Source/Restoration/RestorationState.h`) — §6 lists exactly
what that skeleton still lacks against this schema.

Constants that are canon (never change the numbers):

| Constant | Value | Home |
|---|---|---|
| `SAVE_VERSION` | 16 | `URestorationState::SaveVersion` (present) |
| `SAVE_PATH` | `user://transmitter_log.json` | slot `"restoration"` (present) |
| `SETTINGS_PATH` | `user://settings.cfg` | not yet ported (§4) |
| `DEMO` | `false` | build flag; see §5 for what it strips |
| `Mode` enum | `MATINEE=0, LATE_NIGHT=1, ONE_TAKE=2` | `SaveGame.Mode` int; default LATE_NIGHT=1 (skeleton defaults 0 — §6) |
| `ITEM_ORDER` | `WATCH, PEN, PHOTOGRAPH, LIGHTER, COMPACT, KEYS, LOUPE` | 7 entries; `items_lost` indexes it |
| `GLYPH_MAP` | `E→interact, SPACE→respond, Q→improvise, T→toggle_tbc, M→map` | glyph substitution in toasts |
| `REMAP_ACTIONS` | `interact, respond, improvise, toggle_tbc, map` | the five rebindable actions |
| Paper default | `{S1:3, S2:3, S3:3, S4:3, S5:3}` (DEMO: `{S1:3, S5:3}`) | 3 lines per station per tape |
| Full sheet | `strikes >= 4` (or any strike in ONE_TAKE) | `Strike()` (present) |
| Dead room rect | `|x-19.0| <= 2.2 && |z-2.5| <= 2.7` (Godot m) | `InDeadRoom` (present, in uu) |
| Fallback respawn | `Vector3(0, 1.0, 2.5)` | `respawn_point()` when no signature |
| Station respawn offset | `pos + (0, 0.5, 1.2)` | `register_station()` |
| Sign-log noise | `noise_event(respawn_point(), 4.0)` | `_sign_finish()` |
| Tape cap | `current_tape = min(day, 5)` | `set_night(false)` |
| Prototype complete | `day >= 3` on a morning | `set_night(false)` sets `run_complete` |
| `mouse_sens` clamp | `0.2 .. 3.0` | `load_settings()` |
| `ui_scale` clamp | `0.8 .. 1.6` | `set_ui_scale()` |
| Documents total | 10 (`read_props` toast says "of 10") | `mark_read()` |
| Assets total | 4 (`assets` toast says "of 4") | `gain_asset()` |
| Leland answers needed | 5, with `seance_wear > 70.0` for the offer | `seance_dock.gd`, `hud.gd` |

---

## 1 · THE v16 `_save_dict` SCHEMA (55 keys incl. `version`, in dict order)

Types are the GDScript declared types. "Load coerces" is what `load_log()`
does to the JSON value — it is the migration rule: every key is read with
`data.get(key, default)`, so ANY older log loads and missing keys take the
default. Arrays and the paper dict are only accepted if the JSON type
matches; otherwise the field keeps its current value.

| # | JSON key | Var | Type | Default | Load coerces | Written by (outside game_state.gd) |
|---|---|---|---|---|---|---|
| 1 | `version` | `SAVE_VERSION` | int | 16 | `int`, default 1 if absent | — |
| 2 | `mode` | `mode` | int (Mode) | `LATE_NIGHT` (1) | `int` | `set_mode()` only |
| 3 | `tbc` | `tbc_enabled` | bool | false | `bool` | `set_tbc()` only |
| 4 | `tape` | `current_tape` | int | 1 | `int` | 1 external assignment |
| 5 | `paper` | `paper` | Dictionary String→int | 5 stations × 3 | per-key `int`, merged INTO existing dict (keys not in the file survive) | — |
| 6 | `signatures` | `signatures` | Array of Dict `{station:String, tape:int, signed:String, presigned?:bool}` | `[]` | array replaces | — (`sign_log`, `mark_presigned`) |
| 7 | `captures` | `captures` | Array of Dict `{name:String, tape:int, at:String}` | `[]` | array replaces | — (`log_capture`) |
| 8 | `strikes` | `strikes` | int | 0 | `int` | — |
| 9 | `items_lost` | `items_lost` | int | 0 | `int` | — |
| 10 | `day` | `day` | int | 1 | `int` | 1 external assignment |
| 11 | `keys` | `keys` | Array of String (key ids, e.g. `"QUIET ROOM"`) | `[]` | array replaces | — (`take_key`) |
| 12 | `pt` | `pt` | int | 0 | `int` | — (`add_pt`) |
| 13 | `dailies` | `dailies` | Array of Dict `{id:int, take:int}` (take −1 = shortcut daily) | `[]` | array replaces | — |
| 14 | `daily_seq` | `daily_seq` | int | 0 | `int` | — |
| 15 | `carried_id` | `carried_id` | int | −1 | `int` | — (`pick_daily`, `burn_daily`) |
| 16 | `carried_take` | `carried_take` | int | 0 | `int` | — |
| 17 | `film_watched` | `film_watched` | bool | false | `bool` | 1 |
| 18 | `signals_known` | `signals_known` | Array of String | `[]` | array replaces | — (`add_show_signal`) |
| 19 | `screening_done` | `screening_done` | bool | false | `bool` | 1 |
| 20 | `run_complete` | `run_complete` | bool | false | `bool` | — |
| 21 | `has_fire_tape` | `has_fire_tape` | bool | false | `bool` | 2 |
| 22 | `fire_tape_watched` | `fire_tape_watched` | bool | false | `bool` | 1 |
| 23 | `seance_wear` | `seance_wear` | **float** | 0.0 | `float` | — (`add_wear`) |
| 24 | `leland_answers` | `leland_answers` | Array of **int** (answer frame indices) | `[]` | array replaces | `seance_dock.gd` appends / resets |
| 25 | `presigned_seen` | `presigned_seen` | bool | false | `bool` | — (`mark_presigned`) |
| 26 | `dock_done` | `dock_done` | bool | false | `bool` | 1 |
| 27 | `assets` | `assets` | Array of String (e.g. `"VERSE"`) | `[]` | array replaces | 1 (`gain_asset` + one direct) |
| 28 | `decision` | `decision` | String | `""` | `str` | 2 |
| 29 | `lockdown_done` | `lockdown_done` | bool | false | `bool` | 2 |
| 30 | `finale_done` | `finale_done` | bool | false | `bool` | — (`mark_ending`) |
| 31 | `ending_reached` | `ending_reached` | String | `""` | `str` | — (`mark_ending`) |
| 32 | `lie_pending` | `lie_pending` | bool | false | `bool` | 1 |
| 33 | `vess_insight` | `vess_insight` | bool | false | `bool` | 1 |
| 34 | `vess_credited` | `vess_credited` | bool | false | `bool` | 1 |
| 35 | `ng_relic` | `ng_relic` | String (an ITEM_ORDER name or `""`) | `""` | `str` | — (`reset_new_game`) |
| 36 | `crate_opened` | `crate_opened` | bool | false | `bool` | 1 |
| 37 | `night_tripped` | `night_tripped` | bool | false | `bool` | 1 |
| 38 | `cov_monitor` | `cov_monitor` | float | 0.0 | `float` | 2 (`coverage_director`) |
| 39 | `cov_move` | `cov_move` | float | 0.0 | `float` | 2 |
| 40 | `cov_still` | `cov_still` | float | 0.0 | `float` | 2 |
| 41 | `photo_safe` | `photo_safe` | bool | false | `bool` | — (`set_photo_safe`) |
| 42 | `cascade_done` | `cascade_done` | bool | false | `bool` | 1 |
| 43 | `read_props` | `read_props` | Array of String (`"D01"`..`"D10"`) | `[]` | array replaces | — (`mark_read`) |
| 44 | `af_active` | `af_active` | bool | false | `bool` | 1 |
| 45 | `af_taught` | `af_taught` | bool | false | `bool` | 1 |
| 46 | `casualties` | `casualties` | Array of Dict `{who:String, cause:String, line:String, day:int}` | `[]` | array replaces | — (`mark_casualty`) |
| 47 | `merle_offered` | `merle_offered` | bool | false | `bool` | 1 |
| 48 | `signoff_completed` | `signoff_completed` | bool | false | `bool` | 1 |
| 49 | `row_casualties` | `row_casualties` | int | 0 | `int` | 1 |
| 50 | `h2_pending` | `h2_pending` | bool | false | `bool` | 2 |
| 51 | `deadroom_seen` | `deadroom_seen` | bool | false | `bool` | 1 |
| 52 | `rejected_seen` | `rejected_seen` | bool | false | `bool` | 1 |
| 53 | `glimpse_seen` | `glimpse_seen` | bool | false | `bool` | 1 |
| 54 | `merle_1974` | `merle_1974` | bool | false | `bool` | 1 |
| 55 | `fire_unsealed` | `fire_unsealed` | bool | false | `bool` | 1 |

(55 rows: 54 state keys plus `version`.)

Casualty `who` vocabulary as used by `all_cast_dead()`: `MERLE`, `VESS`,
`HARRIET`, `FLOOR MANAGER`; `LELAND` is also queried via `is_dead`.

**Save-write contract.** `save_log()` is called from inside game_state on
every mutation listed above and from 18 other scripts directly. There is no
autosave timer and no save-on-quit: the log is a ledger, written at the
moment of the act (canon: saving IS signing a log station, but the file is
kept current so a crash loses nothing). UE: `SaveToSlot()` after every
mutating call, same as now — do not batch.

**Version rules.** `v < 16` → re-save immediately, then deferred toast
`"LOG MIGRATED · format v%d to v%d. Nothing was lost."`. `v > 16` → deferred
toast `"LOG FROM A NEWER BUILD · v%d read by v%d. Proceed gently."`. There is
no per-version upgrade code: defaults ARE the migration. Keep it that way.

---

## 2 · LIVE FIELDS THAT ARE NOT SAVED (session-only, reset on boot/new game)

| Var | Type | Default | Reset in `reset_new_game` | Written by | Notes |
|---|---|---|---|---|---|
| `is_night` | bool | false | yes | `set_night()`, 3 external | drives `night_changed`; **saved? NO** — night never survives a reload (day advances on morning) |
| `in_retake` | bool | false | yes | `strike()`, 1 external | retake presentation clears it |
| `station_points` | Dict String→Vector3 | `{}` | no (rebuilt by world) | `register_station()` | respawn anchors, world-stamped |
| `coverage_label` | String | `"AUDIENCE"` | no | `coverage_director` | HUD read only |
| `premiere_live` | bool | false | yes | `mark_ending()`, 1 external | |
| `screening_active` | bool | false | no | 2 external | `merle.gd` reads |
| `map_points` | Array of `[id:String, Vector2(x,z)]` | `[]` | no (rebuilt) | `world_builder` | map view |
| `cascade_active` | bool | false | yes | 2 external | brain-relevant (present in C++) |
| `mouse_sens` | float | 1.0 | no | settings.cfg | §4 |
| `ui_scale` | float | 1.0 | no | settings.cfg | §4 |
| `captions_on` | bool | false | no | settings.cfg | §4 |
| `assist_on` | bool | false | no | settings.cfg | §4 |
| `recording` | bool | false | no | 3 external (bench) | brain-relevant (present) |
| `recording_left` | float | 0.0 | no | 2 external | brain-relevant (present) |
| `crossing` | bool | false | no | 2 external | brain-relevant (present) |
| `crossing_caught` | bool | false | no | 2 external | brain-relevant (present) |
| `harriet_slip` | bool | false | yes | 1 external | consumed by `sign_log` on empty paper |
| `fader_self` | bool | false | no | `live_production` (3) | |
| `_glyph_re` | Dict | `{}` | — | private | regex cache |
| `_demo_t0` | int | 0 | — | private | demo funnel timer |

Eight SAVED fields are NOT reset by `reset_new_game()` — they carry across
runs by design (the reset list is lines 718–768; verified by diff against
§1): `mode`, `tbc_enabled`, `photo_safe`, `lie_pending`, `af_active`,
`af_taught`, `signoff_completed`, `deadroom_seen`. Everything else in §1 is
reset. `ng_relic` is COMPUTED by reset: if `finale_done` and `items_lost > 0`,
the last item lost (`ITEM_ORDER[min(items_lost, 7) - 1]`) becomes the
new-game relic; otherwise `""`.

---

## 3 · SIGNAL INVENTORY (20 signals → multicast delegates, same names)

Emitters "internal" = inside game_state.gd. Listeners from a grep of
`GameState.<signal>.connect` across `scripts/`.

| Signal | Params | Emitted by | Listeners | UE note |
|---|---|---|---|---|
| `tbc_changed` | `enabled:bool` | `set_tbc` | hud, bench_tv | |
| `log_signed` | `station:String, remaining:int` | `_sign_finish`, `mark_presigned` | hud, achievements | |
| `log_refused` | `station:String` | `sign_log` (paper 0, no slip) | hud | |
| `notify` | `text:String` | `toast`, `log_capture`, migration toasts | hud | text already glyph-substituted + `tr()` |
| `capture_status` | `text:String` | `set_capture_status[_raw]` | hud | |
| `sheet_changed` | `count:int` | `strike`, `burn_daily` | hud, dresser | **present** (`OnSheetChanged`) |
| `night_changed` | `now_night:bool` | `set_night`; EXTERNAL: live_production, soak_runner | rundown, world_builder, floor_manager, achievements | rundown gate — the brain listens |
| `captured` | `take:int, sheet_full:bool, lost_item:String, respawn:Vector3` | `strike` (non-full) | hud | retake presentation trigger |
| `daily_added` | `id:int, take:int` | `strike`, `mint_shortcut_daily` | dailies_manager | |
| `daily_burned` | — | `burn_daily` | coverage_director | |
| `run_ended` | `take:int` | `strike` (full sheet); EXTERNAL: rundown | hud, achievements | **present** (`OnRunEnded`) |
| `finale_started` | `decision:String` | `start_finale` | hud | |
| `noise_event` | `pos:Vector3, loudness:float` | `noise()`, `_sign_finish` (4.0 at respawn) | rundown | maps to `ARundown::ReportNoise` (present) — the sign-log noise must be wired |
| `photo_changed` | `on:bool` | `set_photo_safe` | bench_tv | |
| `blackout_changed` | `alpha:float` | `set_blackout` | hud | UMG scrim per migration map |
| `ui_scale_changed` | `scale:float` | `set_ui_scale` | hud | |
| `caption` | `text:String` | `show_caption` (only if `captions_on`) | hud | |
| `pause_requested` | — | EXTERNAL only: player | hud | |
| `demo_ended` | — | EXTERNAL only: capture_bench | hud | DEMO builds |
| `ending_marked` | `ending_name:String` | `mark_ending` | world_builder | also calls `Achievements.on_ending(name)` |

Every one of the 20 declared signals has at least one listener today; none
is dead. Two are emitted ONLY from outside game_state.gd (`pause_requested`
from player, `demo_ended` from capture_bench) — in UE they still live on the
subsystem so the HUD has one place to bind.

---

## 4 · SETTINGS (`user://settings.cfg`, NOT part of the save)

ConfigFile sections/keys → UE: a `UGameUserSettings` subclass or a second
SaveGame slot `"settings"`. Keep the keys.

| Section | Key | Type | Default | Applies to |
|---|---|---|---|---|
| `audio` | `master` | float linear | 1.0 | master bus volume (`linear_to_db(max(vol, 0.001))`) |
| `input` | `sensitivity` | float | 1.0, clamp 0.2..3.0 | `mouse_sens` |
| `access` | `ui_scale` | float | 1.0 | `ui_scale` (set clamp 0.8..1.6) |
| `access` | `captions` | bool | false | `captions_on` |
| `access` | `assist` | bool | false | `assist_on` |
| `keys` | `<action>` | int physical keycode | 0 = unset | one per `REMAP_ACTIONS`; `rebind()` refuses a key already bound to another remappable action ("KEY IN USE · …") |
| `video` | `fullscreen` | bool | false | skipped in headless |

`glyphs(text)` replaces whole-word tokens `E/SPACE/Q/T/M` in toast text with
the CURRENT binding's key name, upper-cased — UE: the controls map's real
binding glyphs (canon: "real binding glyphs"), via Enhanced Input key names.

---

## 5 · DEMO BUILD (Tape 1) STRIPPING

When `DEMO` is true, `save_log()` ERASES these keys before writing (they are
reloaded as defaults): `decision, assets, leland_answers, lockdown_done,
finale_done, ending_reached, lie_pending, seance_wear, has_fire_tape,
fire_tape_watched, dock_done, crate_opened, presigned_seen, cascade_done,
casualties`. Paper is `{S1:3, S5:3}`. `demo_mark(event)` appends
`[min %.1f] event` lines to `user://demo_funnel.txt` (events seen:
`started`, `s1_signed`). `objective_text()` short-circuits after the first
capture. Port when 5.8 lands; the save contract is the point here.

---

## 6 · DELTAS: current C++ skeleton vs this schema (the 0.8b checklist)

`URestorationSaveGame` (0.8a) has 23 properties; the v16 dict has 55. Fix
the SHAPE mismatches first — they are semantic changes and the save's
semantic fields must not change (migration map: WHAT MUST NOT CHANGE):

- [ ] `Mode` default is 0 (MATINEE); spec default is `LATE_NIGHT` = 1.
- [ ] `CurrentTape` default 0; spec 1.
- [ ] `Paper` is `int32`; spec is a per-station map `TMap<FString,int32>`
      seeded `S1..S5 = 3`, and load MERGES keys into the existing map.
- [ ] `Signatures` is `int32`; spec is `TArray<FRestorationSignature>`
      `{Station, Tape, Signed(FString), bPresigned}` — `respawn_point()` reads
      the LAST entry's station, so the array is load-bearing, not a count.
- [ ] `Captures` is `int32`; spec is `TArray<FRestorationCapture>`
      `{Name, Tape, At}` — `objective_text` and the demo check read `.size()`
      only, but the ledger is canon (never-stated ledger law).
- [ ] `SeanceWear` is `int32`; spec is **float** (`> 70.0` threshold).
- [ ] `LelandAnswers` is `int32`; spec is `TArray<int32>` of frame indices
      (`.has(frame)` dedupe — a count cannot dedupe).
- [ ] Missing entirely (add with defaults per §1): `pt`, `carried_id`,
      `carried_take`, `signals_known`, `presigned_seen`, `dock_done`,
      `assets`, `decision`, `lie_pending`, `vess_insight`, `vess_credited`,
      `ng_relic`, `crate_opened`, `night_tripped`, `cov_monitor`, `cov_move`,
      `cov_still`, `photo_safe`, `cascade_done`, `read_props`, `af_active`,
      `af_taught`, `casualties`, `merle_offered`, `signoff_completed`,
      `row_casualties`, `h2_pending`, `deadroom_seen`, `rejected_seen`,
      `glimpse_seen`, `merle_1974`, `fire_unsealed` (32 keys).
- [ ] `SaveToSlot`/`LoadFromSlot` currently copy 4 fields (strikes,
      items_lost, daily_seq, dailies); they must copy all 54.
- [ ] `Strike()`: `ItemsLost` is clamped to 6 but ITEM_ORDER has 7 entries —
      spec is `if items_lost < 7: lost = ITEM_ORDER[items_lost]; items_lost += 1`.
      Also `bFull = strikes >= 4 || mode == ONE_TAKE`; the non-full branch
      must broadcast `captured(take, false, lost, respawn_point())`.
- [ ] `bIsNight` lives in the subsystem but is NOT in the save — correct;
      keep it out.
- [ ] Delegates to add (§3): the 18 not yet declared. `noise_event` should
      route to `ARundown::ReportNoise` exactly as rundown.gd connects it.
- [ ] Functions to port, verbatim order of effects (toast text is canon,
      through `tr()` + glyphs): `paper_for`, `sign_log` (+ harriet_slip
      branch), `_sign_finish` (sign → save → tick sfx → demo_mark S1 →
      `log_signed` → `noise_event(respawn, 4.0)`), `mark_read`, `log_capture`,
      `register_station`, `respawn_point`, `has_key`/`take_key`,
      `add_show_signal`, `pick_daily`, `burn_daily` (strike −1 only if > 0;
      toasts differ), `mint_shortcut_daily`, `set_mode`, `set_night` (morning:
      day += 1, tape = min(day,5), run_complete at day ≥ 3), `set_tbc`,
      `set_photo_safe`, `start_finale`, `mark_ending` (premiere_live=false,
      finale_done=true, ending, `ending_marked`, achievements, lie flag),
      `gain_asset` (4-of-4 toast), `mark_presigned` (a `"TOMORROW"` signature
      at S4 with `presigned=true`), `add_wear`, `add_pt`, `mark_casualty`
      (dedupe by who; toast "THE LEDGER TAKES IT DOWN."), `cause_of`,
      `is_dead`, `all_cast_dead`, `objective_text` (priority ladder as
      written, lines 687–710), `reset_new_game` (with the relic rule).

When every box above is ticked and a v16 log written by the Godot build
round-trips through the UE slot with identical field values, 0.8b-2's state
half is done; the bench loop, stations and Harriet freeze are the other half.
