# RESTORATION · QA EXECUTABLE (C13) — every regression line as a UE proof, or OPEN

For each line of `docs/production/restoration-qa-regression.md` (the QA
REGRESSION SCRIPT v1: "every line is action, then expected"), this file names
the thing that PROVES it in Unreal Engine 5.8: an existing fixture under
`ue/pyscripts/`, a named automation test to write, a capture to take and look
at, a static inspection to run, or a device pass a human must sit — and where
none of those can be designed yet because canon is silent or the system has
no port, the word **OPEN**. Every rule asserted carries a citation
`[KEY §section]` or `path:line` (keys in §0.1). Nothing here invents canon;
where a QA line, a law and the reference code disagree, all three are quoted
and the disagreement is an OPEN in §4, not a ruling.

This is a paper deliverable from the cloud lane: no Unreal, no Blender, no
Godot was run. Every fixture marked EXISTS was last run at HEAD 4ba8db8 by the
Mac lane (`ue/GATE-0.10-EVIDENCE.md` line 1); its expected lines below are
quoted from that evidence, not re-observed here. Every fixture marked DESIGNED
is a specification the Mac lane builds when the unit that owns the system
lands; none of them exists today.

**The count.** The tracker box says "the 51 QA items" [PROGRESS §CLOUD LANE
BACKLOG C13]. The canon file has **61** lines, QA-01 to QA-61
[restoration-qa-regression.md lines 5–85]; at its first intake (commit
c974da2) it had 58, at the packet intake (799933f) 61, and at no commit 51.
QA-51 is also the id of the braid audit the comparative study added
[restoration-comparative-study.md adoptions; AAA_BUILD_PLAN §5 PHASE 4], which
is the likeliest origin of the box's "51". This file covers all 61 so that
nothing in the regression script is dropped; the box's count is **OPEN-0** for
the owner (§4). Rows 52–61 are the addenda (the after-fire, the ledger, the
object law, the secret) and are marked as such in §2.

---

## 0 · CONVENTIONS

### 0.1 Source keys

| Key | Path |
|---|---|
| QA | `docs/production/restoration-qa-regression.md` (the 61 lines; quoted verbatim per row) |
| INV | `docs/production/restoration-invariant-suite.md` (I01–I31) |
| PROTO | `docs/production/restoration-playtest-protocol.md` (probes P1–P26, verdicts V1–V7) |
| LAWS | `docs/packet/portbrief/THE-LAWS.md` (11 laws) |
| PLAN | `AAA_BUILD_PLAN.md` (§0 protocol, §1 doctrine, §4 verification loop, §5 work breakdown) |
| PROGRESS | `PROGRESS.md` (unit ids cited as "unit 0.8b-5", "unit 4.ACCESS" etc.) |
| GATE | `ue/GATE-0.10.md` (the parity-slice package and the owner's §5 rulings) |
| EVIDENCE | `ue/GATE-0.10-EVIDENCE.md` (verbatim fixture output at HEAD 4ba8db8) |
| LAW9 | `docs/production/UE-ACCESS-SPEC-LAW9.md` (booth, captions, assist, remap, pause, deferral — named tests in §2.4/3.4/5.4/6.4/7.4/8.4) |
| PN-STATE / PN-BROADCAST / PN-RETAKE / PN-SCREENING / PN-FINALE | `ue/PORT-NOTES-STATE.md`, `-BROADCAST.md`, `-RETAKE.md`, `-SCREENING.md`, `-FINALE.md` (the transcriptions the port reads from) |
| AUDIT | `ue/PORT-AUDIT-1.md` (C++ vs GDScript drift checklist) |
| MOTION | `docs/canon/restoration-chum-motion-and-sound.md` |
| WALK | `docs/canon/restoration-walkthrough-levels-endings.md` |
| TAX | `docs/canon/restoration-object-taxonomy.md` |
| LORE | `docs/canon/restoration-ambient-lore-ledger.md` |
| ACH | `docs/production/restoration-achievements-design.md` |
| PRESENCE | `docs/production/restoration-steam-presence.md` |
| DEMO | `docs/production/restoration-demo-cut-plan.md` |
| GAP | `docs/production/restoration-gap-audit.md` |
| CONFORM | `docs/production/restoration-accessibility-conformance-pass.md` (§5 THE DEVICE PASS) |
| TIMINGS | `ue/Restoration/Data/Timings.csv` (32 canon constants with homes) |
| GAMETEXT | `ue/Restoration/Data/GameText.csv` (714 keys) |
| PARSER | `tools/invariant_parser.py` (the scorecard; exit 0 iff no FAIL) |
| REF | the reference implementation, `scripts/*.gd` — "the code is the intent" [`docs/packet/portbrief/PORT-BRIEF.md` line 2, cited via PLAN §1 THE PORT KIT] |
| UE | `ue/Restoration/Source/Restoration/*.h,.cpp` at origin/main cff3914 |

### 0.2 Proof kinds

| Kind | Meaning | How it is run |
|---|---|---|
| **FIXTURE** | A headless editor-python script under `ue/pyscripts/` that spawns actors, simulates N seconds, and appends telemetry to `ue/Restoration/Saved/decision_log.txt`; verdict by grep or by PARSER | `UnrealEditor-Cmd ue/Restoration/Restoration.uproject -run=pythonscript -script=ue/pyscripts/<name>.py -unattended -nop4 -nosplash`, then `python3 tools/invariant_parser.py ue/Restoration/Saved/decision_log.txt [--bot fail]` [PLAN §1 "Automation loop"; PARSER docstring lines 1–19; EVIDENCE lines 3–4] |
| **TEST** | A UE Automation Framework test (`-ExecCmds="Automation RunTests <name>"`), named `Restoration.<Area>.<Case>`; names already fixed by LAW9 are reused verbatim [PLAN §1 "Automation loop"; LAW9 §2.4–§8.4] |
| **CAPTURE** | A HighResShot / MRQ still or frame sequence archived under `docs/telemetry/ue-baselines/`, judged by eye per PLAN §4 step 4 ("look at them (ACCEPTANCE VIEW)"); for motion ≥ 8 frames [PLAN §4 "Animation units"] |
| **INSPECT** | A static check: a grep over `Source/` or `Data/`, a CSV row-count assertion (the `tools/extract_data.py` style), or a save-file diff — scriptable, no editor needed |
| **PLAYTEST** | A human at the device, per PROTO or CONFORM §5; the QA line cannot be proved by a machine (feel, legibility, "visibly") |
| **SOAK** | A bot run of the invariant harness (WANDERER / CHECKER / FAIL bots, `scripts/soak_runner.gd:3`, `bot_driver.gd:3-4`) reproduced in UE per PN-FINALE §8.3 |

### 0.3 Status legend

| Status | Meaning |
|---|---|
| **EXISTS** | The proof runs today; its expected lines are in EVIDENCE |
| **PARTIAL** | Part of the line is proved by an existing fixture; the rest is DESIGNED or OPEN (the split is stated) |
| **DESIGNED** | The proof is specified here, buildable when the named unit lands; the reference code that fixes the expected values is cited |
| **OPEN** | Cannot be specified without a ruling: canon is silent, canon contradicts code, or the reference implementation does not build the thing the line tests |

### 0.4 Rules this file obeys

- The reference code fixes every number (PLAN §1 THE PORT KIT: "constants are canon"; TIMINGS carries the 32 with homes). Where a QA line names a number the code does not, the difference is quoted, not resolved.
- A telemetry line is quoted in the exact form the C++ emits today (UE `LogLine` sites) or the reference emits (`director.log_line`, `_plog`, `_log`); PN-FINALE §8.4's unified-log rule applies (every Godot `user://*_log.txt` write becomes an append to `Saved/decision_log.txt`; liveness lines gain the `LIVENESS ` prefix).
- New fixtures follow the standing shape: spawn, tick, log, parse (`ue/pyscripts/test_invariants.py` is the template; PROGRESS 0.9a–0.9d). A new automation test reuses a LAW9 name when one exists.
- LAW 3's forbidden name appears in no row (LAWS line 4: "Its name appears in no code file"); QA-25 is proved through the save keys and the `glimpse` id, as GATE §2 row 3 does.
- Nothing here edits PROGRESS.md; where a proof needs a tracker box, the row names the unit it belongs to and §3 lists the proposal for the Mac lane to splice.

---

## 1 · THE SIXTY-ONE, ITEM BY ITEM

Each row: the QA line verbatim · REF truth (script:line) · UE home today · PROOF · STATUS · OPEN.

### A · BOOT AND TITLE

#### QA-01
> QA-01 First launch, no settings file: the booth opens over the title with the BEFORE THE SHOW banner; closing writes settings; relaunch does not re-prompt.

- **REF:** `scripts/title.gd:49-51` (`OptionsPanel.new()`, `first_run = true`, `add_child`); `scripts/options_panel.gd:26-27` (`if first_run: GameState.save_settings()` — the write happens on open), `:35` (`tr("BEFORE THE SHOW · set your hands and eyes. O reopens this anytime.")`, GAMETEXT row 515).
- **UE home:** none — no title map, no `URestorationSettings` (LAW9 §1.1); scheduled unit 4.ACCESS [PROGRESS PHASE 4; GATE §5 "LAW 9 placement: Later, with the Phase 4 UI"].
- **PROOF:** TEST `Restoration.Access.Booth.FirstRun` exactly as LAW9 §2.4 specifies: delete the `"settings"` slot; boot the title in simulate; assert `bFirstRun == true`, the booth widget live with the BEFORE THE SHOW row visible, and the `"settings"` slot existing BEFORE close (the reference writes on open, `options_panel.gd:26-27`); relaunch the title; assert no booth. Plus CAPTURE of the title with the booth open, archived as the LAW 9 baseline.
- **STATUS:** DESIGNED (LAW9 §2.4; unit 4.ACCESS).
- **OPEN:** none.

#### QA-02
> QA-02 Tab through the title: every button shows the phosphor focus ring; Enter activates.

- **REF:** `scripts/title.gd:47` (`add_theme_stylebox_override("focus", sb)` on every menu child), `:52` (`new_btn.grab_focus()`); `scripts/options_panel.gd:137-143` (`_focusize`, the same ring on every booth control).
- **UE home:** none (unit 4.ACCESS / 5.2).
- **PROOF:** PLAYTEST per LAW9 §2.4 "Visual (device pass, CONFORM §5): keyboard-only traversal of the booth, focus ring photographed" — extended to the title's four buttons: Tab four times, photograph each focused state (CAPTURE ×4), press Enter on each and assert the bound action fires (NEW GAME → the world map loads; CONTINUE → the slot loads; OPTIONS → booth; CREDITS → credits map). Machine half: TEST `Restoration.Access.Title.FocusRing` asserting every `UButton` in the title widget carries the phosphor focus style (colour per the art bible's phosphor — value OPEN-1).
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-1 — the ring's colour value in UE is not in canon as a number (the reference uses a StyleBox built in code; the art bible names "phosphor green = information" [PLAN §1 Lighting law] without a hex).

#### QA-03
> QA-03 CREDITS from title: crawl runs, any key after grace skips, tower-light card holds, returns to title.

- **REF:** `scripts/credits.gd:5` (`SPEED := 42.0`, TIMINGS row `credits.gd,SPEED,42.0`), `:49-55` (crawl; `_hold_and_exit` when off the top), `:58-60` (any key or mouse button after `_t > 1.5` s → title), `:63-73` (card "the tower light stays on", 3.0 s hold, then title), `:76-79`.
- **UE home:** none (unit 4.FINALE or 5.2; the credits map is also QA-47's home).
- **PROOF:** TEST `Restoration.Credits.Crawl`: open the credits map in simulate; assert the crawl widget's Y decreases at 42 px/s (±1 frame); inject a key at 1.0 s → assert still in credits; inject at 1.6 s → assert the title map loads. Second run without input: assert the "the tower light stays on" card appears when the crawl clears the top, holds 3.0 s, then the title loads. CAPTURE one frame of the crawl and one of the tower-light card.
- **STATUS:** DESIGNED.
- **OPEN:** none (all four numbers are in the reference: 42.0, 1.5, 3.0, and "any key").

#### QA-04
> QA-04 With unshown achievements pending: title shows FILED WHILE YOU WERE OUT exactly once.

- **REF:** `scripts/title.gd:29-40` (`Achievements.flush_silent()`; if non-empty, a label `"FILED WHILE YOU WERE OUT:\n" + ...` — GAMETEXT row 643); `scripts/achievements.gd:99` (`flush_silent` marks shown, so a second call returns empty).
- **UE home:** none — `URestorationAchievements` is LAW9 §8.2 (unit 4.ACCESS or the proposed 0.8c).
- **PROOF:** TEST `Restoration.Access.Deferral.TitleOnce` verbatim from LAW9 §8.4: "unlock A05 with no morning; `FlushSilent()` returns `[STILLNESS, HELD WHOLE]`; a second `FlushSilent()` returns empty." Plus the title half: boot the title with one pending entry → assert the FILED stack widget is visible with one line; reboot → assert absent.
- **STATUS:** DESIGNED (LAW9 §8.4).
- **OPEN:** none.

### B · CORE LOOP

#### QA-05
> QA-05 Sign S1: paper decrements by one, save writes, pen-tick caption appears when captions on.

- **REF:** `scripts/game_state.gd:163-175` (`sign_log`: `paper[station] = paper_for(station) - 1`), `:178-190` (`_sign_finish`: `save_log()`, `Sfx.tick()`, `log_signed`, `noise_event(respawn_point(), 4.0)`). The pen-tick CAPTION is not in `_sign_finish` (it calls `Sfx.tick()` only); LAW9 §3.4 lists "QA-05 (pen tick on S1 sign)" as a visual check and counts caption call sites in `Source/`.
- **UE home:** `URestorationState::SignLog / SignFinish` (`RestorationState.cpp:59`, `:79` — `SIGNED %s (paper left %d)`); PROVEN by fixture `test_loop_fns.py` at HEAD: `SIGNED S2 (paper left 2)` and `SIGNFLOW signed=1 paper 3->2 ...` [EVIDENCE lines 41–42]. No caption pipeline yet (LAW9 §3.2).
- **PROOF:** FIXTURE `test_loop_fns.py` (EXISTS) for the decrement — expected `SIGNED S1 (paper left 2)` after one S1 sign from the seeded 3 (`RestorationState.h` "Paper TMap seeded S1..S5=3"); the save write is asserted by extending the fixture to read the slot after `SignFinish` and compare `Paper["S1"] == 2` (the round-trip machinery exists: `SAVE-ROUNDTRIP v16 ok=1 match=1`, EVIDENCE line 14). The caption clause: TEST `Restoration.Access.Captions.GateOn` (LAW9 §3.4) with a pen-tick key; CAPTURE of the HUD at the sign moment with captions on.
- **STATUS:** PARTIAL — decrement + save EXISTS (fixture output at HEAD); caption DESIGNED (unit 0.8b-5 caption pipeline per LAW9 §3.5).
- **OPEN:** OPEN-2 — the pen-tick caption's key does not exist in GAMETEXT (LAW9 §3.3 counts 15 reference caption sites vs 14 CSV rows; the tick is a sound with no caption text in `game_state.gd:185`). Which text the caption carries is the owner's.

#### QA-06
> QA-06 Capture: 12 real seconds, status counts down, A CLEAN SIGNAL logs, bars play.

- **REF:** `scripts/capture_bench.gd:33` (`_t = CAPTURE_SECONDS`, TIMINGS `capture_bench.gd,CAPTURE_SECONDS,12.0`), `:64-65` (`recording_left`, status `CAPTURE · TAPE %d · 00:%05.2f`), `:54-58` (`log_capture("TAPE %d · A CLEAN SIGNAL")`), `:36` (`tv.stage.play_tape(CAPTURE_SECONDS)` — the bars are the tape stage's business, `scripts/tape_stage.gd`).
- **UE home:** `ABenchCapture` (`BenchCapture.h:19-20` CaptureSeconds 12, Tether 4; `BenchCapture.cpp:67` `CAPTURE start tape %d`, `:122` `TAPE %d · A CLEAN SIGNAL`); PROVEN: fixture `test_bench.py` → `CAPTURE start tape 1` … `TAPE 1 · A CLEAN SIGNAL` [EVIDENCE lines 28–31]. The countdown surface and the bars are UI/monitor work (unit 0.8b-5 "visible countdown"; SPIKE 2 wall for the feeds, PROGRESS 0.6b).
- **PROOF:** FIXTURE `test_bench.py` (EXISTS) proves the 12 s and the log line; the fixture's Bench A ticks 12 s of forced real time before the CLEAN SIGNAL line (`BenchCapture.cpp` drives `State->RecordingLeft`). Add to the fixture: sample `State->RecordingLeft` at t = 1, 6, 11 s and assert monotone descent ≈ 11, 6, 1 (±0.1). "Bars play": CAPTURE of the bench monitor at the last frame (the `tape_stage` bars are unported — OPEN-3).
- **STATUS:** PARTIAL — 12 s + log EXISTS; countdown sample DESIGNED (trivial extension); bars OPEN.
- **OPEN:** OPEN-3 — the tape stage (`tape_stage.gd`, the CRT shader stack) has no UE home yet (UE5-MIGRATION-MAP: "CRT shader → material function stack with the same parameter names", PLAN §1). Bars are provable only after it lands (Phase 4/5).

#### QA-07
> QA-07 Die with items: retake presentation lists losses in order; loupe is lost last of the seven.

- **REF:** `scripts/game_state.gd:482-506` (`strike`: `lost = ITEM_ORDER[items_lost]`; ITEM_ORDER = WATCH PEN PHOTOGRAPH LIGHTER COMPACT KEYS LOUPE, `RestorationState.h` comment "7, canon"); `scripts/hud.gd:273-306` (`_on_captured`: `ITEM MISSING · your %s is gone from the dresser`); `scripts/dresser.gd:3` ("the loupe goes last"), `:40-46`; PN-RETAKE §2–§3.
- **UE home:** `URestorationState::Strike` (`RestorationState.cpp:205` `RETAKE take=%d lost=%s dailies=%d items_lost=%d`), PROVEN in order at HEAD: PROGRESS 0.8b-6 "lost items WATCH/PEN/PHOTOGRAPH in order". The presentation is unit 0.8b-5 "retake presentation" (unticked).
- **PROOF:** FIXTURE `test_failbot.py` (EXISTS) — extend the assertion: grep the seven `RETAKE take=N lost=<item>` lines across two runs (a sheet resets at 4; the loupe needs a seventh strike, so the fixture runs the pinned target through 7 strikes with `bInRetake` cleared per O1 below) and assert the `lost=` sequence equals WATCH, PEN, PHOTOGRAPH, LIGHTER, COMPACT, KEYS, LOUPE and that the eighth strike carries `lost=` empty (`items_lost < ITEM_ORDER.size()` guard, `game_state.gd:489`). The presentation clause: TEST `Restoration.Retake.Card` — with the UMG card of PN-RETAKE §3 landed, assert the frame table (◼ CAPTURED 0.7 s → SCENE 4 · TAKE n 0.9 s → ◀◀ REWINDING 14×0.06 s → ITEM MISSING 1.2 s → PRESENTATION KEPT 0.9 s, `hud.gd:278-305`), then CAPTURE the ITEM MISSING frame.
- **STATUS:** PARTIAL — order EXISTS at the state level (three items proven at HEAD; seven is a fixture extension); card DESIGNED (unit 0.8b-5).
- **OPEN:** PN-RETAKE O1 (`in_retake` never clears after a run death in the reference; C++ clears it) decides whether a 7-strike fixture is even reachable in one process — cite, do not rule.

#### QA-08
> QA-08 Run death (sheet full or One Take): NEXT WEEK'S EPISODE · STARRING RITA IVORI, then straight to title, no credits.

- **REF:** `scripts/game_state.gd:492-498` (`full := strikes >= 4 or mode == Mode.ONE_TAKE` → `run_ended`); `scripts/hud.gd:309-328` (`_on_run_ended`: TAKE n → REWINDING 10×0.07 → THE REWIND DOES NOT STOP 1.4 s → `NEXT WEEK'S EPISODE` / `STARRING RITA IVORI` 2.2 s → `change_scene_to_file("res://scenes/title.tscn")`); no `_roll_credits` on that path. GAP ruling 6 per PN-RETAKE §9 ("the single card, straight to title, no credits").
- **UE home:** `Rundown.cpp:70` `RUN ENDED take=%d (full sheet, fail forward)`; PROVEN by `test_failbot.py`: `RUN ENDED take=4 (full sheet, fail forward)` [EVIDENCE line 99] and PARSER `UE-R1 full-sheet-ends-run: PASS` [line 110]. The card and the title return are 0.8b-5.
- **PROOF:** FIXTURE `test_failbot.py` + PARSER (EXISTS) for "sheet full ends the run"; One Take: add a `bTestForceOneTake` (Mode = ONE_TAKE) variant and assert `RUN ENDED take=1`. The card: TEST `Restoration.Retake.RunDeathCard` — assert the four texts in order with their holds and that the map after the card is the title map with no credits widget instantiated (assert the credits map was never loaded: a `UWorld` name check). CAPTURE of the NEXT WEEK'S EPISODE frame.
- **STATUS:** PARTIAL — state EXISTS; card DESIGNED.
- **OPEN:** PN-RETAKE O5 (the run-death save writes `strikes = 0`) is a state semantic the fixture must not "fix"; the assertion reads the value the reference writes.

### C · SCHEDULE AND HOUSE

#### QA-09
> QA-09 BREAK: Harriet freezes mid-motion; interacting yields her line; cup height strictly rises across tapes.

- **REF:** `scripts/harriet.gd:68-70` (`_cup.position.y = 0.99 + 0.05 * min(day, 6)` — rises per DAY, capped at day 6), `:83-98` (interact lines; `:95` "She does not resume until the return cue. Her cup has been rising since Tape 1."), `:120` (`HARRIET · %s` line); PN-BROADCAST §2 (harriet.gd:71 freeze on `phase_changed`).
- **UE home:** `AHarriet` (`Harriet.h`, `Harriet.cpp:27-28` prompts, `:35` `HARRIET interact (%s)`, `:66` `HARRIET-FREEZE swayA= swayB= frozenC= swaying= held=`); PROVEN: `HARRIET-FREEZE swayA=0.6090 swayB=1.7783 frozenC=1.7783 swaying=1 held=1` [EVIDENCE line 49].
- **PROOF:** FIXTURE `test_harriet.py` (EXISTS) proves the freeze holds mid-motion to four decimals. Extend for the cup: set `State->Day` to 1, 3, 6, 7 in turn, re-run `BeginPlay`, log the cup's relative Z and assert strictly increasing for 1→3→6 and equal for 6→7 (the reference caps at 6 — the QA line says "strictly rises across tapes"; tapes cap at 5 [`RestorationState.cpp` "tape = min(day, 5)", PROGRESS 0.8b-4], so within tapes 1–5 strictness holds). Interact clause: the fixture's `HARRIET interact (...)` line already fires; assert the line text is one of `LINES` (`harriet.gd:120`).
- **STATUS:** PARTIAL — freeze EXISTS; cup + line DESIGNED (one fixture extension; cup geometry is unit 2.3).
- **OPEN:** none.

#### QA-10
> QA-10 Window holds honored except during cascade; ON AIR clock and hum agree.

- **REF:** `scripts/door.gd:28-29` (prompt `HELD FOR AIR · moves on the break` when `window_bound and Broadcast.on_air and not GameState.cascade_active`), `:40-41` (interact refused with the HELD FOR AIR toast, GAMETEXT rows 108–109); `scripts/wall_clock.gd:43` (label colour by `Broadcast.on_air`); the "hum": `scripts/rundown.gd:65` `SEGMENT_FREQS` (segment tone, changes on BREAK per PN-BROADCAST §2.1 step 4); INV I04 ("holds yield only to the cascade… liveness_log 'window holds waived' lines exist only while cascade_active").
- **UE home:** `URestorationClock` 50/18 s (`RestorationClock.h:21-22`, timer-driven); doors are greybox slabs with locked-reason text only (`build_greybox.py`; PROGRESS 0.6) — no `window_bound` door actor yet (unit 4.0 enumeration / 3.x doors).
- **PROOF:** TEST `Restoration.Schedule.WindowHold`: spawn a door actor with `bWindowBound`; at t = 1 s (ON AIR) call `Interact` → assert no state change and the HELD FOR AIR notify; at t = 51 s (BREAK) → assert it opens; set `State->bCascadeActive = true` at t = 101 s (ON AIR) → assert it opens (the waiver). "Clock and hum agree": TEST `Restoration.Schedule.ToneFollowsPhase` — bind to `OnPhaseChanged` and assert the segment tone's frequency parameter changes on the same tick (the audio object is 5.1's; until then assert the parameter). CAPTURE of the wall clock in both colours.
- **STATUS:** DESIGNED (clock EXISTS; door + tone are unported).
- **OPEN:** PN-BROADCAST O11 — canon's "two room tones" (audio bible) has no reference code; the only "hum" that agrees with the clock in code is the rundown's segment tone. Which sound QA-10 means is the owner's.

#### QA-11
> QA-11 Coat pegs drift per day table; Merle is at kettle, chair, or DOORWAY per schedule and pen state, never elsewhere.

- **REF:** `scripts/coat_pegs.gd:50` (`_drift()`), `:70-76` (three lines at drift < 0.3, < 0.75, else); `scripts/merle.gd:12-14` (move toward `_where()` at SPEED 1.6, TIMINGS `merle.gd,SPEED,1.6`), `:17-24` (`_where`: screening → (0.4, 0, 1.4); pen up → DOORWAY; night or lockdown → CHAIR; else KETTLE), `:34-36` (prompt names the three); PN-SCREENING §5.1.
- **UE home:** none (Merle is unit 2.2; the pegs are unit 3.1 dressing "coat pegs drift ground zero").
- **PROOF:** TEST `Restoration.House.MerleWhere`: for each (screening_active, pen_up, is_night, lockdown_done) combination assert `Where()` returns exactly one of the four canon points (the screening point is a fourth place in code — see OPEN-4) and that after ≥ (distance / 1.6) s of ticking her position is within 0.05 m of it; then a 60 s SOAK sampling her position every 0.5 s asserting every sample lies on the straight segment between two of the four points (she walks straight lines, PN-SCREENING §8 "straight line 1.6 m/s through walls"). Pegs: INSPECT — the per-day drift value table read from `coat_pegs.gd:50-58` (OPEN-5) and the three lines asserted at 0.29, 0.74, 0.76.
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-4 — the QA line names three places; `merle.gd:18-19` has a fourth (the screening seat). OPEN-5 — the "day table" the QA line cites is `_drift()`'s formula, not a table; the numbers per day are the formula's and no canon document lists them.

### D · THE HUNTER

#### QA-12
> QA-12 Warn at 7 m fills ledger line; strike at 2.2 m; third strike triggers savoring, not instant.

- **REF:** `scripts/rundown.gd:323-330` (warn once at `_warn_r`, WARN_RADIUS 7.0; the toast "It is not hurrying anymore." when `strikes >= 3`), `:305-321` (strike at `_strike_r`; `" savor" if GameState.strikes >= 3`), `:150` (`_strike_r = 2.6 if strikes >= 3 else STRIKE_RADIUS` — the savor reach widens), `:151` (HIDER profile warn 5.0); TIMINGS `WARN_RADIUS 7.0`, `STRIKE_RADIUS 2.2`. INV I01.
- **UE home:** `ARundown` (`Rundown.h:30-31`; `Rundown.cpp:407` `WARN seg %d d=%.1f%s`, `:396` `STRIKE seg %d d=%.1f%s%s`); PROVEN: `WARN seg 0 d=6.1` → `STRIKE seg 0 d=1.8` [EVIDENCE lines 54–55], savor at ≥ 3: `WARN seg 2 d=1.8 savor` / `STRIKE seg 2 d=1.8 savor` [lines 97–98]; PARSER `I01 warn-precedes-strike: PASS`.
- **PROOF:** FIXTURE `test_invariants.py` + `test_failbot.py` + PARSER (EXISTS). "Not instant": the savor rule in code is a wider reach (2.6 m) and a different line, not a delay — the fixture proves the savor tag; the "savoring" presentation (the 0.9 s strike pose, `rundown.gd:320`; the pre-strike jaw beat, MOTION) is unit 1.11 CAPTURE (≥ 8 frames of the pose).
- **STATUS:** PARTIAL — radii + savor tag EXISTS; the savoring presentation DESIGNED (1.11).
- **OPEN:** OPEN-6 — "fills ledger line": no code writes the binder on WARN; the reference toasts. Which ledger line QA-12 means is the owner's.

#### QA-13
> QA-13 Make noise behind it: within 12 s it relocates toward the noise and the It-changed-direction line fires once per run.

- **REF:** `scripts/rundown.gd:127-134` (`_on_noise` four gates), `:167-181` (on BREAK, if `now - _heard_t < 12.0` → nearest anchor to the noise; `RELOCATE toward heard noise at %s -> segment %d`; `:178-181` `_heard_once` → "It changed direction. You were not quiet." once); `scripts/noise_tracker.gd:9-19` (footstep noise every 0.6 s at loudness 6.0 while moving at night). INV I22.
- **UE home:** `ARundown::ReportNoise` (`Rundown.h:76`; `Rundown.cpp:184`); PROVEN: `RELOCATE toward heard noise at X=-500.000 Y=-2900.000 Z=0.000 -> segment 2`, PARSER `I22 heard-noise-attribution: PASS (1 attributed)` [EVIDENCE lines 57, 64]; the 0.9c note that segment 2 proves NEAREST-ANCHOR attribution [PROGRESS 0.9c].
- **PROOF:** FIXTURE `test_invariants.py` + PARSER (EXISTS). The "within 12 s" clause: the reference's 12.0 is the HEARD-MEMORY window (`rundown.gd:167`), i.e. a noise older than 12 s at the next BREAK is forgotten — add a negative fixture variant: `ReportNoise` at t = 3.5 s, force the break branch at t = 16 s → assert `RELOCATE cycle` not `toward heard noise`. The once-per-run line: assert the notify "It changed direction. You were not quiet." fires once across two attributed relocations (`bHeardFired`-style latch; the C++ has `bHeardFired` for the harness only, `Rundown.h:109` — the player-facing latch is 0.8b-5 UI).
- **STATUS:** PARTIAL — relocation EXISTS; 12 s negative + once-line DESIGNED.
- **OPEN:** OPEN-7 — the QA line reads "within 12 s it relocates"; the code relocates at the next BREAK (up to 50 s away) if the noise is < 12 s old. Both are quoted; the code is the intent [PORT-BRIEF] unless the owner rules otherwise.

#### QA-14
> QA-14 On-camera check: standing in an active camera cone prevents the strike; patchbay revive works.

- **REF:** No camera-cone strike guard exists in the reference: grep `cone|covered|is_watched|in_view|on_camera` over `rundown.gd`, `monitor_rig.gd`, `coverage_director.gd`, `game_state.gd`, `patchbay_console.gd` → 0 hits. What exists: the tally contract (`rundown.gd:242` — while `recording`, the AF layer approaches and never strikes; LAW 10), the premiere guard (`rundown.gd:204-208`, I03/I05 per PN-FINALE §8.5), and the CHECKER kill of the most-watched rig (`rundown.gd:155-160`). Patchbay revive: `scripts/patchbay_console.gd:62-64` (`RE-PATCHED · the feed climbs back onto the board.` when `_any_killed()`).
- **UE home:** tally contract PROVEN (`test_state_af.py`: `AF loom d=1.2 (the jaw works its lever)` … `STRIKE af tally-cool` only after cutoff+cool [EVIDENCE lines 15–17]; GATE §2 row 1 "EXERCISED (mechanic) / NOT YET (cones)"). Cones: "Static camera-cone hides are Phase 3 world content" [GATE §2 row 1]; patchbay: none (unit 3.16 / 4.0).
- **PROOF:** For the mechanic that exists — FIXTURE `test_state_af.py` (EXISTS) + a SOAK per INV I23 ("recording true forbids GameState.strike from the hunter · soak bot captures with him adjacent for 10 minutes · any AF strike log line during recording is S0"): a 600 s simulate with `bTestForceRecording` held and the pawn adjacent; assert zero `STRIKE ` lines (PARSER retake section counts them). Revive: TEST `Restoration.Patchbay.Revive` — kill a rig (`SetKilled(true)`), interact the console, assert `bKilled == false` and the RE-PATCHED notify. The cone clause itself: **OPEN**.
- **STATUS:** PARTIAL — tally-contract guard EXISTS; revive DESIGNED; cone OPEN.
- **OPEN:** **OPEN-8 (LAW-level).** LAWS line 2 "ON CAMERA IS SAFE. An active camera cone prevents the strike, always." and LAWS line 12 "The safe hide is the lit one (camera cones)" describe a guard the reference does not implement; the code's on-camera safety is the tally contract (LAW 10) and the premiere yield (I03/I05). GATE §2 row 1 schedules cones as Phase 3 content. Whether "in an active camera cone" is to be built as a hunter guard (a new rule in `ARundown`) or is satisfied by the tally contract is the owner's ruling; this file does not design a guard canon's code never had.

### E · SYSTEMS AND BOOTH

#### QA-15
> QA-15 Map on M: sealed rooms dashed, station dots labeled, footer shows the BOUND map key.

- **REF:** `scripts/map_view.gd:19-43` (`_draw`: room names at `:26` (draw_string per room), station labels at `:30`, footer at `:43` `"FACILITY MAP · %s to close · amber: landmarks · dot: you" % GameState.key_name("map")` — the bound key, `game_state.gd:388`). PROTO P15 (outlines match walls; the dot never exits geometry).
- **UE home:** none (unit 5.2 UI; LAW9 §6.4 "Visual: QA-15 map footer").
- **PROOF:** TEST `Restoration.UI.MapFooter`: with `Rebind(map, N)` the footer string equals `FACILITY MAP · N to close · …` (LAW9 §6 `KeyName`); with defaults, `M`. Sealed rooms dashed + station dots: CAPTURE of the map with two rooms sealed (SEALED FOR BROADCAST via QA-26's lockdown) and all five stations from `Stations.csv` (S1..S5) visible and labelled — count 5 by eye. P15 walk: PLAYTEST (three rooms, outlines vs walls).
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-9 — "dashed" is not in `map_view.gd`'s grep surface (`dash` 0 hits); the sealed style in the reference is whatever `_draw()` does for locked doors, to be read at port time; the line style is not in canon as a rule.

#### QA-16
> QA-16 Booth: every slider and check persists across relaunch; NEW GAME leaves settings intact.

- **REF:** `scripts/options_panel.gd:44-67` (sliders and checks call `GameState.save_settings()` on change; ASSIST row `:66-67`), `scripts/game_state.gd:308-340` (`load_settings` / `save_settings`, `user://settings.cfg`, `:317` `assist`, `:332`).
- **UE home:** none (`URestorationSettings`, LAW9 §1.1; unit 4.ACCESS).
- **PROOF:** TEST `Restoration.Access.Settings.RoundTrip` and `Restoration.Access.Settings.NewGameLeavesSettings` verbatim from LAW9 §2.4 (seven properties set to non-defaults, save, fresh subsystem, load, assert equality; clamps 3.0 / 0.8; then `ResetNewGame` + `SaveToSlot` and assert settings unchanged).
- **STATUS:** DESIGNED (LAW9 §2.4).
- **OPEN:** none.

#### QA-17
> QA-17 Remap RESPOND onto E: refused with KEY IN USE; remap onto an unused key: prompts everywhere show the new key.

- **REF:** `scripts/game_state.gd:370-386` (`rebind`; `:376` `KEY IN USE · that key already answers to %s.`, GAMETEXT row 167), `:193` (`glyphs()` substitution), `:388` (`key_name`).
- **UE home:** none (LAW9 §6.2; Enhanced Input split, unit 0.8b-1b proposal / 4.ACCESS).
- **PROOF:** TESTs `Restoration.Access.Remap.Conflict` (E refused, notify once, keys unchanged), `Restoration.Access.Remap.RoundTrip`, `Restoration.Access.Remap.Glyphs` (byte-identity at defaults over the 63 token-bearing keys; F substitution on THE SIGN PULSES), `Restoration.Access.Remap.NoDefaultLeak` — all verbatim LAW9 §6.4. "Prompts everywhere": CAPTURE ×2 after respond→F: the bench prompt and the screening toast (LAW9 §6.4 "Visual").
- **STATUS:** DESIGNED (LAW9 §6.4).
- **OPEN:** none.

#### QA-18
> QA-18 ASSIST on: beat window visibly forgiving, premiere clocks half again longer, holding E passes both stillness checks.

- **REF:** `scripts/screening_event.gd` `_on_beat()` tolerances (PN-SCREENING §4; LAW9 §5.4 table: off `T,T,F,F,F,F,T,T`, on `T,T,T,T,F,F,T,T`), `:59-65` (still check); `scripts/live_production.gd:349-350` (`_timed`: `dur * (1.5 if assist_on else 1.0)` — "half again" = 1.5 ✔); `scripts/floor_manager.gd:63-72` (`held_still := assist_on and Input.is_action_pressed("interact")`).
- **UE home:** none (unit 0.8b-5 "screening + assist"; LAW9 §5).
- **PROOF:** TESTs `Restoration.Access.Assist.BeatWindow`, `.HoldStill`, `.PremiereClock` (67.5 s ± one frame vs 45.0), `.NeverGates` — verbatim LAW9 §5.4. "Visibly forgiving": PLAYTEST (LAW9 §5.4 "Visual: QA-18") plus a CAPTURE sequence of the sign's pulse with assist on and off (≥ 8 frames each).
- **STATUS:** DESIGNED (LAW9 §5.4).
- **OPEN:** none.

### F · NIGHTS AND EVENTS

#### QA-19
> QA-19 Night 1 trip fires once ever; Floor Manager watch fails on movement, passes on assist-hold.

- **REF:** `scripts/night_trip.gd:12` (guards: `night_tripped`, `is_night`, `premiere_live`), `:16-17` (at `_armed_t >= 20.0` → `night_tripped = true`, saved key 37 `NightTripped`), `:22-29` (breaker / feed / hummed bar toasts); `scripts/floor_manager.gd:49` (visible only night ∧ on_air ∧ ¬premiere), `:77-81` (inside 9.0 m → `_watch_t = 3.0`), `:63-72` (movement spoils; assist-hold passes). PROTO P8, P9.
- **UE home:** none (Floor Manager is unit 2.6 variant + Phase 4; the trip is 4.0 enumeration).
- **PROOF:** TEST `Restoration.Night.TripOnce`: fresh save, `SetNight(true)`, tick 25 s → assert the three notifies once and `bNightTripped == true`; save, reload, `SetNight(true)`, tick 60 s → assert zero. TEST `Restoration.Access.Assist.HoldStill` (LAW9 §5.4, verbatim) for both watch outcomes ("You moved on camera…" / "The hand lowers. The take holds."). CAPTURE of the raised arm (P8's horizontal arm, `floor_manager.gd:59-61`).
- **STATUS:** DESIGNED.
- **OPEN:** none.

#### QA-20
> QA-20 Night 4+: circuit C then B; restoring out of order refuses with B before C; waived window holds during.

- **REF:** `scripts/cascade.gd:20-40` (C lets go `:24`, B follows `:32`, F holds `:40`); `scripts/patchbay_console.gd:39-60` (stage 1: restore B — `:53-55` `CIRCUIT B RESTORED … B before C, the way the panel is labeled.`; stage 2: C — `:57-60`), `:43` (`Q · GET VESS`); `scripts/door.gd:28-29, 40` (`not cascade_active` = the waiver); `scripts/liveness_check.gd:21-24` (`OK · console valid · window holds waived · stage %d` / `VIOLATION · console invalid`). INV I04, I07. PN-FINALE §2, §3.
- **UE home:** none (unit 4.0 / 4.FINALE); PARSER already carries I07 (`liveness()`), reporting `N/A (cascade did not run)` [EVIDENCE line 65].
- **PROOF:** FIXTURE `test_cascade.py` (new, PN-FINALE §8.3 shape): force day ≥ 4 night, trigger the cascade, tick through the stage-1 window; interact the console → assert stage 2 and the B RESTORED notify; interact again → stage 0 and C RESTORED; the "out of order" clause: the reference has no C-first path to refuse (stage 1 IS B; the panel's labels make the order) — assert the stage-1 prompt/notify text carries "B before C". Doors: assert a window-bound door opens ON AIR while `bCascadeActive`. Then PARSER: `I07 cascade-liveness: PASS (n checks)` from `LIVENESS … OK … window holds waived` lines every 5 s (PN-FINALE §3.1), and a negative variant with the console destroyed → `FAIL (violation logged)`.
- **STATUS:** DESIGNED (parser half EXISTS).
- **OPEN:** OPEN-10 — "restoring out of order refuses": the reference offers no out-of-order action (one interact per stage); the refusal QA-20 describes is the label, not a rejected input. Quoted; the code is the intent.

### G · STORY GATES

#### QA-21
> QA-21 Day 2+, S4 with zero paper: the presigned page appears and saves free, once.

- **REF:** `scripts/log_station.gd:19-31` (`station_id == "S4" and day >= 2 and not presigned_seen` → three toasts, `mark_presigned()`); `scripts/game_state.gd:445-455` (`mark_presigned`: `presigned_seen = true`, a signature appended with `"presigned": true`, no paper spent). INV I10; PROTO P6. Note: the gate in code is `day >= 2` and first S4 interaction — NOT "zero paper" (the QA line's precondition is stricter than the code's).
- **UE home:** `URestorationSaveGame::PresignedSeen` (key 25), `FRestorationSignature::bPresigned` exist (`RestorationState.h`); no S4 behaviour yet (0.8b-4 ported `RegisterStation`; the presigned branch is unit 4.0).
- **PROOF:** TEST `Restoration.Story.Presigned`: Day 2, paper S4 = 0, interact S4 → assert `Signatures.Last().bPresigned == true`, `Paper["S4"] == 0` unchanged, `bPresignedSeen == true`, three notifies; interact again → assert `SIGN REFUSED S4 (no paper)` (`RestorationState.cpp:59`) and no second presigned entry. INSPECT: save diff shows the signature added and paper unchanged (INV I10's telemetry).
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-11 — precondition drift: QA says "with zero paper"; code fires on the first S4 interaction from Day 2 regardless of paper. Quoted; code is the intent.

#### QA-22
> QA-22 Crate before seance: seance refuses; after: wear ladder degrades generations per answer.

- **REF:** `scripts/impossible_crate.gd:8` (visible `day >= 2 and not crate_opened`), `:15-18`; `scripts/seance_dock.gd:22` (`visible = GameState.crate_opened` — before the crate the dock does not exist to refuse), `:71-75` (`_step`: `add_wear(1.5)` per frame step; answers at ANSWER frames), `:87-91` (`set_temp_generation(min(2.0, seance_wear / 30.0))` — the ladder is per WEAR, i.e. per frame stepped, not per answer), `:83-84` ("The frame tears a little more each pass." above 70). INV I19, I20; PROTO P16.
- **UE home:** `SeanceWear` (key 23), `CrateOpened` (36), `LelandAnswers` (24) exist; no dock (unit 3.9 bench-room hero + 4.0).
- **PROOF:** TEST `Restoration.Story.SeanceGate`: Day 2, `bCrateOpened = false` → assert the seance dock actor is hidden / non-interactable; open the crate → visible. Then step frames 0→40: assert `SeanceWear` = 1.5 × steps and the generation parameter = min(2.0, wear/30) at each step (equality to 1e-4). I20 determinism: CAPTURE frame 14 twice across two launches and byte-diff (INV I20 "seed = f(idx)").
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-12 — "per answer" (QA) vs per frame-step (code, `_step` adds wear on every step, answers only at 5 frames). Quoted.

#### QA-23
> QA-23 Fire tape: forced watch, no sting anywhere in it; watching marks the flag.

- **REF:** `scripts/fire_tape_dock.gd:26-59` (`_run`: the sequence of toasts `:48-54`, `fire_tape_watched = true` `:55-56`, `af_active = true` + the wake line `:57-59`); no `Sfx` call in the file (grep: `Sfx.` → 0 in `fire_tape_dock.gd`; the only `Sfx.bell()` in the game is `hud.gd:452`). INV I15 ("The fire tape carries no sting"); LAWS line 3 (ONE STARTLE).
- **UE home:** `bFireTapeWatched` (22), `bAfActive` (44) exist; the dock is unit 3.9 / 4.0.
- **PROOF:** TEST `Restoration.Story.FireTape`: interact the dock → assert input is locked for the sequence's duration (forced), `bFireTapeWatched == true` and `bAfActive == true` at the end, and a bound audio-event counter reports zero one-shots during the sequence (INV I15 becomes "an asset-review gate" — INSPECT: the fire-tape sequence's MetaSound graph contains no transient one-shot; a static list check against the audio bible's stinger policy). CAPTURE of the tape's last card.
- **STATUS:** DESIGNED.
- **OPEN:** none.

#### QA-24
> QA-24 Dock: filing all six completes with nothing following; the warm one never acts, on camera or off.

- **REF:** `scripts/dock_task.gd:22-40` (`notify_counted` → "Inventory complete: six units, one anomaly, zero incidents."; `interact` → "Filed. Six units."), `scripts/dock_chum.gd:21-23` (the warm unit's line; nothing else). INV I12 ("no code path exists; keep it that way: this invariant is a review rule on future commits"); LAWS line 5 (THE WARM ONE NEVER ACTS). PROTO P7.
- **UE home:** `bDockDone` (26) exists; the dock is unit 3.20 SCENE DOCK; GATE §2 row 4 "NOT YET".
- **PROOF:** INSPECT (the review rule, machine-checked): grep `Source/` for any Tick, timer, delegate binding or animation on the dock-unit class → assert none beyond the interact prompt (a static test `Restoration.Dock.WarmOneIsInert` asserting the warm unit's class overrides nothing but `GetPrompt`/`Interact`). TEST `Restoration.Dock.FileSix`: interact six units, assert `bDockDone`, then tick 600 s with the tally on and off and assert zero notifies, zero spawns, zero log lines from the dock (INV I12 "full-run tail watch" as a SOAK tail).
- **STATUS:** DESIGNED.
- **OPEN:** none.

#### QA-25
> QA-25 Day 4 unseal: the once-ever moment can occur exactly once per save, and never again after.

- **REF:** `scripts/glimpse.gd:18-19` (guards `glimpse_seen`, `_firing`, `is_night`, `premiere_live`), `:64` (`glimpse_seen = true`, saved key 53 `GlimpseSeen`); `FireUnsealed` key 55. INV I11 ("harness asserts single spawn per save lifetime"), I30; LAWS line 4 (ONCE, EVER — "never referenced again by any system … Its name appears in no code file"). PROTO P10.
- **UE home:** keys 53/55 exist; the corridor's Day-4 content is unit 3.13 + 4.0; GATE §2 row 3.
- **PROOF:** TEST `Restoration.Story.OnceEver`: Day 4 night at the fire-corridor elbow → assert exactly one spawn and `bGlimpseSeen == true`; save, reload, revisit twice across two launches → zero spawns (I11's telemetry). INSPECT `Restoration.Access.Deferral.MetaSilence` (LAW9 §8.4): the moment's name absent from every file under `Source/` and `Data/`; no achievement, presence string or log line names it (INV I30; PRESENCE "Never: … the once-ever moment"). The log itself must not name it — assert the fixture's decision log contains only the `glimpse` id.
- **STATUS:** DESIGNED.
- **OPEN:** none. (This row deliberately uses the save key's name only.)

### H · FINALE

#### QA-26
> QA-26 Lockdown: monitors sync, doors read SEALED FOR BROADCAST, rec chairs tween to rows and persist.

- **REF:** `scripts/lockdown.gd:26-43` (`_fire` toasts; `_apply`: `rig.sync_to(tex)` `:41`, `d.locked_reason = "SEALED FOR BROADCAST · lock-in's just till air"` `:43`, GAMETEXT row 482); `scripts/rec_chairs.gd:4` ("They do not convert back."), `:45-55`. INV I18 (permanent; re-applied on ready); PROTO P11. PN-FINALE §1.
- **UE home:** `bLockdownDone` (29) exists; SPIKE 2 wall proves twelve feeds can be driven (PROGRESS 0.6b) — `sync_to` is a texture swap on those; unit 4.FINALE.
- **PROOF:** TEST `Restoration.Finale.Lockdown`: with four assets banked, `SetNight(true)` → assert every `AMonitorRig` samples the same feed texture, every exterior door's locked reason equals the SEALED text, and each rec chair's transform reaches its row target (tween complete within the reference's duration — OPEN-13); save, reload → assert all three re-applied without the toasts (`_apply(silent=true)`, `lockdown.gd:37`). CAPTURE of the rec room in rows and a door prompt reading SEALED FOR BROADCAST.
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-13 — the chair tween's duration is in `rec_chairs.gd` (read at port), not in any canon document.

#### QA-27
> QA-27 Premiere: cue marks require the PGM camera; each incident type fail-forwards within its guarantee.

- **REF:** `scripts/live_production.gd:316-346` (`_on_mark_press(label, need_cam)`: fires only when `_pgm == need_cam` `:328`; wrong camera `:345-346`; TALLY refuses at most twice `:329-331`; BOOM holds once `:339-341`), `:391-408` (`_pressure`: interval `max(14, 26 − 4·fail_takes)` `:393`; incident older than 40 s → `_resolve(_incident, "club auto-fix")` `:399-400`; `INCIDENT %s (fail_takes %d, interval %.0f)` `:405`), `:381-384` (`RESOLVED %s (%s) t=%.1f`). INV I06 (RESOLVED "club auto-fix" at or under 40 s; tally refusals never exceed 2; boom holds exactly 1). PN-FINALE §4.4–§4.5, §8.
- **UE home:** none (unit 4.FINALE); PARSER `premiere()` EXISTS with the verbatim I06 rules (`tools/invariant_parser.py:50-76`; `N/A (premiere not yet ported)` today).
- **PROOF:** FIXTURE `test_premiere_failbot.py` (new; PN-FINALE §8.3): the director with `bTestForceFinale`, a pawn that never interacts, ≥ 120 s, then `python3 tools/invariant_parser.py <log> --bot fail` → `I06 fail-forward-finale: PASS (n incidents, m auto-fixed)`; assert additionally that no `RESOLVED` line has `t=` > 41.0 (parser rule), tally refusals ≤ 2 and exactly one boom hold per incident (grep the notifies). PGM clause: TEST `Restoration.Finale.MarkNeedsPgm` — `_pgm = 2`, press at a mark needing 1 → assert "Wrong camera is program…" and no cue advance; `_pgm = 1` → advance.
- **STATUS:** DESIGNED (parser EXISTS).
- **OPEN:** PN-FINALE O7 — as built, the auto-fix fires at > 40 s measured from `_incident_started`, and the parser fails a fix logged at > 41.0 s: a long run can straddle the line. Expected result on the code as-is is quoted in PN-FINALE §8.3; the owner rules whether 40/41 is a defect.

#### QA-28
> QA-28 Divert at the final break with the fire tape: DEAD AIR path plays; otherwise the committed decision's ending plays; ending exits roll credits.

- **REF:** `scripts/live_production.gd:116-137` (final break; divert gate `:124` = key QUIET ROOM ∧ 5 answers ∧ fire tape watched; `:129` `_fader_choice`), `:222-234` (the crossing: 75 s, 62 if Vess dead, −13 if self-hold); `scripts/hud.gd:381-395` (`_on_finale(decision)`), `:503-515` (4a/4b DEAD AIR credits, GAMETEXT rows 364/372), `:347-358` (`_roll_credits` → credits map). INV I19 (divert gates). PN-FINALE §4.9, §6.1 routing table.
- **UE home:** `Decision` (28), `EndingReached` (31), `FinaleDone` (30) exist; unit 4.FINALE.
- **PROOF:** TEST `Restoration.Finale.Divert`: set the three gate facts, reach the final break → assert the Q prompt; take Q → assert `_last_crossing` runs with t = 75.0 (62.0 with VESS dead; −13.0 with `fader_self`) and, on reaching the dead room, `EndingReached == "DEAD AIR"` and the credits map loads. Negative: any gate fact false → no Q prompt, and the `Decision` string's ending plays (routing table PN-FINALE §6.1; one TEST per row of that table). Every ending exit: assert the credits map is the next world (loop over the table).
- **STATUS:** DESIGNED.
- **OPEN:** PN-FINALE §9 rows (canon prose the code does not implement — e.g. the dead-room re-patch precondition, the PT ≥ 70 audition clause) are NOT tested here; the code's gate is the test's gate.

### I · META AND MODES

#### QA-29
> QA-29 No achievement toast ever appears between title and morning; morning shows FILED lines.

- **REF:** `scripts/achievements.gd:4-5` ("at exactly two gates: the morning toast and the title screen"), `:36-42` (`night_changed` off → `flush_to_toasts`), `:45-50` (`unlock` queues only), `:88-96` (`FILED · <title>` ≤ 2, else `FILED · %d entries, %s among them.`). INV I30. ACH §ENGINE DELTA.
- **UE home:** none (`URestorationAchievements`, LAW9 §8.2).
- **PROOF:** TEST `Restoration.Access.Deferral.NeverSurfacesDuringPlay` verbatim LAW9 §8.4 (counter on `OnNotify` stays 0 through recording / screening / premiere unlocks; exactly ONE toast `FILED · 3 entries, CAREFUL HANDS among them.` at the morning; none on a second morning), `.TwoOrFewer`, `.OnlyTwoExits` (static: one `Toast(` site, inside `FlushToToasts`).
- **STATUS:** DESIGNED (LAW9 §8.4).
- **OPEN:** none.

#### QA-30
> QA-30 DEMO true: only the seven rooms open, doors carry demo reasons, bed declines, S1 and S5 only, card protects three seconds, completed demo save contains none of the whitelisted-out fields, funnel file has six marks.

- **REF:** `scripts/game_state.gd:6` (`const DEMO := false`), `:719` (`paper = {"S1": 3, "S5": 3} if DEMO`), `:514-522` (`save_log` strips the DEMO whitelist-out fields: `finale_done, ending_reached, lie_pending, seance_wear, … presigned_seen, cascade_done, casualties`), `:344-357` (`demo_mark` → `user://demo_funnel.txt`); `scripts/world_builder.gd:60` (`DEMO_OPEN` = the seven rooms = `Data/DemoOpen.csv` rows), `:262-266` (demo door reasons: "SEALED · you can hear it from here…" / "SEALED · the club opens the rest when the contract is signed."); `scripts/bed_prop.gd:13-14` (declines); `scripts/hud.gd:361-380` (`_on_demo_end`: `demo_mark("card")`, `_wait(3.0)` before "(any key)" — three seconds ✔). The marks: grep `demo_mark("` over `scripts/` finds SEVEN distinct names — `started` (`game_state.gd:714`), `s1_signed` (`:187`), `capture_start` (`capture_bench.gd:32`), `lunge` (`bench_tv.gd:63`), `capture_done` (`capture_bench.gd:61`), `screening` (`screening_event.gd:70`), `card` (`hud.gd:368`) — against the QA line's six (OPEN-14). DEMO §DP1–DP3.
- **UE home:** `DemoOpen.csv` (7 rooms) EXISTS in data (PROGRESS 0.5); no DEMO flag in C++ (unit 5.8).
- **PROOF:** INSPECT `Restoration.Demo.RoomsFromData`: with DEMO true, every `Doors.csv` row whose rooms are not both in `DemoOpen.csv` carries one of the two demo reasons (a CSV × CSV assertion, `extract_data.py` style: 7 open rooms, 20 doors, count the sealed set and assert the reasons). TEST `Restoration.Demo.Save`: play S1 sign → capture → screening → card; then assert the slot's serialized object lacks every whitelisted-out field (LAW9-style static list from `game_state.gd:518-522`), `Paper` has keys S1 and S5 only, the bed's `Interact` produces the decline notify, the card accepts no input for 3.0 s, and the funnel file holds the marks the owner rules (OPEN-14: six per QA, seven in code). LAW9 §8.4 `.DemoSilent` covers achievements.
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-14 — the reference writes seven named marks (`started`, `s1_signed`, `capture_start`, `lunge`, `capture_done`, `screening`, `card`); the QA line says six. Whether `started` (written at new-game, `game_state.gd:714`) or `lunge` (`bench_tv.gd:63`) is outside the six, or the count is seven, is the owner's.

#### QA-31
> QA-31 Load a v15 save into this build: migration toast, nothing lost; settings file untouched.

- **REF:** `scripts/game_state.gd:672-676` (`v < SAVE_VERSION` → `save_log()` then `_announce_migration`), `:772-773` (`LOG MIGRATED · format v%d to v%d. Nothing was lost.`, GAMETEXT row 187); settings live in a separate `settings.cfg` (`:308-340`). PN-STATE §1 load coercions.
- **UE home:** `URestorationSaveGame::Version = 16` and `LoadFromSlot` (PROGRESS 0.8b-3 round-trip `match=1`); AUDIT §2.6 "Load version handling" lists what the C++ does on an older version (cite at port).
- **PROOF:** TEST `Restoration.State.MigrateV15`: write a v15-shaped save (every key of PN-STATE §1 minus the v16 additions, `Version = 15`) into the slot; `LoadFromSlot` → assert the notify `LOG MIGRATED · format v15 to v16. Nothing was lost.` exactly once, every carried field equal to the v15 values, every v16-only field at its PN-STATE default, and the re-saved slot reads `Version == 16`; assert the settings slot's bytes are identical before and after.
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-15 — which keys v15 lacked is not in this repo's history (the reference ships v16 only); the fixture's v15 shape must come from PN-STATE §1's "load coercions" column, which lists defaults, not versions.

#### QA-32
> QA-32 Pause anywhere unlocked: world and clocks hold, audio mutes; pause during any authored sequence: refused.

- **REF:** `scripts/hud.gd:34` (`pause_requested`), `:87-140` (`_toggle_pause`: `if player and player.locked: return` `:97` — the refusal; `get_tree().paused = true` `:99`; `PROCESS_MODE_ALWAYS` menu), `:189-191` (Escape while paused resumes); `player.locked` is set by every authored sequence (`hud.gd:276, 312, 364, 384`). LAW9 §7.
- **UE home:** none (LAW9 §7.5 proposes the core in 0.8b-5; GATE §5 rules LAW 9 into Phase 4).
- **PROOF:** TESTs `Restoration.Access.Pause.ClockHolds` (the 50 s flip lands 50.0 s of unpaused time later; `ARundown` position unchanged), `.RefusedWhenLocked` (both clauses), `.AudioSilent` (master submix 0 while paused), `.MenuKeyboard` — verbatim LAW9 §7.4.
- **STATUS:** DESIGNED (LAW9 §7.4).
- **OPEN:** LAW9 §10 item 2 (pause during the live premiere: refuse or hold) is the owner's; the test asserts whichever ruling lands.

### J · THE AFTER-FIRE (added post-c036)

#### QA-33
> QA-33 Watch the fire tape: the wake toast fires once; af_active persists across save and load.

- **REF:** `scripts/fire_tape_dock.gd:57-59` (`if not af_active: af_active = true; toast("Something answers the tape from three rooms away…")` — once by the guard); `af_active` saved key 44 (`game_state.gd:573`). QA-54's "the wake bleed occurs exactly once per save" is the same guard.
- **UE home:** `bAfActive` (44) round-trips today (`SAVE-ROUNDTRIP v16 … taught=1`, EVIDENCE line 14 proves the sibling key; the key set is "all 55 keys", PROGRESS 0.8b-3). The dock is unit 3.9 / 4.0.
- **PROOF:** FIXTURE `test_state_af.py` (EXISTS) proves `bAfActive` survives save → clobber → load (extend the `SAVE-ROUNDTRIP` line to print `af=%d`). Wake-once: TEST `Restoration.Story.FireTape` (QA-23) run twice on one save → the wake notify counted once.
- **STATUS:** PARTIAL — persistence EXISTS (round-trip machinery; one printed field to add); once DESIGNED.
- **OPEN:** none.

#### QA-34
> QA-34 Start a capture with him awake: he approaches at walking-dread pace, footsteps thunk on interval, and the HUD reads REC · SAFE WHILE LIT with a live countdown; at 1.2 m he stops and the first-sighting toast fires exactly once per save.

- **REF:** `scripts/rundown.gd:242-268` (`AF_APPROACH_SPEED` 0.8 `:259`; `_af_step_t > 1.1` → `Sfx.thunk` `:261-264`; at `pd <= AF_LOOM_DIST` 1.2 → `_af_seen_once` latch, caption `[THE JAW WORKS ITS LEVER]`, the sighting toast, `_work_jaw()` `:265-269`); `scripts/hud.gd:172-175` (`● REC · SAFE WHILE LIT · %04.1f`). TIMINGS `AF_APPROACH_SPEED 0.8`, `AF_LOOM_DIST 1.2`. LAWS line 11 (THE TALLY CONTRACT). MOTION "0.8 m/s approach, 1.2m loom".
- **UE home:** `ARundown` AF layer (`Rundown.h:24-25`; `Rundown.cpp:307` `AF loom d=%.1f (the jaw works its lever)`); PROVEN: `AF loom d=1.2 (the jaw works its lever)` [EVIDENCE line 15]. HUD countdown = unit 0.8b-5 "visible countdown" (GATE §2 row 10 "NOT YET (visible)"). Footsteps = unit 5.1 (S17 footfall). Note `_af_seen_once` in C++ is `bAfSeenOnce` (`Rundown.h:106`) — a per-process latch, not saved (the reference's is also unsaved: `rundown.gd:35`).
- **PROOF:** FIXTURE `test_state_af.py` (EXISTS): loom at 1.2 proven. Extend: sample the actor's position at t and t+2 s during the approach and assert speed = 0.80 m/s ± 0.02; count `AF loom` lines across two contracts in one run → exactly one (the latch). HUD: TEST `Restoration.HUD.TallyCountdown` — with `bRecording` true and `bAfActive` true, the widget text matches `● REC · SAFE WHILE LIT · %04.1f` and decrements with `RecordingLeft`; CAPTURE ×2 (gameplay distance and 1 m, PLAN §R.5). Footsteps: TEST `Restoration.Audio.AfStepInterval` — S17 footfall events at 1.1 s intervals ± one frame while approaching (5.1).
- **STATUS:** PARTIAL — loom EXISTS; speed/latch fixture extension, HUD and footfall DESIGNED.
- **OPEN:** OPEN-16 — "exactly once per save" (QA) vs once per process (`_af_seen_once` is not a saved key in either engine). Quoted.

#### QA-35
> QA-35 The eye: red glow ONLY while a capture runs; dark the instant it stops or aborts.

- **REF:** `scripts/rundown.gd:82-100` (the tally eye light, energy 0 at build), `:240-241` (`_eye.light_energy = 1.6 if (af_active and recording) else 0.0`, every physics frame), `:204-208` (premiere: eye 0). LAWS line 11 ("The eye's light and the contract are the same fact"). PLAN §1 Lighting law ("His eye is the game's only mobile red").
- **UE home:** the puppet's lens is a mesh slot (PROGRESS 0.3 "tally not yet emissive in UE"); the emissive/light binding to `State->bRecording` is unit 1.12 "Tally states … wired to AI".
- **PROOF:** TEST `Restoration.Chum.EyeFollowsRecording`: with the tally light component bound, toggle `bRecording` true → intensity > 0 on the same tick; false (via the bench's cutoff `TEST recording off`, `Rundown.cpp:268`, and via the tether abort `CAPTURE ABORTED`, `BenchCapture.cpp:106`) → intensity == 0 on the same tick (zero-frame latency: assert in the tick after the write). CAPTURE sequence ≥ 8 frames across a cutoff. INSPECT: no other red light exists in any level (`build_greybox.py` lamps are amber (0.95, 0.72, 0.45); assert no light asset with hue in the red band outside the tally component — the "only mobile red" law).
- **STATUS:** DESIGNED (unit 1.12).
- **OPEN:** none.

#### QA-36
> QA-36 Let the tally die with him adjacent: THE TALLY COOLS, then a strike; let it die with distance: he withdraws to his segment. First cool ever runs 4.0 s with the teaching line; every later cool runs 2.0.

- **REF:** `scripts/rundown.gd:272-279` (`af_taught` → `AF_COOL_SECONDS` 2.0 + "The tally cools."; else `af_taught = true`, `_af_cool = 4.0`, "THE TALLY COOLS. Two doorways stand between you and anywhere. Use them." GAMETEXT row 578), `:280-289` (at expiry: strike if within `_strike_r + 0.4`, else hide and return to `_anchor(_idx)`). INV I26 (ONE COOL TEACHES — "grep the teaching line count"). TIMINGS `AF_COOL_SECONDS 2.0`; `af_taught` key 45.
- **UE home:** `Rundown.cpp:320` `AF tally cools (taught)`, `:324` `AF tally cools`, `:335` `STRIKE af tally-cool`; PROVEN: `AF tally cools (taught)` → `STRIKE af tally-cool` [EVIDENCE lines 16–17] (the adjacent branch, first cool). The withdrawal is a teleport today (GATE §4 1c: "the post-cool withdrawal is not simulated (he hides and teleports; canon shows a reversed walk)").
- **PROOF:** FIXTURE `test_state_af.py` (EXISTS) for the adjacent branch. Extend with three runs in one script: (1) fresh state, adjacent → assert `AF tally cools (taught)`, the STRIKE line at 4.0 s ± one tick after cutoff; (2) `bAfTaught` true, adjacent → `AF tally cools` then STRIKE at 2.0 s; (3) `bAfTaught` true, pawn moved to 6 m before cutoff → `AF tally cools`, NO STRIKE line, and the actor at `SegmentAnchors[SegIdx]` after expiry (the withdrawal's end state; the walk is unit 1.10's CAPTURE, ≥ 8 frames reversed along the approach path). I26: grep count of `(taught)` == 1 across the three runs.
- **STATUS:** PARTIAL — first cool + strike EXISTS; 2.0 s and distance branch DESIGNED (fixture extension); the withdrawal MOTION is 1.10.
- **OPEN:** none (the 4.0 s teaching value is `rundown.gd:278`, not in TIMINGS — it is a literal; the test cites the line).

#### QA-37
> QA-37 Doorways: every threshold costs him 2.2 s, captioned, in the capture approach AND the night hunt; a route through two doors buys 4.4 s, verifiably.

- **REF:** `scripts/rundown.gd:333-347` (`_door_fold_check`: within `AF_DOOR_NEAR` 1.0 of a door and that door's per-door cooldown > 6.0 s → `_fold_t = AF_FOLD_SECONDS` 2.2, caption `[IT FOLDS THROUGH THE DOORWAY]`, toast within 12 m); called from the AF approach (`:250, :258`) and from the BREAK hunt path (`:296-298`). TIMINGS `AF_FOLD_SECONDS 2.2`, `AF_DOOR_NEAR 1.0`. LAWS line 12 ("every threshold costs him 2.2 s, and that toll is the player's counterplay"). INV I24 (THE FOLD IS PAID — "position-delta audit across door radii in the coverage log").
- **UE home:** `ARundown::DoorFoldCheck` (`Rundown.cpp:195`; `DoorPositions` from `Doors.csv`, `Rundown.h:42`); PROGRESS 0.7 "2.2s door fold toll from Data/Doors.csv"; GATE §2 row 11 "EXERCISED (dead room, toll)". No dedicated fold fixture exists; no fold line is logged today (the C++ `LogLine` list has no FOLD entry).
- **PROOF:** FIXTURE `test_fold.py` (new): add a `FOLD door=%d t=%.1f` telemetry line at the toll's start (mirrors nothing in Godot — an evidence line, named so it never collides with the parser's tokens, per the 0.8b-6 RETAKE lesson); place the pawn two doors from his anchor (TAPE LIBRARY → CORRIDOR → REC ROOM via `Doors.csv` gaps (0, −11) and (0, −4)); run the approach under `bTestForceAF + bTestForceRecording`; assert two FOLD lines, each followed by ≥ 2.2 s of zero position delta (I24's position-delta audit), total arrival time ≥ straight-line time + 4.4 s; run the same route under `bTestForceNight` on a BREAK and assert the same. Captions: `Restoration.Access.Captions.LeverAndFold` (LAW9 §3.4, verbatim). CAPTURE sequence of one fold (unit 1.10, ≥ 8 frames).
- **STATUS:** DESIGNED (the toll code EXISTS; the fixture and the caption are new).
- **OPEN:** OPEN-17 — the per-door 6.0 s re-fold cooldown (`rundown.gd:339`) means a route that crosses the SAME door twice inside 6 s buys 2.2 s, not 4.4; the QA line's "two doors" is read as two distinct doors. Quoted.

#### QA-38
> QA-38 The dead room: noise made inside registers nowhere; he tracks to the felt door, holds, says his line once; first entry gives the radio toast and [NO ECHO].

- **REF:** `scripts/game_state.gd:121` (`in_dead_room`: |x−19| ≤ 2.2 ∧ |z−2.5| ≤ 2.7); `scripts/rundown.gd:128-129` (`_on_noise` returns if the noise is in the dead room), `:248-256` (approach `DEADROOM_DOOR` at 0.8 m/s, hold within 0.6 m, `_deadroom_line` once: "It stops at the felt door…"); `scripts/hud.gd:168-171` (`deadroom_seen` once → the radio toast + caption `[NO ECHO]`, GAMETEXT row 224; key 51 `DeadroomSeen`). INV I25 (DEAF TO THE DEAD ROOM). LAWS line 12 (THE TWO HIDES).
- **UE home:** `URestorationState::InDeadRoom` (`RestorationState.h`, the same rect in uu), `ReportNoise` gate 1 (`Rundown.h:74-76`), `Rundown.cpp:293` `AF holds at the felt door`; PROVEN: the felt-door hold in `test_state_af.py` (GATE §2 row 11 "EXERCISED (dead room, toll)"; PROGRESS 0.8b-6 "dead room deaf" gate ported). The HUD half is 0.8b-5.
- **PROOF:** FIXTURE `test_state_af.py` (EXISTS) for the hold. Extend: `ReportNoise` from inside the rect at loudness 6.0 then force the break branch → assert `RELOCATE cycle`, never `toward heard noise` (I25); count `AF holds at the felt door` == 1 across two entries in one run (the `bDeadroomLine` latch, `Rundown.h:107`). HUD: TEST `Restoration.HUD.DeadRoomFirstEntry` — pawn enters the rect → one notify (the radio line) + one caption `[NO ECHO]`; `bDeadroomSeen` true; re-enter → nothing; save/load → still nothing.
- **STATUS:** PARTIAL — hold EXISTS; deafness assertion + once-line + HUD DESIGNED.
- **OPEN:** none.

### K · THE CASUALTY LEDGER (added post-c043)

#### QA-39
> QA-39 Binder page one: NO ENTRIES. KEEP IT SO. until a death; then who, cause, day, epitaph per entry.

- **REF:** `scripts/hud.gd:241-258` (`_fill_binder`: `CASUALTY LEDGER · NO ENTRIES. KEEP IT SO.` when `casualties.is_empty()` `:248`); `scripts/game_state.gd:113-118` (`mark_casualty(who, cause, epitaph)` appends `{who, cause, line, day}`; `:114` idempotent by `is_dead`; `:118` "THE LEDGER TAKES IT DOWN."). INV I27, I28. LAWS line 8 (EVERY DEATH HAS A SIGNATURE — "the binder names it").
- **UE home:** `FRestorationCasualty{Who, Cause, Line, Day}` and `Casualties` (key 46) exist (`RestorationState.h`); `mark_casualty` and the binder are 0.8b-5 (deferred, UI-heavy) / 4.0. GATE §2 row 7 "NOT YET (schema ready)".
- **PROOF:** TEST `Restoration.Ledger.BinderPageOne`: fresh state → binder page text contains `NO ENTRIES. KEEP IT SO.`; `MarkCasualty("VESS", "V2 · THE UNCREDITED FIX", "…")` on Day 3 → the page lists who, cause, day 3, epitaph; call it again → still one entry and one "THE LEDGER TAKES IT DOWN." notify (I27). INSPECT: every `MarkCasualty` call site in `Source/` carries a non-empty cause and epitaph (LAW 7's signature: a static grep asserting no empty string literal in those arguments).
- **STATUS:** DESIGNED.
- **OPEN:** none.

#### QA-40
> QA-40 M1: refusing Merle at the fire tape saves her and never re-offers; consent plays the repossession, the kettle caption, and she is absent everywhere after; THE BURN and NEW PRODUCER play their variants.

- **REF:** `scripts/fire_tape_dock.gd:29-31` (offer only if `not fire_tape_watched and not is_dead("MERLE") and not merle_offered`; `merle_offered = true` — never re-offers, key 47), `:42-44` (consent / refuse lines), `:63-69` (consent: the repossession lines, the kettle line "The kettle, two rooms away, clicks off by itself.", `mark_casualty("MERLE", "M1 · THE SECOND VIEWING", …)`); `scripts/merle.gd` (PN-SCREENING §5.3: dead Merle is invisible, still moves, prompt inert — "absent everywhere" as built = invisible, OPEN); `scripts/hud.gd:395-408` (`_end_burn` cobbler variant when Merle is dead), PN-FINALE §6.3 (variant lines by casualty, verbatim in `hud.gd`).
- **UE home:** `bMerleOffered` (47), `Casualties` exist; Merle is unit 2.2; the dock is 3.9 / 4.0; endings 4.FINALE.
- **PROOF:** TEST `Restoration.Ledger.M1`: (refuse) interact the dock, answer refuse → `bMerleOffered == true`, `IsDead("MERLE") == false`; interact again → no offer. (consent) → `IsDead("MERLE")`, the kettle notify text present, and Merle's actor hidden thereafter (assert `bHidden` in every room across a 120 s SOAK sample). Variants: TEST `Restoration.Finale.VariantLines` — with MERLE dead run ending 3 (THE BURN) and ending 2 (NEW PRODUCER) and assert the `_say` sequences equal the casualty variants transcribed in PN-FINALE §6.3 (string-compare, I28's method).
- **STATUS:** DESIGNED.
- **OPEN:** PN-SCREENING §8 "Dead Merle: invisible, still moves, still prompts, interact inert — as code or fix; OPEN". The test asserts hidden, not removed, until ruled. "The kettle caption" — the reference toasts the kettle line; no `show_caption` call exists at `fire_tape_dock.gd:67` (OPEN-18: caption vs toast).

#### QA-41
> QA-41 H1: the slip arms only Day 2+ while frozen; taking it grants exactly one paperless signature that toasts in her hand; the next break plays the absence and the cabinet; the seventh signal is unlearnable if her card was unfound; screenings judge 0.05 tighter.

- **REF:** `scripts/harriet.gd:83-98` (`interact` on a BREAK (frozen): `day >= 2 and not harriet_slip and not _h1_pending` → `_slip_armed`; E again `:89-92` → `harriet_slip = true`), `scripts/game_state.gd:163-170` (`sign_log` with zero paper and `harriet_slip` → the one free signature, "Signed. The hand on the slip is not yours…"), `scripts/harriet.gd:112-116` (next break: "Harriet's chair is warm. Harriet is not in it, or anywhere." + the film cabinet line; `mark_casualty("HARRIET", "H1 · CONTINUITY", …)`); `scripts/film_cabinet.gd:33-40` ("Six signals. The film rattles out. It never mentions a seventh."); the 0.05: LAW9 §5.4 (Harriet dead: on-beat tolerance 0.15 vs 0.20 off-assist; 0.30 vs 0.35 on-assist — the 0.05 ✔), PN-SCREENING §3.
- **UE home:** `bHarrietSlip` (live, `RestorationState.h`), `SignLog`'s "harriet-slip branch" PORTED (PROGRESS 0.8b-4); the H1 sequence "deferred (UI-heavy)" (PROGRESS 0.8b-5 Harriet sub-box); screening 0.8b-5.
- **PROOF:** FIXTURE `test_loop_fns.py` (EXISTS) — extend: set `bHarrietSlip = true`, `Paper["S2"] = 0`, `SignLog("S2")` → assert `SIGNED S2 (paper left 0)` and `bHarrietSlip == false`; a second `SignLog` → `SIGN REFUSED S2 (no paper)` (exactly one). TEST `Restoration.Ledger.H1`: Day 1 BREAK interact → no arm; Day 2 ON AIR → no arm; Day 2 BREAK → armed; E again → `bHarrietSlip`; next BREAK → the absence line, the cabinet line, `IsDead("HARRIET")`. Seventh signal: with `SignalsKnown.Num() == 6` and Harriet dead, interact the cabinet → the "never mentions a seventh" line and `SignalsKnown` unchanged. Tolerances: `Restoration.Access.Assist.BeatWindow` (LAW9 §5.4, the Harriet-dead rows).
- **STATUS:** PARTIAL — the paperless-signature branch EXISTS (0.8b-4; one fixture extension to print); the rest DESIGNED.
- **OPEN:** "toasts in her hand" — the reference toasts at the sign, not at Harriet (`game_state.gd:168`); "her card was unfound" — the film cabinet's seventh-signal gate reads `is_dead("HARRIET")`, not a card flag (OPEN-19: which flag "her card" is).

#### QA-42
> QA-42 V1: AUTHENTICATE while credited plays the all-monitors taking after the INK ripple; alternatively the credited living die at the final breaker AFTER the farewell, lights held. V2: GET VESS appears only for the uncredited who used the insight; taking it fixes both circuits then plays circuit F. Dead, the breaker is the pin plus the hard blackout, and the crossing runs 62.

- **REF:** V1: `scripts/decision_ledger.gd:57-61` ("INK · the record now includes one name you added." → "Across the building, every monitor cuts to the patch bay. VESS…" → "holds one frame too long. Then bars. His plastic pin is fused…"), `scripts/live_production.gd:87-95` (credited at the final breaker: "The margin. You wrote my name…" → "The handle drops. The lights hold." → bars, the pin); V2: `scripts/patchbay_console.gd:43` (`Q · GET VESS` in the stage-1 prompt), `:82-93` (`_v2_taken`: both circuits in eleven seconds, then circuit F, `mark_casualty("VESS", "V2 · THE UNCREDITED FIX", …)`); dead: `live_production.gd:100` ("A plastic pin, fused in the enamel…"), `:104-113` (the BLACKOUT retake, 30 s), `:232` (`62.0 if is_dead("VESS") else 75.0`). PN-FINALE §4.8, §6.4. "the uncredited who used the insight": `bVessInsight` (33) ∧ ¬`bVessCredited` (34).
- **UE home:** keys 33/34/46 exist; the ledger prop, console and premiere are units 3.9 / 3.16 / 4.FINALE.
- **PROOF:** TEST `Restoration.Ledger.V1`: `bVessCredited = true`, interact AUTHENTICATE → the three notifies in order and `IsDead("VESS")`; alternative: credited and alive at the final breaker → the farewell notify precedes the `IsDead` write and the light state is unchanged across it (assert a lighting parameter before/after). TEST `Restoration.Ledger.V2`: `bVessInsight = true`, `bVessCredited = false`, cascade stage 1 → the prompt contains `GET VESS`; every other combination → absent; take it → stage 0 within the sequence, then the circuit-F lines, `IsDead("VESS")`. Dead: final breaker → the pin line and the BLACKOUT retake clock (30 s, assist ×1.5); `_last_crossing` t == 62.0.
- **STATUS:** DESIGNED.
- **OPEN:** PN-FINALE §9 ("the credited branch has no clock at all" vs the walkthrough's "hesitation is the window") — the test asserts the code.

#### QA-43
> QA-43 F2: exactly the third blind tally call; the unlisted-camera beats; cue flow continues after. F1: the fader choice precedes the crossing; self-hold costs 13 s and routes 4b; his hold routes 4a with the casualty marked inside the epilogue; if he is already dead, self-hold is forced.

- **REF:** F2: `scripts/live_production.gd:329-338` (TALLY incident: refusals < 2 → refused; else `_blind_calls += 1`; `>= 3 and not is_dead("FLOOR MANAGER")` → `_f2_unlisted()` `:182-187`, then "You call it blind. Correctly."), cue flow continues (`_on_mark_press` returns normally). F1: `:193-218` (`_fader_choice` before `_last_crossing` `:129-131`; `is_dead("FLOOR MANAGER")` → `fader_self = true` forced `:194-198`; E → self-hold `:208-210`), `:232-234` (−13.0 if `fader_self`); `scripts/hud.gd:503-515` (`fader_self` → 4b HER HAND; else `mark_ending("DEAD AIR")` 4a HIS HAND, with the casualty marked inside `_end_dead_air`). PN-FINALE §4.9, §5, §6.4.
- **UE home:** none (4.FINALE).
- **PROOF:** TEST `Restoration.Ledger.F2`: TALLY incident live, `_pgm == need_cam`, press respond ×2 → two refusals, no F2; press ×3 more → F2 fires on the third BLIND call (blind_calls == 3), the two unlisted-camera notifies, `IsDead("FLOOR MANAGER")`, and the next cue mark still advances. TEST `Restoration.Ledger.F1`: divert with the Floor Manager alive → the fader prompt precedes `_last_crossing`; choose E → `fader_self`, crossing t = 75 − 13 = 62, ending 4b; choose SPACE → 4a with `IsDead("FLOOR MANAGER")` set inside the epilogue sequence (assert the write happens after the credits `_say` begins, per `hud.gd:503-515`); with him already dead → no prompt, `fader_self` forced true.
- **STATUS:** DESIGNED.
- **OPEN:** PN-FINALE O10 (controls map "E held 4.6 s" vs code's 4.6 s wait after one press) — the test asserts the code.

#### QA-44
> QA-44 L1: offered only past five answers AND wear above 70; the ink-drain beats; the dock inert forever; 1A unreachable; 1B shows the pencil card. L2: offered whenever the fire tape is held; consumes it, empties answers, sets the completed sign-off; the final break then plays 4c with no divert prompt.

- **REF:** L1: `scripts/seance_dock.gd:28-33` (prompt extra only when `leland_answers.size() >= 5 and seance_wear > 70.0`), `:60` (respond gate), `:94-103` (`_l1_sixth`: the ink-drain beats `:97-99`, "He is retroactively unfound. The reel is blank leader…" `:102`, `mark_casualty("LELAND", "L1 · THE SIXTH QUESTION", …)`), `:41` ("The dock is a box with a window now. Nothing reads." — inert); `scripts/hud.gd:460` (1A requires ≥ 5 answers ∧ wear ≤ 70 ∧ ¬dead LELAND), `:471-475` (1B cards: SAINTS / STAFF / the pencil READER card). L2: `seance_dock.gd:32` (`Q feed the fire tape into the wake` when `has_fire_tape`), `:111-125` (`_l2_reading`: answers emptied `:123`, `signoff_completed = true` `:124`, `mark_casualty("LELAND", "L2 · THE READING", …)`); `scripts/live_production.gd:118-123` (`signoff_completed` → "the rundown simply ends" → `signoff_4c`, before the divert gate at `:124`). PN-FINALE §6.1.
- **UE home:** keys 23/24/48 exist; the dock and finale are 3.9 / 4.FINALE.
- **PROOF:** TEST `Restoration.Ledger.L1`: (4 answers, wear 80) → no offer; (5, 70.0) → no offer (strict >); (5, 70.1) → offer; take it → the three ink-drain notifies, `IsDead("LELAND")`, every later interact returns the inert line, `hud` routing: 1A branch false, ending 1B's `_say` list contains the pencil card text. TEST `Restoration.Ledger.L2`: `bHasFireTape` → the Q prompt regardless of answers; take → `bHasFireTape == false` (OPEN-20), `LelandAnswers.Num() == 0`, `bSignoffCompleted`; at the final break → ending `signoff_4c` and no divert prompt even with the divert gate facts true.
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-20 — "consumes it": whether `_l2_reading` clears `has_fire_tape` is not in the lines read here (`seance_dock.gd:111-125` shows answers cleared and the sign-off set; the tape flag's write is to be read at port). Quoted as the QA line states; the test asserts the code's write.

#### QA-45
> QA-45 ENDING 0: with all four ledgered before lockdown, the premiere intercepts at entry; credits show nine cards, one name; A28 files at the next flush gate.

- **REF:** `scripts/game_state.gd:102-103` (`all_cast_dead`: MERLE ∧ VESS ∧ HARRIET ∧ FLOOR MANAGER), `scripts/live_production.gd:45-47` (`run()` → `_one_woman()` at entry), `:156-165` (the one-woman toasts; returns `"one_woman"`); `scripts/hud.gd:443-445` (`_end_zero`); `scripts/credits.gd:32-34` (cards[4] = the cast list every part RITA IVORI; cards[5] = "and CHUM / as RITA IVORI"), `:35-36` (ENDING REACHED card inserted at 6); `scripts/achievements.gd:27` (`"A ONE-WOMAN SHOW": "A28"`), `:53-56` (`on_ending` → unlock queued; toasts at the next flush gate). ACH line 45 (A28, "its icon is the only card in the set with a name on it").
- **UE home:** none (4.FINALE, credits map, achievements subsystem).
- **PROOF:** TEST `Restoration.Finale.EndingZero`: four casualties marked, lockdown not yet fired → `SetNight(true)` for the premiere → assert the director's `Run()` returns `one_woman` before the first cue; `EndingReached == "A ONE-WOMAN SHOW"`; credits widget card count == 9 (OPEN-21) and every cast line's name is RITA IVORI; `Unlocked` contains A28 with zero notifies until the next morning, then one `FILED · A ONE-WOMAN SHOW` (LAW9 §8.4 pattern). CAPTURE of the cast card.
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-21 — "nine cards": `credits.gd:21-36` builds a card list whose length depends on the ending (insertion at 6); the exact count for ending 0 is to be read from the list at port (this file did not count the base list).

#### QA-46
> QA-46 Rows: every timed incident that expires takes a seat, cycling its three lines with the caption; the count persists.

- **REF:** `scripts/live_production.gd:349-360` (`_timed(dur, label)`: on expiry `_row_taken()`), `:168-177` (`ROW_LINES` (three), `row_casualties += 1`, `toast(ROW_LINES[(row_casualties − 1) % 3])`); `row_casualties` saved key 49 (`game_state.gd:578`). PN-FINALE §4.6. Note: the reference toasts the row line; a `show_caption` at that site is not in the grep (OPEN-22).
- **UE home:** `RowCasualties` (49) exists; premiere 4.FINALE.
- **PROOF:** FIXTURE `test_premiere_failbot.py` (QA-27's): the never-interacting pawn lets CUE 2 (45 s) expire repeatedly → assert `RowCasualties` increments once per expiry, the notify text cycles ROW_LINES[0], [1], [2], [0]; save, reload → the count persists (round-trip machinery EXISTS).
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-22 — "with the caption": no caption call at `live_production.gd:175-177`; toast only. Quoted.

#### QA-47
> QA-47 Every ending's credits open with THE LEDGER, READ ALOUD when anything is in it, including fifty-eight minus N; a clean run reads nothing and A27 files.

- **REF:** `scripts/hud.gd:347-358` (`_roll_credits`: if casualties or rows > 0 → "THE LEDGER, READ ALOUD, because that is what ledgers are for:" → one `_say` per casualty (who · cause / line; HARRIET adds "TRANSITION UNRESOLVED.") → "THE 58 CLUB: fifty-eight, minus %d." when rows > 0; else nothing); `scripts/achievements.gd:53-56` (`on_ending`: empty ledger ∧ zero rows → A27). INV I28 (string-compare at credits), I29 (S0 if any reading text on a clean run). ACH line 45 (A27).
- **UE home:** none (4.FINALE; achievements subsystem).
- **PROOF:** TEST `Restoration.Finale.LedgerReadAloud`: for every row of PN-FINALE §6.1's routing table, run the ending with (a) one casualty + 2 rows → assert the `_say` sequence equals the binder page's entries verbatim (I28 string-compare) and ends with "fifty-eight, minus 2."; (b) clean → assert the first `_say` after "ENDING · …" is NOT the ledger header and `Unlocked` gains A27 (I29: any reading text on a clean run fails the test — S0). CAPTURE of one ledger card.
- **STATUS:** DESIGNED.
- **OPEN:** none.

#### QA-48
> QA-48 Demo build: no death is reachable, no casualty field survives in the save, achievements stay dark.

- **REF:** `scripts/game_state.gd:518-522` (`casualties` in the DEMO strip list), `scripts/world_builder.gd:262-266, 390, 572, 976, 1010, 1114` (DEMO guards — the spawns that carry deaths are skipped: DEMO E2 "skip spawning Rundown, FM, dock, crate, seance, cascade"), `scripts/achievements.gd:46` (`GameState.DEMO` → `unlock` returns). DEMO §DP2 ("hand-inspect a completed demo save for absent fields").
- **UE home:** none (unit 5.8).
- **PROOF:** INSPECT `Restoration.Demo.NoDeathPath` (static): with DEMO true, every actor class that calls `MarkCasualty` or `Strike` is absent from the spawned set (assert by enumerating the level's actors after the data stamp — the reference's skip list is the expected absent set). TEST `Restoration.Demo.Save` (QA-30) asserts no `Casualties` field in the slot; `Restoration.Access.Deferral.DemoSilent` (LAW9 §8.4) asserts `Unlocked` stays empty.
- **STATUS:** DESIGNED.
- **OPEN:** none.

#### QA-49
> QA-49 H2: after the rejected viewing, the block offers the splice with the label disclosed; performing it mints a daily immediately and the NEXT break doubles her; she persists on set as scenery with one line forever; the double rebuilds after save and load.

- **REF:** `scripts/rejected_edit.gd:11-12` (visible after the crate; offered while Harriet alive and not pending), `:21-27` (second interact → `_splice()` unless dead/pending), `:32-40` (`_splice`: "DAILY MINTED · no capture, no bench, no twelve seconds." `:37` — `mint_shortcut_daily` (`game_state.gd:95`), `h2_pending = true` `:40`); `scripts/harriet.gd:100-107` (next BREAK with `h2_pending`: the two doubling lines, `_splice_visual()`, `mark_casualty("HARRIET", "H2 · THE SPLICE", …)`), `:17-29` (`_doubled` rebuilt on `_process` when dead — "the double rebuilds after save and load"), `:86` ("Two of her. Neither resumes…" — the one line forever). `h2_pending` key 50. PN-RETAKE §5 (shortcut daily, take −1: `FRestorationDaily::Take = -1`).
- **UE home:** `bH2Pending` (50), `FRestorationDaily.Take = -1` exist; Harriet's visual double is unit 2.3; the block is 3.9 / 4.0.
- **PROOF:** TEST `Restoration.Ledger.H2`: after the rejected viewing, interact → the splice prompt text contains the disclosed label (OPEN-23 for the exact label); perform → `Dailies.Last().Take == -1` on the same tick and `bH2Pending`; next BREAK → the two lines, `IsDead("HARRIET")`, the double component present; every later interact returns the one line; save, reload → the double component present at `BeginPlay` without a BREAK.
- **STATUS:** DESIGNED.
- **OPEN:** OPEN-23 — "with the label disclosed": the prompt text at `rejected_edit.gd:15-19` is to be read at port; not quoted here.

#### QA-50
> QA-50 Seance grief: with Harriet dead, frame 14 reads PAUSED PROPERLY; with Merle dead, frame 28 reads SHE'S HERE NOW; every reading that names Harriet also carries TRANSITION UNRESOLVED.

- **REF:** `scripts/seance_dock.gd:78-81` (frame 14 ∧ dead HARRIET → "SHE WAS THE ONLY ONE WHO PAUSED PROPERLY."; frame 28 ∧ dead MERLE → "I KNOW. SHE'S HERE NOW."), `:82` (`LEGAL PAD · ` + a); `scripts/hud.gd:352-354` (HARRIET entry at credits → "HER CARD, HER OWN STAMP REGISTER: / TRANSITION UNRESOLVED."). Note "every reading that names Harriet" in code = the credits ledger reading, not the seance frame.
- **UE home:** none (3.9 dock; 4.FINALE credits).
- **PROOF:** TEST `Restoration.Ledger.SeanceGrief`: HARRIET dead, step to frame 14 → the notify equals `LEGAL PAD · SHE WAS THE ONLY ONE WHO PAUSED PROPERLY.`; MERLE dead, frame 28 → `LEGAL PAD · I KNOW. SHE'S HERE NOW.`; neither dead → the base ANSWERS text for both frames. Credits: `Restoration.Finale.LedgerReadAloud` (QA-47) with HARRIET in the ledger → the TRANSITION UNRESOLVED card follows her entry (assert adjacency).
- **STATUS:** DESIGNED.
- **OPEN:** none.

#### QA-51
> QA-51 Braid audit: at every premiere pressure peak, at least two simultaneous attention demands share the clock; single-threaded peaks are filed as tuning defects.

- **REF:** No code defines a "pressure peak". What the premiere braids as built: a timed cue clock (`_timed`, `live_production.gd:349-360`) running concurrently with the incident roller (`_pressure`, `:391-408`, one incident at a time, interval `max(14, 26 − 4·fail_takes)`), the PGM switcher (`:36-42`), and the mark press (`:316-346`). PN-FINALE §4.5–§4.6. PLAN §5 PHASE 4 "QA-51 BRAID AUDIT — at every pressure peak, at least two simultaneous attention demands (braid, never queue)"; PROGRESS box 4.QA51. Comparative study adoption A2.
- **UE home:** none (4.FINALE, then 4.QA51).
- **PROOF (mechanical part):** FIXTURE `test_premiere_failbot.py` (QA-27's) post-processed by a new script `tools/braid_audit.py`: reconstruct from the log the intervals during which a cue clock is running (`_timed` start/expiry — add `CUE <label> start` / `expired` evidence lines) and during which an incident is live (`INCIDENT` → `RESOLVED`); define a "peak" as any instant with a cue clock under 10 s remaining (OPEN-24); assert every peak overlaps a live incident or a second clock. Report single-threaded peaks as a list (the "tuning defects" file).
- **STATUS:** OPEN — the audit is executable only once "pressure peak" has a definition; the fixture above is offered as the mechanism, the definition is the owner's.
- **OPEN:** OPEN-24 — what counts as a pressure peak and what counts as an attention demand (is the PGM switcher one?) are not defined in any canon document; PLAN §5 gives the rule, not the measure.

### ADDENDA (rows 52–61)

#### QA-52
> QA-52 The fold is one authored montage timed at 2.2 s per door width; head arrives last; no procedural blending.

- **REF:** MOTION ("THE FOLD (2.2s doorway montage — shoulder first, head late on an impossible hinge)"); PLAN §1 Motion & sound law ("fold as authored montage per door width"); `docs/production/CHUM-RIG-AND-ANIMATION-SPEC.md` (the fold montage rows); TIMINGS `AF_FOLD_SECONDS 2.2`; `Doors.csv` widths (per door).
- **UE home:** unit 1.10 (unticked).
- **PROOF:** CAPTURE sequence per PLAN §4 "Animation units: capture sequences (≥8 frames or MRQ clip), review motion": one fold per distinct door width in `Doors.csv`, frames at 0.0/0.55/1.1/1.65/2.2 s, judged by eye: shoulder leads, head last, hard stop at 2.2 s. INSPECT: the montage asset's length equals 2.2 s × (width / reference width) for each width variant (assert on the `UAnimMontage` play length), the AnimBP has no blend node on the fold slot (blend-in/out time 0.0 — "no procedural blending"), and the brain's toll (`DoorFoldCheck`) and the montage length agree to a frame.
- **STATUS:** DESIGNED (1.10).
- **OPEN:** "per door width" — whether the 2.2 s scales with width or is fixed at 2.2 s for every width (the toll in code is a constant, `rundown.gd:341`; MOTION says "per door width") is OPEN-25.

#### QA-53
> QA-53 After-Fire zero-secondary sweep: no jiggle, cloth, or idle sway on the AF body in any state; the eye is the only articulation during stillness; the performance quote (frontal square plus fifteen-degree tilt) occurs only while the tally burns.

- **REF:** MOTION ("AFTER-FIRE Chum = the unoperated body: puppet grammar DELETED … NO SECONDARY MOTION EVER … PARKED (statue-still, zero idle sway, no breathing) while the eye alone tracks"; "THE PERFORMANCE QUOTE (at 1.2m under a burning tally …)"; "Rig note: AF rig ships with physics secondaries DISABLED, wool baked stiff"). `scripts/rundown.gd:415-424` (the reference's ON AIR idle shoulder sway — `_shoulder_l.rotation.x = -0.28 + 0.2·sin(...)` — a PRE-canon-rev behaviour the port must NOT carry for the AF body: PN-BROADCAST §2.2 "The ON AIR idle at rundown.gd:415 — a known canon conflict").
- **UE home:** units 1.9 (the POUR, parked idle), 1.11 (the quote), 1.12 (eye layer).
- **PROOF:** INSPECT `Restoration.Chum.ZeroSecondary` (static): the AF skeletal mesh has no cloth asset, no physics asset bodies simulating, no AnimDynamics/RigidBody nodes in the AnimBP; the parked state's animation is a single pose (bone transforms constant across the clip). TEST `Restoration.Chum.ParkedStillness`: parked for 30 s → every bone transform except the eye bone identical at t=0 and t=30 (≤ 1e-4). TEST `Restoration.Chum.QuoteOnlyUnderTally`: the quote montage plays only while `bRecording` (assert the montage never starts with `bRecording` false across a 300 s SOAK). CAPTURE sequence of the quote (≥ 8 frames): frontal square, one 15° tilt (measure the head bone yaw delta = 15° ± 1°).
- **STATUS:** DESIGNED (1.9 / 1.11 / 1.12).
- **OPEN:** none (PN-BROADCAST §2.2 already files the idle-sway conflict; the AF body's rule is unambiguous in MOTION).

#### QA-54
> QA-54 The audio law holds: every pre-fire source band-limited, every AF source full-range with the throat speaker's band-limited room tone as the one standing inversion; the jaw opens only via the two-beat self-operated act (tally-state lever work, and the single pre-strike telegraph with its 0.9 s beat); it never syncs to sound; the bell never sounds; no vocalization exists; the wake bleed occurs exactly once per save.

- **REF:** PLAN §1 Motion & sound law and AUDIO LAW (verbatim there: "band-limited is memory, full-range is present"; "THE JAW OPENS ONLY BY HIS OWN HAND … Exactly two grammar entries"; "The bell NEVER sounds (clapperless)"; "NO vocalizations"); MOTION; `scripts/rundown.gd:320` (`_strike_pose_t = 0.9`); `scripts/sfx.gd:16` (`bell()`), its single call site `scripts/hud.gd:452` (the finale beat: "The bell rings once, three feet behind camera position."); LAWS line 6 (SILENCE CONTRACTS: "The bell rings once, at the finale beat, and its caption says so. Chum's bell is otherwise silent"); GATE §4 1c (no 0.9 s telegraph before a strike exists in C++ yet); fire-tape wake once: QA-33.
- **UE home:** units 1.11 (jaw acts), 1.12 (throat room tone; "bell never sounds; no vocalizations; jaw never syncs to sound"), 5.1 (audio bed; "the wake's band-step-down cut").
- **PROOF:** INSPECT `Restoration.Audio.BandLimits` (static over the MetaSound/submix graph): every pre-fire source routes through the band-limited submix (≈50 Hz–8 kHz per PLAN §1); every AF source through the full-range submix except the throat room tone (band-limited) — assert the routing table, one row per source from C15's SOUND MANIFEST (its deliverable; until it lands the row list is the audio bible's). TEST `Restoration.Chum.JawOnlyByHand`: across a 300 s SOAK with captures, the jaw bone opens only inside the lever montage (tally state) or the 0.9 s pre-strike telegraph montage; a strike with no telegraph montage fails; no jaw curve is driven by any audio envelope (static: no audio-driven parameter feeds the jaw). Bell: INSPECT — exactly one call site of the bell one-shot in `Source/`, inside the finale beat with its caption (LAWS line 6); zero bell events in any AF fixture log. Vocalization: INSPECT — no voice-class asset referenced by the AF actor. Wake once: QA-33.
- **STATUS:** DESIGNED (1.11 / 1.12 / 5.1; the static halves are cheap and can run before the audio lands).
- **OPEN:** **OPEN-26 (LAW-level wording).** QA-54 and PLAN §1 say "the bell never sounds"; LAWS line 6 says it rings ONCE at the finale beat and the reference rings it once (`hud.gd:452`). Read together: Chum's bell never sounds as a puppet sound; the one finale ring is the house's beat. The test above asserts that reading (one site, finale only). The owner confirms.

#### QA-55
> QA-55 Prompt discipline: nothing ambient prompts; everything that prompts is stable across the run.

- **REF:** TAX (AMBIENT LORE NEVER PROMPTS; INTERACTABLES carry verbs, never drift, never lie); PLAN §1 Object taxonomy law; PROGRESS PHASE 3 preamble ("Taxonomy QA each room: QA-55 prompt discipline"); `docs/production/ROOM-BRIEFS-3.1-3.5.md` §0.3 and `-3.6-3.10.md` §0.1 (I/L/D caps per room); `ue/Restoration/Source/Restoration/RestorationInteractable.h:1-2` ("if it prompts, it is a promise").
- **UE home:** every prompting actor implements `IRestorationInteractable` (0.8b-2); rooms are Phase 3.
- **PROOF:** INSPECT `Restoration.Taxonomy.PromptCensus` (per room, run at each 3.x close): enumerate actors in the room's bounds (`Rooms.csv`) implementing the interface; assert none is tagged `Ambient` / listed in LORE for that room (the room brief's ambient list is the negative set), and the count ≤ the brief's I cap. Stability: run the census at Day 1, Day 3 night, post-lockdown → the set of prompting actors is identical except for the brief's declared state-gated interactables (e.g. W2 after W1).
- **STATUS:** DESIGNED (one static test, run per room; Phase 3).
- **OPEN:** ROOM-BRIEFS OPEN 0-G (what the L cap counts) affects the census' denominator, not the QA-55 assertion.

#### QA-56
> QA-56 Drift audit: every drift instance resolves to the dressing tier; interactables and lore never move.

- **REF:** TAX (DRESSING is the only drift-eligible tier); PROGRESS PHASE 3 preamble ("QA-56 drift=dressing-only"); the reference's drift instances: `scripts/coat_pegs.gd:3` ("the club's palette drifts"), the room briefs' "drift hooks" rows.
- **UE home:** Phase 3.
- **PROOF:** INSPECT `Restoration.Taxonomy.DriftAudit`: every actor with a drift component/schedule is tagged DRESSING; a SOAK of one full day cycle samples the transform of every `IRestorationInteractable` and every LORE-tagged actor at each phase flip → zero transform deltas (≤ 1e-3 uu) except the declared exceptions (rec chairs at lockdown, QA-26 — an authored state change, not drift; Merle, an NPC).
- **STATUS:** DESIGNED (Phase 3).
- **OPEN:** none.

#### QA-57
> QA-57 Hero census: no room carries more than one hero interactable.

- **REF:** TAX ("one hero interactable per room max"); PROGRESS PHASE 3 preamble; ROOM-BRIEFS-3.6-3.10 finding 3.9-C ("the bench room prompts seven objects against a cap of 3").
- **UE home:** Phase 3.
- **PROOF:** INSPECT `Restoration.Taxonomy.HeroCensus`: actors tagged `Hero` per room ≤ 1, asserted against `Rooms.csv` bounds; the tag is authored by the room unit from its brief's IDENTITY row.
- **STATUS:** DESIGNED.
- **OPEN:** ROOM-BRIEFS 3.9-C — the bench room's seven prompting objects (each a route to an ending) vs the cap; which is the hero is the owner's, and QA-57 cannot pass in 3.9 until ruled.

#### QA-58
> QA-58 Crouch honesty: toggling crouch changes camera height and speed only; hunter coverage, relocation, and noise attribution are byte-identical between a walking and a crouch-walking soak; no prompt, hint, or text ever implies crouch conceals.

- **REF:** GAP line 9 (ruling c045: "CROUCH: RULED, allowed as a BODY VERB and useless against him BY ARCHITECTURE: his model has no posture channel and no footstep channel"); INV I31 ("no hunter or director code path reads player posture … grep-level audit plus a soak with a crouch-walking bot showing identical coverage response"); `scripts/noise_tracker.gd:9-19` (footstep noise keyed to velocity > 0.5, not posture); TIMINGS `CROUCH_MULT 0.55`.
- **UE home:** `ARitaCharacter` (`RitaCharacter.h:22-23`: CrouchMult 0.55, CrouchDrop 0.6); PROVEN: `RITA crouch speed=1.71 m/s camdrop=0.60` [EVIDENCE line 23]; grep `Crouch|bCrouched|posture` over `Rundown.cpp` and `RestorationState.cpp` → 0 hits (verified for this file).
- **PROOF:** FIXTURE `test_rita.py` (EXISTS) for height/speed. INSPECT `Restoration.Crouch.NoReaders` (static, I31's grep): `bCrouched` is read only inside `ARitaCharacter`. SOAK: run `test_invariants.py` twice, the second with the target pawn crouched (the fixture's target is a cube today — add a crouched-Rita variant when the noise tracker lands, 4.0) → the two decision logs are byte-identical after stripping timestamps. INSPECT `Restoration.Crouch.NoTextImpliesHiding`: grep GAMETEXT for `crouch|duck|hide` in the same key → assert none pairs crouch with concealment (the only crouch text is the booth's label, if any).
- **STATUS:** PARTIAL — height/speed EXISTS; static grep EXISTS in effect (0 hits today); soak DESIGNED.
- **OPEN:** none.

#### QA-59
> QA-59 Ambient ledger audit: every item in the Ambient Lore Ledger exists in its room, prompts nothing, never moves, and reads at all three depths; any graduated statement of a protected truth is an S0.

- **REF:** LORE (the ledger); PLAN §1 Design law ("never-stated ledger — naming a ledger truth in text is an S0 defect"); PROGRESS PHASE 3 preamble ("every one promptless, static, three-reads compliant"); the room briefs' §3.N.6 placement tables (3.1–3.10 exist; 3.11–3.20 are C4/C5, in PRs #23/#24).
- **UE home:** Phase 3.
- **PROOF:** INSPECT `Restoration.Lore.LedgerPlaced` (per room): for each LORE line homed in the room (the brief's list, which the C3 verification already asserted against the canon ledger), an actor exists inside the room bounds tagged `AmbientLore:<key>`, implements no interactable interface (QA-55), and has zero transform delta across the QA-56 soak. "Reads at all three depths": CAPTURE ×3 per item (gameplay distance, 1 m, and the room-wide frame; PLAN §R.5 "Scale-truth: judge at gameplay distance AND 1m closeup") judged by eye. The S0 clause: INSPECT — GAMETEXT and every `Data/` string vs the ledger's protected-truth list (LORE's never-stated entries) → any literal match is an S0.
- **STATUS:** DESIGNED (Phase 3).
- **OPEN:** none.

#### QA-60
> QA-60 The unnumbered reels: W1 in the skip gap (Day 2); W2 exists only after W1 (Day 3); W3 only after W2 (Day 4); each first viewing requires four dailies logged and consumes one S2 slip with refusal lines otherwise; re-reads free; nothing announces on completion; A26 counts only the D series.

- **REF:** WALK line 292 (the pilgrimage, verbatim: W1 in the library's skip gap where 0118 should be (Day 2) → W2 behind the burn barrel (Day 3) → W3 on the shed shelf (Day 4); "each viewing spends one S2 slip"); ACH line 45 ("A26 FULL ACCESSION remains at ten documents; the Peak dossier (D11) is extra credit"); `scripts/achievements.gd:77` (`read_props.size() >= 10` → A26 — counts every read prop; D-only filtering is not in that line). **The reels are not in the reference code**: grep `W1|W2|W3|unnumbered` over `scripts/*.gd` → 0 hits; ROOM-BRIEFS-3.1-3.5 3.5-G and -3.6-3.10 §3.6/§3.8 note "W-series text keys not in GameText.csv".
- **UE home:** none; no unit names the reels (Phase 3 briefs place W2/W3 spawn sites; the mechanic has no box — §3 proposes one).
- **PROOF:** TEST `Restoration.Secret.Reels` (buildable only after the mechanic exists): Day 1 → no W1 actor; Day 2, dailies < 4 → W1 present, interact → the refusal line (text OPEN-27), no S2 paper spent; dailies ≥ 4, paper S2 = 3 → viewing, `Paper["S2"] == 2`; W2 absent until W1 viewed and Day 3; W3 absent until W2 viewed and Day 4; re-read → paper unchanged; on W3's completion → zero notifies, zero achievements; `ReadProps` with all three reels + 9 D-series → A26 NOT unlocked (D-only count); with 10 D-series → unlocked.
- **STATUS:** OPEN — the mechanic exists in canon only (WALK c046 addendum); the reference does not implement it, so no fixture can be run against a reference truth; the test above is written from WALK and ACH and waits for a ruling to build the mechanic.
- **OPEN:** OPEN-27 — refusal lines, the reels' text keys, and the "nothing announces" rule have no code and no GAMETEXT rows; `achievements.gd:77` counts all read props, contradicting "A26 counts only the D series" (ACH line 45 agrees with QA-60; code does not).

#### QA-61
> QA-61 AUDIENCE ONLY: the radio caption fires only with all three reels watched AND the dial confirmed at the dead room radio (which appears only after W3); Q within six seconds starts the 75 s run; reaching the dead room routes ending A with her single credit card; declining or arriving late falls through to the normal break chain untouched; no achievement exists for this ending by design; the post-credits program guide plays for this ending only; the title screen carries 58 · STILL ON on every later launch.

- **REF:** WALK line 292 (verbatim: "visit the dead room and CONFIRM the radio's dial. Only then does the final break gain a caption no run sheet carries: a radio, through three walls. Take Q, cross inside 75 seconds … ENDING A · AUDIENCE ONLY … the exclusive post-credits PROGRAM GUIDE … a permanent mark on the title screen ever after: 58 · STILL ON. … No achievement acknowledges it"). PRESENCE ("Never: any ending name"). **Not in the reference code**: grep `AUDIENCE ONLY|STILL ON|program guide` over `scripts/*.gd` → 0 hits; GAMETEXT has no `STILL ON` / `AUDIENCE ONLY` row (grep → 0). The existing crossing (`live_production.gd:222-234`) is DEAD AIR's, 75 s, not ending A's. The "six seconds" window and the dial confirm have no code.
- **UE home:** none; no unit.
- **PROOF:** TEST `Restoration.Secret.EndingA` (after the mechanic exists): all three reels viewed ∧ dial confirmed → the final break carries the radio caption; any one false → no caption and the normal chain (QA-28) untouched; Q at 5.9 s → the 75 s run; Q at 6.1 s → falls through; reach the dead room → `EndingReached` = the ending-A name, credits with exactly one credit card, then the program-guide sequence; `Unlocked` unchanged (no achievement — INSPECT: no achievement id maps to this ending); a later title boot shows `58 · STILL ON` (a new saved flag, OPEN-28); the program guide does not play after any other ending (loop the routing table).
- **STATUS:** OPEN — canon only (WALK c046); nothing in code or data carries it.
- **OPEN:** OPEN-28 — the persistent title mark needs a saved (or settings-level) flag the v16 schema does not have (55 keys, none for it) — a schema change is "WHAT MUST NOT CHANGE: save semantics" territory [PLAN §1 UE5-MIGRATION-MAP] and needs the owner. OPEN-29 — ending A's routing name and credit-card text have no GAMETEXT rows.

---

## 2 · THE MATRIX (61 rows)

Kind: F fixture · T automation test · C capture · I inspect · P playtest · S soak. Status per §0.3. "Owns" = the PROGRESS unit that makes the proof runnable.

| QA | Kind | Status | Existing proof today | Owns |
|---|---|---|---|---|
| 01 | T, C | DESIGNED | — | 4.ACCESS |
| 02 | P, T, C | DESIGNED | — | 4.ACCESS / 5.2 |
| 03 | T, C | DESIGNED | — | 4.FINALE / 5.2 |
| 04 | T | DESIGNED | — | 4.ACCESS |
| 05 | F, T, C | PARTIAL | test_loop_fns.py (SIGNED, SIGNFLOW) | 0.8b-5 (caption) |
| 06 | F, C | PARTIAL | test_bench.py (12 s, CLEAN SIGNAL) | 0.8b-5 (countdown); bars OPEN-3 |
| 07 | F, T, C | PARTIAL | test_failbot.py + RETAKE lines (0.8b-6) | 0.8b-5 (card) |
| 08 | F, T, C | PARTIAL | test_failbot.py + parser UE-R1 | 0.8b-5 (card) |
| 09 | F | PARTIAL | test_harriet.py (freeze) | 2.3 (cup geometry) |
| 10 | T, C | DESIGNED | clock exists (0.7) | 4.0 doors; 5.1 tone |
| 11 | T, I | DESIGNED | — | 2.2 Merle; 3.1 pegs |
| 12 | F, C | PARTIAL | test_invariants.py, test_failbot.py, parser I01 | 1.11 (savoring pose) |
| 13 | F | PARTIAL | test_invariants.py, parser I22 | 0.8b-5 (once-line) |
| 14 | F, S, T | PARTIAL | test_state_af.py (tally contract) | 3.x cones; 3.16 revive; **OPEN-8** |
| 15 | T, C, P | DESIGNED | — | 5.2 |
| 16 | T | DESIGNED | — | 4.ACCESS |
| 17 | T, C | DESIGNED | — | 4.ACCESS |
| 18 | T, P, C | DESIGNED | — | 0.8b-5 / 4.ACCESS |
| 19 | T, C | DESIGNED | — | 2.6 / 4.0 |
| 20 | F | DESIGNED | parser I07 | 4.0 / 4.FINALE |
| 21 | T, I | DESIGNED | keys 25 + struct field | 4.0 |
| 22 | T, C | DESIGNED | keys 23/24/36 | 3.9 / 4.0 |
| 23 | T, I, C | DESIGNED | keys 22/44 | 3.9 / 4.0 |
| 24 | I, T, S | DESIGNED | key 26 | 3.20 |
| 25 | T, I | DESIGNED | keys 53/55 | 3.13 / 4.0 |
| 26 | T, C | DESIGNED | key 29; SPIKE 2 feeds | 4.FINALE |
| 27 | F, T | DESIGNED | parser I06 | 4.FINALE |
| 28 | T | DESIGNED | keys 28/30/31 | 4.FINALE |
| 29 | T, I | DESIGNED | — | 4.ACCESS (0.8c) |
| 30 | I, T | DESIGNED | DemoOpen.csv | 5.8 |
| 31 | T | DESIGNED | round-trip (0.8b-3) | 4.SAVE |
| 32 | T | DESIGNED | — | 4.ACCESS |
| 33 | F, T | PARTIAL | test_state_af.py (round-trip) | 3.9 / 4.0 |
| 34 | F, T, C | PARTIAL | test_state_af.py (AF loom) | 0.8b-5 HUD; 5.1 steps |
| 35 | T, C, I | DESIGNED | — | 1.12 |
| 36 | F, C | PARTIAL | test_state_af.py (taught cool → strike) | 1.10 (withdrawal) |
| 37 | F, T, C | DESIGNED | DoorFoldCheck exists (0.7) | 1.10; 0.8b-5 caption |
| 38 | F, T | PARTIAL | test_state_af.py (felt door) | 0.8b-5 HUD |
| 39 | T, I | DESIGNED | struct + key 46 | 0.8b-5 / 4.0 |
| 40 | T, S | DESIGNED | key 47 | 2.2 / 4.FINALE |
| 41 | F, T | PARTIAL | SignLog slip branch (0.8b-4) | 0.8b-5 |
| 42 | T | DESIGNED | keys 33/34 | 3.16 / 4.FINALE |
| 43 | T | DESIGNED | — | 4.FINALE |
| 44 | T | DESIGNED | keys 23/24/48 | 3.9 / 4.FINALE |
| 45 | T, C | DESIGNED | — | 4.FINALE |
| 46 | F | DESIGNED | key 49 | 4.FINALE |
| 47 | T, C | DESIGNED | — | 4.FINALE |
| 48 | I, T | DESIGNED | — | 5.8 |
| 49 | T | DESIGNED | key 50; Take = −1 | 2.3 / 4.0 |
| 50 | T | DESIGNED | — | 3.9 / 4.FINALE |
| 51 | F, I | **OPEN** | — | 4.QA51 (**OPEN-24**) |
| 52 | C, I | DESIGNED | — | 1.10 |
| 53 | I, T, C | DESIGNED | — | 1.9 / 1.11 / 1.12 |
| 54 | I, T | DESIGNED | — | 1.11 / 1.12 / 5.1 (**OPEN-26**) |
| 55 | I | DESIGNED | interface exists (0.8b-2) | 3.x per room |
| 56 | I, S | DESIGNED | — | 3.x per room |
| 57 | I | DESIGNED | — | 3.x per room |
| 58 | F, I, S | PARTIAL | test_rita.py; 0 posture readers | 4.0 (soak) |
| 59 | I, C | DESIGNED | — | 3.x per room |
| 60 | T | **OPEN** | — | none (**OPEN-27**) |
| 61 | T, I | **OPEN** | — | none (**OPEN-28/29**) |

Census: EXISTS 0 (no line is fully proved by a fixture that runs today) · PARTIAL 14 · DESIGNED 44 · OPEN 3. Fixture lines quoted from EVIDENCE cover parts of the 14 PARTIAL rows.

---

## 3 · WHAT THE MAC LANE NEEDS (proposals; nothing here edits PROGRESS.md)

### 3.1 Fixture extensions to existing `ue/pyscripts/` (cheap; the machinery is proven)
| Fixture | Extension | Rows |
|---|---|---|
| `test_loop_fns.py` | read the slot after `SignFinish` and print `Paper["S1"]`; the harriet-slip branch printed (`bHarrietSlip`, paper 0 → one SIGNED then one SIGN REFUSED) | 05, 41 |
| `test_bench.py` | sample `RecordingLeft` at 1/6/11 s | 06 |
| `test_failbot.py` | 7-strike run printing the `lost=` sequence; One-Take variant | 07, 08 |
| `test_harriet.py` | cup Z at Day 1/3/6/7; the interact line ∈ LINES | 09 |
| `test_invariants.py` | negative 12 s memory variant; once-line counter; crouched-target twin run | 13, 58 |
| `test_state_af.py` | print `af=%d` in SAVE-ROUNDTRIP; approach speed sample; loom-line count; three cool runs (taught 4.0 / later 2.0 / distance → anchor); dead-room deafness + felt-door once | 33, 34, 36, 38 |

### 3.2 New fixtures
`test_fold.py` (37; adds one `FOLD door= t=` evidence line — token chosen not to collide with the parser's WARN/STRIKE/RELOCATE/INCIDENT/RESOLVED/VIOLATION/RUN ENDED set), `test_cascade.py` (20), `test_premiere_failbot.py` (27, 46, 51), `tools/braid_audit.py` (51, after OPEN-24).

### 3.3 Automation tests, by name
LAW9's 24 named tests are reused verbatim (rows 01, 04, 05, 16–18, 19, 25, 29, 30, 32, 37, 48). New names introduced here: `Restoration.Access.Title.FocusRing`, `Restoration.Credits.Crawl`, `Restoration.Retake.Card`, `.RunDeathCard`, `Restoration.Schedule.WindowHold`, `.ToneFollowsPhase`, `Restoration.House.MerleWhere`, `Restoration.Patchbay.Revive`, `Restoration.UI.MapFooter`, `Restoration.Night.TripOnce`, `Restoration.Story.{Presigned,SeanceGate,FireTape,OnceEver}`, `Restoration.Dock.{WarmOneIsInert,FileSix}`, `Restoration.Finale.{Lockdown,MarkNeedsPgm,Divert,VariantLines,EndingZero,LedgerReadAloud}`, `Restoration.Demo.{RoomsFromData,Save,NoDeathPath}`, `Restoration.State.MigrateV15`, `Restoration.HUD.{TallyCountdown,DeadRoomFirstEntry}`, `Restoration.Audio.{AfStepInterval,BandLimits}`, `Restoration.Chum.{EyeFollowsRecording,ZeroSecondary,ParkedStillness,QuoteOnlyUnderTally,JawOnlyByHand}`, `Restoration.Ledger.{BinderPageOne,M1,H1,V1,V2,F2,F1,L1,L2,H2,SeanceGrief}`, `Restoration.Taxonomy.{PromptCensus,DriftAudit,HeroCensus}`, `Restoration.Crouch.{NoReaders,NoTextImpliesHiding}`, `Restoration.Lore.LedgerPlaced`, `Restoration.Secret.{Reels,EndingA}`.

### 3.4 Tracker boxes this file implies (for the owner to splice, per LAW9 §9's precedent)
- **4.QA (new, under PHASE 4):** "the QA-61 executable: build §3.1 extensions and §3.2 fixtures as each system lands; a row ticks only with its proof's output in the ledger" — the standing home for this file.
- **4.SECRET (new):** the reels and ending A (QA-60/61) — no box exists; canon-only (WALK c046). Needs OPEN-27/28/29 ruled first.
- 4.QA51 already exists; it needs OPEN-24 (the peak definition) before it can start.

---

## 4 · OPEN (consolidated; the owner rules, this file does not)

| Id | Rows | Question |
|---|---|---|
| OPEN-0 | all | The box says 51 items; canon lists 61 (never 51 at any commit). This file covers 61. Confirm, or name the 51. |
| OPEN-1 | 02 | The phosphor focus ring's colour value in UE (art bible names the colour, not a number). |
| OPEN-2 | 05 | The pen-tick caption's text/key (the reference has a sound, no caption text; LAW9 §3.3 counts the gap). |
| OPEN-3 | 06 | The tape stage / CRT stack has no UE home yet; "bars play" is provable only after it. |
| OPEN-4 | 11 | Merle has a fourth place in code (the screening seat) vs the QA line's three. |
| OPEN-5 | 11 | The pegs' "day table" is `_drift()`'s formula; no canon document lists per-day values. |
| OPEN-6 | 12 | "Warn fills ledger line": no code writes the binder on WARN. |
| OPEN-7 | 13 | "Within 12 s it relocates" (QA) vs "relocates at the next BREAK if the noise is < 12 s old" (code). |
| **OPEN-8** | 14 | **LAW 1 / LAW 11 "camera cone prevents the strike" has no reference implementation; the code's on-camera safety is the tally contract (LAW 10) + the premiere yield. Build a cone guard, or rule the contract satisfies it?** |
| OPEN-9 | 15 | "Sealed rooms dashed" — the style is whatever `map_view.gd:_draw` does; not a canon rule. |
| OPEN-10 | 20 | "Restoring out of order refuses" — the reference offers no out-of-order input; the label is the order. |
| OPEN-11 | 21 | Presigned precondition: QA "with zero paper" vs code "first S4 interaction from Day 2". |
| OPEN-12 | 22 | Wear ladder "per answer" (QA) vs per frame-step (code). |
| OPEN-13 | 26 | The rec-chair tween duration (in `rec_chairs.gd`, not canon). |
| OPEN-14 | 30 | Seven named `demo_mark` sites in the reference (`started`, `s1_signed`, `capture_start`, `lunge`, `capture_done`, `screening`, `card`); QA says six. Which six? |
| OPEN-15 | 31 | The v15 save's shape (the repo ships v16 only). |
| OPEN-16 | 34 | First-sighting toast "once per save" (QA) vs once per process (`_af_seen_once` unsaved in both engines). |
| OPEN-17 | 37 | The 6.0 s per-door re-fold cooldown: two crossings of the same door inside 6 s buy 2.2 s, not 4.4. |
| OPEN-18 | 40 | "The kettle caption" — the reference toasts; no caption call. |
| OPEN-19 | 41 | "Her card was unfound" — the seventh-signal gate reads `is_dead("HARRIET")`, not a card flag. |
| OPEN-20 | 44 | Whether L2 clears `has_fire_tape` ("consumes it"). |
| OPEN-21 | 45 | "Nine cards" — the count depends on `credits.gd`'s list; not counted here. |
| OPEN-22 | 46 | Row lines "with the caption" — toast only in code. |
| OPEN-23 | 49 | The splice prompt's disclosed label text. |
| **OPEN-24** | 51 | **What is a "pressure peak" and what counts as an "attention demand" (is the PGM switcher one?). Until defined, QA-51 is not executable.** |
| OPEN-25 | 52 | Does the fold's 2.2 s scale with door width (MOTION "per door width") or stay constant (code)? |
| **OPEN-26** | 54 | **"The bell never sounds" (QA-54, PLAN §1) vs LAWS line 6 "rings once, at the finale beat" and `hud.gd:452`. This file tests: one site, finale only, captioned.** |
| **OPEN-27** | 60 | **The unnumbered reels exist in WALK only; no code, no GAMETEXT; `achievements.gd:77` counts all read props vs "A26 counts only the D series".** |
| **OPEN-28** | 61 | **Ending A's permanent title mark needs a saved flag the v16 schema lacks (save semantics are frozen by the migration map).** |
| OPEN-29 | 61 | Ending A's routing name and credit-card text have no rows. |

---

## 5 · WHAT THIS FILE DID NOT DO

- Run anything. No fixture, test, capture or soak was executed; every EXISTS claim is EVIDENCE's, at HEAD 4ba8db8, re-quoted.
- Rule. Every disagreement between a QA line, a law and the reference is quoted and numbered; none is resolved.
- Name the once-ever moment, or Chum in any presence, achievement or title string (LAWS lines 4 and 6; PRESENCE).
- Count the 51. It counted the 61 and asked.
