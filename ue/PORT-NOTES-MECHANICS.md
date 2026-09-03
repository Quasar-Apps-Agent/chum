# PORT NOTES · MECHANICS — the Phase 4 register (unit 4.0, CLOUD-OK)

**What this is.** Every gameplay mechanic the canon docs and the reference
implementation carry, enumerated ONCE, keyed to the Phase 4 boxes in
`PROGRESS.md` (4.1 … 4.34). Each entry names the Godot spec (the code is the
intent — PORT-BRIEF law), the state it reads and writes (per
`PORT-NOTES-STATE.md`), its UE home (per `UE5-MIGRATION-MAP.md`), the laws
and invariants it must keep, the QA lines that accept it, and the four-step
unit shape the plan §5 prescribes: **port → diegetic feedback → fail-forward
integration → automation test**. Where the register and the GDScript
disagree, fix the register.

**How it was made.** Read in full: THE-LAWS, BUILD-ORDER, PORT-BRIEF, the
migration map, the design doc, the game master, the walkthrough/endings doc,
the player routing doc, the casualty ledger, the after-fire canon, the
reaction matrix, the invariant suite (I01–I31), the QA regression script
(QA-01–QA-61), the playtest protocol (P1–P26, V1–V7), the achievements design
(A01–A28), the demo cut plan, the controls map, the accessibility matrix, the
gap audit rulings, the dread doctrine, the object taxonomy, the props packet
(D01–D10) — and every header, constant, signal and public function of the 73
scripts in `scripts/`, plus `world_builder.gd`'s spawn list and
`project.godot`'s input map. `tools/verify_phase4.py` asserts the coverage
tables in §C against the live sources (VERIFY-OK is the unit's evidence).

**Ordering.** Boxes follow BUILD-ORDER: P4 (hunter & nights remainder) →
P5 (story gates & finale) → P6 (meta & modes). What Phase 0 already owns is
NOT re-boxed (0.7 brain, 0.8a AF layer + state core, 0.8b-1 Rita, 0.8b-2
bench, 0.8b-3 save parity, 0.8b-4 P3 remainder, 0.9 harness) — §C maps
those scripts to their Phase 0 boxes so nothing falls between the phases.

**Standing rules for every 4.x unit** (do not repeat them per entry):
- Numbers are canon: every constant in `Data/Timings.csv` and in the spec
  script ports verbatim; the register cites the ones the unit owns.
- Telemetry formats do not change (`coverage_log`, `liveness_log`,
  `premiere_log`, `decision_log`); the 0.9 parser must read UE output.
- Text comes from `Data/GameText.csv` (StringTable keys = source strings).
- Diegetic feedback means a world object or a caption, never a floating
  HUD element (design doc Part III); captions carry source tags.
- Fail-forward means no soft-lock: every gate has a re-entry, every refusal
  states its reason, every timed thing has a guarantee (I06's shape).
- Test means a functional-test map or Gauntlet step the 0.9 harness runs,
  reading the same logs; a text unit's test is an assert script.
- CANON-ONLY entries (no Godot code exists) are marked; there the docs are
  the spec and QA lines are the acceptance, and the port must not invent.

---

## A · THE BOXES

### P4 · THE HUNTER AND NIGHTS (remainder after 0.7 / 0.8a)

### 4.1 · Frame Discipline: camera cones and the lit hide
SPEC `monitor_rig.gd` (a camera somewhere else rendered live onto a wall
set; tally, kill, re-patch, lockdown `sync_to`), `rundown.gd`'s visible/
on-camera gate (ported in 0.8a), `world_builder._spawn_monitor` from
`Data/Monitors.csv`. STATE `recording` (0.8b-2), rig liveness (live, not
saved). UE HOME `USceneCaptureComponent2D` → `UTextureRenderTarget2D` per
feed onto unlit screen materials (0.6b proved twelve at 116 fps); a camera
cone volume per rig that the Rundown queries before any strike. LAWS Law 1
ON CAMERA IS SAFE, Law 10 the tally contract (the eye's light and the
contract are the same fact), Law 11 the safe hide is the lit one; I05 on
camera is safe, I23 no strike while lit. ACCEPTS QA-14 (cone prevents the
strike; patchbay revive), QA-35 (eye red ONLY while a capture runs).
FEEDBACK tally lamps shape-coded not color-only (accessibility matrix),
the REC line + countdown pair. FAIL-FORWARD a killed camera leaves the
cone dark, never the map unreadable; revive at the patchbay (4.2). TEST
soak bot parked in a cone with strikes forced → zero STRIKE lines; QA-35
eye-state probe scripted.

### 4.2 · The patchbay and the amperage budget
SPEC `patchbay_console.gd` (routing v0: one amperage budget, two circuits,
something is always dark), `world_builder._spawn_patchbay_circuits`
(CTL light, hall light, console) and `_wire_cascade_console`. STATE
circuit states (live), `cascade_done` (saved). UE HOME an interactable
actor (`IRestorationInteractable`) driving light actors + rig liveness;
the breaker order is data. LAWS Law 6 the schedule is real (holds bind);
I04 window holds yield only to the cascade. ACCEPTS QA-14 (revive half),
QA-20 (restore order refusal with reason). FEEDBACK the polished breaker
(taxonomy: affordance is wear), circuit labels as world text, a caption
per throw. FAIL-FORWARD power overdraw is never a fail condition
(walkthrough V-B: protection, not health). TEST functional map: kill a
rig, throw the circuit, assert rig live; the 4.6 cascade test reuses it.

### 4.3 · Noise, the dead room, the felt door
SPEC `noise_tracker.gd` (player footstep noise at night → `GameState.noise`
→ `noise_event`), `rundown._on_noise` (0.7's ReportNoise), the dead-room
rectangle `in_dead_room` (0.8a) and the felt-door hold `DEADROOM_DOOR`,
`world_builder._spawn_dead_room_felt`. STATE `dead_room_seen` (saved;
first-entry radio toast + `[NO ECHO]`). UE HOME AIPerception hearing or the
custom noise delegate already in ARundown; a dead-room volume that drops
noise events born inside it. LAWS Law 11 the single dark hide; I22 heard
noise is attributable (0.7, telemetered), I25 deaf to the dead room.
ACCEPTS QA-13 (relocates within 12 s; It-changed-direction line once per
run → A08 YOU WERE NOT QUIET), QA-38 (inside noise registers nowhere; he
tracks to the felt door, holds, says his line once; first entry gives the
radio toast and `[NO ECHO]`). FEEDBACK the caption pair, the room's
silence as absence of room tone (5.1). FAIL-FORWARD he holds at the door;
the room never traps (door opens from inside always). TEST bot signs and
slams inside the bounds; assert his target never moves (I25); the I22 line
count from the 0.9 parser.

### 4.4 · Night trip (first blood, once per save)
SPEC `night_trip.gd` (night one, ~20 s: a breaker lets go, a feed dies,
something behind you knows the closing song; once per save),
`world_builder._spawn_event_wave`. STATE `night_trip_done` (saved). UE HOME
a level-scripted actor firing on `night_changed(true)` with the flag
guard. LAWS Law 2 one startle (this is dread, not a lunge — no sting);
I15 the silence ledger. ACCEPTS QA-19 (fires once ever), P9. FEEDBACK the
feed dying on the monitor, the caption for the hummed bar. FAIL-FORWARD
the breaker beat cannot kill; the route home stays lit by the trip's own
end. TEST fresh save soak: exactly one trip line in the log across two
nights and a relaunch.

### 4.5 · The Floor Manager
SPEC `floor_manager.gd` (nights, on air, at the stack's end; one hand
rises; look inside 9 m → hold still 3 s or the take is spoiled; assist-hold
passes; absent during breaks and the premiere; spoken inventory: nothing;
`mark_read("D08")` the run sheet). STATE `fm_seen`-class flags per the
schema; `signals_known` (4.13). UE HOME a character actor with a
freeze-check component reading the clock; the signal vocabulary is an
anim set (2.9) driven by the same enum. LAWS Law 6 (he obeys breaks);
I15 he is never heard moving; Law 5 (he has no voice). ACCEPTS QA-19
(watch fails on movement, passes on assist-hold), P8; the F2 inversion
(stillness draws his point) belongs to 4.24c. FEEDBACK hands only: the
point is the UI; the caption names the signal. FAIL-FORWARD a spoiled
take is a retake, never a death by itself. TEST functional map: bot looks
at him and moves → spoiled line; assist-hold → pass line; assert no FM
spawn during BREAK or premiere.

### 4.6 · The cascade and liveness (Night 4+)
SPEC `cascade.gd` (trip, spread, ordered restoration C then B, circuit F
which cannot be de-energized), `liveness_check.gd` (during the cascade the
panel is always reachable; window holds waived; OK cadence every 5 s to
`liveness_log.txt`; VIOLATION on breach). STATE `cascade_done`,
`cascade_active` (live). UE HOME two actors as in Godot; the log writer is
an `FFileHelper` append in the parser's dialect. LAWS Law 6; I04 window
holds obey the clock and yield only to the cascade; I07 cascade liveness.
ACCEPTS QA-20 (C then B; out of order refuses with "B before C"; waived
holds during), A15 ORDER MATTERS; the GET VESS option at the dead panel is
4.24c. FEEDBACK panel events as captions, the stage end dropping dark.
FAIL-FORWARD by construction: liveness is the invariant. TEST the 0.9
harness's I07 step with doors deliberately closed; assert OK cadence and
zero VIOLATION lines.

### 4.7 · The Coverage Director
SPEC `coverage_director.gd` (profiles the player at night from behavior —
AUDIENCE / CHECKER / SPRINTER / HIDER — never from menus; append-only
`coverage_log.txt`; burning dailies resets the read). STATE
`coverage_label`, counters (saved per the schema). UE HOME a
`UWorldSubsystem`; counters in the SaveGame; the log append unchanged.
LAWS I21 deterministic and explainable (every blocking decision carries a
reason string). ACCEPTS V5 director reads earned; P5 (burn → binder shows
AUDIENCE). Blocking VARIANTS per scare (game master Appendix A, the
poisoned-well once-per-run rule) are content for 4.ENCOUNTERS; this unit
is the profiler and the reason strings. FEEDBACK the binder's morning read
line (4.32). FAIL-FORWARD the profile only re-blocks, never adds kills.
TEST input-replay diff (Spike 5): identical inputs → identical profile;
grep that every RELOCATE/blocking line carries a reason.

### 4.8 · The casting sheet, the dresser and the run's end
SPEC `casting_sheet_prop.gd` (the death counter as a physical object on the
Studio A wall), `dresser.gd` (seven items in `ITEM_ORDER`, one leaves per
capture, the loupe last), `GameState.strike()` (0.8a) and `run_ended`,
`hud._on_run_ended` (NEXT WEEK'S EPISODE · STARRING RITA IVORI, then
title, no credits), modes MATINEE / LATE_NIGHT / ONE_TAKE. STATE
`strikes`, `items_lost`, `run_complete`, `mode`. UE HOME sheet + dresser
as interactables reading state; the run-end card in UMG. LAWS I16 item
loss is ordered and bounded (losses persist through run end), I17 sheet
retirement is honest (zeroes strikes, keeps losses, mints no daily).
ACCEPTS QA-07 (loupe lost last of seven), QA-08 (run death → card → title,
no credits), P3, P4 (One Take); A18 NEXT WEEK'S EPISODE, A19 EMPTY DRAWER.
FEEDBACK the sheet is readable at the wall; the dresser's empty slots.
FAIL-FORWARD CONTINUE from the last signed log always resumes sane.
TEST full-run matrix step: force four strikes → assert sheet full, items
order, run_ended once, strikes zeroed after, losses kept.

### 4.9 · Burn Your Dailies
SPEC `dailies_manager.gd` (canisters in library `SLOTS`: existing on load,
new per capture), `dailies_canister.gd` (labeled SCENE/TAKE; single-carry),
`degausser.gd` (the climate room's coil: burning a daily takes her name off
the line and resets the Director read), `GameState.pick_daily/burn_daily`,
signals `daily_added/daily_burned`, `world_builder._spawn_burn_loop`.
STATE `dailies`, `carried_daily`. UE HOME a spawner actor + two
interactables; the coil is a hero interactable of CLIMATE (taxonomy:
one per room). LAWS I09 abort never costs a daily (0.8b-2 already refuses
the mint on abort — re-assert here). ACCEPTS P5 (mint two, carry one,
single-carry rule, burn resets the read), P2. FEEDBACK the canister label
as world text, the coil's stripe, the fade on the sheet. FAIL-FORWARD a
canister is optional forever; nothing gates on burning. TEST functional
map: capture → assert one canister; burn → assert strikes−1 and
coverage_label AUDIENCE; abort → assert zero canisters.

### 4.10 · Doors, keys and window holds
SPEC `door.gd` (a hinged door: locks state their reasons, keys satisfy
them, window-bound doors honor the grammar and move only during the
BREAK), `key_item.gd` (taking a key is remembered: EDITH, TRAINING, QUIET
ROOM), `GameState.has_key/take_key`, `Data/Doors.csv` (locked reasons
already stamped as world text in 0.6). STATE `keys` (saved). UE HOME
`ACompoundDoor` (interactable) built FROM Doors.csv by the 0.6 stamper;
keys as pickups. LAWS I08 every locked door states its reason (data +
manual sweep for empty strings), I04 holds obey the clock; Law 6.
ACCEPTS QA-10 (holds honored except during cascade; clock and hum agree),
P15 extension (door sweep); A16 THE LONG WAY AROUND (the QUIET ROOM key).
FEEDBACK the reason on the door, the hold as a refusal line with the
clock's state. FAIL-FORWARD every locked door is openable by data (key or
condition), never by chance; the 2.2 s fold toll (0.7) is his cost, not
the player's. TEST sweep every Doors.csv row: locked rows have non-empty
reasons; window-bound rows refuse during ON AIR and open during BREAK.

### P5 · STORY GATES AND FINALE

### 4.11 · Readables and the Three Reads
SPEC `readable_prop.gd` (a found document, physically in the world, per
the props packet), `GameState.mark_read` ("of 10"), `world_builder.
_spawn_readables` (D02 D04 D05 D09 D10 D11 spawned as props; D01 via the
seance reel box, D03 the ledger, D06 Harriet's note, D07 Vess's binder, D08
the run sheet are read by their own interactables). STATE `read_props`.
UE HOME `AReadableProp` + the binder's document view (4.32); bodies from
the props packet through the StringTable. LAWS lore architecture: the
game never explains, it corroborates; naming a ledger truth in text is S0;
the Peak dossier D11 appears only after first sighting. ACCEPTS A26 FULL
ACCESSION (D01–D10; D11 extra credit by ruling); QA-59 (ambient ledger
audit) and QA-55 (prompt discipline) are Phase 3's per-room sweep — this
unit owns the HANDLED tier only. FEEDBACK the prompt glyphs the real
binding; READ · filed to memory toast. FAIL-FORWARD re-reads free; nothing
gates on reading except A26. TEST assert 10 distinct ids reachable and
`mark_read` idempotent.

### 4.12 · The credit chain (Vess)
SPEC `credit_entry.gd` (a margin in the accession ledger: PER V. KEYS →
`vess_credited`), `vess_binder.gd` (his research, door ajar: one true
insight, one confident error; `mark_read("D07")`), `vess.gd` (Vess at the
shrine wall; lines keyed to whether anyone wrote his name). STATE
`vess_credited`, `vess_insight_used`. UE HOME three interactables; the
credit is a state write with a caption. LAWS the reaction matrix (V-R1,
V-R2, M-R6 queue in 4.WEB); the casualty preconditions for V1/V2 (4.24c)
are set HERE and nowhere else. ACCEPTS A11 PER V. KEYS, P13 (skip the
binder → blackout retake variant; credit him → credited line). FEEDBACK
the margin reprints as a credit; his line changes. FAIL-FORWARD the
window closes at lockdown (routing: Conduct Ledger's Vess entries close
Day 4) — after that the ledger is fixed, honestly. TEST two-save assert:
credited vs not → `finale_breaker` variant line differs (4.26b).

### 4.13 · The film cabinet and the seventh signal
SPEC `film_cabinet.gd` (the instructional film: SIX signals YOU'RE ON /
CUT / STRETCH / WRAP IT UP / THIRTY SECONDS / ON TIME, taught once; TRAINING
key), `harriet_note.gd` (folded paper on Harriet's chair: the SEVENTH, HOLD
YOUR APPLAUSE; `mark_read("D06")`), `GameState.add_show_signal`,
`world_builder._spawn_film_and_note`. STATE `signals_known`. UE HOME two
interactables + a film playback on the bench monitor (4.16's stack).
LAWS generations gate understanding never endings (design doc §11); the
seventh is the only warning the unscripted seek ever gives (SCARE 8
blocking split). ACCEPTS A07 HOLD YOUR APPLAUSE; QA-41's clause (the
seventh is unlearnable if Harriet died before her card was found — 4.24b
enforces, this unit exposes the gate). FEEDBACK the six as captions during
the film; the card's pencil text. FAIL-FORWARD the film is re-watchable;
the note is optional (G2). TEST assert `signals_known` = 6 after the film,
7 after the note, and the note absent when `is_dead("HARRIET")` pre-card.

### 4.14 · The presigned page (the save scare, singular)
SPEC `GameState.mark_presigned` (Day 2+, S4 with zero paper: the page
appears and saves free, once; three beats; signature listed with
`presigned: true`), the S4 station branch in `log_station.gd` (0.8b-4
ports the station; this unit ports the branch). STATE `presigned_seen`,
`signatures`. UE HOME a branch in the station interactable + a
three-caption sequence. LAWS I10 the presigned page costs no paper;
Law 8 this is diegetic content, NOT the interface lie (walkthrough V:
no save is ever falsified by the interface). ACCEPTS QA-21, P6; A09
TOMORROW'S DATE (hidden). FEEDBACK the page itself, her handwriting,
tomorrow's date; caption per beat. FAIL-FORWARD it is a free save;
nothing can be lost by it. TEST save diff: signature added, paper
unchanged, flag set, never re-fires.

### 4.15 · The impossible crate and the frame-seance
SPEC `impossible_crate.gd` (Tape 4's delivery at the front door; opening
it unlocks the seance reel), `seance_dock.gd` (frame stepping Z/X through
the impossible tape, `MAX_FRAME` 40, ANSWERS at frames 7/14/21/28/35,
`add_wear(1.5)` per pass, the temp generation ladder `wear/30` on the
bench TV, the L1 offer when ≥5 answers AND `seance_wear > 70`, `mark_read
("D01")`), `frame_sequence.gd` (one procedurally built frame per index,
seeded per frame, `W`×`H` = 320×240 — the exact pipeline real footage
drops into). STATE `crate_opened`, `leland_answers`, `seance_wear` (float,
burns in across reload — the burn-in rule). UE HOME `UTexture2D::
CreateTransient` filled per index with the same seeded generator, or an
image-sequence Media Source stepped by frame; the wear ladder is a
material parameter; actions `frame_back` / `frame_fwd`. LAWS I19 the
seance gates on the crate; I20 the same frame is always the same frame;
generations: scrub = G1 at wear cost. ACCEPTS QA-22 (crate before seance
refuses; after: wear degrades generations per answer), QA-50 (grief
variants: frame 14 PAUSED PROPERLY with Harriet dead, frame 28 SHE'S HERE
NOW with Merle dead; TRANSITION UNRESOLVED on every Harriet reading), P16
(the knob returns to 3RD GEN not MASTER), V6 (the crop); A14 I'VE READ THE
ENDING. FEEDBACK `SEANCE · FRAME n · WEAR x%` on the capture status line;
the pad's text changing between stepped frames (SCARE 7). FAIL-FORWARD
answers persist; wear is the only price and it is bounded by MAX_FRAME
passes the player chooses. TEST capture frame 14 twice across relaunches
and diff (I20); assert the five answer frames; assert the L1 offer gate.

### 4.16 · The tape stage, the CRT stack, the gen knob, TBC and photo-safe
SPEC `tape_stage.gd` (a tiny Gladhouse in a viewport: Tape 1's timeline
ending on the approach, the hold, the lunge — `lunge_happened`; knobs V2:
approach 1.35, hold 0.78→0.12, lunge scale 1.45), `bench_tv.gd` (the bench
monitor behind the artifact shader; the slate lies about the generation,
the scope does not; `set_temp_generation`), `gen_knob.gd` (MASTER / 1ST
DUB / 3RD GEN), `shaders/crt_tape.gdshader` (chroma offset, scanline,
noise, tracking band, head-switch, dot crawl, vignette; params
`generation`, `tbc_on`, `photo_safe`), `GameState.set_tbc/set_photo_safe`,
actions `toggle_tbc` (T) and `photo_safe` (P). STATE `tbc_enabled`,
`photo_safe`, `generation`. UE HOME the diorama as a small sublevel
captured by its own SceneCapture; the Scare 1 timeline as a Level
Sequence with the lunge as a one-frame track; the shader as a Material
Function stack on the RT with scalar parameters of the SAME NAMES driven
from a Material Parameter Collection. LAWS Law 2 ONE STARTLE (the in-tape
lunge is the game's single jump scare); I14; the accessibility matrix
(photosensitivity IS the TBC; the flicker/grain slider in UE is additive
to, never a replacement for, the in-world device); Law 9 access is canon.
ACCEPTS QA-06 (bars play after the take — 0.8b-2 owns the loop, this owns
the picture), V2 THE HOLD, V3 artifact loudness at gen 0, V4 TBC feel;
A03 THE SCOPE READS MASTER. FEEDBACK the picture obeys the knob, the scope
does not; the TBC state on the HUD is the device's lamp. FAIL-FORWARD the
lunge is the one startle and it is disclosable in the booth (4.31).
TEST capture the last 3.2 s of the Tape 1 timeline as a frame sequence
(≥8 frames) and review the hold; assert the MPC parameter names.

### 4.17 · The fire tape
SPEC `fire_tape_pickup.gd` (the 1977 reel in Craik's cage), `fire_tape_dock
.gd` (the forced watch; no sting anywhere in it; sets `af_active`; the wake
toast once; the M1 second-viewing offer Day 3+ → 4.24b). STATE
`fire_tape_held`, `fire_tape_watched`, `af_active` (persists), `wake_bleed`
once per save. UE HOME a pickup + a bench-dock interactable running a
Level Sequence on the bench RT; the af flag flips the ARundown into the AF
body (0.8a already branches on it). LAWS Law 2 and I14 (no sting), I15
(the fire tape carries no sting — asset-review gate), Law 3 is NOT this
(the once-ever sight is 4.20); the audio law's wake bleed exactly once
(QA-54 clause). ACCEPTS QA-23 (forced watch, no sting, flag marked), QA-33
(wake toast once; `af_active` persists across save/load); A13 THE
UNFINISHED LINE. FEEDBACK the pan with no operator; bars before any card;
the reel's weight line. FAIL-FORWARD unskippable by design (design doc's
defended unsafe choice) but pausable? NO — QA-32: pause during an
authored sequence is refused; the booth's flicker slider still applies.
TEST assert af_active after the dock; relaunch → still true; no
STING-class audio event in the sequence (silence-ledger grep).

### 4.18 · The Sign-Off assets
SPEC `asset_pickup.gd` (an asset where canon left it: CART in MASTER
CONTROL, SCRIPT in the TRANSMITTER HALL cage, CARD in the dock's props
crate after filing), `spectro_dock.gd` (the audio bench: the VERSE under the
closing song, in the sidebands), `asset_rack.gd` (four labels above the
bench, `ORDER` VERSE/CART/SCRIPT/CARD), `GameState.gain_asset` ("of 4"),
`world_builder._spawn_assets_and_decision`. STATE `assets` (array of
ids). UE HOME three pickups + one dock + the rack as a bench widget-in-
world. LAWS generations gate understanding: the ASK alternative (Harriet
hums the verse with one wrong word) is a Phase 4.WEB/4.ENCOUNTERS content
branch; the classic route is what ships first. ACCEPTS the walkthrough's
asset table (T2 verse, T3 cart + script, T4 card); QA-28's 4/4
precondition. FEEDBACK the rack label lights per asset; the toast counts.
FAIL-FORWARD assets are never lost by retake (they are saved state, not
inventory). TEST assert four ids gained in any order → rack shows four;
PERFORM with <4 routes per 4.28a's table.

### 4.19 · The dock contract
SPEC `dock_task.gd` (the scene dock inventory: six units, one anomaly, zero
incidents, by contract), `dock_chum.gd` (a retired unit on its armature;
one is warm; nothing follows, ever), `world_builder._spawn_dock_task`.
STATE `dock_done`, `dock_count`. UE HOME six interactables + the task
actor; the CARD asset (4.18) spawns into the props crate only after
filing. LAWS Law 4 THE WARM ONE NEVER ACTS (on camera, off camera, in any
ending; nothing follows filing it; no system may contradict this,
including audio — I12 is a review rule on every future commit); the dock
never springs (scare compendium); the Director never stages the dock
(4.7). ACCEPTS QA-24, P7 (exactly one warm unit; no follow-up event ever;
card after filing); A10 THE ROWS KEEP THEIR ORDER (text never mentions
warmth). FEEDBACK her gloved hand on a body that is warm — one line, then
nothing. FAIL-FORWARD by definition: nothing can go wrong in the dock.
TEST assert no Rundown, Director, or audio event can be scheduled with a
dock-zone origin (grep-level audit + a soak with the bot camping the dock
for 10 min → zero events).

### 4.20 · The once-ever sight (fire corridor, Day 4)
SPEC `glimpse.gd` (T4.8: once, ever, under two seconds, unmediated; the
fire corridor unseals on Day 4 and the elbow keeps its appointment),
`world_builder._spawn_event_wave`. STATE `glimpse_seen` (saved; the single
spawn per save lifetime). UE HOME a level-scripted actor guarded by the
flag; the animation must read as genuinely undecidable (puppeteer missing
its puppet or the reverse) — a 2.x anim deliverable this unit consumes.
LAWS Law 3 ONCE, EVER (occurs at most once per save and is never
referenced again by any system, including achievements, presence, and
logs; its name appears in no code file — name the UE class as the Godot
precedent does, and grep the achievements/presence tables for it: must
be absent); I11 the glimpse never repeats; I30 meta-silence holds at
scale. ACCEPTS QA-25, P10 (fire, quit, relaunch, revisit: never refires);
NO achievement by doctrine. FEEDBACK none beyond the sight and the
sheeting's breath. FAIL-FORWARD it cannot harm; the corridor is traversed
by daylight once first (routing Day 7) so its geography is known.
TEST harness assert single spawn per save across two relaunches; grep
build tables for the name.

### 4.21 · Lockdown (Tape 4's turn)
SPEC `lockdown.gd` (every monitor the same frame — `sync_to`; exterior
doors sealed on schedule; Merle radiant at the head of the room),
`rec_chairs.gd` (CASUAL → ROWS, tweened on camera; they do not convert
back; rows persist), state re-applied on ready. STATE `lockdown_done`
(saved). UE HOME an actor sequencing the rig sync (one RT to many screen
materials), door seal, chair tween; re-application on load. LAWS I18
lockdown is permanent (sealed doors, synced monitors, rowed chairs survive
reload); routing law: the map's reversibility ends here, loudly, once.
ACCEPTS QA-26 (monitors sync, doors read SEALED FOR BROADCAST, chairs tween
to rows and persist), P11; A20 SEALED FOR BROADCAST. FEEDBACK the sync
itself (SCARE 9, blocking variants per 4.7 profile), Merle's line, the
door text. FAIL-FORWARD the four assets are gatherable before it by
routing; after it the premiere is always reachable (I06's world).
TEST save/reload after lockdown → assert all three persist; chairs never
return to CASUAL.

### 4.22 · The club on schedule (Merle, the pegs)
SPEC `merle.gd` (Merle on her schedule: the KETTLE by day, her CHAIR by
night, the DOORWAY saying nothing when the pen is up; `SPEED` 1.6),
`coat_pegs.gd` (the entry pegs as a readable group-state meter: NEUTRALS →
SHOW palette drifting per the day table), `world_builder._spawn_club/
_spawn_details`; her 1974 scene → `merle_1974`. STATE `merle_1974`,
`day`, the pen state (live). UE HOME Merle as a character actor with a
three-point schedule driven by `night_changed` and the pen; the pegs as
dressing-tier drift (taxonomy: the ONLY drift-eligible tier). LAWS the
comfort is never the trap (no scare via Merle, the kitchen, or kindness);
Law 4 adjacency: her warmth is load-bearing dread; QA-56 drift resolves
to dressing. ACCEPTS QA-11 (pegs drift per day table; Merle at kettle,
chair, or DOORWAY per schedule and pen state, never elsewhere), P14 (raise
the pen and wait: she walks to the doorway and says nothing until ink is
down); A12 NO SEARCHER SINGS (hidden). Harriet's freeze is 0.8b-4; Vess's
lines are 4.12. FEEDBACK her position IS the meter; the towel; the pegs.
FAIL-FORWARD she never blocks a door. TEST assert her position ∈ {KETTLE,
CHAIR, DOORWAY} at every tick of a day/night soak; pegs monotonic.

### 4.23 · The rejected edit and the splice temptation
SPEC `rejected_edit.gd` (T4.5: Vess threads his own cut; it plays once, in
full; the take-up reel turns backward one rotation; afterward the block
offers the SPLICE with Harriet's label disclosed), `GameState.
mint_shortcut_daily` (a daily minted immediately). STATE `rejected_seen`,
`h2_done` (→ 4.24b doubles her at the NEXT break). UE HOME an interactable
running a Level Sequence on the rec-room set, then a choice prompt on the
ordinary keys (controls map: temptation never gets a special button).
LAWS Law 7 every death has a signature (the splice is a nameable choice);
the reaction matrix's V-arc anchor scene (design doc named gap 3). ACCEPTS
QA-49 (after the viewing the block offers the splice with the label
disclosed; performing it mints a daily immediately; the NEXT break doubles
her; she persists as scenery with one line; rebuilds after save/load).
FEEDBACK the reel's refusal, the club's textured silence (5.1 silence-as-
event). FAIL-FORWARD refusing costs nothing; the offer does not recur.
TEST assert daily count +1 on splice and `is_dead("HARRIET")` with cause
H2 at the next BREAK flip.

### 4.24a · The casualty ledger core
SPEC `GameState.mark_casualty(who, cause, epitaph)` (idempotent), `cause_of`,
`is_dead`, `all_cast_dead`, the binder's ledger page (`hud._fill_binder`:
NO ENTRIES. KEEP IT SO. until a death; then who, cause, day, epitaph), the
epilogue reader in every `_end_*` (THE LEDGER, READ ALOUD; fifty-eight
minus N; a clean run reads nothing). STATE `casualties` (array of ids
with cause tags — a load-bearing array, per 0.8b-3's delta list), per-
death flags. UE HOME state subsystem API + the binder page widget + a
reader function every ending calls. LAWS Law 7 EVERY DEATH HAS A
SIGNATURE (the binder names the choice; house idiom is the broadcast-
body); I27 deaths are idempotent (no double entries, no double toasts);
I28 the ledger never lies (every epilogue reading matches the binder page
exactly); I29 clean hands are silent (S0 if any reading appears on a
clean run; A27 files once). ACCEPTS QA-39, QA-47; A27 EVERYONE GOES HOME;
P24, P25, P26 (feel). FEEDBACK the stamp-register entry; the final card
THE 58 CLUB followed by the new number. FAIL-FORWARD no death is a game
over; the run continues. TEST force both Vess triggers in sequence →
one entry (I27); string-compare epilogue vs page at credits (I28); clean
run → zero reading text (I29).

### 4.24b · M1 / M2 and H1 / H2
SPEC casualty ledger canon + as-built: M1 THE SECOND VIEWING (`fire_tape_
dock.gd` offer Day 3+: refusing saves her and never re-offers; consent
plays the repossession, the kettle caption, absence everywhere after);
M2 THE HOME SINGER (premiere: put her on the call sheet; the swapped word
HERE/HOME; struck through in her own handwriting); H1 CONTINUITY
(`harriet.gd`: the slip arms only Day 2+ while frozen; exactly one
paperless signature that toasts in her hand; the next break plays the
absence and the film cabinet holds her); H2 THE SPLICE (4.23 → doubled at
the next break, scenery with one line forever, rebuilt after load).
RIPPLES: kitchen cold and the kettle still (the hunter lingers there);
pegs freeze at her peg's day; night trips escalate one stage early (M1);
incidents lose 20% forgiveness (M2); the seventh signal unlearnable if
Harriet dies before her card (4.13); screenings judged 0.05 tighter
without her (0.8b-4's stance window reads `is_dead`). UE HOME branches
in the four owning actors + the reader's variant lines. LAWS Law 4
(Merle never sinister: she dies being exactly who she is), Law 7. ACCEPTS
QA-40 (M1 both branches; THE BURN and NEW PRODUCER variants), QA-41 (H1
all five clauses), QA-49 (H2). TEST speedpaths: M1 Day 3 consent; H1 any
Day 2 break; assert ripples via state reads.

### 4.24c · V1 / V2 and F1 / F2
SPEC V1 CREDITED, THEREFORE CAST (precondition `vess_credited` from 4.12;
triggers: commit AUTHENTICATE at the ledger, or the final breaker itself
after the farewell — `finale_breaker.gd`, `live_production.gd`); V2 THE
UNCREDITED FIX (precondition insight used, never credited; cascade night:
GET VESS at the dead panel → circuit F; restoring alone in order saves
him — `cascade.gd`); F1 THE FADER (inside DEAD AIR only: choice by
omission at the divert — 4.27 `_fader_choice`); F2 THE UNLISTED CAMERA
(`live_production._f2_unlisted`: exactly the third blind tally call; the
unlisted-camera beats; cue flow continues; thereafter he exists only in
the program feed and stillness near monitors draws his point). RIPPLES:
breaker incidents lose their easy variant; DEAD AIR's breaker grace
window lost without Vess (crossing 62 s); cue marks stop auto-
highlighting after either F death. CANON-ONLY remainders named by the
ledger's AS BUILT: the margin's green bleed and the post-F2 monitor haunt
+ freeze-check inversion — build from the doc, flag in the ledger entry.
LAWS Law 7; Law 5 (the FM has no voice, in death too). ACCEPTS QA-42
(V1 both triggers, V2 GET VESS only for the uncredited; dead: pin + hard
blackout, crossing 62), QA-43 (F2 third blind call; F1 self-hold costs
13 s and routes 4b; his hold routes 4a; dead → self-hold forced); A11's
inverse. TEST speedpaths: V1-fast credit then AUTHENTICATE Day 3; V2
cascade night uncredited; F2 three blind calls; F1 by omission.

### 4.24d · L1 / L2, the rows and ENDING 0
SPEC L1 THE SIXTH QUESTION (`seance_dock.gd`: offered only past five
answers AND wear > 70; `respond` asks it; the ink drains; the dock inert
forever; 1A closed; 1B shows the pencil READER card); L2 THE READING
(bring the fire tape to the seance dock and `improvise`: consumes it,
empties answers, sets the completed sign-off → ending 4c with no divert
prompt); THE ROWS (`live_production.ROW_LINES/_row_taken`: every timed
incident that expires past guarantee takes a seat, cycling three lines
with the caption; the count persists and feeds every final card);
ENDING 0 A ONE-WOMAN SHOW (`_one_woman`: all four ledgered before
lockdown → the premiere intercepts at entry; credits show nine cards, one
name; A28 files at the next flush gate). STATE `leland_answers`,
`seance_wear`, `fire_tape_held`, `signoff_completed`, `rows_taken`.
LAWS Law 7; I26 is NOT this (that is the AF cool, 0.8a); I30 meta-silence
(ending 0 still toasts nothing mid-play). ACCEPTS QA-44 (L1 gate + beats;
L2 consumes, empties, sets, 4c with no divert), QA-45 (ENDING 0 intercept;
nine cards, one name; A28), QA-46 (rows: seat per expired incident, lines
cycle, count persists); A28 A ONE-WOMAN SHOW; no achievement for 4c by
ruling. TEST speedpaths: L1 five answers then grind wear past 70 then
respond; L2 carry the fire tape to the dock and improvise; rows: fail-bot
lets every incident expire → assert seats == expired incidents.

### 4.25 · The decision ledger (the point of no return)
SPEC `decision_ledger.gd` (three entries possible in her hand:
AUTHENTICATE / DESTROY / PERFORM; `COMMIT_LINES`; `mark_read("D03")`),
`GameState.start_finale` → `finale_started(decision)`; Merle in the
doorway watching the pen (4.22's DOORWAY state) is the no-modal
point-of-no-return signal (walkthrough named gap 4). STATE `decision`
(saved; never written by the demo build). UE HOME the bench's hero
interactable with a three-way prompt on ordinary keys. LAWS the V1
trigger on AUTHENTICATE (4.24c); the INK ripple toast; PT never forces an
ending by itself. ACCEPTS A17 INK; QA-28's routing precondition; V7
(which ending first, design telemetry). FEEDBACK the pen is the loudest
thing in the building (no music; 5.1); Merle's silence. FAIL-FORWARD a
committed decision is final by design and the walkthrough's rule: the
unmistakable no-return signal is Merle, not a dialog. TEST assert
`decision` ∈ the three, `finale_started` once, DEMO write path absent
(4.30).

### 4.26a · The premiere: cues, the switcher and incidents
SPEC `live_production.gd` (Phase 2 playable: `run()`, the cue marks on
`MARK`, `_on_mark_press(label, need_cam)` requiring the PGM camera —
actions `cam_1`/`cam_2`/`cam_3` are the switcher; `INCIDENTS` TALLY /
HOUSE / BOOM / CARDS with `FIX_LINES`; `_timed` guarantees; `_resolve`
with "club auto-fix" at or under 40 s; `_tally_refusals` ≤ 2; `_boom_held`
exactly 1; `premiere_log`), `finale_fixture.gd` (aux panel, boom winch,
card stand: each fixes one incident), `world_builder`'s LiveProduction
node. STATE `finale_done`, `fail_takes`, live counters. UE HOME a
GameMode-scoped director actor; cue marks as trigger volumes; the
switcher as Enhanced Input actions mapped one-to-one to the console's
button bank (design doc Part V); fixtures as interactables; `premiere_log`
unchanged. LAWS I03 the premiere yields the floor (the Rundown never
hunts while the show is live), I05, I06 FAIL-FORWARD FINALE (a cue can
always be re-entered; no incident hard-blocks; auto-fix ≤ 40 s; refusals
≤ 2; boom holds 1); Law 1 on camera is safe; the braid law (4.QA51).
ACCEPTS QA-27 (cue marks require the PGM camera; each incident type
fail-forwards within its guarantee); the fail-bot's I06 scorecard line.
FEEDBACK the incident line as the club's apology; the fix line as the
fixture's own voice; tallies as lamps. FAIL-FORWARD is the unit. TEST the
0.9 fail-bot premiere soak (ignores every incident, fails every cue
thrice) → I06 PASS with counts.

### 4.26b · The premiere: sabotage, the breaker, pressure and the bell
SPEC `finale_breaker.gd` (the patch bay during the premiere; the club is
helping), `live_production._pressure/_fail_takes/_blind_calls` (the
sabotage sprint loop STA → CTL → PB inside the break window and back
before the return cue; the Vess breaker: credited → his hand stops above
the handle; uncredited → the handle, the dark, earn the retake),
`sfx.gd`'s bell (two inharmonic partials; it rings ONCE, three feet behind
camera position, at the midpoint; its caption says so), SCARES 10/11/12
(the bell, the plunge with tallies dying toward her, the delivery: the
club's hands holding her off camera). STATE `vess_credited` (read),
`bell_rung` once. UE HOME the breaker as an interactable with the two
variants; the sprint loop is the level's window schedule; the bell is one
MetaSound one-shot with a caption and a VISUAL BELL bloom (accessibility).
LAWS Law 5 SILENCE CONTRACTS (the bell rings once, at the finale beat;
otherwise silent; clapperless on the AF body); Law 6 (the loop is
window-bound); I05 (the delivery is human hands, never his, until the
frame is lost). ACCEPTS QA-42's breaker clauses (credited living die at
the final breaker AFTER the farewell, lights held), QA-46 (rows are
4.24d's — the seat is taken HERE on expiry), the bell's caption; P22.
FEEDBACK the hesitation is the window; the bell's caption; tallies dying
in sequence (shape + position, never color alone). FAIL-FORWARD a lost
frame is seconds to regain, never instant (fail condition 5). TEST assert
exactly one BELL event per run in the audio event log; breaker variant by
`vess_credited`; blind-call counter reaching 3 → 4.24c's F2.

### 4.27 · The divert, the fader and the last crossing
SPEC `live_production._fader_choice` (SPACE for his hand; E held 4.6 s
for hers), `_hold_fader` (self-hold costs 13 s and an arm), `_last_
crossing` (the divert at the final break: master control to the little
door, 75 s base, 62 without Vess, minus 13 self-held; him behind her at
`AF_CROSSING_SPEED` 1.6 with folds still costing 2.2 apiece; his tally
eye DARK the whole way; three outcomes: reached → DEAD AIR, caught → the
old run end inside her own ending, too slow → the window closes and the
committed line plays), `_little_door` (closed by hand, on camera). STATE
`decision`, `fire_tape_held`, `has_key("QUIET ROOM")`, `leland_answers`,
`signoff_completed`, `divert_taken`, `fader_hand`. UE HOME the director
actor's divert branch; ARundown's crossing state (0.8a's AF layer gains
one speed constant); the little door is a `CompoundDoor`. LAWS Law 11
(every threshold costs him 2.2 s — the toll is the player's counterplay);
I19 the divert gates on key + answers + the fire tape; I24 the fold is
paid on the honest route (two folds); Law 10 inverted honestly: you are
not in this broadcast, nothing on the log protects you. ACCEPTS QA-28
(divert with the fire tape → DEAD AIR path; otherwise the committed
decision's ending), QA-43's F1 clauses (self-hold 13 s → 4b; his hold →
4a; dead FM → self-hold forced), the protocol's "the divert window only
appears when earned"; P22, P23. FEEDBACK the caption for the divert (a
radio through three walls belongs to 4.28b, not here); the countdown; the
fold captions. FAIL-FORWARD all three outcomes are authored and hers.
TEST position-delta audit across door radii (I24) during a scripted
crossing; assert 75/62/13 arithmetic from the log timestamps.

### 4.28a · Endings and credits
SPEC `hud.gd` `_on_finale` → `_end_burn` (Ending 3 THE BURN: DESTROY;
playable destruction via the degausser and bake oven; cold-cobbler
variant), `_end_producer` (Ending 2 THE NEW PRODUCER: AUTHENTICATE, or
PERFORM with <4 assets while PT ≥ 70; `mark_ending(name, lie=true)` →
`lie_pending`), `_end_perform` (1A Leland closes: PERFORM, 4/4, five
answers, wear ≤ 70 / LI ≥ 60 as built; 1B Rita closes otherwise, SAINTS
+ STAFF + READER cards as earned), `_end_4c`, `_end_zero`, `_end_dead_air`
(4a HIS HAND / 4b HER HAND; the erase loop; the FORCE-path hairline hum
variant), `_roll_credits` → `credits.gd` (period cards, phosphor on black,
`SPEED` 42; any key after grace skips; the tower-light card holds; returns
to title), `GameState.mark_ending` → `ending_marked`, `title.gd`'s NEW
EPISODE once then revert. STATE `ending_reached`, `lie_pending`,
`finale_done`, `pt`. UE HOME UMG ending sequences + a credits widget; the
lie is a title-widget branch on the flag that clears itself. LAWS Law 8
THE INTERFACE MAY LIE EXACTLY ONCE (Ending 2's post-credits: CONTINUE? in
the CG face, NEW GAME reads NEW EPISODE, reverts next launch); I13 the lie
is spent exactly once; I28 the reader (4.24a) opens every credits; the
casting-drift binder is dressing, never deception (design doc named gap
2). ACCEPTS QA-03 (credits crawl, skip after grace, tower-light card),
QA-28 (ending exits roll credits), QA-47 (every ending's credits open
with THE LEDGER, READ ALOUD when anything is in it); A21 THERE'S COBBLER,
A22 WELCOME HOME, A23 FILE UNDER: SAINTS, A24 IT'S OKAY. NOBODY'S
WATCHING., A25 SIGNED OFF (the all-black icon); protocol §3 speedpaths
(objective line ENDING REACHED; CONTINUE resumes sane). FEEDBACK the
final ledger line in her hand per ending; the card; dark that is only
dark. FAIL-FORWARD every ending exits to title with a sane CONTINUE.
TEST the full-run matrix per ending (I13, I16–I19) in the harness;
relaunch twice after Ending 2 → NEW EPISODE exactly once.

### 4.28b · ENDING A · AUDIENCE ONLY — CANON-ONLY
SPEC none in `scripts/` (grep: no W1/W2/W3 reels, no S2 slip economy, no
radio dial confirm, no 58 · STILL ON mark, no PROGRAM GUIDE). The canon is
the walkthrough's c046 SPOILER addendum and QA-60/QA-61, and it is
detailed enough to build from: four clean dailies first; W1 in the
library's skip gap where 0118 should be (Day 2); W2 behind the burn barrel
only after W1 (Day 3); W3 on the shed shelf only after W2 (Day 4, him
awake); each first viewing requires four dailies logged and consumes one
S2 slip with refusal lines otherwise; re-reads free; nothing announces on
completion; A26 counts only the D series; then CONFIRM the dead room
radio's dial (appears only after W3); the final break gains the caption
"a radio, through three walls"; `improvise` within six seconds starts the
75 s run; reaching the dead room routes ENDING A with her single credit
card; declining or late falls through untouched; no achievement by
design; the post-credits PROGRAM GUIDE plays for this ending only; the
title carries 58 · STILL ON on every later launch. STATE new keys (reels
watched, slips, dial confirmed, still_on) — extend the v16 schema only via
0.8b-3's rule (defaults ARE the migration; bump SAVE_VERSION to 17 and
record the policy the gap audit asks for). LAWS I30 (no achievement, ever,
for this); Law 5 (the radio's last words are Harriet's line, not his);
Law 3 adjacency (nothing new referenced elsewhere). ACCEPTS QA-60, QA-61
in full. FLAG this box in the ledger as the first unit that ports prose
with no code beneath it: build to the QA lines, and add the reels to the
Godot reference only if the owner wants the spec to stay two-engine.
TEST the QA-61 chain as a functional map; assert the title mark persists
across relaunch and that no achievement id fires.

### P6 · META AND MODES

### 4.29 · Achievements with deferral
SPEC `achievements.gd` (autoload: `unlock(id)` idempotent; `user://
achievements.cfg`; nothing surfaces during play; the queue flushes at
exactly two gates — the morning toast on `night_changed(false)` and the
title's `_ready`; disabled entirely under DEMO; the once-ever moment has
no entry, on purpose; `achievement_unlocked` for the Steam bridge;
`TITLES` A01–A28). STATE the cfg (apart from the save). UE HOME a
`UGameInstanceSubsystem` with its own ini/SaveGame slot; the flush gates
bind to the same delegates; the Steam bridge later. LAWS the deferral
rule; the meta-silence ledger (Chum's name in no title; the warm unit
acknowledged only via A10 whose text never mentions warmth; the seance
grants A14 once, never per answer; no per-death achievements — deaths are
entries, not trophies); I30. ACCEPTS QA-04 (FILED WHILE YOU WERE OUT once —
the title half is 4.34), QA-29 (no toast between title and morning;
morning shows FILED lines), QA-48 (demo: achievements stay dark); the
full id table A01…A28 with triggers as designed. FEEDBACK the morning
FILED lines in the ledger's register. FAIL-FORWARD unlocks never block
and never lose (queued until a gate). TEST harness grep: zero unlock
toasts inside any protected beat; each id fires once across the matrix.

### 4.30 · The DEMO build (Tape 1, free)
SPEC `GameState.DEMO` (build flag), `demo_mark` (funnel telemetry: six
marks, local file only), `demo_ended` → `hud._on_demo_end` (the end card;
input protected 3 s), the demo door-reason override table and the
`Data/DemoOpen.csv` seven rooms (0.5 extracted it), `bed_prop.gd`'s demo
branch (the bed declines), paper S1 + S5 only, the save writer whitelist
(the demo build is INCAPABLE of writing decision, assets, leland_answers,
lockdown, finale, or any ending field — absent from the write path, not
gated), Merle's carry line on first CONTINUE from a demo save. STATE
`demo_complete`; the whitelist per `PORT-NOTES-STATE.md` §5. UE HOME a
build configuration + a data flag the stamper and the SaveGame writer
read; the end card in UMG. LAWS the demo cut plan §4 guarantees; the
achievements-dark parity; the casualty ledger's demo clause (a full-game
save with Merle dead refuses to load forward). ACCEPTS QA-30 (seven rooms;
demo reasons on doors; bed declines; S1 and S5 only; card protects three
seconds; completed demo save contains none of the whitelisted-out fields;
funnel file has six marks), QA-48, DP1–DP5. FEEDBACK the sealed-door
strings; TAPE 1 · FREE DEMO under the logo (4.34). FAIL-FORWARD DP4: paper
exhaustion at S1 still leaves S5. TEST hand-inspect a completed demo
save (DP2) by script; assert the six marks.

### 4.31 · The booth (options)
SPEC `options_panel.gd` (master volume, mouse feel, the window, text scale
0.8–1.6, high-contrast map, captions, ASSIST, TBC and photo-safe switches,
the five-verb remap with KEY IN USE refusal; `user://settings.cfg` apart
from the log so NEW GAME never touches it; opens BEFORE first play with
the BEFORE THE SHOW banner), `GameState.load_settings/save_settings/
rebind/key_name/set_ui_scale/set_captions/set_assist`, action `options`
(O). STATE the settings file (§4 of the state notes). UE HOME UMG over a
custom settings object (not the SaveGame); Enhanced Input remapping of
EVERY action including movement (controls map's UE target); hold-to-
toggle for capture, fader, stillness with durations preserved. LAWS Law 9
ACCESS IS CANON (the booth, captions, assist, remap, pause, and the
deferral rule ship in every build); the accessibility matrix R1–R7 +
the full target (flicker/grain slider, visual bell, mono downmix, stick
sensitivity/invert, gyro, toast dwell); the controls map's hold-vs-toggle
contract. ACCEPTS QA-01 (first launch: booth over title, banner, writes
settings, no re-prompt), QA-16 (every slider and check persists; NEW GAME
leaves settings intact), QA-17 (remap onto E refused with KEY IN USE;
onto unused: prompts everywhere show the new key), QA-18's assist half
(0.8b-4 owns the beat window). FEEDBACK a station-paperwork form on WGLD
letterhead (design doc Part III). FAIL-FORWARD nothing in the booth can
gate content or endings. TEST settings round-trip diff; remap conflict
matrix; glyph substitution grep across all prompts.

### 4.32 · The HUD, the binder, captions and pause
SPEC `hud.gd` (binder-toned HUD: interact prompt with real glyphs
(`glyphs`/`key_name`), save toast, TBC lamp, the tally lamp REC · SAFE
WHILE LIT with the live countdown (`_process_tally`), captions with source
tags (`caption`/`show_caption`), the blackout scrim (`blackout_changed`),
the binder on `ledger` (TAB): the form (mode, assist), the binder page
(objective_text, director read, sheet count, casualty page, assets,
documents), pause (`pause_requested`: world and clocks hold, audio mutes;
refused during any authored sequence), the demo end and every ending
sequence (4.28a), retake presentation (0.8b-4)). STATE `ui_scale`,
`captions_on`, `objective_text()`. UE HOME UMG widgets; the scrim as a
UMG layer (recommended over post-process for the layering guarantee);
captions extended with left/right directionality and proximity weight.
LAWS Law 9; the two-layer diegesis (world UI is broadcast engineering,
meta UI is station paperwork — no floating HUD element without a 1970s
device that already displays it); the binder IS the inventory (gap audit
ruling 4); binder and map true-pause in the day, LIVE-TIME during the
premiere only (ruling 3). ACCEPTS QA-05's pen-tick caption, QA-32 (pause
anywhere unlocked; refused in authored sequences), QA-34's HUD half (REC ·
SAFE WHILE LIT with a live countdown), the toast-never-overlap rule and
TOAST DWELL. FEEDBACK is the unit. FAIL-FORWARD toasts queue; captions
never cover the tally. TEST assert pause refused during fire tape /
premiere / endings; caption log matches the audio event log.

### 4.33 · The map
SPEC `map_view.gd` (M: the facility map drawn live from the room table;
rooms, `LANDMARKS`, station dots labeled, a moving dot with a facing tick;
sealed rooms dashed after lockdown; footer shows the BOUND map key; high-
contrast palette at 5.85:1), action `map`. STATE `lockdown_done` (read),
`hc_map` (settings). UE HOME a UMG widget with `OnPaint` reading the same
Rooms.csv DataTable and the station registry. LAWS the binder/map pause
ruling (4.32); the taxonomy (landmarks are interactables, never dressing).
ACCEPTS QA-15 (sealed rooms dashed, station dots labeled, footer BOUND
key), P15 (outlines match walls; the dot never exits geometry).
FEEDBACK the map is paper (Part III). FAIL-FORWARD none needed. TEST
walk three rooms with the map open in a functional map; assert dot-in-
room from Rooms.csv bounds every tick.

### 4.34 · The title screen and the string table
SPEC `title.gd` (channel dark, the card, the menu; phosphor focus ring;
FILED WHILE YOU WERE OUT exactly once; NEW EPISODE once when `lie_pending`
then revert; TAPE 1 · FREE DEMO under the logo in the demo), `Data/
GameText.csv` (714 keys = source strings; extracted in 0.5) → a UE
StringTable wired into every widget and caption, `translations/` for the
localized builds (localization plan). STATE `lie_pending`, the
achievements queue. UE HOME UMG title widget; the StringTable asset;
the 58 · STILL ON mark is 4.28b's. LAWS Law 8 (the lie's revert lives
here), Law 5 (Chum has no presence string, no title, no account); the
deferral rule's second gate. ACCEPTS QA-02 (Tab through the title: focus
ring on every button; Enter activates), QA-04 (once), QA-31's toast
surface (the migration itself is 4.SAVE's). FEEDBACK the card. FAIL-
FORWARD the title never blocks on a missing save. TEST assert every
UI string resolves through the table (no raw literals in widgets); the
NEW EPISODE relaunch test with 4.28a.

### The existing Phase 4 boxes (kept verbatim in PROGRESS.md; where they sit)
- **4.WEB** reaction-matrix wiring audit — the QUEUE items (H-R2 and F-R1
  the crowns; M-R5 and B-R2; then M-R1..4, V-R1..3, L-R1) land AFTER the
  mechanics above exist; each with QA lines; no reaction explains.
- **4.SAVE** integrity pass — QA-31 (v15 → v16 migration toast, nothing
  lost, settings untouched), the burn-in rule (wear, splices, dailies
  survive retakes and reloads), the save-migration policy the gap audit
  asks for once v17 exists (4.28b will need it), `SAVE_VERSION` policy.
- **4.ENCOUNTERS** choreography per room — the scripted set pieces with
  their two-to-three blockings per 4.7 profile (game master Appendix A,
  SCARES 2–9 outside the premiere), the poisoned-well once-per-run rule,
  the silence tell (1.5–3 s) before every scripted impact, the Rundown's
  nightly segment shuffle within grammar, camera-kill rate per tape.
- **4.FINALE** premiere sequence — the end-to-end choreography of 4.25 →
  4.26a/b → 4.27 → 4.28a on the real Studio A with the club's sabotage
  tuned so retries escalate (walkthrough named gap 3), captured and
  reviewed as one continuous take.
- **4.QA51** braid audit; **4.VERB** per-day verb-texture audit; **4.FINAL**
  the phase gate (deep soaks, invariants extended).

---

## B · LAWS, INVARIANTS, QA AND ACHIEVEMENTS — WHERE EACH LIVES

### B.1 THE LAWS (THE-LAWS.md) → owning boxes
| Law | Owning boxes |
|---|---|
| Law 1 ON CAMERA IS SAFE | 4.1, 4.26a, 0.8a (visible gate) |
| Law 2 ONE STARTLE | 4.16 (the lunge), 4.4, 4.17 (no sting) |
| Law 3 ONCE, EVER | 4.20 |
| Law 4 THE WARM ONE NEVER ACTS | 4.19, 4.22 |
| Law 5 SILENCE CONTRACTS | 4.26b (the bell), 4.5, 4.29, 4.34 |
| Law 6 THE SCHEDULE IS REAL | 0.7 (clock), 0.8b-4 (Harriet), 4.2, 4.6, 4.10, 4.26b |
| Law 7 EVERY DEATH HAS A SIGNATURE | 4.24a, 4.24b, 4.24c, 4.24d, 4.23 |
| Law 8 THE INTERFACE LIES EXACTLY ONCE | 4.28a, 4.34, 4.14 (what is NOT the lie) |
| Law 9 ACCESS IS CANON | 4.31, 4.32, 4.16 |
| Law 10 THE TALLY CONTRACT | 0.8a, 4.1, 4.27 (its honest inversion) |
| Law 11 THE TWO HIDES + THE DOOR TOLL | 4.1, 4.3, 0.7 (the fold), 4.27 |

### B.2 INVARIANTS (I01–I31) → owning boxes
| Invariant | Owning boxes |
|---|---|
| I01 warning precedes reach | 0.7, 0.9 |
| I02 no strike through walls | 0.7, 0.9 |
| I03 the premiere yields the floor | 4.26a |
| I04 window holds obey the clock, yield only to the cascade | 4.6, 4.10 |
| I05 on camera is safe | 4.1, 4.26a, 4.26b |
| I06 fail-forward finale | 4.26a |
| I07 cascade liveness | 4.6 |
| I08 every locked door states its reason | 4.10 |
| I09 abort never costs a daily | 4.9, 0.8b-2 |
| I10 the presigned page costs no paper | 4.14 |
| I11 the glimpse never repeats | 4.20 |
| I12 the warm unit never acts | 4.19 |
| I13 the interface lie is spent exactly once | 4.28a |
| I14 one startle in the whole game | 4.16, 4.17 |
| I15 the silence ledger (no sting, chairs silent, FM never heard moving) | 4.17, 4.5, 4.4, 5.1 |
| I16 item loss is ordered and bounded | 4.8 |
| I17 sheet retirement is honest | 4.8 |
| I18 lockdown is permanent | 4.21 |
| I19 the dock/seance/divert gates | 4.19, 4.15, 4.27 |
| I20 the same frame is always the same frame | 4.15 |
| I21 the Director is deterministic and explainable | 4.7 |
| I22 heard noise is attributable | 0.7, 4.3 |
| I23 no strike while lit | 4.1, 0.8a |
| I24 the fold is paid | 0.7, 4.27 |
| I25 deaf to the dead room | 4.3 |
| I26 one cool teaches | 0.8a |
| I27 deaths are idempotent | 4.24a |
| I28 the ledger never lies | 4.24a, 4.28a |
| I29 clean hands are silent | 4.24a |
| I30 meta-silence holds at scale | 4.29, 4.20, 4.24d, 4.28b |
| I31 crouch does not hide | 0.8b-1, 0.9 |

### B.3 QA REGRESSION (QA-01–QA-61) → owning boxes
| QA | Box | QA | Box | QA | Box |
|---|---|---|---|---|---|
| QA-01 | 4.31 | QA-21 | 4.14 | QA-41 | 4.24b |
| QA-02 | 4.34 | QA-22 | 4.15 | QA-42 | 4.24c, 4.26b |
| QA-03 | 4.28a | QA-23 | 4.17 | QA-43 | 4.24c, 4.27 |
| QA-04 | 4.29, 4.34 | QA-24 | 4.19 | QA-44 | 4.24d |
| QA-05 | 0.8b-4, 4.32 | QA-25 | 4.20 | QA-45 | 4.24d |
| QA-06 | 0.8b-2, 4.16 | QA-26 | 4.21 | QA-46 | 4.24d, 4.26b |
| QA-07 | 4.8 | QA-27 | 4.26a | QA-47 | 4.28a, 4.24a |
| QA-08 | 4.8 | QA-28 | 4.27, 4.28a | QA-48 | 4.30, 4.29 |
| QA-09 | 0.8b-4 | QA-29 | 4.29 | QA-49 | 4.23, 4.24b |
| QA-10 | 4.10, 4.6 | QA-30 | 4.30 | QA-50 | 4.15 |
| QA-11 | 4.22 | QA-31 | 4.SAVE, 4.34 | QA-51 | 4.QA51 |
| QA-12 | 0.7 | QA-32 | 4.32 | QA-52 | 1.10 |
| QA-13 | 4.3 | QA-33 | 4.17 | QA-53 | 1.9 |
| QA-14 | 4.1, 4.2 | QA-34 | 0.8a, 4.32 | QA-54 | 1.12, 5.1 |
| QA-15 | 4.33 | QA-35 | 4.1 | QA-55 | 3.x (per room), 4.11 |
| QA-16 | 4.31 | QA-36 | 0.8a | QA-56 | 3.x, 4.22 |
| QA-17 | 4.31 | QA-37 | 0.7 | QA-57 | 3.x |
| QA-18 | 0.8b-4, 4.31 | QA-38 | 4.3 | QA-58 | 0.8b-1, 0.9 |
| QA-19 | 4.4, 4.5 | QA-39 | 4.24a | QA-59 | 3.x, 4.11 |
| QA-20 | 4.6 | QA-40 | 4.24b | QA-60 | 4.28b |
| | | | | QA-61 | 4.28b |

### B.4 ACHIEVEMENTS (A01–A28) → owning boxes
| Id | Box | Id | Box | Id | Box | Id | Box |
|---|---|---|---|---|---|---|---|
| A01 | 0.8b-4 | A08 | 4.3 | A15 | 4.6 | A22 | 4.28a |
| A02 | 0.8b-2 | A09 | 4.14 | A16 | 4.10 | A23 | 4.28a |
| A03 | 4.16 | A10 | 4.19 | A17 | 4.25 | A24 | 4.28a |
| A04 | 0.8b-4 | A11 | 4.12 | A18 | 4.8 | A25 | 4.28a |
| A05 | 0.8b-4 | A12 | 4.22 | A19 | 4.8 | A26 | 4.11 |
| A06 | 0.8b-4 | A13 | 4.17 | A20 | 4.21 | A27 | 4.24a |
| A07 | 4.13 | A14 | 4.15 | A21 | 4.28a | A28 | 4.24d |

### B.5 INPUT ACTIONS (project.godot) → owning boxes
| Action | Box | Action | Box |
|---|---|---|---|
| interact | 0.8b-1 | photo_safe | 4.16 |
| crouch | 0.8b-1 | cam_1 | 4.26a |
| toggle_tbc | 4.16 | cam_2 | 4.26a |
| ledger | 4.32 | cam_3 | 4.26a |
| respond | 0.8b-4, 4.27, 4.24d | map | 4.33 |
| improvise | 0.8b-4, 4.24d, 4.28b | frame_back | 4.15 |
| options | 4.31 | frame_fwd | 4.15 |

### B.6 TIMINGS (Data/Timings.csv) → owning boxes
| Constant | Box | Constant | Box |
|---|---|---|---|
| ON_AIR_SECONDS | 0.7 | AF_APPROACH_SPEED | 0.8a |
| BREAK_SECONDS | 0.7 | AF_LOOM_DIST | 0.8a |
| CAPTURE_SECONDS | 0.8b-2 | AF_COOL_SECONDS | 0.8a |
| TETHER | 0.8b-2 | AF_HEIGHT | 0.8a |
| SPEED (credits.gd) | 4.28a | AF_FOLD_SECONDS | 0.7 |
| W | 4.15 | AF_DOOR_NEAR | 0.7 |
| H | 4.15 | AF_CROSSING_SPEED | 4.27 |
| SAVE_VERSION | 4.SAVE, 0.8b-3 | WARN_RADIUS | 0.7 |
| SPEED (merle.gd) | 4.22 | STRIKE_RADIUS | 0.7 |
| SPEED (player.gd) | 0.8b-1 | BASE_HEIGHT | 1.8 |
| ACCEL | 0.8b-1 | HEAD_TILT | 1.9 |
| MOUSE_SENS | 0.8b-1 | BEAT | 0.8b-4 |
| REACH | 0.8b-1 | WINDOW | 0.8b-4 |
| CROUCH_MULT | 0.8b-1 | MAX_FRAME | 4.15 |
| MOVE_SPEED | 0.7 | RATE | 5.1 |
| WALL_H | 0.6 | WALL_T | 0.6 |

---

## C · SCRIPT COVERAGE — every `scripts/*.gd`, one primary home

Primary home is the box that PORTS it; other boxes may read it. Homes
outside Phase 4: a Phase 0 box id, a phase tag (`1.x` Blender factory,
`2.x` cast, `3.x` studio, `5.1` audio, `0.9` harness), or `DEV-TOOL`
(Godot-only look-dev scenes superseded by the Blender factory + UE
captures; not ported).

| Script | Home | Note |
|---|---|---|
| `achievements.gd` | 4.29 | autoload → GameInstance subsystem |
| `arm_preview.gd` | DEV-TOOL | look-dev scene |
| `asset_pickup.gd` | 4.18 | |
| `asset_rack.gd` | 4.18 | |
| `bed_prop.gd` | 0.8b-4 | the day/night lever; demo branch read by 4.30 |
| `bench_tv.gd` | 4.16 | |
| `bot_driver.gd` | 0.9 | the three bots |
| `broadcast.gd` | 0.7 | URestorationClock (done) |
| `capture_bench.gd` | 0.8b-2 | ABenchCapture (done) |
| `cascade.gd` | 4.6 | |
| `cast_preview.gd` | DEV-TOOL | look-dev scene |
| `casting_sheet_prop.gd` | 4.8 | |
| `character_kit.gd` | 2.x | procedural cast superseded by the Blender factory (1.x for Chum) |
| `coat_pegs.gd` | 4.22 | dressing-tier drift |
| `coverage_director.gd` | 4.7 | |
| `credit_entry.gd` | 4.12 | |
| `credits.gd` | 4.28a | |
| `cue_sign.gd` | 0.8b-4 | screening + assist |
| `dailies_canister.gd` | 4.9 | |
| `dailies_manager.gd` | 4.9 | |
| `decision_ledger.gd` | 4.25 | |
| `degausser.gd` | 4.9 | |
| `dock_chum.gd` | 4.19 | |
| `dock_task.gd` | 4.19 | |
| `door.gd` | 4.10 | reasons already stamped in 0.6 |
| `dresser.gd` | 4.8 | |
| `film_cabinet.gd` | 4.13 | |
| `finale_breaker.gd` | 4.26b | |
| `finale_fixture.gd` | 4.26a | |
| `fire_tape_dock.gd` | 4.17 | M1 branch in 4.24b |
| `fire_tape_pickup.gd` | 4.17 | |
| `floor_manager.gd` | 4.5 | F2 inversion in 4.24c |
| `frame_sequence.gd` | 4.15 | |
| `game_state.gd` | 0.8a | URestorationState (done); parity 0.8b-3 |
| `gen_knob.gd` | 4.16 | |
| `glimpse.gd` | 4.20 | |
| `harriet.gd` | 0.8b-4 | the freeze; H1/H2 branches in 4.24b |
| `harriet_note.gd` | 4.13 | |
| `head_preview.gd` | DEV-TOOL | look-dev scene |
| `hud.gd` | 4.32 | endings in 4.28a; retake presentation 0.8b-4 |
| `impossible_crate.gd` | 4.15 | |
| `interactable.gd` | 0.8b-2 | IRestorationInteractable (done) |
| `invariant_parser.gd` | 0.9 | |
| `key_item.gd` | 4.10 | |
| `live_production.gd` | 4.26a | 4.26b, 4.27, 4.24c/d read it |
| `liveness_check.gd` | 4.6 | |
| `lockdown.gd` | 4.21 | |
| `log_station.gd` | 0.8b-4 | stations + paper; presigned branch 4.14 |
| `map_view.gd` | 4.33 | |
| `merle.gd` | 4.22 | |
| `monitor_rig.gd` | 4.1 | |
| `night_trip.gd` | 4.4 | |
| `noise_tracker.gd` | 4.3 | |
| `options_panel.gd` | 4.31 | |
| `patchbay_console.gd` | 4.2 | |
| `player.gd` | 0.8b-1 | ARitaCharacter (done) |
| `prop_kit.gd` | 3.x | procedural art pass superseded by Megascans + the factory |
| `readable_prop.gd` | 4.11 | |
| `rec_chairs.gd` | 4.21 | |
| `rejected_edit.gd` | 4.23 | |
| `rundown.gd` | 0.7 | ARundown (done); AF layer 0.8a; crossing speed 4.27 |
| `screening_event.gd` | 0.8b-4 | screening + assist |
| `seance_dock.gd` | 4.15 | L1/L2 in 4.24d |
| `sfx.gd` | 5.1 | MetaSounds; the bell's once-rule is 4.26b's |
| `soak_runner.gd` | 0.9 | |
| `spectro_dock.gd` | 4.18 | |
| `tape_stage.gd` | 4.16 | |
| `title.gd` | 4.34 | |
| `tone_emitter.gd` | 5.1 | |
| `vess.gd` | 4.12 | |
| `vess_binder.gd` | 4.12 | |
| `wall_clock.gd` | 0.8b-4 | clock repeaters read the 0.7 clock |
| `world_builder.gd` | 0.6 | the stamper (done); dressing 3.x; spawn tables feed 4.x |

---

## D · WHAT THE ENUMERATION FOUND (for the ledger)
1. Thirty-four mechanics (thirty-nine boxes with the four casualty and
   three premiere/ending splits), all but one with GDScript beneath them.
   The one without is ENDING A (4.28b), canon-only, flagged.
2. Two canon-only remainders inside 4.24c (the green bleed; the post-F2
   monitor haunt and freeze-check inversion) — the ledger's own AS BUILT
   names them as unbuilt; the register keeps them visible.
3. Phase 0's 0.8b-4 already claims six of the reference scripts; nothing
   is double-boxed, and nothing among the 73 scripts is unowned.
4. Every law, invariant, QA line, achievement, input action and timing
   constant resolves to at least one box (asserted by
   `tools/verify_phase4.py`).
5. The register cites the schema extension 4.28b will need; 4.SAVE must
   settle the v17 migration policy before that unit, not during it.
