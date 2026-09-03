# RESTORATION · AAA BUILD PLAN

**The charter for the recurring build routine.** Every session that opens this
repo to do build work MUST read this file and `PROGRESS.md` first, do exactly
one unit of work (two only if the first comes up trivially green), verify it
through the full check loop, mark it off, and leave the repo green. The game is
done when every box in `PROGRESS.md` is checked and the Phase 6 exit gates pass.

Mission: take the fully-coded game in this repo from greybox-with-a-hero-head
to a smooth, cohesive, AAA-looking horror experience — piece by piece, asset
by asset, verified at every step. Order of campaign: **Chum → the rest of the
cast → every room and prop in the studio → puzzle & game functionality →
polish, audio, performance, packaging.**

---

## 0 · SESSION PROTOCOL (read this, then work)

1. `git status` if repo is a git repo, else check `README.md` tail — confirm
   the last session left things green. If something is broken, FIXING IT IS
   THE UNIT. Never build on red.
2. Open `PROGRESS.md`. Find the first unchecked box in the earliest unfinished
   phase. That is the unit. Do not skip ahead; do not gold-plate finished units.
3. Work the unit using the doctrine (§1), the asset policy (§2), and the
   pipeline (§3).
4. Run the FULL verification loop (§4). A unit is not done until every
   applicable check passes AND the images have actually been looked at.
5. Close out: tick the box in `PROGRESS.md`, append a commit-style entry to
   `README.md` (what, why, what broke, what's proven), copy current renders to
   `~/Desktop/chum-head-current.png` / `chum-ingame-current.png` (or the
   subject-appropriate names), then `git add -A && git commit` (message = the
   unit name + one-line result) and `git push` to
   `https://github.com/Quasar-Apps-Agent/chum` (auth is in the keychain).
   Small, verified, shippable increments beat heroic half-done rewrites.

Session budget: ONE unit. If a unit turns out to be >2 hours of work, split it
into sub-boxes in `PROGRESS.md`, finish the first sub-box, and stop clean.

---

## 1 · DOCTRINE (paid for in blood — do not relearn these)

**Views & verification**
- There is ONE model per subject (e.g. `blend/chum_af.blend`) and THREE honest
  views: Cycles beauty (`tools/render_chum_af_beauty.py`), EEVEE bench check,
  and the real-renderer Godot capture (`--write-movie`, WITHOUT `--headless` —
  headless uses the dummy renderer and crashes on texture reads). Judge in all
  three. The user works in the Blender APP — what File→Open shows matters:
  save .blends with Material Preview shading + relationship lines off.
- **Measure the texel, not the render.** When a surface "renders wrong," raycast
  it (`scene.ray_cast` from the camera) and sample the actual baked pixels via
  UV lookup before touching materials. Three multiplier "fixes" once chased a
  lighting problem.
- AgX + hot lights desaturate dark albedos to grey. If it looks washed out,
  check the light rig before the material. The plate look is a DIM portrait.
- Blender on Metal occasionally SIGABRTs mid-render. Retry once before
  investigating anything.

**Geometry & materials**
- Author colors in sRGB and convert with `srgb_to_linear()` — glTF
  baseColorFactor is linear. This bug has bitten at least three times.
- NEVER shrinkwrap a thin plane/shell onto geometry and bake or rely on it —
  it collapses into slivers (the "giraffe artifact"). Panels and patches are
  SOLID remeshed geometry.
- Cycles' Principled has a ~4% specular floor: near-black + close light = grey.
  Lightproof black = zero-strength Emission (`void_black`) in Cycles, and the
  game paints any `MawBlack`-named surface unshaded black in
  `scripts/character_kit.gd` (glTF exports emission-black with a WHITE base).
- Bake pipeline: `organic()` remesh → smart UV → scan-based Cycles nodes →
  bake DIFFUSE(COLOR)/NORMAL/ROUGHNESS → simple Principled with baked maps.
  **Pack every generated image** (`img.pack()`) or reopening loses the bakes.
- Principled Hair BSDF needs `parametrization="MELANIN"` — Color input alone
  renders blond.
- Every directory that ever contains a `.blend` inside the project tree gets a
  `.gdignore` (`blend/`, `tools/texsrc/`, `tools/modelsrc/`) or the Godot
  importer hangs for minutes.
- Fur: particle hair lives IN the .blend (grown post-bake — `bake_all()`
  clears material slots) for viewport/Cycles; the GAME gets textured fur
  CARDS wearing `tools/texsrc/fur_tuft_atlas.png` (regenerate with
  `tools/make_fur_cards.py`). glTF ignores particle hair — that's the design.
- Metals/leathers get `scan_dress()` (box-projected scan × tint multiply).
  Watch the value multiplier: 2.2 turned the mouth grille into cream pickets;
  shadow-machinery parts want ~0.7.

**Game contract (do not break; verify after every model change)**
- `chum_af.glb` must contain nodes `Head` and `Jaw`; `rundown.gd` finds gait
  pivots by name (`_hip_l/_hip_r/_shoulder_l/_shoulder_r/_tail_pivot`).
- Runtime tally dot: head-local `(0.13, 0.06, 0.39)` r≈0.027 (rundown.gd +
  head_preview.gd). If the lens moves, move the dot.
- BASE_HEIGHT 2.6 / AF_HEIGHT 3.35; rig scaled by rundown.gd.
- Coordinates: Blender Z-up/−Y-front → Godot Y-up/+Z-front; head-local Godot
  z = −(Blender y).
- Character kit passthrough: materials WITH albedo textures pass through;
  bare wool/patch names get triplanar fabric; `MawBlack` goes unshaded black.

**Checks that gate everything**
- `Godot --headless --import` → 0 errors.
- Fail-bot soak: `Godot --headless res://scenes/soak.tscn -- --bot=fail
  --minutes=2` → I01/I02/I22/I06 PASS. Longer wanderer/checker soaks at phase
  gates.
- Real-renderer capture for anything visual:
  `Godot res://scenes/head_preview.tscn --write-movie renders/x.png
  --fixed-fps 30 --quit-after 3` (build a preview scene per subject as needed).
- For ANIMATION units: capture 60–120 frames (`--quit-after N`), read several
  spread across the motion, and judge arcs/timing/contact like a reviewer —
  smooth ease-in/out, no pops, no foot-slide, secondary motion follows through.

---

## 2 · ASSET POLICY (use the world's assets; never build what exists)

- **Sources (all CC0, no auth):** Poly Haven (`api.polyhaven.com` — models,
  HDRIs, textures), AmbientCG (`ambientcg.com` — needs a User-Agent header,
  e.g. `curl -A "restoration-build/1.0"`). Model downloads: prefer the
  `.blend` @1k with its texture includes into `tools/modelsrc/<Asset>/`.
- Every import gets: a line in `tools/texsrc/CREDITS.md`; textures packed;
  a **soot/wear pass** (multiply toward char, roughness up) so nothing looks
  showroom-new — this also kills any legible donor branding (the lens
  engraving precedent); scale/orientation fitted in the build script so
  rebuilds are deterministic. Cut donors down with bmesh by material index
  (the Camera_01 → TallyLens precedent).
- Search the library FIRST for: speakers, radios, bells, clocks, lamps, tools,
  furniture, crates, cables, pipes, doors, switches, tape machines, chairs,
  desks, kitchenware. Build procedurally only what cannot be sourced (the
  puppets themselves, bespoke set pieces).
- Audio (Phase 6): freesound.org CC0 and sonniss GDC packs; credit everything
  in `assets/audio/CREDITS.md`.
- License rule: CC0 only. No CC-BY unless the user approves the attribution;
  nothing NC/ND; no ripped game assets, ever.

---

## 3 · PIPELINE MAP (what exists; extend, don't fork)

- `tools/build_chum_af.py` — the After-Fire Chum build (geometry, materials,
  bakes, fur cards, in-file hair, viewport prefs, glb + blend export). The
  template for all character builds.
- `tools/render_chum_af_beauty.py` — Cycles design renders (head / ears /
  full). Clone per subject.
- `tools/make_fur_cards.py` — fur tuft atlas generator.
- `tools/debug_face.py` — albedo-emission debug render (the forensic tool).
- `scripts/character_kit.gd` — glb loaders + procedural humans;
  `scripts/rundown.gd` — Chum AI + procedural animation brain;
  `scripts/world_builder.gd` — the whole greybox studio;
  `scripts/prop_kit.gd` — prop builders with scan-textured `_pbr()`.
- `scenes/head_preview.tscn`, `arm_preview`, `cast_preview` — capture rigs.
- `scenes/soak.tscn` — invariant soak harness (bots: wanderer/checker/fail).
- `README.md` — the commit ledger. Every session appends its entry.

---

## 4 · THE VERIFICATION LOOP (run at the end of every unit)

```
1. Rebuild the touched build script(s)            → "WROTE" with no Traceback
2. Cycles beauty render(s) of the subject         → look at the image(s)
3. EEVEE bench render                              → look (this is the user's app view)
4. Godot --headless --import                       → 0 errors
5. Real-renderer capture (stills or anim frames)   → look
6. Fail-bot 2-min soak                             → I01/I02/I22/I06 PASS
7. PROGRESS.md tick + README ledger + Desktop copies
```
Animation units add: frame-sequence review (≥4 frames across the motion) and,
at phase gates, a 30-minute wanderer soak.

---

## 5 · WORK BREAKDOWN (the campaign — boxes live in PROGRESS.md)

### PHASE 1 — AFTER-FIRE CHUM, COMPLETE & FULLY ANIMATED
The hero. The head is done (Commits 060–072). Remaining: the body at head
tier, then the full animation set.
- **1.1 Torso**: quilted patchwork per the plate (rust chest, green side, tan
  belly circle, plum/blue remnants as burnt versions), seam staples, char
  zones; bake at 2048.
- **1.2 Throat speaker** (dossier detail 2): source a real vintage
  speaker/radio model, cut the driver, mount it in the chest with a grille
  and cable runs to the jaw.
- **1.3 Collar & bell**: leather collar strap (Leather030), sourced or built
  brass keyhole bell, hung dead (it never rings).
- **1.4 Arms & hands**: exposed tendon cables (dossier detail 3) on BOTH arms
  (left is already dense), articulated 3-finger+thumb hands with rod
  knuckles, claw tips; fur cards + hair to wrists.
- **1.5 Legs** (dossier detail 5): internal control rods knee-to-ankle
  visible through torn fur windows, weighted foot bases, toe caps.
- **1.6 Tail**: segmented rod core, fur cards + hair, rust tip.
- **1.7 Full-figure pass**: proportion check vs the 11-ft plate, silhouette
  low-angle render, tone unification, glb size budget (≤80 MB; WebP-compress
  bakes if over).
- **1.8 Gait animation**: rework `rundown.gd` walk — weight shift onto the
  planted foot, hip drop, shoulder counter-rotation, head bob with lag. Judge
  from 90-frame captures, three angles.
- **1.9 Strike & fold**: anticipation crouch, fast strike, recovery; fold-up
  idle per canon. No pose pops.
- **1.10 Jaw & lever sync**: jaw motion driven with the visible mouth lever
  arm movement; teeth/lip staples ride correctly (parented to jaw ✓).
- **1.11 Secondary motion**: ear micro-sway, tail follow-through, whisker
  jitter on head turns, tally-eye brightness flicker states (idle/tracking/
  hunting) wired to AI states.
- **1.12 PHASE GATE**: 30-min wanderer soak + full check loop + a 10-shot
  render gallery (`docs/telemetry/gallery-chum/`) reviewed image by image.

### PHASE 2 — THE REST OF THE CAST
Plates in `docs/canon/art/`. Upgrade the shared human pipeline once, then per
character. Each character = model unit + animation unit.
- **2.1 Human pipeline v2**: one build-script template (`tools/build_human.py`)
  with: sculpted head (remesh + displacement from reference proportions),
  particle-hair grooms per style, scan-dressed clothing (AmbientCG fabrics),
  fur-card technique reused for hair cards in-game, baked 1024 textures,
  shared armature-free pivot contract matching `character_kit.gd` poses.
- **2.2–2.6 Per plate**: Merle Cottry · Harriet · Vess Keys · Leland Merrick ·
  Rita Ivori (+ floor manager variant). Each: build vs plate → three-view
  verify → cast_preview capture → kit hookup.
- **2.7 1974 Chum**: apply the AF pipeline (bakes, fur cards, hair, real-asset
  amber eye/bell) to `build_chum_1974.py` — pristine, loved, clean.
- **2.8 1971 pilot Chum**: same treatment, rougher build per canon.
- **2.9 Cast animation set**: idle/walk/talk gestures per character via the
  kit's pose system; blink/head-track where faces allow.
- **2.10 PHASE GATE**: cast_preview lineup render + captures reviewed; soaks.

### PHASE 3 — THE STUDIO: ROOMS & PROPS
First session of this phase: read `scripts/world_builder.gd` + the canon
docs, enumerate EVERY room/zone into `PROGRESS.md` as its own box, then work
them one per session. Per-room unit template:
- Replace greybox surfaces with scan materials (AmbientCG: floors, walls,
  ceiling tiles, carpets); check tiling scale at player height.
- Source props from Poly Haven (desks, chairs, lamps, crates, tape machines,
  cables…) into `prop_kit.gd` loaders; soot/wear pass; bespoke props built
  procedurally only where sourcing fails.
- Lighting pass per room: motivated practicals, horror-dim, tally-red
  accents; player-path readability check from actual gameplay captures.
- Collision/nav verify (walk the room with the wanderer bot), then the loop.
Known majors from the docs (verify against world_builder at enumeration):
lobby, stage floors, corridor ring, workshop/repair bay, archives, control
booth, break room, storage, basement/service, the shrine wall (Vess),
premiere spaces. **3.FINAL PHASE GATE**: full-studio walkthrough capture set
+ 30-min soaks on all three bots.

### PHASE 4 — PUZZLES & GAME FUNCTIONALITY
Source of truth: the 13 canon design docs. First session: extract the full
puzzle/mechanic list into `PROGRESS.md`. Per unit: implement/upgrade the
mechanic → interactable polish (prompts, feedback, diegetic UI) → failure
states feed the fail-forward system (I06) → soak with the checker bot →
invariant added to the harness if the mechanic is load-bearing.
Includes: save/load integrity (v16+ format), difficulty/pacing tuning passes,
Chum encounter choreography per room, scripted premiere finale sequence.

### PHASE 5 — SIXTH SENSE: AUDIO, UI, POST, PERFORMANCE
- **5.1 Audio bed**: CC0 ambience per room, Chum servo/cloth/bell foley tied
  to animation events, adaptive tension layers driven by AI state, premiere
  cue. Mix pass with captures.
- **5.2 UI/UX**: diegetic-first HUD polish, menus (main/pause/settings with
  audio+sensitivity+accessibility), readable interaction prompts, no physical
  text blocking the camera (regression-tested — this was a launch complaint).
- **5.3 Post & atmosphere**: film grain, vignette, fog volumes, tonemap
  tuning per room, tally-red grade moments.
- **5.4 Performance**: 60fps target on this Mac — draw-call audit, fur-card
  LODs, texture budget (WebP), occlusion, soak with FPS logging invariant.
- **5.5 Packaging**: export presets (macOS at minimum), icon, first-run flow,
  crash-free 60-min soak on the packaged build.

### PHASE 6 — FINAL GATES (100% definition)
- [ ] Every box above checked.
- [ ] 60-min soaks, all bots, packaged build: all invariants PASS, zero
      script errors in logs.
- [ ] Full-game capture playthrough reviewed scene by scene for visual bar.
- [ ] CREDITS complete (art + audio). README ledger tells the whole story.
- [ ] The user has said the word: shipped.

---

## 6 · WHEN THINGS GO WRONG
- Regression found mid-unit → fixing it becomes the unit; ledger it honestly.
- An approach fails twice → stop, write the post-mortem in the ledger, pick a
  different technique (the box-lips → curve-lips precedent).
- Asset can't be sourced after two searches → build it procedurally, note it.
- NEVER leave the repo failing import or soak at session end. If out of time,
  revert the unit's changes (build scripts are deterministic — the previous
  state is one rebuild away) and log what happened.
