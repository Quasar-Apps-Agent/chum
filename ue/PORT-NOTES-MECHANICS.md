# PORT NOTES · MECHANICS — Phase 4 enumerated from the canon and the code

**Unit 4.0 (CLOUD-OK).** The plan's Phase 4 says "ENUMERATE from the canon
docs. Per mechanic: port/implement → diegetic feedback → fail-forward
integration → automation test." This file is that enumeration: every
mechanic the game has, where its truth lives (the canon doc AND the
reference GDScript — PORT-BRIEF law: where prose and code disagree, THE
CODE IS THE INTENT), which QA lines accept it, which invariants guard it,
and which PROGRESS box owns the port. Written from `scripts/*.gd` at the
commit this file landed in (73 files) and from `docs/canon`,
`docs/production`, `docs/packet/portbrief`.

Verification for a text unit is an assert script, not an eye:
`python3 tools/verify_mechanics.py` parses the tables below and asserts
(a) every referenced script exists, (b) every one of the 73 reference
scripts is claimed exactly by this file (by a Phase 4 row or by the
"owned elsewhere" census), (c) every QA line in
`restoration-qa-regression.md` (QA-01..QA-61) has a home, (d) every
invariant in `restoration-invariant-suite.md` (I01..I31) has a home,
(e) every Phase 4 box in PROGRESS.md is enumerated here and vice versa.
It prints `VERIFY-OK` with the counts.

Doctrine that shaped the cut:

- **Phase 0 already owns the core.** P0–P3 of BUILD-ORDER (walk, spike,
  state/saves, the loop) are units 0.5–0.8b-4 and 0.9/0.10. Nothing here
  duplicates them; §5 says exactly which scripts and QA lines those units
  keep. Phase 4 = BUILD-ORDER **P4 (hunter & nights), P5 (story gates &
  finale), P6 (meta & modes)** plus the tape-world presentation.
- **Boxes are mechanics with reference code.** Where the canon promises a
  mechanic that has NO GDScript (the code is the spec, and the spec is
  silent), the box is tagged **CANON-ONLY** and says so; it is authored
  from the doc, in UE, after 0.10 (Godot stops being the live spec at the
  parity gate). Three such boxes exist (4.8, 4.28, 4.29); they are real
  gaps, not gold-plating.
- **Design-doc-only systems are NOT boxes.** §7 lists the design doc's
  systems that never reached the prototype AND carry no QA line. Per the
  gap audit ("consult the rulings before re-deciding anything") they need a
  canon ruling before they become units. Enumerating them as boxes would be
  the gold-plating rule 2 forbids.
- Every number below is the code's number, and most also live in
  `ue/Restoration/Data/Timings.csv`. Never change them.

---

## 1 · HOW TO READ A ROW

`Box` is the PROGRESS.md id. `Reference` lists the GDScript that IS the
spec for that mechanic (read it as exact pseudocode). `QA` are the
acceptance lines from `docs/production/restoration-qa-regression.md`;
`Inv` are `docs/production/restoration-invariant-suite.md` entries the box
must keep green (the harness in 0.9 encodes I01/I02/I22/I06; the rest are
box-level asserts or review rules). `Src` is the canon doc that authored
it. UE homes follow `docs/packet/portbrief/UE5-MIGRATION-MAP.md`:
interactables → actors implementing `IRestorationInteractable` (0.8b-2's
interface), autoload logic → `URestorationState` (0.8a), the hunter →
`ARundown` (0.7), the clock → `URestorationClock` (0.7), logs → the same
file formats the parser reads.

---

## 2 · THE ENUMERATION (Phase 4 boxes, in PROGRESS order)

### P4 · THE HUNTER AND NIGHTS

| Box | Mechanic | Reference | QA | Inv | Src |
|---|---|---|---|---|---|
| 4.1 | **The noise bus, the dead room's deafness, crouch honesty.** Player footsteps emit `noise(pos, 6.0)` every 0.6 s of movement at night (never during the premiere); doors emit 8.0 on every swing; signing a log emits 4.0 at the respawn point. The hunter hears a noise only if `distance < loudness × 3.0`, only at night, never in the premiere, and NEVER if the noise originates inside the dead-room rectangle (`abs(x−19.0) ≤ 2.2 ∧ abs(z−2.5) ≤ 2.7`). Heard noise is honored for 12 s at the next BREAK (0.7 ported the relocation; this box ports the EMITTERS and the deaf rectangle). No code path reads crouch posture; no footstep channel is muffled by it. | `noise_tracker.gd`, `door.gd`, `game_state.gd` (`noise`, `_sign_finish`, `in_dead_room`), `rundown.gd` (`_on_noise`) | QA-13, QA-38, QA-58 | I22, I25, I31 | after-fire-chum (THE TWO HIDES), gap-audit ruling 2 |
| 4.2 | **The Coverage Director and its blockings.** Night counters: seconds facing a monitor within 3.5 m (dot > 0.6), moving (> 0.5 m/s), still; persisted to `cov_*` every 5 s; profile = AUDIENCE (all under 2/4/4 s) else CHECKER ≥ SPRINTER ≥ HIDER by dominant counter; `coverage_label` for the binder; `most_watched_rig`; `reset_read()` on `daily_burned`. Expressed in the Rundown at each ON AIR flip: CHECKER → kill the most-watched rig if < 14 m and log `KILL most-watched rig (CHECKER read)`; SPRINTER → relocate toward the player's nearest segment; HIDER → warn radius 5.0 (else 7.0); cascade active → warn −1.5 (floor 3.5); strikes ≥ 3 → strike radius 2.6 and the "not hurrying" savor line. Append-only `coverage_log.txt` with `[day N night]` prefix — the harness parses it. | `coverage_director.gd`, `rundown.gd` (`_on_phase`) | QA-12, QA-13 | I21, I22 | design-doc §12, spike brief 5 |
| 4.3 | **Camera kills, re-patch, the two-circuit budget, window-bound doors.** At each ON AIR flip at night every unkilled rig within 9.0 m dies (toast "Somewhere, a camera dies…"); a killed rig shows `KILLED · RE-PATCH AT PB`, an unpowered one `NO SIGNAL`; the patchbay's first verb revives the control rig, otherwise it flips CONTROL RUN ↔ STAGE HALL (lights + control rig power; "The budget is the budget."). `window_bound` doors read HELD FOR AIR and refuse while ON AIR unless `cascade_active`; every locked door states its reason and a key satisfies it. Rigs stay `SubViewport` feeds in Godot; in UE they are the 0.6b SceneCapture rig with `sync_to`/`set_killed`/`set_powered`. | `monitor_rig.gd`, `patchbay_console.gd` (non-cascade branch), `door.gd` (`window_bound`), `rundown.gd` (kill loop) | QA-10, QA-14 | I04, I08 | design-doc §2, spike brief 6 |
| 4.4 | **The night trip and the Floor Manager's watch.** Night trip: 20 s into any night (not premiere, once per save via `night_tripped`), rig 0 dies and three toasts play the closing-song beat. Floor Manager: visible only at night, ON AIR, not premiere; body faces the player; when the player is within 9 m and facing him (dot > 0.5) he points once per night (`YOU'RE ON`), then a 3.0 s watch: velocity > 0.4 spoils the take unless ASSIST and E held; the hand lowers, the take holds. Interact reads D08. Hidden once ledgered. | `night_trip.gd`, `floor_manager.gd` | QA-18, QA-19 | — | game-master T2.7/T3.5, design-doc §3, probe P8/P9 |
| 4.5 | **The cascade, liveness, and GET VESS.** Night 4+ (never premiere, once via `cascade_done`): blackout 0.55 + rigs 2–4 die (circuit C), 4 s, 16 s, then blackout 0.75 + rigs 4–6 (circuit B), console `cascade_stage=1`; the panel restores B (stage 2, blackout 0.55) before C (stage 0, clear) — "order matters"; `cascade_active` waives window holds; `liveness_log.txt` writes `OK`/`VIOLATION` every 5 s. At stage 1, if `vess_insight ∧ ¬vess_credited ∧ Vess alive`, the Q option GET VESS: he fixes both circuits then walks to circuit F (V2, `mark_casualty`). A15 on completion. | `cascade.gd`, `liveness_check.gd`, `patchbay_console.gd` (stages, `_v2_taken`) | QA-20, QA-42 | I04, I07 | spike brief 6, casualty ledger V2 |
| 4.6 | **The tally lamp, AF captions, the taught cool, the felt door, D11.** HUD tally `● REC · SAFE WHILE LIT · ss.s` only while `af_active ∧ recording`; his eye light 1.6 only then (dark the instant it stops); body scales to 3.35 m on wake; footfalls thunk every 1.1 s approaching / 0.7 s crossing; `[THE JAW WORKS ITS LEVER]` + first-sighting toast once per save; `[IT FOLDS THROUGH THE DOORWAY]` per door (6 s per-door cooldown, radius 1.0); first cool 4.0 s with the teaching line once (`af_taught`), 2.0 after; player in the dead room → he walks to the felt door (19,0,0), holds within 0.6, says his line once; first dead-room entry → radio toast + `[NO ECHO]` (`deadroom_seen`, persists across new game). D11 readable at day ≥ 4 in CONTROL. (0.8a ported the state arc; this box is the PRESENTATION and captions.) | `rundown.gd` (eye, scale, folds, dead-room hold, `_work_jaw`), `hud.gd` (`_process_tally`), `sfx.gd` (`thunk` caption), `world_builder.gd` (D11) | QA-33, QA-34, QA-35, QA-36, QA-37, QA-38 | I23, I24, I26 | after-fire-chum (all sections), motion-and-sound |
| 4.7 | **Keys and locked doors.** Three key items: EDITH (key board, KITCHEN), TRAINING (key board), QUIET ROOM (the shed shelf, felt-wrapped); `take_key` dedupes and saves; a door with `required_key` unlocks the first time the key turns ("It was cut for this."); locked doors toast their reason. Doors.csv carries the reasons (SHED needs EDITH; DEAD ROOM needs QUIET ROOM; FIRE CORRIDOR sealed until 4.21 unseals it). A16 on the quiet-room key. | `key_item.gd`, `door.gd` (`_locked`, `required_key`), `world_builder.gd` (`_spawn_keys`) | QA-38 | I08 | game-master T2.4/T4.7, Doors.csv |
| 4.8 | **CANON-ONLY · LAW 1 AT NIGHT — camera cones as the lit hide.** THE-LAWS 1 and 11 and the after-fire doc promise: press into an active camera cone and he cannot strike; he waits at the edge of frame. The reference implements on-camera safety ONLY as the tally contract (`recording`) and the premiere guard (`premiere_live`); `rundown.gd`'s night hunt has no cone test, and I05 admits it ("re-verify when hunting and premiere ever coexist"). QA-14's cone clause therefore has no reference code. Author the rule (rig cone test against the player, "waits at the edge" pose, patchbay-built corridors as safe paths) in UE from the doc; the fold and the tally arithmetic must survive unchanged. | — | QA-14 | I05 | THE-LAWS 1/11, after-fire-chum (THE TWO HIDES), routing grammar 2 |

### P5 · STORY GATES AND THE FINALE

| Box | Mechanic | Reference | QA | Inv | Src |
|---|---|---|---|---|---|
| 4.9 | **Burn Your Dailies.** Every non-final strike appends `{id, take}` to `dailies` and spawns a canister in one of four library slots (existing ones respawn on load); one canister carried at a time (`carried_id`); the climate-room degausser burns it: strikes −1 only if > 0, `sheet_changed`, `daily_burned` (which resets the Director's read); the splicing block mints a shortcut daily with take −1 (4.20). Abort never mints (0.8b-2). | `dailies_manager.gd`, `dailies_canister.gd`, `degausser.gd`, `game_state.gd` (`pick_daily`, `burn_daily`, `mint_shortcut_daily`) | QA-07, QA-49 | I09, I16 | walkthrough V-B (Burn Your Dailies), probe P5 |
| 4.10 | **The presigned page.** First interaction with S4 on day ≥ 2 (`presigned_seen` false) plays three beats and `mark_presigned`: a signature `{S4, tape, "TOMORROW", presigned:true}` is appended with NO paper spent, `log_signed` fires. Deviation to keep: QA-21 says "with zero paper"; the code fires on the first S4 visit regardless of paper — the code is the intent. A09 hidden. | `log_station.gd` (`_presigned`), `game_state.gd` (`mark_presigned`) | QA-21 | I10 | game-master T3.6, walkthrough Save Scare |
| 4.11 | **The film cabinet, six signals, Harriet's note.** Cabinet locked until TRAINING; the 1971 film teaches SIX signals 1.1 s apart into `signals_known` (`film_watched` once); Harriet's folded note (D06) appears only after the film and teaches the seventh, HOLD YOUR APPLAUSE, then frees itself; the note hides forever if Harriet is dead before it was read (the seventh becomes unlearnable — QA-41). A07 at seven signals. The generation payoff (SCARE 8 warned vs ambush) is design-doc only — see §7. | `film_cabinet.gd`, `harriet_note.gd`, `game_state.gd` (`add_show_signal`) | QA-41 | — | game-master T2.4, casualty ledger (Harriet ripples) |
| 4.12 | **The crate, the seance, L1 and L2.** The crate at ENTRY (day ≥ 2) sets `crate_opened` and reveals the seance dock (D01). Z/X step frames 0..40, +1.5 wear per step, temp generation `min(2.0, wear/30)` restored on close; answers at frames 7/14/21/28/35 appended once each (frame 14 → PAUSED PROPERLY if Harriet dead; 28 → SHE'S HERE NOW if Merle dead); wear > 70 tears. L1: SPACE offered only at ≥ 5 answers ∧ wear > 70 → ink drains, Leland ledgered, dock inert ("a box with a window"). L2: Q with the fire tape held → the sign-off completes in his voice, `has_fire_tape=false`, answers cleared, `signoff_completed=true`, Leland ledgered. Frames are `FrameSequence` (320×240, seeded per index — I20). A14 at five answers. | `impossible_crate.gd`, `seance_dock.gd`, `frame_sequence.gd`, `bench_tv.gd` (`set_temp_generation`) | QA-22, QA-44, QA-50 | I20, I27 | game-master T4.4, casualty ledger L1/L2, spike brief 3 |
| 4.13 | **The fire tape and M1.** The 1977 reel in Craik's cage sets `has_fire_tape`; the bench dock runs the forced watch (11 s, `play_fire`: no lunge, no sting, light fades) and sets `fire_tape_watched` and, once, `af_active` ("Something answers the tape from three rooms away"). Before the first watch, if Merle lives and was never offered: E lets her stay (M1 — carried mid-sentence, `[THE KETTLE, TWO ROOMS AWAY, CLICKS OFF]`, `mark_casualty`), Q refuses and saves her; `merle_offered` makes it once-only. A13 hidden. | `fire_tape_pickup.gd`, `fire_tape_dock.gd`, `tape_stage.gd` (`play_fire`) | QA-23, QA-33, QA-40 | I15 | game-master T3.4, casualty ledger M1, after-fire-chum (THE REVEAL) |
| 4.14 | **Vess: the binder, the credit, V1 and V2.** His binder (D07) sets `vess_insight` and hides; the ledger margin appears only while `vess_insight ∧ ¬vess_credited` and sets `vess_credited` (A11); Vess at the shrine cycles four lines and vanishes when dead. V1 fires either at AUTHENTICATE (`decision_ledger`: INK toast, all monitors, bars) or at the final breaker (4.23) — both `mark_casualty("VESS", "V1 …")`, idempotent. V2 lives in 4.5. | `vess_binder.gd`, `credit_entry.gd`, `vess.gd`, `decision_ledger.gd` (`_v1_taken`) | QA-42 | I27 | game-master T2.3, casualty ledger V1/V2, probe P13 |
| 4.15 | **The dock inventory.** Six units on armatures; one warm index chosen at setup (random, unsaved); count each by hand; the warm one: "You write the number down anyway."; all six → `dock_done`, which reveals the CARD asset and the fan letter D10. Nothing follows. Ever. A10. | `dock_task.gd`, `dock_chum.gd` | QA-24 | I12 | game-master T4.3, walkthrough Level Principle 6, probe P7 |
| 4.16 | **The Sign-Off assets and the rack.** VERSE from the spectrogram (needs ≥ 1 capture), CART at the master-control rack, SCRIPT (D02) in Craik's box at the transmitter threshold, CARD in the props crate after `dock_done`; `gain_asset` dedupes, toasts n-of-4 and the "All four" line; the rack above the bench lights labels and canisters per banked asset. Four assets + night trigger 4.18. | `spectro_dock.gd`, `asset_pickup.gd`, `asset_rack.gd`, `game_state.gd` (`gain_asset`) | QA-26 | I19 | walkthrough VII (Tracked Variables), game-master T2.6/T3.2/T3.3/T4.3 |
| 4.17 | **The decision ledger and Merle's doorway.** Day ≥ 3 only; E cycles AUTHENTICATE → DESTROY → PERFORM with the pen up (`is_pen_up`), SPACE commits while the ledger is the reach-ray target; the entry stands forever ("does not entertain appeals"); D03 on first touch; while the pen is up Merle walks to the DOORWAY and says nothing (probe P14). A17 on commit. AUTHENTICATE with Vess credited triggers V1 (4.14). | `decision_ledger.gd`, `merle.gd` (`_pen_up`, DOORWAY) | — | I19 | game-master T5.2, walkthrough Named Gap 4, probe P14 |
| 4.18 | **The lockdown, the rows, the pegs.** `assets ≥ 4 ∧ night` (once): every rig `sync_to` rig 0's feed, exterior doors read SEALED FOR BROADCAST, Merle's line, `lockdown_done`; re-applied silently on load; the five armchairs tween (1.6 s) from CASUAL to ROWS and never return; coat pegs drift `(day−1)/4` toward the show palette, +0.35 after lockdown, with three prompt lines by drift band. A20. | `lockdown.gd`, `rec_chairs.gd`, `coat_pegs.gd`, `monitor_rig.gd` (`sync_to`) | QA-11, QA-26 | I18 | game-master T4.10, dread doctrine L1, probe P11 |
| 4.19 | **Merle: schedule, lines, 1974.** Targets by state: screening spot while `screening_active`, DOORWAY when the pen is up, CHAIR at night or after lockdown, else KETTLE, at 1.6 m/s; lines by decision then by day (1, 2, else); after the crate, the first interact plays the 1974 monologue once (`merle_1974`, A12 hidden); hidden when dead. | `merle.gd` | QA-11 | — | game-master T4.6, cast sheets, reaction matrix (BUILT rows) |
| 4.20 | **Harriet's graves and the rejected edit.** H1: while frozen (BREAK) on day ≥ 2, the second E takes the slip (`harriet_slip`), which lets `sign_log` sign once on empty paper "in her hand"; the next ON AIR interact plays the absence + the cabinet and ledgers her. Rejected edit (after the crate): Vess's cut plays once (`rejected_seen`); thereafter the block offers the splice with the label disclosed → shortcut daily now, `h2_pending`; the next BREAK interact doubles her (`_splice_visual` ghost rig, rebuilt on load), ledgered H2, one line forever. Screening tolerance tightens 0.05 with her dead (0.8b-4's screening reads `is_dead`). The freeze itself is 0.8b-4. | `harriet.gd` (H1/H2 paths), `rejected_edit.gd` | QA-41, QA-49, QA-50 | I27 | casualty ledger H1/H2 + AS BUILT, game-master T4.5 |
| 4.21 | **The glimpse and the fire corridor.** Day ≥ 4 clears the fire door's reason once (`fire_unsealed`, toast); at night, not premiere, entering the elbow rectangle (center −9.75,−16.0; 7.5×3.0) spawns the undecidable figure for 1.8 s, sets `glimpse_seen`, two lines. Never refires; no achievement; its name appears in no code file (THE-LAWS 3). | `glimpse.gd` | QA-25 | I11, I30 | game-master T4.8, THE-LAWS 3, probe P10 |
| 4.22 | **Live production: cues, incidents, fixtures, rows, premiere_log.** `premiere_live`, night forced, Rita to the mark; cam_1..3 set PGM; a cue lands on SPACE within 1.6 m of MARK with PGM = 1 (wrong camera: "the hand does not move"). Pressure loop from cue 1: interval `max(14, 26 − 4·fail_takes)` s, one of TALLY/HOUSE/BOOM/CARDS (HOUSE = blackout 0.35); club auto-fix at 40 s; fixtures fix by id (AUX resets TALLY or HOUSE); TALLY refuses the cue at most twice then counts a blind call; BOOM holds the cue once. Timed restores (45 s cart deck; ×1.5 with ASSIST) that expire take a row seat (`row_casualties`, three cycling lines, `[A CHAIR, BETWEEN FRAMES]`) and re-enter as TAKE n. `premiere_log.txt`: `INCIDENT …` / `RESOLVED … t=` — the parser's I06 dialect. | `live_production.gd` (`run` through cue 2, `_pressure`, `_on_mark_press`, `_timed`, `_row_taken`, `fix`, `_plog`), `finale_breaker.gd`, `finale_fixture.gd` | QA-27, QA-46 | I03, I05, I06 | game-master T5.3, spike brief 7, casualty ledger THE ROWS |
| 4.23 | **The final breaker and F2.** After the song: Vess credited ∧ alive → his farewell, the handle drops, V1 (casualty); Vess dead → the fused pin, 30 s MAIN BUS retake loop; else the dark, 30 s retake loop ("The dark is patient."). F2: the third counted blind tally call with the Floor Manager alive → the unlisted camera, `[YOU'RE ON · TO NOTHING LISTED]`, ledgered. | `live_production.gd` (breaker branch, `_f2_unlisted`) | QA-42, QA-43 | I27 | game-master T5.3 (THE FINAL BREAKER), casualty ledger V1/F2 |
| 4.24 | **The divert, the fader, the last crossing, 4c, ending 0.** `signoff_completed` → the rundown ends itself (route 4c). Divert offered only with QUIET ROOM key ∧ ≥ 5 answers ∧ `fire_tape_watched`: SPACE places, Q diverts. Fader: FM dead → forced self-hold; else SPACE his hand / E hers (4.6 s, `fader_self`). Crossing: the hunter is placed at (5.5, 0, −29.5), pours at 1.6 m/s with folds, eye DARK; time 75 s, 62 without Vess, −13 self-held; reached (< 2 m of the little door) → DEAD AIR; caught (inside strike radius) → `run_ended`; late → cue 3 continues. `all_cast_dead()` at entry → ending 0 intercept. | `live_production.gd` (`_fader_choice`, `_hold_fader`, `_last_crossing`, `_one_woman`), `rundown.gd` (crossing branch) | QA-28, QA-43, QA-44, QA-45 | — | after-fire-chum (THE LAST CROSSING), casualty ledger F1/L2/ending 0, THE-LAWS 11 |
| 4.25 | **Cue 3, the line, the bell.** The little door (group `little_door`) unlocks; the player opens then closes it by hand on camera; the HUD takes the floor: `Sfx.bell()` once with `[THE BELL RINGS · once]`, SPACE delivers the line, then 1A (≥ 5 answers ∧ wear ≤ 70 ∧ Leland alive) or 1B (with STAFF / READER cards per the ledger). The bell sounds nowhere else. | `live_production.gd` (cue 3), `hud.gd` (`_end_perform`), `sfx.gd` (`bell`) | QA-28, QA-47 | I14 | game-master T5.3 cue 5 / T5.4, THE-LAWS 5 |
| 4.26 | **Endings, the epilogue reader, credits, the one lie.** `finale_started(decision)` routes DESTROY → THE BURN (cold-cobbler variant), AUTHENTICATE → THE NEW PRODUCER (`mark_ending(…, lie=true)` → `lie_pending`; the title reads NEW EPISODE exactly once, then clears), PERFORM → 4.22–4.25 → 1A / 1B / 4c / 0 / DEAD AIR 4a (FM ledgered F1 inside the epilogue, CUE GIVEN) or 4b (her hand). `_roll_credits`: THE LEDGER, READ ALOUD whenever anything is in it (name · cause · epitaph; TRANSITION UNRESOLVED for Harriet; fifty-eight minus N), nothing on a clean run; credits crawl with the ENDING REACHED card, the one-name cast for ending 0, any key after 1.5 s. Achievements A21–A25/A27/A28 map from `mark_ending`. | `hud.gd` (`_on_finale`, `_end_*`, `_roll_credits`), `credits.gd`, `title.gd` (NEW EPISODE), `game_state.gd` (`mark_ending`, `start_finale`) | QA-03, QA-28, QA-45, QA-47 | I13, I28, I29, I30 | game-master THE ENDINGS, walkthrough VII + addendum, casualty ledger THE FULL BOARD |
| 4.27 | **The casualty ledger: presentation and ripples.** `mark_casualty` dedupes by `who` (I27) and toasts THE LEDGER TAKES IT DOWN; `is_dead`/`cause_of`/`all_cast_dead`; binder page one reads NO ENTRIES. KEEP IT SO. until then; every death's ripple is a read of `is_dead` somewhere else (bodies hide, lines change, tolerances tighten, fader forced, credits gain cards). Demo builds never write casualties. (Fields themselves ride in 0.8b-3.) | `game_state.gd` (`mark_casualty`, `is_dead`, `cause_of`, `all_cast_dead`), `hud.gd` (`_fill_binder`) | QA-39, QA-46, QA-48 | I27 | casualty ledger (THE MECHANIC), THE-LAWS 7 |
| 4.28 | **CANON-ONLY · post-F2 monitor haunt, freeze-check inversion, the margin's green bleed.** The casualty ledger's AS BUILT names these as "canon-only remainders": after F2 he exists only in the program feed cueing rooms he is not in, and stillness near monitors now draws his point; after either Vess death the binder margin bleeds green (HE COUNTED RIGHT.). No GDScript. Author in UE from the ledger. | — | — | — | casualty ledger (AS BUILT), reaction matrix F row |
| 4.29 | **CANON-ONLY · the secret ending pilgrimage.** W1 in the skip gap (Day 2) → W2 behind the burn barrel (Day 3) → W3 on the shed shelf (Day 4); each first viewing needs four dailies logged and consumes one S2 slip; the dead-room radio appears after W3 and its dial must be CONFIRMED; then the final break carries the radio caption, Q within six seconds starts the 75 s run, reaching the dead room routes ENDING A · AUDIENCE ONLY (single credit card, the PROGRAM GUIDE post-credits, `58 · STILL ON` on the title forever, no achievement by design). No GDScript exists for any of it (walkthrough addendum c046 is the spec). | — | QA-60, QA-61 | — | walkthrough (SPOILER · THE SECRET), lore architecture |

### P6 · META AND MODES (+ the tape world)

| Box | Mechanic | Reference | QA | Inv | Src |
|---|---|---|---|---|---|
| 4.30 | **Achievements and the deferral rule.** `unlock(id)` idempotent, refused under DEMO, persisted to `achievements.cfg` (unlocked + shown); triggers: signal-bound (A01 on `log_signed`, A18 on `run_ended`), call-site (A03–A06, A08), a 1 s state poll (A02, A07, A09–A17, A19, A20, A26 at 10 documents), and `on_ending` (A21–A25, A28; A27 when casualties and rows are both empty). Flush ONLY at `night_changed(false)` (FILED · … toast, ≤ 2 named else a count) and at the title (FILED WHILE YOU WERE OUT, once). The glimpse has no entry, ever. | `achievements.gd`, `title.gd` (flush), `readable_prop.gd` (`mark_read` → A26) | QA-04, QA-29 | I30 | achievements design, THE-LAWS 3/5 |
| 4.31 | **Modes, the binder, the objective ladder, the sheet.** MATINEE = paper 99 everywhere; LATE NIGHT = 3 lines/station, sheet full at 4; ONE TAKE = any strike ends the run. TAB cycles closed → status page (mode, signatures, CASUALTY LEDGER, sheet n/4, PT, keys, dailies, coverage read, Leland wear/answers, photosafe, Vess state, signals, last five captures) → presentation form (1/2/3 set mode). `objective_text()` priority ladder (DEMO → finale → decision → run_complete → night → day 1 steps → day ≥ 3 → default). The casting sheet on the Studio A wall reads `strikes` of 4; HUD `SHEET · n/4` on `sheet_changed`. Ruling: THE BINDER IS THE INVENTORY (no grid); binder is true-pause in the day, live during the premiere (gap-audit 3; the prototype's binder does not pause — port the ruling). | `hud.gd` (`_fill_binder`, `_fill_form`, binder keys, `_on_sheet`), `game_state.gd` (`set_mode`, `paper_for`, `objective_text`), `casting_sheet_prop.gd` | QA-08, QA-39 | — | walkthrough V-B (Modes, The Casting Sheet), gap-audit rulings 3/4/5 |
| 4.32 | **The booth: settings, remap, glyphs, first run.** `settings.cfg` apart from the log (NEW GAME never touches it): master volume, mouse sensitivity 0.2–3.0, fullscreen, TBC, photo-safe (P), UI text scale 0.8–1.6 (walks every Label), captions, ASSIST; remap for the five verbs with KEY IN USE refusal; `glyphs()` rewrites E/SPACE/Q/T/M tokens in every toast and prompt to the live binding; the booth opens BEFORE the title on first run (no settings file) with the BEFORE THE SHOW banner; O toggles it anywhere; phosphor focus ring on every control. UE target: everything remappable incl. movement, controller rows per the controls map. | `options_panel.gd`, `game_state.gd` (`load_settings`, `save_settings`, `rebind`, `key_name`, `glyphs`, `set_ui_scale`, `set_captions`, `set_assist`, `set_photo_safe`) | QA-01, QA-02, QA-16, QA-17 | — | controls map, accessibility matrix, THE-LAWS 9 |
| 4.33 | **Intermission.** ESC: `pause_requested` → tree paused, master bus muted, cursor freed, INTERMISSION scrim with RESUME / THE BOOTH / RETURN TO TITLE (progress holds at the last signature); refused while `player.locked` (every authored sequence locks her). UMG scrim in UE per the migration map. | `hud.gd` (`_toggle_pause`), `player.gd` (`ui_cancel` → `pause_requested`) | QA-32 | — | accessibility matrix (INTERMISSION), THE-LAWS 9 |
| 4.34 | **The map.** M toggles a full-rect overlay drawn from the ROOMS table (fit to 86 %), station dots from `map_points`, six amber landmarks, the player dot with a facing tick, footer naming the bound key. Deviation to note: QA-15's "sealed rooms dashed" has no code; port what is drawn, log the dashed-outline delta for the UE widget. | `map_view.gd` | QA-15 | — | UE5-MIGRATION-MAP (UI), probe P15 |
| 4.35 | **Captions and the blackout scrim.** `show_caption` emits only when `captions_on`; bracketed source tags are the law ([door], [pen tick], [THE BELL RINGS · once], [WEIGHTED FOOTSTEP] etc.); the HUD holds 1.4 s then fades 0.6; `set_blackout(alpha)` drives the scrim under all labels (cascade 0.55/0.75, HOUSE incident 0.35). UE adds L/R directionality and proximity weight per the accessibility matrix. | `hud.gd` (`_on_caption`, `_on_blackout`), `game_state.gd` (`show_caption`, `set_blackout`), `sfx.gd` (caption calls) | QA-05, QA-37 | — | accessibility matrix (HEARING), design-doc Captions |
| 4.36 | **The tape world: shader, gen knob, the lunge, FrameSequence.** `crt_tape.gdshader` params `generation`, `tbc_on`, `photo_safe` (same names in the UE material function stack); the bench TV's slate lies (3RD GENERATION DUB) while the scope reads MASTER; the gen knob cycles MASTER/1ST DUB/3RD GEN (A03); the tape stage timeline: idle sway, approach at 1.35 from 3.2 s out, hold 0.78→0.12, one-frame lunge at 1.45× (`lunge_happened` → toast), bars 1.6 s; screenings and the fire tape play WITHOUT the lunge; `FrameSequence` frames are deterministic per index. The in-tape lunge is the game's ONE startle. | `bench_tv.gd`, `tape_stage.gd`, `gen_knob.gd`, `frame_sequence.gd` | QA-06 | I14, I20 | design-doc (The Two Render Worlds), spike brief 1, playtest V2–V4, THE-LAWS 2 |
| 4.37 | **Monitor rigs as gameplay.** The rig's four states (live / NO SIGNAL / KILLED / synced) as material swaps on the 0.6b SceneCapture wall pattern; group `rig` for the Director, the bots and the kill loop; `monitor_position`/`cam_position` are the Director's and the hunter's geometry. Spike 2 proved the budget; this box is the state machine. | `monitor_rig.gd` | QA-14, QA-26 | — | spike brief 2, UE5-MIGRATION-MAP (CAMERA FEEDS) |
| 4.38 | **The DEMO build (Tape 1).** `DEMO` build flag: DemoOpen.csv rooms only, demo door reasons, skipped spawns (rundown, FM, dock, crate, seance, cascade, assets, ledger, fire pickup), the bed declines, paper S1/S5 only, the save whitelist strips 15 keys (PORT-NOTES-STATE §5), `demo_funnel.txt` marks (started, s1_signed, screening, capture_start, capture_done, lunge, card), achievements dark, the end-card sequence on `demo_ended` (RESPOND sign alone, TAPE 1 OF 5 card, 3 s protected), title foot TAPE 1 · FREE DEMO. | `bed_prop.gd` (DEMO branch), `game_state.gd` (`demo_mark`, DEMO stripping), `hud.gd` (`_on_demo_end`), `world_builder.gd` (DEMO_OPEN, skips) | QA-30, QA-48 | — | demo cut plan (§2–§6), PORT-NOTES-STATE §5 |
| 4.39 | **Title, continue, the relic, the string table.** CONTINUE disabled without a log; NEW GAME → `reset_new_game` (the eight persisting fields per PORT-NOTES-STATE §2; `ng_relic` = last item lost if the finale was reached, placed on the set in shot, unremarked); migration toasts (v < 16 re-save, v > 16 proceed gently); every toast and prompt passes `tr()` then `glyphs()`, keys = source strings (GameText.csv, 714 keys) — UE StringTable; the `.translation` registration note for localized builds (gap audit). | `title.gd`, `world_builder.gd` (`_spawn_details` relic), `game_state.gd` (`reset_new_game`, `load_log` migration, `toast`) | QA-31 | I13 | PORT-BRIEF §3, PORT-NOTES-STATE §1–§2, localization plan |

---

## 3 · QA COVERAGE (every line of the regression script has a home)

Homes are PROGRESS boxes. "0.x" = a Phase 0 unit already owns it (the
Phase 4 box listed after a slash only adds presentation). Phase 1/3/5
lines are routed to those phases' existing boxes.

| QA | Home | QA | Home | QA | Home |
|---|---|---|---|---|---|
| QA-01 | 4.32 | QA-22 | 4.12 | QA-43 | 4.23 / 4.24 |
| QA-02 | 4.32 | QA-23 | 4.13 | QA-44 | 4.12 / 4.24 |
| QA-03 | 4.26 | QA-24 | 4.15 | QA-45 | 4.24 / 4.26 |
| QA-04 | 4.30 | QA-25 | 4.21 | QA-46 | 4.22 / 4.27 |
| QA-05 | 0.8b-4 / 4.35 | QA-26 | 4.18 / 4.16 / 4.37 | QA-47 | 4.25 / 4.26 |
| QA-06 | 0.8b-2 / 4.36 | QA-27 | 4.22 | QA-48 | 4.38 / 4.27 |
| QA-07 | 0.8b-4 / 4.9 | QA-28 | 4.24 / 4.25 / 4.26 | QA-49 | 4.20 / 4.9 |
| QA-08 | 0.8b-4 / 4.31 | QA-29 | 4.30 | QA-50 | 4.12 / 4.20 |
| QA-09 | 0.8b-4 | QA-30 | 4.38 | QA-51 | 4.QA51 |
| QA-10 | 4.3 | QA-31 | 0.8b-3 / 4.39 | QA-52 | 1.10 |
| QA-11 | 4.18 / 4.19 | QA-32 | 4.33 | QA-53 | 1.9 |
| QA-12 | 0.7 / 4.2 | QA-33 | 4.13 / 4.6 | QA-54 | 1.12 / 5.1 |
| QA-13 | 4.1 / 4.2 | QA-34 | 0.8a / 4.6 | QA-55 | 3.1–3.20 |
| QA-14 | 4.3 / 4.37 / 4.8 | QA-35 | 4.6 | QA-56 | 3.1–3.20 |
| QA-15 | 4.34 | QA-36 | 0.8a / 4.6 | QA-57 | 3.1–3.20 |
| QA-16 | 4.32 | QA-37 | 0.7 / 4.6 / 4.35 | QA-58 | 0.8b-1 / 4.1 |
| QA-17 | 4.32 | QA-38 | 4.1 / 4.6 / 4.7 | QA-59 | 3.1–3.20 |
| QA-18 | 0.8b-4 / 4.4 | QA-39 | 4.27 / 4.31 | QA-60 | 4.29 |
| QA-19 | 4.4 | QA-40 | 4.13 | QA-61 | 4.29 |
| QA-20 | 4.5 | QA-41 | 4.11 / 4.20 | | |
| QA-21 | 4.10 | QA-42 | 4.14 / 4.5 / 4.23 | | |

Demo probes DP1–DP5 → 4.38. Playtest probes P1–P16 map onto the same
boxes (P1 paper 0.8b-4, P2 abort 0.8b-2, P3 retake 0.8b-4, P4 one take
4.31, P5 dailies 4.9, P6 presigned 4.10, P7 dock 4.15, P8 FM 4.4, P9 trip
4.4, P10 glimpse 4.21, P11 lockdown 4.18, P12 stances 0.8b-4, P13 Vess
4.14, P14 doorway 4.17, P15 map 4.34, P16 knob 4.36); P17–P26 are
feel questions, not mechanics.

---

## 4 · INVARIANT HOMES (I01–I31)

| Inv | Home | Inv | Home | Inv | Home |
|---|---|---|---|---|---|
| I01 | 0.7 / 0.9 | I12 | 4.15 | I23 | 0.8a / 4.6 |
| I02 | 0.7 / 0.9 | I13 | 4.26 / 4.39 | I24 | 0.7 / 4.6 |
| I03 | 4.22 | I14 | 4.36 / 4.25 | I25 | 4.1 |
| I04 | 4.3 / 4.5 | I15 | 4.13 / 5.1 | I26 | 0.8a / 4.6 |
| I05 | 4.8 / 4.22 | I16 | 0.8b-4 / 4.9 | I27 | 4.27 / 4.12 / 4.14 / 4.20 / 4.23 |
| I06 | 4.22 / 0.9 | I17 | 0.8b-4 | I28 | 4.26 |
| I07 | 4.5 | I18 | 4.18 | I29 | 4.26 |
| I08 | 4.7 / 4.3 | I19 | 4.16 / 4.17 | I30 | 4.26 / 4.30 / 4.21 |
| I09 | 0.8b-2 / 4.9 | I20 | 4.12 / 4.36 | I31 | 4.1 |
| I10 | 4.10 | I21 | 4.2 | | |
| I11 | 4.21 | I22 | 4.1 / 4.2 / 0.9 | | |

---

## 5 · SCRIPT CENSUS — reference scripts owned OUTSIDE Phase 4

Every `scripts/*.gd` not named in a §2 row is claimed here, so the union is
all 73 and nothing in the reference implementation goes unported by
accident. (A script may also appear in §2 for the part of it Phase 4 owns.)

| Script | Home | Why |
|---|---|---|
| `game_state.gd` | 0.8a / 0.8b-3 | the autoload → `URestorationState`; §2 rows cite its functions where a mechanic lives in them |
| `player.gd` | 0.8b-1 | ARitaCharacter, feel parity proven |
| `capture_bench.gd` | 0.8b-2 | ABenchCapture, tether abort |
| `interactable.gd` | 0.8b-2 | IRestorationInteractable |
| `rundown.gd` | 0.7 / 0.8a | ARundown tick brain + AF layer; §2 rows cite its presentation/blocking branches |
| `broadcast.gd` | 0.7 | URestorationClock, ON AIR 50 / BREAK 18 |
| `world_builder.gd` | 0.6 / 3.1–3.20 | greybox stamped from the CSVs; dressing is Phase 3; §2 rows cite its spawn functions for keys, readables, the relic, DEMO |
| `log_station.gd` | 0.8b-4 | stations + paper economy + respawn |
| `dresser.gd` | 0.8b-4 | retake presentation: the seven items, loupe last |
| `bed_prop.gd` | 0.8b-4 | the day/night lever; `start_finale` handoff |
| `wall_clock.gd` | 0.8b-4 | the clock repeater on the walls |
| `harriet.gd` | 0.8b-4 | the freeze, the cup height; graves are 4.20 |
| `screening_event.gd` | 0.8b-4 | screening + stances + ASSIST beat |
| `cue_sign.gd` | 0.8b-4 | RESPOND / HOLD signs |
| `bot_driver.gd` | 0.9 | the three bots |
| `invariant_parser.gd` | 0.9 | INVARIANTS.txt from the three logs |
| `soak_runner.gd` | 0.9 | headless soak entry |
| `readable_prop.gd` | 3.1–3.20 | the D-series handled lore (D04/D05/D09/D10/D11 spawned in world_builder); A26 hook is 4.30 |
| `tone_emitter.gd` | 5.1 | placeholder room tones and the three segment tones (the hunter's location tell: 220/262/196 Hz) → MetaSounds |
| `sfx.gd` | 5.1 | synthesized bell/thunk/tick → MetaSounds; the bell's once-only call site is 4.25 |
| `character_kit.gd` | 1.7 / 2.1–2.6 | the cast bodies (Blender factory replaces them) |
| `prop_kit.gd` | 3.1–3.20 | procedural props (Megascans/Fab replace them) |
| `arm_preview.gd` | dev tool | Godot-era render target; not ported |
| `cast_preview.gd` | dev tool | Godot-era render target; not ported |
| `head_preview.gd` | dev tool | Godot-era render target; not ported |

---

## 6 · DELTAS AND DEVIATIONS TO CARRY (code vs prose, honestly)

- **QA-14 cone clause has no code** → 4.8 (CANON-ONLY). The only on-camera
  safety in the reference is the tally contract and the premiere guard.
- **QA-15 "sealed rooms dashed"** — not drawn by `map_view.gd`; port as an
  authored delta in the UE widget (4.34).
- **QA-21 "with zero paper"** — the presigned page fires on the first S4
  visit at day ≥ 2 regardless of paper; code wins (4.10).
- **QA-12 warn at 7 m / strike 2.2 / third strike savors**: 0.7 ported the
  radii; savor = radius 2.6 + the line; "not instant" is the line, not a
  delay (4.2).
- **QA-34 "first-sighting toast exactly once per save"** — `_af_seen_once`
  is a live var, not saved; it is once per SESSION in the reference. Port
  as once per save (the QA line is the stricter, intended reading; add the
  flag to the v16 schema only via a canon ruling — for now keep the live
  var and file the delta) (4.6).
- **QA-19 "Night 1 trip fires once ever"** — fires 20 s into the FIRST
  NIGHT THAT RUNS 20 s, not necessarily night 1; `night_tripped` makes it
  once per save (4.4).
- **Design-doc SCARE blockings 2–12** — only the Director's three
  expressions (4.2) and the authored events (4.4, 4.21, 4.18, 4.25) exist;
  the compendium's per-profile variants are unbuilt (see §7).
- **Reaction matrix QUEUE (commit order 045–047)** — none of H-R2, F-R1,
  M-R5, B-R2, M-R1..4, V-R1..3, L-R1, B-R1 is in the reference; they are
  4.WEB's worklist (already a box) — 14 items, each "lands with QA lines
  and stays inside the laws".
- **The binder does not pause** in the reference; gap-audit ruling 3 says
  true-pause by day, live in the premiere — port the ruling (4.31).

---

## 7 · UNSPECCED — design-doc systems with no code and no QA line

Not boxes. Each needs a ruling in `restoration-gap-audit.md` before it
becomes a unit; enumerating them as work would violate rule 2 (no
gold-plating) and the PORT-BRIEF (the code is the intent).

Bake and splice as bench tools · the audio bench beyond the spectrogram
(waveform, frequency fragments 1–3 as a dialable number) · AVERT (the
clipboard hold) · the Quiet Game breath / microphone input · the full
amperage budget and breaker map (v0 is two circuits) · catwalk routing over
Studio A · airdate math as an interface (141/138, the light table) ·
Producer Track TELLS (reflection budget, binder stationery drift; `pt`
exists and gates nothing yet) · seance jump-cue by timecode (green-ink
timecodes) · generations G1/G2/G3 as a ledger GEN field · Ask/Force
branches beyond those built (TH after-hours entry, drilled dead-room door
and its hummed epilogue) · SCARE compendium blockings B/C per profile ·
the Understudy's off-camera partials · Matinee's halved wear (`add_wear` is
flat 1.5) · Late Night/Matinee tell-window scaling beyond ASSIST · NEW
GAME PLUS (PARKED by the author's word; the relic is the one nod and it is
built) · sprint (RULED none) · photo mode (RULED Tier B; nothing built).

---

## 8 · WHAT "DONE" MEANS FOR PHASE 4

Per the PORT-BRIEF: QA-01..QA-61 pass on the UE build as written and every
law in THE-LAWS holds. Per this file: every §2 box ticked (its QA lines run
by hand or bot, its invariants green in the 0.9 harness where encoded),
4.WEB's fourteen reactions landed, and `tools/verify_mechanics.py` still
prints VERIFY-OK — because a box added to PROGRESS without a row here, or a
reference script nobody claimed, is how a mechanic goes missing in a port.
