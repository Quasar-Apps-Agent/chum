# RESTORATION · CAST DOSSIER (C2)

Per-character build dossier for PHASE 2 (units 2.1–2.10) and the Chum
variants the studio and dock need, assembled from the canon cast plates, the
walkthrough, the motion-and-sound doctrine and their neighbours. One entry per
character: silhouette · materials · scale truth · motion hooks · rooms · beats ·
LAW constraints · voice · reference implementation · OPEN. Every rule carries a
citation `[KEY §section]` (keys in §0.1). Where canon is silent the cell says
**OPEN** and the question is numbered in §8. Nothing here invents canon; where
two canon documents disagree the disagreement is recorded in §7, not resolved.

This is a paper deliverable from the cloud lane: no Blender, no UE, no capture
was run. It is read by the Mac lane before unit 2.1 and by every 2.x unit as
its brief.

---

## 0 · CONVENTIONS

### 0.1 Source keys

| Key | Path |
|---|---|
| SHEETS | `docs/canon/restoration-cast-sheets.md` (the plates' ruling text) |
| PLATE-RITA / -MERLE / -VESS / -LELAND / -HARRIET / -AF | `docs/canon/art/cast-rita-ivori.png`, `cast-merle-cottry.png`, `cast-vess-keys.png`, `cast-leland-merrick.png`, `cast-harriet.png`, `after-fire-chum-dossier.png` |
| DESIGN | `docs/canon/restoration-design-doc.md` |
| WALK | `docs/canon/restoration-walkthrough-levels-endings.md` |
| MASTER | `docs/canon/restoration-game-master.md` |
| PLOT | `docs/canon/full-plotlines-anatomy-restoration.md` |
| MOTION | `docs/canon/restoration-chum-motion-and-sound.md` |
| AF | `docs/canon/restoration-after-fire-chum.md` |
| CASUALTY | `docs/canon/restoration-casualty-ledger.md` |
| LAWS | `docs/packet/portbrief/THE-LAWS.md` |
| ROOMS | `docs/canon/restoration-room-bible.md` |
| INVENTORY | `docs/canon/restoration-room-inventory.md` |
| AMBIENT | `docs/canon/restoration-ambient-lore-ledger.md` |
| LORE | `docs/canon/restoration-lore-architecture.md` |
| DREAD | `docs/canon/restoration-dread-doctrine.md` |
| REACT | `docs/canon/restoration-reaction-matrix.md` |
| LIGHT | `docs/canon/restoration-lighting-bible.md` |
| ART | `docs/production/restoration-art-bible.md` |
| AUDIO | `docs/production/restoration-audio-bible.md` |
| FABRIC | `docs/production/restoration-puppet-fabrication-brief.md` |
| CASTING | `docs/production/restoration-merle-casting-breakdown.md` |
| PROPS | `docs/production/restoration-props-packet.md` |
| ACH | `docs/production/restoration-achievements-design.md` |
| QA | `docs/production/restoration-qa-regression.md` |
| KEYART | `docs/production/restoration-key-art-brief.md` |
| ACCESS | `docs/production/UE-ACCESS-SPEC-LAW9.md` |
| RIG | `docs/production/CHUM-RIG-AND-ANIMATION-SPEC.md` |
| P1 | `docs/production/PHASE1-CHUM-BUILD-BRIEF.md` |
| BRIEFS | `docs/production/ROOM-BRIEFS-3.1-3.5.md` (format template; §0 conventions) |
| PLAN | `AAA_BUILD_PLAN.md` |
| PROGRESS | `PROGRESS.md` |
| KIT | `scripts/character_kit.gd` (the reference implementation's figure builds) |
| WB | `scripts/world_builder.gd` (reference placements) |
| HARRIET.gd / MERLE.gd / VESS.gd / FM.gd / DOCK.gd / GLIMPSE.gd / STAGE.gd / RUNDOWN.gd / PLAYER.gd | `scripts/harriet.gd`, `merle.gd`, `vess.gd`, `floor_manager.gd`, `dock_chum.gd`, `glimpse.gd`, `tape_stage.gd`, `rundown.gd`, `player.gd` |
| ROOMS.csv / TIMINGS.csv / GAMETEXT.csv | `ue/Restoration/Data/Rooms.csv`, `Timings.csv`, `GameText.csv` |

The reference implementation is cited as "the code is the intent" [PLAN §1 THE
PORT KIT, quoting `docs/packet/portbrief/PORT-BRIEF.md`]. Its figure builds are stylised low-poly
stand-ins [KIT header comment: "built as stylized low-poly humans"]; their
numbers are recorded here as the ONLY numbers that exist, never as canon.

### 0.2 Two rulings that govern every plate

| Rule | Text | Source |
|---|---|---|
| The station | "THE STATION IS WGLD, CHANNEL 58, EVERYWHERE, by the author's explicit word. Where any sheet's incidental set dressing reads otherwise, it is an artifact of the art process and reads as WGLD 58 in canon." Every `WJBU-TV`, `CHANNEL 7`, `TECHNICIAN 7`, `ARCHIVIST 7` on a plate is therefore WGLD 58 | SHEETS header; the plates carry WJBU/7 marks (PLATE-RITA, PLATE-VESS, PLATE-LELAND) |
| The plates are law | "Everything else on these sheets is law." The cast-sheet set "is complete at five: Rita, Merle, Vess, Leland, Harriet, plus the After-Fire dossier" | SHEETS header; SHEETS §HARRIET |
| The Gladhouse ran 1971 to 1977 | dates every era below | SHEETS header |

### 0.3 The render language (read before modelling any human)

| Rule | Source |
|---|---|
| "Humans are needle-felt and cloth figures over armature." "Humans: needle-felt heads over wire armature, cloth bodies, mitten hands with stitched finger definition reserved for principals (Merle, Vess, Harriet). Head-to-body one to five and a half." | ART §1, §6 |
| "EYE HIERARCHY, a hard law: human figures wear glass beads or embroidered eyes only; buttons are reserved for Chum. A button on a human face is an event we never spend." | ART §6 |
| "Crafted, not photoreal … photoreal humans are not the goal, lying materials are the defect." | PLAN §R.7 |
| "Humans are crafted figures in the same language, cloth and needle-felt over armature." | DESIGN Part II · The Two Render Worlds |
| Unit 2.1 "evaluate MetaHuman vs Blender template in-unit" — "the puppet cast may not suit it" | PROGRESS 2.1; PLAN §5 Phase 2 |
| The cast plates are photographic. They are the source of record for likeness, wardrobe, props and turnaround [SHEETS header], while the render doctrine above is the source of record for MATERIAL. The dossier reads each plate as a costume-and-likeness reference for a crafted figure, not as a photoreal target | this dossier's reading; the tension is logged as **OPEN-1** for unit 2.1 |
| Wardrobe drift: environments and wardrobe interpolate from compound neutrals toward the show palette (MUSTARD #C9A33D, AVOCADO #6B7D3B, BURNT #B35A2B) on the coat-peg curve; per-character rules in ART §5 and repeated per entry below | ART §4, §5 |
| The sodium check binds every fibre material: "every fiber material is judged as a physical sample photographed under a sodium lamp beside its render" | ART §10; PLAN §1 THE SODIUM CHECK |

### 0.4 Scale and coordinate law

| Rule | Value | Source |
|---|---|---|
| Unit | 1 m = 100 uu, verified on a 1 m cube | PROGRESS 0.2; PLAN §1 |
| Plan mapping | UE (X, Y, Z) uu = (Godot x, Godot z, Godot y) × 100; the reference placements below are Godot metres | BRIEFS §0.1 (from `ue/pyscripts/build_greybox.py`) |
| Rita's eye | UE ≈ 148 uu above floor; Godot reference 1.6 m | BRIEFS §0.1 (**OPEN 0-B** there, unchanged here) |
| Human heights | **No canon height exists for any human.** ART §6 gives only the head-to-body ratio 1 : 5.5. Reference figure heights are listed per entry from KIT arithmetic | ART §6; KIT |
| After-Fire Chum | 3.35 m standing, tally eye at 3 m, on wake; imported unscaled at 3.08 m; the authoring-scale ruling is RIG OPEN-1 / P1 §1.7 | AF §THE SCALE LAW; PLATE-AF "11 FT (ABOUT 3.35 M)"; TIMINGS.csv `AF_HEIGHT 3.35`, `BASE_HEIGHT 2.6`; PROGRESS 0.3 |
| Stage puppet | seated height 55 cm, hand puppet with rod-arm option | FABRIC §3 |
| Understudy on-set live build | Chum plus four percent overall scale, tolerance ± 0.5 % | ART §6; FABRIC §2 D5 |

### 0.5 Naming (the prefix law is canon; the names below it are proposals)

`SM_`/`SK_` meshes, `M_`/`MI_` materials, `T_*_BC/_N/_ORM` textures, `UCX_`
collision, sockets `SOCKET_*` [PLAN §1 Unreal side]. `SK_Chum_AfterFire` is
already named [RIG §1.2]. No canon names any human asset. **Proposed, not
canon**: `SK_Merle`, `SK_Harriet`, `SK_Vess`, `SK_Leland`, `SK_FloorManager`,
`SK_Rita_Hands`, `SM_Chum_1974`, `SM_Chum_1971`, `SK_Chum_Stage_1974` (if the
stage body ever animates), `SM_Chum_PostFire_Stage`. Adopt or rename in 2.1
(**OPEN-2**). Per LAW 3, no asset, class, log line or achievement may carry the
name of the Day 4 fire-corridor moment [LAWS 3] — see §2.11 and §7.

---

## 1 · ROSTER

| # | Character | Plate | Phase 2 unit | Age (canon) | Pronouns (canon) | Reference height (KIT, not canon) | Primary LAW hooks |
|---|---|---|---|---|---|---|---|
| 2.1 | Rita Ivori (player) | PLATE-RITA | 2.6 (with FM variant) | **OPEN-3** (none stated) | she/her [SHEETS §RITA "she restores"] | first person; eye 1.6 m Godot / 148 uu UE | LAW 7 (every death is her choice), LAW 8 (the one lie is spent on her menu), LAW 9 |
| 2.2 | Merle Cottry | PLATE-MERLE | 2.2 | Late 60s [SHEETS §MERLE] (see §7 C-1) | she/her | ≈ 1.6 m (capsule 1.6) | LAW 7 (M1, M2), never-sinister rule, LAW 4 does NOT name her (see §3) |
| 2.3 | Harriet | PLATE-HARRIET | 2.3 | Late 60s [SHEETS §HARRIET] | she/her | ≈ 1.6 m (capsule 1.6) | LAW 6 (freezes on BREAK), LAW 7 (H1, H2) |
| 2.4 | Vess Keys | PLATE-VESS | 2.4 | Early 20s [SHEETS §VESS] | he/him, "ruled by the sheet" [SHEETS §VESS] | ≈ 1.67 m by mesh arithmetic; KIT comment says 1.78 (capsule 1.7) | LAW 7 (V1, V2) |
| 2.5 | Leland Merrick | PLATE-LELAND | 2.5 | Mid-40s "at the end" [SHEETS §LELAND] | he/him | ≈ 1.66 m (in-tape stand-in 1.7 m box) | LAW 7 (L1, L2), LORE never-stated ledger ("whether Leland chose to stay") |
| 2.6 | The Floor Manager | none (no sheet) | 2.6 variant | **OPEN-4** | canon uses both "they" [DESIGN, WALK] and "he" [CASUALTY, REACT] — **OPEN-5**; this dossier says "the FM" | ≈ 1.69 m (capsule 1.7) | LAW 7 (F1, F2), AUDIO S12 never heard moving, LAW 2 (never pops) |
| 2.7 | Chum · 1974 stage puppet | four reference plates [ART header; DESIGN Part I] — not in this repo (**OPEN-6**) | 2.7 | built 1974 | he [AF, MOTION throughout] | seated 55 cm [FABRIC §3]; reference stand-in ≈ 1.05 m [KIT] | LAW 4 (the warm dock unit), LAW 5 (bell) |
| 2.8 | Chum · 1971 pilot | era table only | 2.8 | built 1971 | he | as 2.7 (**OPEN-7**) | LAW 4, LAW 5 |
| — | Chum · post-fire stage puppet (nine deltas) | tell-table | not a Phase 2 box (**OPEN-8**) | after 1977 | he | hand-sized [P1 §0.5] | LAW 5 |
| — | Chum · 4K premiere | era table | not a Phase 2 box (**OPEN-8**) | — | he | "impossible fidelity" | LAW 5, LAW 8 |
| 1.x | After-Fire Chum (the mascot) | PLATE-AF | Phase 1 (P1, RIG) | rebuilt after 1977 | he | 3.35 m | LAWS 1, 2, 5, 10, 11 |
| — | The Understudy / the glimpse figure | none, by law | not a box | — | "it" [DESIGN §The Understudy] | glimpse stand-in 2.5 m capsule + bar at 2.9 m [GLIMPSE.gd] | LAW 3 (once ever), LAW 2 (no sting) |
| — | Ansel Craik | archival only | not a box | — | he | — | never in the compound |
| — | The 58 Club rows / extras | none | not a box | — | — | — | LAW 7 (THE ROWS) |

---

## 2 · THE ENTRIES

### 2.1 RITA IVORI · TAPE CONSERVATOR (player character)

**Identity.** "Professional. Patient. Precise. What others discard, she
restores. Restoration Division; open-reel video, 2-inch quad, 1-inch Type C,
U-matic, acetate and binder repair. Her tools are the dresser's seven,
confirmed: cotton gloves, the 10x loupe, splicing block, leader tape, the
archival binder, isopropyl and swabs, clipboard and accession forms." Marketing
lines: PRESERVE. REWIND. REMEMBER. / WHAT OTHERS DISCARD, SHE RESTORES [SHEETS
§RITA]. Freelance film and tape conservator hired for the 50th-anniversary boxed
set; "her authentication work is, without her knowledge, production work" [PLOT
§characters]. Arc: detachment → craft pride → understanding → complicity →
authorship, carried by Producer Track tells, "never by voiced introspection"
[WALK Part I]. "Rita speaks only inside the show's formats and her own
paperwork; her interiority lives in ledger text, written in her hand" [MASTER
header].

**Silhouette (what the game shows).** First person: "Rita's design is her
hands, her tools, and her rare reflections. Her hands are the most animated
character in the game: white cotton conservator gloves (the iconic archival
image), sleeve garters, a jeweler's loupe on a lanyard that swings into frame
when she leans in. Wardrobe glimpsed at mirrors and dead CRTs: work apron over
practical clothes, hair pinned with a film-can lid clip" [DESIGN Part I · Rita].
The plate agrees and adds: dark ribbed turtleneck, dark denim bib apron with a
RESTORATION name tag, white sleeve protectors to the elbow, white cotton
gloves, loupe(s) on a lanyard at the sternum, clipboard with accession form in
the left hand, a reel held up in the right, dark work trousers, brown leather
boots, hair up with the round metal film-can-lid clip [PLATE-RITA].

**Materials.** Gloves: "her gloves are the whitest object in the game" [ART §5];
"her white gloves are the brightest object in frame, per the bible" [KEYART
§comp]. Apron cotton/denim, turtleneck knit, sleeve protectors white cotton,
loupe brass and glass, clipboard wood and steel clip [PLATE-RITA]. Rita "wears"
the crafted doctrine like everyone: "She is a needle-felt figure" in the key art
[KEYART §comp] — for the first-person hands this means felted/cloth glove
material under the sodium check, not skin (**OPEN-1** applies).

**Scale truth.** Eye height UE ≈ 148 uu, Godot 1.6 m [BRIEFS §0.1, OPEN 0-B
there]. Walk 3.10 m/s, crouch ×0.55 = 1.71 m/s (crouch is "a body verb, useless
against him" per the gap-audit ruling c045), camera drop 0.60 m eased at 12/Δ,
interact reach 2.6 m [TIMINGS.csv `player.gd`; PLAYER.gd 8–10, 58; PROGRESS
0.8b-1]. No body height, no hand size in canon (**OPEN-3**).

**Motion hooks.** "Rita adjusts her gloves at decisions; the loupe swings into
frame when she commits" [MASTER header]. "the gloves, squared" is the finale's
beat [MASTER T5.4]. Avert: "hold to raise Rita's clipboard, blocking direct
sight while preserving movement at a slow walk"; "clipboard raise runs about
200ms with an ease-out" [DESIGN Part IV.2; Part V Feel Notes]. Reflection
budget: "From Tape 3 onward, her reflections begin composing better: centered,
headroom correct, rule-of-thirds. Nobody comments" [DESIGN Part I · Rita].
"RITA: player wardrobe never drifts" [ART §5]. The seven dresser items vanish
one per capture, loupe last [INVENTORY §5; WALK Part V-B].

**Rooms.** Everywhere; home is the BENCH ROOM "Rita's altar; the game's heart at
9,-16" [ROOMS §BENCH ROOM]; her room is in DORMS, "Rita's unadorned room"
[ROOMS §DORMS]; PlayerStart is REC ROOM (0, 0, 160) uu [BRIEFS §0.1].

**Beats.** T1 arrival, tour, proving, capture one, mini-screening [MASTER
T1.1–T1.7]; T2 patchbay, airdate math, first blood, the screening [T2.2–T2.8];
T3 the fire tape, the pre-signed page in her hand [T3.4, T3.6]; T4 the crate,
the seance, the glimpse [T4.1, T4.4, T4.8]; T5 the decision point ("The pen is
the loudest thing in the building"), the premiere on Craik's mark, the line
into the lens [T5.2–T5.4]. Ending 1B: "Rita in frame, in palette, at rest";
ending 4b: "her arm never fully works again, stated flatly" [MASTER §ENDING 1B;
CASUALTY §FLOOR MANAGER · ENDINGS]. Ending 0: "every role's title card reads
RITA IVORI" [CASUALTY §THE FULL BOARD].

**LAW constraints.** LAW 7: "every death, including run death, traces to a
nameable choice of Rita's, and the binder names it" [LAWS 7]. LAW 8: the one
interface lie is spent on her menu after ending 2 [MASTER §ENDING 2; LAWS 8].
LAW 9: booth, captions, assist, remap, pause ship in every build [LAWS 9;
ACCESS]. Her spoken inventory is the response pools only [MASTER App. C].

**Voice.** "Rita: minimal lines, breath-first acting; recorded dry on the WORLD
bus" [AUDIO §5]. Response pools verbatim [MASTER App. C].

**Reference implementation.** No figure; a capsule + camera [PLAYER.gd]. UE:
`ARitaCharacter`, feel parity proven to the digit [PROGRESS 0.8b-1].

**OPEN.** OPEN-1 (render language for the hands), OPEN-3 (age, height, hand
scale), OPEN 0-B/0-C inherited from BRIEFS.

---

### 2.2 MERLE COTTRY · PRESIDENT. COOK. CARETAKER.

**Identity.** "Late 60s, the 58 Club matriarch, occupation: everything. Voice
warm, folksy, unhurried; hands never still: towel, spoon, mug, or someone
else's sleeve. 'This place runs on love and leftovers.' NEW CANON: MERLE
FOUNDED THE CLUB WITH LELAND. She remembers the early broadcasts not as research
but as home, and she will protect the Club with open arms and bury the truth if
she must. Guardrail, restated: burying the truth is grief's custodianship,
never menace; the never-sinister rule survives untouched" [SHEETS §MERLE]. She
was seven in 1974, "carried home by something singing" [CASTING §THE ROLE; MASTER
T4.6; PROPS D04]. "THE ONE LAW … Warm-genuine, never warm-sinister. There is no
twist in this performance" [CASTING §THE ONE LAW]. "The comfort is never the
trap. No scare is ever delivered through Merle's warmth, the kitchen, or an act
of kindness" [WALK Part IV · The Rules].

**Silhouette.** Plate: a stout woman in a maroon cable-knit cardigan over a
floral blouse, a floral bib apron with a stitched **58** on the bib, a striped
cotton tea towel wrung between both hands, a small pendant on a fine chain,
gray-brown hair escaping a loose high bun; turnaround gives left profile, back,
right profile [PLATE-MERLE]. DESIGN adds "cardigans, reading glasses on a
beaded chain, enamel Chum pin polished daily" [DESIGN Part I · Merle] — neither
the glasses-chain nor a separate enamel pin is visible on the plate (**OPEN-9**;
the reference builds both, KIT 659–674). Head-to-body 1 : 5.5, mitten hands with
stitched finger definition (principal) [ART §6].

**Materials.** Cardigan: wool, cable knit, maroon (reference tint (0.31, 0.11,
0.11) [KIT 636]); blouse and apron: printed cotton florals [PLATE-MERLE; KIT
"apron_floral"]; towel: cotton, red stripe [PLATE-MERLE]; hair grey-brown [KIT
677]. Wardrobe drift rule: "MERLE: begins already warm (mustard apron from Day 1)
and never drifts, because she was carried in 1974 and has nothing left to drift
toward; her constancy is the tell hiding in plain sight" [ART §5]. The plate's
apron is cream floral, not mustard (§7 C-2). Her quilt in her dorm room "drifts
to show palette by T4" [INVENTORY §5].

**Scale truth.** No canon height. Reference ≈ 1.6 m (head centre 1.46 m + skull
and bun; collision capsule 1.6 m) [KIT 632–680; WB 1063–1067]. Walk speed 1.6
m/s [TIMINGS.csv `merle.gd SPEED`].

**Motion hooks.**
- "Merle's hands stay busy with domestic objects; when they still, listen"
  [MASTER header]. The towel stops at: "It's what our last archivist did" [T1.3],
  "Don't make me regret the word" [T2.1], "138 … That's all there ever were"
  [T2.3 ASK], "He asks so many questions" [T2.5].
- Self-narration in presenter cadence: "Now Merle is just going to put the
  kettle on" [DESIGN Part I · Merle; MASTER T1.6; ENDING 2].
- THE PEN-UP SILENCE: "forty-five seconds of watching someone sign a document,
  hands empty and open, saying nothing … the in-game figure holds this pose at
  the game's decision point, and the reference footage drives it" [CASTING §THE
  CALLBACK; MASTER T5.2]. Reference: she walks to DOORWAY (6.0, 0, −16.4) while
  the ledger's pen is up [MERLE.gd 9, 20–21].
- The 1974 monologue: "her hands, for once, empty and open" [MASTER T4.6]; seven
  toasts at 3.0–3.4 s intervals [MERLE.gd 67–82] (**OPEN-18** for its UE pacing).
- M1: "the last thing she does is pat Rita's hand" [CASUALTY §MERLE M1]. M2: "Taken
  on the beat, mouth still shaped around the true word" [CASUALTY §MERLE M2].
- Hand inserts pouring tea are a marketing asset [CASTING §LOGISTICS].
- Schedule, exact: KETTLE (8.0, 0, −1.0) by day; CHAIR (2.6, 0, 1.2) at night or
  after lockdown; (0.4, 0, 1.4) during a screening; DOORWAY when the pen is up
  [MERLE.gd 6–24]; "Merle is at kettle, chair, or DOORWAY per schedule and pen
  state, never elsewhere" [QA-11].

**Rooms.** KITCHEN ("Merle's sovereign nation … the kettle's glow (a real light)";
"the kettle click-off is a death beat") [ROOMS §KITCHEN]; REC ROOM (her chair,
the shrine wall, the screenings) [MERLE.gd; MASTER T1.6, T2.8, T4.6]; the BENCH
ROOM doorway at the decision point [MASTER T5.2]; Merle's dorm room, "open door
policy" [INVENTORY §5]. Kitchen key board holds TRAINING and EDITH [INVENTORY
§4]. Reference placements mapped in §5.

**Beats.** T1.1 the door, T1.2 the tour, T1.3 the junk reel, T1.6 "I remember
this one", T2.1 keys on a crocheted fob, T2.3 the club's canon (G3), T2.5 the
plate dried past dry, T3.1 the errand pretext, T4.5 "Sit down, sweetheart. There's
cobbler", T4.6 1974, T4.10 lockdown "in the show's palette head to toe", T5.2 the
doorway [MASTER]. Endings: 1A "freed and bereft … the game holds on her hands,
which have nothing to do"; 1B "keeps a chair facing the dead set"; 2 "Now Merle
is just going to watch it again"; 3 "no anger anywhere on her … There's cobbler"
[MASTER §ENDINGS]. Casting-drift arc by tape: grandmother → presenter cadence →
1974 as recruitment → the scene that earns her → high priestess [WALK Part I].

**LAW constraints.** LAW 7: M1 THE SECOND VIEWING (Day 3+, the fire tape;
consent kills her; refusing saves her) and M2 THE HOME SINGER (premiere; the
call sheet) [CASUALTY §MERLE]. Ripples: kettle never moves again, coat pegs
freeze at her peg's day, night trips escalate one stage early (M1) or premiere
forgiveness timers −20 % (M2) [CASUALTY §MERLE RIPPLES]. LAW 4 is about the warm
dock unit, not Merle (§3). The never-stated ledger protects "What Merle knows
and buried" and "the mechanism of carrying" — no line, caption or prop may state
either [LORE §THE NEVER-STATED LEDGER]. "M-R4: she never says his name after
the fire tape exists; her lines route around it like water" [REACT §MERLE].
DREAD amplifier: "WARMTH: Merle makes Chum scarier … the kettle's warmth is
load-bearing dread infrastructure" [DREAD §AMPLIFIERS].

**Voice.** "Warm alto. Age carried in the breath, not the pitch. Zero irony
available anywhere in the instrument" [CASTING §VOICE SPEC; AUDIO §5]. Sides and
the redirect protocol verbatim in CASTING §§AUDITION SIDES, THE REDIRECT
PROTOCOL. "the monologue is one unbroken take if it kills us" [AUDIO §5].

**Reference implementation.** `Merle` (Interactable) with schedule and
monologue [MERLE.gd]; figure `CharacterKit.merle()` [KIT 632–680]; spawned at
(8.0, 0, −1.0) with a 0.3 × 1.6 capsule [WB 1060–1078]. Toast set per day and
per decision [MERLE.gd 44–64].

**OPEN.** OPEN-9 (glasses chain and enamel pin: plate-absent, DESIGN-present);
§7 C-1 (age), C-2 (drift: DESIGN/WALK "showcase" vs ART "never drifts").

---

### 2.3 HARRIET · SENIOR CLUB MEMBER · THE CONTINUITY KEEPER

**Identity.** "Late 60s, mononymous by the club's own records, and the sheet
grants her the title … THE CONTINUITY KEEPER. Voice precise, measured,
transitional; her signature line, now canon and now in the build: 'And now. The
tour continues.' The sheet's biography paragraph arrived illegible and is ruled
an artifact, which is itself in character: her handwritten pages photograph as
script that will not resolve, because her hand is transitional too. Confirmed
props: THE teacup (floral china, the one that rises), a 58 Club flask whose
contents go unrecorded, her pin card, and a reel in her keeping annotated for
frame loss, which the club does not discuss" [SHEETS §HARRIET]. "Elderly,
immaculate, speaks increasingly in transitional phrases ('And now.' 'But first.'
'When we come back.')" [DESIGN Part I · Harriet]. Her room's door "never opens";
"Everything inside mid-motion" [INVENTORY §5].

**Silhouette.** Plate: seated upright in a carved wooden armchair; chocolate
cable-knit cardigan buttoned once, cream high-collared blouse with a small oval
brooch, brown tweed skirt; silver hair curled and pinned high; pearl drop
earrings; floral china teacup raised in the right hand, saucer in the left;
turnaround left profile, back, right profile [PLATE-HARRIET]. Props panel:
58 Club pin card, the flask, the teacup and saucer, the illegible pages, the
annotated reel [PLATE-HARRIET; SHEETS §HARRIET]. Principal: stitched finger
definition [ART §6].

**Materials.** Cardigan wool cable, brown (reference (0.27, 0.2, 0.14)) [KIT
691]; blouse cream cotton (0.95, 0.9, 0.78); skirt tweed (0.29, 0.24, 0.18)
[KIT 692–695]; brooch brass; pearls [KIT 703, 712]; teacup floral china, saucer
[PLATE-HARRIET; HARRIET.gd 49–58]. Drift: "HARRIET: drifts on the curve exactly,
the control subject" [ART §5].

**Scale truth.** No canon height. Reference ≈ 1.6 m; capsule 0.3 × 1.6 [KIT
687–714; HARRIET.gd 42–47]. Cup position in the raised hand: (0.18, 0.99 + 0.05 ×
min(day, 6), 0.17) m — rises 5 cm per day, capped at day 6 [HARRIET.gd 70].
Reference tilt while swaying: rotation.z = sin(t × 0.9) × 0.04 rad [HARRIET.gd
73–74].

**Motion hooks.**
- THE HOLDING PATTERN: "during the compound's commercial-break windows she stops
  mid-motion, teacup half-raised, and resumes on the return cue. This is a
  background-behavior system, never a cutscene" [DESIGN Part I · Harriet]. "Her
  mid-motion freezes during break windows lengthen each act" [WALK Part I].
  Reference: sways ON AIR, freezes on BREAK holding exactly where the cue left
  her (test: swayA 0.835 → swayB 1.791 swaying, frozenC 1.791 held) [HARRIET.gd
  68–74; PROGRESS 0.8b-5 AHarriet].
- H-R2: "HER FREEZES LENGTHEN when After-Fire is active in the building, one
  extra second, unexplained" [REACT §HARRIET] — QUEUE, not built (**OPEN-10** for
  the port).
- H-R1: "her next transition adds one corrective beat of pause, precisely her
  length of disapproval" [REACT §HARRIET] — QUEUE.
- The cup "raised since Tape 1, comes down" at CUE 4 [MASTER T5.3]; in SIGN-OFF
  "she resumes, finishes raising the teacup, and drinks. The game never explains
  how long she was holding" [WALK Part I; MASTER §ENDING 1A].
- The seventh signal recital: "she performs them, precise as liturgy, and then a
  seventh: both hands pressed flat, pushed down twice. Hold your applause" [MASTER
  T2.4 ASK; PROPS D06].
- H1: absent, "chair warm, and the film cabinet now contains her, folded, with
  leader tape where her voice was" [CASUALTY §HARRIET H1]. H2: "seated one frame to
  the left of herself, doubled at the shoulders, both mouths open on different
  vowels, the teacup rising in two hands at two heights. She remains like this, on
  set, for the rest of the game, and the game treats her as scenery" [CASUALTY
  §HARRIET H2]. Reference double: a duplicate rig at +0.13 m x, +0.03 m z, yawed
  0.06 rad [HARRIET.gd 27–33].
- Screening: "Harriet's cup does not" resume on QUIET [MASTER T2.8]; "stances are
  judged 0.05 tighter without her metronome presence" [CASUALTY §HARRIET RIPPLES].

**Rooms.** GREEN ROOM is "Harriet's parlor … HER CHAIR, the teacup's saucer
ring" and "her doubling is staged here or Studio A per scene" [ROOMS §GREEN
ROOM]; INVENTORY lists "Harriet's chair + teacup" in the rec room [INVENTORY
§3] and "Harriet's deepest holding-pattern freeze" at the green room couch
[INVENTORY §17]; the reference spawns her once, in the REC ROOM at (1.2, 0, 2.6)
[WB 1082–1084]. Which chair is home per tape is **OPEN-11**. Audience seat 14
"wears a brass RESERVED plate with the name line blank [HH, and frame fourteen
knows why]" [AMBIENT §STUDIO A].

**Beats.** T1.2 "And now. The tour continues." (said "like a station break.
Nobody reacts") [MASTER T1.2]; Night 2 her first freeze [WALK Part VI]; T2.4 the
signals plus the seventh; T2.6 hums the verse with one wrong word (HERE for
HOME) [MASTER T2.6]; T4.2 at the rail; T5.3 CUE 2 variant beat, CUE 4 the cup
comes down. Endings: all replace her epilogue line with TRANSITION UNRESOLVED
when she is dead [CASUALTY §HARRIET ENDINGS]; ending A: "Harriet's line as the
radio's last words" [WALK §ADDENDUM · THE SECRET]. Seance frame 14 reads PAUSED
PROPERLY when she is dead [QA-50].

**LAW constraints.** LAW 6: "Harriet freezes on breaks" is a law, not a flourish
[LAWS 6]. LAW 7: H1 CONTINUITY (any break, Day 2+, the slip) and H2 THE SPLICE
(the rejected edit on a reel carrying her segment) [CASUALTY §HARRIET].
Ripple: the seventh signal is unlearnable if she dies before her index card is
found [CASUALTY §HARRIET RIPPLES]. DREAD L1: "Harriet's cup is higher than
yesterday" is ambient wrongness and must never be called out by text [DREAD
§L1]. Captions in the parity set: `[ONE FRAME LEFT OF HERSELF]`, `[A REEL,
LABELED IN HER HAND: ME]` [ACCESS §3.2; HARRIET.gd 105, 115]. A06 MID-MOTION is
the only achievement that touches her [ACH A06].

**Voice.** "Harriet: transitions only, always mid-cadence, as if resuming"
[AUDIO §5]. S13: "A gentle fabric-and-breath sway loop that hard-stops on break
windows and resumes phase-accurate on the return cue; the teacup gains a single
porcelain tick per day at first touch" [AUDIO §3 S13]. Line set: "And now. The
tour continues." / "'And now.'" / "'But first.'" / "'When we come back.'"
[HARRIET.gd 7–8].

**Reference implementation.** `Harriet` (Interactable) [HARRIET.gd]; figure
`CharacterKit.harriet()` — "Right hand holds the cup; the left, the saucer.
Mid-motion, always" [KIT 683–714]; the cup mesh is script-owned and rises
[HARRIET.gd 49–58, 70]. NOTE: HARRIET.gd line 3 comments "Harriet Lund" — the
sheet rules her mononymous (§7 C-3). UE: `AHarriet` built in 0.8b-5 [PROGRESS].

**OPEN.** OPEN-10 (H-R2 lengthened freezes, unbuilt), OPEN-11 (home chair per
tape), §7 C-3 (surname in a code comment).

---

### 2.4 VESS KEYS · TAPE HUNTER

**Identity.** "Early 20s. Tape Hunter, Source Researcher, Provenance
Specialist. Alignment: Lawful Curious. Voice eager, quick, searching; tell:
touches the label maker or the 58 Club pin when nervous, and the pin on the
sheet IS the plastic pin the deaths fuse into the enamel … 'Some tapes shouldn't
exist. But they do. And I find them.' Corrections executed: surname KEYS (the
margin reads PER V. KEYS), pronouns he/him across the engine and the ledger"
[SHEETS §VESS]. "The status detail that carries his whole arc: his club pin is
plastic where everyone else's is enamel … he is what the fandom looks like when
the fandom is not chosen" [DESIGN Part I · Vess]. "Vess touches the label maker
at his belt when nervous and the plastic pin when hurt" [MASTER header].

**Silhouette.** Plate: slight, pale, freckled, dark unruly curls; washed-black
work jacket open over a paisley shirt, a cord necklace, a round **58 CLUB**
patch on the jacket's left breast, three pens and a DYMO label maker in the
chest pocket; props: the 58 Club pin, the DYMO label maker labelled PROPERTY OF
V. KEYS, a spiral FIELD NOTES pad, the PROVENANCE BINDER (V. KEYS, tabbed);
turnaround left profile, front, back [PLATE-VESS]. DESIGN: "thrift-store
seventies shirts worn as devotion cosplay, label maker on his belt, chewed
pens" [DESIGN Part I · Vess]. T4.1: "three days of beard" [MASTER T4.1].
Principal: stitched finger definition [ART §6].

**Materials.** Jacket washed black cotton (0.13, 0.12, 0.12) [KIT 731]; shirt
patterned (KIT "floral" (0.5, 0.33, 0.23)) [KIT 726]; trousers dark [KIT 725].
THE PIN: plastic, never enamel [DESIGN; SHEETS §VESS] — the plate's pin reads
metal-rimmed and is overruled by its own ruling text (§7 C-4). Drift: "VESS:
resists longest; neutrals through Day 4, and his only show-palette object is the
plastic pin he has always carried, which is the other tell; if he credits and is
credited, he adds one avocado scarf for the premiere, chosen, not drifted"
[ART §5].

**Scale truth.** No canon height. Reference: base figure with `rig.scale =
(0.95, 1.07, 0.95)` "taller, narrower" [KIT 729]; the KIT header says "Vess
1.78" while the mesh arithmetic gives ≈ 1.67 m (head centre 1.44 m + curls
0.125 m, × 1.07); capsule 0.3 × 1.7 [KIT 94, 720–758; VESS.gd 18–23]
(**OPEN-12**).

**Motion hooks.**
- Label maker: "the label maker clicks in his pocket, twice, like a habit
  praying" [MASTER T2.8]; "thumb on the label maker" [T1.7]; "pin in his fist"
  [T2.8, T4.5]; "pin catching the light" [T1.3]; "the pin, touched twice" [T4.1];
  "the pin, turned once" [T4.7 ASK].
- V-R2: "post-wake he goes quiet in rooms with monitors, and his tell (touching
  the pin) doubles in frequency" [REACT §VESS] — QUEUE.
- V-R1: "he narrates provenance uninvited" when his binder is snooped; V-R3:
  files Merle's recipes as accessions if she dies [REACT §VESS] — QUEUE.
- T2.8 the Screening: "answers too eagerly, and the room goes wrong around him
  for one held second" [WALK Part VI T2].
- T4.5: "standing in it, pin in his fist, voice level by force" [MASTER T4.5].
- THE FINAL BREAKER: credited, "his hand stops above the handle … the hand comes
  down off the breaker, empty"; uncredited, "The handle. The dark." [MASTER T5.3].
- V1: "taken live, cut mid-sentence on his own slate insight, his plastic pin
  fused into the panel enamel" [CASUALTY §VESS V1]. V2: "Found interlaced with the
  transmitter hum, his outline refreshing at 60 fields a second" [CASUALTY §VESS
  V2]; caption `[MAINS HUM, SHAPED LIKE A STANDING PERSON]` [ACCESS §3.2].

**Rooms.** PATCH BAY is "Vess country … cable looms with his tags, D07 binder,
the credit margin … V2's offer lives here; his absence makes this room loudest"
[ROOMS §PATCH BAY]; TAPE LIBRARY "Vess's country borders here; the crate lives
deep" [ROOMS §TAPE LIBRARY]; DORMS: "Vess's room · door ajar" with the research
binder [INVENTORY §5]; ENTRY: "Vess's delivery spot" [INVENTORY §2]. Reference:
spawned at the REC ROOM shrine wall (−3.7, 0, −1.2), facing −X [WB 1086–1089];
his binder in DORMS (−6.5, 0.6, 1.8); his cut (REJECTED EDIT) in REC (−2.6,
0.9, 1.0) [WB 1052–1055, 1126–1130].

**Beats.** T1.2 "You're the conservator. Vess."; T1.3 "It's what Leland did";
T1.7 "The sign. Over the door. You saw it light."; T2.3 FORCE the binder ("one
insight … one wrong theory"); T2.8 "It never says my name. Three years."; T4.1
the crate ("Tapes dated after the fire. After."); T4.5 the rejected edit ("Your
cuts, it keeps"); T4.7 ASK trade for a named credit; T5.3 the final breaker
[MASTER]. Arc by tape [WALK Part I · Vess]. Endings: 2 "the producer's office
contains his chair, still warm, facing the monitor wall"; DEAD AIR "loses its
grace window" without him (crossing 62 s vs 75) [CASUALTY §VESS ENDINGS; WALK
§ADDENDUM c043].

**LAW constraints.** LAW 7: V1 CREDITED, THEREFORE CAST (precondition the margin
credit; trigger AUTHENTICATE or the final breaker) and V2 THE UNCREDITED FIX
(cascade night, GET VESS, circuit F) [CASUALTY §VESS; §AS BUILT]. "V1 teaches
record-equals-cast better than any note could" [LORE §DELIVERY BANS]. He is the
character allowed to be wrong: "Vess speculates and is sometimes wrong" [LORE
§DELIVERY BANS]. Never a device: his T4 anchor scene is mandatory [DESIGN
§CLOSING gap 3; WALK Part I].

**Voice.** "Vess: fast, precise, a man narrating to keep his hands steady"
[AUDIO §5]. Line set [VESS.gd 6–11].

**Reference implementation.** `VessProp` (Interactable) [VESS.gd]; figure
`CharacterKit.vess()` [KIT 717–758]; `VessBinder`, `RejectedEdit`, `CreditEntry`
props [WB 1052–1059, 1126–1130]; state `vess_insight`, `vess_credited`
[`scripts/game_state.gd` 58–59]; GAMETEXT carries `PER V. KEYS` and `'per V.
Keys'` [GAMETEXT.csv 11, 65].

**OPEN.** OPEN-12 (height), §7 C-4 (pin material on the plate), §7 C-5 (ACH A11
still reads PER V. CARDONA).

---

### 2.5 LELAND MERRICK · PREVIOUS ARCHIVIST

**Identity.** "Filed. Not shelved. Mid-40s at the end; archivist and
conservator, tenure 1972 to 1976, vanished the year before the fire. Voice dry,
kind, careful; tell: green fine-liner in the margins. Always slightly cropped by
the frame edge, as if the image cannot hold him correctly, which the engine's
seance frames already honor. He left green-ink warnings in the accession logs
that were later discovered inside the tapes themselves, and before he vanished
he left one addressed to a conservator not yet hired, by name: 'Rita. You are
safe as audience. Do not be interesting. Never accept a role.'" [SHEETS
§LELAND]. Co-founded the club with Merle [SHEETS §MERLE]. "Exists only inside
the tapes … He holds a legal pad on which answers appear across frames. In the
physical world he survives as green fine-liner annotations" [DESIGN Part I ·
Leland]. Tenure vs the club's "previous archivist … two years ago" is a canon
conflict (§7 C-6).

**Silhouette.** Plate: a tired, kind man in round wire glasses, stubble, dark
hair going grey and a little long; brown cardigan over a striped shirt with a
dark loosened tie; a yellow legal pad clutched to the chest with green ink;
cropped by the left frame edge; props: ID badge (L. MERRICK · ARCHIVIST ·
1972–1976), the legal pad ("AUDIENCE ONLY", "Never accept a role", "Rita — You
are safe as audience"), archival shelves (ACCESSION LOGS 1972–1976 /
UNCATALOGUED TRANSFERS / MASTER TAPES), a reel labelled for partial frame loss
with GREEN NOTES PRESENT; turnaround left profile, front, back [PLATE-LELAND].
"mid-forties, archivist's cardigan" [DESIGN Part I · Leland].

**Materials.** Cardigan brown wool (0.27, 0.2, 0.13); shirt (0.66, 0.61, 0.51);
tie dark; trousers (0.2, 0.17, 0.14); legal pad (0.78, 0.7, 0.5) with green ink
(0.2, 0.45, 0.25); wire glasses [KIT 765–805]. Green fine-liner is a type voice:
"Annotation layer: Leland's green fine-liner, hand-rendered" [DESIGN Part III ·
Type System]. Ledger green #596B52 [ART §4].

**Scale truth.** He is never in the compound, so scale truth is FRAME truth: in
the tape stage he is a 0.35 × 1.7 × 0.25 m dark box at (1.35, 0.85, −0.5) in a
320 × 240 viewport, camera at (0, 0.8, 2.6) — placed camera-right so the frame
edge crops him [STAGE.gd 26–31, 55–57]. Reference compound figure exists
(`CharacterKit.leland()`, `rig.scale (0.97, 1.06, 0.97)`, ≈ 1.66 m) for
`cast_preview.gd` only [KIT 765–805]. Tape world reproduction: "authentic
period video … correct 4:3 pillarboxing, generation loss modeled per dub"
[DESIGN Part II].

**Motion hooks.**
- "always partially cropped by the frame edge as though the composition refuses
  him" [DESIGN Part I · Leland]. Ending 1A: "inside the frame he was cropped from
  for two years, Leland steps to center and is allowed to be whole" [MASTER
  §ENDING 1A].
- "on the bench, single-frame stepping with the jog wheel reveals him moving only
  in the unobserved intervals, and questions written on the bench notepad are
  answered on his legal pad across a span of frames" [DESIGN Part IV.7].
- T4.4: "a man at the edge of frame … legal pad against his chest. Holding
  still. Playing the game" [MASTER T4.4]. The five answers, verbatim, MASTER
  T4.4 (Q1 FILED. NOT SHELVED. … Q5 I'VE READ THE ENDING. IT'S GOOD.). "a breath
  he does not need and takes anyway" [MASTER §ENDING 1A].
- L1: "His remaining print burns from the inside of the frames; the green ink
  drains upward out of every note in the building" [CASUALTY §LELAND L1]. L2: "his
  five answers un-write in reverse; the final frame shows the little door closing
  from the inside, his hand on the inner knob" [CASUALTY §LELAND L2].
- Grief answers at frames 14 and 28 [REACT §LELAND; QA-50]; L-R1 the unsigned
  margin NOT THAT ONE. PLEASE. (QUEUE) [REACT §LELAND].

**Rooms.** Bench (the seance, on the monitor) [MASTER T4.4]; SCENE DOCK "the
SEANCE DOCK, D10 IRIS, D01's shelf" and "the reading, the sixth line" [ROOMS
§SCENE DOCK]; TAPE LIBRARY "Leland's desk … green pens, tidy abandonment" and
his card-catalog cross-references [INVENTORY §7]; his margins in the binder at
S1 [MASTER T1.4]; ambient traces: ENTRY sign-in IN with OUT blank forever; DORMS
door four's blank card; BENCH lip scratched L.M.; the 1975 chair that faced the
door [AMBIENT §§ENTRY, DORMS, BENCH ROOM, CONTROL]. Reference: LEDGER MARGIN
(credit entry) at (7.4, 0.9, −15.2) in the BENCH ROOM [WB 1056–1059].

**Beats.** T1.4 the first green note; T1.7 "He also left without saying goodbye";
T3 tallies "Leland's marginal notes end mid-sentence: 'If you find me, don't'";
T4.4 recognition and the five answers; ending 1A "Goodnight, everyone. It's okay.
Nobody's watching."; 1B the ledger line in green: SHE CLOSED IT PROPERLY. FILE
UNDER: SAINTS [MASTER]. Margin set verbatim [MASTER App. D]; D01 four pages
[PROPS D01]. 4c THE COMPLETED SIGN-OFF "in his voice" [CASUALTY §LELAND ENDINGS]
— see §7 C-7 against AUDIO "never voiced".

**LAW constraints.** LAW 7: L1 THE SIXTH QUESTION (past wear 70 with five
answers; closes 1A) and L2 THE READING (the fire tape into the wake; consumes the
tape; creates 4c) [CASUALTY §LELAND; §AS BUILT]. Never-stated: "Whether Leland
chose to stay" [LORE §THE NEVER-STATED LEDGER]. Marketing: "Leland's face [is]
never depicted in any marketing material, ever" [KEYART §rules]. Three
generations of the same man [DESIGN Part IV-B.11].

**Voice.** "Leland: never voiced. The legal pad is text by canon; his silence is
load-bearing" [AUDIO §5]. Endings 1A and 4c give him speech in prose (§7 C-7).

**Reference implementation.** In-tape box and pad label [STAGE.gd]; seance in
`scripts/seance_dock.gd` (MAX_FRAME 40 [TIMINGS.csv]); `leland_answers` array
[`game_state.gd` 46]; A14 at five answers [ACH].

**OPEN.** §7 C-6 (tenure), C-7 (voiced endings vs never voiced).

---

### 2.6 THE FLOOR MANAGER (unit 2.6 variant)

**Identity.** "Never named, face never fully lit, headphones with a coiled cable
connected to nothing, laminated run sheet. Communicates only in countdowns and
real television floor-manager hand signals: stretch, wrap it up, cut, thirty
seconds, you're on … The scariest character in the game never touches anyone;
they just count things in and out of existence" [DESIGN Part I · The Floor
Manager]. "No arc, which is the point. They count things in and out for five
acts. After the sign-off completes, they remove the headphones, and the game
ends before showing anything further" [WALK Part I]. No cast sheet exists
[SHEETS §HARRIET: "complete at five"].

**Silhouette.** "absolute black-adjacent neutrals forever, outside the palette
system entirely, the way he is outside everything" [ART §5]. Reference build:
blacks (0.08, 0.075, 0.07), a dark work jacket, a dark cap whose brim keeps the
face in its own shadow, headset band, earcups, boom and a six-loop coiled cable
"descending to nowhere", the laminated run sheet held in the left hand "angled
away, always", the right arm a pivot that hangs or points [KIT 808–873]. D08 THE
FLOOR MANAGER'S RUN SHEET · "glimpsed angle only" [PROPS D08]. A worn mark on the
Studio A floor paint "decades deep" [INVENTORY §12].

**Materials.** Blacks (cotton work jacket, trousers), the headset's plastics, the
run sheet's laminate [KIT 816–873]. Outside the drift system [ART §5].

**Scale truth.** No canon height. Reference: base figure × (1.0, 1.08, 1.0) ≈
1.69 m; capsule 0.3 × 1.7 [KIT 823; FM.gd 28–33]. Arm pivot at shoulder (0.2,
1.17, 0); raised = rotation.x −π/2 (horizontal point) [KIT 835–840; FM.gd 60–62].

**Motion hooks (the signal vocabulary is the threat-telegraph UI).**
- The six signals: YOU'RE ON (the point), CUT (the slash), STRETCH (taffy
  hands), WRAP IT UP (the circle), THIRTY SECONDS (the T), ON TIME (the nose
  touch); the seventh, HOLD YOUR APPLAUSE (both hands pressed flat, pushed down
  twice), known only through Harriet [MASTER T2.4; App. C Signal glossary].
- "The Floor Manager is hands and countdowns, nothing else" [MASTER header].
- YOU'RE ON in the reference: within 9 m, facing (dot > 0.5), on a night ON AIR,
  the arm rises and a 3.0 s watch begins; moving > 0.4 m/s spoils the take unless
  assist-hold [FM.gd 48–84; QA-19]. The whole body turns to face the player,
  lerp 4/s [FM.gd 55–58].
- F-R1: "HE POINTS AT THE DOORWAY seconds before the first fold a player ever
  sees, a cue given to no listed camera" [REACT §THE FLOOR MANAGER] — QUEUE.
- F-R2: gives Harriet's mark to the empty half after her doubling — QUEUE.
- Never seen moving: "S12 Floor Manager. LAW: never heard moving. No footsteps,
  no cloth. His only audio is the room refusing to acknowledge him" [AUDIO §3
  S12; §8]. The reference teleports nothing — he simply is at the stack's end
  when visible [FM.gd 49].
- F1: "found after with his headset still cued, arm locked in a YOU'RE ON point at
  a camera that faces nothing, finished the way a gesture is finished" [CASUALTY
  §THE FLOOR MANAGER F1]. F2: "he exists only in the program feed, visible in
  monitors giving cues to rooms he is not in, and his freeze-check mechanic
  INVERTS: stillness near monitors now draws his point" [CASUALTY F2].
- Ending 1A: "The Floor Manager removes the headphones" [MASTER §ENDING 1A].

**Rooms.** MASTER CONTROL "the FM's realm … his headset's hook, the unlisted
camera's absence on the sheet" [ROOMS §MASTER CONTROL]; STAGE HALL "the FM's
point (F-R1) reads best from here" [ROOMS §STAGE HALL]; STUDIO A the mark
[INVENTORY §12]; ambient: two headset hooks, one bent straight and retired
[AMBIENT §MASTER CONTROL]. Reference spawn: TAPE LIBRARY (−4.5, 0, −19.4) "at the
stack's end", visible only `is_night and Broadcast.on_air and not premiere_live`
[WB 1123–1125; FM.gd 49].

**Beats.** T2 nights "glimpsed counting a corridor out" [WALK Part VI T2]; T3.5
the you're-on at the stack end [MASTER T3.5; SCARE 5]; T4.9 the seventh signal
warning [MASTER T4.9]; T5 F1 the fader, F2 the unlisted camera [CASUALTY]; the
Take: "The Floor Manager's count" [WALK Part V-B].

**LAW constraints.** LAW 2: the FM never lunges or pops; the point is a tell, not
a startle [LAWS 2; WALK Part IV]. LAW 7: F1 THE FADER (by omission at the divert)
and F2 THE UNLISTED CAMERA (three blind tally calls) [CASUALTY §THE FLOOR
MANAGER; §AS BUILT]. LAW 9: the signals must read by shape and position (the
assist-hold mercy for the watch is ACCESS §5). AUDIO silence ledger: "the Floor
Manager is never heard moving" [AUDIO §8; `restoration-invariant-suite.md` I15].

**Voice.** "Floor Manager: silent, contractually" [AUDIO §5]. Complete spoken
inventory: "'In five, four...' (three, two, one are hands). Nothing else, ever"
[MASTER App. C]; PLOT: "back in five, four..." [PLOT §characters]. The reference
speaks nothing ("Complete spoken inventory: nothing, here" [FM.gd 4]) — §7 C-8.

**Reference implementation.** `FloorManager` (Interactable) [FM.gd]; figure
`CharacterKit.floor_manager()` returns `{rig, arm}` [KIT 814–873]; interact
marks D08 read [FM.gd 90–94]; `[YOU'RE ON · TO NOTHING LISTED]` caption in the
premiere [ACCESS §3.2].

**OPEN.** OPEN-4 (age), OPEN-5 (pronoun), §7 C-8 (the count line).

---

### 2.7 CHUM · THE 1974 STAGE PUPPET (the icon)

**Identity.** "A handmade patchwork cat, canonized by the reference plate set
(four spec-sheet photographs, gray seamless, typewriter labels)" [DESIGN Part I ·
Chum]. Era: "1974 peak · Professional rebuild, the icon · 12 patches, collar and
bell added (silent), symmetric cross-stitch grin, amber eye viewer-left" [DESIGN
era table]. "the stage puppet, hand-sized, the one in the footage, the one the
tell-table catches lying about being repaired" [AF §WHAT IT IS]. Made by Peak
Production for WGLD [AF header]. "Built for maximum plush conversion … with
horror carried entirely in variant deltas" [DESIGN Part I · Chum].

**Silhouette and the patch ledger (base design, verbatim).** "brown boiled-wool
body, triangle ears with contrasting inner-ear patches (mustard left, navy
right), a round head with a visible center seam, one amber glass cat eye
(viewer left) and one black four-hole button (viewer right), a small dark nose,
three twisted-string whiskers per side, and a cross-stitched grin of small X
ticks along the smile curve. Hand-cut felted patches over the body: rust at the
chest, green at the right side, a large tan belly circle (his most huggable
feature), blue at the arm, plum at the thigh, mustard toe caps, navy at the tail
tip, all in contrasting blanket stitch. Thin brown collar with a brass keyhole
bell that never rings" [DESIGN Part I · Chum]. FABRIC §3 specifies: "Form: a
patchwork cat, seated height 55 cm, hand puppet with rod-arm option … THE MOUTH
DOES NOT ARTICULATE: the grin is cross-stitched and fixed by design; all
performance lives in head, ears, tail, and posture. Eyes: viewer-left, amber
glass, taxidermy grade, 14 mm; viewer-right, black four-hole button, 18 mm,
attached with visible waxed thread. Whiskers: fine wire, six per side. Bell:
brass, 25 mm, at the collar, SUPPLIED SILENT: clapper removed invisibly"
[FABRIC §3]. Whisker count and material disagree between DESIGN and FABRIC
(§7 C-9). Dressing kits: 1971 NEW and 1974 LOVED ("hand-polish on grip zones,
sun-fade crown, one visible early patch") [FABRIC §2 D2].

**Materials.** "Exterior: brown wool, hand-patchwork over a stuffed muslin core;
visible hand-stitching throughout; nothing may read machine-made at 30 cm.
Armature: wire in ears, tail, and spine; neck poseable and repeat-accurate; paws
weighted" [FABRIC §3]. Swatch library: "wools (Chum brown plus five compound
wools) … flannels including the school-gray" [ART §3]. "the wool spike shader is
the interim standard for all fiber surfaces" until scans pass sodium [ART §3].
Reference wool tint (0.34, 0.26, 0.17), belly (0.45, 0.36, 0.24), inner ears
mustard (0.72, 0.55, 0.18) / navy (0.16, 0.2, 0.35) [KIT 20, 335–345]. The
Blender factory has `tools/build_chum_1974.py` → `assets/models/chum_1974.glb`
(present in repo; not inspected by this lane).

**Scale truth.** Seated height 55 cm [FABRIC §3]. The reference stand-in is
≈ 1.05 m tall ("~1.05 tall" [KIT 290]) standing on the dock armatures — twice
the RFQ figure; which size the dock units and the Studio A stage body ship at is
**OPEN-13**. Understudy live build = +4 % [ART §6].

**Motion hooks (pre-fire = the operated body).** "Grammar: PERFORMED FOR CAMERA.
Broad, front-facing, cheated out to the lens. Classic puppet timing:
anticipation, overshoot, bounce-and-settle. Head tilts land in clean
fifteen-degree stops. The jaw flaps a half-beat off the phonemes … Weight reads
as five kilograms of felt and foam: fast starts, damped ends, secondary motion
everywhere (ears lag, whiskers tremble, the bell answers every gesture). Curve
language for animators: ease-heavy, bouncy, generous. In-game, the stage body
never animates; it participates in L1 drift only (a head angle that is not
yesterday's)" [MOTION §PRE-FIRE]. Note FABRIC's fixed grin vs MOTION's flapping
jaw (§7 C-10). The stage puppet rig "carries full secondaries and cloth"
[MOTION §PRODUCTION NOTES] — that rig exists for FOOTAGE (the tape stage), not
for the compound. In-tape beats: the Quiet Game, the approach and single-frame
lunge (SCARE 1), the fire tape's unfinished line, the 4K "Say it with me"
[MASTER T1.5, T3.4, §ENDING 2]. Live at the premiere "beside her, warm as ever,
bound to the format" [MASTER T5.3] (§7 C-11 against LAW 5).

**Rooms.** STUDIO A: "the stage body's home … CHUM'S MARK at center stage …
Drift: the mark's tape lifts one corner across days" [ROOMS §STUDIO A]; SCENE
DOCK: "the spare Chum inventory, rows of retired puppet bodies on armatures. One
of them is warm" [WALK Part II · Scene dock]; "DOCK: rows two deep, years in
order … the units' wools graying left to right by era" [ART §7]. Reference dock
rows: six `DockChum` units at x = −18, −16, −14 and z = −40, −41.7 (SCENE DOCK),
units 1–2 = `chum_pilot()`, units 3–6 = `chum_mini()` [WB 982–1006].

**Beats.** Every capture (in tape) T1.5 → T5; T4.3 the inventory count and the
warm unit; T5.3 the live premiere; ending 2 the 4K lean-in [MASTER].

**LAW constraints.** LAW 4: "THE WARM ONE NEVER ACTS. On camera, off camera, in
any ending. Nothing follows filing it. No system may contradict this, including
audio" — this is the warm dock unit [LAWS 4; WALK Part III.6 "Nothing springs in
the dock"; AUDIO §8 "The warm unit makes no sound"; DESIGN Part IV-B.12 "it never
stages the dock"]. LAW 5: "The bell rings once, at the finale beat, and its
caption says so. Chum's bell is otherwise silent; Chum speaks nowhere; Chum has
no account, no achievement title, no presence string" [LAWS 5]; "Chum's name
appears in no achievement title" [ACH §DOCTRINE 2]; A10 THE ROWS KEEP THEIR
ORDER "never mentions warmth" [ACH]. The bell on TAPE is a separate slot (S08:
"Chum's bell on tape which is DIFFERENT from S06: small, sweet, frequent") —
§7 C-12 against LAW 5 / DESIGN. LAW 2: the in-tape lunge is the only startle
[LAWS 2; MASTER SCARE 1].

**Voice (on tape only).** "Chum / the Understudy: double-voice: warm
children's-host falsetto with a chest resonance underneath that the period
chain cannot quite hide; ALL Chum lines recorded through dynamic mic, tube pre,
tape emulation, then the TAPE bus. He must never exist on the WORLD bus until the
finale's live set, and there he is quieter than expected" [AUDIO §5]. Pre-fire
sound: "EVERYTHING MEDIATED … roughly 50 Hz to 8 kHz, tape wow, studio slap"
[MOTION §PRE-FIRE]. Segment loops STORY CORNER / CRAFT TIME / THE SONG / THE
QUIET GAME with their lines [MASTER App. C]; S03 [AUDIO §3].

**Reference implementation.** `CharacterKit.chum_mini()` loads `chum_1974.glb`
or the procedural build [KIT 325–405]; `DockChum` "One of them is warm. Nothing
follows. Ever." [DOCK.gd]; the tape stage builds its own small Chum for the
lunge [STAGE.gd]. UE: nothing yet.

**OPEN.** OPEN-6 (the four reference plates are not in this repo), OPEN-13
(shipped size of the dock units and the stage body), §7 C-9, C-10, C-11, C-12.

---

### 2.8 CHUM · THE 1971 PILOT

**Identity and silhouette.** "1971 pilot · Cruder, endearing prototype · 9
hand-cut patches, no bell yet, frayed yarn whiskers, faintly uneven grin" [DESIGN
era table]. Dressing kit "1971 NEW (unworn finish)" [FABRIC §2 D2]. Base design
otherwise per 2.7 (DESIGN Part I · Chum) with the 1974 additions removed:
no collar-and-bell, nine patches, yarn whiskers, asymmetric grin. Which nine of
the twelve patches the pilot carries is **OPEN-7**.

**Materials.** As 2.7; "unworn finish" [FABRIC §2 D2]; oldest wool in the dock's
left-to-right greying [ART §7].

**Scale truth.** As 2.7 (**OPEN-7**, **OPEN-13**).

**Motion hooks.** None in the compound (dock unit, static). In footage the
pre-fire grammar applies [MOTION §PRE-FIRE].

**Rooms.** SCENE DOCK units 1 and 2 [WB 994–996]; the 1971 footage (WGLD STAFF
ORIENTATION, 1971 is the FM's film, not Chum's) [MASTER T2.4].

**Beats.** T4.3 the count [MASTER T4.3]. Ambient: the yard's crimp tag stamped
1971 [AMBIENT §YARD].

**LAW constraints.** LAW 4 (if it is the warm one), LAW 5 (no bell to ring).

**Reference implementation.** `CharacterKit.chum_pilot()` loads `chum_1971.glb`
or the procedural fallback (which is the 1974 build, i.e. the fallback is not
era-correct) [KIT 294–297]; `tools/build_chum_1971.py` exists in the factory.

---

### 2.9 CHUM · POST-FIRE STAGE PUPPET (nine deltas) and the 4K PREMIERE BODY

Not Phase 2 boxes (**OPEN-8**); recorded because the dock, the tape world and
the key art need them and because P1 §0.5 warns that their canon "must not be
mixed" with the mascot's.

**The delta set (design law: "fire damage reads as victimhood; the fear lives in
the repairs").** Nine deltas verbatim in DESIGN Part I (over-grin, wrong button,
chirality tell, whisker asymmetry, the bell opened, the belly accessed, two
wrong-material patches (school-gray flannel at the chest, glossy dark leather
at the leg; patch count 14), the tilt 2–3°, weight on the wrong foot) [DESIGN
§The post-fire delta set]. The caliper tell-table T1–T9 [FABRIC §5]: grin +18 mm
past each cheek seam; 28 mm horn button; amber eye now viewer-RIGHT, pupil axis
8° off vertical; whisker stubs 6 mm all sides; bell blackened with crown pry
marks, still silent; belly seam resewn in undyed thread; fourteen patches with
S-07 gray school flannel and a 40 × 55 mm leather patch at P11; neck tilt 2.5°
resting; left forepaw 12 mm forward. "REPAIRED, NOT BURNED. No char, no melt, no
horror finishing" [FABRIC §5; KEYART §rules]. The reference `HEAD_TILT 0.045`
rad ≈ 2.6° [TIMINGS.csv; RUNDOWN.gd 373]. DESIGN delta 4 and FABRIC T4 disagree
on whiskers (§7 C-9). "The post-fire tells are never called out by the game"
[DESIGN]. The flannel rhymes with D04's "square of gray flannel" and the green
room shim [PROPS D04; AMBIENT §GREEN ROOM; LORE §THE SHARD MODEL] — never stated.

**The 4K premiere body.** "1974 configuration in impossible fidelity ·
Individually rendered fur sheen, moisture in the glass eye, detail no puppet
could carry" [DESIGN era table]; D4 4K FINISH PASS "cleaned and groomed to
unsettling perfection" [FABRIC §2]; ending 2: "fur rendered strand by strand,
moisture in the button eyes" [MASTER §ENDING 2]. No grain on it: "no tape image
may ever appear clean except the anomaly slates" [ART §2] — the 4K premiere is
the digital broadcast, so its cleanliness is the point (**OPEN-14**: whether the
4K body passes through the artifact ladder at all).

**LAW constraints.** LAW 5 (bell), LAW 8 (ending 2's post-credits lie is the
only lie), KEYART "No startle imagery, no open mouths, no lunging poses in any
still".

---

### 2.10 AFTER-FIRE CHUM · THE MASCOT (cross-reference; Phase 1 owns the build)

This entry does not restate P1 or RIG. It records the facts the rest of the cast
must be consistent with.

| Fact | Value | Source |
|---|---|---|
| What it is | "the MASCOT: the 1974 walkaround body built for station events, eleven feet of it … someone rebuilt the mascot afterward from what survived: salvaged cable for tendons, a studio monitor speaker revoiced into the throat, leg rods, a weighted foot base, the original button eye melted shut and kept anyway, purely cosmetic. The other socket got a TALLY LIGHT CAMERA EYE." | AF §WHAT IT IS; PLATE-AF |
| Plate labels | HEIGHT (APPROX.) 11 FT (ABOUT 3.35 M); TALLY LIGHT CAMERA EYE; MELTED BUTTON EYE (NON-FUNCTIONAL) SCORCHED & WARPED; THROAT SPEAKER / RESONATOR; EXPOSED PUPPET TENDONS / CONTROL LINES; MANUAL JAW HINGE ASSEMBLY (LEFT & RIGHT) HAND-OPERATED NOT MOTORIZED; LEG CONTROL RODS; WEIGHTED FOOT BASE; "CHUM MANUALLY CONTROLS HIS OWN JAW"; "Requires minimum 3 puppeteers for full performance"; STATUS: ACTIVE / HAZARDOUS; "HE REMEMBERS THE AUDIENCE." | PLATE-AF |
| Eye sides | button eye viewer-LEFT (melted, cosmetic), tally camera eye viewer-RIGHT | PLATE-AF; KIT header comment; consistent with the post-fire stage swap (FABRIC T3) |
| Scale | 3.35 m standing, eye at 3 m, on wake; "HE DOES NOT FIT THROUGH DOORS"; 2.2 s per doorway | AF §THE SCALE LAW; LAWS 11 |
| Timings | 0.8 m/s approach, 1.2 m loom, 2.0 s cool (4.0 s taught), 2.2 s fold, 1.6 m/s crossing, 75 s crossing (62 without Vess, −13 self-held) | MOTION header; AF §THE TAUGHT CHASE, §THE LAST CROSSING; TIMINGS.csv; WALK §ADDENDUM c043 |
| Grammar | puppet grammar DELETED; POUR or PARKED; faces PATHS; three exceptions (FOLD, WITHDRAWAL, PERFORMANCE QUOTE); jaw by his own hand only, two grammar entries; bell never sounds; no vocalizations; throat speaker = band-limited room tone | MOTION §AFTER-FIRE; PLAN §1 Motion & sound law; QA-54 |
| Segments and anchors (reference) | STORY CORNER → TAPE LIBRARY; THE SONG → STUDIO A; CRAFT TIME → PATCH BAY; DEADROOM_DOOR (19, 0, 0) | RUNDOWN.gd 9–13, 22 |
| Lighting | "His eye is the only MOBILE red source in the game"; "HIS SHADOW IS A MECHANIC" at 3.35 m | LIGHT §HIM |
| Reveal | af_active on watching the fire tape; the dossier becomes D11 after first sighting | AF §THE REVEAL |
| The rig and clips | `SK_Chum_AfterFire`, bone list, shot list, OPEN-1..15 | RIG §§1–5 |
| The build | Phase 1 units 1.1–1.13, assets, sodium findings | P1 |

Never-stated: "What Chum is" and "Who rebuilt the after-fire body, and with whose
hands" [LORE §THE NEVER-STATED LEDGER] — the plate's "minimum 3 puppeteers" is a
shard, and the chalked puppeteer marks on the grid ("three, one scuffed to a
smear") rhyme with it [AMBIENT §STUDIO A]; no text may add the sum.

---

### 2.11 THE UNDERSTUDY and THE GLIMPSE FIGURE (no canonical body, by law)

**Identity.** "it has no canonical off-camera body, and the game never spends
that mystery. Manifestation rules: On any monitor or viewfinder: it is Chum,
performing, correct, bound by the show's physical logic. Off-camera, peripheral:
partials only. A felt hand at human scale resting on a doorframe. A proscenium
shadow that accompanies it like a stage edge it carries. Footsteps with the
weight of a person and the texture of upholstery. Direct sight: reserved for one
scripted glimpse in the entire game, late, brief, and never repeated. What the
glimpse shows is a puppeteer whose puppet is missing, or a puppet whose
puppeteer is missing; the animation should read as genuinely undecidable, and
playtests should confirm players split on which they saw" [DESIGN Part I · The
Understudy]. "the Understudy is not a character but a format" [PLOT §Dead Air].
Before af_active "it remains the old unseen presence" [AF §THE REVEAL].

**The glimpse (T4.8).** "At the corridor's elbow, for under two seconds,
unmediated: it … and it does not turn, and the plastic sheeting breathes once
with the draft of something passing that has already passed" [MASTER T4.8].
Reference stand-in: a near-black capsule r 0.22 × 2.5 m at (−12.6, 0, −16.0) in
the FIRE CORRIDOR with a 1.8 m bar at 2.9 m and four strings ("strings, or
tendons — part of what refuses to resolve"), shown 1.8 s [GLIMPSE.gd 33–61].
Sound: "S11 The glimpse. LAW: no sting. Before: nothing. After: one breath of
plastic sheeting, close, dry" [AUDIO §3 S11].

**LAW constraints.** LAW 3: "ONCE, EVER. The Day 4 fire-corridor moment occurs at
most once per save and is never referenced again by any system, including
achievements, presence, and logs. Its name appears in no code file" [LAWS 3].
"The glimpse has NO achievement, ever" [ACH §DOCTRINE 2]. Marketing: "The
glimpse figure and Leland's face are never depicted in any marketing material,
ever" [KEYART §rules]. LAW 2: no sting [AUDIO S11]. DREAD L5: "One once-ever
sight" [DREAD §L5]. The reference implementation names the moment in
`scripts/glimpse.gd`, `class_name Glimpse` and `GameState.glimpse_seen` — a
LAW 3 finding for the port audit (C17), recorded here, not resolved (§7 C-13).
For the UE asset: no mesh, class, log line or content path may carry that name
(**OPEN-15**: the UE name for the once-ever actor).

**Reference implementation.** `Glimpse` [GLIMPSE.gd]; not in UE yet.

---

### 2.12 ANSEL CRAIK (archival footage only)

"Seventies TV-crew look: big glasses, mustache, puppeteer's black sleeves. The
single most important design detail in the archival footage: in one late
episode, Craik is fully visible on set, both hands accounted for, while Chum
performs in the same shot. The game never zooms in" [DESIGN Part I · Ansel
Craik]. "Delivered entirely through materials in reverse order of composition"
[WALK Part I · Ansel Craik]. Voice: "Craik: archival only, optical-track
character, 8 mm sound" [AUDIO §5]. Not a Phase 2 unit; the in-tape footage
(tape stage) needs a figure only if the late episode is ever authored
(**OPEN-16**). Props D02 and the childhood scripts are his presence [PROPS D02;
MASTER T3.2]. Never-stated ledger applies to "What Chum is".

---

### 2.13 THE 58 CLUB ROWS and EXTRAS

"Enamel pins as regalia, potluck domesticity … members' clothing migrates over
the acts from civilian colors into the show palette" [DESIGN Part I · The 58
Club]. "EXTRAS AND PEGS: lead the curve by half a day, so the background is
always slightly ahead of the people you know" [ART §5]. THE ROWS: "each incident
abandoned past guarantee takes a seated club member on camera: cut away from a
smile, cut back to an empty chair, or to something half-resolved and interlaced,
still trying to applaud at the held-applause mark. Casualty count feeds every
epilogue's final card: THE 58 CLUB, followed by the new number" [CASUALTY §THE
ROWS]. "the club can deliver: from the lockdown onward they can restrain Rita and
hold her off camera" [WALK Part V-B]; SCARE 12 "hands, human and gentle and
immovable" [MASTER T5.3]. Rows seat in STUDIO A ("row casualties seat here")
[ROOMS §STUDIO A]. Extras: needle-felt, mitten hands WITHOUT stitched finger
definition (reserved for principals) [ART §6]. No count of extras exists
(**OPEN-17**). Not a Phase 2 box; ART §10 puts "extras, exterior, premiere
dressing" in P2.

---

## 3 · THE LAW MATRIX (who each law binds, per the cast)

| LAW | Text (short) | Cast members it binds and how |
|---|---|---|
| 1 ON CAMERA IS SAFE | "An active camera cone prevents the strike, always." | AF Chum (tally contract), the Understudy (bound on any monitor), Rita (the safe hide is lit) [LAWS 1; AF §THE TALLY CONTRACT; DESIGN Part IV.2] |
| 2 ONE STARTLE | "The in-tape lunge is the game's single jump scare." | 1974 stage Chum on tape (SCARE 1) only; FM never pops; the glimpse has no sting; the AF strike "is nearly silent" [LAWS 2; MASTER SCARE 1; AUDIO S11, S12; MOTION §AFTER-FIRE] |
| 3 ONCE, EVER | the Day 4 fire-corridor moment; "Its name appears in no code file." | The glimpse figure (§2.11); no achievement; no marketing [LAWS 3; ACH; KEYART] |
| 4 THE WARM ONE NEVER ACTS | "On camera, off camera, in any ending. Nothing follows filing it." | The warm dock unit — a 1971/1974 stage puppet on an armature in the SCENE DOCK (§2.7/2.8), NOT Merle, whose warmth is a different contract (CASTING §THE ONE LAW). Audio: "The warm unit makes no sound." The Coverage Director "never stages the dock" [LAWS 4; WALK Part III.6; AUDIO §8; DESIGN Part IV-B.12] |
| 5 SILENCE CONTRACTS | "The bell rings once, at the finale beat … Chum speaks nowhere; Chum has no account, no achievement title, no presence string." | Every Chum body: the collar bell is clapperless in every build (FABRIC §3; RIG `bell` bone locked; AF §SOUND AND CAPTION LAW); S06 is the one strike [AUDIO S06]; A-list titles never carry his name [ACH]. Conflicts logged: §7 C-11 (live premiere lines), C-12 (on-tape bell) |
| 6 THE SCHEDULE IS REAL | "Harriet freezes on breaks; window holds bind except during cascade." | Harriet (§2.3); the FM's signals report the window [MASTER App. C]; AF relocates on the BREAK flip [PROGRESS 0.7] |
| 7 EVERY DEATH HAS A SIGNATURE | "every death … traces to a nameable choice of Rita's, and the binder names it." | Merle M1/M2, Vess V1/V2, Harriet H1/H2, FM F1/F2, Leland L1/L2, THE ROWS — table in §4. "No per-death achievements, ever" [LAWS 7; CASUALTY] |
| 8 THE INTERFACE MAY LIE EXACTLY ONCE | ending 2 post-credits. | 4K Chum's ending only; Harriet doubled and the FM's feed-only haunt are WORLD states, not interface lies; the binder's casting drift "is not the interface lying" [LAWS 8; DESIGN Part III · Color] |
| 9 ACCESS IS CANON | booth, captions, assist, remap, pause, deferral. | Every character's sound event carries a caption from the parity set (ACCESS §3.2); the FM's watch has an assist-hold; signals read by shape [ACCESS; DESIGN Part III · Captions] |
| 10 THE TALLY CONTRACT | 1.2 m, no strike, visible countdown, 2.0 s cool. | AF Chum and Rita at the bench [LAWS 10; AF §THE TALLY CONTRACT] |
| 11 THE TWO HIDES | lit hide = camera cones; the dead room; 2.2 s per threshold. | AF Chum (holds at the felt door), Rita [LAWS 11; AF §THE TWO HIDES, §THE SCALE LAW] |

---

## 4 · THE CASUALTY SIGNATURES (LAW 7, per character, as built)

| Id | Character | Window / precondition | Rita's choice | The body (the house idiom) | Ripples the cast build must carry | Source |
|---|---|---|---|---|---|---|
| M1 THE SECOND VIEWING | Merle | Day 3+, the fire tape | let her watch with you (refusing saves her) | repossessed mid-sentence; "her voice finishes the sentence from inside the speaker, warm, three seconds after her chair is empty" | kettle never moves again (a rundown-audible silence), pegs freeze at her peg's day, night trips escalate one stage early | CASUALTY §MERLE; QA-40 |
| M2 THE HOME SINGER | Merle | premiere only | put her on the call sheet | sings HOME against HERE; "Taken on the beat, mouth still shaped around the true word"; MERLE O., STRUCK THROUGH | premiere forgiveness timers −20 %; the club noticed | CASUALTY §MERLE |
| V1 CREDITED, THEREFORE CAST | Vess | margin credit written | AUTHENTICATE, or the final breaker itself (as built) | "taken live, cut mid-sentence … his plastic pin fused into the panel enamel" | breaker incidents lose the easy variant; margin bleeds green (HE COUNTED RIGHT.); INK toast appends a line | CASUALTY §VESS; §AS BUILT; QA-42 |
| V2 THE UNCREDITED FIX | Vess | used his insight, never credited; cascade night | GET VESS at the dead panel | "interlaced with the transmitter hum, his outline refreshing at 60 fields a second" | as V1; crossing runs 62 s | CASUALTY §VESS; QA-42 |
| H1 CONTINUITY | Harriet | any break, Day 2+ | take the slip | absent; "the film cabinet now contains her, folded, with leader tape where her voice was"; the slip signs in her hand | seventh signal gated if before her card; screening unison loses her (0.05 tighter) | CASUALTY §HARRIET; HARRIET.gd 109–116 |
| H2 THE SPLICE | Harriet | the rejected edit as temptation | splice a reel carrying her segment | "doubled at the shoulders, both mouths open on different vowels, the teacup rising in two hands at two heights"; scenery thereafter | as H1; the second teacup retires (M-R5); the FM gives the empty half her mark (F-R2) | CASUALTY §HARRIET; HARRIET.gd 100–108; REACT |
| F1 THE FADER | FM | inside DEAD AIR | proceed to the door without arranging the fader | "headset still cued, arm locked in a YOU'RE ON point at a camera that faces nothing" | DEAD AIR splits 4a HIS HAND / 4b HER HAND | CASUALTY §THE FLOOR MANAGER |
| F2 THE UNLISTED CAMERA | FM | premiere | refuse or blind-call the tally cues three times | "exists only in the program feed, visible in monitors giving cues to rooms he is not in"; freeze-check inverts | cue marks stop auto-highlighting; persistent non-hostile monitor wrongness | CASUALTY §THE FLOOR MANAGER; §AS BUILT |
| L1 THE SIXTH QUESTION | Leland | five answers and wear past 70 | ask it | print burns from inside the frames; ink drains upward; D01 blanks mid-read | 1A closed; seance dock inert | CASUALTY §LELAND; §AS BUILT |
| L2 THE READING | Leland | the fire tape at the seance dock | play it into the wake | the sign-off completes in his reading voice; answers un-write; "the little door closing from the inside, his hand on the inner knob" | fire tape consumed; classic 4 replaced by 4c | CASUALTY §LELAND |
| THE ROWS | club members | premiere incidents past guarantee | abandon an incident | "cut back to an empty chair, or to something half-resolved and interlaced" | final card THE 58 CLUB + number | CASUALTY §THE ROWS |

Deaths are idempotent [`restoration-invariant-suite.md` I27]. Every death scene
ends in ≥ 1.5 s of authored silence [AUDIO §ADDENDUM S17–S19]. Two hidden
achievements only: A27 EVERYONE GOES HOME, A28 A ONE-WOMAN SHOW [ACH ADDENDUM].

---

## 5 · REFERENCE PLACEMENTS (Godot metres → UE uu → room, from ROOMS.csv)

Room membership computed from `Rooms.csv` rectangles (centre ± width/2 on x,
± depth/2 on z); the mapping rule is BRIEFS §0.1. These are where the reference
implementation PUTS the cast; canon rooms per entry may differ (noted).

| Actor / prop | Godot (x, y, z) m | UE (X, Y, Z) uu | Room by CSV | Canon room note | Source |
|---|---|---|---|---|---|
| Merle · KETTLE (day) | (8.0, 0, −1.0) | (800, −100, 0) | KITCHEN | matches ROOMS §KITCHEN | MERLE.gd 7; WB 1061 |
| Merle · CHAIR (night / after lockdown) | (2.6, 0, 1.2) | (260, 120, 0) | REC ROOM | matches | MERLE.gd 8 |
| Merle · screening spot | (0.4, 0, 1.4) | (40, 140, 0) | REC ROOM | matches | MERLE.gd 19 |
| Merle · DOORWAY (pen up) | (6.0, 0, −16.4) | (600, −1640, 0) | on the TAPE LIBRARY / BENCH ROOM edge line (x = 6.0 is both rooms' shared wall) | "Merle in the doorway" of the bench room [MASTER T5.2] | MERLE.gd 9 |
| Harriet | (1.2, 0, 2.6) | (120, 260, 0) | REC ROOM | canon home also GREEN ROOM (OPEN-11) | WB 1083 |
| Harriet's note (D06) | (2.8, 0.55, 2.2) | (280, 220, 55) | REC ROOM | PROPS D06 places it in the film cabinet | WB 900–901 |
| Vess (shrine wall) | (−3.7, 0, −1.2), yaw −π/2 | (−370, −120, 0) | REC ROOM | canon country is PATCH BAY / TAPE LIBRARY | WB 1086–1088 |
| Vess's binder (D07) | (−6.5, 0.6, 1.8) | (−650, 180, 60) | DORMS | matches INVENTORY §5 | WB 1052–1053 |
| Vess's cut (rejected edit) | (−2.6, 0.9, 1.0) | (−260, 100, 90) | REC ROOM | matches MASTER T4.5 | WB 1126–1128 |
| Ledger margin (credit entry) | (7.4, 0.9, −15.2) | (740, −1520, 90) | BENCH ROOM | matches | WB 1056–1057 |
| Floor Manager | (−4.5, 0, −19.4) | (−450, −1940, 0) | TAPE LIBRARY | "at the stack's end" [MASTER T3.5] | WB 1123–1124 |
| Dock clipboard (task) | (−19.5, 0.7, −38.0) | (−1950, −3800, 70) | SCENE DOCK | matches | WB 979 |
| Dock units 1–6 | x ∈ {−18, −16, −14}, z ∈ {−40, −41.7} | X ∈ {−1800, −1600, −1400}, Y ∈ {−4000, −4170} | SCENE DOCK | "rows two deep" [ART §7] | WB 982–987 |
| Sign-off card (props crate) | (−13.0, 0.5, −41.5) | (−1300, −4150, 50) | SCENE DOCK | matches MASTER T4.3 | WB 1041–1047 |
| Glimpse figure | (−12.6, 0, −16.0) | (−1260, −1600, 0) | FIRE CORRIDOR | matches MASTER T4.8 | GLIMPSE.gd 34 |
| Rundown anchors | segments → TAPE LIBRARY / STUDIO A / PATCH BAY; dead-room door (19, 0, 0) | — | — | matches ROOMS web ties | RUNDOWN.gd 9–13, 22 |
| Impossible crate (T4.1) | (0.0, 0.5, 6.0) | (0, 600, 50) | ENTRY | matches INVENTORY §2 | WB 1119–1120 |

---

## 6 · PHASE 2 UNIT MAP (what each box takes from this dossier)

| PROGRESS box | Reads | Must ship with |
|---|---|---|
| 2.1 Human pipeline v2 | §0.3, §0.4, OPEN-1, OPEN-2 | the render-language ruling (crafted vs MetaHuman), the naming ruling, the head-to-body 1 : 5.5 template, the eye-hierarchy law, sodium pass on every fibre |
| 2.2 Merle | §2.2 | the pen-up pose (45 s, hands empty and open), the busy-hands set (towel, spoon, mug, sleeve), the kettle/chair/doorway schedule, the never-drifts wardrobe, the 58 on the bib |
| 2.3 Harriet | §2.3 | the raised cup on its own rising track, the freeze that is a hard stop, the double (H2) as a second instance offset +0.13 m, pearls, brooch |
| 2.4 Vess | §2.4 | the plastic pin, the label maker, three pens, the 58 CLUB patch, the beard variant (T4), the avocado scarf variant (credited premiere) |
| 2.5 Leland | §2.5 | an in-frame body only (4:3, cropped by the frame edge), the legal pad as a text surface, green fine-liner; no compound placement |
| 2.6 Rita + floor manager variant | §2.1, §2.6 | Rita's gloves, sleeve protectors, loupe lanyard, clipboard (the avert shield), the film-can-lid clip for reflections; the FM's blacks, cap, headset with the coil to nothing, the right-arm point pivot, the run sheet angled away |
| 2.7 1974 Chum | §2.7, §2.9 | 12-patch ledger, amber viewer-left / button viewer-right, silent bell, the LOVED kit; the post-fire stage variant if OPEN-8 rules it in |
| 2.8 1971 pilot | §2.8 | 9 patches, no bell, yarn whiskers, uneven grin, NEW finish |
| 2.9 Cast animation sets | §2.2–2.6 motion hooks; §3 | Merle hands, Harriet sway/freeze/cup, Vess tells, FM signals (six + the seventh), the pen-up hold, H2/F1 death poses; AF Chum is RIG's |
| 2.10 GATE lineup | §1 | every figure beside its plate at matching framing [PLAN §R] |

---

## 7 · CANON CONFLICTS FOUND (recorded, not resolved)

| # | Conflict | Side A | Side B | Note |
|---|---|---|---|---|
| C-1 | Merle's age | "Late 60s" [SHEETS §MERLE]; "authentic 62 plus" [CASTING header] | "Late fifties" [DESIGN Part I · Merle]; seven in 1974 [MASTER T4.6; PROPS D04] | SHEETS is the later ruling ("Everything else on these sheets is law"); the arithmetic from 1974 is the owner's to settle (the game's "now" is never dated) |
| C-2 | Merle's wardrobe drift | "MERLE: begins already warm (mustard apron from Day 1) and never drifts" [ART §5] | "The casting-drift showcase … across the five tapes her wardrobe migrates into the show's host palette" [DESIGN Part I · Merle; WALK Part I]; plate apron is cream floral, not mustard [PLATE-MERLE] | ART §5 gives a reason ("nothing left to drift toward"); MASTER T4.10 ("in the show's palette head to toe") is consistent with either |
| C-3 | Harriet's surname | "mononymous by the club's own records" [SHEETS §HARRIET] | `## Harriet Lund.` [HARRIET.gd 3] | code comment only; no string ships it (GAMETEXT has no "Lund") |
| C-4 | Vess's pin material | plastic [DESIGN Part I · Vess; SHEETS §VESS "the plastic pin"] | the plate renders a metal-rimmed enamel-looking pin [PLATE-VESS] | SHEETS' own text overrules its image |
| C-5 | Vess's surname in achievements | KEYS [SHEETS §VESS; GAMETEXT.csv 11, 65] | "A11 PER V. CARDONA" [ACH A11] | stale; belongs to C14 (achievements audit) |
| C-6 | Leland's tenure | "tenure 1972 to 1976, vanished the year before the fire" [SHEETS §LELAND; PLATE-LELAND badge] | the club's "last archivist" whose project began "two years ago" [MASTER T1.3; PLOT §timeline "Two years ago, Leland's project begins and stops"; casting sheet LELAND "typed recently" [WALK Part V-B]] | both cannot be true of one man unless the game intends it; never-stated ledger territory ("Whether Leland chose to stay") — owner rules |
| C-7 | Leland's voice | "Leland: never voiced. The legal pad is text by canon" [AUDIO §5] | ending 1A gives him a spoken line "on every screen at once, dry and kind" [MASTER §ENDING 1A]; 4c "in his voice" [CASUALTY §LELAND ENDINGS] | could be text-on-screen in 1A; 4c says voice outright |
| C-8 | The FM's count | "'In five, four...' … Nothing else, ever" [MASTER App. C]; "back in five, four..." [PLOT] | "Complete spoken inventory: nothing, here" [FM.gd 4]; "Floor Manager: silent, contractually" [AUDIO §5] | the reference ships silent; the count line is unbuilt |
| C-9 | Whiskers | "three twisted-string whiskers per side" (1974); post-fire "three singed stubs on one side; two replacements on the other, too long, too straight, fine dark wire" [DESIGN] | "fine wire, six per side"; post-fire "T4 Whiskers replaced by stubs: 6 mm cut ends, all sides" [FABRIC §3, §5] | FABRIC is the RFQ the fabricator builds from; DESIGN is the catalog the community reads; the AF mascot has its own whisker set [P1] |
| C-10 | The stage puppet's mouth | "THE MOUTH DOES NOT ARTICULATE: the grin is cross-stitched and fixed by design" [FABRIC §3] | "The jaw flaps a half-beat off the phonemes" [MOTION §PRE-FIRE]; "the soft wooden clop of the jaw" [MOTION §PRE-FIRE sound] | the tape stage's lunge and the premiere's live Chum need a ruling on whether the 1974 body has a jaw |
| C-11 | "Chum speaks nowhere" | LAWS 5 | Chum speaks on tape throughout and LIVE at the premiere "beside her, warm as ever" with scripted lines [MASTER T1.5, T2.8, T3.4, T5.3, §ENDING 2]; AUDIO §5 specs his voice and "the finale's live set" | likely LAW 5 means the compound outside the format (no presence, no account); the premiere live lines are inside the format on camera; owner should restate LAW 5's scope in one sentence |
| C-12 | The bell on tape | "Chum's bell is otherwise silent" [LAWS 5]; "a brass keyhole bell that never rings. It rings exactly once in the entire game" [DESIGN] | "S08 … Chum's bell on tape which is DIFFERENT from S06: small, sweet, frequent" [AUDIO §3]; "the bell bright and forward in the mix" [MOTION §PRE-FIRE sound]; a child's bicycle bell with the clapper removed on the yard fence "rhymes with his" [AMBIENT §YARD] | one ruling decides S08 |
| C-13 | LAW 3 in code | "Its name appears in no code file" [LAWS 3] | `scripts/glimpse.gd`, `class_name Glimpse`, `GameState.glimpse_seen`, `fire_unsealed` toasts [GLIMPSE.gd] | reference implementation; for the port audit (C17) and the UE actor's name (OPEN-15) |
| C-14 | Harriet's home chair | GREEN ROOM "HER CHAIR" [ROOMS §GREEN ROOM] | REC ROOM chair + teacup [INVENTORY §3]; reference spawns her in REC [WB 1083] | per-tape schedule is OPEN-11 |
| C-15 | Dock row count | "in row three, mid-count" [MASTER T4.3] | "rows two deep" [ART §7]; reference 2 rows × 3 [WB 985–987] | six units in two rows have no row three; "row three" may be prose |

---

## 8 · OPEN (canon is silent; do not invent)

| # | Question | What is known | Who rules |
|---|---|---|---|
| OPEN-1 | Render language for the humans in UE: needle-felt crafted figures per ART §6 / PLAN §R.7, or MetaHuman-based likenesses of the photographic plates? | ART §1, §6, DESIGN Part II and PLAN §R.7 say crafted; PROGRESS 2.1 says evaluate MetaHuman in-unit; the plates are photographs | Owner, in 2.1 |
| OPEN-2 | Asset names for the cast (`SK_Merle` etc.) | only the prefix law exists [PLAN §1] | Mac lane, 2.1 |
| OPEN-3 | Rita's age, height, glove/hand scale | none stated anywhere; first person | Owner |
| OPEN-4 | The Floor Manager's age | none stated | Owner |
| OPEN-5 | The Floor Manager's pronoun in shipped text | DESIGN/WALK "they"; CASUALTY/REACT "he"; MASTER header "The Floor Manager is hands and countdowns" | Owner (a localization-readiness item for C12) |
| OPEN-6 | Where the four Chum reference plates ("gray seamless, typewriter labels") live | cited as ground truth by ART header, DESIGN Part I, FABRIC §1; not in `docs/canon/art/` | Owner |
| OPEN-7 | The 1971 pilot's nine patches (which nine), grin asymmetry amount, whisker count/length, standing size | DESIGN era table gives counts only | Owner / art |
| OPEN-8 | Whether the post-fire stage puppet and the 4K premiere body are Phase 2 boxes or Phase 4/5 (finale) assets | PROGRESS Phase 2 lists 2.7 and 2.8 only | Mac lane (tracker) |
| OPEN-9 | Merle's reading glasses on a beaded chain and a separate enamel pin: keep (DESIGN) or drop (plate shows neither; the 58 is stitched on the apron) | DESIGN Part I; PLATE-MERLE; KIT builds both | Owner |
| OPEN-10 | H-R2 (freezes +1 s while AF is active) and H-R1 — build in the port or leave QUEUE? | REACT queue 045/047; not in HARRIET.gd; not in `AHarriet` [PROGRESS 0.8b-5] | Owner / port |
| OPEN-11 | Harriet's schedule of chairs: REC ROOM vs GREEN ROOM per tape / per state | ROOMS §GREEN ROOM; INVENTORY §3, §17; WB 1083 | Owner |
| OPEN-12 | Vess's height | KIT comment 1.78 m vs mesh ≈ 1.67 m; no canon | Owner (or accept the head-to-body ratio and drop absolute heights) |
| OPEN-13 | Shipped size of the dock units and the Studio A stage body | FABRIC §3 seated 55 cm (a hand puppet); reference ≈ 1.05 m standing on armatures [KIT 290] | Owner |
| OPEN-14 | Does the 4K premiere body pass through the artifact ladder at all (ART §2: no tape image clean except anomaly slates)? | DESIGN era table "impossible fidelity"; MASTER §ENDING 2 | Owner |
| OPEN-15 | The UE name for the once-ever fire-corridor actor and its state flag, given LAW 3 | reference names it (C-13) | Owner + engineer |
| OPEN-16 | Whether Craik is ever an in-frame figure (the late episode with both hands visible) | DESIGN Part I · Craik; no tape stage content for it | Owner |
| OPEN-17 | Number and identities of club extras / the rows | none stated | Owner |
| OPEN-18 | Merle's monologue pacing in UE (the reference toasts at 3.0–3.4 s) vs "one unbroken take" | MERLE.gd 67–82; CASTING §LOGISTICS | Audio lead |

---

Verification for this file (cloud lane, no engine): a script checked that every
source key in §0.1 resolves to a file in the repo, that every `OPEN-n` is
defined exactly once in §8 and referenced at least once elsewhere, that the
reference placements in §5 fall in the rooms claimed when tested against
`Rooms.csv`, that the quoted canon lines exist verbatim in their sources, and
that the file contains no banned vocabulary [DREAD §ANTI-CREEP]. Output is in
the PR body.
