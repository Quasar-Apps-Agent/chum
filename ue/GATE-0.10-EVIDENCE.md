# GATE 0.10 · RAW EVIDENCE (auto-collected at HEAD 4ba8db8, 2026-09-04 09:20)

Every Phase-0 fixture re-run in one pass. Lines are verbatim from
Saved/decision_log.txt (game telemetry) and the parser's INVLOG verdicts.
Collected by the loop; REVIEW IS THE OWNER'S — nothing here self-certifies.

## fixture: test_rundown.py
```
RELOCATE cycle -> segment 1 (profile UNKNOWN)
```

## fixture: test_state_af.py
```
SAVE-ROUNDTRIP v16 ok=1 match=1 strikes=7 wear=72.5 taught=1 decision=HIS HAND paperS3=1 sigs=1 leland=1
AF loom d=1.2 (the jaw works its lever)
AF tally cools (taught)
STRIKE af tally-cool
```

## fixture: test_rita.py
```
RITA walk speed=3.10 m/s (max=310)
RITA crouch speed=1.71 m/s camdrop=0.60
```

## fixture: test_bench.py
```
CAPTURE start tape 1
CAPTURE start tape 1
CAPTURE ABORTED · the take is lost
TAPE 1 · A CLEAN SIGNAL
```

## fixture: test_loop_fns.py
```
MORNING · Day 2 · Tape 2
NIGHT · the building belongs to the schedule
MORNING · Day 3 · Tape 3
PROTOTYPE COMPLETE
DAYNIGHT day=3 tape=3 run_complete=1
SIGNED S2 (paper left 2)
SIGNFLOW signed=1 paper 3->2 respawn=V(X=700.00, Y=-2980.00, Z=50.00) seg_now=0
READ D01 (1 of 10 documents)
TAKEN · the dead-room key
```

## fixture: test_harriet.py
```
HARRIET-FREEZE swayA=0.6090 swayB=1.7783 frozenC=1.7783 swaying=1 held=1
```

## fixture: test_invariants.py
```
WARN seg 0 d=6.1
STRIKE seg 0 d=1.8
WARN seg 0 d=1.8
RELOCATE toward heard noise at X=-500.000 Y=-2900.000 Z=0.000 -> segment 2
STRIKE seg 2 d=1.8
WARN seg 2 d=1.8
--- parser:
INVLOG| RESTORATION · INVARIANTS SCORECARD (UE)
INVLOG| I01 warn-precedes-strike: PASS
INVLOG| I02 no-strike-thru-wall: PASS
INVLOG| I22 heard-noise-attribution: PASS (1 attributed)
INVLOG| I07 cascade-liveness: N/A (cascade did not run)
INVLOG| I06 fail-forward-finale: N/A (premiere not yet ported)
INVLOG| UE-R1 full-sheet-ends-run: N/A (2 strikes, no full sheet)
INVLOG| PARSER-EXIT 0
```

## fixture: test_invariants_wall.py
```
WARN seg 0 d=6.1
STRIKE seg 0 d=1.8 THRU-WALL
WARN seg 0 d=1.8
RELOCATE toward heard noise at X=-500.000 Y=-2900.000 Z=0.000 -> segment 2
--- parser:
INVLOG| RESTORATION · INVARIANTS SCORECARD (UE)
INVLOG| I01 warn-precedes-strike: PASS
INVLOG| I02 no-strike-thru-wall: FAIL x1
INVLOG| I22 heard-noise-attribution: PASS (1 attributed)
INVLOG| I07 cascade-liveness: N/A (cascade did not run)
INVLOG| I06 fail-forward-finale: N/A (premiere not yet ported)
INVLOG| UE-R1 full-sheet-ends-run: N/A (1 strikes, no full sheet)
INVLOG| PARSER-EXIT 1
```

## fixture: test_failbot.py
```
WARN seg 0 d=6.1
STRIKE seg 0 d=1.8
WARN seg 0 d=1.8
RELOCATE toward heard noise at X=-500.000 Y=-2900.000 Z=0.000 -> segment 2
STRIKE seg 2 d=1.8
WARN seg 2 d=1.8
STRIKE seg 2 d=1.8
WARN seg 2 d=1.8 savor
STRIKE seg 2 d=1.8 savor
RUN ENDED take=4 (full sheet, fail forward)
WARN seg 2 d=1.8
STRIKE seg 2 d=1.8
WARN seg 2 d=1.8
--- parser:
INVLOG| RESTORATION · INVARIANTS SCORECARD (UE)
INVLOG| I01 warn-precedes-strike: PASS
INVLOG| I02 no-strike-thru-wall: PASS
INVLOG| I22 heard-noise-attribution: PASS (1 attributed)
INVLOG| I07 cascade-liveness: N/A (cascade did not run)
INVLOG| I06 fail-forward-finale: N/A (premiere not yet ported)
INVLOG| UE-R1 full-sheet-ends-run: PASS (5 strikes, run ended x1)
INVLOG| PARSER-EXIT 0
```
GATE-RUN-DONE 09:27:14
