# PORT NOTES · MECHANICS — Phase 4 enumerated from the canon

**Unit 4.0 (CLOUD-OK).** Every puzzle and functional system the canon
names, as a box in `PROGRESS.md` Phase 4, with its source of truth. The
plan's per-mechanic loop applies to each: **port/implement → diegetic
feedback → fail-forward integration → automation test.** Where the Godot
reference has code, THE CODE IS THE INTENT (PORT-BRIEF law) and the box is a
PORT; where only the canon has it, the box is an IMPLEMENT and the docs cited
are the spec; where the canon has not ruled, the box is a RULING and nothing
is built until the gap audit carries the decision.

Sources of record, in the order they were read: `AAA_BUILD_PLAN.md`,
`docs/packet/portbrief/{THE-LAWS,PORT-BRIEF,BUILD-ORDER,UE5-MIGRATION-MAP}.md`,
`docs/canon/restoration-game-master.md` (content + Appendix B solutions
matrix), `docs/canon/restoration-design-doc.md` (Part IV mechanics 1–12),
`docs/canon/restoration-walkthrough-levels-endings.md` (saves, threat
architecture, endings, the c043/c046 addenda),
`docs/canon/restoration-player-routing.md`, `docs/canon/restoration-after-fire-chum.md`,
`docs/canon/restoration-casualty-ledger.md`, `docs/canon/restoration-controls-map.md`,
`docs/canon/restoration-reaction-matrix.md`, `docs/canon/restoration-object-taxonomy.md`,
`docs/production/restoration-gap-audit.md` (RULINGS 1–10),
`docs/production/restoration-qa-regression.md` (QA-01..QA-61),
`docs/production/restoration-invariant-suite.md` (I01..I31),
`docs/production/restoration-achievements-design.md` (A01..A28), and the
reference implementation in `scripts/*.gd` (73 scripts, 9286 lines).

Verification for this unit is `tools/verify_mechanics.py` (deterministic,
python3, no engine): it parses this file and `PROGRESS.md` and asserts that
every QA line, every invariant, every achievement, and every reference
script has exactly a home; that every `4.N` box exists in both files and
cites its own evidence ids; and that every canon constant quoted here matches
`ue/Restoration/Data/Timings.csv` to the digit. Run it after any edit to
either file. It prints `VERIFY-OK` or a Traceback.

Constants quoted below use the `Timings.csv` names verbatim so the script
can check them: `ON_AIR_SECONDS = 50.0`, `BREAK_SECONDS = 18.0`,
`CAPTURE_SECONDS = 12.0`, `TETHER = 4.0`, `WARN_RADIUS = 7.0`,
`STRIKE_RADIUS = 2.2`, `AF_APPROACH_SPEED = 0.8`, `AF_LOOM_DIST = 1.2`,
`AF_COOL_SECONDS = 2.0`, `AF_FOLD_SECONDS = 2.2`, `AF_CROSSING_SPEED = 1.6`,
`AF_HEIGHT = 3.35`, `MAX_FRAME = 40`, `BEAT = 0.8`, `WINDOW = 3.2`,
`CROUCH_MULT = 0.55`, `REACH = 2.6`. Numbers the canon owns but the CSV does
not (wear 7 / 3.5 per pass, the 70 wear threshold, the 60 integrity gate,
PT 70 audition, sheet lines 4 / 7 / 0, paper 3 per station per tape,
club auto-fix at or under 40 s, the crossing 75 / 62 / minus 13 s, the first
cool 4.0 s, seek grace 3 s, sight grace about 1 s) are quoted in prose.

---

## §0 · HOMED ELSEWHERE (evidence ids that already have a box)

The QA lines, invariants and achievements below belong to boxes outside
Phase 4 — the Phase 0 core port, the Phase 1 body, Phase 3 rooms, Phase 5
polish — exactly as `BUILD-ORDER.md` assigns them. Phase 4 does not re-home
them; the verifier counts them here so coverage is total.

| Evidence | Home box | Why it lives there |
|---|---|---|
| I08 | 0.6 | every locked door states its reason — stamped from Doors.csv as world text (ticked) |
| QA-12, QA-13, A08 | 0.7 | warn at WARN_RADIUS, strike at STRIKE_RADIUS, savor at ≥3, heard-noise relocation once per run — proven in simulate (ticked) |
| QA-37, I24 | 0.7 | the 2.2 s door fold toll from Doors.csv (ticked); the AF montage itself is 1.10 |
| QA-36, I23, I26 | 0.8a | the taught 4.0 s cool once, 2.0 s after; no strike while recording — the AF layer (ticked) |
| QA-06, A02, I09 | 0.8b-2 | 12 s forced-real-time capture, A CLEAN SIGNAL, the 4 m tether abort (ticked); "abort never costs a daily" is asserted again by 4.9 once dailies exist |
| QA-31 | 0.8b-3 | v15 → v16 load: defaults ARE the migration (PORT-NOTES-STATE §2) |
| QA-05, QA-07, QA-08, QA-09, QA-10, QA-18, I16, I17, A01, A04, A05, A06, A18, A19 | 0.8b-4 | P3 remainder: stations + paper, retake presentation (loupe last), run death card, Harriet freeze, ON_AIR_SECONDS / BREAK_SECONDS window holds, screening stances + assist |
| I01, I02, I06, I22, I31, QA-58 | 0.9 | the harness: the four named invariants plus crouch honesty (byte-identical coverage between walking and crouch-walking bots) |
| QA-52 | 1.10 | the fold is one authored montage at 2.2 s per door width, head last |
| QA-53 | 1.13 | after-fire zero-secondary sweep, gallery + long soak |
| QA-54 | 1.12 | the audio law, the two-beat jaw, the silent bell, no vocalization — wired to AI; the sound assets themselves are 5.1 |
| QA-55, QA-56, QA-57, QA-59 | 3.1 | the taxonomy QA runs per room from 3.1 onward (Phase 3 header) |
| QA-51 | 4.QA51 | the braid audit is the standing Phase 4 audit box the tracker already carried (every premiere pressure peak braids ≥2 demands) |
| I14, I15 | 5.1 | one startle; the silence ledger (fire tape stingless, chairs nameless, the Floor Manager never heard moving) — asset-review gates on the audio pass |

Reference scripts that are NOT Phase 4 mechanics (each has a home or a
reason; the verifier requires every `scripts/*.gd` to be listed here or
cited by a box):

- `scripts/player.gd` — ported in 0.8b-1 (ARitaCharacter, feel parity to the digit)
- `scripts/capture_bench.gd` — ported in 0.8b-2 (ABenchCapture)
- `scripts/interactable.gd` — ported in 0.8b-2 (IRestorationInteractable)
- `scripts/broadcast.gd` — ported in 0.7 (URestorationClock)
- `scripts/rundown.gd` — ported in 0.7 + 0.8a (ARundown tick brain + AF layer); Phase 4 boxes cite it only for the surfaces still unported
- `scripts/game_state.gd` — ported in 0.8a, parity in 0.8b-3 (PORT-NOTES-STATE.md)
- `scripts/log_station.gd` — stations + paper are 0.8b-4; the presigned page on it is 4.10
- `scripts/screening_event.gd`, `scripts/cue_sign.gd` — the screening with stances (BEAT = 0.8, WINDOW = 3.2) and the RESPOND / HOLD signs are 0.8b-4's "screening + assist"
- `scripts/dresser.gd` — the ordered item loss (loupe last) is 0.8b-4's retake presentation (I16)
- `scripts/world_builder.gd` — the greybox was stamped from its CSVs in 0.6; its interactable spawns are the per-box work of Phase 4; its props are Phase 3
- `scripts/bot_driver.gd`, `scripts/soak_runner.gd`, `scripts/invariant_parser.gd` — the harness, 0.9
- `scripts/arm_preview.gd`, `scripts/cast_preview.gd`, `scripts/head_preview.gd` — Godot look-dev rigs, superseded by the UE capture loop (0.2 / 0.3)
- `scripts/character_kit.gd`, `scripts/prop_kit.gd` — mesh-era procedural art kits (873 + 789 lines), superseded by the Blender factory (Phase 1 / 2) and Fab (Phase 3)

---

## §1 · P4 REMAINDER — THE HUNTER AND NIGHTS (after 0.7 / 0.8a)

### 4.1 · Camera cones and tally logic (Law 1: ON CAMERA IS SAFE)
- status: PORT
- ref: `scripts/monitor_rig.gd`, `scripts/rundown.gd`
- canon: THE-LAWS 1; design doc Part IV §2 (mediated viewing is safe, tally logic, shape-coded lamps); walkthrough Part V-B "where a capture cannot happen"; Data/Monitors.csv
- proves: QA-14, I05
- ue: monitor feeds are SceneCapture2D per 0.6b's Spike 2 rig; tally state on the rig actor; the strike guard reads cone membership, never posture
- loop: port the cone test + powered/killed states → tally lamps shape-coded (never color alone, accessibility matrix) → a killed camera is always revivable at the patchbay (4.2) → soak: a bot parked in a live cone for ten night minutes takes zero strikes

### 4.2 · Patchbay routing, the amperage budget, the revive
- status: PORT (v0: one budget, two circuits, "something is always dark") + IMPLEMENT (the building-scale routing puzzle the design doc specifies)
- ref: `scripts/patchbay_console.gd`, `scripts/monitor_rig.gd`
- canon: design doc Part IV §2 (patchbay + power budget; named gap 4: routes, not percentages); game master T2.2, T2.7, T3.5; routing doc movement grammar 2
- proves: QA-14
- ue: an APatchbay interactable over a URoutingBudget (data: which rigs draw what); routing state in the save (v16 `station_points` / map points already carry corridor state — PORT-NOTES-STATE)
- loop: port v0 exactly (PATCHED · X live · Y dark; the budget is the budget) → the panel's polished breaker is the affordance, no outlines → overdraw trips breakers in the worst order, never a soft-lock (I07 keeps the panel reachable) → soak: every corridor can be made live by some legal routing

### 4.3 · The night trip (Night 1, once ever)
- status: PORT
- ref: `scripts/night_trip.gd`, `scripts/floor_manager.gd`
- canon: QA-19; game master T1.4 (the obedience moment); casualty ledger M1 ripple (night trips escalate one stage early if Merle is gone)
- proves: QA-19
- ue: a one-shot night event actor keyed on `night_tripped` in state
- loop: port the trip + the Floor Manager watch (fails on movement, passes on assist-hold) → captioned, no sting (Law 2) → failing it is a retake, never a run death → test: fires exactly once per save across reload

### 4.4 · The Floor Manager (hands only: signals, YOU'RE ON, the seventh)
- status: PORT + IMPLEMENT (reaction queue F-R1 the early point at the doorway, F-R2 her mark to the empty half)
- ref: `scripts/floor_manager.gd`, `scripts/film_cabinet.gd`, `scripts/harriet_note.gd`
- canon: design doc Part I + IV §3 (the signal glossary is the threat-telegraph UI); game master Appendix C glossary; reaction matrix F-R1/F-R2; casualty ledger F2 (the freeze-check inverts after the unlisted camera)
- proves: QA-41, A07
- ue: a hands-only pawn with a signal state machine; `signals_known` gates which signals the player can read; HOLD YOUR APPLAUSE is Harriet-only (unlearnable if her card was unfound, QA-41)
- loop: port the signals + freeze check → every signal renders as a real hand pose, never text-first → a missed signal marks Rita as performance (fail condition 4), retake → test: signal log matches world events (build plan invariant 6)

### 4.5 · The cascade (Night 4+: C then B, the waived window)
- status: PORT
- ref: `scripts/cascade.gd`, `scripts/liveness_check.gd`, `scripts/door.gd`, `scripts/patchbay_console.gd`
- canon: QA-20; I04, I07; casualty ledger V2 (GET VESS at the dead panel; circuit F); achievements A15 ORDER MATTERS
- proves: QA-20, I04, I07, A15
- ue: a cascade sequence actor; liveness_log cadence every 5 s, VIOLATION on breach, in the parser's exact format (UE5-MIGRATION-MAP: log formats never change)
- loop: port the order refusal (B before C) + waived holds during `cascade_active` → doors read their reason, the panel reads the order → the panel is always reachable (I07) → test: doors deliberately closed, liveness OK every 5 s

### 4.6 · Noise, segment audio, and the dead room (Law 11: the one dark hide)
- status: PORT
- ref: `scripts/noise_tracker.gd`, `scripts/tone_emitter.gd`, `scripts/rundown.gd`
- canon: THE-LAWS 11; after-fire canon THE TWO HIDES; walkthrough Part V-B (the audio tells you which segment, therefore where it is); game master Appendix C segment pool; QA-38; I25
- proves: QA-38, I25
- ue: ReportNoise already exists on ARundown (0.7); the dead room is a volume whose interior noise never reaches `_on_noise`; segment tones become MetaSounds in 5.1, the emitters are placed here
- loop: port the tracker + the dead-room deafness + the felt-door hold and his one line → first entry gives the radio toast and [NO ECHO] → nothing inside the room can ever be heard, so nothing inside can ever be punished → soak: bot signs and slams inside; his target must not move (I25)

### 4.7 · The tally HUD and the eye's light (Law 10 made visible)
- status: PORT
- ref: `scripts/hud.gd`
- canon: THE-LAWS 10; after-fire canon THE COUNTDOWN, VISIBLE (REC · SAFE WHILE LIT, one number two meanings) and THE SCALE LAW (the eye burns only while a capture runs); QA-33, QA-34, QA-35; 0.3's known delta "tally not yet emissive in UE"
- proves: QA-33, QA-34, QA-35
- ue: the HUD lamp reads `bRecording` + `RecordingLeft` (0.8b-2 already drives them); the eye emissive on SK_ChumAF's tally material is switched by the same fact — one bool, two lights; the material itself is 1.12
- loop: port the lamp + first-sighting toast (once per save) + wake toast → AF_APPROACH_SPEED footfalls thunk on interval with distance-scaled captions → the countdown is progress and expiry at once, never hidden → test: eye dark the instant a capture stops or aborts; `af_active` persists across save/load

### 4.8 · The Coverage Director (profile, blockings, the poisoned well)
- status: PORT (v0 profile: checker / sprinter / hider from behavior, coverage_log, burning resets the read) + IMPLEMENT (blockings A/B/C per scripted scare, the mood law, the once-per-run monitor lie with its static telegraph, the poltergeist layer that never stages the dock)
- ref: `scripts/coverage_director.gd`, `scripts/dailies_manager.gd`
- canon: design doc Part IV-B §12; game master Appendix A blocking table (12 × 3) + mood law; build plan risk 2 (four booleans and a corridor histogram, never ML); I21
- proves: I21
- ue: a world subsystem writing coverage_log in the parser's format; blockings are data (scare id × profile → staging id) with a reason string per decision
- loop: port v0 counters + reset-on-burn → every decision logs a reason (explainable) → the well is poisoned at most once per run, always with rising static → test: input-replay diff yields identical profiles (Spike 5)

### 4.9 · Burn Your Dailies (the strike-recovery errand)
- status: PORT
- ref: `scripts/dailies_manager.gd`, `scripts/dailies_canister.gd`, `scripts/degausser.gd`, `scripts/casting_sheet_prop.gd`
- canon: walkthrough Part V-B (the casting sheet is the cap: 4 / 7 / 0 lines; every capture types RITA IVORI; degaussing fades the line; unburned canisters are the Director's scouting film); design doc §12; I09
- proves: I09
- ue: canisters spawn from `dailies` in state after each strike; the degausser is an interactable that decrements `strikes` and fires `daily_burned` (which 4.8 listens to)
- loop: port spawn + burn + the sheet prop that reads the count → the sheet is a physical wall object the club dusts → aborting a capture never mints a daily (I09) → test: sheet count, canisters and item-loss ledger reconcile after any sequence of captures and burns (build plan invariant 8)

---

## §2 · P5 — STORY GATES

### 4.10 · The presigned page (the save scare, singular)
- status: PORT
- ref: `scripts/log_station.gd`
- canon: game master T3.6; walkthrough Part V "the save scare"; QA-21; I10; A09
- proves: QA-21, I10, A09
- ue: a branch in the station interactable: Day 2+, S4, zero paper → the page appears, signs free, once (`presigned_seen`)
- loop: port the branch → her handwriting, tomorrow's date, no interface deception (Law 8 is untouched) → costs no paper ever → test: save diff shows a signature added and paper unchanged

### 4.11 · The impossible crate and the frame-séance
- status: PORT
- ref: `scripts/impossible_crate.gd`, `scripts/seance_dock.gd`, `scripts/frame_sequence.gd`, `scripts/tape_stage.gd`
- canon: design doc Part IV §7; game master T4.4 (the five-question thread, verbatim) and T4.7; routing thread 1A (the Leland discipline: wear 7 / 3.5 per pass, five answers, the 60 integrity gate); QA-22, QA-50; I20; A14; casualty ledger L1 / L2
- proves: QA-22, QA-50, I20, A14
- ue: frame stepping on Z / X (controls map) over a MAX_FRAME = 40 sequence; grain seeded by frame index so frame 14 is always frame 14; wear burns in across retake and reload (walkthrough Part V)
- loop: port the crate gate + the dock + the wear ladder → answers arrive across frames on his legal pad, grief variants at frames 14 and 28 → the sixth question is offered only past five answers AND wear above 70 (QA-44) → test: capture frame 14 twice across relaunches and diff

### 4.12 · The fire tape (forced watch; the wake)
- status: PORT
- ref: `scripts/fire_tape_pickup.gd`, `scripts/fire_tape_dock.gd`, `scripts/merle.gd`
- canon: game master T3.4 (no sting anywhere); after-fire canon THE REVEAL (watching sets `af_active`); casualty ledger M1 (the second viewing); QA-23, QA-40; A13
- proves: QA-23, QA-40, A13
- ue: a dock interactable that plays the sequence through 4.15's stage, marks `fire_tape_watched`, and broadcasts the wake once per save
- loop: port pickup + dock + Merle's offer (refusing saves her; consent plays the repossession) → the wake toast fires once, the band-step-down cut is 5.1's → the watch cannot be skipped and cannot kill → test: the wake bleed occurs exactly once per save

### 4.13 · The scene dock (the contract room; the warm one never acts)
- status: PORT
- ref: `scripts/dock_task.gd`, `scripts/dock_chum.gd`, `scripts/asset_pickup.gd`, `scripts/asset_rack.gd`
- canon: THE-LAWS 4; game master T4.3; walkthrough Part III principle 6 (nothing springs in the dock); QA-24; I12, I19 (the dock card gates on the filed inventory); A10
- proves: QA-24, I12, I19, A10
- ue: an inventory task over six units; the sign-off card asset pickup unlocks on `dock_done`; no code path may follow the warm unit — I12 is a review rule on every commit here
- loop: port the task + the card gate → the count is diegetic (row by row) → completing it triggers nothing, ever → test: full-run tail watch; the achievement text never mentions warmth

### 4.14 · The unseal and the glimpse (Law 3: once, ever)
- status: PORT
- ref: `scripts/glimpse.gd`
- canon: THE-LAWS 3; game master T4.8; walkthrough Part IV; QA-25; I11; achievements doctrine 2 (no achievement, ever)
- proves: QA-25, I11
- ue: `fire_unsealed` opens the corridor on Day 4; `glimpse_seen` is the single-spawn guard; its name appears in no code file (Law 3) — keep the class name as the reference has it
- loop: port the unseal + the one spawn → under two seconds, unmediated, undecidable, no caption names it → nothing references it afterward, including logs → test: single spawn per save lifetime including relaunch

### 4.15 · The tape world: stage, bench TV, frame sequences, the one startle
- status: PORT
- ref: `scripts/tape_stage.gd`, `scripts/bench_tv.gd`, `scripts/frame_sequence.gd`
- canon: design doc Part II (the two render worlds; authentic period video, generation loss modeled per dub) and Part III (TBC = photosensitivity mode); THE-LAWS 2 (the in-tape lunge is the single startle); gap audit ruling 8 (photo mode Tier B, day, never him); build plan spike 1
- proves: (none of its own — I14 / I15 are 5.1's; QA-23 is 4.12's; the surface is shared by 4.11, 4.12, 4.19)
- ue: MediaFramework playback into the CRT material-function stack with the same parameter names (UE5-MIGRATION-MAP); bars, screening, fire and séance frames all play through one stage
- loop: port play_tape / play_screening / play_fire / set_seance_frame + bars → the TBC toggle stabilizes flicker across the whole game as an in-world device → no tape ever harms outside the lunge's authored beat → test: photosensitivity audit passes with TBC on, on every tape asset

### 4.16 · Sign-off assets, the Vess credit dilemma, the rejected edit
- status: PORT
- ref: `scripts/asset_rack.gd`, `scripts/vess.gd`, `scripts/vess_binder.gd`, `scripts/rejected_edit.gd`, `scripts/harriet.gd`
- canon: walkthrough Part VII tracked variables (assets 0–4); game master T2.3 FORCE (the insight + the wrong theory), T4.5, Appendix B; casualty ledger V1 / V2 / H2 (the splice temptation discloses her label); QA-42, QA-49; A11; reaction matrix V-R1..3
- proves: QA-42, QA-49, A11
- ue: `assets`, `vess_insight`, `vess_credited`, `h2_pending` in state (PORT-NOTES-STATE); the rejected edit plays through 4.15
- loop: port the four pickups + the binder + the edit + the splice offer → the take-up reel turns backward one rotation, the label is disclosed before the cut → both of Vess's graves are dug by opposite choices, never by chance (Law 7) → test: the credit flag closes at the end of Tape 4 and never reopens

### 4.17 · The decision ledger and THE BURN
- status: PORT
- ref: `scripts/decision_ledger.gd`, `scripts/degausser.gd`
- canon: game master T5.2 + ENDING 3; walkthrough Part VII (Authenticate → 2, Destroy → 3, Perform → 1 / 4); walkthrough named gap 4 (Merle in the doorway is the point of no return, no modal); A17, A21
- proves: A17, A21
- ue: three entries in her hand; `decision` in state; the burn is playable destruction at the degausser and the bake oven (the oven is 4.28's if it is ever ruled in; today the reference burns at the degausser)
- loop: port the pen + the three commits → INK toast, the pen is the loudest thing in the building → Destroy is always available from Tape 4, never a dead end → test: each entry routes to its ending across the matrix (QA-28)

### 4.18 · Lockdown (permanent: sealed doors, synced monitors, rowed chairs)
- status: PORT
- ref: `scripts/lockdown.gd`, `scripts/rec_chairs.gd`, `scripts/door.gd`, `scripts/monitor_rig.gd`, `scripts/coat_pegs.gd`
- canon: game master T4.10; QA-26; I18; A20; casualty ledger THE ROWS (seats taken by abandoned incidents persist)
- proves: QA-26, I18, A20
- ue: `lockdown_done` re-applies sealed doors (SEALED FOR BROADCAST reason text), monitor sync, chair rows and frozen pegs on ready
- loop: port the sequence + the re-apply → doors state their reason, the RESPOND sign burns steady → reversibility ends here loudly, once (routing grammar 5) → test: relaunch after lockdown, everything holds (I18)

### 4.19a · The premiere: cues, incidents, the rows (fail-forward as a mortgage)
- status: PORT
- ref: `scripts/live_production.gd`, `scripts/finale_fixture.gd`, `scripts/finale_breaker.gd`, `scripts/floor_manager.gd`
- canon: design doc Part IV §9; game master T5.3 cues 1–5 (verbatim), Appendix A scares 10–12; walkthrough named gap 3 (never soft-lock); casualty ledger THE ROWS, F2, V1's breaker trigger, M2; QA-27, QA-43, QA-46, QA-51 (the braid audit is the 4.QA51 box); I03, I05, I06
- proves: QA-27, QA-43, QA-46, I03, I05, I06
- ue: a live-production director actor with premiere_log in the parser's format; every incident type carries a guarantee (club auto-fix at or under 40 s; tally refusals never exceed 2; boom holds exactly 1); the Rundown never hunts while the show is live (I03)
- loop: port the cue runner + incident types + rows → cue marks highlight on the PGM camera only while the Floor Manager lives (QA-43) → every incident fail-forwards inside its guarantee, each abandonment takes a seat → soak: FAIL-BOT fails every cue thrice, leaves every incident; RESOLVED lines at or under 40 s

### 4.19b · The last crossing and the divert (DEAD AIR's price)
- status: PORT
- ref: `scripts/live_production.gd`, `scripts/rundown.gd`, `scripts/hud.gd`
- canon: after-fire canon THE LAST CROSSING (75 s, AF_CROSSING_SPEED, folds still AF_FOLD_SECONDS apiece, eye dark the whole way); casualty ledger F1 (the fader: his hand or hers, self-hold costs 13 s and an arm), V-dead hard mode (the crossing runs 62); controls map (fader = SPACE his hand, E held 4.6 s hers; RT on pad); QA-28, QA-44 (L2 → 4c, no divert prompt)
- proves: QA-28, QA-44
- ue: `crossing`, `crossing_caught`, `fader_self`, `signoff_completed` in state; the divert gate is key + answers + the fire tape (I19)
- loop: port the divert gate + fader choice + the crossing timer → the fader is the same finger as the recording, on purpose → three authored outcomes (reach, caught, too slow), all hers → test: the three outcomes each reachable by a scripted bot

### 4.20 · The casualty ledger (Law 7: every death has a signature)
- status: PORT
- ref: `scripts/game_state.gd`, `scripts/merle.gd`, `scripts/harriet.gd`, `scripts/patchbay_console.gd`, `scripts/seance_dock.gd`, `scripts/hud.gd`
- canon: THE-LAWS 7; the casualty ledger whole (M1 / M2 / H1 / H2 / V1 / V2 / F1 / F2 / L1 / L2, the rows, the full board, AS BUILT deviations); QA-39, QA-40, QA-41, QA-42, QA-44, QA-45, QA-47; I27, I28, I29, I30; A27, A28
- proves: QA-39, QA-45, QA-47, I27, I28, I29, I30, A27, A28
- ue: `casualties` (array of ids with cause tags) + the per-death flags; mark_casualty idempotent; binder page one reads NO ENTRIES. KEEP IT SO. until a death
- loop: port the ledger + every trigger as the reference orders them → each entry in stamp register: who, cause, day, epitaph → deaths are idempotent, the reading matches the page exactly → test: force both Vess triggers in sequence; string-compare the epilogue to the page at credits

### 4.21 · Endings, credits, the reading, the one interface lie
- status: PORT
- ref: `scripts/hud.gd`, `scripts/credits.gd`, `scripts/credit_entry.gd`, `scripts/title.gd`
- canon: game master THE ENDINGS, SCRIPTED (1A, 1B, 2, 3, 4) + design doc Part III (the lie is spent once, post-credits of ending 2); walkthrough addendum c043 (4a / 4b / 4c / 0); THE-LAWS 8; QA-03, QA-28, QA-47; I13; A21, A22, A23, A24, A25
- proves: QA-03, I13, A22, A23, A24, A25
- ue: one ending runner per id; the credits crawl opens with THE LEDGER, READ ALOUD when anything is in it; `lie_pending` flips CONTINUE? / NEW EPISODE on the next title only, then reverts
- loop: port every `_end_*` + the crawl + the lie → the crawl's tower-light card holds, any key after grace skips → ending exits always roll credits, no ending is ever locked by deaths → test: reach ending 2, relaunch twice (I13); attempted-access test proves the lie is unreachable elsewhere

### 4.22 · The house: coat pegs, Merle's stations, Harriet's holding pattern, the bed
- status: PORT + IMPLEMENT (reaction queue M-R1..M-R6, H-R1 / H-R2 the lengthened freezes, B-R1 / B-R2 the bulbs — the 4.WEB box audits them)
- ref: `scripts/coat_pegs.gd`, `scripts/merle.gd`, `scripts/harriet.gd`, `scripts/bed_prop.gd`, `scripts/wall_clock.gd`
- canon: QA-11 (pegs drift per day table; Merle at kettle, chair or DOORWAY per schedule and pen state, never elsewhere); THE-LAWS 6; reaction matrix; game master T4.6 (Merle, 1974 — A12); object taxonomy (drift is dressing-only; the pegs are drift ground zero, Room Bible 3.1)
- proves: QA-11, A12
- ue: schedule-driven placement from the clock; the bed advances the day (declines under DEMO per QA-30)
- loop: port the day table + the stations + the bed → nothing that prompts ever moves (QA-56); only dressing drifts → the club never harms, never blocks a route → test: Merle's position is one of three, always; peg state matches the day

### 4.23 · Readables, keys, the D-series and the ambient covenant
- status: PORT
- ref: `scripts/readable_prop.gd`, `scripts/key_item.gd`, `scripts/harriet_note.gd`, `scripts/casting_sheet_prop.gd`
- canon: object taxonomy (handled lore prompts and marks read; AMBIENT LORE NEVER PROMPTS; registry D01–D11 with homes per the Room Bible); game master Appendix D (canonical found text); A16 THE LONG WAY AROUND (the QUIET ROOM key), A26 FULL ACCESSION (D01–D10; D11 is extra credit)
- proves: A16, A26
- ue: `read_props` and `keys` in state; readables carry their text keys from GameText.csv (714 keys, 0.5)
- loop: port the readable + key interactables → the Three Reads Rule holds per readable → keys never gate an ending, only a route (Appendix B law) → test: QA-59 per room (Phase 3) reads every ambient item at three depths; A26 counts exactly ten

---

## §3 · THE PUZZLES (Appendix B, obstacle by obstacle)

### 4.24 · Airdate math (141 slated, 138 aired, three names)
- status: IMPLEMENT — no reference code; the four paper sources and the GEN field are the whole puzzle
- ref: (none)
- canon: game master T2.3 + Appendix B row 1 (PRESERVE G1: four sources; ASK G3: Merle's canon; FORCE G2: Vess's binder, one insight + one wrong theory); design doc Part IV §6 + §11 (generations; every G2 source carries exactly one authored gap); room inventory / ambient lore ledger for where each source lives
- proves: (none yet — write QA-62 when the box opens: the three names assemble only in the player's log, never stated)
- ue: four readables + a ledger form with a GEN field the player fills; the truth is never autocompleted
- loop: implement the four sources as readables and the ledger form → the ledger's GEN field accepts G1 / G2 / G3 and the club reads it → no generation gates an ending (Appendix B law) → test: a bot that reads only Merle's canon can still finish the game

### 4.25 · The film cabinet (six signals; the seventh; the pry)
- status: PORT (built: the key tagged TRAINING, the 1971 orientation film, `signals_known`, Harriet's seventh via her note) + IMPLEMENT (the FORCE variant: pry it, four of six survive, the rest learned live)
- ref: `scripts/film_cabinet.gd`, `scripts/harriet_note.gd`
- canon: game master T2.4 + Appendix B row 2; design doc §11 worked example; casualty ledger H1 (the seventh is unlearnable if her card was unfound)
- proves: A07
- ue: the cabinet interactable plays through 4.15; `film_watched` + `signals_known` feed 4.4
- loop: port the key path + the recital → the film is real floor-signal vocabulary, taught once, trusted forever → the pried film's dropouts are honest gaps, not softlocks → test: the seventh signal grants the 3 s grace on the unscripted seek (QA-41's inverse)

### 4.26 · The missing verse, the spectrogram, the assembled frequency
- status: PORT (the spectro dock and the verse extraction) + IMPLEMENT (the audio bench as a tool; the three-fragment frequency assembled at the bench for DEAD AIR: verse sidebands T2, fire-tape carrier T3, impossible-tape subcarrier T4)
- ref: `scripts/spectro_dock.gd`
- canon: game master T2.6 + Appendix B row 3 (Harriet hums it with one wrong word — HERE for HOME — and the finale variant beat follows); routing thread 4 step 2; walkthrough tracked variables (Dead Air set: 3 items)
- proves: (none of its own — the assembled frequency is exercised by 4.19b)
- ue: fragments as flags in state; the dial at the dead room radio confirms the number (4.30 reuses the radio)
- loop: port the dock + extraction → structure in the sidebands is visible in the actual audio (shipped soundtrack files are minable, design doc §1) → the hummed version is a real alternative with a real fault line → test: both verse sources reach the finale; the epilogue static carries the fault either way, ungraded

### 4.27 · The provenance suite: the GEN knob, the accession log, the light table
- status: PORT (the GEN knob: "you turned the knob, the label did not care") + IMPLEMENT (the accession log as a form the player fills: date, generation, provenance, contents; truth versus cover entries as the Conduct Ledger; the light table for paper overlays)
- ref: `scripts/gen_knob.gd`, `scripts/decision_ledger.gd`
- canon: design doc Part IV §6 (the journal is a stance) + §11; game master T1.5 LEDGER COMMITMENT 1 (TRUTH / COVER), T2.3; gap audit ruling 4 (THE BINDER IS THE INVENTORY: possession is recorded, not managed)
- proves: A03
- ue: ledger entries as data rows in the save (v16 has no field for conduct entries yet — a v17 candidate; gap audit technical gap "save-migration policy once v17 exists")
- loop: port the knob → the club reads your log and reacts in character (4.WEB) → logging a cover story is never a fail state (walkthrough: never fail conditions) → test: the Vess-credit flag derives from entries, not a menu

### 4.28 · The bench craft suite: bake, splice, quality grade
- status: IMPLEMENT — design doc Part IV §1 specifies bake (temperature-and-time hold), splice (loupe alignment, permanent on the master) and the grade (the club's rubric; high grades feed the Producer Track); the reference ships the capture and the tether only (0.8b-2) and the splice as a temptation (H2, 4.16)
- ref: (none — `scripts/rejected_edit.gd` is the only splice in the reference and it is 4.16's)
- canon: design doc Part IV §1; game master T1.3 tutorial (inspect, bake timing, splice, capture, ledger entry); build plan M1 (full restoration suite); walkthrough Part V burn-in rule (splice surgery persists across retake and reload)
- proves: (none yet — write QA-63..65 when the box opens; the burn-in invariant is build plan invariant 7)
- ue: bench sub-tools as interactables on the bench actor; the oven doubles as THE BURN's film heat (4.17)
- loop: implement bake → splice → grade → every tool visibly alters the tape-world artifacts (restoration quality is diegetic, never a popup) → bench mistakes cost tapes, never life → test: burn-in survives retake, reload and crash recovery

### 4.29 · RULINGS FIRST: the unruled canon verbs
- status: RULING — the gap audit's mechanics list (1–10) rules sprint, crouch, binder time, inventory, difficulty, death card, saves, photo, NG+, interaction feel; it does NOT rule these design-doc verbs, and the plan's doctrine says consult rulings before re-deciding anything. File each as a gap-audit line with a proposed ruling; build nothing until ruled.
- ref: (none)
- canon: design doc Part IV §2 AVERT (hold to raise the clipboard; the notebook is the shield), §5 THE QUIET GAME breath (mic or hold-and-release rhythm; the controls map ships stillness as the check, not breath), §3 formal-correctness phrases ("That's all for today, Chum" forces a scene exit on a valid beat), §8 the PRODUCER TRACK tells (the reference keeps `pt` with the PT weights; the binder's casting drift, the reflection budget and the club's ceremony are unbuilt), walkthrough Part III principle 5 THE CATWALKS (the greybox carries the geometry; the route above the format and its ladder noise are unbuilt), design doc §12 THE POLTERGEIST LAYER (staged props that always resolve as legal, never in the dock), design doc Part V bench controls (jog wheel spring return, tape tension on triggers); build plan descope ladder (mic input dies first; blocking C second)
- proves: (none — a ruling produces QA lines; it does not consume them)
- ue: n/a until ruled
- loop: propose → the author rules in the gap audit → the ruled verbs become IMPLEMENT boxes here (sub-boxes of 4.29) → each arrives with its QA line

### 4.30 · The secret eighth ending: the unnumbered reels and AUDIENCE ONLY
- status: IMPLEMENT — canon c046 (walkthrough addendum THE SECRET) with QA-60 / QA-61 written; no reference code exists for W1–W3, the radio dial confirm, the 75 s run to the dead room, the program guide or the title mark
- ref: (none)
- canon: walkthrough ADDENDUM · SPOILER · THE SECRET (c046); QA-60, QA-61; achievements ruling (no achievement, by design: the acknowledgment is its absence); gap audit ruling 9 (NG+ parked — the title mark 58 · STILL ON is not NG+, it is a permanent mark)
- proves: QA-60, QA-61
- ue: three findables gated in order by day and by four clean dailies; each viewing spends one S2 slip; the dead room radio (4.6) gains CONFIRM after W3; the final break gains its caption only then
- loop: implement W1 → W2 → W3 → the radio confirm → nothing announces on completion; the caption is a radio through three walls → declining or arriving late falls through to the normal break chain untouched → test: QA-61 end to end by a scripted bot, plus the title mark on every later launch

---

## §4 · P6 — META AND MODES (Law 9: ACCESS IS CANON)

### 4.31 · The title and the booth (options, remap, first launch)
- status: PORT
- ref: `scripts/title.gd`, `scripts/options_panel.gd`
- canon: QA-01, QA-02, QA-04, QA-16, QA-17; THE-LAWS 9; controls map (remap covers five verbs today with conflict refusal; the UE target is every action remappable including movement; hold ↔ toggle contract); accessibility matrix; PORT-NOTES-STATE §4 (settings.cfg schema)
- proves: QA-01, QA-02, QA-04, QA-16, QA-17
- ue: settings persist outside the save (the settings.cfg contract); glyphs swap to pad iconography the frame a pad speaks
- loop: port the booth + BEFORE THE SHOW first launch + FILED WHILE YOU WERE OUT → every slider and check is a WGLD form (station paperwork) → NEW GAME leaves settings intact; KEY IN USE refuses conflicts → test: relaunch persistence; remap onto E refused, onto an unused key propagates to every prompt

### 4.32 · Achievements with the deferral rule (meta-silence)
- status: PORT
- ref: `scripts/achievements.gd`
- canon: achievements design v1 + c043 addendum (A01–A28; the deferral rule's two flush gates; the meta-silence ledger: the glimpse has none, Chum's name in none, the warm unit only via the dock; disabled under DEMO); QA-29; I30
- proves: QA-29, I30
- ue: a GameInstance subsystem with unlock(id) idempotent, a queue, flush on night_changed(false) and on the title's ready; the Steam bridge is a plain delegate (id table is the API)
- loop: port the queue + gates + the list → the morning shows FILED lines in the ledger's register → no toast ever lands between title and morning, ending 0 included → test: grep the event table per build; force every death and assert zero mid-play toasts

### 4.33 · Modes and the demo (MATINEE / LATE_NIGHT / ONE_TAKE; DEMO whitelist; Tape 1 funnel)
- status: PORT
- ref: `scripts/game_state.gd`, `scripts/bed_prop.gd`, `scripts/capture_bench.gd`, `scripts/bench_tv.gd`
- canon: walkthrough Part V-B modes (four-line sheet + paper economy + full aggression; seven lines + unlimited paper + halved wear + longer tells; any capture final); gap audit ruling 5 (ASSIST only, one game honestly tuned — the modes are presentation, not difficulty); QA-30, QA-48; PORT-NOTES-STATE §5 (what DEMO strips); Data/DemoOpen.csv (7 rooms); demo cut plan
- proves: QA-30, QA-48
- ue: `Mode` on the save (default LATE_NIGHT = 1 — 0.8b-3 fixes the skeleton's 0); DEMO as a build flag with the save whitelist
- loop: port the mode arithmetic + the whitelist + the funnel file (six marks) → doors carry demo reasons, the bed declines, the card protects three seconds → no death is reachable in the demo, no casualty field survives its save → test: QA-30 and QA-48 line by line on a DEMO build

### 4.34 · Pause, the binder, the map (time rulings 3 and 4)
- status: PORT
- ref: `scripts/hud.gd`, `scripts/map_view.gd`, `scripts/player.gd`
- canon: gap audit rulings 3 (binder and map true-pause in the day, LIVE during the premiere only) and 4 (the binder IS the inventory); design doc Part III (meta UI is station paperwork); QA-15, QA-32; controls map (TAB binder, M map, ESC pause)
- proves: QA-15, QA-32
- ue: pause holds world and clocks and mutes audio; refused during any authored sequence; the map draws sealed rooms dashed, station dots labeled, the BOUND key in the footer
- loop: port the binder + map + pause gate → every page is WGLD letterhead; casting drift dresses it as PT rises (dressing, never deception — design doc named gap 2) → the premiere's live binder is the one place the monitor tax exists → test: pause during the fire tape refused; pause anywhere unlocked holds clocks

### 4.35 · Captions, glyph substitution, SFX cues and the string table
- status: PORT
- ref: `scripts/sfx.gd`, `scripts/hud.gd`, `scripts/game_state.gd`
- canon: design doc Part III captions (period television captions with speaker tags and directional sound captions — the full fear channel); accessibility matrix; PORT-NOTES-STATE (GLYPH_MAP substitution in every toast); Data/GameText.csv (714 keys, 0.5); localization plan; gap audit technical gap (translation registration for localized builds)
- proves: (none of its own — QA-05's pen-tick caption is 0.8b-4's; every box above emits through this surface)
- ue: a caption subsystem fed by the `caption` delegate; string table from GameText.csv; sfx cues become MetaSounds in 5.1, the cue ids are fixed here
- loop: port the caption channel + glyph substitution + the string table → every prompt renders the player's ACTUAL binding per device, always → captions never miss a threat sound (footsteps, the fold's two ticks, the cool) → test: a captions-on soak logs a caption for every telemetry line that has a sound

---

## §5 · WHAT THIS ENUMERATION DOES NOT DO

It does not tick anything but 4.0. It does not reorder Phase 0 (0.8b-3, 0.8b-4,
0.9, 0.10 stay ahead of every box here — the parity gate is the door to
Phase 4). It does not invent mechanics: the three IMPLEMENT boxes without
reference code (4.24, 4.28, 4.30) are each named in the canon with page
references above, and 4.29 explicitly refuses to build unruled verbs. The
standing audit boxes the tracker already carried (4.WEB, 4.SAVE,
4.ENCOUNTERS, 4.FINALE, 4.QA51, 4.VERB, 4.FINAL) are kept verbatim and
unticked; 4.FINALE and 4.SAVE are gates over 4.19a/b and 4.10–4.21
respectively, not duplicates of them.
