# RESTORATION · Godot Prototype v0.7 · Commit 024 · THE CLUB IS HELPING
## The engine's from-here debt list is now EMPTY.

## Run it
Godot 4.3+ · Import · F5.

## New in 024 · systemic sabotage
The premiere now carries continuous pressure. After the cold open, a
sabotage loop rolls incidents from a table: tally lights that lie about
program, house lights dropping to a murmured apology, the boom drifting
into frame, cue cards shuffling themselves. One incident at a time, each
announced, each with a fixture that fixes it (aux panel, boom winch, card
stand), and each escalating: failed takes shorten the interval between
incidents. Fail-forward is guaranteed three ways: the tally caps at two
refusals then lets you call it blind, the boom holds exactly one press,
and any incident older than 40 seconds is fixed by the club themselves,
apologizing. Every incident and resolution logs to user://premiere_log.txt
with timings, which is the soak harness's food.

## Standing
Twenty-four commits, 71 files. Everything the spike briefs marked
"owner: from here" is retired. What remains is hardware-bound (Spike 2),
asset-bound (footage, audio, VO, scans), tuning-bound (your verdicts), or
lives in the document queue. The zip owes nothing it can pay from here.

## Commit 025 · THE HARNESS (the zip tests itself)
The invariant suite's machine-side plan now ships in the box:
- scenes/soak.tscn + soak_runner.gd: headless soak entry.
  godot --headless res://scenes/soak.tscn -- --bot=wanderer --minutes=240
- Bots: wanderer (random legal movement, feeds I01/I02/I22), checker
  (monitor camping, feeds the Director), fail (seeds a PERFORM premiere,
  ignores every incident for two minutes, then stands the mark; feeds I06).
- Telemetry upgrade: the Rundown now logs WARN and STRIKE with segment,
  distance, savor flag, and a wall raycast at strike time (THRU-WALL flags),
  making I01 and I02 machine-checkable instead of aspirational.
- InvariantParser reads coverage, liveness, and premiere logs and writes
  user://INVARIANTS.txt, the per-build scorecard the milestone gates staple.

## Commit 027 · DEMO MODE (the cut plan's E1-E10, in the box)
Flip one line for the Tape 1 free demo: const DEMO := true in
scripts/game_state.gd. Demo build: Day 1 only (the bed declines), paper at
S1 and S5, every door past the library sealed with in-fiction reasons, no
Rundown, nights, dock, crate, seance, assets, or ledger. Capture completion
plays the end sequence: the sign lights alone, the protected card, any key
to title. The save writer whitelists under DEMO: it cannot write decision,
assets, answers, or ending fields. Local demo funnel at
user://demo_funnel.txt (disclosed here, never networked).

## Commit 028 · THE BOOTH (options)
O in game, or OPTIONS at the title: master volume, mouse sensitivity,
fullscreen, and the two access switches (TBC, photo-safe) in one panel.
Settings persist in user://settings.cfg, deliberately apart from the
transmitter log, so NEW GAME never resets your hands or your ears. The
loader guards headless mode so the soak harness stays indifferent.

## Commit 029 · ACCESS (remediation R1-R3 from the conformance pass)
UI TEXT SIZE and CAPTIONS join the booth. Every HUD label now carries a
black outline (dynamic-background contrast) and scales live from a cached
base size. The bell, doors, and pen announce themselves in text when
captions are on. The conformance pass lives at
docs/production/restoration-accessibility-conformance-pass.md and, per its
own methodology, still describes commit 028 until a device retest.

## Commit 030 · FILED (achievements)
The design doc's autoload, live: idempotent unlocks to
user://achievements.cfg, a Steam-ready unlock signal, and the DEFERRAL RULE
in code: nothing surfaces during play; the queue flushes only at the
morning toast (FILED · ...) or the title screen (FILED WHILE YOU WERE
OUT). Twenty-five of twenty-six wired to existing state; FULL ACCESSION
waits on prop read-flags. Disabled entirely under DEMO. The build check
that forbids the once-ever moment's name in this file caught its author's
own comment on the first run, which is exactly what it is for.

## Commit 031 · ACCESS WAVE TWO (R4-R7)
Focus rings everywhere focus goes. One ASSIST switch, three mercies:
wider beats, slower premiere clocks, hold E to be still. First run opens
the booth before the show. And REMAP: click an action, press a key; five
actions, conflict-refused, persisted. Residue named: prompts still print
letters, pending the glyph pass shared with localization.

## Commit 032 · THE EXTRACTION (localization L01)
tr() at the four chokepoints plus the booth, source-strings-as-keys:
byte-identical behavior until a locale column fills. tools/extract_strings.py
regenerates translations/strings.csv on demand, preserving prior
translations by key. Percent-templates are the counted residue: translate
the template, keep the placeholders.

## Commit 033 · FULL ACCESSION (the ledger closes)
The props packet's four missing documents are now physical readables (the
1974 clipping behind shrine glass, the welcome packet at the dorms, the
marshal report in control from Day 2, Iris Bell's letter in the dock after
filing), and six existing interactions mark their documents, so all ten
carry read-flags and A26 is live at 10 of 10. The glyph layer renders bound
keys for the five remappable actions at every text surface. Save v16.

## Commit 034 · INTERMISSION AND SIGN-OFF (past-zero, elective)
Escape now pauses: the world and its clocks hold, audio mutes, and the
intermission offers RESUME, THE BOOTH, or RETURN TO TITLE, refused only
mid-sequence. Endings roll a real credits crawl (CHUM, as himself; the
Floor Manager uncredited by request; the ending you reached, named), also
reachable from the title. Deaths and the demo still cut straight to title,
as they should. Edit the byline card in scripts/credits.gd.

## Commit 035 · AFTER-FIRE (the tally contract)
Watching the fire tape wakes the eleven-footer: the Rundown embodied per
docs/canon/restoration-after-fire-chum.md and the dossier art beside it.
While a capture runs he may cross the whole building to stand at 1.2 m,
weighted footsteps sounding, jaw captioned once, strike forbidden: the
tally is the contract. When it cools (2.0 s, announced) a strike lands
only if you let the clock die with him beside you; otherwise he withdraws.
The HUD counts it both ways: REC · SAFE WHILE LIT. Abort clears the flag
too: fleeing the bench starts the cool immediately. Dossier findable as
D11 (Day 4, master control) once he walks.

## Commit 036 · ELEVEN FEET (the scale law)
The number is now the mechanic. On waking, the body stands 3.35 m; the
tally eye at 3 m glows red only while a capture runs, so the light IS the
contract; and he does not fit through doors: every threshold costs him a
2.2 s fold, captioned, day and night. Rooms are his; doorways are yours.

## Commits 037-038 · THE TWO HIDES and THE LAST CROSSING
The lit hide: camera cones remain the shelter, him waiting at frame's edge.
The dark hide: the dead room eats your sound; he is deaf to anything born
inside it and holds at the felt door. The taught chase: his first cool runs
4.0 s with instructions written in dread. And DEAD AIR now costs a chase:
seventy-five seconds, master control to the little door, tally eye dark
because you diverted yourself off the rundown. Reached, caught, or late:
three authored outcomes.

## Commit 039 · THE LEDGER OPENS (M1, H1)
The casualty ledger is real: binder page one lists entries in stamp
register, or NO ENTRIES. KEEP IT SO. Merle asks at the fire tape and
consent is her first grave: repossessed mid-sentence, warm to the last
unfinished word, the kettle clicking off two rooms away. Harriet's frozen
hand offers a slip on Day 2+: free paper that signs in her hand, and the
next break edits her for continuity; the seventh signal gates shut if her
card was never found, and screenings judge 0.05 tighter without her.
Ending 3 and 2 carry their dead-Merle variants.

## Commit 040 · VESS (the credit dilemma)
Two pens, two graves. Credited: the record is a call sheet, activating at
AUTHENTICATE (every monitor cuts to her mid-sentence) or at the final
breaker she keeps (the handle drops, the lights hold, bars). Uncredited
but used: the cascade panel offers GET VESS, the full fix in eleven
seconds, then circuit F bare-handed, because nobody thanked her first.
Dead, the breaker is a fused pin and a hard blackout; the crossing loses
its grace (62 s); ending 2 inherits her warm chair; 1B files FILE UNDER:
STAFF. Restoring alone, in order, saves her. Choose her danger.

## Commit 041 · THE FLOOR MANAGER (F1, F2)
F2: the third blind tally call has a cost now. Coverage must come from
somewhere, and he steps into frame to cue a camera the run sheet never
carried. F1 lives inside the crossing as promised: at the divert, he is
already reaching for the master fader. Let him hold it and DEAD AIR
becomes 4a HIS HAND, found after in a YOU'RE ON point, CUE GIVEN beneath
the sign-off. Hold it yourself and your arm takes the argument, the
crossing loses thirteen seconds, and 4b HER HAND signs off left-handed.
If he is already dead, no one reaches for it but you. Ending 2 gains the
open headset nobody closes.

## Commit 042 · LELAND (L1, L2, endings 4c and 0)
Past the wear, the pad has room for a sixth line: ask it and the ink
leaves the paper, he is retroactively unfound, the dock goes inert, and 1A
closes forever (1B files AND THE READER, UNFILED, in pencil, because the
green ink is gone from the world). Or feed the fire tape into the wake:
the sign-off completes in his reading voice, the answers un-write, the
little door closes from the inside, and the premiere's final break simply
ends itself: 4c · THE COMPLETED SIGN-OFF, every light down in reverse tour
order, the tower light out, reading as rest. And if all four living are in
the ledger before lockdown, the premiere runs anyway: 0 · A ONE-WOMAN
SHOW, nine credit cards, one name, hidden A28, never advertised.

## Commit 043 · THE ARC CLOSES (rows, A27, the reading)
Every timed incident abandoned past its window now takes a seated club
member (cut away from a smile, cut back to an empty chair). Every ending
opens its credits by reading the ledger aloud: name, cause, epitaph, and
the club's new arithmetic. A27 EVERYONE GOES HOME rewards the run with
nothing to read. Cast sheets canonized under docs/canon/art (Vess Keys,
he, PER V. KEYS everywhere; Leland Merrick, whose green-ink L.M. was in
the props packet all along; Merle co-founded the Club with him; Rita's
taglines adopted). The station is WGLD, Channel 58, by the author's word.

## Commit 044 · THE SPLICE (H2, and the answers grieve)
The rejected block's second life: after the viewing it offers the splice,
label disclosed (THE SONG, HARRIET LEFT OF FRAME), and joining the takes
mints a daily with no bench and no twelve seconds. The next break doubles
her, an inch to the left, both mouths on different vowels, and she stays:
scenery the schedule stopped scheduling, one line forever, the double
rebuilt on every load. The seance now grieves: frames 14 and 28 answer
differently for the dead, and every reading with her name carries
TRANSITION UNRESOLVED. Ten of ten deaths built. Zero open graves.

## Session 65 · HARRIET CANONIZED + THE PRESS KIT
The Continuity Keeper joins the cast doc, her sheet quote now speaks in
the build, and docs/press-kit ships whole: factsheet (features all
implementation-backed), cleared pull quotes with a firm embargo doctrine
(graves are not previews), and all six portraits. Standalone press zip in
outputs.

## FIRST BOOT (Session 66)
Executed for the first time on Godot 4.3 headless inside the build
environment: fifteen import errors fixed in one round, then ZERO errors,
two clean soak runs, invariants I01/I02/I22 PASS, and a valid v16 save
written by the running game. Full report and raw telemetry in
docs/telemetry/first-boot/.

## Commit 045 · THE BODY SHOP (the art pass begins)
Two libraries, no imports, the zip still owes nothing: scripts/prop_kit.gd
(procedural PBR — plaster, concrete, wood, metal, fabric, generated normal
and roughness maps, cached and shared) and scripts/character_kit.gd (the
cast as sewn things: button eyes, proud seams, visible craft). Walls and
floors carry relief; every room gets a baseboard; the corridor monitors
live in real CRT cabinets — bezel, knobs, a warm power lamp — the
SubViewport feed inset as glass. The armchairs are armchairs (the lockdown
still converts them). Merle has her apron and bun in the round; Harriet
her collar and rising cup, and the splice doubles her whole body now, not
her parts. The Floor Manager turns to face you always, and the point is a
real arm: it rises for YOU'RE ON and hangs when the take holds. The dock's
six units and the stage mark carry the canonical Chum body — ears, amber
eye, button eye. And the eleven-footer is embodied per the dossier:
flannel over a frame that shows, a patch nobody matched, hands sized to
close a distance, the tally eye seated in the right socket, and a jaw on
a visible lever that works — twice — at first sighting. The scale law now
scales the whole body. Verified on Godot 4.3 headless this session: clean
import, wanderer soak I01/I02/I22 PASS, fail-bot premiere I06 PASS.

## Commit 046 · THE MACHINE SHOP (and the walk)
The instruments stop being boxes. The patchbay is a console: angled
fascia, two knob rows, six faders at honest heights. The bench is a
workbench — top, legs, and a reel-to-reel with spoked reels and transport
buttons. The degausser shows its coil and wears a hazard stripe; the flat
file grows four drawer faces, the second sitting proud because it will not
fully close; the projector aims a lens at the club print and carries two
reels. Every hinged door is paneled now, handled on both faces, the little
door included. Log stations are lecterns — post, angled top, binder, pen
on a chain. Keys read as keys: bow, shaft, teeth. The bench TVs live in
the same CRT cabinets as the corridor rigs. Rita's bed is made (frame,
mattress, blanket tucked hard, one pillow) and the dresser's three drawers
have knobs. Wall clocks get housings; the readout hangs beneath the face.
And the eleven-footer walks like a thing with weight: bob and sway while
he covers ground, facing his own direction of travel, deeper and slower
after the fire. Verified: clean import; wanderer, checker, and fail-bot
soaks all PASS (one duplicate-variable parse error caught by the machine
and fixed before it could ship — the harness eats first).

## Commit 047 · THE STACKS, THE HALL, THE TOWER
The rooms named for things now contain them. The tape library grows four
used archives: uprights, shelves, spines with deterministic jitter —
widths, tints, leaners, and the gaps where borrowed tapes were never
returned (seeded stable, so your library is your library on every load).
The transmitter hall gets four rack cabinets along the east wall: vent
slats, paired gauges whose needles disagree, one warm lamp apiece, a
handle big enough to mean it. The dead room shows its felt: panel runs on
three inner faces, because the hum stops at the seam and the felt is why.
The yard raises the tower — four tapering legs, cross-braces, the red
beacon — and THE COMPLETED SIGN-OFF puts its light out, per its own
credits (new GameState.ending_marked signal, emitted from mark_ending).
Pallets accumulate at the base, the way they do. The bench reels turn
while tape rolls, supply and take-up at honest, different speeds. The
asset rack becomes a plank with four berths; a canister lands as each
asset banks. Cue signs get surrounds and hoods; the entry coats get their
rail and pegs. All new furniture carries collision. Verified: clean
import; wanderer and fail-bot premiere soaks PASS (the harness ate a
cosf-for-cos typo first, as is its right).

## Commit 048 · THE KETTLE (domestic dressing, and the set completes)
The kitchen earns its name: a five-meter counter run against the north
wall — door faces, knobs, a sink with taps, uppers — and on the counter,
the kettle. Spout, lid knob, handle arch. It is the same kettle that
clicks off two rooms away, eventually, and now you can look at it every
morning without knowing that. Two mugs nobody collected; a small table
where the club took its breaks. In Studio A the cubby wall becomes actual
cubbies: a seeded grid of cells, roughly half still holding a ball, a
block, or a tin, because a show for children keeps things. The three
camera pedestals grow pan heads, bodies, lens hoods, viewfinders, and
operator handles, and every lens is aimed at Chum's mark, because it
always was. The yard gets packed dirt underfoot and the two worn path
legs everyone actually walked: door to junction, junction to shed. And
every dock in the building — seance, spectro, ledger, cart rack, crates,
readables, all fifteen-odd of them — now stands as cased equipment:
plinth, rim, brass plaque, one _dock_body upgrade paying out everywhere
at once. Verified: clean import; wanderer and fail-bot premiere soaks
PASS (the harness ate an untyped-Variant inference error first).

## Commit 049 · PLAYABLE (WASD, the last rooms, and proof)
Make sure you can actually play it, so: WASD joins the arrows on the
four movement actions (project.godot, defaults preserved). The green
room furnishes — vanity with two-of-three bulbs burning, couch, low
table. The scene dock leans three painted flats in ranks and stacks its
crates. The dorms sleep three now: two more beds, blankets loose because
nobody checks, and a locker run with one door ajar. The shed keeps paint
cans, a shelf, and a broom behind its padlock. The environment learns
filmic tonemapping, subtle glow (the tally eye, the lamps, and the
vanity bulbs bloom now), and SSAO to sit the furniture down. And the
proof: Movie Maker mode drew the game's first real frames — title screen
with focus ring, Day 1 rec room with the HUD alive — at 6.9 ms/frame on
the build machine's GPU. Frames archived at docs/telemetry/first-render/.
Wanderer and fail-bot premiere soaks PASS. Import · F5 · WASD + mouse ·
E to interact. It plays.

## Commit 050 · THE PLAYTEST ANSWERS (first human contact)
The first human playtest found what soaks never could, and each finding
is now a fix. YOU COULD NOT TURN: the HUD's full-rect Control was eating
every mouse-motion event before the player saw it (mouse look now lives
in _input, the HUD passes events through, and sensitivity is clamped so
a zeroed settings file can never freeze the camera again). YOU WALKED
THROUGH THE ARMCHAIRS: solid now, before and after the rows. THE TEXT
WAS PHYSICAL: the giant floating room names and the CATWALKS banner are
gone (the map carries the names); every surviving tag drops to plate
size. IT WAS TOO BRIGHT FOR WHAT THIS IS: ambient falls to a floor, the
sun to a memory, fog thickens, exposure drops, SSAO deepens, walls and
floors darken, and every room keeps exactly one dim warm practical that
browns out further at night — the building is lit in pools now, like
the cast portraits always said it was. AND THE CHARACTERS WERE WRONG:
rebuilt from docs/canon/art. Chum is a CAT, as the dossier plate has
always shown — triangular ears (one singed short), wire whiskers, melted
button left eye, tally socket right, stitched mouth with staples, manual
jaw with its lever inside, throat speaker, collar bell, salvage patches,
claw hands, weighted paws, tail — at puppet scale and at eleven feet.
Merle and Harriet are PEOPLE: cardigans, blouses, skirts, buns, the
apron with its 58, the brooch, per their sheets. scenes/cast_preview.tscn
stages the whole cast under portrait light for checking against canon.
Renders verified frame-by-frame on the real renderer; lineup and rec
room archived in docs/telemetry/first-render/. All soaks PASS.

## Commit 051 · THE ENGINE QUESTION, ANSWERED WITH TEXTURES
The UE5 migration map (docs/unreal-5) was consulted and its own doctrine
held: engines are replaceable, the laws are not — and the laws are here,
tested, in sixty invariant-green soaks. What Unreal actually offers is a
store; the assets themselves are engine-agnostic. So the zip now carries
its first imported assets, six CC0 PBR sets from Poly Haven
(assets/textures, credits filed): worn cracked plaster, worn concrete
floor, worn table wood, woven fabric, floor-plate metal, dirty carpet.
PropKit gained _pbr(): scanned maps, triplanar world-space tiling so
every procedurally-sized box tiles honestly, tint preserved per prop,
and the old procedural surfaces kept as fallback if the files are
absent. Walls crack now. Floors are poured. The armchairs are
upholstered in actual weave. The studio carpet is a carpet that has
been walked on since 1974. Verified frame-by-frame on the real
renderer; soaks PASS. The engine memo can stay unsigned another year.

## Commit 052 · THE PLATE SET (canon reconciled, deltas sewn in)
The full document stack arrived on the desktop and was reconciled against
the repo: the repo's canon was already newest everywhere it mattered (the
cat plate, Revision 2's armed scare economy, Rita Ivori, the Crafted
World doctrine — humans as cloth and needle-felt over armature, which is
what the character kit already builds). One genuinely new document filed:
docs/pre-production/restoration-build-plan.md, the plan this build has
been unknowingly following (systems first, content in tapes, the
invariants as CI — Part VI's suite is running nightly here in spirit).
And the design doc's reference plate is now sewn into the bodies. The
1974 mini carries the plate exactly: mustard inner-ear left, navy right,
head center seam, rust chest and blue arm patches, mustard toe caps,
brown collar, brass keyhole bell, navy tail tip. The after-fire body
carries the delta set by number: the over-grin sewn past where a cat's
mouth ends (1); the wrong button, too large, over-wrapped (2); whisker
asymmetry, three singed stubs and two wire replacements too long and too
straight (4); the belly accessed, darker wool, dense restitch scarring
(6); school-gray flannel at the chest and glossy leather at the leg,
materials no toy should have (7); and the tilt, the neck restitched
2-3 degrees off true, permanently cocked, listening (8) — the cheapest,
most terrible delta on the sheet, now one line of rotation. Deltas 3
(chirality) and 9 (footage-only weight) belong to the tape world and
wait there. Verified: clean import, cast render checked against the
plate, soaks PASS.

## Commit 053 · THE CASTING CALL (the figures earn their sheets)
The blob era ends. character_kit.gd grows a real figure system — anatomy
(calves under hems, hips joining legs to torsos, shoulders, elbows, hands
with fingers and thumbs), faces (skull and jaw, cheeks, nose bridge and
tip, whites-and-iris eyes, brows, the soft downturned mouth age writes),
four hairstyles (Harriet's neat curled crown and high bun; Merle's low
loose bun with six escaping strands; Vess's twelve-sphere dark mop;
Leland's grey-going part), posed arms (down, folded, cup-raised, clutch,
pocket), and the props the sheets insist on: Merle's towel with its red
stripe, her reading glasses on a beaded chain, the enamel pin, the floral
apron with the stitched 58; Harriet's saucer in the left hand while the
script-owned cup rises through the days in her right, the brooch, the
pearl earrings; Leland's legal pad with five green-ink lines, the wire
glasses, the loosened tie, the stubble; the Floor Manager's cap and
shadowed face, earcup headset, run sheet angled away, and a coiled cable
descending to nothing. AND VESS KEYS ENTERS THE BUILDING: the tape hunter
finally has a body — washed-black jacket over the patterned shirt, 58
patch, plastic pin, three chewed pens, the label maker on his belt — and
stands at the shrine wall as an interactable, speaking his own sheet's
lines, hiding himself if the ledger ever carries his grave. The fabric
tint math calmed from rust toward the sheets' browns and creams. Two
render iterations against the plates, archived. All soaks PASS.

## Commit 054 · THE FABRICATION (Chum, sculpted)
The build plan's one unsafe choice was "build Chum for real." Done, in
the only shop this zip owns: tools/build_chum_af.py drives Blender
headless — fused organic masses voxel-remeshed into one continuous
felted body, displaced twice (felt lump, fiber), decimated to game
weight, and exported as assets/models/chum_af.glb (the project's first
modeled asset, built from its own code, reproducible with one command).
The dossier plate is honored in mesh now: the round-bellied scorched
body; weighted paw feet with toe lobes; tendon cables on the left arm
and control rods at the legs; clawed mitts; the collar and brass bell;
the throat speaker; patches shrinkwrapped to the lumpy surface so they
sit sewn, not floated — rust, green, the school-gray flannel, the
leather; the huge head with brow ridge and cheeks, triangular ears
(left singed short, edge ragged), the melted button in its char ring,
the empty right socket where the tally eye seats at runtime, the felt
nose, whisker stubs left and wire whiskers right, and the over-grin's
staples above a jaw hinged at a real pivot — the Jaw node, driven by
the same one line of tween the box body used. Head empty at the exact
coordinates rundown.gd has always used, so the scale law, the tally
eye, the fold, and the gait all ported without touching the hunter's
code. Godot dresses the imported wool in the scanned fabric relief via
triplanar (remeshed surfaces carry no UVs; triplanar doesn't care).
The procedural body remains as fallback if the glb is absent. Three
Blender iterations, one color-space lesson (glTF baseColorFactor is
linear; the palette is authored sRGB), premiere soak PASS. He has
never looked more like what the dossier says he is: ACTIVE / HAZARDOUS.

## Commit 055 · HE WALKS (and the icon returns)
Two more turns of the fabrication crank. First, THE WALK: the after-fire
body rebuilt with pivot empties at the hips, the shoulders, and the tail
root, and the Rundown's gait now drives them — legs striding, arms in
counter-swing at six-tenths, the tail dragging nine-tenths of a beat
behind, everything easing back to stillness when he stops to watch. The
weighted footstep thunks finally belong to feet that move. Second, THE
1974 PEAK: tools/build_chum_1974.py fabricates the icon itself —
chum_1974.glb, the professional rebuild the club fell in love with.
Warm brown boiled wool, pristine surfaces (this one was kept clean),
the big tan belly circle he was hugged by, triangle ears with mustard
inner viewer-left and navy viewer-right, the head's visible center
seam stitched as a thread hoop, one amber glass eye and one black
button, a cross-stitched grin of true X ticks, twisted-string whiskers,
rust chest, green side, blue arm, plum thigh, mustard toe caps, navy
tail tip, the thin brown collar, and the brass keyhole bell that never
rings. The dock's six retired units and the stage mark now hold the
sculpted icon; the procedural body remains as fallback. In the preview
lineup he stands between the club and his own scorched future, which is
the entire corruption gap in one camera frame. All soaks PASS.

## Commit 056 · THE PERFORMANCE (body language as canon)
Chum's character, not just his body. The head tracks now: within eleven
meters the eye finds you and holds — through the walk, through the fold,
through everything — because the head is the honest part. Standing at
his segment at night, he PERFORMS: the jaw works lines nobody wrote for
an audience that is not there, the arms present alternately, the tail
keeps slow time; the sound of a show performed to no one finally has a
body doing the performing. The doorway fold is an actual fold: he
compresses, ducks, pulls the arms in, and the head stays on you the
whole way through, per the caption that has always said so. Strikes
have a delivery: both arms rise past the shoulders and the jaw opens
past where the grin ends, nine-tenths of a second the retake blackout
almost mercifully covers. And the dock now shelves his generations in
order: tools/build_chum_1971.py fabricates the pilot — cruder voxels,
heavier lumps, frayed yarn whiskers, a faintly uneven grin, ears cocked
unevenly, no collar and no bell yet, somebody made this at a kitchen
table and you can tell — and the first two dock units wear it, so the
rows read as fur going gray forward, the way T4.3 has always described
the room. Every animation line null-guards the procedural fallback.
Wanderer and premiere soaks PASS.

## Commit 057 · THE FACE (six passes against the plate)
The head, iterated against the dossier until it answered: a dedicated
head-check scene (scenes/head_preview.tscn, the bench light's view of
him, tally lit, jaw ajar) rendered six build iterations, each diffed
against docs/canon/art/after-fire-chum-dossier.png feature by feature.
What the plate demanded and now exists in mesh: the TALLY-LIGHT CAMERA
EYE as a true lens assembly — metal outer ring, recessed barrel, dark
glass, and the runtime red dot seated in front of it, small and hot,
a lens and not a bulb. The MELTED BUTTON EYE as a flat four-hole
rosette in a char ring with one drip. THE MAW: a single dark throat
spanning the lower face, rimmed in rolled-fabric lip beads, ringed
with steel staple teeth that emerge from under the upper lip and rise
from the lower — and the entire lower assembly (lip, teeth, void)
rides the Jaw node, so the trap opens on the same hinge the lever has
always worked. Hooded scowl brows. A patchwork skull — rust, charcoal,
tan panels shrinkwrapped to the burlap — with the center seam as
stitch bumps over the crown and X-ticks where panels meet. Ears tall
and forward, tip patches sewn on, the left still singed short. Straw
whisker stubs left, wire replacements right, rooted at the muzzle.
The lessons of six passes are in the script for the next model: mouths
are ellipses wrapped onto curved surfaces, lower lips belong to jaws,
and a red light is a lens only if the housing swallows it. Before and
after archived in docs/telemetry/first-render/. Soaks PASS.

## Commit 058 · THE MATERIAL TRUTH (Blender bakes the burlap)
The realism the flat colors could not carry now ships in the glb.
tools/build_chum_af.py grew a full Cycles bake stage: every fabric part
is UV-unwrapped (modifiers applied at build so the maps sit on real
topology) and dressed in a procedural burlap built in nodes — two
crossed wave bands for the weave, noise for the dye mottle, a
large-scale scorch field thresholded into burn blotches, ambient
occlusion pooling soot in the crevices, and the weave's own height fed
through a bump into the normals. Three maps per part — albedo,
roughness, tangent normal — baked in 47 seconds across eighteen parts
and packed into the glb, which grew from two megabytes to twenty-seven
and earns every one. The Godot loader now recognizes baked materials
(albedo texture present) and passes them through untouched; the
triplanar weave remains only as dressing for unbaked fallbacks. One
lesson re-learned at a new address: shader tints author in sRGB and
travel linear, in bakes as much as in factors — the first bake rendered
him oatmeal. The head that emerges is the dossier's material truth:
scorched wool with visible fiber, dye gone uneven, soot where the
folds are, a worn rust patch, steel teeth gone cold. Premiere soak
PASS. He was always a thing somebody made. Now he looks handled.

## Commit 059 · THE FRAY (Blender, deeper: fuzz, folds, machinery)
The head's last mile, still in Blender, still one command. A fiber
fringe generator now samples the skull, ears, and jaw surfaces and
grows real geometry fuzz along the normals — six hundred fine tapered
fibers, seeded deterministically, that break every silhouette the way
burnt wool actually frays; no shader fakes it because none can. A
marble-noise fold layer pulls cloth wrinkles across the skull. The two
brow welts fused into one heavy bar that hoods both sockets into the
dossier's scowl. The tally lens gained its inner ring and six rivets
(and one stray fiber that reads as a scratch across the glass, kept,
because the dossier would have kept it). The button eye sits in a
six-rayed scorch star. The upper lip carries X-stitches between its
beads; inside the mouth, two curved steel jaw bars glimmer where the
dossier's construction plates say the mechanism lives. Fibers tuned
finer in a second pass so the fray reads as wool, not needles.
Nineteen bakes, soaks green, and the head now answers the plate in
structure, material, and silhouette — the three things a reference
sheet is for.

## Commit 060 · THE GATE AND THE ARM
The head passed its gate. Version thirteen against the plate: the burn
field pools char around the lens eye so the face reads two-toned the
way the fire left it; the whiskers are kinked straw bundles now, two
overlapping segments each, eight per side of asymmetry (burnt short
left, wire-long right); the ear interiors turn their mustard and navy
forward; the grin corners curl up past where a cat's mouth ends with
staples following; the nose went waxy. Thirteen iterations, each
rendered and held against the dossier, and the last one answers it.
Then, per the construction plate's detail 3, ONE ARM, crafted: a
segmented limb with a stitched seam ring where it was sewn back on,
a tied fabric wrap at the elbow, tendon cables running shoulder to
wrist through three brass guide rings (three cables on the exposed
left, one survivor on the right), and a hand rebuilt as a palm with
three two-lobed fingers in dark claw sheaths, everything fuzzed and
baked like the rest of him. scenes/arm_preview.tscn joins the check
scenes. Soaks PASS. Current renders on the desktop and in telemetry:
the puppet is being fabricated exactly the way the dossier says he
was — one salvaged piece at a time.

## Commit 061 · THE COAT (fur, at last, and the blend in the open)
The head was bald and the plate never was. A matted-fur system now
grows thousands of curved ribbon strands directly in bmesh — surface-
tangent, drooping, width-tapered, tinted from a three-color palette
(char-dark, mid-brown, rust) — across the skull, ears, and chin. A
face mask keeps the muzzle, the maw, and both eye assemblies worn
bald, so the hardware reads through the coat the way the dossier
draws it: fur where he survived, wear where he works. Teeth and lip
beads went irregular (jittered scale and pitch, one missing on each
row, like the plate). And the shop door is open now: every build
saves blend/chum_af.blend — the live Blender file, openable and
sculptable in the app — with a .gdignore so Godot's importer keeps
its hands off the folder (it tried; the import hung a full seven
minutes on the discovery before the ignore file ended the argument).
Premiere soak PASS. The coat is the character: he was soft once, and
most of him still is, and that is the worst part.

## Commit 062 · THE RESOURCE LAYER (real cloth, real burns, full coat)
The tons of free resources, used. Four CC0 scan sets from ambientCG
now feed the bake as build-time sources (tools/texsrc, credited,
gdignored after Godot tried to import the sample .blends and hung the
pipeline a second time): Fabric031's wool carries the body and skull,
Fabric030's coarse weave carries the patches, Leather030 the leather
patch, and Metal058A's smudge maps drive the burn blotches — real
grime shapes where noise used to guess. The scans ride box projection
in object space (no UVs needed at bake time), tinted into the palette,
tiled at nine-to-sixteen repeats the meter, with scanned weave normals
under a grunge bump. Bakes doubled to 2048 for the big parts. A
Poly Haven workshop HDRI (assets/env) feeds the preview's reflections
at low energy so the lens ring and staple teeth catch a real room.
And the coat finished growing: the fur system now covers the body,
arms, legs, and tail — some ten thousand strands across the whole
puppet — with masks keeping the accessed belly, the foot soles, and
the face plate worn bald. One color-tuning pass en route (the first
HDRI wash and a too-coarse tiling both got caught by the render-diff
loop). Premiere soak PASS. The blend file in the open Blender app
refreshes on every build: File > Revert shows the newest body.

## Commit 063 · THE RIGHT RENDERER (Cycles, real hair, and the answer)
Why did he still look terrible? Because every image so far came from
the game engine's real-time rasterizer, judging a creature design that
was authored against a path-traced painting. The design loop now runs
in Blender end to end: tools/render_chum_af_beauty.py opens the live
blend, swaps the game's ribbon fur for REAL PARTICLE HAIR — ten
thousand parents, a quarter million children, clumped, curled,
melanin-randomized, masked bald at the muzzle, belly, and soles —
adds subsurface to the cloth, lights it like the plate (HDRI world,
warm key, cool rim, a dedicated face light, the tally's own red spill),
and renders denoised Cycles stills on the Metal GPU to renders/. Two
bugs died on the way: the Principled Hair BSDF ignored its Color input
until parametrized by melanin (the first coat rendered blond), and —
the big one — the baked textures were never PACKED into the .blend,
so every reopen (including the beauty render, including the user's
open Blender app) saw black albedo and zero roughness: the black-glass
face. One img.pack() loop fixed three symptoms at once. The game
still ships the baked glb; the character is now DESIGNED in Cycles.
Design in Cycles, ship baked — the build plan's shoot-clean doctrine,
finally implemented in the pipeline itself.

## Commit 064 · THE FACE, FULLY HARDWARED (the plate's anatomy, in Blender)
The face crop of the dossier plate, item by item, in Cycles. The face
is a QUILT now: staggered wool panels whose seams cross the whole
front, stitched with staple runs — a center seam from crown to nose,
cheek seams, brow seams. The ears carry their fabric panels at last,
mustard viewer-left and navy viewer-right, big and front-facing. The
tally eye sits in an aged copper ring with eight rivets and a recessed
barrel; the button eye became a gear-toothed bronze rosette. The felt
nose went plate-sized. And THE MOUTH became the manual jaw rig the
construction plates describe: a lightproof black slot (emission-zero
shader — Cycles' Principled keeps a specular floor that renders even
near-black cloth as grey under a close key; a zero-strength emission
cannot reflect anything, and the mystery of the grey muffin died
there), framed top and bottom by aged bronze bands with dense staple
rows, machinery slats glimpsed deeper inside, a riveted chin strap
riding the jaw, and hinge bolts at the corners. Twelve build-render
iterations on the face today, one raycast forensics session, one
debug render with the voids hidden that finally showed the muzzle
mass for what it was. The game glb inherits every piece of hardware.
The blend in the app carries it all, textures packed. He has the
face the file says he has.

## Commit 065 · THE HEAD, DONE (as this pipeline can do it)
Declared against the plate crop at 256 samples: the quilted face with
its seam runs and the sewn crown border; the mustard and navy ear
panels; the copper tally ring, riveted, barrel recessed, core glowing
with its own red spill; the gear-rosette button in its bronze socket;
the plate-sized felt nose; the lightproof mouth slot framed in aged
bronze bands with dense dark staples, machinery slats inside, the
riveted chin strap, hinge bolts at the corners; kinked straw whiskers,
burnt short left and wire-long right; the matted quarter-million-strand
coat crowding in from every side. The tone pass took the cloth to
chocolate, the staples to aged steel, the whiskers to dark straw, and
the face light down to a whisper so the key could model the face the
way the plate's light does. The game imported every piece and the
premiere soak held. What remains between this and the painted plate is
hand-sculpt territory — individually placed stitches, painted grime
strokes, fur groomed by brush — and the .blend is open on the bench
for exactly that. The pipeline's verdict stands: design in Cycles,
ship baked, and the head that hunts the halls is now the head in
the file.

## Commit 066 · THE HEAD, INTERROGATED (the "done" that wasn't)
The owner looked at 065's head and said not done, and the forensics
agreed. Raycast + albedo-emission debug renders found three buried
truths: the tally lens ring and the whole button-eye assembly were
sunk BEHIND the face cloth (the "orange crescent" was the ring's one
exposed edge; the "white shard" was the button poking through), the
face bake was chocolate all along (0.082 linear at the face texel) but
the 450W portrait rig was blasting it into AgX's grey shoulder, and
the head quilt panels were baking garbage-bright from their thin
shrinkwrap shells. The fixes: both eye assemblies moved proud of the
cloth like real sewn hardware (runtime tally seat moved to head-local
z 0.39 in rundown.gd/head_preview.gd to match), head patches excluded
from the bake keeping their true panel tones, the rig dimmed to
110/110/25/4W, and a plate-accurate tone pass — near-black melted
button with dead specular, charred socket rosette, small white-hot
core in a deep red iris in dark aged copper, muted burnt ear remnants,
darker lip bands, matte felt nose, straw whiskers. Side-by-side with
docs/canon/art/after-fire-chum-dossier.png this is finally the same
face: dark button eye left, burning camera eye right, black maw with
its staple bands and slats. Import 0 errors; fail-bot soak I01/I02/
I22/I06 all PASS. The bake multiplier saga (3.8→0.9) turned out to be
a red herring worth recording: measure the texel, not the render.

## Commit 067 · THE EARS, FULLY HD
The flat colored triangles are gone. Each ear is now a thick felt slab
remeshed at 7mm voxel with double displacement (ragged burn over woven
wrinkle, the left rougher and shorter), carrying: steel staples sewn
along both long edges and shrinkwrap-snapped onto the displaced felt
so none float; a solid tattered inner panel (mustard viewer-left, navy
viewer-right) remeshed with its own tatter and crinkle, embedded in
the front face; dark blanket stitches crossing the panel borders; a
charred melt cap on the singed left tip; and 1600 ribbon strands per
ear (game) / up to 1600 particle-hair guides (Cycles) crowding the
back and rim while a corrected bald mask keeps the sewn front face
readable. The ears got their own bake identity — EarFelt, darker tint,
tighter weave scale — after the shared BurntWool bake left them pale.
One casualty on the way: the first panel attempt shrinkwrapped a thin
plane onto the slab and collapsed into slivers (the giraffe artifact),
reconfirming the thin-shell-wrap lesson from the head patches; panels
are solid geometry now. New render shot 1b (chum_af_ears.png) frames
both ears for review. Import 0 errors; fail-bot soak I01/I02/I22/I06
all PASS.

## Commit 068 · THE BENCH LOOKS LIKE THE PUPPET NOW
The owner opened the .blend and saw a grey thornbush wearing an egg.
Fair. Fixes, in order of shame: the EarLTipChar cap (a smooth sphere
riding the singed tip like a balloon) is deleted — the ragged short
tip carries the singe alone; the ribbon fur is matted down (lift 0.22
to 0.11, narrower strands, deeper tip droop, ears at 2200 shorter
strands) so it reads as wet plush instead of thorns; the per-ear
staples and blanket ticks are joined into single EdgeStitches /
BlanketStitches objects, killing the parent-line spider web in the
viewport; and the .blend now saves with Material Preview shading and
relationship lines off, so File-Open shows the textured puppet, not
solid-grey geometry. EEVEE viewport-check render added to the loop
(renders/vp_ears_check.png) — the bench view is now part of what gets
verified, not just the Cycles glamour shots. Import 0 errors; fail
soak I06 PASS.

## Commit 069 · REAL ASSETS: THE FUR CARD PIPELINE
The owner asked the right question — why hand-paint strips when assets
exist? Answer built: tools/make_fur_cards.py renders REAL Cycles hair
tufts (four variants, char-to-rust, wispy separated tips) onto an
alpha atlas — an asset authored in the character's own palette. The
ribbon fur is gone; fur() now emits UV-mapped CARDS wearing that
atlas (alpha-clip, ~0.38x the old strand counts), the standard game
fur technique — so the same tufts read in Blender's viewport, in
EEVEE, and in Godot. The full particle-hair coat (all ten zones,
25k guides) now lives IN the .blend, grown post-bake, so opening the
file shows the actual coat; the beauty renderer detects it and skips
its own hair pass. Raw cloth (panels, patches, nose) got procedural
felt-grain bump. And the first real-renderer game capture
(head_preview --write-movie) caught a day-one bug: the Cycles
zero-emission maw exports to glTF with a white base color — the game
was rendering the lightproof void as a glowing cream mouth. The kit
now paints MawBlack surfaces unshaded absolute black. In-game check:
black maw, slats silhouetted, tufted coat. Soak I01/I02/I06 PASS.

## Commit 070 · THE REST OF THE HEAD, ON REUSED ASSETS
The owner's directive: finish the head, reuse the assets. Every piece
of this pass runs on machinery already on the bench. The nose is now
the plate's wide felt triangle, apex down, remeshed and near-black
with dead specular (its first draft rendered as a pale spike — the
raycast said the geometry was right and the material was lying). The
crown's bead spheres became staple stitches crossing the seam, joined
into one object, reusing the stitch pattern. Every alloy — bands,
rings, grille, staples, rods, brass — wears the Metal058A scan
box-projected and tint-multiplied via one scan_dress() function; the
leather grips wear Leather030 the same way, and both textures ride
into the glb. The dossier's detail 4 hand lever now stands inside the
maw (rod + leather grip), visible when the jaw hangs open. The felt
face plate grew 700 guides of short singed fuzz reusing the particle
-hair machinery, so the face reads as worn nap, not smooth CG cloth.
Whiskers thinned toward the tips. Verified in all three views — Cycles
beauty, EEVEE bench, and the real-renderer game capture. Import 0
errors; fail soak I01/I02/I06 PASS.

## Commit 071 · A REAL LENS FOR THE TALLY EYE
The owner said stop building what already exists — so the tally eye's
barrel is now an actual camera lens: Poly Haven's Camera_01 (CC0),
appended from tools/modelsrc (with its own .gdignore — the importer
trap claims no more victims), cut down in bmesh to the lens-barrel
faces alone, front glass deleted so the core burns openly, scaled
2.75x and seated inside the sewn copper mount, its 1K PBR textures
packed and riding into the glb. The donor's crisp white engraving got
a programmatic sooting (multiply toward char) — a fire-salvaged part
shouldn't read like a showroom shelf, and stray branding dies in the
same pass. The one Chum clarification, for the record: there is ONE
model, blend/chum_af.blend, and three honest views of it — Cycles
beauty, EEVEE bench, Godot capture — which light it very differently;
File > Revert in the app shows the current state. Verified in all
three; import 0 errors; fail soak I06 PASS. Credits updated.

## Commit 072 · THE MOUTH, REBUILT
The owner: "you really need to work on the mouth something terrible."
Correct. Post-mortem of the old mouth: a black blob void bulging past
the corners, bronze bricks chained along the lip, and pale pickets
floating mid-void. The rebuild: both voids tightened to hug the lip
line (one overshoot on the way — pulled too shallow, the void slipped
BEHIND the bulging muzzle cloth and the mouth interior rendered as
lit felt); continuous rolled-leather lip tubes (bevelled curves along
the maw parametric, burnt-dark Leather030 dress) replacing the box
chain — the first pass at r=0.021 rendered as grey garden hose,
halved to r=0.012 they read as stitched seams; 26 staples joined into
one object per lip, crossing the leather like zipper teeth; TEETH at
last — bone slats rooted IN the upper lip hanging into the dark,
uneven lengths, two knocked out, one snapped stub, four crooked lower
teeth rising from the jaw lip (parented to the jaw, so they ride the
bite); the grille dimmed to a third value (the metal-aging pass had
brightened it into cream pickets) and pushed deep as shadow
machinery. The in-game capture is the money shot: staple rows lining
both lips, teeth descending into black, the grin curling up into the
cheeks. Import 0 errors; fail soak I01/I02/I06 PASS.

## Commit 073 · UNREAL: FIRST LIGHT (unit 0.1)
The pivot is real. ue/Restoration exists — Lumen + virtual shadow maps
configured, Python and Movie Render Pipeline plugins on, Metal SM5,
generated dirs gitignored — and UnrealEditor-Cmd loaded it headless and
ran our Python: RESTORATION-PY-OK engine=5.8.0. The automation seam that
made the Godot loop work (script in, evidence out) exists in Unreal from
day one. The Godot game stays runnable as the reference spec per the
rewritten charter. Next: 0.2, the import/capture loop.

## Commit 074 · UNIT 0.2 · THE LOOP, CLOSED (with a zombie post-mortem)
One command now walks a mesh from Blender to an Unreal-rendered PNG:
tools/ue_loop.sh = export_ue.py (FBX, UE preset) → import_fbx.py
(headless commandlet, SM_/SK_ naming law enforced, scale contract
VERIFIED: the 1m calibration cube lands at exactly 100.0uu, written on
the wall as the pipeline doc demands) → stage_and_capture.py (look-dev
lights, bounds-framed camera, HighRes screenshot) run by a gated
Content/Python/init_unreal.py. That last piece exists because of the
week's best bug: -ExecCmds="py <path>" cannot survive a repo path
containing a space, so UE executed `py ` with nothing, never quit, and
idled for ten CPU-hours as a zombie. -ExecutePythonScript was no
better — it quits before deferred tick callbacks fire. The auto-run
init_unreal.py with an env-var gate dodges quoting entirely. Also this
session: the first scheduled cloud run correctly no-opped in a
toolless container, so the plan gained rule 0 and [CLOUD-OK] units —
remote sessions now extract CSVs instead of bowing out. Next: 0.3,
the head under Lumen — the first true acceptance baseline.

## Commit 075 · UNIT 0.3 · CHUM STANDS IN UNREAL (acceptance baseline set)
The whole puppet crossed the bridge: 78MB FBX out of the live blend
(jaw at rest per canon), 3.08m tall at exactly meters-times-100, every
bake on his body wired and rendering. The war stories are the unit's
real yield, all now structural fixes in the pipeline: packed images
are invisible to FBX (export unpacks all 64 maps to disk first); the
FBX importer silently reuses existing textureless materials on
re-import (fixup imports the PNGs directly and wires all 30 instances
from the Blender-written manifest); parent empties do not survive the
combine (export flattens with KEEP_TRANSFORM); auto-exposure
ghost-whites a dark scene (the capture rig now locks manual EV, as the
lighting bible commands); and iteration overwrote a keeper frame once
(accepted frames now archive to docs/telemetry/ue-baselines on the
spot). Two baselines stand: the daylight full-body (textures true) and
the dark locked-EV head portrait — burnt patchwork out of blackness,
the lens a pale blind eye — which is the frame every future Chum unit
must beat. Deltas honestly held for 1.8+: emissive tally, fur mottle
density, hardware tier per the realism bar.

## Commit 076 · UNIT 0.3b · THE SODIUM LIGHT COMES ON
tools/sodium_check.py is the pipeline doc's material gate, permanent
and headless: a near-monochrome sodium lamp, a neutral floor, and no
place for a material to hide behind hue. Two modes, because the first
contact sheet taught an immediate lesson: baked per-object materials
on generic shader balls read as black glass (empty bake margins), so
balls are for MASTERS and --subject puts the real asset under the
lamp. Chum's first subject pass is the honest audit: fur, lens,
mouth hardware, whiskers, ear panels PASS — they read as fiber,
machined metal, straw, felt. The belly, chest patches, hands and feet
FAIL as faceted clay and wax, which is exactly right: they are the
pre-head-era body, and their sodium verdicts are now filed against
units 1.1, 1.4 and 1.5. The gate is wired: every future material
pass ends under this lamp before it ships.

## Commit 077 · UNIT 0.5 · THE DATA CROSSES THE BRIDGE
tools/extract_data.py rebuilds the port kit's missing Data deliverable
from the source that outranks every document: 20 rooms, 20 doors with
their locked-reason strings word for word, 5 stations, 2 monitor
rigs, the 7-room demo whitelist, 32 tuning constants each tagged with
the file it lives in, and 714 text keys straight from the shipped
translations table. The extraction is deterministic and re-runnable,
so when the Godot spec moves, the CSVs move with one command. The
world can now be STAMPED FROM DATA in Unreal exactly as world_builder
stamps it in Godot — which is unit 0.6. (Landmarks have no single
source table; they spawn in code and port with the interactables.)
Two regex bugs caught by counting: the block matcher over-captured
DEMO_OPEN into STATIONS (17 ≠ 7 — arithmetic is a fine tripwire).

## Commit 078 · UNIT 0.4 · THE MEGASCANS DOOR IS OPEN
The owner signed the machine into Epic; the engine turns out to ship
all three access plugins (Fab, legacy Bridge, MegascansPlugin) and Fab
is now enabled in Restoration.uproject. ue/FAB-IMPORT.md is the
doctrine: the five-minute pull path, the Room-Bible-derived starter
shopping list (parquet, aged plaster, acoustic tile, soot decals, the
lot), the 2K quality law, the wear pass, and the credits ledger every
asset must sign. The one honest limit: Fab has no scripted-download
API — the pull itself is editor-UI, so it rides with Phase 3's first
room instead of blocking the port. Foundation phase rolls on: 0.6,
stamping the studio from the CSVs.

## Commit 079 · UNIT 0.6 · WGLD STANDS IN UNREAL
ue/pyscripts/build_greybox.py stamps the studio from Data/*.csv with
world_builder.gd's own wall-splitting algorithm ported line for line:
20 rooms, 119 wall segments, 7 door slabs (locked reasons floating as
world text, per the build order), 5 station markers, a practical per
room, PlayerStart in the REC ROOM. The top-down proof is the floor
plan made light: the dorm block, the spine, the library cross, the
studio wing — every gap where a door belongs. Two lessons for the
wall: commandlets cannot author levels (full editor via the
generalized UE_RUN_PYSCRIPT gate), and 'mobility' lives on components,
not actors. DefaultPawn's engine-defined bindings give boot-and-walk
free; true feel parity rides with the 0.8 pawn. Next: the twelve-feed
wall, in MASTER CONTROL where it belongs.

## Commit 080 · UNIT 0.6b · SPIKE 2: THE WALL HOLDS
The port brief called this the one technical question Godot never
answered on hardware, and the reason UE5 was being tested at all:
twelve simultaneous video feeds at 60fps. Answered: twelve
SceneCapture2D components, capture_every_frame, 256px targets, fed
from twelve canon rooms of the stamped greybox onto a 4x3 unlit
render-target wall standing in MASTER CONTROL where the canon puts
it. Six hundred and one PIE frames on the M1 Pro: 8.61ms average
(116 fps), 10.42ms at p95 (96 fps), against a 60fps pass line — and
PIE is HEAVIER than a packaged build, so the margin is conservative.
verdict=PASS, written into the record as the engine memo demands.
The spike rig is ephemeral by design; spike_wall.py resurrects it in
one command whenever the live monitor system (P3/P4) wants a
reference. Phase 0 remaining: 0.7 the Rundown tick-brain, 0.8
state/saves/loop, 0.9 the harness, 0.10 the parity gate.

## Commit 081 · UNIT 0.7 · THE BRAIN CROSSES, AND IT REMEMBERS ITS LINES
The Rundown is C++ now: a tick brain, no Behavior Tree, because the
grammar is the point. Ported verbatim from rundown.gd: the warn-once
latch, the strike with its savor widening after three, the
no-strike-thru-wall ray (I02's teeth), the BREAK relocation order
(heard noise outranks the cycle), the 2.2s door toll read from the
same Doors.csv the walls were stamped from, and a ReportNoise entry
point for the bus. The schedule is real: URestorationClock flips
ON AIR 50 / BREAK 18 on timers. Telemetry appends to
Saved/decision_log.txt in the parser's exact dialect. Three bugs paid
for the crossing: a bare AActor has no root so SetActorLocation
no-ops silently; GetPlayerPawn happily hands you the simulate
SpectatorPawn (he struck the camera, repeatedly, savoring it); and
tickable world subsystems do not tick in simulate worlds — timers do.
The verification run reads like the spec: stand at the anchor, warn
once at 6.1m, hold, and when the show goes to break — move. First
C++ compile of the project: 42 seconds, clean.

## Commit 082 · UNIT 0.8a · THE CONTRACT KEEPS ITS WORD IN C++
URestorationState stands: the GameInstance subsystem with the brain's
fields, the retake economy core (strikes, takes, dailies, full sheet
at four), the dead-room rectangle, and a v16 save whose round-trip
came back with its strikes intact. The AF layer crossed into the
Rundown: on the tally he shows and pours to the 1.2m loom; the log
speaks the jaw line; when the recording dies the taught cool runs
its four seconds; and the strike that follows is arithmetic, never
betrayal — then he is hidden until the next contract, and the log
falls silent, which is the correct sound. Porting taught twice more
why the code is the spec: the night gate belongs BELOW the AF layer
(my tidier order silently killed the whole branch), and Godot's
visible flag is load-bearing (without it the cool re-armed forever).
Both fixed by putting the lines back where rundown.gd always had
them. Remaining in 0.8b: paper, stations, the bench loop, Harriet's
freeze, the real day/night driver.

## Commit 083 · THE WATCHDOG EARNS ITS KEEP
The cloud session no-opped by design and, on its way out, audited the
tracker better than the tracker's own author: unit 0.6 was still
unticked (a scripted replace had no-opped silently — no assert), the
CLOUD-OK lane had evaporated the same way (one tag never applied, the
other erased in a rewrite), and six .pyc files were riding in git.
All three fixed: 0.6 ticked with its honest deferral note, the lane
restored with two real cloud units (the v16 save-schema transcription
feeding 0.8b, and the Phase 4 mechanic enumeration), __pycache__
ignored and untracked, and the plan gained rule 4b: tracker edits are
code — assert your anchors, preserve the tags. The arithmetic-tripwire
lesson from the CSV extractor, relearned in markdown.

## Commit 084 · UNIT 0.8b-1 · RITA WALKS, AND SHE WALKS CORRECTLY
ARitaCharacter is the port of player.gd with its constants carried
whole: 310uu walk on 1000uu of deliberate weight, the 2.6m reach ray,
and crouch per ruling c045 — toggle, 0.55x, the camera easing down
0.6m at exactly the 12-per-delta rate the GDScript lerps it.
ARestorationGameMode makes her the default body; the input map speaks
the controls doctrine (WASD, mouse, Ctrl and pad-B for the body verb,
E to ask the world questions). The self-driving feel test read back
the spec to the digit: walk 3.10, crouch 1.71, drop 0.60. One
dependency lesson (AIController lives in AIModule) and zero drama —
the pipeline is starting to feel like a pipeline. Next: 0.8b-2, the
loop around her — paper, the bench, the recording windows that make
the tally mean something, and the clock that makes night real.

## Commit 085 · UNIT 0.8b-spec · THE LOG, READ BACK IN FULL (cloud unit)
A cloud session, so per rule 0 the unit is text: the v16 transmitter
log transcribed whole into ue/PORT-NOTES-STATE.md. Fifty-five keys in
dict order with types, defaults, and exactly how load_log coerces
each one (defaults ARE the migration — there is no upgrade code, and
there must not be); the eighteen live fields that never touch the
file; the eight saved fields that survive a new game on purpose; all
twenty signals with who fires them and who listens (rundown hears
night_changed and noise_event — the brain's two ears); the settings.cfg
contract; what the Tape 1 demo strips. Then the part that earns the
unit: the delta list against the 0.8a C++ skeleton. Seven fields have
the wrong SHAPE — paper is a per-station map, not an int; signatures
is a load-bearing array (respawn reads its last entry), not a count;
seance_wear is a float with a 70.0 threshold; Leland's answers dedupe
by frame — plus thirty-two keys missing outright and two wrong
defaults (mode boots MATINEE, tape boots 0). Verification for a text
unit is an assert script, not an eye: 55 == 55 in order, every key
read back by load_log, 20 == 20 signals, 72 of 72 public vars
documented, persist set 8 == 8. No renders this session (no Blender,
no Unreal, no Desktop here) — Desktop copies skipped, honestly.
Repo green on entry (HEAD == origin/main f79877c) and on exit.

## Commit 086 · UNIT 0.8b-2 · THE BENCH KEEPS NO HALF-TRUTHS
The game's core verb runs in C++: ABenchCapture, the first
IRestorationInteractable, holds a 12-second capture in forced real
time and drives State->bRecording — which is the switch that ARMS the
tally contract, so the bench and the hunter are now wired to the same
truth. The two-bench trial proved both halves in one simulate: a still
Rita rode it to TAPE 1 · A CLEAN SIGNAL; a walking Rita crossed the
4-metre tether and got CAPTURE ABORTED · the take is lost. Rita's
reach ray casts the interface and speaks the prompt before it acts.
One infrastructure lesson: the decision log picked up a UTF-16 byte
somewhere and crashed the Python reader mid-parse; all telemetry now
writes ForceUTF8WithoutBOM. The cloud lane's PR #7 merged the same
day, and its §6 delta audit — 7 shape mismatches and 32 missing keys
against my own 0.8a SaveGame — is now unit 0.8b-3, a worklist I did
not have to write myself. Two hands, one main.

## Commit 087 · UNIT 0.8b-3 · THE LOG SPEAKS FULL v16
The cloud lane audited my 0.8a save and found it half-shaped; this
unit finishes it. URestorationSaveGame now carries all fifty-five
keys of _save_dict in order, each with the type the spec demands — the
paper as a per-station map seeded three-per, the signatures and
captures and casualties as real struct arrays (respawn_point reads the
last signature's station, so a count would have been a latent bug),
seance wear as the float its 70.0 threshold needs, Leland's answers as
the int array that dedupes frames. Save and load copy the whole set,
paper merging so keys absent from a file survive. And Strike() clamps
lost items at seven, not six — the off-by-one that would have kept the
LOUPE from ever becoming the New Game+ relic, filed by the cloud as
9.x and now closed. The round-trip test set a value of every container
kind, saved, clobbered every field, loaded, and compared: match=1.
The two-handed loop's full arc in one unit — cloud found it, Mac fixed
it, and the save that carries a whole playthrough now round-trips
clean. §6's gameplay-function tail is 0.8b-4.

## Commit 088 · UNIT 0.8b-4 · THE CONNECTIVE TISSUE
The state functions that stitch the loop together are C++ now, ported
line for line. SetNight is the day/night driver: morning advances the
day, caps the tape at five, and calls the prototype complete at day
three — the run's whole spine in nine lines. The paper economy signs
and decrements per station, with the Harriet-slip one-shot that lets a
hand not yours close the log. Stations register with the (0, 0.5, 1.2)
Godot offset mapped faithfully to UE's (0, 1.2, 0.5) metres, and the
respawn resolved to exactly (700, -2980, 50) — the coordinate contract
holding to the centimetre. And the receipt the world keeps: signing
the log broadcasts a noise at your respawn, the hunter's brain records
it, and it relocates toward you on the next break — SignFinish ->
OnNoise -> ReportNoise, the same deferred relocation rundown.gd
performs. One simulate proved all of it: two mornings, the paper
falling 3 to 2, the respawn exact, the documents and keys filed. The
presentation and NPC half — the retake screen, Harriet's freeze,
screening and assist — is 0.8b-5.

## Commit 089 · UNIT 0.8b-5a · HARRIET FREEZES INSIDE THE COLOR CHANGE
The schedule is real, and Harriet is its proof. AHarriet sways gently
while the building is ON AIR — roll on a slow sine, sin(t·0.9) — and
the instant the break comes she FREEZES mid-motion, holding exactly
where the cue left her, resuming only on the return signal. The test
caught her in the act: swaying from 0.835 to 1.791 degrees of roll
under ON AIR, then the break landing and freezing her at 1.791, held
to the fourth decimal a full second later. swaying=1 held=1. Her cup
rises by the day, and her prompt tells the phase. This is LAW 6 wearing
a cardigan — the one member of the club who visibly obeys the same
clock the hunter does, so the player learns to read the break in her
stillness. Her H1/H2 casualty sequences are UI-heavy and wait for the
presentation half, alongside the retake screen and screening.

## Commit 090 · UNIT 0.9a · THE SAME PARSER, THE SAME VERDICT
The migration map promised the harness would be "the parser as a test
step reading the identical log files," and now it is. tools/
invariant_parser.py carries the coverage rules of invariant_parser.gd
line for line — a STRIKE with no WARN before it fails I01, a STRIKE
marked THRU-WALL fails I02, relocations toward heard noise are counted
for I22 — and exits zero only when the sheet is clean. The scenario
lives in the Rundown itself: hold the tagged target at six metres,
pull it to strike range with a clear line of sight, let the ordinary
hunt logic speak. It spoke: WARN at 6.1, STRIKE at 1.8, and the
warn-latch reset re-warning before the next strike, exactly as
rundown.gd orders the grammar. The parser read the log the brain
wrote and ruled PASS, PASS. Two bugs turned up, both in the harness
and neither in the hunter: a target spawned STATIC ignores every
SetActorLocation (so it sat at warn range forever, a silent no-op
worth remembering), and one too many ".." in the parser path. Honest
edges left as boxes: I22 was counted, not exercised — no break falls
inside five seconds — and a positive-only run does not prove the
parser catches a violation. 0.9b puts a wall between them and demands
a FAIL.

## Commit 091 · UNIT 0.9b · A WALL, AND THE PARSER SAYS NO
A harness that only ever passes proves nothing, so this unit built the
case for the prosecution. First on paper: three synthetic logs fed to
the parser — a strike marked THRU-WALL failed I02, a strike with no
warning before it failed I01, and a clean pair passed — each with the
right exit code, so the detector detects. Then in the building: a
three-metre wall spawned squarely between the hunter's anchor and the
prey pulled to strike range. The brain's own raycast hit it, and the
brain did what rundown.gd does at line 314 — it struck anyway and
wrote THRU-WALL into the log, because marking is the canon and the
soak is the judge. The parser read those two marked strikes and ruled
I02 FAIL x2, exit 1, while I01 stayed PASS because the warn-latch
still spoke before each strike. So the invariant machinery is now
proven from both sides: it lets a clean run through and it convicts a
dirty one. The wall scenario stays in the tree as the standing
negative fixture — the test you run when you suspect the harness has
gone soft. 0.9c gives I22 a real break to relocate through.

## Commit 092 · UNIT 0.9c · TOWARD THE NOISE, NOT THE NEXT IN LINE
I22 had been a count that could never fail, so it was not yet a
finding. Now the invariant fixture makes the brain earn it: at 3.5s a
noise lands beside PATCH BAY and the break is invoked directly —
OnPhaseChanged(false), the real 50-second flip being outside a 5-
second window — and the relocation grammar answers "RELOCATE toward
heard noise -> segment 2." The segment was the whole point of the
design. From segment 0 a plain cycle steps to 1; only the nearest-
anchor search reaches 2. The first pass had used STUDIO A, and its
"-> segment 1" was true but could not tell attribution from order —
so it was moved rather than trusted. The parser now rules all three
coverage invariants from one five-second simulate: I01 PASS, I02
PASS, I22 PASS with one attributed. What remains of the harness is
the cast of bots and I06, the finale that must fail forward.

## Commit 093 · UNIT 0.9d · THE SHEET FILLS, THE RUN ENDS, THE LOOP GOES ON
The last harness question was the one that matters most to a horror
game: what happens when the player simply loses. A fail-bot — the
target pinned in the hunter's face for fifteen seconds — was struck
to a full sheet, and the log read like the design document: warn,
strike, warn, strike, and at the third strike the savor rule woke and
signed its name on the next pair, exactly as canon orders it. On the
fourth strike: RUN ENDED take=4, fail forward. And then — the proof
that counts — a fresh warn and strike with no savor on them, because
the sheet had reset and the schedule had resumed. No soft-lock. The
parser's new UE-R1 line ruled it PASS live and convicted a synthetic
four-strikes-no-ending as a soft-lock. The parser also learned the
liveness and premiere sections verbatim, and here the ledger keeps
its receipts honestly: canonical I06 measures the finale's club
auto-fixing an incident within 41 seconds, and I07 the cascade's
liveness — neither system exists in Unreal yet, so both report N/A
rather than a green they did not earn. They go live when Phase 4 and
5 port them. The harness is complete for everything Phase 0 can
exercise. What stands between here and Phase 1 is the gate.

## Commit 094 · GATE 0.10 · THE PACKAGE, NOT THE VERDICT
Phase 0 ends where the plan said it would: at a gate the loop is not
allowed to open. So the loop assembled the case and stopped. Every one
of the nine Phase-0 fixtures was re-run at HEAD in a single pass and
its verbatim lines kept; the parity slice was mapped clause by clause
to what proves it; the eleven laws were audited one by one and marked
EXERCISED, BY ABSENCE or NOT YET — with LAW 9, access, flagged in red
because nothing in the port yet honors it. Then the capture. The first
frame was a lit wall: the camera sat a metre outside the room, and the
rule that says look before you ship earned its keep. The second, from
inside, showed the After-Fire puppet standing nearly wall-height at his
own anchor, the S1 station beside him and the FIRE CORRIDOR's "SEALED ·
reopens for the anniversary (Tape 4)" hanging at the door — the stamped
data made visible around him. And it showed, honestly, a body that
still reads as faceted clay beneath a head that reads finished: the
sodium gate's finding, now in a room, which is the exact shape of
Phase 1. The tracker notes the package and leaves the box unticked.
The gate is the owner's. Meanwhile the lanes opened: a cloud routine
on an eighteen-unit backlog with a claim check, four prep agents
writing Phase 1's brief and rig spec, the access spec, and the first
five room briefs. The build no longer waits on one pair of hands.

## Commit 095 · THE SUBAGENT LANE'S FIRST FOUR
While the gate waited, four agents wrote the papers the next phases
will build from, in parallel, one file each, none touching the
tracker. The Phase 1 brief verified its asset ids live against the
Poly Haven and AmbientCG APIs — wool bouclé, hessian, teddy curl,
leather, rusted metal, a vintage transceiver — and named the realism
risk without flinching: the coat still reads as a plush toy, and canon
wants a fused, scorched, stitched quilt. The rig spec tabled every
bone and every shot the brain can call, locked the bell so it can
never ring, and hands the jaw to the lever and the lever to the hand.
The access spec turned LAW 9 from a red flag into six named classes
with tests, and found that canon's "deferral rule" is the achievement
deferral, not a scare's. The room briefs converted five rooms into
uu-exact dressing orders with a template for the other fifteen — and
found that canon never states a single EV, kelvin or candela, that the
reference code browns the night down where the bible turns it off,
and that no room has a window the data can draw. Two of the four,
working blind to each other, flagged the same thing: the puppet is
authored at 2.6 m, imported at 3.08, and canon wants 3.35 with the eye
at three metres. The gate doc now asks for that ruling instead of
asserting a number. Fifty-odd OPENs in all, every one cited, none
invented. That is what the lane is for: the owner rules once, and the
build never guesses.
