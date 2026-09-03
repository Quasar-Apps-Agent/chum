# RESTORATION · INVARIANT SUITE v1
Per the build plan: each law, its test, its telemetry. Format per entry: LAW (the rule as fiction states it) · TEST (manual probe id from the playtest protocol, or soak assert) · TELEMETRY (the artifact that proves it in the wild) · STATUS (ENFORCED = the code cannot violate it; TELEMETERED = violations would be logged; MANUAL = probe-only for now). Any violation files at the protocol's severity S1 unless noted S0.

## A · GRAMMAR (the thing keeps the rules)
I01 Warning precedes reach. LAW: the Rundown warns inside its radius before any strike, except at three sheet lines, where silence is the design. TEST: soak assert on warn-then-strike ordering; probe V5 nights. TELEMETRY: coverage_log relocation and kill lines plus a strike-event line (harness adds). STATUS: ENFORCED (radius ordering), TELEMETERED partial.
I02 No strike through walls. TEST: soak with wall-adjacent bot; assert strike only with clear segment path. TELEMETRY: harness raycast log. STATUS: MANUAL (radius is spatial; wall check is harness work).
I03 The premiere yields the floor. LAW: the Rundown never hunts while the show is live. TEST: probe during PERFORM. TELEMETRY: absence of coverage_log hunt lines during premiere_log activity. STATUS: ENFORCED (premiere guard).
I04 Window holds obey the clock, and yield only to the cascade. TEST: probes P11 and cascade run. TELEMETRY: liveness_log "window holds waived" lines exist only while cascade_active. STATUS: ENFORCED.
I05 On camera is safe. LAW: no harm lands while the player is program on a live covered mark. TEST: soak in premiere with strikes forced. STATUS: ENFORCED by I03's guard at prototype grain; re-verify when hunting and premiere ever coexist.

## B · MERCY AND FAIRNESS
I06 Fail-forward finale. LAW: a cue can always be re-entered; no incident hard-blocks. TEST: fail every cue three times (protocol Spike 7 soak); leave every incident unfixed. TELEMETRY: premiere_log RESOLVED lines with "club auto-fix" at or under 40s; tally refusals never exceed 2; boom holds exactly 1. STATUS: ENFORCED + TELEMETERED.
I07 Cascade liveness. LAW: the panel is always reachable during the cascade. TEST: cascade run with doors deliberately closed. TELEMETRY: liveness_log OK cadence every 5s; VIOLATION line on breach. STATUS: ENFORCED + TELEMETERED.
I08 Every locked door states its reason. TEST: sweep all doors each build (probe P15 extension). TELEMETRY: none needed; the reason is the UI. STATUS: ENFORCED by data (locked_reason strings), MANUAL sweep for empty strings.
I09 Abort never costs a daily. TEST: probe P2. STATUS: ENFORCED.
I10 The presigned page costs no paper. TEST: probe P6. TELEMETRY: save diff shows signature added, paper unchanged. STATUS: ENFORCED.

## C · SCARCITY CONTRACTS (the once-evers; violations are S0)
I11 The glimpse never repeats. TEST: probe P10 including relaunch. TELEMETRY: glimpse_seen flag in save; harness asserts single spawn per save lifetime. STATUS: ENFORCED.
I12 The warm unit never acts. LAW: nothing follows, ever. TEST: probe P7 plus a full-run tail watch. STATUS: ENFORCED (no code path exists; keep it that way: this invariant is a review rule on future commits).
I13 The interface lie is spent exactly once. TEST: reach Ending 2, relaunch twice. TELEMETRY: lie_pending flips in save. STATUS: ENFORCED.
I14 One startle in the whole game. LAW: the Scare 1 lunge is the only startle-class event. STATUS: review rule + audio bible stinger policy; harness greps event table per build.
I15 The fire tape carries no sting; chairs make no nameable sound; the Floor Manager is never heard moving. TEST: silence-ledger audit per audio pass. STATUS: ENFORCED now (no audio exists to violate); becomes an asset-review gate.

## D · ECONOMY AND STATE
I16 Item loss is ordered and bounded. LAW: dresser order fixed, loupe last, losses persist through run end. TEST: probe P3 plus run-end CONTINUE. STATUS: ENFORCED.
I17 Sheet retirement is honest. LAW: run end zeroes strikes, keeps losses, mints no daily. TEST: probe P4. STATUS: ENFORCED.
I18 Lockdown is permanent. LAW: sealed doors, synced monitors, rowed chairs survive reload. TEST: probe P11 with relaunch. STATUS: ENFORCED (state re-applied on ready).
I19 The dock card gates on the filed inventory; the seance gates on the crate; the divert gates on key plus answers plus the fire tape. TEST: matrix probes (Section 3 of the protocol). STATUS: ENFORCED.

## E · DETERMINISM
I20 The same frame is always the same frame. LAW: seance frame idx renders identically forever (seeded grain). TEST: capture frame 14 twice across relaunches, diff. STATUS: ENFORCED (seed = f(idx)).
I21 The Director is deterministic and explainable. LAW: identical inputs yield identical profiles, and every blocking decision carries a reason string. TEST: input-replay diff (Spike 5). TELEMETRY: coverage_log. STATUS: TELEMETERED; replay harness is machine-side.
I22 Heard noise is attributable. LAW: every relocation-toward-noise names its cause. TELEMETRY: coverage_log "RELOCATE toward heard noise" with position. STATUS: ENFORCED + TELEMETERED.

## F · THE HARNESS PLAN (machine-side)
Headless Godot runner with three bots: WANDERER (random legal movement), CHECKER-BOT (monitor camping), FAIL-BOT (premiere: ignores every incident, fails every cue thrice). Runs: 4-hour night soak (I01, I02, I21), full-run matrix per ending (I13, I16 to I19), premiere soak (I03, I05, I06). Parsers over coverage_log, liveness_log, premiere_log emit a single INVARIANTS.txt scorecard per build. CI cadence: every zip before it is handed to a tester; the scorecard staples to the milestone gates (3.7 / 4.0 / 4.2) alongside the Dread Ledger.
Filing: violations use the protocol's severity language; S0 (scarcity contracts, save corruption) stops the line.

## ADDENDUM · INVARIANTS I23-I30 (the after-fire and the ledger)
I23 NO STRIKE WHILE LIT · law: recording true forbids GameState.strike from the hunter · test: soak bot captures with him adjacent for 10 minutes · telemetry: any AF strike log line during recording is S0.
I24 THE FOLD IS PAID · law: no AF door transit without the 2.2 s hold · test: position-delta audit across door radii in the coverage log.
I25 DEAF TO THE DEAD ROOM · law: noise events originating inside the bounds never alter his heard-state · test: bot signs and slams inside; his target must not move.
I26 ONE COOL TEACHES · law: the 4.0 s cool occurs at most once per save · telemetry: grep the teaching line count.
I27 DEATHS ARE IDEMPOTENT · law: mark_casualty for a taken name is a no-op; no double entries, no double toasts · test: force both Vess triggers in sequence.
I28 THE LEDGER NEVER LIES · law: every epilogue reading matches the binder page exactly, names and causes · test: string-compare at credits.
I29 CLEAN HANDS ARE SILENT · law: zero casualties and zero rows produce no reading and file A27 once · S0 if any reading text appears on a clean run.
I30 META-SILENCE HOLDS AT SCALE · law: no death, ending 0 included, produces a mid-play achievement toast; the once-ever moment still has no entry anywhere new · build check extended over the casualty files.
