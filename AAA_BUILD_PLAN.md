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
7. **Crafted, not photoreal** (the art bible's law, market-validated per the
   comparative study): the bar is MATERIAL TRUTH on crafted objects — wool
   that reads as wool under sodium, wear that reads as history — not skin
   pores. Damage reads as history, and history is scarier than teeth.
   Fidelity serves the puppet-and-practical world; photoreal humans are not
   the goal, lying materials are the defect.

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

**Unreal side — STANDARDS ARE CANON: `docs/canon/restoration-blender-ue5-pipeline.md`**
- Engine: UE 5.8 at `/Users/Shared/Epic Games/UE_5.8`; editor CLI:
  `Engine/Binaries/Mac/UnrealEditor-Cmd "<uproject>" ...`. Project:
  `ue/Restoration/Restoration.uproject`.
- Machine is M1 Pro / 16GB / ~18GB free disk: caches capped, generated dirs
  gitignored; below 8GB free, cleanup IS the unit.
- **Export: FBX with the UE preset** — Blender meters → 1m = 100uu; UE is
  X-forward Z-up. Verify ONCE on a 1m cube and record the result in the
  ledger. Naming law: `SM_`/`SK_` meshes, `M_`/`MI_` materials, `T_*_BC/_N/
  _ORM` textures; collision as `UCX_` children in Blender (auto-import);
  sockets `SOCKET_JawLever`, `SOCKET_EyeTally`, `SOCKET_Bell` (clapperless).
- **Textures ORM-packed; 2K default, 4K only Chum + readables.** LOD1 for
  set dressing only; hero props none (crafted-world polycounts are modest).
- **Material masters** (parents in UE): `M_Wool` (subsurface, sodium-honest),
  `M_TapeStock`, `M_Phosphor` (monitors), `M_Paper`, `M_Enamel`,
  `M_Practical` (fixture glass). MawBlack → unlit black; fur cards →
  two-sided masked.
- **THE SODIUM CHECK**: a permanent Blender lookdev scene (one
  sodium-spectrum lamp, neutral floor). Every material passes through before
  export; if it lies under sodium it does not ship.
- **Data-driven world**: rooms/doors/timings come from the port kit's CSVs —
  the level is BUILT FROM DATA in UE exactly as in Godot; the import
  automation enforces naming so the pipeline complains, not the artist.
- Automation loop: Editor Python (`-run=pythonscript`), MRQ/HighResShot for
  captures, `-ExecCmds="Automation RunTests"` — all headless. First runs
  compile shaders: SLOW; don't kill young processes.
- Gameplay: Blueprints for visual/simple, C++ for systemic; TRANSLATE the
  proven GDScript reference, don't redesign.
- Binary `.uasset` → git LFS for `ue/Restoration/Content` (set up when the
  first .uasset lands; decision recorded per pipeline doc).

**Lighting law — CANON: `docs/canon/restoration-lighting-bible.md`**
- Colors are contracts: RED = watched = SAFE (the inversion is the
  language); phosphor green = information, never room light; amber tungsten
  = warmth; SODIUM = the truth light (scene dock). Dark is a room, not a
  wall — silhouettes always resolve; never buy fear with unreadability.
- Lumen GI software tier; virtual shadow maps; **auto-exposure OFF, locked
  EV per room-state, transitions CUT with the schedule**; volumetrics low
  and motivated. Practicals authored in Blender with TRUE BULB GEOMETRY so
  Lumen bounces honestly. Per-day color script via post volumes (Day 1
  warmest → Day 5 coolest) over unchanged practicals.
- His eye is the game's only mobile red; HIS SHADOW IS A MECHANIC (3.35m —
  the fold announces by silhouette through doorways).

**Design law — CANON: dread doctrine, lore architecture, comparative study**
- The dread stack L1–L5 and the VIOLATION BUDGET (one startle, one
  interface lie, one once-ever sight — the budget never grows). Any new
  creep passes the three tests: repetition, law, earned.
- BANNED: random scares, musical stings, darkness-as-content, enemy
  quantity, gore-for-volume, jumpscare kill-loop retention, randomized
  anomalies, co-op, procedural levels, any text containing "creepy".
- Lore: the game never explains, it corroborates (shard model, three reads
  rule, never-stated ledger — naming a ledger truth in text is an S0
  defect). Consequence is exposition.

**Motion & sound law — CANON: `restoration-chum-motion-and-sound.md`**
- PRE-FIRE Chum = the operated body: full puppet grammar (anticipation,
  overshoot, settle, secondary everywhere, 15° head-tilt stops, jaw a
  half-beat off phonemes). In-game the stage body never animates (L1 drift
  only). All pre-fire sound is band-limited (≈50Hz–8kHz, tape wow).
- AFTER-FIRE Chum = the unoperated body: puppet grammar DELETED. No
  anticipation, no overshoot, no settle, NO SECONDARY MOTION EVER. He POURS
  (single-axis, head leads, linear-dominant curves with ≤2-frame ease caps)
  or he is PARKED (statue-still, zero idle sway, no breathing) while the eye
  alone tracks, servo-smooth. He faces PATHS, not people.
- Three authored exceptions only: THE FOLD (2.2s doorway montage — shoulder
  first, head late on an impossible hinge), THE WITHDRAWAL (reverse along
  the exact approach path, motion played backward), THE PERFORMANCE QUOTE
  (at 1.2m under a burning tally: fully frontal broadcast stance + one clean
  15° head tilt — the tally turns him back into a performer).
- HARD RULES: the jaw NEVER opens. The bell NEVER sounds (clapperless). NO
  vocalizations — no growl, no breath. Timings as built: 0.8 m/s approach,
  1.2m loom, 2.0s cool, 2.2s fold, 1.6 m/s crossing.
- AUDIO LAW: band-limited is memory, full-range is present; his sounds are
  wrong sources doing honest labor (wood-through-floor sub footfall,
  wet-felt groan, hull-tick armature — never servo-whine); under 3m he
  OCCLUDES the room (reverb ducks, 200Hz bloom); the strike is nearly
  silent. Rig note: AF rig ships with physics secondaries DISABLED, wool
  baked stiff, root-motion clips, fold as authored montage per door width,
  eye on its own always-on track layer.
- CAPTURE CANON: After-Fire renders/captures pose the jaw SHUT (current
  beauty/preview jaw-open poses are canon-wrong; fix at next asset touch).

**Interaction & systems law — controls map, accessibility matrix, reaction
matrix (all in docs/canon/)**: stable inputs, holds mean commitment, real
binding glyphs; accessibility never breaks canon (dark readable by doctrine,
the one startle disclosable, safety never color alone); THE WEB LAW — every
significant player action echoes in ≥2 systems or people, in character, at
the right time.

**Object taxonomy law — `restoration-object-taxonomy.md`**: three tiers as
promises — INTERACTABLES carry verbs, never drift, never lie (affordance is
diegetic wear, not outlines; one hero interactable per room max); LORE
carries shards (handled lore prompts; AMBIENT LORE NEVER PROMPTS); DRESSING
is the only drift-eligible tier and earns its place by biography. No fake
affordances, ever. QA-55/56/57 sweep every room.

**The doctrine library**: `docs/production/` holds the full production
canon (art bible, audio bible, invariant suite, QA regression, gap audit
with RULINGS — sprint: none; crouch: body verb c045; binder IS the
inventory; assist-only difficulty — plus Steam/trailer/demo/ARG plans).
Consult the gap audit's rulings before re-deciding anything.

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
metals, fur density; jaw posed SHUT per motion canon) · 1.9 The POUR
(locomotion per motion doctrine: linear curves, head-leads arc, absolute
stops, parked-statue idle, servo eye layer) · 1.10 The FOLD + THE
WITHDRAWAL (2.2s doorway montage per door width; reverse-path retreat) ·
1.11 THE PERFORMANCE QUOTE (1.2m loom: frontal square-up + the one 15°
tilt, tally-synced) · 1.12 Tally states & eye tracking wired to AI ·
1.13 GATE: gallery + long soak test.

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
4.0 ENUMERATE from the canon docs. Per mechanic: port/implement → diegetic
feedback → fail-forward integration → automation test. Plus: save
integrity, encounter choreography per room, premiere finale sequence.
**Study adoptions (canon)**: QA-51 BRAID AUDIT — at every pressure peak, at
least two simultaneous attention demands (braid, never queue); PER-DAY
VERB-TEXTURE AUDIT — each day owns a mechanical texture per the dread
curve; a day without one is a defect.

### PHASE 5 — POLISH
5.1 Audio bed & foley on anim events (MetaSounds; silence-as-event law) ·
5.2 UI/menus/accessibility · 5.3 Post & atmosphere per room (per-day color
script volumes) · 5.4 Performance: 60fps on M1 Pro · 5.5 Packaging: macOS
build, 60-min packaged soak · **5.6 STREAMER MODE** (study A1:
compression-kind grain, overlay-safe HUD margins, capture-clean toggle) ·
**5.7 CLIP LEDGER pass** (study A4: the named clippables — first doorway
fold, THE TALLY COOLS, SAFE WHILE LIT countdown, the bell, the WARNING
page, Harriet doubled, THE LEDGER read aloud — each verified capturable in
≤30s with one legible frame) · **5.8 DEMO — TAPE 1** (study A6: the funnel).

### PHASE 6 — FINAL GATES
All boxes checked · packaged-build soaks clean · full playthrough capture
review · credits complete (art/audio/Fab) · **fan-content policy drafted
(study A5, generous, Fanverse-shaped)** · owner sign-off.

---

## 6 · WHEN THINGS GO WRONG
Regression = the unit. Two failed attempts at an approach = post-mortem in
the ledger, switch technique. Can't source an asset after two searches =
build it. Disk under 8GB = cleanup unit. NEVER leave the repo un-runnable;
Blender scripts are deterministic and the UE project must always open.
