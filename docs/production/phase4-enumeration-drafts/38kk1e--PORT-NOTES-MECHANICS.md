# PORT NOTES · MECHANICS — the Phase 4 enumeration

**Unit 4.0 (CLOUD-OK).** Every mechanic the canon names, as one box each in
`PROGRESS.md` Phase 4, with its sources, its reference code, its acceptance
lines, and its owner if some earlier unit already carries the port. This
file is the long form; the tracker boxes are the short form; the ids match
one to one and `tools/verify_mechanics.py` asserts that they do.

**Method.** Sources read in the plan's order: `docs/canon/restoration-design-doc.md`
(Part IV, the mechanic list), `docs/canon/restoration-game-master.md` (every
scene, Appendix B solutions matrix, the tunables), `docs/canon/restoration-walkthrough-levels-endings.md`
(fail conditions, saves, threat architecture, endings, the c043/c046
addenda), `docs/canon/restoration-casualty-ledger.md`, `docs/canon/restoration-reaction-matrix.md`,
`docs/canon/restoration-controls-map.md`, `docs/canon/restoration-object-taxonomy.md`,
`docs/canon/restoration-room-inventory.md`, `docs/canon/restoration-accessibility-matrix.md`,
`docs/production/restoration-gap-audit.md` (RULINGS), `docs/production/restoration-qa-regression.md`
(QA-01..QA-61), `docs/production/restoration-invariant-suite.md` (I01..I31),
`docs/production/restoration-achievements-design.md` (A01..A28),
`docs/production/restoration-spike-briefs.md`, `docs/packet/portbrief/THE-LAWS.md`,
`docs/packet/portbrief/BUILD-ORDER.md`, `docs/packet/portbrief/UE5-MIGRATION-MAP.md`.
Then every one of the 73 files in `scripts/` was placed: owned by a box, or
excluded with a reason (SCRIPT INDEX at the end). Where prose and code
disagree THE CODE IS THE INTENT (`docs/packet/portbrief/PORT-BRIEF.md`);
where the code has nothing, the mechanic is filed CANON-ONLY and needs an
author ruling before anyone ports it. Constants are quoted as NAME=VALUE
from `ue/Restoration/Data/Timings.csv` so the verify script can cross-check
them.

**How to read a box.** CANON = where it is specified. CODE = the reference
scripts (exact pseudocode). ACCEPT = QA lines, invariants, achievements,
laws. UE = the migration-map home. P0 = a Phase 0 unit that already owns
part of the port; the Phase 4 box then means "close it": diegetic feedback,
fail-forward, the QA lines green, the automation test in 0.9's harness.
MILESTONE = the port kit's P2..P6 slot.

**Boxes the enumeration adds: 50** (4.1..4.50) in seven families. The seven
pre-existing audit boxes (4.WEB, 4.SAVE, 4.ENCOUNTERS, 4.FINALE, 4.QA51,
4.VERB, 4.FINAL) stay as they were: they are sweeps across the boxes, not
mechanics.

---

## A · THE BODY AND THE HANDS

### 4.1 Interaction reach, prompts and glyphs
CANON: design doc Part V controls; controls map (prompts render the ACTUAL
binding via the glyph system); object taxonomy (affordance is diegetic wear,
no outlines, one hero interactable per room); gap audit ruling 10 (reach
2.1 m, 35-degree cone, final numbers await the device pass).
CODE: `scripts/interactable.gd` (base: `get_prompt()`, `interact()`),
`scripts/player.gd` (REACH=2.6 ray, ACCEL=10.0, MOUSE_SENS=0.0022,
`current_target()`), `scripts/hud.gd` (prompt label, `GameState.glyphs()`
substitution via GLYPH_MAP). Code is intent: ship REACH=2.6 until the device
pass rules otherwise, then change one number in both engines.
ACCEPT: QA-17 (prompts everywhere show the remapped key), QA-55 (prompt
discipline), QA-57 (hero census); Law 9 (glyphs are access).
UE: `IRestorationInteractable` + the reach ray in `ARitaCharacter` (present
since 0.8b-1); glyph substitution reads the Enhanced Input mapping.
P0: 0.8b-1 (ray + E stub). MILESTONE: P0/P3.

### 4.2 Crouch honesty (the body verb)
CANON: gap audit ruling 2 (c045): a BODY VERB, useless against him BY
ARCHITECTURE; toggle on Ctrl / pad B; camera lowers 0.6; speed 0.55x.
CODE: `scripts/player.gd` CROUCH_MULT=0.55, the 12/delta camera lerp.
ACCEPT: QA-58 (coverage byte-identical walking vs crouch-walking), I31
(no hunter or director code path reads posture).
UE: `ARitaCharacter` (0.8b-1 proved 1.71 m/s and the 0.60 m drop to the
digit). The Phase 4 work is the grep-level audit plus the crouch-bot soak
in 0.9's harness, and the text sweep: no prompt ever implies crouch hides.
P0: 0.8b-1. MILESTONE: P0.

### 4.3 Noise bus and attribution
CANON: walkthrough Part V-B (the Rundown hears); spike 4 (audio-event
localization); game master tunables (sign-log noise); invariant suite E.
CODE: `scripts/noise_tracker.gd` (player footsteps at night),
`GameState.noise()` → `noise_event(pos, loudness)`, `scripts/rundown.gd`
`_on_noise()` (heard-first relocation at BREAK), `_sign_finish()` emits
`noise_event(respawn_point(), 4.0)`; the dead room swallows noise
(`in_dead_room`).
ACCEPT: QA-13 (relocates toward noise within 12 s; the It-changed-direction
line fires once per run), I22 (every relocation-toward-noise names its
cause in coverage_log), I25 (deaf to the dead room), A08.
UE: `ARundown::ReportNoise` (present since 0.7); a footstep emitter on Rita;
the sign-log noise from the station actor.
P0: 0.7 (ReportNoise + relocation grammar). MILESTONE: P4.

## B · THE SCHEDULE AND THE HOUSE

### 4.4 Broadcast clock, wall clocks, ON AIR
CANON: design doc IV.3 (commercial breaks govern the compound); THE LAWS
Law 6 (the schedule is real); room inventory (clock repeaters, the ON AIR
master the player may never throw).
CODE: `scripts/broadcast.gd` ON_AIR_SECONDS=50.0 / BREAK_SECONDS=18.0,
`phase_changed`; `scripts/wall_clock.gd` (repeaters read the clock; readout
beneath the face).
ACCEPT: QA-10 (window holds honored except during cascade; ON AIR clock and
hum agree), I04 (holds obey the clock, yield only to the cascade).
UE: `URestorationClock` (present since 0.7, timer-driven); wall-clock actors
and the ON AIR sign material bind to its delegate.
P0: 0.7. MILESTONE: P3.

### 4.5 Doors, locks, keys and window holds
CANON: THE LAWS Law 11 (every threshold costs him 2.2 s); invariant I08
(every locked door states its reason); room inventory per-room gates;
Doors.csv kinds (blank / door / window / locked:reason|KEY).
CODE: `scripts/door.gd` (`_locked()` reads the reason and key id; window-bound
holds during ON AIR; demo reasons under DEMO), `ue/Restoration/Data/Doors.csv`
(20 rows, locked reasons intact).
ACCEPT: QA-10 (holds), QA-30 (demo reasons), I08 (data-enforced, manual
sweep for empty strings), I24 (the fold is paid: see 4.23).
UE: door actors stamped FROM Doors.csv by `ue/pyscripts/build_greybox.py`
(0.6 placed the slabs and floated the reasons as world text); the
interactable behaviour, key satisfaction and hold binding are the port.
P0: 0.6 (geometry + reasons). MILESTONE: P0 (walk) / P3 (holds).

### 4.6 Harriet: the holding pattern (H1, H2)
CANON: design doc (the holding pattern; transitional phrases); game master
(cup raised since Tape 1, comes down in Cue 4); casualty ledger H1 (the
slip) and H2 (the splice, doubled at the shoulders, scenery forever);
reaction matrix H-R1 (corrective beat) and H-R2 (freezes lengthen with
After-Fire active, the matrix's crown).
CODE: `scripts/harriet.gd` (sway ON AIR, freeze on BREAK, LINES, cup
height strictly rising by tape, `_splice_visual()` for the double, the
slip offer Day 2+ while frozen), `scripts/harriet_note.gd` (SEVENTH =
HOLD YOUR APPLAUSE, gated by her being alive and her card found).
ACCEPT: QA-09 (freeze, line, cup rises), QA-41 (H1 economy, seventh
unlearnable if card unfound, screenings 0.05 tighter), QA-49 (H2), QA-50
(grief frame 14), A06, A07.
UE: a character actor bound to the clock delegate; the double is a second
mesh offset one frame left. Reaction queue items H-R1/H-R2 land here.
MILESTONE: P3 (freeze) / P5 (deaths).

### 4.7 Merle: the schedule, the pen, 1974, M1
CANON: design doc (presenter cadence, the warmth is the leash); game
master T1.6, T2.5, T4.6 (the 1974 monologue), T5.2 (in the doorway
watching the pen); casualty ledger M1 (the second viewing) and M2 (the
home singer, premiere); reaction matrix M-R1..M-R6.
CODE: `scripts/merle.gd` (KETTLE / CHAIR / DOORWAY by schedule and
`_pen_up()`; `_monologue()` sets `merle_1974`; `screening_active`
awareness), `scripts/fire_tape_dock.gd` (the M1 offer and refusal).
ACCEPT: QA-11 (never elsewhere), QA-40 (M1 refusal saves her; consent
plays the repossession, the kettle caption, absence everywhere after; THE
BURN and NEW PRODUCER variants), A12.
UE: schedule-driven character actor; M2 is canon for the premiere's HOME
segment and is not in the reference code (see 4.34's deltas).
MILESTONE: P3 / P5.

### 4.8 Vess and the credit dilemma (V1, V2)
CANON: design doc (the plastic pin); game master T2.3 FORCE (the binder:
one insight, one wrong theory), T4.1, T4.5, T5.3 (the final breaker,
credited variant); casualty ledger V1 (credited, therefore cast) and V2
(the uncredited fix, cascade night, circuit F); reaction matrix V-R1..R3.
CODE: `scripts/vess.gd` (LINES by act), `scripts/vess_binder.gd`
(`vess_insight`), `scripts/credit_entry.gd` (the margin: `vess_credited`),
`scripts/decision_ledger.gd` `_v1_taken()`, `scripts/patchbay_console.gd`
`_v2_taken()` (GET VESS on the dead panel), `scripts/live_production.gd`
(the breaker beat and the 62 s crossing without him).
ACCEPT: QA-42 (both graves, INK ripple, GET VESS only for the uncredited
who used the insight), A11.
UE: same three interactables plus the two death hooks in the ledger and
the panel. MILESTONE: P5.

### 4.9 Drift: coat pegs, cup, casting sheet, chairs
CANON: dread doctrine L1 (ambient wrongness, monotonic, never called out);
object taxonomy (dressing is the ONLY drift-eligible tier); design doc
(casting-drift wardrobe; the casting sheet as a physical death counter).
CODE: `scripts/coat_pegs.gd` (NEUTRALS→SHOW palette by `_drift()` per day
table), `scripts/casting_sheet_prop.gd` (lines fill per capture),
`scripts/rec_chairs.gd` (CASUAL until the lockdown converts to ROWS, see
4.32); Harriet's cup lives in 4.6.
ACCEPT: QA-11 (pegs per day table), QA-56 (every drift resolves to the
dressing tier), QA-59 (ambient ledger items never move).
UE: material/transform drift driven from `URestorationState.Day`; no drift
on any interactable, ever (review rule).
MILESTONE: P3.

### 4.10 Day/night cycle, the bed, the morning
CANON: design doc Part II core loop (day bench / night traversal); game
master (tapes chapter days); achievements doctrine (the morning flush
gate); port notes state (`set_night(false)` caps the tape at min(day, 5)
and marks `run_complete` at day 3 on a morning).
CODE: `scripts/bed_prop.gd` (the day/night lever; declines under DEMO),
`GameState.set_night()` (day++, tape cap, `night_changed`, achievement
flush), `scripts/night_trip.gd` and `scripts/glimpse.gd` listen for night.
ACCEPT: QA-29 (morning shows FILED lines, never a toast between), QA-30
(bed declines in DEMO), QA-33 (`af_active` persists across the cycle).
UE: `SetNight` broadcast exists since 0.8b-2; the bed actor and the
morning flush are the port. P0: 0.8b-4 ("real day/night cycle").
MILESTONE: P3.

## C · THE BENCH

### 4.11 Tape stage, CRT stack, TBC, gen knob, the capture scare
CANON: design doc II (the two render worlds; artifact authenticity is
load-bearing), IV.1 capture, III (photosensitivity mode IS the TBC); THE
LAWS Law 2 (ONE STARTLE: the in-tape lunge); spike 1 (four generation
states, tool-reactive, safe mode); game master T1.5 SCARE 1.
CODE: `scripts/capture_bench.gd` CAPTURE_SECONDS=12.0, TETHER=4.0 (ported
in 0.8b-2), `scripts/tape_stage.gd` (the diorama; `play_tape`, the lunge
timeline, bars, `play_fire`, `play_screening`, `set_seance_frame`),
`scripts/bench_tv.gd` (crt_tape shader parameters generation / tbc /
photo_safe; `_on_lunge`), `scripts/gen_knob.gd` (MASTER / 1ST DUB / 3RD
GEN: the picture obeys, the scope does not), `GameState.set_tbc()`.
ACCEPT: QA-06 (12 real seconds, countdown, A CLEAN SIGNAL, bars), A02,
A03, I14 (Scare 1 is the only startle-class event; harness greps the
event table per build).
UE: the tape stage as a captured sublevel + Level Sequence with the lunge
as a one-frame track; crt_tape as a Material Function stack with the SAME
parameter names via a Material Parameter Collection. P0: 0.8b-2 (capture
loop). MILESTONE: P3.

### 4.12 Retake presentation, the dresser, the sheet, run death
CANON: walkthrough V-B (what a capture is: the take; the casting sheet
cap 4/7/0; what each capture takes; the final capture); gap audit ruling 6
(single NEXT WEEK'S EPISODE card, no per-location variants).
CODE: `GameState.strike()` (strikes, `items_lost`, `captured` signal,
respawn), `scripts/hud.gd` `_on_captured()` / `_on_run_ended()` (the
retake presentation, losses in order), `scripts/dresser.gd` (ITEM_ORDER,
loupe last, `_refresh()`), `scripts/casting_sheet_prop.gd`.
ACCEPT: QA-07 (losses in order, loupe last of seven), QA-08 (run death →
card → title, no credits), I16 (loss ordered and bounded, persists through
run end), I17 (sheet retirement honest: zeroes strikes, keeps losses, mints
no daily), A18, A19.
UE: `URestorationState::Strike()` core exists since 0.8a; the presentation
(UMG scrim + slate + count) and the dresser actor are the port. P0: 0.8a
(economy core), 0.8b-4 ("retake presentation"). MILESTONE: P3.

### 4.13 Dailies and the degausser (burn your dailies)
CANON: walkthrough V-B (a canister per capture in the stacks; degaussing
fades the name; unburned canisters are the Director's scouting film);
game master (Burn Your Dailies resets its read); H2 mints a shortcut daily.
CODE: `scripts/dailies_manager.gd` (SLOTS in the library; spawn on load and
per capture), `scripts/dailies_canister.gd`, `scripts/degausser.gd` (CLM
coil), `GameState.pick_daily()` / `burn_daily()` / `mint_shortcut_daily()`,
`daily_burned` → `CoverageDirector.reset_read()`.
ACCEPT: I09 (abort never costs a daily), QA-22 (the Destroy path shares
the coil, see 4.36), QA-49 (the shortcut daily mints immediately).
UE: canister actors from a slot table; the degausser as an interactable
that calls `BurnDaily` and broadcasts to the Director subsystem.
MILESTONE: P3.

### 4.14 Screening, stances, the beat, ASSIST
CANON: design doc IV.4 (Audience / Quiet / Improvise) and III (cue signs
RESPOND / HOLD); game master T1.7, T2.8 (the line to our new friend);
accessibility matrix (ASSIST widens the beat 0.2→0.35, stretches 1.5x,
never gates content); casualty ledger (0.05 tighter without Harriet).
CODE: `scripts/screening_event.gd` BEAT=0.8, WINDOW=3.2, `_on_beat()`,
SPACE on the beat / Q improvises (`add_pt(10)` or 5) / stillness is QUIET;
`scripts/cue_sign.gd` (`flash`, `set_lit`; never player-operable);
`GameState.set_assist()`.
ACCEPT: QA-18 (beat visibly forgiving, premiere clocks half again longer,
holding E passes both stillness checks), QA-41 (0.05 tighter), A04, A05.
UE: a screening director actor + cue-sign materials; ASSIST from the
settings save. P0: 0.8b-4 ("screening + assist"). MILESTONE: P3.

### 4.15 Audio bench and the four Sign-Off assets
CANON: design doc IV.1 (the spectrogram is the deep-dig instrument); game
master T2.6 (ASSET 1 the verse), T3.2 (ASSET 4 the script), T3.3 (ASSET 3
the cart), T4.3 (ASSET 2 the card); walkthrough VII (assets 0..4 gate the
Sign-Off variants and the audition clause).
CODE: `scripts/spectro_dock.gd` (the verse in the sidebands),
`scripts/asset_pickup.gd` (an asset where canon left it),
`scripts/asset_rack.gd` (ORDER = VERSE, CART, SCRIPT, CARD above the bench),
`GameState.gain_asset()` ("of 4" toast).
ACCEPT: QA-28 (the committed decision's ending plays; assets select the
variant, see 4.36); the ASK alternative (Harriet hums HERE for HOME, the
finale variant beat) is canon-only in code (delta, see 4.34).
UE: four pickups + the rack display bound to `Assets` in the SaveGame.
MILESTONE: P5.

### 4.16 Seance: frame stepping, wear, five answers, L1/L2, grief
CANON: design doc IV.7 (the frame-seance; wear is real and cumulative);
game master T4.4 (the five questions verbatim) and tunables (wear per pass
7/3.5; L1 offer past five answers AND wear over 70); casualty ledger L1
(the sixth question) and L2 (the reading); reaction matrix (grief answers
at frames 14 and 28); spike 3; controls map (Z / X frame back and forward).
CODE: `scripts/seance_dock.gd` (ANSWERS by frame, MAX_FRAME=40, `_step()`
adds wear, `_l1_sixth()`, `_l2_reading()` on Q with the fire tape),
`scripts/frame_sequence.gd` (deterministic frame per index, seeded grain,
W/H 320x240), `GameState.add_wear()`, `leland_answers` (frame indices,
deduped), `scripts/tape_stage.gd` `set_seance_frame()`.
ACCEPT: QA-22 (crate gates the seance; wear ladder degrades generations per
answer), QA-44 (L1 offered only past five answers AND wear over 70; L2
consumes the fire tape and sets the completed sign-off), QA-50 (frame 14
PAUSED PROPERLY with Harriet dead; frame 28 SHE'S HERE NOW with Merle
dead), I19 (gates on the crate), I20 (frame idx renders identically
forever), A14.
UE: `UTexture2D::CreateTransient` per index with the same seeded generator,
or an image-sequence Media Source; wear as a material parameter; the
answers table as a DataTable keyed by frame. MILESTONE: P5.

### 4.17 Readables, mark_read, the taxonomy sweeps
CANON: object taxonomy (handled lore prompts and marks read; AMBIENT LORE
NEVER PROMPTS; readables registry D01..D11 with homes per the Room Bible);
lore architecture (the three reads rule; the never-stated ledger is an S0
tripwire); `docs/canon/restoration-ambient-lore-ledger.md` (placement of
record); achievements A26 at ten documents.
CODE: `scripts/readable_prop.gd` (a found document; `_run()` reads it,
`GameState.mark_read(id)` "of 10" toast), `read_props` in the save.
ACCEPT: QA-55 (nothing ambient prompts), QA-56 (drift is dressing-only),
QA-57 (hero census), QA-59 (every ambient ledger item exists, prompts
nothing, never moves, reads at three depths; a graduated protected truth is
an S0), A26.
UE: readable actors from a landmark table (the Landmarks.csv extraction was
deferred at 0.5: "landmarks spawn in code", `scripts/world_builder.gd`);
Phase 3 rooms place the ambient tier FROM the ledger. MILESTONE: P5.

### 4.18 Producer Track (hidden)
CANON: design doc IV.8 (raised by restoration quality, accepted roles,
interesting improvisation; never a number; surfaced by tells; gates ending
2's audition clause at 70+); game master tunables (PT weights: A-captures
+10 each, T2 improvise +10, T4 gathering +10, read-through role +15,
audition at 70).
CODE: `GameState.add_pt()` (`pt` in the save), `scripts/screening_event.gd`
(+10 / +5 on Improvise), `scripts/hud.gd` binder page shows PRODUCER
TRACK as a debug line (canon says never shown: strip it for ship).
ACCEPT: QA-28 (ending routing), design doc IV.8 (never displayed as a
number — a text sweep, not a QA line yet; file one when 4.36 lands).
UE: an int on the state subsystem; the tells (address specificity, binder
stationery drift) are Phase 3/5 art wired to thresholds. MILESTONE: P5.

## D · THE HUNTER AND THE NIGHTS

### 4.19 Rundown night hunt: segments, warn/strike, savoring, camera kills
CANON: walkthrough V-B (the Rundown: segment audio is the map; it stares
cameras dead; aggression escalates per tape); game master Appendix C
(segment line pools); game master Appendix A (Coverage Director mood law:
last line earns savoring); spike 4.
CODE: `scripts/rundown.gd` (SEGMENTS with homes, MOVE_SPEED=2.4,
WARN_RADIUS=7.0, STRIKE_RADIUS=2.2, warn-once latch, savor at strikes ≥ 3,
no-strike-thru-wall raycast, camera kill within 14.0 of a rig while
walking, BASE_HEIGHT=2.6, HEAD_TILT=0.045, gait bob), `scripts/tone_emitter.gd`
(SEGMENT_FREQS 220/262/196 Hz: the segment audio that places him).
ACCEPT: QA-12 (warn at 7 m fills a ledger line; strike at 2.2 m; third
strike triggers savoring, not instant), QA-13 (noise relocation, see 4.3),
QA-14 (on-camera check prevents the strike, see 4.20), I01 (warning
precedes reach), I02 (no strike through walls), I03 (never hunts while
the show is live).
UE: `ARundown` (present since 0.7: warn latch, strike + savor rule, wall
ray, BREAK relocation, telemetry in the parser's dialect,
`ue/pyscripts/test_rundown.py`). Phase 4 closes: segment tone emitters,
camera kills against the rigs of 4.20, the pre-fire gait (the AF body's
motion is Phase 1's). P0: 0.7. MILESTONE: P4.

### 4.20 Frame Discipline: rigs, tallies, kills, revive, on-camera safety
CANON: design doc IV.2 (mediated viewing is safe; tally logic; shape-coded
lamps); THE LAWS Law 1 (ON CAMERA IS SAFE: an active camera cone prevents
the strike, always); spike 2 (twelve feeds; safety-state assertion
overlay still open); accessibility (tally pairs glow with REC text).
CODE: `scripts/monitor_rig.gd` (a camera somewhere else rendered onto a
wall set; `set_powered`, `set_killed`, `sync_to`, `get_feed_texture`),
`ue/Restoration/Data/Monitors.csv` (cam_pos, look_at, monitor_pos),
`scripts/rundown.gd` (the cone check before a strike), `scripts/patchbay_console.gd`
(revive-first re-patch).
ACCEPT: QA-14 (standing in an active cone prevents the strike; patchbay
revive works), I05 (on camera is safe), Law 1.
UE: `USceneCaptureComponent2D` → RT per feed (0.6b proved twelve at
116/96 fps; `ue/pyscripts/spike_wall.py` rebuilds the rig); tally
materials; the cone test in `ARundown`. Spike 2's remaining half is the
SAFE/EXPOSED assertion overlay — build it here. P0: 0.6b (feeds).
MILESTONE: P4.

### 4.21 Patchbay, power budget, night trip, the cascade, liveness
CANON: design doc IV.2 (the patchbay and the amperage budget; routing
builds mediated corridors; overdraw trips breakers in the worst order);
game master T2.2, T2.7 (first blood), Appendix B power shortfalls (ASK:
Merle's kitchen circuit; FORCE: cut dorm heat); spike 6 (full panel map,
the Night 4 cascade, liveness); invariant suite I04, I07; casualty V2.
CODE: `scripts/patchbay_console.gd` (routing v0: ONE budget, TWO circuits;
`apply_initial`, `_apply`, the V2 GET VESS branch), `scripts/night_trip.gd`
(night one: a breaker lets go, a feed dies; `night_tripped`),
`scripts/cascade.gd` (Night 4+: trip, spread, circuit C then B, `_kill_range`),
`scripts/liveness_check.gd` (OK cadence every 5 s to liveness_log;
VIOLATION on breach; "window holds waived" only while `cascade_active`).
ACCEPT: QA-19 (night 1 trip fires once ever), QA-20 (C then B; out of
order refuses with B BEFORE C; waived holds during), QA-42 (V2 fixes both
circuits then plays circuit F), I04, I07, A15.
DELTA: canon's full panel (room-inventory breaker map, the floodlight
trap, the spare-fuse drawer, kitchen circuit ASK) is beyond the v0 two
circuits; code is intent for the port, the panel scale is a Phase 3/4
extension the author sizes.
UE: a console actor + breaker actors; liveness as the same actor writing
the same log. MILESTONE: P4.

### 4.22 Floor Manager: signals, the watch, F1/F2
CANON: design doc (hand signals are the threat-telegraph UI; spoken
inventory: "In five, four..." and nothing else); game master T3.5 (the
you're-on), Appendix C signal glossary; walkthrough fail condition 4
(moving after the hand drop marks you as performance); casualty ledger F1
(the fader, Dead Air) and F2 (the unlisted camera: third blind tally call);
reaction matrix F-R1 (points at the doorway before the first fold), F-R2.
CODE: `scripts/floor_manager.gd` (nights, on air, at the stack's end; the
freeze watch fails on movement, passes on assist-hold),
`scripts/film_cabinet.gd` (the six taught signals, see 4.27),
`scripts/live_production.gd` (`_blind_calls` → F2 on the third; the fader
choice → F1), `scripts/harriet_note.gd` (the seventh).
ACCEPT: QA-19 (watch fails on movement, passes on assist-hold), QA-43
(exactly the third blind call; the unlisted-camera beats; F1 fader choice
precedes the crossing), I15 (the Floor Manager is never heard moving),
A07.
UE: a silent character actor with hand-pose states; the watch as a
stillness check reading Rita's velocity. MILESTONE: P4 / P5.

### 4.23 After-Fire layer: tally contract, cool, fold, dead room, crossing
CANON: THE LAWS Law 10 (the tally contract) and Law 11 (the two hides;
2.2 s per threshold); `docs/canon/restoration-after-fire-chum.md`;
`docs/canon/restoration-chum-motion-and-sound.md` (the pour, the fold, the
performance quote, the two-beat jaw); QA section J; invariants I23..I26.
CODE: `scripts/rundown.gd` AF layer: AF_APPROACH_SPEED=0.8, AF_LOOM_DIST=1.2,
AF_COOL_SECONDS=2.0 (first cool 4.0 with the teaching line, `af_taught`),
AF_HEIGHT=3.35, AF_FOLD_SECONDS=2.2, AF_DOOR_NEAR=1.0,
AF_CROSSING_SPEED=1.6, DEADROOM_DOOR hold and line, `_work_jaw()`,
`_door_fold_check()`; `GameState.in_dead_room()` rectangle; `recording` /
`recording_left` drive the HUD's REC · SAFE WHILE LIT countdown
(`scripts/hud.gd` `_process_tally()`); the eye light only while recording.
ACCEPT: QA-33 (wake toast once; `af_active` persists), QA-34 (approach at
0.8, footsteps on interval, REC countdown, stops at 1.2, first-sighting
toast once per save), QA-35 (eye red only while a capture runs), QA-36
(THE TALLY COOLS then strike; distance → withdraws; 4.0 once then 2.0),
QA-37 (every threshold 2.2 s, captioned, in approach AND hunt; two doors
buy 4.4 s), QA-38 (dead room: noise registers nowhere; he holds at the
felt door, says his line once; radio toast + [NO ECHO] on first entry),
I23 (no strike while lit), I24 (the fold is paid), I25, I26 (one cool
teaches). Motion acceptance QA-52 (one authored fold montage per door
width, head last), QA-53 (zero secondary on the AF body), QA-54 (audio
law; the two-beat jaw; bell never sounds; no vocalization) belong to Phase
1 units 1.9..1.12 and 5.1 and are listed here so the family is whole.
UE: ported in 0.8a (`ue/Restoration/Source/Restoration/Rundown.cpp`,
`ue/pyscripts/test_state_af.py`: approach → loom → cutoff → taught cool →
strike → hidden). Phase 4 closes: the captions, the two once-per-save
toasts, the dead-room radio toast, the countdown widget, QA-33..38 green in
the harness. P0: 0.8a. MILESTONE: P4.

### 4.24 Coverage Director
CANON: design doc IV-B.12 (reads camera-checker / sprinter / hider,
favored corridors, take history; blocking variants A/B/C; the poisoned-well
rule: monitor deception once per run, telegraphed by rising static; the
poltergeist layer never stages the dock; mood tracks the sheet); spike 5
(deterministic, explainable from the log); game master Appendix A
blockings table.
CODE: `scripts/coverage_director.gd` (counters `cov_monitor` / `cov_move`
/ `cov_still` persisted, `profile()` → CHECKER / SPRINTER / HIDER /
AUDIENCE, `most_watched_rig()`, `reset_read()` on `daily_burned`,
`log_line()` to coverage_log with reason strings); `scripts/rundown.gd`
consumes `director` for expressed blockings and the savor label.
ACCEPT: I21 (deterministic and explainable: identical inputs yield
identical profiles; every blocking decision carries a reason), I22 (its log
is the noise-attribution telemetry), the once-per-run poisoned well (a
review rule until a QA line exists; file it with 4.19's blockings).
UE: a WorldSubsystem; counters in the SaveGame; the append-only decision
log via FFileHelper in the parser's format. MILESTONE: P4.

### 4.25 Glimpse (once, ever)
CANON: THE LAWS Law 3 (once, ever; never referenced by any system; its
name appears in no code file); game master T4.8; walkthrough (under two
seconds, undecidable); achievements doctrine (no achievement, ever).
CODE: `scripts/glimpse.gd` (T4.8: the fire corridor unseals on Day 4;
`_fire()` once; `glimpse_seen` and `fire_unsealed` in the save).
ACCEPT: QA-25 (exactly once per save, never again after), I11 (never
repeats, including relaunch), I30 (no entry anywhere new).
UE: one actor, one flag, one Level Sequence; the naming law holds in C++
too (the class name says what the file does, not what he is).
MILESTONE: P5.

## E · STORY GATES AND THE FINALE

### 4.26 Log stations, paper, signatures, presigned page, respawn
CANON: walkthrough Part V (stations S1..S5; paper economy three lines per
station per tape on Late Night; the save scare, singular); gap audit ruling
7 (stations plus signatures only, no autosave; the signature IS the save);
game master T3.6; invariant I10.
CODE: `scripts/log_station.gd` (signing saves; `_presigned()` at S4 on Day
2+ with zero paper), `GameState.sign_log()` / `_sign_finish()` /
`paper_for()` / `mark_presigned()` / `register_station()` /
`respawn_point()` (last signature, else the fallback), the Harriet slip
(`harriet_slip` consumed on empty paper), `ue/Restoration/Data/Stations.csv`.
ACCEPT: QA-05 (paper decrements, save writes, pen-tick caption), QA-21
(presigned appears and saves free, once), I10 (costs no paper), A01, A09.
UE: five station actors from Stations.csv (0.6 placed the markers); paper
as the per-station TMap the 0.8b-3 delta list demands. P0: 0.8b-3 (save
shape), 0.8b-4 ("paper economy + stations + respawn"). MILESTONE: P2.

### 4.27 Film cabinet and the signal vocabulary; PRESERVE / ASK / FORCE
CANON: game master T2.4 (PRESERVE: the TRAINING key, six signals, G1; ASK:
Harriet's recital plus the seventh, G2; FORCE: pry it, four of six, G2);
design doc IV-B.10 (the three approach families and their cost
signatures) and IV-B.11 (generations: every G2 source carries one authored
gap); game master Appendix B (the whole solutions matrix).
CODE: `scripts/film_cabinet.gd` (needs `has_key("TRAINING")`; six signals
via `add_show_signal`; `film_watched`), `scripts/harriet_note.gd` (the
seventh, ASK), `scripts/vess_binder.gd` (FORCE for airdate math). The
FORCE branch of the cabinet (pry; four of six) and the ASK/FORCE branches
of the other matrix rows are canon-only in code.
ACCEPT: QA-41 (seventh unlearnable if her card was unfound), A07; the
matrix's law (generations never gate endings) is a review rule.
DELTA for ruling: the reference build ships the PRESERVE spine plus two
ASK/FORCE branches; the rest of Appendix B is a content list, not a system
— enumerate the remaining branches as Phase 4 content sub-boxes after the
author confirms scope (or accepts the built subset as the game).
UE: the cabinet as an interactable + a StringTable-driven film; signals as
a name set on the state subsystem. MILESTONE: P5.

### 4.28 Crate, fire tape (pickup, forced watch, M1 offer), the wake
CANON: game master T3.2 (the reel in Craik's cage), T3.4 (the forced watch:
no sting anywhere), T4.1 (the delivery); QA section J (the wake); casualty
ledger M1; reaction matrix L-R1 (carrying the fire tape past his shelves:
NOT THAT ONE. PLEASE.) and M-R4 (she never says his name after the tape
exists).
CODE: `scripts/impossible_crate.gd` (`crate_opened` gates the seance),
`scripts/fire_tape_pickup.gd` (`has_fire_tape`), `scripts/fire_tape_dock.gd`
(the forced watch; `fire_tape_watched`; the M1 offer; sets `af_active`:
the wake).
ACCEPT: QA-22 (crate before seance refuses), QA-23 (forced watch, no
sting, flag marked), QA-33 (wake toast once), QA-40 (M1), I15 (the fire
tape carries no sting), I19, A13.
UE: three interactables; the watch as a Level Sequence over the tape
stage with the audio bible's silence enforced by asset review.
MILESTONE: P5.

### 4.29 Dock inventory and the warm one
CANON: THE LAWS Law 4 (THE WARM ONE NEVER ACTS; nothing follows filing
it); game master T4.3 (ASSET 2 in the props crate); design doc IV-B.12
(the poltergeist layer never stages the dock); walkthrough (nothing
springs in the dock); achievements (A10 text never mentions warmth).
CODE: `scripts/dock_task.gd` (six units, one anomaly, zero incidents;
`is_warm()`, `notify_counted()`, `dock_done`), `scripts/dock_chum.gd` (a
retired unit; the warm one: nothing further, ever).
ACCEPT: QA-24 (filing all six completes with nothing following; on camera
or off), I12 (no code path exists; a review rule on every future commit),
I19 (the card gates on the filed inventory), A10.
UE: the rows are Phase 1/3 art on armatures; the task is one clipboard
interactable and six touch targets. MILESTONE: P5.

### 4.30 Rejected edit (H2 temptation)
CANON: game master T4.5 (Vess's cut, played in full; the reel stops itself
and reverses one rotation); casualty ledger H2 (splicing her segment
doubles her; the temptation discloses her label).
CODE: `scripts/rejected_edit.gd` (`rejected_seen`; `_splice()` offers the
shortcut daily with the label disclosed; sets `h2_pending`), `scripts/harriet.gd`
(the double at the next break).
ACCEPT: QA-49 (offer after the viewing; daily mints immediately; NEXT break
doubles her; persists through save/load).
UE: one interactable + the projector sequence; the H2 flag rides in the
SaveGame. MILESTONE: P5.

### 4.31 Keys: TRAINING, EDITH, QUIET ROOM; the shed; FORCE instruments
CANON: game master T2.4 (TRAINING on Merle's board, Leland's green tag),
T4.7 (the shed: PRESERVE EDITH key; ASK Vess trades for a credit; FORCE
bolt cutters or drilling the dead room door: the seal is never perfect
again, hummed epilogue, one surviving copy); room inventory (tool wall:
BOLT CUTTERS and the DRILL, taking either logs itself; the kitchen key
board).
CODE: `scripts/key_item.gd` (a key where it was left; taking it is
remembered: `take_key`), `scripts/world_builder.gd` spawns EDITH (KEY
BOARD) and TRAINING when not held; `has_key("QUIET ROOM")` gates the felt
door (Doors.csv) and the divert. No bolt cutters, no drill, no Vess trade
exist in the reference code.
ACCEPT: A16 (the felt door has a key after all); the FORCE consequences
(hairline hum, the post-credit canister) are canon-only.
DELTA for ruling: the FORCE instruments and the ASK trade are unbuilt
branches of the solutions matrix (see 4.27's ruling).
UE: key pickups from the landmark table; `Keys` array in the SaveGame.
MILESTONE: P5.

### 4.32 Lockdown
CANON: game master T4.10 (every monitor the same frame; doors seal on
schedule; chairs in rows; the RESPOND sign burns steady); invariant I18
(permanent through reload).
CODE: `scripts/lockdown.gd` (`_fire()` once; `_apply(silent)` re-applies on
ready: monitors `sync_to` one feed, doors read SEALED FOR BROADCAST, chairs
tween to ROWS), `scripts/rec_chairs.gd`, `lockdown_done` in the save.
ACCEPT: QA-26 (sync, SEALED FOR BROADCAST, rows persist), I18, A20.
UE: one director actor; sync = one RT assigned to many screen materials
(migration map). MILESTONE: P5.

### 4.33 Decision ledger (AUTHENTICATE / DESTROY / PERFORM)
CANON: game master T5.2 (three entries in her hand; Merle in the doorway;
no music; the pen is the loudest thing); walkthrough VII routing summary;
casualty ledger V1 (AUTHENTICATE while credited takes him); design doc gap
4 (unmistakable point of no return without a modal).
CODE: `scripts/decision_ledger.gd` (CHOICES, COMMIT_LINES, `is_pen_up()`
read by Merle's DOORWAY schedule, `_v1_taken()` after the INK ripple,
`GameState.start_finale()` → `finale_started(decision)`).
ACCEPT: QA-42 (V1 on AUTHENTICATE while credited, after INK), A17, QA-28
(the committed decision's ending plays).
UE: one interactable with a three-way hold; `Decision` string in the
SaveGame. MILESTONE: P5.

### 4.34 Live production: cues, incidents, fixtures, breaker, rows, ending 0
CANON: design doc IV.9 (live production under sabotage; switcher on face
buttons one to one); game master T5.3 (Cues 1..5 verbatim; SCARE 10 the
bell; SCARE 11 the plunge; SCARE 12 the delivery; the final breaker
variants); casualty ledger THE ROWS (each incident abandoned past guarantee
takes a seat), M2 (the home singer), ENDING 0; invariant suite I03, I05,
I06; spike 7; gap audit ruling 3 (binder is LIVE-TIME during the premiere
only); THE LAWS Law 5 (the bell rings once, at the finale beat, captioned).
CODE: `scripts/live_production.gd` (MARK, INCIDENTS TALLY / HOUSE / BOOM /
CARDS with FIX_LINES, `_pgm` from cam_1..3, `_on_mark_press`, `_timed()`
takes with `_fail_takes`, club auto-fix guarantees, `_tally_refusals`,
`_boom_held`, `_blind_calls`, the cart-deck breaker at 45 s, the rows,
`_one_woman()` intercept when `all_cast_dead()`, the little door),
`scripts/finale_fixture.gd`, `scripts/finale_breaker.gd`, `Sfx.bell()`
(`scripts/sfx.gd`, two inharmonic partials, once).
ACCEPT: QA-27 (cue marks require the PGM camera; each incident fail-forwards
within its guarantee), QA-42 (the credited living die at the final breaker
AFTER the farewell), QA-45 (ENDING 0 intercepts at entry; nine cards, one
name), QA-46 (rows: every expired incident takes a seat, cycling three
lines; count persists), QA-51 (braid audit: two simultaneous demands at
every pressure peak), I03, I05, I06 (RESOLVED with club auto-fix at or
under 40 s; tally refusals never exceed 2; boom holds exactly 1), A28.
DELTA: M2 (Merle on the call sheet for the HOME segment) and the
delivery scare's physical restraint are canon without reference code;
size with the author before P5.
UE: a GameMode-scoped director actor; cue marks as trigger volumes; the
switcher as Enhanced Input actions; premiere_log unchanged; the binder's
live-time wiring per ruling 3. MILESTONE: P5.

### 4.35 Crossing and the divert: Dead Air 4a / 4b / 4c
CANON: game master ENDING 4 (the divert during the final break: STA to TH
to DR, the felt door closed; the radio; the erase loop; the FORCE-path
hum variant); casualty ledger F1 (his hand 4a / her hand 4b: self-hold pays
13 s and an arm) and L2 (4c the completed sign-off, the break ends
itself); walkthrough addendum c043 (75 s base, 62 without Vess, minus 13
self-held; two folds on the honest route); controls map (SPACE for his
hand, E held 4.6 s for hers; FADER SELF-HOLD shares the capture trigger).
CODE: `scripts/live_production.gd` (the divert window gated on
`has_key("QUIET ROOM")` AND five answers AND `fire_tape_watched`; the
fader choice; `crossing` / `crossing_caught` / `fader_self` on the state;
the 4c branch when `signoff_completed`), `scripts/rundown.gd`
AF_CROSSING_SPEED=1.6 ("he declines to look up"), `scripts/hud.gd`
`_end_dead_air()` / `_end_4c()`.
ACCEPT: QA-28 (divert with the fire tape plays DEAD AIR; otherwise the
committed decision's ending), QA-43 (self-hold costs 13 s and routes 4b;
his hold routes 4a with the casualty inside the epilogue; forced self-hold
if he is dead), QA-44 (L2 → 4c with no divert prompt), I19 (the divert
gates on key plus answers plus the fire tape), A25.
UE: the same director actor; the crossing as an `ARundown` state (present
in 0.8a's AF layer as a stub). MILESTONE: P5.

### 4.36 Endings, credits, the reading, the one lie
CANON: game master THE ENDINGS SCRIPTED (1A, 1B, 2, 3, 4) and the post-
credits interface lie; walkthrough VII (exact conditions: PERFORM + 4/4 +
LI; AUTHENTICATE or PERFORM under four at PT 70+; DESTROY via degausser
and oven from Tape 4); casualty ledger THE FULL BOARD (1A needs Leland
intact; 1B collects memorial cards; 2 gains furniture per death; 3 cold
cobbler; 4a/4b/4c; 0); THE LAWS Law 8 (the interface lies exactly once);
invariants I13, I28, I29.
CODE: `scripts/hud.gd` `_on_finale()` → `_end_burn()` / `_end_producer()`
/ `_end_perform()` (1A vs 1B by `leland_answers` and wear) / `_end_dead_air()`
/ `_end_4c()` / `_end_zero()`, `_roll_credits(label)`; `GameState.mark_ending(name, lie)`
(`ending_reached`, `finale_done`, `lie_pending`); `scripts/title.gd` (the
lie spent once on the next launch: CONTINUE? and NEW EPISODE, then
reverts); `scripts/credits.gd` (THE LEDGER, READ ALOUD opens every credits
when anything is in it); `scripts/achievements.gd` ENDING_MAP.
ACCEPT: QA-28 (ending exits roll credits), QA-45 (ending 0 credits), QA-47
(the reading opens every ending's credits including fifty-eight minus N; a
clean run reads nothing and files A27), I13 (relaunch twice: the lie flips
once), I28 (every reading matches the binder page exactly), I29 (clean
hands are silent), A21..A25 (the five ending cards; A25's all-black icon),
A27, A28.
UE: ending sequences as Level Sequences driven by the director; the lie as
a main-menu widget state read from the SaveGame's `LiePending`; credits as
a UMG crawl reading the casualty array. MILESTONE: P5 / P6.

### 4.37 Casualty ledger and ripples (the reaction matrix)
CANON: THE LAWS Law 7 (every death has a signature; the binder names it);
`docs/canon/restoration-casualty-ledger.md` (ten deaths, the rows, ripples
per death, ending effects); `docs/canon/restoration-reaction-matrix.md`
(THE WEB LAW; QUEUE items M-R1..R6, V-R1..R3, H-R1..R2, F-R1..R2, L-R1,
B-R1..R2 in the 045/046/047 wiring order); invariant I27.
CODE: `GameState.mark_casualty(who, cause, epitaph)` (idempotent),
`casualties` array, `row_casualties`, `cause_of()`, `is_dead()`,
`all_cast_dead()`; `scripts/hud.gd` `_fill_binder()` page one (NO ENTRIES.
KEEP IT SO.); BUILT ripples per the matrix (the kettle click-off, cold
cobbler, grief answers, her doubled state, the open headset).
ACCEPT: QA-39 (page one until a death; then who, cause, day, epitaph),
QA-46 (rows), I27 (deaths are idempotent: no double entries, no double
toasts). The QUEUE items are the 4.WEB audit's worklist, one QA line each
as they land.
UE: the casualty array as a TArray of structs in the SaveGame (0.8b-3
delta list); each ripple is a delegate listener on `mark_casualty`.
MILESTONE: P5.

### 4.38 Secret ending: the unnumbered reels, ENDING A (CANON-ONLY)
CANON: walkthrough ADDENDUM · SPOILER · THE SECRET (c046): four clean
dailies first; W1 in the library skip gap (Day 2) → W2 behind the burn
barrel (Day 3) → W3 on the shed shelf (Day 4); each viewing consumes one
S2 slip; CONFIRM the dead-room radio's dial; the final break gains a
caption (a radio, through three walls); Q within six seconds starts the
75 s run; ENDING A · AUDIENCE ONLY with her single credit card; the
exclusive post-credits PROGRAM GUIDE; 58 · STILL ON on the title forever;
no achievement by design.
CODE: NONE. `scripts/` contains no W1/W2/W3 reels, no radio dial confirm,
no ENDING A branch, no STILL ON title mark, and `translations/strings.csv`
carries none of its text. The addendum's "c046" is a doc-era commit number
that does not correspond to this repo's Commit 046 (the machine shop).
ACCEPT: QA-60, QA-61 are written against it and cannot pass on the
reference build today.
RULING NEEDED (blocking for this box only): (a) build ENDING A in UE from
canon with the reference build's grammar (it is the only mechanic whose
spec is prose alone), or (b) strike QA-60/61 and the addendum from the
acceptance suite. Recommendation: (a), after P5, as its own box, because
the ending is the lore architecture's thesis (Leland's warning, obeyed
completely, wins) and its cost is one interactable, three pickups, one
title flag and a credits variant.
UE: not before the ruling. MILESTONE: P5+ (author's call).

## F · META AND MODES

### 4.39 Binder: pause, map, pages, intermission
CANON: design doc III (meta UI is station paperwork; the binder is pause,
settings, saves, journal); gap audit rulings 3 (true-pause by day, LIVE-TIME
during the premiere) and 4 (THE BINDER IS THE INVENTORY: no grid, no
weight; possession is recorded); accessibility (INTERMISSION pauses
everything honestly; the schedule board states today's obligations).
CODE: `scripts/hud.gd` (`_toggle_pause()`, `_fill_binder()`,
`_fill_form()`, `objective_text()`, casualty page, `pause_requested`),
`scripts/map_view.gd` (M: drawn live from the room table; sealed rooms
dashed; station dots; LANDMARKS; the BOUND map key footer).
ACCEPT: QA-15 (map), QA-32 (pause holds world and clocks, mutes audio;
refused during any authored sequence), QA-39 (page one).
UE: UMG widgets; the map redraws from the Rooms DataTable via OnPaint
(migration map); pause policy per ruling 3. MILESTONE: P6.

### 4.40 Booth: settings, remap, assist, captions, photo-safe, scale
CANON: THE LAWS Law 9 (ACCESS IS CANON: booth, captions, assist, remap,
pause, deferral ship in every build); `docs/canon/restoration-accessibility-matrix.md`
(text scale 0.8..1.6, high-contrast map, TBC and photo-safe, captions with
source tags, full remap, hold-to-toggle with durations preserved, ASSIST
never gates); `docs/production/restoration-accessibility-conformance-pass.md`
(R1..R7 shipped); controls map (five verbs remappable today, everything in
UE; conflict refusal); design doc III (the booth opens BEFORE first play).
CODE: `scripts/options_panel.gd` (every control enumerated: sliders,
checks, `_remap_row` with KEY IN USE refusal), `GameState.load_settings()`
/ `save_settings()` (settings.cfg: mouse_sens 0.2..3.0, ui_scale 0.8..1.6,
captions, assist, the five REMAP_ACTIONS), `set_captions()`,
`show_caption()`, `set_photo_safe()`, `set_ui_scale()`.
ACCEPT: QA-01 (first launch opens the booth over the title; relaunch does
not re-prompt), QA-16 (every slider and check persists; NEW GAME leaves
settings intact), QA-17 (remap refusal and propagation), QA-18 (ASSIST).
UE: the settings file is NOT the SaveGame (port notes state §4); UMG booth
bound to a settings USaveGame or GameUserSettings subclass; every action
remappable via Enhanced Input. MILESTONE: P6.

### 4.41 Title, boot, credits crawl, FILED WHILE YOU WERE OUT
CANON: QA section A; achievements doctrine (flush at the title); the
interface lie (4.36) lives on this screen; the lockdown-era static card.
CODE: `scripts/title.gd` (channel dark, the card, the menu, phosphor focus
ring, the pending-achievements card, the lie), `scripts/credits.gd`
(SPEED 42.0 crawl, grace then any key skips, tower-light card holds,
returns to title).
ACCEPT: QA-02 (Tab focus ring, Enter activates), QA-03 (credits from
title), QA-04 (FILED WHILE YOU WERE OUT exactly once).
UE: UMG title + credits; the same focus discipline. MILESTONE: P6.

### 4.42 Achievements: deferral, flush gates, meta-silence
CANON: `docs/production/restoration-achievements-design.md` (the deferral
rule: silent queue, flush at the morning toast or the title; the
meta-silence ledger: the glimpse has no achievement, ever; Chum's name in
no title; A27/A28 the only casualty additions; 4c has none by design);
THE LAWS Law 5 (Chum has no achievement title) and Law 3 (the once-ever
moment has no entry anywhere).
CODE: `scripts/achievements.gd` (TITLES A01..A28, ENDING_MAP, `unlock()`
idempotent, `pending()`, `flush_to_toasts()` on `night_changed(false)`,
`flush_silent()` at title, achievements.cfg, disabled under DEMO).
ACCEPT: QA-29 (no toast between title and morning), QA-48 (demo: dark),
I30 (meta-silence holds at scale: no death, ending 0 included, toasts
mid-play), A01..A28 as the id table (Steam bridge later).
UE: a GameInstance subsystem with the same two flush gates; Steam
achievement ids are the A-codes. MILESTONE: P6.

### 4.43 Modes: Late Night / Matinee / One Take vs the ASSIST-only ruling
CANON: design doc II (Late Night and Matinee, framed diegetically; Matinee
is first-class); walkthrough V-B modes (4 / 7 / 0 sheet lines, paper on or
unlimited, halved wear); gap audit ruling 5: "DIFFICULTY: RULED, ASSIST
only. One game, honestly tuned."
CODE: `GameState.set_mode()` (Mode enum MATINEE=0, LATE_NIGHT=1,
ONE_TAKE=2; `mode` is v16 save key 2, default LATE_NIGHT), the sheet cap
in `strike()` (full at 4, or any strike in ONE_TAKE).
ACCEPT: QA-08 (One Take run death), QA-18 (ASSIST is the only sanctioned
relief), QA-31 (a loaded save keeps its mode).
DELTA for ruling: the ruling says one game plus ASSIST; the code (the
intent) still carries three modes in the save. Recommendation: keep the
field and the enum for save semantics (migration map: the save's semantic
fields must not change), ship LATE_NIGHT as the only selectable mode, and
let Matinee's numbers stay as the ASSIST profile's tuning if the author
wants them. Decide before the booth (4.40) is built.
UE: `Mode` int on the SaveGame (present since 0.8a; default fix in
0.8b-3). MILESTONE: P2 / P6.

### 4.44 DEMO build (Tape 1): whitelist, funnel, stripping
CANON: `docs/production/restoration-demo-cut-plan.md` (E1..E10),
`ue/Restoration/Data/DemoOpen.csv` (the seven rooms), port notes state §5
(what the demo strips), casualty ledger (a full-game save with Merle dead
refuses to load forward), achievements (disabled under DEMO).
CODE: `GameState.DEMO` build flag, `demo_mark()` (the funnel file, six
marks), the save whitelist in `_save_dict()`, `demo_ended` signal,
`scripts/hud.gd` `_on_demo_end()` (the card protects three seconds),
`scripts/door.gd` demo reasons, `scripts/bed_prop.gd` declines, stations
S1 and S5 only.
ACCEPT: QA-30 (seven rooms, demo reasons, bed declines, S1/S5, card three
seconds, whitelisted-out fields absent, six funnel marks), QA-48 (no death
reachable; no casualty field survives; achievements dark).
UE: a build configuration flag read by the world stamper and the SaveGame
serializer. MILESTONE: P6.

### 4.45 Save integrity and migration (defaults are the migration)
CANON: gap audit (save-migration policy once v17 exists); port notes state
§1 (55 keys; every key read with a default; v<16 re-saves and toasts LOG
MIGRATED; v>16 toasts LOG FROM A NEWER BUILD; there is no per-version
upgrade code and there must not be); migration map (the save's semantic
fields must not change); walkthrough Part V (what saves guard; the burn-in
rule: wear, splices, dailies survive retakes and reloads).
CODE: `scripts/game_state.gd` `_save_dict()` / `load_log()` / `save_log()`
(written at the moment of every mutating act; no autosave timer),
`reset_new_game()` (eight fields carry across runs; `ng_relic` computed:
the one New Game Plus nod, gap audit ruling 9), `_announce_migration()`,
SAVE_VERSION=16.
ACCEPT: QA-31 (load a v15 save: migration toast, nothing lost, settings
untouched), QA-16 (NEW GAME leaves settings intact), I16 (losses persist
through run end), I18 (lockdown survives reload), I20 (the same frame is
the same frame after reload).
UE: `URestorationSaveGame` (0.8a) brought to the full schema by 0.8b-3;
this box is the 4.SAVE audit's mechanics: the round-trip matrix per ending
(I13, I16..I19) in 0.9's harness. P0: 0.8a, 0.8b-3. MILESTONE: P2.

### 4.46 Strings, captions and telemetry formats
CANON: port brief §3 (GameText as a StringTable; source strings are the
keys); `docs/production/restoration-localization-plan.md`; accessibility
HEARING (captions with source tags; band-limited sources caption in
brackets, full-range plain; directional tags in UE); migration map WHAT
MUST NOT CHANGE (log formats, the silence ledger); invariant suite F (the
three logs feed one INVARIANTS.txt scorecard).
CODE: `translations/strings.csv` (714 keys → `ue/Restoration/Data/GameText.csv`,
`tools/extract_strings.py`, `tools/extract_data.py`), `GameState.show_caption()`
/ `caption` signal (THE BELL, doors, the pen tick), the three log writers
(`scripts/coverage_director.gd` coverage_log, `scripts/liveness_check.gd`
liveness_log, `scripts/live_production.gd` premiere_log) and their reader
`scripts/invariant_parser.gd`.
ACCEPT: QA-05 (pen-tick caption when captions on), QA-37 (the fold is
captioned), QA-54's caption half (the bell's caption says it rang once),
I21 / I22 (log lines carry reasons and positions in the parser's dialect).
UE: StringTable import; the decision log already writes ForceUTF8WithoutBOM
in the parser's exact format (0.8b-2 lesson); captions as a UMG caption
bar bound to a `Caption` delegate with source and direction tags.
MILESTONE: P6 (strings) / P4 (logs, with 0.9).

## G · CANON-ONLY MECHANICS (no reference code; ruling before any port)

These are named in the design doc or the walkthrough and have NO home in
`scripts/`. The port brief's law (the code is the intent) means none of
them is in the acceptance suite today; each needs the author to either
size it as a Phase 4 sub-box or strike it from the design canon. They are
enumerated so the decision is explicit rather than forgotten.

### 4.47 Avert and held direct sight
CANON: design doc IV.2 (Avert: hold to raise the clipboard, slow walk;
direct sight frees it), Part V controls (Hold LB / Hold Q), walkthrough
fail condition 2 (gaze past about one second frees it; glances survive),
game master tunables (sight grace about 1 s).
CODE: none. The reference threat model is radius + camera cone + the two
hides (`scripts/rundown.gd`; `scripts/coverage_director.gd` reads facing
only to profile checkers). Q is IMPROVISE in the shipped controls map.
RULING: recommend PARK. Law 1 and Law 11 already define safety (the lit
hide and the dead room); an avert verb would be a third hide and would
touch I31's "no code path reads posture" spirit. If kept, it needs its own
invariant and a controls-map revision first.

### 4.48 Bench sub-tools: bake, splice, quality grade, GEN field
CANON: design doc IV.1 (bake: temperature-and-time hold; splice: precision
surgery with permanent consequences; quality grade on the club's rubric,
feeding PT and hostility) and IV-B.11 (the accession log's GEN field the
player fills); game master T1.3 (the tutorial names bake and splice);
walkthrough V (splice surgery burns in).
CODE: none as tools. The bench verb is CAPTURE only (4.11); the only
splice is H2's temptation (4.30); the gen knob (4.11) is a display, not a
field the player fills; there is no grade.
RULING: recommend building the GEN field as a ledger stance (cheap, and
it is the deduction system's commitment device) and parking bake, splice
and the grade until Phase 4 content is scoped: the grade in particular
would give PT a visible input, which IV.8 forbids being shown.

### 4.49 Level mechanics: compactus, catwalk route, airdate math, light table, radio tuning
CANON: walkthrough II/III (compactus rolling stacks: player-cranked walls,
the T3 chase geometry; catwalks: the one space above the format, noise
toll, ladder exposure; break windows as pacing skeleton); design doc IV.6
(airdate math interface; the light table; the dead room radio, tunable);
game master T2.3 (the four airdate sources), T3.5 (the compactus chase);
room inventory (LIB, CAT, DR rows).
CODE: none. `scripts/world_builder.gd` defers the catwalks ("vertical
greybox arrives with Studio A's grid pass") and has no compactus; airdate
math exists only as readables (4.17) with the FORCE branch via the binder
(4.8); the radio is a toast (4.23) and the Dead Air instrument (4.35), not
a tuner.
RULING: these are room mechanics and belong to the Phase 3 room units
(3.8 TAPE LIBRARY, 3.15 STUDIO A, 3.18 DEAD ROOM) as their hero
interactables, with a Phase 4 sub-box each only if the author wants them
systemic. Note QA-57 (one hero per room) caps how many can land.

### 4.50 Input canon: Quiet Game mic, Improvise wheel, one-to-one switcher pad map, photo mode Tier B
CANON: design doc IV.5 (optional microphone breath with a button
equivalent), Part V (Y opens the Improvise wheel; switcher face buttons
map one to one to the console), accessibility MOTOR (no QTEs; one-hand
viability), controls map CONTROLLER (RT is the capture hold; the fader
shares it), gap audit ruling 8 (photo mode Tier B, studio-safe, day, never
him).
CODE: none. Stances are single keys (SPACE / Q / stillness, 4.14); the
switcher is cam_1..3 on number keys (4.34); no mic; `photo_safe` (4.40)
is the photosensitivity toggle, not photo mode.
RULING: the controller map is P6's Enhanced Input context (rows already
specified in the controls map); the mic is optional by canon and can stay
parked without breaking Law 9; photo mode Tier B is a Phase 5.2 item.
Enumerated here so P6 sizes them, not so P4 builds them.

---

## PHASE-0 OWNERSHIP (who already carries part of a box)

| P0 unit | Boxes it seeded | What Phase 4 still closes |
|---|---|---|
| 0.6 greybox | 4.5, 4.26 | door behaviour, station behaviour |
| 0.6b spike 2 | 4.20 | tallies, kills, revive, the SAFE/EXPOSED assertion |
| 0.7 ARundown + clock | 4.3, 4.4, 4.19 | segment audio, camera kills, wall clocks |
| 0.8a state + AF layer | 4.12, 4.23, 4.43, 4.45 | presentation, captions/toasts, mode ruling |
| 0.8b-1 Rita | 4.1, 4.2 | reach ruling, crouch audit |
| 0.8b-2 bench | 4.11 | tape stage, CRT stack, the one startle |
| 0.8b-3 save parity | 4.26, 4.37, 4.45 | (shape only) |
| 0.8b-4 P3 remainder | 4.10, 4.12, 4.14, 4.26 | QA-06..11, QA-18 green |
| 0.9 harness | every I-line above | the three bots + parser in UE |

## DELTAS AND RULINGS NEEDED (collected)

1. 4.38 the secret ending: canon has it, code does not (QA-60/61 cannot
   pass). Build from canon or strike. Recommend build, after P5.
2. 4.43 modes vs ruling 5 (ASSIST only): keep the save field, ship one
   selectable mode. Decide before the booth.
3. 4.27 / 4.31 the solutions matrix: the reference ships the PRESERVE spine
   plus two ASK/FORCE branches; the rest (pry the cabinet, Vess's trade,
   bolt cutters, the drill, the kitchen circuit, Harriet's hummed verse) is
   unbuilt content. Enumerate as sub-boxes once the author confirms scope.
4. 4.21 the power panel: v0 is two circuits, one budget; canon is a
   building-scale routing puzzle. Size it.
5. 4.34 M2 and the delivery scare's restraint: premiere content without
   reference code.
6. 4.18 the HUD's PRODUCER TRACK debug line must not ship (IV.8).
7. 4.1 reach: code says 2.6 m, ruling says 2.1 m / 35 degrees pending the
   device pass. Code stands until the pass.
8. 4.47..4.50 canon-only mechanics: park, room-unit, or P6 per the notes.

## SCRIPT INDEX

Every file in `scripts/` (73), placed. Owner is the box that ports it, or
EXCLUDED with the unit that owns it instead.

| Script | Owner |
|---|---|
| `achievements.gd` | 4.42 |
| `arm_preview.gd` | EXCLUDED — dev preview tool (Phase 1 arm check) |
| `asset_pickup.gd` | 4.15 |
| `asset_rack.gd` | 4.15 |
| `bed_prop.gd` | 4.10 |
| `bench_tv.gd` | 4.11 |
| `bot_driver.gd` | EXCLUDED — 0.9 harness (the three bots) |
| `broadcast.gd` | 4.4 |
| `capture_bench.gd` | 4.11 (ported 0.8b-2) |
| `cascade.gd` | 4.21 |
| `cast_preview.gd` | EXCLUDED — dev preview tool (Phase 2 lineup) |
| `casting_sheet_prop.gd` | 4.12 |
| `character_kit.gd` | EXCLUDED — Phase 2 art (the cast bodies) |
| `coat_pegs.gd` | 4.9 |
| `coverage_director.gd` | 4.24 |
| `credit_entry.gd` | 4.8 |
| `credits.gd` | 4.41 |
| `cue_sign.gd` | 4.14 |
| `dailies_canister.gd` | 4.13 |
| `dailies_manager.gd` | 4.13 |
| `decision_ledger.gd` | 4.33 |
| `degausser.gd` | 4.13 |
| `dock_chum.gd` | 4.29 |
| `dock_task.gd` | 4.29 |
| `door.gd` | 4.5 |
| `dresser.gd` | 4.12 |
| `film_cabinet.gd` | 4.27 |
| `finale_breaker.gd` | 4.34 |
| `finale_fixture.gd` | 4.34 |
| `fire_tape_dock.gd` | 4.28 |
| `fire_tape_pickup.gd` | 4.28 |
| `floor_manager.gd` | 4.22 |
| `frame_sequence.gd` | 4.16 |
| `game_state.gd` | 4.45 (shape via 0.8b-3) |
| `gen_knob.gd` | 4.11 |
| `glimpse.gd` | 4.25 |
| `harriet.gd` | 4.6 |
| `harriet_note.gd` | 4.6 |
| `head_preview.gd` | EXCLUDED — dev preview tool (Phase 1 head check) |
| `hud.gd` | 4.39 (retake 4.12, tally 4.23, endings 4.36) |
| `impossible_crate.gd` | 4.28 |
| `interactable.gd` | 4.1 |
| `invariant_parser.gd` | EXCLUDED — 0.9 harness (the scorecard) |
| `key_item.gd` | 4.31 |
| `live_production.gd` | 4.34 (divert 4.35) |
| `liveness_check.gd` | 4.21 |
| `lockdown.gd` | 4.32 |
| `log_station.gd` | 4.26 |
| `map_view.gd` | 4.39 |
| `merle.gd` | 4.7 |
| `monitor_rig.gd` | 4.20 |
| `night_trip.gd` | 4.21 |
| `noise_tracker.gd` | 4.3 |
| `options_panel.gd` | 4.40 |
| `patchbay_console.gd` | 4.21 |
| `player.gd` | 4.1 (crouch 4.2) |
| `prop_kit.gd` | EXCLUDED — Phase 3 art (the props pass as code) |
| `readable_prop.gd` | 4.17 |
| `rec_chairs.gd` | 4.9 (lockdown 4.32) |
| `rejected_edit.gd` | 4.30 |
| `rundown.gd` | 4.19 (AF layer 4.23) |
| `screening_event.gd` | 4.14 |
| `seance_dock.gd` | 4.16 |
| `sfx.gd` | EXCLUDED — Phase 5.1 audio (bell / tick / thunk → MetaSounds; Law 5 holds there) |
| `soak_runner.gd` | EXCLUDED — 0.9 harness (headless entry) |
| `spectro_dock.gd` | 4.15 |
| `tape_stage.gd` | 4.11 |
| `title.gd` | 4.41 |
| `tone_emitter.gd` | 4.19 |
| `vess.gd` | 4.8 |
| `vess_binder.gd` | 4.8 |
| `wall_clock.gd` | 4.4 |
| `world_builder.gd` | EXCLUDED — 0.6 stamped it from the CSVs; Phase 3 rooms own the rest (landmark spawns pending extraction) |

## VERIFICATION

`tools/verify_mechanics.py` asserts: boxes 4.1..4.50 contiguous with 4.0
ticked and tagged; one notes section per box with the same title; QA-01..61
all claimed; I01..I31 all claimed; A01..A28 all claimed; all 73 scripts
indexed exactly once with a box or an exclusion reason; every NAME=VALUE
quoted above equals `ue/Restoration/Data/Timings.csv`; every cited path
exists; Laws 1..11 each cited. It prints VERIFY-OK or fails on the first
miss. Run it after any edit to the Phase 4 section.
