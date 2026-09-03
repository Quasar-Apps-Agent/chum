# RESTORATION · AAA BUILD PLAN — BLENDER + UNREAL ENGINE 5.8

**The charter for the recurring build routine.** Every session MUST read this
file and `PROGRESS.md` first, do exactly one unit, verify it through the full
check loop, mark it off, commit, push, and leave the repo green.

**THE STACK (owner decision, 2026-09):** assets are built in **Blender**
(the factory in `tools/` — unchanged); the game runs in **Unreal Engine 5.8**
(`/Users/Shared/Epic Games/UE_5.8`). The Godot implementation in this repo is
now the **REFERENCE IMPLEMENTATION**: it holds the proven gameplay, AI,
puzzle logic, and invariants. It is the SPEC for the port — keep it runnable,
mine it constantly, delete none of it until Phase 0's parity gate passes.

Mission: a smooth, cohesive, AAA-looking horror game. Campaign order:
**Unreal foundation & port → Chum → cast → studio rooms & props → puzzles &
functionality → polish/audio/perf/packaging.**

---

## 0 · SESSION PROTOCOL

1. Confirm the repo is green (last README ledger entry + `git status`).
   Broken = fixing it IS the unit. Never build on red.
2. Take the FIRST unchecked box in `PROGRESS.md`. No skipping, no gold-plating.
3. Work it using the doctrine (§1), asset policy (§2), pipeline map (§3).
4. Run the verification loop (§4). Look at every image with your own eyes.
5. Close out: tick the box, append the README ledger entry, copy current
   renders/captures to the Desktop (`chum-*-current.png`), `git add -A &&
   git commit && git push` (remote: github.com/Quasar-Apps-Agent/chum,
   auth in keychain). One unit per session; split oversized units into
   sub-boxes and finish the first.

---

## R · THE REALISM BAR (what "AAA" means — checkably)

**The ACCEPTANCE VIEW is the in-engine Unreal capture** (Movie Render Queue
or high-res screenshot from the look-dev level). Blender Cycles renders are
design tools only. Every visual unit ends with its in-engine capture next to
the canon plate at matching framing: *same league? Would this frame pass on
a 2020s horror title's store page?* If no — iterate before ticking.

1. **No naked primitives.** Everything visible is a sourced asset, a merged/
   remeshed/sculpted mesh, or beveled with edge wear. Raw cylinder caps and
   perfect circles = programmer art = rejected.
2. **Small detail lives in MAPS.** Stitches/staples/seams/engravings <2cm go
   in normal+roughness+albedo maps baked onto parent surfaces; separate
   geometry only where silhouette demands (teeth yes, threads no).
3. **Every surface breaks light three ways**: albedo variation, roughness
   variation, normal detail.
4. **Lighting is part of the asset**: Lumen GI + virtual shadow maps, fog
   volumes, tuned exposure in the standard look-dev level. A model is done
   only when the ENGINE shows it well.
5. **Scale-truth**: judge at gameplay distance AND 1m closeup.
6. **Motion**: animation passes anticipation/ease/follow-through on captured
   frame sequences; no pops.

---

## 1 · DOCTRINE

**Blender asset factory (unchanged, battle-tested)**
- Deterministic build scripts in `tools/` (`build_chum_af.py` is the
  template): remesh organics, scan-dressed materials, 2048 bakes with packed
  images, fur-card generation (`make_fur_cards.py` atlas), in-file particle
  hair for design renders, real CC0 donor meshes cut down via bmesh (the
  Camera_01 tally-lens precedent).
- sRGB→linear on authored colors; measure the texel not the render; raycast
  forensics for mystery surfaces; thin shrinkwrapped shells are BANNED
  (they collapse — solid geometry only); Principled Hair needs MELANIN
  parametrization; Metal renders SIGABRT occasionally — retry once.
- Every dir containing `.blend` keeps a `.gdignore` (harmless post-Godot,
  protects the reference implementation's importer).
- Cycles beauty + EEVEE bench renders remain the DESIGN loop before any
  engine import.

**Unreal side (learned so far; extend as lessons land)**
- Engine: UE 5.8 at `/Users/Shared/Epic Games/UE_5.8`; editor CLI:
  `Engine/Binaries/Mac/UnrealEditor-Cmd "<uproject>" ...`. Project lives at
  `ue/Restoration/Restoration.uproject` in this repo.
- Machine is M1 Pro / 16GB / ~20GB free disk: KEEP CACHES CAPPED (project
  DerivedDataCache local, prune `Saved/`, `Intermediate/` — all gitignored).
  Watch disk before every session; below 8GB free, cleanup IS the unit.
- Import path: Blender→glTF (.glb) via Interchange, or FBX where Interchange
  fights us. Units: UE is centimeters — export scale ×100 (glTF importer
  handles when "Uniform Scale" left default; VERIFY on first import).
- Material mapping on import never fully survives: budget a material-fixup
  Python step per asset (Editor Python: `-run=pythonscript -script=...`).
  MawBlack → Unlit black material. Fur cards → two-sided masked material.
- Automation loop: Editor Python scripts for import/setup, Movie Render
  Queue (or `HighResShot`) for captures, `-ExecCmds="Automation RunTests"`
  for tests, all headless via UnrealEditor-Cmd. First runs compile shaders —
  SLOW (minutes); patience, don't kill young processes.
- Gameplay code: Blueprints where visual/simple, C++ where systemic. Port
  from the GDScript reference — logic is already proven; translate, don't
  redesign. Keep node/bone naming contracts (Head, Jaw, tally socket).

**The reference implementation (Godot, in place)**
- `scripts/rundown.gd` = Chum's whole AI + procedural animation brain.
- `scripts/player.gd`, interactables, `world_builder.gd` (whole studio
  layout with coordinates!), save v16, `scenes/soak.tscn` invariant harness
  (I01 warn-precedes-strike, I02 no-strike-thru-wall, I22 noise-attribution,
  I06 fail-forward-finale) — these invariants get UE automation-test
  equivalents in Phase 0.9.

---

## 2 · ASSET POLICY

- **CC0 web sources (as before):** Poly Haven (api.polyhaven.com — models/
  HDRIs/textures), AmbientCG (User-Agent header required). Downloads into
  `tools/modelsrc/` + `tools/texsrc/` with CREDITS.md lines.
- **NEW — the Unreal ecosystem (the reason for this pivot):**
  **Fab / Quixel Megascans** — free-in-Unreal content via the Fab plugin or
  fab.com while signed into the owner's Epic account. Surfaces, decals,
  3D scans, foliage. License: fine for this UE game; note each import in
  `ue/CREDITS-FAB.md`. Prefer Megascans for environment surfaces & props
  before building anything by hand.
- Everything imported gets the wear pass (nothing showroom-new) and a
  credits line. CC0 or Fab-standard licenses only; no ripped content.
- Audio later: freesound.org CC0 / Sonniss GDC packs.

---

## 3 · PIPELINE MAP

- Blender factory: `tools/build_*.py`, `tools/render_*_beauty.py`,
  `tools/make_fur_cards.py`, `tools/debug_face.py` — unchanged.
- Unreal project: `ue/Restoration/` — Content/{Characters,Studio,Props,
  LookDev,Core}. Editor Python utilities live in `ue/pyscripts/` (import,
  material fixup, capture, test-run helpers) — build them once, reuse
  forever.
- Reference Godot game: repo root (runnable via Godot 4.3 as before).
- Ledger: `README.md`. Tracker: `PROGRESS.md`. Push every session.

---

## 4 · VERIFICATION LOOP (every unit)

```
1. Blender rebuild of touched assets     → WROTE, no Traceback
2. Cycles/EEVEE design renders           → look at them
3. UE import/update (headless python)    → no errors in log
4. UE look-dev capture(s) of the subject → look at them (ACCEPTANCE VIEW)
5. UE automation tests (once they exist) → green; plus reference-Godot soak
   only while the Godot game is still the live spec for the ported system
6. Tick box → ledger → Desktop copies → commit → push
```
Animation units: capture sequences (≥8 frames or MRQ clip), review motion.
Disk check every session start (see doctrine).

---

## 5 · WORK BREAKDOWN

### PHASE 0 — UNREAL FOUNDATION & CORE PORT (new; everything else waits)
- **0.1 Project skeleton**: create `ue/Restoration` (Blueprint project,
  Forward+? No — Deferred, Lumen on, VSM on), git hygiene (.gitignore for
  Intermediate/Saved/DerivedDataCache/Binaries), first headless launch
  proven, disk audit.
- **0.2 Automation loop proven**: `ue/pyscripts/` — headless import script,
  material-fixup script, capture script (MRQ or HighResShot), log-grep
  helpers. Exit criteria: one command imports a test mesh and produces a
  capture PNG unattended.
- **0.3 Chum head into UE**: export `chum_af.glb` → import → material fixup
  (bakes wired, fur cards masked+two-sided, MawBlack unlit, lens PBR) →
  look-dev level v1 (Lumen, three-point rig, fog) → capture vs plate.
  **This capture is the new acceptance baseline.**
- **0.4 Quixel/Fab hookup**: owner signs into Epic/Fab once; pull a starter
  set of studio-relevant Megascans surfaces; document the import path.
- **0.5 Player port**: first-person controller + interaction trace + HUD
  shell (Blueprint), parity with `player.gd` feel (sens, speeds).
- **0.6 Studio blockout import**: export world_builder geometry (or rebuild
  greybox from its coordinates) so there's a place to walk; collision.
- **0.7 Chum actor port**: rig import, `rundown.gd` brain → Behavior Tree +
  anim blueprint (gait/strike/fold/head-track/tally states).
- **0.8 Systems port**: saves, doors/interactables, inventory/notes — per
  the reference scripts.
- **0.9 Test harness**: UE automation tests encoding I01/I02/I22/I06 +
  soak-style bot wander map test; wire into the loop.
- **0.10 PHASE GATE — PARITY SLICE**: one full room playable in UE with
  Chum encounter, saves, and tests green, captured and reviewed. Only now
  does Godot stop being the live spec (it stays in-repo as archive).

### PHASE 1 — AFTER-FIRE CHUM (Blender factory → UE acceptance)
1.1 Torso (quilt/patches/char, 2048 bakes) · 1.2 Throat speaker (donor
speaker asset) · 1.3 Collar & dead bell · 1.4 Arms & articulated hands ·
1.5 Legs & control rods · 1.6 Tail · 1.7 Full-figure unification + budget ·
1.8 Head realism retrofit per §R (staples→maps, sculpted teeth, beveled
metals, fur density) · 1.9 Gait anim (UE anim BP) · 1.10 Strike/fold ·
1.11 Jaw+lever sync · 1.12 Secondary motion & tally states · 1.13 GATE:
gallery + long soak test.

### PHASE 2 — THE CAST
2.1 Human pipeline v2 (Blender template; consider MetaHuman for the humans
— evaluate in-unit, the puppet cast may not suit it) · 2.2–2.6 Merle /
Harriet / Vess / Leland / Rita+manager · 2.7 1974 Chum · 2.8 1971 pilot ·
2.9 Cast anim sets · 2.10 GATE lineup.

### PHASE 3 — THE STUDIO (rooms & props)
3.0 ENUMERATE rooms from `world_builder.gd` + canon docs into boxes. Per
room: Megascans surfaces, Fab/PolyHaven props (wear pass), bespoke set
pieces from the Blender factory, Lumen lighting pass, collision/nav,
capture review. 3.FINAL GATE: full-studio walkthrough captures + soaks.

### PHASE 4 — PUZZLES & FUNCTIONALITY
4.0 ENUMERATE from the 13 canon docs. Per mechanic: port/implement →
diegetic feedback → fail-forward integration → automation test. Plus:
save integrity, encounter choreography per room, premiere finale sequence.

### PHASE 5 — POLISH
5.1 Audio bed & foley on anim events (MetaSounds) · 5.2 UI/menus/
accessibility · 5.3 Post & atmosphere per room · 5.4 Performance: 60fps on
M1 Pro (scalability tuning, Nanite where it helps, texture budgets) ·
5.5 Packaging: macOS build, 60-min packaged soak.

### PHASE 6 — FINAL GATES
All boxes checked · packaged-build soaks clean · full playthrough capture
review · credits complete (art/audio/Fab) · owner sign-off.

---

## 6 · WHEN THINGS GO WRONG
Regression = the unit. Two failed attempts at an approach = post-mortem in
the ledger, switch technique. Can't source an asset after two searches =
build it. Disk under 8GB = cleanup unit. NEVER leave the repo un-runnable;
Blender scripts are deterministic and the UE project must always open.
