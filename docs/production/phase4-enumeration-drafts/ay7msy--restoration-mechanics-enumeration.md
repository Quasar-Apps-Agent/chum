# RESTORATION · MECHANICS ENUMERATION (Phase 4 census, unit 4.0)

**Unit 4.0 (CLOUD-OK).** Every mechanic the canon names, enumerated into
Phase 4 boxes in `PROGRESS.md`, each keyed to the milestone that accepts it
(`docs/packet/portbrief/BUILD-ORDER.md`, P2–P6), the reference script that IS
its specification (PORT-BRIEF law: where prose and code disagree, THE CODE IS
THE INTENT), the save fields it owns, the canon numbers it must keep, the QA
lines and invariants that accept it, and its Unreal home per
`docs/packet/portbrief/UE5-MIGRATION-MAP.md`.

Method: read every canon and production document (design doc Part IV, game
master, walkthrough Parts IV–VII and addenda, routing, casualty ledger,
after-fire canon, dread doctrine, lore architecture, object taxonomy,
reaction matrix, controls map, accessibility matrix, achievements design,
demo cut plan, gap audit, QA regression v1 through QA-61, invariant suite
I01–I31, spike briefs, playtest protocol, build plan, port kit); then read
the reference scripts' headers, the `game_state.gd` field and save-dict
inventory, the Timings table, and the UE source tree; then assign every
mechanic exactly one owner box. Verified by `tools/verify_mechanics_enum.py`
(assert script — every QA line, invariant, achievement, save key, Timings
constant, and reference script must be accounted for here, and every 4.x box
here must exist in `PROGRESS.md`).

**Per-box work shape (from the plan's Phase 4):** port/implement from the
reference script → diegetic feedback (no HUD element that a piece of 1970s
equipment does not already display) → fail-forward integration → automation
test (0.9 harness reads the same log formats). A box is ticked only after the
plan's §4 loop, and for these units the ACCEPTANCE VIEW is the in-engine
capture of the mechanic doing its work plus the QA lines named on the box.

**Ownership rule:** mechanics already claimed by a Phase 0 box are listed in
§0 as OWNED and get no Phase 4 box (no double-booking). Phase 4 boxes carry
only the residue. Boxes tagged **[CLOUD-OK]** are pure data/text work a
cloud session may take.

---

## 0 · ALREADY OWNED (Phase 0 boxes; listed so the census is complete)

| Mechanic | Reference | Owner | Status in UE |
|---|---|---|---|
| The broadcast clock (ON_AIR_SECONDS 50 / BREAK_SECONDS 18) | `broadcast.gd` | 0.7 | PORTED (`URestorationClock`) |
| The night hunt: warn-once at WARN_RADIUS 7.0, strike at STRIKE_RADIUS 2.2, savor rule at ≥3, no-strike-thru-wall raycast, BREAK relocation heard-noise-first, MOVE_SPEED 2.4, BASE_HEIGHT 2.6, HEAD_TILT 0.045, WARN/STRIKE/RELOCATE telemetry in the parser's format (I01, I02, I22 lines; QA-12) | `rundown.gd` | 0.7 | PORTED (`ARundown`) |
| The After-Fire arc: AF_APPROACH_SPEED 0.8 → AF_LOOM_DIST 1.2 loom → AF_COOL_SECONDS 2.0 (taught 4.0 once, `af_taught`) → strike only on adjacency, else withdrawal; AF_HEIGHT 3.35; AF_FOLD_SECONDS 2.2 at AF_DOOR_NEAR 1.0 from `Doors.csv`; AF_CROSSING_SPEED 1.6 (I23, I24, I26) | `rundown.gd` | 0.7 + 0.8a | PORTED (simulate-proven) |
| State core: `URestorationState` subsystem, `Strike()` retake economy, `InDeadRoom`, v16 `URestorationSaveGame` round-trip | `game_state.gd` | 0.8a | PORTED (skeleton) |
| v16 save parity: 55 keys in dict order (version, mode, tbc, tape, paper, signatures, captures, strikes, items_lost, day, keys, pt, dailies, daily_seq, carried_id, carried_take, film_watched, signals_known, screening_done, run_complete, has_fire_tape, fire_tape_watched, seance_wear, leland_answers, presigned_seen, dock_done, assets, decision, lockdown_done, finale_done, ending_reached, lie_pending, vess_insight, vess_credited, ng_relic, crate_opened, night_tripped, cov_monitor, cov_move, cov_still, photo_safe, cascade_done, read_props, af_active, af_taught, casualties, merle_offered, signoff_completed, row_casualties, h2_pending, deadroom_seen, rejected_seen, glimpse_seen, merle_1974, fire_unsealed), SAVE_VERSION 16, the §6 deltas of `ue/PORT-NOTES-STATE.md` | `game_state.gd` | 0.8b-3 | OPEN |
| Rita: SPEED 3.1, ACCEL 10.0, MOUSE_SENS 0.0022, REACH 2.6 (gap-audit note: 2.1 m / 35° awaits the device pass — the code's 2.6 is the intent until then), CROUCH_MULT 0.55, cam drop 0.60 (body verb c045) | `player.gd` | 0.8b-1 | PORTED (`ARitaCharacter`) |
| The bench capture: CAPTURE_SECONDS 12 forced real time, TETHER 4.0 abort, drives `recording` / `recording_left` (arms the tally contract), A CLEAN SIGNAL / CAPTURE ABORTED, `IRestorationInteractable` base (A02; QA-06 timing half) | `capture_bench.gd`, `interactable.gd` | 0.8b-2 | PORTED (`ABenchCapture`) |
| P3 remainder: log stations + paper economy (`paper` 3 lines per station per tape, `sign_log`/`_sign_finish`, `log_refused` OUT OF PAPER, `station_points` + `respawn_point`; QA-05, A01, P1), retake presentation (slate, rewind, item loss order via `captured`, respawn at last signature; P3), Harriet's break-window freeze + rising cup + `And now. The tour continues.` (QA-09, A06), real day/night via the bed (`bed_prop.gd`, `set_night`, `night_changed`; `merle.gd` SPEED 1.6 is her walk), the screening with three stances (BEAT 0.8, WINDOW 3.2, on/off-beat, stillness for QUIET, `pt` award, unison beat, `screening_done`; A04, A05, P12) + ASSIST mercies (0.35 tolerance, 1.5× premiere clocks, hold-E stillness; QA-18) | `log_station.gd`, `harriet.gd`, `bed_prop.gd`, `screening_event.gd`, `cue_sign.gd`, `merle.gd` (walk only) | 0.8b-4 | OPEN |
| The harness: three bots (WANDERER / CHECKER / FAIL), invariant parser reading coverage_log, liveness_log, premiere_log → INVARIANTS.txt; I01 / I02 / I22 / I06 green in UE, plus the soak-style wander map | `soak_runner.gd`, `bot_driver.gd`, `invariant_parser.gd`, `scenes/soak.tscn` | 0.9 | OPEN |
| The parity gate | — | 0.10 | OPEN |

Out of Phase 4 entirely (named so the script census closes): `sfx.gd`
(synth one-shots — the bell's two inharmonic partials, thunks, ticks) and
`tone_emitter.gd` (RATE 22050, hum/coil/segment tones) → Phase 5.1
MetaSounds; `shaders/wool.gdshader` → Phase 1 materials; `world_builder.gd`
(ROOMS/WALL_H 3.0/WALL_T 0.24 stamped in 0.6; its dressing spawns →
Phase 3 rooms; its interactable spawns → box 4.1 below); `arm_preview.gd`,
`cast_preview.gd`, `head_preview.gd` (dev look-dev tools, superseded by the
UE look-dev level); `prop_kit.gd`, `character_kit.gd` (greybox mesh helpers,
superseded by the Blender factory); `credit_entry.gd` (a credits row
widget, folded into 4.29); `finale_fixture.gd` (the premiere's fixable
fixture, folded into 4.24); `frame_sequence.gd` W 320 × H 240 (folded into
4.18); `credits.gd` SPEED 42 (folded into 4.29); `hud.gd` (split across
4.13, 4.16, 4.26, 4.28, 4.29 — the HUD is not a system, it is where five
systems speak).

---

## P2 · STATE, SAVES, DATA (accepts QA-05, QA-16, QA-31)

**4.1 [CLOUD-OK] Landmarks.csv + Achievements.csv** — the two port-kit
tables the 0.5 extraction deferred. Extract the interactable spawn registry
from every `world_builder.gd` `_spawn_*` site (bench, keys, readables D01–D11,
assets and rack, docks, crate, cabinet and note, dresser and bed, casting
sheet, chairs, pegs, club figures, clocks, cue signs, canister sites,
degausser, patchbay circuits, monitors, the fire-tape pickup, the decision
ledger) with position, class, gate, and label; and the 28-row achievement
table (id, title, description, trigger flag, hidden) from `achievements.gd`
+ the design doc. Extend `tools/extract_data.py` (deterministic,
re-runnable). Canon: the data-driven world law (every later box spawns
FROM these tables, never by hand). UE: two DataTables. Status: not started.

**4.SAVE integrity pass** (existing box) — QA-31 (a v15 log loads with the
migration toast, nothing lost, settings untouched; `_announce_migration` /
`_announce_newer`), the burn-in rule (wear, splices, dailies survive retake,
reload, crash: walkthrough Part V), I16 (item loss ordered and bounded),
I17 (run end zeroes strikes, keeps losses, mints no daily; `run_complete`),
I18 (lockdown survives reload), the DEMO whitelist inspection (QA-30 half,
QA-48), the `Mode` enum (MATINEE 7 lines / LATE_NIGHT 4 / ONE_TAKE 0;
`set_mode`; Matinee unlimited paper and halved wear), `reset_new_game` and
the eight fields that persist across a new game (`ue/PORT-NOTES-STATE.md`
§3), and the v17 migration policy the gap audit asks for. Runs after 0.8b-3.

---

## P3 · THE LOOP RESIDUE (accepts QA-06 to QA-11, QA-18)

**4.2 The tape world** — `shaders/crt_tape.gdshader` (chroma offset,
scanlines, noise floor, tracking band, head-switch tear, dot crawl,
vignette; generation-scaled, TBC-steadied by the 0.7 factor, photo-safe
suppressing bands/flicker/crawl) → a Material Function stack on the render
target with scalar parameters `generation`, `tbc_on`, `photo_safe` driven
from state through a Material Parameter Collection; `tape_stage.gd` (the
diorama: idle, approach 1.35, hold 0.78→0.12, single-frame lunge ×1.45,
bars; abort sync) → a sublevel captured by its own SceneCapture with the
Scare 1 timeline as a Level Sequence whose lunge is a one-frame track;
`bench_tv.gd` (the bench monitor through the artifact shader; the slate lies
about the generation, the scope does not — the demo's one contradiction);
`gen_knob.gd` (MASTER / 2ND / 3RD GEN; A03; base-vs-temp restore per P16);
`set_tbc` (T) and `set_photo_safe` (P) as the diegetic access switches
(`tbc`, `photo_safe`). Canon: design doc Part II (the two render worlds),
Spike 1 pass line (one clip, four generation states, tool-reactive,
photosensitivity-safe), verdicts V2 / V3 / V4, Law 2 (the in-tape lunge is
the game's one startle — I14 audits that nothing else lunges). QA-06 (bars
play). UE: material graph + Level Sequence. Status: not started.

**4.3 Doors, keys & the grammar v0** — `door.gd` (hinged; locked doors
state their reason from `Doors.csv` `kind`; keys satisfy locks; window-bound
doors HELD FOR AIR move only during BREAK and are waived during the
cascade), `key_item.gd` (the chain: kitchen board tagged EDITH → shed →
QUIET ROOM; `keys`, `has_key` / `take_key`; A16), `wall_clock.gd` (studio
clock repeaters reading the 0.7 clock). Canon: design doc Part IV §3
(entrances and exits), routing rule 3 (break windows are traffic lights),
solutions matrix (the Force path — drill the dead room door — is prose-only
in the reference; if built it leaves the seal imperfect and hums the DEAD
AIR epilogue). Accepts QA-10, QA-20 (waived holds), I04, I08. UE: the 0.6
door slabs gain hinge, lock, key, and hold behavior; `ADoor` reads the same
CSV row. Status: slabs with world text only.

**4.4 The dresser, the sheet & run death** — `dresser.gd` (ITEM_ORDER
WATCH, PEN, PHOTOGRAPH, LIGHTER, COMPACT, KEYS, LOUPE; one leaves per
capture, the loupe last; `items_lost`), `casting_sheet_prop.gd` (the death
counter as a wall object, `strikes` typed onto blank lines), `run_ended`
(sheet full at 4 / Matinee 7 / any in ONE_TAKE → NEXT WEEK'S EPISODE ·
STARRING RITA IVORI → title, no credits, morning-after CONTINUE; A18, A19),
`ng_relic` (the NG+ nod: the last item lost stands on the set in Tape 1,
unremarked — the gap audit parks PREMIERE+ but the nod is built). Accepts
QA-07, QA-08, I16, I17, P3, P4. UE: actors + `URestorationState` fields
(present from 0.8a). Status: `Strike()` economy ported; the objects and the
card are not.

**4.5 The club on schedule** — `merle.gd` (kettle by day, chair by night,
the DOORWAY saying nothing while the pen is up; state-tracked lines; the
1974 monologue `merle_1974`, A12; her body honors the ledger), `coat_pegs.gd`
(the entry pegs as the L1 group-state meter: drift per day table,
monotonic, never called out; freezes at her peg's day if Merle dies),
`vess.gd` (at the shrine wall; PER V. KEYS; `vess_credited`, A11),
`vess_binder.gd` (his research in his room: one true insight
`vess_insight`, one confident error — the G2 source), `harriet_note.gd`
(folded paper on her chair: the seventh signal, not on any film; A07).
Canon: game master T1–T4, reaction matrix (the BUILT column), dread
doctrine L1, art bible drift law. Accepts QA-11, QA-56 (drift resolves to
dressing), P13, P14. UE: scheduled actors reading the 0.7 clock delegate.
Status: not started.

---

## P4 · THE HUNTER AND NIGHTS (accepts QA-12 to QA-14, QA-19, QA-20; amended QA-33 to QA-38)

**4.6 Frame Discipline (camera safety)** — `monitor_rig.gd` (a camera
somewhere else rendered live onto a wall set; tally; NO SIGNAL when its
circuit is dark; kill by his stare with static rising; re-patch revive;
`sync_to` for lockdown) → `USceneCaptureComponent2D` per feed (the 0.6b
Spike 2 wall proved the budget; `spike_wall.py` is the rig); the on-camera
gate in `ARundown` (standing in an active camera cone prevents the strike —
Law 1, I05, QA-14) and the Spike 2 other half: a SAFE / EXPOSED assertion
overlay and a test that walks every state transition. Camera-kill priority
comes from 4.11. Canon: design doc Part IV §2, walkthrough Part V-B (fail
conditions 1 and 2; Avert is prose-only in the reference — a clipboard
raise on Q that the code never built; note it, do not invent it). UE:
`Monitors.csv` already extracted (2 rows; the rest come with 4.1). Status:
feeds proven, safety gate absent.

**4.7 The patchbay & the power budget** — `patchbay_console.gd` (one
amperage budget, two circuits, something is always dark; NO SIGNAL
propagation to the rigs it feeds; revive-first re-patch after a kill;
`apply_initial`; the cascade console stages; the GET VESS offer site for
V2), `finale_breaker.gd` (the panel during the premiere: the club is
helping). Canon: design doc §2 (the FNAF power meter grown into a
building-scale routing puzzle; tuning target: players think in routes, not
percentages), Spike 6 half one, routing rule 2 (mediated corridors are
player-built roads). Accepts QA-14 (revive), the power half of QA-20. UE:
circuit actors + a UMG scrim for the blackout layer (`set_blackout`,
`blackout_changed`). Status: not started.

**4.8 The noise bus & night one** — `noise_tracker.gd` (the player's
footsteps at night; `noise` → `noise_event`), plus door thunks, signature
ticks, and the degausser coil as sources into the ported `ReportNoise`; the
"It changed direction" line once per run (A08) and relocation within 12 s
(QA-13, I22 — the telemetry line is ported, the sources are not); crouch
honesty (I31, QA-58: no posture or footstep channel exists for the hunter
to read — byte-identical soaks walking and crouch-walking); `night_trip.gd`
(~20 s into the first night: a breaker lets go, a feed dies, something
behind you hums the closing song; `night_tripped`, once per save; QA-19
first half, P9; its M1 ripple escalates night trips a stage early). UE:
AIPerception hearing or the custom delegate the map allows. Status: API
ported, emitters absent.

**4.9 The Floor Manager** — `floor_manager.gd` (nights, ON AIR, at the
stack's end inside 9 m; one hand rises: YOU'RE ON; 3 s freeze check — take
holds or take spoiled; absent during breaks and the premiere; assist
hold-E passes; complete spoken inventory: "In five, four…" and nothing
else; the seventh signal grants 3 s grace before the unscripted seek
(4.15); F2 body honors the ledger; the post-F2 monitor haunt and the
freeze-check inversion are canon-only). Canon: design doc (the signals are
the threat-telegraph UI), silence ledger (I15: never heard moving). Accepts
QA-19 second half, P8. UE: an actor on the clock delegate. Status: not
started.

**4.10 The cascade (Night 4+)** — `cascade.gd` (circuit C trips, darkness
spreads through the blackout layer, circuit B follows, ordered two-stage
restoration refusing B before C, circuit F the marshal's tie that cannot be
de-energized; window holds waived while `cascade_active`; the Rundown
bolder in the dark; `cascade_done`; A15), `liveness_check.gd` (the panel is
always reachable: liveness_log OK every 5 s, VIOLATION on breach; I07).
Canon: Spike 6 pass line (Night 4 end to end), game master T2.7, fire
marshal report D09. Accepts QA-20, I04, I07, and V2's site (QA-42 second
half via 4.27). UE: same two actors; liveness_log format unchanged.
Status: not started.

**4.11 The Coverage Director** — `coverage_director.gd` (profiles CHECKER /
SPRINTER / HIDER from `cov_monitor` / `cov_move` / `cov_still`, persisted
across sleeps; `coverage_label` shown in the binder as AUDIENCE until read;
coverage_log append-only with a reason string on every blocking decision;
`most_watched_rig` drives camera-kill priority; savoring at the last sheet
line; `reset_read` on a burn). The blocking table (game master Appendix A:
twelve scripted scares × A / B / C) ports as data; C variants sit on the
descope ladder; the poisoned-well rule (monitor deception at most once per
run, only via the Director, only with the static telegraph — build plan
invariant 3) and the poltergeist prop layer (never the dock) are the
Director's remaining canon. Accepts I21 (deterministic, explainable), V5,
Spike 5 (replay diff). UE: a WorldSubsystem; counters in the SaveGame;
`FFileHelper` append. Status: not started.

**4.12 Burn your dailies** — `dailies_manager.gd` + `dailies_canister.gd`
(a canister labeled SCENE/TAKE appears in the library stacks per capture;
existing ones respawn on load; `dailies`, `daily_seq`), single-slot carry
(`carried_id`, `carried_take`; `pick_daily`), `degausser.gd` (the climate
room coil: `burn_daily` takes her name off the line and resets the
Director's read; `daily_burned`), abort never mints (I09), run end mints
none (I17), `mint_shortcut_daily` for H2 (4.20). Canon: walkthrough Part
V-B (deaths produce gameplay; the archivist survives by destroying
footage), the secret's four-clean-dailies gate (4.28). Accepts P2, P5. UE:
actors + state (fields present from 0.8a's skeleton once 0.8b-3 lands).
Status: not started.

**4.13 After-Fire presentation & the dead room** — the residue of the
ported AF arc: the HUD tally lamp (`_process_tally`: a red dot, REC · SAFE
WHILE LIT, the capture's own seconds — one number, two meanings), the AF
captions ([WEIGHTED FOOTSTEP] distance-scaled, [THE JAW WORKS ITS LEVER],
the fold captions and the close-range bending line, THE TALLY COOLS with
the 4.0 s teaching line once), the first-sighting toast exactly once per
save, the wake toast (fired from 4.17), `in_dead_room` bounds (noise born
inside registers nowhere — I25; he tracks to the felt door, holds, says his
line once; `deadroom_seen` first entry gives the radio toast and [NO ECHO]),
the withdrawal to segment when the tally dies at distance, the tally eye
burning ONLY while `recording` (logic here; the emissive itself is Phase
1.12), the crossing's dark eye (4.26). Canon: `restoration-after-fire-chum.md`
whole, motion and sound doctrine (jaw by his own hand only; the bell never
sounds; no vocalizations — QA-54 is Phase 1/5's to prove on the asset, the
logic gates live here), THE-LAWS 10 and 11. Accepts QA-33 (toast half),
QA-34, QA-35, QA-36, QA-37 (captioned), QA-38, I23–I26 (tests in 0.9), P17–P20.
UE: `ARundown` + UMG. Status: arc ported, presentation absent.

---

## P5 · STORY GATES AND FINALE (accepts QA-21 to QA-28; amended QA-39 to QA-47)

**4.14 Tape progression & the presigned page** — day-mapped tapes
(`current_tape`, `day`; `log_capture` slates captures; `captures`),
`objective_text` per day including ENDING REACHED, `mark_presigned`
(S4, Day 2+, the next line already in her hand dated tomorrow; costs no
paper — I10; `presigned_seen`; A09; the save system's one scare, singular).
Canon: walkthrough Part V (the save scare), game master T3.6. Accepts
QA-21, P6. UE: state + a station variant. Status: not started (0.8b-4 owns
the day/night lever itself).

**4.15 The film cabinet & the signal vocabulary** — `film_cabinet.gd`
(WGLD STAFF ORIENTATION 1971: six signals taught once, trusted forever —
YOU'RE ON, CUT, STRETCH, WRAP IT UP, THIRTY SECONDS, ON TIME; `film_watched`,
`signals_known`, `add_show_signal`), the seventh HOLD YOUR APPLAUSE via
Harriet's note (4.5; A07; unlearnable if she died before her card was found
— QA-41's gate) granting 3 s grace before the unscripted seek. Canon: game
master T2.4 and Appendix C (the signal glossary), solutions matrix (the
Force path — pry it, four of six signals — is prose-only). UE: a readable
variant + state. Status: not started.

**4.16 The readables & the binder** — `readable_prop.gd` (D01–D11 placed
physically per the props packet; `mark_read`, `read_props`; A26 FULL
ACCESSION at ten, D11 the Peak dossier readable in master control Day 4
after first sighting), the binder on TAB (`_fill_binder`: page one lists the
casualty ledger or NO ENTRIES. KEEP IT SO.; PT, keys, coverage label lines;
the presentation form `_fill_form` with live mode switching), `map_view.gd`
on M (drawn live from the room constants: sealed rooms dashed, station dots
from the registry, the player dot with a facing tick, footer showing the
BOUND key), the binder-is-the-inventory ruling (no grid, possession is
recorded), true-pause in the day and LIVE-TIME during the premiere only
(gap audit ruling 3), the casting-drift stationery (dressing, never
deception). Canon: design doc Part III, object taxonomy (QA-55 prompt
discipline: nothing ambient prompts; QA-59 the ambient ledger — the Phase
3 rooms place the objects, this box proves the prompt boundary), lore
architecture (the binder records facts observed, never interpretation).
Accepts QA-15, QA-39 (page one), QA-55, QA-59, P15. UE: UMG widgets; the
map redraws from `Rooms.csv` via OnPaint. Status: not started.

**4.17 The fire tape** — `fire_tape_pickup.gd` (`has_fire_tape`),
`fire_tape_dock.gd` (the forced watch: restraint scene, dimming stage, no
sting anywhere — I15; `fire_tape_watched` sets `af_active` and fires the
wake toast once, A13; M1's offer site Day 3+ — `merle_offered`, consent
kills warm, refusal saves; L2 consumes the tape at the seance dock, 4.18).
Canon: game master T3.4, after-fire canon (THE REVEAL). Accepts QA-23,
QA-33, QA-40 (M1 half), Law 2 audit. UE: a dock actor + a Level Sequence
without a stinger track. Status: not started.

**4.18 The crate & the seance** — `impossible_crate.gd` (Tape 4's
delivery at the front door; `crate_opened` unlocks the reel — I19 first
clause; QA-22 first half), `seance_dock.gd` (Z back / X forward over
MAX_FRAME 40; five answers at fixed frames; wear per pass 7 / Matinee 3.5
into `seance_wear`, burned in; `leland_answers`; the knob's dialed value
restored on close — P16; the grief answers at frame 14 Harriet and frame
28 Merle — QA-50; L1 THE SIXTH QUESTION offered only past five answers and
wear above 70, the ink drains, the dock goes inert, 1A closes; L2 THE
READING when the fire tape is fed into the wake — answers un-write,
`signoff_completed`, the tape consumed; A14), `frame_sequence.gd` (one
deterministic seeded frame per index, W 320 × H 240, Leland cropped at the
edge stepping in on answer frames; I20 the same frame is always the same
frame; the drop-in swap point for real footage). Canon: design doc §7 (the
game's tenderest mechanic), game master T4.4, Spike 3. Accepts QA-22,
QA-44, QA-50, I19, I20, V6. UE: `UTexture2D::CreateTransient` per index or
an image-sequence Media Source; wear stays a material parameter. Status:
not started.

**4.19 The dock task** — `dock_task.gd` + `dock_chum.gd` (six retired units
on armatures, one anomaly found by touch, zero incidents by contract;
`dock_done` gates the sign-off card; the Director never stages the dock;
A10; Law 4 — the warm one never acts: I12 is a review rule on every later
commit, keep it that way). Canon: game master T4.3, walkthrough Part III
principle 6. Accepts QA-24 (first clause), P7. UE: actors. Status: not
started.

**4.20 The rejected edit & the splice** — `rejected_edit.gd` (Vess threads
his own cut: played in full, the mechanical refusal, the take-up reel's one
backward rotation, his two lines, Merle's cobbler; `rejected_seen`; the H2
temptation disclosed with her label — performing it mints a daily at once
via `mint_shortcut_daily`, sets `h2_pending`, and the next break doubles
her: one frame left of herself, scenery forever with one line, rebuilt on
load through her `_process` gate). Canon: game master T4.5, casualty ledger
H2. Accepts QA-49. UE: a scene actor + Harriet's ghost meshes. Status: not
started.

**4.21 The Sign-Off assets & the decision ledger** — `asset_pickup.gd` /
`asset_rack.gd` (four labels above the bench: the missing verse from
`spectro_dock.gd` (the audio bench: the verse under the closing song's
sidebands, T2), the station ID cart (T3 master control), the finale script
(T3 Craik's boxes), the sign-off card (T4 dock, after filing); `assets`,
`gain_asset`), `decision_ledger.gd` (three entries in her hand: AUTHENTICATE
/ DESTROY / PERFORM; pen cycle + SPACE commit, ink final; `decision`;
`start_finale`; Merle walks to the doorway while the pen is up; A17; the
AUTHENTICATE commit is V1's first trigger when credited). Canon: game
master T5.2, walkthrough Part VII (tracked variables). Accepts QA-24
(card gate), I19, P14. UE: actors + `finale_started` delegate. Status: not
started.

**4.22 The glimpse & the unseal** — `glimpse.gd` (the fire corridor
unseals from the library side on Day 4 — `fire_unsealed`; at the elbow,
once ever, under two seconds, unmediated, undecidable; `glimpse_seen`
persisted; nothing refires after relaunch). Law 3: no achievement, no
presence string, no log line, no reference by any later system; the UE
class carries no descriptive name. Accepts QA-25, I11, P10. Status: not
started.

**4.23 Lockdown** — `lockdown.gd` (every monitor `sync_to` the same frame,
exterior doors SEALED FOR BROADCAST, Merle radiant at the head of the room,
`lockdown_done` persistent and re-applied on ready; A20), `rec_chairs.gd`
(the armchairs tween to forward-facing rows and never convert back;
persist). The ending-0 precondition is read here (`all_cast_dead` before
lockdown → 4.26 intercepts at premiere entry). Canon: game master T4.10.
Accepts QA-26, I18, P11. Status: not started.

**4.24 Live production I — cues & sabotage** — `live_production.gd` core:
cue marks at MARK requiring the PGM camera (switcher `cam_1..3` with
wrong-camera refusal), the incident loop (TALLY / HOUSE / BOOM / CARDS, one
active at a time, a `finale_fixture.gd` to fix each, escalation via failed
takes), the triple fail-forward guarantee (tally refusals capped at 2, the
boom held exactly once, the club auto-fixes at or under 40 s — I06),
premiere_log in the parser's format, the Rundown yielding the floor (I03)
and on-camera safety while live (I05), the bell beat once at the midpoint
(Law 5: its caption says so), the little door closed by hand on camera,
ASSIST's 1.5× clocks. Canon: design doc §9, Spike 7, THE-LAWS 6. Accepts
QA-27, QA-51 (braid audit lives in its own box, 4.QA51), I03, I05, I06.
UE: a GameMode-scoped director actor; cue marks as trigger volumes; the
switcher as Enhanced Input actions. Status: not started.

**4.25 Live production II — the club's hands** — the Vess breaker
(credited: his hand stops above the handle; uncredited: the handle, the
dark, earn the retake; dead: the fused pin plus the hard blackout — V1's
second trigger is the final breaker itself, after the farewell, lights
held), F2 THE UNLISTED CAMERA on the third blind tally call ([YOU'RE ON ·
TO NOTHING LISTED], cue flow continues), the rows (`_row_taken`: every
timed incident that expires takes a seat, three cycling lines, [A CHAIR,
BETWEEN FRAMES], `row_casualties` counted and persisted; M2 THE HOME SINGER
is prose-only in the reference — see §7). Canon: game master T5.3, casualty
ledger V1 / F2 / THE ROWS. Accepts QA-42 (V1 half), QA-43 (F2 half), QA-46.
Status: not started.

**4.26 Live production III — the divert, the fader & the crossing** — the
divert window in its canon slot at the final break (gated on the QUIET ROOM
key + five answers + the fire tape — I19 third clause; no prompt if 4c is
set), F1 THE FADER (he is already reaching: SPACE lets him hold → 4a HIS
HAND; hold E 4.6 s to hold it yourself → 4b HER HAND with the 13 s tax;
`fader_self`; forced self-hold if he is dead), the crossing (`crossing`,
`crossing_caught`: 75 s base, 62 without Vess, minus 13 self-held; master
control to the little door at AF_CROSSING_SPEED with folds intact and the
eye dark; reached → DEAD AIR, caught → a starring credit inside her own
ending, late → the window closes and the committed line plays), ending 0's
intercept at premiere entry (`_one_woman`). Canon: after-fire canon (THE
LAST CROSSING), casualty ledger F1, walkthrough addendum board. Accepts
QA-43 (F1 half), QA-45 (intercept), P22, P23. Status: not started.

**4.27 The casualty ledger** — `mark_casualty` (idempotent — I27; the stamp
toast; `casualties` array of who / cause / line / day), `is_dead`,
`cause_of`, `all_cast_dead`; the ten authored deaths and their sites: M1
(4.17), M2 (prose-only, §7), V1 (4.21 + 4.25), V2 (4.10 panel: GET VESS for
the uncredited who used the insight; eleven-second full fix then circuit
F bare-handed), H1 (`harriet_slip` armed on a frozen interact Day 2+;
taking it grants one paperless signature in her hand; the next break edits
her out with the film-cabinet beat; QA-41), H2 (4.20), F1 / F2 (4.26 /
4.25), L1 / L2 (4.18); the ripples as data (the kettle cold and the hunter
lingering there, the peg freeze, breaker incidents losing their easy
variant, screenings judged 0.05 tighter, the seventh-signal gate, the
crossing at 62, 1B's SAINTS / STAFF / READER cards, ending 2's furniture,
the cold cobbler plated for two, Leland's answer variants); the readings
(I28 the ledger never lies: every epilogue reading matches page one
exactly). Canon: `restoration-casualty-ledger.md` whole (Law 7). Accepts
QA-39, QA-40, QA-41, QA-42, QA-44 (L1 / L2 halves), QA-49, QA-50, I27, I28,
P21, P24, P25. UE: state + the sites above. Status: not started.

**4.28 The endings & credits** — `_on_finale` routing in `hud.gd`: THE BURN
(DESTROY; degausser + bake oven; the cold-cobbler variant; A21), THE NEW
PRODUCER (AUTHENTICATE, or PERFORM under four assets at PT ≥ 70 — `pt`,
`add_pt`; the game's one interface lie spent at the title: `lie_pending` →
CONTINUE? / NEW EPISODE once, reverting next launch — I13; A22), SIGN-OFF
1A (PERFORM, four assets, five answers, wear under the threshold, Leland's
print intact; A24) / 1B (otherwise; SAINTS plus earned cards; A23), DEAD
AIR 4a / 4b (the drilled-door hum variant is prose-only; A25), 4c THE
COMPLETED SIGN-OFF (lights down in reverse tour order; no achievement by
ruling), ENDING 0 (nine cards, one name; A28), `mark_ending` /
`ending_reached` / `finale_done`; every ending's credits open with THE
LEDGER, READ ALOUD (fifty-eight minus N) when anything is in it and A27
files on clean hands (I29). ENDING A · AUDIENCE ONLY (the secret: four
clean dailies, the unnumbered reels W1–W3 in sequence each spending an S2
slip, the dead-room radio confirmed, the caption at the final break, Q
within six seconds, the 75 s run to the dead room, the sit, the program
guide post-credits, 58 · STILL ON on the title forever, no achievement) is
prose-only in the reference (walkthrough addendum c046; QA-60, QA-61) —
build it from the addendum's text. Canon: game master THE ENDINGS,
walkthrough Part VII + addenda, routing THE FOUR THREADS. Accepts QA-28,
QA-45, QA-47, QA-60, QA-61, I13, I28, I29, A21–A25, A27, A28, V7, P26.
UE: Level Sequences + the credits widget. Status: not started.

---

## P6 · META AND MODES (accepts QA-01 to QA-04, QA-17, QA-29, QA-30, QA-32, QA-48, THE-LAWS audited)

**4.29 Title, pause & the credits shell** — `title.gd` (channel dark, the
card, the save-aware menu; FILED WHILE YOU WERE OUT exactly once; NEW
EPISODE once; TAPE 1 · FREE DEMO badge; the first-run booth over the
title; 58 · STILL ON when 4.28's secret lands), the pause system
(`pause_requested`: tree-wide hold, audio mute, keyboard-operable menu
with booth access, honest RETURN TO TITLE, refused during any authored
sequence), `credits.gd` + `credit_entry.gd` (period cards at SPEED 42,
CHUM as himself, the ending-reached card, any key after grace skips, the
tower-light hold), the ending-reached card. Accepts QA-01, QA-02, QA-03,
QA-04, QA-32. UE: UMG. Status: not started.

**4.30 The booth** — `options_panel.gd` (MASTER VOLUME, MOUSE SENSITIVITY
multiplying the player constant, FULLSCREEN, TBC (T), PHOTOSENSITIVITY-SAFE
(P), UI TEXT SIZE 0.8–1.6 via the recursive walker — `ui_scale`,
`set_ui_scale`; CAPTIONS — `captions_on`; ASSIST — `assist_on`; the
five-verb remap with press-a-key and KEY IN USE refusal — `rebind`,
`key_name`; O in game and OPTIONS on the title; `load_settings` /
`save_settings` to settings.cfg apart from the log so NEW GAME never
touches them — `mouse_sens`), the first-run booth (QA-01), focus rings.
UE target per the controls map: every action remappable including
movement, the controller map (RECORDING IS THE TRIGGER), hold-to-toggle
equivalents with durations preserved. Accepts QA-16, QA-17, QA-18 (the
switch; the mercies are 0.8b-4's). Phase 5.2 owns the accessibility
matrix's full target beyond R1–R7. UE: UMG + Enhanced Input. Status: not
started.

**4.31 Captions, glyphs & the string table** — `show_caption` / `caption`
(significant one-shots with source tags: THE BELL, doors, the pen tick;
band-limited sources bracketed as broadcast, full-range plain — the audio
law survives captioning), the glyph layer (`glyphs`, GLYPH_MAP: word-
boundary substitution of E / SPACE / Q / T / M to bound keys at prompts,
toasts, say lines, cue status, the map footer), `tr()` at the four
chokepoints plus the booth labels → `GameText.csv` as a StringTable (714
keys; the source string is the key; `tools/extract_strings.py` re-runnable;
locale waves per the localization plan; toast durations reading-speed
scaled). UE extension: directional and proximity caption tags (5.2).
Accepts QA-05 (caption half), QA-17 (prompts show the new key). Status:
`GameText.csv` extracted; nothing wired.

**4.32 Achievements** — `achievements.gd` (28 ids A01–A28, `unlock`
idempotent, persisted; the deferral queue flushing only at the morning
toast on `night_changed(false)` and the title's stack; meta-silence: the
glimpse has no entry, Chum's name in no title, no per-answer seance pings,
4c and ENDING A carry none by ruling; disabled entirely under DEMO; a plain
signal for the Steam bridge; `demo_mark` is the demo's, not this). The
table itself is 4.1's extraction. Accepts QA-29, QA-45 (A28), QA-47 (A27),
I30. UE: a GameInstance subsystem + the Online Achievements interface.
Status: not started.

**4.33 Demo mode** — `DEMO` build flag (E1–E10): `DemoOpen.csv` (seven
rooms), door reasons overriding `Doors.csv` (the transmitter corridor's own
line), five spawn gates (no Rundown, FM, dock, crate, seance, cascade,
assets, ledger, fire pickup), the bed declines, paper S1 + S5 only, the
capture-complete end sequence (bars 1.6 s, the sign alone 2.0 s, the
protected card 3 s, any key to title; `demo_ended`), the save-writer
whitelist (no decision, assets, leland_answers, lockdown, finale, ending,
or casualty field can be written — absent from the write path, not gated),
local funnel telemetry (`demo_mark`: six marks), the title badge, Merle's
carry line on the full game's first CONTINUE, the dead-Merle refusal to
load forward. Accepts QA-30, QA-48, DP1–DP5. Status: `DemoOpen.csv`
extracted; nothing wired.

**4.34 THE-LAWS + rulings audit** — the eleven laws audited line by line on
the UE build (Law 1 on camera is safe — 4.6; 2 one startle — 4.2, I14; 3
once ever — 4.22; 4 the warm one never acts — 4.19; 5 silence contracts —
4.24, 5.1; 6 the schedule is real — 0.7, 4.3, 0.8b-4; 7 every death has a
signature — 4.27; 8 the interface lies once — 4.28; 9 access is canon —
4.30, 4.31; 10 the tally contract — 0.8a, 4.13; 11 the two hides — 4.13,
0.7), plus the gap audit's rulings verified in the build: no sprint; crouch
as a body verb that conceals nothing (QA-58, I31); the binder is the
inventory; stations plus signatures only, no autosave (the walkthrough's
Part V autosave policy is superseded by the ruling — code has none);
the single death card; photo mode Tier B studio-safe (day, never him —
unbuilt, ruled); the seek grace 3 s / sight grace ~1 s / PT weights
(+10 A-captures, +10 T2 improvise, +10 T4 gathering, +15 read-through,
audition at 70) as the tunables the code keeps. Runs last in Phase 4,
before 4.FINAL. Status: not started.

---

## 1 · THE EXISTING PHASE 4 BOXES (kept, now keyed)

- **4.WEB** reaction-matrix wiring: the QUEUE is thirteen unbuilt items —
  H-R2 (her freezes lengthen one second when After-Fire is active), F-R1
  (he points at the doorway before the first fold), M-R5 (the retired
  teacup), B-R2 (corridor practicals lose one bulb per casualty), M-R1..4,
  V-R1..3, L-R1 (NOT THAT ONE. PLEASE.), B-R1 — in the doc's commit order
  045 → 046 → 047, each landing with a QA line. Grep-verified: none of
  them exist in the reference; only H2's doubling (BUILT) does.
- **4.SAVE** — see P2 above.
- **4.ENCOUNTERS** choreography per room: the blocking table's A / B / C
  variants (4.11) staged room by room after Phase 3's rooms exist, plus
  the Rundown's segment homes (STORY CORNER library, CRAFT TIME workshop
  with PATCH BAY standing in, THE SONG studio) — the audio tells you
  which segment, therefore where.
- **4.FINALE** premiere sequence: the acceptance pass over 4.24–4.26 as one
  playable night with the fail-bot soak (Spike 7's 30-minute fail-forward).
- **4.QA51** braid audit: at every premiere pressure peak at least two
  simultaneous demands share the clock (comparative study A2).
- **4.VERB** per-day verb-texture audit against the dread curve (Day 1 L2
  leads, Day 2 L3, Day 3 L2 inverts, Day 4 L4 arrives, Day 5 all layers;
  comparative study A3).
- **4.FINAL** deep soaks, invariants extended (I01–I31 all machine-checked
  where the suite says ENFORCED or TELEMETERED; MANUAL ones probed).

---

## 2 · QA COVERAGE (every line of `restoration-qa-regression.md` has an owner)

| QA | Owner |
|---|---|
| QA-01, QA-02, QA-03, QA-04 | 4.29 (QA-01 first-run booth with 4.30) |
| QA-05 | 0.8b-4 (paper) + 4.31 (caption) |
| QA-06 | 0.8b-2 (12 s, log) + 4.2 (bars) |
| QA-07, QA-08 | 4.4 |
| QA-09 | 0.8b-4 |
| QA-10 | 4.3 |
| QA-11 | 4.5 |
| QA-12 | 0.7 (ported) — proven by 0.9 |
| QA-13 | 4.8 |
| QA-14 | 4.6 + 4.7 |
| QA-15 | 4.16 |
| QA-16, QA-17 | 4.30 (+ 4.31 for the prompt glyphs) |
| QA-18 | 0.8b-4 (mercies) + 4.30 (switch) + 4.24 (clocks) |
| QA-19 | 4.8 (trip) + 4.9 (watch) |
| QA-20 | 4.10 + 4.3 |
| QA-21 | 4.14 |
| QA-22 | 4.18 |
| QA-23 | 4.17 |
| QA-24 | 4.19 + 4.21 |
| QA-25 | 4.22 |
| QA-26 | 4.23 |
| QA-27 | 4.24 |
| QA-28 | 4.28 |
| QA-29 | 4.32 |
| QA-30 | 4.33 + 4.SAVE |
| QA-31 | 4.SAVE |
| QA-32 | 4.29 |
| QA-33 | 4.17 + 4.13 |
| QA-34, QA-35, QA-36, QA-37, QA-38 | 4.13 (arc from 0.8a; 4.37's fold from 0.7) |
| QA-39 | 4.16 + 4.27 |
| QA-40 | 4.17 + 4.27 |
| QA-41 | 4.27 + 4.15 |
| QA-42 | 4.25 (V1) + 4.10 (V2) + 4.27 |
| QA-43 | 4.25 (F2) + 4.26 (F1) |
| QA-44 | 4.18 + 4.27 |
| QA-45 | 4.26 + 4.28 |
| QA-46 | 4.25 |
| QA-47 | 4.28 |
| QA-48 | 4.33 + 4.SAVE |
| QA-49 | 4.20 |
| QA-50 | 4.18 |
| QA-51 | 4.QA51 (over 4.24) |
| QA-52 | Phase 1.10 (the fold montage is an animation unit; its 2.2 s toll is 0.7's) |
| QA-53 | Phase 1.9 / 1.13 (AF zero-secondary sweep on the asset) |
| QA-54 | Phase 1.11 / 5.1 (the audio law on the assets; the logic gates are 4.13's) |
| QA-55 | 4.16 (prompt boundary) + Phase 3 rooms |
| QA-56 | 4.5 (pegs) + Phase 3 rooms |
| QA-57 | Phase 3 rooms (hero census) |
| QA-58 | 4.8 |
| QA-59 | 4.16 + Phase 3 rooms |
| QA-60, QA-61 | 4.28 (prose-only in the reference) |

## 3 · INVARIANT COVERAGE (`restoration-invariant-suite.md`)

I01 0.7 / 0.9 · I02 0.7 / 0.9 · I03 4.24 · I04 4.3 + 4.10 · I05 4.6 + 4.24
· I06 4.24 / 0.9 · I07 4.10 · I08 4.3 · I09 4.12 · I10 4.14 · I11 4.22 ·
I12 4.19 (review rule) · I13 4.28 · I14 4.2 (review rule + event-table
grep) · I15 4.9 + 4.17 + 5.1 · I16 4.4 + 4.SAVE · I17 4.4 + 4.12 · I18 4.23
· I19 4.18 + 4.21 + 4.26 · I20 4.18 · I21 4.11 · I22 4.8 / 0.9 · I23 0.8a +
4.13 · I24 0.7 + 4.13 · I25 4.13 · I26 0.8a + 4.13 · I27 4.27 · I28 4.27 +
4.28 · I29 4.28 · I30 4.32 · I31 4.8.

## 4 · ACHIEVEMENT COVERAGE (`restoration-achievements-design.md`)

A01 0.8b-4 · A02 0.8b-2 · A03 4.2 · A04 0.8b-4 · A05 0.8b-4 · A06 0.8b-4 ·
A07 4.15 · A08 4.8 · A09 4.14 · A10 4.19 · A11 4.5 · A12 4.5 · A13 4.17 ·
A14 4.18 · A15 4.10 · A16 4.3 · A17 4.21 · A18 4.4 · A19 4.4 · A20 4.23 ·
A21 4.28 · A22 4.28 · A23 4.28 · A24 4.28 · A25 4.28 · A26 4.16 · A27 4.28
+ 4.32 · A28 4.28 + 4.32. The table extraction is 4.1.

## 5 · SAVE-KEY OWNERSHIP (the 55 keys of `_save_dict`, per box)

version, mode, tbc, tape, paper, signatures → 0.8b-3 / 0.8b-4 / 4.SAVE ·
captures, day → 4.14 · strikes, items_lost, run_complete → 4.4 · keys →
4.3 · pt → 4.28 (+ 0.8b-4 awards) · dailies, daily_seq, carried_id,
carried_take → 4.12 · film_watched, signals_known → 4.15 · screening_done
→ 0.8b-4 · has_fire_tape, fire_tape_watched, af_active, merle_offered →
4.17 · seance_wear, leland_answers, crate_opened, signoff_completed → 4.18
· presigned_seen → 4.14 · dock_done → 4.19 · assets, decision → 4.21 ·
lockdown_done → 4.23 · finale_done, ending_reached, lie_pending → 4.28 ·
vess_insight, vess_credited → 4.5 · ng_relic → 4.4 · night_tripped → 4.8 ·
cov_monitor, cov_move, cov_still → 4.11 · photo_safe → 4.2 · cascade_done
→ 4.10 · read_props → 4.16 · af_taught → 0.8a · casualties, row_casualties,
h2_pending → 4.27 / 4.25 / 4.20 · deadroom_seen → 4.13 · rejected_seen →
4.20 · glimpse_seen, fire_unsealed → 4.22 · merle_1974 → 4.5.

## 6 · TIMINGS OWNERSHIP (`ue/Restoration/Data/Timings.csv`, 32 rows)

broadcast.gd ON_AIR_SECONDS, BREAK_SECONDS → 0.7 · capture_bench.gd
CAPTURE_SECONDS, TETHER → 0.8b-2 · credits.gd SPEED → 4.29 ·
frame_sequence.gd W, H → 4.18 · game_state.gd SAVE_VERSION → 0.8b-3 ·
merle.gd SPEED → 0.8b-4 / 4.5 · player.gd SPEED, ACCEL, MOUSE_SENS, REACH,
CROUCH_MULT → 0.8b-1 · rundown.gd MOVE_SPEED, AF_APPROACH_SPEED,
AF_LOOM_DIST, AF_COOL_SECONDS, AF_HEIGHT, AF_FOLD_SECONDS, AF_DOOR_NEAR,
AF_CROSSING_SPEED, WARN_RADIUS, STRIKE_RADIUS, BASE_HEIGHT, HEAD_TILT →
0.7 / 0.8a (AF_CROSSING_SPEED exercised by 4.26) · screening_event.gd
BEAT, WINDOW → 0.8b-4 · seance_dock.gd MAX_FRAME → 4.18 · tone_emitter.gd
RATE → 5.1 · world_builder.gd WALL_H, WALL_T → 0.6.

## 7 · FINDINGS (canon versus code, surfaced not resolved)

1. **M2 THE HOME SINGER is prose-only.** The casualty ledger's AS BUILT
   section says all ten deaths are implemented; `live_production.gd` has
   no HOME segment, no call-sheet offer, no "I know the songs." Nine deaths
   are in code. 4.27 authors M2 from the ledger text (window: premiere;
   trivially solves one incident; the swapped word; MERLE O., STRUCK
   THROUGH). No QA line exists for it — add QA-62 when it lands.
2. **ENDING A · AUDIENCE ONLY is prose-only.** The walkthrough addendum
   (c046) describes it as built; nothing in the reference carries the
   W-reels, the S2 slip spend, the radio confirm, the program guide, or
   58 · STILL ON. QA-60 and QA-61 exist. 4.28 builds it from the addendum.
3. **The Force paths of the solutions matrix are prose-only** (pry the
   cabinet, drill the dead room door with the hummed epilogue, after-hours
   TH entry with +1 patrol density, cut the dorm heat). The reference
   implements PRESERVE and ASK. Named on 4.3, 4.15, 4.28; not owed.
4. **Avert (the clipboard raise) is prose-only.** The design doc's Q-hold
   shield never shipped; Q became IMPROVISE. The code is the intent: no
   Avert. Named on 4.6.
5. **Modes versus the "ASSIST only" ruling.** Gap audit ruling 5 reads
   "DIFFICULTY: RULED, ASSIST only. One game, honestly tuned." The code
   ships three run modes (MATINEE 7 lines / LATE_NIGHT 4 / ONE_TAKE 0) in
   the binder's presentation form, with Matinee's unlimited paper and
   halved wear. By the port law the code stands; the owner decides at 4.34
   whether the ruling meant "no difficulty ladder beyond these framings".
6. **The reaction matrix's QUEUE is entirely unbuilt** (thirteen items;
   only H2's doubling exists). 4.WEB stands as written.
7. **Reach: 2.6 in code, 2.1 / 35° in the gap audit** (ruling 10 says the
   final numbers await the device pass). 0.8b-1 ported 2.6 correctly.
8. **The post-F2 monitor haunt, the freeze-check inversion, and the
   margin's green bleed** are canon-only by the ledger's own AS BUILT
   admission; named on 4.9 / 4.27, not owed.
9. **`Achievements.csv` and `Landmarks.csv`** are named in the PORT-BRIEF's
   data dictionary but absent from `ue/Restoration/Data/` — 4.1.

---

## 8 · THE BOXES (as written into PROGRESS.md; the verifier diffs these ids)

4.1 · 4.2 · 4.3 · 4.4 · 4.5 · 4.6 · 4.7 · 4.8 · 4.9 · 4.10 · 4.11 · 4.12 ·
4.13 · 4.14 · 4.15 · 4.16 · 4.17 · 4.18 · 4.19 · 4.20 · 4.21 · 4.22 · 4.23 ·
4.24 · 4.25 · 4.26 · 4.27 · 4.28 · 4.29 · 4.30 · 4.31 · 4.32 · 4.33 · 4.34,
then the kept 4.WEB · 4.SAVE · 4.ENCOUNTERS · 4.FINALE · 4.QA51 · 4.VERB ·
4.FINAL. Thirty-four new units, one [CLOUD-OK], in BUILD-ORDER acceptance
order P2 → P3 → P4 → P5 → P6. Every box is one session or splits.
