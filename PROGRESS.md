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
- [x] 0.2 Automation loop proven: tools/ue_loop.sh runs Blender FBX export
      → headless import (naming law enforced; 1m cube = 100.0uu exactly,
      recorded) → staged Lumen capture via gated init_unreal.py, one
      command, unattended (LOOP-COMPLETE 2026-09-03)
- [x] 0.3 Chum imported (full puppet FBX, 3.08m scale-true, all 30
      materials wired via manifest + direct texture import, MawBlack unlit
      + FurCards masked rebuilt natively) + dark locked-EV capture rig +
      ACCEPTANCE BASELINE archived (docs/telemetry/ue-baselines/). Known
      deltas for 1.8+: tally not yet emissive in UE, fur mottle vs plate,
      hardware tier. LFS deferred: no .uasset tracked in git yet (Content
      generated dirs ignored; revisit when Content assets need versioning)
- [x] 0.3b SODIUM CHECK built (tools/sodium_check.py): contact-sheet mode
      for master materials + --subject mode for baked assets (ball UVs lie
      on bakes — their own mesh tells the truth). First gate run on Chum
      PASSED fur/lens/hardware/whiskers and CAUGHT the un-rebuilt body:
      belly+patches read as faceted clay, hands/feet as wax — findings
      filed against units 1.1 / 1.4 / 1.5
- [x] 0.4 Quixel/Fab hookup: owner signed in; Fab plugin enabled in the
      project; import doctrine + starter shopping list at ue/FAB-IMPORT.md;
      credits ledger at ue/CREDITS-FAB.md. The physical pull is editor-UI
      only (no API) — batched into Phase 3's first room unit, or any time
      the owner spends 5 min in Window→Fab per the doc
- [x] 0.5 Data extraction (tools/extract_data.py, deterministic):
      ue/Restoration/Data/ = Rooms(20) Doors(20, locked reasons intact)
      Stations(5) Monitors(2) DemoOpen(7) Timings(32 constants w/ homes)
      GameText(714 keys from translations/strings.csv). Landmarks: no
      single source table exists — landmarks spawn in code; extract at
      P0 world-stamping when the interactable spawns are ported
- [x] 0.6 P0 — boot & walk: /Game/Greybox stamped FROM the CSVs
      (build_greybox.py, world_builder's algorithm: 20 rooms, 119 walls,
      7 door slabs w/ locked-reason world text, 5 stations, PlayerStart);
      DefaultPawn engine bindings = walkable; proofs archived. Godot feel
      parity (3.1 m/s, crouch c045) deferred into 0.8b — tracked there
- [x] 0.6b P1 — SPIKE 2 PASS: twelve SceneCapture2D feeds (256px,
      capture_every_frame) from twelve canon rooms onto a 4x3 unlit-RT
      wall in MASTER CONTROL; 601 PIE frames measured on the M1 Pro:
      avg 116.1 fps, p95 96.0 fps vs the 60 line — native territory,
      as the migration map predicted. Rig is ephemeral (ue/pyscripts/
      spike_wall.py rebuilds it on demand); numbers in the ledger are
      the engine memo's evidence
- [x] 0.7 P4a — ARundown (C++ tick brain, no Behavior Tree) + 
      URestorationClock (ON AIR 50s / BREAK 18s, timer-driven): ON AIR hunt
      with warn-once latch, strike + savor rule (>=3), no-strike-thru-wall
      raycast, BREAK relocation grammar (heard-noise-first, else cycle),
      2.2s door fold toll from Data/Doors.csv, ReportNoise API; telemetry
      appends Saved/decision_log.txt in the parser's exact format. Verified
      in simulate: WARN d=6.1 once, RELOCATE at the 50s flip, zero false
      strikes. AF states (tally contract/cool/crossing/dead-room hold)
      attach with GameState in 0.8 — marked TODO(0.8) in source
- [x] 0.8a State core: URestorationState (GameInstanceSubsystem) with the
      brain-relevant fields, Strike() retake economy core, InDeadRoom, v16
      URestorationSaveGame + round-trip verified; THE AF LAYER ported into
      ARundown — full arc proven in simulate: approach 0.8 m/s → loom 1.2m
      ("the jaw works its lever") → recording cutoff → taught 4s cool →
      STRIKE af tally-cool → hidden until the next contract. Two spec-order
      bugs caught: night gate must sit BELOW the AF layer; the visible gate
      guards cool re-arm (both exactly as rundown.gd orders them)
- [x] 0.8b-spec [CLOUD-OK] Transcribed the FULL v16 _save_dict schema
      (55 keys, types, defaults, load coercions, external writers) +
      game_state.gd public field/signal inventory (72 vars, 20 signals
      with emitters/listeners) into ue/PORT-NOTES-STATE.md, plus the
      settings.cfg schema, DEMO stripping, and a 0.8b delta checklist
      against the 0.8a C++ skeleton (7 shape mismatches, 32 missing
      keys). Verified by assert script against the source (VERIFY-OK)
- [x] 0.8b-1 ARitaCharacter + ARestorationGameMode + input map: feel
      parity proven to the digit (walk 3.10 m/s, crouch 1.71, cam drop
      0.60m, eased at 12/delta as player.gd lerps it); interact reach ray
      2.6m stubbed; WASD/mouse + Ctrl/pad-B crouch + E per controls map
- [x] 0.8b-2 The bench loop: ABenchCapture (IRestorationInteractable),
      12s forced-real-time capture driving State->bRecording (which arms
      the tally contract), 4m tether abort — both proven (TAPE 1 A CLEAN
      SIGNAL + CAPTURE ABORTED); Rita's reach ray dispatches the interface;
      SetNight broadcast added. Logging forced UTF-8 (0xff BOM crashed the
      py reader). CurrentTape/Captures in state
- [ ] 0.8b-3 State parity: apply ue/PORT-NOTES-STATE.md §6 deltas to the
      v16 SaveGame (7 shape mismatches inc. Paper->TMap, Signatures->array;
      32 missing keys; Mode/CurrentTape defaults) — the save's semantic
      fields must match the spec exactly
- [ ] 0.8b-4 P3 remainder: paper economy + stations + respawn, retake
      presentation, Harriet freeze, real day/night cycle, screening + assist
- [ ] 0.9 Harness: Gauntlet/functional-test maps, three bots, invariant
      parser reading the same logs; I01/I02/I22/I06 green in UE
- [ ] 0.10 PHASE GATE: parity slice — one room, Chum encounter, saves,
      QA subset green, THE-LAWS spot-audit, captured & reviewed

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
- [ ] 1.11 THE PERFORMANCE QUOTE (1.2m loom: frontal square-up + the one
      15° tilt + the jaw worked by his own hand at the lever, arrhythmic —
      and the once-only pre-strike jaw beat: hand, click, open, silence)
- [ ] 1.12 Tally states, eye tracking, throat-speaker room tone wired to AI
      (bell never sounds; no vocalizations; jaw never syncs to sound)
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

## PHASE 3 — The Studio (enumerated from docs/canon/restoration-room-bible.md;
per room: light family per lighting bible, I/L/D object budget, drift hooks,
web tie, Megascans surfaces + Fab/PolyHaven props + bespoke pieces, Lumen
pass, collision/nav, capture review. Dressing is authored FROM
docs/canon/restoration-ambient-lore-ledger.md — the room's ambient lore
details are placed FIRST, then dressing around them; every one promptless,
static, three-reads compliant. Taxonomy QA each room: QA-55 prompt
discipline, QA-56 drift=dressing-only, QA-57 one hero object max.)
- [x] 3.0 ENUMERATE — done by the Room Bible (all twenty below)
- [ ] 3.1 ENTRY (threshold; coat pegs drift ground zero; 1/0/8)
- [ ] 3.2 REC ROOM (the hearth; warmest light in the game; 2/1/14)
- [ ] 3.3 KITCHEN (Merle's nation; kettle is a real light; 1/1/12)
- [ ] 3.4 DORMS (five doors, three slept-in; blank name card; 1/1/10)
- [ ] 3.5 YARD (the only sky; tower light; 0/1/8)
- [ ] 3.6 SHED (tools that predate everyone; 1/1/6)
- [ ] 3.7 CORRIDOR (the spine; authored light gaps; 1/0/6)
- [ ] 3.8 TAPE LIBRARY (chapel of holdings; skip cluster; 2/2/16)
- [ ] 3.9 BENCH ROOM (Rita's altar; drift FORBIDDEN; 3/1/8)
- [ ] 3.10 CLIMATE (the lungs; gauge glow; 1/1/6)
- [ ] 3.11 TRANSMITTER HALL (the plant; mains organ note; 2/1/10)
- [ ] 3.12 DEAD ROOM (the one dark hide; mattest room; 1/1/3)
- [ ] 3.13 FIRE CORRIDOR (the scar; the wake begins here; 1/1/5)
- [ ] 3.14 STAGE HALL (anticipation as architecture; 0/1/6)
- [ ] 3.15 STUDIO A (the church; Chum's mark; little door; 3/2/18)
- [ ] 3.16 PATCH BAY (Vess country; the cascade panel; 3/2/12)
- [ ] 3.17 CONTROL (the marshal's corridor of record; 1/2/6)
- [ ] 3.18 MASTER CONTROL (the show's eye; monitor wall; 3/2/12)
- [ ] 3.19 GREEN ROOM (Harriet's parlor; two dead bulbs, always; 2/2/10)
- [ ] 3.20 SCENE DOCK (the confessional; THE SODIUM LIGHT lives here; 3/3/14)
- [ ] 3.FINAL PHASE GATE: full-studio walkthrough captures + soaks

## PHASE 4 — Puzzles & Functionality
- [x] 4.0 [CLOUD-OK] ENUMERATED: the mechanics census is
      docs/production/restoration-mechanics-enumeration.md — 34 boxes
      below in BUILD-ORDER acceptance order (P2→P6), each keyed to its
      reference script (the code is the intent), save keys, canon numbers,
      QA lines, invariants, and UE home. Every QA-01..61, I01..I31,
      A01..A28, all 55 save keys, all 32 Timings rows and all 73 reference
      scripts have an owner; verified by tools/verify_mechanics_enum.py
      (VERIFY-OK). Surfaced: M2 and ENDING A are prose-only in the
      reference; the reaction QUEUE (13 items) is entirely unbuilt
- [ ] 4.1 [CLOUD-OK] Landmarks.csv + Achievements.csv: extract the
      interactable spawn registry (every world_builder _spawn_* site:
      class, position, gate, label) and the 28-row achievement table via
      tools/extract_data.py, deterministic — the data-driven-world law;
      every box below spawns FROM these tables, never by hand
- [ ] 4.2 The tape world: crt_tape → material function stack (generation /
      tbc_on / photo_safe via an MPC), tape stage sublevel + Scare 1 Level
      Sequence (one-frame lunge), bench TV, gen knob (the slate lies, the
      scope does not); Spike 1 pass line; T and P as diegetic switches
- [ ] 4.3 Doors, keys & grammar v0: hinged/locked doors stating reasons
      from Doors.csv, the key chain (EDITH → shed → QUIET ROOM), window-
      bound doors HELD FOR AIR waived only in cascade, wall clocks (QA-10,
      I04, I08, A16)
- [ ] 4.4 The dresser, the sheet & run death: seven items loupe-last, the
      casting sheet as a wall object, NEXT WEEK'S EPISODE → title (no
      credits, morning-after CONTINUE), the NG+ relic (QA-07/08, I16/I17)
- [ ] 4.5 The club on schedule: Merle (kettle / chair / DOORWAY pen watch,
      1974), the coat-peg drift meter, Vess at the shrine + his binder
      (insight / credit flags), Harriet's seventh-signal note (QA-11, QA-56)
- [ ] 4.6 Frame Discipline: monitor rigs as SceneCapture feeds with tally /
      NO SIGNAL / stare-kill / re-patch / sync_to, the on-camera safety
      gate in ARundown + a SAFE/EXPOSED assertion overlay (QA-14, I05;
      Spike 2's other half)
- [ ] 4.7 The patchbay & power budget: one amperage budget, circuits,
      NO SIGNAL propagation, revive-first re-patch, the finale breaker
      phases, blackout scrim (Spike 6 half one; routes, not percentages)
- [ ] 4.8 The noise bus & night one: footsteps / doors / signatures / coil
      → ReportNoise, "It changed direction" once per run (QA-13, I22, A08),
      crouch honesty (QA-58, I31), the night-one trip once per save (P9)
- [ ] 4.9 The Floor Manager: nights ON AIR at the stack end inside 9 m,
      YOU'RE ON 3 s freeze check (holds / spoiled), absent on breaks and
      the premiere, assist hold; never heard moving (QA-19, P8, I15)
- [ ] 4.10 The cascade (Night 4+): circuit C → spread → B → ordered
      restoration refusing B before C → circuit F; holds waived; the
      Rundown bolder; liveness_log OK/VIOLATION (QA-20, I04, I07, A15)
- [ ] 4.11 The Coverage Director: checker / sprinter / hider from the
      counters, coverage_log with reason strings, kill priority, savoring
      at the last line, burn reset, the A/B(/C) blocking table as data,
      the poisoned well once per run (I21, V5, Spike 5)
- [ ] 4.12 Burn your dailies: a canister per capture in the stacks, single
      carry, the degausser burn removes a line and resets the read; abort
      and run end mint none (I09, I17, P2, P5)
- [ ] 4.13 After-Fire presentation & the dead room: the HUD REC · SAFE
      WHILE LIT lamp, the AF captions, first-sighting once per save, dead-
      room deafness + the felt-door hold + [NO ECHO], the eye lit only while
      recording (QA-34..38, I23..I26; the arc itself is 0.8a's)
- [ ] 4.14 Tape progression & the presigned page: day-mapped tapes, slated
      captures, the objective line, S4 Day 2+ zero-paper signature once
      (QA-21, I10, A09)
- [ ] 4.15 The film cabinet & the signal vocabulary: six signals taught
      once, the seventh via Harriet's note, signals_known feeding the FM
      and the 3 s seek grace (A07; QA-41's gate)
- [ ] 4.16 The readables & the binder: D01–D11 with read flags (A26 at ten;
      D11 after first sighting), TAB binder (ledger page one, presentation
      form, PT / keys / coverage lines; true-pause by day, live in the
      premiere), the M map from Rooms.csv, the glyph layer (QA-15, QA-39,
      QA-55, QA-59)
- [ ] 4.17 The fire tape: pickup, the forced watch with no sting, the wake
      (af_active + toast) once, M1's offer site, L2's consumption (QA-23,
      QA-33, QA-40, I15, A13)
- [ ] 4.18 The crate & the seance: the crate gate, Z/X over deterministic
      seeded frames (I20), five answers at fixed frames, wear 7 / 3.5
      burned in, knob restore, grief answers 14 / 28, L1 the sixth
      question, L2 the reading (QA-22, QA-44, QA-50, Spike 3, A14)
- [ ] 4.19 The dock task: six units, one warm, nothing follows ever, the
      card gated on filing, the Director never stages here (QA-24, I12,
      A10, P7)
- [ ] 4.20 The rejected edit & the splice: played, refused, one backward
      rotation, cobbler; the H2 temptation → shortcut daily → Harriet
      doubled forever, rebuilt on load (QA-49)
- [ ] 4.21 The Sign-Off assets & the decision ledger: verse (spectro dock),
      cart, script, card + the bench rack; pen cycle + SPACE commit, ink
      final, Merle to the doorway; V1's first trigger (QA-24, I19, A17)
- [ ] 4.22 The glimpse & the unseal: Day 4 fire corridor unseals; the
      elbow, under 2 s, once ever, unmediated; no entry anywhere and no
      descriptive class name (QA-25, I11, Law 3)
- [ ] 4.23 Lockdown: monitor sync, SEALED FOR BROADCAST, rec chairs to rows
      forever, Merle's line, persistent and re-applied on load; ending 0's
      precondition read here (QA-26, I18, A20)
- [ ] 4.24 Live production I — cues & sabotage: PGM cue marks + switcher
      refusal, the incident loop (tally / house / boom / cards) with
      fixtures and escalation, the triple fail-forward guarantee (≤2
      refusals, boom once, 40 s auto-fix), premiere_log, the Rundown
      yields, the bell once, the little door by hand (QA-27, I03, I05,
      I06, Spike 7)
- [ ] 4.25 Live production II — the club's hands: the Vess breaker
      (credited / uncredited / dead), F2 on the third blind call, the rows
      triage; M2 authored from the ledger text, prose-only in the reference
      (QA-42, QA-43, QA-46)
- [ ] 4.26 Live production III — the divert, the fader & the crossing: the
      window at the final break, F1 (SPACE his hand / hold-E 4.6 s hers +
      13 s tax), the 75 / 62 s crossing with the eye dark (reached / caught
      / late), ending 0's intercept (QA-43, QA-45)
- [ ] 4.27 The casualty ledger: mark_casualty idempotent, the ten deaths at
      their sites (M1 M2* V1 V2 H1 H2 F1 F2 L1 L2) + the rows, the ripples
      as data (kettle, pegs, breaker, 0.05, seventh signal, 62 s, cards,
      furniture), page one, the readings that never lie (QA-39..50,
      I27, I28)
- [ ] 4.28 The endings & credits: BURN (cold cobbler), NEW PRODUCER + the
      one interface lie at the title (I13), SIGN-OFF 1A/1B, DEAD AIR 4a/4b,
      4c, ENDING 0, THE LEDGER READ ALOUD + A27; ENDING A · AUDIENCE ONLY
      built from the addendum, prose-only in the reference (QA-28, QA-45,
      QA-47, QA-60, QA-61, I28, I29, A21–A25, A27, A28)
- [ ] 4.29 Title, pause & the credits shell: the save-aware menu, FILED
      WHILE YOU WERE OUT once, NEW EPISODE once, the demo badge, tree-wide
      pause refusing authored sequences, the crawl with grace-skip and the
      tower card (QA-01..04, QA-32)
- [ ] 4.30 The booth: volume / sens / fullscreen / TBC / photo-safe / text
      scale / captions / ASSIST, five-verb remap with KEY IN USE (UE: every
      action + the pad map, hold-to-toggle), settings apart from the save,
      the first-run booth (QA-16, QA-17, QA-18's switch)
- [ ] 4.31 Captions, glyphs & the string table: the caption bus with source
      tags, glyph substitution at the five chokepoints, tr() → GameText.csv
      StringTable (QA-05, QA-17)
- [ ] 4.32 Achievements: 28 ids, the deferral queue (morning toast / title),
      meta-silence, DEMO-disabled, the Steam bridge (QA-29, QA-45, QA-47,
      I30)
- [ ] 4.33 Demo mode: DemoOpen rooms + door reasons, spawn gates, the bed
      declines, S1 + S5 paper, the end sequence + protected card, the save
      whitelist, six funnel marks, the carry line, dead-Merle refusal
      (QA-30, QA-48, DP1–5)
- [ ] 4.34 THE-LAWS + rulings audit: eleven laws line by line on the UE
      build; the gap-audit rulings verified (no sprint, crouch honesty,
      binder-is-inventory, stations-only saves, one death card, photo mode
      Tier B); the modes-vs-"ASSIST only" conflict put to the owner
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
