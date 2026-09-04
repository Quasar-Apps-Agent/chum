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

Two frames, both archived to `docs/telemetry/ue-baselines/` and copied to
the Desktop as `chum-gate-0.10-current.png` / `-back.png`:

- **`renders/gate_0.10_greybox_chum.png` (primary, face side).** The
  imported After-Fire puppet (`/Game/Imported/SM_ChumAF`, scale-true
  3.08 m — he stands nearly wall-height, the walls being 3.0 m) at the
  TAPE LIBRARY anchor, camera inside the room at (4.2, −19.7) m. What to
  see: the tally lens lit (LAW 10's "the eye's light"), the rebuilt mouth
  and whiskers, the collar and dead bell, the belly patch; and the stamped
  DATA made visible — the **S1** station marker (Stations.csv) and the
  locked-door text **"SEALED · reopens for the anniversary (Tape 4)"** at
  the FIRE CORRIDOR door (Doors.csv, LAW 3's corridor). That is the "one
  room" clause in one frame: room, station, locked door, Chum.
- **`renders/gate_0.10_greybox_chum_back.png` (body-state evidence).**
  The same placement from behind: ears, collar, tail, and the torso and
  limbs in full.

**Honest reads, so the owner is not surprised:** (1) the torso, arms and
legs read as the faceted, white-flecked "clay" surface — that is
precisely the 0.3b sodium finding filed against units 1.1 / 1.4 / 1.5,
i.e. Phase 1's mandate, not a regression; the head is the only part that
has passed the gate and it is the only part that reads finished. (2) The
ears are blown out because the greybox lights each room with one plain
overhead practical and the puppet stands directly under it; the locked-EV
rig from 0.3 is not applied to the greybox (that is the lighting bible's
Phase 3 pass). Neither is a reason to fail the gate; both are reasons the
next phases exist. (3) The first attempt shot a lit wall slab from OUTSIDE
the room (camera at y = −10.4 m, wall at −11 m) — caught by looking before
shipping, per rule 4. The inside-camera positions now live as the script's
defaults.

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
