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
- [x] 0.8b-3 State parity: URestorationSaveGame now carries all 55 v16
      keys in dict order with spec types (Paper TMap seeded S1..S5=3;
      Signatures/Captures/Casualties struct arrays; SeanceWear float;
      LelandAnswers int array) and spec defaults (Mode=1 LATE_NIGHT,
      CurrentTape=1, CarriedId=-1); Save/Load copy the full set (paper
      MERGES on load); Strike() clamp fixed 6->7 (the LOUPE relic). Full
      cross-type round-trip: match=1 (int/float/bool/string/map/struct
      array/int array all survive save->clobber->load); AF contract still
      fires atop the reshaped state. The gameplay functions (§6 tail) are
      0.8b-4
- [x] 0.8b-4 The loop's connective tissue (state functions ported
      verbatim): SetNight day/night driver (morning advances day, tape=
      min(day,5), PROTOTYPE COMPLETE at day>=3); paper economy (PaperFor
      MATINEE=99 else per-station, SignLog decrement + harriet-slip branch,
      SignFinish); RegisterStation + RespawnPoint (Godot offset (0,0.5,1.2)
      mapped to UE (0,1.2,0.5)m — respawn resolved exact); MarkRead,
      HasKey/TakeKey, LogCapture; and the sign->noise->relocate wiring
      (SignFinish broadcasts OnNoise -> ARundown::ReportNoise, deferred to
      the next break as the spec defers it). All verified in one simulate
- [~] 0.8b-5 P3 presentation/NPC half (in progress):
      - [x] Harriet freeze on breaks (AHarriet, IRestorationInteractable):
            sways ON AIR via sin(t*0.9), FREEZES mid-motion on break, holds
            exactly where the cue left her (test: swayA 0.835 -> swayB 1.791
            swaying, frozenC 1.791 held=1); cup rises by the day; prompt
            per phase. H1/H2 casualty flows deferred (UI-heavy)
      - [ ] retake presentation (the strike screen + carried-daily flow)
      - [ ] screening + assist
      - [ ] pawn day/night-driven lighting states
- [x] 0.9 Harness — Phase-0 scope complete (I06/I07 honestly N/A until
      the premiere/cascade port; see 0.9d):
      - [x] 0.9a Invariant parser ported as a test step (tools/
            invariant_parser.py, the SAME coverage rules as
            invariant_parser.gd, exit 0 iff pass) + warn->strike scenario
            (Rundown bTestInvariants: hold tagged target at 6m, pull to
            strike range, clear LOS) run under simulate and fed to the
            parser: I01 warn-precedes-strike PASS (two warn->strike pairs),
            I02 no-strike-thru-wall PASS. Two harness bugs fixed (target
            needed MOVABLE mobility; parser path) — test bugs, not brain
            bugs. I22 only COUNTED this run (no break in 5s)
      - [x] 0.9b Negative test, both halves: (1) parser unit test on
            synthetic logs — THRU-WALL strike -> I02 FAIL x1 exit 1;
            strike with no prior WARN -> I01 FAIL x1 exit 1; clean -> PASS
            exit 0. (2) LIVE: a 3m wall spawned between hunter (0,-1600)
            and prey pulled to strike range — the brain's raycast hit it,
            both strikes logged THRU-WALL, parser ruled I02 FAIL x2 exit 1
            (I01 PASS). Godot parity confirmed: rundown.gd also MARKS thru-
            wall (line 314) and lets the soak catch it — mark-not-gate is
            canon. test_invariants_wall.py is the standing negative fixture
      - [x] 0.9c I22 exercised: the fixture fires ReportNoise near PATCH
            BAY at 3.5s then invokes the break branch directly (the real
            50s flip is outside the window) -> "RELOCATE toward heard noise
            ... -> segment 2", parser I22 PASS (1 attributed). Segment 2 was
            chosen deliberately: from 0 a plain cycle gives 1, so 2 proves
            NEAREST-ANCHOR attribution, not order. One fixture now covers
            I01/I02/I22 in a 5s simulate
      - [x] 0.9d Fail-bot + fail-forward at the retake level: the pinned
            target (test_failbot.py, 15s) is struck to a full sheet; the
            log shows the SAVOR rule engaging at strikes>=3 exactly as
            canon, then RUN ENDED take=4 (full sheet, fail forward), then
            a fresh non-savor warn/strike proving the sheet reset — no
            soft-lock. Parser gained liveness (I07), premiere (I06, the
            verbatim INCIDENT/RESOLVED t<=41 rules) and a clearly-labelled
            UE-R1 full-sheet-ends-run check (PASS live; synthetic negative
            convicted as soft-lock). HONEST SCOPE: canonical I06 measures
            the finale's premiere auto-fix and I07 the cascade — neither
            system is ported yet, so both report N/A, not green; they go
            live with Phase 4/5. Explorer/still bots as real AI pawns are a
            refinement — coverage is already exercised by the fixtures
- [x] 0.8b-6 AUDIT FIXES (High), ported verbatim from the GDScript the
      audit cites: S6 Strike() resolves lost=ITEM_ORDER[items_lost] before
      the increment and broadcasts captured(take, full, lost, respawn) +
      daily_added; S7 SaveToSlot() at the strike (game_state.gd:502); R1
      ReportNoise(pos, loudness) applies _on_noise's four gates (dead room
      deaf, night only, not during premiere, within loudness*3 m) and the
      noise bus passes loudness through; P4 Rita eye 1.60 m (camera Z 72).
      R6/S8 per the audit's own wording: the 3s cooldown, post-strike
      teleport and bInRetake reset are DOCUMENTED as harness stand-ins in
      the headers, removed when 0.8b-5's retake presentation lands. Proven:
      invariants + failbot + state_af — lost items WATCH/PEN/PHOTOGRAPH in
      order, I22 attributed through the gates with a loud test noise, savor
      at >=3, RUN ENDED take=4, I01/I02/I22 PASS, UE-R1 PASS, exit 0.
      THE HARNESS CAUGHT A REGRESSION OF MINE FIRST: a new evidence line
      "STRIKE recorded ..." collided with the parser's STRIKE token (I01
      FAIL x4, a false soft-lock) — renamed to RETAKE, guard comment added
- [x] 0.10 PHASE GATE: parity slice — one room, Chum encounter, saves,
      QA subset green, THE-LAWS spot-audit, captured & reviewed — OPENED BY
      OWNER RULING 2026-09-05 (ue/GATE-0.10.md §5): spot-audit accepted as
      drafted; scale 3.35 m / eye 3 m; stage deltas stripped; LAW 9 -> Phase
      4 UI. The 3 High audit drifts are 0.8b-6 above, not carried silently
      - [x] PACKAGE ASSEMBLED, REVIEWED — ue/GATE-0.10.md
            (clause map + 11-law spot-audit, LAW 9 flagged), ue/GATE-0.10-
            EVIDENCE.md (all 9 fixtures re-run at HEAD, verbatim lines),
            renders/gate_0.10_greybox_chum{,_back}.png (scale-true puppet
            in the stamped TAPE LIBRARY with the S1 marker and the SEALED
            door text visible). The box above is the OWNER'S to tick

## CLOUD LANE BACKLOG — [CLOUD-OK] units (Linux, repo only; see plan rule 0)
Cloud routines take the FIRST unclaimed box here, on branch
`cloud/<id>-<slug>`, as a draft PR, ONE deliverable file each. The Mac
lane merges green PRs at session start and ticks these boxes. Ordered by
what the Mac lane needs soonest. Every unit: cite the canon doc+section
for each rule asserted; where canon is silent write OPEN, never invent.
- [x] C17 [CLOUD-OK] (merged PR #15) PORT AUDIT: diff the UE C++ (ue/Restoration/Source/
      Restoration/*.h,.cpp) against scripts/game_state.gd, rundown.gd,
      harriet.gd, player.gd, bench/capture scripts — every constant,
      default, order-of-effects and signal; list drift as a checklist like
      ue/PORT-NOTES-STATE.md §6 did. Deliverable: ue/PORT-AUDIT-1.md
- [x] C8 [CLOUD-OK] (merged PR #16) PORT-NOTES BROADCAST: transcribe scripts/broadcast.gd +
      coverage_director.gd (ON AIR/BREAK clock surface, window holds,
      coverage labels cov_monitor/move/still, every signal + listener).
      Deliverable: ue/PORT-NOTES-BROADCAST.md
- [x] C9 [CLOUD-OK] (merged PR #17) PORT-NOTES RETAKE: the retake presentation + dailies
      (game_state pick_daily/burn_daily/mint_shortcut_daily, carried_id/
      take, the retake screen script, toasts verbatim, timings).
      Deliverable: ue/PORT-NOTES-RETAKE.md
- [x] C10 [CLOUD-OK] (merged PR #18) PORT-NOTES SCREENING: screening + assist + Merle
      (screening_active/done, merle.gd, assist rule, Day-1 flow).
      Deliverable: ue/PORT-NOTES-SCREENING.md
- [x] C11 [CLOUD-OK] (merged PR #19) PORT-NOTES FINALE: premiere incidents (INCIDENT/
      RESOLVED t=, the 41s club auto-fix rule = I06), cascade + liveness
      (I07), start_finale/mark_ending/endings, LOCKDOWN. Deliverable:
      ue/PORT-NOTES-FINALE.md — makes I06/I07 implementable
- [x] C2 [CLOUD-OK] (merged PR #20) CAST DOSSIER: per character from docs/canon cast plates
      + walkthrough + chum motion & sound: silhouette, materials, scale
      truth, motion hooks, rooms, beats, LAW constraints (LAW 4 warm one,
      LAW 5 silence, LAW 7 signatures). Deliverable: docs/production/
      CAST-DOSSIER.md
- [x] C6 [CLOUD-OK] (merged PR #21) PROP MANIFEST from restoration-object-taxonomy.md +
      room bible + ambient lore ledger: every prop, taxonomy class, room(s),
      interactable?, real-world dims (scale truth), CC0/Fab source
      candidate. Deliverable: docs/production/PROP-MANIFEST.md (+ .csv)
- [x] C3 [CLOUD-OK] (merged PR #22) ROOM BRIEFS 3.6–3.10 (format: docs/production/
      ROOM-BRIEFS-3.1-3.5.md once it lands; else the room bible + lighting
      bible + taxonomy + lore ledger). Deliverable: docs/production/
      ROOM-BRIEFS-3.6-3.10.md
- [ ] C4 [CLOUD-OK] ROOM BRIEFS 3.11–3.15. Deliverable: docs/production/
      ROOM-BRIEFS-3.11-3.15.md
- [ ] C5 [CLOUD-OK] ROOM BRIEFS 3.16–3.20. Deliverable: docs/production/
      ROOM-BRIEFS-3.16-3.20.md
- [ ] C18 [CLOUD-OK] LIGHTING DATA: restoration-lighting-bible.md → per-room
      locked EV / state (red=watched=safe) / practical list / transition
      rule as data. Deliverable: ue/Restoration/Data/Lighting.csv + a
      README paragraph in the PR body explaining columns. NOTE (from
      docs/production/ROOM-BRIEFS-3.1-3.5.md §0): NO EV, kelvin or candela
      value exists anywhere in canon, and world_builder.gd contradicts the
      bible at night (×0.56 brown-out vs OFF). Do NOT invent numbers: ship
      the STRUCTURE (room × state × practical × red-reads × transition)
      with every numeric cell marked STAND-IN or OPEN and cite the stand-
      in's source; put the ruling list in the PR body
- [ ] C7 [CLOUD-OK] LANDMARKS TABLE: extract every landmark/interactable
      spawn from scripts/world_builder.gd (name, room, x,z, kind, script)
      into ue/Restoration/Data/Landmarks.csv and extend tools/
      extract_data.py deterministically (row count asserted in the PR)
- [ ] C12 [CLOUD-OK] GAMETEXT AUDIT: the 714 keys → class (UI/caption/
      toast/lore/achievement), glyph-substitution map, LAW 5 check (no
      Chum presence/achievement string), localization readiness.
      Deliverable: docs/production/GAMETEXT-AUDIT.md
- [ ] C13 [CLOUD-OK] QA-51 EXECUTABLE: each of the 51 QA items → the
      fixture/capture/inspection that proves it in UE, or OPEN.
      Deliverable: docs/production/QA-51-EXECUTABLE.md
- [ ] C14 [CLOUD-OK] ACHIEVEMENTS + PRESENCE AUDIT vs LAW 3/5 (ONCE EVER
      never referenced; Chum has no title/presence). Deliverable:
      docs/production/ACHIEVEMENTS-AND-PRESENCE-AUDIT.md
- [ ] C15 [CLOUD-OK] SOUND MANIFEST: every sound event in chum motion &
      sound + dread doctrine + room bible; the bell-never-sounds rule;
      CC0/Fab source candidates with licenses. Deliverable:
      docs/production/SOUND-MANIFEST.md
- [ ] C16 [CLOUD-OK] STREAMER MODE + CLIP LEDGER + TAPE 1 DEMO SPEC from
      restoration-comparative-study.md adoptions (units 5.6–5.8), as
      implementable UE specs. Deliverable: docs/production/
      STREAMER-CLIP-DEMO-SPEC.md
- [ ] C1 [MAC] = unit 4.0 below (Phase 4 mechanics enumeration). CLOUD:
      SKIP — six drafts already exist on the old routine's branches (PRs
      #9–#14, pre-lane era); the Mac lane picks the best one and splices
      its boxes into PHASE 4. Not a cloud unit any more

## PHASE 1 — After-Fire Chum (Blender factory → UE acceptance)
OWNER RULINGS 2026-09-05 (bind every unit below): (1) SCALE — author the
puppet at the TRUE 3.35 m body with the tally eye at 3.0 m, actor scale
1.0, one uniform scale frozen before export, never per-bone (resolves
CHUM-RIG-AND-ANIMATION-SPEC OPEN-1 and PHASE1-CHUM-BUILD-BRIEF §1.7).
(2) STRIP the two stage-puppet deltas (flannel, leather patches) from the
MASCOT; the plate after-fire-chum-dossier.png is the mascot's canon, not
the stage tell-table (PHASE1-CHUM-BUILD-BRIEF §0.5).
- [ ] 1.1 Torso: quilted patchwork, seams, char zones, 2048 bake — at
      3.35 m; NO flannel, NO leather patches (owner ruling: stripped)
      - [x] 1.1a GEOMETRY + SCALE (evidence docs/telemetry/blender-phase1/
            1.1a_*.png): tools/fetch_scans.py + 10 CC0 scans (Poly Haven /
            AmbientCG, 2K, credited, gitignored as re-fetchable); FINAL_SCALE
            3.35/2.6 applied and FROZEN before the bake (tallest point 4.00
            m = ear tips; body 3.35); BodyCore at voxel 0.02 + smooth pass
            (no facets) with the PLATE's forward-belly slump; belly rebuilt
            as an EMBEDDED 20 mm panel (boolean of the proud body — no egg);
            seven patches as SOLID booleaned mass (rust, olive, navy, ochre,
            2 brown, plaid — shells GONE; flannel + leather STRIPPED per
            ruling); bakes on wool_boucle/corduroy/denim/plaid; island
            margin 0.03; beauty rig rescaled (+0.73 EV). HONEST VERDICT:
            the QUILT DOES NOT READ — 3000 fur cards + 3600 post-bake guides
            bury every patch and the scorch layer darkens them to the body's
            tone; plaid + brownA are BURIED under the belly panel (my
            placement: inside its footprint, 14 mm proud vs 20); stitch
            cylinders read as pipes. 1.1 stays unticked
      - [ ] 1.1b THE QUILT MUST READ: fur cards to singed rims on the
            shoulder/hip crests only (900, 20–40 mm); post-bake body hair
            masked off the front; patch/belly scorch 0.5→0.2 and tints up so
            rust/olive/navy/plaid identify in the beauty; move the two
            buried patches off the belly; then seams-to-maps + delete the
            sring/stt stitch cylinders; char zones (bark/rustleak); UE
            export + locked-EV capture; sodium + beauty re-judged
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
- [ ] 4.ACCESS LAW 9 — implement docs/production/UE-ACCESS-SPEC-LAW9.md
      (booth, captions, assist, remap, pause, the achievement deferral
      rule) with the Phase 4 UI. OWNER RULING 2026-09-05: here, not before
      the gate. Its 12 GATE RULING NEEDED items are this unit's first step
- [ ] 4.0 [CLOUD-OK] ENUMERATE mechanics from the canon docs into boxes here
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
