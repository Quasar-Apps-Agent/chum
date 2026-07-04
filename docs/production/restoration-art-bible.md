# RESTORATION · ART BIBLE v1
Authority chain: the four Chum reference plates are ground truth; the design doc Part II owns Chum's base design, era table, and the nine-delta post-fire set (cited here, never duplicated); this bible owns everything else visual. Engine color values in v0.7 are the palette's provisional hexes and are listed here as canon until repainted.

## 1 · THE CRAFTED WORLD DOCTRINE
One law: everything in this world was made by hand, at one-to-one scale, by people who cared. Rooms are built sets. Humans are needle-felt and cloth figures over armature. Props are painted plywood, real brass, real glass. This is craft realism, not stylization: stitches read as stitches, fibers catch light as fibers, glue is where glue would be. The uncanny is never achieved by distorting the craft; it is achieved by the craft being too careful in places nobody should have cared about. If a surface looks digital, it is wrong. If it looks mass-produced, it is wrong. If it looks loved, it is right, and that includes the things that should frighten you.

## 2 · THE TWO-WORLDS CONTRAST LAW
The compound and the tape world share one material language. The contrast between them is delivered exclusively by lighting and by the artifact pipeline. Consequences: no separate art style for tape content; no grain, chroma error, or scanline may ever appear on compound surfaces (grain belongs to tape only); no tape image may ever appear clean except the anomaly slates, which are authored one at a time. Footage is always shot or rendered clean and degraded live in the shader ladder; artifacts are never baked into masters. Photosensitivity-safe mode must preserve the two-worlds read while suppressing bands, flicker, and crawl (engine parity already exists; art must not reintroduce risk via authored flashes).

## 3 · MATERIAL SYSTEM · SCAN FIRST
Fabricate a physical swatch library, then capture it: wools (Chum brown plus five compound wools), felts (dead-room gray, set greens), flannels including the school-gray that ties patch seven to the 1974 clipping, corduroy, aged brass, glass (amber eye stock), painted plywood in three wear states, mimeograph and newsprint papers. Photogrammetry or photometric stereo per swatch into tiling PBR sets with clean, worn, and loved wear states. The wool spike shader is the interim standard for all fiber surfaces; it retires per surface only when its scanned replacement passes the sodium test (Section 10). Nothing ships on a procedural fiber that a scan could carry.

## 4 · PALETTE SYSTEM
Compound neutrals: ash #6B6862, dust #7F7A70, slate #5C5C61, oat #756E66, fog #666B6B. Show palette (the Gladhouse's colors): MUSTARD #C9A33D, AVOCADO #6B7D3B, BURNT #B35A2B. Supporting canon: phosphor #D9EDC4 (UI, tags, title), paper #DED4B8, ledger green #596B52, warning red #C23A2E used only for slates, tallies, and the breaker.
THE DRIFT LAW: environments and wardrobe interpolate from neutrals toward the show palette on the coat-peg curve (day-driven, lockdown-boosted; the engine's CoatPegs drift function is the canonical curve). Set dressing drifts through replaced small props first (a mustard tea towel on Day 2), textiles second, wall tones never (walls hold neutral so the drift reads on things people chose).

## 5 · CASTING-DRIFT WARDROBE RULES (per character)
MERLE: begins already warm (mustard apron from Day 1) and never drifts, because she was carried in 1974 and has nothing left to drift toward; her constancy is the tell hiding in plain sight. HARRIET: drifts on the curve exactly, the control subject. VESS: resists longest; neutrals through Day 4, and his only show-palette object is the plastic pin he has always carried, which is the other tell; if he credits and is credited, he adds one avocado scarf for the premiere, chosen, not drifted. EXTRAS AND PEGS: lead the curve by half a day, so the background is always slightly ahead of the people you know. FLOOR MANAGER: absolute black-adjacent neutrals forever, outside the palette system entirely, the way he is outside everything. RITA: player wardrobe never drifts; her gloves are the whitest object in the game.

## 6 · CHARACTER BUILD SPECS
Humans: needle-felt heads over wire armature, cloth bodies, mitten hands with stitched finger definition reserved for principals (Merle, Vess, Harriet). Head-to-body one to five and a half. EYE HIERARCHY, a hard law: human figures wear glass beads or embroidered eyes only; buttons are reserved for Chum. A button on a human face is an event we never spend. CHUM: per design doc Part II in full; the Understudy's on-set live build is dimensionally identical to Chum plus four percent overall scale, an error the eye reports as distance being wrong rather than size being wrong. The post-fire build follows the nine-delta set exactly; fabricators receive the tell-table, not adjectives.

## 7 · HERO ROOMS (render order: BEN, REC, STA, DR, DOCK)
BENCH: the altar. Paper stock and ledger green dominate; one warm task lamp; the monitor is the room's only saturated light; the asset rack reads amber against dust.
REC ROOM: the heart. Warmest neutrals, the shrine's glass, chairs in their casual arrangement (the plate is shot pre-lockdown; a second plate in rows is the pair that sells the game).
STUDIO A: the stage. Tungsten wash on the set island, catwalk darkness above with one practical; the little door lit like a prop that knows it is one.
DEAD ROOM: flat, shadowless, felt-swallowed; the radio's dial is the only specular object; palette entirely fog and slate.
DOCK: rows two deep, years in order; cold north light through high glass; the units' wools graying left to right by era; the clipboard's paper the brightest value in frame.

## 8 · LIGHTING DOCTRINE
Day: overcast north key plus warm tungsten practicals; nothing pretty, everything kind. Night: sodium exterior spill at the windows (the wool verdict's test light), phosphor monitor glow as interior key, pools with honest falloff. The cascade: darkness is absence, never blue; restored circuits return light in the panel's order. Premiere: full tungsten stage wash, the one gorgeous image in the game, because the trap should be beautiful. Dead room: no key at all.

## 9 · CAMERA, POST, UI
In-world eye: 24 mm equivalent, mild breathing on focus, no depth-of-field cinematics outside authored scenes. Compound post: none; color is achieved in light and material. Tape post: owned entirely by the artifact ladder. UI art: the WGLD binder specimen is source of truth (phosphor CRT title, form stock, cue-sign faces); print props follow the props packet's stock specs.

## 10 · DELIVERABLES AND THE GATE
P0: swatch library fabricated and scanned; Chum base build contract (the puppet is also the trailer, per the build plan); BEN and REC dressing kits; the five hero plates. P1: STA, DR, DOCK kits; principal character builds, Merle first; drift prop sets per day. P2: extras, exterior, premiere dressing.
ACCEPTANCE, THE SODIUM TEST: every fiber material is judged as a physical sample photographed under a sodium lamp beside its render under the same light. If a blind viewer cannot reliably pick the render, it passes. This is verdict V1 from the playtest protocol, promoted to the material gate for the whole game.
