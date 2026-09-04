# PHASE 1 · AFTER-FIRE CHUM · BUILD BRIEF (units 1.1 – 1.13)

Prep deliverable for the Mac lane (plan §0 rule 0, SUBAGENT LANE). One file,
no tracker edits, no git. The build agent executes Phase 1 unit by unit from
this brief without re-reading the canon; every canon claim below carries its
document and section so a doubt can be checked at the source in one hop.

Sources of record used (read these if a citation is disputed):

| Short name | Path |
|---|---|
| PLAN | `AAA_BUILD_PLAN.md` (§R realism bar, §1 doctrine, §2 asset policy, §4 verification loop, §5 Phase 1) |
| TRACKER | `PROGRESS.md` (§PHASE 0 units 0.3 / 0.3b, §PHASE 1 units 1.1–1.13) |
| DOSSIER | `docs/canon/restoration-after-fire-chum.md` |
| PLATE | `docs/canon/art/after-fire-chum-dossier.png` (file CHUM-AF-1974-P (REV.), the source of record per DOSSIER §1) |
| MOTION | `docs/canon/restoration-chum-motion-and-sound.md` |
| PIPELINE | `docs/canon/restoration-blender-ue5-pipeline.md` |
| ARTBIBLE | `docs/production/restoration-art-bible.md` |
| FABRIC | `docs/production/restoration-puppet-fabrication-brief.md` (the STAGE puppet RFQ; see the two-bodies note) |
| DESIGN | `docs/canon/restoration-design-doc.md` (post-fire delta set, STAGE puppet) |
| BUILD | `tools/build_chum_af.py` (the current procedural build, 1468 lines) |
| SODIUM | `tools/sodium_check.py` |
| BEAUTY | `tools/render_chum_af_beauty.py` |
| EXPORT | `tools/export_ue.py`, `ue/pyscripts/fixup_materials.py`, `ue/pyscripts/capture_gate.py` |
| CREDITS | `tools/texsrc/CREDITS.md`, `ue/CREDITS-FAB.md`, `ue/FAB-IMPORT.md` |
| LEDGER | `README.md` commit paragraphs 066, 067, 075, 076 |

---

## 0 · STANDING RULES THAT BIND EVERY UNIT

### 0.1 The realism bar, checkably (PLAN §R, quoted)

> "**The ACCEPTANCE VIEW is the in-engine Unreal capture** … Blender Cycles
> renders are design tools only."
> 1. "No naked primitives. Everything visible is a sourced asset, a merged/
>    remeshed/sculpted mesh, or beveled with edge wear."
> 2. "Small detail lives in MAPS. Stitches/staples/seams/engravings <2cm go in
>    normal+roughness+albedo maps … separate geometry only where silhouette
>    demands (teeth yes, threads no)."
> 3. "Every surface breaks light three ways: albedo variation, roughness
>    variation, normal detail."
> 4. "Lighting is part of the asset … A model is done only when the ENGINE
>    shows it well."
> 5. "Scale-truth: judge at gameplay distance AND 1m closeup."
> 6. "Motion: animation passes anticipation/ease/follow-through on captured
>    frame sequences; no pops." (For the After-Fire body read this against
>    MOTION §AFTER-FIRE, which DELETES anticipation and follow-through; the
>    §R test is "no pops", the curve law is MOTION's.)
> 7. "Crafted, not photoreal … the bar is MATERIAL TRUTH on crafted objects
>    — wool that reads as wool under sodium, wear that reads as history."

### 0.2 Asset policy (PLAN §2)

- CC0 web sources: Poly Haven (`api.polyhaven.com`) and AmbientCG (needs a
  User-Agent header). Downloads land in `tools/modelsrc/` + `tools/texsrc/`
  with a line in `tools/texsrc/CREDITS.md` (PLAN §2; format precedent in
  CREDITS: "Camera_01 — Poly Haven (polyhaven.com), CC0. Vintage camera; its
  lens becomes After-Fire Chum's tally camera eye.").
- Fab / Quixel Megascans: free-in-Unreal via the Fab plugin, owner's Epic
  account; every import gets a line in `ue/CREDITS-FAB.md` as
  `<fab id> · <name> · <rooms used>` (PLAN §2; `ue/CREDITS-FAB.md` line 1).
  Fab has no scripted download; the pull is editor-UI only
  (`ue/FAB-IMPORT.md` §WHY NOT HEADLESS) — so every Fab candidate below is a
  SEARCH TERM to confirm in Window→Fab, not a guaranteed id.
- "Prefer Megascans for environment surfaces & props before building
  anything by hand" and "Everything imported gets the wear pass (nothing
  showroom-new)" (PLAN §2). The owner's standing rule as relayed for this
  brief: use excellent existing assets, never build from scratch what
  exists.
- Texture law: "ORM packed; 2K default, 4K only for Chum and the readables"
  (PIPELINE §STANDARDS). Chum is the one asset allowed 4K.

### 0.3 Blender doctrine (PLAN §1 "Blender asset factory")

- Techniques already proven in BUILD and to be reused: voxel remesh of fused
  masses (`organic()`), scan-dressed materials by box projection
  (`scan_dress()`, `burlap_nodes()`), 2048 Cycles bakes with packed images
  (`bake_all()`), fur-card atlas (`fur()` + `tools/make_fur_cards.py`),
  in-file particle hair for design renders only, "real CC0 donor meshes cut
  down via bmesh (the Camera_01 tally-lens precedent)" (PLAN §1), procedural
  felt grain (`feltify()`), bevelled poly-curves for continuous rolled forms
  (`lip_tube()`).
- **BANNED: thin shrinkwrapped shells.** "thin shrinkwrapped shells are
  BANNED (they collapse — solid geometry only)" (PLAN §1). History: the head
  quilt panels "were baking garbage-bright from their thin shrinkwrap shells"
  (LEDGER 066) and the first ear panel "shrinkwrapped a thin plane onto the
  slab and collapsed into slivers (the giraffe artifact)" (LEDGER 067). The
  body patches in BUILD (`patch()`, lines 472–496) are exactly this banned
  construction and are the subject of unit 1.1.
- "sRGB→linear on authored colors; measure the texel not the render;
  raycast forensics for mystery surfaces … Principled Hair needs MELANIN
  parametrization; Metal renders SIGABRT occasionally — retry once" (PLAN §1).
- Sodium check is the material gate: "every material passes through before
  export; if it lies under sodium it does not ship" (PIPELINE §MATERIAL
  MASTERS; PLAN §1). Baked per-object materials MUST be checked with
  `--subject`, never on shader balls ("on foreign ball UVs their empty bake
  margins read as black glass" — SODIUM docstring; TRACKER 0.3b).

### 0.4 Coordinates, scale and naming

- Blender scene in metres, FBX with the UE preset, 1 m = 100 uu, verified on
  the unit cube in 0.2 (PIPELINE §STANDARDS; TRACKER 0.2 "1m cube = 100.0uu
  exactly"). UE is X-forward Z-up; the Blender build faces −Y (BUILD
  docstring).
- Naming: `SM_`/`SK_` meshes, `M_`/`MI_` materials, `T_*_BC/_N/_ORM`
  textures, `UCX_` collision children, sockets `SOCKET_JawLever`,
  `SOCKET_EyeTally`, `SOCKET_Bell` (clapperless) (PIPELINE §STANDARDS).
- Scale law: "the body stands 3.35 meters the moment he wakes, the tally eye
  sits at three meters" (DOSSIER §THE SCALE LAW; PLATE "HEIGHT (APPROX.) 11 FT
  (ABOUT 3.35 M)"). BUILD authors at 2.6 m base and relies on the Godot
  `rundown.gd` to scale to 3.35 (BUILD docstring); the UE import measured
  3.08 m unscaled (TRACKER 0.3; LEDGER 075). **Unit 1.7 resolves this** —
  see §1.7.
- The maw is lightproof unlit black (`M_MawBlack`) and fur cards are masked
  two-sided (`M_FurCards`) — both rebuilt natively in UE by
  `ue/pyscripts/fixup_materials.py`; every other material is wired from the
  Blender-written manifest (`export_ue.py --all-meshes`; LEDGER 075).

### 0.5 The two bodies (read before touching any "post-fire" canon)

There are two post-fire Chums and their canon must not be mixed:

1. The STAGE puppet's post-fire build — "REPAIRED, NOT BURNED. No char, no
   melt, no horror finishing" with the nine-delta tell-table T1–T9 (FABRIC §5;
   DESIGN "The post-fire delta set"). That body is hand-sized and is NOT the
   Phase 1 subject.
2. The MASCOT — "the 1974 walkaround body built for station events, eleven
   feet of it … The fire took the vault; someone rebuilt the mascot afterward
   from what survived" (DOSSIER §WHAT IT IS). This is the After-Fire Chum,
   the hunter, and the Phase 1 subject. Its source of record is the PLATE,
   which shows char, melt and salvage.

Prior builds already transferred two stage-puppet deltas onto the mascot
(the school-gray flannel patch and the leather patch, BUILD lines 495–496;
LEDGER "patches … rust, green, the school-gray flannel, the leather"). No
canon document says the mascot carries them. Treat them as an established
build decision, flagged **OPEN** in §1.1, not as canon.

### 0.6 The verification loop (PLAN §4, verbatim order)

```
1. Blender rebuild of touched assets     → WROTE, no Traceback
2. Cycles/EEVEE design renders           → look at them
3. UE import/update (headless python)    → no errors in log
4. UE look-dev capture(s) of the subject → look at them (ACCEPTANCE VIEW)
5. UE automation tests (once they exist) → green; plus reference-Godot soak
6. Tick box → ledger → Desktop copies → commit → push
```
Plus, for every material unit: `Blender --background blend/chum_af.blend
--python tools/sodium_check.py -- --subject --out renders/sodium_chum.png`
before step 3 (SODIUM docstring; PLAN §1). Animation units: "capture
sequences (≥8 frames or MRQ clip), review motion" (PLAN §4).

### 0.7 Assets already in hand (do not re-download)

| Asset | Source / license | Used by |
|---|---|---|
| Fabric031 (grey wool weave), Fabric030 (coarse weave), Leather030, Metal058A (copper smudge) | AmbientCG, CC0 (`tools/texsrc/CREDITS.md`) | `SCANS`, `SCORCH_MASK`, `scan_dress()` in BUILD |
| Camera_01 (1k blend + textures) | Poly Haven, CC0 (CREDITS) | the tally lens barrel, cut via bmesh (BUILD lines 774–827) |
| `fur_tuft_atlas.png` | generated by `tools/make_fur_cards.py` | `FurCards` material |
| `assets/env/workshop_1k.hdr` | (license line missing from CREDITS — **OPEN**, record it) | BEAUTY world |
| Fab starter set | none pulled yet (`ue/CREDITS-FAB.md` is an empty header) | — |

---

## 1 · THE UNITS

Each unit: (1) canon, (2) what exists + sodium verdict, (3) asset-reuse
plan, (4) Blender steps, (5) acceptance test, (6) risks and OPEN questions.

Poly Haven ids below were read from `api.polyhaven.com/assets?t=…` on
2026-09-04; AmbientCG ids from `ambientcg.com/api/v2/full_json`. Both are
CC0. Fab entries are search terms (see §0.2).

---

### 1.1 TORSO — quilted patchwork, seams, char zones, 2048 bake

**(1) Canon.**
- "brown wool, hand-patchwork over a stuffed muslin core; visible
  hand-stitching throughout; nothing may read machine-made at 30 cm"
  (FABRIC §3 — the stage puppet's construction, which the mascot's plate
  echoes at scale; the mascot itself is "original 1974 mascot body and
  salvaged studio materials", PLATE "NOTES").
- "the wool is fused and reads as mass, and nothing on him bounces, ever"
  (MOTION §AFTER-FIRE); "the After-Fire wool must read as the same material
  that forgot how to be soft" (MOTION §PRODUCTION NOTES).
- The PLATE's torso (observed, main figure and back view): an irregular
  quilt of differently coloured patches (rust-red on the left shoulder,
  olive green on the right chest, tan/ochre, navy, dark browns) with dense
  running stitches along every patch edge; a large lighter tan oval BELLY
  panel with a darker sewn border in the centre; scorched, matted surface
  everywhere (no loose fluffy nap); a rectangular riveted metal access
  panel with cabling on the spine in the BACK VIEW.
- Wool material law: `M_Wool (subsurface, sodium-honest)` is the UE master
  (PIPELINE §MATERIAL MASTERS); "Nothing ships on a procedural fiber that a
  scan could carry" (ARTBIBLE line 11).

**(2) What exists.** BUILD lines 333–350: `BodyCore` = seven joined UV
spheres → `organic()` (voxel 0.035, lump/fiber displace, decimate 0.4),
BurntWool bake; `Belly` = one scaled sphere → `organic()` (voxel 0.02),
BellyWool bake; `body_fur` cards over everything but the belly zone. Lines
472–496: four patches built as SUBSURF plane → SHRINKWRAP (TARGET_PROJECT)
→ SOLIDIFY 14 mm — **the banned thin-shell construction**. Hair plan
`BodyCore` 3600 guides (design only).
Sodium verdict (TRACKER 0.3b; LEDGER 076): "belly + chest patches … FAIL as
faceted clay" — `renders/sodium_chum.png` shows the belly as a smooth
faceted egg and the patches as flat floating discs. The Cycles beauty
(`renders/chum_af_full.png`) reads as a fluffy plush toy, not fused burnt
quilt; the UE daylight baseline shows the body as a mottled dark mass with
no quilt structure. TRACKER 0.3 lists "fur mottle vs plate" as a held delta.

**(3) Asset-reuse plan.**

| Need | Candidate (id · source · license) | Why / how |
|---|---|---|
| Base fused-wool weave (albedo/normal/rough) | `Fabric031` · AmbientCG · CC0 (in hand) | keep as the base; already tinted per `BAKE_TINTS` |
| Looped, matted wool for the fused read | `wool_boucle` · Poly Haven · CC0 (314×390 mm) | box-project at 1:1 mm scale on the BodyCore; its looped pile reads as matted wool under sodium |
| Coarse wool alternatives | `poly_wool_herringbone` (grey), `knitted_fleece` (brown), `caban` (orange woolen fleece) · Poly Haven · CC0 | patch palette: herringbone = the school-gray flannel candidate; caban = rust patch base; knitted_fleece = brown panels |
| Singed/matted plush for scorch rims | `curly_teddy_natural` · Poly Haven · CC0 | a scanned teddy plush; use its height/normal for the "wool that forgot how to be soft" zones, darkened |
| Burlap (muslin core showing through tears) | `hessian_230` / `hessian_380` · Poly Haven · CC0 | inside torn windows; also the elbow/shoulder wraps |
| Green patch | `ribbed_corduroy` (green) · Poly Haven · CC0, or `Fabric018` (green wool) · AmbientCG · CC0 | the olive chest patch |
| Plaid/flannel patch | `Fabric080` (cotton plaid) / `Fabric060` (tartan) · AmbientCG · CC0 | one or two plate patches read as checked cloth |
| Navy / dark worn cloth | `denim_fabric_06` (dark worn) · Poly Haven · CC0 | navy patch base |
| Scorch / soot masks | `Metal058A` (in hand); `Rust009`, `Metal021`/`Metal022`/`Metal024`/`Metal025` (rust leaks/spots) · AmbientCG · CC0 | mask sources for `burlap_nodes()` burn ramp; leak textures give directional soot runs |
| Char crackle height | `Bark015` (damaged, layered, old) · AmbientCG · CC0; `bark_willow_02` (rough, dry) · Poly Haven · CC0 | no CC0 "charred wood" exists on either API (checked); bark crackle is the honest substitute for alligator-char height in the char zones |
| Fab / Megascans (confirm in editor) | search "burnt wood", "charred wood", "charcoal", "burnt fabric", "wool fabric", "quilted fabric", "felt", "soot decal", "burn decal" · Fab standard license → `ue/CREDITS-FAB.md` | Megascans surfaces for the UE-side `M_Wool` instances and char decals; use the 2K tier |
| Back access panel | `metal_plate_02` (corroded, rusted) / `rusty_painted_metal` · Poly Haven · CC0; `MetalPlates013` · AmbientCG · CC0 | the spine plate in the PLATE back view |

**(4) Blender steps.**
1. Keep `BodyCore` as the fused mass but raise its truth: rebuild the seven
   spheres with a sculpted silhouette (belly forward, chest sagging over the
   collar line as in the PLATE), voxel remesh at 0.02, then add a
   SMOOTH_CORRECTIVE pass so the decimated surface never facets at 1 m.
2. **Patches as solid geometry, never shells.** For each patch: duplicate
   the remeshed body, boolean-intersect with a rounded-rectangle prism
   pushed 8–15 mm proud of the surface, voxel remesh at 0.006, displace with
   the patch's own scan normal (as the ear panels do, BUILD lines 669–691),
   and join to the body OR keep as its own bake object. Patch count and
   placement: read the PLATE (at least: rust-red left shoulder, olive right
   chest, tan belly oval, navy flank, two or three small dark browns); the
   stage tell-table's "fourteen patches" (FABRIC §5 T7) is stage canon —
   **OPEN** whether the mascot count matches.
3. Seams and stitches go to MAPS (PLAN §R.2): author a seam mask in the
   bake material (`burlap_nodes()` gains a `seam` input: an edge-distance
   or painted vertex-colour mask from the patch borders) and bake stitches
   as normal + darker albedo + rougher roughness along it. Delete the
   `sring`/`stt` stitch cylinders at the shoulders (BUILD 406–417) once the
   map carries them.
4. Belly: rebuild as a sewn-in panel of the body (boolean-embedded, 10–20 mm
   proud, its own bake at 2048 with `BellyWool` tint), seam ring in the
   normal map; the "accessed belly … darker wool carrying a central seam
   opened and resewn repeatedly" (DESIGN delta 6) is STAGE canon — **OPEN**
   whether the mascot's belly carries the resewn scar (the PLATE shows a
   plain lighter oval with a dark border).
5. Char zones: extend `burlap_nodes()` with a second, larger-scale burn
   layer (`Bark015` height into the bump, `Rust009` leak mask into a
   directional soot multiply) so char reads as history, not noise. Char
   zones per PLATE: right shoulder/arm root, left hip, the ear tips, the
   crown patch. Roughness in char must go to ≥0.95 and albedo ≤0.02 linear.
6. Fur: reduce `body_fur` to a singed rim only (mask everything except
   patch edges and the shoulder/hip crests), shorten cards to 20–40 mm, and
   let the wool scan carry the pile. The fused body must not read as plush.
7. Bake at 2048 (Chum may use 4K per PIPELINE §STANDARDS — reserve 4K for
   the torso albedo only if the 1 m closeup demands it); UV via
   `smart_project` as now, but raise `island_margin` to 0.03 to kill the
   black-glass margins the sodium check exposed.
8. Rebuild → `--subject` sodium render → BEAUTY → `export_ue.py
   --all-meshes` → `fixup_materials.py` → capture.

**(5) Acceptance test.**
- Sodium (`--subject`, 1100×1400): no visible facets on belly or patches at
  the framing the script produces; patches read as raised sewn cloth with
  a stitched border (normal relief) rather than discs; char zones read as
  matte black with crackle, not as smooth dark paint. Three-way response:
  under the single sodium lamp the torso shows albedo mottling, roughness
  variation (matte wool vs slightly less-matte flannel vs glossier leather)
  and normal weave — all three visible in one frame.
- Cycles beauty (`chum_af_full.png`): the body reads as the PLATE's quilt —
  patch colours identifiable in monochrome-ish light, fused/matted surface,
  no plush halo.
- UE acceptance capture (dark locked-EV rig, LEDGER 075): the quilt
  structure survives Lumen at gameplay distance (3–6 m) and the seam maps
  hold at the 1 m closeup. Scale truth: belly panel ≈ 0.85 m tall on the
  3.35 m body (BUILD belly 0.27 r × 1.25 × 2 ≈ 0.68 m at 2.6 m base ×
  1.288); patches 0.2–0.35 m across. Judge both at gameplay distance and
  1 m (PLAN §R.5).
- Texture check: every torso material has _BC, _N and roughness (or _ORM)
  — no flat-colour slots left in the manifest.

**(6) Risks / OPEN.**
- OPEN: mascot patch count and placement (stage T7 says fourteen with a
  numbered diagram "supplied at contract" that does not exist in the repo).
- OPEN: whether the flannel and leather patches (stage deltas) belong on
  the mascot at all — keep them (build precedent) unless the owner rules.
- OPEN: the back-view spine access panel is PLATE-only; no text canon names
  it. Build it (it is on the plate) and note it.
- Risk: making the body read fused (canon) while keeping enough surface
  life for §R.3 — the answer is scan-carried pile, not cards.
- Risk: 4K bakes on a 16 GB M1 Pro (PLAN §1 machine limits); bake CPU at
  2 samples as now, and keep the count of 4K maps ≤2.

---

### 1.2 THROAT SPEAKER — donor speaker/radio driver, chest mount, cabling

**(1) Canon.**
- "a studio monitor speaker revoiced into the throat" (DOSSIER §WHAT IT IS);
  "THE THROAT SPEAKER … a salvaged studio monitor revoiced into the chest,
  and under the tally it breathes band-limited room tone … If it ever
  plays more than room tone, that is a canon event and the author signs it
  first" (MOTION §AFTER-FIRE); "NO VOCALIZATIONS, EVER: the throat speaker
  is not a voice" (MOTION §AFTER-FIRE).
- PLATE callout "THROAT SPEAKER / RESONATOR" at the upper chest below the
  collar; detail 2 "THROAT SPEAKER — STUDIO MONITOR SPEAKER REVOICED &
  MOUNTED IN CHEST TO PROJECT VOICE THROUGH PUPPET THROAT" (observed: a
  round woven-wire mesh grille inside a riveted metal ring, set into the
  chest cloth; cabling runs from it under the collar).
- Unit text: "donor speaker/radio driver, chest mount, cabling"
  (TRACKER 1.2).

**(2) What exists.** BUILD lines 466–469: `spk` = one 12-vertex cylinder
(r 0.09, h 0.05) in `CharDark`, tilted 78° — a naked primitive, rejected on
sight by PLAN §R.1. No cabling, no mount. Sodium: not called out (it hides
in the collar shadow); the chest region reads as a flat dark disc.

**(3) Asset-reuse plan.**

| Need | Candidate | Notes |
|---|---|---|
| Donor driver + grille | `vintage_radio_transceiver` · Poly Haven · CC0 (field radio: grille, dial, handset) | cut the grille/driver out via bmesh exactly as Camera_01 was (BUILD 777–811); it is the same era language as the PLATE |
| Donor driver (alt) | `boombox` · Poly Haven · CC0 (two loudspeaker drivers) | if the transceiver grille is too small; cut one driver + surround |
| Donor cone / horn (alt) | `Megaphone_01` · Poly Haven · CC0 | horn throat if the "resonator" reading is preferred — **OPEN** |
| Mount ring metal | `Metal058A` (in hand) + `Metal063` (oxidized steel) / `Metal041B` (iron rust) · AmbientCG · CC0 | scan-dress the ring like `BronzeBand` |
| Grille mesh | `metal_grate_rusty` · Poly Haven · CC0 (500 mm, rusty grate) or `Net002B` (broken old net) · AmbientCG · CC0 as an alpha | if the donor grille is deleted, a masked plane with a real wire-mesh scan is better than modelled wires (PLAN §R.2) |
| Cabling | `Rope002` (steel rope/cable) · AmbientCG · CC0; `modular_electric_cables` · Poly Haven · CC0 | bevel curves wearing Rope002; connector boxes cut from the modular cables set |
| Fab (confirm) | "vintage speaker", "speaker grille", "studio monitor", "audio cable", "cable bundle" · Fab standard → `ue/CREDITS-FAB.md` | prefer a Megascans speaker scan if one exists in the free tier |

**(4) Blender steps.**
1. Append the donor (`bpy.data.libraries.load`), cut to driver + grille +
   surround with a bmesh face filter by material/position (Camera_01
   precedent), scale so the grille is ≈ 0.18–0.22 m across at 2.6 m base
   (≈ 0.25 m at 3.35 m; the PLATE grille spans about the width of the bell).
2. Cut a recess into `BodyCore` for the mount (boolean DIFFERENCE before
   `organic()` so the remesh heals the cloth edge), seat the driver
   recessed, add a mount ring as a bevelled poly-curve (not a torus —
   perfect circles are programmer art, PLAN §R.1) with a scan-projected
   rivet normal; rivets ≥ 2 cm may be low-poly spheres remeshed into the
   ring.
3. Cabling: two or three poly-curves with `bevel_depth` 0.006–0.01 from the
   grille edge, under the collar, into the cloth at the shoulder; `Rope002`
   scan-dressed. Cables must enter cloth through a visible slit, never
   float (LEDGER, `README.md` ~line 400: patches must "sit sewn, not
   floated").
4. Grille material: scan-dressed dark steel, roughness 0.5–0.7, normal from
   the grate scan; driver cone: a paper-like matte (`M_Paper` master exists
   in PIPELINE §MATERIAL MASTERS) dusted and scorched.
5. Pack donor textures (`img.pack()` loop as for the lens), soot-multiply
   any donor branding illegible (BUILD 812–827 precedent).
6. Add empty `SOCKET_ThroatSpeaker` at the driver centre for the audio
   emitter (naming by analogy with the three canon sockets; **OPEN** — not
   in PIPELINE's socket list).

**(5) Acceptance test.**
- Sodium `--subject`: the grille reads as woven wire (normal + roughness
  breakup), the ring as worn metal with rivet relief, the cone as matte
  paper; no cylinder cap visible anywhere.
- Beauty + UE capture: the speaker is legible as a speaker at 3 m in the
  dark locked-EV portrait; cabling casts contact shadow on the cloth
  (recess proves depth). Scale truth: grille ≈ 0.25 m at 3.35 m.
- Credits: donor line in `tools/texsrc/CREDITS.md` (CC0) or `ue/CREDITS-FAB.md`.

**(6) Risks / OPEN.**
- OPEN: "resonator" vs "monitor speaker" — the PLATE labels both; build the
  monitor grille (both text docs say monitor).
- OPEN: no UE audio in this unit; the emitter is wired in 1.12.
- Risk: the recess boolean fighting the voxel remesh — run the boolean on
  the joined spheres before `organic()`, never after.

---

### 1.3 COLLAR, LEATHER STRAP, DEAD BRASS BELL

**(1) Canon.**
- "THE BELL NEVER SOUNDS (clapperless by canon; the absence is the tell)"
  (MOTION §AFTER-FIRE); "The bell at his collar stays silent, per the oldest
  law; if the model ever swings it, it is clapperless, and the caption for
  that is nothing" (DOSSIER §SOUND AND CAPTION LAW); socket
  `SOCKET_Bell (clapperless)` (PIPELINE §STANDARDS).
- Stage bell canon for material reference only: "Bell: brass, 25 mm, at the
  collar, SUPPLIED SILENT: clapper removed invisibly" (FABRIC §3); post-fire
  stage bell "blackened, crown pry-marks, still silent" (FABRIC §5 T5;
  DESIGN delta 5 "with a bright pried-and-recrimped scratch at the seam").
- PLATE (observed): a broad dark collar band with a riveted edge and a
  buckle/strap, a round brass bell with a slot and a hanging loop, front
  centre, roughly the size of the throat grille. TRACKER 1.3: "Collar,
  leather strap, dead brass bell".

**(2) What exists.** BUILD 458–464: `collar` = torus (LeatherCol,
Leather030 scan-dressed), `bell` = a plain UV sphere in `Brass` (Metal058A
smudge). Both are naked primitives per PLAN §R.1. Sodium: the brass ball
passed as metal on the contact sheet but is a sphere, not a bell.

**(3) Asset-reuse plan.**

| Need | Candidate | Notes |
|---|---|---|
| Aged, stitched leather strap | `fabric_leather_01` / `fabric_leather_02` (aged, stitched, creased) · Poly Haven · CC0; `Leather034C` (stitched, dark) / `Leather032` (scratched black) · AmbientCG · CC0 | replaces Leather030 on the collar; the stitched scan carries the edge stitching in maps |
| Brass, worn | `brass_pot_01` / `brass_vase_01` / `brass_candleholders` · Poly Haven · CC0 (models with brass PBR sets) | borrow their brass texture sets for the bell's `Brass` material; cut a bell dome from `brass_vase_01`'s body if its profile fits |
| Blackened/pried brass | `Metal008` (bronze, scratches) · `Metal058B`/`Metal058C` (copper oxidation) · AmbientCG · CC0 | oxidation for the blackened crown; a hand-painted bright scratch mask for the pry mark |
| Buckle / rivets | `gate_latch_01` · Poly Haven · CC0 (bolt, latch) | cut the latch tongue as the buckle |
| Fab (confirm) | "leather strap", "belt buckle", "brass bell", "sleigh bell", "worn brass" | a Megascans brass or leather surface for the UE MI |

**(4) Blender steps.**
1. Collar: a bevelled poly-curve following the neck (not a torus), flat
   profile (use a 2-point rectangular bevel object), 40–60 mm wide at 2.6 m
   base, solidified 8 mm, voxel remesh 0.005 so edges soften; box-project
   the stitched leather scan; rivets along the edge as map detail.
2. Bell: revolve a real bell profile (crown, waist, slot) as a spin of a
   bevel curve OR cut the dome of `brass_vase_01`; add the crown loop as a
   thick bevelled ring; the slot as a boolean; NO clapper geometry inside
   (the void is the tell — model the empty interior black). Blacken the
   crown with the oxidation scan, one bright scratch in the albedo/rough
   at the seam.
3. Hanging loop: bevel curve from the collar's strap through the bell loop.
4. Empty `SOCKET_Bell` at the bell's hang point (PIPELINE §STANDARDS).
5. Scan-dress with `scan_dress()` on the new leather/brass scans; the bell
   material gets its own `T_ChumAF_Bell_*` set since 4K is not needed.

**(5) Acceptance test.**
- Sodium: the leather reads as leather (creases, roughness breakup), the
  brass as worn brass with an oxidised crown and one specular scratch; the
  bell silhouette reads as a bell at the sodium framing.
- UE capture: the bell catches the tally's red spill (BEAUTY's `TallySpill`
  precedent) without blooming; the interior is black.
- Scale truth: bell diameter **OPEN** (stage bell is 25 mm; the PLATE bell on
  the mascot is roughly grille-sized, ≈ 0.12–0.15 m at 3.35 m). Use the
  PLATE proportion.

**(6) Risks / OPEN.**
- OPEN: bell size on the mascot (above).
- OPEN: whether the mascot's bell carries the stage pry-mark (T5/delta 5).
  It is cheap and canon-adjacent; build it, note it.
- Risk: the collar must not intersect the jaw at full open — check with the
  jaw at the BEAUTY's 0.2 rad pose and at the 1.11 quote pose.

---

### 1.4 ARMS & HANDS — tendons both sides, articulated fingers

**(1) Canon.**
- "salvaged cable for tendons" (DOSSIER §WHAT IT IS); PLATE callout "EXPOSED
  PUPPET TENDONS / CONTROL LINES" and detail 3 "PUPPET TENDONS — SALVAGED
  CABLES ACT AS ARM TENDONS, PULLED BY PUPPETEER TO DRIVE ARM MOVEMENT";
  "ARM MOVEMENT DRIVEN BY CABLE TENDONS" (PLATE §PUPPET CONSTRUCTION LOGIC).
- The hands must work the jaw: "THE JAW OPENS, AND ONLY BY HIS OWN HAND … a
  lever inside the mouth, pulled to open, pushed to close" (MOTION
  §AFTER-FIRE); PLATE turnaround shows his hand raised to the mouth lever.
- Strike scale: "a hand the size of a door" (DOSSIER §THE LAST CROSSING).
- PLATE (observed): viewer-left arm bare to the tendons — a bundle of dark
  cables with metal ferrules running shoulder to wrist over a burnt cloth
  core, ending in a skeletal metal hand with segmented fingers and claws;
  viewer-right arm cloth-covered with a fur mitt hand, claws, a rust-red
  patch at the shoulder. TRACKER 1.4: "tendons both sides, articulated
  fingers".

**(2) What exists.** BUILD 376–441: arms as joined spheres → `organic()`;
hands as joined spheres → `organic()` (voxel 0.016); claws as 16-vertex
cones; tendons as straight cylinders (3 left, 1 right); guides as tori;
elbow wrap torus; shoulder seam ring + 5 stitch cylinders. Sodium verdict:
"hands … FAIL as … wax" (TRACKER 0.3b) — `renders/sodium_chum.png` shows
smooth low-poly mitts with cone claws. Cylinders/tori/cones = naked
primitives (PLAN §R.1). Hair plan `ArmL/ArmR` 700 guides.

**(3) Asset-reuse plan.**

| Need | Candidate | Notes |
|---|---|---|
| Steel cable tendons | `Rope002` (steel cable) · AmbientCG · CC0; `modular_electric_cables` · Poly Haven · CC0 (connectors, junctions) | bevel curves wearing Rope002; ferrules/junction blocks cut from the modular set |
| Rod/ferrule metal | `Metal041B`/`Metal041C` (iron rust) · `Metal063` · AmbientCG · CC0; `rusty_metal_03` · Poly Haven · CC0 | scan-dress `RodMetal` with real rust instead of copper smudge |
| Skeletal hand hardware | `bolt_cutters_01`, `pipe_wrench`, `ratchet_wrench`, `gate_latch_01` · Poly Haven · CC0 | cut pivots, bolts and jaws as finger knuckles/joints (donor-cut precedent) |
| Cloth arm / mitt | as 1.1 (wool_boucle, Fabric031, hessian for the wraps) | the mitt is the same fused wool |
| Claw | `bull_head` · Poly Haven · CC0 (horn material) — or Fab "horn", "claw", "bone" | horn/bone PBR for the claws; no CC0 claw mesh found — sculpt from a remeshed cone with a horn scan |
| Fab (confirm) | "steel cable", "wire rope", "rusty bolt", "animal claw", "bone", "horn" | |

**(4) Blender steps.**
1. Arms: keep the sphere-chain silhouette but add a real elbow crease and
   wrist taper; remesh at 0.015; the LEFT arm gets a torn cloth window (boolean
   cut, hessian-lined) exposing the cable bundle over a dark core.
2. Tendons: 3–5 poly-curves per arm (both sides now — TRACKER 1.4) with
   `bevel_depth` 0.006, following the arm through guide blocks; guides as
   remeshed cut donor hardware, not tori. Cables sag slightly between
   guides (curves, not straight cylinders) but are STATIC in animation (no
   secondary motion, MOTION §AFTER-FIRE).
3. Hands: build a palm + 4 finger chains per hand (PLATE shows four digits
   on the skeletal hand; **OPEN** digit count on the mitt — BUILD has three)
   with 3 phalanges each; the skeletal left hand from donor-cut metal, the
   right mitt as remeshed wool with sewn finger seams in maps; claws
   remeshed from cones with a horn scan and a chipped tip. Fingers must
   articulate: each phalanx is a separate remeshed piece (or a skinned
   single mesh in 1.9) with a pivot empty at the knuckle — the right hand
   must close on the mouth lever in 1.11.
4. Elbow wrap and shoulder seam ring → bandage as a bevelled ribbon curve
   with hessian scan; shoulder stitch cylinders → seam map (PLAN §R.2).
5. Bake: hands get their own 2048 bakes (they appear at 1 m in the strike).

**(5) Acceptance test.**
- Sodium: hands read as sewn wool (right) and machined/rusted iron (left),
  not wax; cables show twisted-strand normal; claws show horn roughness
  variation. No cone or torus caps anywhere on the arm.
- Beauty + UE 1 m closeup of the right hand: finger seams in maps, claw
  chips, cable strand detail hold. Scale truth: hand span ≈ 0.45–0.55 m at
  3.35 m ("the size of a door" is prose; the PLATE hand is about
  head-width — **OPEN** exact span).
- Articulation proof: pose the right hand closed on the mouth lever in a
  design render with no interpenetration.

**(6) Risks / OPEN.**
- OPEN: digit count on each hand (PLATE reads four on the skeletal hand).
- OPEN: which arm is bare — PLATE has viewer-LEFT bare (BUILD matches with
  the dense left tendons); TRACKER 1.4 says tendons "both sides" — build
  cables on both, the right side mostly under cloth with a few exposed.
- Risk: fingers as separate remeshed pieces bloat the material count
  (already 30 instances in UE, TRACKER 0.3) — share one hand material per
  side.

---

### 1.5 LEGS — control rods, torn fur windows, weighted feet

**(1) Canon.**
- "leg rods, a weighted foot base" (DOSSIER §WHAT IT IS); PLATE callouts
  "LEG CONTROL RODS", "WEIGHTED FOOT BASE", detail 5 "LEG CONTROL RODS —
  INTERNAL RODS LINKED TO KNEE AND ANKLE FOR WALKING & WEIGHT SHIFT";
  "REINFORCED FRAME POINTS SUPPORT PUPPET WEIGHT" (PLATE construction logic).
- Motion: "knees nearly stiff, stride long, cadence slow, silhouette always
  at full height" (MOTION §AFTER-FIRE); "Weighted footfalls thunk on his
  step interval" (DOSSIER §SOUND AND CAPTION LAW); sound "sub-heavy
  wood-through-floor footfall (S17, interval-driven)" (MOTION §Sound).
- PLATE (observed): thick cloth legs; a torn window on the viewer-right
  shin exposing a vertical rod assembly with brackets; big rounded paw feet
  with three toe lobes each; a pale worn patch on the viewer-left foot's
  top; the weighted base reads as a flat dark plinth under each paw.
  TRACKER 1.5: "control rods, torn fur windows, weighted feet".

**(2) What exists.** BUILD 353–374: legs as joined spheres → `organic()`
(voxel 0.025), one straight rod cylinder outside the cloth per leg; foot as
a scaled sphere + three toe spheres in the same join. Sodium verdict:
"feet FAIL as wax" (TRACKER 0.3b). Rods are naked cylinders, outside the
cloth rather than in a window.

**(3) Asset-reuse plan.**

| Need | Candidate | Notes |
|---|---|---|
| Rods, brackets, clamps | `modular_industrial_pipes_01`, `modular_pipes` · Poly Haven · CC0 (rusted pipes, flanges, valves) | cut rod lengths, flanges and brackets from the modular set (donor-cut precedent) |
| Rusted iron | `Metal041B`, `Rust009`, `MetalPlates013` · AmbientCG · CC0; `rust_coarse_01`, `rusty_metal_04` · Poly Haven · CC0 | rod and bracket surfaces |
| Torn cloth window lining | `hessian_230` · Poly Haven · CC0 | the muslin core visible at the tear |
| Foot pad / worn patch | `polar_fleece` (worn light) · Poly Haven · CC0 for the pale worn patch; wool as 1.1 | the PLATE's pale foot patch is worn-through pile |
| Weighted base | `metal_plate_02` / `blue_metal_plate` (scratched, painted) · Poly Haven · CC0; `dark_wooden_planks` · Poly Haven · CC0 if the plinth is wood | **OPEN** material (see 6) |
| Fab (confirm) | "steel rod", "rusty pipe", "bracket", "cast iron", "burnt wood", "charred wood" | |

**(4) Blender steps.**
1. Legs: rebuild with a real knee (nearly stiff — the silhouette is a
   column) and ankle; remesh 0.02; boolean a torn window into the
   viewer-right shin, lined with hessian, edges frayed by displacement.
2. Rod assembly inside the window: two vertical rods (bevel curves or
   donor pipe cuts), a knee bracket and an ankle bracket cut from the
   modular pipe flanges, bolts ≥ 2 cm as geometry, smaller as map. Rods must
   be INSIDE the leg, visible through the window (PLATE detail 5), not
   bolted to the outside as now.
3. Feet: sculpt the paw as one remeshed mass with three toe lobes and a
   pad underside; sole flattened; voxel 0.012; foot fur cards only on the
   upper rim (BUILD's `hsole_mask` precedent). Pale worn patch on the left
   foot top via albedo/rough mask.
4. Weighted base: a flat plinth 30–40 mm thick under each paw, edge-worn
   (bevel + wear mask), scan-dressed; it is what the floor contact sound is
   about (1.12).
5. `UCX_` collision children for the feet and plinths (PIPELINE
   §STANDARDS) — the first collision on the puppet; keep them as simple
   convex boxes named `UCX_SK_ChumAF_00..`.

**(5) Acceptance test.**
- Sodium: feet read as sewn wool over a weighted pad (roughness break
  between pile and the pale worn top), rods as rusted iron with bracket
  relief; the window's frayed edge shows fibre normal.
- UE capture at gameplay distance: the leg column silhouette holds at full
  height; at 1 m the window's internal rods cast Lumen contact shadow
  inside the leg (depth proof). Scale truth: foot length ≈ 0.6–0.7 m at
  3.35 m (BUILD foot 0.185 r × 1.45 × 2 ≈ 0.54 m at 2.6 m × 1.288 ≈ 0.69 m).
- Collision: UCX children imported automatically with no log errors.

**(6) Risks / OPEN.**
- OPEN: weighted base material (metal plate vs wood). The PLATE reads as a
  dark flat plinth; sound canon says "wood-through-floor" footfall (MOTION
  §Sound) — that describes the SOUND source, not the base. Ask.
- OPEN: which leg has the window (PLATE: viewer-right shin; BUILD has none).
- Risk: rods inside the leg are invisible at gameplay distance — the window
  must be large enough (≈ 0.3 m tall at 3.35 m) to read.

---

### 1.6 TAIL — segmented core, fur, rust tip

**(1) Canon.**
- PLATE (observed, main figure and back view): a thick tail curving out low
  behind the viewer-right leg, matted fur, a lighter rust/ochre tip; in the
  back view it hangs to the ground. Stage canon for reference: "wire in
  ears, tail, and spine" (FABRIC §3).
- Motion: "no secondary motion of any kind … nothing on him bounces, ever"
  (MOTION §AFTER-FIRE) — the tail is rigid mass; "the After-Fire rig has
  physics secondaries DISABLED and wool baked stiff" (MOTION §PRODUCTION
  NOTES). TRACKER 1.6: "segmented core, fur, rust tip".

**(2) What exists.** BUILD 443–456: five spheres joined → `organic()`
(voxel 0.02); fur cards; `TailPivot` empty. In UE the tail imported as
DISCONNECTED lumps trailing behind the body (`renders/ue_chum_af.png`
shows three separate blobs) — the FBX flatten or the decimate split it.
Not in the sodium findings (it was off-frame).

**(3) Asset-reuse plan.**

| Need | Candidate | Notes |
|---|---|---|
| Matted fur / rust tip | `curly_teddy_natural` (matted plush) + `caban` (rust woolen fleece) · Poly Haven · CC0 | tip albedo/normal from caban tinted rust; body from teddy/boucle as 1.1 |
| Segmented core showing at breaks | `Rope002` · AmbientCG · CC0 (cable spine) ; `modular_pipes` · Poly Haven · CC0 (a flanged segment) | if the "segmented core" is exposed at a torn segment (**OPEN**) |
| Fab (confirm) | "fur", "matted fur", "rope" | |

**(4) Blender steps.**
1. Build the tail as ONE continuous bevelled poly-curve (radius tapering
   0.09 → 0.04 at 2.6 m base) with 6–8 control points — a single mesh,
   never joined spheres (fixes the UE disconnection).
2. Optional segment ridges via a displace along the curve U (the
   "segmented core" read) — the PLATE shows the segmentation as fur banding,
   not exposed hardware; keep hardware hidden unless the owner rules
   otherwise.
3. Remesh 0.015, fused-wool scan, rust tip via a gradient multiply mask on
   the bake; fur cards only along the dorsal ridge and at the tip.
4. Parent to `TailPivot`; in 1.9 the tail gets 3 bones but no physics.

**(5) Acceptance test.**
- Sodium: the tail reads as matted wool with a distinct rust tip in value,
  not hue (sodium kills hue — the tip must differ in roughness/normal too).
- UE capture from behind: ONE continuous tail, grounded, no gaps.
- Scale truth: tail length ≈ 1.3 m at 3.35 m.

**(6) Risks / OPEN.**
- OPEN: whether any core hardware is exposed on the tail (no text canon).
- Risk: the FBX flatten (`parent_clear KEEP_TRANSFORM`, EXPORT) cannot
  split a single mesh — confirm the disconnection was the sphere join.

---

### 1.7 FULL-FIGURE UNIFICATION + TEXTURE/SIZE BUDGET

**(1) Canon.**
- Scale: 3.35 m standing, tally eye at 3 m (DOSSIER §THE SCALE LAW; PLATE).
- Textures: "ORM packed; 2K default, 4K only for Chum and the readables"
  (PIPELINE §STANDARDS); "LOD1 for set dressing only, hero props none"
  (PIPELINE §STANDARDS); "crafted-world polycounts are modest by doctrine"
  (PIPELINE §STANDARDS).
- Sockets `SOCKET_JawLever`, `SOCKET_EyeTally`, `SOCKET_Bell` (PIPELINE
  §STANDARDS). Machine: "M1 Pro / 16GB / ~18GB free disk" (PLAN §1).
  TRACKER 1.7: "Full-figure unification + texture/size budget".

**(2) What exists.** `assets/models/chum_af.glb` is 79.5 MB; the UE FBX
was 78 MB with 64 maps and 30 material instances (LEDGER 075; TRACKER 0.3).
Bakes are separate diff/nrm/rgh PNGs (`bake_all()`), not ORM-packed. The
body is authored at 2.6 m and stands 3.08 m in UE unscaled (TRACKER 0.3).
Every part is a separate object; ~200 objects (stitches, staples, rivets,
whiskers) each become draw calls.

**(3) Asset-reuse plan.** None new. This unit consolidates: one
`T_ChumAF_<part>_BC/_N/_ORM` triplet per material group; pack ORM in
Blender (compositor or a numpy pass) at export so `fixup_materials.py`
wires three textures per instance.

**(4) Blender steps.**
1. **Authoring scale decision (resolve here):** rescale the whole build to
   true 3.35 m in Blender (multiply every coordinate by 3.35/2.6 = 1.2885
   via a global scale applied before remesh, or rebuild constants) so the
   FBX is scale-true with no runtime scaling — UE has no `rundown.gd`
   scaling step and PLAN §R.5 demands scale truth in the acceptance view.
   Check: tally eye centre lands at z ≈ 3.01 m (BUILD 2.34 × 1.2885) — matches
   "sits at three meters" (DOSSIER §THE SCALE LAW). Voxel sizes in `organic()`
   scale with it (0.035 → 0.045) unless tightened.
2. Material groups (target ≤ 12 instances): Wool (body/legs/arms/tail/
   skull/jaw/ears share one BC/N/ORM atlas or one per limb group), Patches,
   Leather (collar, lips, grips), Iron (rods, brackets, staples, hinge),
   Brass (bell, bands), Bone (teeth, claws), Lens (Camera_01), Speaker,
   MawBlack, FurCards, Whiskers, Button.
3. Join stitch/staple/rivet families into their parent bake objects and
   move sub-2 cm detail into maps (finishes what 1.1/1.8 start).
4. Emit `SOCKET_JawLever` (at the mouth lever grip, BUILD `lgrip` 0.115,
   −0.372, 2.14 × scale), `SOCKET_EyeTally` (lens centre), `SOCKET_Bell`
   as empties exported with the mesh (EXPORT keeps `EMPTY` types).
5. Budget target (**proposal — no canon number exists, OPEN**): FBX ≤ 25 MB,
   maps ≤ 20 with ≤ 2 at 4K, ≤ 300 k triangles including fur cards, 0 LODs.
6. Extend `export_ue.py` to write ORM and to assert the naming law on every
   object/material (pipeline "complains instead of the artist remembering",
   PIPELINE §VERSIONING AND FLOW).

**(5) Acceptance test.**
- UE import log: 0 errors, every instance wired with BC/N/ORM (manifest
  count == instance count), sockets present on the mesh.
- Capture at the greybox anchor (`capture_gate.py` precedent): full body
  3.35 m ± 0.02 measured against the stamped 1 m calibration cube
  (`export_ue.py --cube`, the 0.2 precedent); tally at 3.0 m.
- Budget numbers recorded in the ledger; the daylight and dark baselines
  re-shot and archived to `docs/telemetry/ue-baselines/`.

**(6) Risks / OPEN.**
- OPEN: budget numbers (above) — record the owner's ruling.
- OPEN: whether the Godot reference (`rundown.gd` scaling to 3.35 from
  2.6) should keep consuming `chum_af.glb` at 2.6 m — if the reference
  game must stay runnable (PLAN preamble), export the glb at 2.6 and the
  FBX at 3.35 from the same build.
- Risk: ORM packing changes sRGB/linear handling — roughness and metallic
  are Non-Color; test on one material before the batch.

---

### 1.8 HEAD REALISM RETROFIT per §R

**(1) Canon.**
- "Head realism retrofit per §R (staples→maps, sculpted teeth, beveled
  metals, fur density/anisotropy; AF jaw posed SHUT per canon)" (TRACKER
  1.8; PLAN §5).
- "CAPTURE CANON: After-Fire poses show the jaw open ONLY with his hand at
  the lever (the two-beat act); a jaw hanging open with no hand at work is
  canon-wrong. Default resting pose: jaw closed, hand down." (PLAN §1
  "Motion & sound law").
- PLATE callouts: "MELTED BUTTON EYE (NON-FUNCTIONAL) SCORCHED & WARPED";
  "TALLY LIGHT CAMERA EYE"; "MANUAL JAW HINGE ASSEMBLY (LEFT & RIGHT)
  HAND-OPERATED NOT MOTORIZED"; detail 1 "MELTED BUTTON EYE — ORIGINAL BUTTON
  SCORCHED, HEAT-WARPED, AND LOCKED INTO FELT. PURELY COSMETIC"; detail 4
  "MANUAL JAW RIG — LOWER JAW ON HINGE WITH LEVER LINKAGE. HAND LEVER INSIDE
  MOUTH CONNECTED TO LOWER JAW ROD"; "MANUAL JAW CONTROL BREAKDOWN: HAND
  LEVER (INSIDE MOUTH) · LINKAGE ROD TO LOWER JAW · LOWER JAW ON HINGE ·
  PUPPETEER OR CHUM'S OWN HAND PULLS LEVER TO OPEN JAW. PUSHES TO CLOSE. NO
  MOTORS. PURELY MECHANICAL."
- "the original button eye melted shut and kept anyway, purely cosmetic. The
  other socket got a TALLY LIGHT CAMERA EYE" (DOSSIER §WHAT IT IS); the eye
  "burns ONLY while a capture runs" (DOSSIER §THE SCALE LAW); "His eye is
  the game's only mobile red" (PLAN §1 "Lighting law").
- Eye hierarchy: "buttons are reserved for Chum" (ARTBIBLE line 21).
- Held deltas from 0.3: "tally not yet emissive in UE, fur mottle vs plate,
  hardware tier" (TRACKER 0.3).

**(2) What exists.** BUILD 498–1055: the head is the most developed part —
skull `organic()` with folds; HD ears (voxel 0.007, staples shrinkwrap-
snapped as SOLID cylinders onto the felt, solid inner panels, blanket
stitches); quilt face panels (still `head_patch()` thin shells, excluded
from the bake — LEDGER 066); ~70 stitch/staple cylinders (`stitch_run`,
crown seam, X-ticks, border stitches); gear-rosette button eye (10 sphere
teeth, 4 hole cylinders, 6 scorch-ray cylinders, a melt drip sphere);
Camera_01 lens barrel in a copper torus ring with 8 sphere rivets; remeshed
felt nose; MawBlack void; `lip_tube()` bevelled leather lips with 26 + 20
staple cylinders; 11 upper + 4 lower teeth as scaled CUBES; 7 grille cubes;
mouth lever rod + grip; 8 straw whiskers (2-segment cylinders); jaw as
remeshed sphere with 9 chin-band cubes + rivets, 2 hinge bolts, 2 jaw bars
(tori), a lever cylinder. Sodium verdict: "fur, lens, mouth hardware,
whiskers, ear panels PASS — they read as fiber, machined metal, straw,
felt" (LEDGER 076). The UE dark baseline shows "the lens a pale blind eye"
(LEDGER 075) — the tally core is not emissive in UE.

**(3) Asset-reuse plan.**

| Need | Candidate | Notes |
|---|---|---|
| Teeth / bone | Fab "bone", "animal bone", "tooth", "ivory" (Megascans has bone atlases) · Fab standard; CC0 fallback: `bull_head` · Poly Haven (horn PBR) | replace the cube teeth with remeshed, chipped slats wearing a bone scan (ToothBone stays the tint) |
| Beveled hinge / bands | `gate_latch_01`, `bench_vice_01` (rusted, worn) · Poly Haven · CC0; `Metal008` (bronze scratches) · AmbientCG · CC0 | chin bands, hinge bolts, jaw bars: cut from donor hardware or bevel-curve with edge wear; copper smudge → real bronze/iron scans |
| Lens ring | `Metal058B`/`058C` (copper oxidation) · AmbientCG · CC0 | the "dark aged copper" (LEDGER 066) with oxidation instead of smudge |
| Button | `Leather026`/`Leather027` (black, smooth) · AmbientCG · CC0 for the horn/bakelite read | melted button: matte near-black with dead specular (LEDGER 066) — needs roughness variation to pass §R.3 |
| Face felt / quilt | as 1.1 plus `poly_wool_herringbone`, `Fabric031` | the face panels re-baked as solid panels |
| Whisker straw | `hessian_380` (jute) · Poly Haven · CC0 for the straw normal | whiskers stay geometry (silhouette) but wear a fibre normal |
| Fur | fur cards atlas (in hand) regenerated with denser, shorter, singed tufts | `make_fur_cards.py` parameters, not a new asset |

**(4) Blender steps.**
1. Face quilt panels: rebuild as SOLID embedded panels (the ear-panel
   method, BUILD 669–691) and include them in the bake with their PanelA/B/C
   tints — the thin shells go away.
2. Staples → maps: bake every stitch/staple family (`SeamC/L/R`, crown,
   X-ticks, border, `LipStaplesU/L`, ear edge/blanket stitches) into the
   parent's normal/albedo/roughness by a one-off "high→low" bake (select
   the stitch cylinders as the high-poly source with `use_selected_to_active`
   + cage) — then delete the cylinders. Keep as geometry ONLY what breaks
   the silhouette: teeth, lips, hinge bolts, chin bands, lever, lens, rivets
   ≥ 2 cm (PLAN §R.2).
3. Teeth: 13 upper + 4 lower remeshed slats (voxel 0.004) with chipped tips
   and root staining; bone scan; keep the two knocked-out gaps and the stub
   (BUILD 909–917 already encode this asymmetry — preserve it).
4. Beveled metals: chin bands, jaw bars, hinge bolts and the lens ring as
   bevel-curve or donor-cut geometry with an edge-wear mask (Cycles `Bevel`
   node baked to the normal + a curvature-driven roughness/albedo wear in
   the bake material); no tori, no scaled cubes.
5. Tally core: an emissive inner element behind the lens (BEAUTY builds a
   `TallyEyeLive` sphere at runtime — bake it into the asset as a small
   remeshed lamp element with an `Emissive` material named
   `M_TallyCore` so UE can drive intensity 0 ↔ lit); `SOCKET_EyeTally` at
   its centre.
6. Fur density/anisotropy: regenerate the atlas with shorter, singed,
   clumped tufts; restrict skull cards to the crown/cheeks/neck; ear backs
   keep density (LEDGER 067); in UE the `M_FurCards` roughness constant
   (`fixup_materials.py`) gains an anisotropy/roughness texture from the
   atlas alpha so the pile breaks light three ways.
7. Jaw posed SHUT at export (`Jaw` empty rotation 0); BEAUTY's 0.2 rad open
   is a design-only pose and must be paired with the hand at the lever in
   any shipped render (PLAN §1 CAPTURE CANON) — update BEAUTY to raise the
   right hand to the lever when it opens the jaw, or render shut.
8. Sodium `--subject` framed on the head (add a `--frame head` option to
   SODIUM that reuses BEAUTY's shot-1 camera: location (0.06, −2.65, 2.5)
   aimed at (0, −0.05, 2.35) at 2.6 m base — scale with 1.7).

**(5) Acceptance test.**
- Sodium (head frame): staples read as sewn steel from the map at the
  script's distance and do not "pop" as separate objects; teeth read as
  bone (roughness/albedo variation, no flat faces); metals show edge wear
  under the single lamp; the button reads matte horn, not plastic.
- UE dark locked-EV head portrait (the frame "every future Chum unit must
  beat", LEDGER 075): the tally core burns red at an intensity that reads
  through the Camera_01 barrel without bloom washout; dark → lit toggles by
  one scalar parameter on `M_TallyCore`; fur reads as singed pile, not
  ribbon strips; hardware reads at the "hardware tier" (TRACKER 0.3 held
  delta closed).
- Scale truth: head width ≈ 1.0 m at 3.35 m; lens ≈ 0.22 m; teeth 0.1–0.14 m.
- Capture canon: every archived frame has the jaw SHUT or the hand at the
  lever (PLAN §1).

**(6) Risks / OPEN.**
- OPEN: the PLATE shows the jaw open with the hand at the lever in the
  turnaround and open with no hand in the hero pose — the hero pose is a
  dossier photo, not a game capture; PLAN §1's CAPTURE CANON governs the
  build's renders.
- OPEN: emissive behaviour is 1.12's to wire; 1.8 only ships the element.
- Risk: the high→low stitch bake is a new technique in this pipeline; do
  one seam first and inspect the normal map texel (measure the texel, PLAN
  §1) before batching.
- Risk: the button eye's "dead specular" (LEDGER 066) fights §R.3 — give it
  roughness VARIATION (scorch crazing) rather than flat 0.9.

---

### 1.9 THE POUR — After-Fire locomotion

**(1) Canon (MOTION §AFTER-FIRE, verbatim rules).**
- "No anticipation, no overshoot, no settle, no secondary motion of any
  kind"; "Where the stage body bounced, this one POURS: single-axis
  commitment, the head leading and the body arriving in one uninterrupted
  arc, knees nearly stiff, stride long, cadence slow, silhouette always at
  full height."
- "LINEAR IS THE HORROR CURVE: linear-dominant with two-frame ease caps at
  most. Stops are ABSOLUTE and binary: he is pouring or he is parked,
  statue-still, zero idle sway, no breathing, while the eye alone keeps
  tracking, servo-smooth."
- "He never orients to the player as a person; he faces PATHS."
- Timings as built: "0.8 m/s approach, 1.2 m loom, 2.0 s cool, 2.2 s fold,
  1.6 m/s crossing" (MOTION §1); the crossing is "double approach speed"
  (DOSSIER §THE LAST CROSSING).
- Rig: "the After-Fire rig has physics secondaries DISABLED and wool baked
  stiff, root-motion authored clips … eye on its own always-on track layer"
  (MOTION §PRODUCTION NOTES). Blender owns rigging ("rigging (Chum's jaw
  lever, sockets)", PIPELINE §DIVISION OF LABOR).
- TRACKER 1.9 restates: linear-dominant curves, head-leads single arc,
  absolute stops, parked-statue idle, NO secondary motion, servo eye on its
  own layer.

**(2) What exists.** No armature. The build uses empties (`Head`, `Jaw`,
`HipL/R`, `ShoulderL/R`, `TailPivot`) as parents; the Godot `rundown.gd` did
procedural animation on those empties (PLAN §1 "reference implementation").
The UE brain `ARundown` already moves the actor at the canon speeds
(TRACKER 0.7, 0.8a) but the mesh is a static `SM_ChumAF`.

**(3) Asset-reuse plan.** No CC0 animation is applicable — the grammar is
authored. Reuse: UE's root-motion pipeline and Animation Blueprint; Blender
Rigify is NOT recommended (its IK/secondary defaults are the wrong
grammar); a hand-built minimal armature is the asset.

**(4) Blender steps.**
1. Armature `SK_ChumAF`: Root (ground), Pelvis, Spine1, Spine2, Neck, Head,
   Jaw (hinge at the `Jaw` empty), EyeTally (child of Head; its own layer),
   Clavicle/UpperArm/Forearm/Hand + 4 finger chains × 3 per side (1.4),
   Thigh/Shin/Foot/Toe per side, Tail1–3. No physics, no cloth, no jiggle.
2. Skin with automatic weights then HARD-edge the weights (wool baked
   stiff: the fused body deforms only at hip/shoulder/neck; the quilt does
   not stretch — use rigid-body-style weights of 1.0 per limb with 2–3 cm
   blend bands).
3. Clips (Blender actions → separate FBX per action, `bake_anim=True`
   for animation exports — EXPORT currently sets `bake_anim=False`; add an
   `--anim` mode):
   - `A_ChumAF_Pour_Walk`: root motion 0.8 m/s, stride ≈ 1.6–1.8 m at
     3.35 m, knees ≤ 10° flex, head leads each step by 2–4 frames, torso
     follows in one arc; curves LINEAR with ≤ 2-frame ease caps (Blender:
     interpolation LINEAR on all keys, then 2-frame BEZIER caps only at the
     step contacts).
   - `A_ChumAF_Pour_Cross`: the same at 1.6 m/s (time-scale the walk; no
     added bounce).
   - `A_ChumAF_Parked`: a single held frame (statue) — zero-length loop.
   - `A_ChumAF_Stop` / `A_ChumAF_Start`: absolute, ≤ 2 frames each.
   - Eye: `A_ChumAF_EyeTrack` is NOT a clip — in UE the EyeTally bone is
     driven by an AnimBP layer (Look-At with a slew-rate limit, "servo-
     smooth") that stays live in Parked.
4. Export `SK_ChumAF.fbx` (mesh + armature + sockets) and one FBX per
   action; naming per PIPELINE (`SK_`, and `A_` for animations — **OPEN**:
   PIPELINE lists no animation prefix; `A_` is the UE convention).

**(5) Acceptance test.**
- Frame-sequence capture (≥ 8 frames or an MRQ clip, PLAN §4) of the walk
  at the greybox corridor: overlay consecutive frames — the head crosses
  the frame first, the body arrives in one arc; no vertical bob beyond the
  stride geometry; no part moves after a stop (diff the last two frames of
  a stop: pixel-identical except the eye).
- Curve audit: export the walk action's F-curves and assert every key is
  LINEAR except ≤ 2 frames at contacts (a small script; record the count).
- Speed: root motion measured at 0.8 m/s ± 0.02 over 10 s in PIE
  (`ARundown` telemetry format, TRACKER 0.7).
- Silhouette at full height for the whole loop (max head z varies < 3 cm).

**(6) Risks / OPEN.**
- OPEN: animation asset prefix (above).
- OPEN: stride length and cadence numbers (canon says "long" and "slow"
  only) — propose 1.7 m / 0.47 Hz at 0.8 m/s and record.
- Risk: root-motion FBX from Blender needs the Root bone on the ground and
  the UE import option "Force Root Lock" off — test on a 2 m straight clip
  before authoring the loop.

---

### 1.10 THE FOLD + THE WITHDRAWAL

**(1) Canon.**
- "THE FOLD (2.2 s at every doorway): he does not duck, he REORGANIZES:
  shoulder through first, then the head arriving late on a hinge that
  should not exist: the one place puppet logic returns, horribly, rod
  movement without rods." (MOTION §AFTER-FIRE). "HE DOES NOT FIT THROUGH
  DOORS. Every doorway costs him 2.2 seconds of folding, announced by
  caption and, when close, by a line about him bending and keeping his eye
  on you the whole way through" (DOSSIER §THE SCALE LAW). "the fold as a
  single authored 2.2 s montage per door width" (MOTION §PRODUCTION NOTES).
- Fold sound: "S18 plus one soft textile drag and a single low wooden
  knuckle as the head arrives" (MOTION §Sound).
- "THE WITHDRAWAL (tally cools with distance): he reverses along his exact
  approach path without turning, motion played backward, an undo" (MOTION
  §AFTER-FIRE); "If you are clear, he withdraws to his segment" (DOSSIER
  §THE TALLY CONTRACT).
- Door toll data: "2.2s door fold toll from Data/Doors.csv" (TRACKER 0.7).
  His "SHADOW IS A MECHANIC (3.35m — the fold announces by silhouette
  through doorways)" (PLAN §1 "Lighting law").

**(2) What exists.** `ARundown` charges the 2.2 s toll from `Data/Doors.csv`
(TRACKER 0.7); no fold animation; no withdrawal clip. Doors.csv holds 20
doors (TRACKER 0.5).

**(3) Asset-reuse plan.** None (authored motion). Reuse: 1.9's rig and the
Doors.csv widths.

**(4) Blender steps.**
1. `ue/Restoration/Data/Doors.csv` (columns `room_a,room_b,gap_x,gap_z,
   width,axis,kind`; extracted deterministically by TRACKER 0.5) carries
   exactly THREE distinct widths across its 20 doors, read 2026-09-04:
   **1.2 m (2 doors), 1.4 m (11 doors), 1.6 m (7 doors)**. So "per door
   width" (MOTION §PRODUCTION NOTES) means three fold variants:
   `A_ChumAF_Fold_120`, `A_ChumAF_Fold_140`, `A_ChumAF_Fold_160`. Against a
   3.35 m body with a ≈ 1.0 m head (§1.8) every width forces the fold; the
   1.2 m variant is the most contorted.
2. Per distinct width: `A_ChumAF_Fold_<w>` exactly 2.2 s (66 frames at
   30 fps; **OPEN** frame rate — UE default 30, record the choice): frames
   0–20 the lead shoulder drops and rotates through the threshold; 20–50
   the torso follows as a single arc; 50–66 the head arrives LATE on a
   neck hinge that bends past a real neck's limit (the "hinge that should
   not exist"), the eye held on the player's last position (EyeTally layer
   stays live). Linear curves; the head's late arrival is the only
   non-uniform timing and it ends absolutely.
3. Withdrawal: no new clip — the UE AnimBP plays `A_ChumAF_Pour_Walk` at
   play-rate −1 while `ARundown` retraces the recorded approach path
   without a turn (MOTION: "motion played backward"). Blender contributes
   nothing except confirming the walk loop reverses cleanly (no
   asymmetric contact pops).
4. Silhouette check: render the fold from the far side of a stamped
   greybox door with a single practical behind him — the shadow must read
   as the fold on the floor.

**(5) Acceptance test.**
- MRQ clip of the fold at a greybox door: duration exactly 2.2 s from
  first shoulder motion to head rest; shoulder crosses the threshold before
  the head; the head arrives last, on the impossible hinge; the eye tracks
  through the whole fold; no idle motion after the head lands.
- Withdrawal clip: the path replay diff (position log forward vs backward)
  is mirror-exact within 5 cm; the body never yaws more than 2° during the
  reversal.
- Caption hook present: `[THE JAW WORKS ITS LEVER]`-style caption events
  exist for the fold per DOSSIER §THE SCALE LAW ("announced by caption") —
  the text key lives in GameText (714 keys, TRACKER 0.5); **OPEN** which key.

**(6) Risks / OPEN.**
- Resolved: three fold variants (1.2 / 1.4 / 1.6 m) from Doors.csv; the
  door HEIGHT is not in the CSV (greybox slabs are stamped by
  `build_greybox.py`, TRACKER 0.6) — **OPEN** whether height varies; if it
  does, the variant key becomes width×height.
- OPEN: fold frame rate.
- Risk: a reversed walk with root motion in UE needs the root motion
  extracted forward and applied by the brain, not by the clip, or the
  reversal will slide.

---

### 1.11 THE PERFORMANCE QUOTE

**(1) Canon.**
- "THE PERFORMANCE QUOTE, the doctrine's crown: while the tally burns and
  he stands at 1.2 m, he squares FULLY FRONTAL to you, broadcast stance,
  and permits himself exactly one pre-fire mannerism: the clean
  fifteen-degree head tilt. THE TALLY TURNS HIM BACK INTO A PERFORMER."
  (MOTION §AFTER-FIRE).
- "Under the tally, inside the performance quote, the jaw hand works its
  lever open and closed at no rhythm a song would keep: a show with the
  sound removed, performed at you. Outside the light, the jaw opens exactly
  once: the beat before a strike, hand rising, click, open, and then the
  near-silence. The jaw NEVER syncs to any sound, never flaps, never chews
  the air." (MOTION §AFTER-FIRE). "every opening is a two-beat act: the hand
  rises, one dry click, the jaw" (MOTION §AFTER-FIRE).
- "STATE A · TALLY LIT … he may approach, all the way to 1.2 meters. He
  cannot strike. He watches. The jaw hand works its lever, open, closed,
  open, at no rhythm a song would keep. The throat speaker breathes room
  tone." (DOSSIER §THE TALLY CONTRACT). "at loom distance the player is
  looking up into it" (DOSSIER §THE SCALE LAW).
- Pre-fire tilt reference: "Head tilts land in clean fifteen-degree stops"
  (MOTION §PRE-FIRE). TRACKER 1.11 adds "the once-only pre-strike jaw beat:
  hand, click, open, silence".

**(2) What exists.** `ARundown` reaches the 1.2 m loom and logs "the jaw
works its lever" (TRACKER 0.8a); the mouth lever grip exists in the mesh
(BUILD 936–945); no hand-to-lever reach; the jaw pivots on the `Jaw` empty.

**(3) Asset-reuse plan.** None (authored). The lever click is 1.12's audio.

**(4) Blender steps.**
1. `A_ChumAF_Quote_Enter`: from Parked, a single linear yaw to fully
   frontal (broadcast stance: feet square, arms at rest), absolute stop;
   then the ONE tilt: head rolls 15.0° in a clean linear move with ≤ 2-frame
   caps, and HOLDS (the tilt is the quote; do not return it during the
   quote — **OPEN**: whether the tilt holds for the whole tally or plays
   once and returns; canon says "the one 15° tilt", TRACKER says "the one
   15° tilt"; hold until ruled).
2. `A_ChumAF_Quote_JawWork` (additive, arms + jaw only): the right hand
   rises to `SOCKET_JawLever`, closes on the grip (1.4's fingers), then the
   lever pulls → jaw opens (Jaw bone −20° to −35°, **OPEN** max opening — the
   PLATE hero shows roughly 30°), pushes → closes. Openings and closings at
   IRREGULAR intervals (author 5–7 events across a 20 s loop with
   non-repeating gaps 1.3 s, 2.9 s, 0.8 s, 3.6 s … so no rhythm emerges);
   the hand never leaves the lever during the loop; each open is the
   two-beat act (hand tension → click → jaw).
3. `A_ChumAF_JawBeat_PreStrike`: once-only: hand rises (0.6 s), click,
   jaw opens (≤ 0.3 s, linear), hold; the strike (an `ARundown` event — the
   strike animation itself is **OPEN**, not in this unit's box) follows.
4. All three exported per 1.9's `--anim` path; every jaw key is paired
   with a hand-at-lever pose (CAPTURE CANON, PLAN §1).

**(5) Acceptance test.**
- MRQ clip from the player's eye height at 1.2 m looking up (camera
  1.6 m high, 1.2 m from the chest): the body is fully frontal (yaw error
  < 1°), the tilt reads as exactly 15° (measure the head roll in the
  skeleton, not the image), and the jaw never moves without the hand on
  the lever (frame-by-frame audit: any frame with jaw ≠ closed AND hand
  not at socket = FAIL).
- Interval audit: the jaw event times over 60 s have no period (no two
  equal gaps).
- Pre-strike beat: exactly one opening outside the tally in the fixture
  (`test_state_af.py` extended), then silence.

**(6) Risks / OPEN.**
- OPEN: tilt hold vs return; jaw opening angle; the strike animation's
  home unit.
- Risk: the hand-to-lever reach must clear the lips/teeth — validate the
  1.4 hand at the 1.8 mouth before authoring keys.

---

### 1.12 TALLY STATES, EYE TRACKING, THROAT-SPEAKER ROOM TONE WIRED TO AI

**(1) Canon.**
- Tally: "the tally eye sits at three meters and its red light burns ONLY
  while a capture runs (the light is the contract made visible)" (DOSSIER
  §THE SCALE LAW); STATE A lit / STATE B dark with "THE TALLY COOLS for a
  marked 2.0 seconds" (DOSSIER §THE TALLY CONTRACT); the first cool "runs
  4.0 seconds" (DOSSIER §THE TAUGHT CHASE); in the last crossing "his tally
  eye DARK the whole way" (DOSSIER §THE LAST CROSSING). "RED = watched =
  SAFE" (PLAN §1 "Lighting law").
- Eye: "the eye alone keeps tracking, servo-smooth" while parked (MOTION
  §AFTER-FIRE); "eye on its own always-on track layer" (MOTION §PRODUCTION
  NOTES); "keeping his eye on you the whole way through" the fold (DOSSIER
  §THE SCALE LAW).
- Throat speaker: "under the tally it breathes band-limited room tone"
  (MOTION §AFTER-FIRE); "BAND-LIMITED IS MEMORY. FULL-RANGE IS PRESENT …
  every After-Fire sound lives in true room acoustics with floor-coupled
  sub" (MOTION §THE AUDIO LAW) — the throat speaker is the standing
  exception ("PRESENCE wearing MEMORY, always, quietly", MOTION §AFTER-FIRE);
  band: "roughly 50 Hz to 8 kHz, tape wow, studio slap" (MOTION §PRE-FIRE).
- Hard negatives (TRACKER 1.12): "bell never sounds; no vocalizations; jaw
  never syncs to sound". Other AF sounds (footfall S17, groan, hull-tick,
  fold S18, occlusion under 3 m, mains hum while recording, near-silent
  strike) are MOTION §Sound canon but belong to the SOUND MANIFEST unit
  (TRACKER C15) and Phase 5 audio — **OPEN** whether 1.12 wires more than
  the three named systems; the box names three.
- AI homes: `ARundown` AF states "tally contract/cool/crossing/dead-room
  hold" attach with GameState (TRACKER 0.7, 0.8a); the brain has no
  Behavior Tree by law (PLAN §1 PORT KIT).

**(2) What exists.** `ARundown` runs the full AF arc in simulate (approach →
loom → cutoff → cool → strike → hidden, TRACKER 0.8a) with `State->
bRecording` arming the contract (TRACKER 0.8b-2). Nothing visual or audible
is driven yet: no emissive tally in UE (TRACKER 0.3), no eye bone, no
audio emitter. `M_TallyCore` element arrives from 1.8; `SOCKET_EyeTally`,
`SOCKET_ThroatSpeaker` from 1.7/1.2.

**(3) Asset-reuse plan.**
- Room tone source: CC0 room tone from freesound.org ("Audio later:
  freesound.org CC0 / Sonniss GDC packs", PLAN §2) — search "studio room
  tone", "empty room tone 1970s", "control room hum"; band-limit in a
  MetaSound (50 Hz–8 kHz band-pass + subtle wow) rather than baking it into
  the file. Credit line in `tools/texsrc/CREDITS.md` or a new
  `assets/audio/CREDITS.md` (**OPEN** where audio credits live).
- UE: MetaSounds + submixes per the migration map (PLAN §1 PORT KIT).

**(4) Steps (UE-side, headless python + C++ per doctrine).**
1. `M_TallyCore` material instance parameter `TallyIntensity` (0 dark,
   1 lit) bound to `ARundown`'s contract state: lit while
   `State->bRecording` and the contract is active; dark otherwise; the
   2.0 s cool (4.0 s first) fades intensity linearly to 0 across the cool
   (**OPEN** — canon says the tally "cools"; whether that is a fade or a
   cut is not stated; the lighting law says transitions "CUT with the
   schedule" (PLAN §1) — ask). Add a small red point light at
   `SOCKET_EyeTally` driven by the same scalar so the "only mobile red"
   spills onto the fur (BEAUTY `TallySpill` precedent).
2. Eye tracking: AnimBP layer on the EyeTally bone, Look-At the player's
   head with a slew-rate limit (servo-smooth, e.g. 90°/s max, no easing
   curve — constant rate), always on, including Parked and Fold. Never
   drives the head (he faces PATHS, MOTION §AFTER-FIRE).
3. Throat speaker: an AudioComponent at `SOCKET_ThroatSpeaker` playing the
   band-limited room-tone MetaSound only while the tally is lit; volume
   low; NO other content ever (assert in code: the component's sound
   asset is the room-tone only).
4. Bell: no AudioComponent, and an automation test asserting no sound
   asset references `Bell`. Jaw: no audio-driven blend anywhere; the
   `[THE JAW WORKS ITS LEVER]` caption fires from the animation notify,
   not from sound (DOSSIER §SOUND AND CAPTION LAW).
5. Wire the HUD lamp only if in scope (**OPEN** — the HUD "red dot, SAFE
   WHILE LIT, the same seconds the capture counts" (DOSSIER §THE TALLY
   CONTRACT) is UI, likely Phase 4).

**(5) Acceptance test.**
- Fixture (`ue/pyscripts/test_state_af.py` extended): log lines
  `TALLY LIT` / `TALLY COOL t=` / `TALLY DARK` align with the brain's
  contract transitions; the eye Look-At target updates every frame while
  parked; the throat-speaker component reports playing only between LIT
  and DARK.
- Captures: two dark locked-EV head portraits, lit and dark, archived to
  `docs/telemetry/ue-baselines/`; the red spill visible on the fur in the
  lit frame and absent in the dark frame; no other red in frame.
- Audio: a recorded 10 s clip of the lit state analysed for energy above
  8 kHz (must be ≥ 40 dB down); silence when dark.
- Negative tests: no `Bell` audio asset; no jaw animation driven by audio;
  no vocal asset in `/Game/Characters/ChumAF`.

**(6) Risks / OPEN.**
- OPEN: cool = fade or cut; HUD scope; audio credits home; whether the
  wider AF soundscape belongs here or in Phase 5.
- Risk: the tally light must never read as room light — keep radius small
  (< 1 m) so red stays the eye's, not the room's (PLAN §1 colour contracts).

---

### 1.13 PHASE GATE — 10-shot gallery + long soak, reviewed

**(1) Canon.** "1.13 GATE: gallery + long soak test" (PLAN §5); "PHASE
GATE: 10-shot gallery + long soak, reviewed" (TRACKER 1.13). Gate style:
the owner reviews and signs; nothing self-certifies (precedent
`ue/GATE-0.10.md` "AWAITING OWNER REVIEW … nothing here is
self-certified"). Acceptance view = in-engine capture beside the canon
plate at matching framing: "same league? Would this frame pass on a 2020s
horror title's store page?" (PLAN §R).

**(2) What exists.** Gate 0.10 package format (`ue/GATE-0.10.md`,
`GATE-0.10-EVIDENCE.md`), `capture_gate.py`, the fail-bot soak
(`test_failbot.py`, 15 s; TRACKER 0.9d) and the invariant parser
(`tools/invariant_parser.py`).

**(3) Asset-reuse plan.** None new; the gallery reuses the look-dev level
and the lighting bible's locked-EV states.

**(4) Steps.**
1. The ten shots (**proposal — the shot list is not canon; OPEN for the
   owner to amend**): (1) full body vs PLATE hero framing, dark locked-EV;
   (2) head portrait dark, tally lit; (3) head portrait, tally dark;
   (4) 1 m closeup torso quilt; (5) 1 m closeup right hand on lever;
   (6) throat speaker + bell + collar; (7) legs window + feet on floor;
   (8) the fold through a stamped door, shadow visible; (9) the loom at
   1.2 m from the player's eye, tilt; (10) the walk mid-stride at gameplay
   distance, from behind a bench. Each with its sodium `--subject` frame
   for the material units.
2. Long soak: the fail-bot/explorer fixtures run for the longest practical
   duration on the M1 Pro (**OPEN** duration; propose 30 min PIE) with the
   AF body live: parser I01/I02/I22 PASS, plus new checks: no jaw-without-
   hand frames (1.11 audit), tally state log consistent (1.12), no
   secondary motion while parked (1.9 frame diff), fold toll exactly 2.2 s
   per door (1.10).
3. Package `ue/GATE-1.13.md` in the 0.10 format with a scorecard per §R
   item 1–7 per shot.

**(5) Acceptance test.** Owner signature on `ue/GATE-1.13.md`; every shot
beside the PLATE at matching framing; every material unit's sodium frame
attached; soak log attached with parser output; budget numbers from 1.7
re-measured.

**(6) Risks / OPEN.** OPEN: shot list, soak duration. Risk: the gate is
the first time all Phase-1 systems run together; reserve a session for
fixing rather than shooting.

---

## 2 · QUICK TABLE — UNIT × EXISTING × VERDICT × PRIMARY ASSETS

| Unit | BUILD lines | Sodium/engine verdict | Primary reuse (all CC0 unless Fab) |
|---|---|---|---|
| 1.1 Torso | 333–350, 472–496 | FAIL faceted clay; patches are banned shells | wool_boucle, Fabric031, hessian_230/380, ribbed_corduroy, Fabric080, Bark015, Rust009, Metal058A; Fab "burnt wood"/"quilted fabric" |
| 1.2 Speaker | 466–469 | naked cylinder | vintage_radio_transceiver / boombox (donor cut), Rope002, metal_grate_rusty; Fab "vintage speaker" |
| 1.3 Collar/bell | 458–464 | torus + sphere | fabric_leather_01/02, Leather034C, brass_vase_01/brass_pot_01 sets, Metal058B/C, gate_latch_01 |
| 1.4 Arms/hands | 376–441 | FAIL wax hands; primitives | Rope002, modular_electric_cables, bolt_cutters_01/pipe_wrench (donor cuts), Metal041B, bull_head horn; Fab "bone"/"claw" |
| 1.5 Legs/feet | 353–374 | FAIL wax feet; rods outside | modular_industrial_pipes_01, modular_pipes, Rust009, MetalPlates013, hessian_230, metal_plate_02 |
| 1.6 Tail | 443–456 | disconnected in UE | curly_teddy_natural, caban; single bevel curve |
| 1.7 Unify | all | 78 MB FBX, 64 maps, 30 MIs, 3.08 m | none; ORM pack, sockets, 3.35 m |
| 1.8 Head | 498–1055 | PASS fur/lens/hardware/whiskers; staples are geometry; teeth cubes; tally not emissive | Fab "bone", Metal008, Metal058B/C, gate_latch_01/bench_vice_01 cuts, fur atlas regen |
| 1.9 Pour | — (no rig) | — | authored armature + clips |
| 1.10 Fold/Withdraw | — | toll charged, no motion | Doors.csv widths |
| 1.11 Quote | — | loom reached, no motion | authored clips |
| 1.12 Tally/eye/tone | — | brain states only | freesound CC0 room tone, MetaSound band-pass |
| 1.13 Gate | — | — | gate package |

---

## 3 · THE BIGGEST REALISM RISK ACROSS PHASE 1

The single largest risk is that the body keeps reading as a plush toy
instead of the canon's fused, scorched, quilted mass. Today the head passes
sodium and the rest fails, but the failure is not only the faceted
belly and wax hands the check named: the whole coat is built from fluffy
fur cards and particle hair over smooth spheres, so the Cycles beauty
reads as a soft teddy with hardware glued on, while MOTION §AFTER-FIRE
demands "the wool is fused and reads as mass" and PLATE shows matted char
with every patch seam stitched. Units 1.1, 1.4, 1.5 and 1.8 all pull on
the same thread — move pile, seams and staples into scan-carried maps on
solid remeshed geometry, keep fur cards only at singed rims, and give
every surface the three-way light response — and if that thread is pulled
inconsistently (one limb fused, one limb plush; patches as maps here and
shells there) the puppet will fail §R.7's material-truth test no matter how
good each unit looks alone. The mitigation is procedural: settle the fused
wool material stack in 1.1 (`burlap_nodes()` + wool_boucle + char masks),
reuse it verbatim for every limb, and run the `--subject` sodium frame after
every unit so the body is judged as one material that "forgot how to be
soft", not as seven separately pretty parts.
