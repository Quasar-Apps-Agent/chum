# PORT NOTES · STATE (unit 0.8b-spec · the 0.8b implementation checklist)

Source of truth: `scripts/game_state.gd` at commit f79877c, `SAVE_VERSION = 16`.
THE CODE IS THE INTENT (PORT-BRIEF). Every field, type, default, coercion,
signal and method below was extracted from that file by script and
cross-checked against the 0.8a C++ (`ue/Restoration/Source/Restoration/
RestorationState.h/.cpp`). Nothing here is a redesign; where the C++
already disagrees with the GDScript, §9 says so and 0.8b fixes it.

Migration-map homes (do not re-decide): autoload → `URestorationState`
(UGameInstanceSubsystem); JSON log → `URestorationSaveGame` (USaveGame,
Version int + upgrade chain); signals → multicast delegates with the SAME
names; settings.cfg → GameUserSettings/ini, separate from the save.
BUILD-ORDER P2 exit = QA-05, QA-16, QA-31.

---

## 1 · CONSTANTS AND ENUMS

| Godot | Value | Port note |
|---|---|---|
| `SAVE_PATH` | `user://transmitter_log.json` | slot name `restoration` (0.8a); one slot, overwritten on every save |
| `SETTINGS_PATH` | `user://settings.cfg` | separate file, never inside the save |
| `DEMO` | `false` (compile-time; `true` for the Tape 1 demo build) | build flag; drives the §3 whitelist and `objective_text` |
| `SAVE_VERSION` | `16` | `URestorationState::SaveVersion = 16` ✅ |
| `enum Mode` | `MATINEE = 0, LATE_NIGHT = 1, ONE_TAKE = 2` | serialized as int; default `LATE_NIGHT` (1). C++ default `Mode = 0` is WRONG (§9) |
| `ITEM_ORDER` | `["WATCH","PEN","PHOTOGRAPH","LIGHTER","COMPACT","KEYS","LOUPE"]` | 7 entries; `items_lost` indexes it, max 7 |
| `GLYPH_MAP` | `{"E":"interact","SPACE":"respond","Q":"improvise","T":"toggle_tbc","M":"map"}` | word-boundary token → live binding name, applied to every toast |
| `REMAP_ACTIONS` | `["interact","respond","improvise","toggle_tbc","map"]` | the five rebindable actions |
| dead-room rect | `abs(x-19.0) <= 2.2 and abs(z-2.5) <= 2.7` (Godot m) | `InDeadRoom` ported ✅ (1900/220 · 250/270 uu, Godot z → UE y) |
| default respawn | `Vector3(0, 1.0, 2.5)` | when no signature or unknown station |
| station offset | registered pos `+ (0, 0.5, 1.2)` | `register_station` |

---

## 2 · THE SAVE — v16 `_save_dict()` (55 keys, THIS order)

Column "load" is `load_log()`'s exact coercion: scalars go through
`int()/bool()/float()/str()` with the default shown; containers are
accepted ONLY if `typeof()` matches, else the in-memory value is kept.
"C++ 0.8a" = state of `URestorationSaveGame` today (✅ matches · ⚠ type
wrong · ✗ missing · ⏸ declared but never written/read by Save/LoadToSlot).

| # | key | godot var | type | default | load coercion | C++ 0.8a |
|---|---|---|---|---|---|---|
| 1 | `version` | `SAVE_VERSION` | int | 16 | `int(get("version", 1))` → migration (§3) | ✅ |
| 2 | `mode` | `mode` | int (Mode) | 1 LATE_NIGHT | `int(…, Mode.LATE_NIGHT)` | ⚠ default 0 |
| 3 | `tbc` | `tbc_enabled` | bool | false | `bool(…, false)` | ⏸ |
| 4 | `tape` | `current_tape` | int 1..5 | 1 | `int(…, 1)` | ⚠ default 0 |
| 5 | `paper` | `paper` | Dictionary station→int | `{S1:3,S2:3,S3:3,S4:3,S5:3}` | dict typecheck, then MERGED key by key (`paper[k]=int(p[k])`) — never replaced | ⚠ int32 |
| 6 | `signatures` | `signatures` | Array of §4.1 | `[]` | array typecheck, replace | ⚠ int32 |
| 7 | `captures` | `captures` | Array of §4.2 | `[]` | array typecheck, replace | ⚠ int32 |
| 8 | `strikes` | `strikes` | int 0..3 | 0 | `int(…, 0)` | ✅ |
| 9 | `items_lost` | `items_lost` | int 0..7 | 0 | `int(…, 0)` | ✅ (cap bug §9) |
| 10 | `day` | `day` | int ≥1 | 1 | `int(…, 1)` | ⏸ |
| 11 | `keys` | `keys` | Array of String ids | `[]` | array typecheck | ⏸ |
| 12 | `pt` | `pt` | int | 0 | `int(…, 0)` | ✗ |
| 13 | `dailies` | `dailies` | Array of §4.3 | `[]` | array typecheck | ✅ |
| 14 | `daily_seq` | `daily_seq` | int | 0 | `int(…, 0)` | ✅ |
| 15 | `carried_id` | `carried_id` | int (−1 = none) | −1 | `int(…, -1)` | ✗ |
| 16 | `carried_take` | `carried_take` | int | 0 | `int(…, 0)` | ✗ |
| 17 | `film_watched` | `film_watched` | bool | false | `bool` | ⏸ |
| 18 | `signals_known` | `signals_known` | Array of String | `[]` | array typecheck | ✗ |
| 19 | `screening_done` | `screening_done` | bool | false | `bool` | ⏸ |
| 20 | `run_complete` | `run_complete` | bool | false | `bool` | ⏸ |
| 21 | `has_fire_tape` | `has_fire_tape` | bool | false | `bool` | ⏸ |
| 22 | `fire_tape_watched` | `fire_tape_watched` | bool | false | `bool` | ⏸ |
| 23 | `seance_wear` | `seance_wear` | float (percent, >70 is the threshold) | 0.0 | `float(…, 0.0)` | ⚠ int32 |
| 24 | `leland_answers` | `leland_answers` | Array of int (seance frame indices) | `[]` | array typecheck | ⚠ int32 |
| 25 | `presigned_seen` | `presigned_seen` | bool | false | `bool` | ✗ |
| 26 | `dock_done` | `dock_done` | bool | false | `bool` | ✗ |
| 27 | `assets` | `assets` | Array of String ids | `[]` | array typecheck | ✗ |
| 28 | `decision` | `decision` | String enum | `""` | `str(…, "")` | ✗ |
| 29 | `lockdown_done` | `lockdown_done` | bool | false | `bool` | ⏸ |
| 30 | `finale_done` | `finale_done` | bool | false | `bool` | ⏸ |
| 31 | `ending_reached` | `ending_reached` | String enum | `""` | `str` | ⏸ |
| 32 | `lie_pending` | `lie_pending` | bool | false | `bool` | ✗ |
| 33 | `vess_insight` | `vess_insight` | bool | false | `bool` | ✗ |
| 34 | `vess_credited` | `vess_credited` | bool | false | `bool` | ✗ |
| 35 | `ng_relic` | `ng_relic` | String (ITEM_ORDER member or `""`) | `""` | `str` | ✗ |
| 36 | `crate_opened` | `crate_opened` | bool | false | `bool` | ✗ |
| 37 | `night_tripped` | `night_tripped` | bool | false | `bool` | ✗ |
| 38 | `cov_monitor` | `cov_monitor` | float seconds | 0.0 | `float` | ✗ |
| 39 | `cov_move` | `cov_move` | float seconds | 0.0 | `float` | ✗ |
| 40 | `cov_still` | `cov_still` | float seconds | 0.0 | `float` | ✗ |
| 41 | `photo_safe` | `photo_safe` | bool | false | `bool` | ✗ |
| 42 | `cascade_done` | `cascade_done` | bool | false | `bool` | ✗ |
| 43 | `read_props` | `read_props` | Array of String `D01`..`D10` | `[]` | array typecheck | ✗ |
| 44 | `af_active` | `af_active` | bool | false | `bool` | ✗ (live field exists) |
| 45 | `af_taught` | `af_taught` | bool | false | `bool` | ✗ (live field exists) |
| 46 | `casualties` | `casualties` | Array of §4.4 | `[]` | array typecheck | ✗ |
| 47 | `merle_offered` | `merle_offered` | bool | false | `bool` | ✗ |
| 48 | `signoff_completed` | `signoff_completed` | bool | false | `bool` | ✗ |
| 49 | `row_casualties` | `row_casualties` | int | 0 | `int` | ✗ |
| 50 | `h2_pending` | `h2_pending` | bool | false | `bool` | ✗ |
| 51 | `deadroom_seen` | `deadroom_seen` | bool | false | `bool` | ✗ |
| 52 | `rejected_seen` | `rejected_seen` | bool | false | `bool` | ✗ |
| 53 | `glimpse_seen` | `glimpse_seen` | bool | false | `bool` | ✗ |
| 54 | `merle_1974` | `merle_1974` | bool | false | `bool` | ✗ |
| 55 | `fire_unsealed` | `fire_unsealed` | bool | false | `bool` | ✗ |

Value domains (from the writers):
- `keys`: `"EDITH"`, `"TRAINING"`, `"QUIET ROOM"` (world_builder key_items; doors gate on `required_key`).
- `assets`: `"CART"`, `"SCRIPT"`, `"CARD"` (asset_pickup) + `"VERSE"` (spectro_dock); four = finale-ready.
- `signals_known`: the six from film_cabinet (`"YOU'RE ON"`,`"CUT"`,`"STRETCH"`,`"WRAP IT UP"`,`"THIRTY SECONDS"`,`"ON TIME"`) + the seventh from harriet_note (`"HOLD YOUR APPLAUSE"`).
- `read_props`: `D01` (seance_dock) `D02` (script prop) `D03` (decision_ledger) `D06` (harriet_note) `D07` (vess_binder) `D08` (floor_manager) + readable_prop ids; the toast counts "of 10".
- `decision`: `""` | `"AUTHENTICATE"` | `"DESTROY"` | `"PERFORM"`.
- `ending_reached`: `"THE BURN"`, `"THE NEW PRODUCER"` (lie=true), `"SIGN-OFF · LELAND CLOSES"`, `"SIGN-OFF · RITA CLOSES"`, `"THE COMPLETED SIGN-OFF"`, `"A ONE-WOMAN SHOW"`, `"DEAD AIR"`.
- `leland_answers`: seance frame indices (ints; 5 needed; frames 14 and 28 have casualty-aware lines).

---

## 3 · SAVE SEMANTICS THAT MUST NOT CHANGE

1. **One file, whole-state, rewritten on every `save_log()`.** Pretty JSON
   (`JSON.stringify(data, "\t")`). No partial writes, no autosave timer:
   the save is a side effect of the acts listed in §8 ("saves" column).
   Canon: saving IS signing a log station (paper economy), but the file is
   also refreshed by every state-changing act so a crash loses nothing
   after the last act.
2. **Load is tolerant and forward-defaulting.** Missing key → default from
   §2; scalar of the wrong JSON type → coerced; container of the wrong
   type → ignored (in-memory default survives). Non-dictionary file →
   ignored entirely (fresh state). No key is ever required.
3. **`paper` MERGES** — loaded stations overwrite matching defaults; a
   station absent from the file keeps 3. (This is how a DEMO save with
   `{S1,S5}` loads into the full game with S2–S4 intact.)
4. **Version chain.** `v = int(get("version", 1))`. `v < 16` → re-save
   immediately in v16, then deferred toast `LOG MIGRATED · format v%d to
   v%d. Nothing was lost.` `v > 16` → deferred toast `LOG FROM A NEWER
   BUILD · v%d read by v%d. Proceed gently.` (still loads). 0.8a logs the
   same two lines (UE_LOG) — keep the wording for the toast in P3.
5. **DEMO whitelist (erase before write, 15 keys):** `decision, assets,
   leland_answers, lockdown_done, finale_done, ending_reached, lie_pending,
   seance_wear, has_fire_tape, fire_tape_watched, dock_done, crate_opened,
   presigned_seen, cascade_done, casualties`. The demo build never persists
   the late-game arc; on load those keys default. PORT-BRIEF names this
   behavior explicitly as part of the save contract.
6. **NEW GAME (`reset_new_game`) resets every saved key EXCEPT** `version,
   mode, tbc, lie_pending, photo_safe, af_active, af_taught,
   signoff_completed, deadroom_seen`. mode/tbc/photo_safe are player
   preferences riding in the save; the other five carry across runs by the
   code's own behavior (`lie_pending` is consumed by title.gd; af_* and
   deadroom_seen/signoff_completed are once-learned knowledge). Port
   exactly this set — do not "tidy" it.
   NEW GAME also computes `ng_relic = ITEM_ORDER[min(items_lost, 7) - 1]`
   iff `finale_done and items_lost > 0` (the New Game+ relic tag in
   world_builder), then re-issues paper (`{S1,S5}` in DEMO, all five
   otherwise), and saves.
7. **Not persisted, by design:** `is_night`, `in_retake`, `premiere_live`
   and the rest of §5. A loaded game always resumes in DAY of `day`, with
   no retake in flight and no live premiere.
8. **`_ready()` order:** `load_settings()` then `load_log()`. Settings
   never touch the save and vice versa.

---

## 4 · RECORD SHAPES (array elements)

### 4.1 `signatures[]`
`{"station": "S1".."S5", "tape": int, "signed": String}` — `signed` is
`Time.get_datetime_string_from_system()`; the presigned entry is
`{"station":"S4","tape":t,"signed":"TOMORROW","presigned":true}`
(`mark_presigned`). Last entry's station drives `respawn_point()`.

### 4.2 `captures[]`
`{"name": String, "tape": int, "at": datetime String}` (`log_capture`).
Readers: hud (last 5), spectro_dock (needs ≥1), achievements A02, DEMO
objective text.

### 4.3 `dailies[]`
`{"id": int, "take": int}`; `take = -1` for the shortcut daily
(`mint_shortcut_daily`). `FRestorationDaily{Id,Take}` ✅.

### 4.4 `casualties[]`
`{"who": String, "cause": String, "line": String, "day": int}` where
`who ∈ {MERLE, VESS, HARRIET, FLOOR MANAGER, LELAND}` and `cause` is the
canon code + title (`"V1 · CREDITED, THEREFORE CAST"`, `"V2 · THE
UNCREDITED FIX"`, `"M1 · THE SECOND VIEWING"`, `"H1 · CONTINUITY"`, `"H2 ·
THE SPLICE"`, `"F1 · THE FADER"`, `"F2 · THE UNLISTED CAMERA"`, `"L1 · THE
SIXTH QUESTION"`, `"L2 · THE READING"`). One entry per `who` ever
(`mark_casualty` no-ops on a repeat). `all_cast_dead()` = MERLE ∧ VESS ∧
HARRIET ∧ FLOOR MANAGER (Leland excluded).

### 4.5 `paper{}`
`{"S1":int,…,"S5":int}`; `paper_for()` returns 99 in MATINEE regardless.

---

## 5 · RUNTIME-ONLY FIELDS (public, NOT in the save)

| var | type | default | writer(s) | readers | C++ 0.8a |
|---|---|---|---|---|---|
| `is_night` | bool | false | `set_night`; live_production, soak_runner (direct) | bed_prop cascade coverage_director floor_manager glimpse hud live_production lockdown merle night_trip noise_tracker rundown soak_runner | `bIsNight` ✅ |
| `in_retake` | bool | false | `strike` (true); hud:306 (false, when the retake presentation ends) | hud | `bInRetake` ⚠ (§9) |
| `station_points` | Dictionary id→Vector3 | `{}` | `register_station` | `respawn_point` | ✗ |
| `coverage_label` | String | `"AUDIENCE"` | coverage_director | hud | ✗ |
| `premiere_live` | bool | false | live_production (true at premiere start); `mark_ending`/reset (false) | cascade floor_manager glimpse night_trip noise_tracker rundown | `bPremiereLive` ✅ |
| `screening_active` | bool | false | screening_event | merle | ✗ |
| `map_points` | Array of `[id, Vector2(x,z)]` | `[]` | world_builder | map_view | ✗ (P3 map) |
| `cascade_active` | bool | false | cascade | door liveness_check rundown | `bCascadeActive` ✅ |
| `recording` | bool | false | capture_bench | hud rundown | `bRecording` ✅ |
| `recording_left` | float s | 0.0 | capture_bench | hud | `RecordingLeft` ✅ |
| `crossing` | bool | false | live_production | rundown | `bCrossing` ✅ |
| `crossing_caught` | bool | false | live_production, rundown | live_production rundown | `bCrossingCaught` ✅ |
| `harriet_slip` | bool | false | harriet (true); `sign_log` consumes (false) | `sign_log` | ✗ |
| `fader_self` | bool | false | live_production | hud | ✗ |
| `mouse_sens` | float 0.2..3.0 | 1.0 | settings (§6) | player options_panel | settings, not state |
| `ui_scale` | float 0.8..1.6 | 1.0 | settings | hud options_panel | settings |
| `captions_on` | bool | false | settings | options_panel, `show_caption` | settings |
| `assist_on` | bool | false | settings | floor_manager live_production screening_event options_panel | settings |

Private: `_glyph_re` (regex cache), `_demo_t0` (demo funnel clock).

---

## 6 · SETTINGS (`user://settings.cfg`, ConfigFile) — port to GameUserSettings

| section.key | type | default | clamp | applies to |
|---|---|---|---|---|
| `audio.master` | float linear | 1.0 | `max(v, 0.001)` → dB on bus 0 | master submix |
| `input.sensitivity` | float | 1.0 | `clamp 0.2..3.0` | `mouse_sens` |
| `access.ui_scale` | float | 1.0 | `clamp 0.8..1.6` (setter) | `ui_scale` → `ui_scale_changed` |
| `access.captions` | bool | false | | `captions_on` |
| `access.assist` | bool | false | | `assist_on` |
| `keys.<action>` | int physical keycode | 0 (= unbound → keep default) | one key per action; `rebind` refuses a key already bound to another REMAP action (`KEY IN USE`) | InputMap |
| `video.fullscreen` | bool | false | skipped when headless | window mode |

`rebind(action, keycode, persist=true)` erases existing InputEventKey events
for the action, adds the new one, then saves. `key_name(action)` returns the
first key's `OS.get_keycode_string` or `"?"` — this is what `glyphs()`
substitutes into every toast, so UI text carries REAL binding glyphs
(controls-map law).

---

## 7 · SIGNALS → multicast delegates (same names)

| signal | params | emitted by | connected in | C++ 0.8a |
|---|---|---|---|---|
| `tbc_changed` | `enabled: bool` | `set_tbc` | bench_tv hud | ✗ |
| `log_signed` | `station: String, remaining: int` | `_sign_finish`, `mark_presigned` | achievements hud | ✗ |
| `log_refused` | `station: String` | `sign_log` | hud | ✗ |
| `notify` | `text: String` | `toast`, `log_capture`, migration notices | hud | ✗ |
| `capture_status` | `text: String` | `set_capture_status(_raw)` | hud | ✗ |
| `sheet_changed` | `count: int` | `burn_daily`, `strike` | dresser hud | `OnSheetChanged` ✅ |
| `night_changed` | `now_night: bool` | `set_night`; ALSO emitted directly by live_production:50 and soak_runner:30 (`emit(true)` without `set_night`) | achievements floor_manager live_production rundown soak_runner world_builder | ✗ |
| `captured` | `take: int, sheet_full: bool, lost_item: String, respawn: Vector3` | `strike` (non-full only) | hud (the retake presentation) | ✗ |
| `daily_added` | `id: int, take: int` | `strike`, `mint_shortcut_daily` | dailies_manager | ✗ |
| `daily_burned` | — | `burn_daily` | coverage_director | ✗ |
| `run_ended` | `take: int` | `strike` (full sheet); ALSO rundown:224 emits with `dailies.size()` | achievements hud rundown | `OnRunEnded` ✅ |
| `finale_started` | `decision: String` | `start_finale` | hud | ✗ |
| `noise_event` | `pos: Vector3, loudness: float` | `noise`, `_sign_finish` (4.0 at respawn point) | rundown | `ReportNoise` API exists on ARundown; the bus signal itself ✗ |
| `photo_changed` | `on: bool` | `set_photo_safe` | bench_tv | ✗ |
| `blackout_changed` | `alpha: float` | `set_blackout` | hud | ✗ |
| `ui_scale_changed` | `scale: float` | `set_ui_scale` | hud | ✗ |
| `caption` | `text: String` | `show_caption` (only if captions_on) | hud | ✗ |
| `pause_requested` | — | player:44 (external emitter) | hud player | ✗ |
| `demo_ended` | — | capture_bench:62 (external emitter) | capture_bench hud | ✗ |
| `ending_marked` | `ending_name: String` | `mark_ending` | world_builder | ✗ |

Four signals are emitted from OUTSIDE the autoload (`night_changed`,
`run_ended`, `pause_requested`, `demo_ended`): the delegates must stay
publicly broadcastable, not wrapped behind private setters.

---

## 8 · PUBLIC METHOD INVENTORY (45)

"saves" = calls `save_log()`. Call counts are across `scripts/*.gd`
(`toast` alone: 198 sites — it is the game's voice).

| method | returns | side effects | saves | calls |
|---|---|---|---|---|
| `toast(text)` | — | `notify.emit(glyphs(tr(text)))` | | 198 |
| `is_dead(who)` | bool | | | 36 |
| `set_capture_status(text)` | — | `capture_status.emit(glyphs(text))` | | 30 |
| `set_capture_status_raw(text)` | — | `capture_status.emit(text)` (no glyph pass) | | internal |
| `save_log()` | — | writes the file (§3) | ✓ | 20 external |
| `show_caption(text)` | — | `caption.emit(tr(text))` iff `captions_on` | | 16 |
| `mark_casualty(who, cause, epitaph)` | — | append §4.4 once; toast `THE LEDGER TAKES IT DOWN.` | ✓ | 10 |
| `set_blackout(alpha)` | — | `blackout_changed.emit` | | 8 |
| `mark_ending(name, lie=false)` | — | `premiere_live=false; finale_done=true; ending_reached=name; ending_marked.emit; Achievements.on_ending(name); lie→lie_pending=true` | ✓ | 8 |
| `has_key(id)` | bool | | | 8 |
| `mark_read(id)` | — | append once; toast `READ · filed to memory. (%d of 10 documents)` | ✓ | 7 |
| `demo_mark(event)` | — | DEMO only: appends `[min %.1f] event` to `user://demo_funnel.txt` | | 5 |
| `save_settings()` | — | writes settings.cfg | | 4 |
| `set_mode(m)` | — | no-op if same; toast `MODE · %s`; ONE TAKE extra toast | ✓ | 3 |
| `key_name(action)` | String | | | 3 |
| `in_dead_room(pos)` | bool | | | 3 |
| `glyphs(text)` | String | binding substitution | | 3 |
| `strike(player)` | — | §9.3 (the retake economy) | ✓ | 2 |
| `start_finale()` | — | `finale_started.emit(decision)` | | 2 |
| `set_tbc(on)` | — | `tbc_changed.emit` (NO save — tbc persists only via the next save_log) | | 2 |
| `set_photo_safe(on)` | — | `photo_changed.emit`; toast | ✓ | 2 |
| `reset_new_game()` | — | §3.6 | ✓ | 2 |
| `noise(pos, loudness)` | — | `noise_event.emit` | | 2 |
| `gain_asset(id, display)` | — | append once; toast `ASSET BANKED · %s (%d of 4)`; at 4 a second toast | ✓ | 2 |
| `cause_of(who)` | String | | | 2 |
| `add_show_signal(sig)` | — | append once (NO save — persists on the next act) | | 2 |
| `add_pt(n)` | — | `pt += n` | ✓ | 2 |
| `take_key(id, display)` | — | dup → toast `You already carry %s.`; else append, toast `TAKEN · %s` | ✓ | 1 |
| `sign_log(station)` | bool | §9.4 (paper economy) | ✓ | 1 |
| `set_ui_scale(v)` | — | clamp 0.8..1.6; `ui_scale_changed.emit`; save_settings | | 1 |
| `set_night(on)` | — | §9.5 (day advance) | ✓ | 1 |
| `set_captions(on)` / `set_assist(on)` | — | save_settings | | 1 each |
| `register_station(id, pos)` | — | `station_points[id] = pos + (0,0.5,1.2)` | | 1 |
| `rebind(action, keycode, persist=true)` | — | §6 | | 1 |
| `pick_daily(id, take)` | — | remove from `dailies` by id; `carried_id/take`; toast `CARRYING · SCENE 4 TAKE %d. The degausser is in the climate room.` | ✓ | 1 |
| `paper_for(station)` | int | 99 in MATINEE | | 1 |
| `objective_text()` | String | the HUD objective ladder (DEMO → finale → decision → run_complete∧day≥3 → night → day 1 chain → day≥3 → default) | | 1 |
| `mint_shortcut_daily()` | — | `daily_seq+=1; dailies.append({id, take:-1}); daily_added.emit` | ✓ | 1 |
| `mark_presigned()` | — | `presigned_seen=true`; append the TOMORROW signature; `log_signed.emit("S4", paper_for("S4"))` | ✓ | 1 |
| `log_capture(name)` | — | append §4.2; `notify.emit("CAPTURED · %s · presentation kept")` (raw, not toast) | ✓ | 1 |
| `burn_daily()` | — | clears carried; `strikes -= 1` if >0 (two toasts by case); `sheet_changed.emit; daily_burned.emit` | ✓ | 1 |
| `all_cast_dead()` | bool | | | 1 |
| `add_wear(n)` | — | `seance_wear += n` | ✓ | 1 |
| `respawn_point()` | Vector3 | last signature's station point or default | | internal |
| `load_settings()` / `load_log()` | — | §6 / §3 | | `_ready` |

---

## 9 · DELTAS vs THE 0.8a C++ — THE 0.8b CHECKLIST

Findings from reading `RestorationState.h/.cpp` against the spec above.
Each is a box for 0.8b-2 (or its sub-boxes); none is optional.

- [ ] **9.1 `URestorationSaveGame` field types.** `Paper` int32 → `TMap<FString,int32>`;
      `Signatures` int32 → `TArray<FRestorationSignature{Station,Tape,Signed,bPresigned}>`;
      `Captures` int32 → `TArray<FRestorationCapture{Name,Tape,At}>`;
      `SeanceWear` int32 → float; `LelandAnswers` int32 → `TArray<int32>`.
      Defaults: `Mode = 1` (LATE_NIGHT), `CurrentTape = 1`.
- [ ] **9.2 Missing save keys (32).** Add every ✗ row of §2 to the USaveGame
      AND to both `SaveToSlot`/`LoadFromSlot` (today only `Version, Strikes,
      ItemsLost, DailySeq, Dailies` are actually written/read; the ⏸ rows are
      declared and ignored). Order and names as §2 so a JSON export (if ever
      wanted for the parser) matches the Godot log 1:1.
- [ ] **9.3 `Strike()` fidelity.** (a) `ItemsLost = Min(ItemsLost+1, 6)` caps at
      6; Godot caps at **7** (`if items_lost < ITEM_ORDER.size()`), and the
      lost item NAME (`ITEM_ORDER[items_lost]`) rides the `captured` signal —
      port the name and the 7. (b) full sheet = `strikes >= 4 OR mode ==
      ONE_TAKE`. (c) Godot saves in BOTH branches (full: before the emits;
      non-full: after the daily append) — C++ saves only on full. (d) Godot
      leaves `in_retake = true` until hud's retake presentation clears it;
      C++ resets it inline (documented stopgap "presentation owns this in
      P3") — remove the reset when the presentation lands. (e) emit
      `captured(take, full, lost, respawn_point())` on the non-full path;
      emit `daily_added(daily_seq, take)` before it.
- [ ] **9.4 `sign_log` / paper economy.** MATINEE bypasses paper entirely;
      otherwise `paper_for(station) <= 0` → if `harriet_slip` consume it (toast
      `Signed. The hand on the slip is not yours, and the log accepts it
      anyway.`) and sign anyway, else `log_refused` and return false; else
      decrement. `_sign_finish`: append §4.1, save, `Sfx.tick()`, `demo_mark
      ("s1_signed")` on S1, `log_signed(station, remaining)`, then
      `noise_event(respawn_point(), 4.0)` — signing is LOUD (4.0) at the
      station. The noise line is the web-law echo; do not drop it.
- [ ] **9.5 `set_night` day advance.** `is_night = on`; on FALSE: `day += 1;
      current_tape = min(day, 5)`; toast `MORNING · Day %d · Tape %d. The
      building pretends nothing happened.`; `day >= 3 and not run_complete` →
      `run_complete = true` + the PROTOTYPE COMPLETE toast. On TRUE: toast
      `NIGHT · the building belongs to the schedule.` Then save, then
      `night_changed.emit(on)` (signal AFTER save). This replaces the
      `bTestForceNight` scaffold in ARundown.
- [ ] **9.6 Live fields missing** from `URestorationState` (§5 ✗ rows):
      `StationPoints`, `CoverageLabel`, `bScreeningActive`, `MapPoints`,
      `bHarrietSlip`, `bFaderSelf`. Plus every saved field that is also live
      (all of §2) as the subsystem's working copy.
- [ ] **9.7 Delegates missing** (§7 ✗ rows, 18 of 20). Keep `night_changed`,
      `run_ended`, `pause_requested`, `demo_ended` externally broadcastable.
- [ ] **9.8 `LoadFromSlot` semantics.** Implement §3.2/§3.3 (forward-default,
      paper MERGE) and §3.4 (a `< 16` load must immediately re-save). Add the
      DEMO whitelist (§3.5) behind a build-config bool. Add `ResetNewGame`
      with the exact §3.6 exclusion set and the `ng_relic` computation.
- [ ] **9.9 Settings** → `URestorationUserSettings : UGameUserSettings` with
      the §6 keys and clamps; `Glyphs()` reads live Enhanced Input mappings
      so toasts keep carrying real binding glyphs.
- [ ] **9.10 Verification for 0.8b-2** (extend `ue/pyscripts/test_state_af.py`
      or add `test_state_save.py`): round-trip a save with EVERY §2 key set to
      a non-default value and assert equality on reload; load a v15-shaped
      slot and assert the re-save + MIGRATED log line; strike four times and
      assert `items_lost == 4`, `strikes == 0`, `run_ended` once; strike
      seven+ times across runs and assert `items_lost` stops at 7.

---

Extraction method (cloud unit 0.8b-spec): a scratch script parsed
`_save_dict`, `load_log`, the `var` declarations, `reset_new_game`, the DEMO
whitelist, `signal` and `func` lines from game_state.gd and printed the
tables; writer/reader columns come from `grep GameState.<field>` across
`scripts/*.gd`. Re-run the same extraction against the file before trusting
this document past commit f79877c — if `SAVE_VERSION` moves, this file is
stale by definition.
