# RESTORATION · PLAYTEST PROTOCOL v1
Build under test: Godot prototype v0.5 (commits 001 to 020). Owner: Ciel.
Purpose: convert playthrough hours into tuning decisions with named knobs.
Two modes: SELF (you, now) and EXTERNAL (testers, later; spoiler tiers below).

## 0 · SETUP
- Godot 4.3+, import the project folder, F5. Boots to title.
- Save file: user://transmitter_log.json (Godot: Project > Open User Data Folder).
- Full reset: NEW GAME from title. Migration test: copy an older commit's save in first, then CONTINUE; expect a MIGRATION toast, no crash.
- Controls: WASD, mouse, E interact, SPACE respond, Q improvise, T TBC, TAB binder, M map, Z/X seance frames.
- Record: timestamped plain notes. Format: [hh:mm] WHERE · WHAT · FELT. One line each. Do not tidy while playing.

## 1 · SESSION STRUCTURE
RUN 1 · THE COLD RUN (60 to 120 min): play title to any ending without this document open. Note only what pulls you out or pulls you in. Which ending you reach first is itself a datum: write it down before reading Section 3.
RUN 2 · DIRECTED PROBES (60 to 90 min): work Section 4 in order, skipping anything Run 1 already answered.
CLOSE: fill the report template (Section 8) same day. Memory of feel decays overnight.

## 2 · THE SEVEN STANDING VERDICTS
Each has: do, observe, anchors, and the knob it tunes.

V1 · WOOL SPIKE UNDER SODIUM. Do: stand at the bench, look at Chum on the tape stage; also the dock units. Observe: does the surface read as fiber or as fuzzy plastic? Anchors: 1 plastic, 3 acceptable greybox, 5 I want to touch it. Knob: shaders/wool.gdshader (fresnel strength, wrap term).
V2 · THE HOLD. Do: run a capture, watch the monitor through the final 3.2 seconds. Observe: does dread peak during the stillness before the lunge, or only at the lunge? Anchors: 1 lunge does all the work, 3 hold registers, 5 I wanted to look away before the lunge. Knobs: scripts/tape_stage.gd (approach speed 1.35, hold window 0.78 to 0.12, lunge scale 1.45).
V3 · ARTIFACT LOUDNESS AT GEN 0. Do: gen knob to MASTER, watch idle tape 20 seconds, TBC off. Observe: is the image damage distracting at the cleanest setting? Anchors: 1 unreadably noisy, 3 texture, 5 invisible until pointed at. Knobs: shaders/crt_tape.gdshader (noise floor 0.03 base, chroma 0.0012 base, band 0.16 factor).
V4 · TBC FEEL. Do: toggle T while watching tape. Observe: does TBC-on still feel like tape, or like turning the horror off? Anchors: 1 sterile, 3 steadier tape, 5 same world, calmer hand. Knob: the 0.7 steady factor in crt_tape.gdshader.
V5 · DIRECTOR READS EARNED. Do: one night living on monitors, one night sprinting, one night freezing near it. Check binder read each morning; note which blocking variants you saw. Observe: did consequences feel caused by you? Anchors: 1 arbitrary, 3 plausible, 5 it knows me. Knobs: scripts/coverage_director.gd thresholds; rundown warn 7/5, reach 2.2/2.6.
V6 · LELAND'S CROP. Do: open the seance, step to frame 7. Observe: does the frame-edge figure read as cropped by the frame, or as a prop standing at the side? Knob: tape_stage leland x 1.35 and camera framing.
V7 · FIRST ENDING REACHED. Record which, and why you chose that ledger entry. No knob; this is design telemetry.

## 3 · ENDING MATRIX SPEEDPATHS (for Run 2)
- Burn: decision DESTROY, four assets, night, sleep.
- New Producer: AUTHENTICATE path; afterward confirm the title reads NEW EPISODE exactly once, then reverts next launch.
- 1A: PERFORM with all five seance answers and wear at or under 70. 1B: PERFORM without.
- Dead Air: PERFORM holding the quiet room key, five answers, fire tape watched; take Q at the final break.
Verify each ending sets the objective line to ENDING REACHED and that CONTINUE resumes sane.

## 4 · DIRECTED PROBES
P1 Paper economy: burn all three S1 sheets by repeated signing; confirm the OUT OF PAPER state and that respawn falls back correctly.
P2 Capture abort: start a capture, walk past 4 meters; expect abort, tape stops with you, no daily minted.
P3 Retake presentation: take a strike; confirm slate, timecode rewind, item loss order (watch first, loupe last), respawn at last signed station.
P4 One Take: switch mode in the binder form, take one capture; expect the full NEXT WEEK'S EPISODE ending and morning-after CONTINUE.
P5 Dailies: mint two dailies, carry one to the climate room; confirm single-carry rule and that burning resets the Director read (binder shows AUDIENCE).
P6 Presigned page: Day 2+, first S4 interaction; confirm the three beats, no paper spent, signature listed.
P7 Dock: complete the count; confirm exactly one warm unit, no follow-up event ever, card appears in props crate only after filing.
P8 Floor Manager: at night on air, look at him inside 9 m; hold still 3 s (take holds), repeat next night and move (take spoiled). Confirm he is absent during breaks and the premiere.
P9 Night trip: fresh save, first night; at ~20 s expect the breaker beat once, never again on that save.
P10 Glimpse: Day 4 night, fire corridor elbow; after it fires, quit, relaunch, revisit; confirm it never refires.
P11 Lockdown: with four assets, at nightfall; confirm monitor sync, sealed exterior doors persist after reload, chairs in rows and staying in rows.
P12 Screening stances: hit SPACE deliberately off beat once, on beat once, improvise late once, and do one perfectly still QUIET; confirm all five outcome lines are reachable.
P13 Vess chain: skip the binder entirely on one run; confirm the blackout retake variant. Credit him on another; confirm the credited line.
P14 Merle doorway: raise the pen and wait; confirm she walks to the doorway and says nothing until ink is down.
P15 Map truth: with M open, walk three rooms; confirm outlines match walls and the dot never exits geometry.
P16 Seance knob: dial 3RD GEN, scrub five frames, close the reel; confirm the picture returns to 3RD GEN, not MASTER.

## 5 · FAIRNESS INVARIANTS TO WITNESS (from the build plan)
While playing, flag any violation as S1 minimum: warning always precedes reach (except at three strikes, by design); no strike through walls or during ON AIR camera coverage of the premiere; no scare during the forced fire tape; the glimpse never repeats; the warm unit never acts; every locked door states its reason; aborting capture never costs a daily; the divert window only appears when earned.

## 6 · SEVERITY AND TRIAGE
S0 crash or save corruption. S1 invariant violation or ending unreachable. S2 system misreads (Director, stances) or presentation break. S3 polish. File as: [S#] probe id · repro steps · expected vs got. S0/S1 jump the commit queue; S2 batches; S3 waits for its system's pass.

## 7 · EXTERNAL TESTER VARIANT
Tier A (spoiler safe): Run 1 cold plus probes P1 to P5, P15. Tier B (mechanics spoiled): P6 to P13. Tier C (story spoiled): Section 3 matrix. Never hand Tier C to a first-time player. Ask externals only V2, V3, V4 of the verdicts; the rest are author calls.

## 8 · SESSION REPORT TEMPLATE
Date / build zip name / mode (Matinee, Late Night, One Take) / TBC on or off.
Run 1 ending reached and why. Three moments that worked. Three that broke or bored.
Verdicts V1 to V7: score plus one sentence each.
Probes attempted / passed / failed (ids). Issues filed (ids with severity).
One tuning decision you are ready to make today. One question for the next build.

## 9 · DREAD LEDGER QUICK PASS (optional, end of session)
Score 1 to 5 per domain from the rubric: Fear Architecture, Player Truth, World Coherence, Systemic Honesty, Craft Surface, Sound, Performance Feel, Endings Weight. The prototype gates at 3.7 average for M-milestone purposes; note the two lowest and stop there.
