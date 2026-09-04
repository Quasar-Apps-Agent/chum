# RESTORATION · ROOM BRIEFS 3.1–3.5 (ENTRY · REC ROOM · KITCHEN · DORMS · YARD)

Executable dressing briefs for the first five Phase 3 units, in the exact order
PROGRESS.md §PHASE 3 lists them. A build agent dresses each room in UE 5.8 from
this file alone. This file is also the FORMAT TEMPLATE for briefs 3.6–3.20
(Appendix A). Every canon claim carries a citation `[doc §section]`; where the
canon gives no number the cell says **OPEN**. Nothing here invents canon.

Source set read for this brief: PROGRESS.md §PHASE 3; docs/canon/
restoration-room-bible.md; restoration-lighting-bible.md; restoration-object-
taxonomy.md; restoration-ambient-lore-ledger.md; restoration-dread-doctrine.md;
restoration-walkthrough-levels-endings.md; restoration-comparative-study.md;
restoration-lore-architecture.md; restoration-room-inventory.md;
restoration-game-master.md; restoration-player-routing.md; restoration-
reaction-matrix.md; restoration-casualty-ledger.md; docs/production/
restoration-art-bible.md; restoration-audio-bible.md; restoration-props-
packet.md; docs/packet/portbrief/THE-LAWS.md; ue/Restoration/Data/{Rooms,
Doors,Stations,Monitors,DemoOpen,Timings,GameText}.csv; ue/FAB-IMPORT.md;
AAA_BUILD_PLAN.md §2 and §R; ue/pyscripts/build_greybox.py (the stamp);
scripts/world_builder.gd + coat_pegs.gd + rec_chairs.gd + harriet.gd (the
reference implementation's placements — "the code is the spec"
[docs/packet/portbrief/PORT-BRIEF.md, cited via AAA_BUILD_PLAN.md §1 THE PORT KIT]).

---

## 0 · CONVENTIONS (read once, apply to every room)

### 0.1 Coordinate law (scale truth)
| Rule | Value | Source |
|---|---|---|
| Unit | 1 m = 100 uu, verified on a 1 m cube | PROGRESS.md 0.2; AAA_BUILD_PLAN.md §1 Unreal side |
| Plan mapping | UE (X, Y, Z) uu = (Godot x, Godot z, Godot y) × 100. All Rooms/Doors/Stations CSV columns are Godot metres: `center_x → X`, `center_z → Y`, height → Z | ue/pyscripts/build_greybox.py docstring + `S = 100.0` |
| Floor | Room floor slab is a cube at Z = −10 uu, 20 uu thick → walkable floor top at **Z = 0** | build_greybox.py line 111 |
| Walls | 3.0 m high (Z 0..300), 0.24 m thick, centred on the room edge line; door gaps cut per Doors.csv | build_greybox.py `WALL_H`, `WALL_T`, `wall_run()`; Timings.csv world_builder.gd WALL_H/WALL_T |
| Door slabs | Only rows with a non-empty `kind`. `door`/`locked:` → slab 2.6 m high × 0.10 thick at the gap; `window` → sill 0.9 m + header 1.1 m. Locked reason rendered as world text at Z = 290 | build_greybox.py lines 127–154 |
| Reference door leaf | Godot leaf is 2.2 m tall (`PropKit.door_leaf(gw, 2.2, …)`) vs the greybox 2.6 m slab | scripts/world_builder.gd line 279 — **OPEN 0-A** which height is truth |
| Stations | 0.5 × 0.5 × 1.1 m marker at (x, z, 0.55) + id text at Z = 150; reference prop is a lectern with binder and chained pen | build_greybox.py lines 156–163; world_builder.gd `_spawn_station` + prop_kit.gd `lectern()` |
| Plan words used below | **+Y = yard side** (ENTRY/YARD lie at +Y), **−Y = studio side** (the studio wing lies at Y ≤ −2000), **+X = kitchen side**, **−X = dorms side**. Compass words are avoided because Godot's "north" comment convention is −z (see world_builder.gd `_spawn_kitchen` comment vs its z = −2.15) | this brief |
| Rita's eye | Camera at Z = +60 uu above capsule centre → **eye ≈ 148 uu above floor** | ue/Restoration/Source/Restoration/RitaCharacter.cpp line 31. Godot reference eye is 1.6 m (scenes/main.tscn Camera3D y = 1.6) — **OPEN 0-B** parity delta |
| Capture FOV | UE ARitaCharacter sets no FieldOfView → engine default 90° horizontal. Godot main.tscn `fov = 70.0` (vertical, keep-height). Art bible: "24 mm equivalent" [restoration-art-bible.md §9] | **OPEN 0-C** — until ruled, all acceptance captures below use the UE Rita camera as-is (90° H) so captures match what the player sees |
| PlayerStart | (0, 0, 160) in REC ROOM | build_greybox.py line 166 |

### 0.2 Lighting law applied to these rooms
| Rule | Text | Source |
|---|---|---|
| Grammar | RED = WATCHED = SAFE (tallys, ON AIR signs, his eye). PHOSPHOR GREEN = information, illuminates data never rooms. AMBER TUNGSTEN = the club's warmth (kitchen, rec room, dorms; practicals with real fixtures). SODIUM = one fixture, the scene dock. DARK IS A ROOM, NOT A WALL: minimum readable floor everywhere | restoration-lighting-bible.md §THE GRAMMAR |
| States | DAY ON AIR (full practicals + every tally); BREAK (tallys die together, red drains, Harriet freezes); NIGHT (practicals off; exit signage, standby LEDs, phosphor spill, moonless windows); CASCADE (circuit geography, C's zone then B's); THE CROSSING (his eye dark, sign-off glow under doors); 4c (reverse-tour blackout in Day 1 order, entry last, then the tower light, then nothing) | restoration-lighting-bible.md §STATES |
| Clock | ON AIR 50.0 s / BREAK 18.0 s | Data/Timings.csv broadcast.gd; PROGRESS.md 0.7 |
| Technicals | Lumen GI software tier; VSM; **AUTO-EXPOSURE OFF; locked EV per room-state; transitions CUT with the schedule, never swim**; volumetrics low and motivated (transmitter hall only); practicals authored in Blender with TRUE BULB POSITIONS; per-day colour script as post volumes over unchanged practicals (Day 1 warmest → Day 5 coolest) | restoration-lighting-bible.md §UE5 TECHNICALS |
| Fixture families | REC: amber overheads plus the kettle's glow. CORRIDORS: spaced tungsten with authored gaps. STUDIO: grid + tallys. DEAD ROOM: one flat toplight | restoration-lighting-bible.md §UE5 TECHNICALS |
| Day/Night art | Day: overcast north key + warm tungsten practicals. Night: sodium exterior spill at the windows, phosphor monitor glow as interior key, pools with honest falloff | restoration-art-bible.md §8 — **OPEN 0-D**: art bible §8's "sodium exterior spill at the windows" vs lighting bible's "SODIUM is one fixture, the scene dock" (the lighting bible is the later, named canon per AAA_BUILD_PLAN.md §1 Lighting law) |
| Numbers | **No EV value, candela, kelvin or lux exists anywhere in canon** (grep of docs/canon, docs/production, docs/packet). Every EV cell below is OPEN. Recorded stand-ins, NOT canon: greybox room lamp = PointLight at (cx, cy, 275), 9.0 cd, colour (0.95, 0.72, 0.45), attenuation 0.75 × max(width, depth) × 100, no shadows; SkyLight 0.12; YARD gets no lamp [build_greybox.py lines 116–126, 169–170]. Reference night ratio: practicals 0.5 → 0.28, ambient 0.09 → 0.03, sun 0.07 → 0.005 [world_builder.gd `_on_night_lighting` lines 700–709] — note this BROWN-OUT contradicts the bible's "NIGHT: practicals off" → **OPEN 0-E** |
| Red in these five rooms | Monitors.csv holds two feeds (CAM 1 · CORRIDOR, CAM 2 · STACKS); no camera or tally lives in ENTRY/REC/KITCHEN/DORMS/YARD. The cue signs are AMBER [restoration-game-master.md T1.7]; the tower light is RED but not a tally [restoration-room-bible.md YARD; world_builder.gd `_spawn_yard_dressing`]. Warning red is reserved for slates, tallies, the breaker [restoration-art-bible.md §4] | **OPEN 0-F**: whether the tower beacon's red participates in the red=watched grammar, and whether any practical in a tally-less room changes on BREAK (the bible only names the tallys) |

### 0.3 Object law applied
| Rule | Source |
|---|---|
| INTERACTABLES prompt, glyph the binding, never drift; affordance is diegetic wear; **one HERO interactable per room** | restoration-object-taxonomy.md ¶INTERACTABLES |
| LORE: HANDLED (D-series; prompts; mark_read; Three Reads) and AMBIENT (**never prompts, never flagged**; found by looking) | restoration-object-taxonomy.md ¶LORE OBJECTS; restoration-lore-architecture.md §THE THREE READS RULE |
| DRESSING is the only drift-eligible tier; every dressed object implies a person and a habit; clutter without authorship banned | restoration-object-taxonomy.md ¶DRESSING |
| Budgets I/L/D are caps not quotas; the ledger is the source of record for ambient placement; **ambient lore is placed FIRST, dressing around it** | restoration-room-bible.md header; restoration-object-taxonomy.md ADDENDUM; PROGRESS.md §PHASE 3 header |
| QA-55 prompt discipline · QA-56 drift = dressing only · QA-57 one hero max | restoration-object-taxonomy.md ¶QA HOOKS |
| Reading of the L cap used in this brief: L counts HANDLED lore (D-series) — ENTRY is 1/0/8 yet carries three ledger items, so ambient cannot be what L counts. **OPEN 0-G** for the owner to confirm | this brief |
| Drift law for props: small replaced props first, textiles second, wall tones never; pegs/extras lead the curve by half a day | restoration-art-bible.md §4–5 |

### 0.4 Asset and wear law
| Rule | Source |
|---|---|
| Prefer Megascans (Fab plugin, FREE + Quixel filter, MEDIUM/2K) for surfaces and props before building by hand; CC0 from Poly Haven / AmbientCG into tools/modelsrc + tools/texsrc with CREDITS.md lines; no ripped content | AAA_BUILD_PLAN.md §2; ue/FAB-IMPORT.md §THE PULL |
| Every import: wear pass (nothing showroom-new — MI with grime/desat, or sodium_check.py --subject via Blender), credits line in ue/CREDITS-FAB.md (`<fab id> · <name> · <rooms used>`) | ue/FAB-IMPORT.md §AFTER EVERY PULL; ue/CREDITS-FAB.md |
| Naming: `MI_<Room>_<Surface>` instances (masters stay in Content/Megascans); `SM_`/`SK_`, `M_`/`MI_`, `T_*_BC/_N/_ORM`; `UCX_` collision; 2K default | ue/FAB-IMPORT.md; AAA_BUILD_PLAN.md §1 Unreal side |
| Material masters: M_Wool, M_TapeStock, M_Phosphor, M_Paper, M_Enamel, M_Practical (fixture glass) | AAA_BUILD_PLAN.md §1 |
| Realism bar: no naked primitives; <2 cm detail in maps; every surface breaks light three ways; lighting is part of the asset; scale truth at gameplay distance AND 1 m closeup; crafted not photoreal — material truth | AAA_BUILD_PLAN.md §R.1–7 |
| Palette: neutrals ash #6B6862 dust #7F7A70 slate #5C5C61 oat #756E66 fog #666B6B; show MUSTARD #C9A33D AVOCADO #6B7D3B BURNT #B35A2B; paper #DED4B8; ledger green #596B52; warning red #C23A2E (slates/tallies/breaker only) | restoration-art-bible.md §4 |
| Room short-names for MI_ naming in this file: `Entry`, `RecRoom`, `Kitchen`, `Dorms`, `Yard` | this brief |
| Asset-id honesty: Fab entries are SEARCH TERMS (Fab has no API; ids are read off the editor at pull time and logged). CC0 ids marked *(verify id)* must be confirmed on the site before download; the licence is the same for any id on that site | this brief |

### 0.5 The pass order (every room, same order)
P0 data check → P1 surfaces → P2 fixed props (interactables + hero) → P3
practicals + EV lock (delete the P0 stand-in lamp) → P4 LORE (ledger items,
placed before any dressing mass) → P5 dressing mass to the D cap → P6 wear,
decals, drift hooks → P7 QA-55/56/57 + acceptance capture. Lore-before-dressing
is PROGRESS.md §PHASE 3 header; the rest is the requested order.

Capture verb used below: "capture at (X, Y, Z) → look-at (X, Y, Z)" means a
HighResShot/MRQ still from that camera position and aim, Rita FOV (0.1),
locked EV of the stated state, auto-exposure off. Archive under
docs/telemetry/ue-baselines/ per the 0.3 precedent [PROGRESS.md 0.3].

---

## 3.1 · ENTRY — the threshold that decides you are expected

### 3.1.1 IDENTITY
| Field | Value | Source |
|---|---|---|
| Rooms.csv | `ENTRY, 0.0, 7.0, 6.0, 6.0` → centre (0, 700), 6 × 6 m | Data/Rooms.csv |
| Floor bounds (uu) | X −300..300, Y 400..1000, floor top Z 0, ceiling/wall top Z 300 | derived per §0.1 |
| Door → REC ROOM | Doors.csv `REC ROOM, ENTRY, 0.0, 4.0, 1.6, x, door` → gap centre (0, 400), 1.6 m wide (X −80..80) in the −Y wall; slab stamped; **not locked** | Data/Doors.csv |
| Door → YARD | `ENTRY, YARD, 0.0, 10.0, 1.6, x, door` → gap centre (0, 1000), 1.6 m wide in the +Y wall; slab stamped; **not locked**. Exterior door: 2.2 s fold toll applies to him at every threshold | Data/Doors.csv; THE-LAWS.md 11 |
| Stations | none | Data/Stations.csv |
| Monitors | none | Data/Monitors.csv |
| Demo | open in Tape 1 demo | Data/DemoOpen.csv |
| Reference placements | Coat pegs at Godot (2.7, 1.5, 7.0) → **UE (270, 700, 150)**, rail 2.2 m long running along Y against the +X wall, 5 pegs at 0.45 m pitch, coats 0.34 × 0.80 × 0.10 m hanging to Z ≈ 105 | world_builder.gd `_spawn_details` line 1091; coat_pegs.gd `_ready` |
| Adjacent rooms | REC ROOM (−Y), YARD (+Y). The −X and +X walls face unstamped exterior | Data/Rooms.csv |

### 3.1.2 ROLE
| Aspect | Canon | Source |
|---|---|---|
| Personality | "The threshold that decides you are expected. Amber over the door, the rest borrowed." Bed: yard wind under the door, the delivery van's absence | restoration-room-bible.md ENTRY |
| Budget | 1 / 0 / 8 (I/L/D); drift: pegs, mat angle; web: deliveries land here; the door eases with ritual kept (B-R1) | restoration-room-bible.md ENTRY; PROGRESS.md 3.1 |
| Dread role | L1 AMBIENT WRONGNESS ground zero: "the coat pegs migrate on their curve"; drift is monotonic, never reset, never called out | restoration-dread-doctrine.md L1; restoration-room-bible.md ENTRY "drift ground zero" |
| Drift curve | coats lerp NEUTRALS → SHOW by d = clamp((day − 1)/4), +0.35 after lockdown; pegs lead the wardrobe curve by half a day | scripts/coat_pegs.gd `_drift`; restoration-art-bible.md §5 EXTRAS AND PEGS |
| Beats | T1.1 ARRIVAL: Merle opens before Rita knocks, "the wind takes the door" (the exterior sign THE 58 CLUB, EST. WITH LOVE hangs outside). T4.1 DELIVERY, dawn: Vess backs through the door with the impossible-tapes crate (the crate then lives at the bench) | restoration-game-master.md T1.1, T4.1; restoration-room-inventory.md §2 "Vess's delivery spot", §GLOBAL "impossible-tapes crate" |
| Route | Day 1 spine begins ENT → REC; Night 7 exterior leaves ENT → EXT | restoration-player-routing.md Day 1 spine, Night 7 spine |
| 4c | Reverse-tour blackout goes room by room in Day 1 order, **entry last**, then the tower light | restoration-lighting-bible.md §STATES 4c |
| Inventory listing | Club charter framed (inspect), coat pegs (inspect, DYN), bulletin board (DYN; T5 gains the PREMIERE bill), guest book podium (sign; Leland's entry two pages back), umbrella stand (one child-size handle), Vess's delivery spot (T4 EVT) | restoration-room-inventory.md §2 — reconciled against the 1/0/8 cap in OPEN 3.1-A |

### 3.1.3 LIGHTING STATE TABLE
| State | Locked EV | Practicals (type · position hint · colour · intensity) | Red reads? | Transition | Source |
|---|---|---|---|---|---|
| DAY ON AIR | **OPEN** | P-E1 amber tungsten fixture "over the door" — one real fixture with true bulb geometry. Position: over the door gap at (0, ≈990, ≈270) on the +Y wall if "the door" is the exterior door, or (0, ≈410, ≈270) if the REC door — **OPEN 3.1-B**. Colour: amber tungsten (family word only; no kelvin in canon). Intensity: OPEN. Everything else is BORROWED: rec-room amber through the −Y door gap, yard through the +Y door when open | No tally here; no red source | CUT on the schedule | restoration-room-bible.md ENTRY; restoration-lighting-bible.md §GRAMMAR, §UE5 TECHNICALS |
| BREAK | **OPEN** (same as DAY unless ruled otherwise) | Same practicals; only the tallys die on the cue and there is none here | — | CUT at the 50 s flip | restoration-lighting-bible.md §STATES BREAK; OPEN 0-F |
| NIGHT | **OPEN** | P-E1 OFF (practicals off). Allowed sources: exit signage / standby LEDs (an EXIT fixture over the exterior door is grammar-consistent — **OPEN 3.1-C** whether one exists), the tower's red through the +Y door seam. Floor must still read (dark is a room, not a wall) | Tower red visible only through the door/seam | CUT | restoration-lighting-bible.md §STATES NIGHT, §GRAMMAR |
| CASCADE | **OPEN** — which circuit zone the entry sits on is not in canon | — | — | ordered by the panel's labels | restoration-lighting-bible.md §STATES CASCADE |
| THE CROSSING | **OPEN** | Sign-off glow leaking under doors along the broadcast path — whether the path crosses the entry is OPEN | his eye dark | — | restoration-lighting-bible.md §STATES |
| 4c | **OPEN** | Entry is the LAST room to black out, then the tower light, then nothing | — | room-by-room, Day 1 order | restoration-lighting-bible.md §STATES 4c |
| Colour script | Per-day post volume over unchanged practicals (Day 1 warmest) — values OPEN | — | — | — | restoration-lighting-bible.md §UE5 TECHNICALS |

### 3.1.4 FIXED PROPS
| Prop | Tier | Interact? | Real dims (m) | Placement (uu, proposed unless cited) | Asset candidate · licence |
|---|---|---|---|---|---|
| COAT PEGS (rail, 5 pegs, 5 coats) — the HERO | Interactable (DYN, drift meter) | YES — prompt key `COAT PEGS · the club's palette (E)`; late text `Show palette, head to toe, every peg. Somebody ironed.` [Data/GameText.csv lines 58, 61] | rail 2.2 × 0.08 × 0.08; peg Ø0.04 × 0.10; coat 0.34 × 0.80 × 0.10 | (270, 700, 150), rail along Y, on the +X wall [world_builder.gd 1091] | Bespoke (Blender factory): rail + brass pegs; coats as 5 wool/cloth garments under M_Wool with a per-coat tint parameter driven by the drift curve. Fab search: "coat rack wall wooden" (Fab Standard) for the rail only if free |
| Sign-in / guest book podium (with pages) | Dressing (ambient lore host) — see OPEN 3.1-A | NO (bible cap 1/0/8) | 0.5 × 0.42 top, 1.2 tall | (−200, 560, 0) inside the REC door, −X side | Poly Haven search "lectern" *(verify id)*, CC0; or reuse the station lectern build (prop_kit.gd `lectern()` geometry: post 0.12 sq × 0.95, top 0.5 × 0.42 tilted 0.35 rad) with a different binder |
| Door mat, worn through at one heel | Dressing (ambient lore host) | NO | 0.9 × 0.6 × 0.02 | (0, 940, 1) inside the +Y door; the worn heel faces −Y (toward the building) | AmbientCG search "Fabric" coir/jute texture *(verify id)*, CC0, on a bevelled slab; hole and heel wear in the mask |
| Club charter, framed | Dressing | NO | 0.4 × 0.5 | −X wall at (−298, 800, 160) | Poly Haven `hanging_picture_frame_01` *(verify id)*, CC0; glass under M_Practical or plain glass; text key none (quote per room inventory §2 is flavour: "The 58 Club exists to preserve what loved us first") |
| Bulletin board (casserole rotation, screening notices; T5 PREMIERE bill) | Dressing (DYN by tape) | NO | 0.9 × 0.6 | −X wall at (−298, 620, 160) | Fab search "cork board" / "notice board" (Megascans free tier if present); paper under M_Paper |
| Umbrella stand, one child-size handle | Dressing | NO | Ø0.25 × 0.6 | (−250, 960, 0) corner by the +Y door | Fab search "umbrella stand" or bespoke cylinder-with-bevels + 3 umbrellas |
| Key hook board incl. hook labelled TOWER | Dressing (ambient lore host) | NO | 0.3 × 0.2 | +X wall at (298, 880, 150) above peg-rail height | Bespoke: 4 brass hooks on a pine board; tags under M_Paper |
| Door leaves ×2 (REC side, YARD side) | Interactable (doors are interactables) — but counted in the Doors table, not the room's I cap | YES (door verb) | 1.6 wide gap; leaf 2.2 (ref) / slab 2.6 (greybox) — OPEN 0-A | at the gaps (0, 400) and (0, 1000) | Fab search "wooden door old painted" (Megascans) for the leaf; steel exterior door per T1.1 "industrial steel" [restoration-game-master.md T1.1] — Fab search "steel door industrial" |
| Surfaces | — | — | floor 36 m², walls 4 × 6 × 3 m | — | Floor: Megascans "worn parquet wood floor" or "linoleum/checker" (FAB-IMPORT starter set) → `MI_Entry_Floor`. Walls: Megascans "plaster wall painted aged" → `MI_Entry_Wall`, tint held at compound neutral (walls never drift). Ceiling: Megascans "acoustic ceiling tile" → `MI_Entry_Ceiling`. Alternative CC0: AmbientCG `WoodFloor051`, `PaintedPlaster017` *(verify ids)* |

### 3.1.5 LORE ITEMS (ledger; all promptless, static, three-reads compliant)
| Item | Tag | Sits | Text key | Source |
|---|---|---|---|---|
| The podium's oldest pages: a 1976 line where L. MERRICK signs IN, OUT column blank forever; every later line neatly closed | T3 | On the podium's open book, page turned back; legible at 1 m closeup only | none (ambient never prompts — QA-55) | restoration-ambient-lore-ledger.md ENTRY |
| The mat's worn heel faces the building, not the door | HF | The door mat, +Y door | none | restoration-ambient-lore-ledger.md ENTRY |
| Key hook labelled TOWER whose key has a newer cut than its tag | T4 | The key hook board, +X wall | none | restoration-ambient-lore-ledger.md ENTRY |
| (Room inventory, not the ledger) Leland's guest-book entry two pages back, never checked out | — | Same podium — the ledger's 1976 line is its canonical form; dress ONE object, not two | none | restoration-room-inventory.md §2 |

### 3.1.6 DRESSING PASSES
| # | Pass | Steps | Verification capture | Must read |
|---|---|---|---|---|
| P0 | Data check | Confirm floor X −300..300 / Y 400..1000, two slabs at (0,400) and (0,1000), no station marker, no locked text | top-down capture at (0, 700, 900) → (0, 700, 0) | Bounds and both gaps exactly as Doors.csv; nothing else |
| P1 | Surfaces | Apply MI_Entry_Floor / _Wall / _Ceiling; skirting board strip at Z 0..12 (Megascans "wood trim"); wear pass on all three | (0, 440, 148) → (0, 1000, 150) | Three-way light break on floor and wall (albedo, roughness, normal); no tiling repeat visible across 6 m; neutral wall tone |
| P2 | Fixed props | Place coat pegs (270, 700, 150); podium; mat; door leaves with hinge side and swing that fits the 1.6 m gap | (0, 440, 148) → (270, 700, 120) | Pegs read as brass, coats as wool at 1 m; rail sits flat on the wall; coats do not clip the floor (hem ≈ Z 105) |
| P3 | Practicals + EV | Build P-E1 with true bulb geometry (M_Practical glass); set the DAY ON AIR EV (OPEN → record the value chosen in the PR as a proposal); delete the P0 stand-in PointLight for this room | (0, 960, 148) → (0, 400, 120) (yard door looking in) | One authored amber pool "over the door"; the rest of the room reads as borrowed rec-room light; floor still resolves in the far corners |
| P4 | Lore FIRST | Podium pages (1976 MERRICK line), mat heel orientation, TOWER hook + key | 1 m closeups: (−120, 560, 148) → podium page; (0, 880, 148) → (0, 940, 1) mat; (200, 880, 150) → hook board | Each item legible at 1 m and unremarkable at 3 m; no prompt fires when the reach ray (2.6 m) touches them [Data/Timings.csv player.gd REACH] |
| P5 | Dressing mass (≤ 8) | Charter, bulletin board, umbrella stand, boot tray, a second mat outside the door, wall thermostat, a delivery-van absence (tyre-mark decal outside the +Y door), one folded chair — each with an owner | (0, 440, 148) → (0, 1000, 150) | Count ≤ 8; every object implies a person/habit; nothing looks interactable that is not (no fake affordance) |
| P6 | Wear/decals/drift | Scuff decals at the threshold; tape residue where notices were; hook the peg tint to the drift curve (day-driven, +0.35 post-lockdown); mat angle drift hook (dressing tier) | Day 1 vs Day 5 pair from (0, 440, 148) → (270, 700, 120) | Day 1 coats neutral, Day 5 coats in show palette; walls unchanged between the pair |
| P7 | QA + acceptance | QA-55 sweep (only pegs + doors prompt), QA-56 (drift = pegs, mat only), QA-57 (hero = pegs); acceptance capture §3.1.7 | see §3.1.7 | see §3.1.7 |

### 3.1.7 ACCEPTANCE CAPTURE
- Camera A (threshold): **(0, 430, 148) → look-at (0, 1000, 150)**, Rita FOV (OPEN 0-C, use 90° H), state DAY ON AIR, Day 1 post volume.
- Camera B (return view): **(0, 970, 148) → look-at (0, 400, 120)**, state NIGHT.
- Checklist: (1) amber over the door is the only authored pool, everything else borrowed; (2) coat pegs read as the room's hero by wear, not outline; (3) mat heel faces −Y; (4) the podium page is findable, unflagged; (5) at NIGHT the floor still resolves and the tower's red is visible only through the seam/door; (6) no naked primitive; (7) frame passes the store-page test [AAA_BUILD_PLAN.md §R].

### 3.1.8 OPEN
- **3.1-A** Interactable count: room bible/PROGRESS cap 1/0/8 vs room inventory §2 (podium `sign`, charter/bulletin/umbrella `inspect`). This brief treats the coat pegs as the single I and the rest as promptless dressing; owner to confirm.
- **3.1-B** "Amber over the door": which door (exterior +Y or REC −Y)?
- **3.1-C** Does an EXIT sign / standby LED exist in the entry at NIGHT?
- **0-A/B/C/D/E/F/G** as in §0.

---

## 3.2 · REC ROOM — the hearth; the club's living proof

### 3.2.1 IDENTITY
| Field | Value | Source |
|---|---|---|
| Rooms.csv | `REC ROOM, 0.0, 0.0, 10.0, 8.0` → centre (0, 0), 10 × 8 m | Data/Rooms.csv |
| Floor bounds (uu) | X −500..500, Y −400..400, Z 0 floor / 300 wall top | derived |
| Door → KITCHEN | `REC ROOM, KITCHEN, 5.0, 0.0, 1.4, z,` → open gap (500, 0), 1.4 m (Y −70..70) in the +X wall; no slab; not locked | Data/Doors.csv |
| Door → DORMS | `REC ROOM, DORMS, -5.0, 0.0, 1.4, z,` → open gap (−500, 0), 1.4 m in the −X wall; no slab | Data/Doors.csv |
| Door → ENTRY | `REC ROOM, ENTRY, 0.0, 4.0, 1.6, x, door` → (0, 400), slab | Data/Doors.csv |
| Door → CORRIDOR | `REC ROOM, CORRIDOR, 0.0, -4.0, 1.6, x,` → open gap (0, −400), 1.6 m; no slab | Data/Doors.csv |
| Station | **S5 REC ROOM at Godot (−4.2, 0, 3.2) → UE (−420, 320, 0)**; greybox marker 0.5 × 0.5 × 1.1 at Z 55; reference: lectern with binder + chained pen | Data/Stations.csv; world_builder.gd `_spawn_station` |
| PlayerStart | (0, 0, 160) | build_greybox.py 166 |
| Monitors | none (CAM 1 · CORRIDOR's monitor sits at Godot (2.4, 1.7, −3.82) → UE (240, −382, 170), i.e. ON THE REC ROOM'S −Y WALL just +X of the corridor gap, facing into the room) | Data/Monitors.csv |
| Reference placements (Godot → UE) | Screen/cabinet TV (−4.78, 1.6, 1.0) rot π/2 → **(−478, 100, 160)** on the −X wall facing +X · Projector (−1.4, 0.55, 1.0) → **(−140, 100, 55)**, lens toward −X · Cue signs RESPOND (−0.9, 2.5, 3.55) → **(−90, 355, 250)** and HOLD (0.9, 2.5, 3.55) → **(90, 355, 250)** over the ENTRY door · D04 clipping (−4.2, 1.15, −1.5) → **(−420, −150, 115)** on the −X wall (the shrine/corkboard zone) · Harriet (1.2, 0, 2.6) → **(120, 260, 0)** in her chair · Vess at the shrine (−3.7, 0, −1.2) → **(−370, −120, 0)** facing −X · Armchairs CASUAL: (60, 20) yaw 0.6 · (200, 200) −0.9 · (−80, 240) 1.9 · (320, 40) 2.6 · (−220, 20) −0.4; ROWS after lockdown: (−150, 60) · (0, 60) · (150, 60) · (−75, 180) · (75, 180), all facing −X toward the screen; chair collision 0.66 × 0.95 × 0.66 · Wall clock reference (0, 2.3, 0) → (0, 0, 230) — **OPEN 3.2-D** which wall | world_builder.gd `_spawn_screening`, `_spawn_readables`, `_spawn_details`, `_spawn_wall_clocks`; rec_chairs.gd CASUAL/ROWS |

### 3.2.2 ROLE
| Aspect | Canon | Source |
|---|---|---|
| Personality | "The hearth; the club's living proof. Warm amber, the safest light in the game." Bed: clock, upholstery quiet, distant kitchen. Keynotes: tournament bracket in three handwritings, doily archipelago, corkboard with D04, S5 under a shaded lamp | restoration-room-bible.md REC ROOM |
| Budget | 2 / 1 / 14; drift: bracket updates, doilies migrate; web: kitchen smells reach here on your habits (M-R1) | restoration-room-bible.md REC ROOM; PROGRESS.md 3.2; restoration-reaction-matrix.md MERLE (M-R1) |
| Dread role | WARMTH amplifier: comfort raises stakes; the hub is genuinely safe for three acts and its Tape 5 conversion lands because the comfort was real; "the comfort is never the trap" | restoration-dread-doctrine.md AMPLIFIERS; restoration-walkthrough-levels-endings.md Part III.1, Part IV Rules |
| Sanctuary | No capture "in the rec room until the lockdown" | restoration-walkthrough-levels-endings.md Part V-B "Where a Capture Cannot Happen" |
| Beats | T1.2 tour (armchairs in rows that almost face the cabinet TV, shrine wall, casserole whiteboard; Harriet with tea; Vess stands too fast) · T1.4 N1: TV plays static in 4:3 with the set off at the wall · T1.6 Merle remembers · T1.7 MINI-SCREENING, lights down, RESPOND wakes in warm amber over the doorway · T2.1 keys on a crocheted fob · T2.8 THE SCREENING (unison; "our new friend in the back") · T4.5 the rejected edit (take-up reel turns backward one rotation) · T4.6 Merle, 1974, at the shrine wall · T4.10 LOCKDOWN: armchairs stand in rows facing forward, RESPOND burns steady · T5 premiere gallery | restoration-game-master.md T1.2, T1.4, T1.6, T1.7, T2.1, T2.8, T4.5, T4.6, T4.10; restoration-walkthrough-levels-endings.md Part II Zone Design Notes |
| Chairs law | Conversion makes "no sound worth naming": a 1 dB room-tone dip, nothing else | restoration-audio-bible.md S10 |
| Harriet | Sways ON AIR, FREEZES mid-motion on BREAK; cup rises by the day (cup Z = 0.99 + 0.05 × min(day, 6) m in her raised hand); prompt `HARRIET · in her chair (E)` | PROGRESS.md 0.8b-5; harriet.gd line 70; THE-LAWS.md 6; Data/GameText.csv line 202 |
| Cue signs | RESPOND / HOLD in diegetic audience-sign style; lit only during response windows; never player-operable; hang over the rec room "like they always belonged there" | restoration-design-doc.md §The Call-and-Response UI; restoration-room-inventory.md §3 |
| Inventory listing | Cabinet TV (DYN), armchairs (DYN), shrine wall (ALDER/BELL/PRICE clippings + "find our friend" articles; the gray flannel jacket photo), cue signs, projector + screen, S5, Harriet's chair + teacup, Gladhouse board game (1975; rhyme missing its fourth line), photo albums (T2), doily'd equipment rack | restoration-room-inventory.md §3 — reconciled in OPEN 3.2-A |
| Clip | "Harriet doubled at the break" is a named clippable | restoration-comparative-study.md §V |

### 3.2.3 LIGHTING STATE TABLE
| State | Locked EV | Practicals | Red reads? | Transition | Source |
|---|---|---|---|---|---|
| DAY ON AIR | **OPEN** (the brightest/warmest interior EV in the game by doctrine) | P-R1..R3 amber overheads (three real ceiling fixtures with true bulb geometry, proposed at (−250, 0, 290), (0, 0, 290), (250, 0, 290)) · P-R4 shaded lamp over S5 at (−420, 320, ≈150) (floor/table lamp, amber) · the kettle's glow bleeding through the +X gap from KITCHEN · cue signs DARK · TV dark by day (**OPEN 3.2-B**) | No tally in room; CAM 1 monitor on the −Y wall shows the corridor feed (phosphor: data, not room light) | CUT | restoration-room-bible.md REC ROOM; restoration-lighting-bible.md §UE5 TECHNICALS "REC amber overheads plus the kettle's glow" |
| BREAK | **OPEN** (unchanged unless ruled) | Same; Harriet freezes inside the colour change — in a tally-less room the freeze IS the visible cue | — | CUT at the 50 s flip | restoration-lighting-bible.md §STATES BREAK; OPEN 0-F |
| SCREENING (room-specific: T1.7 / T2.8 / T4.5) | **OPEN** | "Lights down": overheads off or dimmed (OPEN which); the SCREEN is the key (M_Phosphor, tape-world content only — no grain on compound surfaces); RESPOND lit warm amber over the doorway (−90, 355, 250); HOLD as cued | Amber, not red | CUT on the screening event | restoration-game-master.md T1.7; restoration-art-bible.md §2 |
| NIGHT | **OPEN** | Practicals off; N1 the cabinet TV plays 4:3 static (phosphor spill allowed as data, not room light); standby LEDs on the doily'd equipment rack; corridor-side monitor glow | none | CUT | restoration-lighting-bible.md §STATES NIGHT; restoration-game-master.md T1.4 |
| LOCKDOWN / PREMIERE GALLERY (T4 end → T5) | **OPEN** | RESPOND burns STEADY; chairs in ROWS; sanctuary revoked | amber steady | CUT with the lockdown | restoration-game-master.md T4.10; restoration-room-inventory.md §3 State changes |
| CASCADE | **OPEN** zone | — | — | panel order | restoration-lighting-bible.md §STATES |
| 4c | **OPEN** | Blacks out in Day 1 order: REC is the second room out (ENT → REC → KIT → DRM → LIB → BEN) | — | room-by-room | restoration-lighting-bible.md 4c; restoration-player-routing.md Day 1 spine |
| Colour script | Day 1 warmest; values OPEN | — | — | — | restoration-lighting-bible.md §UE5 TECHNICALS |

### 3.2.4 FIXED PROPS
| Prop | Tier | Interact? | Real dims (m) | Placement (uu) | Asset candidate · licence |
|---|---|---|---|---|---|
| THE PROJECTOR (16 mm, two reels) — the HERO | Interactable | YES — `THE PROJECTOR · run the mini-screening (E)`, `THE PROJECTOR · reel running` [GameText lines 588–589] | body 0.5 × 0.4 × 0.7; reels Ø0.32; on a stand 0.55 high | (−140, 100, 55), lens toward −X [world_builder.gd 731–765] | Bespoke from a CC0 donor (Poly Haven search "projector" *(verify id)*; else Blender build per prop_kit geometry); painted steel under M_Enamel; take-up reel must be animatable backward one rotation [T4.5] |
| S5 LOG STATION (lectern, transmitter log binder, chained pen) | Interactable | YES — `%s · %s · sign the log (E) · %d line(s) left` [GameText 485–486] | post 0.12 sq × 0.95; top 0.5 × 0.42 tilted; binder 0.36 × 0.30 | (−420, 320, 0) [Data/Stations.csv]; shaded lamp above | Bespoke lectern (reuse across S1–S5 with per-station wear); paper under M_Paper; pen chain in maps (<2 cm) |
| Cabinet television (the screen; 4:3) | Dressing driven by events (the projector's screen; N1 static; lockdown sync; dark only in ending 1) | NO prompt (inventory says `inspect` — OPEN 3.2-A) | 1970s console ≈ 1.0 × 0.5 × 0.75 | (−478, 100, 160) screen centre, on the −X wall [world_builder.gd 724] — a console TV of that size stands on the floor; keep screen centre near Z 100–160 (OPEN 3.2-C) | Fab search "vintage television console 70s" (Fab Standard/free); screen under M_Phosphor; wood under Megascans "veneer" |
| Cue signs RESPOND / HOLD | Dressing, event-lit (never operable) | NO | ≈0.6 × 0.2 × 0.1 each, amber lens | (−90, 355, 250) and (90, 355, 250) over the ENTRY door [world_builder.gd 715, 719] | Bespoke: steel box, amber gel face (M_Practical), one true bulb inside each; gel amber matches the catwalk gel per inventory §14 |
| Five armchairs (mismatched) | Dressing, DYN (rows at lockdown; do not convert back) | NO prompt (inventory `use` — OPEN 3.2-A) | ≈0.85 × 0.9 × 0.95 each; collision 0.66 × 0.95 × 0.66 | CASUAL and ROWS positions per §3.2.1 | Poly Haven `ArmChair_01` *(verify id)*, CC0, ×5 with five upholstery tints from rec_chairs.gd (0.5,0.36,0.24 / 0.42,0.44,0.30 / 0.55,0.42,0.28 / 0.38,0.40,0.34 / 0.48,0.38,0.30) as MI variants; wear pass on arms/seat |
| Harriet's chair + teacup/saucer (her seat) | Dressing (she is a character; the chair is stable) | Character prompt on Harriet, not the chair | chair as above; cup Ø0.08 | (120, 260, 0) [world_builder.gd 1083] | Same armchair family; Poly Haven `tea_set_01` *(verify id)*, CC0 for cup/saucer |
| Shrine wall / corkboard (D04 host; ALDER/BELL/PRICE clippings; pins) | Handled lore host + dressing | D04 prompts (see lore) | corkboard 1.2 × 0.9; frames 0.2–0.4 | −X wall, centred (−498, −150, 150) [D04 at (−420, −150, 115)] | Fab search "cork board"; clippings under M_Paper (2K allowed for readables); enamel pins in maps |
| Doily'd equipment rack (standby LEDs) | Dressing | NO | 19-inch rack 0.6 × 0.6 × 1.2 | (450, −300, 0) +X/−Y corner | Fab search "server rack vintage" / "audio rack"; doilies as alpha cards |
| Casserole whiteboard | Dressing | NO | 0.9 × 0.6 | −Y wall (−200, −398, 160) | Bespoke plane with bevelled frame; marker text in the albedo |
| Tournament bracket (three handwritings) | Dressing (drift: updates) | NO | 0.6 × 0.9 poster | −Y wall (250, −398, 160) beside the CAM 1 monitor | M_Paper plane; handwriting in the albedo (three hands) |
| CAM 1 · CORRIDOR monitor | Interactable elsewhere (T2 read) — it is the corridor feed's endpoint; placed by Monitors.csv | per port | CRT 0.5 × 0.45 | (240, −382, 170) yaw π [Data/Monitors.csv] | M_Phosphor screen; steel case |
| Wall clock (break-window repeater) | Dressing, event-driven | NO | Ø0.3 | reference (0, 0, 230) — OPEN 3.2-D | Fab search "wall clock vintage" |
| Surfaces | — | — | floor 80 m² | — | Floor: Megascans "office carpet short pile 70s tone" over "worn parquet" at the edges → `MI_RecRoom_Floor`; walls: painted plaster + wallpaper band (Megascans "wallpaper vintage" if free; else AmbientCG search "Wallpaper" *(verify id)*) → `MI_RecRoom_Wall`; ceiling: acoustic tile → `MI_RecRoom_Ceiling` |

### 3.2.5 LORE ITEMS
| Item | Tag | Sits | Text key | Source |
|---|---|---|---|---|
| D04 THE CLIPPING · Chillicothe Courier, October 1974 (HANDLED) | the carrying | Behind shrine glass on the −X wall at (−420, −150, 115); Day 1 gate | `THE CLIPPING · 1974, behind glass` + the three D04 lines [GameText line 696; world_builder.gd 1153–1157]; full body in restoration-props-packet.md D04 | restoration-props-packet.md D04; restoration-room-bible.md REC ROOM |
| Tournament bracket's fifth name inked out; the scoring continues one more round anyway | HC | On the bracket poster, −Y wall | none | restoration-ambient-lore-ledger.md REC ROOM |
| One photo frame faces the wallpaper; wire dusty, nail not | T5 | Shrine wall, near the frame cluster (−498, −60, 170) | none | restoration-ambient-lore-ledger.md REC ROOM |
| Corkboard's green pushpins hold only the oldest papers; nobody stocks green pins now | T3, HC | The corkboard around D04 | none | restoration-ambient-lore-ledger.md REC ROOM |
| Board game (1975 box; counting rhyme missing its fourth line) | inventory | Shelf under the equipment rack | none (inventory `inspect` — OPEN 3.2-A) | restoration-room-inventory.md §3 |

### 3.2.6 DRESSING PASSES
| # | Pass | Steps | Verification capture | Must read |
|---|---|---|---|---|
| P0 | Data check | Bounds X ±500 / Y ±400; four gaps (500,0) (−500,0) (0,400 slab) (0,−400); S5 marker at (−420, 320); PlayerStart (0,0,160); CAM 1 monitor spot | top-down (0, 0, 900) → (0, 0, 0) | Exact CSV geometry; nothing added |
| P1 | Surfaces | Carpet with parquet margin; plaster + wallpaper band; ceiling tile; skirting; wear pass | (0, −380, 148) → (0, 400, 150) (from the corridor gap) | Warmest neutrals of the five rooms; no repeat tiling across 10 m |
| P2 | Fixed props | Projector, S5 lectern, TV, cue signs, five chairs CASUAL, Harriet's chair, rack, whiteboard, bracket, clock | (300, 300, 148) → (−478, 100, 120) | The projector reads as hero by wear (worn carry handle, polished switch); chairs mismatched, casual; sightline projector → screen unobstructed |
| P3 | Practicals + EV | Three amber overheads + the S5 shaded lamp with true bulbs; lens-glow off; delete the P0 stand-in lamp; lock DAY EV; author SCREENING and NIGHT states as separate lighting scenarios (CUT) | DAY: (0, −380, 148) → (0, 400, 150); SCREENING: (350, 250, 148) → (−478, 100, 160); NIGHT: same as DAY cam | DAY: safest light in the game, honest falloff; SCREENING: the screen is the key, RESPOND amber over the door; NIGHT: floor resolves, TV static is the only glow, no room-lighting from phosphor |
| P4 | Lore FIRST | D04 behind glass; bracket fifth name; the reversed frame (dust on wire, clean nail — normal/roughness detail in maps); green pins on old papers only | 1 m closeups: (−320, −150, 148) → D04; (150, −300, 148) → bracket; (−400, −60, 150) → frame | D04 prompts inside 2.6 m reach; the three ambient items never prompt; each legible at 1 m |
| P5 | Dressing mass (≤ 14) | Doily archipelago (rack, TV top, side table), photo albums (T2 shelf), board game, side tables ×2, floor lamp, curtains on any window (OPEN 3.2-E windows), coasters, a cardigan on a chair back, the crocheted key fob hook, a radio, magazines | (0, −380, 148) → (0, 400, 150) | ≤ 14; every object owned by a named habit; density does not hide D04 |
| P6 | Wear/decals/drift | Chair-leg carpet crush, coffee rings on tables (Megascans decal), tape residue on the whiteboard; drift hooks: bracket updates, doilies migrate (dressing tier only); rows tween 1.6 s ease-in-out at lockdown | Day 1 CASUAL vs post-lockdown ROWS pair from (0, −380, 148) → (0, 400, 150) | Rows face the screen; RESPOND steady in the second frame; nothing else moved |
| P7 | QA + acceptance | QA-55 (prompts: projector, S5, Harriet, D04 only), QA-56, QA-57 (hero = projector) | §3.2.7 | §3.2.7 |

### 3.2.7 ACCEPTANCE CAPTURE
- Camera A (the hearth): **(0, −380, 148) → look-at (0, 400, 150)**, DAY ON AIR, Day 1 post volume. Sees: cue signs over the ENTRY door, S5 under its lamp at left, chairs casual, Harriet in her chair.
- Camera B (the pair that sells the game): **(350, 250, 148) → look-at (−478, 100, 160)**, SCREENING state, then again post-lockdown ROWS — the art bible asks for exactly this pair [restoration-art-bible.md §7 REC ROOM].
- Checklist: (1) warmest, safest light of the five rooms; (2) one hero (projector) by wear; (3) D04 findable behind glass; (4) three ambient items present and promptless; (5) Harriet's cup height matches the day; (6) no grain/scanline on any compound surface, phosphor only on the screen and the CAM 1 monitor; (7) store-page test.

### 3.2.8 OPEN
- **3.2-A** Interactable count: cap 2/1/14 vs inventory §3 (TV, chairs, shrine, projector, S5, Harriet's chair, board game, albums, rack all listed as touchable). This brief: I = projector + S5; everything else promptless. Owner to confirm.
- **3.2-B** Is the cabinet TV dark by day, or does it carry the 4:3 static only at N1?
- **3.2-C** Reference screen centre Z 160 vs a floor-standing console's screen height (≈ Z 100).
- **3.2-D** Wall clock reference sits at room centre (0, 0, 230): which wall does it hang on?
- **3.2-E** Windows: none in the data; "moonless windows" [lighting bible NIGHT] implies some rooms have them — does the rec room?

---

## 3.3 · KITCHEN — Merle's sovereign nation

### 3.3.1 IDENTITY
| Field | Value | Source |
|---|---|---|
| Rooms.csv | `KITCHEN, 8.0, 0.0, 6.0, 5.0` → centre (800, 0), 6 × 5 m | Data/Rooms.csv |
| Floor bounds (uu) | X 500..1100, Y −250..250 | derived |
| Door → REC ROOM | open gap (500, 0), 1.4 m (Y −70..70) in the −X wall; no slab; not locked | Data/Doors.csv |
| Other walls | +X, +Y, −Y face unstamped exterior/void | Data/Rooms.csv |
| Stations / Monitors | none / none | Data/Stations.csv; Data/Monitors.csv |
| Demo | open | Data/DemoOpen.csv |
| Reference placements (Godot → UE) | Counter run 5.0 m long along X on the −Y wall: block at (8.0, 0, −2.15) → **(800, −215, 0)**, 0.58 deep, cabinets 0.86 high, counter top at **Z 91** (0.885 + 0.025) · KETTLE (9.4, 0.91, −2.1) yaw 0.6 → **(940, −210, 91)** · two mugs (8.4, 0.91, −2.2) → (840, −220, 91) and (8.62, 0.91, −2.05) → (862, −205, 91) · break table 0.9 × 0.9 top at (9.6, 0.74, 1.0) → **(960, 100, 74)** on a single pedestal · KEY BOARD: EDITH key (10.6, 1.2, −2.3) → **(1060, −230, 120)**, TRAINING key (10.2, 1.2, −2.3) → **(1020, −230, 120)** → the board hangs on the −Y wall above the counter's +X end · Merle (8.0, 0, −1.0) → **(800, −100, 0)** at the counter | world_builder.gd `_spawn_kitchen` 1265–1306, `_spawn_keys` 776–782, `_spawn_club` 1061; prop_kit.gd `kitchen_block`, `kettle` |

### 3.3.2 ROLE
| Aspect | Canon | Source |
|---|---|---|
| Personality | "Merle's sovereign nation. Amber plus the kettle's glow (a real light)." Bed: kettle lifecycle, refrigerator sigh. Keynotes: menu chalkboard, recipe box, two aprons and one hook | restoration-room-bible.md KITCHEN |
| Budget | 1 / 1 / 12; drift: chalkboard menu, jar order; web: the kettle click-off is a death beat; recipes become accessions if she goes (V-R3) | restoration-room-bible.md KITCHEN; PROGRESS.md 3.3 |
| Dread role | WARMTH: "Merle makes Chum scarier … the kettle's warmth is load-bearing dread infrastructure, which is why its click-off is a death beat." No scare is ever delivered through the kitchen | restoration-dread-doctrine.md AMPLIFIERS; restoration-walkthrough-levels-endings.md Part IV Rules "The comfort is never the trap" |
| Merle's death ripples | Kitchen goes cold; the kettle never moves again and its stillness is rundown-audible (the hunter lingers); coat pegs freeze at her peg's day | restoration-casualty-ledger.md MERLE RIPPLES |
| Kettle text | `[THE KETTLE, TWO ROOMS AWAY, CLICKS OFF]`; "The kettle, two rooms away, clicks off by itself." (two rooms from the bench, i.e. the geography is load-bearing) | Data/GameText.csv lines 141–142 |
| Merle drift | Begins already warm (mustard apron from Day 1) and never drifts — the constancy is the tell; she narrates herself ("Now Merle is just going to put the kettle on") | restoration-art-bible.md §5 MERLE; restoration-game-master.md T1.6 |
| Beats | T1.2 "kitchen never closes" · T2.5 "HE ASKS SO MANY QUESTIONS" (kitchen; the dried-past-dry plate at the rack) · T2.8 aftermath: Vess in the kitchen doorway, pin in fist, label maker clicking · T2 key board: TRAINING (film cabinet, Leland's green tag) and EDITH (shed, from T4) · T3 kitchen circuit sub-panel (ASK: Merle unlocks it, with questions; FORCE is cutting dorm heat and the club notices) | restoration-game-master.md T1.2, T2.5, T2.8, §table "Power shortfalls"; restoration-room-inventory.md §4 |
| Key texts | `KEY BOARD`; `the EDITH key, felt-tagged in a child's hand`; `the TRAINING key, tagged in green ink` | Data/GameText.csv lines 677, 676, and the TRAINING line via world_builder.gd 780 |
| Reaction web | M-R1 kitchen smells scheduled to your habits; M-R2 extra sandwich; M-R3 she narrates the object's story when you snoop; M-R5 the second teacup retired from the rack (Harriet doubled) — "the saddest line of set dressing in the game"; M-R6 Vess's name at breakfast | restoration-reaction-matrix.md MERLE |
| Route | Day 1 spine REC → KIT → DRM; airdate circuit passes "KIT hallway listings" (framed TV listings, hallway) | restoration-player-routing.md Day 1 spine, optional loop |
| Inventory listing | Kettle (inspect), key board (T2 take), framed TV listings hallway (T2), kitchen circuit sub-panel (T3 COND operate), casserole dishes/plate rack, fridge + magnets (children's drawings, one signed T.A.), coffee urn (use) | restoration-room-inventory.md §4 — reconciled in OPEN 3.3-A |

### 3.3.3 LIGHTING STATE TABLE
| State | Locked EV | Practicals | Red reads? | Transition | Source |
|---|---|---|---|---|---|
| DAY ON AIR | **OPEN** | P-K1 amber overhead (one real fixture, proposed (800, 0, 290)) · P-K2 under-cabinet/over-counter amber tube or bulb along the −Y wall (proposed (800, −200, 200)) · **P-K3 THE KETTLE'S GLOW — a real light source** at (940, −210, 91): the bible names the glow, not the mechanism — **OPEN 3.3-B** (stove element under the kettle vs an electric kettle's indicator). Colour amber/warm; intensity OPEN | No tally; no red | CUT | restoration-room-bible.md KITCHEN; restoration-lighting-bible.md §UE5 TECHNICALS |
| BREAK | **OPEN** | Same (no tally to die) | — | CUT | OPEN 0-F |
| NIGHT | **OPEN** | Practicals off; standby LEDs (fridge, urn); "kitchen never closes" [T1.2] — whether the kettle glow persists at night is **OPEN 3.3-C** | none | CUT | restoration-lighting-bible.md §STATES NIGHT |
| MERLE GONE (room-specific, casualty state) | **OPEN** | The kettle never moves again; kitchen goes cold — whether P-K3 goes dark is OPEN 3.3-C; ending 3's epilogue: "the kitchen light was on. Nobody had eaten." | — | — | restoration-casualty-ledger.md MERLE RIPPLES/ENDINGS |
| CASCADE | **OPEN** — the kitchen has its own circuit sub-panel (T3) so it is plausibly its own zone; not stated | — | — | panel order | restoration-room-inventory.md §4; lighting bible CASCADE |
| 4c | **OPEN** | Third room out in Day 1 order (after ENT, REC) | — | room-by-room | lighting bible 4c; player-routing Day 1 spine |

### 3.3.4 FIXED PROPS
| Prop | Tier | Interact? | Real dims (m) | Placement (uu) | Asset candidate · licence |
|---|---|---|---|---|---|
| KEY BOARD (EDITH + TRAINING keys on tags) — the HERO | Interactable | YES — keys are pickups (`KEY BOARD` label; key strings above) | board 0.3 × 0.25; keys 0.06 with felt/paper tags | on the −Y wall at (1040, −248, 120), keys at (1060, −230, 120) and (1020, −230, 120) [world_builder.gd 778–780] | Bespoke: pine board, brass hooks; keys from Poly Haven search "key" *(verify id)* CC0 or bespoke; EDITH tag is FELT in a child's hand (M_Wool-adjacent felt), TRAINING tag paper in green ink (M_Paper) |
| THE KETTLE (stovetop, steel) | Dressing-tier PRACTICAL + state object (never drifts; stills when Merle dies) | NO prompt under the 1/1/12 cap (inventory `inspect` — OPEN 3.3-A) | body Ø0.20 × 0.14 + spout/handle ≈ 0.25 tall | (940, −210, 91), yaw 0.6 rad [world_builder.gd 1273] | Poly Haven search "kettle" *(verify id)* CC0; else bespoke; brushed steel with real dents in normal map; the glow per P-K3 |
| Counter run (cabinets, doors with knobs, counter top, sink) | Dressing (collision) | NO | 5.0 × 0.58 × 0.91 | (800, −215, 0) along X [world_builder.gd 1269–1271] | Fab search "kitchen cabinet vintage" (Megascans/Fab free) or bespoke per prop_kit `kitchen_block` (door faces 0.44 × 0.62, knob Ø0.036); counter laminate: AmbientCG search "Laminate"/"Terrazzo" *(verify id)* |
| Break table (single pedestal) | Dressing | NO | 0.9 × 0.9 × 0.74 | (960, 100, 0) [world_builder.gd 1295] | Poly Haven `wooden_table_02` *(verify id)* CC0 or `coffee_table_round_01` *(verify id)*; the reference is square on one pedestal |
| Two mugs "nobody collected" | Dressing (biography: Merle's two) | NO | Ø0.08 × 0.09 | (840, −220, 91), (862, −205, 91) | Poly Haven `tea_set_01`/"mug" *(verify id)* CC0; OCHRE tint (0.89, 0.64, 0.24) per prop_kit OCHRE |
| Mug hook rail: six hooks, five mugs | Dressing (ambient lore host) | NO | rail 0.6 | −Y wall above counter (700, −248, 150) | bespoke rail + 5 mugs |
| Menu chalkboard | Dressing (drift: menu) | NO | 0.6 × 0.9 | +Y wall (800, 248, 160) | Fab search "chalkboard"; chalk text in albedo; must be re-authorable per day (dressing-tier drift) |
| Recipe box | Dressing (V-R3 accessions if she goes) | NO | 0.15 × 0.12 × 0.10 | counter (700, −215, 91) | bespoke tin/wood box; cards under M_Paper |
| Two aprons, one hook (one apron mustard = Merle's Day 1 constant) | Dressing | NO | apron 0.6 × 0.9 hanging | +X wall (1098, −150, 170) | cloth cards under M_Wool-family cotton; MUSTARD #C9A33D for hers |
| Refrigerator + magnets (children's drawings; one signed T.A.) | Dressing (bed: refrigerator sigh) | NO | 0.7 × 0.7 × 1.7 | +X wall (1060, 180, 0) | Fab search "refrigerator vintage 70s"; drawings under M_Paper |
| Plate rack + casserole dishes (the dried-past-dry plate, T2.5) | Dressing | NO | rack 0.5 × 0.3 | counter end (600, −215, 91) | Fab search "dish rack"; Poly Haven search "plate"/"casserole" *(verify id)* CC0 |
| Coffee urn | Dressing (inventory `use` — OPEN 3.3-A) | NO | Ø0.25 × 0.45 | counter (1000, −215, 91) | Fab search "coffee urn" |
| Kitchen circuit sub-panel (T3 COND) | Interactable in the inventory; **not in the reference build**; exceeds the 1 cap | OPEN 3.3-A | 0.3 × 0.4 | +X wall (1098, 60, 160) | Megascans "electrical panel" if free; breaker toggles under M_Enamel (warning red only on the breaker per art bible §4) |
| Cabinet door (host of the feeding-rotation lore, taped inside) | Dressing | NO | 0.44 × 0.62 | one counter door, e.g. (720, −186, 42), openable ajar | part of the counter run |
| Surfaces | — | — | floor 30 m² | — | Floor: Megascans "linoleum/checker" (FAB-IMPORT starter) → `MI_Kitchen_Floor`; walls: painted plaster + tile splashback along the −Y wall (Megascans "ceramic tile") → `MI_Kitchen_Wall`, `MI_Kitchen_Tile`; ceiling: painted plaster |

### 3.3.5 LORE ITEMS
| Item | Tag | Sits | Text key | Source |
|---|---|---|---|---|
| Recipe card CHUM'S BIRTHDAY SHEET CAKE, SERVES 60, amended to SERVES 12, then to nothing | HC, T1 | Front card of the recipe box, lid open | none | restoration-ambient-lore-ledger.md KITCHEN |
| Six mug hooks, five mugs; the empty hook is the most polished | T3 | The mug rail above the counter | none | restoration-ambient-lore-ledger.md KITCHEN |
| Taped inside a cabinet door: a volunteer feeding rotation dated the week after the fire, all names crossed off but one | T5, HF | Inside the ajar counter door | none | restoration-ambient-lore-ledger.md KITCHEN |
| Framed TV listings (airdate source two of four) — the inventory places these in the "hallway" | inventory T2 | **OPEN 3.3-D** — no hallway exists in the data between REC and KITCHEN (the gap is 1.4 m in a 0.24 m wall); nearest honest home is the kitchen's −X wall beside the gap at (502, 150, 160) | none stated | restoration-room-inventory.md §4; restoration-player-routing.md airdate circuit |
| Handled L=1 | — | No D-series readable is homed in the kitchen; the L cap's occupant is OPEN 0-G/3.3-D | — | — |

### 3.3.6 DRESSING PASSES
| # | Pass | Steps | Verification capture | Must read |
|---|---|---|---|---|
| P0 | Data check | Bounds X 500..1100 / Y ±250; one gap at (500, 0) 1.4 m; no slab | top-down (800, 0, 900) → (800, 0, 0) | Exact |
| P1 | Surfaces | Linoleum floor with worn lane from the gap to the kettle; plaster walls; tile splashback −Y; ceiling | (520, 0, 148) → (940, −210, 91) (from the doorway, at the kettle) | Worn lane reads as habit; three-way light break; tile grout in normal map |
| P2 | Fixed props | Counter run, key board + keys, kettle, mugs, table, fridge, rack, urn, chalkboard, recipe box, aprons, cabinet door ajar | (520, 0, 148) → (940, −210, 91) | The key board reads as hero (polished hooks, tag wear); the kettle is the eye-magnet; counter top exactly Z 91 (Merle's hands land on it) |
| P3 | Practicals + EV | P-K1, P-K2, P-K3 with true bulb/element geometry; delete the stand-in lamp; lock DAY EV; author NIGHT | DAY and NIGHT from (520, 0, 148) → (940, −210, 91) | The kettle's glow is visibly a LIGHT (bounce on the tile and the counter), not an emissive sticker; at NIGHT the floor still resolves |
| P4 | Lore FIRST | Recipe card (SERVES 60 → 12 → nothing), mug rail (6 hooks, 5 mugs, polished empty hook), feeding rotation inside the door, TV listings | 1 m closeups: (700, −120, 148) → recipe box; (700, −150, 150) → rail; (720, −100, 120) → inside the door | All promptless; each legible at 1 m and invisible at 3 m; polished hook reads via roughness only |
| P5 | Dressing mass (≤ 12) | Jars in an order (drift hook), tea towel (mustard on Day 2 per art bible §4 — the first drifted prop), dish soap, kettle trivet, calendar, crocheted key fob hook, radio, bread bin, spice rack, second teacup on the rack (retires on M-R5), casserole on the table, a chair | (520, 0, 148) → (960, 100, 74) | ≤ 12; each owned; nothing fake-affords |
| P6 | Wear/decals/drift | Steam stain above the kettle, ring marks, scuffs at the gap; drift hooks: chalkboard menu, jar order (dressing); state hook: kettle stillness + glow on Merle's death (OPEN 3.3-C) | Day 1 vs Day 2 pair (tea towel neutral → mustard) | Only the towel changed |
| P7 | QA + acceptance | QA-55 (prompts: keys only; kettle promptless unless 3.3-A rules otherwise), QA-56, QA-57 (hero = key board) | §3.3.7 | §3.3.7 |

### 3.3.7 ACCEPTANCE CAPTURE
- Camera A (Merle's nation): **(520, 0, 148) → look-at (940, −210, 91)**, DAY ON AIR, Day 1 post volume.
- Camera B (the death beat, geography): **(940, −100, 148) → look-at (940, −210, 91)** at 1 m, NIGHT, kettle glow state per 3.3-C.
- Checklist: (1) amber plus a real kettle light; (2) key board hero by wear; (3) five mugs six hooks, recipe card, feeding rotation present and promptless; (4) Merle's apron mustard, everything else neutral on Day 1; (5) counter at Z 91; (6) no scare geometry — the room must feel kind; (7) store-page test.

### 3.3.8 OPEN
- **3.3-A** Interactable count: cap 1/1/12 vs inventory §4 (kettle inspect, key board take, listings, sub-panel operate, dishes, fridge, urn use). This brief: I = key board; kettle is a practical/state object without prompt. Owner to confirm, especially the T3 sub-panel (a routing-critical interactable that would breach the cap).
- **3.3-B** The kettle's glow: stove element or electric indicator? Determines the fixture geometry.
- **3.3-C** Kettle glow at NIGHT and after Merle's death.
- **3.3-D** "Framed TV listings, hallway": no hallway exists in Rooms.csv between REC and KITCHEN.

---

## 3.4 · DORMS — five doors, three slept-in

### 3.4.1 IDENTITY
| Field | Value | Source |
|---|---|---|
| Rooms.csv | `DORMS, -9.0, 0.0, 8.0, 5.0` → centre (−900, 0), 8 × 5 m, **a single box with no interior partitions in the data** | Data/Rooms.csv |
| Floor bounds (uu) | X −1300..−500, Y −250..250 | derived |
| Door → REC ROOM | open gap (−500, 0), 1.4 m in the +X wall; no slab; not locked | Data/Doors.csv |
| Other walls | −X, +Y, −Y face unstamped exterior; the +Y wall looks across ≈ 12 m of unstamped ground toward the tower at (−900, 1450) | Data/Rooms.csv; world_builder.gd 1234 |
| Stations / Monitors | none / none | CSVs |
| Demo | open | Data/DemoOpen.csv |
| Reference placements (Godot → UE) | RITA'S BED (−9.0, 0.3, 1.5), 2.0 × 1.1 footprint, long axis X → **(−900, 150, 30)**; headboard at the −X end; blanket, one pillow, "made every morning" · DRESSER (−11.5, 0.28, −1.8) 1.7 × 0.5 × 0.56 → **(−1150, −180, 28)** against the −Y wall · D05 WELCOME PACKET (−11.9, 0.9, −1.0) → **(−1190, −100, 90)** · Bed A (−12.0, 0, 1.6) → (−1200, 160, 0) · Bed B (−6.2, 0, 1.6) → (−620, 160, 0) · Lockers, run of 4, 1.8 × 0.55 × 1.9 at (−7.2, 0, −2.2) → **(−720, −220, 0)** against the −Y wall · VESS'S ROOM (research binder dock) (−6.5, 0.6, 1.8) → **(−650, 180, 60)** | world_builder.gd `_spawn_bed_and_dresser` 587–656, `_spawn_dorms_extra` 1395–1408, `_spawn_club` 1053 |

### 3.4.2 ROLE
| Aspect | Canon | Source |
|---|---|---|
| Personality | "Five doors, three slept-in; the club sleeps where it worked. Practicals per room, hall gap authored." Bed: radiators, one door that settles. Keynotes: D05 welcome folder, name cards (one blank), Rita's unadorned room | restoration-room-bible.md DORMS |
| Budget | 1 / 1 / 10; drift: which doors stand open; web: the blank card is a shard | restoration-room-bible.md DORMS; PROGRESS.md 3.4 |
| Dread role | "The dresser is the game's quietest horror meter; by a bad run's end the room is nearly empty" — CONSEQUENCE MEMORY (the world keeps receipts) | restoration-room-inventory.md §5 State changes; restoration-dread-doctrine.md AMPLIFIERS |
| The seven items | Watch, pen, photograph, lighter, compact, keys, loupe — one vanishes per capture, loupe last; each reappears as a prop inside restored episodes | restoration-walkthrough-levels-endings.md Part V-B "What Each Capture Takes"; restoration-room-inventory.md §5 |
| Texts | `RITA'S BED · sleep until morning (E)`, `RITA'S BED · end the day (E)`, `The club insists you sleep at home until the contract is signed.`, `RITA'S DRESSER · take stock (E)`, `Seven things, squared to the dresser's edge. Everything where you left it.`, `your %s is gone from the dresser. it will be in the footage.`, `VESS'S ROOM`, `WELCOME PACKET · mimeograph purple` | Data/GameText.csv lines 38–40, 111–112, 258, 693, 700 |
| Beats | T1.2 Merle at the dorm door: "Yours. Bath down the hall, kitchen never closes, and if the tower light bothers you, the curtain's thick." · D05 on Rita's dresser Day 1 · T2 FORCE: Vess's binder (G2) from his room, door ajar; the credit flag dies if his insight is cited unnamed · Bed advances day/night; DAY 1 objective "end the day at Rita's bed" · Harriet's room never opens (everything inside mid-motion) · Merle's room open-door policy, quilt drifts to show palette by T4 · Mirror obeys the reflection budget (from T3 her reflections compose better) · Thick curtain blocks the beacon, "purely humane" · communal bath mirror | restoration-game-master.md T1.2, T2.1 [FORCE, G2]; restoration-props-packet.md D05, D07; Data/GameText.csv 184; restoration-room-inventory.md §5 |
| Route | The pendulum: Tape 1 trains a home loop Dorms → Rec → Library → Bench until muscle memory; later acts violate it | restoration-player-routing.md §1 |
| Sanctuary | Not a sanctuary; the lockdown seals doors "on schedule" (T4.10) | restoration-game-master.md T4.10 |

### 3.4.3 LIGHTING STATE TABLE
| State | Locked EV | Practicals | Red reads? | Transition | Source |
|---|---|---|---|---|---|
| DAY ON AIR | **OPEN** | "Practicals per room, hall gap authored": one amber bedside/ceiling practical per sleeping bay (proposed P-D1 Rita (−900, 220, 200) wall lamp above the headboard side; P-D2 bay A (−1200, 220, 200); P-D3 bay B (−620, 220, 200)); the hall/shared floor keeps an authored GAP (no fixture) between bays — the gap is content | No tally; no red by day | CUT | restoration-room-bible.md DORMS; restoration-lighting-bible.md §UE5 TECHNICALS CORRIDORS "the gaps are content" |
| BREAK | **OPEN** | Same | — | CUT | OPEN 0-F |
| NIGHT | **OPEN** | Practicals off; **the tower light through the +Y window** unless the thick curtain is drawn (curtain = operable, humane); standby LED on Vess's label maker charger (proposal); floor must resolve | Red beacon leak — not a tally (OPEN 0-F) | CUT | restoration-game-master.md T1.2; restoration-room-inventory.md §5 Thick curtain; lighting bible NIGHT "moonless windows" |
| CASCADE | **OPEN** | FORCE path cuts "dorm heat" (radiators), not light — lighting zone unknown | — | — | restoration-room-inventory.md §4 |
| 4c | **OPEN** | Fourth room out in Day 1 order | — | room-by-room | lighting bible 4c; player-routing Day 1 spine |
| Colour script | Day 1 warmest; OPEN | — | — | — | lighting bible |

### 3.4.4 FIXED PROPS
| Prop | Tier | Interact? | Real dims (m) | Placement (uu) | Asset candidate · licence |
|---|---|---|---|---|---|
| RITA'S BED — the HERO (day/night driver) | Interactable | YES — bed texts above | 2.0 × 1.1 × 0.5 (frame 0.24 + mattress 0.2); headboard 0.7 high at the −X end | (−900, 150, 30) footprint centre; collision 2.0 × 0.6 × 1.1 [world_builder.gd 589–593] | Fab search "single bed metal frame vintage" or Poly Haven search "bed" *(verify id)* CC0; blanket tucked hard (cloth normal in maps), one pillow; neutral tints per rec: blanket (0.42, 0.34, 0.26), pillow (0.8, 0.77, 0.7) |
| RITA'S DRESSER with the seven items | Interactable (DYN) — **exceeds the 1 cap with the bed; OPEN 3.4-A** | YES in the reference (`RITA'S DRESSER · take stock (E)`) | 1.7 × 0.5 × 0.56 (reference; a real dresser is ≈ 0.8–0.9 high — **OPEN 3.4-B**) | (−1150, −180, 28) against the −Y wall [world_builder.gd 642] | Poly Haven `vintage_wooden_drawer_01` *(verify id)* CC0 or Fab search "dresser vintage"; seven hero-small props: watch, pen, photograph, lighter, compact, keys, loupe — bespoke, each squared to the edge; each removable by state |
| D05 WELCOME PACKET (handled lore, mimeograph purple) | Handled lore | YES — `WELCOME PACKET · mimeograph purple` + 3 lines [GameText 700–703] | one page 0.216 × 0.279 | on the dresser at (−1190, −100, 90) — reference floats at Z 90 above a Z 56 top; sit it ON the top (Z ≈ 57) or on the OPEN 3.4-B taller dresser | M_Paper (4K allowed for readables); purple mimeograph ink; Merle's ballpoint annotations in a second layer |
| Vess's room (door ajar) + research binder D07 | Handled lore (D07) behind a FORCE path; dock label `VESS'S ROOM` | binder YES (T2 take, FORCE) | door 0.9 × 2.1 ajar 15°; binder 0.3 × 0.28 × 0.06 three-ring | bay B: binder at (−650, 180, 60) [world_builder.gd 1053]; spare label maker beside it | Fab search "ring binder"; printouts under M_Paper; label maker bespoke |
| Beds A and B (two of the other slept-in bays) | Dressing (biography: Merle's with quilt drifting to show palette by T4; Vess's neutrals) | NO | 2.0 × 1.1 | (−1200, 160, 0), (−620, 160, 0) [world_builder.gd 1398, 1402] | same bed family; quilt for Merle's under M_Wool with drift-tint parameter |
| Lockers, run of 4 | Dressing (the name-card host if doors are lockers — OPEN 3.4-C) | NO | 1.8 × 0.55 × 1.9 | (−720, −220, 0) [world_builder.gd 1406] | Megascans "metal locker" (starter list "metal shelving" family) or Fab search "locker vintage"; painted steel under M_Enamel |
| Five doors (three slept-in; door four with the blank card; Harriet's never opens; one door settles) | Dressing (drift: which stand open) — **geometry OPEN 3.4-C** | NO (Harriet's door: inspect through, never opens) | 0.9 × 2.1 each | proposed as five door frames on the −Y wall between the lockers and the corners, 1.2 m pitch: X −1250, −1130, −1010, −890 (door four), −770 — or as partition flats making bays — see 3.4-C | Fab search "interior door wooden painted"; name cards under M_Paper |
| Mirror (reflection budget) + communal bath mirror | Dressing, scripted reflection | NO | 0.4 × 0.6 | on the −X wall (−1298, 60, 160) | planar reflection or SceneCapture per port; frame bespoke |
| Thick curtain + window on the +Y wall (latch painted shut from inside) | Dressing, operable (humane) — **window needs a wall cut not in Doors.csv: OPEN 3.4-D** | curtain operable per inventory | window 1.0 × 1.2; curtain 1.4 × 1.6 | +Y wall at (−900, 248, 150) above Rita's headboard side | Curtain cloth under M_Wool-family; latch in maps |
| Radiators (bed: radiators) | Dressing | NO | 1.0 × 0.2 × 0.6 cast iron | under the window (−900, 235, 0) and one per bay | Fab search "cast iron radiator" (Megascans if free) |
| The binder (meta UI home) | Interactable (global UI) — lives with Rita, not the room | — | — | — | UI, not dressing |
| Surfaces | — | — | floor 40 m² | — | Floor: Megascans "worn parquet" or "linoleum" → `MI_Dorms_Floor` (bays may carry rugs); walls: painted plaster, neutral → `MI_Dorms_Wall` (wall tones never drift); ceiling: plaster |

### 3.4.5 LORE ITEMS
| Item | Tag | Sits | Text key | Source |
|---|---|---|---|---|
| D05 WELCOME PACKET (HANDLED) | house rules | Rita's dresser, Day 1 | `WELCOME PACKET · mimeograph purple` + lines 701–703 | restoration-props-packet.md D05; Data/GameText.csv |
| The blank name card on door four; inside, a wallpaper square brighter than its wall where something hung the length of a warning | T3 | Door four (position per OPEN 3.4-C); the bright square on the bay's wall behind the door, ≈ 0.3 × 0.4 at Z 150 | none | restoration-ambient-lore-ledger.md DORMS |
| The welcome folder's earlier revision misfiled beneath the shelf liner, listing a room count of six | HC | Under the liner of the dresser's top drawer (opens on inspect? — no: ambient never prompts; make the liner corner lifted so the page edge shows) | none | restoration-ambient-lore-ledger.md DORMS |
| Window latch on the yard side painted shut from the inside | HF | The +Y window latch | none | restoration-ambient-lore-ledger.md DORMS |
| D07 VESS'S RESEARCH BINDER (HANDLED, FORCE) | insight + error | Vess's bay, door ajar | dock label `VESS'S ROOM`; body per props packet | restoration-props-packet.md D07 |

### 3.4.6 DRESSING PASSES
| # | Pass | Steps | Verification capture | Must read |
|---|---|---|---|---|
| P0 | Data check | Bounds X −1300..−500 / Y ±250; one gap (−500, 0) 1.4 m | top-down (−900, 0, 900) → (−900, 0, 0) | Exact; resolve 3.4-C/3.4-D BEFORE P1 (partition flats and a window cut change what P1 covers) |
| P1 | Surfaces | Floor, walls, ceiling; rugs per bay; skirting | (−520, 0, 148) → (−1300, 0, 150) | Neutral walls; floor wear lanes to each slept-in bay and none to the two unused |
| P2 | Fixed props | Rita's bed + dresser + seven items; beds A/B; lockers; five doors (or frames); mirror; radiators; window + curtain; Vess's binder + label maker | (−520, 0, 148) → (−900, 150, 60) | Rita's bay unadorned (bible); Merle's bay warm; Vess's bay tidy-obsessive; the two unused bays read unused (dust, no wear) |
| P3 | Practicals + EV | P-D1..D3 with true bulbs; authored hall gap; window leak of the tower light at NIGHT; curtain state; delete stand-in lamp; lock EVs | DAY: (−520, 0, 148) → (−1300, 0, 150); NIGHT curtain open: (−700, −100, 148) → (−900, 248, 150); NIGHT curtain drawn: same | DAY: three pools, one dark gap; NIGHT open: red leak on the pillow, floor still resolves; NIGHT drawn: no red, floor still resolves |
| P4 | Lore FIRST | D05 on the dresser; blank card on door four + bright wallpaper square; liner-corner revision page; painted-shut latch | 1 m closeups: (−1150, −80, 148) → D05; door four at 1 m; (−900, 150, 148) → latch | D05 prompts inside 2.6 m; the three ambient items never prompt; bright square reads via albedo only |
| P5 | Dressing mass (≤ 10) | Name cards on the other four doors, Merle's quilt, Vess's spare label maker + label strips, a bath towel, Rita's suitcase (unpacked), a hallway runner, a clock, a wash basin, a chair with a cardigan, a wastebasket | (−520, 0, 148) → (−1300, 0, 150) | ≤ 10; each owned |
| P6 | Wear/decals/drift | Door-settle offset on one door (dressing drift: which doors stand open, monotonic); scuffs at the gap; radiator rust; seven-item removal states wired (state, not drift — interactable tier never drifts) | Day 1 vs Day 4 pair | Only door-open states and Merle's quilt tint changed |
| P7 | QA + acceptance | QA-55 (prompts: bed, dresser [OPEN 3.4-A], D05, D07, curtain), QA-56, QA-57 (hero = bed) | §3.4.7 | §3.4.7 |

### 3.4.7 ACCEPTANCE CAPTURE
- Camera A (Rita's room, unadorned): **(−700, −100, 148) → look-at (−1150, −180, 60)** — dresser with seven items and D05 in frame, bed at right; DAY ON AIR, Day 1.
- Camera B (the tower through the curtain): **(−700, −100, 148) → look-at (−900, 248, 150)**, NIGHT, curtain open.
- Checklist: (1) practicals per bay with an authored gap; (2) seven items squared to the dresser's edge; (3) D05 findable, purple; (4) blank card on door four, promptless; (5) at NIGHT the beacon leaks in and the floor still resolves; (6) Harriet's door reads as never-opened; (7) store-page test.

### 3.4.8 OPEN
- **3.4-A** Interactable count: cap 1/1/10 vs reference (bed, dresser, D05, D07/binder, curtain). This brief keeps the reference prompts and flags the breach.
- **3.4-B** Dresser height: reference 0.56 m vs real-world ≈ 0.85 m (scale truth).
- **3.4-C** "Five doors, three slept-in" vs a single 8 × 5 m box with no partitions in Rooms.csv: dress as five door frames on one wall (bays implied) or add dressing-tier partition flats (which alter navigation and Chum's routes)? Decide before P1.
- **3.4-D** The +Y window (tower light, painted-shut latch) requires a wall opening that Doors.csv does not carry; the greybox has no windows. Wall-cut authority is the data pipeline, not dressing.

---

## 3.5 · YARD — the only sky the game owns

### 3.5.1 IDENTITY
| Field | Value | Source |
|---|---|---|
| Rooms.csv | `YARD, 0.0, 14.0, 30.0, 8.0` → centre (0, 1400), 30 × 8 m | Data/Rooms.csv |
| Floor bounds (uu) | X −1500..1500, Y 1000..1800 | derived |
| Perimeter | The stamper runs 3 m walls around EVERY room including the yard; only the ceiling lamp is skipped for YARD → the yard's perimeter is currently four 3 m walls — **OPEN 3.5-A** (fence vs wall) | build_greybox.py lines 107–116 |
| Door → ENTRY | `ENTRY, YARD, 0.0, 10.0, 1.6, x, door` → (0, 1000), slab | Data/Doors.csv |
| Door → SHED | `YARD, SHED, 8.5, 14.0, 1.2, z, locked:PADLOCKED · the tag reads EDITH · a key exists|EDITH` → gap (850, 1400), 1.2 m in the shed's −X face; slab; **LOCKED**, reason text at (850, 1400, 290), key id EDITH (from the kitchen key board) | Data/Doors.csv; Data/GameText.csv 655 |
| SHED (unit 3.6; exterior only here) | `SHED, 10.0, 14.0, 3.0, 3.0` → X 850..1150, Y 1250..1550; 3 m walls | Data/Rooms.csv |
| Stations / Monitors | none / none | CSVs |
| Demo | NOT in DemoOpen.csv (Tape 1 demo does not open the yard) | Data/DemoOpen.csv |
| Reference placements (Godot → UE) | TOWER rig (−9.0, 0, 14.5) → **(−900, 1450, 0)**, `PropKit.tower(7.5)`: 7.5 m tall lattice, base 1.4 m square tapering to 0.3 m, four sections with cross braces, red beacon (emission (1.0, 0.12, 0.08)) at the top; collider 1.5 × 2.4 × 1.5 · Pallets (−6.5, 0.06, 13.0) → (−650, 1300, 6) and (−6.2, 0.06, 15.6) → (−620, 1560, 6), three slats 1.1 × 0.05 × 0.24 at 0.35 pitch · Packed dirt 29.6 × 7.6 m at (0, 1400, 1.5) · Worn path leg 1: 1.1 × 4.2 m at (0, 1240) (entry door toward the middle) · leg 2: 8.6 × 1.1 m at (420, 1400) (to the shed door) | world_builder.gd `_spawn_yard_dressing` 1230–1254, `_spawn_yard_ground` 1309–1333; prop_kit.gd `tower` 482–510 |
| Beacon rule in code | On ending "THE COMPLETED SIGN-OFF" (4c) the beacon's emission turns off and its albedo goes to (0.25, 0.1, 0.08) | world_builder.gd 1238–1243 |

### 3.5.2 ROLE
| Aspect | Canon | Source |
|---|---|---|
| Personality | "The only sky the game owns. Night exterior, tower light visible and steady." Bed: wind, wire hum, gravel. Keynotes: laundry line, antenna guy-wires, distance measured in dark | restoration-room-bible.md YARD |
| Budget | 0 / 1 / 8; drift: laundry count; web: the tower light's meanings (premiere, 4c) read from here | restoration-room-bible.md YARD; PROGRESS.md 3.5 |
| Beacon pulse vs steady | Walkthrough: "under the red beacon's slow pulse. The beacon blink is a rhythm players can time movement to"; game master T4.7 "Movement timed to the blink"; room inventory §1 "Beacon pulse is a night movement metronome; never operable". Room bible: "tower light visible and steady" — **OPEN 3.5-B** | restoration-walkthrough-levels-endings.md Part II Exterior; restoration-game-master.md T4.7; restoration-room-inventory.md §1; restoration-room-bible.md YARD |
| The tower light's meanings | 4c: "…entry last, then the tower light, then nothing, as rest"; demo/title string `the tower light stays on` / `TAPE 1 · FREE DEMO · the tower light stays on`; ending: "The transmitter unclenches. The tower light, for the first time, …" | restoration-lighting-bible.md §STATES 4c; Data/GameText.csv 78, 642, 340 |
| Beats | T1.1 arrival at dusk: "the compound crouches on the hill under the tower's red pulse … wind in guy wires, a hand-painted sign over industrial steel: THE 58 CLUB, EST. WITH LOVE" · Night 7 (T4): ENT → EXT under the beacon → the tower-base shed → the dead room key → return before the window closes; the only mandated exterior night · T4.7 THE SHED: PRESERVE the EDITH key; FORCE bolt cutters → patrol density up that night · the secret: W2 exists behind the burn barrel (Day 3) after W1 · Gravel lot floodlight (T2, draws amperage — "a trap for the generous") · Rita's car locked in by the club's van from the T4 lockdown | restoration-game-master.md T1.1, T4.7, §table "Locked shed"; restoration-player-routing.md Night 7 spine; restoration-walkthrough-levels-endings.md ADDENDUM SPOILER; restoration-room-inventory.md §1 |
| Dread role | L2 ritual/schedule outdoors (the return before the window closes) and PATIENCE AT SCALE; "distance measured in dark" — and DARK IS A ROOM, NOT A WALL still binds outdoors | restoration-dread-doctrine.md L2, AMPLIFIERS; restoration-lighting-bible.md §GRAMMAR |
| Bell law | The zip-tied bicycle bell has its clapper removed "and it rhymes with his" — it must never sound; Chum's bell rings once, at the finale beat, and nowhere else | restoration-ambient-lore-ledger.md YARD; THE-LAWS.md 5; restoration-audio-bible.md S06 |
| Not in data | Rita's car, the 58 CLUB sign, the gravel lot floodlight, guy-wire FIELD and tower BASE as a zone, the burn barrel, the laundry line, the fence — none are stamped; all are dressing placed inside the 30 × 8 m box (or OPEN 3.5-A beyond it) | restoration-room-inventory.md §1 vs Data/Rooms.csv |

### 3.5.3 LIGHTING STATE TABLE
| State | Locked EV | Practicals | Red reads? | Transition | Source |
|---|---|---|---|---|---|
| DAY (the yard by day) | **OPEN** — the bible describes the yard only as "Night exterior"; the art bible's Day is "overcast north key" | Sky: overcast, no sun disc (DirectionalLight + SkyAtmosphere were stripped by the stamper — restore for the yard only, motivated); the tower light on (red, static or pulsing per 3.5-B) | Tower red visible; not a tally (OPEN 0-F) | CUT | restoration-art-bible.md §8 Day; build_greybox.py 29–34; **OPEN 3.5-C** |
| NIGHT (the canonical state) | **OPEN** | Moonless sky; THE TOWER LIGHT (red) at the top of the 7.5 m rig at (−900, 1450, 750) — the yard's fixture; shed bulb spill through the shed door seam when unlocked (3.6); gravel lot floodlight T2-operable (OPEN 3.5-D: position, and it costs amperage); the entry's amber over the door through the +Y door (if 3.1-B rules the exterior door); wind/wire hum bed | Red, static, exterior | CUT | restoration-room-bible.md YARD; restoration-lighting-bible.md §STATES NIGHT; restoration-room-inventory.md §1 |
| BREAK | **OPEN** | No tally; unchanged | — | — | OPEN 0-F |
| THE PLUNGE (T5, from the studio) | — | "Total instant dark; the beacon through the skylight is the only light" — the tower light survives the plunge and reads INTO the studio | red | CUT | restoration-game-master.md §Scare table row 11 |
| 4c | **OPEN** | After the entry goes dark: the tower light goes out (emission off, albedo (0.25, 0.1, 0.08)), then nothing, as rest | red → none | last CUT in the game | restoration-lighting-bible.md 4c; world_builder.gd 1238–1243 |
| Colour script | OPEN | — | — | — | — |
| Sodium | Art bible §8 puts "sodium exterior spill at the windows" at night — the lighting bible reserves sodium for the dock — OPEN 0-D; **do not add a sodium lamp to the yard until ruled** | — | — | — | restoration-art-bible.md §8; restoration-lighting-bible.md §GRAMMAR |

### 3.5.4 FIXED PROPS
| Prop | Tier | Interact? | Real dims (m) | Placement (uu) | Asset candidate · licence |
|---|---|---|---|---|---|
| THE TOWER + red beacon (never operable) — the room's fixture, not an interactable (I = 0) | Dressing/practical | NO | reference rig 7.5 m tall, base 1.4 m sq → 0.3 m top; a real UHF mast is far taller — **OPEN 3.5-E** (scale truth vs the 8 m-deep yard; the rig's height is a design choice the owner must ratify) | base at (−900, 1450, 0); beacon at (−900, 1450, ≈750) [world_builder.gd 1234] | Bespoke lattice (Blender factory) with real angle-iron profiles (no naked box legs — §R.1); beacon glass under M_Practical with a true bulb; galvanised steel: Megascans "galvanized metal" |
| Antenna guy-wires + anchors (crimp tag 1971) | Dressing (ambient lore host; bed: wire hum) | NO | wire Ø0.01; anchors 0.3 × 0.3 × 0.6 concrete | three anchors at (−1400, 1100), (−1400, 1750), (−400, 1750) → wires to the rig's top section | Cable meshes (spline) with M_Enamel-free steel; anchors: Megascans "concrete block"; tag under M_Enamel |
| The SHED exterior (door, padlock hasp, EDITH tag) | Door = interactable (Doors table, locked) | door YES (locked reason text per Doors.csv) | shed 3 × 3 × 3 m box; door 1.2 wide; padlock 0.05; hasp 0.15 | shed at X 850..1150 / Y 1250..1550; door in its −X face at (850, 1400) | Walls: Megascans "corrugated metal"/"painted wood siding" → `MI_Shed_Ext`; padlock + hasp bespoke or Fab search "padlock"; the felt EDITH tag in a child's hand |
| Laundry line + pegs + laundry (count drifts) | Dressing (drift: laundry count) | NO | line 6 m at 1.7 m high; garments 0.6–0.9 | posts at (200, 1700) and (800, 1700); line along X | Poly Haven search "clothes line"/"towel" *(verify id)* CC0; cloth under M_Wool-family; garments in compound neutrals, drifting per the coat-peg curve only if ruled (dressing tier) |
| Burn barrel (fused film-can lids, GLADHOUSE rim stamps; W2 behind it from Day 3) | Dressing (ambient lore host; W2 spawn site) | NO (W2 is the pickup; the barrel is not) | 55-gal drum Ø0.58 × 0.88 | (−300, 1650, 0), back to the +Y perimeter | Fab search "oil drum rusted" (Megascans) ; fused-lid disk bespoke with rim stamps in the normal map (<2 cm → maps, §R.2) |
| Fence with a zip-tied child's bicycle bell (clapper removed) | Dressing (ambient lore host) | NO | chain-link 1.8 m high; bell Ø0.05 | fence run along the +Y perimeter (OPEN 3.5-A); bell at (600, 1795, 110) | Fab search "chain link fence" (Megascans); bell bespoke, clapperless (silent by law) |
| Pallets ×2 by the tower base | Dressing | NO | 1.1 × 0.94 × 0.15 | (−650, 1300, 6), (−620, 1560, 6) [world_builder.gd 1246] | Fab search "wooden pallet" (Megascans) |
| Rita's car (locked in by the van from T4) | Dressing (inventory T1 inspect — I cap is 0 → promptless; OPEN 3.5-F) | NO | ≈ 4.4 × 1.7 × 1.4 (1970s sedan) | parking at (1200, 1100, 0), nose toward −X — or beyond the box per 3.5-A | Fab search "sedan 70s" (Fab Standard free) or Poly Haven search "car" *(verify id)*; wear pass mandatory |
| Hand-painted sign THE 58 CLUB, EST. WITH LOVE over the steel entry door | Dressing | NO | 1.2 × 0.4 | above the ENTRY door on the yard face at (0, 1005, 275) | bespoke plywood board, painted letters (albedo), under M_Enamel-free paint |
| Gravel lot floodlight (T2 operable; draws amperage) | Interactable per inventory — I cap 0 → **OPEN 3.5-D** | OPEN | pole 4 m; head 0.3 | (1300, 1050, 0) by the car | Fab search "floodlight pole industrial"; head under M_Practical |
| Surfaces | — | — | 240 m² ground | — | Ground: Megascans "gravel" over "packed dirt" (starter: none listed — pull "gravel ground" + "dirt path") → `MI_Yard_Ground`, `MI_Yard_Path` following the two reference path legs; sky: moonless (no moon disc); perimeter per 3.5-A |

### 3.5.5 LORE ITEMS
| Item | Tag | Sits | Text key | Source |
|---|---|---|---|---|
| Guy-wire crimp tag stamped 1971, still bright | HC | On the anchor nearest the entry path, (−400, 1750, 70), tag Ø0.03 — bright metal via roughness/metallic only | none | restoration-ambient-lore-ledger.md YARD |
| Child's bicycle bell zip-tied to the fence, clapper removed | T1 (rhymes with his) | Fence, (600, 1795, 110) | none; must be silent (LAW 5) | restoration-ambient-lore-ledger.md YARD; THE-LAWS.md 5 |
| Burn barrel: melted film-can lids fused into one disk, rim stamps just legible: GLADHOUSE | T5, HF | Inside the barrel, disk at Z ≈ 30, legible only from above at 1 m | none | restoration-ambient-lore-ledger.md YARD |
| W2 (the secret pilgrimage's second viewing) | secret | "behind the burn barrel (Day 3)", exists only after W1 is found in the library's skip gap; each viewing spends one S2 slip | OPEN — the W-series text keys are not identified in this brief (grep GameText for W1/W2/W3 at build time) | restoration-walkthrough-levels-endings.md ADDENDUM SPOILER THE SECRET |
| Handled L = 1 | — | Candidate occupant: W2 (a viewing pickup) — OPEN 0-G | — | — |

### 3.5.6 DRESSING PASSES
| # | Pass | Steps | Verification capture | Must read |
|---|---|---|---|---|
| P0 | Data check | Bounds X ±1500 / Y 1000..1800; ENTRY slab (0, 1000); SHED locked slab (850, 1400) with reason text at Z 290; shed box; no lamp | top-down (0, 1400, 1500) → (0, 1400, 0) | Exact; decide 3.5-A (perimeter) before P1 |
| P1 | Surfaces | Gravel over dirt; the two worn path legs (entry → middle; → shed door) as MI_Yard_Path; perimeter per 3.5-A; shed exterior siding; sky (moonless) | (0, 1040, 148) → (850, 1400, 120) (from the entry door toward the shed) | Path reads as habit, not decal; gravel breaks light three ways; no tiling across 30 m |
| P2 | Fixed props | Tower rig + beacon + guy-wires + anchors; pallets; shed door + hasp + EDITH tag; laundry line; burn barrel; fence; car; sign; floodlight (3.5-D) | (0, 1040, 148) → (−900, 1450, 400) | Lattice reads as angle-iron, beacon as a real fixture; guy-wires plausible (tension, sag) |
| P3 | Practicals + EV | Beacon as a true light (red, static/pulse per 3.5-B); no sodium; restore a motivated overcast sky for DAY (3.5-C); lock NIGHT EV; ensure the floor resolves across 30 m at NIGHT (readable-floor law) | NIGHT: (0, 1040, 148) → (−900, 1450, 400); NIGHT: (0, 1040, 148) → (850, 1400, 120) | The tower light is the frame's only red; distance reads as distance (falloff honest); the shed door is findable in the dark without a flashlight |
| P4 | Lore FIRST | Crimp tag 1971; the clapperless bell; the fused GLADHOUSE disk; W2 spawn site behind the barrel | 1 m closeups: (−400, 1650, 148) → tag; (600, 1700, 148) → bell; (−300, 1550, 200) → into the barrel | All promptless; rim stamps legible only at 1 m from above |
| P5 | Dressing mass (≤ 8) | Laundry (count drifts), a hose reel, a coal scuttle, tyre marks of the absent van (decal), a bench by the door, a bird feeder, a stacked-chair pair, a coax spool | (0, 1040, 148) → (850, 1400, 120) | ≤ 8; the yard reads as a lived yard, not a lot |
| P6 | Wear/decals/drift | Rust streaks under the beacon mount, gravel wear at the shed door, weathering on the sign; drift hook: laundry count (dressing, monotonic) | Day 1 vs Day 4 laundry pair | Only the laundry count changed |
| P7 | QA + acceptance | QA-55 (prompts: the shed door only; car/floodlight per 3.5-D/F), QA-56, QA-57 (no hero; I = 0) | §3.5.7 | §3.5.7 |

### 3.5.7 ACCEPTANCE CAPTURE
- Camera A (the only sky): **(0, 1040, 148) → look-at (−900, 1450, 400)**, NIGHT, tower light on.
- Camera B (the walk to the shed, Night 7): **(0, 1040, 148) → look-at (850, 1400, 120)**, NIGHT.
- Camera C (4c, the last light): **(0, 1040, 148) → look-at (−900, 1450, 750)** before and after the beacon goes out.
- Checklist: (1) the tower light is the only red and reads from the yard; (2) the ground resolves across 30 m (dark is a room); (3) guy-wires, laundry, barrel, bell present; the bell silent; (4) the shed's PADLOCKED · EDITH reason readable at the door; (5) no sodium, no moon; (6) no naked primitives on the lattice; (7) store-page test.

### 3.5.8 OPEN
- **3.5-A** Perimeter: the stamper gives the yard four 3 m walls; canon implies a fence and open ground beyond (tower base, guy-wire field, lot). Fence dressing on the stamped walls, or a data change?
- **3.5-B** Beacon steady (room bible) vs pulse (walkthrough, game master, room inventory).
- **3.5-C** The yard by DAY: no canon description of its daytime lighting state.
- **3.5-D** Gravel lot floodlight: exists in the inventory (T2 operable, amperage) but not in the data; breaches I = 0.
- **3.5-E** Tower height: reference rig 7.5 m; scale truth for a UHF mast is far greater.
- **3.5-F** Rita's car (inspect) and the 58 CLUB sign: dressing only under I = 0?
- **W-series text keys** not resolved here.

---

## APPENDIX A · FORMAT TEMPLATE FOR 3.6–3.20 (copy exactly)

```
## 3.N · ROOM NAME — one-line personality quote [room bible]
### 3.N.1 IDENTITY      table: Rooms.csv row → centre/size → uu bounds; every Doors.csv row touching the room
                         (gap centre in uu, width, axis, kind, LOCKED reason + key id); Stations.csv; Monitors.csv;
                         DemoOpen; reference placements from world_builder.gd converted (Godot x,y,z → UE X=x, Y=z, Z=y ×100)
### 3.N.2 ROLE          table: personality · budget I/L/D + drift + web · dread role · beats (game master scene ids,
                         walkthrough parts) · route · sanctuary/laws · inventory listing reconciled against the cap
### 3.N.3 LIGHTING      table per state: DAY ON AIR · BREAK · NIGHT · CASCADE · CROSSING · 4c · room-specific states;
                         columns: Locked EV (OPEN unless canon gives a number) · practicals (id, type, uu position,
                         colour family, intensity) · red reads? · transition (CUT) · source
### 3.N.4 FIXED PROPS   table: prop · tier · interact? (+ exact GameText key) · real dims m · placement uu · asset
                         candidate + licence (Fab search term / Megascans / Poly Haven id (verify) / AmbientCG id
                         (verify) / bespoke) · surfaces row with MI_<Room>_<Surface> names
### 3.N.5 LORE ITEMS    table: every ledger line for the room + every D-series readable homed there; tag; where it
                         sits (uu); text key (none for ambient — QA-55)
### 3.N.6 PASSES        P0 data check → P1 surfaces → P2 fixed props → P3 practicals + EV (delete the stand-in lamp)
                         → P4 LORE FIRST → P5 dressing ≤ D → P6 wear/decals/drift → P7 QA-55/56/57 + acceptance;
                         each with a capture (cam uu → look-at uu) and a must-read line
### 3.N.7 ACCEPTANCE    cameras (uu, look-at, state, day) + 7-point checklist ending in the store-page test
### 3.N.8 OPEN          numbered 3.N-A… ; never invent canon
```
Rules of the template: cite `[doc §section]` on every canon claim; write OPEN
where canon is silent; the code's placements are the spec for positions; the
room bible's cap governs prompts (flag inventory breaches, do not resolve
them); the ledger's items are placed before any dressing mass; asset ids are
search terms unless verified.

## APPENDIX B · CONSOLIDATED OPEN QUESTIONS (owner rulings needed)
| Id | Question | Blocks |
|---|---|---|
| 0-A | Door leaf height: 2.2 m (reference) vs 2.6 m slab (greybox) | all door leaves |
| 0-B | Eye height: UE 148 uu vs Godot 160 uu | capture parity |
| 0-C | FOV: UE default 90° H vs Godot 70° V vs art bible 24 mm | every acceptance capture |
| 0-D | Sodium exterior spill (art bible §8) vs one sodium fixture (lighting bible) | 3.5 P3, any window |
| 0-E | NIGHT practicals OFF (bible) vs brown-out ×0.56 (reference code) | every NIGHT row |
| 0-F | Does the tower's red join the red=watched grammar; does anything change on BREAK in tally-less rooms | 3.4/3.5 NIGHT, all BREAK rows |
| 0-G | What the L cap counts (this brief: handled D-series only) | budgets |
| 3.1-A/B/C, 3.2-A..E, 3.3-A..D, 3.4-A..D, 3.5-A..F | per room, above | per room |
| EV | No EV number exists in canon; the build agent records each chosen EV per room-state in the PR as a PROPOSAL, never as canon, until unit C18 (Lighting.csv) lands | every room |

## APPENDIX C · ONE FAB PULL FOR ALL FIVE ROOMS (batch per ue/FAB-IMPORT.md §THE PULL)
Surfaces (Megascans, FREE, MEDIUM/2K): worn parquet wood floor · linoleum/
checker · office carpet short pile 70s tone · plaster wall painted aged ·
wallpaper vintage (if free) · acoustic ceiling tile · ceramic tile splashback ·
gravel ground · packed dirt · galvanized metal · corrugated metal / painted
wood siding · painted wood trim/skirting.
Decals: coffee stains · scuffs/tyre marks · water damage · tape residue · rust
streaks.
Props (free tier if present): wooden pallet · oil drum rusted · chain link
fence · metal locker · cast iron radiator · cork board · wall clock vintage ·
refrigerator vintage 70s · kitchen cabinet vintage · dish rack · console
television 70s · electrical panel · floodlight pole · sedan 70s.
CC0 (Poly Haven, verify ids): ArmChair_01 · tea_set_01 · wooden_table_02 ·
coffee_table_round_01 · hanging_picture_frame_01 · vintage_wooden_drawer_01 ·
search: lectern, projector, kettle, key, bed, clothes line, car.
Bespoke (Blender factory): coat-peg rail + 5 coats · the projector · S5 lectern
· cue signs · key board + keys + felt/paper tags · the kettle (if no CC0 donor
passes sodium) · the seven dresser items · the tower lattice + beacon · fused
lid disk · clapperless bell · the 58 CLUB sign.
Every pull: credits line in ue/CREDITS-FAB.md, wear pass, MI_<Room>_<Surface>
naming [ue/FAB-IMPORT.md §AFTER EVERY PULL].
