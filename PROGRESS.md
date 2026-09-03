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
(Enumerated by unit 4.0 from the canon docs + the reference scripts. The
register is ue/PORT-NOTES-MECHANICS.md: per box the GDScript spec, state,
UE home, laws/invariants, QA acceptance, and the four-step unit shape from
the plan §5 — port → diegetic feedback → fail-forward → automation test.
Boxes follow BUILD-ORDER P4 → P5 → P6; Phase 0 keeps what it already owns.
tools/verify_phase4.py asserts tracker ↔ register ↔ sources.)
- [x] 4.0 [CLOUD-OK] ENUMERATE mechanics from the canon docs into boxes here
      (34 mechanics / 39 boxes below; 73 scripts each given one home; laws
      1–11, I01–I31, QA-01–61, A01–A28, 14 actions, 32 timings all resolve;
      one CANON-ONLY box flagged (4.28b) — VERIFY-OK, cloud unit)
- [ ] 4.1 Frame Discipline: camera cones = the lit hide (monitor_rig.gd →
      SceneCapture feeds + cone volumes the Rundown queries; Laws 1/10/11,
      I05/I23; QA-14, QA-35)
- [ ] 4.2 Patchbay + amperage budget (patchbay_console.gd; circuits, revive;
      I04; QA-14 revive, QA-20 order refusal)
- [ ] 4.3 Noise, the dead room, the felt door (noise_tracker.gd, dead-room
      volume drops inside noise; I25; QA-13 → A08, QA-38 radio toast +
      [NO ECHO])
- [ ] 4.4 Night trip: first blood once per save (night_trip.gd; QA-19, P9)
- [ ] 4.5 The Floor Manager: 9 m look, 3 s hold, assist-hold; absent in
      BREAK + premiere; hands only (floor_manager.gd; I15; QA-19, P8)
- [ ] 4.6 The cascade + liveness: C then B, circuit F, holds waived only
      here (cascade.gd, liveness_check.gd; I04/I07; QA-20, A15)
- [ ] 4.7 The Coverage Director: profile from behavior, reason strings,
      burn resets the read (coverage_director.gd; I21; V5, P5)
- [ ] 4.8 Casting sheet, dresser, run end + modes (casting_sheet_prop.gd,
      dresser.gd, run_ended card; I16/I17; QA-07, QA-08, P3/P4; A18, A19)
- [ ] 4.9 Burn Your Dailies (dailies_manager/canister.gd, degausser.gd;
      single-carry; I09; P5)
- [ ] 4.10 Doors, keys, window holds (door.gd, key_item.gd from Doors.csv;
      I08/I04; QA-10; A16)
- [ ] 4.11 Readables + the Three Reads (readable_prop.gd, mark_read of 10,
      D01–D11; A26)
- [ ] 4.12 The credit chain: PER V. KEYS, Vess's binder, his lines
      (credit_entry.gd, vess_binder.gd, vess.gd; A11, P13)
- [ ] 4.13 Film cabinet + the seventh signal (film_cabinet.gd,
      harriet_note.gd; signals_known 6→7; A07; QA-41 gate)
- [ ] 4.14 The presigned page: Day 2+, S4, zero paper, saves free once
      (mark_presigned; I10; QA-21, P6; A09)
- [ ] 4.15 The crate + the frame-seance (impossible_crate.gd,
      seance_dock.gd, frame_sequence.gd; answers at 7/14/21/28/35, wear
      1.5/pass burns in; I19/I20; QA-22, QA-50, P16; A14)
- [ ] 4.16 Tape stage, CRT material stack, gen knob, TBC + photo-safe
      (tape_stage.gd, bench_tv.gd, gen_knob.gd, crt_tape params by name;
      Law 2 the one lunge; I14; QA-06 picture, V2/V3/V4; A03)
- [ ] 4.17 The fire tape: forced watch, no sting, af_active (fire_tape_
      pickup/dock.gd; I14/I15; QA-23, QA-33; A13)
- [ ] 4.18 Sign-Off assets: verse/cart/script/card + rack (asset_pickup.gd,
      asset_rack.gd, spectro_dock.gd; gain_asset of 4)
- [ ] 4.19 The dock contract: six units, one warm, nothing follows ever
      (dock_task.gd, dock_chum.gd; Law 4, I12; QA-24, P7; A10)
- [ ] 4.20 The once-ever sight, Day 4 fire corridor (glimpse.gd; Law 3,
      I11/I30; QA-25, P10; no achievement, no reference anywhere)
- [ ] 4.21 Lockdown: monitor sync, sealed doors, chairs to rows, permanent
      (lockdown.gd, rec_chairs.gd; I18; QA-26, P11; A20)
- [ ] 4.22 The club on schedule: Merle kettle/chair/DOORWAY, the pegs' drift
      (merle.gd, coat_pegs.gd; QA-11, P14; A12)
- [ ] 4.23 The rejected edit + the splice temptation (rejected_edit.gd,
      mint_shortcut_daily; QA-49)
- [ ] 4.24a Casualty ledger core: mark_casualty idempotent, binder page,
      the epilogue reader (Law 7; I27/I28/I29; QA-39, QA-47; A27)
- [ ] 4.24b M1/M2 + H1/H2 with ripples (fire tape offer, the slip, the
      double; QA-40, QA-41)
- [ ] 4.24c V1/V2 + F1/F2 (AUTHENTICATE/final breaker; GET VESS at the
      cascade; the fader; third blind call; QA-42, QA-43) — green bleed +
      post-F2 haunt are CANON-ONLY remainders
- [ ] 4.24d L1/L2 + the rows + ENDING 0 (sixth line; the reading → 4c;
      seats per expired incident; nine cards one name; QA-44/45/46; A28)
- [ ] 4.25 The decision ledger: three entries, Merle watching the pen
      (decision_ledger.gd; finale_started; A17)
- [ ] 4.26a Premiere: cues on the mark, PGM switcher cam_1..3, incidents
      TALLY/HOUSE/BOOM/CARDS with guarantees, fixtures (live_production.gd,
      finale_fixture.gd; I03/I05/I06; QA-27)
- [ ] 4.26b Premiere: sabotage sprint loop, the Vess breaker, pressure, the
      bell ONCE (finale_breaker.gd; Law 5; QA-42 breaker, QA-46 seats)
- [ ] 4.27 The divert, the fader, the last crossing: 75/62/−13 s, folds
      paid, eye dark (Law 11; I19/I24; QA-28, QA-43 F1; P22/P23)
- [ ] 4.28a Endings 1A/1B/2/3/4a/4b/4c/0 + credits + the one interface lie
      (hud.gd _end_*, credits.gd; Law 8, I13; QA-03, QA-28, QA-47; A21–A25)
- [ ] 4.28b ENDING A · AUDIENCE ONLY — CANON-ONLY (reels W1–W3, S2 slips,
      radio dial, program guide, 58 · STILL ON; QA-60, QA-61; needs the v17
      schema policy from 4.SAVE first)
- [ ] 4.29 Achievements with deferral: two flush gates, meta-silence, DEMO
      dark (achievements.gd; I30; QA-04, QA-29, QA-48)
- [ ] 4.30 The DEMO build: seven rooms, demo reasons, S1+S5, whitelist,
      six funnel marks, end card (QA-30, QA-48, DP1–DP5)
- [ ] 4.31 The booth: settings apart from the save, remap with KEY IN USE,
      opens before first play, full accessibility target (options_panel.gd;
      Law 9; QA-01, QA-16, QA-17)
- [ ] 4.32 HUD, binder, captions, pause (hud.gd; glyphs, tally lamp REC ·
      SAFE WHILE LIT, scrim; Law 9; QA-32, QA-34 HUD)
- [ ] 4.33 The map: from Rooms.csv, sealed dashed, BOUND key (map_view.gd;
      QA-15, P15)
- [ ] 4.34 Title + string table: focus ring, FILED once, NEW EPISODE once,
      GameText.csv → StringTable (title.gd; QA-02, QA-04)
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
