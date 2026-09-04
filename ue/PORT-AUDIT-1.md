# PORT AUDIT 1 · the UE C++ against the GDScript it claims to port

**Unit C17 (CLOUD-OK).** A line-by-line diff of `ue/Restoration/Source/
Restoration/*.h,.cpp` (17 files, 1638 lines, at origin/main `0e8166d`)
against `scripts/game_state.gd` (777), `rundown.gd` (482), `harriet.gd`
(121), `player.gd` (77), `capture_bench.gd` (66), `bench_tv.gd` (65) and
`broadcast.gd` (31): every constant, every default, every order of
effects, every signal. Drift is listed as a checklist in §9, in the shape
`ue/PORT-NOTES-STATE.md` §6 used, so the Mac lane can tick it.

**The law this audit applies.** "The Godot build is the specification;
where prose and code disagree, the code is the intent" and "every
constant in it is canon" (`docs/packet/portbrief/PORT-BRIEF.md` §0 and
§1). "WHAT MUST NOT CHANGE, REGARDLESS OF ENGINE": the invariant suite,
log formats, save semantics, room table, tell-table, silence ledger,
every knob number (`UE5-MIGRATION-MAP.md` §WHAT MUST NOT CHANGE); signals
become multicast delegates with the same names (same doc, §SYSTEM MAP
STATE); the rundown is a tick brain with no Behavior Tree (§SYSTEM MAP
THE RUNDOWN). THE-LAWS bind where named (`docs/packet/portbrief/THE-LAWS.md`).

**Verdicts used.** MATCH = identical value/order. DRIFT = C++ differs from
the GDScript in a way that changes behavior, a saved value, or a knob.
ABSENT = the GDScript behavior has no C++ counterpart yet (not a bug; a
box still open, but listed so nothing is forgotten). UE-ONLY = the C++
does something the GDScript does not (harness scaffolding or an addition
the port must justify). OPEN = canon and code are silent; a ruling is
needed, not a guess.

Coordinate convention assumed throughout (from `ue/pyscripts/
build_greybox.py` line 3, the stamped world): Godot (x, y-up, z) → UE
(x, y = Godot z, z = Godot y), metres × 100. Every C++ position below
was checked against that mapping, not against UE's X-forward convention
(`docs/canon/restoration-blender-ue5-pipeline.md` line 8 states X-forward
for FBX import; the world data uses the greybox mapping — both hold, they
answer different questions).

---

## 1 · CONSTANTS (every knob number, Godot vs C++)

| Constant | GDScript | C++ | Verdict |
|---|---|---|---|
| `SAVE_VERSION` | 16 (`game_state.gd:7`) | `SaveVersion = 16` (`RestorationState.h:123`) | MATCH |
| `Mode` enum | MATINEE=0, LATE_NIGHT=1, ONE_TAKE=2 (`:9`) | raw ints 0/1/2 in comments (`RestorationState.cpp:43,49,174`) | MATCH (no enum type; see §9 L1) |
| `ITEM_ORDER` | 7 names (`:133`) | only the count 7 (`RestorationState.cpp:170`) | DRIFT — names absent, `lost` never computed (§9 S6) |
| Paper default | `{S1..S5: 3}` (`:16`) | `SeedPaper()` S1..S5=3 (`:149-157`) | MATCH |
| Full sheet | `strikes >= 4 or mode == ONE_TAKE` (`:492`) | same (`:174`) | MATCH |
| Dead room rect | `|x-19|<=2.2 && |z-2.5|<=2.7` (`:122`) | `|X-1900|<=220 && |Y-250|<=270` (`.h:220-224`) | MATCH under mapping |
| Fallback respawn | `(0, 1.0, 2.5)` (`:244`) | `(0, 250, 100)` uu (`:104`) | MATCH under mapping |
| Station offset | `pos + (0, 0.5, 1.2)` (`:235`) | `+ (0, 120, 50)` uu (`:90`) | MATCH under mapping |
| Sign-log noise | `noise_event(respawn_point(), 4.0)` (`:189`) | `OnNoise.Broadcast(RespawnPoint(), 4.0f)` (`:82`) | MATCH |
| Tape cap | `min(day, 5)` (`:471`) | `FMath::Min(Day, 5)` (`:25`) | MATCH |
| Prototype complete | `day >= 3` (`:473`) | `Day >= 3` (`:27`) | MATCH |
| Documents total | "of 10" (`:208`) | "of 10" (`:112`) | MATCH (text differs, §3) |
| `SAVE_PATH` | `user://transmitter_log.json` | slot `"restoration"` | MATCH by design (PORT-NOTES §0) |
| `SETTINGS_PATH`, `REMAP_ACTIONS`, `GLYPH_MAP`, `DEMO` | present | — | ABSENT (PORT-NOTES §4/§5 scope) |
| `MOVE_SPEED` | 2.4 (`rundown.gd:14`) | 2.4 (`Rundown.h:23`) | MATCH |
| `AF_APPROACH_SPEED` | 0.8 | 0.8 | MATCH |
| `AF_LOOM_DIST` | 1.2 | 1.2 | MATCH |
| `AF_COOL_SECONDS` | 2.0 | 2.0 | MATCH |
| `AF_HEIGHT` | 3.35 (`:18`) | — | ABSENT (the scale law; the rig is a mesh in UE — OPEN, see GATE-0.10 ruling 1b) |
| `AF_FOLD_SECONDS` | 2.2 | 2.2 | MATCH (LAW 11) |
| `AF_DOOR_NEAR` | 1.0 | 1.0 | MATCH |
| `AF_CROSSING_SPEED` | 1.6 (`:21`) | 1.6 (`Rundown.h:29`) declared, unused | MATCH value; crossing ABSENT (§4 R12) |
| `DEADROOM_DOOR` | `(19, 0, 0)` (`:22`) | inline `FVector(1900, 0, 0)` (`Rundown.cpp:277`) | MATCH under mapping (not a named constant) |
| `WARN_RADIUS` | 7.0 | 7.0 | MATCH |
| `STRIKE_RADIUS` | 2.2 | 2.2 | MATCH |
| Savor widening | `2.6 if strikes >= 3` (`:150`) | `2.6f` if `StrikesNow() >= 3` (`:164`) | MATCH |
| HIDER warn radius | `5.0` (`:151`) | — | ABSENT (director not ported) |
| Cascade warn narrowing | `max(3.5, warn_r - 1.5)` (`:153`) | — | ABSENT (cascade not ported) |
| Heard-noise window | `12.0 s` (`:167`) | `12.0f` (`:170`) | MATCH |
| Hearing radius | `loudness * 3.0` (`:132`) | — | DRIFT — no radius at all (§9 R1) |
| Fold cooldown per door | `6.0 s` (`:339`) | `6.0f` (`:202`) | MATCH |
| Dead-door hold distance | `0.6` (`:249`) | `0.6f * M` (`:278`) | MATCH |
| Untaught first cool | `4.0` (`:278`) | `4.0f` (`:310`) | MATCH |
| Tally-cool strike reach | `_strike_r + 0.4` (`:283`) | `StrikeR + 0.4f` (`:327`) | MATCH |
| Strike raycast height | `+ Vector3.UP` (1 m) (`:310`) | `+ (0,0,M)` (`:385-386`) | MATCH |
| Strike cooldown | none in `rundown.gd` | `StrikeCooldown = 3.0f` (`:394`) | UE-ONLY (§9 R6) |
| `BASE_HEIGHT` 2.6, `HEAD_TILT` 0.045, `SEGMENT_FREQS` | present | — | ABSENT (rig/presentation) |
| Segment anchors | `rooms[zone]` lookup (`:350-355`) | hardcoded `(0,-16) (-15.5,-30) (-5.5,-29.5)` (`Rundown.cpp:24-25`) | MATCH values vs `Data/Rooms.csv` rows 9/16/17; DRIFT in sourcing (§9 R10) |
| `ON_AIR_SECONDS` | 50.0 (`broadcast.gd:5`) | 50.0 (`RestorationClock.h:21`) | MATCH |
| `BREAK_SECONDS` | 18.0 | 18.0 | MATCH |
| `SPEED` | 3.1 (`player.gd:4`) | 3.1 (`RitaCharacter.h:19`) | MATCH |
| `ACCEL` | 10.0 | 10.0 → `MaxAcceleration`, `BrakingDecelerationWalking` (`.cpp:22-23`) | MATCH value (§9 P3 on braking) |
| `MOUSE_SENS` | 0.0022 × clamp(0.2..3.0) (`:6,34`) | — | DRIFT — engine default yaw scale (§9 P1) |
| Pitch clamp | ±1.3 rad (`:36`) | — (engine default ±89.9°) | DRIFT (§9 P1) |
| `REACH` | 2.6 | 2.6 | MATCH |
| `CROUCH_MULT` | 0.55 | 0.55 | MATCH |
| Crouch camera drop | 0.6 (`:58`) | 0.6 (`.h:23`) | MATCH |
| Camera ease | `12.0 * delta` lerp (`:58`) | `FInterpTo(..., 12.0f)` (`.cpp:118`) | MATCH in spirit (lerp-by-fraction vs FInterpTo; both 12/s) |
| Gravity | `12.0` m/s² (`:55`) | engine default 9.8 | DRIFT (§9 P2) |
| Eye height | camera y = 1.6 m over floor (`scenes/main.tscn:67`) | 88 + 60 = 148 uu (`.cpp:18,31`) | DRIFT (§9 P4) |
| `CAPTURE_SECONDS` | 12.0 (`capture_bench.gd:6`) | 12.0 (`BenchCapture.h:19`) | MATCH |
| `TETHER` | 4.0 | 4.0 | MATCH |
| AF teach teleport | `(-5, 0, -16)` (`:31`) | `(-500, -1600, 0)` (`BenchCapture.cpp:63`) | MATCH under mapping |

`Data/Timings.csv` carries 32 constants; the 18 that have a named C++
constant all match (verified by script, PR body). The 14 without one are
`credits.gd`, `frame_sequence.gd`, `merle.gd`, `screening_event.gd`,
`seance_dock.gd`, `tone_emitter.gd`, `world_builder.gd` rows (systems not
yet ported), `AF_HEIGHT`/`BASE_HEIGHT`/`HEAD_TILT` (the Godot rig), and
`MOUSE_SENS` — the one of the 14 that IS a ported system's knob and is
missing (§9 P1).

---

## 2 · `game_state.gd` ↔ `URestorationState` / `URestorationSaveGame`

### 2.1 Saved fields (55 keys)
All 55 `_save_dict` keys exist on both `URestorationSaveGame` and the
subsystem, in dict order, with spec types and spec defaults
(`RestorationState.h:56-110`, `:140-193`; verified against
`game_state.gd:528-585` by the script in the PR body). `SaveToSlot` and
`LoadFromSlot` copy all 54 non-version fields (`.cpp:195-274`). Paper
MERGES on load (`.cpp:250`) exactly as `load_log` does (`:600-603`).
MATCH.

Two value-format deltas inside otherwise-matching fields:
- `signatures[].signed` and `captures[].at` are
  `Time.get_datetime_string_from_system()` in Godot (ISO `YYYY-MM-DDTHH:MM:SS`,
  `:182,:228`); C++ writes `FDateTime::Now().ToString()`
  (`YYYY.MM.DD-HH.MM.SS`, `.cpp:76,137`). Nothing reads these strings
  today, but PORT-NOTES §6's done-criterion is "a v16 log written by the
  Godot build round-trips through the UE slot with identical field
  values". DRIFT, low (§9 S1).
- `ABenchCapture` writes `At = "BENCH"` (`BenchCapture.cpp:120`) instead of
  a timestamp, bypassing `LogCapture()`. DRIFT (§9 B2).

### 2.2 Live (unsaved) fields
Present: `is_night, in_retake, recording, recording_left, premiere_live,
crossing, crossing_caught, cascade_active, harriet_slip, station_points`
(`.h:128-137`). MATCH.
Absent: `coverage_label` ("AUDIENCE"), `screening_active`, `map_points`,
`fader_self`, `mouse_sens`, `ui_scale`, `captions_on`, `assist_on`
(`game_state.gd:42,56,57,82,67-70`). ABSENT — they belong to the director,
screening, map, seance and settings systems, none ported (§9 S9).

### 2.3 Boot
`_ready()` calls `load_settings()` then `load_log()` (`:152-154`).
`Initialize()` only seeds paper (`.cpp:143-147`); nothing calls
`LoadFromSlot` at boot. DRIFT — the transmitter log is never read back
on launch (§9 S2).

### 2.4 Functions ported — order of effects, line by line

**`paper_for`** (`:157-160` ↔ `.cpp:41-45`): MATINEE → 99, else
`paper.get(station, 0)` ↔ `FindRef` (0 default). MATCH.

**`sign_log`** (`:163-175` ↔ `.cpp:47-69`): non-MATINEE → no paper →
slip? (consume, toast) : (`log_refused.emit`, return false); else
decrement; then `_sign_finish`. C++ order identical. Missing inside it:
the slip toast "Signed. The hand on the slip is not yours, and the log
accepts it anyway." and the `log_refused` delegate (C++ writes a LogLine
`SIGN REFUSED` instead). DRIFT on signals/toasts (§9 S3, S4).

**`_sign_finish`** (`:178-190` ↔ `.cpp:71-84`). Godot: append {station,
tape, signed} → `save_log` → `Sfx.tick()` → `demo_mark("s1_signed")` if
S1 → `log_signed.emit(station, paper_for(station))` → `noise_event.emit(
respawn_point(), 4.0)` → true. C++: append → `SaveToSlot` → LogLine
`SIGNED` → `OnNoise.Broadcast` → true. Same order for what exists;
`Sfx.tick` (audio, ABSENT), `demo_mark` (DEMO, ABSENT), `log_signed`
(delegate ABSENT — §9 S4). Also: Godot never fills `presigned` on a
normal signature; C++ struct defaults `bPresigned=false`, which
serializes a key Godot omits. Harmless for UE-only saves; OPEN whether
the UE save must byte-match the JSON (§9 S1).

**`mark_read`** (`:203-208` ↔ `.cpp:107-113`): dedupe → append → save →
toast "READ · filed to memory. (%d of 10 documents)". C++ LogLines
`READ %s (%d of 10 documents)` — no toast. Order MATCH; toast ABSENT.

**`log_capture`** (`:224-231` ↔ `.cpp:132-141`): append → save →
`notify.emit("CAPTURED · %s · presentation kept")` (raw notify, no
`tr()`/glyphs — note that Godot deliberately bypasses `toast` here). C++
LogLines the same text. Order MATCH; notify ABSENT.

**`register_station` / `respawn_point`** (`:234-244` ↔ `.cpp:86-105`):
MATCH (offsets verified §1). `respawn_point` reads the LAST signature's
station — both do.

**`has_key` / `take_key`** (`:247-257` ↔ `.cpp:115-130`): MATCH; the
"You already carry %s." toast is a LogLine.

**`set_night`** (`:467-479` ↔ `.cpp:19-39`): `is_night = on` → morning:
`day += 1`, tape cap, toast, `run_complete` at day≥3 (+toast) → else
night toast → `save_log` → `night_changed.emit(on)`. C++ identical order
with LogLines for the toasts. MATCH. Delegate signature: Godot
`night_changed(bool)`; C++ reuses `FOnSheetChanged` (int32) and
broadcasts 1/0 (`.h:197`, `.cpp:38`). DRIFT, low (§9 S5). Nobody in C++
subscribes to it — `rundown.gd:123,137-143` does (§9 R4).

**`strike`** (`:482-506` ↔ `.cpp:159-193`). Godot, verbatim order:
1. `if in_retake: return`; `in_retake = true`
2. `strikes += 1`; `take = strikes`
3. `lost = ITEM_ORDER[items_lost]` if `items_lost < 7`; `items_lost += 1`
4. `full = strikes >= 4 or mode == ONE_TAKE`
5. full: `strikes = 0` → `save_log` → `sheet_changed.emit(0)` →
   `run_ended.emit(take)` → return. **`in_retake` stays TRUE.**
6. not full: `daily_seq += 1` → `dailies.append({id, take})` →
   `daily_added.emit` → `save_log` → `sheet_changed.emit(strikes)` →
   `captured.emit(take, full, lost, respawn_point())`. **`in_retake`
   stays TRUE** — it is cleared by `hud.gd:306` at the END of the retake
   presentation (≈3 s later, after the player is teleported to `respawn`
   at `hud.gd:288-290`), and by `reset_new_game` (`:726`). Nothing else
   clears it: after a full sheet the Godot hunter can never strike again
   in that run.
C++: 1–2 MATCH; 3 increments `ItemsLost` but never records WHICH item
(`lost` is not computed, the `captured` delegate does not exist); 4
MATCH; 5 MATCH except `bInRetake = false` before return; 6: `DailySeq`,
`Dailies.Add`, `OnSheetChanged` — **no `SaveToSlot`**, no `daily_added`,
no `captured`, then `bInRetake = false`. DRIFT ×4 (§9 S6, S7, S8).

**`in_dead_room`**: MATCH (§1).

### 2.5 Functions not ported (the §6 tail of PORT-NOTES, still open)
`glyphs`, `toast`, `set_capture_status(_raw)`, `add_show_signal`,
`pick_daily`, `burn_daily`, `mint_shortcut_daily`, `set_mode`,
`load_settings`, `save_settings`, `demo_mark`, `set_ui_scale`,
`set_assist`, `rebind`, `key_name`, `set_captions`, `show_caption`,
`set_blackout`, `noise`, `set_photo_safe`, `start_finale`,
`mark_ending`, `gain_asset`, `mark_presigned`, `add_wear`, `add_pt`,
`set_tbc`, `cause_of`, `is_dead`, `all_cast_dead`, `mark_casualty`,
`objective_text`, `reset_new_game`, `_signed_station`,
`_announce_migration`, `_announce_newer`. 36 functions. ABSENT (§9 S10).
Two of them matter for LAWS already exercised: `is_dead`/`cause_of`
gate every Harriet branch (LAW 7), and `show_caption` carries the
captions LAW 9 requires.

### 2.6 Load version handling
Godot: after reading fields, `v < SAVE_VERSION` → `save_log()` (rewrites
the file at the new version) then announces; `v > SAVE_VERSION` →
announces (`:672-677`). C++ logs both cases, never re-saves, never
notifies (`.cpp:240-247`). DRIFT, low (§9 S2).

---

## 3 · SIGNALS (20 in `game_state.gd:19-23, 135-149`) → delegates

| Godot signal | C++ delegate | Verdict |
|---|---|---|
| `sheet_changed(int)` | `OnSheetChanged` (int32) | MATCH |
| `night_changed(bool)` | `OnNightChanged` typed `FOnSheetChanged` (int32) | DRIFT type |
| `run_ended(int)` | `OnRunEnded` (int32) | MATCH |
| `noise_event(Vector3, float)` | `OnNoise` (FVector, float) | MATCH; the listener drops `float` (§9 R1) |
| `tbc_changed(bool)` | — | ABSENT |
| `log_signed(String, int)` | — | ABSENT (LogLine only) |
| `log_refused(String)` | — | ABSENT (LogLine only) |
| `notify(String)` | — | ABSENT — every toast in §2 rides this |
| `capture_status(String)` | — | ABSENT (HUD countdown; LAW 10 "the countdown is visible") |
| `captured(int, bool, String, Vector3)` | — | ABSENT — the retake presentation's trigger |
| `daily_added(int, int)` | — | ABSENT |
| `daily_burned` | — | ABSENT |
| `finale_started(String)` | — | ABSENT |
| `photo_changed(bool)` | — | ABSENT |
| `blackout_changed(float)` | — | ABSENT |
| `ui_scale_changed(float)` | — | ABSENT |
| `caption(String)` | — | ABSENT (LAW 9) |
| `pause_requested` | — | ABSENT (LAW 9: pause ships in every build) |
| `demo_ended` | — | ABSENT |
| `ending_marked(String)` | — | ABSENT |

4 of 20 declared; 16 ABSENT; 1 typed wrong. Also `Broadcast.phase_changed
(bool)` → `URestorationClock::OnPhaseChanged(bool)` MATCH.

Listener wiring that exists in Godot and is checked here:
- `GameState.noise_event → Rundown._on_noise` ↔ `OnNoise → ReportNoise`
  lambda (`Rundown.cpp:65`): wired, but the filter is gone (§9 R1).
- `Broadcast.phase_changed → Rundown._on_phase` ↔ `Clock->OnPhaseChanged
  .AddUObject(OnPhaseChanged)` (`:56`): MATCH.
- `GameState.night_changed → Rundown._on_night` ↔ nothing (§9 R4).
- `GameState.tbc_changed / photo_changed → BenchTV` ↔ nothing (BenchTV ABSENT).
- UE-ONLY: `OnRunEnded → LogLine("RUN ENDED take=%d …")` (`:68-71`). In
  Godot `run_ended` is consumed by `hud.gd:_on_run_ended` (locks the
  player); the line exists so the parser's UE-R1 check can read it
  (`tools/invariant_parser.py:81`). Justified addition; note the format
  is UE-only and must stay stable.

---

## 4 · `rundown.gd` ↔ `ARundown`

### 4.1 Construction / `_ready`
Godot (`:68-125`): builds the rig, eye, label, audio, tone; connects
`noise_event`; `global_position = _anchor(_idx)`; `_target`; connects
`phase_changed`, `night_changed`; **`visible = GameState.is_night`**.
C++ `BeginPlay` (`:29-135`): places at anchor, loads doors from
`Data/Doors.csv` (20 rows, the same 20 the Godot `DOORS` const feeds at
`world_builder.gd:580-581` — MATCH), wires phase + noise + run-ended,
then harness pushes. **Never sets initial hidden state** — he is visible
by day (§9 R5). The body (rig, eye light `1.6` energy while
`af_active and recording`, label, tone) is presentation: ABSENT, and the
eye IS the contract (LAW 10 "the eye's light and the contract are the
same fact") — flagged for the presentation half (§9 R13).

### 4.2 `_on_noise` (`:127-134`) ↔ `ReportNoise` (`:151-155`)
Godot rejects the noise if `in_dead_room(pos)` (LAW 11 "the dead room …
eats sound"; room bible DEAD ROOM "deaf to noise"), if `not is_night`,
if `premiere_live`, and only hears within `loudness * 3.0` m. C++ stores
every noise, from anywhere, at any hour, and the lambda discards the
loudness. DRIFT, high — signing the log at any station relocates him on
the next break regardless of distance, and a noise made inside the dead
room reaches him (§9 R1).

### 4.3 `_on_phase` ON AIR (`:147-164`) ↔ (`:159-167`)
Godot: label → `_warned = false` → `_strike_r` savor → `_warn_r` (HIDER
5.0 else 7.0) → cascade narrowing → if night: CHECKER kills the
most-watched rig <14 m, and any rig <9 m. C++: `bWarned = false`,
`StrikeR`, `WarnR = 7`. Order MATCH for the ported subset; director
profiles, cascade, rig kills ABSENT (marked TODO(0.8) in source) (§9 R11).

### 4.4 `_on_phase` BREAK (`:165-200`) ↔ (`:168-188`)
Godot: heard within 12 s → nearest anchor to `_heard_pos`, log
`RELOCATE toward heard noise at %s -> segment %d`, first time ever:
`Achievements.unlock("A08")` + toast; elif SPRINTER → nearest anchor to
the player, log `RELOCATE sprinter-bias`; else cycle, log `RELOCATE cycle
-> segment %d (profile %s)`; then `_target`, label, tone. C++: heard →
nearest (MATCH, same log text); else cycle with `(profile UNKNOWN)`. The
SPRINTER branch ABSENT; A08 and toast ABSENT. Log text: Godot prints
`str(_heard_pos.round())` (Godot Vector3 print, rounded metres); C++
prints `HeardPos.ToString()` (uu, `X= Y= Z=`). The parser matches on the
prefix only (`invariant_parser.py:27-29`), so it still rules; the
payload format differs. DRIFT, low (§9 R9).

### 4.5 `_physics_process` (`:203-330`) ↔ `Tick` (`:213-404`) — order of effects
Godot order: (1) `premiere_live` → crossing block or hide, return; (2)
`af_active and not _af_bodied` → scale the rig; (3) eye energy; (4)
`af_active and recording and _player` → the contract block; (5) cool
re-arm; (6) cool countdown; (7) `not is_night → return`; (8) resolve
`_player`; (9) `not on_air` → BREAK move (fold only `if af_active`); (10)
ON AIR hunt.
C++ order: (0) `StrikeCooldown` decrement; (0b) **`FoldT > 0 → decrement,
return` before everything**; (0c) invariants driver; (0d) recording-off
driver; (4) contract block; (5) re-arm; (6) countdown; (7) night gate;
(9) BREAK move with `DoorFoldCheck` unconditionally; (10) hunt.
- (1) premiere/crossing ABSENT (Phase 5; `AF_CROSSING_SPEED` declared
  for it). (2)(3) presentation ABSENT.
- (0b): Godot only decrements `_fold_t` inside blocks (4), (9-if-AF) and
  (1); a fold begun under the contract that is interrupted by the
  recording ending leaves `_fold_t > 0` frozen through the countdown and
  the hunt. C++ ticks it everywhere. Difference is a ≤2.2 s edge; note
  as DRIFT, low (§9 R7).
- (4) contract block: `SetActorHiddenInGame(false)` ↔ `visible = true`;
  dead-room hold at the felt door (`> 0.6` → fold check → approach at
  0.8; else one-shot line) MATCH; loom (`pd > 1.2` → fold check →
  approach; else one-shot `_af_seen_once`) MATCH; `_af_cool = -100`
  MATCH. ABSENT inside: `Sfx.thunk` every 1.1 s of approach, the caption
  `[THE JAW WORKS ITS LEVER]`, the toast, `_work_jaw()` (the two-beat
  act — motion canon, AAA_BUILD_PLAN §1 hard rules). Godot toasts "It
  stops at the felt door…" ↔ C++ `AF holds at the felt door`.
- (5) re-arm: condition `af_active and _player and _af_cool < -50 and
  not recording and visible and not is_night` ↔ `Prey && AfCool < -50 &&
  !bRecording && !bIsNight && !IsHidden()` MATCH. Taught branch order
  MATCH (2.0 / set taught then 4.0). Toasts → LogLines. **But** because
  of §4.1 (never hidden at boot), on any daytime BeginPlay with
  `bAfActive` and a player pawn present the C++ re-arms immediately,
  burns `bAfTaught = true` without a contract ever having been shown,
  counts 4 s, then hides him. Godot cannot: `visible` is false until the
  first capture shows him. DRIFT, medium (§9 R5).
- (6) countdown → strike if within `StrikeR + 0.4` → hide → home anchor:
  MATCH, including the `STRIKE af tally-cool` line.
- (7) night gate placement MATCH (the 0.8a finding).
- (9) BREAK: Godot pays the door toll only `if GameState.af_active`
  (`:296-300`); C++ always (`:352-355`). The pre-fire stage body has no
  fold in the reference. DRIFT, medium (§9 R8).
- (10) hunt: `d < _strike_r` → raycast `+UP` excluding the player →
  `thru` → log `STRIKE seg %d d=%.1f[ savor][ THRU-WALL]` →
  `_strike_pose_t = 0.9` → `GameState.strike` → `_warned = false`. C++:
  same raycast (also ignores self — no-op, Godot's Rundown has no
  collider), same log text (MATCH, the parser's format), `Strike`, then
  **`StrikeCooldown = 3.0` and `SetActorLocation(SegmentAnchors[SegIdx])`**
  — neither is in `rundown.gd`. In Godot the latch is `in_retake`
  (held ≈3 s by the HUD, see §2.4) and the hunter stays where he struck;
  the PLAYER moves (to `respawn`). Combined with §9 S7 (C++ clears
  `bInRetake` at once), the 3.0 s cooldown is the port's stand-in for the
  HUD's latch and the teleport is a stand-in for the player's respawn.
  Both are UE-ONLY behaviors the retake presentation box (0.8b-5) must
  replace, and the 3.0 s number is not canon (§9 R6). `WARN` line MATCH;
  its two toasts ABSENT.

### 4.6 `_door_fold_check` (`:333-347`) ↔ `DoorFoldCheck` (`:191-211`)
`_fold_t > 0 → true`; per door `< 1.0 m` and `now - last > 6.0` → stamp,
`_fold_t = 2.2`, true. MATCH (Godot's 3D distance equals C++ Dist2D
because both hunter and door sit at height 0). ABSENT: `Sfx.thunk`,
caption `[IT FOLDS THROUGH THE DOORWAY]`, the <12 m toast. UE-ONLY risk:
C++ splits CSV rows on `,` (`:43`); a future locked-reason containing a
comma would shift `gap_x/gap_z`. Godot reads the typed `DOORS` const.
Low (§9 R14).

### 4.7 `_process` body language (`:376-483`)
Head track (11 m, ±1.05 rad, 3.5/s), gait, idle performance, fold pose,
strike pose — all presentation on the Godot rig. ABSENT by design (the
UE body is Phase 1/2 + anim). Listed once so the motion canon's "he
faces PATHS, not people" (AAA_BUILD_PLAN §1) is re-checked when the anim
layer lands: `_head_track` in the reference tracks the PLAYER; the
motion & sound canon says the after-fire body faces paths. That is a
reference-vs-canon conflict, not a port drift; "the code is the intent"
(PORT-BRIEF) vs a later canon revision. OPEN (§9 O2).

### 4.8 Harness scaffolding (UE-ONLY, fine)
`bTestForceNight/AF/Recording`, `TestRecordingOffAfter`,
`bTestSaveRoundtrip`, `bTestLoopFns`, `bTestInvariants`, tagged-target
resolution. One harness bug: `TestClock` is advanced by BOTH the
invariants driver (`:231`) and the recording-cutoff driver (`:258`);
with both flags set it runs at 2× (§9 R15).

---

## 5 · `harriet.gd` ↔ `AHarriet`

- Freeze spine (`:68-74` ↔ `:71-78`): `not on_air → return`; `_t +=
  delta`; `rotation.z = sin(_t*0.9)*0.04` ↔ `Roll = sin(T*0.9) *
  RadToDeg(0.04)`. MATCH (Godot z-rotation and UE Roll are both the
  side-to-side roll for a forward-facing figure).
- Prompt (`:77-80` ↔ `:25-29`): both strings MATCH verbatim.
- Cup rise `0.99 + 0.05 * min(day, 6)` (`:70`): no cup in `AHarriet`.
  PROGRESS 0.8b-5 says "cup rises by the day" is done; the C++ has no
  cup and no mesh. If it lives in a Blueprint the source of truth is off
  the audit's path — OPEN (§9 H2).
- Collision: Godot Harriet is an `Interactable` (StaticBody3D) with a
  capsule r=0.3 h=1.6 at y=0.8 (`:42-48`). `AHarriet` has a bare
  SceneComponent root and no collision (`.cpp:7-11`), so Rita's
  ECC_Visibility reach ray (`RitaCharacter.cpp:97`) cannot hit her.
  DRIFT, medium (§9 H1).
- `interact` (`:83-121`): dead check (H2 toast), break branch (slip
  arming at `day >= 2`, A06, the "She does not resume…" toast, slip take
  sets `harriet_slip = true` + `_h1_pending`), ON AIR: `h2_pending`
  splice (2.8 s, caption `[ONE FRAME LEFT OF HERSELF]`, `mark_casualty
  H2`), `_h1_pending` (2.4 s, caption `[A REEL, LABELED IN HER HAND: ME]`,
  `mark_casualty H1`), LINES cycle (4 lines). C++ logs one line. ABSENT
  by stated scope (`Harriet.h:3-4`); the `harriet_slip` write is the
  only way `bHarrietSlip` ever becomes true in UE, so `SignLog`'s slip
  branch is currently dead code (§9 H3).
- `_process` (`:17-25`): dead → hide, or H2 → splice ghost. ABSENT (§9 H3).

---

## 6 · `player.gd` ↔ `ARitaCharacter`

- Movement: `wish = basis * (x,0,y) * SPEED * (0.55 if crouching)`;
  `velocity.xz = move_toward(velocity, wish, ACCEL*delta)` — symmetric
  accelerate/decelerate at 10 m/s², no friction term (`:59-62`). C++:
  `MaxWalkSpeed 310`, `MaxAcceleration 1000`,
  `BrakingDecelerationWalking 1000`, `MaxWalkSpeedCrouched 170.5`
  (`:21-24`). Top speeds MATCH (0.8b-1 proved 3.10 / 1.71). Braking:
  UE's CharacterMovement applies `GroundFriction` (default 8) on top of
  braking deceleration unless `bUseSeparateBrakingFriction`; the stop is
  sharper than Godot's. Not a knob in canon; DRIFT, low (§9 P3).
- Gravity: Godot `12.0` (`:55`); UE default 980 uu/s². DRIFT (§9 P2).
  Rita never leaves the floor in the reference, so exposure is stairs
  and the yard only.
- Look: Godot `MOUSE_SENS 0.0022 * clamp(GameState.mouse_sens,0.2,3.0)`
  rad/px, pitch ±1.3 rad (`:33-37`). C++ binds `Turn/LookUp` to the
  controller's default input scale, pitch to the engine default (`:54-55`).
  DRIFT (§9 P1). The settings clamp is PORT-NOTES §4 (ABSENT).
- Crouch: toggle on `crouch` just-pressed, camera lerps to `base - 0.6`
  at 12/delta, speed ×0.55, collider unchanged (`:56-60`). C++ toggle,
  `FInterpTo 12`, `Crouch()/UnCrouch()` which ALSO shrinks the capsule by
  30 uu (`:25`). MATCH on the ruled knobs (gap audit c045); UE-ONLY on
  the capsule (§9 P5).
- Eye height: Godot camera at y=1.6 over the floor (`scenes/main.tscn:67`).
  C++ 148 uu (`RitaCharacter.cpp:31`, comment "eye ~1.48m"). DRIFT — 12 cm
  on the scale-truth axis; the R-bar says judge at 1 m closeup (§9 P4).
- Inputs: Godot `ui_cancel → pause_requested`, `toggle_tbc → set_tbc`,
  `interact` (`:43-48`), plus `respond/improvise/map` in `REMAP_ACTIONS`.
  C++ binds `Crouch`, `Interact` only (`:56-57`). ABSENT: pause (LAW 9),
  TBC toggle, respond, improvise, map; the `locked` flag the HUD uses to
  freeze Rita during the retake (`hud.gd:276,304`) (§9 P6).
- Interact: camera-forward ray of REACH, `hit is Interactable` →
  `interact(self)` (`:66-77`) ↔ line trace + `IRestorationInteractable`
  (`:89-110`). MATCH; extra `INTERACT` LogLines are UE-ONLY telemetry.

---

## 7 · `capture_bench.gd` + `bench_tv.gd` ↔ `ABenchCapture`

- Prompt strings MATCH verbatim (`:16-19` ↔ `:30-39`).
- `interact` (`:22-37`): `_running` guard → `recording = true` →
  `recording_left = 12` → AF teach teleport if `af_active and not
  af_taught` → `demo_mark` → `_t` → `_player` → `tv.stage.play_tape` →
  `set_capture_status("CAPTURE · TAPE %d · 00:%05.2f")`. C++ (`:41-68`):
  guard (+ null player) → `bRunning`, `Player`, `T` → `bRecording`,
  `RecordingLeft` → teleport → LogLine. Effective order MATCH (the
  reorderings are between independent writes). ABSENT: `demo_mark`,
  the TV stage, `capture_status` (LAW 10: "the countdown is visible").
- Tick abort (`:46-53` ↔ `:98-108`): `> TETHER` → stop → `recording =
  false` → status "" → toast. MATCH; C++ additionally zeroes
  `RecordingLeft` (Godot leaves it stale — harmless, UE-ONLY tidy).
- Tick completion (`:55-62` ↔ `:110-124`): Godot `log_capture("TAPE %d ·
  A CLEAN SIGNAL")` → append {name, tape, **at = datetime**} → **save_log**
  → notify; DEMO → `demo_ended`. C++ builds the capture inline with
  `At = "BENCH"`, appends, LogLines — **does not call the existing
  `LogCapture()` and does not `SaveToSlot`**. DRIFT, medium — a completed
  capture is lost on quit until the next unrelated save (§9 B1, B2).
- Reel spin (`:44-45`), `bench_tv.gd` (CRT shader with `tbc_on`,
  `photo_safe`, `generation`; slate; `lunge_happened → toast + demo_mark`)
  — presentation, ABSENT. Note for the presentation half: the ONE STARTLE
  (LAW 2) is `stage.lunge_happened`; the CRT shader → "material function
  stack with the same parameter names" (migration map) must carry
  `tbc_on`, `photo_safe`, `generation`.

---

## 8 · `broadcast.gd` ↔ `URestorationClock`

- 50 / 18, starts ON AIR, flip emits `phase_changed(on_air)`. MATCH.
- Godot decrements in `_process` (frame-accurate, pauses with the tree);
  C++ uses a one-shot timer re-armed on flip (`.h:34-47`), for the
  simulate-world reason its header states. Equivalent cadence; a paused
  game must pause the timer (default `SetTimer` respects game pause —
  fine). MATCH.
- `time_left()` and `phase_text()` ("● ON AIR · break in 0:%02d" / "○
  BREAK · window closes 0:%02d", `:23-31`) ABSENT. The wall clocks and the
  HUD read them; `GetTimerRemaining(PhaseTimer)` can supply it (§9 C1).

---

## 9 · THE DRIFT CHECKLIST (tick as the Mac lane fixes each)

Severity: **H** changes a LAW-bound behavior or a saved value; **M**
changes gameplay the fixtures could observe; **L** cosmetic, format, or
tidy. Every box cites the line pair it came from above.

**STATE — `RestorationState`**
- [ ] **S1 (L)** Timestamp format: write `signed`/`at` as ISO
      `YYYY-MM-DDTHH:MM:SS` (`FDateTime::Now().ToIso8601()` minus the
      zone suffix) so a Godot-written v16 log and a UE-written one carry
      identical values (§2.1). OPEN: whether `presigned=false` may be
      serialized on ordinary signatures or must be omitted as Godot omits it.
- [ ] **S2 (M)** Boot: `Initialize()` must `LoadFromSlot()` after
      `SeedPaper()` as `_ready()` does; on `Version < 16` re-save at 16
      as `load_log` does (§2.3, §2.6).
- [ ] **S3 (M)** Toasts are canon text ("through `tr()` + glyphs",
      PORT-NOTES §6): every LogLine that replaced a `toast()` in §2.4
      (slip, READ, already-carried, TAKEN, MORNING, NIGHT, PROTOTYPE
      COMPLETE) also needs the `notify` delegate with the verbatim string.
- [ ] **S4 (M)** Declare the 16 missing delegates of §3 with the Godot
      names and parameter types; fire `log_signed` and `log_refused` from
      `SignFinish`/`SignLog` in the order §2.4 gives.
- [ ] **S5 (L)** `OnNightChanged` must be its own `bool` delegate, not a
      reuse of `FOnSheetChanged(int32)` (§2.4 `set_night`).
- [ ] **S6 (H)** `Strike()`: compute `lost = ITEM_ORDER[ItemsLost]`
      before incrementing (the 7 names are canon; the dresser and the
      NG+ relic read them) and broadcast `captured(Take, false, Lost,
      RespawnPoint())` in the non-full branch (§2.4 step 3, 6).
- [ ] **S7 (H)** `Strike()` non-full branch must `SaveToSlot()` between
      `Dailies.Add` and `OnSheetChanged` (`game_state.gd:502`) — a strike
      is a save point in the reference; the C++ one is not (§2.4 step 6).
- [ ] **S8 (M)** `bInRetake` semantics: Godot holds it TRUE until the
      retake presentation ends (`hud.gd:306`) and, after a full sheet,
      until `reset_new_game`. C++ clears it inside `Strike()` and stands
      in with a 3.0 s `StrikeCooldown` in `ARundown` (R6). When 0.8b-5's
      retake presentation lands, move the clear to the presentation's end
      and delete the cooldown. OPEN (ruling recorded in 0.9d as UE-R1):
      whether a full sheet ends the RUN (Godot: no further strikes) or
      resets the sheet and continues (UE today). The 0.9d ledger chose
      the latter deliberately for the fixture; canon's "fail forward"
      (I06) is about the premiere, not the sheet. Needs the owner's word.
- [ ] **S9 (L)** Live fields absent: `coverage_label`, `screening_active`,
      `map_points`, `fader_self`, `mouse_sens`, `ui_scale`, `captions_on`,
      `assist_on` (§2.2) — add with the systems that own them.
- [ ] **S10 (—)** The 36 unported functions of §2.5 remain the §6 tail;
      `is_dead`/`cause_of` (LAW 7), `show_caption` and the pause path
      (LAW 9), `set_tbc` are the ones the already-ported actors would
      call first.
- [ ] **S11 (L)** `Mode` is a raw `int32` with the enum values in
      comments; an `enum class ERestorationMode : uint8 { Matinee=0,
      LateNight=1, OneTake=2 }` keeps the save int identical and removes
      the magic numbers at `.cpp:43,49,174`.

**RUNDOWN — `ARundown`**
- [ ] **R1 (H)** `ReportNoise` must apply `_on_noise`'s four gates
      (`rundown.gd:128-134`): ignore if `State->InDeadRoom(Pos)` (LAW 11,
      room bible DEAD ROOM "deaf to noise"); ignore unless `bIsNight`;
      ignore if `bPremiereLive`; hear only if `Dist(Pos, Me)/M < Loudness
      * 3.0`. The lambda at `Rundown.cpp:65` must pass the loudness
      through (`ReportNoise(const FVector&, float Loudness)`). The 0.9c
      fixture fires `ReportNoise` directly and sets night, so it keeps
      passing.
- [ ] **R2 (M)** BREAK relocation: add the SPRINTER branch (nearest anchor
      to the player) when the director ports; until then the cycle
      branch's `(profile UNKNOWN)` is an honest placeholder — keep it.
- [ ] **R3 (L)** First heard relocation: `Achievements.unlock("A08")` +
      toast "It changed direction. You were not quiet." (`:178-181`) —
      with the achievements system (C14 audits it against LAW 3/5).
- [ ] **R4 (M)** Subscribe to `OnNightChanged` and port `_on_night`
      (`:137-143`): show/hide, teleport to `SegmentAnchors[SegIdx]`,
      `bWarned = false` at nightfall.
- [ ] **R5 (M)** Initial visibility: `BeginPlay` must
      `SetActorHiddenInGame(!State->bIsNight)` as `_ready` sets `visible =
      is_night` (`:124`). Without it the daytime re-arm at `:307` fires
      on boot and burns `bAfTaught` with no contract shown (§4.5 (5)).
- [ ] **R6 (M)** Remove `StrikeCooldown = 3.0f` and the post-strike
      `SetActorLocation(anchor)` (`:394-395`) once S8's latch and the
      retake presentation's player respawn exist; neither number nor
      teleport is in `rundown.gd:305-322`. Until then, document both as
      harness stand-ins in the header (they are not).
- [ ] **R7 (L)** `FoldT` decrement placement: Godot only ticks it inside
      the contract, the AF break-move, and the crossing; C++ ticks it at
      the top of `Tick`. Align, or record the ≤2.2 s edge as accepted.
- [ ] **R8 (M)** BREAK move: gate `DoorFoldCheck` on `State->bAfActive`
      as `rundown.gd:296-300` does. The pre-fire stage body pays no toll.
- [ ] **R9 (L)** `RELOCATE toward heard noise at %s` payload: Godot
      prints rounded metres `(x, y, z)`; C++ prints uu `X= Y= Z=`. Print
      `HeardPos/M` rounded in Godot's form so logs diff cleanly.
- [ ] **R10 (L)** Anchors are hardcoded (`:24-25`) though the world is
      "BUILT FROM DATA" (AAA_BUILD_PLAN §1; migration map "world built
      FROM Data CSVs"): read `Data/Rooms.csv` rows for TAPE LIBRARY /
      STUDIO A / PATCH BAY at `BeginPlay`, as `_anchor()` reads `rooms`.
- [ ] **R11 (—)** Director profiles (HIDER warn 5.0, CHECKER rig kill
      <14 m, any rig <9 m), cascade narrowing `max(3.5, warn-1.5)`:
      ABSENT with `coverage_director.gd`; the two rig-kill toasts are canon
      text.
- [ ] **R12 (—)** Premiere/crossing block (`:204-233`): ABSENT (Phase 5).
      `AfCrossingSpeed` is already declared; `crossing_caught` sets
      `_strike_pose_t` and emits `run_ended(dailies.size())` — note the
      argument is the DAILIES COUNT, not `strikes`.
- [ ] **R13 (—)** Presentation on the hunter: eye light 1.6 while
      `bAfActive && bRecording` else 0 (LAW 10, the same fact), the three
      captions (`[THE JAW WORKS ITS LEVER]`, `[IT FOLDS THROUGH THE
      DOORWAY]`), `_work_jaw` two-beat, `Sfx.thunk` cadence 1.1 s
      (approach) / 0.7 s (crossing), the WARN toasts, the felt-door toast.
- [ ] **R14 (L)** `Doors.csv` parse splits on bare commas; a locked
      reason with a comma would shift columns. Use a quoted-CSV parser
      or assert `Cols.Num() == 7`.
- [ ] **R15 (L)** Harness: `TestClock` is shared by two drivers
      (`:231`, `:258`); give the recording-cutoff driver its own clock.

**HARRIET — `AHarriet`**
- [ ] **H1 (M)** Add the capsule collider (r 0.3 m, h 1.6 m, centre
      0.8 m up; `harriet.gd:42-48`) so the reach ray can reach her.
- [ ] **H2 (OPEN)** The cup (`0.99 + 0.05*min(day,6)`) is ticked in
      PROGRESS 0.8b-5 but is not in the C++. If it is a Blueprint, name
      it in the ledger; if not, it is unticked work.
- [ ] **H3 (—)** `interact` and `_process` bodies (§5): slip arming
      `day >= 2`, `harriet_slip` write, A06, H1/H2 casualty flows with
      their two captions, LINES cycle, dead-state hide/splice. The slip
      write is what makes `SignLog`'s slip branch reachable.

**RITA — `ARitaCharacter`**
- [ ] **P1 (M)** Look: yaw/pitch = `0.0022 rad/px × clamp(mouse_sens,
      0.2, 3.0)`; pitch clamp ±1.3 rad (`player.gd:34-37`). Set
      `PlayerCameraManager` ViewPitchMin/Max = ∓74.48° and scale the
      axis input, or bind through Enhanced Input with the same scalar.
- [ ] **P2 (L)** Gravity 12.0 m/s²: `GravityScale = 12.0/9.8 ≈ 1.2245`,
      or record the engine default as an accepted divergence.
- [ ] **P3 (L)** Braking: set `GroundFriction = 0` and
      `bUseSeparateBrakingFriction = true` with
      `BrakingFriction = 0` so `BrakingDecelerationWalking = 1000` alone
      decelerates, as `move_toward` alone does in Godot.
- [ ] **P4 (M)** Eye height 1.60 m over the floor (`main.tscn:67`), not
      1.48: camera relative Z = 160 − 88 = 72 uu (crouch drop unchanged).
- [ ] **P5 (L)** `Crouch()` shrinks the capsule; Godot's does not. Keep
      (it is the honest body verb the gap audit rules) but note that
      the crouch-height capsule can pass where the reference cannot;
      QA-58 / I31 guard the promise.
- [ ] **P6 (M)** Bind `ui_cancel → pause_requested` (LAW 9: pause ships in
      every build), `toggle_tbc → SetTbc`, and the `respond`, `improvise`,
      `map` actions; port the `locked` flag the retake presentation and
      `run_ended` handler set (`hud.gd:276,304,312`).

**BENCH — `ABenchCapture`**
- [ ] **B1 (M)** Completion must call `State->LogCapture(FString::Printf(
      "TAPE %d · A CLEAN SIGNAL", tape))` (which appends, timestamps, saves
      and notifies) instead of building the struct inline without a save
      (`BenchCapture.cpp:117-121` ↔ `capture_bench.gd:59`).
- [ ] **B2 (L)** `At = "BENCH"` is not a value the reference ever writes;
      B1 removes it.
- [ ] **B3 (—)** `capture_status` countdown text `CAPTURE · TAPE %d ·
      00:%05.2f` every tick and `""` on stop (LAW 10: the countdown is
      visible and means both progress and expiry); `demo_mark` /
      `demo_ended` with the DEMO flag.
- [ ] **B4 (—)** `bench_tv.gd`: CRT material with `tbc_on`, `photo_safe`,
      `generation` parameters by the same names; slate text; the lunge
      (LAW 2, the ONE STARTLE) with its toast.

**CLOCK — `URestorationClock`**
- [ ] **C1 (L)** Expose `TimeLeft()` (= `GetTimerRemaining(PhaseTimer)`)
      and `PhaseText()` with the two verbatim strings (`broadcast.gd:23-31`).

**OPEN (canon silent or conflicting — needs a ruling, not a guess)**
- [ ] **O1** S1's question: must a UE-written save be field-for-field
      identical to the Godot JSON (including omitted optional keys), or
      only value-identical for keys present?
- [ ] **O2** `_head_track` in `rundown.gd:443-455` turns the head toward
      the PLAYER within 11 m; the motion & sound canon (AAA_BUILD_PLAN §1)
      says the after-fire body "faces PATHS, not people" while "the eye
      alone tracks". PORT-BRIEF says the code is the intent; the canon rev
      is later. Which wins for the UE anim layer.
- [ ] **O3** S8's question: does a full sheet end the run (reference) or
      reset it (UE-R1)?
- [ ] **O4** `AF_HEIGHT = 3.35` and `BASE_HEIGHT = 2.6` exist only to scale
      the Godot rig; the UE import is 3.08 m (PROGRESS 0.3). Already
      raised in GATE-0.10 ruling 1b; the C++ has no equivalent and should
      not until ruled.

Counts: 44 boxes — 3 H, 14 M, 15 L, 7 scope-only (—), plus 5 OPEN
(H2 and O1–O4). Zero knob numbers differ where a C++ home exists (§1);
the drift is in gates, order, signals and stand-ins.
