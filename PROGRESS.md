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
- [ ] 0.2 Automation loop proven (pyscripts: FBX import w/ naming law /
      material fixup / capture / log-grep; 1m-cube scale verify recorded;
      one-command mesh→capture unattended)
- [ ] 0.3 Chum head imported (FBX, sockets, ORM) + look-dev level v1
      (Lumen, locked EV, practicals w/ true bulbs) + ACCEPTANCE BASELINE
      capture vs the dossier plate; git LFS for ue Content when first
      .uasset lands
- [ ] 0.3b SODIUM CHECK lookdev scene in Blender (permanent material gate:
      sodium lamp, neutral floor; wired into the factory verification loop)
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
      beveled metals, fur density/anisotropy; AF jaw posed SHUT per canon)
- [ ] 1.9 THE POUR: AF locomotion per motion doctrine (linear-dominant
      curves, head-leads single arc, absolute stops, parked-statue idle,
      NO secondary motion, servo eye on its own layer)
- [ ] 1.10 THE FOLD + THE WITHDRAWAL (2.2s doorway montage per door width;
      reverse-exact-path retreat)
- [ ] 1.11 THE PERFORMANCE QUOTE (1.2m loom: frontal broadcast square-up +
      the one 15° head tilt, synced to tally state)
- [ ] 1.12 Tally states & eye tracking wired to AI (jaw NEVER opens; bell
      NEVER sounds; no vocalizations)
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
- [ ] 4.WEB reaction-matrix wiring audit (every action echoes in ≥2
      systems/people, per the QUEUE order in the canon doc)
- [ ] 4.SAVE integrity pass
- [ ] 4.ENCOUNTERS choreography per room
- [ ] 4.FINALE premiere sequence
- [ ] 4.QA51 braid audit (every pressure peak: ≥2 simultaneous demands)
- [ ] 4.VERB per-day verb-texture audit vs the dread curve
- [ ] 4.FINAL PHASE GATE: deep soaks, invariants extended

## PHASE 5 — Polish
- [ ] 5.1 Audio bed + foley on anim events (MetaSounds; AUDIO LAW:
      band-limited=memory / full-range=present; S17 footfall, S18 fold,
      occlusion bloom <3m, the wake's band-step-down cut)
- [ ] 5.2 UI/menus/accessibility (controls map: stable inputs, hold=commit,
      real binding glyphs; accessibility matrix R1-R7+ full target)
- [ ] 5.3 Post & atmosphere per room
- [ ] 5.4 Performance to 60fps on M1 Pro
- [ ] 5.5 Packaging (macOS) + 60-min packaged soak
- [ ] 5.6 Streamer mode (A1: compression-kind grain, safe HUD margins)
- [ ] 5.7 Clip ledger pass (A4: all named clippables verified capturable)
- [ ] 5.8 Demo — Tape 1 (A6: the funnel)

## PHASE 6 — Final Gates
- [ ] All boxes checked
- [ ] Packaged-build soaks clean
- [ ] Full playthrough capture review
- [ ] Credits complete (art + audio + Fab)
- [ ] Fan-content policy drafted (A5: generous, Fanverse-shaped)
- [ ] Owner sign-off

---
### ARCHIVE — Godot-era progress (pre-pivot, reference implementation)
- [x] Chum AF head designed & built in Blender through Commit 072 (face,
      real-lens tally eye, HD ears, rebuilt mouth, fur cards, in-file hair)
- [x] Asset pipeline proven (bakes, scans, donors, fur atlas, credits)
- [x] Godot look-dev rig upgraded (SSAO/SSIL/SDFGI/fog) — superseded by UE
- [x] Godot game: playable, soak harness green (kept as the port spec)
