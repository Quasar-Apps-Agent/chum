# GATE 0.10 · PHASE 0 → PHASE 1 · PARITY SLICE — OWNER REVIEW PACKAGE

**Status: AWAITING OWNER REVIEW. Assembled by the loop; nothing here is
self-certified.** The gate ticks in PROGRESS.md only when the owner has
looked at the capture, read the scorecards, and signed the spot-audit.

The plan's gate reads: *parity slice — one room, Chum encounter, saves, QA
subset green, THE-LAWS spot-audit, captured & reviewed.* Each clause below
maps to evidence in the tree at this commit.

## 1 · The parity slice, clause by clause

| Clause | Evidence | State |
|---|---|---|
| One room | `/Game/Greybox` stamped from `Data/*.csv` with world_builder's algorithm: 20 rooms, 119 walls, 7 door slabs, 5 stations (0.6) | in the tree |
| Chum encounter | The brain: `ARundown` warn→strike with the savor rule, thru-wall marking, heard-noise relocation, door toll; the AF tally-contract arc (loom 1.2 m → cutoff → 2.0 s cool → strike → hidden) (0.7, 0.8a) | EXERCISED — see `GATE-0.10-EVIDENCE.md` fixtures rundown / state_af / invariants |
| Saves | v16 `URestorationSaveGame`, all 55 keys, spec types; cross-type round-trip `match=1` (0.8b-3) | EXERCISED — fixture state_af |
| QA subset green | All nine Phase-0 fixtures re-run at HEAD in one pass, verbatim lines kept | `GATE-0.10-EVIDENCE.md` (auto-collected) |
| THE-LAWS spot-audit | §2 below | DRAFTED — owner signs |
| Captured | `renders/gate_0.10_greybox_chum.png` — the After-Fire puppet placed in TAPE LIBRARY, greybox lighting | see §3 |
| Reviewed | — | **OWNER** |

## 2 · THE-LAWS spot-audit (11 laws, Phase-0 evidence)

Legend — **EXERCISED**: a fixture proves it. **BY ABSENCE**: nothing built
yet can violate it, and a grep confirms no offending code. **NOT YET**: the
system it governs is a later phase; listed so it is scheduled, not forgotten.

| # | Law | Phase-0 evidence | State | Owner check |
|---|---|---|---|---|
| 1 | ON CAMERA IS SAFE | Tally contract: while `bRecording`, the brain approaches to 1.2 m and does not strike; STRIKE only after cutoff+cool (state_af). Static camera-cone hides are Phase 3 world content. | EXERCISED (mechanic) / NOT YET (cones) | ☐ |
| 2 | ONE STARTLE | No lunge exists yet; nothing else lunges, stings or pops (grep: no camera shake, no sting audio). The single in-tape lunge is Phase 2/4. | BY ABSENCE | ☐ |
| 3 | ONCE, EVER | No Day-4 content in UE. Save keys `has_fire_tape` / `fire_unsealed` are canonical v16 keys, not the moment's name. Owner to confirm the forbidden name appears in no UE file (the loop does not know it by design). | NOT YET / BY ABSENCE | ☐ |
| 4 | THE WARM ONE NEVER ACTS | Not instantiated in UE. | NOT YET | ☐ |
| 5 | SILENCE CONTRACTS | UE Chum has no audio, no vocalization, no presence/achievement string (grep Source: no "bell", no achievement, no presence). | BY ABSENCE | ☐ |
| 6 | THE SCHEDULE IS REAL | `URestorationClock` 50/18 s; hunt and relocation keyed to phase (rundown); **Harriet freezes on the break and holds mid-motion to the 4th decimal** (harriet). Window holds / cascade: NOT YET. | EXERCISED | ☐ |
| 7 | EVERY DEATH HAS A SIGNATURE | `FRestorationCasualty{Who,Cause,Line,Day}` carried in the v16 save; `mark_casualty` and the H1/H2 sequences are 0.8b-5 (deferred, UI-heavy). | NOT YET (schema ready) | ☐ |
| 8 | THE INTERFACE MAY LIE ONCE | No UI built. | NOT YET | ☐ |
| 9 | ACCESS IS CANON | **GATE CONCERN.** No booth, captions, assist, remap UI, pause or deferral rule exists in UE yet. Five rebindable actions are named in the data (`REMAP_ACTIONS`). This must be scheduled into the UI phase before any build is called shippable. | NOT YET — flagged | ☐ |
| 10 | THE TALLY CONTRACT | `AfLoomDist 1.2`, `AfCoolSeconds 2.0`, "AF tally cools (taught)" announced in the log; bench drives `RecordingLeft` (bench). The VISIBLE countdown is UI (0.8b-5). | EXERCISED (mechanic) / NOT YET (visible) | ☐ |
| 11 | THE TWO HIDES | Dead-room rect + "AF holds at the felt door" (state_af); door toll 2.2 s from `Doors.csv` (rundown). Lit camera-cone hides: Phase 3. | EXERCISED (dead room, toll) / NOT YET (cones) | ☐ |

## 3 · The capture

`renders/gate_0.10_greybox_chum.png`, archived to
`docs/telemetry/ue-baselines/`. It shows the imported After-Fire puppet
(`/Game/Imported/SM_ChumAF`, scale-true 3.08 m) standing at the TAPE
LIBRARY anchor inside the stamped greybox under its practicals.

**Honest note:** the puppet is PLACED for the capture; the brain
(`ARundown`) and the puppet are not yet one actor. Making the brain wear
the puppet — and move it under the motion doctrine (the pour, the fold,
the jaw by his own hand) — is Phase 1/2 work, not a gate hack. The gate
question is whether the slice's parts each hold; wearing them together is
the next phase's job.

## 4 · What the owner is being asked to decide

1. Open the capture. Does the room read as the club, and the puppet as the
   thing described? (Realism is Phase 1's mandate; here the question is
   scale-truth and placement.)
2. Read `GATE-0.10-EVIDENCE.md`. Every fixture's verbatim lines are there.
   Anything surprising?
3. Sign the spot-audit boxes above, or strike a row.
4. Rule on the flagged concern (LAW 9): agree it is scheduled into the UI
   phase, or demand it earlier.
5. Then tick 0.10 in PROGRESS.md yourself (or tell the loop to).

Known open Phase-0 items that do NOT block the gate but need eyes: the
0.8b-5 UI half (retake screen, screening, visible countdown, lighting
states). They are the first things the owner will see, so they wait for
the owner.
