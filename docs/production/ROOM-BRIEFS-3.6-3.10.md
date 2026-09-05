# RESTORATION · ROOM BRIEFS 3.6–3.10 (SHED · CORRIDOR · TAPE LIBRARY · BENCH ROOM · CLIMATE)

Executable dressing briefs for Phase 3 units 3.6–3.10, in the exact order
PROGRESS.md §PHASE 3 lists them, in the format of
docs/production/ROOM-BRIEFS-3.1-3.5.md Appendix A (copied exactly). A build
agent dresses each room in UE 5.8 from this file plus §0 of the 3.1–3.5 brief.
Every canon claim carries a citation `[doc §section]`; where the canon gives no
number the cell says **OPEN**. Nothing here invents canon. Where the reference
code and a canon document disagree, both are quoted and the disagreement is an
OPEN (the code is the spec for POSITIONS [docs/packet/portbrief/PORT-BRIEF.md,
cited via AAA_BUILD_PLAN.md §1 THE PORT KIT]; the bible's cap governs prompts
[ROOM-BRIEFS-3.1-3.5.md Appendix A rules]).

Source set read for this brief: PROGRESS.md §PHASE 3 and §CLOUD LANE BACKLOG;
docs/canon/restoration-room-bible.md; restoration-lighting-bible.md;
restoration-object-taxonomy.md; restoration-ambient-lore-ledger.md;
restoration-dread-doctrine.md; restoration-walkthrough-levels-endings.md;
restoration-game-master.md; restoration-player-routing.md;
restoration-reaction-matrix.md; restoration-casualty-ledger.md;
restoration-lore-architecture.md; restoration-comparative-study.md;
restoration-after-fire-chum.md; restoration-cast-sheets.md;
restoration-room-inventory.md; restoration-design-doc.md; docs/production/
restoration-art-bible.md; restoration-audio-bible.md;
restoration-props-packet.md; restoration-qa-regression.md;
restoration-invariant-suite.md; restoration-gap-audit.md;
docs/packet/portbrief/THE-LAWS.md; ue/Restoration/Data/{Rooms, Doors, Stations,
Monitors, DemoOpen, Timings, GameText}.csv; ue/FAB-IMPORT.md; ue/CREDITS-FAB.md;
ue/pyscripts/build_greybox.py (the stamp); ue/Restoration/Source/Restoration/
RitaCharacter.cpp; scripts/world_builder.gd + prop_kit.gd + monitor_rig.gd +
capture_bench.gd + dailies_manager.gd + degausser.gd + film_cabinet.gd +
log_station.gd + key_item.gd + gen_knob.gd + decision_ledger.gd +
credit_entry.gd + spectro_dock.gd + asset_rack.gd + seance_dock.gd +
fire_tape_dock.gd + bench_tv.gd + night_trip.gd + cascade.gd + rundown.gd +
merle.gd + glimpse.gd (the reference implementation's placements — "the code is
the spec").

---

## 0 · CONVENTIONS (inherited; read ROOM-BRIEFS-3.1-3.5.md §0 first)

### 0.1 Inherited without change
| Rule | Where it lives |
|---|---|
| Coordinate law: 1 m = 100 uu; UE (X, Y, Z) = (Godot x, Godot z, Godot y) × 100; floor top Z 0; walls 3.0 m high, 0.24 m thick, centred on the room edge; door slabs 2.6 m (greybox) vs leaf 2.2 m (reference) = **OPEN 0-A**; Rita's eye 148 uu (**OPEN 0-B** vs Godot 160); FOV **OPEN 0-C**; PlayerStart (0, 0, 160) | ROOM-BRIEFS-3.1-3.5.md §0.1; ue/pyscripts/build_greybox.py; ue/Restoration/Source/Restoration/RitaCharacter.cpp line 31 |
| Lighting grammar, states, clock (ON AIR 50.0 s / BREAK 18.0 s), technicals, fixture families, **no EV/kelvin/candela/lux exists anywhere in canon** (every EV cell below is OPEN), the stand-in lamp per room (PointLight at (cx, cy, 275), 9.0 cd, colour (0.95, 0.72, 0.45), attenuation 0.75 × max(w, d) × 100, no shadows; SkyLight 0.12), the NIGHT brown-out contradiction **OPEN 0-E**, BREAK in tally-less rooms **OPEN 0-F** | ROOM-BRIEFS-3.1-3.5.md §0.2; restoration-lighting-bible.md; build_greybox.py lines 116–126, 169–170; world_builder.gd lines 162–170, 700–709 |
| Object law: I/L/D caps, one hero per room, ambient never prompts, lore placed FIRST, drift = dressing only, QA-55/56/57; what the L cap counts = **OPEN 0-G** (this brief: handled D-series only) | ROOM-BRIEFS-3.1-3.5.md §0.3; restoration-object-taxonomy.md; restoration-qa-regression.md QA-55..57 |
| Asset and wear law, naming (`MI_<Room>_<Surface>`, `SM_`/`SK_`, `M_`/`MI_`, `T_*_BC/_N/_ORM`, `UCX_`), material masters, realism bar §R.1–7, palette, asset-id honesty (Fab entries are search terms; CC0 ids *(verify id)*) | ROOM-BRIEFS-3.1-3.5.md §0.4; AAA_BUILD_PLAN.md §1, §2, §R; ue/FAB-IMPORT.md; restoration-art-bible.md §4 |
| Pass order P0 → P7 and the capture verb "capture at (X, Y, Z) → look-at (X, Y, Z)" (HighResShot/MRQ still, Rita FOV, locked EV of the stated state, auto-exposure off, archived under docs/telemetry/ue-baselines/) | ROOM-BRIEFS-3.1-3.5.md §0.5; PROGRESS.md 0.3 |

### 0.2 Conventions added for this set
| Rule | Value | Source |
|---|---|---|
| Plan words | **−Y = deeper into the studio wing** (the corridor runs from REC at Y −400 to the library at Y −1100; the library's far wall is Y −2100); **+X = the bench/climate/transmitter side**; **−X = the fire-corridor side**; the SHED alone lies in the yard at +Y | Data/Rooms.csv |
| Room short-names for `MI_` naming | `Shed`, `Corridor`, `TapeLibrary`, `BenchRoom`, `Climate` | this brief |
| Open gaps are thresholds | Doors.csv rows with an empty `kind` stamp NO slab and spawn NO leaf, but the reference Rundown counts EVERY Doors row as a door for the 2.2 s fold (`for d in DOORS: r.doors.append(...)`), so an open 1.6 m gap costs him the fold exactly as a hinged door does | world_builder.gd lines 580–581; THE-LAWS.md 11; QA-37 |
| Camera rigs (CAM 1, CAM 2) | Each MonitorRig is a SubViewport camera at `cam_pos` looking at `look_at`, vertical FOV 65°, rendered onto a 1.6 × 1.2 m screen quad seated in a period CRT shell (bezel 0.14 m, cabinet ≈ 1.88 × 1.48 m, depth ≈ 0.99 m) at `monitor_pos` with `yaw_rad`; killed/unpowered screens read NO SIGNAL or KILLED · RE-PATCH AT PB. Godot yaw 0 faces −z (UE −Y); yaw π faces +z (UE +Y). **No tally lamp exists on the rig in the reference** | scripts/monitor_rig.gd lines 21–68, 94–106; scripts/prop_kit.gd `crt_shell` lines 179–211; Data/Monitors.csv; Data/GameText.csv lines 509–510 |
| Dock bodies | Every dock (`_dock_body`) is a 0.45 × 0.4 × 0.45 m cased body on a 0.55 × 0.07 plinth with a wood rim and a brass plaque, centred at the spawn height; a dock spawned at Godot y 0.9 has its plinth bottom at 0.63 m above the floor **with nothing under it** | world_builder.gd lines 929–972 |
| Rundown anchors | A segment's home is its ROOM CENTRE from Rooms.csv (`_anchor` → (center_x, 0, center_z)); STORY CORNER's home is TAPE LIBRARY | scripts/rundown.gd lines 8–12, 350–354 |

### 0.3 New global OPENs raised by this set (owner rulings; consolidated in Appendix B)
- **0-H · HE IS TALLER THAN THE WALLS.** `AF_HEIGHT` is 3.35 m [Data/Timings.csv rundown.gd AF_HEIGHT; restoration-after-fire-chum.md §THE SCALE LAW; restoration-lighting-bible.md §HIM] and `WALL_H` is 3.0 m [Data/Timings.csv world_builder.gd WALL_H; build_greybox.py WALL_H]. Neither the reference nor the stamp builds a ceiling slab; the 3.1–3.5 brief assumes ceilings at Z 300 (`MI_<Room>_Ceiling`). If P1 authors ceilings at Z 300 the After-Fire body clips every ceiling by 35 cm; the fold montage handles the 2.6 m door, not the ceiling. Ruling needed BEFORE any P1 ceiling pass in any room he enters (all five here except the shed, which he reaches only in the W3 spoiler sense). Options are the owner's: raise the ceiling plane (data), drop the body (canon change), or ceilings only where he never goes.
- **0-I · WHERE ARE THE TALLY LAMPS?** Canon: "Camera mounts + tally lamps · T2 route/read · tallies are shape-coded" [restoration-room-inventory.md §GLOBAL]; "Tally lamps (shape-coded, not just color) broadcast liveness at a glance" [restoration-design-doc.md Part IV §2]; "Tally lamps, ON AIR signs, his camera eye: red is the contract burning" [restoration-lighting-bible.md §GRAMMAR]. Reference: MonitorRig has no lamp mesh and no light [monitor_rig.gd]. The CORRIDOR (CAM 1) and TAPE LIBRARY (CAM 2) are the only two rooms in this set with a camera; whether a physical red tally lamp hangs on each mount (and dies on kill/BREAK) decides every "Red reads?" cell in §3.7.3 and §3.8.3.
- **0-J · THE DOCKS FLOAT.** In the reference every bench-room dock, the shed key and the film-cabinet-adjacent readables spawn at a working height with no table beneath (§0.2 Dock bodies). Canon puts the ledger "squared to the desk edge" [restoration-game-master.md T1.3]. The desk/table that carries each dock is not in the data; this brief proposes one per room and marks it PROPOSED.

---

## 3.6 · SHED — the yard's shadow; tools that predate everyone

### 3.6.1 IDENTITY
| Field | Value | Source |
|---|---|---|
| Rooms.csv | `SHED, 10.0, 14.0, 3.0, 3.0` → centre (1000, 1400), 3 × 3 m | Data/Rooms.csv |
| Floor bounds (uu) | X 850..1150, Y 1250..1550, floor top Z 0, wall top Z 300 (a 3 × 3 × 3 m box; a real garden shed is ≈ 2.2 m at the eaves — **OPEN 3.6-A**) | derived per §0.1 |
| Door → YARD | `YARD, SHED, 8.5, 14.0, 1.2, z, locked:PADLOCKED · the tag reads EDITH · a key exists\|EDITH` → gap centre (850, 1400), 1.2 m wide (Y 1340..1460) in the −X wall; slab stamped 2.6 m; **LOCKED**, reason text at (850, 1400, 290); required key `EDITH` (kitchen key board, unit 3.3); reference hinge at (850, 1340, 0) rotated π/2, leaf 1.2 × 2.2 m. Exterior threshold: 2.2 s fold toll | Data/Doors.csv; Data/GameText.csv line 655; world_builder.gd lines 242–280; THE-LAWS.md 11 |
| Other walls | +X, +Y, −Y face the yard box (the shed sits INSIDE the yard's 30 × 8 m footprint: yard Y 1000..1800 contains shed Y 1250..1550) — the shed's walls double as yard dressing (3.5 §3.5.4 SHED exterior) | Data/Rooms.csv |
| Stations / Monitors | none / none | Data/Stations.csv; Data/Monitors.csv |
| Demo | **NOT** in DemoOpen.csv (the Tape 1 demo never opens the shed) | Data/DemoOpen.csv |
| Reference placements (Godot → UE) | Shelf 0.3 × 0.04 × 2.4 m (long axis along Y) at (11.2, 1.2, 14.0) → **(1120, 1400, 120)** against the +X wall · three paint cans Ø0.16 × 0.20 at (11.2, 1.32, 13.4 / 14.0 / 14.6) → **(1120, 1340, 132), (1120, 1400, 132), (1120, 1460, 132)** · broom handle 0.04 × 1.5 × 0.04 at (8.9, 0.75, 15.1) → **(890, 1510, 75)**, leaning 0.18 rad, head 0.3 × 0.12 × 0.06 at (9.03, 0.06, 15.1) → (903, 1510, 6) in the −X/+Y corner · THE QUIET ROOM KEY (`KeyItem` id `QUIET ROOM`, display "the quiet room key · felt-wrapped", label FOR THE QUIET ROOM) at (10.0, 0.5, 14.0) → **(1000, 1400, 50)** — floating at room centre with nothing beneath it (OPEN 0-J) | world_builder.gd `_spawn_shed_interior` lines 1411–1446, `_spawn_keys` line 782, `_spawn_key` lines 785–806 |
| Stand-in lamp | reference OmniLight (1000, 1400, 275), energy 0.5, range 2.25 m; greybox PointLight (1000, 1400, 275), 9.0 cd, attenuation 225 uu — delete at P3 | world_builder.gd lines 162–170; build_greybox.py lines 116–126 |
| Adjacent | YARD only (−X door). The tower rig stands at (−900, 1450) across the yard; the beacon at ≈ (−900, 1450, 750) is visible from the open door | Data/Rooms.csv; world_builder.gd line 1234 |

### 3.6.2 ROLE
| Aspect | Canon | Source |
|---|---|---|
| Personality | "The yard's shadow; tools that predate everyone. Single bulb, pull chain." Bed: paint cans, wasp-quiet. Keynotes: padlock hasp (unlocked, always), stenciled initials gone illegible | restoration-room-bible.md SHED |
| Budget | 1 / 1 / 6; drift: the hasp's angle; web: shard site for the rebuild question (never stated) | restoration-room-bible.md SHED; PROGRESS.md 3.6 |
| Never-stated | "Who rebuilt him, and with whose hands" is on the Never-Stated Ledger; every shed item rhymes with T4 and none may state it (S0 defect) | restoration-lore-architecture.md §THE NEVER-STATED LEDGER; restoration-ambient-lore-ledger.md SHED tags [T4] |
| Dread role | L2 RITUAL AND SCHEDULE outdoors: Night 7 is the only mandated exterior night; "return before the window closes"; PATIENCE AT SCALE (the yard between you and him for W3) | restoration-dread-doctrine.md L2, AMPLIFIERS; restoration-player-routing.md Night 7 spine; restoration-walkthrough-levels-endings.md ADDENDUM SPOILER |
| Beats | T4.7 THE SHED (exterior, night, beacon pulse): PRESERVE = "the shed under the tower, Edith Craik's overflow: DEAD AIR ITEM 2: THE DEAD ROOM KEY, felt-wrapped, tagged in a boy's hand: FOR THE QUIET ROOM"; ASK = Vess trades the location for a named credit; FORCE = bolt cutters (TH tool wall) → patrol density up that night, or later drill the dead room door itself · Night 7 spine: ENT → EXT under the beacon → the tower-base shed → the dead room key → return before the window closes · W3 "exists on the shed shelf (Day 4, with him awake and the yard between you)" after W1 (library skip gap) and W2 (burn barrel); each viewing spends one S2 slip | restoration-game-master.md T4.7, Appendix B "Locked shed"; restoration-player-routing.md Night 7; restoration-walkthrough-levels-endings.md ADDENDUM SPOILER |
| Route | Reached only via the YARD (ENT → YARD → SHED); gated T4 by the EDITH key; the yard is not in the Tape 1 demo | Data/Doors.csv; Data/DemoOpen.csv; restoration-room-inventory.md §1 |
| Key text | `the quiet room key · felt-wrapped` · dock label `FOR THE QUIET ROOM` · prompt `%s · take (E)` (display upper-cased → `THE QUIET ROOM KEY · FELT-WRAPPED · take (E)`) · on pickup `TAKEN · %s`; the dead room door then reads `LOCKED · felt-faced · the hum stops at the seam` until the key turns: `The %s key turns. It was cut for this.` | Data/GameText.csv lines 679, 680, 37, 158, 656, 110; scripts/key_item.gd line 10 |
| Inventory listing | §1 EXTERIOR: "The shed · T4 · operate · Locked. PRESERVE: EDITH-tagged key from the kitchen key board. FORCE: bolt cutters (TH tool wall); raises Rundown density that night" · "Edith Craik's overflow boxes (shed) · T4 · take · Contains the DEAD ROOM KEY, felt-wrapped, tagged FOR THE QUIET ROOM; child's drawings of Chum, pre-show" — reconciled against 1/1/6 in OPEN 3.6-B | restoration-room-inventory.md §1 |
| Lock conflict | Room bible keynote "padlock hasp (unlocked, always)" vs Doors.csv `PADLOCKED` with a required key and T4.7's locked shed — **OPEN 3.6-C** (the hasp may be the INSIDE hasp of a second door, or the bible describes the post-T4 state) | restoration-room-bible.md SHED; Data/Doors.csv; restoration-game-master.md T4.7 |
| Sanctuary | none stated; the Rundown's anchors are room centres and the SHED is not a segment home, so he enters it only if a noise draws him ("RELOCATE toward heard noise") | scripts/rundown.gd lines 8–12, 171–177 |

### 3.6.3 LIGHTING STATE TABLE
| State | Locked EV | Practicals (type · position hint · colour · intensity) | Red reads? | Transition | Source |
|---|---|---|---|---|---|
| NIGHT (the canonical state; the shed is entered on Night 7) | **OPEN** | P-S1 ONE BARE BULB ON A PULL CHAIN, ceiling centre (1000, 1400, ≈285), true bulb geometry (M_Practical glass), tungsten (family word only); the chain hangs to ≈ Z 190. Default OFF until pulled — whether the pull chain is player-operable is **OPEN 3.6-D** (an operable chain is an interactable and would breach I = 1 with the key). The beacon's red enters through the open door only. "Dark is a room, not a wall": the shelf and the key must resolve with the bulb off | Tower red through the door; not a tally (OPEN 0-F) | CUT (the pull chain is itself a cut) | restoration-room-bible.md SHED; restoration-lighting-bible.md §GRAMMAR, §STATES NIGHT |
| DAY | **OPEN** — the shed has no daytime canon (the yard by day is OPEN 3.5-C); daylight through the door seam and board gaps only | none | CUT | ROOM-BRIEFS-3.1-3.5.md OPEN 3.5-C |
| BREAK / ON AIR | **OPEN** | No tally exists here; unchanged | — | — | OPEN 0-F |
| CASCADE | **OPEN** — the reference cascade only kills monitor rigs (indices 2..5, none of which exist) and dims globally (`set_blackout` 0.55 → 0.75); no circuit geography is stamped for any room | — | panel order | scripts/cascade.gd lines 20–46; restoration-lighting-bible.md §STATES CASCADE |
| THE CROSSING | **OPEN** | The sign-off's glow leaks along the broadcast path; the shed is not on it (MC → little door) | his eye dark | — | restoration-after-fire-chum.md §THE LAST CROSSING |
| 4c | **OPEN** | The reverse tour blacks out Day 1's rooms then the tower light; the shed was never toured — whether P-S1 is on the circuit that dies is OPEN | — | — | restoration-lighting-bible.md §STATES 4c; restoration-player-routing.md Day 1 spine |
| Colour script | per-day post volume; values OPEN | — | — | — | restoration-lighting-bible.md §UE5 TECHNICALS |

### 3.6.4 FIXED PROPS
| Prop | Tier | Interact? | Real dims (m) | Placement (uu, proposed unless cited) | Asset candidate · licence |
|---|---|---|---|---|---|
| EDITH CRAIK'S OVERFLOW BOXES with THE QUIET ROOM KEY, felt-wrapped — the HERO | Interactable (the key is the pickup; the boxes are its host) | YES — `THE QUIET ROOM KEY · FELT-WRAPPED · take (E)` [GameText 679, 37] | key 0.06 (PropKit key_prop: bow Ø0.12, shaft 0.18 — oversized; **OPEN 3.6-E** scale truth); felt wrap 0.10 × 0.06; boxes: two cardboard cartons ≈ 0.45 × 0.35 × 0.30 | key at (1000, 1400, 50) [world_builder.gd 782]; PROPOSED: the top carton at (1000, 1400, 0..30) with its lid folded back so the key sits ON it at Z 50 (resolves OPEN 0-J for this room); the second carton beneath/behind at (1000, 1470, 0) | Fab search "cardboard box old" (Megascans free, FAB-IMPORT starter set "cardboard boxes"); key bespoke (brass under M_Enamel-free metal; felt tag under the wool/felt family, a BOY'S HAND lettering in the albedo: FOR THE QUIET ROOM) |
| Shelf (single plank on brackets) | Dressing (lore host: STAGE FLOOR '74 can; W3 spawn site) | NO | 2.4 × 0.30 × 0.04 | (1120, 1400, 120) along Y on the +X wall [world_builder.gd 1419] | Megascans "wood plank weathered"; brackets bespoke steel |
| Three paint cans | Dressing (one is the ledger's STAGE FLOOR '74) | NO | Ø0.16 × 0.20 (a US quart can is Ø0.11 × 0.12; a gallon Ø0.17 × 0.19 — the reference reads as gallons) | (1120, 1340, 132), (1120, 1400, 132), (1120, 1460, 132) [world_builder.gd 1430] | Fab search "paint can rusted" or Poly Haven search "paint can" *(verify id)* CC0; labels under M_Paper; the brush balanced across the middle can |
| Broom | Dressing | NO | handle Ø0.04 × 1.5; head 0.3 × 0.12 × 0.06 | (890, 1510, 75) leaning 0.18 rad against the −X/+Y corner [world_builder.gd 1437–1438] | Poly Haven search "broom" *(verify id)* CC0 or bespoke |
| Rod stock in a coil, felt scraps snagged on the cut ends | Dressing (ambient lore host) | NO | coil Ø0.5, rod Ø0.008 | hung on a nail on the −Y wall at (1000, 1252, 140) | Bespoke spline coil; felt scraps as alpha cards (M_Wool family) |
| The door's INSIDE face: pencil tally marks in fives, stopping at fifty-eight | Door (interactable in the Doors table, counted there) | door verb (locked until EDITH) | leaf 1.2 × 2.2 (ref) / slab 2.6 — OPEN 0-A | leaf hinged at (850, 1340) [world_builder.gd 271–279]; marks at Z 120–160 on the inside face, pencil in the albedo/normal (<2 cm → maps, §R.2) | Fab search "wooden door old planks" (Megascans); padlock + hasp on the yard face per 3.5 §3.5.4 |
| Stenciled initials gone illegible | Dressing detail (keynote) | NO | 0.2 × 0.08 stencil | on the top carton's side or the shelf's end board — OPEN which object | stencil in the albedo, worn to illegibility (three reads: SURFACE a stencil, CURIOUS which letters, OBSESSIVE none — the illegibility is the point) |
| Child's drawings of Chum, pre-show | Dressing (inventory §1) | NO | crayon on 0.28 × 0.22 paper | loose in the second carton, one corner showing | M_Paper; crayon albedo; must show the STAGE puppet (patchwork, buttons), never the After-Fire body |
| W3 (the third viewing) | Secret pickup (spawns Day 4 after W2) | per port | — | "on the shed shelf" → the plank at (1120, 1400, 120), empty berth at Y ≈ 1520 | OPEN — W-series text keys are not in GameText.csv (grep at build time) [restoration-walkthrough-levels-endings.md ADDENDUM SPOILER] |
| Surfaces | — | — | floor 9 m², walls 4 × 3 × 3 m | — | Floor: Megascans "packed dirt" over a concrete pad → `MI_Shed_Floor`; walls: Megascans "painted wood siding" interior face with visible studs → `MI_Shed_Wall` (the yard-side face is `MI_Shed_Ext` per 3.5); roof underside: rafters + corrugated metal → `MI_Shed_Ceiling` (subject to OPEN 3.6-A height) |

### 3.6.5 LORE ITEMS (ledger; all promptless, static, three-reads compliant)
| Item | Tag | Sits | Text key | Source |
|---|---|---|---|---|
| A paint can labeled STAGE FLOOR '74 with a clean brush balanced across it, hardened mid-care | T4 | The middle can on the shelf, (1120, 1400, 132); brush 0.25 long across the rim; label legible at 1 m | none (ambient never prompts — QA-55) | restoration-ambient-lore-ledger.md SHED |
| Rod stock in a coil, felt scraps snagged on the cut ends | T4, T1 | The nail on the −Y wall, (1000, 1252, 140) | none | restoration-ambient-lore-ledger.md SHED |
| On the door's inside, tally marks in pencil, groups of five, stopping at fifty-eight | HC | Inside face of the leaf at Z 120–160; countable only at 1 m | none | restoration-ambient-lore-ledger.md SHED |
| (Inventory, not the ledger) child's drawings of Chum, pre-show | — | Second carton | none | restoration-room-inventory.md §1 |
| Handled L = 1 | — | No D-series readable is homed in the shed; the L cap's occupant is OPEN 0-G (candidate: W3, a viewing pickup) | — | — |

### 3.6.6 DRESSING PASSES
| # | Pass | Steps | Verification capture | Must read |
|---|---|---|---|---|
| P0 | Data check | Bounds X 850..1150 / Y 1250..1550; one slab at (850, 1400) with the PADLOCKED reason at Z 290; no station; no lamp change yet; resolve OPEN 3.6-A (3 m box vs shed eaves) before P1 | top-down (1000, 1400, 900) → (1000, 1400, 0) | Exact CSV geometry |
| P1 | Surfaces | Dirt-over-pad floor; stud-and-siding walls; rafters; wear pass; board gaps that admit slivers of beacon red | (870, 1400, 148) → (1150, 1400, 120) (from the door, at the shelf) | Three-way light break on siding; no repeat across 3 m; the room reads older than the building |
| P2 | Fixed props | Shelf, three cans, broom, cartons + key, rod coil, drawings, door leaf inside face | (870, 1400, 148) → (1000, 1400, 50) | The key reads as felt-wrapped brass at 1 m; the cartons carry the key (nothing floats); the hero is the key by wear (the felt is the only soft thing in the room) |
| P3 | Practicals + EV | P-S1 bulb + chain with true bulb geometry; delete the P0 stand-in lamp; author NIGHT-OFF (bulb dark) and NIGHT-ON (pulled) as two scenarios (CUT); record the chosen EVs in the PR as PROPOSALS | NIGHT-OFF: (870, 1400, 148) → (1120, 1400, 120); NIGHT-ON: same | OFF: the shelf resolves by beacon spill and board-gap slivers alone; ON: one hard tungsten pool, hard shadows of the cans on the wall |
| P4 | Lore FIRST | STAGE FLOOR '74 can + brush; rod coil with felt; the tally marks inside the door | 1 m closeups: (1020, 1400, 148) → can; (1000, 1350, 148) → coil; (950, 1400, 140) → door inside face | Each legible at 1 m, unremarkable at 3 m; no prompt fires inside the 2.6 m reach [Data/Timings.csv player.gd REACH] |
| P5 | Dressing mass (≤ 6) | A dead wasp nest under the rafters ("wasp-quiet"), a coil of guy-wire (rhymes with the yard's 1971 tag), a coffee can of screws, a rake, a folded tarp, a hand-painted sign blank — each owned by the club's yard habits | (870, 1400, 148) → (1150, 1400, 120) | Count ≤ 6; nothing looks operable that is not |
| P6 | Wear/decals/drift | Rust streaks under the shelf brackets, paint drips on the floor pad, the hasp's angle hook (dressing drift, monotonic) | Day 1 vs Day 4 pair (hasp angle only) | Only the hasp angle changed |
| P7 | QA + acceptance | QA-55 (prompts: the key and the door only; pull chain per OPEN 3.6-D), QA-56 (drift = hasp angle only), QA-57 (hero = the key/boxes) | §3.6.7 | §3.6.7 |

### 3.6.7 ACCEPTANCE CAPTURE
- Camera A (the reason you came): **(870, 1400, 148) → look-at (1000, 1400, 50)**, NIGHT, bulb pulled, Day 4 post volume.
- Camera B (the walk back): **(1130, 1400, 148) → look-at (850, 1400, 120)** through the open door toward the yard, NIGHT, bulb off — the beacon must read in the doorway.
- Checklist: (1) one bulb, one chain, nothing else authored; (2) the key sits ON something and reads felt-wrapped; (3) STAGE FLOOR '74 legible at 1 m, promptless; (4) tally marks countable at 1 m only; (5) with the bulb off the room still resolves (dark is a room); (6) no naked primitive (cans have seams and dents in maps); (7) store-page test [AAA_BUILD_PLAN.md §R].

### 3.6.8 OPEN
- **3.6-A** Shed height: the stamp gives a 3 × 3 × 3 m box; a shed of this footprint has ≈ 2.2 m eaves. Data change or dress the extra metre as rafters?
- **3.6-B** Interactable count: cap 1/1/6 vs inventory §1 (the shed door `operate`, the boxes `take`). This brief: I = the key (boxes as host); the door counts in the Doors table.
- **3.6-C** "Padlock hasp (unlocked, always)" vs `PADLOCKED` + EDITH key. Which state does the bible describe?
- **3.6-D** Is the pull chain operable (a second interactable), or does P-S1 come on with the door?
- **3.6-E** Key scale: PropKit key_prop is ≈ 0.3 m long (a stage prop); a real key is 0.06 m.
- **W3 text keys** not in GameText.csv.

---

## 3.7 · CORRIDOR — the spine; the walk you will know blind

### 3.7.1 IDENTITY
| Field | Value | Source |
|---|---|---|
| Rooms.csv | `CORRIDOR, 0.0, -7.5, 3.0, 7.0` → centre (0, −750), 3 × 7 m, long axis Y | Data/Rooms.csv |
| Floor bounds (uu) | X −150..150, Y −1100..−400, floor top Z 0, wall top Z 300 | derived |
| Door → REC ROOM | `REC ROOM, CORRIDOR, 0.0, -4.0, 1.6, x,` → OPEN gap (0, −400), 1.6 m (X −80..80) in the +Y wall; no slab, no leaf; a fold threshold for him (§0.2) | Data/Doors.csv; world_builder.gd 580–581 |
| Door → TAPE LIBRARY | `CORRIDOR, TAPE LIBRARY, 0.0, -11.0, 1.6, x,` → OPEN gap (0, −1100), 1.6 m in the −Y wall; no slab | Data/Doors.csv |
| Stations | none inside. **S1 LIBRARY LANDING** sits at Godot (−1.2, 0, −11.8) → UE (−120, −1180, 0), 0.8 m PAST the library gap, inside TAPE LIBRARY (unit 3.8) — the bible's "S1 at the library mouth" is honoured on the library side | Data/Stations.csv; restoration-room-bible.md CORRIDOR |
| Monitors | **CAM 1 · CORRIDOR**: camera at Godot (0, 2.4, −10.6) → **(0, −1060, 240)**, look-at (0, 1.2, −4.5) → **(0, −450, 120)**: the camera hangs high at the LIBRARY end of the corridor looking back up its whole length toward REC, vertical FOV 65°. Its monitor is at Godot (2.4, 1.7, −3.82) → **(240, −382, 170)**, yaw π, i.e. on the REC ROOM side of the shared wall, facing into REC (see 3.1–3.5 §3.2.1). The corridor is therefore the game's first mediated corridor and its whole 7 m is inside CAM 1's cone; the feed is watched FROM the rec room | Data/Monitors.csv; scripts/monitor_rig.gd lines 26–30; ROOM-BRIEFS-3.1-3.5.md §3.2.1 |
| Rig index | CAM 1 is `rigs[0]`: the Night 1 trip kills it (`rigs[0].set_killed(true)`) 20 s into the first night; the cascade's `_kill_range(2, 4)` / `(4, 6)` never reaches it | scripts/night_trip.gd lines 16–29; scripts/cascade.gd lines 23, 31, 43–46 |
| Demo | open | Data/DemoOpen.csv |
| Reference placements | none besides the stand-in lamp (0, −750, 275) (energy 0.5, range 5.25 m; greybox 9.0 cd, attenuation 525 uu); no notice board, clock, or fixture exists in code | world_builder.gd lines 162–170; build_greybox.py 116–126; `_spawn_wall_clocks` line 538 (no corridor spot) |
| Adjacent | REC ROOM (+Y), TAPE LIBRARY (−Y); the ±X walls face unstamped void (KITCHEN's −Y wall ends at Y −250; DORMS likewise) | Data/Rooms.csv |

### 3.7.2 ROLE
| Aspect | Canon | Source |
|---|---|---|
| Personality | "The spine; the walk you will know blind. Spaced tungsten with authored gaps." Bed: your own footsteps returned a half-size large. Keynotes: S1 at the library mouth, notice board, floor wax history | restoration-room-bible.md CORRIDOR |
| Budget | 1 / 0 / 6; drift: notice board papers; web: bulbs die per casualty (B-R2) | restoration-room-bible.md CORRIDOR; PROGRESS.md 3.7 |
| B-R2 | "To the ledger filling: corridor practicals lose one bulb per casualty, never replaced (QUEUE B-R2: the lighting bible's grief)" — up to ten named deaths plus the rows | restoration-reaction-matrix.md THE BUILDING; restoration-casualty-ledger.md THE FULL BOARD |
| Dread role | THE MEDIATION LESSON, first instance: T1.4 "In the hallway feed, on the wall monitor, something crosses at the far end and stops at the frame line, toes to an invisible mark, and waits, and withdraws [DREAD, uncatalogued: the obedience moment]" — the far end is the CAM 1 look-at end (REC gap) or the camera end; the frame line is CAM 1's frame edge · L2: the pendulum home loop (Dorms → Rec → Library → Bench) walks this spine every day and night until muscle memory; later acts violate it | restoration-game-master.md T1.4; restoration-player-routing.md §MOVEMENT GRAMMAR 1, Night 1 spine; restoration-dread-doctrine.md L2 |
| Sightlines | "Every space is authored twice: once for direct sight and once for mediation … Corridor kinks, monitor placement, and camera mounts are the geometry of survival." The stamped corridor is straight (no kink) | restoration-walkthrough-levels-endings.md Part III.2 |
| Beats | Night 1 spine: DRM → living-wing corridor → REC (4:3 static) → corridor wall monitor (the frame-edge obedience) → LIB landing S1 → DRM · NIGHT TRIP (code, once per save): 20 s into the first night `rigs[0]` dies: "A breaker lets go somewhere below. A feed drops off the board." (2.8 s) "Behind you, unhurried: a hummed bar of the closing song." (2.4 s) "The hall behind you is a hall. The patch bay can fix the rest." · T2.7 NIGHT FOUR: "The corridor monitor dies. In the half second of live phosphor after power, something crosses the reflection where nothing crosses the hall [SCARE 2: the reflection cross]" then the blackout pursuit CTL → PB · Night 4 spine: "a required corridor route REC→LIB. Overdraw trips a breaker mid-route" · Night 2: return "via REC (Harriet's freeze catchable at the KIT threshold in periphery)" | restoration-player-routing.md Night 1, Night 2, Night 4 spines; scripts/night_trip.gd; Data/GameText.csv lines 511–513; restoration-game-master.md T2.7, Appendix A row 2 |
| Sound | S14 THE HUMMED BAR: "A human contralto, unaccompanied, two rooms behind the player, dry (unmediated: this is the one rationed breach)" — fired by the night trip while the player is on the Night 1 loop; S04 door thunks (no leaf here); the bed "footsteps returned a half-size large" = a reflective corridor (hard floor, hard walls) | restoration-audio-bible.md S14, S04; restoration-room-bible.md CORRIDOR |
| Him | 3.35 m tall in a 3.0 m-walled, 3 m-wide corridor (OPEN 0-H); the two open gaps each cost him 2.2 s (QA-37: "a route through two doors buys 4.4 s"); "HIS SHADOW IS A MECHANIC … his shadow precedes him through doorways" — CAM 1's fixture spacing decides whether that shadow has a light to be cast by at NIGHT | Data/Timings.csv; QA-37; restoration-lighting-bible.md §HIM |
| Route | Day 1 spine REC → … → LIB passes here; 4c blacks out rooms "in Day 1 order, entry last": the spine lists rooms, not the corridor — its place in the order is **OPEN 3.7-A** | restoration-player-routing.md Day 1 spine; restoration-lighting-bible.md §STATES 4c |
| Inventory listing | The room inventory has no living-wing corridor section (§10 CONTROL CORRIDOR is a different room); GLOBAL items that apply: camera mounts + tally lamps (T2 route/read), wall monitors (T2 read), break-window clocks ("every zone carries a repeater or sightline to one" — none stamped here: **OPEN 3.7-B**) | restoration-room-inventory.md §GLOBAL |
| The I | Cap I = 1 and nothing in the room prompts in the reference. Candidates: the CAM 1 mount (GLOBAL "T2 route/read" — but routing happens at the patchbay) or the notice board (bible keynote; drift-eligible → dressing by law). This brief: I = the CAM 1 camera mount with its tally (read-only), hero by wear (the polished pan handle, the taped label) — **OPEN 3.7-C** | restoration-object-taxonomy.md ¶INTERACTABLES, ¶DRESSING; restoration-room-inventory.md §GLOBAL |

### 3.7.3 LIGHTING STATE TABLE
| State | Locked EV | Practicals | Red reads? | Transition | Source |
|---|---|---|---|---|---|
| DAY ON AIR | **OPEN** | "Spaced tungsten with authored gaps (the gaps are content)": PROPOSED three ceiling fixtures on the corridor axis, P-C1 (0, −500, 290), P-C2 (0, −750, 290), P-C3 (0, −1000, 290), true bulb geometry; P-C2's socket EMPTY on Day 1 (the authored gap at the corridor's middle, where the stand-in lamp was); tungsten family word; intensities OPEN. Fixture COUNT is **OPEN 3.7-D**: B-R2 removes one bulb per casualty and the board holds up to ten deaths plus rows; two lit bulbs go dark at two deaths, which buys darkness-as-content (banned) — the owner must set the bulb count against the casualty count so the floor always resolves | CAM 1's tally lamp at (0, −1060, 240) IF one exists (OPEN 0-I); lit = watched = safe for the whole corridor | CUT | restoration-lighting-bible.md §UE5 TECHNICALS CORRIDORS, §GRAMMAR; restoration-reaction-matrix.md B-R2; restoration-dread-doctrine.md ANTI-CREEP |
| BREAK | **OPEN** | Same fixtures; the tally (if any) dies with every tally at the 50 s flip — the corridor is then a lit but unwatched hall, which is the bible's "BREAK IS VISIBLY LESS SAFE" made spatial | red drains | CUT at the flip | restoration-lighting-bible.md §STATES BREAK; Data/Timings.csv broadcast.gd |
| NIGHT | **OPEN** | Practicals off; CAM 1's tally (if any) and the REC-side monitor's phosphor through the +Y gap; the library's stack-end glow through the −Y gap; floor must resolve end to end (7 m) | tally only | CUT | restoration-lighting-bible.md §STATES NIGHT |
| NIGHT 1 TRIP (room-specific, once per save) | — | CAM 1 killed → its tally (if any) dies; "A breaker lets go somewhere below" — whether the corridor's own practicals are on that breaker is OPEN; the reference dims nothing here | red → none | instant | scripts/night_trip.gd; Data/GameText.csv 511–513 |
| CASUALTY STATES (B-R2) | **OPEN** | One bulb out per casualty, never replaced: ten authored states from the casualty ledger's board; order of loss (nearest REC first? nearest the library?) is OPEN | — | CUT at the casualty toast | restoration-reaction-matrix.md B-R2; restoration-casualty-ledger.md |
| CASCADE | **OPEN** — no circuit stamped; the reference kills rigs 2..5 only | — | — | panel order | scripts/cascade.gd; lighting bible §STATES CASCADE |
| 4c | **OPEN** (OPEN 3.7-A: between REC and LIB in the order, or with one of them) | — | — | room-by-room | lighting bible 4c |
| Colour script | Day 1 warmest; values OPEN | — | — | — | lighting bible §UE5 TECHNICALS |

### 3.7.4 FIXED PROPS
| Prop | Tier | Interact? | Real dims (m) | Placement (uu) | Asset candidate · licence |
|---|---|---|---|---|---|
| CAM 1 · CORRIDOR camera mount (+ tally lamp per OPEN 0-I) — the HERO (OPEN 3.7-C) | Interactable (GLOBAL: route/read; routing at PB) | read-only; no prompt in the reference | 1970s studio/security camera ≈ 0.45 × 0.2 × 0.2 on a wall bracket 0.3; tally lamp Ø0.03 | camera at (0, −1060, 240) aimed at (0, −450, 120) [Data/Monitors.csv]; bracket on the −Y wall above the library gap header (the gap is 1.6 m wide, slab-less; the header is Z 260–300) | Poly Haven search "security camera"/"cctv camera" *(verify id)* CC0 or bespoke (a broadcast-style box camera, taped label CAM 1 in the albedo); tally lamp under M_Practical with a true red bulb IF ruled |
| Notice board (FOUND PROPERTY memo host; drift: papers) | Dressing (ambient lore host) | NO | 0.9 × 0.6 cork in a frame | +X wall at (148, −600, 160) (between P-C1 and P-C2, in the light) | Fab search "cork board" (as 3.1/3.2); papers under M_Paper; pins in maps |
| S1 LIBRARY LANDING (lectern; chained pen) | Interactable — **in TAPE LIBRARY (3.8)**; listed here because the bible names it a corridor keynote | see 3.8 | — | (−120, −1180, 0) | see 3.8 |
| Floor wax history: the newest wax over an older traffic lane that "bends toward the dead room's door before the club ever labeled it" | Surface detail (ambient lore) | NO | lane 0.8 wide | the lane runs the corridor's axis and BENDS at the library end toward +X — **OPEN 3.7-E**: the dead room is at (1900, 250), east of the transmitter hall; no door toward it exists on this corridor; the bend can only gesture (+X) | roughness/normal detail in `MI_Corridor_Floor` (a second wax layer mask); never albedo-loud |
| Ceiling fixtures P-C1..C3 | Practicals | NO | pendant/flush tungsten fixture Ø0.25, true bulb | (0, −500, 290), (0, −750, 290 — empty socket), (0, −1000, 290) PROPOSED | Fab search "ceiling light vintage industrial" (Megascans free tier if present) or bespoke; glass under M_Practical; bulbs removable per B-R2 state |
| Skirting / threshold plates | Dressing (surface) | NO | skirting 0.16 high (reference baseboard 0.16 × 0.28) | both long walls; steel threshold strips at Y −400 and Y −1100 | prop_kit.gd `baseboard` lines 246–254; Megascans "painted wood trim" |
| Fire extinguisher (starter list) | Dressing | NO | Ø0.15 × 0.55 on a bracket | −X wall at (−148, −900, 90) | Megascans "fire extinguisher" (FAB-IMPORT starter set) |
| Surfaces | — | — | floor 21 m², walls 2 × 7 × 3 + 2 × 3 × 3 m | — | Floor: Megascans "linoleum/checker" or "vinyl tile waxed" → `MI_Corridor_Floor` with the two-layer wax mask; walls: Megascans "brick (painted-over)" (starter) or "plaster wall painted aged" → `MI_Corridor_Wall`, neutral held (walls never drift); ceiling: "acoustic ceiling tile" → `MI_Corridor_Ceiling` (subject to OPEN 0-H) |

### 3.7.5 LORE ITEMS
| Item | Tag | Sits | Text key | Source |
|---|---|---|---|---|
| The notice board's yellowed memo: FOUND PROPERTY, ONE CHILD'S MITTEN, UNCLAIMED, dated three years before the fire (1974), initialed and never taken down | T2 | The notice board, +X wall (148, −600, 160), pinned under newer papers with one corner showing; legible at 1 m | none (QA-55) | restoration-ambient-lore-ledger.md CORRIDOR |
| Beneath the newest wax, an older traffic lane bends toward the dead room's door before the club ever labeled it | T7 adjacent, HH | The floor, library end, bending +X (OPEN 3.7-E) | none | restoration-ambient-lore-ledger.md CORRIDOR |
| S1's pen is chained; the chain has been replaced twice, the pen never | ritual, HC | S1's lectern at (−120, −1180, 0) — in TAPE LIBRARY; dressed in 3.8 P4 | none | restoration-ambient-lore-ledger.md CORRIDOR; Data/Stations.csv |
| Handled L = 0 | — | No D-series readable here (D09 is CONTROL's) | — | restoration-props-packet.md |

### 3.7.6 DRESSING PASSES
| # | Pass | Steps | Verification capture | Must read |
|---|---|---|---|---|
| P0 | Data check | Bounds X ±150 / Y −1100..−400; two open gaps (0, −400) and (0, −1100), no slabs; no station inside; CAM 1 camera position (0, −1060, 240) confirmed against the level's rig | top-down (0, −750, 900) → (0, −750, 0) | Exact; resolve OPEN 0-H before any ceiling |
| P1 | Surfaces | Waxed floor with the two-layer lane; painted-over brick or plaster; skirting; threshold plates; wear pass (scuffs at both gaps) | (0, −410, 148) → (0, −1100, 150) (from the REC gap, down the spine) | The lane reads as habit under raking light only; three-way light break; no tiling repeat across 7 m |
| P2 | Fixed props | CAM 1 mount (+ tally per 0-I), notice board, extinguisher, fixture housings | (0, −410, 148) → (0, −1060, 240) | The camera reads as broadcast steel with a taped label; the board reads as decades of paper |
| P3 | Practicals + EV | P-C1, P-C3 lit, P-C2 socket empty (the gap); true bulbs; delete the stand-in; lock DAY EV; author NIGHT and the ten B-R2 states as bulb-removal scenarios (CUT) | DAY: (0, −410, 148) → (0, −1100, 150); NIGHT: same | DAY: two pools and one authored dark stretch, floor readable through the gap; NIGHT: the floor still resolves end to end by the tally and the two doorway spills |
| P4 | Lore FIRST | The mitten memo; the wax lane bend; (S1's chain is 3.8's) | 1 m closeups: (60, −600, 148) → memo; (0, −1000, 148) → floor lane at raking angle | Promptless; the memo's date reads only at 1 m |
| P5 | Dressing mass (≤ 6) | A folding chair (starter) against the −X wall, a wall thermostat, a light-switch plate worn to brass, a dust mop leaning at the library end, a coat hook with one cardigan (pegs lead the drift curve — but wall tones never drift), a framed station map | (0, −410, 148) → (0, −1100, 150) | ≤ 6; each owned; nothing fake-affords |
| P6 | Wear/decals/drift | Scuff decals at both gaps; hand-height wear band on the walls at Z 90–120 (the walk you know blind); drift hook: notice board papers (dressing); state hook: bulb removal per casualty (B-R2) | Day 1 vs post-first-casualty pair from (0, −410, 148) → (0, −1100, 150) | One bulb fewer in the second frame; nothing else moved |
| P7 | QA + acceptance | QA-55 (nothing prompts unless 3.7-C rules the camera does), QA-56 (drift = papers only), QA-57 (hero = camera or none) | §3.7.7 | §3.7.7 |

### 3.7.7 ACCEPTANCE CAPTURE
- Camera A (the spine): **(0, −410, 148) → look-at (0, −1100, 150)**, DAY ON AIR, Day 1 post volume — the authored gap must read as content, not error.
- Camera B (CAM 1's own frame): **(0, −1060, 240) → look-at (0, −450, 120)**, vertical FOV 65° to match Monitors.csv exactly (this frame is what the REC monitor shows on Night 1), NIGHT — the obedience-moment frame line is this frame's bottom edge.
- Checklist: (1) spaced tungsten with one authored gap; (2) the tally (if ruled) is the only red; (3) the wax lane reads only under raking light; (4) the mitten memo is findable, unflagged; (5) at NIGHT the floor resolves end to end; (6) no naked primitive on the fixtures or camera; (7) store-page test.

### 3.7.8 OPEN
- **3.7-A** Where the corridor falls in the 4c reverse-tour order (the Day 1 spine names rooms only).
- **3.7-B** Break-window clock: canon says every zone carries a repeater or a sightline to one; none is stamped in the corridor and REC's clock spot is itself OPEN 3.2-D.
- **3.7-C** The I = 1 occupant: the CAM 1 mount (read-only) or the notice board (drift-eligible, so dressing by law)?
- **3.7-D** Fixture/bulb count vs the casualty count for B-R2 (the floor must always resolve).
- **3.7-E** The wax lane "bends toward the dead room's door": no such door exists on this corridor; the bend can only gesture +X.
- **0-H, 0-I** as in §0.3.

---

## 3.8 · TAPE LIBRARY — a chapel of holdings; quiet is enforced by the room itself

### 3.8.1 IDENTITY
| Field | Value | Source |
|---|---|---|
| Rooms.csv | `TAPE LIBRARY, 0.0, -16.0, 12.0, 10.0` → centre (0, −1600), 12 × 10 m, the largest room in the living/work wing | Data/Rooms.csv |
| Floor bounds (uu) | X −600..600, Y −2100..−1100, floor top Z 0, wall top Z 300 | derived |
| Door → CORRIDOR | `CORRIDOR, TAPE LIBRARY, 0.0, -11.0, 1.6, x,` → OPEN gap (0, −1100), 1.6 m (X −80..80) in the +Y wall; no slab | Data/Doors.csv |
| Door → BENCH ROOM | `TAPE LIBRARY, BENCH ROOM, 6.0, -16.0, 1.4, z,` → OPEN gap (600, −1600), 1.4 m (Y −1670..−1530) in the +X wall; no slab. **Merle's DOORWAY mark is here**: `DOORWAY := Vector3(6.0, 0.0, -16.4)` → (600, −1640, 0), in the gap, when the pen is up | Data/Doors.csv; scripts/merle.gd lines 9, 21, 35 |
| Door → FIRE CORRIDOR | `TAPE LIBRARY, FIRE CORRIDOR, -6.0, -16.0, 1.4, z, locked:SEALED · reopens for the anniversary (Tape 4)` → gap (−600, −1600), 1.4 m in the −X wall; slab 2.6 m; **LOCKED with no key** (event-unsealed: `_fire_door`; Day 4 toast "The club unseals the fire corridor for the anniversary. Nobody goes first."); reason text at (−600, −1600, 290); reference hinge at (−600, −1670, 0) rotated π/2; the Glimpse spawns beyond it at (−1260, −1600, 0) | Data/Doors.csv; Data/GameText.csv lines 657, 193; world_builder.gd lines 260–261, 268–279; scripts/glimpse.gd line 33 |
| Door → CONTROL | `TAPE LIBRARY, CONTROL, 0.0, -21.0, 1.6, x,` → OPEN gap (0, −2100), 1.6 m in the −Y wall; no slab (so no leaf exists to carry the demo's "SEALED · the club opens the rest when the contract is signed" — **OPEN 3.8-A**: CONTROL is not in DemoOpen.csv yet the gap has no door node to seal) | Data/Doors.csv; Data/DemoOpen.csv; world_builder.gd lines 91–93, 262–266 |
| Station | **S1 LIBRARY LANDING** at Godot (−1.2, 0, −11.8) → **(−120, −1180, 0)**; greybox marker 0.5 × 0.5 × 1.1 at Z 55 + id text at Z 150; reference: lectern (post 0.12 sq × 0.95, angled top 0.5 × 0.42, binder 0.36 × 0.30, chained pen), label `S1 LOG`; prompt `S1 · LIBRARY LANDING · sign the log (E) · %d line(s) left` / `… · unlimited paper` / `… · no paper. walk to the next station.`; Day 1 objective "sign the log at S1, the library landing"; first save (QA-05) | Data/Stations.csv; build_greybox.py 156–163; world_builder.gd `_spawn_station` 283–304; prop_kit.gd `lectern` 347–361; scripts/log_station.gd 9–15; Data/GameText.csv lines 483–486, 181; QA-05 |
| Monitors | **CAM 2 · STACKS**: camera at Godot (0, 2.4, −20.4) → **(0, −2040, 240)**, look-at (0, 1.2, −12.0) → **(0, −1200, 120)** — high at the CONTROL end, looking up the centre aisle toward the corridor mouth and S1, vertical FOV 65°. Its monitor at Godot (7.2, 1.7, −13.18) → **(720, −1318, 170)**, yaw 0 → inside the BENCH ROOM on its +Y wall, facing −Y into the bench room (3.9). The library is watched; the watching is done from the bench | Data/Monitors.csv; monitor_rig.gd 26–30 |
| Demo | open | Data/DemoOpen.csv |
| Reference placements (Godot → UE) | FOUR STACKS (`tape_shelf(3.0, 2.2, 4, seed)`: 3.0 m long along local X, 2.2 m high, 0.42 m deep, 4 shelves, spines seeded stable with borrowed-tape gaps and leaners; collider 3.0 × 2.2 × 0.5): (−3.2, 0, −13.2) rot π seed 101 → **(−320, −1320, 0)** facing −Y; (3.2, 0, −13.2) rot π seed 102 → **(320, −1320, 0)** facing −Y; (−3.2, 0, −18.8) rot 0 seed 103 → **(−320, −1880, 0)** facing +Y; (3.2, 0, −18.8) rot 0 seed 104 → **(320, −1880, 0)** facing +Y. All four face the CENTRE AISLE at Y −1600 (stack faces at Y ≈ −1341 and ≈ −1859: a 5.2 m aisle); a CROSS AISLE X −170..170 (3.4 m) runs door to door (0, −1100) → (0, −2100); "every lane to a door kept clear" · FILM CABINET (`FilmCabinet`) at (−5.4, 0.7, −19.0) → **(−540, −1900, 70)**: flat file 0.7 × 1.4 × 0.7 (Z 0..140), four drawer faces 0.62 × 0.28 with pulls, the second drawer sitting 3 cm proud "because it will not fully close"; the media alcove is the −X/−Y corner · DAILIES SLOTS (`SLOTS`, canisters spawn one per capture, +40 uu X per wrap): (−3.5, 0.35, −14.0) → **(−350, −1400, 35)**; (2.5, 0.35, −18.5) → **(250, −1850, 35)**; (4.0, 0.35, −13.0) → **(400, −1300, 35)**; (−4.5, 0.35, −19.0) → **(−450, −1900, 35)**; tag `TAKE %d` in warning red · THE TAUGHT CHASE start: at the first capture after the wake the Rundown is placed at (−5.0, 0, −16.0) → **(−500, −1600, 0)**, the far −X end of the centre aisle beside the sealed FIRE door, two thresholds from the bench · STORY CORNER anchor = room centre **(0, −1600, 0)** · stand-in lamp (0, −1600, 275), range 9 m / 9.0 cd attenuation 900 uu | world_builder.gd `_spawn_library_stacks` 1203–1216, `_spawn_film_and_note` 858–897; prop_kit.gd `tape_shelf` 387–415; scripts/dailies_manager.gd 5–7, 21–22, 40–44; scripts/capture_bench.gd 28–31; scripts/rundown.gd 8–12, 350–354; README.md Commit 047 |
| Adjacent | CORRIDOR (+Y), BENCH ROOM (+X, gap at Y −1600), FIRE CORRIDOR (−X, sealed), CONTROL (−Y). Between the bench-room gap and the corridor the +X wall (X 600, Y −1530..−1100) faces void | Data/Rooms.csv |

### 3.8.2 ROLE
| Aspect | Canon | Source |
|---|---|---|
| Personality | "A chapel of holdings; quiet is enforced by the room itself. Cool practicals, stack-end lamps." Bed: HVAC breath, ballast tick. Keynotes: card catalog, accession spines (the skip cluster findable), one mislabeled decade | restoration-room-bible.md TAPE LIBRARY |
| Budget | 2 / 2 / 16; drift: a spine reversed; web: Vess's country borders here; the crate lives deep | restoration-room-bible.md TAPE LIBRARY; PROGRESS.md 3.8 |
| The crate | Bible: "the crate lives deep" (library). Inventory GLOBAL: "The impossible-tapes crate · T4 · EVT then BEN · Delivered at ENT, lives at the bench thereafter". Code: `ImpossibleCrate` at ENTRY (0, 600, 50) only; "The seance reel is on the bench now. He would not carry it further than that." — **OPEN 3.8-B** (three homes) | restoration-room-bible.md; restoration-room-inventory.md §GLOBAL; world_builder.gd 1119–1122; Data/GameText.csv 382 |
| Dread role | L3 THE NOTICING GAME made architecture: "the game hides deltas and hands the player instruments"; the skip cluster is "findable by anyone who runs a finger down the spines" · THE COMPACTUS PRINCIPLE: "player-operated architecture (rolling stacks …) means the player configures their own level" · from T3 the Rundown's STORY CORNER claims these aisles at night: "the stacks the player arranged by day are the corridor walls by night" · Night 2: "first scripted Quiet Game, low stakes, stillness taught" in a LIB aisle | restoration-dread-doctrine.md L3; restoration-walkthrough-levels-endings.md Part II Tape library and bench, Part III.3; restoration-room-inventory.md §6 State changes; restoration-player-routing.md Night 2 spine |
| Beats | T1.4 NIGHT ONE "S1 log station introduced at the library landing; first save signature … Opening the binder at S1 surfaces the first green-ink margin note: LELAND (green ink): You are safe as audience. Do not be interesting. Never accept a role." · Day 1 spine "LIB (stacks tour, S1 station shown)" · T2.3 airdate circuit: "station logs (LIB drawer)" = source one of four · T2.4 THE FILM CABINET (library media alcove): PRESERVE the TRAINING key → "WGLD STAFF ORIENTATION, 1971 … six signals"; ASK Harriet → the seventh; FORCE pry → four of six · T3.5 NIGHT: THE RUNDOWN WAKES (library): "the story corner drifting through the stacks … the Floor Manager stands at the stack end with one hand rising, and points. YOU'RE ON [SCARE 5]. The compactus cranks from the far end, aisle walls walking [SCARE 4]. Escape is built, not run: LIB to CTL inside a break window, then PB" · Night 5 spine: objective the next reel from CLM; route DRM → REC → LIB → CLM; the chase on the return leg · Night 8 spine: LIB → FIRE (the glimpse) → DOCK → GRN → S3 · Burn Your Dailies: "a new film canister appears in the library stacks, labeled with the scene and take … retrieve the footage of your own death, at night, under the Rundown" · W1 "in the library's skip gap where 0118 should be (Day 2)" · H1: after taking Harriet's slip "the film cabinet now contains her, folded, with leader tape where her voice was" (`[A REEL, LABELED IN HER HAND: ME]`) · L-R1: carrying the fire tape past Leland's shelves adds one unsigned margin: NOT THAT ONE. PLEASE. | restoration-game-master.md T1.4, T2.3, T2.4, T3.5; restoration-player-routing.md Day 1, Night 5, Night 8; restoration-walkthrough-levels-endings.md Part V-B Burn Your Dailies, ADDENDUM SPOILER; restoration-casualty-ledger.md H1; Data/GameText.csv 212–214; restoration-reaction-matrix.md LELAND |
| Texts | Film cabinet: `FILM CABINET · LOCKED · the key is tagged TRAINING, in green` / `… run the 1971 orientation film (E)` / `… run the orientation film again (E)`; `Locked. Somewhere, a key is tagged TRAINING in green ink.`; `WGLD STAFF ORIENTATION, 1971. A floor manager smiles at you across fifty years.`; `SIGNAL · %s`; `Six signals. The film rattles out. It never mentions a seventh.` · Dailies: `DAILIES · SCENE 4 TAKE %d · pick up (E)`, `Hands full. One canister at a time.`, `CARRYING · SCENE 4 TAKE %d. The degausser is in the climate room.`, binder line `DAILIES IN THE STACKS: %d · carrying: %s` · Story corner: `STORY CORNER` / `TAPE LIBRARY`; `You can hear it. %s, performed to no one.`; segment line "Once there was a house where nobody had to knock." · Night objective `NIGHT · optional: burn your dailies (library to climate room) · sleep when ready` | Data/GameText.csv lines 118–125, 79–80, 159, 243, 559–560, 585, 179; restoration-game-master.md Appendix C |
| Scare blockings in this room | SCARE 4 compactus: A shelves crank from the far end; B (camera-checker) the aisle monitor shows the aisle empty — THE POISONED WELL, once per run, telegraphed by rising static; C (sprinter) shelves crank BOTH ends, escape is up and over · SCARE 5 the you're-on: A point from the stack's end; B delivered through a monitor she trusts; C from behind, reflected in dead glass | restoration-game-master.md Appendix A rows 4–5; restoration-design-doc.md Part IV-B §12 |
| Sound | Bed: HVAC breath, ballast tick (fluorescent ballasts → the "cool practicals" are fluorescent by implication; no kelvin in canon); S03 STORY CORNER loop "page turns and felt movement", duckable by distance; the compactus crank (no slot yet); rail ladder "creaks on a fixed note"; "noise draws attention at night" | restoration-room-bible.md; restoration-audio-bible.md S03; restoration-room-inventory.md §6 |
| Route | The pendulum's third stop (Dorms → Rec → Library → Bench); Day 1 order puts LIB fifth (ENT → REC → KIT → DRM → LIB → BEN), so in 4c the library goes dark SECOND, right after the bench | restoration-player-routing.md §1, Day 1 spine; restoration-lighting-bible.md 4c |
| Sanctuary | none; the Rundown's story corner is homed here (anchor = room centre) | scripts/rundown.gd 10 |
| Inventory listing | §6: compactus rolling stacks (T1 operate; player-cranked; T3 chase; noise at night) · reel shelving + canisters (T1 inspect/take) · dailies canisters (SPAWN take) · card catalog (T1 operate; Leland's cross-reference cards in green) · S1 (T1 sign) · station log drawer (T2 inspect; airdate source one of four) · media alcove film cabinet (T2 operate; TRAINING key; FORCE pry) · 16 mm projector (T2 operate; plays the instructional film) · Leland's desk (T1 inspect DYN; T3 the mid-sentence final note) · rail ladder (T1 operate) — reconciled against 2/2/16 in OPEN 3.8-C | restoration-room-inventory.md §6 |
| Compactus vs data | The reference stacks are STATIC (`_spawn_library_stacks`, static colliders); no crank, no motion, no SCARE 4 geometry exists in code. Rolling stacks are a mechanics/data unit (Phase 4), not dressing — this brief dresses the four static stacks and marks the crank **OPEN 3.8-D** | world_builder.gd 1203–1216 |

### 3.8.3 LIGHTING STATE TABLE
| State | Locked EV | Practicals | Red reads? | Transition | Source |
|---|---|---|---|---|---|
| DAY ON AIR | **OPEN** | "Cool practicals, stack-end lamps": PROPOSED P-L1..L4 STACK-END LAMPS, one per stack at the aisle-facing end nearest the cross aisle — (−170, −1341, 200), (170, −1341, 200), (−170, −1859, 200), (170, −1859, 200) — shaded reading fixtures, true bulbs; P-L5/P-L6 two COOL ceiling tubes over the centre aisle at (−300, −1600, 290) and (300, −1600, 290) (fluorescent by the ballast-tick bed; no kelvin in canon); the S1 landing lit by borrowed corridor tungsten plus P-L1's spill. Colour family "cool" only; intensities OPEN | CAM 2's tally at (0, −2040, 240) IF ruled (OPEN 0-I): lit = the centre aisle is watched; the stacks' shadowed backs (Y −1100..−1341 and −1859..−2100 behind the shelves) are OUTSIDE the cone by geometry | CUT | restoration-room-bible.md TAPE LIBRARY; restoration-lighting-bible.md §GRAMMAR; Data/Monitors.csv |
| BREAK | **OPEN** | Same; the tally dies at the flip; "quiet is enforced by the room itself" is unchanged | red drains | CUT at 50 s | lighting bible §STATES BREAK |
| NIGHT | **OPEN** | Practicals off; standby: the ballast-glow of P-L5/L6 as dead tubes (no light), the film cabinet's nothing, the bench room's phosphor through the +X gap, the CAM 2 tally if ruled; the STORY CORNER performs here from T3 — his tally eye is DARK outside a capture (QA-35), so at night the library's only red is CAM 2's (if any). Dailies canisters must resolve at floor level (Z 35) in the dark: the errand is authored to be dared, not to be blind | CAM 2 only | CUT | lighting bible §STATES NIGHT; restoration-after-fire-chum.md §THE TALLY CONTRACT; QA-35 |
| THE TAUGHT CHASE (room-specific, once per save) | — | The first post-wake capture places him at (−500, −1600, 0); his eye burns red (the capture runs) as he crosses the aisle toward the bench gap: the library's one MOBILE red; "THE TALLY COOLS. Two doorways stand between you and anywhere. Use them." (4.0 s first cool) | his eye, lit, moving +X | — | capture_bench.gd 28–31; Data/GameText.csv 576–578; restoration-after-fire-chum.md §THE TAUGHT CHASE; I26 |
| CASCADE | **OPEN** — no circuit stamped; the reference dims globally only | — | — | panel order | scripts/cascade.gd |
| 4c | **OPEN** | Second room to black out (reverse of ENT → REC → KIT → DRM → LIB → BEN) | — | room-by-room | lighting bible 4c; player-routing Day 1 spine |
| Colour script | Day 1 warmest → Day 5 coolest; a "cool" room cools further; values OPEN | — | — | — | lighting bible §UE5 TECHNICALS |

### 3.8.4 FIXED PROPS
| Prop | Tier | Interact? | Real dims (m) | Placement (uu) | Asset candidate · licence |
|---|---|---|---|---|---|
| THE FILM CABINET (flat file, four drawers, the second proud) — the HERO | Interactable | YES — `FILM CABINET · LOCKED · the key is tagged TRAINING, in green` → `… run the 1971 orientation film (E)` [GameText 118–120] | 0.7 × 1.4 × 0.7 (reference); a real four-drawer flat file is ≈ 0.9 × 0.6 × 1.3 — **OPEN 3.8-E** | (−540, −1900, 70), drawer faces toward +Y [world_builder.gd 860–889] | Fab search "flat file cabinet vintage metal" (Fab Standard/free); painted steel under M_Enamel; the proud drawer is geometry (silhouette), its pull-marks are maps; the 16 mm print inside on a reel (M_TapeStock) |
| S1 LIBRARY LANDING (lectern, binder, chained pen) | Interactable | YES — `S1 · LIBRARY LANDING · sign the log (E) · %d line(s) left` [GameText 486] | post 0.12 sq × 0.95; top 0.5 × 0.42 tilted 0.35 rad; binder 0.36 × 0.30; pen 0.11 on a chain | (−120, −1180, 0), marker to Z 110, id text Z 150 [Data/Stations.csv; build_greybox.py 159–163] | Bespoke lectern shared with S2–S5, per-station wear; paper under M_Paper; the chain replaced twice — two chain gauges visible in maps, the pen's brass worn (ledger item) |
| Four tape stacks (uprights, 4 shelves, spines seeded) | Dressing mass (the room's body; lore host: skip cluster, mislabeled decade, reversed spine) | NO (inventory `inspect/take` → OPEN 3.8-C) | 3.0 × 2.2 × 0.42 each; spines 0.035–0.06 × 0.24–0.30 × 0.3 | (−320, −1320, 0), (320, −1320, 0) facing −Y; (−320, −1880, 0), (320, −1880, 0) facing +Y [world_builder.gd 1206–1209] | Uprights/shelves: Megascans "wood plank" or bespoke pine (the reference frame is wood, tint (0.30, 0.24, 0.17)); spines as an instanced box set with six tint variants (0.32,0.28,0.22 / 0.25,0.27,0.3 / 0.35,0.25,0.18 / 0.28,0.3,0.24 / 0.24,0.22,0.2 / 0.4,0.34,0.24) under M_TapeStock labels; accession numbers in the label albedo; deterministic per-shelf seed preserved (101–104) so "your library is your library on every load" [README.md Commit 047] |
| Dailies canisters (spawn per capture) | Pickup (event) — counted outside the I cap like doors? **OPEN 3.8-C** | YES — `DAILIES · SCENE 4 TAKE %d · pick up (E)` [GameText 79] | film can Ø0.30 × 0.04 (reference collider 0.4) | slots (−350, −1400, 35), (250, −1850, 35), (400, −1300, 35), (−450, −1900, 35), +40 X per wrap [dailies_manager.gd 5–7, 21–22] | Fab search "film canister" or Poly Haven search "film reel can" *(verify id)* CC0; label SCENE 4 TAKE n in warning red (#C23A2E is permitted on slates — a daily is a slate) |
| Card catalog (drawer G scissored card; Leland's green cross-reference cards) | Dressing (ambient lore host; inventory `operate` → OPEN 3.8-C) | NO | 60-drawer oak cabinet ≈ 1.0 × 0.45 × 1.3 | −Y wall at (−300, −2078, 0), left of the CONTROL gap | Fab search "card catalog cabinet" (Fab Standard) or Poly Haven search "drawer cabinet" *(verify id)* CC0; drawer G's card corner in the albedo at 1 m |
| Station log drawer (airdate source one of four) | Dressing (T2 inspect per inventory → OPEN 3.8-C) | NO | a drawer in S1's lectern base or a side table 0.5 × 0.4 × 0.7 | beside S1 at (−220, −1180, 0) | bespoke; logs under M_Paper |
| Leland's desk (green pens, tidy abandonment; T3 mid-sentence note) | Dressing (ambient lore host) | NO (inventory `inspect DYN` → OPEN 3.8-C) | 1.2 × 0.6 × 0.75 | +X wall at (560, −1350, 0), between the corridor and the bench gap, facing −X into the stacks ("Vess's country borders here": the bench gap is beside it) | Poly Haven `wooden_table_02` *(verify id)* CC0 or Fab search "office desk vintage"; green fine-liners (cast sheet: "green fine-liner in the margins"), a blotter, a legal pad |
| Rail ladder (creaks on a fixed note) | Dressing (inventory `operate` → OPEN 3.8-C) | NO | 2.4 m ladder on a rail | on the stack at (320, −1880) | bespoke or Fab search "library ladder" |
| 16 mm projector (plays the instructional film) | Dressing — the reference plays the film from the cabinet prompt itself | NO | as 3.2's projector | on a cart at (−440, −1980, 0) in the media alcove beside the cabinet | reuse 3.2's projector build (a second unit, same family) |
| Donations ledger (27 REELS, ANONYMOUS …) | Dressing (ambient lore host) | NO | ledger book 0.4 × 0.3 | open on Leland's desk or the card catalog top — this brief: the catalog top (−300, −2078, 130) | M_Paper (2K; not a D-series readable, so no 4K) |
| D01 LELAND'S CATALOG NOTES pages 1–3 (green ink, steno sheets) | Handled lore per the packet ("Placement: LIB compactus, page 4 inside the seance reel's box") — **not in the reference's readables** (defs: D04, D05, D09, D10, D11) | packet: prompts; code: absent — **OPEN 3.8-F** | steno sheets 0.15 × 0.23 | proposed: tucked at the top shelf of stack (−320, −1880) near the skip gap | M_Paper (4K allowed for readables); green fine-liner albedo |
| D06 HARRIET'S NOTE (the seventh signal; index card) | Handled lore — packet homes it in the FILM CABINET; the reference spawns `HarrietNote` at Godot (2.8, 0.55, 2.2) → REC ROOM (280, 220, 55) — **OPEN 3.8-G** | YES — `A FOLDED NOTE · Harriet's hand · read (E)` [GameText 218–219] | index card 0.127 × 0.076 | packet: inside the film cabinet, post-training-film gate; code: REC | M_Paper; pencil capitals per D06 spec |
| CAM 2 · STACKS camera mount (+ tally per 0-I) | Interactable (GLOBAL route/read) — counted with the coverage system, not the room | read-only | as CAM 1 | (0, −2040, 240) aimed at (0, −1200, 120) [Data/Monitors.csv], bracket on the −Y wall above the CONTROL gap header | as CAM 1 |
| Surfaces | — | — | floor 120 m² | — | Floor: Megascans "industrial concrete floor" (starter; the reference floor is scanned concrete) with a waxed lane on the cross aisle → `MI_TapeLibrary_Floor`; walls: "plaster wall painted aged" → `MI_TapeLibrary_Wall`; ceiling: "acoustic ceiling tile" with tube fixtures → `MI_TapeLibrary_Ceiling` (OPEN 0-H); stack wood → `MI_TapeLibrary_Shelf` |

### 3.8.5 LORE ITEMS
| Item | Tag | Sits | Text key | Source |
|---|---|---|---|---|
| The accession skip cluster, findable by running a finger down the spines (0118–0121 absent; W1's gap "where 0118 should be") | T5 | Stack (−320, −1880), third shelf, X ≈ −380: a gap of four spine-widths between 0117 and 0122, the gap's shelf dust undisturbed | none (QA-55); W1 text key OPEN | restoration-ambient-lore-ledger.md TAPE LIBRARY; restoration-props-packet.md D03; restoration-walkthrough-levels-endings.md ADDENDUM SPOILER |
| Card catalog drawer G: one card's corner scissored off cleanly, the cut older than the dust | T5 | The card catalog, drawer G ajar 3 cm, (−300, −2078, ≈90) | none | restoration-ambient-lore-ledger.md TAPE LIBRARY |
| A donations ledger line in Merle's hand: 27 REELS, ANONYMOUS, WATER DAMAGE, DO NOT ACCESSION, M.C., and no reels answer to it anywhere | T5, missable forever | The donations ledger, open on the catalog top | none | restoration-ambient-lore-ledger.md TAPE LIBRARY |
| One mislabeled decade (keynote) | — | A shelf-end label on stack (320, −1320) reading a decade the spines beneath contradict | none | restoration-room-bible.md TAPE LIBRARY |
| S1's pen chained; the chain replaced twice, the pen never | ritual, HC | S1 (−120, −1180) — ledgered under CORRIDOR, dressed here | none | restoration-ambient-lore-ledger.md CORRIDOR |
| D01 pages 1–3 (HANDLED per packet; absent in code) | Leland's descent | per OPEN 3.8-F | none in GameText.csv | restoration-props-packet.md D01 |
| D06 Harriet's note (HANDLED) | the seventh signal | per OPEN 3.8-G | `A FOLDED NOTE · Harriet's hand · read (E)`; `'Hold your applause.' Both hands pressed down, twice …` [GameText 218–219] | restoration-props-packet.md D06 |
| Handled L = 2 | — | D01 + D06 by the packet's homes — matches the 2/2/16 cap exactly if both are homed here | — | OPEN 0-G |

### 3.8.6 DRESSING PASSES
| # | Pass | Steps | Verification capture | Must read |
|---|---|---|---|---|
| P0 | Data check | Bounds X ±600 / Y −2100..−1100; four gaps: (0, −1100) open, (600, −1600) open, (−600, −1600) SEALED slab + reason at Z 290, (0, −2100) open; S1 marker at (−120, −1180); CAM 2 camera at (0, −2040, 240); no stand-in changes yet; resolve OPEN 0-H before ceilings | top-down (0, −1600, 1200) → (0, −1600, 0) | Exact; the four stack footprints do not intrude on the cross aisle (X ±170) or the door lanes |
| P1 | Surfaces | Concrete floor with the cross-aisle wax lane; plaster; ceiling tile; skirting; wear at all four gaps and along the aisle where the cart ran | (0, −1110, 148) → (0, −2100, 150) (from the corridor mouth down the cross aisle) | Coolest neutrals of this set; no repeat across 12 m; three-way light break |
| P2 | Fixed props | Four stacks with seeded spines (seeds 101–104), film cabinet + projector cart, S1 lectern + log drawer, card catalog, Leland's desk, rail ladder, CAM 2 mount, dailies slot markers (empty on Day 1) | (0, −1110, 148) → (−320, −1880, 110) | Spines read as a used archive (leaners, gaps); the cabinet's proud drawer reads at 3 m; the film cabinet is hero by wear (pull-marks, the one drawer that will not close) |
| P3 | Practicals + EV | Stack-end lamps P-L1..L4 + tubes P-L5/L6 with true bulbs; delete the stand-in; lock DAY EV; author NIGHT and the TAUGHT CHASE lighting (his eye as the only mobile red) as scenarios | DAY: (0, −1110, 148) → (0, −2100, 150); NIGHT: same; CHASE: (580, −1600, 148) → (−500, −1600, 300) | DAY: a chapel, pools at the stack ends, the aisle cool; NIGHT: canisters at Z 35 still resolve; CHASE: the red eye reads at 11 m down the aisle |
| P4 | Lore FIRST | The skip gap (0117 → 0122); drawer G's card; the donations ledger line; the mislabeled decade label; S1's two chain gauges; D01/D06 per 3.8-F/G rulings | 1 m closeups: (−380, −1760, 148) → the gap; (−300, −1980, 148) → drawer G; (−300, −1980, 160) → ledger line; (−120, −1080, 148) → S1 chain | All promptless except D01/D06 (handled); the gap reads only by counting; the ledger line only at 1 m |
| P5 | Dressing mass (≤ 16) | Library cart, step stool, reel boxes on the floor ends, a hygrometer card on a stack end (the vault's climate), a "RETURN REELS HERE" tray, a stack-end reading chair, a wastebasket with leader offcuts, a wall map of the accession ranges, a desk lamp on Leland's desk, a mug of green pens, a coat on the chair back, a kick-stool, a dust cover folded on the projector cart, a cardboard box of unfiled canisters (starter), a fire extinguisher (starter), a clock (OPEN 3.7-B family) | (0, −1110, 148) → (0, −2100, 150) | ≤ 16; each owned; density never hides the skip gap or the cabinet |
| P6 | Wear/decals/drift | Cart-wheel lanes, hand wear on stack uprights at Z 100–130, dust gradients on upper shelves; drift hook: ONE spine reversed (dressing, monotonic, day-driven) — the stacks themselves never move (OPEN 3.8-D) | Day 1 vs Day 3 pair from (0, −1110, 148) → (−320, −1320, 110) | Exactly one spine reversed in the second frame |
| P7 | QA + acceptance | QA-55 (prompts: film cabinet, S1, dailies, D01/D06 as ruled; nothing else), QA-56 (drift = one spine), QA-57 (hero = film cabinet) | §3.8.7 | §3.8.7 |

### 3.8.7 ACCEPTANCE CAPTURE
- Camera A (the chapel): **(0, −1110, 148) → look-at (0, −2100, 150)**, DAY ON AIR, Day 1 post volume — S1 at left, the cross aisle, CAM 2 at the far end.
- Camera B (CAM 2's own frame): **(0, −2040, 240) → look-at (0, −1200, 120)**, vertical FOV 65° per Monitors.csv, NIGHT — the aisle as the bench room sees it; this is the poisoned-well frame.
- Camera C (the media alcove): **(−400, −1700, 148) → look-at (−540, −1900, 70)**, DAY.
- Checklist: (1) cool practicals with stack-end pools; (2) one hero (film cabinet) by wear; (3) the skip gap findable by counting, unflagged; (4) drawer G and the donations line present and promptless; (5) at NIGHT canisters at floor level resolve; (6) spines are instanced boxes with label maps, no naked primitive on uprights (bevelled); (7) store-page test.

### 3.8.8 OPEN
- **3.8-A** The CONTROL gap (0, −2100) has no leaf to carry the demo's SEALED reason though CONTROL is not in DemoOpen.csv.
- **3.8-B** The crate's home: library ("lives deep"), bench (inventory), entry (code).
- **3.8-C** Interactable count: cap 2/2/16 vs inventory §6 (ten touchables). This brief: I = film cabinet + S1; dailies are event pickups; everything else promptless. Owner to confirm, especially the compactus and card catalog (`operate`).
- **3.8-D** The compactus: static stacks in the data; the crank (SCARE 4) is a mechanics unit, not dressing.
- **3.8-E** Film cabinet scale: reference 0.7 × 1.4 × 0.7 vs a real flat file.
- **3.8-F** D01's home and its absence from the reference readables.
- **3.8-G** D06's home: film cabinet (packet) vs REC ROOM (code).
- **0-H, 0-I** as in §0.3.

---

## 3.9 · BENCH ROOM — Rita's altar; the game's heart at 9,-16

### 3.9.1 IDENTITY
| Field | Value | Source |
|---|---|---|
| Rooms.csv | `BENCH ROOM, 9.0, -16.0, 6.0, 6.0` → centre (900, −1600), 6 × 6 m — "the game's heart at 9,-16" is this row | Data/Rooms.csv; restoration-room-bible.md BENCH ROOM |
| Floor bounds (uu) | X 600..1200, Y −1900..−1300, floor top Z 0, wall top Z 300 | derived |
| Door → TAPE LIBRARY | OPEN gap (600, −1600), 1.4 m (Y −1670..−1530) in the −X wall; no slab; Merle's DOORWAY mark (600, −1640, 0) stands in it | Data/Doors.csv; scripts/merle.gd 9 |
| Door → CLIMATE | `BENCH ROOM, CLIMATE, 12.0, -16.0, 1.4, z,` → OPEN gap (1200, −1600), 1.4 m in the +X wall; no slab | Data/Doors.csv |
| Stations / Monitors | none / **CAM 2 · STACKS monitor** at (720, −1318, 170), yaw 0 (facing −Y into the room), on the +Y wall 18 cm inside; CRT shell ≈ 1.88 × 1.48 × 0.99 m around a 1.6 × 1.2 m screen — **OPEN 3.9-A** scale truth (a 1.6 m screen is not a 1970s monitor; canon says "monitor bank") | Data/Monitors.csv; monitor_rig.gd 32–51; prop_kit.gd `crt_shell` |
| Demo | open (the demo's last room: Tape 1's capture ends the demo here) | Data/DemoOpen.csv; scripts/capture_bench.gd 60–62 |
| Reference placements (Godot → UE) | THE BENCH (`CaptureBench`) at (9.0, 0.5, −17.6) → **(900, −1760, 50)**: collision 1.8 × 1.0 × 0.8; top slab 1.8 × 0.08 × 0.8 with its surface at **Z 100**; four legs 0.08 sq × 0.92 at X ±80, Y ±30 from centre; REEL DECK 0.72 × 0.5 × 0.16 standing on the top at (8.55, 1.28, −17.8) → **(855, −1780, 128)**, two reels Ø0.26 that spin while tape rolls (supply and take-up at different speeds), four transport buttons; label THE BENCH at Z 160 · BENCH TV (`BenchTV`, the capture screen) at (9.0, 1.55, −18.82) → **(900, −1882, 155)** on the −Y wall facing +Y: screen quad 1.7 × 1.28 in a CRT shell; red slate text at Z 69 · GEN KNOB at (10.2, 1.0, −18.5) → **(1020, −1850, 100)**: brass cylinder Ø0.20 × 0.12; states MASTER / 1ST DUB / 3RD GEN · 1977 DOCK (`FireTapeDock`, non-demo) at (7.8, 0.9, −18.4) → **(780, −1840, 90)** · SEANCE REEL (`SeanceDock`, non-demo) at (7.8, 0.9, −17.2) → **(780, −1720, 90)**; MAX_FRAME 40 · SPECTROGRAM (`SpectroDock`, non-demo) at (10.6, 0.9, −17.2) → **(1060, −1720, 90)** · ASSET RACK at (9.0, 2.35, −18.82) → **(900, −1882, 235)**: plank 2.2 × 0.05 × 0.3 with four berths VERSE · CART · SCRIPT · CARD at X 810, 870, 930, 990; a canister lands as each asset banks · ACCESSION LEDGER (`DecisionLedger`, non-demo) at (8.2, 0.9, −16.2) → **(820, −1620, 90)** · LEDGER MARGIN (`CreditEntry`) at (7.4, 0.9, −15.2) → **(740, −1520, 90)** · WOOL SPIKE 001 at (10.8, 0, −14.3) → **(1080, −1430, 0)**: plinth 0.7 × 0.5 × 0.7, wool sphere r 0.28 at Z 80, head r 0.20 at Z 118 — a SHADER TEST OBJECT, not canon dressing (**OPEN 3.9-B**) · every dock is a `_dock_body` (§0.2) floating with its plinth bottom at Z ≈ 63 (**OPEN 0-J**) · stand-in lamp (900, −1600, 275), range 4.5 m / 9.0 cd attenuation 450 uu | world_builder.gd `_spawn_bench` 327–406, `_spawn_assets_and_decision` 1009–1022, `_spawn_club` 1056–1059, `_spawn_wool_spike` 409–447; prop_kit.gd `reel_deck` 294–322; scripts/bench_tv.gd 17–35; scripts/asset_rack.gd 5–36; scripts/capture_bench.gd 43–45; scripts/gen_knob.gd 5 |
| Merle's marks | KETTLE (800, −100, 0) by day; CHAIR (260, 120, 0) by night; DOORWAY (600, −1640, 0) "saying nothing, when the pen is up" — the doorway is the LIBRARY gap of this room | scripts/merle.gd 3–9, 35; QA-11 |
| Adjacent | TAPE LIBRARY (−X), CLIMATE (+X); the +Y wall (Y −1300) and −Y wall (Y −1900) face void | Data/Rooms.csv |

### 3.9.2 ROLE
| Aspect | Canon | Source |
|---|---|---|
| Personality | "Rita's altar; the game's heart at 9,-16. Task lamp truth over the bench, warm elsewhere." Bed: machine idle, tape whisper at speed. Keynotes: THE BENCH, the decision LEDGER with D03, splice tools in surgical order | restoration-room-bible.md BENCH ROOM |
| Budget | 3 / 1 / 8; **drift: none here ever (trust law: the altar is stable)**; web: everything routes through this room's verbs | restoration-room-bible.md BENCH ROOM; PROGRESS.md 3.9 |
| Hero room | Render order #1: "BENCH: the altar. Paper stock and ledger green dominate; one warm task lamp; the monitor is the room's only saturated light; the asset rack reads amber against dust." Plate the hero rooms first: "1) BEN (the star, warmest light, densest craft)" | restoration-art-bible.md §7; restoration-room-inventory.md RENDER ORDER |
| Dread role | THE CAPTURE SCARE lives here ("Chum's face arriving at lens distance … fires on every capture"); L4 PROXIMITY UNDER CONTRACT: "The tally: safety that is visible, absolute, and expiring on a clock the player can read. He crosses the room BECAUSE you are safe"; MUNDANITY: "paperwork against wrongness; the accession form is the flashlight"; "the bench turns watching into work and work into exposure, and every capture session is a small screening with an audience of one" | restoration-walkthrough-levels-endings.md Part IV; restoration-dread-doctrine.md L4, AMPLIFIERS; restoration-design-doc.md Part IV §1 Capture |
| Sanctuary | "Where a Capture Cannot Happen: … the bench during capture sessions"; "the bench room is the most mediated, safest-feeling space in the compound, on purpose"; I23 NO STRIKE WHILE LIT; the tally contract: he may approach to 1.2 m and may not strike; the cool is 2.0 s (4.0 s once, the taught chase) | restoration-walkthrough-levels-endings.md Part V-B, Part II; restoration-invariant-suite.md I23, I26; THE-LAWS.md 10 |
| Beats | T1.3 THE PROVING: "The bench: capstans, scopes, the TBC, the accession ledger squared to the desk edge. Merle sets down a battered reel." · T1.5 CAPTURE ONE: forced real time; the waveform wrong for a third-generation dub; the loupe swings; SCARE 1 the in-tape lunge (the game's only startle, delivered on THIS screen) · T2.6 CAPTURE TWO: colour where the logs say black and white; the spectrogram's sidebands → ASSET 1 THE MISSING VERSE · T3.4 THE FIRE TAPE: forced watch, no sting; M1 THE SECOND VIEWING at this dock ("MERLE, from the doorway: 'I was there the first time …'"; E let her stay / Q turn her away; the kettle two rooms away clicks off) · T4.4 LELAND: the frame-séance opens; five questions on the bench pad; every pass wears the only copy · T5.2 THE DECISION POINT: "The ledger open. Three entries possible in her hand: AUTHENTICATE. DESTROY. PERFORM. Merle in the doorway, hands empty, watching the pen, saying nothing. The scene has no music." · Ending 3 and Ending 4 both end at this bench ("Rita at her own bench, watching the archive die, reel by reel") | restoration-game-master.md T1.3, T1.5, T2.6, T3.4, T4.4, T5.2, ENDING 3, ENDING 4; Data/GameText.csv 130–142, 276–280 |
| Texts (prompts) | `THE BENCH · begin capture, Tape %d (E) · runs real time` / `TAPE ROLLING · stay with it` / `CAPTURE · TAPE %d · 00:%05.2f` / `CAPTURE ABORTED · the take is lost. The bench keeps no half-truths.` · `GEN KNOB · showing %s · cycle (E)` / `GEN SET · the picture agrees to look %s. The scope still reads MASTER.` · `DOCK · 1977 · thread the fire tape (E)` / `… watch it again (E)` · `SEANCE REEL · the impossible tape · open (E)` / `SEANCE REEL · close (E) · Z back · X forward` (+ ` · Q feed the fire tape into the wake` / ` · SPACE the pad has room for a sixth line`) · `SPECTROGRAM · pull the sidebands (E)` / `… needs a captured tape first` / `… the verse is banked` · `ACCESSION LEDGER · take up the pen (E)` / `… three entries possible · the decision ripens Day 3` / `LEDGER · pen over: %s · E next · SPACE commit` / `… entry stands: %s · the ink does not entertain appeals` · `LEDGER MARGIN · credit the insight (E) · 'per V. Keys'` · HUD while recording: `● REC · SAFE WHILE LIT · %04.1f` · `TBC · %s · toggle with T anywhere` · the wake caption: `It stands at the edge of the bench light. Eleven feet of salvage, watching the tally. The jaw hand moves. Nothing else does.` | Data/GameText.csv lines 48, 47, 49, 50, 191–192, 129, 128, 609, 608, 606–607, 636, 635, 634, 87, 86, 88, 85, 65, 225, 232, 576 |
| Timings | CAPTURE_SECONDS 12.0; TETHER 4.0 m (leave the bench → abort); AF approach 0.8 m/s, loom 1.2 m, cool 2.0 s, fold 2.2 s | Data/Timings.csv capture_bench.gd, rundown.gd |
| Sound | Bed: machine idle, tape whisper at speed; S07 capture transport (reel motor start, 12 s bed, stop clunk; abort adds a tape-slap); S23 REC SYNC HUM "faint mains alignment while the tally burns"; S22 OCCLUSION PRESENCE under 3 m; the degausser's coil is audible from CLIMATE (reach 10 m from (1425, −1760): the bench is 5.3 m away) — Merle: "The degausser hums at night. I hear it too."; the strike is nearly silent | restoration-audio-bible.md S07, S22, S23; world_builder.gd 848–854; Data/GameText.csv 498; AAA_BUILD_PLAN.md §1 AUDIO LAW |
| Trust law | INTERACTABLES never drift; the bench room's drift is "none here ever"; ambient lore here "is static and quiet, because the altar tells the truth by not changing" | restoration-object-taxonomy.md ¶INTERACTABLES; restoration-ambient-lore-ledger.md BENCH ROOM |
| Route | The pendulum's fourth stop; Day 1 order ENT → REC → KIT → DRM → LIB → BEN puts BEN LAST, so in 4c the bench room goes dark FIRST | restoration-player-routing.md §1, Day 1 spine; restoration-lighting-bible.md 4c |
| Inventory listing | §8 (13 rows): tape transport + capstans (operate), bake oven (operate; Destroy tool from T4), splice block/blades/leader (operate), TBC unit (operate), waveform + vector scopes (inspect), audio bench + spectrogram (T2 operate), jog/shuttle wheel (operate; séance verb T4), monitor bank (inspect), accession ledger (commit/sign), bench notepad (T4 write), asset shelf (DYN inspect), Craik's finale script (T3 inspect), glove box + lamp (use) — reconciled against 3/1/8 in OPEN 3.9-C | restoration-room-inventory.md §8 |
| Interactables in code | THE BENCH, GEN KNOB, 1977 DOCK, SEANCE REEL, SPECTROGRAM, ACCESSION LEDGER, LEDGER MARGIN = seven prompting objects vs cap I = 3 — all routing-critical (assets, endings, the séance). **OPEN 3.9-C** is the largest cap breach in the twenty rooms; this brief keeps every reference prompt and names THE BENCH the hero | world_builder.gd; restoration-object-taxonomy.md ¶QA HOOKS QA-57 |
| Kettle geography | "The kettle, two rooms away, clicks off by itself" is spoken at this dock; by Rooms.csv the kitchen is four rooms from the bench (BEN → LIB → CORRIDOR → REC → KIT) — **OPEN 3.9-D** (a line, not a layout, may be what changes) | Data/GameText.csv 141–142; Data/Rooms.csv |

### 3.9.3 LIGHTING STATE TABLE
| State | Locked EV | Practicals | Red reads? | Transition | Source |
|---|---|---|---|---|---|
| DAY ON AIR | **OPEN** | P-B1 THE TASK LAMP: one articulated bench lamp clamped to the bench's −Y edge at ≈ (990, −1795, 100) with its head over the splice area at ≈ (960, −1760, 150), true bulb, warm tungsten, the room's TRUTH light ("task lamp truth over the bench") · P-B2 one amber overhead "warm elsewhere", proposed (900, −1550, 290) over the ledger side · the BENCH TV screen (M_Phosphor) = "the room's only saturated light" — data, never room light · the CAM 2 monitor's phosphor likewise · the asset rack "reads amber against dust" by reflected task light, not its own | No camera tally in the room. While a CAPTURE runs the HUD carries `● REC · SAFE WHILE LIT`; whether the reel deck carries a physical red tally lamp is **OPEN 3.9-E** (the reference deck has four buttons and no lamp; the doctrine's "his eye's light and the contract are the same fact" makes HIS eye the red) | CUT | restoration-room-bible.md BENCH ROOM; restoration-art-bible.md §7 BENCH; restoration-lighting-bible.md §GRAMMAR; THE-LAWS.md 10 |
| CAPTURE (room-specific; 12.0 s, every capture) | **OPEN** (same as DAY — the room does not change; the screen does) | The TV plays the tape (phosphor content only, grain on the screen and nowhere else); the reels turn; after the wake HIS TALLY EYE burns red at ≈ Z 300 as he approaches to 1.2 m — the only red in the room, mobile, at head height above Rita's eye (148): "at loom distance the player is looking up into it" | HIS EYE, lit | — | restoration-after-fire-chum.md §THE TALLY CONTRACT, §THE SCALE LAW; QA-34, QA-35; restoration-art-bible.md §2 (no grain on compound surfaces) |
| THE TALLY COOLS (2.0 s; 4.0 s once) | — | His eye goes dark the instant the capture ends (QA-35); the task lamp is now the only authored light between Rita and him | red → none | instant | QA-35, QA-36; Data/GameText.csv 577–578 |
| BREAK | **OPEN** | Same; no tally here | — | — | OPEN 0-F |
| NIGHT | **OPEN** | Practicals off; the TV's standby (a dot, not a glow); the CAM 2 monitor's phosphor showing the dark library; the degausser's coil-glow through the +X gap (3.10); Ending 3/4 nights are worked at this bench under the task lamp alone ("You work through the night. Reel by reel. Entry by entry.") — so the task lamp is the one practical that may stay on at night: **OPEN 3.9-F** | CAM 2 monitor phosphor | CUT | restoration-lighting-bible.md §STATES NIGHT; Data/GameText.csv 276–280 |
| THE DECISION POINT (T5 Phase 1) | **OPEN** | Same as DAY; Merle a silhouette in the LIBRARY gap at (600, −1640) against the library's cool; "The scene has no music. The pen is the loudest thing in the building." | — | — | restoration-game-master.md T5.2; scripts/merle.gd 9 |
| CASCADE | **OPEN** | — | — | panel order | scripts/cascade.gd |
| 4c | **OPEN** | FIRST room to black out in the reverse tour | — | first CUT of the sequence | lighting bible 4c; player-routing Day 1 spine |
| Colour script | Day 1 warmest; OPEN | — | — | — | lighting bible |

### 3.9.4 FIXED PROPS
| Prop | Tier | Interact? | Real dims (m) | Placement (uu) | Asset candidate · licence |
|---|---|---|---|---|---|
| THE BENCH with the reel deck — the HERO | Interactable | YES — `THE BENCH · begin capture, Tape %d (E) · runs real time` [GameText 48] | top 1.8 × 0.8 at 1.0 high (reference); a real bench is 0.9 high — keep 1.0 (Rita's eye 1.48 looks down at the deck); deck 0.72 × 0.5 × 0.16, reels Ø0.26 | (900, −1760, 50) centre, top at Z 100; deck at (855, −1780, 128) [world_builder.gd 329–357] | Bespoke (Blender factory): hardwood top with the worn edge (affordance is wear — the bench's "worn edge" is the taxonomy's own example), steel legs, a 2-inch quad transport as the deck (CC0 donor: Poly Haven search "reel to reel" *(verify id)*; else bespoke); reels animatable; brushed metal under the metal family, no naked cylinder caps (§R.1) |
| BENCH TV (capture screen, 4:3) in a CRT shell | Interactable in spirit (the screen the capture plays on) — no prompt of its own | NO prompt | reference screen 1.7 × 1.28 — **OPEN 3.9-A**: a period broadcast monitor is ≈ 0.5 m; keep the 4:3 ratio and shrink, or keep the reference size as a wall-mounted rear-projection cabinet? | (900, −1882, 155) on the −Y wall facing +Y [world_builder.gd 368] | Fab search "broadcast monitor vintage" / "CRT monitor 70s"; screen under M_Phosphor; red slate text as a diegetic character-generator line under the screen (Z 69) |
| GEN KNOB | Interactable | YES — `GEN KNOB · showing %s · cycle (E)` [GameText 191] | Ø0.20 × 0.12 (reference; a real rotary switch is Ø0.05) — scale OPEN with 3.9-A | (1020, −1850, 100) — on the bench top's +X end (the bench top spans X 810..990 — the knob at X 1020 sits 3 cm PAST the bench edge in the reference; PROPOSED: on a side rack at (1020, −1850, 100)) | Bespoke brass knob with an index dot (prop_kit `knob`); MASTER · 1ST DUB · 3RD GEN engraved in maps |
| 1977 DOCK (the fire tape's dock) | Interactable | YES — `DOCK · 1977 · thread the fire tape (E)` [GameText 129] | dock body 0.45 × 0.4 × 0.45 on a 0.55 plinth | (780, −1840, 90) [world_builder.gd 394] — floating; PROPOSED on a second bench/table (see "The side table") | Bespoke cased transport (a second, older machine); brass plaque 1977 DOCK |
| SEANCE REEL dock | Interactable | YES — `SEANCE REEL · the impossible tape · open (E)` [GameText 609] | as above; the impossible tape's box holds D01 page 4 (packet) | (780, −1720, 90) [world_builder.gd 399] | Bespoke; a jog/shuttle wheel on its face (the séance verb); the legal-pad frames appear on the BENCH TV |
| SPECTROGRAM dock (the audio bench) | Interactable | YES — `SPECTROGRAM · pull the sidebands (E)` [GameText 636] | as above | (1060, −1720, 90) [world_builder.gd 1013] | Bespoke: a spectrum analyser with a phosphor trace (M_Phosphor), waveform + vector scopes beside it ("THE SCOPE READS MASTER") |
| ACCESSION LEDGER (D03; the decision point) | Interactable + handled lore | YES — `ACCESSION LEDGER · take up the pen (E)` [GameText 87] | ledger book 0.45 × 0.35 open; "squared to the desk edge" | (820, −1620, 90) [world_builder.gd 1020] — PROPOSED: on THE DESK (below) | Green-columned bookkeeping stock under M_Paper (4K allowed: a readable); multiple hands across decades; the 0118–0121 absence; the green 0299 line [restoration-props-packet.md D03] |
| LEDGER MARGIN (credit entry) | Interactable | YES — `LEDGER MARGIN · credit the insight (E) · 'per V. Keys'` [GameText 65] | the same ledger's margin (a second dock in code) | (740, −1520, 90) [world_builder.gd 1057] — PROPOSED: merged onto THE DESK's ledger as a second hotspot; the two docks are one object in fiction | as D03 |
| THE DESK (carries the ledger, the margin, the notepad; Rita's paperwork) — PROPOSED | Dressing (collision) | NO | 1.4 × 0.7 × 0.75 | (790, −1580, 0) against the −X wall between the gap and the +Y corner, so Merle in the doorway (600, −1640) watches the pen from 2 m | Poly Haven `wooden_table_02` *(verify id)* CC0 or Fab search "writing desk vintage"; resolves OPEN 0-J for the ledger docks |
| The side table (carries the 1977 dock, the séance dock, the spectrogram) — PROPOSED | Dressing (collision) | NO | 3.0 × 0.6 × 0.75 along Y | (780, −1780, 0) for the two −X docks; (1060, −1720, 0) a second 0.8 × 0.6 stand for the spectrogram | steel lab bench (Fab search "workbench metal"); resolves OPEN 0-J |
| ASSET RACK (four berths) | Dressing (DYN: canisters land) | NO (inventory `inspect` → OPEN 3.9-C) | plank 2.2 × 0.3; canisters Ø0.3 | (900, −1882, 235) above the TV [world_builder.gd 1017] | pine plank + steel brackets; labels VERSE · CART · SCRIPT · CARD in stencil (amber #C9A33D-adjacent when banked, dust when not — the reference tints the label amber when held) |
| Splice tools in surgical order (block, blades, leader, burnisher, swabs, isopropyl, cotton gloves, the 10× loupe) | Dressing (inventory `operate` → OPEN 3.9-C); the seven of Rita's tools | NO | a tray 0.5 × 0.3 | on the bench top at (930, −1740, 100) under the task lamp | Bespoke small props; "her gloves are the whitest object in the game" — M_Paper-white cotton, no tint; the splice block as brass on hardwood [restoration-cast-sheets.md RITA] |
| TBC unit | Dressing-tier device (T toggles anywhere: `TBC · %s · toggle with T anywhere`) | NO prompt | 19-inch rack unit 0.48 × 0.09 × 0.4 | in the side rack at (1020, −1800, 60) | rack unit with one phosphor readout |
| Bake oven (Destroy-path tool) | Dressing (inventory `operate`; not in code) → OPEN 3.9-C | NO | lab oven 0.6 × 0.6 × 0.7 | +X wall at (1150, −1400, 0) | Fab search "laboratory oven" / "industrial oven small"; enamel under M_Enamel |
| CAM 2 · STACKS monitor | Coverage endpoint (GLOBAL read) | per port | CRT shell ≈ 1.88 × 1.48 (OPEN 3.9-A) | (720, −1318, 170) yaw 0 [Data/Monitors.csv] | as the corridor rigs; M_Phosphor |
| WOOL SPIKE 001 | **Not dressing** — a shader test (`WOOL SPIKE 001` label) | — | — | (1080, −1430, 0) in the reference | **OPEN 3.9-B**: remove from the dressed room, or keep as the sodium-check swatch on a plinth (art bible §3: "the wool spike shader is the interim standard … retires per surface") |
| Surfaces | — | — | floor 36 m² | — | Floor: Megascans "industrial concrete floor" (reference concrete) with an anti-fatigue mat at the bench → `MI_BenchRoom_Floor`; walls: painted plaster, neutral, with a LEDGER-GREEN (#596B52) painted dado/wainscot to Z 100 ("paper stock and ledger green dominate") → `MI_BenchRoom_Wall`, `MI_BenchRoom_Dado`; ceiling: acoustic tile → `MI_BenchRoom_Ceiling` (OPEN 0-H) |

### 3.9.5 LORE ITEMS
| Item | Tag | Sits | Text key | Source |
|---|---|---|---|---|
| D03 ACCESSION LEDGER (HANDLED): 0117 GLADHOUSE 22 … 0118–0121 absent … 0122 "per V. Keys the skip cluster begins here" … in green, older, small: 0299, UNLABELED, DO NOT BENCH, L.M. | the paper economy's altar; the decision point's stage | The desk, (820, −1620, ≈78) | `ACCESSION LEDGER · take up the pen (E)` and the ledger's commit lines [GameText 82–89] | restoration-props-packet.md D03; Data/GameText.csv |
| Under the bench lip, scratched shallow where only a cleaner's hand would find it: L.M. | T3 | The bench top's underside lip at the −Y edge, (900, −1800, 96); found by crouching (crouch camera lowers 0.6 m — the body verb's "honest job: peeking") | none (QA-55) | restoration-ambient-lore-ledger.md BENCH ROOM; restoration-gap-audit.md ruling 2 |
| The splice blade log: blades changed weekly for years, then a four-month gap in 1977, then weekly again in a different hand | HF, T6 | A clipboard hung on the −Y wall beside the TV at (1080, −1898, 150) | none | restoration-ambient-lore-ledger.md BENCH ROOM |
| Craik's finale script (Asset 4, T3 readable after retrieval): "Typed, hand-amended. The margin, pressed hard: 'No. Tell them the truth or it doesn't take.'" | asset | Lands in the rack's SCRIPT berth (930, −1882, 223) | `the finale script` / flavour line [GameText 687–688] | restoration-room-inventory.md §8; world_builder.gd 1032–1039 |
| Handled L = 1 | — | D03 exactly (the cap fits) | — | OPEN 0-G |

### 3.9.6 DRESSING PASSES
| # | Pass | Steps | Verification capture | Must read |
|---|---|---|---|---|
| P0 | Data check | Bounds X 600..1200 / Y −1900..−1300; two open gaps (600, −1600) and (1200, −1600); CAM 2 monitor spot (720, −1318, 170); the seven interactable spawn points; the wool spike (decide OPEN 3.9-B before P2); resolve OPEN 0-H before ceilings | top-down (900, −1600, 900) → (900, −1600, 0) | Exact; nothing moved — the altar's positions are the reference's |
| P1 | Surfaces | Concrete floor with the mat; plaster + ledger-green dado; ceiling tile; skirting; wear at both gaps and a worn arc where the stool turns | (620, −1600, 148) → (900, −1760, 100) | Paper and green dominate; three-way light break; the floor around the bench is the most worn floor in the game |
| P2 | Fixed props | Bench + deck, TV, knob (+ side rack), the desk with the ledger, the side table with the three docks, asset rack, splice tray, TBC, oven, CAM 2 monitor; remove or re-home the wool spike per 3.9-B | (620, −1600, 148) → (900, −1760, 100) | Nothing floats (0-J closed for this room); the bench is hero by wear (the worn edge, the polished transport buttons); the deck's reels read as machined steel at 1 m |
| P3 | Practicals + EV | P-B1 task lamp with true bulb over the splice area; P-B2 overhead; TV and CAM 2 screens under M_Phosphor as emissive data only; delete the stand-in; lock DAY EV; author CAPTURE (screen on) and NIGHT (task lamp per 3.9-F) as scenarios | DAY: (620, −1600, 148) → (900, −1760, 100); CAPTURE: (900, −1660, 148) → (900, −1882, 155) (Rita's working view, screen on); NIGHT: same as DAY | DAY: one truth pool, warm elsewhere, the screen the only saturation; CAPTURE: grain on the screen only, none on the bench; NIGHT: the floor resolves by the task lamp alone if 3.9-F rules it on |
| P4 | Lore FIRST | D03 open on the desk at the 0117/0122 spread with the green 0299 line; the L.M. scratch under the lip (normal map, 1 mm depth, roughness only); the blade log clipboard | 1 m closeups: (700, −1620, 148) → D03; crouched (900, −1700, 88) → the lip; (1000, −1800, 148) → clipboard | D03 prompts inside 2.6 m; the scratch and the log never prompt; the scratch is invisible standing |
| P5 | Dressing mass (≤ 8) | A stool, the club's grading rubric sheet pinned by the TV, a box of reel boxes labelled in three hands, a pegboard of leader spools, a dust cover folded on the oven, a desk lamp on the desk (secondary, unlit by day), a wall calendar, a wastebasket of leader offcuts | (620, −1600, 148) → (900, −1760, 100) | ≤ 8; each owned by Rita's or Leland's habits; the room reads as a conservator's, not a hobbyist's |
| P6 | Wear/decals | Coffee ring on the desk (Leland's), glove-cotton lint on the bench, tape-oxide smear under the deck heads, a worn arc under the stool. **NO DRIFT HOOKS: the altar never changes** | Day 1 vs Day 5 pair from (620, −1600, 148) → (900, −1760, 100) | IDENTICAL frames except the rack's banked canisters and Harriet-unrelated state; any other delta is a QA-56 defect |
| P7 | QA + acceptance | QA-55 (prompts: the seven reference interactables + D03; nothing else), QA-56 (zero drift instances), QA-57 (hero = THE BENCH; flag the cap breach 3.9-C in the PR) | §3.9.7 | §3.9.7 |

### 3.9.7 ACCEPTANCE CAPTURE
- Camera A (the altar, hero plate #1): **(620, −1600, 148) → look-at (900, −1760, 100)**, DAY ON AIR, Day 1 post volume — bench, deck, TV, rack, task lamp in frame; this is the art bible's first plate [restoration-art-bible.md §7, §10 P0 "the five hero plates"].
- Camera B (the working view, CAPTURE): **(900, −1660, 148) → look-at (900, −1882, 155)**, CAPTURE state, screen playing bars, HUD off for the plate.
- Camera C (the decision point): **(1180, −1600, 148) → look-at (820, −1620, 78)** from the climate gap across the room to the desk, with the library gap at (600, −1640) in frame where Merle stands — DAY, T5 Phase 1.
- Checklist: (1) one warm task lamp is the truth light, the screen the only saturation; (2) the bench is hero by wear; (3) D03 findable, green line legible at 1 m; (4) L.M. under the lip invisible standing, findable crouched; (5) nothing floats; (6) no grain anywhere off the screens; (7) store-page test.

### 3.9.8 OPEN
- **3.9-A** Screen scale: the reference bench TV (1.7 × 1.28 m) and CAM 2 monitor (1.6 × 1.2 m) are wall-sized; canon says "monitor bank". Shrink to period size and add a bank, or keep?
- **3.9-B** WOOL SPIKE 001 is a shader test object standing in the dressed room.
- **3.9-C** Interactable count: cap 3/1/8 vs seven prompting objects in the reference (all routing-critical) and thirteen inventory rows. The cap or the code must move; this brief keeps the code.
- **3.9-D** "The kettle, two rooms away" vs four rooms by Rooms.csv.
- **3.9-E** Is there a physical tally lamp on the deck, or is his eye the only red (doctrine says the eye)?
- **3.9-F** Does the task lamp stay on at NIGHT (the Burn and Dead Air epilogues are worked at night at this bench)?
- **0-H, 0-J** as in §0.3.

---

## 3.10 · CLIMATE — the building's lungs

### 3.10.1 IDENTITY
| Field | Value | Source |
|---|---|---|
| Rooms.csv | `CLIMATE, 14.25, -16.0, 4.5, 6.0` → centre (1425, −1600), 4.5 × 6 m, long axis Y | Data/Rooms.csv |
| Floor bounds (uu) | X 1200..1650, Y −1900..−1300, floor top Z 0, wall top Z 300 | derived |
| Door → BENCH ROOM | OPEN gap (1200, −1600), 1.4 m (Y −1670..−1530) in the −X wall; no slab | Data/Doors.csv |
| Door → TRANSMITTER HALL | `CLIMATE, TRANSMITTER HALL, 14.5, -13.0, 1.4, x,` → OPEN gap (1450, −1300), 1.4 m (X 1380..1520) in the +Y wall; no slab, no leaf — the hall (Y −1300..0) opens directly off the climate room's +Y wall. In the demo the hall is closed ("SEALED · you can hear it from here. That is enough for today.") but only doors with a `kind` carry reasons — **OPEN 3.10-A** (this gap has none) | Data/Doors.csv; world_builder.gd 262–264; Data/GameText.csv 661 |
| Stations | none inside. **S4 TRANSMITTER THRESHOLD** at Godot (14.5, 0, −11.4) → **(1450, −1140, 0)** stands 1.6 m PAST the +Y gap, inside the TRANSMITTER HALL, on the gap's axis — visible from anywhere on the climate room's centreline; the pre-signed page (T3.6) is signed there | Data/Stations.csv; restoration-game-master.md T3.6 |
| Monitors | none | Data/Monitors.csv |
| Demo | **NOT** in DemoOpen.csv | Data/DemoOpen.csv |
| Reference placements (Godot → UE) | THE DEGAUSSER (`Degausser`) at (14.25, 0.55, −17.6) → **(1425, −1760, 55)**: housing 1.2 × 0.9 × 0.8 (Z 0..90), collision 1.2 × 1.1 × 0.8; exposed COIL RING (torus, inner r 0.18, outer r 0.30) on top at **Z 97**; OCHRE HAZARD STRIPE 1.22 × 0.10 × 0.82 at Z 70; label DEGAUSSER at Z 160; a ToneEmitter at 120/240 Hz, noise 0.05, −16 dB, reach 10.0 m (S02's stand-in) · stand-in lamp (1425, −1600, 275), range 4.5 m / 9.0 cd attenuation 450 uu | world_builder.gd `_spawn_burn_loop` 809–855, 162–170; build_greybox.py 116–126 |
| Adjacent | BENCH ROOM (−X), TRANSMITTER HALL (+Y); the +X wall (X 1650) and −Y wall (Y −1900) face void. The hall's hum emitter at (1675, −650, 160) (55/110 Hz, −8 dB, reach 26 m) is ≈ 9.8 m from the room centre — audible here, filtered | Data/Rooms.csv; world_builder.gd 918–926; restoration-audio-bible.md S01 |

### 3.10.2 ROLE
| Aspect | Canon | Source |
|---|---|---|
| Personality | "The building's lungs. Green gauge glow, grille shadows." Bed: the deepest hum, compressor cycles. Keynotes: gauges with handwritten ranges, filter log ending mid-1977 | restoration-room-bible.md CLIMATE |
| Budget | 1 / 1 / 6; drift: one needle's rest point; web: the hum settles a cent flat when ritual holds (B-R1) | restoration-room-bible.md CLIMATE; PROGRESS.md 3.10; restoration-reaction-matrix.md THE BUILDING |
| Function | The vault's climate plant (the tape library's HVAC) and the erasure machine: "Burns dailies (strike removal) and, on the Destroy path, the archive; humming coil, felt-lined throat"; reel racks hold the nightly retrieval objectives ("the errand that bait the T3 chase"); bake supplies feed the bench oven | restoration-room-inventory.md §7 |
| Dread role | THE ERRAND: "Every death therefore generates a dangerous optional errand: retrieve the footage of your own death, at night, under the Rundown, or live with the strike … burning them also resets its read on your habits" — the errand ends HERE; "CLM reel runs (nightly): PRESERVE route coverage first, slow; ASK Vess fetches; FORCE sprint it dark" | restoration-walkthrough-levels-endings.md Part V-B Burn Your Dailies; restoration-game-master.md Appendix B "CLM reel runs" |
| Beats | Night 5 spine: "objective: retrieve the next reel from CLM. Route DRM → REC → LIB → CLM. On the return leg, the you're-on … the compactus chase" · every capture: `CARRYING · SCENE 4 TAKE %d. The degausser is in the climate room.` → `BURNED · TAKE %d. Her name fades from the line. Its read on you resets.` (or `… The sheet was already clean. The canister burns anyway.`) · Ending 3 THE BURN: "BEN → CLM (the degausser) with the masters, plus the bake oven for the film elements → Phase 1 ledger entry: Destroy"; `DESTROY. The degausser is warm already. Your hands know how to touch tape.` · Merle: `'The degausser hums at night. I hear it too.' Her hands keep drying the plate.` · Day 5 spine passes the +Y gap: CTL → MC → TH threshold (S4) — the climate room is the hall's back door | restoration-player-routing.md Night 5, THREAD 3, Day 5; Data/GameText.csv 159–161, 83, 498; restoration-game-master.md ENDING 3 |
| Texts (prompts) | `THE DEGAUSSER · humming · bring it a daily` / `THE DEGAUSSER · burn TAKE %d (E)`; flavour `It hums, felt-throated. It wants a canister.`; binder `READ RESET · dailies burned` | Data/GameText.csv 97, 96, 98, 64; scripts/degausser.gd 6–9 |
| Sound | Bed: "the deepest hum, compressor cycles"; S02 DEGAUSSER COIL target: "coil whine that rises through the wipe, snaps off; a magnet-pop tail" (now 120/240 + noise); S01 the hall's mains hum "audible two rooms out, filtered"; B-R1 "To ritual kept: doors ease, the hum settles a cent flat" | restoration-room-bible.md; restoration-audio-bible.md S02, S01; restoration-reaction-matrix.md THE BUILDING |
| Route | Not on the Day 1 tour; first entered on a night errand; the Rundown's segments are not homed here (anchors: LIB, STA, PB) | restoration-player-routing.md Day 1, Night 5; scripts/rundown.gd 10–12 |
| Sanctuary | none | — |
| Inventory listing | §7: reel racks (T1 take; nightly retrieval) · hygrometer + thermograph (T1 inspect; "drum recorder; one night's trace shows a spike no thermostat explains") · the degausser (T1 inspect; T4 operate — the reference lets it burn from Day 1) · bake supplies (T1 use) · silica bins (T1 inspect; "one bin holds a single small mitten, desiccated" — rhymes with the corridor's FOUND PROPERTY memo [T2]) — reconciled against 1/1/6 in OPEN 3.10-B | restoration-room-inventory.md §7; restoration-ambient-lore-ledger.md CORRIDOR |

### 3.10.3 LIGHTING STATE TABLE
| State | Locked EV | Practicals | Red reads? | Transition | Source |
|---|---|---|---|---|---|
| DAY ON AIR | **OPEN** | "Green gauge glow, grille shadows": the GAUGES glow phosphor green — information, never room light (M_Phosphor emissive, no light contribution); the ROOM light is unnamed in canon: PROPOSED P-CL1 one caged BULKHEAD FITTING on the ceiling at (1425, −1600, 290) whose cage throws the "grille shadows", true bulb, colour family OPEN (a plant room reads as cool-white or tungsten; canon does not say) — **OPEN 3.10-C**; the degausser's coil glow (S02 rises "through the wipe") is a state light, not a practical | none (no camera; no tally) | CUT | restoration-room-bible.md CLIMATE; restoration-lighting-bible.md §GRAMMAR "PHOSPHOR GREEN … illuminates data, never rooms" |
| BREAK | **OPEN** | Same | — | — | OPEN 0-F |
| NIGHT (the errand's state) | **OPEN** | Practicals off; the gauges' green persists (standby data); the degausser's pilot; the hall's pilot lamps through the +Y gap ("Phosphor and pilot lamps" is the hall's family); the floor must resolve for a player carrying a canister from the library through the bench room | none | CUT | restoration-lighting-bible.md §STATES NIGHT; restoration-room-bible.md TRANSMITTER HALL |
| THE BURN (room-specific: burning a daily; Ending 3's playable destruction) | — | The coil glows and rises through the wipe, snaps off (S02) — a brief warm-orange bloom (the reference coil is copper-tinted (0.5, 0.32, 0.18)); no red | — | rise / snap | restoration-audio-bible.md S02; world_builder.gd 826–832 |
| CASCADE | **OPEN** — no circuit stamped | — | — | panel order | scripts/cascade.gd |
| 4c | **OPEN** | Not on the Day 1 tour; whether it blacks out with the bench room or at all is OPEN | — | — | lighting bible 4c; player-routing Day 1 spine |
| Colour script | OPEN | — | — | — | — |

### 3.10.4 FIXED PROPS
| Prop | Tier | Interact? | Real dims (m) | Placement (uu) | Asset candidate · licence |
|---|---|---|---|---|---|
| THE DEGAUSSER (housing, exposed coil ring, hazard stripe, felt-lined throat) — the HERO | Interactable | YES — `THE DEGAUSSER · burn TAKE %d (E)` / `… humming · bring it a daily` [GameText 96–97] | 1.2 × 0.8 × 0.9 housing; coil Ø0.6; a bulk tape eraser of the period is table-top (0.4 × 0.3) — the reference is a floor unit; keep the floor unit (the room's altar) | (1425, −1760, 55): housing Z 0..90, coil at Z 97, stripe at Z 70 [world_builder.gd 812–840] | Bespoke (Blender factory): steel cabinet under the metal family with a copper coil (real winding detail in normal maps <2 cm), a FELT-LINED THROAT (M_Wool family felt, dead-room gray) where the canister goes, hazard stripe in OCHRE/warning red only if ruled (art bible §4 reserves red for slates, tallies, the breaker — the stripe is OCHRE in the reference); the label DEGAUSSER as a brass plaque |
| Reel racks (nightly retrieval objectives) | Interactable per inventory (T1 take) — **OPEN 3.10-B** (cap I = 1) | OPEN | steel shelving 0.9 × 0.45 × 1.8 × 2 bays | +X wall at (1620, −1450, 0) and (1620, −1750, 0) | Megascans "metal shelving" (FAB-IMPORT starter set); reels in canisters (M_TapeStock labels) |
| Gauges with handwritten ranges (twin gauges; one heat-cracked) | Dressing (ambient lore host; drift: one needle's rest point) | NO (inventory `inspect`) | Ø0.15 dial gauges × 2 on a panel 0.5 × 0.3 | +X wall panel at (1648, −1450, 160) — the gauge nearer the +Y (transmitter) wall wears the crack; its twin at (1648, −1500, 160) does not | Bespoke: brass bezels, glass under M_Practical, PHOSPHOR-GREEN backlit faces (M_Phosphor), handwritten range marks in grease pencil on the glass (albedo) |
| Thermograph drum recorder + hygrometer | Dressing (ambient lore host: the unexplained spike) | NO | drum recorder 0.35 × 0.2 × 0.3; hygrometer Ø0.12 | on a shelf at (1620, −1600, 120) between the racks | Poly Haven search "barometer"/"gauge" *(verify id)* CC0 or bespoke; the drum's trace paper under M_Paper with one spike |
| Filter bank + FILTER LOG clipboard | Dressing (ambient lore host) | NO | filter housing 0.6 × 0.6 × 0.6 in the duct; clipboard 0.23 × 0.32 | AHU on the −Y wall at (1425, −1870, 0); clipboard hung at (1300, −1898, 150) | Fab search "HVAC unit industrial" (Megascans free tier if present); log under M_Paper |
| AHU / compressor + duct run + grilles ("the building's lungs") | Dressing (surface-scale; bed source) | NO | AHU 1.2 × 0.8 × 1.6; duct Ø0.4 along the ceiling to the +Y gap header | AHU at (1425, −1870, 0); duct along Y at Z 270 from the AHU to the hall | Fab search "ventilation duct" / "air handling unit"; galvanised under the metal family; grilles: Megascans "steel plate"/"riveted metal panel" (starter) |
| Silica bins (one holds a single small mitten, desiccated) | Dressing (ambient lore host, inventory) | NO | 3 bins 0.4 × 0.3 × 0.3 | floor at (1250, −1850, 0) | Fab search "plastic bin"/"storage tote"; silica beads in maps; the mitten bespoke (M_Wool family, the only knitted object in the room) |
| Bake supplies shelf | Dressing (inventory `use`) | NO | 0.6 × 0.3 shelf | −X wall at (1215, −1400, 120) | kraft boxes, foil, a thermometer |
| Maintenance tag (three initial-sets across one decade; the third only after 1974) | Dressing detail (ambient lore) | NO | 0.08 × 0.15 card tag on wire | on the AHU's access panel handle at (1400, −1830, 100) | M_Paper; three inks |
| Surfaces | — | — | floor 27 m² | — | Floor: Megascans "industrial concrete floor" (starter) with a floor drain and a condensate stain → `MI_Climate_Floor`; walls: Megascans "brick (painted-over)" (starter) → `MI_Climate_Wall`; ceiling: exposed structure with the duct → `MI_Climate_Ceiling` (OPEN 0-H); metals → `MI_Climate_Duct` |

### 3.10.5 LORE ITEMS
| Item | Tag | Sits | Text key | Source |
|---|---|---|---|---|
| The filter log ends mid-1977 and resumes with no explanation and better handwriting | HF, T6 | The clipboard at (1300, −1898, 150); the page turned to the 1977 break; legible at 1 m | none (QA-55) | restoration-ambient-lore-ledger.md CLIMATE |
| The gauge nearest the transmitter wall wears a heat crack; its twin does not | HF | The gauge panel, (1648, −1450, 160) cracked (nearer the +Y hall wall), (1648, −1500, 160) whole | none | restoration-ambient-lore-ledger.md CLIMATE |
| A maintenance tag signed by three initial-sets across one decade, the third set appearing only after 1974 | T4 | The AHU access-panel handle, (1400, −1830, 100) | none | restoration-ambient-lore-ledger.md CLIMATE |
| (Inventory) one silica bin holds a single small mitten, desiccated; the thermograph's one-night spike | rhyme with CORRIDOR's T2 memo; wrongness | Bins at (1250, −1850); the drum at (1620, −1600, 120) | none | restoration-room-inventory.md §7 |
| Handled L = 1 | — | No D-series readable is homed here; the L cap's occupant is OPEN 0-G | — | restoration-props-packet.md |

### 3.10.6 DRESSING PASSES
| # | Pass | Steps | Verification capture | Must read |
|---|---|---|---|---|
| P0 | Data check | Bounds X 1200..1650 / Y −1900..−1300; two open gaps (1200, −1600) and (1450, −1300); the degausser's footprint (1425, −1760); S4 visible through the +Y gap at (1450, −1140); no stand-in changes yet; resolve OPEN 0-H before ceilings and 3.10-A (demo leaf) with the data owner | top-down (1425, −1600, 900) → (1425, −1600, 0) | Exact |
| P1 | Surfaces | Concrete with drain and condensate stain; painted-over brick; exposed ceiling with the duct run; grilles; wear at both gaps and a worn lane from the −X gap to the degausser | (1220, −1600, 148) → (1425, −1760, 97) (from the bench gap, at the coil) | The lane reads as the errand's habit; grilles throw shadows under P-CL1; three-way light break |
| P2 | Fixed props | Degausser (throat felt, coil, stripe), reel racks, gauge panel, thermograph shelf, AHU + duct + filter bank + clipboard, silica bins, bake shelf | (1220, −1600, 148) → (1425, −1760, 97) | The degausser is hero by wear (a polished throat rim where canisters go in; the stripe scuffed); the coil reads as copper winding at 1 m |
| P3 | Practicals + EV | P-CL1 caged bulkhead with true bulb; gauge faces phosphor-emissive with ZERO light contribution; delete the stand-in; lock DAY EV; author NIGHT and THE BURN (coil bloom rise/snap) as scenarios | DAY: (1220, −1600, 148) → (1425, −1760, 97); NIGHT: (1425, −1450, 148) → (1425, −1760, 97); BURN: same as NIGHT mid-wipe | DAY: grille shadows on the walls, green on the gauge faces only; NIGHT: the floor resolves, the gauges are the brightest thing and light nothing; BURN: the coil bloom is warm and brief |
| P4 | Lore FIRST | Filter log at the 1977 break; the cracked gauge vs its twin; the three-hand maintenance tag; the mitten in the bin; the drum's spike | 1 m closeups: (1300, −1800, 148) → clipboard; (1560, −1470, 160) → gauges; (1400, −1740, 120) → tag; (1250, −1760, 148) → bin | All promptless; the crack reads in the normal map at 1 m, not in albedo |
| P5 | Dressing mass (≤ 6) | A mop and bucket (condensate), a wall thermostat with a handwritten range, a coil of duct tape on a hook, a fire extinguisher (starter), a crate of empty canisters awaiting return, a pair of cotton gloves left on the rack (not Rita's white — grey, someone else's) | (1220, −1600, 148) → (1650, −1600, 150) | ≤ 6; each owned; nothing fake-affords |
| P6 | Wear/decals/drift | Rust at the drain, scuffs at the degausser's base, dust on the upper racks; drift hook: ONE gauge needle's rest point (dressing, monotonic) | Day 1 vs Day 4 pair (needle only) | Only the needle moved |
| P7 | QA + acceptance | QA-55 (prompts: the degausser; racks per 3.10-B), QA-56 (drift = one needle), QA-57 (hero = degausser) | §3.10.7 | §3.10.7 |

### 3.10.7 ACCEPTANCE CAPTURE
- Camera A (the lungs): **(1220, −1600, 148) → look-at (1425, −1760, 97)**, DAY ON AIR, Day 1 post volume — degausser, racks, gauges, the duct.
- Camera B (the errand's end): **(1425, −1450, 148) → look-at (1425, −1760, 97)**, NIGHT, a canister in hand implied — the coil and the green gauges are the frame's only glow.
- Camera C (the hall's back door): **(1425, −1700, 148) → look-at (1450, −1140, 110)** through the +Y gap to S4, DAY.
- Checklist: (1) green glows only on gauge faces and lights nothing; (2) grille shadows read under the one caged fitting; (3) the degausser is hero by wear; (4) filter log, cracked gauge, tag present and promptless; (5) at NIGHT the floor resolves for the errand; (6) no naked primitive (the coil is wound, the ducts have seams and rivets); (7) store-page test.

### 3.10.8 OPEN
- **3.10-A** The +Y gap to the TRANSMITTER HALL has no leaf to carry the demo's SEALED reason though the hall is closed in the demo.
- **3.10-B** Interactable count: cap 1/1/6 vs inventory §7 (reel racks `take` nightly, degausser, bake supplies `use`). This brief: I = degausser; racks OPEN.
- **3.10-C** The room's actual light source and its colour family: canon names only the gauge glow (information, not room light) and "grille shadows".
- **0-H** as in §0.3.

---

## APPENDIX A · FORMAT TEMPLATE (unchanged from ROOM-BRIEFS-3.1-3.5.md Appendix A; briefs 3.11–3.20 copy it exactly)

See docs/production/ROOM-BRIEFS-3.1-3.5.md Appendix A. Rules of the template
restated: cite `[doc §section]` on every canon claim; write OPEN where canon is
silent; the code's placements are the spec for positions; the room bible's cap
governs prompts (flag inventory breaches, do not resolve them); the ledger's
items are placed before any dressing mass; asset ids are search terms unless
verified.

## APPENDIX B · CONSOLIDATED OPEN QUESTIONS (owner rulings needed)
| Id | Question | Blocks |
|---|---|---|
| 0-A..0-G | as in ROOM-BRIEFS-3.1-3.5.md Appendix B | as there |
| **0-H** | AF_HEIGHT 3.35 m vs WALL_H 3.0 m: no ceiling is stamped; ceilings at Z 300 clip him | every P1 ceiling pass in 3.7–3.10 and in every room he enters |
| **0-I** | Physical tally lamps on CAM 1 / CAM 2 mounts (canon: shape-coded lamps; reference: none) | 3.7.3 and 3.8.3 "Red reads?" and both acceptance captures |
| **0-J** | Docks and the shed key float at working height with no table beneath | 3.6 P2, 3.9 P2 (this brief proposes a desk, a side table and a carton) |
| 3.6-A..E | shed height; I count; hasp "unlocked, always" vs PADLOCKED; pull chain operable; key scale | 3.6 |
| 3.7-A..E | 4c order; break clock; the I occupant; bulb count vs casualties (B-R2); the wax lane's bend | 3.7 |
| 3.8-A..G | CONTROL gap has no leaf for the demo; the crate's home; I count (ten touchables vs 2); compactus is not in data; film cabinet scale; D01's home/absence; D06's home (cabinet vs REC) | 3.8 |
| 3.9-A..F | screen scale; WOOL SPIKE 001; I count (seven prompts vs 3); "two rooms away"; deck tally lamp; task lamp at night | 3.9 |
| 3.10-A..C | TH gap has no leaf for the demo; I count (racks); the room's light source and colour family | 3.10 |
| W-series | W1/W3 text keys are not in GameText.csv | 3.8 P4, 3.6 P4 |
| EV | No EV number exists in canon; every chosen EV per room-state is recorded in the build PR as a PROPOSAL, never as canon, until unit C18 (Lighting.csv) lands | every room |

## APPENDIX C · ONE FAB PULL FOR ALL FIVE ROOMS (batch per ue/FAB-IMPORT.md §THE PULL)
Surfaces (Megascans, FREE, MEDIUM/2K): industrial concrete floor · linoleum/
checker or vinyl tile waxed · brick (painted-over) · plaster wall painted aged ·
acoustic ceiling tile · steel plate · riveted/painted metal panel · painted wood
siding · wood plank weathered · packed dirt · painted wood trim/skirting.
Decals: scuffs · coffee stains · water damage/condensate · rust streaks · tape
residue · oxide smear.
Props (free tier if present): cardboard boxes · metal shelving · fire
extinguisher · folding chairs · cork board · paint can rusted · ventilation duct ·
air handling unit · HVAC unit industrial · flat file cabinet vintage metal · card
catalog cabinet · office/writing desk vintage · workbench metal · laboratory oven
· broadcast monitor vintage / CRT monitor 70s · ceiling light vintage industrial ·
film canister · plastic bin/storage tote · library ladder.
CC0 (Poly Haven, verify ids): wooden_table_02 · search: broom, paint can, security
camera, reel to reel, film reel can, drawer cabinet, barometer/gauge.
Bespoke (Blender factory): the felt-wrapped quiet-room key · the shed's rod coil ·
CAM 1/CAM 2 camera bodies (+ tally lamps if ruled) · S1 lectern (shared family) ·
the tape-spine instanced set with label maps · THE BENCH + reel deck · the gen knob
· the three bench docks as cased machines · the accession ledger (D03, 4K) · the
splice tray (Rita's seven tools) · THE DEGAUSSER (coil, felt throat) · the gauge
panel · the desiccated mitten.
Every pull: credits line in ue/CREDITS-FAB.md, wear pass, MI_<Room>_<Surface>
naming [ue/FAB-IMPORT.md §AFTER EVERY PULL].
