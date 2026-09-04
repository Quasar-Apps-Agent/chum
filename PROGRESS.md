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
(Enumerated by unit 4.0 from the canon into ue/PORT-NOTES-MECHANICS.md —
one entry per box with sources, constants, evidence ids, UE home and the
four-step loop. PORT = reference code exists, the code is the intent;
IMPLEMENT = canon-only, the cited docs are the spec; RULING = unruled,
build nothing until the gap audit carries the decision. Order follows the
port kit: P4 remainder → P5 story gates → the puzzles → P6 meta. Verifier:
tools/verify_mechanics.py must print VERIFY-OK after any edit here.)
- [x] 4.0 [CLOUD-OK] ENUMERATE mechanics from the canon docs into boxes here
      (36 boxes below + ue/PORT-NOTES-MECHANICS.md; every QA-01..61, I01..31,
      A01..28 and every scripts/*.gd homed; assert-verified VERIFY-OK)
- [ ] 4.1 Camera cones + tally logic, Law 1 (PORT: monitor_rig; QA-14, I05)
- [ ] 4.2 Patchbay routing + amperage budget + revive (PORT v0 two circuits;
      IMPLEMENT the building-scale routing puzzle; QA-14)
- [ ] 4.3 The night trip, once ever (PORT: night_trip; QA-19)
- [ ] 4.4 The Floor Manager: signals, YOU'RE ON, the seventh (PORT +
      IMPLEMENT F-R1/F-R2; QA-41, A07)
- [ ] 4.5 The cascade: C then B, waived holds, liveness (PORT; QA-20, I04,
      I07, A15)
- [ ] 4.6 Noise, segment audio, the dead room — Law 11 (PORT; QA-38, I25)
- [ ] 4.7 The tally HUD + the eye's light — Law 10 visible (PORT; QA-33,
      QA-34, QA-35)
- [ ] 4.8 The Coverage Director: profile, blockings A/B/C, the poisoned well
      (PORT v0 + IMPLEMENT blockings/mood law; I21)
- [ ] 4.9 Burn Your Dailies + the casting sheet (PORT; I09)
- [ ] 4.10 The presigned page, singular (PORT; QA-21, I10, A09)
- [ ] 4.11 The impossible crate + the frame-séance, wear 7/3.5, MAX_FRAME 40
      (PORT; QA-22, QA-50, I20, A14)
- [ ] 4.12 The fire tape: forced watch, the wake, Merle's M1 (PORT; QA-23,
      QA-40, A13)
- [ ] 4.13 The scene dock — the warm one never acts, Law 4 (PORT; QA-24,
      I12, I19, A10)
- [ ] 4.14 The unseal + the glimpse — once ever, Law 3 (PORT; QA-25, I11)
- [ ] 4.15 The tape world: stage, bench TV, frame sequences, TBC, photo
      Tier B (PORT; shared surface for 4.11/4.12/4.19; no ids of its own)
- [ ] 4.16 Sign-off assets, the Vess credit dilemma, the rejected edit + H2
      splice (PORT; QA-42, QA-49, A11)
- [ ] 4.17 The decision ledger + THE BURN (PORT; A17, A21)
- [ ] 4.18 Lockdown, permanent (PORT; QA-26, I18, A20)
- [ ] 4.19a The premiere: cues, incidents ≤40 s, the rows (PORT; QA-27,
      QA-43, QA-46, I03, I05, I06)
- [ ] 4.19b The last crossing + the divert: 75/62/−13 s, the fader (PORT;
      QA-28, QA-44)
- [ ] 4.20 The casualty ledger — Law 7 (PORT; QA-39, QA-45, QA-47, I27,
      I28, I29, I30, A27, A28)
- [ ] 4.21 Endings, credits, THE LEDGER READ ALOUD, the one lie — Law 8
      (PORT; QA-03, I13, A22, A23, A24, A25)
- [ ] 4.22 The house: coat pegs, Merle's stations, Harriet, the bed (PORT +
      IMPLEMENT reaction queue; QA-11, A12)
- [ ] 4.23 Readables, keys, D01–D11, the ambient covenant (PORT; A16, A26)
- [ ] 4.24 Airdate math: 141/138, three names, GEN field (IMPLEMENT; no
      reference code; QA-62 to be written)
- [ ] 4.25 The film cabinet: six signals, the seventh, the pry (PORT +
      IMPLEMENT FORCE variant; A07)
- [ ] 4.26 The missing verse, the spectrogram, the assembled frequency (PORT
      spectro dock + IMPLEMENT audio bench/3 fragments; exercised by 4.19b)
- [ ] 4.27 The provenance suite: GEN knob, accession log, light table (PORT
      knob + IMPLEMENT log form/light table; A03; v17 candidate)
- [ ] 4.28 The bench craft suite: bake, splice, quality grade (IMPLEMENT; no
      reference code; QA-63..65 to be written)
- [ ] 4.29 RULINGS FIRST: avert, breath, formal-correctness phrases, PT
      tells, catwalk route, poltergeist layer, bench feel (RULING; build
      nothing until the gap audit rules)
- [ ] 4.30 The secret eighth ending: W1–W3, the radio confirm, AUDIENCE ONLY,
      58 · STILL ON (IMPLEMENT; canon c046; QA-60, QA-61)
- [ ] 4.31 The title + the booth: options, remap, first launch — Law 9
      (PORT; QA-01, QA-02, QA-04, QA-16, QA-17)
- [ ] 4.32 Achievements with the deferral rule, meta-silence (PORT; QA-29,
      I30)
- [ ] 4.33 Modes + DEMO whitelist + the Tape 1 funnel (PORT; QA-30, QA-48)
- [ ] 4.34 Pause, the binder, the map — rulings 3/4 (PORT; QA-15, QA-32)
- [ ] 4.35 Captions, glyphs, SFX cues, the string table (PORT; every box
      emits through it; no ids of its own)
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
