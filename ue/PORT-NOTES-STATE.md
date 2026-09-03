# PORT NOTES · STATE — the v16 transmitter log and `game_state.gd`, transcribed

Unit 0.8b-spec [CLOUD-OK]. Source of truth: `scripts/game_state.gd` (777
lines, autoload `GameState`). The code is the spec: every field, default,
coercion, and signal below is read off the GDScript, not the prose docs.
This file is the implementation checklist for 0.8b-2 (`URestorationState`,
`URestorationSaveGame`). It is checked mechanically by
`tools/check_port_notes_state.py`, which parses the GDScript and asserts
that every save key, public var, signal, and method is named here.

Conventions used below:
- Godot `Vector3(x, y_up, z)` → UE `FVector(x*100, z*100, y*100)` (the
  stamping convention; see `InDeadRoom` in `RestorationState.h`).
- "reset" = touched by `reset_new_game()`. "DEMO-erased" = stripped from
  the file by `save_log()` when `const DEMO := true`.
- "0.8a" = already present in `RestorationState.h` as of Commit 082.
  ⚠ marks a divergence between 0.8a's skeleton and the GDScript that
  0.8b-2 must correct before the field is considered ported.

---

## 1 · THE FILE

| item | value |
|---|---|
| path | `user://transmitter_log.json` (`SAVE_PATH`) |
| format | `JSON.stringify(dict, "\t")` — tab-indented JSON object, one flat level (nested arrays of dicts for signatures/captures/dailies/casualties) |
| version | `SAVE_VERSION := 16` (`"version"` key) |
| written by | `save_log()` — called on every state mutation that matters (20 call sites inside game_state.gd, 20 external) |
| read by | `load_log()` in `_ready()` after `load_settings()` |
| missing file | `load_log()` returns silently; defaults stand |
| non-dict JSON | `load_log()` returns silently; defaults stand |
| `version < 16` | fields load with defaults for anything absent, `save_log()` rewrites immediately, then deferred toast `"LOG MIGRATED · format v%d to v%d. Nothing was lost."` |
| `version > 16` | loads anyway, deferred toast `"LOG FROM A NEWER BUILD · v%d read by v%d. Proceed gently."` |
| absent `version` | treated as v1 → migration path |
| UE home (0.8a) | `URestorationSaveGame` (USaveGame), slot `"restoration"`, `SaveToSlot`/`LoadFromSlot` on `URestorationState`. The migration-map law: SEMANTIC field names and defaults mirror 1:1; the byte container may be USaveGame rather than JSON. |

**Load coercion rules (apply per field, see §2 column "load"):**
- `int(data.get(k, d))`, `bool(...)`, `float(...)`, `str(...)` — the JSON
  value is coerced; a wrong-typed value coerces rather than errors.
- Arrays: `if typeof(v) == TYPE_ARRAY: field = v` — a non-array value is
  IGNORED and the default (empty array) stands.
- `paper`: MERGED, not replaced — `for k in p.keys(): paper[k] = int(p[k])`.
  Missing stations keep the default 3. (A DEMO save carrying only S1/S5
  loads into the full build with S2–S4 still at 3.)

---

## 2 · THE v16 SAVE SCHEMA — all 55 keys of `_save_dict()`, in file order

Columns: JSON key · GDScript var · type · default (fresh autoload) · load
coercion · reset by `reset_new_game()` · DEMO-erased · external writers
(scripts that assign the field directly, bypassing a method) · 0.8a status.

| # | key | var | type | default | load | reset | DEMO-erased | external writers | 0.8a |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `version` | `SAVE_VERSION` (const) | int | 16 | `int(..., 1)` | — | no | — | `Version=16` ✓ |
| 2 | `mode` | `mode` | int (enum `Mode`: 0 MATINEE, 1 LATE_NIGHT, 2 ONE_TAKE) | **1 (LATE_NIGHT)** | `int(..., Mode.LATE_NIGHT)` | **NOT reset** (mode survives NEW GAME) | no | — (via `set_mode`) | ⚠ `Mode=0` — default must be 1 |
| 3 | `tbc` | `tbc_enabled` | bool | false | `bool` | **NOT reset** | no | — (via `set_tbc`) | `Tbc` ✓ |
| 4 | `tape` | `current_tape` | int | 1 | `int(..., 1)` | → 1 | no | soak_runner.gd | ⚠ `CurrentTape=0` — default must be 1 |
| 5 | `paper` | `paper` | Dictionary String→int | `{"S1":3,"S2":3,"S3":3,"S4":3,"S5":3}` (DEMO reset: `{"S1":3,"S5":3}`) | merge, `int` per key | → default dict | no | — (via `sign_log`) | ⚠ `Paper` is `int32` — must be `TMap<FString,int32>` |
| 6 | `signatures` | `signatures` | Array of `{station:String, tape:int, signed:String(datetime or "TOMORROW"), presigned?:bool}` | `[]` | array-or-ignore | → `[]` | no | — | ⚠ `Signatures` is `int32` — must be `TArray<FRestorationSignature>` |
| 7 | `captures` | `captures` | Array of `{name:String, tape:int, at:String(datetime)}` | `[]` | array-or-ignore | → `[]` | no | — | ⚠ `Captures` is `int32` — must be `TArray<FRestorationCapture>` |
| 8 | `strikes` | `strikes` | int | 0 | `int` | → 0 | no | — (via `strike`/`burn_daily`) | `Strikes` ✓ |
| 9 | `items_lost` | `items_lost` | int (0..7, index into `ITEM_ORDER`) | 0 | `int` | → 0 | no | — | ⚠ `ItemsLost` — `Strike()` clamps at 6; GDScript allows 7 (`< ITEM_ORDER.size()` = 7). Port `ITEM_ORDER` and lift the clamp |
| 10 | `day` | `day` | int | 1 | `int(..., 1)` | → 1 | no | soak_runner.gd | `Day=1` ✓ |
| 11 | `keys` | `keys` | Array of String (key ids) | `[]` | array-or-ignore | → `[]` | no | — (via `take_key`) | `Keys` ✓ |
| 12 | `pt` | `pt` | int (points; `add_pt`) | 0 | `int` | → 0 | no | — | missing |
| 13 | `dailies` | `dailies` | Array of `{id:int, take:int}` (take −1 = shortcut daily) | `[]` | array-or-ignore | → `[]` | no | — | `Dailies` (`FRestorationDaily`) ✓ |
| 14 | `daily_seq` | `daily_seq` | int | 0 | `int` | → 0 | no | — | `DailySeq` ✓ |
| 15 | `carried_id` | `carried_id` | int (−1 = none) | −1 | `int(..., -1)` | → −1 | no | — | missing |
| 16 | `carried_take` | `carried_take` | int | 0 | `int` | → 0 | no | — | missing |
| 17 | `film_watched` | `film_watched` | bool | false | `bool` | → false | no | film_cabinet.gd | `FilmWatched` ✓ |
| 18 | `signals_known` | `signals_known` | Array of String | `[]` | array-or-ignore | → `[]` | no | — (via `add_show_signal`) | missing |
| 19 | `screening_done` | `screening_done` | bool | false | `bool` | → false | no | screening_event.gd | `ScreeningDone` ✓ |
| 20 | `run_complete` | `run_complete` | bool | false | `bool` | → false | no | — (via `set_night`) | `RunComplete` ✓ |
| 21 | `has_fire_tape` | `has_fire_tape` | bool | false | `bool` | → false | **yes** | fire_tape_pickup.gd, seance_dock.gd | `HasFireTape` ✓ |
| 22 | `fire_tape_watched` | `fire_tape_watched` | bool | false | `bool` | → false | **yes** | fire_tape_dock.gd | `FireTapeWatched` ✓ |
| 23 | `seance_wear` | `seance_wear` | float | 0.0 | `float` | → 0.0 | **yes** | — (via `add_wear`) | ⚠ `SeanceWear` is `int32` — must be `float` |
| 24 | `leland_answers` | `leland_answers` | Array (answer records, shape owned by seance_dock.gd) | `[]` | array-or-ignore | → `[]` | **yes** | seance_dock.gd | ⚠ `LelandAnswers` is `int32` — must be an array |
| 25 | `presigned_seen` | `presigned_seen` | bool | false | `bool` | → false | **yes** | — (via `mark_presigned`) | missing |
| 26 | `dock_done` | `dock_done` | bool | false | `bool` | → false | **yes** | dock_task.gd | missing |
| 27 | `assets` | `assets` | Array of String (asset ids, max 4) | `[]` | array-or-ignore | → `[]` | **yes** | soak_runner.gd | missing |
| 28 | `decision` | `decision` | String ("" / AUTHENTICATE / DESTROY / PERFORM per `objective_text`) | "" | `str` | → "" | **yes** | decision_ledger.gd, soak_runner.gd | missing |
| 29 | `lockdown_done` | `lockdown_done` | bool | false | `bool` | → false | **yes** | lockdown.gd, soak_runner.gd | `LockdownDone` ✓ |
| 30 | `finale_done` | `finale_done` | bool | false | `bool` | → false | **yes** | — (via `mark_ending`) | `FinaleDone` ✓ |
| 31 | `ending_reached` | `ending_reached` | String | "" | `str` | → "" | **yes** | — (via `mark_ending`) | `EndingReached` ✓ |
| 32 | `lie_pending` | `lie_pending` | bool | false | `bool` | **NOT reset** (title.gd consumes it after NEW GAME) | **yes** | title.gd | missing |
| 33 | `vess_insight` | `vess_insight` | bool | false | `bool` | → false | no | vess_binder.gd | missing |
| 34 | `vess_credited` | `vess_credited` | bool | false | `bool` | → false | no | credit_entry.gd | missing |
| 35 | `ng_relic` | `ng_relic` | String (an `ITEM_ORDER` name or "") | "" | `str` | → computed: `ITEM_ORDER[min(items_lost,7)-1]` if `finale_done and items_lost>0`, else "" — the one field that carries the OLD run into the NEW one | no | — | missing |
| 36 | `crate_opened` | `crate_opened` | bool | false | `bool` | → false | **yes** | impossible_crate.gd | missing |
| 37 | `night_tripped` | `night_tripped` | bool | false | `bool` | → false | no | night_trip.gd | missing |
| 38 | `cov_monitor` | `cov_monitor` | float | 0.0 | `float` | → 0.0 | no | coverage_director.gd | missing |
| 39 | `cov_move` | `cov_move` | float | 0.0 | `float` | → 0.0 | no | coverage_director.gd | missing |
| 40 | `cov_still` | `cov_still` | float | 0.0 | `float` | → 0.0 | no | coverage_director.gd | missing |
| 41 | `photo_safe` | `photo_safe` | bool | false | `bool` | **NOT reset** (accessibility survives NEW GAME; lives in the log, not settings.cfg) | no | — (via `set_photo_safe`) | missing |
| 42 | `cascade_done` | `cascade_done` | bool | false | `bool` | → false | **yes** | cascade.gd | missing |
| 43 | `read_props` | `read_props` | Array of String (document ids, "of 10") | `[]` | array-or-ignore | → `[]` | no | — (via `mark_read`) | missing |
| 44 | `af_active` | `af_active` | bool | false | `bool` | **NOT reset** | no | fire_tape_dock.gd | live `bAfActive` ✓ — NOT in the save struct ⚠ |
| 45 | `af_taught` | `af_taught` | bool | false | `bool` | **NOT reset** | no | rundown.gd | live `bAfTaught` ✓ — NOT in the save struct ⚠ |
| 46 | `casualties` | `casualties` | Array of `{who:String, cause:String, line:String, day:int}` | `[]` | array-or-ignore | → `[]` | **yes** | — (via `mark_casualty`) | missing |
| 47 | `merle_offered` | `merle_offered` | bool | false | `bool` | → false | no | fire_tape_dock.gd | missing |
| 48 | `signoff_completed` | `signoff_completed` | bool | false | `bool` | **NOT reset** | no | seance_dock.gd | missing |
| 49 | `row_casualties` | `row_casualties` | int | 0 | `int` | → 0 | no | live_production.gd | missing |
| 50 | `h2_pending` | `h2_pending` | bool | false | `bool` | → false | no | harriet.gd, rejected_edit.gd | missing |
| 51 | `deadroom_seen` | `deadroom_seen` | bool | false | `bool` | **NOT reset** | no | hud.gd | missing |
| 52 | `rejected_seen` | `rejected_seen` | bool | false | `bool` | → false | no | rejected_edit.gd | missing |
| 53 | `glimpse_seen` | `glimpse_seen` | bool | false | `bool` | → false | no | glimpse.gd | missing |
| 54 | `merle_1974` | `merle_1974` | bool | false | `bool` | → false | no | merle.gd | missing |
| 55 | `fire_unsealed` | `fire_unsealed` | bool | false | `bool` | → false | no | glimpse.gd | missing |

**Casualty `who` ids** (from `all_cast_dead`): `"MERLE"`, `"VESS"`,
`"HARRIET"`, `"FLOOR MANAGER"`. **`ITEM_ORDER`** (loss order on strikes):
`WATCH, PEN, PHOTOGRAPH, LIGHTER, COMPACT, KEYS, LOUPE`.

**DEMO-erased set (15 keys)**, stripped only when `DEMO` is true:
`decision assets leland_answers lockdown_done finale_done ending_reached
lie_pending seance_wear has_fire_tape fire_tape_watched dock_done
crate_opened presigned_seen cascade_done casualties`.

**Fields that survive `reset_new_game()`** (8 of the 55, on purpose):
`mode tbc af_active af_taught photo_safe lie_pending signoff_completed
deadroom_seen` — plus `ng_relic`, which is recomputed from the dying run.
Everything else returns to its column-5 default.

---

## 3 · RUNTIME-ONLY STATE (public vars NOT in the save)

| var | type | default | reset | writers | notes / UE home |
|---|---|---|---|---|---|
| `is_night` | bool | false | → false | `set_night` (bed_prop.gd), live_production.gd, soak_runner.gd (direct) | NOT saved: a save taken at night reloads as day with `day` intact. Live `bIsNight` in 0.8a. 0.8b-2 replaces the direct writes with the day/night driver |
| `in_retake` | bool | false | → false | `strike`, hud.gd (clears it when the retake presentation ends) | `bInRetake` in 0.8a — ⚠ 0.8a clears it inside `Strike()`; canon is that the HUD presentation clears it |
| `station_points` | Dictionary String→Vector3 | `{}` | NOT reset | `register_station` | station pos + `(0, 0.5, 1.2)` = UE `(0, 120, 50)` offset. Fallback respawn `Vector3(0, 1.0, 2.5)` = UE `(0, 250, 100)`. Rebuilt from Data/Stations.csv on level load |
| `coverage_label` | String | "AUDIENCE" | NOT reset | coverage_director.gd | Director's verdict label |
| `premiere_live` | bool | false | → false | live_production.gd; cleared by `mark_ending` | `bPremiereLive` in 0.8a |
| `screening_active` | bool | false | NOT reset | screening_event.gd | |
| `map_points` | Array of `[id:String, Vector2(x, z)]` | `[]` | NOT reset | world_builder.gd appends one per station at build; map_view.gd reads | the binder map's station pins; in UE build it from Data/Stations.csv on level load (not persisted, same as Godot) |
| `cascade_active` | bool | false | → false | cascade.gd | `bCascadeActive` in 0.8a |
| `recording` | bool | false | NOT reset | capture_bench.gd | `bRecording` in 0.8a; the bench loop drives it in 0.8b-2 |
| `recording_left` | float | 0.0 | NOT reset | capture_bench.gd | `RecordingLeft` in 0.8a |
| `crossing` | bool | false | NOT reset | live_production.gd | `bCrossing` in 0.8a |
| `crossing_caught` | bool | false | NOT reset | live_production.gd, rundown.gd | `bCrossingCaught` in 0.8a |
| `harriet_slip` | bool | false | → false | harriet.gd; consumed once by `sign_log` | one free signature on empty paper |
| `fader_self` | bool | false | NOT reset | live_production.gd | |
| `mouse_sens` | float | 1.0 (clamp 0.2–3.0) | NOT reset | options_panel.gd; `load_settings` | settings.cfg `[input] sensitivity` |
| `ui_scale` | float | 1.0 (clamp 0.8–1.6) | NOT reset | `set_ui_scale`; `load_settings` | settings.cfg `[access] ui_scale` |
| `captions_on` | bool | false | NOT reset | `set_captions`; `load_settings` | settings.cfg `[access] captions` |
| `assist_on` | bool | false | NOT reset | `set_assist`; `load_settings` | settings.cfg `[access] assist` (assist-only difficulty per the gap audit ruling) |

Private: `_glyph_re` (compiled `\b<TOKEN>\b` regex cache), `_demo_t0`
(ms tick of first `demo_mark`).

**Constants**: `SAVE_PATH`, `DEMO` (false; true = Tape 1 demo build),
`SAVE_VERSION` 16, `SETTINGS_PATH := "user://settings.cfg"`,
`REMAP_ACTIONS := [interact, respond, improvise, toggle_tbc, map]`,
`GLYPH_MAP := {E→interact, SPACE→respond, Q→improvise, T→toggle_tbc,
M→map}`, `ITEM_ORDER` (above), enum `Mode`.

### 3b · settings.cfg (the second file; ConfigFile, not JSON)

| section | key | type | default | applied to |
|---|---|---|---|---|
| audio | master | float | 1.0 | master bus volume (linear → dB, floor 0.001) |
| input | sensitivity | float | 1.0 | `mouse_sens`, clamped 0.2–3.0 |
| access | ui_scale | float | 1.0 | `ui_scale` |
| access | captions | bool | false | `captions_on` |
| access | assist | bool | false | `assist_on` |
| keys | `<action>` (one per `REMAP_ACTIONS`) | int physical keycode | 0 (= unset) | `rebind(action, key, persist=false)` at load |
| video | fullscreen | bool | false | window mode (skipped when headless) |

`save_settings()` is called by `set_ui_scale`, `set_assist`, `set_captions`,
`rebind(persist=true)`, and 4 external sites. UE home: a `USaveGame` or
`GameUserSettings` subclass; the rebind conflict rule (a key already bound
to another `REMAP_ACTIONS` entry is refused with toast
`"KEY IN USE · that key already answers to %s."`) is part of the contract.

### 3c · demo_funnel.txt (DEMO only)
`demo_mark(event)` appends `[min %.1f] <event>` to `user://demo_funnel.txt`,
minutes since the first mark. Events seen: `started`, `s1_signed`, plus 5
external call sites. Study A6's funnel evidence — port with 5.8.

---

## 4 · SIGNALS — all 20, with emitters and consumers

Delegate naming law (migration map): same names, `FOn<PascalCase>`.

| signal (args) | emitted by | consumers (Godot) | UE delegate | 0.8a |
|---|---|---|---|---|
| `tbc_changed(enabled: bool)` | `set_tbc` | bench_tv.gd, hud.gd | `FOnTbcChanged` | — |
| `log_signed(station: String, remaining: int)` | `_sign_finish`, `mark_presigned` | achievements.gd, hud.gd | `FOnLogSigned` | — |
| `log_refused(station: String)` | `sign_log` (no paper, no slip) | hud.gd | `FOnLogRefused` | — |
| `notify(text: String)` | `toast`, `log_capture`, `_announce_*` | hud.gd | `FOnNotify` | — |
| `capture_status(text: String)` | `set_capture_status[_raw]` | hud.gd | `FOnCaptureStatus` | — |
| `sheet_changed(count: int)` | `strike`, `burn_daily` | dresser.gd, hud.gd | `FOnSheetChanged` | ✓ |
| `night_changed(now_night: bool)` | `set_night` | achievements.gd, floor_manager.gd, rundown.gd, world_builder.gd | `FOnNightChanged` | — (the brain polls `bIsNight` today) |
| `captured(take: int, sheet_full: bool, lost_item: String, respawn: Vector3)` | `strike` (non-full sheet) | hud.gd (the retake presentation) | `FOnCaptured` | — |
| `daily_added(id: int, take: int)` | `strike`, `mint_shortcut_daily` | dailies_manager.gd | `FOnDailyAdded` | — |
| `daily_burned()` | `burn_daily` | coverage_director.gd | `FOnDailyBurned` | — |
| `run_ended(take: int)` | `strike` (full sheet / ONE_TAKE) | achievements.gd, hud.gd | `FOnRunEnded` | ✓ |
| `finale_started(decision: String)` | `start_finale` | hud.gd | `FOnFinaleStarted` | — |
| `noise_event(pos: Vector3, loudness: float)` | `noise`, `_sign_finish` (loudness 4.0 at the respawn point) | rundown.gd | `FOnNoiseEvent` — or route straight into `ARundown::ReportNoise` | — |
| `photo_changed(on: bool)` | `set_photo_safe` | bench_tv.gd | `FOnPhotoChanged` | — |
| `blackout_changed(alpha: float)` | `set_blackout` | hud.gd | `FOnBlackoutChanged` | — |
| `ui_scale_changed(scale: float)` | `set_ui_scale` | hud.gd | `FOnUiScaleChanged` | — |
| `caption(text: String)` | `show_caption` (only when `captions_on`) | hud.gd | `FOnCaption` | — |
| `pause_requested()` | (no emitter inside game_state.gd) | hud.gd | `FOnPauseRequested` | — |
| `demo_ended()` | (no emitter inside game_state.gd) | hud.gd | `FOnDemoEnded` | — |
| `ending_marked(ending_name: String)` | `mark_ending` | world_builder.gd | `FOnEndingMarked` | — |

Note that signing a log is itself a noise (4.0 at the station): the
saving act is audible to the Rundown. That is canon (the schedule is real),
not a side effect to tidy.

---

## 5 · PUBLIC METHODS — the whole surface, with the rules each one keeps

Call counts are across `scripts/` (external callers), for porting priority.

**Paper economy & signing**
- `paper_for(station) -> int` — 99 in MATINEE, else `paper[station]` (0 if unknown). (1 caller)
- `sign_log(station) -> bool` — MATINEE: always signs. Otherwise: paper > 0 → decrement and sign; paper == 0 and `harriet_slip` → consume the slip, toast `"Signed. The hand on the slip is not yours, and the log accepts it anyway."`, sign; else emit `log_refused`, return false. (1 caller)
- `_sign_finish(station)` (private) — append `{station, tape, signed: datetime}`, `save_log`, `Sfx.tick()`, `demo_mark("s1_signed")` if S1, emit `log_signed(station, paper_for)`, emit `noise_event(respawn_point(), 4.0)`.
- `mark_presigned()` — `presigned_seen = true`, append `{station:"S4", tape, signed:"TOMORROW", presigned:true}`, save, emit `log_signed("S4", paper_for("S4"))`. No paper is consumed. (1)
- `register_station(id, pos)` — `station_points[id] = pos + (0, 0.5, 1.2)`. (1)
- `respawn_point() -> Vector3` — the station of the LAST signature if registered, else `(0, 1.0, 2.5)`. Used by `strike`'s `captured` payload and by the signing noise.

**Strikes, sheet, dailies (retake economy)**
- `strike(player)` — guarded by `in_retake`; `in_retake = true`; `strikes += 1`; `take = strikes`; lose `ITEM_ORDER[items_lost]` if `items_lost < 7` (then `items_lost += 1`); `full = strikes >= 4 or mode == ONE_TAKE`. Full: `strikes = 0`, save, emit `sheet_changed(0)`, emit `run_ended(take)`, return (in_retake stays true — the run-end flow owns it). Not full: `daily_seq += 1`, append `{id, take}`, emit `daily_added`, save, emit `sheet_changed(strikes)`, emit `captured(take, false, lost, respawn_point())`. The player is repositioned by the retake presentation, not here. (2 callers) — 0.8a ports the arithmetic; ⚠ mode/ONE_TAKE, item names, `captured` payload, and the in_retake ownership remain.
- `burn_daily()` — `carried_id = -1`, `carried_take = 0`; if `strikes > 0`: `strikes -= 1` + toast `"BURNED · TAKE %d. Her name fades from the line. Its read on you resets."` else toast `"...The sheet was already clean. The canister burns anyway."`; save; emit `sheet_changed`, `daily_burned`. (1)
- `pick_daily(id, take)` — remove the daily with that id from `dailies`, set carried, save, toast `"CARRYING · SCENE 4 TAKE %d. The degausser is in the climate room."`. (1)
- `mint_shortcut_daily()` — `daily_seq += 1`, append `{id, take:-1}`, emit `daily_added(id, -1)`, save. (1)

**Casualties (the ledger)**
- `mark_casualty(who, cause, epitaph)` — no-op if already dead; append `{who, cause, line: epitaph, day}`, save, toast `"THE LEDGER TAKES IT DOWN."`. (10)
- `is_dead(who) -> bool` (36) · `cause_of(who) -> String` (2) · `all_cast_dead() -> bool` = MERLE ∧ VESS ∧ HARRIET ∧ FLOOR MANAGER (1).
- `in_dead_room(pos) -> bool` — `|x−19| ≤ 2.2 ∧ |z−2.5| ≤ 2.7` (Godot m). (3) — 0.8a ✓ as `InDeadRoom` in uu.

**Keys, assets, signals, documents**
- `has_key(id)` (8) · `take_key(id, display)` — duplicate → toast `"You already carry %s."`; else append, save, toast `"TAKEN · %s"`. (1)
- `gain_asset(id, display)` — no-op if held; append, save, toast `"ASSET BANKED · %s (%d of 4)"`; at 4: toast `"All four. The finale has everything it needs, when night falls."`. (2)
- `add_show_signal(sig)` — set-insert into `signals_known` (NO save_log). (2)
- `mark_read(id)` — set-insert into `read_props`, save, toast `"READ · filed to memory. (%d of 10 documents)"`. (7)
- `add_pt(n)` (2) · `add_wear(n: float)` (1) — increment and save.

**Day / night / mode / finale**
- `set_night(on)` — `is_night = on`. Day→ (on=false): `day += 1`, `current_tape = min(day, 5)`, toast `"MORNING · Day %d · Tape %d. The building pretends nothing happened."`; if `day >= 3 and not run_complete` → `run_complete = true` + toast `"PROTOTYPE COMPLETE · ..."`. Night (on=true): toast `"NIGHT · the building belongs to the schedule."`. Save, emit `night_changed(on)`. (1 caller: bed_prop.gd toggles). ⚠ live_production.gd and soak_runner.gd set `is_night` DIRECTLY (no signal) — 0.8b-2's day/night driver replaces those scaffolds.
- `set_mode(m)` — no-op if same; set, save, toast `"MODE · %s"` (MATINEE / LATE NIGHT / ONE TAKE); ONE_TAKE adds `"ONE TAKE · any capture ends the run. ..."`. (3)
- `set_tbc(on)` — set + emit `tbc_changed` (NO save_log; tbc persists only via the next save). (2)
- `start_finale()` — emit `finale_started(decision)`. (2)
- `mark_ending(name, lie=false)` — `premiere_live = false`, `finale_done = true`, `ending_reached = name`, emit `ending_marked`, `Achievements.on_ending(name)`, `lie_pending = true` if lie, save. (8)
- `objective_text() -> String` — the HUD objective line; priority order: DEMO+captures → finale_done → decision set → run_complete∧day≥3 → night (dailies/carried variant) → day 1 chain (S1 signed? → screening_done? → captures? → bed) → day≥3 → default. Port verbatim; strings via GameText.csv. (1)
- `reset_new_game()` — `demo_mark("started")`; compute `ng_relic`; reset every column-6 "→" field (§2/§3); save. (2)

**Presentation / accessibility / input**
- `toast(text)` — emit `notify(glyphs(tr(text)))`. (198 callers — the single busiest API.)
- `glyphs(text)` — replace whole-word tokens E/SPACE/Q/T/M with the CURRENT bound key name, upper-cased (the "real binding glyphs" law). (3)
- `set_capture_status(text)` (glyph-substituted, 30) · `set_capture_status_raw(text)` (as-is).
- `log_capture(name)` — append `{name, tape, at}`, save, emit `notify("CAPTURED · %s · presentation kept")`. (1)
- `show_caption(text)` — emit `caption(tr(text))` only if `captions_on`. (16)
- `set_blackout(alpha)` — emit only. (8) · `noise(pos, loudness)` — emit only. (2)
- `set_photo_safe(on)` — set, SAVE (to the log), emit `photo_changed`, toast `"PHOTOSENSITIVITY-SAFE MODE · ON · bands and flicker suppressed"` / `"... OFF"`. (2)
- `set_ui_scale(v)` — clamp 0.8–1.6, emit, save_settings. (1) · `set_assist(on)` (1) · `set_captions(on)` (1) — set + save_settings.
- `rebind(action, physical_keycode, persist=true)` — refuse if the key is bound to another `REMAP_ACTIONS` entry; erase the action's key events; add the new one; save_settings if persist. (1)
- `key_name(action) -> String` — first bound key's keycode string, else `"?"`. (3)
- `load_settings()` / `save_settings()` — §3b. (`save_settings`: 4 external.)
- `save_log()` (20 external) / `load_log()` — §1.
- `demo_mark(event)` — §3c. (5)
- `_signed_station(id)` (private) · `_announce_migration` / `_announce_newer` (deferred toasts, §1).

---

## 6 · 0.8b-2 IMPLEMENTATION CHECKLIST (derived from the ⚠ marks above)

1. Fix the 0.8a skeleton's type/default divergences: `Mode` default 1,
   `CurrentTape` default 1, `Paper` → `TMap<FString,int32>` with the five
   S1–S5 = 3 defaults, `Signatures`/`Captures`/`LelandAnswers` → struct
   arrays, `SeanceWear` → float, `ItemsLost` cap 7 with `ITEM_ORDER`.
2. Add every save key absent from `URestorationSaveGame` (32 of the 55):
   the 30 rows marked "missing" in §2 plus `af_active`/`af_taught`, which
   are live in 0.8a but never persisted (the fire-tape AF state must
   survive a reload; both are among the 8 reset-survivors). Wire each into
   `SaveToSlot`/`LoadFromSlot`.
3. Honor the reset-survivor set (§2) in the UE `ResetNewGame`, and the
   `ng_relic` handoff.
4. Honor load coercion (§1): missing keys default, array keys ignore
   non-arrays, `paper` merges.
5. Port the 20 signals as delegates (§4); `night_changed` replaces the
   brain's `bIsNight` polling; the direct `is_night` writes in
   live_production.gd / soak_runner.gd are the "test scaffolds" 0.8b-2's
   day/night driver retires.
6. Port the DEMO switch: `paper` default `{S1,S5}` and the 15-key erase
   list, behind one constant.
7. Every toast string in §5 is a GameText.csv key (unit 0.5 extracted 714);
   route through the UE text table, then `Glyphs()`.
8. settings.cfg → UE user settings (§3b) with the rebind-conflict rule.
9. Round-trip test: write a v16 save with every field non-default, reload,
   assert equality; then load a v1 (empty) dict and assert every default
   in §2 column 5; then load a v17 and assert the "newer build" warning.
   Extend `ue/pyscripts/test_state_af.py` or add `test_state_schema.py`.
