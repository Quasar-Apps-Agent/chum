# PORT NOTES · MECHANICS — Phase 4 enumerated from the canon and the code

**Unit 4.0 (CLOUD-OK).** Every mechanic the canon names, boxed for Phase 4 of
`PROGRESS.md`, with the Godot reference script that IS its specification
(PORT-BRIEF law: the GDScript reads as exact pseudocode; where prose and code
disagree, the code is the intent), the numbers it runs on, the save fields it
owns, the QA lines that accept it, the invariants that guard it, and its UE
home per `docs/packet/portbrief/UE5-MIGRATION-MAP.md`.

Sources read whole for this enumeration: the design doc (Parts IV, IV-B, V),
the game master (every scene, the scare compendium, the solutions matrix, the
tunables), the walkthrough (fail conditions, saves, the take, the sheet, the
endings board), the player routing, the room inventory, THE-LAWS, BUILD-ORDER,
the after-fire canon, the casualty ledger, the reaction matrix, the gap audit
RULINGS, the QA regression (QA-01..61), the invariant suite (I01..I31), the
achievements design (A01..A28), the accessibility matrix, the controls map, the
demo cut plan, the spike briefs, and all 73 scripts under `scripts/`.

Verification for a text unit is an assert script: `tools/verify_mechanics.py`
proves that every script is claimed by a box, every QA line and invariant is
assigned, every `Timings.csv` constant is homed, and every `4.x` box here
matches a `4.x` box in `PROGRESS.md` one to one. Run it after any edit to
either file.

Status vocabulary: **BUILT cNNN** = in the Godot reference at that commit;
**PORTED unit** = already in `ue/Restoration/Source` from that Phase 0 unit;
**CANON-ONLY** = written, never built (a RULING box in §2, per the gap audit's
precedent: consult the rulings before re-deciding anything).

---

## 0 · WHAT PHASE 4 DOES NOT OWN (already boxed elsewhere; not re-boxed)

| Mechanic | Owner box | Reference scripts | Note |
|---|---|---|---|
| State, the v16 log, signals | 0.8a, 0.8b-3 | `game_state.gd` | `ue/PORT-NOTES-STATE.md` is the schema; 4.x boxes below cite the fields they own |
| Broadcast clock ON AIR 50 / BREAK 18, wall repeaters | 0.7 | `broadcast.gd`, `wall_clock.gd` | `URestorationClock` present; `phase_text()` on walls is world text |
| The Rundown brain: segments, warn 7.0 / strike 2.2, savor at 3, no-strike-thru-wall, BREAK relocation, ReportNoise, the 2.2 s fold | 0.7 | `rundown.gd` | night-hunt extras that ride the same tick (camera kills, director biases, cascade shrink, the performance idle) are enumerated in 4.3, 4.7, 4.8 |
| The after-fire layer: 0.8 m/s approach, 1.2 m loom, the cool 2.0 / 4.0, tally eye while recording, dead-room hold, THE LAST CROSSING's hunter half | 0.8a | `rundown.gd` | the crossing's fader and timer half is 4.25 |
| Rita: 3.1 m/s, crouch 0.55 / 0.6 m, reach ray, input map | 0.8b-1 | `player.gd` | crouch is a body verb (I31, QA-58) |
| Bench capture 12 s + 4 m tether, `IRestorationInteractable` | 0.8b-2 | `capture_bench.gd`, `interactable.gd` | I09 abort never costs a daily |
| Paper economy, stations S1..S5, respawn at last signature, retake presentation (captured + run-ended), Harriet's freeze and rising cup, the day/night lever, the screening + ASSIST | 0.8b-4 | `log_station.gd`, `bed_prop.gd`, `harriet.gd`, `screening_event.gd`, `cue_sign.gd`, `hud.gd` (`_on_captured`, `_on_run_ended`) | QA-05..09, QA-18 (beat half); Harriet's GRAVES are 4.23 |
| Harness: bots, telemetry parsers, INVARIANTS.txt | 0.9 | `soak_runner.gd`, `bot_driver.gd`, `invariant_parser.gd`, `liveness_check.gd` (log side) | I01, I02, I22 machine-checked |
| World from data: rooms, doors as slabs, stations, monitors | 0.5, 0.6, 0.6b | `world_builder.gd`, `monitor_rig.gd` (the wall) | every 4.x box names its spawn site in `world_builder.gd` |
| Audio: the synth one-shots and room tones | 5.1 | `sfx.gd`, `tone_emitter.gd` | bell partials, thunk, tick, hum, coil, segment tones |
| Art reference, dev tools | Phase 1 / 2 (Blender factory) | `character_kit.gd`, `prop_kit.gd`, `arm_preview.gd`, `cast_preview.gd`, `head_preview.gd` | superseded by the factory; kept runnable |
| The reaction matrix QUEUE (M-R1..6, V-R1..3, H-R1..2, F-R1..2, L-R1, B-R1..2) | 4.WEB (legacy box, kept) | none built | none of the QUEUE items exist in code; `grep` for H-R2 / F-R1 / M-R finds nothing |

---

## 1 · THE PHASE 4 BOXES

Grouped by BUILD-ORDER milestone. Each box: canon · reference · numbers ·
state · accepts · UE home · deltas.

### P3 remainder · the tape half of the loop

#### 4.1 THE TAPE WORLD · the bench monitor, the tape stage, and the one startle · BUILT c008/c020
- Canon: design doc Part II (the two render worlds), Part IV §1 (capture: the
  player must sit with the content), THE-LAWS 2 (ONE STARTLE: the in-tape
  lunge), dread doctrine L5, invariant I14, the demo cut plan (the lunge is
  the demo's only scare).
- Reference: `bench_tv.gd` (the CRT shell; `set_generation`,
  `set_temp_generation`/`restore_generation` so the seance wear ladder never
  overwrites the dialed knob; `_on_tbc`; `_on_lunge`), `tape_stage.gd`
  (`play_tape(12.0)` runs Tape 1's timeline to the approach, the hold, the
  single-frame lunge and bars; `play_screening`, `play_fire`,
  `set_seance_frame`; emits `lunge_happened`), `gen_knob.gd` (MASTER / 1ST
  DUB / 3RD GEN; "the picture obeys; the scope does not"; A03),
  `shaders/crt_tape.gdshader` (chroma, scanlines, noise, tracking band,
  head-switch, dot crawl, vignette; parameters `generation`, `tbc`,
  `photo_safe`).
- Numbers: hold 3.2 s before the lunge (playtest V2 knobs: approach 1.35,
  hold 0.78..0.12, lunge scale 1.45); V3 noise floor 0.03, chroma 0.0012,
  band 0.16; V4 steady factor 0.7.
- State: `tbc_enabled`, `photo_safe` (saved, survive NEW GAME); signals
  `tbc_changed`, `photo_changed`.
- Accepts: verdicts V2 / V3 / V4 (playtest protocol); I14 (review rule: no
  other startle-class event, ever); A03.
- UE home: Material Function stack on the feed RT with the same parameter
  names via a Material Parameter Collection; the diorama as a sublevel with
  its own SceneCapture; Scare 1 as a Level Sequence with a one-frame lunge
  track (migration map: TAPE SHADER, TAPE STAGE).
- Delta: none against code. Real footage replaces the diorama when the
  puppet shoot exists (Gate 0 Memo 4 is unsigned).

### P4 · the hunter's nights (beyond 0.7 / 0.8a)

#### 4.2 THE NOISE BUS · hearing, attribution, and the deaf room · BUILT c021/c037
- Canon: design doc §3 (audio localization), spike 4, invariants I22 and
  I25, after-fire canon THE TWO HIDES ("noise born inside it does not exist
  to his ears"), QA-13, QA-38.
- Reference: `noise_tracker.gd` (player footsteps: `noise(pos, 6.0)` every
  0.6 s while moving > 0.5 m/s, nights only, not during the premiere),
  `door.gd` (`noise(pos, 8.0)` on every swing), `game_state.gd`
  `_sign_finish` (`noise_event(respawn_point(), 4.0)` on every signature),
  `rundown.gd` `_on_noise` (ignored if `in_dead_room(pos)`, if not night, or
  during the premiere; heard when `distance < loudness * 3.0`; remembered
  12 s; at the next BREAK the relocation picks the segment anchor nearest
  the heard position and logs `RELOCATE toward heard noise at <pos> ->
  segment N`; first time ever: A08 + the line "It changed direction. You
  were not quiet.").
- State: `noise_event(pos, loudness)`; `_heard_once` is session-only.
- Accepts: QA-13 (within 12 s it relocates toward the noise; the line fires
  once per run); I22 (attributable), I25 (deaf to the dead room, bot signs
  and slams inside).
- UE home: `ARundown::ReportNoise` exists (0.7); the three emitters do not.
  Footsteps and doors report through it; the sign-log noise is the wiring
  the state notes already flag.
- Delta: A08 fires from the Rundown, not from the state; keep it there.

#### 4.3 CAMERA FEEDS · power, kills, re-patch, and the on-camera law · BUILT c002/c006/c009
- Canon: design doc §2 (tally logic: a camera protects only while live and
  feeding a monitor), THE-LAWS 1 (ON CAMERA IS SAFE), walkthrough V-B (a
  camera it stares into overloads and dies), spike 2 (the wall passed in
  0.6b), invariant I05, QA-14, scare 6 (the camera-kill witnessed).
- Reference: `monitor_rig.gd` (SubViewport feed onto a CRT shell;
  `set_powered`, `set_killed` with the NO SIGNAL / KILLED · RE-PATCH AT PB
  card; `sync_to(tex)` for the lockdown; group `rig`), `rundown.gd`
  `_on_phase` (each ON AIR at night: every rig within 9.0 m of him dies,
  "Somewhere, a camera dies. The map is shorter tonight."; a CHECKER's
  most-watched rig within 14.0 m dies first with the log line `KILL
  most-watched rig`), `patchbay_console.gd` (`_any_killed` → "dead feed on
  the board · re-patch (E)" revives the control rig), `cascade.gd`
  `_kill_range`, `night_trip.gd` (kills rig 0).
- State: `killed` is session-only (kills do not persist; a reload heals the
  board).
- Accepts: QA-14 (patchbay revive works), I05.
- UE home: `USceneCaptureComponent2D` → RT per feed (0.6b's `spike_wall.py`
  rig is the pattern); kill = unassign the RT and show the card.
- **Delta, flagged:** QA-14's first clause ("standing in an active camera
  cone prevents the strike") is NOT in the reference night hunt. `rundown.gd`
  strikes on distance and the wall raycast only; the on-camera guards that
  exist are `recording` (I23, 0.8a) and `premiere_live` (I03). I05's own
  status admits it: "ENFORCED by I03's guard at prototype grain; re-verify
  when hunting and premiere ever coexist." Porting this box as written keeps
  that gap. Cone safety in the night hunt is therefore a RULING item, 4.R2.

#### 4.4 THE PATCHBAY · routing v0 and the two-circuit budget · BUILT c004/c006
- Canon: design doc §2 (the patchbay and the power budget), routing doc
  MOVEMENT GRAMMAR 2 (mediated corridors are player-built roads), spike 6,
  room inventory PB.
- Reference: `patchbay_console.gd` (one budget, two circuits: CONTROL RUN
  or STAGE HALL live, the other dark; `_apply` toggles `control_lights`,
  `hall_lights`, and the control rig's power; prompt states what is live;
  the re-patch branch of 4.3; the cascade stages of 4.8; the V2 offer of
  4.16), `world_builder.gd` `_spawn_patchbay_circuits` and
  `_wire_cascade_console` (`_late_wire`, order-independent).
- State: none saved (routing is session-only; canon says routing changes
  die with the take, walkthrough Part V).
- Accepts: QA-14 (revive), QA-20 (the stages), spike 6's pass line.
- UE home: an actor with the same three branches; lights and rig power as
  references.
- Delta: the building-scale amperage budget is CANON-ONLY (4.R5).

#### 4.5 THE NIGHT TRIP · Night 1's first blood · BUILT c017
- Canon: master T2.7 (the breaker trips mid-route, the reflection cross, the
  hummed closing song), walkthrough scares 2 and 3, QA-19.
- Reference: `night_trip.gd` (arms while `is_night`, not tripped, not the
  premiere; at 20.0 s: `night_tripped = true`, save, kill rig 0, three
  toasts 2.8 / 2.4 s apart).
- State: `night_tripped` (saved; reset on new game).
- Accepts: QA-19 ("Night 1 trip fires once ever"), probe P9.
- UE home: a one-shot actor bound to `night_changed`.
- Delta: the reference stages scares 2 and 3 as this one beat; the routed
  blackout pursuit (REC → CTL → PB unmediated, first possible capture) is
  4.R9's table.

#### 4.6 THE FLOOR MANAGER · the you're-on watch · BUILT c017/c041
- Canon: design doc (the Floor Manager; hand signals as the telegraph),
  master App C (the complete spoken inventory: "In five, four..."; the
  signal glossary), walkthrough fail condition 4 (moving after the point),
  casualty ledger F1 / F2, QA-19, scare 5.
- Reference: `floor_manager.gd` (visible only `is_night and on_air and not
  premiere_live`; the body turns to face you; inside 9.0 m with the player
  facing him (`dot > 0.5`): `_pointed`, `_watch_t = 3.0`, label YOU'RE ON;
  moving faster than 0.4 spoils the take unless ASSIST + hold E; one point
  per night (`_pointed` resets on morning); interact marks D08; hidden when
  dead), `live_production.gd` `_f2_unlisted` (4.24), `hud.gd` `_end_dead_air`
  (F1 marked in the epilogue, 4.26).
- Numbers: 9.0 m, dot 0.5, 3.0 s (the canon "seek grace 3 seconds"), 0.4 m/s.
- State: casualty `FLOOR MANAGER`; D08 in `read_props`.
- Accepts: QA-19 (fails on movement, passes on assist-hold), QA-18 (hold E),
  probe P8.
- UE home: a pawn-less actor with a facing check; ASSIST reads the same
  state switch.
- Delta: the other six signals as mechanics are 4.R4; the post-F2 monitor
  haunt and freeze-check inversion are 4.R16.

#### 4.7 THE COVERAGE DIRECTOR · the thing that watches how you watch · BUILT c009/c021
- Canon: design doc Part IV-B §12, spike 5, invariant I21, playtest V5,
  build plan risk 2 (four booleans and a histogram, never learning).
- Reference: `coverage_director.gd` (nights only: `_moving_s` above 0.5
  m/s else `_still_s`; `_monitor_s` when within 3.5 m of a rig's screen and
  facing it (`dot > 0.6`), per-rig `_watched`; `profile()`: AUDIENCE until
  monitor 2 / move 4 / still 4 seconds, then CHECKER ≥ others, SPRINTER if
  move ≥ still, else HIDER; counters written to the state every 5 s;
  `reset_read` on `daily_burned`; `log_line` prefixes `[day N night]` to
  `user://coverage_log.txt`), `rundown.gd` (the reads expressed: CHECKER →
  most-watched rig dies first; SPRINTER → relocation toward the player;
  HIDER → warn radius 5.0; the profile string in every RELOCATE line).
- State: `cov_monitor`, `cov_move`, `cov_still` (saved), `coverage_label`
  (live; the binder reads it).
- Accepts: I21 (deterministic, every decision carries a reason string),
  V5, probe P5 (burning resets to AUDIENCE).
- UE home: a WorldSubsystem; counters in the SaveGame; the log is a plain
  append (migration map: COVERAGE DIRECTOR).
- Delta: blockings B/C, the poisoned well, poltergeist staging, and the
  mood law beyond the savor line are 4.R8.

#### 4.8 THE CASCADE · Night 4 end to end · BUILT c022/c040
- Canon: spike 6, master T2.7 / walkthrough Night 4, invariants I04 and I07,
  QA-10, QA-20, casualty ledger V2 (the cascade night is his window),
  reaction matrix (windows yield only to the cascade).
- Reference: `cascade.gd` (fires once when `is_night and day >= 4`, not
  done, not the premiere: `cascade_active = true`, blackout 0.55, rigs 2..3
  killed, 4.0 s, 16.0 s, blackout 0.75, rigs 4..5 killed, console stage 1;
  waits for stage 0; `cascade_done`, save, the circuit F line),
  `patchbay_console.gd` (stage 1 RESTORE CIRCUIT B, or GET VESS for the
  uncredited who used his insight; stage 2 RESTORE CIRCUIT C; blackout
  0.55 → 0.0), `liveness_check.gd` (every 5 s during the cascade: OK line
  or VIOLATION if the console is gone, to `user://liveness_log.txt`),
  `door.gd` (window holds waived while `cascade_active`), `rundown.gd`
  (warn radius `max(3.5, r - 1.5)` while the cascade runs).
- State: `cascade_done` (saved), `cascade_active` (live; present in C++).
- Accepts: QA-20 (C then B; restoring out of order refuses; waived holds),
  QA-10, I04, I07; A15 ORDER MATTERS.
- UE home: the same two actors (migration map: CASCADE AND LIVENESS); the
  blackout as a UMG scrim.
- Delta: none against code. Circuit F is text; it "cannot be de-energized"
  by fiction, and V2 pays that.

#### 4.9 DAILIES · Burn Your Dailies · BUILT c006/c009
- Canon: walkthrough V-B (strike recovery: a canister per capture in the
  stacks; degaussing fades her name; unburned canisters are the Director's
  scouting film), room inventory LIB / CLM, invariant I09 (0.8b-2), probe P5.
- Reference: `game_state.gd` `strike` (non-full: `daily_seq += 1`, append
  `{id, take}`, `daily_added`), `pick_daily` / `burn_daily` (strike −1 only
  if > 0; `daily_burned`), `mint_shortcut_daily` (take −1, the H2
  temptation of 4.23), `dailies_manager.gd` (spawns existing on load, new
  on `daily_added`; four SLOTS in the stacks, offset 0.4 m per wrap),
  `dailies_canister.gd` (single carry: "Hands full. One canister at a
  time."), `degausser.gd` (burns the carried take), `coverage_director.gd`
  `reset_read`, `objective_text` (the NIGHT · optional line).
- State: `dailies[]`, `daily_seq`, `carried_id`, `carried_take` (saved).
- Accepts: probe P5 (single-carry; burning resets the read), I17 (run end
  mints no daily: 0.8a), I09.
- UE home: canister actors from the SaveGame array; the degausser is an
  interactable.
- Delta: none.

#### 4.10 THE CASTING SHEET AND THE DRESSER · the two physical counters · BUILT c003/c004
- Canon: walkthrough V-B (the sheet on the studio wall; what each capture
  takes: one item, loupe last), master App D (the sheet's text), room
  inventory STA / DRM, invariant I16, QA-07, A19.
- Reference: `casting_sheet_prop.gd` (reads `strikes` of 4 with the cast
  names ALDER · BELL · PRICE · MERRICK), `dresser.gd` (seven boxes from
  `ITEM_ORDER`, visible while `i >= items_lost`; refreshes on
  `sheet_changed`; two stock-taking lines), `world_builder.gd`
  `_spawn_casting_sheet`, `_spawn_bed_and_dresser`.
- State: `strikes`, `items_lost` (0.8a's `Strike()` owns the arithmetic;
  the ItemsLost clamp bug is in the 0.8b-3 checklist).
- Accepts: QA-07 (loupe last of the seven), I16 (ordered, bounded, persists
  through run end), A19 at 7.
- UE home: two interactables reading the subsystem.
- Delta: canon's Matinee sheet of 7 is not in code (`full := strikes >= 4
  or mode == ONE_TAKE` in every mode; Matinee's mercy is unlimited paper
  only). Code is the intent until the owner rules otherwise (§3 table).

#### 4.11 THE GLIMPSE · once, ever · BUILT c018
- Canon: THE-LAWS 3, master T4.8, walkthrough IV (one direct-sight glimpse,
  under two seconds, undecidable), invariant I11 (S0), I30 (no achievement,
  ever), QA-25, achievements doctrine 2.
- Reference: `glimpse.gd` (Day ≥ 4 clears the fire door's `locked_reason`
  and sets `fire_unsealed` once with the anniversary line; at night, not the
  premiere, when the player enters the elbow rect `[-9.75, -16.0, 7.5,
  3.0]`: build the figure (a capsule, a bar, four strings), 1.8 s, free it,
  `glimpse_seen = true`, save, two lines), `world_builder.gd`
  `_spawn_event_wave` (hands it `_fire_door`).
- State: `glimpse_seen`, `fire_unsealed` (saved; reset on new game).
- Accepts: QA-25, probe P10 (relaunch, revisit, never refires), I11, I30.
- UE home: a trigger volume and a spawned actor; the figure is a Phase 1/2
  asset question, the contract is this box.
- Delta: none. Its name appears in no code file (Law 3) and must not.

#### 4.12 LOCKDOWN AND THE ROWS · Tape 4's turn · BUILT c012/c019
- Canon: master T4.10, walkthrough Tape 4 act climax, room inventory REC
  (sanctuary status revoked on conversion), invariant I18, QA-26, A20,
  scare 9.
- Reference: `lockdown.gd` (fires when `assets.size() >= 4 and is_night`;
  every rig `sync_to` rig 0's feed; exterior doors' reason becomes SEALED
  FOR BROADCAST · lock-in's just till air; Merle's line; `lockdown_done`,
  save; on ready with the flag set, `_apply(true)` re-applies silently),
  `rec_chairs.gd` (five chairs from CASUAL to ROWS, 1.6 s cubic tween once;
  rebuilt in rows on load; solid before and after), `coat_pegs.gd` (+0.35
  drift on lockdown, 4.29), `merle.gd` (CHAIR while `lockdown_done`).
- State: `lockdown_done` (saved).
- Accepts: QA-26, probe P11 (persist after reload), I18, A20.
- UE home: the same one-shot; `sync_to` = one RT on many screen materials.
- Delta: none.

### P5 · story gates and the finale

#### 4.13 KEYS AND DOORS · locks state their reasons · BUILT c002/c005
- Canon: invariant I08 (every locked door states its reason), THE-LAWS 6
  (window holds bind except during cascade), routing doc MOVEMENT GRAMMAR 3
  (break windows are traffic lights), room inventory (KEY BOARD: TRAINING
  and EDITH; the shed's QUIET ROOM key), QA-10, A16.
- Reference: `door.gd` (`locked_reason` + `required_key`: satisfied when
  `has_key`; `window_bound` doors read HELD FOR AIR while ON AIR unless
  `cascade_active`; the first key turn toasts once; 0.45 s cubic swing to
  −1.75 rad; thunk + noise 8.0), `key_item.gd` (`take_key(id, display)`),
  `world_builder.gd` `_spawn_door` (Doors.csv kinds `locked:<reason>|<key>`
  and `window`; DEMO reason overrides), `_spawn_keys` (EDITH and TRAINING
  on the kitchen KEY BOARD; QUIET ROOM felt-wrapped in the shed), the
  little door (group `little_door`, "Not yet. It closes on camera, in
  Tape 5.").
- State: `keys[]` (saved).
- Accepts: QA-10 (holds honored except during cascade), I04, I08 (data:
  Doors.csv locked reasons are already stamped in 0.6), A16 THE LONG WAY
  AROUND (QUIET ROOM key).
- UE home: door actors read Doors.csv (0.6 stamps the slabs; this box gives
  them hinges, keys, and the grammar).
- Delta: none. The FORCE tools (bolt cutters, the drill, the imperfect seal)
  are 4.R6.

#### 4.14 THE PRE-SIGNED PAGE · the save scare, singular · BUILT c011
- Canon: master T3.6, walkthrough Part V (THE SAVE SCARE: diegetic content,
  not interface deception; no save is ever actually lost), invariant I10,
  QA-21, A09.
- Reference: `log_station.gd` (S4, Day ≥ 2, `not presigned_seen`: three
  lines 1.6 / 1.8 s apart, then `mark_presigned`), `game_state.gd`
  `mark_presigned` (a signature `{S4, tape, "TOMORROW", presigned: true}`,
  save, `log_signed`; paper untouched).
- State: `presigned_seen`, the signature entry (saved; `respawn_point` reads
  the last signature, so S4 becomes the respawn).
- Accepts: QA-21 (zero paper: appears and saves free, once), I10, probe P6,
  A09 (hidden).
- UE home: a branch on the S4 station interactable (0.8b-4's station).
- Delta: none.

#### 4.15 THE FILM CABINET AND THE SEVEN SIGNALS · BUILT c006
- Canon: master T2.4 (PRESERVE: the TRAINING key; ASK: Harriet's seventh;
  FORCE: four of six), App C signal glossary, casualty ledger (the seventh
  is gated by Harriet's death), QA-41, A07.
- Reference: `film_cabinet.gd` (needs `has_key("TRAINING")`; runs the six
  in order 1.1 s apart via `add_show_signal`; `film_watched` once; "It never
  mentions a seventh."), `harriet_note.gd` (visible only after the film;
  hidden forever if Harriet is dead and the seventh unknown; marks D06,
  adds HOLD YOUR APPLAUSE, frees itself), `world_builder.gd`
  `_spawn_film_and_note`.
- State: `film_watched`, `signals_known[]` (saved).
- Accepts: QA-41 (unlearnable if her card was unfound), A07 at 7 signals.
- UE home: two interactables.
- Delta: the reference teaches the NAMES only; the signals as mechanics
  (STRETCH / WRAP IT UP / THIRTY / ON TIME / CUT / the seventh's three
  seconds) are 4.R4. The FORCE branch (pry it, four of six) is 4.R6.

#### 4.16 THE VESS CHAIN · the credit dilemma · BUILT c015/c040
- Canon: master T2.3 FORCE (the binder: one insight, one wrong theory) and
  T5.3 (the final breaker), casualty ledger V1 / V2 (paperwork is
  exposure, obscurity is abandonment), QA-42, A11, probe P13.
- Reference: `vess.gd` (four lines at the shrine; hides when dead),
  `vess_binder.gd` (D07; `vess_insight`; hides itself after), `credit_entry.gd`
  (visible only while insight and not credited; `vess_credited`), the V1
  sites: `decision_ledger.gd` `_v1_taken` (AUTHENTICATE while credited:
  the INK ripple, bars on all monitors, the fused pin) and
  `live_production.gd` (the credited living at the final breaker: farewell,
  the handle drops, lights held, casualty), the V2 site:
  `patchbay_console.gd` `_v2_taken` (GET VESS at cascade stage 1 for the
  uncredited who used the insight: eleven seconds, then circuit F,
  [MAINS HUM, SHAPED LIKE A STANDING PERSON]).
- State: `vess_insight`, `vess_credited` (saved); casualty `VESS`.
- Accepts: QA-42 (both triggers, both graves, the dead breaker, crossing
  62), A11, P13.
- UE home: three interactables and two hooks into 4.21 / 4.24 / 4.8.
- Delta: the margin's green bleed (Leland annotates him) is CANON-ONLY,
  4.R16.

#### 4.17 THE CRATE AND THE FRAME-SEANCE · every pass wears him · BUILT c010/c023/c042/c044
- Canon: design doc §7 (the Leland frame-seance; scarcity converts a puzzle
  voice into a person), master T4.4 (the five questions verbatim), casualty
  ledger L1 / L2, spike 3, invariants I19 (crate gate) and I20 (same frame,
  seeded), QA-22, QA-44, QA-50, A14, verdict V6, probe P16.
- Reference: `impossible_crate.gd` (visible Day ≥ 2 until opened;
  `crate_opened`; Vess's two lines), `seance_dock.gd` (visible only after
  the crate; Z back / X forward to MAX_FRAME 40; every step `add_wear(1.5)`;
  answers at frames 7 / 14 / 21 / 28 / 35 appended once to `leland_answers`
  (frame 14 reads SHE WAS THE ONLY ONE WHO PAUSED PROPERLY with Harriet
  dead; frame 28 reads I KNOW. SHE'S HERE NOW with Merle dead); the picture
  rides a temporary generation `min(2.0, wear / 30)` and the knob's dialed
  value is restored on close; past 70 wear the frame "tears a little more";
  SPACE with five answers and wear > 70 offers L1 THE SIXTH QUESTION (the
  ink leaves the paper; dock inert; casualty LELAND); Q with the fire tape
  in hand plays L2 THE READING (answers un-write, `has_fire_tape = false`,
  `signoff_completed = true`, casualty LELAND); inert when Leland is dead),
  `frame_sequence.gd` (320 × 240 frames built per index with grain seeded
  by index, cached; the swap point for real footage), `tape_stage.gd`
  `set_seance_frame` / `seance_end`, `bench_tv.gd` temp generation.
- State: `crate_opened`, `seance_wear` (float), `leland_answers[]` (frame
  indices), `has_fire_tape`, `signoff_completed` (saved).
- Accepts: QA-22 (crate before seance refuses; wear ladder degrades per
  answer), QA-44 (L1 offered only past five and 70; L2 consumes the tape
  and sets the completed sign-off), QA-50 (the grief answers), I19, I20,
  A14 at five, V6, P16.
- UE home: `UTexture2D::CreateTransient` per index with the same seeded
  generator, or an image-sequence Media Source stepped by frame; the wear
  ladder stays a material parameter (migration map: SEANCE SUBSTRATE).
- Deltas (code is the intent): wear is 1.5 per frame step, not the canon
  "7 per pass (3.5 Matinee)"; Matinee's halved wear is not in code; the 1A
  gate reads `seance_wear <= 70.0`, not "Leland Integrity ≥ 60". Recorded
  in §3.

#### 4.18 THE FIRE TAPE AND THE WAKE · the forced watch, no sting · BUILT c010/c035/c039
- Canon: master T3.4 (the centerpiece of restraint), after-fire canon THE
  REVEAL (watching the fire tape sets `af_active`), casualty ledger M1 THE
  SECOND VIEWING, invariant I15, QA-23, QA-33, QA-40, A13.
- Reference: `fire_tape_pickup.gd` (`has_fire_tape`), `fire_tape_dock.gd`
  (visible while the tape is held; first watch offers Merle once: E she
  stays, Q she goes (`merle_offered`); `play_fire(11.0)`; four lines; sets
  `fire_tape_watched`; sets `af_active` once with "Something answers the
  tape from three rooms away" and saves; if she stayed: the pat, the empty
  chair, the sentence finished from the speaker, [THE KETTLE, TWO ROOMS
  AWAY, CLICKS OFF], casualty MERLE), `world_builder.gd` (`FireTapePickup`
  in Craik's cage, `FireTapeDock` at the bench).
- State: `has_fire_tape`, `fire_tape_watched`, `af_active` (survives NEW
  GAME on purpose), `merle_offered` (saved).
- Accepts: QA-23 (no sting anywhere; watching marks the flag), QA-33 (the
  wake toast once; af_active persists), QA-40 (refusing saves her and never
  re-offers; consent plays the repossession), I15, A13.
- UE home: two interactables; `bAfActive` already exists in the subsystem
  (0.8a consumes it; this box is the only writer).
- Delta: none. M2 THE HOME SINGER, Merle's other grave, is 4.R11.

#### 4.19 THE SCENE DOCK · the contract room · BUILT c011
- Canon: THE-LAWS 4 (THE WARM ONE NEVER ACTS), master T4.3, walkthrough
  III.6 (nothing springs in the dock), invariants I12 and I19, QA-24, A10,
  probe P7.
- Reference: `dock_task.gd` (`setup` picks one random warm index unless
  already done; the clipboard prompt counts N of 6; on the last count
  `dock_done`, save, "six units, one anomaly, zero incidents"),
  `dock_chum.gd` (count by hand; the warm line writes the number down
  anyway), the gates it opens: `asset_pickup.gd` `needs_dock` (the CARD),
  `readable_prop.gd` `needs_dock` (D10).
- State: `dock_done` (saved).
- Accepts: QA-24 (filing all six completes with nothing following, on
  camera or off), I12 (a review rule on every future commit: no code path
  may exist), I19 (the card gates on the filed inventory), A10 (its text
  never mentions warmth), P7.
- UE home: two interactables; the rows are a Phase 3.20 room.
- Delta: none, and there must never be one.

#### 4.20 THE SIGN-OFF ASSETS · four berths above the bench · BUILT c012
- Canon: walkthrough VII (Sign-Off Assets 0..4: verse, card, cart, script),
  master T2.6 / T3.2 / T3.3 / T4.3, routing THREAD 1A step 1, invariant
  I19, the lockdown trigger (4.12).
- Reference: `spectro_dock.gd` (needs one capture; VERSE, three lines),
  `asset_pickup.gd` (CART in master control, SCRIPT in Craik's cage which
  also marks a readable via `read_id`, CARD in the props crate gated
  `needs_dock`; each frees itself once banked), `asset_rack.gd` (ORDER
  VERSE · CART · SCRIPT · CARD, a canister per banked asset),
  `game_state.gd` `gain_asset` ("ASSET BANKED · N of 4"; at four: "The
  finale has everything it needs, when night falls."), `objective_text`
  (Day ≥ 3: gather the four assets).
- State: `assets[]` (saved).
- Accepts: I19; the lockdown fires on four (4.12); the ASK alternative for
  the verse (Harriet hums it, one wrong word) is 4.R6.
- UE home: four pickups and a rack reading the array.
- Delta: none.

#### 4.21 THE DECISION LEDGER · three entries in her hand · BUILT c012/c015
- Canon: master T5.2, walkthrough VII (Ending Routing Summary), walkthrough
  named gap 4 (Merle in the doorway is the point-of-no-return signal, no
  modal), gap audit ruling 4 (the binder IS the inventory), A17, probe P14.
- Reference: `decision_ledger.gd` (ripens Day ≥ 3; E cycles AUTHENTICATE /
  DESTROY / PERFORM; SPACE commits only while the ledger is the reach
  target; the ink is final; D03; the V1 hook), `merle.gd` `_pen_up`
  (walks to DOORWAY while the pen is up and says nothing), `bed_prop.gd`
  (with a decision and the lockdown done, sleeping starts the finale:
  `start_finale`), `game_state.gd` `start_finale` (`finale_started`).
- State: `decision` (saved).
- Accepts: A17 INK, P14, walkthrough gap 4 as built.
- UE home: one interactable plus Merle's schedule (4.22).
- Delta: none.

#### 4.22 MERLE · on her schedule · BUILT c015/c018
- Canon: design doc (Merle; the casting-drift showcase), master T1.1 /
  T2.5 / T4.6 (the 1974 monologue verbatim), casualty ledger M1 / M2,
  reaction matrix (warmth is her instrument), QA-11, QA-40, A12, Merle
  casting breakdown (never warm-sinister).
- Reference: `merle.gd` (SPEED 1.6; KETTLE by day, CHAIR at night or after
  lockdown, the screening pull, DOORWAY while the pen is up; lines keyed on
  `decision` then `day`; the 1974 monologue after the crate, once,
  `merle_1974`; hidden when dead), `world_builder.gd` `_spawn_club`.
- State: `merle_1974` (saved); casualty `MERLE`.
- Accepts: QA-11 (kettle, chair, or DOORWAY per schedule and pen state,
  never elsewhere), QA-40, A12 (hidden), P14.
- UE home: a scheduled actor with three anchors.
- Delta: M2 THE HOME SINGER has no code (4.R11); the matrix's M-R1..6 are
  4.WEB.

#### 4.23 HARRIET'S GRAVES AND THE REJECTED EDIT · H1, H2, and T4.5 · BUILT c039/c044/c018
- Canon: casualty ledger H1 CONTINUITY / H2 THE SPLICE, master T4.5 (the
  rejected edit, played once, in full), design doc named gap 3, QA-41,
  QA-49, QA-50 (the frame-14 grief answer lives in 4.17).
- Reference: `harriet.gd` (H1: while frozen, Day ≥ 2, the second interact
  arms a slip; taking it sets `harriet_slip`, which `sign_log` spends as
  one free signature "in her hand"; at the next ON AIR interact she is
  absent, the cabinet will not close, [A REEL, LABELED IN HER HAND: ME],
  casualty; H2: with `h2_pending`, the next break doubles her, [ONE FRAME
  LEFT OF HERSELF], `_splice_visual` builds the ghost an inch left, rebuilt
  on load, one line forever; the freeze and cup themselves are 0.8b-4),
  `rejected_edit.gd` (visible after the crate: first, T4.5 in full with the
  reel stopping itself and Vess's two lines and the cobbler; after
  `rejected_seen`, the block offers the splice with her label disclosed:
  `mint_shortcut_daily`, `h2_pending`; hidden once she is dead or pending),
  `screening_event.gd` (tolerance 0.05 tighter without her),
  `harriet_note.gd` (the seventh gated by her death).
- State: `harriet_slip` (live), `h2_pending`, `rejected_seen` (saved);
  casualty `HARRIET` with cause H1 or H2.
- Accepts: QA-41, QA-49, the seventh-signal gate.
- UE home: branches on the Harriet actor and one bench interactable.
- Delta: none.

#### 4.24 THE PREMIERE · live production under sabotage · BUILT c014/c024/c041/c043
- Canon: design doc §9, master T5.3 (cues 1..5 verbatim; the Vess breaker
  variants), walkthrough V-B fail condition 5 and named gap 3 (the club
  must threaten the broadcast, never soft-lock it), casualty ledger F2 and
  THE ROWS, invariants I03 / I05 / I06, spike 7, QA-27, QA-43, QA-46,
  QA-51, comparative study QA-51 (braid, never queue).
- Reference: `live_production.gd` (`run()`: ending 0 intercept if all four
  living are dead; `premiere_live`, night forced; PLACES; the count; CUE 1
  on the mark (1.6 m) with PGM camera 1 via `cam_1..3`, SPACE; then
  `_pressure()`: one incident at a time from TALLY / HOUSE / BOOM / CARDS
  every `max(14, 26 − 4 · fail_takes)` s, HOUSE dims the scrim 0.35, the
  club auto-fixes anything left 40 s (fail-forward), fixtures fix by hand
  (AUX PANEL covers TALLY and HOUSE, BOOM WINCH, CARD STAND); CUE 2: the
  cart deck breaker, 45 s per take (ASSIST × 1.5), a failed take counts
  and takes a row seat; the TALLY lie refuses twice then accepts a blind
  call, the third blind call over the run is F2 (the unlisted camera,
  casualty FLOOR MANAGER); BOOM holds exactly once; the final breaker:
  credited living Vess → farewell and V1; dead Vess → fused pin, 30 s
  blackout retakes; uncredited → 30 s retakes "Again. The dark is
  patient."; the final break (4.25); CUE 3 the little door opened and
  closed by hand on camera; `premiere_log.txt` INCIDENT / RESOLVED lines
  the parser scores), `finale_breaker.gd`, `finale_fixture.gd`,
  `bot_driver.gd` `_fail` (0.9's FAIL-BOT), `rundown.gd` (yields the floor:
  invisible while `premiere_live` unless crossing).
- Numbers: interval 26 → floor 14; auto-fix 40 s (I06 caps 40 s); tally
  refusals ≤ 2; boom hold 1; cue 2 45 s; retakes 30 s; mark radius 1.6 m.
- State: `premiere_live` (live), `row_casualties` (saved), `fader_self`
  (live), casualties.
- Accepts: QA-27 (cue marks require the PGM camera; every incident
  fail-forwards within its guarantee), QA-43 (F2 exactly the third blind
  call; cue flow continues), QA-46 (rows cycle three lines, count persists),
  QA-51 (braid audit: a tuning defect if any peak is single-threaded), I03,
  I05, I06; spike 7's pass line.
- UE home: a GameMode-scoped director actor; cue marks as trigger volumes;
  the switcher as Enhanced Input actions; `premiere_log` unchanged
  (migration map: LIVE PRODUCTION).
- Delta: scares 11 (the plunge) and 12 (the delivery) are 4.R9; the club's
  hands-on restraint is text.

#### 4.25 THE FINAL BREAK · the divert, the fader, and the last crossing · BUILT c013/c038/c041
- Canon: after-fire canon THE LAST CROSSING (three outcomes, all hers),
  casualty ledger F1 THE FADER, routing THREAD 4 step 4, THE-LAWS 11 (the
  toll is the counterplay), QA-28, QA-43, invariant I19 (the divert gates
  on key plus answers plus the fire tape).
- Reference: `live_production.gd` (after the breaker: if
  `signoff_completed` the rundown simply ends → 4c; else if `has_key("QUIET
  ROOM") and leland_answers.size() >= 5 and fire_tape_watched`: SPACE
  places for cue three, Q diverts; `_fader_choice`: SPACE lets him hold it,
  E holds it yourself for 4.6 s (`fader_self`), a dead Floor Manager forces
  self-hold; `_last_crossing`: `crossing = true`, him placed at master
  control, 75 s (62 with Vess dead, −13 self-held), reached within 2.0 m of
  the little door / caught / late falls through to cue 3 with the window
  gone), `rundown.gd` crossing branch (PORTED 0.8a: 1.6 m/s, eye dark,
  folds still paid, caught = `crossing_caught`, "A hand the size of a
  door", `run_ended`), `hud.gd` `_end_dead_air` (4a HIS HAND with F1 marked
  in the epilogue, or 4b HER HAND with the arm stated flatly).
- State: `crossing`, `crossing_caught`, `fader_self` (live).
- Accepts: QA-28 (divert with the fire tape plays DEAD AIR; otherwise the
  committed decision's ending), QA-43 (the fader choice precedes the
  crossing; self-hold costs 13 s and routes 4b; his hold routes 4a; dead FM
  forces self-hold), I19, probes P22 / P23.
- UE home: the director actor's tail; the hunter half exists.
- Delta: none.

#### 4.26 ENDINGS, THE LEDGER READ ALOUD, AND CREDITS · BUILT c013/c034/c042/c043
- Canon: walkthrough VII (four endings, exact conditions) and the c043
  board (1A / 1B / 2 / 3 / 4a / 4b / 4c / 0), master THE ENDINGS SCRIPTED,
  casualty ledger THE FULL BOARD, THE-LAWS 5 (the bell rings once, at the
  finale beat) and 8 (the interface lie, exactly once), invariants I13,
  I28, I29, QA-03, QA-28, QA-45, QA-47, achievements A21..A25, A27, A28
  (4c carries none by ruling).
- Reference: `hud.gd` (`_on_finale` routes DESTROY → `_end_burn` (cold
  cobbler plated for two with Merle dead), AUTHENTICATE → `_end_producer`
  (the warm chair with Vess dead, the open headset with the FM dead, the
  welcome administered by the room with Merle dead; `mark_ending(..., true)`
  sets `lie_pending`), PERFORM → `_end_perform` (runs 4.24; caught returns
  to the run-ended path; `one_woman` → `_end_zero`; `signoff_4c` → `_end_4c`
  (lights down in reverse tour order, the tower light out as rest);
  `dead_air` → `_end_dead_air`; else `Sfx.bell()` once, the line on SPACE,
  then 1A if `leland_answers >= 5 and seance_wear <= 70 and Leland alive`
  else 1B with FILE UNDER: STAFF (Vess dead) and AND THE READER, UNFILED
  (Leland dead)); `_roll_credits` opens with THE LEDGER, READ ALOUD when
  anything is in it (name · cause · epitaph; TRANSITION UNRESOLVED for
  Harriet; fifty-eight minus N), `credits.gd` (SPEED 42, any key after the
  grace, the tower-light card, back to title), `game_state.gd`
  `mark_ending` (`finale_done`, `ending_reached`, `ending_marked`,
  achievements), `reset_new_game` (the NG+ relic: the last item lost stands
  on the set next run, unremarked), `world_builder.gd` (spawns the relic).
- State: `finale_done`, `ending_reached`, `lie_pending`, `ng_relic` (saved).
- Accepts: QA-03, QA-28, QA-45 (ending 0 intercepts at entry; nine cards,
  one name), QA-47 (every reading; a clean run reads nothing and A27
  files), I13 (with 4.36), I28 (string-compare at credits), I29 (S0 if a
  clean run reads anything); A21..A25, A27, A28; probes P25 / P26.
- UE home: UMG sequences driven by the same routing; credits as a widget.
- Delta: the ending-2 audition clause (PERFORM with fewer than four assets
  at PT ≥ 70) is unreachable in code because the lockdown (4.12) needs four
  assets before the finale can start: 4.R7.

#### 4.27 THE CASUALTY LEDGER · every death has a signature · BUILT c039..c044
- Canon: THE-LAWS 7 (new), the casualty ledger whole (ten authored deaths,
  the rows, the board), invariant I27, QA-39, playtest P24 / P25, lore
  architecture (consequence is exposition).
- Reference: `game_state.gd` `mark_casualty(who, cause, line)` (dedupe by
  who; "THE LEDGER TAKES IT DOWN."; day stamped), `is_dead`, `cause_of`,
  `all_cast_dead` (MERLE, VESS, HARRIET, FLOOR MANAGER), `hud.gd`
  `_fill_binder` (page one: NO ENTRIES. KEEP IT SO. or who · cause · Day ·
  epitaph), and every prop that honors the ledger: `merle.gd`, `vess.gd`,
  `floor_manager.gd` (hide), `harriet.gd` (hide or double), `seance_dock.gd`
  (inert when Leland is dead), `harriet_note.gd`, `rejected_edit.gd`,
  `credit_entry.gd` and the breaker variants.
- State: `casualties[]` `{who, cause, line, day}`, `row_casualties`
  (saved; 0.8b-3 adds the fields).
- Accepts: QA-39, I27 (force both Vess triggers in sequence: one entry, one
  toast), P24 (no death may feel unauthored).
- UE home: the subsystem's array plus `IsDead` checks on every actor above.
- Delta: the code holds NINE of the ten authored deaths (M2 is absent,
  4.R11); the ledger's AS BUILT paragraph says ten. The count is nine until
  M2 lands.

#### 4.28 READABLES D01..D11 · handled lore, three reads deep · BUILT c033/c035
- Canon: object taxonomy (HANDLED lore prompts and `mark_read`s; the Three
  Reads Rule), lore architecture (the shard model; the never-stated
  ledger: naming a protected truth in text is S0), props packet (the ten
  documents), after-fire canon (D11 after first sighting), A26, QA-59
  (Phase 3 sweeps placement).
- Reference: `readable_prop.gd` (visible from `needs_day`, optionally
  `needs_dock`; plays its lines; `mark_read(doc_id)`), `world_builder.gd`
  `_spawn_readables` (D04 the 1974 clipping, D05 the welcome packet, D09
  the fire marshal report Day 2, D10 Iris Bell's letter after the dock,
  D11 the Peak dossier Day 4 in master control) and the six sites that
  mark on use (D01 the seance reel, D02 with Craik's script, D03 the
  ledger, D06 Harriet's note, D07 Vess's binder, D08 the Floor Manager),
  `game_state.gd` `mark_read` ("N of 10"; A26 at ten; D11 is extra credit
  by ruling).
- State: `read_props[]` (saved).
- Accepts: A26 at ten documents, QA-59 (every ambient item exists, prompts
  nothing, never moves), the three-reads rule in review.
- UE home: readable actors; text from GameText.csv (4.39).
- Delta: none.

#### 4.29 L1 DRIFT · the coat pegs, and the cup · BUILT c016
- Canon: dread doctrine L1 (ambient wrongness: monotonic, never called out),
  design doc (the casting-drift wardrobe system: a legible-state system
  that never needs a meter), room inventory ENT, object taxonomy (dressing
  is the only drift-eligible tier), QA-11, QA-56.
- Reference: `coat_pegs.gd` (five coats lerp NEUTRALS → SHOW by `(day −
  1) / 4`, +0.35 after lockdown; three read lines by drift band),
  `harriet.gd` (the cup's height `0.99 + 0.05 · min(day, 6)`, 0.8b-4).
- State: none of its own (`day`, `lockdown_done`).
- Accepts: QA-11 (drift per day table), QA-56 (every drift instance is
  dressing tier).
- UE home: a material parameter on the coats driven by the subsystem.
- Delta: none. Every other drift instance the Room Bible authors is Phase 3.

### P6 · meta, modes, and the shell

#### 4.30 THE HUD WORLD-TEXT SET · BUILT c001..c035
- Canon: design doc Part III (world UI is broadcast engineering; meta UI is
  paperwork), after-fire canon THE COUNTDOWN, VISIBLE (one number, two
  meanings), accessibility matrix (color redundancy: the tally pairs glow
  with the REC line and countdown), QA-34, QA-38.
- Reference: `hud.gd` (prompt through `glyphs(tr(...))`; toast 3.0 s;
  TBC label; capture status line; clock DAY N · / NIGHT · + `phase_text()`,
  amber on air, green on break; SHEET · N/4; objective from
  `objective_text()` (the priority ladder as written, 0.8b-3 ports it);
  the tally lamp ● REC · SAFE WHILE LIT · SS.S while `af_active and
  recording`; captions bottom-right, 1.4 s hold then 0.6 s fade; the
  blackout scrim tweened 1.2 s on `blackout_changed`; the [NO ECHO] first
  dead-room entry toast and `deadroom_seen`; the crosshair).
- State: `deadroom_seen` (survives NEW GAME on purpose).
- Accepts: QA-34 (the lamp with a live countdown), QA-38 (first entry gives
  the radio toast and [NO ECHO]).
- UE home: UMG widgets bound to the subsystem's delegates (0.5's HUD shell
  is the stub this box fills).
- Delta: none.

#### 4.31 THE BINDER · TAB · BUILT c003/c006/c039
- Canon: design doc Part III (the ring binder: pause, settings, saves, the
  journal), gap audit rulings 3 (true-pause by day, LIVE-TIME during the
  premiere: wiring queued) and 4 (THE BINDER IS THE INVENTORY: no grid, no
  weight), QA-39.
- Reference: `hud.gd` (`ledger` action cycles three pages: closed; the
  ledger page (mode, signatures on file, the casualty ledger, sheet of 4,
  PRODUCER TRACK, keys, dailies and what is carried, coverage read, Leland
  wear and answers, photosafe, Vess's standing, signals known, the last
  five captures); the presentation form (1 / 2 / 3 switch MATINEE / LATE
  NIGHT / ONE TAKE live, TBC, controls)), `game_state.gd` `set_mode`.
- State: `mode` (saved; survives NEW GAME).
- Accepts: QA-39 (page one), probe P4 (mode switch in the binder form).
- UE home: a UMG widget over the same fields.
- Delta: the premiere live-time rule and the casting-drift stationery are
  4.R13.

#### 4.32 THE BOOTH · settings apart from the log · BUILT c028/c031
- Canon: THE-LAWS 9 (ACCESS IS CANON: the booth, captions, assist, remap,
  pause, and the deferral rule ship in every build of every engine), the
  accessibility matrix and conformance pass (R1..R7 shipped), controls map
  (remap covers five verbs today; the UE5 target is everything), QA-01,
  QA-16, QA-17.
- Reference: `options_panel.gd` (master volume on bus 0, mouse sensitivity
  0.2..3.0, fullscreen with the headless guard, TBC, photo-safe, UI text
  size 0.8..1.6, captions, ASSIST, five remap rows with press-a-key and
  conflict refusal KEY IN USE; `first_run` writes settings and shows BEFORE
  THE SHOW; O closes), `title.gd` (opens the booth over the title when no
  settings file exists), `game_state.gd` `load_settings` / `save_settings` /
  `rebind` / `key_name` (the `settings.cfg` contract in the state notes §4).
- State: `settings.cfg` only (never the log).
- Accepts: QA-01, QA-16 (every control persists; NEW GAME leaves settings
  intact), QA-17 (refuses a used key; new key shows everywhere).
- UE home: a `UGameUserSettings` subclass or a second slot, same keys;
  Enhanced Input for the remap.
- Delta: none.

#### 4.33 THE ACCESS SWITCHES · TBC, photo-safe, captions, ASSIST, text scale · BUILT c028..c031
- Canon: design doc Part III (photosensitivity mode is the TBC; nothing
  informational lives in motion alone), accessibility matrix (ASSIST widens
  the beat 0.2 → 0.35 and stretches timing 1.5×, never gates content; hold-
  to-toggle with durations preserved), controls map HOLD VERSUS TOGGLE,
  QA-18.
- Reference: `game_state.gd` `set_tbc` (→ shader), `set_photo_safe` (P;
  suppresses bands, flicker, crawl), `set_captions` + `show_caption` (gated
  on `captions_on`), `set_assist`, `set_ui_scale` (recursive label walk in
  `hud.gd`); the ASSIST consumers: `screening_event.gd` (tolerance 0.35,
  hold E counts as still), `floor_manager.gd` (hold E counts as still),
  `live_production.gd` `_timed` (× 1.5).
- State: `tbc_enabled`, `photo_safe` (saved); `captions_on`, `assist_on`,
  `ui_scale` (settings).
- Accepts: QA-18 (beat visibly forgiving, premiere clocks half again longer,
  holding E passes both stillness checks), the matrix's colorblind pass in
  QA.
- UE home: Material Parameter Collection scalars for TBC and photo-safe; a
  flicker-and-grain slider is the UE5 addition the matrix names.
- Delta: none.

#### 4.34 INTERMISSION · pause · BUILT c034
- Canon: accessibility matrix (INTERMISSION pauses everything honestly),
  THE-LAWS 9, QA-32.
- Reference: `hud.gd` `_toggle_pause` (tree paused, bus 0 muted, refused
  while `player.locked` (authored sequences), RESUME / THE BOOTH / RETURN TO
  TITLE · progress holds at your last signature; ESC closes),
  `player.gd` (emits `pause_requested`).
- State: none.
- Accepts: QA-32 (world and clocks hold, audio mutes; refused during any
  authored sequence).
- UE home: `SetGamePaused` plus a UMG menu; the lock flag on Rita.
- Delta: none.

#### 4.35 THE FACILITY MAP · M · BUILT c020/c021/c029
- Canon: QA-15, accessibility matrix (HIGH CONTRAST MAP palette at 5.85:1),
  the greybox HTML map's regeneration rule (the engine is right).
- Reference: `map_view.gd` (draws every room from `WB.ROOMS`, station dots
  from `map_points` (the spawn registry), six LANDMARKS, the player dot with
  a facing tick, a footer that names the bound key through `key_name`).
- State: `map_points` (live, rebuilt by the world).
- Accepts: QA-15 (sealed rooms dashed, station dots labeled, the BOUND map
  key in the footer), probe P15 (outlines match walls; the dot never exits
  geometry).
- UE home: a UMG widget's OnPaint from the same DataTable (migration map: UI).
- Delta: the "sealed rooms dashed" clause of QA-15 has no code (the map
  does not consult door state); note it for the port.

#### 4.36 TITLE, CONTINUE, AND THE INTERFACE LIE · BUILT c007/c013/c030
- Canon: THE-LAWS 8 (the interface may lie exactly once, where the design
  doc says it does), design doc Part III (NEW GAME reads NEW EPISODE; it
  reverts on next launch; it happened anyway), invariant I13, QA-02,
  QA-04, QA-31 (0.8b-3), the demo cut plan (the title badge).
- Reference: `title.gd` (CONTINUE disabled without a log; if `lie_pending`:
  NEW GAME reads NEW EPISODE, the flag clears and saves, so it shows once;
  OPTIONS, CREDITS, QUIT; DEMO foot line; the FILED WHILE YOU WERE OUT
  stack from `Achievements.flush_silent()`; focus rings on every button;
  the first-run booth), `game_state.gd` `mark_ending(name, true)` (sets the
  flag only for THE NEW PRODUCER).
- State: `lie_pending` (survives NEW GAME on purpose).
- Accepts: QA-02, QA-04, I13 (reach ending 2, relaunch twice: once), the
  playtest matrix (NEW EPISODE exactly once).
- UE home: a UMG title; the lie is one string swap on one launch.
- Delta: none, and the lie must remain unreachable elsewhere (build plan
  invariant 10).

#### 4.37 ACHIEVEMENTS · filed, never announced · BUILT c030/c043
- Canon: achievements design (the deferral rule, the meta-silence ledger,
  the voice; A01..A28 with triggers; rulings: 4c has none, A26 stays at
  ten), invariants I29, I30, QA-04, QA-29, QA-48.
- Reference: `achievements.gd` (idempotent `unlock`; `user://achievements.cfg`;
  disabled under DEMO; the queue flushes only at morning (`night_changed(false)`
  → toasts, "N entries, X among them" past two) and at the title (silent
  stack); A01 on `log_signed`, A18 on `run_ended`, `on_ending` maps the
  ending name and files A27 for clean hands; a 1 s poll of fourteen state
  flags; A04 / A05 / A06 / A08 / A03 fire from their sites), Steam-bridge
  signal `achievement_unlocked`.
- State: the cfg only.
- Accepts: QA-04, QA-29 (no toast between title and morning), QA-48 (dark
  in the demo), I29, I30 (the once-ever moment has no entry anywhere).
- UE home: a GameInstance subsystem with the same two flush gates; the
  Steam bridge later.
- Delta: none.

#### 4.38 DEMO MODE · Tape 1, free · BUILT c027
- Canon: the demo cut plan (E1..E10, the boundary spec, the exact ending
  moment, the save-carry guarantees, DP1..DP5), build plan release model,
  QA-30, QA-48, BUILD-ORDER P6 (DEMO flag with whitelist).
- Reference: `game_state.gd` (`const DEMO`; paper S1 + S5; `save_log`
  erases the fifteen whitelisted-out keys; `demo_mark` funnel to
  `user://demo_funnel.txt`; `objective_text` short-circuits after the
  capture), `world_builder.gd` (DemoOpen.csv rooms; door reasons SEALED ·
  the club opens the rest… and the transmitter corridor's own line; five
  spawn gates), `bed_prop.gd` (declines), `capture_bench.gd` (`demo_ended`
  after the capture), `hud.gd` `_on_demo_end` (the sign alone, unasked; the
  card protected 3 s; any key to title), `title.gd` (the badge),
  `achievements.gd` (off).
- State: the whitelist; `_demo_t0`.
- Accepts: QA-30 (all clauses), QA-48, DP1..DP5.
- UE home: a build flag plus the same whitelist in `SaveToSlot`; DemoOpen.csv
  is already in Data/.
- Delta: none.

#### 4.39 THE STRING TABLE AND THE GLYPHS · BUILT c032/c033
- Canon: localization plan (the diegetic-English doctrine; chokepoint
  translation), controls map (every prompt renders the player's ACTUAL
  binding via the glyph system), conformance residue L05 / R6, QA-17,
  PORT-BRIEF §3 (import GameText.csv as a StringTable; source strings are
  the keys).
- Reference: `tools/extract_strings.py` → `translations/strings.csv` (0.5
  re-extracted it to `ue/Restoration/Data/GameText.csv`, 714 keys),
  `game_state.gd` `glyphs(text)` (whole-word E / SPACE / Q / T / M → the
  bound key's name, upper-cased; regex cache), the four chokepoints:
  `toast`, `hud._say`, the prompt display, `show_caption`, plus the map
  footer.
- State: none.
- Accepts: QA-17 (prompts everywhere show the new key), the localization
  plan's pseudo-loc pass.
- UE home: `FText::FromStringTable` at the same chokepoints; Enhanced Input
  key display names for the glyphs.
- Delta: none.

### Legacy boxes, kept as written (never delete history)

4.WEB, 4.SAVE, 4.ENCOUNTERS, 4.FINALE, 4.QA51, 4.VERB, 4.FINAL stand in
`PROGRESS.md` exactly as before this unit. 4.FINALE is the integration gate
over 4.24 / 4.25 / 4.26; 4.SAVE is the integrity pass over every saved field
the boxes above cite; 4.QA51 is QA-51 run against 4.24; 4.WEB is §0's last
row.

---

## 2 · CANON-ONLY MECHANICS · RULING boxes (the gap audit's precedent)

Each is written in canon and absent from the reference build. Per the plan
("TRANSLATE the proven GDScript reference, don't redesign") none is built
until the owner rules: STRIKE (as sprint was), BUILD (with a spec commit to
the Godot reference first, since it stays the live spec through 0.10), or
DEFER. The box in `PROGRESS.md` is the ruling, not the build.

#### 4.R1 THE BENCH SUB-TOOLS · bake, splice, audio bench, quality grade, the GEN field
- Canon: design doc Part IV §1 and §11, room inventory BEN (bake oven,
  splice block, scopes, jog wheel, the accession ledger's GEN stamps), build
  plan M1 (full restoration suite).
- In the reference: capture (0.8b-2), the gen knob and TBC (4.1), the
  spectrogram for one asset (4.20), frame stepping (4.17). No bake timer,
  no splice surgery, no grade, no GEN field.
- Ruling needed: scope. The design doc's craft-is-courtship pillar rides on
  the grade feeding the Producer Track (4.R7).

#### 4.R2 AVERT AND DIRECT SIGHT · the clipboard, held gaze, and cone safety in the hunt
- Canon: design doc §2 (Avert: hold to raise the clipboard; direct sight
  frees it), walkthrough fail condition 2 (held gaze past ~1 s), controls
  Part V (Hold Q / LB), QA-14's first clause, I05.
- In the reference: none. Q is IMPROVISE in the shipped map; the night hunt
  strikes on distance and the wall raycast; the on-camera guards are the
  tally contract and the premiere (4.3's delta).
- Ruling needed: the after-fire canon (Laws 10 and 11, THE TWO HIDES)
  re-founded safety on the tally and the lit hide. Recommend striking Avert
  and the gaze fail as superseded, and ruling separately whether Law 1's
  cone safety enters the night hunt (it is the one clause of QA-14 the code
  cannot pass today).

#### 4.R3 THE QUIET GAME SEEK · scripted Night 2, unscripted T4.9, the mic
- Canon: design doc §5, master T1.5 (the rhyme) and T4.9 (SCARE 8, the
  warned variant), walkthrough fail condition 3, the accessibility matrix
  (button-hold parity), scare compendium.
- In the reference: the two built stillness checks are the Floor Manager's
  watch (4.6) and the screening's QUIET stance (0.8b-4). No seek is ever
  called by the Rundown.
- Ruling needed: build against 4.6's watch (the same three seconds), or
  strike. The seventh signal's payoff (4.R4) depends on it.

#### 4.R4 THE HAND SIGNALS AS MECHANICS · STRETCH, WRAP IT UP, THIRTY SECONDS, ON TIME, CUT, HOLD YOUR APPLAUSE
- Canon: design doc §3 (the Floor Manager's hand signals are the telegraph
  system), master App C (the glossary with mechanical meanings), T4.9
  (three seconds of grace the film-only players never get), casualty
  ledger (the unheld applause moment costs a row member).
- In the reference: the six names are taught and counted (4.15); YOU'RE ON
  is built (4.6); nothing else has an effect, and no code reads
  `signals_known` beyond A07 and the seventh's gate.
- Ruling needed: which signals get mechanics, in what order. STRETCH / WRAP
  IT UP are clock edits (0.7's clock); THIRTY is a caption; the seventh is
  a grace window on 4.R3.

#### 4.R5 THE POWER BUDGET AT BUILDING SCALE
- Canon: design doc §2 (a finite amperage budget at the breaker panel;
  overdraw trips breakers in the worst order) and named gap 4 (routes, not
  percentages), room inventory PB / KIT / EXT (the meter, the kitchen
  circuit ASK, dorm heat FORCE, the floodlight trap, the fuse drawer),
  spike 6 "full panel scale", master App B (power shortfalls T3+).
- In the reference: two circuits, one toggle (4.4); the cascade (4.8).
- Ruling needed: scope, against gap 4's warning.

#### 4.R6 APPROACHES AND GENERATIONS · PRESERVE / ASK / FORCE, G1 / G2 / G3
- Canon: design doc Part IV-B §10 and §11 (hard guardrails: generations
  never gate endings), master App B (the solutions matrix, ten obstacles),
  the airdate math puzzle (141 / 138 / three names), the FORCE tools (bolt
  cutters, the drill, the imperfect seal and the hummed epilogue), build
  plan M3 (the authored-gap table as data).
- In the reference: single paths everywhere except the Vess binder (a
  FORCE G2 source, 4.16) and the keys (PRESERVE, 4.13). No GEN field, no
  airdate puzzle, no drill.
- Ruling needed: scope. The routing doc's one rule (every ending is
  reachable by conduct performed in space) is already met by the built
  paths; generations gate understanding, not endings, so this can be a
  content wave.

#### 4.R7 THE PRODUCER TRACK · tells, weights, and the audition clause
- Canon: design doc §8, master CANON NOTES AND TUNABLES (A-captures +10
  each, T2 improvise +10, T4 gathering +10, read-through role +15, audition
  at 70), walkthrough VII (ending 2's second on-ramp), routing THREAD 2.
- In the reference: `pt` accrues only at the screening (+10 on the beat,
  +5 late, 4.23's neighbor in 0.8b-4), is shown in the binder, and is read
  by nothing. The audition clause is unreachable: the finale cannot start
  before four assets (4.12, 4.21).
- Ruling needed: whether PT stays a hidden flavor stat (strike the clause)
  or the lockdown trigger changes (a routing change the owner signs).

#### 4.R8 THE COVERAGE DIRECTOR'S UPPER HALF · blockings B / C, the poisoned well, poltergeist staging, the mood law
- Canon: design doc §12, master App A (three blockings per scripted scare;
  monitor deception exactly once per run, telegraphed by static; props
  staged to imply rule-breaks that resolve as legal; the dock never staged;
  startle for the confident, dread for the desperate), build plan
  invariant 3 and the descope ladder (blocking Cs go first).
- In the reference: the profile and its three expressions (4.7); the savor
  line and 2.6 m strike radius at three lines (0.7).
- Ruling needed: ship A / B per the ladder, or A only; the poisoned well is
  the one interface-adjacent item and must be reviewed against Law 8.

#### 4.R9 THE TWELVE SCRIPTED SCARES · as set pieces
- Canon: walkthrough Part IV, master App A, the silence tell (1.5 to 3 s),
  I14 (one startle-class event).

| # | Scare | In the reference |
|---|---|---|
| 1 | In-tape lunge | BUILT (4.1) |
| 2 | Reflection cross | not built (4.5 stages the trip) |
| 3 | Blackout pursuit | partial: the night trip's hummed bar (4.5); no routed pursuit |
| 4 | Compactus opening | not built (4.R10) |
| 5 | The you're-on | BUILT (4.6) |
| 6 | Camera-kill witnessed | BUILT systemically (4.3); not staged once |
| 7 | Seance first answer | BUILT (4.17) |
| 8 | Unscripted seek | not built (4.R3) |
| 9 | Lockdown sync | BUILT (4.12) |
| 10 | The bell | BUILT (4.26, `Sfx.bell()` at the line) |
| 11 | The plunge | not built (the HOUSE incident dims 0.35, 4.24) |
| 12 | The delivery | not built (the crossing's "caught" is the nearest, 4.25) |

- Ruling needed: which of 2 / 3 / 4 / 11 / 12 are content waves and which
  are struck. Every one must keep the silence tell and never add a startle.

#### 4.R10 PLAYER-OPERATED ARCHITECTURE · the compactus, the catwalk toll, the rail ladder
- Canon: walkthrough III.3 and III.5 (the compactus principle; one space
  above the format, paid in noise), routing MOVEMENT GRAMMAR 6, room
  inventory LIB / CAT / TH.
- In the reference: catwalks and a ramp exist as geometry
  (`_build_catwalks`); nothing cranks, nothing tolls, nothing is exposed at
  a ladder.
- Ruling needed: Phase 3 rooms own the geometry (3.8, 3.15); the mechanic
  (a crank, a noise event on the grating, ladder exposure) is a Phase 4
  build after the ruling.

#### 4.R11 M2 · THE HOME SINGER (Merle's premiere grave)
- Canon: casualty ledger M2 (the HOME segment needs a body in the rows;
  she volunteers; the swapped word; taken on the beat; the run sheet line
  struck through in her hand) and its ripples (incidents lose 20 percent
  forgiveness).
- In the reference: none. `live_production.gd` has no HOME segment and no
  Merle site; the ledger's AS BUILT count of ten is nine in code.
- Ruling needed: build (the premiere's cue list gains the segment, 4.24) or
  amend the AS BUILT paragraph to say nine. Either way the paragraph must
  match the code.

#### 4.R12 THE VERSE VARIANT AND OTHER G2 PAYOFFS
- Canon: master T2.6 ASK (Harriet hums it; HERE for HOME), T5.3 CUE 2's
  variant beat (Chum stops for one beat and permits it), casualty ledger M2
  (the swapped word is her death's mechanism).
- In the reference: only the PRESERVE verse (4.20); the finale sings HOME.
- Ruling needed: with 4.R6; cheapest of the generations to build because it
  is one flag and one line.

#### 4.R13 THE BINDER'S TWO QUEUED RULES · live-time during the premiere; casting-drift stationery
- Canon: gap audit ruling 3 (RULED as proposed; premiere live-binder wiring
  queued with the reaction commits), design doc Part III (the binder gains
  Gladhouse stationery as PT rises: dressing, never deception).
- In the reference: the binder is a HUD label that never pauses anything
  (4.31); no stationery.
- Ruling needed: none for the first (already ruled: build with 4.WEB); the
  stationery is 5.2's UI pass and must be reviewed against Law 8 (design
  doc named gap 2).

#### 4.R14 PHOTO MODE · Tier B, studio-safe
- Canon: gap audit ruling 8 (RULED: day, never him; graves are not
  previews), press kit embargo doctrine.
- In the reference: none.
- Ruling needed: none (ruled); it is a Phase 5 build (5.6's neighbor) and is
  listed here so the enumeration is complete.

#### 4.R15 AUDIENCE ONLY · the eighth ending
- Canon: walkthrough ADDENDUM · THE SECRET (c046 in the addendum's own
  numbering: W1 in the skip gap Day 2, W2 behind the burn barrel Day 3, W3
  on the shed shelf Day 4; four clean dailies first; each viewing spends an
  S2 slip; the dead room radio's dial CONFIRMED; the final break's caption
  a radio through three walls; Q within six seconds; the 75 s run to the
  dead room; ENDING A with the exclusive PROGRAM GUIDE; 58 · STILL ON on
  the title ever after; no achievement by design), QA-60, QA-61.
- In the reference: none. No script names W1..W3, S2 slips, the dial, the
  program guide, or STILL ON; the README's commit 046 is THE MACHINE SHOP.
- Ruling needed: it carries two QA lines and a spoiler addendum but no
  code; it is either a Phase 4 build after 4.9 / 4.25 or the addendum is
  marked unbuilt. The two QA lines fail on the reference today.

#### 4.R16 THE CASUALTY LEDGER'S NAMED REMAINDERS · the green bleed, the post-F2 haunt, the freeze-check inversion
- Canon: casualty ledger V1 / V2 ripples (Leland annotates him: HE COUNTED
  RIGHT), F2 ripples (he exists only in the program feed; stillness near
  monitors now draws his point), AS BUILT ("canon-only remainders, named").
- In the reference: none (deferred honestly at c040 / c041).
- Ruling needed: build with 4.WEB's reaction commits or strike.

### Notes that are not boxes

- **Reach:** the gap audit's ruling 10 says 2.1 m and a 35-degree cone,
  final numbers pending the device pass; `player.gd` says REACH 2.6 and
  0.8b-1 ported 2.6 to the digit. Code is the intent until the device pass
  re-rules; no box.
- **The switcher bank:** `cam_1..3` exist (4.24); the full face-button
  console mapping is 5.2's controller pass and the controls map already
  specifies it.
- **The reflection budget** (mirrors compose better from Tape 3) is an
  asset and shader question for Phase 3 / 5, not a mechanic box.
- **Audio events on mechanics** (S17 footfall, S18 fold, the wake's
  band-step-down, occlusion under 3 m) are 5.1's box; every 4.x above
  that fires `Sfx` or a caption is a hook 5.1 replaces.

---

## 3 · CANON NUMBERS VERSUS CODE NUMBERS (the code is the intent)

| Knob | Canon says | Code says | Where |
|---|---|---|---|
| Seance wear | 7 per pass (3.5 Matinee) | 1.5 per frame step, every mode | `seance_dock.gd` `_step` |
| 1A threshold | Leland Integrity ≥ 60 | `seance_wear <= 70.0` | `hud.gd` `_end_perform` |
| L1 offer | past five answers and the wear threshold | five answers and `seance_wear > 70.0` | `seance_dock.gd` |
| Sheet lines | 4 Late Night / 7 Matinee / 0 One Take | full at `strikes >= 4` in Matinee and Late Night; any strike in One Take | `game_state.gd` `strike` |
| Matinee mercies | seven lines, unlimited paper, halved wear, longer tells | unlimited paper only | `game_state.gd` `paper_for` |
| Seek grace | 3 seconds | the you're-on watch is 3.0 s | `floor_manager.gd` |
| Sight grace | about 1 second | none (no gaze fail exists) | 4.R2 |
| PT weights | +10 / +10 / +10 / +15, audition at 70 | +10 on the beat, +5 late, read by nothing | `screening_event.gd`, 4.R7 |
| Paper | 3 lines per station per tape | 3 per station, never refilled per tape | `game_state.gd` (paper is seeded once) |
| Crossing | 75 s base, 62 without Vess, −13 self-held | identical | `live_production.gd` |
| Warn / strike | 7 m / 2.2 m, savor at three | identical, savor strike 2.6 m | `rundown.gd` |
| Capture | 12 real seconds, 4 m tether | identical | `capture_bench.gd` |

Where the port must choose, it chooses the code column and files the canon
column as a tuning candidate for 5.x. Changing a number in the code column
is a canon change the owner signs.

---

## 4 · COVERAGE TABLES (the assert script reads these)

### 4.1 Every script, claimed

| Script | Box(es) |
|---|---|
| `achievements.gd` | 4.37 |
| `arm_preview.gd` | DEV |
| `asset_pickup.gd` | 4.20 |
| `asset_rack.gd` | 4.20 |
| `bed_prop.gd` | 0.8b-4, 4.21, 4.38 |
| `bench_tv.gd` | 4.1, 4.17 |
| `bot_driver.gd` | 0.9, 4.24 |
| `broadcast.gd` | 0.7 |
| `capture_bench.gd` | 0.8b-2, 4.38 |
| `cascade.gd` | 4.8 |
| `cast_preview.gd` | DEV |
| `casting_sheet_prop.gd` | 4.10 |
| `character_kit.gd` | ART |
| `coat_pegs.gd` | 4.29, 4.12 |
| `coverage_director.gd` | 4.7, 4.9 |
| `credit_entry.gd` | 4.16, 4.27 |
| `credits.gd` | 4.26 |
| `cue_sign.gd` | 0.8b-4 |
| `dailies_canister.gd` | 4.9 |
| `dailies_manager.gd` | 4.9 |
| `decision_ledger.gd` | 4.21, 4.16 |
| `degausser.gd` | 4.9 |
| `dock_chum.gd` | 4.19 |
| `dock_task.gd` | 4.19 |
| `door.gd` | 4.13, 4.2, 4.8 |
| `dresser.gd` | 4.10 |
| `film_cabinet.gd` | 4.15 |
| `finale_breaker.gd` | 4.24 |
| `finale_fixture.gd` | 4.24 |
| `fire_tape_dock.gd` | 4.18 |
| `fire_tape_pickup.gd` | 4.18 |
| `floor_manager.gd` | 4.6, 4.27, 4.33 |
| `frame_sequence.gd` | 4.17 |
| `game_state.gd` | 0.8a, 0.8b-3, 4.2, 4.9, 4.14, 4.20, 4.26, 4.27, 4.28, 4.32, 4.33, 4.36, 4.38, 4.39 |
| `gen_knob.gd` | 4.1 |
| `glimpse.gd` | 4.11 |
| `harriet.gd` | 0.8b-4, 4.23, 4.27, 4.29 |
| `harriet_note.gd` | 4.15, 4.23 |
| `head_preview.gd` | DEV |
| `hud.gd` | 0.8b-4, 4.26, 4.27, 4.30, 4.31, 4.33, 4.34, 4.38 |
| `impossible_crate.gd` | 4.17 |
| `interactable.gd` | 0.8b-2 |
| `invariant_parser.gd` | 0.9 |
| `key_item.gd` | 4.13 |
| `live_production.gd` | 4.24, 4.25, 4.16, 4.33 |
| `liveness_check.gd` | 4.8, 0.9 |
| `lockdown.gd` | 4.12 |
| `log_station.gd` | 0.8b-4, 4.14 |
| `map_view.gd` | 4.35 |
| `merle.gd` | 4.22, 4.21, 4.27 |
| `monitor_rig.gd` | 4.3, 0.6b |
| `night_trip.gd` | 4.5 |
| `noise_tracker.gd` | 4.2 |
| `options_panel.gd` | 4.32 |
| `patchbay_console.gd` | 4.4, 4.3, 4.8, 4.16 |
| `player.gd` | 0.8b-1, 4.34 |
| `prop_kit.gd` | ART |
| `readable_prop.gd` | 4.28 |
| `rec_chairs.gd` | 4.12 |
| `rejected_edit.gd` | 4.23 |
| `rundown.gd` | 0.7, 0.8a, 4.2, 4.3, 4.7, 4.8, 4.25 |
| `screening_event.gd` | 0.8b-4, 4.33 |
| `seance_dock.gd` | 4.17, 4.27 |
| `sfx.gd` | 5.1 |
| `soak_runner.gd` | 0.9 |
| `spectro_dock.gd` | 4.20 |
| `tape_stage.gd` | 4.1, 4.17 |
| `title.gd` | 4.36, 4.32 |
| `tone_emitter.gd` | 5.1 |
| `vess.gd` | 4.16, 4.27 |
| `vess_binder.gd` | 4.16, 4.28 |
| `wall_clock.gd` | 0.7 |
| `world_builder.gd` | 0.5, 0.6 |

### 4.2 Every QA line, assigned

| QA | Box(es) |
|---|---|
| QA-01 | 4.32 |
| QA-02 | 4.36 |
| QA-03 | 4.26 |
| QA-04 | 4.37 |
| QA-05 | 0.8b-4 |
| QA-06 | 0.8b-2 |
| QA-07 | 0.8b-4, 4.10 |
| QA-08 | 0.8b-4 |
| QA-09 | 0.8b-4 |
| QA-10 | 4.13, 4.8 |
| QA-11 | 4.29, 4.22 |
| QA-12 | 0.7 |
| QA-13 | 4.2 |
| QA-14 | 4.3, 4.R2 |
| QA-15 | 4.35 |
| QA-16 | 4.32 |
| QA-17 | 4.32, 4.39 |
| QA-18 | 0.8b-4, 4.33 |
| QA-19 | 4.5, 4.6 |
| QA-20 | 4.8 |
| QA-21 | 4.14 |
| QA-22 | 4.17 |
| QA-23 | 4.18 |
| QA-24 | 4.19 |
| QA-25 | 4.11 |
| QA-26 | 4.12 |
| QA-27 | 4.24 |
| QA-28 | 4.25, 4.26 |
| QA-29 | 4.37 |
| QA-30 | 4.38 |
| QA-31 | 0.8b-3 |
| QA-32 | 4.34 |
| QA-33 | 4.18 |
| QA-34 | 0.8a, 4.30 |
| QA-35 | 0.8a |
| QA-36 | 0.8a |
| QA-37 | 0.7 |
| QA-38 | 0.8a, 4.30 |
| QA-39 | 4.27, 4.31 |
| QA-40 | 4.18, 4.22 |
| QA-41 | 4.23, 4.15 |
| QA-42 | 4.16 |
| QA-43 | 4.24, 4.25 |
| QA-44 | 4.17 |
| QA-45 | 4.26 |
| QA-46 | 4.24 |
| QA-47 | 4.26 |
| QA-48 | 4.38, 4.37 |
| QA-49 | 4.23 |
| QA-50 | 4.17 |
| QA-51 | 4.QA51, 4.24 |
| QA-52 | 1.10 |
| QA-53 | 1.9 |
| QA-54 | 1.11, 5.1 |
| QA-55 | 3.x |
| QA-56 | 3.x, 4.29 |
| QA-57 | 3.x |
| QA-58 | 0.8b-1, 0.9 |
| QA-59 | 3.x, 4.28 |
| QA-60 | 4.R15 |
| QA-61 | 4.R15 |

### 4.3 Every invariant, assigned

| Invariant | Box(es) |
|---|---|
| I01 | 0.7, 0.9 |
| I02 | 0.7, 0.9 |
| I03 | 4.24 |
| I04 | 4.13, 4.8 |
| I05 | 4.3, 4.R2 |
| I06 | 4.24, 0.9 |
| I07 | 4.8 |
| I08 | 0.6, 4.13 |
| I09 | 0.8b-2 |
| I10 | 4.14 |
| I11 | 4.11 |
| I12 | 4.19 |
| I13 | 4.36, 4.26 |
| I14 | 4.1 |
| I15 | 4.18, 5.1 |
| I16 | 0.8a, 4.10 |
| I17 | 0.8a |
| I18 | 4.12 |
| I19 | 4.19, 4.17, 4.25 |
| I20 | 4.17 |
| I21 | 4.7 |
| I22 | 0.7, 4.2 |
| I23 | 0.8a |
| I24 | 0.7 |
| I25 | 4.2 |
| I26 | 0.8a |
| I27 | 4.27 |
| I28 | 4.26 |
| I29 | 4.26, 4.37 |
| I30 | 4.37, 4.11 |
| I31 | 0.8b-1, 0.9 |

### 4.4 Every Timings.csv constant, homed

| Constant | Box |
|---|---|
| `broadcast.gd` ON_AIR_SECONDS | 0.7 |
| `broadcast.gd` BREAK_SECONDS | 0.7 |
| `capture_bench.gd` CAPTURE_SECONDS | 0.8b-2 |
| `capture_bench.gd` TETHER | 0.8b-2 |
| `credits.gd` SPEED | 4.26 |
| `frame_sequence.gd` W | 4.17 |
| `frame_sequence.gd` H | 4.17 |
| `game_state.gd` SAVE_VERSION | 0.8b-3 |
| `merle.gd` SPEED | 4.22 |
| `player.gd` SPEED | 0.8b-1 |
| `player.gd` ACCEL | 0.8b-1 |
| `player.gd` MOUSE_SENS | 0.8b-1 |
| `player.gd` REACH | 0.8b-1 |
| `player.gd` CROUCH_MULT | 0.8b-1 |
| `rundown.gd` MOVE_SPEED | 0.7 |
| `rundown.gd` AF_APPROACH_SPEED | 0.8a |
| `rundown.gd` AF_LOOM_DIST | 0.8a |
| `rundown.gd` AF_COOL_SECONDS | 0.8a |
| `rundown.gd` AF_HEIGHT | 0.8a |
| `rundown.gd` AF_FOLD_SECONDS | 0.7 |
| `rundown.gd` AF_DOOR_NEAR | 0.7 |
| `rundown.gd` AF_CROSSING_SPEED | 0.8a |
| `rundown.gd` WARN_RADIUS | 0.7 |
| `rundown.gd` STRIKE_RADIUS | 0.7 |
| `rundown.gd` BASE_HEIGHT | 0.8a |
| `rundown.gd` HEAD_TILT | 1.8 |
| `screening_event.gd` BEAT | 0.8b-4 |
| `screening_event.gd` WINDOW | 0.8b-4 |
| `seance_dock.gd` MAX_FRAME | 4.17 |
| `tone_emitter.gd` RATE | 5.1 |
| `world_builder.gd` WALL_H | 0.6 |
| `world_builder.gd` WALL_T | 0.6 |

### 4.5 The knob numbers that are NOT in Timings.csv (extract them when 0.8b-4 / 4.x land)

night trip 20.0 s · Floor Manager 9.0 m, dot 0.5, 3.0 s, 0.4 m/s · noise:
footsteps 6.0 every 0.6 s above 0.5 m/s, door 8.0, signature 4.0, hearing
`loudness × 3.0`, memory 12 s · camera kills 9.0 m, most-watched 14.0 m ·
savor strike 2.6 m · HIDER warn 5.0 m · cascade warn −1.5 floor 3.5 ·
director thresholds 2 / 4 / 4 s, monitor 3.5 m dot 0.6, save every 5 s ·
cascade 4.0 s + 16.0 s, rigs 2..3 then 4..5, scrim 0.55 / 0.75 · lockdown at
4 assets · glimpse rect [−9.75, −16.0, 7.5, 3.0], 1.8 s, Day 4 · seance
wear 1.5, threshold 70, answers 7 / 14 / 21 / 28 / 35, temp gen wear / 30
capped 2.0 · premiere interval max(14, 26 − 4 · fails), auto-fix 40 s,
tally refusals 2, boom hold 1, cue 2 45 s, retakes 30 s, mark 1.6 m, ASSIST
× 1.5 · crossing 75 / 62 / −13, fader 4.6 s, goal 2.0 m · screening
tolerance 0.2 / 0.35 ASSIST / −0.05 without Harriet, PT +10 / +5 · paper 3
· dailies 4 slots · coat drift (day − 1) / 4, +0.35 at lockdown · Merle
KETTLE (8, 0, −1), CHAIR (2.6, 0, 1.2), DOORWAY (6, 0, −16.4) · decision
Day 3 · pre-signed Day 2 at S4 · crate Day 2 · D09 Day 2, D11 Day 4 ·
achievements poll 1 s · captions 1.4 s + 0.6 s · toast 3.0 s · scrim tween
1.2 s.
