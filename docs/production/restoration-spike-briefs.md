# RESTORATION · TECHNICAL SPIKE BRIEFS 1 TO 7
Per the build plan's Workstream 1. Each spike is 1 to 2 weeks, ends in a written PASS or a mitigation memo, and M0 does not exit until all seven are one or the other. The v0.5 prototype (commits 001 to 020) has pre-banked evidence against several; each brief states what is already in hand and what remains before the word PASS may be written.

STATUS BOARD
1 Tape-world pipeline: PARTIALLY RETIRED. 2 Frame Discipline: OPEN (hardware-bound). 3 Seance: PARTIALLY RETIRED. 4 Rundown AI: PARTIALLY RETIRED. 5 Coverage Director: SUBSTANTIALLY RETIRED. 6 Power sim: PARTIALLY RETIRED. 7 Live production: SUBSTANTIALLY RETIRED.

## SPIKE 1 · TAPE-WORLD PIPELINE
Question: can per-generation artifact simulation be a controllable, diegetic, tool-reactive shader stack rather than baked footage?
Pass line (plan): one clip, four generation states, artifacts diegetic and tool-reactive, photosensitivity-safe mode verified.
Method: take one real 20 second clip (phone-shot puppet stand-in is fine), run it through the shader stack, capture the four states side by side, wire TBC and tracking to live uniforms, then run the photosensitivity pass (cap flash frequency and luminance delta; a reduced-artifact mode that preserves diegesis, precedent already set by the UI specimen's reduced-motion support).
Banked: crt_tape.gdshader (chroma, scanlines, noise, tracking band, head-switch tear), generation uniform with the bench knob, TBC as live DSP, wear riding the same ladder (commits 008, 010, 020).
Remaining: real video texture instead of the live diorama, dot crawl term, the four-state capture reel, the safe mode. Timebox: 1 week. Fallback per risk register: licensed hardware-emulation middleware. Owner: Ciel's machine (GPU work), shader text from this side.

## SPIKE 2 · FRAME DISCIPLINE RENDERING
Question: do N live camera feeds at render-target cost hold 60 fps on target hardware with tally logic and provably correct mediated-safety state?
Pass line: 12 simultaneous feeds, one patchbay re-route, safety state provably correct in a test scene.
Method: scale the existing MonitorRig from its current handful to 12 in one scene, profile on the actual target machine, then write the safety-state assertion (a debug overlay that renders SAFE or EXPOSED from the ruleset and a test that walks every state transition).
Banked: MonitorRig as SubViewport render targets, kill and re-patch flow, lockdown sync_to (commits 002, 006, 012).
Remaining: the count, the frame-rate proof, the assertion overlay. This spike is hardware-bound and cannot be retired from text. Timebox: 1 week. Fallback: feed budget of 6 with round-robin refresh (visually authentic to period switchers anyway). Owner: Ciel's machine entirely.

## SPIKE 3 · THE SEANCE
Question: frame-accurate jog and shuttle over video, a compositing layer for Leland between frames, wear persisted?
Pass line: step, jump-cue, wear write-through to save, reload persistence.
Method: replace the diorama's staged frames with an actual VideoStreamTheora clip stepped by frame index, composite the Leland layer at frame boundaries, keep the existing wear plumbing untouched.
Banked: Z and X stepping, five fixed-frame reveals, wear written through to save and driving the artifact ladder, reload persistence proven (commit 010; knob restore fix in 020).
Remaining: real video substrate and jump-cue (type a frame number). Timebox: 1 week. Fallback: image-sequence player (frames as textures), which is period-plausible and trivially frame-accurate. Owner: split; the image-sequence fallback can be written from here.

## SPIKE 4 · RUNDOWN AI v0
Question: segment patrol with audio localization, camera-kill behavior, one unscripted seek, and zero grammar violations under soak?
Pass line: a bot survives a night using only audio cues; the AI never violates a grammar invariant in a 4-hour soak.
Method: add audio-event localization (footsteps, doors, the degausser emit events the Rundown weighs), write the survival bot against the segment-loop audio, then the 4 hour headless soak asserting the invariant list from the build plan (warn precedes reach, no strike through walls, no strike during ON AIR coverage).
Banked: segment patrol with homes and relocation, warn and strike radii, camera kills, savoring mode, director-expressed blockings, premiere yield (commits 003, 006, 009, 014).
Remaining: it does not hear yet; the bot; the soak harness. Timebox: 2 weeks. Fallback: scripted seek table per night instead of localization (authored, still fair). Owner: logic from here, soak on the machine.

## SPIKE 5 · COVERAGE DIRECTOR v0
Question: deterministic behavioral profiling selecting between blockings, explainable from a log?
Pass line: deterministic profile from logged inputs; blocking selection explainable in the log.
Method: add an append-only session log (timestamped counters and every blocking decision with its reason string), replay a recorded input file twice and diff the profiles.
Banked: checker, sprinter, hider profiling from behavior; three expressed blockings plus the savoring mood law; the burn reset (commit 009). The plan's scope guard is already honored: four booleans and counters, no learning.
Remaining: the log and the determinism replay. Timebox: 3 days. Owner: from here, verified on the machine.

## SPIKE 6 · POWER AND PATCHBAY SIM
Question: amperage budget, breaker trips, corridor liveness, sustaining the Night 4 sequence?
Pass line: the Night 4 sequence greyboxed end to end.
Method: extend the two-circuit budget to the full panel map from the room inventory, script the Night 4 cascade (trip, darkness spread, restoration order), assert liveness (some route is always lit or lightable).
Banked: two circuits one budget, NO SIGNAL propagation, revive-first re-patch, the night-one trip event, finale breaker phases (commits 004, 006, 017, 014).
Remaining: full panel scale, the cascade, the liveness assertion. Timebox: 1 week. Owner: from here.

## SPIKE 7 · LIVE-PRODUCTION FINALE LOOP
Question: cue sequencing, input mapping, sabotage events, retake checkpointing per cue?
Pass line: Phase 2 skeleton playable with placeholder everything.
Banked: this pass line is substantially met at prototype grain: cue marks, timed sabotage with take counters and per-cue re-entry, the breaker variants, the divert window, the little door cue (commit 014). The build plan's risk 3 mitigation (a cue can always be re-entered) is implemented.
Remaining before the written PASS: a switcher input map (number keys cutting cameras during cues) and a 30 minute fail-forward soak (deliberately fail every cue three times; no soft-lock). Timebox: 3 days. Owner: input map from here, soak on the machine.

## HOW THESE CLOSE
Each spike ends as one page: the pass line, the evidence (captures, logs, commit ids), and a signature line. Mitigated spikes instead state the fallback adopted and its cost. The seven pages staple to the Gate 0 packet, and M0 exits.
