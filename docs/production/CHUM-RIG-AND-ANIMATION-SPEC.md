# RESTORATION · AFTER-FIRE CHUM · RIG AND ANIMATION SPEC

Purpose: one document a rigger (Blender) and an Unreal engineer (C++/AnimBP) can both work from without re-reading the canon. Every canon claim cites its source. Where canon is silent the entry says OPEN; nothing here is invented to fill a gap.

Primary source: `docs/canon/restoration-chum-motion-and-sound.md` (the corrected revision). Where the Godot reference implementation (`scripts/rundown.gd`) contradicts it, the corrected canon wins (see §0.2).

Sources used (cited below by short name):
| Short name | File |
|---|---|
| MOTION | `docs/canon/restoration-chum-motion-and-sound.md` |
| AF | `docs/canon/restoration-after-fire-chum.md` |
| LAWS | `docs/packet/portbrief/THE-LAWS.md` |
| DREAD | `docs/canon/restoration-dread-doctrine.md` |
| PIPE | `docs/canon/restoration-blender-ue5-pipeline.md` and the production copy `docs/production/restoration-blender-ue5-pipeline.md` (which adds the ADDENDUM · ANIMATION EXPORT) |
| AUDIO | `docs/production/restoration-audio-bible.md` |
| QA | `docs/production/restoration-qa-regression.md` |
| INV | `docs/production/restoration-invariant-suite.md` |
| PLATE | `docs/canon/art/after-fire-chum-dossier.png` (file CHUM-AF-1974-P (REV.)) |
| BRAIN | `ue/Restoration/Source/Restoration/Rundown.h`, `Rundown.cpp` |
| STATE | `ue/Restoration/Source/Restoration/RestorationState.h` |
| BUILD | `tools/build_chum_af.py` (the puppet's geometry and object names) |
| GD | `scripts/rundown.gd` (Godot reference implementation; executable spec per PIPE, superseded where §0.2 says so) |
| TIMINGS | `ue/Restoration/Data/Timings.csv` |
| DOORS | `ue/Restoration/Data/Doors.csv` |
| PLAN | `AAA_BUILD_PLAN.md` (Phase 1 units 1.9 to 1.12) |

---

## 0 · THE ONE SENTENCE, AND WHAT SUPERSEDES WHAT

### 0.1 The grammar in one line
"PUPPET GRAMMAR DELETED. No anticipation, no overshoot, no settle, no secondary motion of any kind ... he is pouring or he is parked, statue-still, zero idle sway, no breathing, while the eye alone keeps tracking, servo-smooth." (MOTION §AFTER-FIRE · THE UNOPERATED BODY.) Curve law: "LINEAR IS THE HORROR CURVE: linear-dominant with two-frame ease caps at most." (same section.)

Three authored exceptions, and only three (MOTION §AFTER-FIRE): THE FOLD (2.2 s at every doorway), THE WITHDRAWAL (reverse along the exact approach path), THE PERFORMANCE QUOTE (frontal square-up at 1.2 m plus one clean fifteen-degree head tilt).

Hard rules (MOTION §AFTER-FIRE, "Hard rules, corrected to the dossier"): the jaw opens ONLY by his own hand via the mouth lever ("pulled to open, pushed to close, no motors"); every opening is a two-beat act ("the hand rises, one dry click, the jaw"); the jaw has exactly two grammar entries (lever work under the tally; once before a strike); "The jaw NEVER syncs to any sound, never flaps, never chews the air"; "THE BELL NEVER SOUNDS (clapperless by canon)"; "NO VOCALIZATIONS, EVER". LAWS 5 restates the bell and the silence: "Chum's bell is otherwise silent; Chum speaks nowhere." LAWS 2: "ONE STARTLE ... Nothing else lunges, stings, or pops."

### 0.2 Godot reference behaviours that the corrected canon supersedes
The Godot brain is the executable spec for TIMING and STATE ORDER (PIPE §intro; BRAIN header: "Verbatim port of scripts/rundown.gd"). Its procedural POSE code predates the corrected motion doctrine and must NOT be ported as-is. Do not port these:

| GD behaviour (line) | Why it is superseded | Ruling source |
|---|---|---|
| Walk bob `_rig.position.y = abs(sin)*0.1` and roll `rotation.z = sin*0.05` (GD 393-400) | "silhouette always at full height", "nothing on him bounces, ever" | MOTION §AFTER-FIRE |
| Arm counter-swing, tail sway on the walk (GD 402-405) | "no secondary motion of any kind" | MOTION §AFTER-FIRE; QA-53 |
| ON AIR idle "the segment, performed to no one": jaw `sin`-flap, sway, shoulder wave, tail (GD 414-428) | "The jaw NEVER ... flaps"; "zero idle sway" | MOTION §AFTER-FIRE |
| `_work_jaw` tweens the JAW ONLY with `TRANS_SINE` (GD 358-366) | The jaw opens only by the hand at the lever (two-beat act); curves linear-dominant | MOTION §AFTER-FIRE |
| `_pose_fold` "compresses, ducks, pulls the arms in" with a sine envelope (GD 458-471) | "he does not duck, he REORGANIZES: shoulder through first, then the head arriving late"; "one authored montage ... no procedural blending" | MOTION §AFTER-FIRE; QA-52 |
| Standing "everything eases home" lerps (GD 431-439) | "Stops are ABSOLUTE and binary" | MOTION §AFTER-FIRE |

Keep from GD (they are timing/state, and canon agrees): the constants (TIMINGS), the head-rest tilt `HEAD_TILT 0.045` ("delta 8: the restitched neck, never straight", GD 373), the tally eye burning only while `af_active and recording` (GD 241; AF §THE SCALE LAW), the captions `[THE JAW WORKS ITS LEVER]` (GD 267; AF §SOUND AND CAPTION LAW) and `[IT FOLDS THROUGH THE DOORWAY]` (GD 343).

---

## 1 · RIG

### 1.1 Scale and coordinate contract
| Item | Value | Source |
|---|---|---|
| Blender units | metres; scene built in metres | PIPE §STANDARDS; BUILD docstring lines 5-10 |
| Export scale | 1 m = 100 uu; `apply_unit_scale=True`, `FBX_SCALE_NONE`; verified on the 1 m cube = 100.0 uu | PIPE §STANDARDS; `tools/export_ue.py` lines 39-43; README commit 075 |
| UE axes | X-forward, Z-up | PIPE §STANDARDS |
| Blender build axes | Z-up, front is -Y; head empty at (0, 0, 2.28); jaw empty child of head at the hinge | BUILD docstring lines 7-10 |
| Build height at scale 1.0 | body built at "2.6 m base height"; ear tips reach about 3.08 m (EarR cone centre z 2.78, half-height 0.26 → tip about 3.04 before displacement) | BUILD docstring line 5; BUILD lines 614-617; measured 3.08 m on import: PROGRESS 0.3, `ue/GATE-0.10.md` §3, README commit 075 |
| Canon wake height | "the body stands 3.35 meters the moment he wakes, the tally eye sits at three meters" | AF §THE SCALE LAW; TIMINGS `AF_HEIGHT 3.35`, `BASE_HEIGHT 2.6`; GD 238 scales the rig by `AF_HEIGHT / BASE_HEIGHT` = 1.2885 |
| Arithmetic that the rigger must know | TallyLens is built at z ≈ 2.34 (BUILD line 802). At scale 1.0 the eye sits at ≈ 2.34 m; at ×1.2885 it sits at ≈ 3.01 m, which is the canon "three meters". At the imported 3.08 m (scale 1.0) the eye is NOT at three metres. | derived from BUILD + AF §THE SCALE LAW |
| Ruling needed | Whether SK_Chum_AfterFire is authored at scale 1.0 (3.08 m ear tips, eye 2.34 m) and the brain applies the wake scale as actor scale exactly as GD 238 does, or authored at 3.35 m body with the eye at 3 m and actor scale 1.0. See OPEN-1. Either way: ONE uniform scale, applied and frozen before export, never per-bone; no runtime bone scaling. | OPEN-1 |

Rest pose is scale-true whichever ruling lands: "scale-truth" is the gate question the owner is asked in `ue/GATE-0.10.md` §4.

### 1.2 Naming and export
| Item | Value | Source |
|---|---|---|
| Skeletal mesh | `SK_Chum_AfterFire` | PIPE production ADDENDUM · ANIMATION EXPORT |
| Sockets (on the skeleton) | `SOCKET_JawLever`, `SOCKET_EyeTally`, `SOCKET_Bell` (clapperless) | PIPE §STANDARDS |
| Materials / textures | `M_` / `MI_`; `T_*_BC/_N/_ORM`; the 30 baked instances wired from the Blender-written manifest by `ue/pyscripts/fixup_materials.py` | PIPE §STANDARDS; README commit 075 |
| Collision | `UCX_` children in Blender | PIPE §STANDARDS |
| Physics | ALL physics secondaries DISABLED; wool baked stiff; no cloth, no AnimDynamics, no physics asset bodies that can move (a physics asset for collision queries only, all bodies kinematic, is acceptable) | MOTION §PRODUCTION NOTES; PIPE production ADDENDUM; QA-53 |
| Clips | root-motion authored clips only; the fold as one montage per door width; the eye on an always-on aim layer | MOTION §PRODUCTION NOTES; PIPE production ADDENDUM |
| Curve discipline at review | AF clips linear-dominant, ease caps of two frames at most; "checkable at review" | PIPE production ADDENDUM; MOTION §AFTER-FIRE |
| Export mechanics already learned | packed images are invisible to FBX: unpack all bakes to disk first; the FBX importer reuses textureless materials on re-import: fixup wires the PNGs directly. The static-mesh path FLATTENS parent empties with KEEP_TRANSFORM (`tools/export_ue.py` lines 87-95): the skeletal path must NOT flatten; the empties become bones (§1.3). | README commit 075; `tools/export_ue.py` |
| Sodium gate | `tools/sodium_check.py --subject` on the skinned mesh before export; the AF wool "must read as the same material that forgot how to be soft" | MOTION §PRODUCTION NOTES; PIPE §MATERIAL MASTERS |

### 1.3 Bone list
Conventions: bone names are CHARACTER-relative (`_l` is the character's own left), the UE convention. BUILD object names are VIEWER-relative (BUILD 614: "mustard viewer-left, navy viewer-right" for `EarL`/`EarR`; BUILD 737/770 "LEFT EYE"/"RIGHT EYE" likewise; the fabrication brief uses viewer-left/right too). In the build, front is -Y, so viewer-right = +X = the character's LEFT. The mapping column below is therefore deliberate: `EarR` (+X) skins to `ear_l`. Rest positions are Blender world metres at build scale 1.0 (see §1.1 for the scale ruling). Rotation locks are the doctrine's "no secondary motion" made mechanical.

| Bone | Parent | Rest position (Blender m, scale 1.0) | Drives (BUILD object names) | Locks / notes | Source |
|---|---|---|---|---|---|
| `root` | — | (0, 0, 0) floor | root motion carrier | The only bone that translates in a pour clip. | PIPE ADDENDUM (root-motion clips) |
| `pelvis` | root | (0, 0, 0.98) | `BodyCore` pelvis/hip lobes, `PatchLeather` | | BUILD 336-340, 496 |
| `spine_01` | pelvis | (0, 0, 1.40) | `BodyCore` belly mass, `Belly`, `PatchRust`, `PatchGreen`, `BodyFur` (lower) | | BUILD 334, 348-350, 493-494 |
| `spine_02` | spine_01 | (0, 0.02, 1.80) | `BodyCore` chest + shoulder lobes, `PatchFlannel`, `ThroatSpeaker`, `BodyFur` (upper) | The throat speaker is rigid to the chest; it "breathes" only in audio (band-limited room tone), never in mesh. | BUILD 335, 467-469, 495; MOTION §THE THROAT SPEAKER |
| `neck` | spine_02 | (0, 0, 2.02) | `Collar` | | BUILD 459-461 |
| `bell` | neck | (0, -0.27, 1.94) | `Bell`; carries `SOCKET_Bell` | ALL rotation and translation locked. No physics body, no jiggle, never keyed in any AF clip. "THE BELL NEVER SOUNDS (clapperless by canon; the absence is the tell)"; "if the model ever swings it, it is clapperless, and the caption for that is nothing." A visibly swinging bell implies a sound; the lock is how the rig keeps the law. | MOTION §AFTER-FIRE; AF §SOUND AND CAPTION LAW; LAWS 5; PIPE §STANDARDS |
| `head` | neck | (0, 0, 2.28), rest rotation 0.045 rad about the build's Y (the restitched-neck tilt, baked into the rest pose) | `Skull`, `SkullFur`, `SkullFuzz`, all `FacePanel*`, `SkullPatch*`, `BurnField`, all `Seam*`, `CrownSeamStitches`, `BorderStitch*`, `XT*`, `Nose`, `SocketL`, `GearTooth*`, `ButtonEye`, `BtnHole*`, `ScorchRay*`, `MeltDrip`, `LensRing`, `LensRivet*`, `MawVoid`, `LipU`, `LipStaplesU`, `ToothU*`, `Grille*`, `HingeBolt-1`, `HingeBolt1`, all `Whisk*` | The Head empty is the exact pivot GD rotates. The 0.045 rad rest tilt is canon ("never straight") and is distinct from the 15-degree performance tilt (§2, shot L2). Whiskers are rigid: the pre-fire "whiskers tremble" is deleted grammar. | BUILD 499-500; GD 373, 455; TIMINGS `HEAD_TILT 0.045`; MOTION §PRE-FIRE vs §AFTER-FIRE |
| `jaw` | head | (0, 0.06, 2.10) as built; hinge bolts sit at (±0.28, -0.30, 2.17) | `JawVoid`, `JawMesh`, `JawFur`, `LipL`, `LipStaplesL`, `ToothL0-3`, `ChinBand0-8`, `ChinRivet*`, `JawBar2.1`, `JawBar2.06`, `JawLever` | Single axis: rotation about the hinge axis only (the build's X); other axes locked. The lower jaw is "on hinge with lever linkage" (PLATE detail 4). Pivot: the Jaw empty is what the reference implementation rotates; whether to move the pivot onto the HingeBolt line is the rigger's call (OPEN-4). Range reference: GD opens to 0.55 rad for lever work and 0.9 rad for the strike. | BUILD 976-1055; PLATE §MANUAL JAW CONTROL BREAKDOWN; GD 364, 478 |
| `lever_grip` | head | (0.115, -0.372, 2.14); rod below it at (0.115, -0.355, 2.075), 0.13 m long, tilted -14° | `MouthLeverGrip`, `MouthLeverRod`; carries `SOCKET_JawLever` | The hand lever INSIDE the mouth (PLATE detail 4: "HAND LEVER (INSIDE MOUTH) → LINKAGE ROD TO LOWER JAW → LOWER JAW ON HINGE"). Mechanical coupling: a driver (Blender) / a copy-rotation with a scalar in the AnimBP (UE) so grip angle is a fixed function of jaw angle: PULLED = open, PUSHED = closed. The grip is on the +X side (viewer-right = character's left), the same side as the tally lens. | BUILD 936-945; PLATE §MANUAL JAW CONTROL BREAKDOWN; MOTION §AFTER-FIRE hard rules |
| `eye_tally` | head | (0.13, -0.37, 2.34) at the LensRing centre; lens barrel `TallyLens` seated at (0.13 - 0.008×2.75, -0.2425, 2.34 - 0.034×2.75) | `TallyLens`; carries `SOCKET_EyeTally` (the emissive core and the red light attach here; GD places the omni at head-local (0.13, 0.06, 0.34), energy 1.6, colour (0.9, 0.15, 0.1), range 6.0, ON only while `af_active and recording`) | The ONLY bone allowed to move while parked: "the eye alone keeps tracking, servo-smooth". Aim constraint, always-on layer. Rotation only; no translation. Aim limits: OPEN-6 (GD tracks the whole HEAD with yaw clamped ±1.05 rad at lerp 3.5/s inside 11 m; canon says the eye). The red light "burns ONLY while a capture runs". | BUILD 770-803; GD 83-100, 241, 441-455; MOTION §AFTER-FIRE; AF §THE SCALE LAW; PIPE §STANDARDS |
| `ear_r` | head | cone centre (-0.24, 0.03, 2.78), tilt -13°, height 0.52×0.74 (the singed, shorter ear) | `EarL`, `EarLPanel`, `EarLEdgeStitches`, `EarLBlanketStitches`, `EarLFur` | Pose-only. Never keyed in AF clips: "ears lag" is pre-fire grammar, deleted. Exists so the stage rig and this rig share a bone map, and for one-off still posing. | BUILD 614-731; MOTION §PRE-FIRE vs §AFTER-FIRE |
| `ear_l` | head | cone centre (0.24, 0.03, 2.78), tilt +13°, height 0.52 | `EarR`, `EarRPanel`, `EarREdgeStitches`, `EarRBlanketStitches`, `EarRFur` | As `ear_r`. | BUILD 614-731 |
| `clavicle_r` / `clavicle_l` | spine_02 | (∓0.45, -0.01, 1.71) at the `SeamRing` | `ArmLSeamRing`/`ArmRSeamRing`, `ArmLSeamStitch*`/`ArmRSeamStitch*` | The stitched ring where the arm was sewn back on. The fold's "shoulder through first" is authored here and on upperarm. | BUILD 406-417; MOTION §AFTER-FIRE (THE FOLD) |
| `upperarm_r` / `upperarm_l` | clavicle | Shoulder empty (∓0.47, 0, 1.72) | `ArmL`/`ArmR` upper lobes, `ArmLFur`/`ArmRFur` (upper), `ArmLTendonA*`/`ArmRTendonA*`, `ArmLGuide1.55`/`ArmRGuide1.55` | The Shoulder empty is the pivot GD rotates. Tendon cables skin rigidly to the segment they run along; they do not sag or swing (no secondary). Left arm (`ArmL`, viewer-left = `_r` here) carries three tendons; the other carries one survivor. | BUILD 378-441 |
| `lowerarm_r` / `lowerarm_l` | upperarm | elbow (∓0.55, -0.03, 1.26) | `ArmL`/`ArmR` forearm lobes, `ArmLElbowWrap`/`ArmRElbowWrap`, `ArmLTendonB*`/`ArmRTendonB*`, `ArmLGuide1.26`, `ArmLGuide1.0` (and R) | | BUILD 383-384, 418-441 |
| `hand_r` / `hand_l` | lowerarm | wrist (∓0.60, -0.06, 0.97); palm centre (∓0.62, -0.07, 0.90) | `ArmLHand`/`ArmRHand` palm | IK target for the lever (shot L3, T1). A hand IK chain (upperarm→lowerarm→hand) with the effector at `SOCKET_JawLever` is REQUIRED so the "hand rises" beat lands on the grip at any head yaw. | BUILD 393-400; MOTION §AFTER-FIRE hard rules |
| `finger_[a|b|c]_01_r/l` | hand | finger roots at x = 0.53, 0.62, 0.71 (×side), y -0.10, z 0.80 | first lobe of each of the three fingers | Two-lobed fingers per BUILD. | BUILD 394-397 |
| `finger_[a|b|c]_02_r/l` | finger_01 | second lobe at (x+0.012, -0.13, 0.73) | second lobe + `ArmLClaw0-2`/`ArmRClaw0-2` (the claw sheath is rigid to the last lobe) | | BUILD 396-405 |
| `thigh_r` / `thigh_l` | pelvis | Hip empty (∓0.20, 0, 0.92) | `LegL`/`LegR` upper lobe, `LegLFur`/`LegRFur` (upper), `LegLRod`/`LegRRod` | The Hip empty is the pivot GD rotates. "knees nearly stiff, stride long, cadence slow" (MOTION). The exposed leg control rod (PLATE detail 5: "internal rods linked to knee and ankle") skins rigidly to the thigh. | BUILD 353-374; MOTION §AFTER-FIRE |
| `calf_r` / `calf_l` | thigh | knee (∓0.20, 0, 0.46) | `LegL`/`LegR` lower lobes | Knee flex kept minimal in clips per "knees nearly stiff". | BUILD 357-358 |
| `foot_r` / `foot_l` | calf | ankle (∓0.20, -0.02, 0.20) | the weighted foot lobe (∓0.20, -0.09, 0.11) | "WEIGHTED FOOT BASE" (PLATE). The sub-heavy footfall (AUDIO S17) is an anim notify on this bone's plant. | BUILD 359; PLATE; AUDIO S17 |
| `ball_r` / `ball_l` | foot | toe lobes at y -0.30, z 0.09 | three toe lobes | Pose-only. | BUILD 360-362 |
| `tail_01` | pelvis | TailPivot (0.04, 0.36, 0.76) | `Tail` lobes 1-2, `TailFur` | "tail, dragging low" (BUILD 443). Pose-only in AF: the tail does not sway (no secondary). GD's tail swing is superseded (§0.2). | BUILD 443-456; MOTION §AFTER-FIRE |
| `tail_02` | tail_01 | (0.28, 0.78, 0.30) | lobes 3-5 | Pose-only. | BUILD 447-450 |

Not bones (skin to the nearest bone above): all fur-card objects (`BodyFur`, `SkullFur`, `LegLFur` ... ) skin 100% to their host's bone so the coat is as stiff as the wool it grows from (MOTION §PRODUCTION NOTES "wool baked stiff"); `ChinBand*`/`ChinRivet*` are the "riveted chin strap (manual jaw hinge assembly)" and ride the jaw (BUILD 1023-1040); `HingeBolt*` ride the head (BUILD 1042-1046).

### 1.4 Control conventions (Blender)
| Control | Rule | Source |
|---|---|---|
| Interpolation default | LINEAR. Bezier permitted only as an ease cap of ≤ 2 frames at a clip's start/stop. Reviewers check the F-curves, not the render. | MOTION §AFTER-FIRE; PIPE ADDENDUM |
| Stops | Binary: a pour clip ends on its last linear frame, then the park pose holds; no settle, no overshoot, no follow-through. | MOTION §AFTER-FIRE ("Stops are ABSOLUTE and binary") |
| Jaw + lever | A single driver: `jaw` rotation drives `lever_grip` (mechanical linkage). A jaw key without the hand IK on the grip is a canon defect: "a jaw hanging open with no hand at work is canon-wrong. Default resting pose: jaw closed, hand down." | PLAN §Motion & sound law (CAPTURE CANON); MOTION §AFTER-FIRE |
| Eye | `eye_tally` on its own always-on action layer; aim-constrained to a target empty; NEVER baked into body clips (the AnimBP layers it). | MOTION §PRODUCTION NOTES; PIPE ADDENDUM |
| Bell, ears, tail, whiskers, tendons | Locked or pose-only; never keyed in AF actions. A "zero-secondary sweep" is a QA item. | QA-53 |
| Facing | The body faces its PATH (the movement vector), never the player: "He never orients to the player as a person; he faces PATHS". Only the loom clip squares him to the player, and only under the tally. | MOTION §AFTER-FIRE; §THE PERFORMANCE QUOTE |
| Root motion | Authored on `root` for every locomotion clip (pour, withdrawal). In-place for park, loom, lever work, telegraph, strike, cool. Fold: see OPEN-3. | MOTION §PRODUCTION NOTES; BRAIN (position is set by the brain, §3.2) |
| Frame rate | OPEN-7 (canon states the ease cap in frames but never the authored rate). |

---

## 2 · ANIMATION SHOT LIST

One row per brain state. Blender action name = UE asset name (sequence `AS_`, montage `AM_`). Constants are BRAIN `Rundown.h` lines 23-31, identical to TIMINGS. Timings are in seconds of game time; the brain's `Tick` is the clock (`GetWorld()->GetTimeSeconds()`).

Universal MUST-NOTs, in force on every row (not repeated per row): no lunge, no sting, no pop (LAWS 2; DREAD §ANTI-CREEP "Random scares. Musical stings."); no vocalization (MOTION hard rules; LAWS 5); the bell never moves enough to imply a sound (MOTION; AF §SOUND AND CAPTION LAW); no secondary motion, no idle sway, no breathing (MOTION §AFTER-FIRE); the jaw never opens without the hand at the lever, and never in sync with any sound (MOTION hard rules; PLAN CAPTURE CANON); no text says "creepy" (DREAD §ANTI-CREEP).

### 2.1 Locomotion and the parked body

| # | Brain state | Action / asset | Duration | Timing tied to | What the body does | Must NOT | Trigger in ARundown |
|---|---|---|---|---|---|---|---|
| P0 | PARK (idle at segment anchor; also the ON AIR hunt while the prey is out of reach; also the dead-door hold; also the cool) | `AS_ChumAF_Park` | loop; effectively a held pose plus the eye layer | none | Statue. Full height, weight even, hand down, jaw closed. Only `eye_tally` moves (servo-smooth). | Sway, breathe, shift weight, "perform to no one" (GD 414-428 is superseded). Must not face the player; faces the path he arrived on. | Any tick in which the brain sets no new location: night gate returns (`Rundown.cpp` 341-345); ON AIR with no strike/warn (362-404, no `SetActorLocation` in that branch); at anchor after BREAK move converges (356-358). |
| P1 | BREAK move-to-target (relocation walk) | `AS_ChumAF_Pour_240` (root motion, 2.4 m/s) | loop; length OPEN-5 | `MoveSpeed 2.4` (`Rundown.h` 23); the brain moves the actor by `VInterpConstantTo` at 2.4 m/s (`Rundown.cpp` 356-358) | THE POUR: "single-axis commitment, the head leading and the body arriving in one uninterrupted arc, knees nearly stiff, stride long, cadence slow, silhouette always at full height". Linear curves. Footfall notify on each plant (AUDIO S17, "interval-driven"). | Bob, roll, arm swing, tail sway, ease-in/out beyond 2 frames, any anticipation before the first step. | `OnPhaseChanged(false)` sets `Target` (`Rundown.cpp` 168-188) and logs `RELOCATE toward heard noise at <pos> -> segment N` or `RELOCATE cycle -> segment N (profile UNKNOWN)`; the walk itself is the `!bOnAir` branch each tick (350-360). |
| P2 | AF approach (tally lit) | `AS_ChumAF_Pour_080` (root motion, 0.8 m/s) | loop | `AfApproachSpeed 0.8` (`Rundown.h` 24); `Rundown.cpp` 293-296 | The pour at the slow cadence. The eye is LIT (red) the whole approach: "the tally eye ... burns ONLY while a capture runs" (AF §THE SCALE LAW). He "crosses the room BECAUSE you are safe" (DREAD L4). | Speed up, lean in, reach. "PATIENCE AT SCALE: he waits at 1.2 m; waiting is scarier than lunging" (DREAD §AMPLIFIERS). | AF layer, `State->bRecording && Prey` and `Pd > AfLoomDist` (`Rundown.cpp` 291-297). |
| P3 | AF dead-room approach | `AS_ChumAF_Pour_080` (same clip) | loop | `AfApproachSpeed 0.8`; hold radius 0.6 m of `DeadDoor (1900, 0, 0)` uu (`Rundown.cpp` 277-282) | The pour toward the felt door, folds paid en route. | As P2. | AF layer, `State->InDeadRoom(Prey)` and distance to `DeadDoor` > 0.6 m (`Rundown.cpp` 275-283). |
| P4 | AF dead-room HOLD at the felt door | `AS_ChumAF_Park` | hold until the capture ends | none (holds while `bRecording`) | Parked at the felt door, eye lit and tracking the door. "at its felt door he stops, holds, and says nothing further" (AF §THE TWO HIDES). | Touch the door, lean, look around, any beat. | Logged once: `AF holds at the felt door` (`Rundown.cpp` 284-288; `bDeadroomLine`). LAWS 11. |
| P5 | The Crossing (ending 4) | `AS_ChumAF_Pour_160` (root motion, 1.6 m/s) | loop | `AfCrossingSpeed 1.6` (`Rundown.h` 29); "him behind her at double approach speed" (AF §THE LAST CROSSING) | The pour at 1.6 m/s, eye DARK "the whole way" (AF §THE LAST CROSSING); folds still 2.2 s each. | Eye lit. Any change of grammar for the chase: it is still the pour. | NOT YET WIRED: `AfCrossingSpeed` is declared (`Rundown.h` 29) but no branch in `Rundown.cpp` uses it; GD 205-226 is the reference (`GameState.crossing`). Engineer hook: OPEN-8. |
| P6 | Hidden / teleport | none (cut to hidden) | 0 | immediate | Nothing: `SetActorHiddenInGame(true)` then teleport to the segment anchor. He is "gone until the next contract". | Any fade, dissolve, or visible exit. | `Rundown.cpp` 333-334 (after the cool) and 395 (after a night STRIKE, teleport without hiding). |

### 2.2 The three authored exceptions

| # | Brain state | Action / asset | Duration | Timing tied to | What the body does | Must NOT | Trigger in ARundown |
|---|---|---|---|---|---|---|---|
| F1 | THE FOLD at a doorway (door toll) | `AM_ChumAF_Fold_120`, `AM_ChumAF_Fold_140`, `AM_ChumAF_Fold_160` — one montage per door width; DOORS carries exactly three widths: 1.2 m (2 doors), 1.4 m (11), 1.6 m (7) | exactly 2.2 s each | `AfFoldSeconds 2.2` (`Rundown.h` 27); `FoldT = AfFoldSeconds` (`Rundown.cpp` 205); the brain freezes position and returns early every tick while `FoldT > 0` (221-225) | "he does not duck, he REORGANIZES: shoulder through first, then the head arriving late on a hinge that should not exist: the one place puppet logic returns, horribly, rod movement without rods." (MOTION §AFTER-FIRE.) Order inside the 2.2 s: clavicle/upperarm lead, torso follows, head LAST (QA-52 "head arrives last"). The eye stays on the player throughout: "bending and keeping his eye on you the whole way through" (AF §THE SCALE LAW). Audio: S18 "dry frame creak, 2.2 s envelope, no sting" plus "one soft textile drag and a single low wooden knuckle as the head arrives" (MOTION §Sound; AUDIO S18). Caption `[IT FOLDS THROUGH THE DOORWAY]` (GD 343). | Duck, crouch, compress downward (GD `_pose_fold` is superseded); procedural blending ("no procedural blending", QA-52); any speed-up after; any sting. | `DoorFoldCheck(Now)` true (`Rundown.cpp` 191-211): within `AfDoorNear 1.0` m of a `DoorPositions[i]` (from DOORS cols gap_x, gap_z) with a 6 s per-door cooldown. Called from BREAK move (352), AF approach (293), dead-room approach (280). Width selection: the brain stores only positions; the montage picker must look up DOORS row `i+1` width (see §3.4). LAWS 11: "every threshold costs him 2.2 s, and that toll is the player's counterplay." |
| W1 | THE WITHDRAWAL (tally cooled with the player out of reach) | `AS_ChumAF_Pour_080` played at rate -1.0 along the recorded approach path (or `AS_ChumAF_Withdraw` = the same clip reversed and exported, if the AnimBP cannot reverse) | until he reaches the segment anchor or is hidden (OPEN-9) | none in canon beyond "cools with distance" | "he reverses along his exact approach path without turning, motion played backward, an undo." (MOTION §AFTER-FIRE.) Eye dark (tally lapsed). | Turn around, look back, change cadence. | NOT SIMULATED as motion by the brain: after the cool, if the player is outside `StrikeR + 0.4` m the brain hides him and teleports him to the anchor (`Rundown.cpp` 326-334). GD does the same (`visible = false`). The withdrawal is therefore a presentation-layer clip that must play before the hide; see OPEN-9. "If you are clear, he withdraws to his segment" (AF §THE TALLY CONTRACT). |
| L1 | THE PERFORMANCE QUOTE, part 1: square-up at the loom | `AS_ChumAF_Loom_Square` (in place) | OPEN-5 (canon gives no duration for the square-up) | fires when `Pd <= AfLoomDist 1.2` (`Rundown.h` 25) | "he squares FULLY FRONTAL to you, broadcast stance" (MOTION §AFTER-FIRE). This is the one clip in which the body turns to the player. Eye lit; "at loom distance the player is looking up into it" (AF §THE SCALE LAW). Throat speaker bed: band-limited room tone (MOTION §THE THROAT SPEAKER; AUDIO). | Step closer than 1.2 m; lean; reach. Occur when the tally is dark (QA-53: the performance quote "occurs only while the tally burns"). | Logged once per contract: `AF loom d=%.1f (the jaw works its lever)` (`Rundown.cpp` 298-302, `bAfSeenOnce`). Caption `[THE JAW WORKS ITS LEVER]` (GD 267; AF §SOUND AND CAPTION LAW). LAWS 10. |
| L2 | THE PERFORMANCE QUOTE, part 2: the one tilt | `AS_ChumAF_Loom_Tilt` (in place; head only, on top of L1's pose) | a "clean fifteen-degree stop" (MOTION §PRE-FIRE describes the stop; §AFTER-FIRE permits exactly one) | none | "permits himself exactly one pre-fire mannerism: the clean fifteen-degree head tilt. THE TALLY TURNS HIM BACK INTO A PERFORMER." (MOTION §AFTER-FIRE.) The 15° is IN ADDITION to the permanent 0.045 rad rest tilt. This is the ONLY place a pre-fire ease is allowed on this rig (the tilt "lands" in a classic puppet stop). | Repeat (it is one tilt, not a nod); tilt outside the lit tally; tilt during the approach. | Same trigger as L1; sequencing L1→L2 is the AnimBP's (§3). Direction of tilt and its exact ease: OPEN-10. |
| L3 | THE PERFORMANCE QUOTE, part 3: the jaw hand works its lever | `AS_ChumAF_LeverWork_A/B/C` (in place; a small set of two-beat opens/closes of differing lengths, sequenced at random so there is "no rhythm a song would keep") | each act: hand rises → click → jaw opens → (hold) → hand pushes → jaw closes. GD reference timing, NOT canon: open 0.45 s, close 0.6 s, gap 0.4 s, twice (GD 361-366). | none beyond "while the tally burns" | "the jaw hand works its lever open and closed at no rhythm a song would keep: a show with the sound removed, performed at you." (MOTION §AFTER-FIRE.) Two-beat act every time: "the hand rises, one dry click, the jaw." The hand IK lands on `SOCKET_JawLever`; jaw and grip are linked (§1.3). AUDIO S25 THE LEVER: "one dry mechanical click ... plays on every jaw opening". Body otherwise a statue: "The jaw hand moves. Nothing else does." (GD 268 toast, consistent with canon.) | Open the jaw without the hand on the grip; flap; sync to any sound; any periodic rhythm; any motion elsewhere on the body. | Same trigger as L1; loops while `bRecording` holds and `Pd <= 1.2` (the brain re-enters the loom branch every tick, `Rundown.cpp` 291-304). |

### 2.3 The contract lapsing, and the strike

| # | Brain state | Action / asset | Duration | Timing tied to | What the body does | Must NOT | Trigger in ARundown |
|---|---|---|---|---|---|---|---|
| C1 | THE TALLY COOLS (taught, first ever) | `AS_ChumAF_Park` with the eye light extinguished at t=0 | 4.0 s | literal `4.0f` (`Rundown.cpp` 310) | Statue. Hand down, jaw closed. Eye dark. "THE TALLY COOLS. Two doorways stand between you and anywhere. Use them." (AF §THE TAUGHT CHASE; GD 279.) | Move, creep, close the distance during the cool (the brain moves nothing during the cool: `Rundown.cpp` 321-337 sets no location). Any tell that reads as a wind-up. | `AfCool = 4.0`, `bAfTaught = true`, log `AF tally cools (taught)` (`Rundown.cpp` 307-315). Conditions: `!bRecording && !bIsNight && !IsHidden()`. LAWS 10 ("the cool is 2.0 s and announced"; the 4.0 s first cool is AF §THE TAUGHT CHASE). |
| C2 | THE TALLY COOLS (every later time) | `AS_ChumAF_Park`, eye dark | 2.0 s | `AfCoolSeconds 2.0` (`Rundown.h` 26) | As C1. | As C1. | log `AF tally cools` (`Rundown.cpp` 316-319). |
| T1 | The pre-strike TELEGRAPH (jaw grammar entry 2) | `AS_ChumAF_Telegraph` (in place) | 0.9 s | QA-54: "the single pre-strike telegraph with its 0.9 s beat" | "Outside the light, the jaw opens exactly once: the beat before a strike, hand rising, click, open, and then the near-silence." (MOTION §AFTER-FIRE.) Hand IK to the grip, S25 click on the opening, jaw stays open into S1. | Lunge, lean, wind up, any arm motion other than the lever hand. Any sound but the click. | NOT IN THE BRAIN as a timed beat: both strike paths call `State->Strike(Prey)` in the same tick they decide (`Rundown.cpp` 329-330 and 390-393) and immediately teleport (334, 395). See OPEN-2 for where the 0.9 s lives. |
| S1 | STRIKE (night hunt) | `AS_ChumAF_Strike` (in place) | OPEN-5 | `StrikeRadius 2.2` (`Rundown.h` 31); widened to 2.6 when `StrikesNow() >= 3` (`Rundown.cpp` 164), the savor rule | "The strike is nearly silent: one textile sweep, then the authored silence, because the loudest thing he ever does is stop making sound." (MOTION §Sound.) GD reference pose, NOT canon: both arms rise to -1.6 rad at 8 rad/s, jaw to 0.9 rad, body lean 0.18 rad (GD 474-479). "a hand the size of a door" (AF §THE LAST CROSSING). | Lunge (LAWS 2: the in-tape lunge is the game's single startle); sting; roar; camera shake. Every death "ends in authored silence" (DREAD §AMPLIFIERS; AUDIO silence ledger ≥ 1.5 s). | `D < StrikeR && StrikeCooldown <= 0` in the ON AIR branch (`Rundown.cpp` 376-397): log `STRIKE seg N d=X[ savor][ THRU-WALL]`, `State->Strike`, cooldown 3.0 s, teleport to anchor, `bWarned = false`. |
| S1s | STRIKE with savor (strikes ≥ 3) | `AS_ChumAF_Strike` (same clip) | as S1 | `StrikeR = 2.6` and the ` savor` log suffix (`Rundown.cpp` 164, 390-392, 401-402) | Canon gives the savor no distinct body; only the radius widens and the log says ` savor`. INV I01 notes the exception: "except at three sheet lines, where silence is the design" (the WARN may be skipped at savor; the parser tolerates STRIKE-without-WARN only when `savor` is present, `tools/invariant_parser.py` 27-34). | Invent a savor pose. | as S1. Whether savor has its own clip: OPEN-11. |
| S2 | STRIKE af tally-cool | `AS_ChumAF_Strike` (same clip), preceded by T1 | as S1 | after `AfCool <= 0` with the player inside `StrikeR + 0.4` m (`Rundown.cpp` 324-330) | As S1. "the arithmetic (never betrayal)" (`Rundown.cpp` 306 comment; DREAD L4 "the horror is arithmetic, not betrayal"). | As S1. | log `STRIKE af tally-cool`, `State->Strike`, then hidden + teleport (329-334). INV I23: no strike while lit is S0. |
| N1 | WARN | none: no shot | — | `WarnRadius 7.0` (`Rundown.h` 30) | The brain logs and moves nothing. Canon assigns no visible beat to the warning; the parked body holds. | Invent a tell. | log `WARN seg N d=X[ savor]` once per approach (`Rundown.cpp` 398-403; `bWarned`). INV I01 requires WARN to precede STRIKE. Whether WARN has any visible tell: OPEN-12. |
| R1 | Heard-noise RELOCATION (decision) | none: no shot; the resulting walk is P1 | — | 12 s memory of the last noise (`Rundown.cpp` 171) | Nothing on the body; the choice of target changes. | Turn the head toward the noise (he "faces PATHS"; the eye layer tracks the player, not sounds: OPEN-13). | `OnPhaseChanged(false)`: `RELOCATE toward heard noise at <pos> -> segment N` (180) else `RELOCATE cycle -> segment N (profile UNKNOWN)` (186). `ReportNoise` is the entry point (151-155), fed by `State->OnNoise`. INV I22, I25 (deaf to the dead room). |

### 2.4 The eye layer (always on)

| # | Layer | Asset | Behaviour | Source |
|---|---|---|---|---|
| E1 | `eye_tally` aim | AnimBP aim layer (not a clip) | Always on, in every state above including the fold and the pour: "the eye alone keeps tracking, servo-smooth"; "keeping his eye on you the whole way through". Reference numbers from GD `_head_track` (which tracks the head, not the eye): yaw clamp ±1.05 rad, `lerp 3.5/s`, only inside 11 m (GD 449-454). Light and emissive ON only while `bAfActive && bRecording` (GD 241; AF §THE SCALE LAW). During the crossing the eye is dark (AF §THE LAST CROSSING). | MOTION §AFTER-FIRE; AF; GD; PIPE ADDENDUM |

---

## 3 · DRIVE PLAN (how ARundown drives the SkeletalMesh)

### 3.1 Principle
The brain stays exactly as it is: a tick brain, no Behavior Tree ("the grammar is the point", BRAIN header; `UE5-MIGRATION-MAP`), position-authoritative, log-line-emitting in the format `tools/invariant_parser.py` reads. The animation system OBSERVES the brain; it never moves the actor. Every visual state below is derivable from BRAIN fields the brain already has; the engineer exposes them, the AnimBP reads them. No canon timing is re-implemented in Blueprint.

### 3.2 Motion-state enum (proposed, read by the AnimBP each frame)
Set by ARundown at the lines cited; the AnimBP never infers them from velocity alone (velocity is `SetActorLocation` deltas, which the brain owns).

| Enum value | Set where (Rundown.cpp) | Existing log line at the same site | Clip (§2) |
|---|---|---|---|
| `Park` | default whenever no other value is set this tick; night gate return (341-345); ON AIR no-move branch (362-404) | — | P0 |
| `PourBreak` | BREAK move branch, before `SetActorLocation` (356-358) | preceded by `RELOCATE ...` in `OnPhaseChanged` (180/186) | P1 |
| `PourApproach` | AF approach `SetActorLocation` (294-296) and dead-room approach (281-282) | — | P2/P3 |
| `PourCrossing` | OPEN-8 (no branch yet; constant at `Rundown.h` 29) | — | P5 |
| `Fold` (+ `FoldDoorIndex`) | `DoorFoldCheck` when it sets `FoldT = AfFoldSeconds` (204-206); clear when `FoldT <= 0` (221-225) | (caption `[IT FOLDS THROUGH THE DOORWAY]`, GD 343; no UE log line today: see §4) | F1 |
| `DeadDoorHold` | 284-288 | `AF holds at the felt door` | P4 |
| `Loom` | 298-302 and every subsequent tick in the `Pd <= AfLoomDist` branch while recording | `AF loom d=%.1f (the jaw works its lever)` (once) | L1 → L2 → L3 loop |
| `Cool` (+ `CoolSeconds` 4.0/2.0) | 307-320 | `AF tally cools (taught)` / `AF tally cools` | C1/C2 |
| `Withdraw` | after the cool when the player is outside `StrikeR + 0.4` (326-334), BEFORE `SetActorHiddenInGame(true)` | — | W1 (OPEN-9) |
| `Telegraph` | OPEN-2 (0.9 s beat has no brain timer) | — | T1 |
| `Strike` | 390-396 (night) and 329-330 (tally-cool) | `STRIKE seg N d=X[ savor][ THRU-WALL]` / `STRIKE af tally-cool` | S1/S2 |
| `Hidden` | 333 (`SetActorHiddenInGame(true)`) | — | P6 |

Also exposed to the AnimBP: `bTallyLit = State->bAfActive && State->bRecording` (drives `SOCKET_EyeTally` emissive + light; GD 241), `bAfActive` (drives the wake scale per OPEN-1), `EyeTarget` (the resolved prey's location, `ResolveTarget()` 137-149), the current speed constant for stride matching.

### 3.3 AnimBP structure
| Layer | Content | Blend rule |
|---|---|---|
| Base state machine | states = the enum above; one clip per state (§2) | Transitions are CUTS (blend time 0) between Park and any Pour, Pour and Park, Park and Loom, Loom and Cool, anything and Hidden: "Stops are ABSOLUTE and binary" (MOTION). Where a blend is unavoidable for continuity it is capped at 2 frames of the authored rate (MOTION "two-frame ease caps at most"; OPEN-7 for the rate). |
| Fold | `AM_ChumAF_Fold_<width>` as a montage on a full-body slot, blend-in 0, blend-out 0 | "no procedural blending" (QA-52). Montage length must equal `AfFoldSeconds` exactly so the montage ends the frame `FoldT` reaches 0. |
| Loom sequence | L1 → L2 (once) → L3 random pick loop; L3 clips chosen by a seeded random with no fixed period | "no rhythm a song would keep" (MOTION). L2 plays exactly once per `bAfSeenOnce` contract. |
| Telegraph + strike | `AS_ChumAF_Telegraph` then `AS_ChumAF_Strike` on a full-body slot | Cut in, cut out. Timing ownership: OPEN-2. |
| Eye aim layer | `eye_tally` aim toward `EyeTarget`, always on, on top of everything including montages | The ONE interpolating thing on the rig ("servo-smooth"). Reference rate GD 3.5/s lerp, clamp ±1.05 rad (OPEN-6 for the eye's own limits). |
| Lever coupling | `lever_grip` rotation = f(`jaw` rotation) as a post-process node (or a Blender driver baked into every clip) | Mechanical; never animated independently. |
| Hand IK | two-bone IK, effector `SOCKET_JawLever`, enabled only inside L3 and T1 by an anim curve authored in those clips | The hand must be at the grip whenever the jaw is off its closed pose (PLAN CAPTURE CANON). |
| Disabled | AnimDynamics, RigidBody, cloth, any "idle additive", any breathing additive | MOTION §PRODUCTION NOTES; QA-53 |

### 3.4 Root motion vs the brain
Canon requires root-motion authored clips (MOTION §PRODUCTION NOTES; PIPE ADDENDUM). The brain sets position every tick (`VInterpConstantTo` at 356, 294, 281). Both cannot own translation. Recommended reconciliation (an engineering choice, not canon; the owner rules, OPEN-9): import the pour clips with root motion authored but `EnableRootMotion = false` in the AnimBP, and match stride to the brain's speed with play-rate scaling (or UE Stride Warping) so feet do not slide at 0.8 / 1.6 / 2.4 m/s. The brain remains authoritative because the invariant fixtures pin positions on it (`ue/pyscripts/test_invariants.py`, `test_state_af.py`).

Door width for the fold montage: `DoorPositions[i]` is built from DOORS in file order skipping the header (`Rundown.cpp` 36-50), so DOORS row `i+1` carries the width (col 4). The picker maps width 1.2 → `_120`, 1.4 → `_140`, 1.6 → `_160`. DOORS contains no other width.

### 3.5 Where today's log lines already mark the state changes (verbatim, for the engineer)
`RELOCATE toward heard noise at %s -> segment %d` · `RELOCATE cycle -> segment %d (profile UNKNOWN)` · `AF holds at the felt door` · `AF loom d=%.1f (the jaw works its lever)` · `AF tally cools (taught)` · `AF tally cools` · `STRIKE af tally-cool` · `STRIKE seg %d d=%.1f[ savor][ THRU-WALL]` · `WARN seg %d d=%.1f[ savor]` · `RUN ENDED take=%d (full sheet, fail forward)` · `DEBUG spawn me=... prey=... d=... onair=...` (all in `Rundown.cpp`; written by `LogLine` to `Saved/decision_log.txt` AND to `LogRundown`). The fold, the withdrawal and the telegraph have NO log line today (§4.3).

---

## 4 · ACCEPTANCE

### 4.1 Capture harness available now
| Tool | What it gives | Source |
|---|---|---|
| `ue/pyscripts/capture_gate.py` | headless editor, loads `/Game/Greybox`, places the puppet at the TAPE LIBRARY anchor `(0, -1600, 0)`, `take_high_res_screenshot(1600, 1000)` at tick 90, quits at 240; env `UE_CAP_OUT`, `UE_CAP_POS`, `UE_CAP_LOOK`, `UE_CAP_FOV` | file docstring; `ue/GATE-0.10.md` §3 |
| `ue/pyscripts/stage_and_capture.py` via `Content/Python/init_unreal.py` (`UE_AUTOCAPTURE=1`) | look-dev capture with locked manual EV (`UE_CAPTURE_DARK=1`) | README commit 075; `tools/ue_loop.sh` |
| `ue/pyscripts/test_state_af.py` | forces AF + recording, target 8 m out; expects approach at 0.8 m/s to 1.2 m, cutoff, cool, `STRIKE af tally-cool`; echoes `decision_log.txt` as `AFLOG|` lines | file docstring |
| `ue/pyscripts/test_rundown.py`, `test_invariants.py` | WARN / STRIKE / RELOCATE ordering; I01, I02, I22 | file docstrings; `tools/invariant_parser.py` |
| Accepted frames | archived to `docs/telemetry/ue-baselines/` on the spot | README commit 075 |

### 4.2 Per-shot verification
"Known frame" = a capture requested at a fixed tick after the state's log line, using the capture_gate pattern; "log" = a line in `Saved/decision_log.txt`; "measure" = a value read from the UE output log timestamps or a position-delta audit.

| Shot | Verify by | Pass condition | Source of the bar |
|---|---|---|---|
| P0 Park | 2 captures 3 s apart, pixel-diff the body region (mask out the eye) | zero motion outside the eye; jaw closed; hand down | MOTION "statue-still"; QA-53; PLAN CAPTURE CANON |
| P1/P2/P5 Pour | capture sequence ≥ 8 frames (PLAN "Animation units: capture sequences (≥8 frames or MRQ clip)"); F-curve review of the Blender action | head-height trace flat (no bob); no arm/tail keys; curves linear with ≤ 2-frame caps; foot plant matches speed (no slide at 0.8 / 1.6 / 2.4 m/s); footfall notify count = plants | MOTION §AFTER-FIRE; PIPE ADDENDUM; AUDIO S17 |
| F1 Fold | position-delta audit across door radii (INV I24 "THE FOLD IS PAID"); montage length check; frame at t = 1.1 s and t = 2.2 s | actor position constant for 2.2 s inside `AfDoorNear`; montage = 2.2 s ± 1 frame per width; at 2.2 s the head is the last part to arrive; eye on the target throughout; no downward compression of the pelvis | LAWS 11; QA-52; AF §THE SCALE LAW |
| P4 Dead-door hold | log `AF holds at the felt door` then a capture; bot slams inside (INV I25) | parked; his target never moves on inside noise | LAWS 11; AF §THE TWO HIDES; INV I25 |
| L1/L2/L3 Loom | log `AF loom d=` then captures at +0.5 s, +2 s, +5 s; soak with him adjacent for 10 minutes while recording (INV I23) | body frontal to the player; exactly one 15° tilt event per contract; every jaw-open frame shows the hand on the grip; interval histogram of lever acts has no dominant period; zero strikes while lit | MOTION §THE PERFORMANCE QUOTE; QA-53; QA-54; INV I23 |
| C1/C2 Cool | `AF tally cools (taught)` on the first ever, `AF tally cools` after; measure to the following `STRIKE af tally-cool` (or hide) | 4.0 s first, 2.0 s after; eye dark at t=0; no body motion during the cool | AF §THE TAUGHT CHASE; LAWS 10; QA-36 |
| T1 Telegraph | capture at strike-decision minus 0.45 s (once OPEN-2 lands) | hand at the grip, click fired once, jaw open, nothing else moved; 0.9 s from hand-rise to strike | MOTION hard rules; QA-54; AUDIO S25 |
| S1/S2 Strike | log line + capture sequence; audio meter | no forward translation spike (no lunge); one textile sweep then ≥ 1.5 s authored silence; no sting | LAWS 2; MOTION §Sound; AUDIO silence ledger |
| W1 Withdrawal | capture sequence | path is the recorded approach path reversed; no turn; eye dark | MOTION §AFTER-FIRE |
| E1 Eye | any state; capture with the target moved between frames | only `eye_tally` changed between frames while parked; light/emissive on iff `bAfActive && bRecording` | MOTION; AF §THE SCALE LAW |
| Bell | F-curve scan of every AF action + a physics-asset audit | `bell` has zero keys and zero simulated bodies in every clip | MOTION; LAWS 5; QA-54 |
| Zero-secondary sweep | F-curve scan of every AF action | no keys on `ear_*`, `tail_*`, `bell`; no AnimDynamics/cloth in the AnimBP | QA-53 |
| Scale-truth | measure the imported skeleton's bounds; compare to OPEN-1's ruling; the 1 m cube reads 100.0 uu | height matches the ruled figure to the centimetre; eye at the ruled height | PIPE §STANDARDS; AF §THE SCALE LAW; `ue/GATE-0.10.md` §4 |
| Sodium | `tools/sodium_check.py --subject` on `SK_Chum_AfterFire` | passes as the SM did (PROGRESS 0.3b) | PIPE §MATERIAL MASTERS |

### 4.3 Measurement gaps the engineer should know (no code changed by this spec)
- `LogLine` writes text with no timestamp (`Rundown.cpp` 411-419). Timing measurements use the `LogRundown` output-log timestamps (the same text is `UE_LOG`ged) or anim-notify events; do not try to time from `decision_log.txt` alone.
- The fold, the withdrawal and the telegraph emit no log line today. The shot list assumes a notify-driven measurement until a line is added; adding lines is the engineer's call, subject to the parser's format (`tools/invariant_parser.py` keys on `WARN `, `STRIKE `, `RELOCATE`, `RUN ENDED`).
- The puppet and the brain are not yet one actor (`ue/GATE-0.10.md` §3 "Honest note"). §3 above is the plan for making them one.

---

## 5 · OPEN (canon is silent; do not invent)

| # | Question | What is known | Who rules |
|---|---|---|---|
| OPEN-1 | Authoring scale of `SK_Chum_AfterFire`: 1.0 (3.08 m ear tips, eye ≈ 2.34 m; the imported SM) or the wake scale (body 3.35 m, eye ≈ 3.01 m)? | AF §THE SCALE LAW: 3.35 m body, eye at 3 m, on wake. TIMINGS `AF_HEIGHT 3.35`, `BASE_HEIGHT 2.6`. GD 238 scales the whole rig ×1.2885 on wake. PROGRESS 0.3 / GATE-0.10 §3: the SM imported at 3.08 m is the UNSCALED build. Both cannot be "scale-true" at once unless the brain applies the wake scale as GD does. | Owner |
| OPEN-2 | Where does the 0.9 s telegraph beat live? | QA-54 names 0.9 s. The brain strikes and teleports in the same tick (`Rundown.cpp` 329-334, 390-395). Options: the brain defers `State->Strike` by 0.9 s inside the strike branch (changes invariant timing, I01/I02 unaffected in order); or the telegraph plays on the death presentation after `Strike`. | Owner + engineer |
| OPEN-3 | Does the fold montage carry root translation through the threshold, or fold in place at ≤ 1.0 m from the gap? | The brain freezes position for 2.2 s then resumes at approach speed (`Rundown.cpp` 221-225). "shoulder through first" implies threshold crossing; the brain implies in-place. | Engineer, with the owner's eye on the capture |
| OPEN-4 | Jaw pivot: the Jaw empty (0, 0.06, 2.10) as built, or the HingeBolt axis (±0.28, -0.30, 2.17)? | BUILD 976 vs 1042-1046. PLATE shows "LOWER JAW ON HINGE" at the mouth corners. | Rigger |
| OPEN-5 | Durations of the pour cycle, the square-up, the strike. | Canon gives speeds, not stride length or clip lengths. GD reference cadence: `_gait_t += delta·TAU·1.5·0.5` (0.75 Hz cycle, GD 394-395), superseded in pose but a usable cadence reference. | Animator, reviewed against "stride long, cadence slow" |
| OPEN-6 | Eye aim limits and rate. Does the head also track, or the eye alone? | MOTION: "the eye alone keeps tracking" while parked; "the head leading" while pouring. GD tracks the head (±1.05 rad, 3.5/s, 11 m). | Owner |
| OPEN-7 | Authored frame rate for the "two-frame" ease cap. | Canon states the cap in frames only. | Owner (30 fps would make the fold 66 frames) |
| OPEN-8 | The Crossing hook in `Rundown.cpp`. | `AfCrossingSpeed 1.6` declared, unused; GD 205-226 is the reference; eye dark throughout (AF §THE LAST CROSSING). | Engineer (later unit) |
| OPEN-9 | The withdrawal's body: the brain hides + teleports instantly after the cool; canon shows a reversed walk. How long does the visual withdrawal run before the hide, and who owns translation (root motion vs brain)? | MOTION §THE WITHDRAWAL; `Rundown.cpp` 326-334; §3.4. | Owner + engineer |
| OPEN-10 | Direction and ease of the one 15° tilt. | MOTION: "the clean fifteen-degree head tilt" and, pre-fire, "Head tilts land in clean fifteen-degree stops". No side given. | Animator, owner signs |
| OPEN-11 | Does savor (strikes ≥ 3) change the body? | Only the radius (2.6) and the log suffix change (`Rundown.cpp` 164, 390). | Owner |
| OPEN-12 | Does WARN have any visible tell? | None in canon or in either brain. | Owner |
| OPEN-13 | Does the eye or head acknowledge a heard noise? | "he faces PATHS"; the eye tracks the player in GD; relocation is a target change only. | Owner |
| OPEN-14 | Which arm works the lever? | The grip is built at +X (viewer-right = character's left; BUILD 938-945). PLATE insets are not consistent enough to rule. Nearest arm is `ArmR` (BUILD sx=+1, the single-tendon side). | Owner; the rig provides IK on both hands so either ruling is free |
| OPEN-15 | Day visibility outside the AF layer. | GD: `visible = is_night` (GD 124, 138). The UE brain hides only in the AF path (`Rundown.cpp` 272, 333). | Engineer (parity item) |
