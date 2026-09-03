# RESTORATION · PROGRESS TRACKER — UE 5.8 CAMPAIGN
Companion to `AAA_BUILD_PLAN.md`. Work the FIRST unchecked box, top to
bottom. Tick only after the full verification loop. Add sub-boxes freely;
never delete history. (Pre-pivot Godot-era progress is archived at the
bottom — the Godot game is the reference implementation, kept runnable
through Phase 0.)

## PHASE 0 — Unreal Foundation & Core Port
- [x] 0.1 UE project skeleton (ue/Restoration, Lumen+VSM, git hygiene,
      headless launch proven: RESTORATION-PY-OK on UE 5.8.0; disk ~19GB —
      monitor per doctrine)
- [ ] 0.2 Automation loop proven (pyscripts: import / material fixup /
      capture / log-grep; one-command mesh→capture unattended)
- [ ] 0.3 Chum head imported + look-dev level v1 + ACCEPTANCE BASELINE
      capture vs the dossier plate
- [ ] 0.4 Quixel/Fab hookup (owner Epic sign-in; starter Megascans set;
      documented import path)
- [ ] 0.5 Player port (movement/look/interact parity with player.gd)
- [ ] 0.6 Studio blockout in UE (geometry + collision, walkable)
- [ ] 0.7 Chum actor port (behavior tree + anim BP: gait/strike/fold/
      head-track/tally states per rundown.gd)
- [ ] 0.8 Systems port (saves, doors, interactables, notes)
- [ ] 0.9 Test harness (automation tests for I01/I02/I22/I06 + wander soak)
- [ ] 0.10 PHASE GATE: parity slice — one room, Chum encounter, saves,
      tests green, captured & reviewed

## PHASE 1 — After-Fire Chum (Blender factory → UE acceptance)
- [ ] 1.1 Torso: quilted patchwork, seams, char zones, 2048 bake
- [ ] 1.2 Throat speaker (donor speaker/radio driver, chest mount, cabling)
- [ ] 1.3 Collar, leather strap, dead brass bell
- [ ] 1.4 Arms & hands: tendons both sides, articulated fingers
- [ ] 1.5 Legs: control rods, torn fur windows, weighted feet
- [ ] 1.6 Tail: segmented core, fur, rust tip
- [ ] 1.7 Full-figure unification + texture/size budget
- [ ] 1.8 Head realism retrofit per §R (staples→maps, sculpted teeth,
      beveled metals, fur density/anisotropy)
- [ ] 1.9 Gait animation (anim BP: weight, hips, counter-rotation, head lag)
- [ ] 1.10 Strike & fold (anticipation/recovery, no pops)
- [ ] 1.11 Jaw + mouth-lever sync
- [ ] 1.12 Secondary motion + tally flicker states wired to AI
- [ ] 1.13 PHASE GATE: 10-shot gallery + long soak, reviewed

## PHASE 2 — The Cast
- [ ] 2.1 Human pipeline v2 (evaluate MetaHuman vs Blender template in-unit)
- [ ] 2.2 Merle Cottry
- [ ] 2.3 Harriet
- [ ] 2.4 Vess Keys
- [ ] 2.5 Leland Merrick
- [ ] 2.6 Rita Ivori + floor manager variant
- [ ] 2.7 1974 Chum full pipeline
- [ ] 2.8 1971 pilot Chum full pipeline
- [ ] 2.9 Cast animation sets
- [ ] 2.10 PHASE GATE: lineup renders + captures

## PHASE 3 — The Studio
- [ ] 3.0 ENUMERATE rooms from world_builder.gd + canon docs into boxes here
- [ ] 3.FINAL PHASE GATE: full-studio walkthrough captures + soaks

## PHASE 4 — Puzzles & Functionality
- [ ] 4.0 ENUMERATE mechanics from the 13 canon docs into boxes here
- [ ] 4.SAVE integrity pass
- [ ] 4.ENCOUNTERS choreography per room
- [ ] 4.FINALE premiere sequence
- [ ] 4.FINAL PHASE GATE: deep soaks, invariants extended

## PHASE 5 — Polish
- [ ] 5.1 Audio bed + foley on anim events (MetaSounds)
- [ ] 5.2 UI/menus/accessibility
- [ ] 5.3 Post & atmosphere per room
- [ ] 5.4 Performance to 60fps on M1 Pro
- [ ] 5.5 Packaging (macOS) + 60-min packaged soak

## PHASE 6 — Final Gates
- [ ] All boxes checked
- [ ] Packaged-build soaks clean
- [ ] Full playthrough capture review
- [ ] Credits complete (art + audio + Fab)
- [ ] Owner sign-off

---
### ARCHIVE — Godot-era progress (pre-pivot, reference implementation)
- [x] Chum AF head designed & built in Blender through Commit 072 (face,
      real-lens tally eye, HD ears, rebuilt mouth, fur cards, in-file hair)
- [x] Asset pipeline proven (bakes, scans, donors, fur atlas, credits)
- [x] Godot look-dev rig upgraded (SSAO/SSIL/SDFGI/fog) — superseded by UE
- [x] Godot game: playable, soak harness green (kept as the port spec)
