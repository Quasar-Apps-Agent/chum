# PORT NOTES · STATE — the v16 save schema + game_state.gd inventory (unit 0.8b-spec)

**Source of truth:** `scripts/game_state.gd` (autoload `GameState`, 777 lines,
`SAVE_VERSION := 16`) at repo commit 5296190. THE CODE IS THE INTENT
(PORT-BRIEF.md). This file transcribes it; it does not redesign it. Where
this file and the GDScript disagree, the GDScript wins and this file is a bug.

**Target (migration map, STATE row):** `URestorationState`
(UGameInstanceSubsystem) + `URestorationSaveGame` (USaveGame) replacing the
JSON transmitter log; signals → multicast delegates with the same names.
**Must not change (UE5-MIGRATION-MAP "WHAT MUST NOT CHANGE"):** the save's
semantic fields, their defaults, the migration announcements, every knob
number below.

**Tripwire:** `python3 tools/check_port_notes_state.py` asserts this file
still names every save key / var / signal / public func in `game_state.gd`
(plan rule 4b — tracker and spec edits are code). Run it after touching
either file.

Contents: §1 the save file · §2 the v16 schema (55 keys) · §3 fields that
are NOT in the save · §4 signals · §5 public API · §6 constants & numbers ·
§7 gap audit of the 0.8a C++ skeleton · §8 the 0.8b checklist.

---

## 1 · THE SAVE FILE (canon: saving is signing a log station)

| | Godot reference | UE home |
|---|---|---|
| Path | `user://transmitter_log.json` (`SAVE_PATH`) | slot `"restoration"`, user index 0 (0.8a: `SaveToSlot/LoadFromSlot`) |
| Format | one JSON object, tab-indented, keys sorted by JSON.stringify | `URestorationSaveGame` UPROPERTYs, names mirror the keys 1:1 |
| Written by | `save_log()` — called by EVERY mutator in game_state.gd AND directly by 18 outside scripts after they poke fields themselves (see §5, "external save_log callers") | one `SaveToSlot()`; expose it, because outside systems will call it |
| Read by | `load_log()` in `_ready()` — every key via `data.get(key, default)`; scalars coerced `int()/bool()/float()/str()`; arrays replaced only if `typeof == TYPE_ARRAY`; `paper` MERGED key-by-key into the default dict (never replaced) | `LoadFromSlot()` at GameInstance init |
| Version | `"version": 16`; missing key reads as **1** | `Version` int32; default forward |
| Older save | fields default forward; **re-saved immediately** (`save_log()`) then a deferred `notify("LOG MIGRATED · format v%d to v%d. Nothing was lost.")` | same two acts: rewrite the slot, then the toast text verbatim |
| Newer save | read anyway; deferred `notify("LOG FROM A NEWER BUILD · v%d read by v%d. Proceed gently.")` | same |
| DEMO build (`DEMO := false`, flip for Tape 1) | `save_log()` ERASES these keys before writing: decision, assets, leland_answers, lockdown_done, finale_done, ending_reached, lie_pending, seance_wear, has_fire_tape, fire_tape_watched, dock_done, crate_opened, presigned_seen, cascade_done, casualties. `reset_new_game` uses `paper = {"S1":3,"S5":3}` in DEMO | a `bDemo` build flag with the same erase list |

A real v16 save (fresh Day 1, night tripped, coverage counters live) is
archived at `docs/telemetry/first-boot/transmitter_log.json` — use it as the
round-trip fixture for the UE test.

---

## 2 · THE v16 `_save_dict` SCHEMA — **55 keys**

Types are the JSON types as written; "Godot var" is the backing field when
the key name differs. Defaults are the `load_log` fallbacks (which equal the
var initializers). "0.8a" = state of `URestorationSaveGame` today: ✅ correct,
⚠️ present but wrong type/default, ❌ missing.

### 2.1 Run identity & economy

| key | type | default | Godot var / notes | 0.8a |
|---|---|---|---|---|
| `version` | int | 16 (missing → 1) | `SAVE_VERSION` | ✅ |
| `mode` | int (enum) | 1 = LATE_NIGHT | `mode`; `Mode {MATINEE=0, LATE_NIGHT=1, ONE_TAKE=2}`. MATINEE: `paper_for()` returns 99 (unlimited, not stored). ONE_TAKE: any capture ends the run | ⚠️ default 0 (MATINEE) |
| `tbc` | bool | false | `tbc_enabled` (time-base corrector toggle; `set_tbc` does NOT save) | ✅ |
| `tape` | int | 1 | `current_tape` = `min(day, 5)`, recomputed each morning | ⚠️ default 0 |
| `paper` | object {station: int} | `{"S1":3,"S2":3,"S3":3,"S4":3,"S5":3}` | `paper` — lines of paper left per log station (Late Night: 3 per tape). Loaded by MERGE: unknown stations survive, missing ones keep 3 | ⚠️ int32 — must be a map |
| `signatures` | array of records | `[]` | `{station:"S1".."S5", tape:int, signed:<datetime string>}`; the presigned S4 entry is `{station:"S4", tape, signed:"TOMORROW", presigned:true}`. Last entry's station drives `respawn_point()` | ⚠️ int32 count — must be TArray<struct> |
| `captures` | array of records | `[]` | `{name:String, tape:int, at:<datetime string>}` from `log_capture()` (bench presentations kept) | ⚠️ int32 count — must be TArray<struct> |
| `strikes` | int | 0 | `strikes` — the sheet; 4 = full (run ends, resets to 0); `burn_daily` decrements | ✅ |
| `items_lost` | int | 0 | `items_lost` — index into `ITEM_ORDER` (7 items); +1 per strike while `< 7`; A19 fires at ≥7; NG+ relic = `ITEM_ORDER[items_lost-1]` | ✅ (but see §7: cap) |
| `day` | int | 1 | `day` — +1 each `set_night(false)`; Day ≥3 unlocks the ledger | ✅ |
| `keys` | array of String | `[]` | `keys` — key ids: `"EDITH"`, `"TRAINING"`, `"QUIET ROOM"` (KeyItem export default `"KEY"`) | ✅ |
| `pt` | int | 0 | `pt` — PRODUCER TRACK points (`add_pt(10)` / `add_pt(5)` from the screening) | ❌ |
| `dailies` | array of records | `[]` | `{id:int, take:int}`; `take == -1` = shortcut daily minted by `mint_shortcut_daily()` (rejected edit) | ✅ (FRestorationDaily) |
| `daily_seq` | int | 0 | `daily_seq` — monotonic id source, never reused | ✅ |
| `carried_id` | int | -1 | `carried_id` — daily in hand (−1 none) | ❌ |
| `carried_take` | int | 0 | `carried_take` | ❌ |

### 2.2 Story flags — Days 1–2 (film, screening, signals)

| key | type | default | Godot var / notes | 0.8a |
|---|---|---|---|---|
| `film_watched` | bool | false | `film_watched` — training film seen (film_cabinet) | ✅ |
| `signals_known` | array of String | `[]` | `signals_known` — the show signals: SIX from the film `"YOU'RE ON","CUT","STRETCH","WRAP IT UP","THIRTY SECONDS","ON TIME"` + the SEVENTH `"HOLD YOUR APPLAUSE"` (harriet_note, only after Harriet is dead). `add_show_signal` does NOT save by itself | ❌ |
| `screening_done` | bool | false | `screening_done` — rec-room mini-screening | ✅ |
| `run_complete` | bool | false | `run_complete` — set the morning `day >= 3` ("PROTOTYPE COMPLETE") | ✅ |

### 2.3 Story flags — the fire tape, the séance, the dock, the ledger

| key | type | default | Godot var / notes | 0.8a |
|---|---|---|---|---|
| `has_fire_tape` | bool | false | `has_fire_tape` | ✅ |
| `fire_tape_watched` | bool | false | `fire_tape_watched` | ✅ |
| `seance_wear` | **float** | 0.0 | `seance_wear` — Leland substrate wear %, `add_wear(n)`; >70 with 5 answers = the reading | ⚠️ int32 — must be float |
| `leland_answers` | array of int | `[]` | `leland_answers` — frame indices from seance_dock `ANSWERS`; 5 expected, no dupes | ⚠️ int32 — must be TArray<int32> |
| `presigned_seen` | bool | false | `presigned_seen` — the S4 "TOMORROW" signature was found | ❌ |
| `dock_done` | bool | false | `dock_done` — scene-dock task complete | ❌ |
| `assets` | array of String | `[]` | `assets` — the four premiere assets: `"CART"`, `"SCRIPT"`, `"CARD"`, `"VERSE"`; `gain_asset` toasts "(n of 4)" | ❌ |
| `decision` | String | `""` | `decision` — ledger choice `"AUTHENTICATE" | "DESTROY" | "PERFORM"` (empty = not yet); `start_finale()` emits it | ❌ |
| `lockdown_done` | bool | false | `lockdown_done` | ✅ |
| `finale_done` | bool | false | `finale_done` — set by `mark_ending` | ✅ |
| `ending_reached` | String | `""` | `ending_reached` — one of: THE BURN · THE NEW PRODUCER · SIGN-OFF · LELAND CLOSES · SIGN-OFF · RITA CLOSES · THE COMPLETED SIGN-OFF · A ONE-WOMAN SHOW · DEAD AIR | ✅ |
| `lie_pending` | bool | false | `lie_pending` — THE ONE INTERFACE LIE armed for the title screen (title.gd consumes + clears it). **Survives `reset_new_game`** | ❌ |
| `vess_insight` | bool | false | `vess_insight` | ❌ |
| `vess_credited` | bool | false | `vess_credited` — Vess credited → V1 casualty path | ❌ |
| `ng_relic` | String | `""` | `ng_relic` — NG+ carry: `ITEM_ORDER[min(items_lost,7)-1]` if the previous run ended with `finale_done && items_lost > 0`; world_builder places it | ❌ |
| `crate_opened` | bool | false | `crate_opened` — the impossible crate | ❌ |
| `night_tripped` | bool | false | `night_tripped` — first night-trip beat consumed | ❌ |

### 2.4 Coverage, accessibility-in-save, cascade, readables

| key | type | default | Godot var / notes | 0.8a |
|---|---|---|---|---|
| `cov_monitor` | float | 0.0 | `cov_monitor` — coverage_director seconds watching monitors | ❌ |
| `cov_move` | float | 0.0 | `cov_move` — seconds moving | ❌ |
| `cov_still` | float | 0.0 | `cov_still` — seconds still. The three drive `coverage_label` (AUDIENCE default) | ❌ |
| `photo_safe` | bool | false | `photo_safe` — photosensitivity-safe mode. Lives in the SAVE, not settings.cfg (quirk: preserve). **Survives `reset_new_game`** | ❌ |
| `cascade_done` | bool | false | `cascade_done` — patch-bay cascade resolved | ❌ |
| `read_props` | array of String | `[]` | `read_props` — document ids `"D01".."D10"` (readable_prop default `"D00"`); `mark_read` toasts "(n of 10 documents)" | ❌ |

### 2.5 After-fire layer & the casualty arc

| key | type | default | Godot var / notes | 0.8a |
|---|---|---|---|---|
| `af_active` | bool | false | `af_active` — the After-Fire body is live. **Survives `reset_new_game`** | ❌ (live field only) |
| `af_taught` | bool | false | `af_taught` — the 4s cool has been taught once. **Survives `reset_new_game`** | ❌ (live field only) |
| `casualties` | array of records | `[]` | `{who, cause, line, day:int}`; `who ∈ "MERLE","VESS","HARRIET","FLOOR MANAGER","LELAND"`; `cause` ids seen: M1 · THE SECOND VIEWING, V1 · CREDITED THEREFORE CAST, V2 · THE UNCREDITED FIX, H1 · CONTINUITY, H2 · THE SPLICE, F1 · THE FADER, F2 · THE UNLISTED CAMERA, L1 · THE SIXTH QUESTION, L2 · THE READING; `line` = epitaph. One entry per `who` (`mark_casualty` is idempotent) | ❌ |
| `merle_offered` | bool | false | `merle_offered` — fire_tape_dock beat | ❌ |
| `signoff_completed` | bool | false | `signoff_completed`. **Survives `reset_new_game`** | ❌ |
| `row_casualties` | int | 0 | `row_casualties` — premiere row deaths counter | ❌ |
| `h2_pending` | bool | false | `h2_pending` — Harriet's splice armed (rejected_edit → harriet) | ❌ |
| `deadroom_seen` | bool | false | `deadroom_seen` — HUD has shown the dead-room line. **Survives `reset_new_game`** | ❌ |
| `rejected_seen` | bool | false | `rejected_seen` — the rejected edit found | ❌ |
| `glimpse_seen` | bool | false | `glimpse_seen` — THE ONCE-EVER SIGHT consumed (THE-LAWS §3: at most once per save; never referenced again by any system) | ❌ |
| `merle_1974` | bool | false | `merle_1974` | ❌ |
| `fire_unsealed` | bool | false | `fire_unsealed` — fire corridor unsealed (glimpse) | ❌ |

Key order in the file is JSON-stringify sorted; the transcription above is
`_save_dict` declaration order, grouped.

---

## 3 · WHAT IS NOT IN THE SAVE (and what survives a new game)

### 3.1 Transient runtime fields (public on the autoload, rebuilt every boot)

| var | type | default | who writes / reads |
|---|---|---|---|
| `is_night` | bool | false | `set_night()`; read by rundown (8 sites), bed, cascade, coverage, floor manager, glimpse, merle, lockdown, night_trip, noise_tracker, soak_runner. NOT saved: a loaded game is always morning of `day` |
| `in_retake` | bool | false | set in `strike()`, cleared by **hud.gd** after the retake presentation (`GameState.in_retake = false`) — the presentation owns the clear |
| `station_points` | Dictionary {id: Vector3} | `{}` | `register_station(id, pos)` from world_builder (S1–S5); offset `+ (0, 0.5, 1.2)` |
| `coverage_label` | String | `"AUDIENCE"` | coverage_director profile(); hud reads |
| `premiere_live` | bool | false | live_production sets; rundown/cascade/glimpse/floor_manager/night_trip/noise_tracker gate on it; `mark_ending` clears |
| `screening_active` | bool | false | screening_event; merle reads |
| `map_points` | Array of `[id, Vector2(x, z)]` | `[]` | world_builder appends; map_view draws |
| `cascade_active` | bool | false | cascade.gd; door.gd, liveness_check, rundown read |
| `recording` | bool | false | capture_bench drives; rundown (4) and hud read — the AF tally contract |
| `recording_left` | float | 0.0 | capture_bench; hud |
| `crossing` | bool | false | live_production; rundown |
| `crossing_caught` | bool | false | rundown sets; live_production reads |
| `harriet_slip` | bool | false | harriet.gd arms; consumed by `sign_log()` when paper is out |
| `fader_self` | bool | false | live_production; hud |
| `mouse_sens` | float | 1.0 | settings.cfg `[input] sensitivity`, clamped 0.2–3.0 |
| `ui_scale` | float | 1.0 | settings.cfg `[access] ui_scale`, clamped 0.8–1.6 by `set_ui_scale` |
| `captions_on` | bool | false | settings.cfg `[access] captions` |
| `assist_on` | bool | false | settings.cfg `[access] assist` |
| `_glyph_re` | Dictionary | `{}` | private RegEx cache for `glyphs()` |
| `_demo_t0` | int | 0 | private demo-funnel epoch (ticks ms) |

Settings file (`user://settings.cfg` → `GConfig`/`UGameUserSettings` in UE):
sections `[audio] master` (linear 0–1 → bus 0 dB), `[input] sensitivity`,
`[access] ui_scale|captions|assist`, `[keys] <action>=physical_keycode` for
`REMAP_ACTIONS`, `[video] fullscreen`. Saved by `save_settings()`, read by
`load_settings()` before `load_log()`.

### 3.2 Saved fields that `reset_new_game()` does NOT reset (they carry across runs — intentional; do not "fix")

`mode`, `tbc_enabled`, `lie_pending` (the interface lie fires on the next
title screen), `photo_safe` (accessibility persists), `af_active`,
`af_taught` (the fire happened; the body stays fired), `signoff_completed`,
`deadroom_seen`. Plus `ng_relic`, which reset_new_game SETS from the dying
run. Everything else in §2 returns to its default; `paper` returns to 3s
(S1+S5 only in DEMO). Transients reset too: `is_night`, `in_retake`,
`premiere_live`, `cascade_active`, `harriet_slip`.

---

## 4 · SIGNALS (20) → multicast delegates, same names

| signal | params | emitted by (in game_state.gd) | listeners outside |
|---|---|---|---|
| `tbc_changed` | (enabled: bool) | `set_tbc` | bench_tv, hud |
| `log_signed` | (station: String, remaining: int) | `_sign_finish`, `mark_presigned` | achievements, hud |
| `log_refused` | (station: String) | `sign_log` when paper is out (and no slip) | hud |
| `notify` | (text: String) | `toast`, `log_capture`, migration announcements | hud (the toast rail) |
| `capture_status` | (text: String) | `set_capture_status[_raw]` | hud |
| `sheet_changed` | (count: int) | `strike`, `burn_daily` | dresser, hud |
| `night_changed` | (now_night: bool) | `set_night` | achievements, floor_manager, live_production, rundown, soak_runner, world_builder |
| `captured` | (take: int, sheet_full: bool, lost_item: String, respawn: Vector3) | `strike` (non-full sheet) | hud (runs the retake presentation, repositions, clears `in_retake`) |
| `daily_added` | (id: int, take: int) | `strike`, `mint_shortcut_daily` | dailies_manager |
| `daily_burned` | () | `burn_daily` | coverage_director |
| `run_ended` | (take: int) | `strike` (full sheet or ONE_TAKE) | achievements, hud, rundown |
| `finale_started` | (decision: String) | `start_finale` | hud |
| `noise_event` | (pos: Vector3, loudness: float) | `noise`, `_sign_finish` (4.0 at the respawn point) | rundown (→ `ReportNoise`, ported in 0.7) |
| `photo_changed` | (on: bool) | `set_photo_safe` | bench_tv |
| `blackout_changed` | (alpha: float) | `set_blackout` | hud |
| `ui_scale_changed` | (scale: float) | `set_ui_scale` | hud |
| `caption` | (text: String) | `show_caption` (only if `captions_on`) | hud |
| `pause_requested` | () | (emitted by callers: player) | hud, player |
| `demo_ended` | () | (emitted by callers: capture_bench/hud in DEMO) | capture_bench, hud |
| `ending_marked` | (ending_name: String) | `mark_ending` | world_builder |

0.8a has only `OnRunEnded` and `OnSheetChanged`. Delegate naming: `FOn<Name>`
per the two that exist.

---

## 5 · PUBLIC API (functions, with side effects)

"saves" = calls `save_log()`. Toast strings are canon UI text: port verbatim
(they are also in `Data/GameText.csv` where localized).

### 5.1 Paper & the log stations
| func | effect |
|---|---|
| `paper_for(station) -> int` | 99 in MATINEE; else `paper[station]` (0 if unknown) |
| `sign_log(station) -> bool` | Non-MATINEE: if no paper → if `harriet_slip` consume it + toast "Signed. The hand on the slip is not yours, and the log accepts it anyway." else emit `log_refused`, return false; else `paper[station] -= 1`. Then `_sign_finish`: append signature, **saves**, `Sfx.tick()`, `demo_mark("s1_signed")` if S1, emit `log_signed(station, paper_for)`, emit `noise_event(respawn_point(), 4.0)`. Returns true |
| `mark_presigned()` | `presigned_seen = true`; append the S4 TOMORROW/presigned record; **saves**; emit `log_signed("S4", …)` |
| `register_station(id, pos)` | `station_points[id] = pos + (0, 0.5, 1.2)` |
| `respawn_point() -> Vector3` | last signature's station point if registered, else `(0, 1.0, 2.5)` |

### 5.2 The sheet, strikes, dailies (retake economy)
| func | effect |
|---|---|
| `strike(player)` | guard `in_retake`; set it; `strikes += 1`; `take = strikes`; lose next `ITEM_ORDER` item if `items_lost < 7`; `full = strikes >= 4 or mode == ONE_TAKE`. Full: `strikes = 0`, **saves**, `sheet_changed`, `run_ended(take)`, return (in_retake stays set). Else: `daily_seq += 1`, append `{id, take}`, `daily_added`, **saves**, `sheet_changed`, `captured(take, false, lost, respawn_point())` |
| `pick_daily(id, take)` | remove from `dailies`; `carried_id/carried_take`; **saves**; toast "CARRYING · SCENE 4 TAKE %d. The degausser is in the climate room." |
| `burn_daily()` | clear carried; if `strikes > 0` decrement + toast "BURNED · TAKE %d. Her name fades from the line. Its read on you resets." else toast "BURNED · TAKE %d. The sheet was already clean. The canister burns anyway."; **saves**; `sheet_changed`, `daily_burned` |
| `mint_shortcut_daily()` | `daily_seq += 1`; append `{id, take:-1}`; `daily_added(id, -1)`; **saves** |
| `log_capture(name)` | append `{name, tape, at}`; **saves**; notify "CAPTURED · %s · presentation kept" |

### 5.3 Day/night, modes, finale
| func | effect |
|---|---|
| `set_night(on)` | `is_night = on`. Off: `day += 1`, `current_tape = min(day, 5)`, toast "MORNING · Day %d · Tape %d. The building pretends nothing happened."; if `day >= 3 and not run_complete`: set it, toast "PROTOTYPE COMPLETE · the loop is proven. The rest is production." On: toast "NIGHT · the building belongs to the schedule." Then **saves**, `night_changed(on)` |
| `set_mode(m)` | no-op if same; **saves**; toast "MODE · %s" (MATINEE/LATE NIGHT/ONE TAKE); ONE_TAKE adds "ONE TAKE · any capture ends the run. (Prototype honors sheet rules until run flow exists.)" |
| `set_tbc(on)` | `tbc_enabled`; emit `tbc_changed` (no save) |
| `start_finale()` | emit `finale_started(decision)` |
| `mark_ending(name, lie=false)` | `premiere_live = false; finale_done = true; ending_reached = name`; `ending_marked(name)`; `Achievements.on_ending(name)`; if lie → `lie_pending = true`; **saves** |
| `reset_new_game()` | `demo_mark("started")`; compute `ng_relic` (§2.3); reset per §3.2; **saves** |
| `objective_text() -> String` | the HUD objective line — a priority ladder over DEMO/finale/decision/run_complete/night/day 1 steps/day≥3; port the exact strings from lines 687–710 |

### 5.4 Inventory, lore, assets
| func | effect |
|---|---|
| `has_key(id) -> bool` / `take_key(id, display)` | dupe → toast "You already carry %s."; else append, **saves**, toast "TAKEN · %s" |
| `gain_asset(id, display)` | dupe → return; append; **saves**; toast "ASSET BANKED · %s (%d of 4)"; at 4: "All four. The finale has everything it needs, when night falls." |
| `mark_read(id)` | dupe → return; append; **saves**; toast "READ · filed to memory. (%d of 10 documents)" |
| `add_show_signal(sig)` | append if new (no save — callers save) |
| `add_wear(n)` / `add_pt(n)` | accumulate; **saves** |
| `set_photo_safe(on)` | set; **saves**; `photo_changed(on)`; toast "PHOTOSENSITIVITY-SAFE MODE · ON · bands and flicker suppressed" / "… · OFF" |

### 5.5 The casualty ledger
| func | effect |
|---|---|
| `mark_casualty(who, cause, epitaph)` | idempotent per `who`; append `{who, cause, line, day}`; **saves**; toast "THE LEDGER TAKES IT DOWN." |
| `is_dead(who) -> bool` · `cause_of(who) -> String` · `all_cast_dead() -> bool` (MERLE ∧ VESS ∧ HARRIET ∧ FLOOR MANAGER — Leland not counted) | queries |
| `in_dead_room(pos) -> bool` | `abs(x-19) <= 2.2 and abs(z-2.5) <= 2.7` (Godot meters; ported 0.8a as 1900/220 · 250/270 uu on X/Y) |

### 5.6 UI plumbing, settings, input
| func | effect |
|---|---|
| `toast(text)` | `notify.emit(glyphs(tr(text)))` — 40+ callers across the codebase |
| `glyphs(text) -> String` | word-boundary replace of `GLYPH_MAP` tokens E/SPACE/Q/T/M with the live key name (upper) |
| `set_capture_status(text)` / `set_capture_status_raw(text)` | emit `capture_status` (glyphed / raw) |
| `show_caption(text)` | emit `caption(tr(text))` only if `captions_on` |
| `set_blackout(alpha)` · `noise(pos, loudness)` | pure emitters |
| `load_settings()` / `save_settings()` | §3.1 settings file |
| `set_ui_scale(v)` (clamp 0.8–1.6, emit, save settings) · `set_assist(on)` · `set_captions(on)` | settings setters |
| `rebind(action, physical_keycode, persist=true)` | refuses a key already bound to another `REMAP_ACTIONS` entry with toast "KEY IN USE · that key already answers to %s."; else replaces the key event; saves settings if persist |
| `key_name(action) -> String` | key string of the bound physical key or "?" |
| `demo_mark(event)` | DEMO only: append `[min %.1f] %s` to `user://demo_funnel.txt` since first mark |
| `save_log()` / `load_log()` | §1 |

Private (`_`-prefixed): `_ready`, `_sign_finish`, `_save_dict`,
`_signed_station`, `_announce_migration`, `_announce_newer`.

**External `save_log()` callers** (systems that mutate GameState fields
directly and then save — the UE port needs public write access or setters
for exactly these fields): cascade (cascade_done), credit_entry
(vess_credited), decision_ledger (decision), dock_task (dock_done),
film_cabinet (film_watched), fire_tape_dock (fire_tape_watched,
merle_offered), fire_tape_pickup (has_fire_tape), glimpse (glimpse_seen,
fire_unsealed), harriet_note (signals_known), impossible_crate
(crate_opened), lockdown (lockdown_done), merle (merle_1974),
night_trip (night_tripped), rejected_edit (rejected_seen, h2_pending),
screening_event (screening_done), seance_dock (leland_answers), title
(lie_pending), vess_binder (vess_insight).

---

## 6 · CONSTANTS & NUMBERS (every one is canon)

| constant | value |
|---|---|
| `SAVE_VERSION` | 16 |
| `SAVE_PATH` / `SETTINGS_PATH` | `user://transmitter_log.json` / `user://settings.cfg` |
| `DEMO` | false (Tape 1 build flips it) |
| `Mode` | MATINEE=0 · LATE_NIGHT=1 · ONE_TAKE=2 (default LATE_NIGHT) |
| paper per station per tape (Late Night) | 3; MATINEE reads 99 |
| full sheet | `strikes >= 4` (or any strike in ONE_TAKE) |
| `ITEM_ORDER` (7) | WATCH, PEN, PHOTOGRAPH, LIGHTER, COMPACT, KEYS, LOUPE |
| `GLYPH_MAP` | E→interact, SPACE→respond, Q→improvise, T→toggle_tbc, M→map |
| `REMAP_ACTIONS` | interact, respond, improvise, toggle_tbc, map |
| tape cap | `current_tape = min(day, 5)` |
| ledger unlock / run_complete | `day >= 3` |
| dead room rect | `|x−19| ≤ 2.2 ∧ |z−2.5| ≤ 2.7` m |
| default respawn | `(0, 1.0, 2.5)` m; station offset `(0, 0.5, 1.2)` |
| sign-log noise | loudness 4.0 at the respawn point |
| séance thresholds | 5 answers; wear > 70.0 = the reading, ≤ 70.0 = the clean close |
| documents / assets totals | 10 (`D01`–`D10`) / 4 (CART, SCRIPT, CARD, VERSE) |
| producer track | +10 / +5 per screening beat |
| clamps | mouse_sens 0.2–3.0 · ui_scale 0.8–1.6 |

---

## 7 · GAP AUDIT — 0.8a `RestorationState.h/.cpp` vs this schema

Findings against the C++ that exists today (all are 0.8b work, none are
0.8a regressions — 0.8a scoped itself to the brain fields + a skeleton):

1. **Wrong types (4):** `Paper` int32 → `TMap<FString,int32>`; `Signatures`
   int32 → `TArray<FRestorationSignature>` {Station, Tape, Signed(FString),
   bPresigned}; `Captures` int32 → `TArray<FRestorationCapture>` {Name, Tape,
   At}; `SeanceWear` int32 → float; `LelandAnswers` int32 → `TArray<int32>`.
2. **Wrong defaults (2):** `Mode` 0 → 1 (LATE_NIGHT); `CurrentTape` 0 → 1.
3. **Missing keys (32 of 55):** pt, carried_id, carried_take, signals_known,
   presigned_seen, dock_done, assets, decision, lie_pending, vess_insight,
   vess_credited, ng_relic, crate_opened, night_tripped, cov_monitor,
   cov_move, cov_still, photo_safe, cascade_done, read_props, af_active,
   af_taught, casualties, merle_offered, signoff_completed, row_casualties,
   h2_pending, deadroom_seen, rejected_seen, glimpse_seen, merle_1974,
   fire_unsealed.
4. **`SaveToSlot` writes 5 fields, `LoadFromSlot` reads 4** — everything
   else in the SaveGame is dead weight until wired. The round-trip test
   (`test_state_af.py`, `bTestSaveRoundtrip`) only proves strikes/dailies.
5. **`Strike()` deltas:** `ItemsLost` capped at 6 — Godot's guard is
   `items_lost < ITEM_ORDER.size()` i.e. cap **7** (A19 achievement needs
   ≥7); lost-item NAME not surfaced (`captured` delegate absent entirely);
   `mode == ONE_TAKE` full-sheet branch absent; `bInRetake` is cleared inside
   `Strike()` (comment says "keep the brain live") whereas Godot leaves it
   set until hud's retake presentation clears it — acceptable as a 0.8a
   scaffold, but the P3 presentation must own the clear, and the brain must
   not read `bInRetake` as "safe to strike again" meanwhile.
6. **Migration:** an older save must be **re-written immediately** and the
   toast text emitted through `notify` (UE only logs today). Missing
   `Version` reads as 1 in Godot; UE's default is 16 — a fresh SaveGame
   object should not be mistaken for a current one (initialize `Version=0`
   or `1` on the class and stamp 16 in `SaveToSlot`).
7. **Delegates:** 2 of 20 exist. `noise_event` is already routed into
   `ARundown::ReportNoise` (0.7) — keep that wiring when the delegate lands.
8. **Live fields present but not persisted** (`bAfActive`, `bAfTaught`) are
   saved keys in Godot AND survive new game — the fire is permanent.
9. Naming: UE properties may be PascalCase, but the **save key semantics** are
   the contract; keep a comment per property with its Godot key so
   `check_port_notes_state.py` (or a future UE-side twin) can diff them.

---

## 8 · THE 0.8b IMPLEMENTATION CHECKLIST (ordered; each step verifiable)

- [ ] **8.1 SaveGame to full v16**: add the 32 missing keys, fix the 4 types
      and 2 defaults, add `FRestorationSignature`, `FRestorationCapture`,
      `FRestorationCasualty` {Who, Cause, Line, Day} USTRUCTs. `SaveToSlot` /
      `LoadFromSlot` cover all 55. Verify: round-trip of a state populated
      from `docs/telemetry/first-boot/transmitter_log.json` values (write a
      loader for that JSON in the test: it IS the fixture).
- [ ] **8.2 Live state = §2 + §3.1** on `URestorationState`, with the §3.2
      carry-over set and `ResetNewGame()` including the `ng_relic` rule.
- [ ] **8.3 Delegates (20)** per §4, same names; `Toast()`/`Glyphs()` →
      `OnNotify`; `ShowCaption` gated on captions.
- [ ] **8.4 Paper economy + stations**: `PaperFor`, `SignLog` (with the
      Harriet slip branch), `MarkPresigned`, `RegisterStation`,
      `RespawnPoint`, the 4.0 noise on sign. Data: station ids from
      `Data/Stations.csv`.
- [ ] **8.5 Retake economy complete**: `Strike` per §5.2 verbatim (cap 7,
      ONE_TAKE, `OnCaptured` with lost item + respawn), `PickDaily`,
      `BurnDaily`, `MintShortcutDaily`, `LogCapture`; in_retake cleared by
      the presentation (P3), not by Strike.
- [ ] **8.6 Day/night driver**: `SetNight` per §5.3 replacing the 0.7/0.8a
      `bTestForceNight` scaffold — Rundown reads `bIsNight` from state only.
- [ ] **8.7 Modes + finale + ledger**: `SetMode`, `StartFinale`,
      `MarkEnding` (+ lie), `MarkCasualty`/`IsDead`/`CauseOf`/`AllCastDead`,
      `GainAsset`, `MarkRead`, `AddShowSignal`, `TakeKey`/`HasKey`,
      `AddWear`, `AddPt`, `SetPhotoSafe`, `ObjectiveText` (exact strings).
- [ ] **8.8 Settings** (§3.1 file) → `UGameUserSettings` subclass or GConfig
      section with the same keys/clamps; `Rebind` refusal rule + toast.
- [ ] **8.9 Migration**: Version<16 → rewrite + "LOG MIGRATED …" toast;
      >16 → "LOG FROM A NEWER BUILD …"; DEMO erase list behind a build flag.
- [ ] **8.10 Bench capture loop, retake presentation, Harriet freeze,
      screening + assist, pawn feel (3.1 m/s, crouch c045)** — the rest of
      the 0.8b box; each consumes the API above, none of them add save keys
      (if one does, bump SAVE_VERSION in BOTH implementations and this file).
- [ ] **8.11 Re-run `tools/check_port_notes_state.py`** and the UE
      round-trip; then tick 0.8b.
