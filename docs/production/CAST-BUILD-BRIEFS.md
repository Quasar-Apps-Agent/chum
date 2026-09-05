# PHASE 2 · THE CAST · BUILD BRIEFS AND RIG SPECS (units 2.2 – 2.8, plus the non-box cast)

Prep deliverable for the Mac lane (PLAN §0 SUBAGENT LANE: one output file, no
tracker edits, no git). One brief per character in the cast dossier, in the
PROGRESS Phase 2 unit order, each written so the build agent can model, rig and
accept the character in Blender and Unreal Engine 5.8 without re-reading the
canon. Every canon claim carries its document and section. Where canon is
silent the cell says **OPEN** and nothing is invented to fill it. After-Fire
Chum is excluded by instruction: his brief is P1 and his rig is RIG (§0.1).

Roster covered (every entry the dossier lists, none added): Merle Cottry ·
Harriet · Vess Keys · Leland Merrick · Rita Ivori · The Floor Manager · Chum,
1974 stage puppet · Chum, 1971 pilot · Chum, post-fire stage puppet and the 4K
premiere body · the Understudy / the once-ever corridor figure · Ansel Craik ·
the 58 Club rows and extras [DOSSIER §1 ROSTER].

---

## 0 · STANDING RULES THAT BIND EVERY CHARACTER

### 0.1 Sources of record (short names used below)

| Key | Path |
|---|---|
| DOSSIER | `docs/production/CAST-DOSSIER.md` (the cloud lane's per-character dossier; §7 conflicts C-1..C-15 and §8 OPEN-1..18 are inherited here by number) |
| P1 | `docs/production/PHASE1-CHUM-BUILD-BRIEF.md` (format precedent; §0.2 asset policy, §0.3 Blender doctrine) |
| RIG | `docs/production/CHUM-RIG-AND-ANIMATION-SPEC.md` (format precedent; §1.3 bone conventions, §3 drive plan) |
| PLAN | `AAA_BUILD_PLAN.md` (§R realism bar, §1 doctrine, §2 asset policy, §4 verification loop, §5 Phase 2) |
| PROGRESS | `PROGRESS.md` (§PHASE 2 unit order; 0.8b-1 ARitaCharacter; 0.8b-5 AHarriet) |
| PIPE | `docs/canon/restoration-blender-ue5-pipeline.md`; PIPE-PROD = `docs/production/restoration-blender-ue5-pipeline.md` (adds ADDENDUM · ANIMATION EXPORT) |
| LAWS | `docs/packet/portbrief/THE-LAWS.md` |
| SHEETS | `docs/canon/restoration-cast-sheets.md` |
| PLATE-RITA / -MERLE / -HARRIET / -VESS / -LELAND | `docs/canon/art/cast-rita-ivori.png`, `cast-merle-cottry.png`, `cast-harriet.png`, `cast-vess-keys.png`, `cast-leland-merrick.png` (viewed for this brief) |
| DESIGN | `docs/canon/restoration-design-doc.md` |
| WALK | `docs/canon/restoration-walkthrough-levels-endings.md` |
| MASTER | `docs/canon/restoration-game-master.md` |
| CASUALTY | `docs/canon/restoration-casualty-ledger.md` |
| DREAD | `docs/canon/restoration-dread-doctrine.md` |
| MOTION | `docs/canon/restoration-chum-motion-and-sound.md` |
| AF | `docs/canon/restoration-after-fire-chum.md` |
| REACT | `docs/canon/restoration-reaction-matrix.md` |
| ROOMS / INVENTORY / AMBIENT / LORE / LIGHT | `docs/canon/restoration-room-bible.md`, `restoration-room-inventory.md`, `restoration-ambient-lore-ledger.md`, `restoration-lore-architecture.md`, `restoration-lighting-bible.md` |
| ART / AUDIO / FABRIC / CASTING / PROPS / ACH / QA / KEYART / ACCESS | `docs/production/restoration-art-bible.md`, `restoration-audio-bible.md`, `restoration-puppet-fabrication-brief.md`, `restoration-merle-casting-breakdown.md`, `restoration-props-packet.md`, `restoration-achievements-design.md`, `restoration-qa-regression.md`, `restoration-key-art-brief.md`, `UE-ACCESS-SPEC-LAW9.md` |
| KIT / HARRIET.gd / MERLE.gd / VESS.gd / FM.gd / STAGE.gd / GLIMPSE.gd / DOCK.gd / WB | `scripts/character_kit.gd`, `harriet.gd`, `merle.gd`, `vess.gd`, `floor_manager.gd`, `tape_stage.gd`, `glimpse.gd`, `dock_chum.gd`, `world_builder.gd` (the Godot reference: "the code is the intent", PLAN §1 quoting `docs/packet/portbrief/PORT-BRIEF.md`) |
| HARRIET.h/.cpp, RITA.h/.cpp, CLOCK.h, STATE.h | `ue/Restoration/Source/Restoration/Harriet.h`, `Harriet.cpp`, `RitaCharacter.h`, `RitaCharacter.cpp`, `RestorationClock.h`, `RestorationState.h` |
| TIMINGS | `ue/Restoration/Data/Timings.csv` |
| BUILD-1974 / BUILD-1971 / BUILD-AF | `tools/build_chum_1974.py`, `tools/build_chum_1971.py`, `tools/build_chum_af.py` |
| CREDITS | `tools/texsrc/CREDITS.md`, `ue/CREDITS-FAB.md` |

### 0.2 The owner rulings of 2026-09-05 (bind every unit below)

| Ruling | Consequence in this brief |
|---|---|
| Every character is authored at its TRUE canon height with actor scale 1.0; ONE uniform scale applied and frozen in Blender before export; never per-bone; no runtime bone scaling | Every §(4) rig below has actor scale 1.0 and a frozen build scale. The Understudy's "+4 %" [ART §6] is a SEPARATE frozen export, never a runtime scale. Harriet's H2 double is a second actor instance, never a scaled bone. Merle's KIT `rig.scale`, Vess's `(0.95, 1.07, 0.95)`, Leland's `(0.97, 1.06, 0.97)` and the FM's `(1.0, 1.08, 1.0)` [KIT 729, 776, 823] are reference-only proportions and are NOT carried as scale into UE. |
| Where canon states no height, write OPEN with the plate-derived estimate clearly labelled as an estimate | "**No canon height exists for any human**" [DOSSIER §0.4, citing ART §6]. Every human §(3) carries a HEIGHT row: canon = OPEN, plate estimate = a number derived by this brief from the plate's visible proportions and labelled ESTIMATE, reference = the KIT arithmetic. The estimate is a placeholder for authoring, not canon. |

### 0.3 The realism bar and the render language (PLAN §R, ART §1, §6; read before modelling any human)

- "The ACCEPTANCE VIEW is the in-engine Unreal capture … Blender Cycles renders are design tools only" [PLAN §R]. §R.1 no naked primitives; §R.2 detail < 2 cm lives in maps ("teeth yes, threads no"); §R.3 every surface breaks light three ways; §R.5 scale-truth at gameplay distance AND 1 m; §R.6 motion passes "anticipation/ease/follow-through … no pops"; §R.7 "Crafted, not photoreal … photoreal humans are not the goal, lying materials are the defect" [PLAN §R.1–7].
- "Humans are needle-felt and cloth figures over armature" [ART §1]. "Humans: needle-felt heads over wire armature, cloth bodies, mitten hands with stitched finger definition reserved for principals (Merle, Vess, Harriet). Head-to-body one to five and a half. EYE HIERARCHY, a hard law: human figures wear glass beads or embroidered eyes only; buttons are reserved for Chum. A button on a human face is an event we never spend" [ART §6]. "Humans are crafted figures in the same language, cloth and needle-felt over armature" [DESIGN Part II · The Two Render Worlds]. "the in-game figure is a crafted needle-felt build and is NOT the performer's likeness" [CASTING header].
- The plates are photographs and are "the source of record for likeness, wardrobe, props and turnaround"; the render doctrine is the source of record for MATERIAL; the tension is **OPEN-1** for unit 2.1 [DOSSIER §0.3]. This brief writes every human as a crafted figure (ART is later, named canon; PLAN §R.7 agrees) and records what changes if 2.1 rules MetaHuman: the material tables, not the rigs or the motion.
- A consequence the Mac lane must see before modelling: at 1 : 5.5 head-to-body [ART §6] and a true height of ~1.6 m, the head is ~0.29 m tall. The plates are ~1 : 7.5. Authoring at true height with the crafted ratio is the owner's ruling read literally; the head size that results is logged as **OPEN-C1** (§SUMMARY) so it is chosen, not discovered.
- The sodium check binds every fibre: `tools/sodium_check.py --subject` on the character's own mesh ("on foreign ball UVs their empty bake margins read as black glass", SODIUM docstring; P1 §0.3) before every export; "If it lies under sodium it does not ship" [PIPE §MATERIAL MASTERS].
- BANNED: thin shrinkwrapped shells ("they collapse — solid geometry only", PLAN §1; the giraffe artifact, P1 §0.3). Cardigans, aprons, collars and patches are solid, remeshed geometry or true cloth simulated to rest and then frozen, never a shrinkwrapped plane.
- Wardrobe drift [ART §4–5] is a material-instance parameter, never a mesh swap: `MI_<Char>_<Garment>` carries a `Drift` scalar 0..1 that interpolates neutral → show palette (MUSTARD #C9A33D, AVOCADO #6B7D3B, BURNT #B35A2B) on the coat-peg curve. Per-character rule in each §(3).

### 0.4 Asset policy and verification (P1 §0.2, PLAN §2, §4)

- CC0: Poly Haven (`api.polyhaven.com/assets?t=textures|models`) and AmbientCG (`ambientcg.com/api/v2/full_json`, User-Agent required). **Every id in the tables below was read from those two endpoints on 2026-09-05** (856 Poly Haven textures, 521 models; 2009 AmbientCG materials). Where a table says "none on either API (checked)" the keyword sweep returned nothing usable; the Fab search term is the fallback. Fab entries are SEARCH TERMS confirmed in Window→Fab, never ids [P1 §0.2; `ue/FAB-IMPORT.md`]; every pull gets a line in `ue/CREDITS-FAB.md`.
- Already in hand (do not re-download): Fabric031, Fabric030, Leather030, Metal058A (AmbientCG), Camera_01 (Poly Haven), `fur_tuft_atlas.png` [CREDITS; P1 §0.7].
- The loop, verbatim order [PLAN §4; P1 §0.6]: Blender rebuild → Cycles/EEVEE design render → UE import (headless) → UE look-dev capture (ACCEPTANCE) → automation tests → tick → ledger. Sodium `--subject` before step 3 for every material unit; animation units: "capture sequences (≥8 frames or MRQ clip), review motion".
- Textures: ORM packed; 2K default; 4K only for Chum and the readables [PIPE §STANDARDS] — so the humans are 2K; the legal pad, run sheet, clipboard form, Vess's binder pages are readables and may take 4K.

### 0.5 Naming, coordinates, the shared skeleton (proposals where marked)

- Canon prefix law: `SM_`/`SK_`, `M_`/`MI_`, `T_*_BC/_N/_ORM`, `UCX_`, `SOCKET_*` [PIPE §STANDARDS]. Names below are **proposed, not canon** (DOSSIER §0.5, OPEN-2): `SK_Merle`, `SK_Harriet`, `SK_Vess`, `SK_Leland`, `SK_Rita_Hands`, `SK_Rita_Reflect`, `SK_FloorManager`, `SM_Chum_1974`, `SM_Chum_1971`, `SK_Chum_Stage` (PIPE-PROD names this one), `SM_Chum_PostFire_Stage`, `SK_Chum_4K`, `SK_Extra_A..`. The once-ever corridor actor's name is OPEN-15 (LAW 3: "Its name appears in no code file").
- Units: metres in Blender, 1 m = 100 uu, verified on the cube (PROGRESS 0.2); UE X-forward Z-up; Blender build front −Y as BUILD-AF does [RIG §1.1]. Plan mapping UE (X, Y, Z) uu = (Godot x, Godot z, Godot y) × 100 [DOSSIER §0.4]. Rita's eye: UE 148 uu (`RitaCharacter.cpp` 31: camera Z 72 over the 88 half-height capsule) vs Godot 1.6 m — OPEN 0-B inherited; PROGRESS 0.8b-6 item P4 moves UE to 1.60 m.
- Bone names are CHARACTER-relative (`_l` = the character's own left), the UE convention [RIG §1.3]. Front is −Y in the build, so viewer-right = +X = character LEFT; plate text says viewer-left/right; the mapping is stated per rig.
- **Proposed: one shared human skeleton `SKEL_Cast_Human`** so unit 2.9's clips (the busy-hands set, the seated freeze, the signals, the rows' applause) retarget without work: `root, pelvis, spine_01, spine_02, spine_03, neck_01, head, clavicle_l/r, upperarm_l/r, lowerarm_l/r, hand_l/r, thumb_01/02_l/r, fingers_l/r (ONE bone for the four-finger mitten mass), thigh_l/r, calf_l/r, foot_l/r, ball_l/r` plus per-character prop bones (§(4) of each). Mitten hands are canon [ART §6]: fingers do not articulate; "stitched finger definition" is a normal/albedo map on principals (PLAN §R.2 "threads no"). Grips (towel, cup, pad, run sheet, clipboard) are thumb-plus-mitten-curl, and the prop rides its own bone.
- Eyes: glass-bead eyes are a rigid sphere pair on `eye_l/r` bones (aim allowed, small); embroidered eyes are a map on the head and do not move [ART §6]. No eyelids, no blink, no mouth phonemes on any human (needle-felt heads do not articulate; nothing in canon asks them to). Speech is delivered by voice and body, never by lip-sync — a lip-synced felt face would be a lying material [PLAN §R.7].

### 0.6 The LAW matrix as it lands on the rigs

| LAW | Text (short) | Where it binds a rig below |
|---|---|---|
| 2 ONE STARTLE | "The in-tape lunge is the game's single jump scare. Nothing else lunges, stings, or pops" | Chum 1974 stage rig owns the ONE lunge (§7); FM never pops (§6B); the corridor figure has no sting (§10) |
| 3 ONCE, EVER | the Day 4 fire-corridor moment "is never referenced again by any system … Its name appears in no code file" | §10: the actor, its asset and its flag must carry a name that says nothing |
| 4 THE WARM ONE NEVER ACTS | "On camera, off camera, in any ending. Nothing follows filing it. No system may contradict this, including audio" | §7/§8: the dock units are STATIC MESHES with no skeleton, no physics, no audio component; the warm one is a state flag on `DockTask`, not on the mesh |
| 5 SILENCE CONTRACTS | "The bell rings once, at the finale beat, and its caption says so. Chum's bell is otherwise silent; Chum speaks nowhere; Chum has no account, no achievement title, no presence string" | Every Chum `bell` bone locked except one authored finale key on the stage rig (§7); dock SMs have no bell articulation at all; no Chum asset name carries "Chum" into an achievement or presence string (asset names are not titles; ACH §DOCTRINE 2) |
| 6 THE SCHEDULE IS REAL | "Harriet freezes on breaks; window holds bind except during cascade" | §3: the freeze is a hard stop of the whole animation graph on `!Clock->IsOnAir()`, already in `Harriet.cpp` |
| 7 EVERY DEATH HAS A SIGNATURE | "the house idiom is the broadcast-body (splice, interlace, dropout, leader where a voice was)" | Each human §(4) carries its two death presentations as rig states (M1/M2, H1/H2, V1/V2, F1/F2, L1/L2) and THE ROWS (§12); none is an achievement (CASUALTY §THE FULL BOARD) |
| 8 ONE LIE | ending 2 post-credits only | §9: the 4K body is the one clean image; nothing else on the cast may render clean on tape |
| 9 ACCESS IS CANON | captions, assist, remap | every sound a character makes carries a parity caption [ACCESS §3.2]; the FM's watch honours assist-hold [ACCESS §5.2] |

---

## 1 · MERLE COTTRY · PRESIDENT. COOK. CARETAKER. (unit 2.2)

### 1.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Who | "Late 60s, the 58 Club matriarch, occupation: everything. Voice warm, folksy, unhurried; hands never still: towel, spoon, mug, or someone else's sleeve … NEW CANON: MERLE FOUNDED THE CLUB WITH LELAND … burying the truth is grief's custodianship, never menace; the never-sinister rule survives untouched" | SHEETS §MERLE |
| The one law | "Warm-genuine, never warm-sinister. There is no twist in this performance … If the warmth can curdle, it is the wrong warmth" | CASTING §THE ONE LAW |
| Never the trap | "The comfort is never the trap. No scare is ever delivered through Merle's warmth, the kitchen, or an act of kindness" | WALK Part IV · The Rules |
| Physical vocabulary | "Merle's hands stay busy with domestic objects; when they still, listen" | MASTER header |
| The pen-up silence | "forty-five seconds of watching someone sign a document, hands empty and open, saying nothing … the in-game figure holds this pose at the game's decision point, and the reference footage drives it" | CASTING §THE CALLBACK; MASTER T5.2 "Merle in the doorway, hands empty, watching the pen, saying nothing" |
| 1974 | "(her hands, for once, empty and open) And then the dark got warmer" | MASTER T4.6 |
| Wardrobe | "MERLE: begins already warm (mustard apron from Day 1) and never drifts, because she was carried in 1974 and has nothing left to drift toward; her constancy is the tell hiding in plain sight" | ART §5 (vs DESIGN Part I · Merle "her wardrobe migrates" — DOSSIER §7 C-2, unresolved) |
| Dread | "WARMTH: Merle makes Chum scarier … the kettle's warmth is load-bearing dread infrastructure, which is why its click-off is a death beat" | DREAD §AMPLIFIERS |
| LAWS that bind her | LAW 7 (M1, M2; CASUALTY §MERLE). LAW 4 does NOT name her: "THE WARM ONE" is the warm dock unit [DOSSIER §3; WALK Part III.6] — a build note, because a rig named for warmth will be confused with the law. | LAWS 4, 7; DOSSIER §3 |
| Never-stated | "What Merle knows and buried. The mechanism of carrying." No prop, pose or caption on her may state either | LORE §THE NEVER-STATED LEDGER |
| Reaction | "M-R4: she never says his name after the fire tape exists" (QUEUE); "M-R5: she retires the second teacup from the rack" (QUEUE) | REACT §MERLE |

### 1.2 WHAT EXISTS

| Item | State | Source |
|---|---|---|
| Godot brain | `Merle` (Interactable): schedule KETTLE (8.0, 0, −1.0) by day, CHAIR (2.6, 0, 1.2) night/lockdown, (0.4, 0, 1.4) during a screening, DOORWAY (6.0, 0, −16.4) when the pen is up; `SPEED 1.6` m/s `move_toward`; monologue as seven toasts at 3.2/3.4/3.2/3.2/3.0/3.4 s; hidden when dead | MERLE.gd 6–24, 44–82; TIMINGS `merle.gd SPEED 1.6` |
| Godot figure | `CharacterKit.merle()`: `_body_base` + floral apron (bib, fall, tie, pocket), red-thread 58 box, maroon `_cardigan`, both arms "folded" with a towel box between, glasses-chain beads + two torus rims, enamel pin sphere, head at (0, 1.46, 0) with `bun_messy`, coin pendant; stylised low-poly, all primitives | KIT 632–680 (header: "stylized low-poly humans") |
| Placement | spawned at (8.0, 0, −1.0) with a 0.3 × 1.6 capsule → UE (800, −100, 0) KITCHEN | WB 1060–1078; DOSSIER §5 |
| UE | nothing: no `AMerle`, no mesh. The decision ledger's `is_pen_up()` (group `decision_ledger`) is not ported (Phase 4) | PROGRESS Phase 2/4 |
| Sodium verdict | none run; the reference figure is programmer art by its own comment and fails §R.1 by construction | KIT header; PLAN §R.1 |

### 1.3 BUILD BRIEF

**Silhouette and proportions (from PLATE-MERLE, read as a costume reference for a crafted figure).** A stout woman; three-quarter framing, hands at the waist wringing a striped tea towel; maroon cable-knit cardigan open over a cream floral blouse and a cream floral bib apron with a stitched maroon **58** on the bib; a small round pendant on a fine chain at the sternum; grey-brown hair in a loose high bun with strands escaping; turnaround left profile / back / right profile (the back shows the apron tie bow at the waist and the cardigan's cable ribs) [PLATE-MERLE; DOSSIER §2.2]. Not on the plate: the beaded glasses chain and a separate enamel pin that DESIGN gives her (OPEN-9).

| Measure | Value | Status |
|---|---|---|
| Height | canon: **OPEN-3-class (none stated)**. Reference KIT ≈ 1.6 m (head centre 1.46 + skull) [DOSSIER §2.2]. **ESTIMATE from the plate: ~1.58 m** (stout, short-necked; head ~1/7 of a body that the apron fall implies ends ~0.45 m below the frame) — a placeholder, not canon | OPEN (owner) |
| Head-to-body | 1 : 5.5 → head ≈ 0.29 m on a 1.58 m figure (OPEN-C1) | ART §6 |
| Capsule (UE) | radius 30 uu, half-height 80 uu (from the 0.3 × 1.6 reference) | WB 1063–1067 |
| Hands | mitten with stitched finger definition (principal) | ART §6 |
| Eyes | glass bead or embroidered; never buttons | ART §6 |

**Materials (verified CC0 candidates; tints from KIT are reference only).**

| Need | Candidate (id · source · licence) | How |
|---|---|---|
| Cable-knit cardigan, maroon | `knitted_fleece` (brown knit, 266×270 mm) · Poly Haven · CC0 as the knit ground; `wool_boucle` (looped wool, 314×390 mm) · Poly Haven · CC0 for loft at the cuffs and hem. **No cable-knit scan exists on either API (checked).** The cable ropes are silhouette (>2 cm) and are modelled: a repeating cable strand as a bevelled curve pair, arrayed on the sleeve and front panels, remeshed into the garment (solid, never a shell), then the knit scan box-projected at 1:1 mm | tint to the maroon reference (0.31, 0.11, 0.11) [KIT 636]; Fab: "cable knit", "chunky knit sweater", "wool knit" |
| Floral blouse and floral apron, cream | ground: `cotton_jersey` (beige, ribbed cotton, 263 mm) · Poly Haven · CC0 or `Fabric001` (old white cloth) · AmbientCG · CC0; print: **no small-floral cotton print exists on either API (checked)** — author the print as a tileable albedo in Blender (painted or procedural rosettes on cream), and take print relief from `Fabric081C` (plastisol printed white) · AmbientCG · CC0; embossed alternative `floral_jacquard` (dark floral, 252×383 mm) · Poly Haven · CC0 | two different florals (blouse small, apron larger) as the plate shows; Fab: "floral cotton", "calico", "vintage floral fabric" |
| Tea towel, red stripe | `Fabric006` (red stripes, white) · AmbientCG · CC0 over `rough_linen` (blue linen crosshatch, tint to cream) · Poly Haven · CC0; `fabric_pattern_05` (windowpane plaid towel, 500 mm) · Poly Haven · CC0 as an alternate weave | the towel is a real cloth mesh simulated to the wrung pose and frozen |
| The stitched 58 | embroidery: a normal + albedo decal on the apron bib (threads < 2 cm → maps, PLAN §R.2); thread height from `Rope001` (string) · AmbientCG · CC0 as the stitch normal source | maroon thread |
| Needle-felt head and hands | `Fabric034` (felt, grey/white) · AmbientCG · CC0 as the felt fibre normal/roughness, tinted to the plate's warm skin; `polar_fleece` (cream fleece) · Poly Haven · CC0 for the fuzz halo at silhouette edges (cards, sparse) | "needle-felt heads" [ART §6]; the felt reads as felt under sodium or it fails |
| Hair, grey-brown bun | felted wool, not strands: `caban` (orange fleece, fibrous) · Poly Haven · CC0 tinted grey-brown for the bun mass; escaping strands as a few wool-yarn curves wearing `Rope001` | hair is part of the felt head |
| Pendant and chain | `Metal042B` (dirty gold) · AmbientCG · CC0; chain as a map on a thin strip | plate: small round pendant |
| Reading glasses on a beaded chain (OPEN-9) | `round_spectacles` · Poly Haven · CC0 (model donor, cut the rims); beads `Metal042B` | build only if OPEN-9 rules them in |
| Enamel Chum pin (OPEN-9) | `M_Enamel` master [PIPE §MATERIAL MASTERS] | the club's enamel pins share this master; Vess's plastic one does not (§4) |
| Shoes | not on the plate | OPEN (dressing) |

**Drift.** `MI_Merle_*` `Drift` is pinned: ART §5 "never drifts"; DESIGN says the opposite (C-2). Build the parameter, set it to 1.0 ("begins already warm") and leave the curve unwired until the owner rules C-2. The apron's cream floral on the plate vs ART's "mustard apron" is the same conflict.

**Blender steps.**
1. Block the figure on `SKEL_Cast_Human` proportions at the ESTIMATE height (1.58 m) with the 1 : 5.5 head; flag OPEN-C1 in the ledger the first time the head is seen beside the plate.
2. Body: a stuffed-cloth torso (solid remesh, voxel 0.01) with the blouse as the body's own surface; apron as a separate solid (bib + fall + tie, cloth-simulated to rest over the torso, then remeshed solid, 6–8 mm thick); cardigan as a third solid with modelled cable strands (voxel 0.006 on the cables) — the three layers must never interpenetrate at the shoulders on the back view.
3. Head: needle-felt sculpt at 1 : 5.5, soft features ("warm, lined, smiling-eyed", KIT 675), bead eyes on `eye_l/r`, felt bun; no mouth cavity, no teeth (a felt head has neither).
4. Hands: mitten sculpts with the stitched finger lines baked as normal + darker albedo; thumb separate.
5. The towel: cloth sim between the two mittens to the wrung pose; freeze; skin to `prop_towel` (§1.4).
6. Bakes at 2K per material group (Cardigan, Blouse, Apron, Felt, Towel, Metal); ORM packed; `island_margin 0.03` (P1 §1.1 step 7).
7. `sodium_check.py --subject` → beauty → `export_ue.py` (skeletal path: do NOT flatten empties; RIG §1.2) → `fixup_materials.py` → capture.

**BANNED on Merle.** Anything that would let the warmth curdle: no asymmetric eye placement, no mouth-corner tension, no dead-eye specular (the CASTING law is a modelling law here: "if a face would read as knowing in a thumbnail, redo the face", KEYART §LAWS). No button eyes. No thin shells for the apron or cardigan. No idle that stills her hands outside the four scripted stills (§1.4). No mesh swap for drift.

### 1.4 RIG & ANIMATION SPEC

**Bones (on `SKEL_Cast_Human`, plus):** `prop_towel` (child of `hand_r`, the wrung towel's root; the towel's far end weighted to `hand_l` with a two-bone IK so the hands can separate for the pen-up pose), `prop_mug`, `prop_spoon` (children of `hand_r`, hidden unless the busy-hands set calls them), `pendant` (child of `spine_03`, a one-bone pendulum, tiny range), `bun` (child of `head`, pose-only), `eye_l/r`.

**Motion states (the UE `AMerle` port of MERLE.gd drives them; the AnimBP observes).**

| # | State | Trigger (MERLE.gd → `AMerle`) | Clip / asset (proposed) | Timing | Must NOT |
|---|---|---|---|---|---|
| M-P0 | AT KETTLE (day) | `!bIsNight && !bLockdownDone && !PenUp && !Screening` | `AS_Merle_Kettle_Busy` loop: towel-wringing, plate-drying, kettle-touching — the busy-hands set | none in canon; the kettle's glow is "a real light" [ROOMS §KITCHEN] | still hands (see M-S1); leave the kettle position [QA-11 "never elsewhere"] |
| M-P1 | WALK to target | `global_position.move_toward(target, 1.6·δ)` | `AS_Merle_Walk_160` (root motion authored; brain owns translation per RIG §3.4) | 1.6 m/s [TIMINGS `merle.gd SPEED`] | run; any speed but 1.6 |
| M-P2 | IN HER CHAIR (night / after lockdown) | `bIsNight || bLockdownDone` | `AS_Merle_Chair_Busy` (seated, hands on a mug or the towel) | — | face the dead set with menace: she "keeps a chair facing the dead set" only in ending 1B [MASTER §ENDING 1B] |
| M-P3 | SCREENING spot | `ScreeningActive` → (0.4, 0, 1.4) | `AS_Merle_Screening` (seated among the rows, hands still on the beat) | screening BEAT 0.8 s, WINDOW 3.2 s [TIMINGS] | react to the cue signs ("no one acknowledges when they light", DESIGN Part III) |
| M-S1 | THE STILLS (hands stop on a line) | line events: "It's what our last archivist did" [T1.3], "Don't make me regret the word" [T2.1], "138 … That's all there ever were" [T2.3 ASK], "He asks so many questions" [T2.5] | `AS_Merle_HandsStill` additive: the towel stops, both hands hold | hold for the line's length; canon gives no number | any other tell; the stop must be absolute (the listening is the cue: "when they still, listen") |
| M-S2 | THE MONOLOGUE (1974) | `crate_opened && !merle_1974` on interact | `AS_Merle_1974` (one clip): hands "empty and open" from "And then the dark got warmer" | reference toasts 3.2/3.4/3.2/3.2/3.0/3.4 s [MERLE.gd 67–82]; audio is "one unbroken take" [AUDIO §5] — OPEN-18 | cut the clip to the toasts if the take is one piece |
| M-S3 | THE PEN-UP (decision point) | `PenUp()` true → walk to DOORWAY, then hold | `AS_Merle_PenUp_Hold`: standing in the doorway, "hands empty and open, watching the pen, saying nothing" | 45 s of reference footage drives it [CASTING §THE CALLBACK]; the hold lasts as long as the pen is up (no timer in MERLE.gd) | breathe visibly (a 45 s hold on a felt figure is a statue; a breathing additive would be a lie about the material), speak, look away from the pen |
| M-D1 | M1 THE SECOND VIEWING | `mark_casualty("MERLE","M1")` | `AS_Merle_M1_Pat` (the last thing she does is pat Rita's hand) → `Hidden`; "her voice finishes the sentence from inside the speaker, warm, three seconds after her chair is empty" | 3.0 s voice lag [CASUALTY §MERLE M1]; caption `[THE KETTLE, TWO ROOMS AWAY, CLICKS OFF]` [ACCESS §3.2] | any body horror on her: the broadcast-body idiom is the speaker, not the figure |
| M-D2 | M2 THE HOME SINGER | premiere, call sheet | `AS_Merle_M2_Sing`: "Taken on the beat, mouth still shaped around the true word" — on a felt head with no mouth articulation the "shaped mouth" is a HEAD POSE (chin lifted, singing) held at the cut, then interlace/dropout on the figure via `M_Broadcast_Body` | on the beat [CASUALTY §MERLE M2] | lip-sync (no phonemes on a needle-felt head, §0.5) |
| M-E | Endings | 1A "the game holds on her hands, which have nothing to do"; 1B "keeps a chair facing the dead set"; 2 "front row, radiant, forever" | `AS_Merle_End_HandsIdle` (hands in her lap, still, for the first time because there is nothing to hold); `AS_Merle_End_Radiant` | — [MASTER §ENDINGS] | — |

**What must NOT move:** the face (felt, no articulation); the apron's 58 (no cloth sim at runtime — bake); nothing on her ever does a "take" or a double-take (never-sinister). Physics: pendant only (one bone, damped); no cloth sim at runtime on the cardigan (bake the rest pose; the crafted world is "physically dependable in craft logic", DESIGN Part II).

**UE drive.** `AMerle : AActor, IRestorationInteractable` ports MERLE.gd verbatim: `Where()` returns the four targets by `State->bIsNight`, `bLockdownDone`, screening flag, `PenUp()`; `Tick` moves the actor with `VInterpConstantTo` at 160 uu/s; the AnimBP reads an enum `{Kettle, Walk, Chair, Screening, PenUp, Monologue, Dead}` set at those sites (the RIG §3 principle: the brain is authoritative, the animation observes). `PenUp()` needs the ledger port (Phase 4); until then a test bool. The M-S1 stills fire from the line sites (toasts) as an anim notify-style event. Casualty state from `State->Casualties` (STATE.h 101, 186).

### 1.5 ACCEPTANCE

- Sodium `--subject` on `SK_Merle`: cardigan reads as knit (cable relief + fibre), apron and blouse as printed cotton (two florals distinguishable in monochrome light by relief and value), towel as woven linen with stripe value, felt face as felt (fibre nap visible at the 1 m closeup, no plastic sheen); three-way light response on every surface.
- Cycles beauty beside PLATE-MERLE at matching framing (three-quarter, hands at the waist): silhouette, wardrobe layering and the 58 match; then the turnaround (L / back / R) beside the plate strip.
- UE locked-EV capture in KITCHEN at (800, −100, 0) uu: amber practicals + the kettle's glow [ROOMS §KITCHEN]; judge at gameplay distance (3 m) and at 1 m on the towel and the 58.
- Scale: imported bounds = the authored height ± 1 cm (1.58 m ESTIMATE until ruled); the 1 m cube reads 100.0 uu; actor scale 1.0 in the level.
- Motion: ≥8-frame capture of M-P1 at 1.6 m/s (no foot slide); a two-capture pixel diff of M-S3 30 s apart (zero motion outside the pendant); the M-S1 still measured as a hard stop of `prop_towel` velocity at the line's notify; QA-11 (kettle / chair / doorway, never elsewhere) in simulate.
- Never-sinister read: the head portrait capture reviewed by the owner against KEYART §LAWS ("if a face would read as knowing in a thumbnail, redo the face").

### 1.6 RISKS / OPEN

- OPEN-9 (glasses chain, enamel pin); C-1 (age); C-2 (drift); OPEN-18 (monologue pacing); OPEN-3-class height (ESTIMATE 1.58 m); OPEN-C1 (head size at 1 : 5.5).
- Risk: the busy-hands set on mitten hands. Wringing a towel without fingers must read as hands-never-still through wrist and forearm; if it reads as flippers the whole character reads as a toy and the warmth fails. Mitigation: the thumb bone plus the `fingers` curl bone, and the towel's own bone doing most of the work.
- Risk: a 45 s statue at the decision point. It is canon; the risk is that the figure reads as a freeze BUG. Mitigation: the pendant's settle in the first second, then nothing; the caption pipeline carries `[pen tick]` only [ACCESS §3.2].

---
## 2 · HARRIET · SENIOR CLUB MEMBER · THE CONTINUITY KEEPER (unit 2.3)

### 2.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Who | "Late 60s, mononymous by the club's own records … THE CONTINUITY KEEPER. Voice precise, measured, transitional; her signature line … 'And now. The tour continues.' … Confirmed props: THE teacup (floral china, the one that rises), a 58 Club flask whose contents go unrecorded, her pin card, and a reel in her keeping annotated for frame loss" | SHEETS §HARRIET |
| The holding pattern | "during the compound's commercial-break windows she stops mid-motion, teacup half-raised, and resumes on the return cue. This is a background-behavior system, never a cutscene" | DESIGN Part I · Harriet |
| Lengthening | "Her mid-motion freezes during break windows lengthen each act. In the Sign-Off ending, when the station goes dark, she resumes, finishes raising the teacup, and drinks. The game never explains how long she was holding" | WALK Part I · Harriet |
| LAW 6 | "THE SCHEDULE IS REAL. ON AIR and BREAK govern behavior mechanically; Harriet freezes on breaks" | LAWS 6 |
| LAW 7 | H1 CONTINUITY: "she does not freeze, she is absent, chair warm, and the film cabinet now contains her, folded, with leader tape where her voice was". H2 THE SPLICE: "seated one frame to the left of herself, doubled at the shoulders, both mouths open on different vowels, the teacup rising in two hands at two heights. She remains like this, on set, for the rest of the game, and the game treats her as scenery" | CASUALTY §HARRIET |
| Ambient wrongness | "Harriet's cup is higher than yesterday" — drift "never called out by text" | DREAD §L1 |
| The seventh signal | "(she performs them, precise as liturgy, and then a seventh: both hands pressed flat, pushed down twice) Hold your applause" | MASTER T2.4 ASK; PROPS D06 |
| Sound | "S13 Harriet. A gentle fabric-and-breath sway loop that hard-stops on break windows and resumes phase-accurate on the return cue; the teacup gains a single porcelain tick per day at first touch" | AUDIO §3 S13 |
| Reaction | H-R1 one corrective beat of pause after a broken beat; H-R2 "HER FREEZES LENGTHEN when After-Fire is active in the building, one extra second, unexplained" (both QUEUE; OPEN-10) | REACT §HARRIET |
| Drift | "HARRIET: drifts on the curve exactly, the control subject" | ART §5 |
| Captions | `[ONE FRAME LEFT OF HERSELF]`, `[A REEL, LABELED IN HER HAND: ME]` | ACCESS §3.2; HARRIET.gd 105, 115 |
| Achievement | A06 MID-MOTION, the only one that touches her | ACH A06 |

### 2.2 WHAT EXISTS

| Item | State | Source |
|---|---|---|
| UE actor | `AHarriet : AActor, IRestorationInteractable` — sways ON AIR by setting actor **Roll** = sin(T × 0.9) × 0.04 rad (as degrees), `T` stops advancing on `!Clock->IsOnAir()` so the pose holds "exactly where the cue left her"; prompt "HARRIET · in her chair (E)" / "HARRIET · mid-motion"; test harness `bTestFreeze` proves swayA 0.835 → swayB 1.791 → frozenC 1.791 held. H1/H2 "land with the presentation half" | HARRIET.h; HARRIET.cpp 27–33, 66–89; PROGRESS 0.8b-5 |
| Clock | `URestorationClock::IsOnAir()`, `OnPhaseChanged(bool)`; ON AIR 50.0 s / BREAK 18.0 s, timer-driven | CLOCK.h; TIMINGS `broadcast.gd` |
| Godot brain | cup at `(0.18, 0.99 + 0.05·min(day, 6), 0.17)` m — rises 5 cm per day, capped at day 6; sway `rotation.z = sin(t·0.9)·0.04`; H2 double = `_rig.duplicate()` at +0.13 x, +0.03 z, `rotate_y(0.06)`; H1 hides her; slip arming Day 2+ while frozen; the two casualty toasts with 2.8 s / 2.4 s waits | HARRIET.gd 27–33, 68–74, 100–116 |
| Godot figure | `CharacterKit.harriet()`: brown `_cardigan` with three buttons "done up once", cream blouse, tweed skirt with belt, brooch sphere, right arm "cup" pose, left arm "clutch" with a saucer cylinder, head (0, 1.46, 0) `bun_neat`, pearl earrings; the CUP is a script-owned cylinder, not part of the figure | KIT 683–714; HARRIET.gd 49–58 |
| Placement | REC ROOM (1.2, 0, 2.6) → UE (120, 260, 0); canon home chair GREEN ROOM "HER CHAIR" vs REC "Harriet's chair + teacup" (OPEN-11, C-14) | WB 1083; ROOMS §GREEN ROOM; INVENTORY §3 |
| Chair | none built; the plate's carved wooden armchair | PLATE-HARRIET |

### 2.3 BUILD BRIEF

**Silhouette and proportions.** Seated upright in a carved dark-wood armchair (turned arms, scrolled front legs); chocolate cable-knit cardigan buttoned once at the sternum; cream high-collared blouse, pin-tucked, with a small oval brooch at the throat; brown tweed skirt to below the knee; silver hair curled and pinned high; pearl drop earrings; the floral china teacup raised in the RIGHT hand at chin height, the saucer held level in the LEFT at the sternum; turnaround L / back / R (the back shows the cardigan's cable ribs and the pinned bun) [PLATE-HARRIET]. Props panel: 58 CLUB pin card (a small dark card with the club's concentric-ring mark), the illegible handwritten pages, a dark hip flask stamped 58 CLUB, the teacup and saucer, a reel annotated "PARTIAL FRAME LOSS" [PLATE-HARRIET; SHEETS §HARRIET].

| Measure | Value | Status |
|---|---|---|
| Height | canon: **OPEN (none stated)**. Reference KIT ≈ 1.6 m, capsule 0.3 × 1.6 [HARRIET.gd 42–47]. **ESTIMATE from the plate: ~1.63 m** (seated head-to-knee span vs the chair's seat height read as ~0.45 m; upright, long-necked) — a placeholder | OPEN (owner) |
| Seated eye height | ESTIMATE ~1.15 m above floor in the chair (for the T4.2 rail beat and the screening sightlines); canon none | OPEN |
| Cup track | rest (0.18, 0.99, 0.17) m relative to her root, +0.05 m/day, cap day 6 → 1.29 m at day 6 | HARRIET.gd 70 (reference; the only numbers) |
| Head-to-body | 1 : 5.5 (OPEN-C1) | ART §6 |
| Hands | mitten, stitched finger definition (principal) | ART §6 |

**Materials.**

| Need | Candidate (id · source · licence) | How |
|---|---|---|
| Cable-knit cardigan, chocolate | as Merle §1.3 (`knitted_fleece`, `wool_boucle`; modelled cables) tinted to (0.27, 0.2, 0.14) [KIT 691]; Fab "cable knit" | shared `M_Knit` instance family |
| Cream blouse, pin-tucked, high collar | `terlenka` (cream fine weave, 265 mm) · Poly Haven · CC0 or `cotton_jersey`; pin-tucks as normal-map ridges (< 2 cm → maps) | (0.95, 0.9, 0.78) [KIT 692] |
| Tweed skirt, brown | `poly_wool_herringbone` (grey wool, 270 mm) · Poly Haven · CC0 tinted; `Fabric013` (brown woven pattern) · AmbientCG · CC0 as an alternate; `Fabric031` (in hand) as the coarse base | (0.29, 0.24, 0.18) [KIT 694] |
| Brooch, oval, brass with a stone | `Metal042B` (dirty gold) · AmbientCG · CC0; `Metal013` (bronze, eroded) for the aged setting | plate: small oval brooch at the collar |
| Pearl drop earrings | `Ivory001A` / `Ivory002A` (ivory, beige/white) · AmbientCG · CC0 for the nacre base with a layered clearcoat; drops on `earring_l/r` bones (tiny pendulum) | KIT 703 |
| THE teacup and saucer, floral china | `tea_set_01` (antique floral tea set, 918×483 mm set) · Poly Haven · CC0 — cut one cup and one saucer via bmesh (the Camera_01 donor precedent, P1 §0.3); `Porcelain001` (white porcelain) · AmbientCG · CC0 for the glaze; the floral transfer authored (brown-on-cream per the plate) | the cup is a SEPARATE mesh on its own bone (it rises; and in H2 there are two) |
| Silver hair | felt: `Fabric034` (felt) · AmbientCG · CC0 + `polar_fleece` (cream) · Poly Haven · CC0 tinted silver; the curls as felted wool ridges (sculpt), not strands | (0.58, 0.56, 0.52) [KIT 708] |
| Needle-felt head and hands | as Merle | |
| The carved armchair | `ArmChair_01` (gothic vintage carved wood chair, 848×765 mm) · Poly Haven · CC0 as the donor, or `WoodenChair_01` / `GreenChair_01` · Poly Haven · CC0; wood `Wood051` (dark espresso hardwood) · AmbientCG · CC0 or `walnut_veneer` · Poly Haven · CC0 | `SM_Harriet_Chair`; the saucer ring on the arm is GREEN ROOM dressing [ROOMS §GREEN ROOM] |
| 58 Club flask | `modified_thermos` (vintage flask) · Poly Haven · CC0 as a form donor only — the plate's is a flat hip flask: build from a bevelled slab with `Leather034C` (stitched dark leather) · AmbientCG · CC0 wrap and `Metal049B` (dirty silver) cap; the 58 CLUB stamp as a decal | contents "go unrecorded" — no liquid, no sound |
| Pin card | `Cardboard002` · AmbientCG · CC0 + `Paper006` (beige) | readable tier → `M_Paper` |
| The illegible pages | `M_Paper` [PIPE]; the hand "photographs as script that will not resolve" — author the handwriting as a texture that never resolves at any mip (SHEETS §HARRIET) | a readable that must NOT be readable: 4K allowed, but the text is designed to fail |
| The annotated reel | no CC0 reel on either API (checked); Fab "film reel", "tape reel", "open reel" | shared with the bench's reels (Phase 3) |

**Drift.** `MI_Harriet_*` `Drift` wired to the coat-peg curve exactly — she is "the control subject" [ART §5]: cardigan and skirt drift toward BURNT/MUSTARD; blouse stays cream (textiles second, per ART §4).

**Blender steps.**
1. Block at the ESTIMATE (1.63 m) on the shared skeleton; author the figure SEATED in its rest pose (she is never seen standing in canon: chair in REC/GREEN, "at the rail" T4.2 is a lean, not a stand — OPEN-H1 whether a stand-up clip exists), with a separate A-pose export for retargeting.
2. Chair donor cut and re-proportioned to her (seat ~0.45 m); `UCX_` box for the chair; the figure's collision is the 0.3 × 1.6 capsule of the reference.
3. Cardigan as Merle (solid, modelled cables); three buttons as geometry (silhouette at 1 m); blouse tucks as maps.
4. Cup + saucer cut from `tea_set_01`; the cup gets its own object `Cup` skinned 100 % to `prop_cup`; the saucer 100 % to `prop_saucer`.
5. Pearls: two drops, `earring_l/r`.
6. Bakes 2K per group (Knit, Blouse, Tweed, Felt, China, Metal); the pages at 4K (readable) but authored illegible.
7. Sodium `--subject` → beauty beside PLATE-HARRIET (seated, cup raised) → export → capture.

**BANNED.** Button eyes. Thin-shell cardigan. A cup that is part of the body mesh (it must rise independently and double independently). Any face articulation for "both mouths open on different vowels" beyond a head pose (§2.4 H2). Any text that calls out the cup's height (DREAD §L1). Runtime cloth (the freeze must hold every vertex where the cue left it; simulated cloth would keep settling through a break and break LAW 6).

### 2.4 RIG & ANIMATION SPEC

**Bones (shared skeleton, plus):** `sway` (child of `root`, parent of `pelvis`; the ONE bone the sway drives, so the whole seated figure rolls as `AHarriet` rolls the actor today — the port may keep rolling the actor or move the sin to this bone; either way ONE source), `prop_cup` (child of `hand_r`; carries `SOCKET_Cup`), `prop_saucer` (child of `hand_l`), `earring_l/r`, `bun`, `eye_l/r`. The chair is a separate `SM_`.

**Motion states.**

| # | State | Trigger | Clip / asset | Timing tied to | Must NOT |
|---|---|---|---|---|---|
| H-P0 | THE SWAY (ON AIR) | `Clock->IsOnAir()` | `AS_Harriet_Sway` loop on `sway` (or the actor roll as built): roll = sin(t · 0.9) · 0.04 rad; plus the S13 "fabric-and-breath" loop as audio, not as mesh breathing | HARRIET.cpp 82–86; HARRIET.gd 73–74 | any other idle; the cup arm must stay at its day height |
| H-P1 | THE FREEZE (BREAK) | `!Clock->IsOnAir()` → `Tick` returns before advancing `T` | none: the graph's global play rate goes to 0.0 the same frame; every bone holds | LAW 6; HARRIET.cpp 79 "THE FREEZE: mid-motion, until the return cue"; BREAK 18.0 s [TIMINGS] | ease into the stop (it is a hard stop, "hard-stops on break windows", AUDIO S13); settle; blink; any pendulum continuing (earrings freeze too — physics OFF on the cue) |
| H-P2 | THE RESUME | `OnPhaseChanged(true)` | resume at the exact stored phase (`T` is preserved) | "resumes phase-accurate on the return cue" [AUDIO S13] | restart the loop from zero |
| H-C | THE CUP RISES | day change | `SOCKET_Cup` offset Z = 0.99 + 0.05 · min(day, 6) m in her root space (reference numbers) | HARRIET.gd 70; QA-09 "cup height strictly rises across tapes" | drop, reset, or be captioned; a porcelain tick per day at first touch is S13's sound cue |
| H-S1 | THE SIGNALS + THE SEVENTH (T2.4 ASK) | dialogue beat | `AS_Harriet_Signals`: "(setting down her cup, mid-motion, resuming)" then the six signals "precise as liturgy", then both hands pressed flat, pushed down twice | canon gives no durations | perform them standing (she sets the cup down and performs seated; OPEN-H1) |
| H-S2 | THE HUM (T2.6) | dialogue beat | head pose only; the hum is audio (S14 is the night-one contralto, a different asset) | MASTER T2.6 | mouth articulation |
| H-S3 | CUE 4: THE CUP COMES DOWN | premiere CUE 4 | `AS_Harriet_CupDown` — the first time in the game the cup lowers | MASTER T5.3 CUE 4 | a flourish |
| H-S4 | SIGN-OFF: SHE FINISHES AND DRINKS | ending 1A/1B, station dark | `AS_Harriet_Drink`: resumes, finishes raising the teacup, drinks | WALK Part I; MASTER §ENDING 1A "Harriet finishes her tea" | explain the duration (no caption) |
| H-D1 | H1 CONTINUITY (absent) | slip taken; next break | `Hidden` on the break; the chair is warm (a heat decal on the seat cushion, dressing) and the film cabinet holds "her, folded, with leader tape where her voice was" — a folded FELT figure asset `SM_Harriet_Folded` in the cabinet with a strip of leader tape at the mouth line | HARRIET.gd 109–116 (2.4 s between toasts); caption `[A REEL, LABELED IN HER HAND: ME]` | gore; the fold is a cloth figure folded like laundry, that is the whole horror |
| H-D2 | H2 THE SPLICE (doubled) | rejected edit on her reel; next break | a SECOND `AHarriet` instance at +0.13 m X, +0.03 m Y (Godot z → UE Y), yaw +0.06 rad (3.4°), permanently frozen in H-P1; "both mouths open on different vowels" = two different HEAD POSES (chin/jaw angle) on the two instances, never mouth articulation; "the teacup rising in two hands at two heights" = the two cups' `SOCKET_Cup` offsets differ by one day step (0.05 m) | HARRIET.gd 27–33; caption `[ONE FRAME LEFT OF HERSELF]`; 2.8 s toast gap | scale either instance; blend the two; any movement thereafter ("the game treats her as scenery"); a second sway (both frozen) |
| H-E | Endings when dead | every ending replaces her line with TRANSITION UNRESOLVED (a card, not a pose) | — | CASUALTY §HARRIET ENDINGS; QA-50 | — |

**Reaction hooks (QUEUE, OPEN-10):** H-R2 adds 1.0 s to the freeze on `State->bAfActive` — implement as a resume delay after `OnPhaseChanged(true)`, never as a longer BREAK (the clock is canon). H-R1: one corrective beat (BEAT 0.8 s) of pause before her next line after a broken beat.

**What must NOT move:** the face; the cup relative to the hand (it rides `prop_cup`; the HAND lifts, the cup does not float — the day rise is authored as an arm pose per day step, the socket offset is the reference's shorthand); anything at all during a BREAK.

**UE drive.** `AHarriet` exists; add `USkeletalMeshComponent` + AnimBP with a `PlayRate` bound to `IsOnAirEffective()` (1.0 / 0.0) and `Day` from `State->Day` (STATE.h 150) for the cup step; H1/H2 from `State->Casualties` cause tags; the H2 double spawned by the presentation half as a second `AHarriet` with `bFrozenForever`. Keep the test harness (`bTestFreeze`) green.

### 2.5 ACCEPTANCE

- Sodium `--subject` on `SK_Harriet` + `SM_Harriet_Chair`: knit vs tweed vs blouse cotton distinguishable by relief and roughness; china reads as glaze (tight highlight, low roughness variation, floral transfer under the glaze); pearls as nacre; felt as felt; the chair's carving as wood, not plastic.
- Cycles beauty beside PLATE-HARRIET (seated, cup raised, saucer level) at matching framing; turnaround strip.
- UE locked-EV capture in REC (120, 260, 0) uu (and GREEN ROOM once OPEN-11 rules): the freeze test re-run with the mesh (`HARRIET-FREEZE … held=1`); a two-capture pixel diff during a BREAK (zero motion anywhere, earrings included); a capture per day 1..6 with the cup's world Z measured strictly increasing by 5.0 cm ± 0.2 (QA-09).
- H2: two instances captured; offset measured 13 cm / 3 cm / 3.4°; two cups at two heights; no motion for 60 s.
- Scale: bounds = authored height ± 1 cm; actor scale 1.0 on BOTH instances.
- A06 fires on interact while frozen [ACH A06]; captions from the parity set fire at HARRIET.gd's sites.

### 2.6 RISKS / OPEN

- OPEN-10 (H-R1/H-R2), OPEN-11 / C-14 (home chair), C-3 (surname in a comment), OPEN-H1 (does she ever stand? no canon clip needs it; the rail beat T4.2 is OPEN), height ESTIMATE 1.63 m, OPEN-C1.
- Risk: "both mouths open on different vowels" on a felt head with no mouth. The brief's answer (two head poses, chin angles) is a reading, not canon; the owner should see the H2 capture before it ships.
- Risk: the freeze must be a hard stop of everything including physics; one earring still swinging during a break is a LAW 6 defect that QA-09 will not catch by eye. Add the pixel diff to the automation.

---

## 3 · VESS KEYS · TAPE HUNTER (unit 2.4)

### 3.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Who | "Early 20s. Tape Hunter, Source Researcher, Provenance Specialist. Alignment: Lawful Curious. Voice eager, quick, searching; tell: touches the label maker or the 58 Club pin when nervous, and the pin on the sheet IS the plastic pin the deaths fuse into the enamel … surname KEYS … pronouns he/him" | SHEETS §VESS |
| The pin | "his club pin is plastic where everyone else's is enamel … he is what the fandom looks like when the fandom is not chosen" | DESIGN Part I · Vess |
| Tells | "Vess touches the label maker at his belt when nervous and the plastic pin when hurt" | MASTER header |
| Wardrobe | "thrift-store seventies shirts worn as devotion cosplay, label maker on his belt, chewed pens"; T4.1 "three days of beard" | DESIGN Part I · Vess; MASTER T4.1 |
| Drift | "VESS: resists longest; neutrals through Day 4, and his only show-palette object is the plastic pin he has always carried, which is the other tell; if he credits and is credited, he adds one avocado scarf for the premiere, chosen, not drifted" | ART §5 |
| LAW 7 | V1 "taken live, cut mid-sentence on his own slate insight, his plastic pin fused into the panel enamel". V2 "Found interlaced with the transmitter hum, his outline refreshing at 60 fields a second" | CASUALTY §VESS; caption `[MAINS HUM, SHAPED LIKE A STANDING PERSON]` [ACCESS §3.2] |
| The final breaker | credited: "his hand stops above the handle … (the hand comes down off the breaker, empty)"; uncredited: "(nothing. The handle. The dark.)" | MASTER T5.3 |
| Anchor scene | T4.5 "standing in it, pin in his fist, voice level by force"; his T4 scene is mandatory | MASTER T4.5; DESIGN §CLOSING gap 3 |
| Reaction | V-R2 post-wake "his tell (touching the pin) doubles in frequency"; V-R1, V-R3 (QUEUE) | REACT §VESS |
| Voice | "fast, precise, a man narrating to keep his hands steady" | AUDIO §5 |

### 3.2 WHAT EXISTS

| Item | State | Source |
|---|---|---|
| Godot brain | `VessProp` (Interactable): four lines cycled, hidden when dead; no schedule, no movement | VESS.gd |
| Godot figure | `CharacterKit.vess()`: `_body_base` with a patterned "floral" blouse, `rig.scale (0.95, 1.07, 0.95)` "taller, narrower", boxy open jacket with lapels, a 58 CLUB patch cylinder on the left chest with the pin sphere beneath, three chewed pens, label maker box on the belt, right arm "pocket", left "down", head (0, 1.44, 0) `curly_dark` | KIT 717–758 |
| Placement | REC shrine wall (−3.7, 0, −1.2) facing −X → UE (−370, −120, 0); canon country PATCH BAY / TAPE LIBRARY | WB 1086–1088; ROOMS §PATCH BAY |
| Props | `VessBinder` DORMS (−6.5, 0.6, 1.8); `RejectedEdit` REC (−2.6, 0.9, 1.0); `CreditEntry` BENCH (7.4, 0.9, −15.2) | WB 1052–1059, 1126–1130 |
| State | `vess_insight`, `vess_credited` → `bVessCredited` | STATE.h 89, 174 |
| UE | no actor, no mesh | — |

### 3.3 BUILD BRIEF

**Silhouette and proportions.** Slight, narrow-shouldered, pale, freckled; dark unruly curls to the collar; a washed-black cotton work jacket worn open over a brown paisley shirt open at the throat and a grey undershirt; a thin cord necklace with a small dark bead; a round embroidered **58 CLUB** patch on the jacket's left breast; three pens and the DYMO label maker in the left chest pocket; turnaround L profile / front / back (the back shows the jacket's yoke seam and the curls) [PLATE-VESS]. Props panel: the 58 CLUB pin (rendered metal-rimmed on the plate — overruled to PLASTIC by SHEETS' own text, C-4), the DYMO label maker labelled PROPERTY OF V. KEYS, a spiral FIELD NOTES pad, the tabbed PROVENANCE BINDER · V. KEYS [PLATE-VESS]. Variants: T4 three-day beard [MASTER T4.1]; premiere avocado scarf if credited [ART §5].

| Measure | Value | Status |
|---|---|---|
| Height | canon: **OPEN-12**. Reference: KIT comment "1.78" vs mesh arithmetic ≈ 1.67 m; capsule 0.3 × 1.7 [KIT 94, 729; VESS.gd 18–23]. **ESTIMATE from the plate: ~1.76 m** (slight, long-necked, narrow; the turnaround's head-to-shoulder proportion reads lanky) — a placeholder | OPEN (owner) |
| Head-to-body | 1 : 5.5 (OPEN-C1) | ART §6 |
| Hands | mitten, stitched finger definition (principal) | ART §6 |
| Capsule | radius 30, half-height 85 uu | VESS.gd 18–23 |

**Materials.**

| Need | Candidate (id · source · licence) | How |
|---|---|---|
| Washed-black cotton work jacket | `denim_fabric_06` (dark worn denim twill, 254 mm) · Poly Haven · CC0 desaturated; `Fabric075` (dark blue-grey) · AmbientCG · CC0 as an alternate | (0.13, 0.12, 0.12) [KIT 731]; wear at the cuffs and pocket mouth |
| Paisley shirt | **no paisley scan on either API (checked)**: author the paisley as a tileable albedo (brown/ochre/blue on brown, as the plate) over `cotton_jersey` · Poly Haven · CC0; print relief from `Fabric081C` · AmbientCG · CC0; Fab "paisley fabric", "70s shirt" | the shirt is the "devotion cosplay" and must read as a thrift-store print, faded |
| Undershirt grey | `jersey_melange` (heathered knit) · Poly Haven · CC0 | |
| Trousers dark | `denim_fabric_05` (dark grey denim) · Poly Haven · CC0 | (0.12, 0.115, 0.12) [KIT 725] |
| Cord necklace | `Rope001` (string) · AmbientCG · CC0 on a bevelled curve; bead `Plastic003` (dark brown plastic) · AmbientCG · CC0 | |
| 58 CLUB patch (embroidered) | thread relief from `Rope001` as a normal source; embroidery authored as albedo/normal decal on the jacket (< 2 cm → maps) | round patch, cream ring, dark centre |
| THE PLASTIC PIN | `Plastic012A` (black plastic) · AmbientCG · CC0 or `Plastic014A` (orange-red) tinted to the pin's colours; a cheap injection-moulded read: soft edges, a sink mark, a mould seam in the normal; **never** `M_Enamel` (that master is for "where the pin fuses" and for everyone else's pins) | LAW 7 V1: the pin is what fuses into the panel enamel; the panel's `M_Enamel` instance gets a fused-pin decal state |
| DYMO label maker | **no donor model on either API (checked)**; build: a bevelled slab with edge wear (PLAN §R.1 allows "beveled with edge wear"), `Plastic012B` (scratched black) · AmbientCG · CC0, embossed tape `Plastic010` (white) with the PROPERTY OF V. KEYS label as a readable decal; Fab "label maker", "dymo" | rides `prop_labelmaker` on the belt; a second instance in the chest pocket per the plate is OPEN (plate shows it in the pocket, DESIGN "on his belt") |
| Three chewed pens | `stationery_supplies` (pens, pencils) · Poly Haven · CC0 cut down; bite marks as normal | red / blue / black [KIT 745] |
| FIELD NOTES spiral pad | `office_notepads` (lined notepads) · Poly Haven · CC0 donor; spiral wire `Metal049B` | readable → `M_Paper` |
| PROVENANCE BINDER | `binder_notebook` · Poly Haven · CC0 is a leather journal — use only its page block; the three-ring binder body from `Cardboard002` · AmbientCG · CC0 + `Leather034C` (stitched dark) · AmbientCG · CC0; rings `Metal049B` · AmbientCG · CC0; tabs A–M as `M_Paper` decals; Fab "ring binder" | D07 [PROPS D07] |
| Curls, near-black | felt: `Fabric034` tinted (0.09, 0.08, 0.08) [KIT 757] with `curly_teddy_natural` (curly plush) · Poly Haven · CC0 for the curl structure normal | felted curls, not strands |
| Freckles, stubble (T4 variant) | albedo layers on the felt head material (`MI_Vess_Head_T4`); stubble as a darker felt nap in roughness/normal | "three days of beard" |
| Avocado scarf (credited premiere) | `knitted_fleece` · Poly Haven · CC0 tinted AVOCADO #6B7D3B | `SK_Vess` material slot + a scarf mesh toggled by `bVessCredited && bPremiereLive` |
| Needle-felt head and hands | as Merle | |

**Drift.** `MI_Vess_*` `Drift` clamps at 0 through Day 4 (neutrals); the pin is the only show-palette object; the scarf is a chosen toggle, not a drift value [ART §5].

**Blender steps.**
1. Block at the ESTIMATE (1.76 m); narrow the shoulder width relative to the shared template (the plate reads slight); 1 : 5.5 head.
2. Jacket as a solid garment over the shirt (open front, boxy), cloth-simmed to rest then remeshed solid; the shirt collar open; the undershirt visible at the throat.
3. The pin: a 25 mm disc (FABRIC §3 gives the BELL as 25 mm; the pin's size is not in canon — OPEN, use 25 mm as the club regalia default) with plastic mould detail.
4. Label maker, pens, pad, binder as separate `SM_` props with sockets on the figure (`SOCKET_Belt`, `SOCKET_ChestPocket`).
5. Head: young, freckled felt sculpt; curls as felted ridges; bead eyes.
6. Bakes 2K; the binder pages and the label tape 4K readables.
7. Sodium `--subject` → beauty beside PLATE-VESS (three-quarter, jacket open, pens visible) → export → capture at (−370, −120, 0) and in PATCH BAY.

**BANNED.** Enamel on his pin (it is plastic; C-4 resolves in the text's favour). Button eyes. Thin-shell jacket. A "menacing" idle — his envy is "designed sympathetically" [DESIGN Part I · Vess]. A shared pin material with the club's.

### 3.4 RIG & ANIMATION SPEC

**Bones (shared skeleton, plus):** `prop_labelmaker` (child of `pelvis`, belt), `prop_pin` (child of `spine_03`, left breast), `prop_pens` (child of `spine_03`, pocket, pose-only), `necklace` (one-bone pendulum), `curls` (pose-only), `eye_l/r`.

**Motion states.**

| # | State | Trigger | Clip / asset | Timing | Must NOT |
|---|---|---|---|---|---|
| V-P0 | AT THE SHRINE WALL, cataloguing | default (reference has no schedule) | `AS_Vess_Catalogue` loop: hands on the shrine's pins/clippings, weight shifting | none in canon | move rooms (no schedule exists; OPEN-V1 whether he should have PATCH BAY hours) |
| V-T1 | THE LABEL-MAKER TELL (nervous) | line events: T1.7 "thumb on the label maker"; T2.8 "clicks in his pocket, twice, like a habit praying" | `AS_Vess_Tell_LabelMaker` additive: right hand to the belt, thumb press ×2 | canon: "twice"; interval OPEN | become a rhythm (it is a habit, not a metronome) |
| V-T2 | THE PIN TELL (hurt) | T1.3 "pin catching the light", T2.8/T4.5 "pin in his fist", T4.1 "touched twice", T4.7 "turned once" | `AS_Vess_Tell_Pin_Touch`, `_Fist`, `_Turn` additives on the left hand to `prop_pin` | post-wake frequency ×2 (V-R2, QUEUE) | — |
| V-S1 | THE SCREENING OVERREACH (T2.8) | screening beat | `AS_Vess_Screening_Eager`: answers too eagerly; "the room goes wrong around him for one held second" is the room, not him | BEAT 0.8 s; the held second 1.0 s | any pop |
| V-S2 | THE REJECTED EDIT (T4.5) | anchor scene | `AS_Vess_T45_Stand`: standing in the projector light, pin in fist, "voice level by force" (a stillness clip) | scene length | fidget (the point is the force) |
| V-S3 | THE FINAL BREAKER, credited | `bVessCredited` | `AS_Vess_Breaker_Hesitate`: hand rises to the handle, stops above it, comes down empty | "the hesitation is the window" [WALK Part I · Vess]; window length OPEN (finale port) | touch the handle |
| V-S4 | THE FINAL BREAKER, uncredited | `!bVessCredited` | `AS_Vess_Breaker_Pull`: "The handle. The dark." | — | — |
| V-D1 | V1 CREDITED, THEREFORE CAST | AUTHENTICATE while credited, or the breaker after the farewell | cut mid-sentence: the figure hard-cuts to `Hidden` on the line's word boundary (a splice, not a fade); the pin stays: `SM_Vess_Pin_Fused` decal/mesh on the panel's `M_Enamel` | QA-42; "all-monitors taking after the INK ripple" | a death animation (the idiom is the cut) |
| V-D2 | V2 THE UNCREDITED FIX | GET VESS at the dead panel, circuit F | `AS_Vess_CircuitF_Reach` then the interlaced body: `MI_Vess_Interlaced` — outline "refreshing at 60 fields a second" (a material state: alternate scanline rows offset per field at 60 Hz, chroma bleed, on the STANDING pose, held) | 60 fields/s; caption `[MAINS HUM, SHAPED LIKE A STANDING PERSON]` | move again; the crossing runs 62 s without him [WALK §ADDENDUM c043] |
| V-E | Ending 2 | "the producer's office contains his chair, still warm, facing the monitor wall" | dressing, not a pose | CASUALTY §VESS ENDINGS | — |

**What must NOT move:** the face; the pin except by his hand; the pens (pose-only). Physics: necklace only.

**UE drive.** `AVess : AActor, IRestorationInteractable` ports VESS.gd; tells fire from the line sites; `State->bVessCredited` (STATE.h 174) selects V-S3/V-S4; casualty cause tags select V-D1/V-D2; the scarf mesh toggles on `bVessCredited && bPremiereLive` (STATE.h 134).

### 3.5 ACCEPTANCE

- Sodium `--subject`: jacket reads as washed cotton twill (matte, worn), shirt as a printed thrift cotton (print relief visible), the pin as PLASTIC (soft edge highlight, mould seam) beside a club enamel pin on the same sheet (the contrast is the character); felt face with freckles.
- Beauty beside PLATE-VESS (three-quarter; pens and label maker visible; pin catching the light) and the L/front/back strip.
- UE locked-EV capture at the shrine wall (−370, −120, 0) and in PATCH BAY (phosphor + clip lamp, ROOMS §PATCH BAY); 1 m closeup on the pin and the patch.
- Variants captured: T4 beard; credited premiere scarf.
- V2 material state captured as an ≥8-frame sequence: the field alternation must be visible frame to frame and the pose must not move.
- Scale: bounds = authored height ± 1 cm (1.76 m ESTIMATE until OPEN-12 rules); actor scale 1.0.

### 3.6 RISKS / OPEN

- OPEN-12 (height), C-4 (pin on the plate), C-5 (ACH A11 CARDONA), OPEN-V1 (does he have a schedule; the reference has none), OPEN-C1.
- Risk: the plastic pin is the arc in one object. If the pin's material does not read as CHEAPER than the club's enamel under sodium, the tell is lost. Put both pins on one sodium sheet.
- Risk: "cut mid-sentence" (V1) requires the audio and the hide to land on the same frame; the presentation half must own that, not the AnimBP.

---
## 4 · LELAND MERRICK · PREVIOUS ARCHIVIST (unit 2.5)

### 4.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Who | "Filed. Not shelved. Mid-40s at the end; archivist and conservator, tenure 1972 to 1976, vanished the year before the fire. Voice dry, kind, careful; tell: green fine-liner in the margins. Always slightly cropped by the frame edge, as if the image cannot hold him correctly, which the engine's seance frames already honor" | SHEETS §LELAND |
| Where he is | "Exists only inside the tapes: mid-forties, archivist's cardigan, always partially cropped by the frame edge as though the composition refuses him. He holds a legal pad on which answers appear across frames. In the physical world he survives as green fine-liner annotations" | DESIGN Part I · Leland |
| How he moves | "single-frame stepping with the jog wheel reveals him moving only in the unobserved intervals, and questions written on the bench notepad are answered on his legal pad across a span of frames … every scrubbing pass wears the tape" | DESIGN Part IV.7 |
| The five answers | Q1 FILED. NOT SHELVED. (across four frames) … Q5 I'VE READ THE ENDING. IT'S GOOD. (one frame, steady hand); "a man at the edge of frame, cropped by the composition like it refuses him, legal pad against his chest. Holding still. Playing the game" | MASTER T4.4 |
| Ending 1A | "inside the frame he was cropped from for two years, Leland steps to center and is allowed to be whole … (a breath he does not need and takes anyway)" | MASTER §ENDING 1A |
| LAW 7 | L1 "His remaining print burns from the inside of the frames; the green ink drains upward out of every note in the building". L2 "his five answers un-write in reverse; the final frame shows the little door closing from the inside, his hand on the inner knob" | CASUALTY §LELAND |
| Voice | "Leland: never voiced. The legal pad is text by canon; his silence is load-bearing" (vs 1A/4c speech — C-7) | AUDIO §5 |
| Marketing | "The glimpse figure and Leland's face are never depicted in any marketing material, ever" | KEYART §LAWS |
| Never-stated | "Whether Leland chose to stay" | LORE §THE NEVER-STATED LEDGER |
| Reaction | L-R1 the unsigned margin NOT THAT ONE. PLEASE. (QUEUE); grief answers at frames 14 and 28 (BUILT) | REACT §LELAND; QA-50 |
| Tape world | "authentic period video reproduction … correct 4:3 pillarboxing, generation loss modeled per dub"; "Footage is always shot or rendered clean and degraded live in the shader ladder; artifacts are never baked into masters" | DESIGN Part II; ART §2 |

### 4.2 WHAT EXISTS

| Item | State | Source |
|---|---|---|
| Tape stage | `TapeStage` (SubViewport 320 × 240, camera at (0, 0.8, 2.6) looking at (0, 0.7, 0), one warm omni): Leland is a dark box 0.35 × 1.7 × 0.25 m at (1.35, 0.85, −0.5), camera-right so the frame edge crops him; a `Label3D` pad at (0.55, 1.15, 0.4) carries the answer text | STAGE.gd 26–57; TIMINGS `frame_sequence.gd W 320 / H 240` |
| Seance | `seance_dock.gd`, `MAX_FRAME 40`; `leland_answers` int array; grief answers at frames 14 / 28; A14 at five answers | TIMINGS; STATE.h `LelandAnswers`; ACH A14 |
| Compound figure | `CharacterKit.leland()` — cardigan, loosened tie, legal pad with five green ink lines and a pen, wire glasses (two torus rims + bridge), `rig.scale (0.97, 1.06, 0.97)`, `side_grey` hair, stubble; used by `cast_preview.gd` only, never spawned in the compound | KIT 765–805 |
| Props | LEDGER MARGIN (7.4, 0.9, −15.2) BENCH; D01 four pages; ambient traces (sign-in IN with OUT blank; L.M. under the bench lip; door four's blank card) | WB 1056–1059; PROPS D01; AMBIENT §§ENTRY, DORMS, BENCH ROOM |
| UE | nothing: no stage, no render target, no actor | — |

### 4.3 BUILD BRIEF

**Silhouette and proportions.** A tired, kind man; round wire-rimmed glasses; stubble; dark hair going grey, a little long, unkempt; brown cable-knit cardigan (shawl collar, buttoned low) over a fine-striped cream shirt with a dark tie loosened; a yellow legal pad held against the chest in both hands with green-ink notes and diagrams; a green fine-liner clipped in the cardigan; cropped by the LEFT frame edge on the plate; turnaround L profile / front / back (the back: cardigan ribs, hair over the collar) [PLATE-LELAND]. Props: ID badge (WJBU-TV → WGLD 58 per SHEETS header; L. MERRICK · ARCHIVIST · 1972–1976, a photo, a laminate with a clip), the legal pad page ("AUDIENCE ONLY", "Never accept a role", "Rita — You are safe as audience"), archival shelves (ACCESSION LOGS 1972–1976 / UNCATALOGUED TRANSFERS / MASTER TAPES), a reel with a hand-written label EP. 17 — PARTIAL FRAME LOSS · GREEN NOTES PRESENT [PLATE-LELAND].

| Measure | Value | Status |
|---|---|---|
| Height | canon: **OPEN (none stated)**. Reference: the in-tape box is 1.7 m tall [STAGE.gd 55]; the KIT figure ≈ 1.66 m. **ESTIMATE from the plate: ~1.78 m** (male, mid-40s, long torso in the three-quarter framing) — a placeholder | OPEN (owner) |
| FRAME truth (the number that matters) | he is composed for a 4:3 frame: 320 × 240 render, camera at (0, 0.8, 2.6) m, subject at x = +1.35 m so the right frame edge crops him; the plate crops him on the LEFT. Which edge per shot is authoring, not canon — keep the reference's right edge for the seance and the plate's left edge for any still | STAGE.gd; PLATE-LELAND |
| Head-to-body | 1 : 5.5 (OPEN-C1) — inside the tape the crafted ratio is doubly load-bearing: the footage is the same craft world seen through the format [ART §2] | ART §6 |
| Hands | mitten WITHOUT stitched finger definition (not a named principal) | ART §6 |

**Materials.**

| Need | Candidate (id · source · licence) | How |
|---|---|---|
| Cardigan, brown cable knit, shawl collar | as Merle §1.3 (`knitted_fleece`, `wool_boucle`, modelled cables) tinted (0.27, 0.2, 0.13) [KIT 765] | shared `M_Knit` family |
| Striped shirt | `Fabric079` (black/grey/white stripes) · AmbientCG · CC0 tinted cream/brown for the fine vertical stripe; `Fabric005` (blue stripes) as an alternate | (0.66, 0.61, 0.51) [KIT 766] |
| Tie, dark, loosened | `Fabric012` (dark blue woven pattern) · AmbientCG · CC0 or `crepe_satin` (satin) · Poly Haven · CC0 desaturated | |
| Trousers | `Fabric075` (dark) · AmbientCG · CC0 | (0.2, 0.17, 0.14) |
| THE LEGAL PAD | `office_notepads` (lined notepads) · Poly Haven · CC0 as the pad donor (cut one, rescale to US letter 216 × 279 mm); `Paper006` (beige) · AmbientCG · CC0 as the stock; ruling lines and the green ink authored on `M_Paper` [PIPE §MATERIAL MASTERS]; the ink is "Leland's green fine-liner, hand-rendered" [DESIGN Part III · Type System], ledger green #596B52 [ART §4] | a 4K readable: the answers are TEXT that must survive the artifact ladder |
| Wire glasses | `round_spectacles` (vintage round frame) · Poly Haven · CC0 | rims as geometry (silhouette); lens as glass with a period bloom under the ladder |
| ID badge | `Plastic013B` (scratched white plastic) · AmbientCG · CC0 for the laminate; `Paper001`; clip `Metal049B` | a readable |
| Hair, dark going grey | felt: `Fabric034` tinted (0.22, 0.2, 0.18) with grey felted streaks | |
| Stubble | roughness/normal nap on the felt face (as Vess T4) | permanent on him |
| The shelves and the reel (set) | `wooden_bookshelf_worn`, `steel_frame_shelves_01` · Poly Haven · CC0; reel: Fab "film reel", "tape reel" | the tape stage set is Phase 3/4 dressing; listed so the stage has walls |
| Little door, inner knob (L2's last frame) | Studio A's little door [ROOMS §STUDIO A]; the knob `Metal042B` | one still: "his hand on the inner knob" |

**Drift.** None: he is inside the tapes; the tape world's look is the artifact ladder's [ART §2]. `MI_Leland_*` carries no `Drift`.

**Blender steps.**
1. Build the full figure at the ESTIMATE (1.78 m) even though he is only ever seen cropped ("Slightly cropped by every frame; the least we can do is build all of him", KIT 762 — a build note that is also the honest approach: ending 1A shows him whole).
2. Cardigan solid with cables; shirt stripes as maps; tie as a solid strip cloth-simmed to the loosened hang; glasses from the donor; the pad as a separate `SM_Leland_Pad` on `prop_pad` with `SOCKET_PadFace` for the text material.
3. The pad's page material: `MI_Leland_Pad_Q0..Q5` (blank, then each answer, the grief variants at frames 14/28 — QA-50 — and the L2 reverse un-write sequence), all authored CLEAN; the ladder degrades them live [ART §2].
4. Head: tired, kind felt sculpt with stubble; bead eyes behind the wire rims.
5. Bakes 2K; the pad and badge at 4K.
6. Sodium `--subject` → beauty beside PLATE-LELAND at the plate's crop (left edge) → export → the STAGE capture (§4.5).

**BANNED.** Voice (never voiced; the pad is text — C-7 is the owner's to reconcile, not the rig's). Any depiction of his face in marketing captures (KEYART §LAWS). Grain, chroma or scanlines baked into any of his textures (ART §2: the ladder is live). A compound placement: no `ALeland` walks the building. Button eyes. Any pose that "resolves" whether he chose to stay.

### 4.4 RIG & ANIMATION SPEC

**Bones (shared skeleton, plus):** `prop_pad` (child of `spine_03`, both mittens weighted to it via IK so the pad sits "against his chest"), `prop_pen` (pose-only), `glasses` (child of `head`, rigid), `hair`, `eye_l/r`.

**The frame law (how he moves at all).** He "moves only in the unobserved intervals" [DESIGN Part IV.7]. In UE this is a POSE-PER-FRAME system, not a clip: the stage holds a pose table `P[0..MAX_FRAME]` (40 frames, TIMINGS `seance_dock.gd MAX_FRAME`); frame N renders pose N; the transition N → N+1 is NEVER rendered (the render target updates only on a frame step). No blend, no interpolation, ever. The seance camera is fixed; the ladder is applied to the render target.

| # | State | Trigger | Asset | Timing | Must NOT |
|---|---|---|---|---|---|
| L-P0 | HOLDING STILL, cropped | the impossible tape's background (T4.4) | `PoseTable_Leland_Seance` pose 0: "legal pad against his chest. Holding still. Playing the game" at x = +1.35 m in the 4:3 frame | — | be centred; be uncropped; move within a frame |
| L-A1..5 | THE ANSWERS | each written question | pad material advances `MI_Leland_Pad_Qn`; Q1 "across four frames", Q4's second line "(next frame, smaller)", Q5 "(one frame, steady hand)"; the FIGURE changes pose between frames only (a hand higher on the pad, the head a degree turned) | MASTER T4.4; wear per answer [QA-22] | animate the writing; show the pen moving |
| L-G | GRIEF VARIANTS | Harriet dead → frame 14 PAUSED PROPERLY; Merle dead → frame 28 SHE'S HERE NOW; 1A's fourth answer I KNOW. SHE'S HERE NOW.; second answer SHE WAS THE ONLY ONE WHO PAUSED PROPERLY | pad material variants | QA-50; CASUALTY §MERLE/§HARRIET ENDINGS | — |
| L-E1A | ENDING 1A: WHOLE | 1A conditions | `AS_Leland_1A_StepToCentre` — the ONE clip on him that is continuous: he steps to centre of the 4:3 frame, uncropped, "a breath he does not need and takes anyway" (one chest rise on `spine_02`, the only breathing motion any human in this cast is permitted, because it is written) | MASTER §ENDING 1A | — |
| L-D1 | L1 THE SIXTH QUESTION | sixth question past wear 70 with five answers | material sequence: "print burns from the inside of the frames" (`MI_Leland_Burn`, an emissive-then-void sweep from the figure's interior outward, per frame), the pad's ink "drains upward" (ink mask scrolls up and out), D01 blanks | caption `[THE INK LEAVES THE PAPER]` [ACCESS §3.2]; QA-44 | fire, char, melt (REPAIRED-NOT-BURNED is the puppet's law, but here the idiom is PRINT burning: photochemical, not flame) |
| L-D2 | L2 THE READING | fire tape into the wake at the seance dock | pad sequence Q5→Q1 un-writing in reverse; final frame `PoseTable_Leland_Door`: the little door closing from the inside, his hand on the inner knob; caption `[THE SIGN-OFF, WHOLE]` | CASUALTY §LELAND L2; QA-44 | show his face in the door frame (a hand and a door) |
| L-R1 | NOT THAT ONE. PLEASE. | fire tape carried past his shelves (QUEUE) | a margin decal, no figure | REACT §LELAND | — |

**What must NOT move:** everything, between frames. Physics: none (the tape world is a render of a still craft world).

**UE drive.** `ALelandStage` (new): a `USceneCaptureComponent2D` into a 320 × 240 `RenderTarget` (pillarboxed 4:3 on the bench monitor via `M_Phosphor` [PIPE]), the figure on a pose table driven by `State->LelandAnswers` (STATE.h) and the seance frame index; the ladder material on the monitor takes generation from `SeanceWear`; captures happen only on frame steps. The bench notepad question → answer mapping is Phase 4's; the rig only needs the pose table and the pad materials.

### 4.5 ACCEPTANCE

- Sodium `--subject` on `SK_Leland` (he is a craft figure like the rest even though he is only ever seen through the format): knit, stripe cotton, satin tie, paper, laminate distinguishable; felt face.
- Beauty beside PLATE-LELAND at the plate's crop.
- UE: the STAGE capture — the render target at 320 × 240 with the ladder at G3, the figure cropped by the right edge at x = +1.35 m; a frame-step sequence of ≥8 frames where no two consecutive frames interpolate (pixel diff between frames shows a hard pose change, zero motion within a frame); the pad text legible at G1 and degraded-but-present at G3 on the bench monitor.
- Ending 1A capture: whole, centred, one chest rise measured on `spine_02` (the only allowed breath).
- Scale: bounds = authored height ± 1 cm (ESTIMATE 1.78 m); actor scale 1.0; the 4:3 framing reproduces the reference's crop (the box's 0.35 m width at 1.35 m off-axis is the reference framing to match).
- KEYART check: no capture of his face leaves `docs/telemetry/`.

### 4.6 RISKS / OPEN

- C-6 (tenure), C-7 (voiced endings), height ESTIMATE 1.78 m, OPEN-C1; OPEN-L1: which frame edge crops him (reference right, plate left).
- Risk: a pose table with 40 hand-authored poses is animation by stills; if a pose is "in-between" it reads as a blend and the frame law dies. Author every pose as a held, composed still.
- Risk: the ladder must never be baked (ART §2); a pad texture with baked grain will look right on the monitor and be wrong at G0.

---

## 5 · RITA IVORI · TAPE CONSERVATOR (unit 2.6, the player)

### 5.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Who | "Professional. Patient. Precise. What others discard, she restores … Her tools are the dresser's seven, confirmed: cotton gloves, the 10x loupe, splicing block, leader tape, the archival binder, isopropyl and swabs, clipboard and accession forms" | SHEETS §RITA |
| What is ever seen | "First person, so Rita's design is her hands, her tools, and her rare reflections. Her hands are the most animated character in the game: white cotton conservator gloves (the iconic archival image), sleeve garters, a jeweler's loupe on a lanyard that swings into frame when she leans in. Wardrobe glimpsed at mirrors and dead CRTs: work apron over practical clothes, hair pinned with a film-can lid clip" | DESIGN Part I · Rita |
| The reflection budget | "her reflection budget is scripted and scarce. Early game, dead CRTs reflect her normally. From Tape 3 onward, her reflections begin composing better: centered, headroom correct, rule-of-thirds. Nobody comments" | DESIGN Part I · Rita |
| Physical vocabulary | "Rita adjusts her gloves at decisions; the loupe swings into frame when she commits"; "(the gloves, squared one last time)" | MASTER header; T5.4 |
| Avert | "hold to raise Rita's clipboard, blocking direct sight while preserving movement at a slow walk … reading your own notes is how you hide"; "clipboard raise runs about 200ms with an ease-out" | DESIGN Part IV.2; Part V Feel Notes |
| Gloves | "her gloves are the whitest object in the game"; "RITA: player wardrobe never drifts" | ART §5 |
| Key art | "She is a needle-felt figure; her white gloves are the brightest object in frame" | KEYART §HERO COMP A |
| The seven | "Watch, pen, photograph, lighter, compact, keys, loupe. One vanishes per capture, loupe last" | INVENTORY §5; WALK Part V-B |
| Voice | "minimal lines, breath-first acting; recorded dry on the WORLD bus"; the response pools are her only speech | AUDIO §5; MASTER App. C |
| LAWS | 7 (every death is her choice), 8 (the one lie is spent on her menu), 9 (access), 10/11 (she is the one under the tally and behind the felt door) | LAWS 7–11 |
| Endings | 1B "Rita in frame, in palette, at rest, the composition finally satisfied with her"; 4b "her arm never fully works again, stated flatly"; 0 "every role's title card reads RITA IVORI" | MASTER §ENDING 1B; CASUALTY §FLOOR MANAGER ENDINGS, §THE FULL BOARD |
| Feel | walk 3.10 m/s, crouch × 0.55 = 1.71 m/s, camera drop 0.60 m eased at 12/Δ, reach 2.6 m; crouch "a body verb, useless against him by architecture" | RITA.h header; TIMINGS `player.gd`; QA-58 |

### 5.2 WHAT EXISTS

| Item | State | Source |
|---|---|---|
| UE | `ARitaCharacter : ACharacter`: capsule 35 × 88 uu, camera at relative Z 72 (eye 160 − 88 = 72; "eye 1.60 m over the floor"), `MaxWalkSpeed 310`, crouched 170.5, `CrouchedHalfHeight 88 − 30`, camera Z `FInterpTo` at 12/s, reach ray 260 uu dispatching `IRestorationInteractable`; no mesh, no hands, no arms | RITA.cpp 15–31, 95–101 |
| Godot | capsule + camera, no figure; camera y 1.6 (`main.tscn`) | DOSSIER §2.1; BRIEFS §0.1 OPEN 0-B |
| Parity | "feel parity proven to the digit (walk 3.10 m/s, crouch 1.71, cam drop 0.60m …)" | PROGRESS 0.8b-1 |
| Bench | `ABenchCapture`: 12 s forced-real-time capture, 4 m tether abort | PROGRESS 0.8b-2 |
| Reflection | none built; dead CRTs are Phase 3 props | — |

### 5.3 BUILD BRIEF

Rita is THREE assets, because the game shows three different things of her:

| Asset (proposed) | What | Seen where |
|---|---|---|
| `SK_Rita_Hands` | first-person forearms + gloved hands, sleeve protectors to the elbow, the loupe on its lanyard, the clipboard; camera-attached | always; "the most animated character in the game" |
| `SK_Rita_Reflect` | the full body, for mirrors and dead CRTs only; low-detail below the waist | "rare reflections", scripted; Tape 3+ composed better |
| `SK_Rita_Frame` (the same mesh as Reflect at hero detail) | the stills of ending 1B "in frame, in palette, at rest"; ending 0's title cards; the premiere's "on camera" monitors (she is on the PGM feed in T5.3) | endings; monitors |

**Silhouette (from PLATE-RITA, full-body).** Dark ribbed turtleneck; dark denim bib apron with a RESTORATION name tag on the bib and a pocket at the hip; white cotton sleeve protectors elasticated to the elbow; white cotton gloves; two loupes on a lanyard at the sternum (the plate shows a paired brass loupe); a wooden clipboard with steel clip and an accession form in the left hand; a reel held up in the right; dark work trousers; brown leather lace-up boots; hair pinned up with a round metal film-can-lid clip at the crown [PLATE-RITA].

| Measure | Value | Status |
|---|---|---|
| Height | canon: **OPEN-3**. The engine's eye is 1.60 m (RITA.cpp 31 comment; PROGRESS 0.8b-6 P4) → a body whose eye sits at 1.60 m is ~1.70 m tall by ordinary proportion. **ESTIMATE from the plate: ~1.70 m** (full-body standing; head ~1/7.5) — consistent with the eye height; a placeholder | OPEN (owner) |
| Eye height | 1.60 m (Godot; UE target after 0.8b-6 P4); today UE 1.48 m (OPEN 0-B) | BRIEFS §0.1; RITA.cpp 31 |
| Hand/glove scale | canon none (OPEN-3) — the first-person hands must match the reach ray (2.6 m) and the bench's prop scale; author the glove at a real conservator's glove (women's size 7 ≈ 180 mm palm-to-fingertip) and log it as a working number | OPEN |
| Head-to-body | 1 : 5.5 for `SK_Rita_Reflect` (OPEN-C1); for `SK_Rita_Hands` the ratio is irrelevant but the HAND must be a felt-figure mitten with a glove over it (OPEN-1 applies hardest here) | ART §6 |
| Hands | ART §6 names principals for stitched fingers as Merle, Vess, Harriet — Rita's hands are gloves; the glove's finger seams are the glove's, not the figure's. Whether her gloved hands are mittens or five-fingered is **OPEN-R1** (the plate shows five-fingered gloves; canon says felt figure; the DESIGN calls the hands "the most animated character") | OPEN (owner, in 2.1) |

**Materials.**

| Need | Candidate (id · source · licence) | How |
|---|---|---|
| WHITE COTTON GLOVES (the whitest object in the game) | `Fabric032` (white wool cloth) · AmbientCG · CC0 or `Fabric019` (white wool weave) · AmbientCG · CC0 as the knit ground; `Fabric001` (old white cloth) for the worn cuff; `garden_gloves_01` (worn gloves, 226×299 mm) · Poly Haven · CC0 as a TOPOLOGY donor only (seams, cuff, thumb gusset), retextured white | albedo must be the brightest value in any frame [ART §5]; never grey; grime only at the fingertips after captures (a `Wear` param, tiny) |
| Sleeve protectors, white cotton, elastic at the elbow | `cotton_jersey` · Poly Haven · CC0 tinted white; `Fabric081C` (plastisol white) for the elastic band | |
| Ribbed turtleneck, dark brown | `cotton_jersey` (ribbed) · Poly Haven · CC0 tinted dark; `jersey_melange` · Poly Haven · CC0 | seen at the sleeve above the protector and in reflections |
| Denim bib apron, dark, worn | `denim_fabric_06` (dark worn denim twill) · Poly Haven · CC0; `denim_fabric_05` for the trousers | the plate's apron is black-blue denim with worn seams |
| RESTORATION name tag | `Paper001` under `Plastic013A` laminate; readable | |
| THE LOUPE (10×, brass and glass) | `magnifying_glass_01` · Poly Haven · CC0 (lens + rim donor); `pocket_watch` / `vintage_pocket_watch` · Poly Haven · CC0 for the brass folding-case profile (the plate's loupe is a folding jeweller's loupe); brass `Metal042B` / `Metal048B` (dirty gold, fingerprints) · AmbientCG · CC0; lens glass `M_Practical` (fixture glass) [PIPE] | on `prop_loupe` at the end of the lanyard (`Rope001` · AmbientCG · CC0 on a curve) — it swings |
| THE CLIPBOARD (the avert shield) | `clipboard` (metal, scratched, 228×336 mm) · Poly Haven · CC0 for the clip; board `Chipboard004` · AmbientCG · CC0 or `Wood049` (oak) · AmbientCG · CC0 (the plate's is wood-backed); the accession form `M_Paper`, 4K readable ("the clipboard is also where session notes live") | `SK_Rita_Hands` prop on `prop_clipboard`; the notes are session text (Phase 4) |
| Boots, brown leather | `Leather014` (brown, old, scratched, scuffed) · AmbientCG · CC0; `rubber_boots` · Poly Haven · CC0 as a last/sole donor | reflections only |
| Film-can lid clip | `Metal049B` (dirty silver) · AmbientCG · CC0; a 40 mm disc with the can lid's rolled rim | reflections; "a detail players will find eventually" |
| Needle-felt head (Reflect) | as Merle; the face is the one the player sees composed better each tape — it must be a felt face that can be lit like a portrait | KEYART §HERO COMP A: "She is a needle-felt figure" |
| Reels (held) | Fab "film reel" (shared) | |

**Drift.** None, ever: "player wardrobe never drifts" [ART §5]. `MI_Rita_*` has no `Drift`. Ending 1B "in palette" is a separate `MI_Rita_Frame_InPalette` used once.

**Blender steps.**
1. `SK_Rita_Hands`: forearms from the elbow, gloves over mitten-or-fingered hands (OPEN-R1), sleeve protectors as a solid cuff (cloth-simmed, frozen), the lanyard as a bevelled curve with a chain of small bones, the loupe from the donors, the clipboard from the donors; authored in the camera's space at the UE eye (Z 160 uu after 0.8b-6) with the reach ray in mind.
2. `SK_Rita_Reflect`: the full figure at the ESTIMATE (1.70 m) on the shared skeleton, hero-detail head and torso, simplified legs; the same gloves.
3. Glove albedo: bake with the white clamped so no texel drops below the bench paper's value (the ART rule is measurable: "whitest object in the game").
4. Bakes 2K; the accession form 4K.
5. Sodium `--subject` on both meshes (white cotton under sodium is the hardest fibre to make honest: it must read as knit cotton, not as plastic); beauty at the bench framing of KEYART HERO COMP A (over the shoulder, gloves brightest) → export → capture.

**BANNED.** Grey gloves. Drift on any garment. A visible body in first person outside reflections (no legs when looking down: canon shows "hands, tools, rare reflections" and nothing else — OPEN-R2 whether a downward look shows the apron). Reflections that appear anywhere a script did not place them ("her reflection budget is scripted and scarce"). Any face on Rita that reads photoreal (the key art says felt). Button eyes.

### 5.4 RIG & ANIMATION SPEC

**`SK_Rita_Hands` bones:** `camera_root, upperarm_l/r (stub), lowerarm_l/r, hand_l/r, thumb_01/02_l/r, fingers_l/r (or index..pinky chains if OPEN-R1 rules five-fingered), prop_clipboard (child of hand_l), lanyard_01..06 (chain from `camera_root` at the sternum), prop_loupe (child of lanyard_06)`. Physics: the lanyard chain is the ONE simulated thing on the player (AnimDynamics, damped; "swings into frame when she leans in"); everything else authored.

**`SK_Rita_Reflect` bones:** the shared skeleton plus `prop_clipboard`, `lanyard_*`, `prop_loupe`, `hairclip` (rigid on `head`).

| # | State | Trigger | Clip / asset | Timing tied to | Must NOT |
|---|---|---|---|---|---|
| R-P0 | HANDS IDLE (walk / stand) | movement | `AS_RitaHands_Idle`, `AS_RitaHands_Walk` (a gentle arm carriage; the loupe pendulum does the rest) | walk 3.1 m/s; crouch 1.71 | bob the camera (no camera bob exists in the reference; "Reduced-motion setting flattens all camera sway", DESIGN Part V) |
| R-A1 | AVERT (clipboard up) | hold LB / Q | `AM_RitaHands_ClipboardRaise`: the clipboard rises to fill the lower two-thirds of frame; "blocking direct sight while preserving movement at a slow walk" | "about 200ms with an ease-out" [DESIGN Part V Feel Notes]; slow-walk speed OPEN (no constant in TIMINGS) | snap (the ease-out is the feel); block the whole frame |
| R-A2 | THE GLOVE ADJUST (decisions) | decision-point commits (AUTHENTICATE / DESTROY / PERFORM; the ledger signs) | `AS_RitaHands_GloveAdjust`: one hand tugs the other's cuff, squared | "Rita adjusts her gloves at decisions" [MASTER header]; T5.4 "the gloves, squared one last time" | become an idle tic (it is a decision beat only) |
| R-A3 | THE LOUPE COMMIT | commit at the bench (hold X / hold E) | the lean-in brings the lanyard forward; the loupe "swings into frame when she commits" — physics plus an authored lean | bench commit hold [DESIGN Part V] | — |
| R-A4 | CROUCH | toggle | camera drop 0.60 m at `FInterpTo` 12/s (already built); hands follow the camera | RITA.cpp 95–99 | imply concealment (QA-58) |
| R-B | BENCH VERBS | bake / splice / capture / jog | `AS_RitaHands_Splice`, `_Jog`, `_Tension`, `_Capture` (12 s hold with tracking adjustments) | CAPTURE_SECONDS 12.0, TETHER 4.0 [TIMINGS] | skip; the capture is real time |
| R-Q | THE QUIET GAME | hold RB rhythm / mic | hands still; the breath is audio (mic or button rhythm) | DESIGN Part IV.5 | any hand motion during stillness checks (StillSpeed 0.4 m/s, ACCESS §5.2) |
| R-S | THE SWITCHER (finale) | face buttons | `AS_RitaHands_Switcher_*` per button bank | DESIGN Part V · Switcher | — |
| R-F | ON CRAIK'S MARK (T5.3, Reflect/Frame on the PGM monitor) | premiere | `AS_RitaFrame_OnMark`: standing on the mark, gloves squared, reading the prompter | — | look at the club |
| R-R | REFLECTIONS (Tape 1–2 normal; Tape 3+ composed) | scripted mirror/CRT | `SK_Rita_Reflect` rendered only in the scripted reflection captures; from Tape 3 the reflection camera re-frames: centred, correct headroom, thirds | DESIGN Part I · Rita | comment; reflect in unscripted surfaces |
| R-D | DEATH (a capture) | strike | the camera goes to tape: "bars, head-switch noise, playback of Rita's final seconds from an angle no camera occupied" — that playback is `SK_Rita_Reflect` seen from the Coverage Director's angle | WALK Part V-B | gore |
| R-E1B | ENDING 1B stills | 1B | `SK_Rita_Frame` in palette, at rest, composed | MASTER §ENDING 1B | — |
| R-E4b | ENDING 4b | her hand held the fader | "her arm never fully works again, stated flatly" — a card, not a pose | CASUALTY §FLOOR MANAGER ENDINGS | animate the injury |

**Shadow.** Canon names hands, tools and reflections; it does not name her shadow. The lighting bible makes HIS shadow a mechanic ("HIS SHADOW IS A MECHANIC", LIGHT §HIM) and says nothing of hers. **OPEN-R3**: whether `ARitaCharacter` casts a body shadow (a `SK_Rita_Reflect` shadow proxy) or only the hands'. Default until ruled: hands cast, body does not (nothing in canon shows her shadow; a wrong shadow would be a lying image).

**UE drive.** `ARitaCharacter` gains a first-person `USkeletalMeshComponent` (owner-only-see) attached to `Camera`; the reflection body is a second component (owner-no-see) enabled only inside scripted reflection volumes; avert / adjust / commit are input-driven montages; the bench verbs are `ABenchCapture`'s (0.8b-2). Constants stay in `RitaCharacter.h` and TIMINGS ("every number in the playtest protocol's knob list", ACCESS §5.2 quoting `UE5-MIGRATION-MAP.md`).

### 5.5 ACCEPTANCE

- Sodium `--subject` on `SK_Rita_Hands`: the glove reads as knit cotton (weave visible at 1 m, matte, no plastic sheen), the sleeve protector as a different white (finer), the loupe as brass + glass (two roughness regimes), the clipboard as wood + steel + paper.
- The whitest-object test: in the KEYART HERO COMP A framing at the bench (locked EV, night, task lamp), a luminance read of the frame: the glove texels are the maximum non-emissive value in frame (the monitor is emissive and excluded).
- Beauty beside PLATE-RITA (full body, `SK_Rita_Reflect`) at the plate's framing; then the reflection framing test: a dead CRT reflection at Tape 1 (normal) vs Tape 3+ (centred, headroom, thirds) — two captures, the composition difference visible, no text.
- UE: the avert montage timed at 200 ms ± one frame with an ease-out (F-curve review); the loupe pendulum swings into frame on the bench commit (≥8-frame capture); the feel test (`bTestAutoWalk`) still reports 3.10 / 1.71 / 0.60 with the mesh attached; the crouch drop at 12/s.
- Scale: reach ray 260 uu lands on the bench interactables with the hands visible at the correct size; `SK_Rita_Reflect` bounds = 1.70 m ESTIMATE ± 1 cm; eye height 160 uu after 0.8b-6 P4.

### 5.6 RISKS / OPEN

- OPEN-1 (felt vs photoreal — hardest on the one face the player studies in reflections), OPEN-3 (age, height ESTIMATE 1.70 m, hand scale), OPEN-R1 (mitten or five-fingered gloves), OPEN-R2 (downward-look body), OPEN-R3 (body shadow), OPEN 0-B / 0-C inherited.
- Risk: first-person hands are the most-seen asset in the game and the one with no canon dimensions. Every bench prop's scale (Phase 3) will be judged against them. Lock the glove size in 2.6 and write it on the wall as 0.2 wrote the cube.
- Risk: white cotton under sodium and Lumen: a white glove that blooms or greys fails ART §5 in the ACCEPTANCE VIEW even if Cycles passes. Test in the dark locked-EV rig first.

---
## 6 · THE FLOOR MANAGER (unit 2.6 variant)

### 6.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Who | "Never named, face never fully lit, headphones with a coiled cable connected to nothing, laminated run sheet. Communicates only in countdowns and real television floor-manager hand signals: stretch, wrap it up, cut, thirty seconds, you're on … The scariest character in the game never touches anyone; they just count things in and out of existence" | DESIGN Part I · The Floor Manager |
| The vocabulary is UI | "the Floor Manager's hand signals are the game's threat-telegraph UI … Threat information is delivered by a silent character's hands" | DESIGN Part I; Part IV.3 |
| The six + the seventh | YOU'RE ON (the point), CUT (the slash), STRETCH (taffy hands), WRAP IT UP (the circle), THIRTY SECONDS (the T), ON TIME (the nose touch); HOLD YOUR APPLAUSE (both hands pressed flat, pushed down twice), "known only through Harriet" | MASTER T2.4; App. C Signal glossary |
| Arc | "No arc, which is the point. They count things in and out for five acts. After the sign-off completes, they remove the headphones, and the game ends before showing anything further" | WALK Part I · The Floor Manager |
| Physical vocabulary | "The Floor Manager is hands and countdowns, nothing else" | MASTER header |
| Sound | "S12 Floor Manager. LAW: never heard moving. No footsteps, no cloth. His only audio is the room refusing to acknowledge him"; "Floor Manager: silent, contractually" | AUDIO §3 S12; §5; §8 |
| Spoken inventory | "'In five, four...' (three, two, one are hands). Nothing else, ever" (vs the reference "nothing, here" — C-8) | MASTER App. C; FM.gd 4 |
| Wardrobe | "FLOOR MANAGER: absolute black-adjacent neutrals forever, outside the palette system entirely, the way he is outside everything" | ART §5 |
| LAW 2 | the point is a tell, not a startle; he never lunges or pops | LAWS 2; DOSSIER §3 |
| LAW 7 | F1 "found after with his headset still cued, arm locked in a YOU'RE ON point at a camera that faces nothing, finished the way a gesture is finished, not a life". F2 "he exists only in the program feed, visible in monitors giving cues to rooms he is not in, and his freeze-check mechanic INVERTS: stillness near monitors now draws his point" | CASUALTY §THE FLOOR MANAGER |
| LAW 9 | the signals read by shape and position; the watch honours assist-hold | ACCESS §5.2; DESIGN Part III · Captions ("Tally states carry shape and position, never color alone") |
| Reaction | F-R1 "HE POINTS AT THE DOORWAY seconds before the first fold a player ever sees" (QUEUE); F-R2 gives the empty half Harriet's mark (QUEUE) | REACT §THE FLOOR MANAGER |
| Pronoun | "they" (DESIGN, WALK) vs "he" (CASUALTY, REACT) — OPEN-5; this brief says "the FM" | DOSSIER §1 |
| No plate | "The cast sheet set is complete at five" — the FM has none; KIT is the only visual reference | SHEETS §HARRIET |
| Ambient | a worn mark on the Studio A floor paint "decades deep"; two headset hooks, "one is bent straight and retired in place [and the FM uses the other]" | INVENTORY §12; AMBIENT §MASTER CONTROL |

### 6.2 WHAT EXISTS

| Item | State | Source |
|---|---|---|
| Godot brain | `FloorManager` (Interactable): visible iff `is_night and Broadcast.on_air and not premiere_live`; the whole rig yaws to face the player at `lerp_angle` 4/s; within 9 m and facing (dot > 0.5) → `_pointed`, `_watch_t = 3.0`, label YOU'RE ON; the arm lerps to `rotation.x = −π/2` at 6/s while a watch runs, back to 0 after; moving > 0.4 m/s during the watch spoils the take unless assist-hold; `_pointed` resets on night change; interact marks D08 read | FM.gd 27–94 |
| Godot figure | `CharacterKit.floor_manager()` → `{rig, arm}`: blacks (0.08, 0.075, 0.07), `rig.scale (1.0, 1.08, 1.0)`, dark work jacket, left arm "clutch" with the run sheet box yawed 0.6 rad ("angled away, always"), the right arm as a pivot Node at (0.2, 1.17, 0) with two capsules and a hand, head (0, 1.44, 0) under a cap (a squashed sphere + brim box), headset band torus, earcups, boom, mic sphere, six coil tori "descending to nowhere" | KIT 808–873 |
| Placement | TAPE LIBRARY (−4.5, 0, −19.4) "at the stack's end" → UE (−450, −1940, 0); capsule 0.3 × 1.7 | WB 1123–1125; FM.gd 28–33 |
| Assist constants | StillSpeed 0.4 m/s; hold-`IA_Interact` counts as still; the FM rules instantly (no 0.3 s grace) | ACCESS §5.2 |
| Captions | `[YOU'RE ON · TO NOTHING LISTED]` (premiere) | ACCESS §3.2 |
| UE | no actor, no mesh | — |

### 6.3 BUILD BRIEF

**Silhouette and proportions (no plate; the reference build plus the text).** A figure in black-adjacent neutrals: dark cotton work jacket, dark trousers, a dark cap whose brim keeps the face in its own shadow; an over-ear headset with a boom mic and a coiled cable that descends and ends in nothing; the laminated run sheet in the left hand, angled away; the right arm hanging, or pointing [KIT 808–873; DESIGN Part I; PROPS D08]. Face: "never fully lit" — the felt face exists but the cap brim, the headset and the lighting keep it in shadow; the eyes are embroidered, not beads (a bead would catch a highlight and light the face — a reading of the canon, logged as OPEN-F1).

| Measure | Value | Status |
|---|---|---|
| Height | canon: **OPEN-4-class (none stated; no plate)**. Reference ≈ 1.69 m (base × 1.08), capsule 0.3 × 1.7 [KIT 823; FM.gd 28–33]. **No plate estimate is possible; this brief carries the reference 1.69 m as a placeholder and labels it REFERENCE, not estimate** | OPEN (owner) |
| Arm pivot | shoulder at (0.2, 1.17, 0) m in rig space; raised = −π/2 (horizontal point) | KIT 835–840; FM.gd 60–62 |
| Head-to-body | 1 : 5.5 (OPEN-C1) | ART §6 |
| Hands | mitten, no stitched definition (not a principal) — the signals are read "by shape and position" [DESIGN Part III], so the mitten silhouette must carry the six shapes: the point (index extended) needs at least an index bone — **OPEN-F2**: the FM's mitten needs one articulated index finger for THE POINT and THE T; ART §6 does not forbid it (it reserves stitched DEFINITION, not articulation) | ART §6; MASTER App. C |
| Capsule | radius 30, half-height 85 uu | FM.gd |

**Materials.**

| Need | Candidate (id · source · licence) | How |
|---|---|---|
| Blacks: work jacket, trousers | `Fabric049` (black polyester) · AmbientCG · CC0; `Fabric004` (black carbon-weave) · AmbientCG · CC0 as an alternate; `denim_fabric_05` · Poly Haven · CC0 desaturated to near-black for the twill | (0.08, 0.075, 0.07) [KIT 816]; "black-adjacent" — value 0.06–0.10 linear, never 0 |
| Cap | `Fabric043` (grey rough) · AmbientCG · CC0 tinted near-black; brim `Plastic012A` core under cloth; **no cap donor on either API (checked)** (`fishermans_hat` is a wide brim) — build a flat cap/work cap by hand: bevelled, edge-worn; Fab "work cap", "flat cap", "newsboy cap" | brim length is the face-shadow tool |
| Headset | **no headphone/headset donor on either API (checked)**; build: band `Plastic012B` (scratched black) · AmbientCG · CC0, earcups `Leather026` (black smooth) · AmbientCG · CC0 pads over `Plastic006` shells, boom mic `Metal049B`; Fab "intercom headset", "vintage headphones", "broadcast headset" | 1970s studio intercom headset; the cable jack ends in air |
| Coiled cable to nothing | a helix curve, six loops per the reference, bevelled, `Plastic006` (shiny black) · AmbientCG · CC0; the end is a bare jack `Metal049B` hanging in air | KIT 865–872 |
| THE RUN SHEET (D08) | `Paper001` (white) · AmbientCG · CC0 under a laminate clearcoat (low roughness, a scratch layer from `Plastic013B`); grease-pencil marks authored; text per PROPS D08: "SEG 4 … :22 / SEG 5 … :41 / SEG 6 … :63 [sic by design] / SIGN-OFF … [grease smear]" | a readable that the player reads "at most one column edge" of; 4K |
| Needle-felt face in shadow | `Fabric034` felt tinted the reference's shadow skin (0.42, 0.35, 0.3) [KIT 811]; embroidered eyes (OPEN-F1) | |
| The worn floor mark (Studio A) | dressing: a decal on the studio floor paint | INVENTORY §12 |

**Drift.** None, ever: "outside the palette system entirely" [ART §5]. No `Drift` parameter on any `MI_FloorManager_*`.

**Blender steps.**
1. Block at the REFERENCE 1.69 m; the shared skeleton; the point pose authored first (it is the character).
2. Jacket and trousers as solid garments; the cap with a real brim; the headset from bevelled parts; the coil as a curve.
3. The run sheet as `SM_FM_RunSheet` on `prop_runsheet`, angled 0.6 rad away from the figure's front (KIT 833: `sheet.rotation.y = 0.6`).
4. Head: felt sculpt with the cap; no bead eyes (OPEN-F1); the boom mic in front of the mouth.
5. Bakes 2K; the run sheet 4K.
6. Sodium `--subject` (blacks are the sodium test's hardest case: black cloth must show weave and nap, or it reads as a hole) → beauty → export → capture at the stack's end at night ON AIR (TAPE LIBRARY stack-end lamps, ROOMS §TAPE LIBRARY).

**BANNED.** A lit face. Any footstep, cloth or breath audio component on the actor (S12; AUDIO §8 silence ledger). A walk cycle: the reference "teleports nothing — he simply is at the stack's end when visible" [DOSSIER §2.6]; if 2.9 ever needs him to move between rooms, the move happens off-screen or the whole move is a cut, never a seen walk (OPEN-F3). Any signal delivered by colour. Bead eyes (OPEN-F1). A pop: the point is a rise at lerp 6/s, and the body turn a lerp at 4/s — both smooth, both slow, both readable before they complete.

### 6.4 RIG & ANIMATION SPEC

**Bones (shared skeleton, plus):** `prop_runsheet` (child of `hand_l`), `headset` (child of `head`, rigid), `boom` (child of `headset`, pose-only), `coil_01..06` (chain from `headset`; pose-only — a coil that swings would imply a body that moved, and he is never heard moving), `cap` (child of `head`, rigid), `index_01/02_r` and `index_01/02_l` (OPEN-F2: the pointing fingers).

**Motion states (FM.gd → `AFloorManager`).**

| # | State | Trigger | Clip / asset | Timing tied to | Must NOT |
|---|---|---|---|---|---|
| F-P0 | STANDING at the stack's end | `bIsNight && Clock->IsOnAir() && !bPremiereLive` → visible | `AS_FM_Stand`: a statue; run sheet angled away; arm down | FM.gd 49 | idle sway; breathe; shift; ever be seen arriving |
| F-P1 | THE TURN | player within 9 m | actor yaw `lerp_angle` toward the player at 4/s ("the whole body turns to face you, always") | FM.gd 55–58 | turn faster; turn the head alone (the whole body turns) |
| F-S1 | YOU'RE ON (the point) | facing dot > 0.5 within 9 m, once per night | `AS_FM_Signal_YoureOn`: the right arm rises to horizontal at lerp 6/s, index extended; holds for the watch; lowers at 6/s after | watch 3.0 s [FM.gd 65]; "The hand lowers. The take holds." | pop; rise faster than the lerp; point with the left (the left holds the sheet) |
| F-S2..6 | CUT, STRETCH, WRAP IT UP, THIRTY SECONDS, ON TIME | premiere / night cues (Phase 4/5 wiring) | `AS_FM_Signal_Cut` (the slash across the throat), `_Stretch` (taffy hands: both hands pull apart — the sheet is tucked under the arm for the two-handed signals, OPEN-F4), `_WrapItUp` (the index circles), `_ThirtySeconds` (the T: fingers of one hand flat on the other's tips), `_OnTime` (the nose touch) | "real television floor-manager hand signals" [DESIGN Part I]; durations OPEN | read by colour; be ambiguous in silhouette at 9 m (test at 9 m, ACCEPTANCE) |
| F-S7 | HOLD YOUR APPLAUSE (the seventh) | T4.9 if Rita holds Harriet's seventh signal; premiere | `AS_FM_Signal_HoldApplause`: both hands pressed flat, pushed down twice; the sheet goes under the arm | "Three seconds of grace" [MASTER T4.9] — the signal must complete within the 3 s | a third push |
| F-C | THE COUNT | "In five, four..." (three, two, one are hands) | `AS_FM_Count`: the voice line (C-8) then three fingers folding down on the raised hand — the count IS the hand | MASTER App. C | any other line, ever |
| F-D1 | F1 THE FADER | DEAD AIR, by omission | `AS_FM_F1_Locked`: "headset still cued, arm locked in a YOU'RE ON point at a camera that faces nothing, finished the way a gesture is finished" — the point pose held permanently, at the fader position | CASUALTY §THE FLOOR MANAGER F1 | slump; any pose but the point |
| F-D2 | F2 THE UNLISTED CAMERA | third blind tally call | the actor is HIDDEN in the world; a `SK_FloorManager` instance renders ONLY into the program-feed render target, giving cues in monitors "to rooms he is not in"; the watch INVERTS: stillness near monitors draws his point | CASUALTY F2; QA-43; caption `[YOU'RE ON · TO NOTHING LISTED]` | harm; a jump; be in the room and on the monitor at once |
| F-E | ENDING 1A | sign-off complete | `AS_FM_RemoveHeadphones`: both hands lift the headset off; the game ends "before showing anything further" — the clip's last frame is the cut | MASTER §ENDING 1A; WALK Part I | show his face lit as the headset comes off (the cap brim stays) |
| F-R1 | THE EARLY POINT (QUEUE) | seconds before the first fold a player sees | `AS_FM_Signal_YoureOn` aimed at the doorway, no watch | REACT §THE FLOOR MANAGER | — |

**What must NOT move:** the coil; the sheet's angle relative to the player (it is re-angled away if the turn would expose it — the turn keeps it away by construction); the face; the feet (he never walks on screen).

**UE drive.** `AFloorManager : AActor, IRestorationInteractable` ports FM.gd: visibility from `State->bIsNight`, `Clock->IsOnAir()`, `State->bPremiereLive`; the 9 m / dot 0.5 / 3.0 s watch; the spoil rule `velocity > 0.4 m/s && !(Assist && IA_Interact held)` (ACCESS §5.2 mercy 2, the FM "rules instantly"); enum `{Stand, Point, Signal_n, Count, F1, F2, RemoveHeadphones}`; the AnimBP reads the enum and an `ArmAlpha` the actor lerps at 6/s (so the rise speed is the brain's, not the clip's); actor yaw lerped at 4/s. F2's feed-only rendering is a `SceneCapture` visibility flag (owner-no-see on the world camera, visible to the PGM capture) — the presentation half's.

### 6.5 ACCEPTANCE

- Sodium `--subject`: the blacks show weave and nap (three-way response on a near-black cloth: this is the unit's real test); the laminate reads as laminate over paper; the headset plastics and leather pads distinct; the felt face in shadow still reads as felt where the brim's shadow ends.
- Beauty: no plate — the reference `cast_preview` framing beside the KIT build; the owner signs the silhouette.
- UE locked-EV night ON AIR capture at (−450, −1940, 0): the face unlit under the stack-end lamps (a luminance read of the face region below the readable floor); then the SIGNAL LEGIBILITY TEST: each of the seven signals captured from Rita's eye at 9 m and at 3 m, in silhouette (a black-on-dark figure): a reviewer names each signal from the still alone (DESIGN Part III "shape and position, never color alone").
- Motion: the point's rise measured at lerp 6/s from an ≥8-frame capture; the turn at 4/s; the watch: QA-19 (fails on movement, passes on assist-hold) in simulate; NO audio component on the actor (a static check: the actor has no `UAudioComponent`, no footstep notify, no cloth).
- F1 capture: the locked point at the fader, held 60 s, zero motion.
- Scale: bounds = 1.69 m REFERENCE ± 1 cm; actor scale 1.0.

### 6.6 RISKS / OPEN

- OPEN-4 (age), OPEN-5 (pronoun), C-8 (the count line), OPEN-F1 (embroidered vs bead eyes), OPEN-F2 (an articulated index for the point and the T), OPEN-F3 (does he ever visibly move between rooms; the reference never does), OPEN-F4 (where the run sheet goes during two-handed signals), height REFERENCE 1.69 m.
- Risk: a black figure in a dark room under locked EV is a hole in the frame, not a character. The brief's answer is the sodium test's answer (nap and weave on the blacks) plus the stack-end lamps; if the silhouette does not read at 9 m the telegraph UI fails and with it LAW 9.
- Risk: the point must be the slowest, most readable motion in the game and still be frightening; if animators add anticipation it pops (LAW 2). Curve review: a single lerp, no overshoot.

---

## 7 · CHUM · THE 1974 STAGE PUPPET (unit 2.7)

### 7.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Base design | "brown boiled-wool body, triangle ears with contrasting inner-ear patches (mustard left, navy right), a round head with a visible center seam, one amber glass cat eye (viewer left) and one black four-hole button (viewer right), a small dark nose, three twisted-string whiskers per side, and a cross-stitched grin of small X ticks along the smile curve. Hand-cut felted patches over the body: rust at the chest, green at the right side, a large tan belly circle (his most huggable feature), blue at the arm, plum at the thigh, mustard toe caps, navy at the tail tip, all in contrasting blanket stitch. Thin brown collar with a brass keyhole bell that never rings. It rings exactly once in the entire game, in Tape 5" | DESIGN Part I · Chum |
| Era | "1974 peak · Professional rebuild, the icon · 12 patches, collar and bell added (silent), symmetric cross-stitch grin, amber eye viewer-left" | DESIGN era table |
| The RFQ body | "Form: a patchwork cat, seated height 55 cm, hand puppet with rod-arm option. Exterior: brown wool, hand-patchwork over a stuffed muslin core; visible hand-stitching throughout; nothing may read machine-made at 30 cm. Armature: wire in ears, tail, and spine; neck poseable and repeat-accurate; paws weighted. THE MOUTH DOES NOT ARTICULATE … Eyes: viewer-left, amber glass, taxidermy grade, 14 mm; viewer-right, black four-hole button, 18 mm, attached with visible waxed thread. Whiskers: fine wire, six per side. Bell: brass, 25 mm, at the collar, SUPPLIED SILENT" | FABRIC §3 (whiskers and jaw conflict with DESIGN/MOTION: C-9, C-10) |
| Kits | "1971 NEW (unworn finish) and 1974 LOVED (authored wear pass: hand-polish on grip zones, sun-fade crown, one visible early patch)" | FABRIC §2 D2 |
| Two bodies | "the stage puppet, hand-sized, the one in the footage, the one the tell-table catches lying about being repaired" — NOT the mascot | AF §WHAT IT IS; P1 §0.5 |
| Motion, pre-fire | "PERFORMED FOR CAMERA … anticipation, overshoot, bounce-and-settle. Head tilts land in clean fifteen-degree stops. The jaw flaps a half-beat off the phonemes … secondary motion everywhere (ears lag, whiskers tremble, the bell answers every gesture). Curve language for animators: ease-heavy, bouncy, generous. In-game, the stage body never animates; it participates in L1 drift only (a head angle that is not yesterday's)" | MOTION §PRE-FIRE |
| The rig | "the stage puppet rig carries full secondaries and cloth"; "SK_Chum_Stage ships with cloth and secondary physics enabled … stage clips ease-heavy" | MOTION §PRODUCTION NOTES; PIPE-PROD ADDENDUM |
| Sound, pre-fire | "EVERYTHING MEDIATED … felted thumps, the soft wooden clop of the jaw, rod clicks the club never mentions, and the bell bright and forward in the mix" (vs LAW 5 — C-12) | MOTION §PRE-FIRE |
| LAW 4 | "THE WARM ONE NEVER ACTS. On camera, off camera, in any ending. Nothing follows filing it. No system may contradict this, including audio"; "Nothing springs in the dock"; "The warm unit makes no sound"; the Coverage Director "never stages the dock" | LAWS 4; WALK Part III.6; AUDIO §8; DESIGN Part IV-B.12 |
| LAW 5 | "The bell rings once, at the finale beat, and its caption says so. Chum's bell is otherwise silent; Chum speaks nowhere; Chum has no account, no achievement title, no presence string" | LAWS 5; ACH §DOCTRINE 2 |
| LAW 2 | the in-tape lunge is the ONE startle: "a single 33 ms broadband frame, band-limited to the TAPE bus" | LAWS 2; AUDIO §4 STINGER POLICY; MASTER SCARE 1 |
| The dock | "Rows of retired Chums on armatures, generations of him, fur going gray in order … in row three, mid-count, her gloved hand on a body that is warm. The game does nothing further. It never will, in this room"; "DOCK: rows two deep, years in order … the units' wools graying left to right by era" | MASTER T4.3; ART §7 (C-15: row three vs two rows) |
| Studio A | "the stage body's home … CHUM'S MARK at center stage … Drift: the mark's tape lifts one corner across days" | ROOMS §STUDIO A |
| Live at the premiere | "CHUM (live, beside her, warm as ever, bound to the format and playing it beautifully)"; the bell "rings once, three feet behind camera position" [SCARE 10]; Cue 3 "(directly to lens …) Till I find you. By and by." | MASTER T5.3 (C-11 against LAW 5's "speaks nowhere") |
| Understudy live build | "dimensionally identical to Chum plus four percent overall scale, an error the eye reports as distance being wrong rather than size being wrong" | ART §6; FABRIC §2 D5 |
| Key art | "No startle imagery, no open mouths, no lunging poses in any still" | KEYART §LAWS |
| Voice | "double-voice: warm children's-host falsetto with a chest resonance underneath … ALL Chum lines … then the TAPE bus. He must never exist on the WORLD bus until the finale's live set, and there he is quieter than expected" | AUDIO §5 |

### 7.2 WHAT EXISTS

| Item | State | Source |
|---|---|---|
| Blender build | `tools/build_chum_1974.py` → `assets/models/chum_1974.glb`: "~1.05 m tall, faces Godot +Z (Blender −Y)"; `organic()` voxel 0.014 remesh with lump/fiber displace, `patch()` (BellyCircle r 0.26 at (0, −0.3, 0.38), RustChest, GreenSide …), ears as cones with inner patches, `AmberEye` / `ButtonEye` spheres, nose cone, `GrinX*` ticks, whiskers, collar torus, bell; Cycles bakes from Fabric031/030, Leather030, Metal058A (CREDITS) | BUILD-1974 docstring, 117–160; CREDITS |
| Godot | `CharacterKit.chum_mini()` loads the glb (procedural fallback ≈ 1.05 m); six `DockChum` units at x ∈ {−18, −16, −14}, z ∈ {−40, −41.7}: units 1–2 `chum_pilot()`, 3–6 `chum_mini()`; box collision 0.6 × 1.4 × 0.6; `DockChum.interact` → "Your gloved hand rests on it. It is warm. You write the number down anyway." / "UNIT n · fur gone gray in order."; `DockTask.is_warm(self)` decides which | KIT 325–331; WB 975–1006; DOCK.gd |
| Tape stage | `TapeStage._build_chum()`: its own small procedural Chum (wool spheres, ear cones, amber sphere) for the Tape 1 timeline "ending on the approach, the hold, and the lunge" | STAGE.gd 5, 82–120 |
| UE | nothing ("UE: nothing yet", DOSSIER §2.7); `SK_Chum_Stage` is named by PIPE-PROD but not built | PIPE-PROD ADDENDUM |
| Sodium | the 1974 glb's bakes were never run through `--subject` (the check post-dates the build; PROGRESS 0.3b ran it on the AF body only) | PROGRESS 0.3b |
| The four reference plates | cited as ground truth by ART, DESIGN, FABRIC; not in this repo | OPEN-6 |

### 7.3 BUILD BRIEF

Two products from ONE Blender source (the P1 §1.7 precedent of one build, two exports):

| Product | What | Where used | Skeleton |
|---|---|---|---|
| `SM_Chum_1974` (static, LOVED kit) | the dock units 3–6 on their armature stands; the Studio A stage body on CHUM'S MARK | SCENE DOCK; STUDIO A | none — a static mesh (LAW 4 made mechanical: a mesh with no skeleton cannot act) |
| `SK_Chum_Stage` (skeletal, LOVED kit; a NEW kit variant per era via material instances) | the footage: every in-tape capture (T1.5 → T5), the Quiet Game, the approach and the lunge; the live premiere body (T5.3); the Understudy live build (+4 %, separate frozen export `SK_Chum_Stage_Understudy`) | the tape stage render target; Studio A at the premiere | `SKEL_Chum_Stage` (§7.4) |

**Silhouette and the patch ledger.** As DESIGN Part I verbatim (§7.1): twelve patches — rust chest, green right side, tan belly circle, blue arm, plum thigh, mustard toe caps (two), navy tail tip, the two inner-ear patches (mustard viewer-left, navy viewer-right), plus two more to reach twelve (**OPEN-7a**: the count of twelve is canon, the twelfth and eleventh placements are not named; BUILD-1974 places belly, rust chest, green side and the ear/toe/tail patches — the build's own count must be read off the script at 2.7 and the gap logged). Round head with a visible centre seam; amber glass eye viewer-LEFT (14 mm), black four-hole button viewer-RIGHT (18 mm, visible waxed thread); cross-stitched grin of X ticks, symmetric; three twisted-string whiskers per side (DESIGN) or six fine wire (FABRIC) — C-9; thin brown collar with a 25 mm brass keyhole bell; wire in ears, tail, spine.

| Measure | Value | Status |
|---|---|---|
| Height | canon: **seated height 55 cm** [FABRIC §3] — the ONLY canon number. The reference stand-in is "~1.05 m" standing [BUILD-1974; KIT 290] — twice the RFQ; which size the dock and stage ship at is **OPEN-13**. Under the owner ruling (true canon height, scale 1.0) this brief authors the puppet at 55 cm SEATED and derives standing height from the same body (≈ 0.75–0.85 m standing for a seated-55 cat, an ESTIMATE from proportion); the armature STAND under each dock unit is separate geometry and sets the row's silhouette height (stand height OPEN-13b) | OPEN-13 (owner) |
| Eyes | 14 mm amber glass viewer-left; 18 mm button viewer-right | FABRIC §3 |
| Bell | 25 mm brass, clapperless | FABRIC §3 |
| Understudy | +4 % overall, tolerance ± 0.5 % — a second frozen export, never a runtime scale | ART §6; FABRIC D5; owner ruling |

**Materials (the P1 §1.1 wool stack, un-scorched, plus the felt patches).**

| Need | Candidate (id · source · licence) | How |
|---|---|---|
| Boiled-wool body, brown, LOVED | `wool_boucle` (looped wool) · Poly Haven · CC0 at 1:1 mm; `Fabric031` (grey wool weave, in hand) tinted (0.36, 0.27, 0.18) [BUILD-1974 `WoolBrown`]; `knitted_fleece` (brown) · Poly Haven · CC0 for the nap; sun-fade crown and hand-polish at grip zones as `Wear` masks (FABRIC D2 LOVED) | the SAME `M_Wool` master as the AF body [PIPE §MATERIAL MASTERS]: "the After-Fire wool must read as the same material that forgot how to be soft" [MOTION §PRODUCTION NOTES] — so this wool is the soft one it forgot |
| Hand-cut FELTED patches (twelve) | `Fabric034` (felt) · AmbientCG · CC0 as the felt base for all patches, tinted: rust (0.55, 0.25, 0.15), green (0.28, 0.38, 0.25), tan belly (0.55, 0.44, 0.28), blue (0.25, 0.32, 0.5), plum (0.4, 0.22, 0.35), mustard (0.72, 0.55, 0.18), navy (0.16, 0.2, 0.35) [BUILD-1971/1974 `M` table]; alternates with real weave: `Fabric018` (green wool) · AmbientCG, `Fabric016` (red wool) → plum/rust, `Fabric068` (orange wool) → mustard, `denim_fabric_06` → navy, `caban` (rust fleece) · Poly Haven | patches are SOLID geometry 6–10 mm proud (P1 §1.1 step 2), never shells; blanket stitch as normal + albedo along the border (< 2 cm → maps) |
| Muslin core (seen nowhere on an intact puppet) | `hessian_230` · Poly Haven · CC0 only if a seam gapes on the LOVED kit | |
| Twisted-string whiskers | `Rope001` (string) · AmbientCG · CC0 on bevelled curves; yarn twist in the normal | C-9: build three per side (DESIGN, the community catalogue) and keep six-wire as a material variant until ruled |
| Amber glass eye | no glass scan; `M_Practical` (fixture glass) [PIPE] with an amber absorption and a taxidermy pupil decal; the AF body's `LensRing` precedent for the socket | "taxidermy grade" |
| Button eye, four-hole, waxed thread | `Leather026` / `Leather027` (black smooth) · AmbientCG · CC0 for the horn/bakelite read (P1 §1.8 precedent); thread `Rope001` | the thread is geometry only where it crosses the holes (silhouette at 30 cm) |
| Nose | `Fabric034` felt, dark | |
| Cross-stitched grin | X ticks: geometry (they are the face's silhouette at 30 cm and the tell-table measures them in mm) — `GrinX*` in the build; thread `Rope001` normal | FABRIC §5 T1 measures the grin at the seam: it must be geometry the caliper can read |
| Collar, thin brown leather | `Leather030` (in hand) or `fabric_leather_01` (aged, stitched) · Poly Haven · CC0 | |
| Brass keyhole bell | `brass_goblets` / `brass_vase_02` · Poly Haven · CC0 for the brass PBR set; `Metal042B` (dirty gold) · AmbientCG · CC0; the keyhole slot as geometry; NO clapper inside (model the hollow, empty: "clapper removed invisibly") | 25 mm |
| Armature stand (dock units) | `metal_stool_02` / `metal_stool_03` (metal frame, workshop, rusted) · Poly Haven · CC0 as donors for a rod-and-base stand; `Metal041B` iron rust · AmbientCG (P1 §1.4) | `SM_Dock_Armature`; stand height OPEN-13b |
| Fab (confirm) | "wool fabric", "felt", "boiled wool", "brass bell", "plush toy fabric" | |

**Drift.** The dock rows grey "left to right by era" [ART §7] — a per-unit `Age` parameter on `MI_Chum1974_Wool` (desaturate + lighten), NOT a texture per unit; the Studio A body's L1 drift is a HEAD ANGLE per day (a static-mesh rotation on the neck pivot set by the level per day), never an animation [MOTION §PRE-FIRE].

**Blender steps.**
1. Rebuild the 1974 body from `build_chum_1974.py` at the canon 55 cm seated (multiply the build's constants by the seated-height ratio once, apply, freeze); log the standing height that results as the ESTIMATE; the 1.05 m stand-in retires (or stays in the Godot glb only, the P1 §1.7 precedent for keeping the reference runnable).
2. Patches as solid embedded geometry (P1 §1.1 step 2); twelve, with OPEN-7a's two unnamed placements logged.
3. Grin ticks, whiskers, eye, button, collar, bell as geometry; stitches to maps; `island_margin 0.03`.
4. Two exports: `SM_Chum_1974` (static, with `UCX_` box, on the armature stand as a separate SM) and `SK_Chum_Stage` (skinned to `SKEL_Chum_Stage`, cloth + secondaries enabled per PIPE-PROD; empties become bones, do not flatten).
5. `SK_Chum_Stage_Understudy`: the same file scaled ×1.04 uniformly, applied, frozen, exported separately.
6. Bakes at 2K default; Chum is "the one asset allowed 4K" [PIPE §STANDARDS] — reserve 4K for the head albedo only.
7. `sodium_check.py --subject` (the soft wool beside the AF wool on ONE sheet: same material, one forgot how to be soft) → beauty (the four-plate framing, gray seamless, typewriter labels — DESIGN Part I — as the beauty rig, OPEN-6 for the plates themselves) → export → captures in SCENE DOCK under the sodium truth light [ROOMS §SCENE DOCK] and on CHUM'S MARK.

**BANNED.** A skeleton, physics, audio or tick on any dock unit (LAW 4). A clapper. A bell key on any clip but the one finale beat (LAW 5). Any in-compound animation of the stage body (MOTION: "the stage body never animates"). Machine-regular stitching ("nothing may read machine-made at 30 cm"). The post-fire deltas on this body (P1 §0.5: the two bodies' canon must not be mixed — the flannel and leather patches belong to §9). Open mouths or lunging poses in any STILL (KEYART §LAWS) — the lunge exists only in the moving footage.

### 7.4 RIG & ANIMATION SPEC (`SK_Chum_Stage`; the dock and stage SMs have no rig)

**Bones (`SKEL_Chum_Stage`; character-relative; the same bone map as RIG §1.3 wherever the two bodies share a part, so the AF rig and this rig "share a bone map" as RIG §1.3 intends):** `root, pelvis, spine_01, spine_02, neck, head, jaw (C-10: built, locked unless the owner rules the flapping jaw in), ear_l, ear_r (+ `ear_tip_l/r`), eye_amber (viewer-left = character RIGHT: `eye_r`), eye_button (`eye_l`, rigid), nose, whisker_01..03_l/r, bell (child of `neck`, carries `SOCKET_Bell`), collar, clavicle_l/r, upperarm_l/r, lowerarm_l/r, hand_l/r (paws, weighted), thigh_l/r, calf_l/r, foot_l/r, tail_01..04, rod_arm_l/r (the rod-arm option's control, hidden)`. Cloth: the belly panel and ear inner patches on a soft cloth setup; secondaries: ears, whiskers, tail, bell on AnimDynamics — ENABLED, this is the body that bounces [PIPE-PROD ADDENDUM].

**Control conventions.** Bezier, ease-heavy; anticipation → overshoot → settle on every move; head tilts snap to 15° stops [MOTION §PRE-FIRE]; jaw: C-10 — FABRIC fixes the grin; MOTION flaps the jaw a half-beat off the phonemes; until ruled, author the jaw bone and the lip-flap clip variants but ship the tape-stage clips with the jaw LOCKED (the cheaper error to reverse).

| # | State | Where | Clip / asset | Timing tied to | Must NOT |
|---|---|---|---|---|---|
| C-T0 | SEGMENT PERFORMANCE (footage beds) | tape stage; S03 loops | `AS_ChumStage_StoryCorner`, `_CraftTime`, `_TheSong`, `_QuietGame` — broad, cheated to lens, bounce-and-settle, ears lagging, whiskers trembling, the bell answering every gesture (visually; its SOUND is S08's — C-12) | segment lines [MASTER App. C]; 76 bpm for THE SONG [AUDIO §4] | face away from the lens; linear curves (that is the other body's grammar) |
| C-T1 | THE QUIET GAME (T1.5) | tape stage | `AS_ChumStage_QuietGame`: the rhyme at distance, the seeking pose | — | — |
| C-T2 | THE APPROACH + THE HOLD + THE LUNGE (SCARE 1) | tape stage, Tape 1's capture | `AS_ChumStage_Approach` (to lens distance) → `_Hold` → `AM_ChumStage_Lunge`: "Chum's face arriving at lens distance, button eyes filling frame"; the startle is ONE frame: 33 ms, TAPE bus | LAWS 2; AUDIO §4 ("a single 33 ms broadband frame"); STAGE.gd's `lunge_happened` | be reused anywhere; exist as a still (KEYART); have a sting outside the TAPE bus |
| C-T3 | THE FIRE TAPE (T3.4) | tape stage | `AS_ChumStage_FireTape_Unfinished`: the sign-off's unfinished line, then the wake bleed (S24) is AUDIO — the body does nothing new | MASTER T3.4; AUDIO S24 | a sting (QA-23 "no sting anywhere in it") |
| C-L1 | LIVE AT THE PREMIERE (T5.3 CUE 1–5) | Studio A, the real body beside Rita | `AS_ChumStage_Live_Cue1..5`: "warm as ever, bound to the format and playing it beautifully"; CUE 2 variant: "Chum stops singing for exactly one beat, head tilting" — one 15° tilt on the beat; CUE 3 "(directly to lens)" | the premiere clocks (45 s cue-2, 30 s blackouts; ×1.5 on assist) [ACCESS §5.2] | leave the format; exist on the WORLD bus louder than "quieter than expected" [AUDIO §5] |
| C-B | THE BELL, ONCE | SCARE 10, CUE 2 midpoint | `AS_ChumStage_BellOnce`: ONE authored key on `bell`, "three feet behind camera position" — it rings where the puppet is not in frame; caption `[THE BELL RINGS · once]`; S06 | LAWS 5; MASTER T5.3; ACCESS §3.2 | a second key on `bell` in any clip (F-curve scan, as RIG §4.2 "Bell"); AnimDynamics on `bell` at the premiere (the secondaries' bell-swing in FOOTAGE is a visual only, and C-12 decides whether it sounds there) |
| C-E1A | ENDING 1A | live | "CHUM (live, small, the performance finally allowed to end): Goodnight, Gladhouse." — `AS_ChumStage_End_Small`: the settle with no overshoot, the one time the puppet grammar runs out | MASTER §ENDING 1A | — |
| C-D | THE DOCK / THE STAGE BODY | compound | NONE. `SM_Chum_1974` has no clips. The warm unit is `DockTask.is_warm` and a toast; "The game does nothing further. It never will, in this room" | LAW 4; MASTER T4.3; QA-24 | anything |

**UE drive.** The tape stage (`ALelandStage`'s sibling `ATapeStage`, a 320 × 240 capture with the ladder) plays the footage clips on a Sequencer timeline per tape; the premiere's live body is a Sequencer-driven `SK_Chum_Stage` in Studio A under `ALiveProduction` (Phase 5). The dock units are `ADockChum` actors with a static mesh and an `IRestorationInteractable` prompt ("UNIT n · count (E)") and NO tick beyond the prompt; `DockTask.is_warm` is state, not presentation.

### 7.5 ACCEPTANCE

- Sodium `--subject` on `SM_Chum_1974`: brown boiled wool reads as soft wool (nap, loft, no facets), the felt patches as felt with a blanket-stitched border in relief, the bell as brass, the amber eye as glass with a pupil, the button as horn/bakelite with thread; beside `SK_Chum_AfterFire` on the same sheet: the same wool, one soft and one fused.
- Beauty in the four-plate language (gray seamless, typewriter labels; OPEN-6) at 30 cm: "nothing may read machine-made at 30 cm".
- UE captures: (a) SCENE DOCK under the sodium truth light: six units in two rows, wools greying left to right (the `Age` parameter visibly monotonic); (b) STUDIO A on CHUM'S MARK, tungsten wash; (c) the tape stage at G0 and G3: the approach/hold/lunge sequence as an MRQ clip; the lunge frame is exactly one frame; (d) the premiere live body beside `SK_Rita_Frame` on the PGM feed.
- Static checks: `SM_Chum_1974` has no skeleton, no physics asset, no audio; every `SK_Chum_Stage` clip's `bell` F-curve has zero keys except `AS_ChumStage_BellOnce` (one); no still in `docs/telemetry/` shows an open mouth or a lunge pose.
- Scale: the puppet's seated height = 0.55 m ± 0.5 cm measured in UE; the Understudy export = ×1.04 ± 0.5 % (FABRIC D5's tolerance); actor scale 1.0 on all.
- Soak: QA-24 (filing all six completes with nothing following).

### 7.6 RISKS / OPEN

- OPEN-6 (the four plates), OPEN-7a (the unnamed 11th/12th patch placements), OPEN-13 / 13b (shipped size; stand height), C-9 (whiskers), C-10 (jaw), C-11 (live lines vs LAW 5), C-12 (the bell on tape), C-15 (row three), OPEN-8 (which units ship the post-fire body, §9).
- Risk: the biggest realism risk in the whole cast sits here, not on the humans — the soft 1974 wool must be recognisably the SAME material as the AF wool and read as loved, not new; if the two wools do not sit together on one sodium sheet the "forgot how to be soft" reading dies and with it the cast's one visual argument.
- Risk: LAW 4 is easiest to break by kindness — a dock unit given an idle "for life" is an S0. The static-mesh rule is the guard.

---
## 8 · CHUM · THE 1971 PILOT (unit 2.8)

### 8.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Era | "1971 pilot · Cruder, endearing prototype · 9 hand-cut patches, no bell yet, frayed yarn whiskers, faintly uneven grin" | DESIGN era table |
| Kit | "1971 NEW (unworn finish)" | FABRIC §2 D2 |
| Base | everything else per DESIGN Part I · Chum (§7.1) with the 1974 additions removed: no collar-and-bell, nine patches, yarn whiskers, asymmetric grin; amber eye already viewer-left [BUILD-1971 docstring] | DESIGN; BUILD-1971 |
| Where | SCENE DOCK units 1 and 2 (the oldest wool, leftmost in the greying) | WB 994–996; ART §7 |
| Footage | the 1971 film in T2.4 is WGLD STAFF ORIENTATION, 1971 — the FM's film, not Chum's; no 1971 Chum footage is scripted | MASTER T2.4; DOSSIER §2.8 |
| Ambient | "the antenna guy-wire's crimp tag, stamped 1971, still bright" | AMBIENT §YARD |
| LAWS | 4 (if unit 1 or 2 is the warm one), 5 (no bell to ring — the silence is total by absence) | LAWS 4, 5 |
| OPEN | which nine of the twelve patches; the grin's asymmetry amount; whisker count/length; standing size | OPEN-7 |

### 8.2 WHAT EXISTS

| Item | State | Source |
|---|---|---|
| Blender build | `tools/build_chum_1971.py` → `assets/models/chum_1971.glb`: "Rougher wool, lumpier remesh — somebody made this at a kitchen table and you can tell"; `organic()` voxel 0.02, lump 0.014 (vs 1974's 0.014 / 0.006); the same `M` palette; a torus head seam tilted (4°, 90°, 6°); ears cones; `AmberEye` at (−0.078, −0.215, 0.9), `ButtonEye` squashed (1, 0.6, 1); "frayed yarn whiskers: thicker, kinked, drooping unevenly"; no collar, no bell | BUILD-1971 docstring, 70–170 |
| Godot | `CharacterKit.chum_pilot()` loads the glb; the procedural fallback is the 1974 build ("the fallback is not era-correct") | KIT 294–297; DOSSIER §2.8 |
| UE | nothing | — |

### 8.3 BUILD BRIEF

One product: `SM_Chum_1971` (static; dock units 1–2). No skeletal export is needed by any canon beat (no 1971 footage exists; OPEN-7c if one is ever authored).

| Measure | Value | Status |
|---|---|---|
| Height | as §7: seated 55 cm is the RFQ's base body [FABRIC §3 D1 is "the 1971-1974 base body"] — the pilot is the same body with the NEW kit; standing size OPEN-7; stand height OPEN-13b | OPEN |
| Patches | nine — WHICH nine is OPEN-7; BUILD-1971 places BellyCircle, RustChest, GreenSide (lines 123–125) plus whatever follows; read the script's count at 2.8 and log the set | OPEN-7 |
| Grin | "faintly uneven" — amount OPEN-7; the build's `GrinX*` ticks should carry a per-tick jitter parameter so the amount is a number the owner can set | OPEN-7 |
| Whiskers | "frayed yarn" — count/length OPEN-7; BUILD-1971's are "thicker, kinked, drooping unevenly" | OPEN-7 |

**Materials.** As §7.3 with these substitutions: the wool is `wool_boucle` / `Fabric031` at a ROUGHER remesh and an unworn NEW finish (no hand-polish, no sun-fade: `Wear` = 0); patches are `Fabric034` felt, hand-cut (deliberately irregular outlines, "kitchen table"); whiskers are YARN: `Rope001` (beige string) · AmbientCG · CC0 with a frayed-end alpha, or `Rope003` (dark/light rope) · AmbientCG · CC0; the head seam is a visible hand-sewn line (thread relief from `Rope001`); NO collar, NO bell materials in the manifest at all (a static check). The oldest wool in the dock's greying: `Age` = 1.0 on units 1–2 [ART §7].

**Blender steps.**
1. Rebuild from `build_chum_1971.py` at the canon seated 55 cm (the same frozen scale factor as §7 so the two bodies are "dimensionally" one base body, FABRIC D1).
2. Nine patches as solid embedded geometry, irregular; grin ticks with a jitter parameter; yarn whiskers as curves with frayed tips (geometry: they are silhouette).
3. No collar, no bell — the neck shows the head-to-body seam instead.
4. Export `SM_Chum_1971` with `UCX_`; on `SM_Dock_Armature`.
5. Sodium `--subject` beside `SM_Chum_1974` (the same wool, rougher and unworn vs loved) → beauty → dock capture, units 1–2 leftmost.

**BANNED.** A bell (there is none yet; do not "add the collar for consistency"). A skeleton, physics, audio (LAW 4). Any 1974 wear on a NEW-finish body. Reusing the 1974 mesh with patches hidden (the pilot is cruder in construction, not in dressing: DESIGN "Cruder, endearing prototype").

### 8.4 RIG & ANIMATION SPEC

None. `SM_Chum_1971` is a static mesh with no skeleton; the dock units never animate (LAW 4; MOTION §PRE-FIRE "the stage body never animates"). If OPEN-7c ever authors 1971 footage, `SKEL_Chum_Stage` (§7.4) without the `bell`, `collar` bones applies, ease-heavy, with the pre-fire grammar.

**UE drive.** `ADockChum` units 1–2 with `SM_Chum_1971`; prompt "UNIT n · count (E)"; nothing else.

### 8.5 ACCEPTANCE

- Sodium `--subject`: the pilot's wool beside the 1974's: same fibre, rougher surface, no polish; felt patches with irregular hand-cut edges; yarn whiskers read as yarn (not wire, not string).
- Beauty in the four-plate language; the dock capture under the sodium truth light with units 1–2 the greyest and the grin visibly uneven at 1 m.
- Static checks: no material named `Brass`/`Bell`/`Collar` in the 1971 manifest; no skeleton; no audio.
- Scale: seated 0.55 m ± 0.5 cm; actor scale 1.0.

### 8.6 RISKS / OPEN

- OPEN-7 (which nine patches, grin asymmetry, whiskers, standing size), OPEN-7c (1971 footage), OPEN-13 / 13b.
- Risk: "cruder" is easy to overdo into "damaged"; the pilot is NEW and endearing. The wear pass is zero; the crudeness is construction (lumpier remesh, irregular patches), not dirt.

---

## 9 · CHUM · THE POST-FIRE STAGE PUPPET (nine deltas) and THE 4K PREMIERE BODY (not Phase 2 boxes — OPEN-8; recorded so the dock, the tape world and the key art can build them)

### 9.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Design law | "Post-fire · Repaired, not burned: the horror is the mending"; "fire damage reads as victimhood; the fear lives in the repairs" | DESIGN era table; §The post-fire delta set |
| The nine deltas | 1 the over-grin (a wider grin sewn past a cat's mouth, tight vertical ticks in waxed near-black thread, the old seam a faint scar); 2 the wrong button (an adult coat button, too large, off-shade, over-attached); 3 the chirality tell (amber eye viewer-RIGHT, pupil off-axis); 4 whisker asymmetry (three singed stubs one side; two too-long, too-straight dark wire replacements the other); 5 the bell opened (blackened, still silent, a bright pried-and-recrimped scratch); 6 the belly accessed (darker wool, a central seam opened and resewn repeatedly); 7 two wrong-material patches (school-gray flannel at the chest, glossy dark leather at the leg; count 14); 8 the tilt (neck restitched 2–3° off true); 9 footage-only: weight on the wrong foot | DESIGN §The post-fire delta set |
| The tell-table (caliper-checked) | T1 grin +18 mm past each cheek seam; T2 28 mm horn button where an 18 mm shell should be; T3 amber viewer-RIGHT, button viewer-LEFT, pupil axis 8° off vertical; T4 whiskers replaced by 6 mm stubs, all sides; T5 bell blackened, crown pry-marks, still silent; T6 belly seam resewn in visibly newer undyed thread; T7 fourteen patches incl. one S-07 gray school flannel and one 40 × 55 mm leather patch at P11; T8 head tilt 2.5° resting; T9 left forepaw 12 mm forward of square. "REPAIRED, NOT BURNED. No char, no melt, no horror finishing" | FABRIC §5 (T4 vs delta 4: C-9) |
| Never stated | "The post-fire tells are never called out by the game. They are deducible-layer content delivered through the player's own restoration monitors" | DESIGN |
| The flannel | D04: "wrapped in a square of gray flannel her mother did not recognize"; "the gray flannel square is the same stock as post-fire patch seven"; the green room's flannel shim | PROPS D04; AMBIENT §GREEN ROOM; LORE §THE SHARD MODEL |
| Key art | HERO COMP A: "post-fire Chum mid-HOLD, close, still, the artifact ladder visible on the screen"; "REPAIRED, NOT BURNED: post-fire Chum per the tell-table, zero char, zero horror finishing" | KEYART §HERO COMP A, §LAWS |
| The 4K body | "4K premiere · 1974 configuration in impossible fidelity · Individually rendered fur sheen, moisture in the glass eye, detail no puppet could carry"; D4 "cleaned and groomed to unsettling perfection"; ending 2: "fur rendered strand by strand, moisture in the button eyes … Say it with me, everyone. Welcome home." | DESIGN era table; FABRIC §2 D4; MASTER §ENDING 2 |
| The one lie | the post-credits CONTINUE? / NEW EPISODE is the interface's single lie; the 4K image is the digital broadcast and is the one image allowed clean (OPEN-14 against ART §2) | LAWS 8; MASTER §ENDING 2; ART §2 |
| Reference tilt | `HEAD_TILT 0.045` rad ≈ 2.6° (the AF body inherits "delta 8") | TIMINGS; RIG §0.2 |
| Two bodies | the mascot already carries the flannel and leather patches by build precedent, "No canon document says the mascot carries them" | P1 §0.5, §1.1 |

### 9.2 WHAT EXISTS

Nothing for either body: no build script, no glb, no UE asset. The tell-table's numbered placement diagram "supplied at contract" is not in the repo [P1 §1.1 OPEN]. The AF mascot (`BUILD-AF`) carries `PatchFlannel` and `PatchLeather` — stage deltas transplanted [P1 §0.5].

### 9.3 BUILD BRIEF

**`SM_Chum_PostFire_Stage` (and `SK_Chum_Stage_PostFire` if footage needs it: the fire tape's body and the key art's monitor image are FOOTAGE, so the skeletal is the primary product here — OPEN-8 decides the box).** Built from the §7 source with the nine deltas applied as MEASURABLE edits — the tell-table is a QC sheet, and the acceptance test is a caliper in Blender:

| Delta | Build edit | Measure |
|---|---|---|
| T1 over-grin | extend the `GrinX*` tick run 18 mm past each cheek seam at the same gauge; keep the original seam as a scar (a faint normal line) | ruler on the seam |
| T2 wrong button | replace the 18 mm button with a 28 mm two-hole coat button, horn (`Ivory001A` ivory/horn base · AmbientCG · CC0 with a dark tint; `Leather026` alt), over-wrapped thread (`Rope001`, many wraps) | 28 mm |
| T3 eye swap | amber to viewer-RIGHT (character left), button viewer-LEFT; pupil decal rotated 8° off vertical | 8° |
| T4 / delta 4 | C-9: FABRIC says 6 mm stubs all sides; DESIGN says three stubs + two wrong wire. Build FABRIC (the RFQ the fabricator QCs) as the mesh and DESIGN as a variant flag until ruled | 6 mm |
| T5 bell opened | blackened brass: `Metal013` (bronze, eroded) / `Metal058B`/`058C` (copper oxidation) · AmbientCG · CC0 with a bright hand-painted pry scratch at the crown seam (P1 §1.3 precedent); still clapperless | — |
| T6 belly resewn | the tan belly replaced by darker wool (`knitted_fleece` tinted); a central seam with dense overlapping restitch in undyed thread (`Rope001` beige, unaged) — restitch scarring is silhouette at 30 cm: geometry ridges | — |
| T7 fourteen patches | the 1974 twelve plus S-07 school-gray flannel at the chest (`poly_wool_herringbone` grey · Poly Haven · CC0 or `Fabric030` grey cloth (in hand) — the same instance the green-room shim and D04's square use, so the shards rhyme in MATERIAL) and a 40 × 55 mm glossy dark leather patch at P11 (`Leather032` black scratched / `Leather026` · AmbientCG · CC0, roughness lower than anything else on him) | 40 × 55 mm; count 14 |
| T8 tilt | the head rotated 2.5° at the neck in the REST mesh (a static mesh has no rig; the tilt is modelled), matching the AF rig's 0.045 rad rest tilt lineage | 2.5° |
| T9 stance | left forepaw 12 mm forward of square in the rest pose | 12 mm |
| Delta 9 (footage only) | weight on the wrong foot — an ANIMATION rule for `SK_Chum_Stage_PostFire` clips, not a mesh edit | — |

No char, no melt, no soot masks, no `burlap_nodes()` burn ramp: everything in P1 §1.1 step 5 is FORBIDDEN on this body. The only "wrongness" is care.

**`SK_Chum_4K` (ending 2's body).** The 1974 configuration (§7) at the 4K tier: 4K maps (Chum is the one asset allowed 4K [PIPE §STANDARDS]); a groom — this is the ONE place in the game particle hair / strand fur is shipped rather than design-only ("Individually rendered fur sheen … detail no puppet could carry"; P1 §0.3 lists in-file particle hair as design-only for the AF body — the 4K body is the exception the canon writes); "moisture in the glass eye": a wet clearcoat on `M_Practical` glass and the button. It renders CLEAN — no ladder — because "no tape image may ever appear clean except the anomaly slates" [ART §2] and the 4K premiere is the digital broadcast; whether it passes through the ladder at all is OPEN-14.

**Blender steps.** (Post-fire) duplicate the §7 source; apply T1–T9 as parametric edits with the measurements as named constants in the script (`GRIN_EXT_MM = 18`, `BUTTON_MM = 28`, `PUPIL_DEG = 8`, `STUB_MM = 6`, `LEATHER_MM = (40, 55)`, `TILT_DEG = 2.5`, `PAW_MM = 12`) so QC is a script assert; export static and skeletal. (4K) duplicate the §7 source; 4K bakes; groom via particle hair converted to strands for UE (Groom asset), `SK_Chum_4K`; wet eye clearcoat.

**BANNED.** Char, melt, scorch, soot, singe, any `BurnField`/`ScorchRay` object from BUILD-AF (those are the mascot's). Any text, caption or prompt naming a tell. Marketing stills with the grin open or a lunge (KEYART). Mixing this body's deltas into the AF mascot beyond the two the build already carries (P1 §0.5 OPEN).

### 9.4 RIG & ANIMATION SPEC

`SK_Chum_Stage_PostFire` uses `SKEL_Chum_Stage` (§7.4) unchanged, with the rest pose carrying T8 (2.5° head) and T9 (12 mm paw); clips are the pre-fire grammar (this is footage: performed, bouncy) with delta 9 applied — weight on the wrong foot in every stance. The fire tape's "unfinished line" is this body's clip (C-T3 in §7.4 becomes this body's when OPEN-8 rules). Post-fire footage sound is still band-limited ("every pre-fire sound lives inside the broadcast band forever", MOTION §THE AUDIO LAW). `SK_Chum_4K`: the same skeleton; the one clip `AS_Chum4K_LeanIn`: "Chum leans to the lens … (the grin, stitch by stitch)" — intimate, slow, the lean is the whole performance; groom physics ON (the fur must move as fur); no lunge.

### 9.5 ACCEPTANCE

- Caliper assert in Blender: every T1–T9 constant measured on the exported mesh within ± 0.5 mm / ± 0.2°.
- Sodium `--subject`: the flannel reads as flannel (nap, matte) beside the wool; the leather reads glossier than anything else on him; the undyed thread reads newer (lighter, cleaner) than the dyed thread; the blackened bell reads as oxidised brass with ONE bright scratch; zero char anywhere (an albedo floor check: nothing ≤ 0.02 linear on this body, the inverse of P1 §1.1 step 5's char rule).
- The KEYART HERO COMP A capture: the post-fire body mid-HOLD on the bench monitor through the ladder, still, close.
- 4K: an ending-2 capture at the platform's native resolution, strand fur visible, eye moisture visible; a monochrome read must still identify it as the 1974 configuration.
- Static: no still with an open grin or lunge leaves the repo.

### 9.6 RISKS / OPEN

- OPEN-8 (which phase), OPEN-14 (the 4K body and the ladder), C-9 (whiskers), the numbered placement diagram (P1 §1.1 OPEN), the mascot's transplanted patches (P1 §0.5).
- Risk: the deltas are small (mm and degrees) and the ladder degrades them; the community is meant to find them frame by frame [DESIGN Part I · Chum "the community can catalog frame by frame"]. Author the tells so they survive G2 on the bench monitor (test at G2 and G3).
- Risk: the 4K groom is the only strand fur in the game and the machine is an M1 Pro / 16 GB [PLAN §1]; budget it as a single ending asset with LODs off and a strand count the owner signs.

---

## 10 · THE UNDERSTUDY and THE ONCE-EVER CORRIDOR FIGURE (no canonical body, by law; not a box)

### 10.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Design philosophy | "it has no canonical off-camera body, and the game never spends that mystery. Manifestation rules: On any monitor or viewfinder: it is Chum, performing, correct, bound by the show's physical logic. Off-camera, peripheral: partials only. A felt hand at human scale resting on a doorframe. A proscenium shadow that accompanies it like a stage edge it carries. Footsteps with the weight of a person and the texture of upholstery. Direct sight: reserved for one scripted glimpse in the entire game, late, brief, and never repeated. What the glimpse shows is a puppeteer whose puppet is missing, or a puppet whose puppeteer is missing; the animation should read as genuinely undecidable, and playtests should confirm players split on which they saw" | DESIGN Part I · The Understudy |
| Not a character | "the Understudy is not a character but a format" | PLOT §Dead Air (via DOSSIER §2.11) |
| Before the wake | "Before af_active it remains the old unseen presence" | AF §THE REVEAL |
| The moment (T4.8) | "At the corridor's elbow, for under two seconds, unmediated: it. A puppeteer whose puppet is missing, or a puppet whose puppeteer is missing, and the animation refuses to resolve which, and it does not turn, and the plastic sheeting breathes once with the draft of something passing that has already passed" | MASTER T4.8 |
| LAW 3 | "ONCE, EVER. The Day 4 fire-corridor moment occurs at most once per save and is never referenced again by any system, including achievements, presence, and logs. Its name appears in no code file" | LAWS 3 |
| LAW 2 / sound | "S11 The glimpse. LAW: no sting. Before: nothing. After: one breath of plastic sheeting, close, dry" | AUDIO §3 S11; §8 |
| Meta-silence | "The glimpse has NO achievement, ever"; never in marketing | ACH §DOCTRINE 2; KEYART §LAWS |
| Dread | "L5 · THE VIOLATION BUDGET. One startle. One interface lie. One once-ever sight … the budget never grows" | DREAD §L5 |
| Never-stated | "What Chum is" | LORE §THE NEVER-STATED LEDGER |
| Reference naming | `scripts/glimpse.gd`, `class_name Glimpse`, `GameState.glimpse_seen` — a LAW 3 finding for the port audit (C-13); the UE name is OPEN-15 | DOSSIER §2.11, §7 C-13 |

### 10.2 WHAT EXISTS

| Item | State | Source |
|---|---|---|
| Godot | `Glimpse`: fires once at night, not during the premiere, when the player enters the FIRE CORRIDOR rect [−9.75, −16.0, 7.5 × 3.0]; spawns at (−12.6, 0, −16.0) a near-black (0.03, 0.028, 0.026) capsule r 0.22 × 2.5 m (centre y 1.25), a bar 1.8 × 0.12 × 0.12 at y 2.9, and four strings 0.012 × 1.4 at x ∈ {−0.8, −0.3, 0.3, 0.8}, y 2.2, tilted −0.22·x ("strings, or tendons — part of what refuses to resolve"); shown 1.8 s; `glimpse_seen` set; two toasts at 2.8 s | GLIMPSE.gd 8–61 |
| The felt hand, the proscenium shadow, the upholstered footsteps | none built (the reference has no peripheral partials) | — |
| UE | nothing; the name is OPEN-15 | — |

### 10.3 BUILD BRIEF

**What is built: three partials and one figure.**

| Asset (proposed; the once-ever asset's name is OPEN-15 — the working name here is deliberately meaningless: `SK_Cast_Unresolved`) | What | Where |
|---|---|---|
| `SM_Partial_FeltHand` | "A felt hand at human scale resting on a doorframe" — a felt mitten hand (the same felt as the humans', `Fabric034`), human scale (the ESTIMATE glove size of §5), resting on a doorframe; no arm beyond the cuff | peripheral, off-camera, Coverage Director blocking (Phase 4/5) |
| `M_Partial_ProsceniumShadow` (a decal/light function, not a mesh) | "A proscenium shadow that accompanies it like a stage edge it carries": a hard-edged rectangular shadow with a curtain-edge silhouette that moves with the presence | peripheral |
| the upholstered footsteps | AUDIO only ("Footsteps with the weight of a person and the texture of upholstery"); caption `[footsteps, upholstered, left]` is DESIGN Part III's own example | peripheral |
| `SK_Cast_Unresolved` | the T4.8 figure: under two seconds, unmediated, at the elbow; "does not turn" | FIRE CORRIDOR (−1260, −1600, 0) uu, once |

**The figure's silhouette (the reference's reading, not canon):** a tall near-black vertical mass (2.5 m in the reference) with a horizontal bar above it (a puppeteer's control bar at 2.9 m) and four strings-or-tendons from the bar into the mass. The canon asks for undecidability: "a puppeteer whose puppet is missing, or a puppet whose puppeteer is missing". The build must therefore contain BOTH readings and resolve neither: a figure whose upper half reads as a black-sleeved operator (Craik's "puppeteer's black sleeves", §11) holding a bar with slack strings to nothing, AND whose lower half reads as a puppet body with rods to nothing — with the join hidden by the corridor's one honest bulb [ROOMS §FIRE CORRIDOR] and the plastic sheeting. Materials: `Fabric049` / `Fabric004` black cloth (sleeves), `velour_velvet` (red velvet desaturated to near-black — the "upholstery" texture the footsteps carry) · Poly Haven · CC0 for the puppet-body read, `Rope001` for strings, `Wood051` or `Metal013` for the bar; albedo floor near 0.03 linear (the reference's colour), never 0.

| Measure | Value | Status |
|---|---|---|
| Height | canon: **OPEN (none; "it has no canonical off-camera body")**. Reference: 2.5 m capsule + bar at 2.9 m [GLIMPSE.gd 33–45]. No plate exists by law; no estimate is possible; the reference numbers stand as REFERENCE | OPEN (owner) |
| Duration | "under two seconds" (canon); reference 1.8 s | MASTER T4.8; GLIMPSE.gd 59 |
| Felt hand | human scale | DESIGN Part I |

**BANNED.** A face. A turn. A second appearance anywhere (LAW 3). A name in any code file, asset path, log line, class, save field or content folder that references the moment ("glimpse", "T4.8", "once-ever", "corridor-elbow"); the flag must be as meaningless as the asset name (OPEN-15). Any sting, any music, any light change on it (S11). Any achievement or presence hook. Any marketing capture (KEYART). Any resolution of the puppeteer/puppet question in the mesh: if a reviewer can say which it is from the still, the build failed.

### 10.4 RIG & ANIMATION SPEC

**Bones (`SK_Cast_Unresolved`):** `root, mass_01..03 (a three-bone spine of the vertical mass), bar (child of `mass_03` OR of a separate `operator` bone — the parenting is itself the undecidable: author the bar on its own bone parented to root, so neither the mass nor an operator visibly owns it), string_01..04_a/b (two-bone chains from the bar), sleeve_l/r (pose-only, the black-sleeve read)`. Physics: the strings on a damped chain (the one motion: they settle as "something passing that has already passed").

| # | State | Trigger | Clip | Timing | Must NOT |
|---|---|---|---|---|---|
| U-1 | THE SIGHT | night, Day 4+, not premiere, player enters the corridor rect, flag unset | `AS_Unresolved_Pass`: the figure is already mid-passage at the elbow; over < 2.0 s the strings settle and the mass's weight shifts once — the animation must contain a puppet's settle (secondary, bouncy) AND an operator's step (a human weight transfer) in the same second, blended so that neither dominates; it does not turn | "under two seconds"; reference 1.8 s; then `Hidden`, flag set, never again | turn; face the player; lunge; ease-heavy OR linear alone (the two grammars must coexist — that is the undecidability, executed) |
| U-2 | THE SHEETING | after U-1 | the plastic sheeting (a Phase 3 corridor prop, cloth) "breathes once" — one cloth impulse, 1 cycle; S11's one breath of plastic | 2.8 s after (reference toast gap) | a second breath |
| U-P | PERIPHERAL PARTIALS (pre-wake presence; Coverage Director) | blocking variants | `SM_Partial_FeltHand` placed on a doorframe by the director; the shadow decal; the footsteps | — | be seen whole; be seen twice in one place |

**UE drive.** A corridor trigger actor (name OPEN-15) reading `State->bIsNight`, `Day >= 4`, `!bPremiereLive` and its own once-flag (a save field whose name says nothing — OPEN-15; the reference's `glimpse_seen` cannot be ported by name, C-13); spawns `SK_Cast_Unresolved`, plays U-1, destroys it; no log line (LAW 3: "never referenced again by any system, including … logs" — the invariant parser must never see a line for it); QA-25 tests it by save-state, not by log.

### 10.5 ACCEPTANCE

- The undecidability test (canon's own): "playtests should confirm players split on which they saw" [DESIGN Part I] — the ≥8-frame capture sequence shown to reviewers cold; if the split is not near half, iterate.
- Sodium `--subject`: the blacks show nap and weave (as the FM's); velvet vs cloth distinguishable.
- UE locked-EV night capture in the FIRE CORRIDOR at (−1260, −1600, 0): the figure at the elbow under the one honest bulb, under 2.0 s from first visible frame to hidden (frame-counted); no audio event in the log except S11 after; no light change.
- Static: grep the UE source, content paths, save schema and log format for any name that references the moment; the flag and the asset carry the OPEN-15 name only; no achievement reads the flag; QA-25 (exactly once per save).
- Scale: reference 2.5 m / 2.9 m bar until ruled; actor scale 1.0.

### 10.6 RISKS / OPEN

- OPEN-15 (the name), C-13 (the reference's name), height REFERENCE only, OPEN-U1: whether the felt hand and the proscenium shadow are Phase 4 (Coverage Director) or Phase 5 assets.
- Risk: this is the one asset that cannot be iterated in front of players (once, ever, per save) and cannot be sold (never in marketing); every review must be by capture, and every capture must stay in `docs/telemetry/` and out of any public package.
- Risk: the reference's name is in `glimpse.gd`; a port that copies file names ports the LAW 3 defect. The port audit (C17) owns the fix; this brief owns the asset name.

---
## 11 · ANSEL CRAIK (archival footage only; not a box)

### 11.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Look | "Seventies TV-crew look: big glasses, mustache, puppeteer's black sleeves. The single most important design detail in the archival footage: in one late episode, Craik is fully visible on set, both hands accounted for, while Chum performs in the same shot. The game never zooms in. The community will" | DESIGN Part I · Ansel Craik |
| Arc | "Delivered entirely through materials in reverse order of composition: the finale script first (his ending), the notebooks second (his understanding), the childhood radio scripts last (his beginning)" | WALK Part I · Ansel Craik |
| Voice | "Craik: archival only, optical-track character, 8 mm sound" | AUDIO §5 |
| Presence | D02 the production notebook ("Merle Cottry, age 7, returned. I did not send him. He went. I have stopped knowing which of us is the vessel."); the childhood scripts (T3.2); Rita reads "the host lines he wrote for himself" on his mark | PROPS D02; MASTER App. D; T3.2; T5.3 |
| Never in the compound | "Ansel Craik · archival only · not a box · never in the compound" | DOSSIER §1 |
| Never-stated | "What Chum is" — the late episode is a shard, never a statement | LORE §THE NEVER-STATED LEDGER; §THE SHARD MODEL |
| OPEN-16 | whether the late episode is ever authored as tape-stage content; no stage content exists for it | DOSSIER §2.12 |

### 11.2 WHAT EXISTS
Nothing: no figure, no footage, no plate. D02's text exists [PROPS D02].

### 11.3 BUILD BRIEF (only if OPEN-16 rules the late episode in)

`SK_Craik` on `SKEL_Cast_Human`, seen only inside the tape stage (4:3, the ladder live, never clean): big 1970s glasses (`round_spectacles` · Poly Haven · CC0 is round; the plate-less "big glasses" want a squarer 70s frame — Fab "70s glasses", "aviator eyeglasses"); moustache as felt nap (map); black long sleeves (`Fabric049` / `Fabric004` · AmbientCG · CC0, the puppeteer's blacks — the SAME instance as §10's sleeves, so the shard rhymes in material and nothing says so); a felt head like the rest (he is a crafted figure in footage, ART §2's one language). Height: canon OPEN, no plate, no estimate; author at the shared template's default and log it. Hands: mittens without stitched definition (not a principal) — and "both hands accounted for" is the whole point: two visible mitten hands, on set, while Chum performs. The shot is authored ONCE, wide, and "the game never zooms in" — no closeup asset, no 4K, 2K only, and the ladder at the episode's generation.

**BANNED.** A closeup. A voice on any bus but the archival optical-track chain [AUDIO §5]. A compound placement. Any caption or text that states what the shot implies (an S0 per LORE).

### 11.4 RIG & ANIMATION SPEC
Shared skeleton; one clip `AS_Craik_LateEpisode_OnSet`: standing on set, both hands visible and idle, while `SK_Chum_Stage` performs in the same frame (C-T0). Sound: 8 mm optical track, band-limited [MOTION §THE AUDIO LAW]. No other clip exists.

### 11.5 ACCEPTANCE
The one wide shot captured through the ladder at the episode's generation: both hands visible, the puppet performing, nothing in the frame composed to draw the eye to the hands (a reviewer who has not read the canon should not notice on first viewing; a reviewer who has should be able to count). No closeup exists in the repo.

### 11.6 RISKS / OPEN
OPEN-16; height OPEN (no plate). Risk: the shot is the game's biggest shard and the easiest to over-author; it must be boring.

---

## 12 · THE 58 CLUB ROWS and EXTRAS (not a box; ART §10 puts extras in P2)

### 12.1 IDENTITY & CANON

| Claim | Text | Source |
|---|---|---|
| Look | "Enamel pins as regalia, potluck domesticity … members' clothing migrates over the acts from civilian colors into the show palette (mustard, avocado, burnt orange), and the environment silently tells you who is furthest gone by how much of the palette they wear" | DESIGN Part I · The 58 Club |
| Drift | "EXTRAS AND PEGS: lead the curve by half a day, so the background is always slightly ahead of the people you know" | ART §5 |
| Build | needle-felt heads, cloth bodies, mitten hands WITHOUT stitched finger definition (reserved for principals); 1 : 5.5; bead or embroidered eyes | ART §6 |
| THE ROWS (LAW 7) | "each incident abandoned past guarantee takes a seated club member on camera: cut away from a smile, cut back to an empty chair, or to something half-resolved and interlaced, still trying to applaud at the held-applause mark. Casualty count feeds every epilogue's final card: THE 58 CLUB, followed by the new number" | CASUALTY §THE ROWS; QA-46 |
| Delivery | "from the lockdown onward they can restrain Rita and hold her off camera while it approaches. Humans become lethal by delivery, never by hand"; SCARE 12 "hands, human and gentle and immovable" | WALK Part V-B; MASTER T5.3 |
| Lockdown | "rec chairs tween to rows and persist"; S10 "Chairs converting. LAW: no sound worth naming" | QA-26; AUDIO §3 S10 |
| Where | STUDIO A "audience rows … row casualties seat here"; seat 14 "wears a brass RESERVED plate with the name line blank" | ROOMS §STUDIO A; AMBIENT §STUDIO A |
| Barks | "T1: 'Sleep well, dear.' T2: 'The sign likes you.' T3: 'Leland worked late too.' T4: 'You'll want to look nice for it.' T5: 'It's almost time, it's almost time, it's almost.'" | MASTER App. C |
| Count | none stated (OPEN-17); the final card is 58 minus N | DOSSIER §2.13; QA-47 |

### 12.2 WHAT EXISTS
Nothing: no extras in KIT, no rows in the reference beyond the chair tween; `RowCasualties` in state (STATE.h 104, 189).

### 12.3 BUILD BRIEF

`SK_Extra_A..F` (six bodies — a proposal: the reference has six dock units and no extras; the count is OPEN-17) on `SKEL_Cast_Human` at the template's default height (canon OPEN; no plates; no estimate — log the template number), with material-instance variation carrying the identity: cardigans/shirts/skirts from the shared families (`M_Knit`, cotton, tweed — §1–§4's ids), each with a `Drift` that LEADS the principals by half a day; an enamel pin each (`M_Enamel`); felt heads in six felt sculpts (age range: the club is "fifty years" of fandom — the members are older, per Merle and Harriet; no younger member is named except Vess). Hands: plain mittens. Extras are 2K, LOD1 allowed ("LOD1 for set dressing only", PIPE §STANDARDS — extras are the one cast tier that IS set dressing).

**The rows' death state (LAW 7):** `MI_Extra_Interlaced` — the same broadcast-body material as Vess's V2 (§3.4 V-D2): field-alternating scanline offset, chroma bleed, "still trying to applaud at the held-applause mark"; and the empty chair (the chair stays, the figure is hidden).

**BANNED.** Stitched finger definition (principals only). Any extra with a face that reads as knowing (KEYART's warmth law applies to the whole club: "Not one sinister face", KEYART §COMP B). Any sound on the chair conversion (S10). Gore on a row casualty (the idiom is interlace and the empty chair).

### 12.4 RIG & ANIMATION SPEC

Shared skeleton; the clips are unit 2.9's shared set: `AS_Extra_Sit_Idle` (hands in lap, occasional lean to a neighbour — the potluck domesticity), `AS_Extra_Applaud`, `AS_Extra_HoldApplause` (both hands pressed flat, held — the FM's seventh signal received), `AS_Extra_Sing_Home` (CUE 2, the club "cannot help joining"), `AS_Extra_Restrain` (SCARE 12: the delivery — "hands, human and gentle and immovable" — a two-extra hold on `SK_Rita_Reflect`'s arms from behind, authored gentle, no violence in the curves), `AS_Extra_Row_Interlaced` (the death: applauding, frozen at the held-applause mark, material state on). Screening seats: `AS_Extra_Screening_Sit` on the beat (BEAT 0.8 s, WINDOW 3.2 s). No extra ever walks on screen in canon except the tween of chairs (which is the chairs, not them) — locomotion clips are OPEN-X1.

**UE drive.** `AClubExtra` instances placed by the level (REC chairs pre-lockdown; STUDIO A rows after); `State->RowCasualties` selects which seats are empty or interlaced (the presentation half); `Drift` from the coat-peg curve + 0.5 day.

### 12.5 ACCEPTANCE
Sodium on one extra (the shared families already passed on the principals; the check is the felt heads' variety). A REC ROOM capture pre-lockdown (KEYART COMP B: Merle at centre, the club around, cobbler on the table, "not one sinister face") and a STUDIO A rows capture post-lockdown with the drift half a day ahead of Merle/Harriet/Vess in the same frame (a colour read of the garments). QA-26 (chairs tween, persist, no sound). A row-casualty capture: the empty chair and the interlaced applause held.

### 12.6 RISKS / OPEN
OPEN-17 (count and identities), OPEN-X1 (locomotion), height OPEN. Risk: six felt heads that read as six people without reading as a cast of caricatures; the plates give five faces of restraint to match.

---

## 13 · UNIT 2.9 (CAST ANIMATION SETS) AND UNIT 2.10 (GATE LINEUP) — the index this brief feeds

### 13.1 The clip inventory by rig (what 2.9 authors; every clip is specified in its §(4) above)

| Rig | Clips (proposed asset names) | Curve law | Physics |
|---|---|---|---|
| `SK_Merle` | Kettle_Busy, Walk_160, Chair_Busy, Screening, HandsStill (additive), 1974, PenUp_Hold, M1_Pat, M2_Sing, End_HandsIdle, End_Radiant | ease, warm, unhurried; the stills are hard stops | pendant only |
| `SK_Harriet` | Sway (or actor roll), Signals, CupDown, Drink; H1/H2 are states not clips | the freeze is a global play-rate 0.0, phase preserved | earrings, OFF on BREAK |
| `SK_Vess` | Catalogue, Tell_LabelMaker, Tell_Pin_Touch/Fist/Turn (additives), Screening_Eager, T45_Stand, Breaker_Hesitate, Breaker_Pull, CircuitF_Reach; V1 cut, V2 material | quick, precise | necklace only |
| `SK_Leland` | pose table ×40, 1A_StepToCentre, Door (one still) | NONE between frames; one continuous clip (1A) | none |
| `SK_Rita_Hands` / `_Reflect` | Idle, Walk, ClipboardRaise (200 ms ease-out), GloveAdjust, bench verbs, Switcher_*, Frame_OnMark | feel per RITA.h | lanyard chain only |
| `SK_FloorManager` | Stand, Signal_YoureOn/Cut/Stretch/WrapItUp/ThirtySeconds/OnTime/HoldApplause, Count, F1_Locked, RemoveHeadphones | single lerps (6/s arm, 4/s turn); no anticipation | none; no audio |
| `SK_Chum_Stage` (+ Understudy, PostFire, 4K) | StoryCorner, CraftTime, TheSong, QuietGame, Approach, Hold, Lunge (AM, 33 ms frame), FireTape_Unfinished, Live_Cue1..5, BellOnce, End_Small; 4K LeanIn | ease-heavy, bouncy, 15° stops | ON: ears, whiskers, tail, cloth; `bell` keyed once in one clip |
| `SM_Chum_1974` / `SM_Chum_1971` / `SM_Chum_PostFire_Stage` | none | — | none (LAW 4) |
| `SK_Cast_Unresolved` (OPEN-15) | Pass (< 2.0 s) | both grammars at once | strings only |
| `SK_Extra_*` | Sit_Idle, Applaud, HoldApplause, Sing_Home, Restrain, Row_Interlaced, Screening_Sit | gentle | none |

The two rigs' curve laws are checkable at review [PIPE-PROD ADDENDUM]: an F-curve scan per clip — humans ease; the stage puppet eases heavily; the FM's lerps are single; the AF body (RIG) is linear. A clip on the wrong side of that table is a defect before it is seen.

### 13.2 The GATE lineup (2.10) — "every figure beside its plate at matching framing" [DOSSIER §6; PLAN §R]

| Shot | Figure | Beside | Framing | State |
|---|---|---|---|---|
| 1 | Merle | PLATE-MERLE | three-quarter, hands at the waist; + turnaround strip | Kettle_Busy frame, KITCHEN, day locked-EV |
| 2 | Harriet | PLATE-HARRIET | seated, cup raised; + strip | Sway frame, REC, ON AIR; then the same frame on BREAK (identical) |
| 3 | Vess | PLATE-VESS | three-quarter; + strip | shrine wall; + T4 beard; + credited scarf |
| 4 | Leland | PLATE-LELAND | the plate's crop, through the ladder at G2 | pose 0 |
| 5 | Rita (Reflect) | PLATE-RITA | full body; then the bench over-the-shoulder (KEYART A) with the hands | night bench |
| 6 | Floor Manager | the KIT preview (no plate) | stack's end, night ON AIR; the seven signals at 9 m | Stand → Point |
| 7 | Chum 1974 + 1971 | the four plates (OPEN-6) / the BUILD renders | the dock rows under sodium; CHUM'S MARK under tungsten | static |
| 8 | Chum stage (footage) | — | the tape stage at G0 and G3: the hold before the lunge (NOT the lunge frame as a still) | Hold |
| 9 | the club | KEYART COMP B | REC, pre-lockdown, everyone | Sit_Idle |
| 10 | the sodium sheet | — | every cast wool and felt on ONE `--subject` contact sheet with `SK_Chum_AfterFire` | — |

Package as `ue/GATE-2.10.md` in the 0.10 format ("AWAITING OWNER REVIEW … nothing here is self-certified", P1 §1.13 quoting `ue/GATE-0.10.md`) with a §R scorecard per shot; the once-ever figure (§10) is NOT in the lineup by law (no still leaves the repo) — its review is a private capture sequence.

---

## SUMMARY

### The one-glance table

| Character | Unit | Height (canon / estimate / reference) | LAW bindings | Biggest realism risk |
|---|---|---|---|---|
| Merle Cottry | 2.2 | OPEN / **ESTIMATE 1.58 m** / KIT ≈ 1.6 | 7 (M1, M2); never-sinister (CASTING); NOT LAW 4 | busy hands on mitten hands reading as flippers; the 45 s statue reading as a bug |
| Harriet | 2.3 | OPEN / **ESTIMATE 1.63 m** / KIT ≈ 1.6 | 6 (freeze); 7 (H1, H2); DREAD L1 (the cup, never captioned) | a hard stop that is not total (one earring swinging in a BREAK); the H2 "two mouths" on a mouthless felt head |
| Vess Keys | 2.4 | OPEN-12 / **ESTIMATE 1.76 m** / KIT 1.67–1.78 | 7 (V1, V2) | the plastic pin not reading cheaper than enamel under sodium |
| Leland Merrick | 2.5 | OPEN / **ESTIMATE 1.78 m** / stage box 1.7 | 7 (L1, L2); never-voiced (AUDIO); never in marketing (KEYART) | a pose table that blends; the ladder baked into the pad |
| Rita Ivori | 2.6 | OPEN-3 / **ESTIMATE 1.70 m** (eye 1.60) / capsule 1.76 (88 uu half-height) | 7, 8, 9, 10, 11; wardrobe never drifts; gloves whitest | white cotton gloves under sodium and Lumen; no canon hand size for the most-seen asset |
| The Floor Manager | 2.6 variant | OPEN-4 / no plate, **REFERENCE 1.69 m** | 2 (never pops); 7 (F1, F2); 9 (shape-legible signals); S12 never heard moving | a black figure that is a hole in the frame; signals illegible at 9 m |
| Chum · 1974 stage | 2.7 | **seated 0.55 m canon** (FABRIC §3); reference 1.05 m standing — OPEN-13 | 4 (dock, static); 5 (bell once); 2 (the lunge, footage only) | the soft wool not reading as the same material as the AF wool |
| Chum · 1971 pilot | 2.8 | as 2.7 / OPEN-7 | 4; 5 (no bell exists) | "cruder" overdone into "damaged" |
| Chum · post-fire stage / 4K | not a box (OPEN-8) | as 2.7 / OPEN-14 | 5; 8 (the 4K clean image); KEYART no open mouths | mm-scale tells lost under the ladder; a groom the M1 Pro cannot afford |
| The Understudy / corridor figure | not a box | OPEN / **REFERENCE 2.5 m + bar 2.9 m** | 3 (once, ever; no name); 2 (no sting); ACH/KEYART silence | a mesh that resolves puppeteer vs puppet; a ported name |
| Ansel Craik | not a box (OPEN-16) | OPEN / none | LORE never-stated | over-authoring the one wide shot |
| The 58 Club rows / extras | not a box (OPEN-17) | OPEN / template default | 7 (THE ROWS); S10; KEYART warmth | six felt heads reading as caricature |

### Cast-wide OPEN added by this brief (beyond the dossier's OPEN-1..18)

OPEN-C1 (the head size that 1 : 5.5 produces at true height); OPEN-H1 (does Harriet ever stand); OPEN-V1 (a schedule for Vess); OPEN-L1 (which frame edge crops Leland); OPEN-R1/R2/R3 (Rita's glove fingers, downward-look body, body shadow); OPEN-F1..F4 (the FM's eyes, index finger, off-screen moves, two-handed signals and the sheet); OPEN-7a/7c (the 11th/12th 1974 patches; 1971 footage); OPEN-13b (dock stand height); OPEN-U1 (which phase owns the partials); OPEN-X1 (extras' locomotion).

### The cast-wide risk, in one paragraph

The single largest risk across Phase 2 is not any one character but the RENDER LANGUAGE decision the dossier logged as OPEN-1 and this brief has to build under: five photographic plates and a canon that says needle-felt, mitten hands and a 1 : 5.5 head, now to be authored at true height with actor scale 1.0. Read literally, that makes a life-size cast with puppet proportions and heads a third of a metre tall, no finger articulation, no faces that move, and gloved first-person hands that are "the most animated character in the game" without fingers to animate; read the other way (MetaHuman, plate likenesses) it breaks ART §1/§6, DESIGN Part II and PLAN §R.7 in one move and puts a photoreal face beside a felt puppet whose whole argument is that everything was made by the same hands. Every material table above is written for the crafted reading; every rig is written so that it survives either (the skeletons, the timings, the freeze, the point, the pose table and the one lunge do not care what the skin is). The mitigation is procedural and cheap: unit 2.1 builds ONE felt head at 1 : 5.5 and true height, one mitten with stitched definition, one white glove, and puts them beside PLATE-MERLE and the AF wool on a single sodium sheet in the locked-EV rig before any other cast unit starts — because if the felt head and the felt wool sit together as one crafted world, every character in this brief follows from the shared families and the shared skeleton; and if they do not, the owner rules OPEN-1 on a capture instead of on a paragraph, and only the material tables change.
