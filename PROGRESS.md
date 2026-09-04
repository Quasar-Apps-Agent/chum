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
- [x] 4.0 [CLOUD-OK] ENUMERATE mechanics from the canon docs into boxes here:
      done in ue/PORT-NOTES-MECHANICS.md. 39 built boxes (4.1-4.39) each
      with its reference script (the code is the intent), its knob numbers,
      its save fields, its QA lines, its invariants and its UE home; 16
      RULING boxes (4.R1-4.R16) for canon that was never built; a canon-vs-
      code number table. Asserted by tools/verify_mechanics.py: 73/73
      scripts claimed, QA-01..61 and I01..I31 all assigned, 32/32
      Timings.csv constants homed, boxes here match the notes one to one
      (VERIFY-OK). Per mechanic the plan's order holds: port -> diegetic
      feedback -> fail-forward integration -> automation test
(P3 remainder: the tape half of the loop)
- [ ] 4.1 THE TAPE WORLD: bench monitor + tape stage + Scare 1 (the one
      startle, I14) + gen knob; TBC/photo-safe as material params (A03)
(P4: the hunter's nights, beyond 0.7 / 0.8a)
- [ ] 4.2 THE NOISE BUS: footsteps 6.0 per 0.6 s, doors 8.0, signatures 4.0
      into ReportNoise; hearing loudness x3, 12 s memory; deaf to the dead
      room (I25); the once-per-run line + A08 (QA-13, I22)
- [ ] 4.3 CAMERA FEEDS: rig power/kill/re-patch/sync; kills at 9 m each ON
      AIR, the CHECKER's most-watched first (QA-14 revive, I05). Cone safety
      in the night hunt is NOT in the reference: ruling 4.R2
- [ ] 4.4 THE PATCHBAY: routing v0, two circuits one budget, CONTROL RUN vs
      STAGE HALL, lights + rig power (spike 6 pass line)
- [ ] 4.5 THE NIGHT TRIP: 20 s into Night 1, once per save, rig 0 dies, the
      hummed bar (QA-19, P9)
- [ ] 4.6 THE FLOOR MANAGER: nights on air only; 9 m facing point, 3 s
      watch, > 0.4 m/s spoils, ASSIST hold-E; one point per night; D08;
      honors F1/F2 (QA-19, QA-18)
- [ ] 4.7 THE COVERAGE DIRECTOR: AUDIENCE/CHECKER/SPRINTER/HIDER from
      monitor/move/still seconds (2/4/4), cov_* persisted every 5 s,
      coverage_log reason strings, burn resets; expressed in the hunt (I21)
- [ ] 4.8 THE CASCADE: Night 4, circuit C then B, scrim 0.55/0.75, panel
      stages B before C, window holds waived, liveness log every 5 s,
      warn radius shrinks (QA-20, QA-10, I04, I07, A15)
- [ ] 4.9 DAILIES: canister per capture in 4 stack slots, single carry,
      the degausser burns strike -1 and resets the Director's read (P5)
- [ ] 4.10 THE CASTING SHEET + THE DRESSER: the two physical counters
      (strikes of 4; seven items, loupe last; QA-07, I16, A19)
- [ ] 4.11 THE GLIMPSE: Day 4 unseals the fire corridor; the elbow rect at
      night, 1.8 s, once ever, no achievement (QA-25, I11, I30, Law 3)
- [ ] 4.12 LOCKDOWN + THE ROWS: 4 assets at night; every feed synced;
      exterior doors SEALED FOR BROADCAST; chairs tween to rows; all of it
      re-applied on load (QA-26, I18, A20)
(P5: story gates and the finale)
- [ ] 4.13 KEYS + DOORS: hinges, locked_reason + required_key, HELD FOR AIR
      window doors (waived in cascade), door noise 8.0; EDITH/TRAINING on
      the key board, QUIET ROOM in the shed; the little door (QA-10, I04,
      I08, A16)
- [ ] 4.14 THE PRE-SIGNED PAGE: S4, Day 2+, a TOMORROW signature that costs
      no paper and becomes the respawn (QA-21, I10, A09)
- [ ] 4.15 THE FILM CABINET + THE SEVEN SIGNALS: TRAINING key; six names
      taught; Harriet's note adds the seventh, gated by her death (A07,
      QA-41). Signals as mechanics: ruling 4.R4
- [ ] 4.16 THE VESS CHAIN: the binder (insight), the margin credit, V1 at
      AUTHENTICATE and at the final breaker, V2 GET VESS at the cascade
      panel (QA-42, A11)
- [ ] 4.17 THE CRATE + THE FRAME-SEANCE: Z/X to frame 40, wear 1.5 per
      step, answers at 7/14/21/28/35 with the grief variants, temp
      generation ladder, L1 past five + 70, L2 with the fire tape; seeded
      frames (QA-22, QA-44, QA-50, I19, I20, A14)
- [ ] 4.18 THE FIRE TAPE + THE WAKE: pickup, the forced watch with no
      sting, fire_tape_watched, af_active set once, M1 offered once (QA-23,
      QA-33, QA-40, I15, A13)
- [ ] 4.19 THE SCENE DOCK: six units counted by hand, one random warm,
      nothing follows ever; gates the CARD and D10 (QA-24, I12, I19, A10)
- [ ] 4.20 THE SIGN-OFF ASSETS: VERSE (spectrogram after a capture), CART,
      SCRIPT, CARD (after the dock); the rack; 4-of-4 arms the lockdown
- [ ] 4.21 THE DECISION LEDGER: Day 3+, E cycles, SPACE commits while
      targeted, ink final; Merle to the DOORWAY while the pen is up; sleep
      starts the finale (A17, P14)
- [ ] 4.22 MERLE: kettle/chair/doorway schedule at 1.6 m/s, lines by day
      and decision, the 1974 monologue after the crate (QA-11, QA-40, A12).
      M2 has no code: ruling 4.R11
- [ ] 4.23 HARRIET'S GRAVES + THE REJECTED EDIT: H1 the slip (free signature
      in her hand, then absence), T4.5 played once in full, then the splice
      that mints a daily and doubles her forever; 0.05 tighter screenings
      without her (QA-41, QA-49)
- [ ] 4.24 THE PREMIERE: cues on the mark with PGM cam 1..3, one incident
      at a time every max(14, 26-4*fails) s, fixtures, 40 s club auto-fix,
      tally lie refused twice then F2 on the third blind call, boom held
      once, cue 2 at 45 s per take, the Vess breaker in three variants,
      rows on expiry, the little door by hand; premiere_log (QA-27, QA-43,
      QA-46, QA-51, I03, I05, I06)
- [ ] 4.25 THE FINAL BREAK: 4c if the sign-off completed; the divert gate
      (QUIET ROOM key + 5 answers + fire tape watched); the fader (SPACE
      his hand / E 4.6 s hers; dead FM forces hers); the crossing 75/62/-13
      s to the little door, reached/caught/late (QA-28, QA-43, I19)
- [ ] 4.26 ENDINGS + THE LEDGER READ ALOUD + CREDITS: 3, 2 (lie_pending),
      1A/1B, 4a/4b, 4c, 0; the bell once at the line; every reading; the
      NG+ relic (QA-03, QA-28, QA-45, QA-47, I13, I28, I29, A21-A25, A27,
      A28)
- [ ] 4.27 THE CASUALTY LEDGER: mark_casualty dedupe, page one, every prop
      honoring is_dead (QA-39, I27). Code holds nine of ten deaths: 4.R11
- [ ] 4.28 READABLES D01-D11: five placed props with day/dock gates, six
      sites that mark on use, "N of 10", A26 at ten (QA-59)
- [ ] 4.29 L1 DRIFT: the coat pegs (day-1)/4 + 0.35 at lockdown, three read
      lines (QA-11, QA-56)
(P6: meta, modes, and the shell)
- [ ] 4.30 THE HUD WORLD-TEXT SET: prompt via glyphs, toast, TBC, capture
      line, DAY/NIGHT clock, SHEET n/4, objective ladder, the tally lamp,
      captions, the scrim, [NO ECHO] (QA-34, QA-38)
- [ ] 4.31 THE BINDER: three TAB pages (ledger, presentation form with live
      mode switch); binder IS the inventory (QA-39). Live-time in the
      premiere: ruling 4.R13
- [ ] 4.32 THE BOOTH: volume, sensitivity, fullscreen, TBC, photo-safe,
      text size, captions, ASSIST, five remaps with KEY IN USE refusal;
      first run before the title; settings apart from the log (QA-01,
      QA-16, QA-17)
- [ ] 4.33 THE ACCESS SWITCHES: TBC/photo-safe to the material, captions
      gate, ASSIST (0.35 beat, x1.5 clocks, hold-E stillness at both
      checks), text scale (QA-18, Law 9)
- [ ] 4.34 INTERMISSION: pause holds world/clocks/audio, refused in
      authored sequences, RESUME / BOOTH / RETURN TO TITLE (QA-32)
- [ ] 4.35 THE FACILITY MAP: rooms from the table, station dots, landmarks,
      the player dot + facing, bound key in the footer (QA-15; "sealed
      rooms dashed" has no code yet)
- [ ] 4.36 TITLE + CONTINUE + THE INTERFACE LIE: CONTINUE gated on a log;
      NEW EPISODE once then reverts; FILED stack; first-run booth (QA-02,
      QA-04, I13, Law 8)
- [ ] 4.37 ACHIEVEMENTS: A01-A28 idempotent, flush only at morning or title,
      1 s flag poll, on_ending + A27 for clean hands, off in DEMO (QA-04,
      QA-29, QA-48, I29, I30)
- [ ] 4.38 DEMO MODE: DEMO flag, DemoOpen rooms + door reasons, S1+S5
      paper, save whitelist, funnel file, the sign-alone end card (QA-30,
      QA-48, DP1-DP5)
- [ ] 4.39 THE STRING TABLE + THE GLYPHS: tr() at the chokepoints from
      GameText.csv; E/SPACE/Q/T/M to the bound key everywhere (QA-17)
(RULING boxes: canon the reference never built. The box is the owner's
ruling STRIKE / BUILD / DEFER, per the gap audit; a BUILD lands in the
Godot reference first while it is the live spec. Full text in the notes.)
- [ ] 4.R1 THE BENCH SUB-TOOLS: bake, splice, audio bench, grade, GEN field
- [ ] 4.R2 AVERT + DIRECT SIGHT + cone safety in the night hunt (QA-14's
      first clause fails on the reference; I05 admits it)
- [ ] 4.R3 THE QUIET GAME SEEK: scripted Night 2, unscripted T4.9, the mic
- [ ] 4.R4 THE HAND SIGNALS AS MECHANICS: STRETCH / WRAP / THIRTY / ON TIME
      / CUT / HOLD YOUR APPLAUSE's three seconds
- [ ] 4.R5 THE POWER BUDGET AT BUILDING SCALE (design gap 4: routes, not
      percentages)
- [ ] 4.R6 APPROACHES + GENERATIONS: PRESERVE/ASK/FORCE branches, G1-G3,
      airdate math, the FORCE tools and the imperfect seal
- [ ] 4.R7 THE PRODUCER TRACK: tells, weights, the audition clause (today
      unreachable: the lockdown needs four assets)
- [ ] 4.R8 THE DIRECTOR'S UPPER HALF: blockings B/C, the poisoned well,
      poltergeist staging, the mood law
- [ ] 4.R9 THE TWELVE SCRIPTED SCARES: 2, 3, 4, 11, 12 unbuilt (table in
      the notes); never a new startle
- [ ] 4.R10 PLAYER-OPERATED ARCHITECTURE: the compactus crank, the catwalk
      toll, ladder exposure
- [ ] 4.R11 M2 THE HOME SINGER (or amend the ledger's AS BUILT to nine)
- [ ] 4.R12 THE VERSE VARIANT + other G2 payoffs (HERE for HOME)
- [ ] 4.R13 THE BINDER'S QUEUED RULES: live-time in the premiere (ruled;
      wire with 4.WEB), casting-drift stationery (5.2, review vs Law 8)
- [ ] 4.R14 PHOTO MODE Tier B (ruled; Phase 5 build)
- [ ] 4.R15 AUDIENCE ONLY, the eighth ending (QA-60/61 fail on the
      reference: no W1-W3, no slips, no dial, no STILL ON)
- [ ] 4.R16 THE LEDGER'S NAMED REMAINDERS: the green bleed, the post-F2
      haunt and freeze-check inversion
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
