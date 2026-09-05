# PORT NOTES · SCREENING — the mini-screening, ASSIST, and Merle, transcribed

**Unit C10 (CLOUD-OK).** The Tape 1 mini-screening as built (the reel, the
sign, the beat, the stances, the judgment), the ASSIST rule at every site
that reads it, Merle Cottry's whole script (her schedule, her prompt, her
lines, her death), and the Day-1 objective ladder that threads them. Source
of truth, at the commit this file landed in (`origin/main` 0e8166d):

| Script | Lines | Owns |
|---|---|---|
| `scripts/screening_event.gd` | 118 | the projector interactable: the run, the window, the stances, the judgment |
| `scripts/cue_sign.gd` | 63 | the RESPOND / HOLD signs: housing, label, amber light, `flash()`, `set_lit()` |
| `scripts/tape_stage.gd` | 250 | `play_screening(duration)` = `play_tape` with the lunge disabled |
| `scripts/world_builder.gd` | 1446 | `_spawn_screening()` (712–773): signs, rec-room TV, projector; `_spawn_club()` (1051–1078; Merle at 1060–1078) |
| `scripts/merle.gd` | 86 | Merle: schedule, prompt, the six lines, the 1974 monologue |
| `scripts/decision_ledger.gd` | 68 | `is_pen_up()`, the only thing that calls Merle to the doorway |
| `scripts/game_state.gd` | 777 | `screening_done` (save key 19), `screening_active`, `assist_on`, `set_assist`, `objective_text()`, `set_night()` |
| `scripts/floor_manager.gd` | 94 | the second stillness check that reads ASSIST (line 65) |
| `scripts/live_production.gd` | 434 | the third ASSIST site, `_timed()` (349–360) |
| `scripts/options_panel.gd` | 166 | the ASSIST check row (66–67) |
| `scripts/achievements.gd` | — | A04, A05, A12; the deferral (`unlock`, `flush_to_toasts`) |
| `scripts/fire_tape_dock.gd` | — | M1, Merle's only built death (29–31, 64–69) |
| `scripts/hud.gd` | — | `_on_notify` (551–553: the toast is REPLACED, held 3.0 s); Merle's epilogue variants |
| `scripts/bed_prop.gd` | 23 | the day/night lever that closes Day 1 |

Where these notes and those files disagree, THE CODE IS THE INTENT
(`docs/packet/portbrief/PORT-BRIEF.md` law); fix the notes. Every string
quoted below is verbatim from source; where it also lives in the shipped
string table it is cited as `GameText.csv row N`
(`ue/Restoration/Data/GameText.csv`, header on row 1, so row N is the Nth
line of the file). Where canon is silent the entry says OPEN. Nothing here
is a ruling.

UE homes (`docs/packet/portbrief/UE5-MIGRATION-MAP.md`: interactables →
actors implementing `IRestorationInteractable`, state → `URestorationState`,
HUD → UMG): `AScreeningEvent`, `ACueSign`, `AMerle` (all
`IRestorationInteractable` except the sign), `bScreeningActive` on
`URestorationState`, and `Access_Assist` on the settings subsystem that
`docs/production/UE-ACCESS-SPEC-LAW9.md` §1.1 specifies. §9 is the delta
checklist against the C++ that exists today.

---

## 1 · CONSTANTS THAT ARE CANON (never change the numbers)

| Constant | Value | Source | In `Data/Timings.csv`? |
|---|---|---|---|
| `ScreeningEvent.BEAT` | 0.8 s | `screening_event.gd:6` | yes (row `screening_event.gd,BEAT,0.8`) |
| `ScreeningEvent.WINDOW` | 3.2 s | `screening_event.gd:7` | yes (row `screening_event.gd,WINDOW,3.2`) |
| beats per window | `int(WINDOW / BEAT)` = 4 | `screening_event.gd:52` | derived |
| beat tolerance | 0.2 s (ASSIST: 0.35 s) | `screening_event.gd:90` | **no** (LAW-9 spec §5.2 asks for it) |
| Harriet-dead penalty | `tol = maxf(0.1, tol - 0.05)` | `screening_event.gd:91–92` | **no** |
| still-speed threshold | `velocity.length() > 0.4` m/s | `screening_event.gd:83`, `floor_manager.gd:66` | **no** (LAW-9 spec §5.2 asks for it) |
| screening move grace | `_move_t > 0.3` s before `_moved` | `screening_event.gd:84–86` | **no** |
| reel run on the rec TV | `play_screening(9.2)` | `screening_event.gd:37` | **no** (inline literal) |
| pre-window holds | 2.4, 1.4, 1.4 s | `screening_event.gd:39, 41, 43` | **no** (inline literals) |
| post-window hold | 1.2 s | `screening_event.gd:66` | **no** |
| PT for improvising | +10 on the beat, +5 late | `screening_event.gd:110, 113` | **no** |
| premiere clock stretch | `dur * 1.5` under ASSIST | `live_production.gd:350` | **no** (LAW-9 spec §5.2 asks for it) |
| Floor Manager watch | 3.0 s, armed within 9.0 m when facing him (`dot > 0.5`) | `floor_manager.gd:77–83` | **no** |
| `Merle.SPEED` | 1.6 m/s | `merle.gd:6` | yes (row `merle.gd,SPEED,1.6`) |
| `Merle.KETTLE` | `(8.0, 0.0, -1.0)` → KITCHEN | `merle.gd:7`; `Data/Rooms.csv` KITCHEN (8, 0) 6×5 | no (a landmark; C7) |
| `Merle.CHAIR` | `(2.6, 0.0, 1.2)` → REC ROOM | `merle.gd:8`; `Rooms.csv` REC ROOM (0, 0) 10×8 | no (C7) |
| `Merle.DOORWAY` | `(6.0, 0.0, -16.4)` → the TAPE LIBRARY / BENCH ROOM door gap | `merle.gd:9`; `Data/Doors.csv` row `TAPE LIBRARY,BENCH ROOM,6.0,-16.0,1.4,z` | no (C7) |
| Merle's screening seat | `(0.4, 0.0, 1.4)` → REC ROOM | `merle.gd:19` | no (C7) |
| Merle spawn | at KETTLE, `(8.0, 0.0, -1.0)` | `world_builder.gd:1061` | no (C7) |
| Merle collision | capsule r 0.3, h 1.6, centred y 0.8 | `world_builder.gd:1062–1067` | — |
| Merle name tag | `Label3D "MERLE"`, size 26, y 1.8, billboard, modulate (0.85, 0.93, 0.77) | `world_builder.gd:1071–1077` | — |
| RESPOND sign | `(-0.9, 2.5, 3.55)` REC ROOM | `world_builder.gd:715` | no (C7) |
| HOLD sign | `(0.9, 2.5, 3.55)` REC ROOM | `world_builder.gd:719` | no (C7) |
| rec-room TV (the screen) | `(-4.78, 1.6, 1.0)`, yaw π/2, slate `THE GLADHOUSE · CLUB PRINT` | `world_builder.gd:722–726` | no (C7) |
| projector | `(-1.4, 0.55, 1.0)`; collision box 0.6×0.5×0.9; body 0.5×0.4×0.7; lens r 0.06/0.08 h 0.22 at (−0.33, 0.08, 0); reels r 0.16 h 0.03 at z ±0.18; `Label3D "PROJECTOR"` size 24 | `world_builder.gd:728–768` | no (C7) |
| sign light | amber (0.89, 0.64, 0.24), range 4.0; lit energy 2.4, dark 0.0 | `cue_sign.gd:44–48, 62` | — |
| sign flash | energy → 3.8 in 0.05 s, then → 2.4 over 0.28 s | `cue_sign.gd:52–57` | — |
| sign label / housing | label lit (0.95, 0.72, 0.28) / dark (0.25, 0.19, 0.1); housing lit (0.16, 0.11, 0.05) / dark (0.09, 0.07, 0.04); box 1.5×0.55×0.14, surround 1.62×0.67×0.1, hood 1.66×0.06×0.3 tilted −0.15 | `cue_sign.gd:13–43, 60–63` | — |
| toast dwell | 3.0 s, REPLACED on each `notify` (no queue) | `hud.gd:551–553` `_on_notify` | — |
| settings key | `[access] assist = false` | `game_state.gd:317, 332` | — (settings.cfg, PORT-NOTES-STATE §4) |
| input bindings (defaults) | `interact` = E (physical 69), `respond` = SPACE (32), `improvise` = Q (81) | `project.godot` `[input]`; `GLYPH_MAP` `game_state.gd:125` | — |

Inline literals marked **no** are numbers the port must carry; the LAW-9
spec (§5.2) proposes a `URestorationAssist` constants header for the four
ASSIST numbers. Whether the rest (2.4 / 1.4 / 1.4 / 1.2 / 9.2 / 0.3 / 0.05 /
0.1 / +10 / +5 / 3.0 / 9.0) also go into `Timings.csv` is **OPEN** (the
migration map's "every number in the playtest protocol's knob list" names
the protocol's list, and P12 names no numbers).

---

## 2 · THE MINI-SCREENING — ORDER OF EFFECTS

`ScreeningEvent extends Interactable` (StaticBody3D). Prompt
(`get_prompt`, lines 21–24):

| State | Prompt | GameText |
|---|---|---|
| idle | `THE PROJECTOR · run the mini-screening (E)` | row 589 |
| `_running` | `THE PROJECTOR · reel running` | row 588 |

`interact()` (27–30): if `_running` return; else `_run()`. There is NO gate:
not on day, not on `screening_done`, not on `is_night`, not on mode, not on
DEMO. The projector re-runs the screening any number of times; only the
first completion sets `screening_done` (§7). Canon puts the mini-screening
on Day 1 as T1.7 (`docs/canon/restoration-game-master.md` §T1.7); code
merely lists it in the Day-1 objective ladder (§6).

`_run()` (33–73), a coroutine on the projector, wall-clock from the E press
(t is cumulative; every wait is `create_timer`, i.e. game time, pausable):

| t (s) | Effect | Verbatim | GameText |
|---|---|---|---|
| 0.0 | `_running = true`; `GameState.screening_active = true` (Merle walks to her seat, §5) | | |
| 0.0 | `tv.stage.play_screening(9.2)` — the rec-room TV runs the tape stage for 9.2 s with `_lunge_enabled = false` (`tape_stage.gd:154–156`). **The screening never lunges** (THE-LAWS 2, ONE STARTLE: the in-tape lunge belongs to the bench capture alone) | | |
| 0.0 | toast | `The club settles into the rows. The reel threads itself true.` | row 590 |
| 2.4 | toast | `ON TAPE · CHUM: 'Goodnight, Gladhouse! Say it with me!'` | row 591 |
| 3.8 | toast | `Half the room answers with the tape. In sync. Eyes forward.` | row 592 |
| 5.2 | `_answered=false; _moved=false; _move_t=0; _welapsed=0; _window=true`; `respond_sign.set_lit(true)`; toast (glyph-substituted: `SPACE`/`Q` become the bound key names, `game_state.gd` `glyphs()`) | `THE SIGN PULSES · SPACE on the beat · Q improvises · or hold still` | row 593 |
| 5.2, 6.0, 6.8, 7.6 | `respond_sign.flash()` × 4 (`for i in beats`, flash THEN wait BEAT) | | |
| 8.4 | `_window = false`; `respond_sign.set_lit(false)` | | |
| 8.4 | if `not _answered`: if `_moved` → toast; else `Achievements.unlock("A05")` + toast | `You said nothing, but you shifted. On tape, the head tilts toward the shift.` / `Stillness, held whole. Harriet's cup does not move. The episode resumes.` | rows 594 / 595 |
| 9.6 | `GameState.screening_active = false` (Merle resumes her schedule) | | |
| 9.6 | toast | `The reel runs out. Somebody is already asking to watch it again.` | row 596 |
| 9.6 | if `not screening_done`: `demo_mark("screening")`; `screening_done = true`; `save_log()` | | |
| 9.6 | `_running = false` | | |

Notes the port must keep:
- The reel on the TV (9.2 s) ends 0.4 s BEFORE the sequence does (9.6 s);
  the stage's own end-of-tape behaviour is `tape_stage.gd`'s, not the
  screening's.
- Only the RESPOND sign is wired (`projector.respond_sign = sign`,
  `world_builder.gd:729`). The HOLD sign is spawned (717–720) and NEVER lit
  by any script (grep `set_lit`/`flash` → only `screening_event.gd`). Canon
  says both signs are "lit only during response windows"
  (`docs/canon/restoration-room-inventory.md` REC ROOM row "Cue signs"). Code
  is the intent: HOLD stays dark in the port until a ruling. **OPEN** (§10).
- No lighting change. Canon's "lights down" (`game-master.md` §T1.7;
  `docs/production/ROOM-BRIEFS-3.1-3.5.md` §3.2 SCREENING state) has no code
  in the reference; ROOM-BRIEFS already marks that state OPEN.
- The toasts arrive 1.4 s apart while the HUD holds each for 3.0 s and
  REPLACES on the next (`hud.gd:551–553` `_on_notify`: `toast.text = text;
  _toast_t = 3.0`). Canon says "toasts queue and never overlap"
  (`docs/canon/restoration-accessibility-matrix.md` §COGNITIVE AND PACING);
  code replaces. Code is the intent; port the replace. Flagged in §8.

---

## 3 · THE STANCES — INPUT, JUDGMENT, OUTCOMES

Three stances (canon: AUDIENCE / QUIET / IMPROVISE, `game-master.md` §T1.7
"RESPONSE OPTION, first use"). Code names them by action: `respond`
(SPACE), `improvise` (Q), or neither.

**The beat** (`_on_beat()`, 89–94):

```
tol   = 0.35 if assist_on else 0.2
if is_dead("HARRIET"): tol = maxf(0.1, tol - 0.05)
phase = fmod(_welapsed, BEAT)          # BEAT = 0.8
on    = phase < tol or phase > BEAT - tol
```

`_welapsed` accumulates `delta` in `_process` from the frame the window
opened; the sign flashes on a timer at 0, 0.8, 1.6, 2.4 s of window. The two
clocks are independent in the reference (frame accumulation vs timer); the
port may drive both from one clock, which is a fidelity improvement, not a
change of contract. The beat instants are t = 0, 0.8, 1.6, 2.4 (and the
wrap at 3.2 is never reachable because the window closes there).

**Movement during the window** (`_process`, 76–86): each frame while
`_window`, find the player (group `"player"`, lazily); `held_still =
assist_on and Input.is_action_pressed("interact")`; if `velocity.length() >
0.4` and not held_still → `_move_t += delta`; `_move_t > 0.3` → `_moved =
true`. (Player `SPEED` is 3.1 m/s, crouch ×0.55 = 1.705 m/s, `player.gd:4,
10` — crouch-walking still counts as moving.)

**Answering** (`_unhandled_input`, 97–114): ignored unless `_window and not
_answered`. The FIRST press wins; a second press in the same window does
nothing. After an answer, movement is no longer judged (the `_moved` line
only prints when `not _answered`).

| Stance | Input | Beat | Effects | Verbatim | GameText |
|---|---|---|---|---|---|
| AUDIENCE | `respond` | on | `Achievements.unlock("A04")`; toast | `ON THE BEAT · 'Goodnight, Gladhouse.' The room exhales; a hand finds your shoulder.` | row 597 |
| AUDIENCE | `respond` | off | toast | `OFF THE BEAT · the room turns, all of it, one motion.` | row 598 |
| IMPROVISE | `improvise` | on | `GameState.add_pt(10)` (saves); toast | `'Goodnight, everyone.' On the beat. On tape, a delighted laugh. (PT +10)` | row 599 |
| IMPROVISE | `improvise` | off | `GameState.add_pt(5)` (saves); toast | `The improvisation lands late. Somewhere, a pencil notes it. (PT +5)` | row 600 |
| QUIET | none, still | — | `Achievements.unlock("A05")`; toast | `Stillness, held whole. Harriet's cup does not move. The episode resumes.` | row 595 |
| (shifted) | none, moved | — | toast only | `You said nothing, but you shifted. On tape, the head tilts toward the shift.` | row 594 |

Six outcome lines. `docs/production/restoration-playtest-protocol.md` P12
says "confirm all five outcome lines are reachable" — the sixth (shifted) is
in code and reachable; treat P12 as under-counting, code is the intent.

Achievements (`docs/production/restoration-achievements-design.md` rows
A04, A05): A04 `ON THE BEAT` on any on-beat respond in a screening; A05
`STILLNESS, HELD WHOLE` on QUIET. Both are re-attemptable on every re-run
of the projector (idempotent `unlock`). No achievement for improvising;
IMPROVISE is Producer Track only. `unlock()` persists silently and NEVER
toasts during play; the queue flushes at the morning (`night_changed`
false → `flush_to_toasts`: `FILED · <title>` for ≤2, else `FILED · %d
entries, %s among them.`) or at the title (`achievements.gd` `_ready`
connects `night_changed`; `flush_to_toasts` 88–97). The deferral does NOT
read `screening_active` in the reference; it is unconditional. Under DEMO
`unlock()` is a no-op (`achievements.gd:45–46`).

Harriet's death tightens the beat by 0.05 s with a floor of 0.1
(`docs/canon/restoration-casualty-ledger.md` HARRIET RIPPLES: "stances are
judged 0.05 tighter without her metronome presence"; QA-41). Note the floor
only bites if tol ≤ 0.15, which no shipped value reaches (0.2 → 0.15, 0.35
→ 0.30); the port keeps the `maxf` anyway (the number is canon).

---

## 4 · ASSIST — THE RULE (cite `UE-ACCESS-SPEC-LAW9.md` §5; do not re-derive)

`docs/production/UE-ACCESS-SPEC-LAW9.md` §5 already specifies the UE ASSIST
port and names this unit as its transcription source (§5.5). These notes
restate only what that section needs from the code and defer to it on
homes, constants header, and tests.

**One switch.** `assist_on: bool = false` (`game_state.gd:70`), persisted as
`[access] assist` in `user://settings.cfg` (`load_settings` 317,
`save_settings` 332), NOT in the save (PORT-NOTES-STATE §2/§4). Set only by
`set_assist(on)` (365–367: assign, `save_settings()`; no signal). The booth
row (`options_panel.gd:66–67`) is a check bound to `set_assist`, labelled
`ASSIST · wider beats, slower clocks, hold E to be still` (GameText row 522). Canon:
"DIFFICULTY: RULED, ASSIST only. One game, honestly tuned."
(`docs/production/restoration-gap-audit.md` §5); "never gates content or
endings" (`restoration-accessibility-matrix.md` §COGNITIVE AND PACING);
LAW 9, ACCESS IS CANON (`docs/packet/portbrief/THE-LAWS.md` 9).

**Exactly three readers** (grep `assist_on` across `scripts/`):

| # | Site | Rule | Canon |
|---|---|---|---|
| 1 | `screening_event.gd:90` | beat tolerance 0.2 → 0.35 (then the Harriet penalty, §3) | matrix §COGNITIVE AND PACING; conformance pass addendum c031 "R5 … three mercies" |
| 2 | `screening_event.gd:82` and `floor_manager.gd:65` | `held_still = assist_on and Input.is_action_pressed("interact")` — holding the INTERACT ACTION counts as still. Screening: 0.3 s grace before `_moved`. Floor Manager: instant — `velocity > 0.4 and not held_still` → `_watch_t = 0`, label `FLOOR MANAGER` (row 147), toast `You moved on camera. Somewhere, a take is ruled spoiled.` (row 148); else when the 3.0 s watch expires → `The hand lowers. The take holds.` (row 149) | QA-18, QA-19 (`docs/production/restoration-qa-regression.md`) |
| 3 | `live_production.gd:350` | `t = dur * (1.5 if assist_on else 1.0)` in `_timed(dur, label)`; status `"%s · 0:%02d" % [label, ceil(t)]`; on expiry `_row_taken()` | c031 "premiere clocks times 1.5"; QA-18 |

Nothing else reads it: not `capture_bench.gd`, not any achievement, ending,
PT award or ledger entry (the LAW-9 spec's `NeverGates` lint, §5.4).
`restoration-controls-map.md` says the bench capture "ASSIST relaxes both";
no code does — already **OPEN** in the LAW-9 spec §10 item 5; not re-opened
here. The matrix's "stretches screening timing 1.5x" is a paraphrase of the
premiere clocks (LAW-9 spec §5.1); nothing in the screening is stretched.

"Hold E" in the label means the ACTION `interact`, not the key: the LAW-9
spec §5.2 item 2 requires the UE check to read the Enhanced Input action so
a remapped interact still counts. The reference does exactly that
(`Input.is_action_pressed("interact")`).

---

## 5 · MERLE — THE SCRIPT

`Merle extends Interactable` (StaticBody3D). Spawned by `_spawn_club()`
(`world_builder.gd:1060–1078`) at KETTLE with the capsule, the plate-accurate
build (`CharacterKit.merle()`, `character_kit.gd:628+`: maroon cable
cardigan, floral blouse and apron with the stitched 58, reading glasses on
a beaded chain, the towel) and the `MERLE` tag. Canon plate:
`docs/canon/restoration-cast-sheets.md` §MERLE COTTRY ("hands never
still"; "NEW CANON: MERLE FOUNDED THE CLUB WITH LELAND"; "the
never-sinister rule survives untouched").

### 5.1 Her schedule (`_where()`, 17–24; evaluated every physics frame)

Priority order, first match wins:

| # | Condition | Target | Room | Canon |
|---|---|---|---|---|
| 1 | `GameState.screening_active` | `(0.4, 0, 1.4)` | REC ROOM (the rows) | T1.7 "The club gathers" (`game-master.md`) |
| 2 | `_pen_up()` — any node in group `decision_ledger` with `is_pen_up()` true (`decision_ledger.gd:19–20`: `_hover >= 0 and decision == ""`, i.e. the player has pressed E on the ledger on Day ≥ 3 and not yet committed) | `DOORWAY (6.0, 0, -16.4)` | the TAPE LIBRARY → BENCH ROOM door gap (`Doors.csv` row 9) | "Merle in the doorway, hands empty, watching the pen, saying nothing." (`game-master.md` §T5 ledger; `restoration-player-routing.md` "The decision point"; `walkthrough-levels-endings.md` open question 4) |
| 3 | `GameState.is_night or GameState.lockdown_done` | `CHAIR (2.6, 0, 1.2)` | REC ROOM | night: OPEN (see below); lockdown: T4.10 / T5 "front row" (`game-master.md`) |
| 4 | otherwise (day) | `KETTLE (8.0, 0, -1.0)` | KITCHEN | "Merle's scenes anchor here" (`restoration-room-inventory.md` KITCHEN "Kettle") |

Movement (`_physics_process`, 12–14): `global_position =
global_position.move_toward(target, SPEED * delta)` — a straight line at
1.6 m/s, no navigation, no collision response (she is a StaticBody3D whose
transform is set directly; she passes through walls between KITCHEN and
the BENCH ROOM doorway). Canon is silent on how she gets there. **OPEN**:
nav-mesh walk vs the reference's straight line (§10).

Her "DOORWAY watch" at night: `restoration-casualty-ledger.md` MERLE
RIPPLES says "If M1: nights lose her DOORWAY watch and night trips escalate
one stage early." No code gives her a night doorway post (nights = CHAIR)
and no code escalates trips on her death. Code is the intent; the ripple is
canon-only. **OPEN** (§10).

### 5.2 Her prompt (`get_prompt`, 34–36)

`MERLE · %s (E)` (row 494) with `%s` = `in the doorway` if `_pen_up()`,
else `in her chair` if `is_night`, else `at the kettle` (rows 491–493 hold
the three fragments; row 493 is `at the kettle`). Note: under
`lockdown_done` by day she SITS in her chair (rule 3) but the prompt says
`at the kettle` (the prompt does not read `lockdown_done`). Code is the
intent; port it as is and list it in §8.

### 5.3 Her visibility and death (`_process`, 39–41; `interact`, 44–46)

`if is_dead("MERLE"): visible = false` — every frame. She keeps moving on
her schedule and keeps prompting (`get_prompt` has no dead check); only
`interact()` returns early. An invisible Merle can still be targeted and
shows `MERLE · … (E)`. Code is the intent; listed in §8 as a port-fidelity
choice.

Merle's ONLY built death is **M1 · THE SECOND VIEWING**
(`fire_tape_dock.gd:29–31, 64–69`): at the fire tape, if `not
fire_tape_watched and not is_dead("MERLE") and not merle_offered` →
`merle_offered = true`; toast `MERLE, from the doorway: 'I was there the
first time. I'd rather not be alone for the second.'` (row 130); status
`E · let her stay for it · Q · turn her away` (row 131); E → she stays (row
132), Q → she leaves (row 133). If she stayed, after the reel:
`Merle pats your hand once, warm, and says 'there, that wasn't so'` (row
139) · 2.2 s · `Her chair is empty. Her voice finishes the sentence from
inside the speaker: 'bad.'` (row 140) · 2.6 s · the kettle line, caption
`[THE KETTLE, TWO ROOMS AWAY, CLICKS OFF]`, then
`mark_casualty("MERLE", "M1 · THE SECOND VIEWING", "carried a second
time, mid-sentence")`. Canon: `restoration-casualty-ledger.md` §MERLE M1
("REFUSING her, which reads as cruelty, saves her"). LAW 7 (EVERY DEATH HAS
A SIGNATURE): the choice is the E press; the binder names it.

**M2 · THE HOME SINGER** (premiere; `casualty-ledger.md` §MERLE M2) has NO
code: grep `mark_casualty(` finds nine distinct causes (M1, V1 ×2 sites,
V2, H1, H2, F1, F2, L1, L2) and no `MERLE` site in `live_production.gd`.
The ledger's AS BUILT paragraph claims "All ten deaths"; the tenth is not
in the reference. Code is the intent for the port; whether M2 is authored
in UE is **OPEN** (§10). Retake/finale notes (C9, C11) own the premiere.

### 5.4 Her lines (`interact`, 44–64), priority order

| # | Condition | Verbatim | GameText |
|---|---|---|---|
| 0 | `is_dead("MERLE")` | (returns; nothing) | |
| 1 | `_pen_up()` | `She says nothing. Her hands are empty and open, watching the pen.` | row 495 |
| 2 | `crate_opened and not merle_1974` | the 1974 monologue (§5.5) | |
| 3 | `decision == "PERFORM"` | `MERLE · 'You'll be wonderful. You were always going to be.'` | row 496 |
| 4 | `decision == "AUTHENTICATE"` | `MERLE · 'The whole world gets to be carried now.'` | row 497 |
| 5 | `decision == "DESTROY"` | `MERLE · 'The degausser hums at night. I hear it too.' Her hands keep drying the plate.` | row 498 |
| 6 | `day == 1` | `MERLE · 'Oh, look at your gloves. You brought your own gloves.'` | row 499 |
| 7 | `day == 2` | `MERLE · 'He asks so many questions. You ask the right amount. I can tell.'` | row 500 |
| 8 | else (day ≥ 3) | `MERLE · 'You've given us back a piece of our childhood, do you know that?'` | row 501 |

Canon for the lines: row 499 ← T1.1 "Oh, look at your gloves, you brought
your own gloves"; row 500 ← T2.3 [ASK] "He asks so many questions, though …
You ask the right amount. I can tell."; row 501 ← T1.6 "You've given us
back a piece of our childhood, do you know that?" (`game-master.md`). Note
the code plays the T1.6 line on Day ≥ 3, not Day 1 (canon T1.6 is Tape 1
after the capture). Code is the intent. Rows 496–498 (post-decision) have
no game-master line; they are code-canon.

The interact never saves except through the monologue (§5.5); it awards
nothing; it reads no ASSIST (§4).

### 5.5 The 1974 monologue (`_monologue`, 67–82) — T4.6, `game-master.md`

Trigger: interact while `crate_opened and not merle_1974`. First effect:
`merle_1974 = true; save_log()` (save key 54) — set BEFORE the first line,
so a quit mid-monologue still counts. Then seven toasts:

| t (s) | Verbatim | GameText |
|---|---|---|
| 0.0 | `MERLE · 'I was seven. Route 9, the culvert end, past where the county stopped mowing.'` | row 502 |
| 3.2 | `'I walked out after a dog that wasn't mine, and the light went, and the corn does not care how loud a girl is.'` | row 503 |
| 6.6 | `Her hands, for once, empty and open. 'And then the dark got warmer. Fur like a coat closet.'` | row 504 |
| 9.8 | `'It carried me the whole way singing the closing song, and it set me down where the porch light reached.'` | row 505 |
| 13.0 | `'The papers said a searcher found me. No searcher sings.'` | row 506 |
| 16.0 | `'So bring me every date and every gap and every terrible arithmetic, and I will hold them. I promise you I will hold them.'` | row 507 |
| 19.4 | `'But I was carried. You don't vote against being carried.'` | row 508 |

Holds: 3.2, 3.4, 3.2, 3.2, 3.0, 3.4 (`_wait`). The monologue is not
interruptible and does not set `_running` — a second E during it starts
nothing new (branch 2 is now false) and falls through to branches 3–8,
which WILL toast over it. Code is the intent; note for the port.
Achievement A12 `NO SEARCHER SINGS` (hidden) unlocks by the 1-s poll on
`merle_1974` (`achievements.gd:69`). Canon text: `game-master.md` §T4.6
(code abridges "and it waited in the ditch till my mother's arms had me"
and the stage direction "she looks at the screen the way people look at
churches" — the verbatim toasts above are the port's text). The comfort is
played straight (`restoration-walkthrough-levels-endings.md` "The comfort
is never the trap").

### 5.6 Merle elsewhere (owned by other notes; listed so nothing is lost)

- LOCKDOWN (`lockdown.gd:32`): `MERLE · 'Fifty years, and we have a
  premiere. Lock-in's just till broadcast, dear.'` (row 481) — C11.
- Rejected edit close (`rejected_edit.gd:61`): `MERLE · soft, hands folded,
  merciless as weather: 'Sit down, sweetheart. There's cobbler.'` (row 558).
- Ledger commit line for PERFORM (`decision_ledger.gd:9`): `PERFORM. Merle,
  in the doorway, says nothing. The pen was the loudest thing in the
  building.` (row 84).
- Epilogue variants on `is_dead("MERLE")` in `hud.gd` `_end_burn` /
  `_end_producer` (rows 284, 304 and neighbours) and the séance answer 28
  variant `I KNOW. SHE'S HERE NOW.` (`seance_dock.gd:80–81`) — C11.
- `all_cast_dead()` counts `MERLE` (`game_state.gd:103`) — ending 0.

---

## 6 · THE DAY-1 FLOW (the objective ladder, `objective_text()` 687–710)

Day 1 as the ladder states it, top to bottom, each rung shown only while
the one above is satisfied and `not is_night`:

| Rung | Test | Objective text | GameText |
|---|---|---|---|
| 1 | `not _signed_station("S1")` | `DAY 1 · sign the log at S1, the library landing` | row 181 |
| 2 | `not screening_done` | `DAY 1 · run the mini-screening at the rec room projector` | row 182 |
| 3 | `captures.size() == 0` | `DAY 1 · capture Tape 1 at the bench · it runs real time` | row 183 |
| 4 | else | `DAY 1 · end the day at Rita's bed` | row 184 |

(Higher rungs of the ladder — DEMO short-circuit, `finale_done`, `decision`,
`run_complete and day >= 3`, `is_night` — precede these; PORT-NOTES-STATE §6
lists the full ladder.)

The ladder is ADVICE, not a gate. Nothing in code orders these: the bench
does not check `screening_done` (grep `screening` in `capture_bench.gd` →
none), the projector does not check S1, the bed does not check any of
them. `bed_prop.gd`: `RITA'S BED · end the day (E)` → `set_night(true)`
(toast `NIGHT · the building belongs to the schedule.`, `night_changed`);
`RITA'S BED · sleep until morning (E)` → `set_night(false)` → `day += 1;
current_tape = min(day, 5)`, the MORNING toast, then the achievement flush
(`game_state.gd:467–480`). Day 1's night is Night 1 (the Floor Manager trip
is `floor_manager.gd`'s; QA-19).

Canon vs code on Day 1: canon puts the capture on Day 2 and the
mini-screening as the Tape 1 act climax (`restoration-walkthrough-levels-
endings.md` "Day 1." / "Day 2."; `restoration-player-routing.md` Day 1 /
Day 2 spines; `game-master.md` T1.5 CAPTURE ONE precedes T1.7). Code puts
the S1 signature, the screening AND the Tape 1 capture on Day 1 and
advances the day only at the bed. Code is the intent (PORT-BRIEF). The
demo funnel agrees with code: `docs/production/restoration-demo-cut-plan.md`
§flow "sign S1 → the mini-screening → the bench: capture Tape 1"; funnel
events `started`, `s1_signed`, `screening`, then capture
(`demo_mark("screening")` at `screening_event.gd:70`).

DEMO: REC ROOM is in `DEMO_OPEN` (`world_builder.gd:60`), the projector is
spawned unconditionally (`_spawn_screening` has no DEMO branch), so the
screening is in the demo. The demo plan says the stances are "judged
gently on Matinee defaults"; the code judges by ASSIST only — `mode` is not
read by `screening_event.gd`. Code is the intent.

---

## 7 · STATE TOUCHED (against PORT-NOTES-STATE)

| Field | Kind | Written by | Read by | Notes |
|---|---|---|---|---|
| `screening_done` | saved, key 19, bool, default false | `screening_event.gd:71` (once); `reset_new_game` → false | `objective_text` rung 2 | present in C++ (`ScreeningDone` / `bScreeningDone`) |
| `screening_active` | session-only bool, default false; NOT reset by `reset_new_game` | `screening_event.gd:35, 67` | `merle.gd:18` ONLY | absent in C++ (§9) |
| `assist_on` | settings, `[access] assist`, default false | `set_assist` | the three sites (§4) | absent in C++ (§9; LAW-9 spec §1.1) |
| `pt` | saved, key 12 | `add_pt(10 / 5)` (saves) | routing on-ramp B | present in C++? — PORT-NOTES-STATE §6 lists `pt` among the 32 missing |
| `merle_1974` | saved, key 54 | `merle.gd:68` (+ `save_log`) | `merle.gd:50`, A12 poll | present in C++ |
| `merle_offered` | saved, key 47 | `fire_tape_dock.gd:30` | `fire_tape_dock.gd:29` | present in C++ |
| `casualties` (`MERLE`) | saved, key 46 | `fire_tape_dock.gd:69` | `merle.gd:40, 45`; hud; seance; `all_cast_dead` | present in C++ |
| `lockdown_done`, `is_night`, `decision`, `crate_opened`, `day` | saved / session | elsewhere | `merle.gd` schedule + lines | |

Signals: the screening and Merle EMIT none of their own. They drive
`notify` (via `toast`), `caption` (M1 only), and the save; Merle reads
`is_night` by polling, not by `night_changed`. Achievements: A04, A05 (direct
`unlock`), A12 (poll). Nothing here touches the Rundown; `rundown.gd` does
not read `screening_active` (grep), so the brain is unaware a screening is
running — Night is the only gate the brain honours (STATE §3
`night_changed`).

---

## 8 · CANON CROSS-CHECK (code is the intent; each row is a note, not a fix)

| Topic | Canon says | Code does | Port |
|---|---|---|---|
| Both signs light | RESPOND and HOLD "lit only during response windows" (`room-inventory.md`); design doc §Cue signs names both | only RESPOND is wired; HOLD never lights | keep dark; OPEN |
| Lights down | T1.7 "lights down"; ROOM-BRIEFS §3.2 SCREENING state | no lighting change | OPEN (ROOM-BRIEFS already) |
| Toasts | "toasts queue and never overlap" (`accessibility-matrix.md`) | HUD replaces, 3.0 s dwell | port the replace; flag for 5.2 |
| Outcome count | P12 "all five outcome lines" | six (the shifted line) | six |
| PT for improvising | routing on-ramp B: "+10 at the Tape 2 screening" | +10 / +5 at the ONLY built screening (Tape 1) | as code |
| Vess's after-line | T1.7 "VESS: The sign. Over the door. You saw it light." | absent | OPEN |
| Screening judged by mode | demo plan "judged gently on Matinee defaults" | ASSIST only, mode unread | as code |
| Day of the capture | Day 2 (walkthrough, routing, T1.5 before T1.7) | Day 1, after the screening (ladder) | as code |
| Merle's T1.6 line | Tape 1, after the capture | `day >= 3` default line | as code |
| Merle night post | casualty ledger ripple: "nights lose her DOORWAY watch" | nights → CHAIR; no doorway watch; no trip escalation on M1 | OPEN |
| Merle's route | silent | straight line 1.6 m/s through walls | OPEN |
| M2 THE HOME SINGER | casualty ledger M2 ("All ten deaths" AS BUILT) | not in code | OPEN |
| Dead Merle | silent | invisible, still moves, still prompts, interact inert | as code or fix; OPEN |
| Lockdown prompt | — | sits in chair by day, prompt says `at the kettle` | as code; flag |
| Mini-screening text | T1.7: CHUM "Goodnight, Gladhouse! Say it with me!"; CLUB answers | rows 591–592 match the beat and the club's unison | verbatim |
| The never-sinister rule | cast sheets; walkthrough "comfort is never the trap" | no scare is delivered through Merle; her death is warm to the last word | holds |
| LAW 2 ONE STARTLE | the in-tape lunge is the single jump scare | `play_screening` disables the lunge | holds |
| LAW 5 SILENCE CONTRACTS | Chum speaks nowhere (in-game); the bell | the screening's Chum lines are ON TAPE, as text toasts; no Chum audio; no bell | holds — Chum's on-tape line is tape content, the pre-fire show; OPEN whether the UE screening plays audio for it (audio bible, C15) |
| LAW 9 ACCESS IS CANON | assist ships in every build | one switch, three sites | LAW-9 spec §5 |

---

## 9 · DELTAS: current C++ vs these notes (the 0.8b-5 "screening + assist" checklist)

Against `ue/Restoration/Source/Restoration/` at 0e8166d (files:
BenchCapture, Harriet, RestorationClock, RestorationGameMode,
RestorationInteractable, RestorationState, RitaCharacter, Rundown):

- [ ] `URestorationState`: add `bool bScreeningActive = false` (session-only,
      not in the SaveGame, not reset by new game — STATE §2).
- [ ] `bScreeningDone` exists (`RestorationState.h:157`, save `ScreeningDone`
      line 74); confirm `ResetNewGame` clears it (STATE §2 says it is reset).
- [ ] Settings subsystem with `Access_Assist` (LAW-9 spec §1.1 owns the
      class; this unit only needs the bool and its `[access] assist` key).
- [ ] `URestorationAssist` constants header per LAW-9 spec §5.2, and the
      four numbers into `Data/Timings.csv` (0.2, 0.35, 0.4, 1.5).
- [ ] `ACueSign` actor: housing + label + amber point light per §1; `Flash()`
      (3.8 → 2.4 over 0.05 + 0.28 s) and `SetLit(bool)`. Two instances from
      data at the §1 positions (RESPOND wired, HOLD dark).
- [ ] `AScreeningEvent : AActor, IRestorationInteractable`: `GetPrompt` rows
      588/589; `Interact` → `Run()`; the §2 timeline with the exact holds;
      `OnBeat()` per §3; `Tick` movement rule per §3 (Enhanced Input action
      value for `IA_Interact`, pawn velocity > 0.4 m/s, 0.3 s grace);
      `respond`/`improvise` bound to `IA_Respond` / `IA_Improvise`; first
      press wins; A04/A05 via the achievements subsystem; `AddPt(10/5)`;
      `DemoMark("screening")`; `bScreeningDone` + save on first completion.
- [ ] The rec-room TV as a second tape-stage instance (`BenchTV` at
      `(-4.78, 1.6, 1.0)`, yaw π/2) with `PlayScreening(9.2)` = play with
      lunge disabled. The bench-capture stage (`BenchCapture.cpp`) must
      expose the lunge switch.
- [ ] `AMerle : AActor, IRestorationInteractable`: schedule per §5.1 (four
      targets, priority order, 1.6 m/s straight line unless ruled
      otherwise), prompt per §5.2 (row 494 + fragments 491–493),
      visibility-on-death per §5.3, lines per §5.4 (rows 495–501), monologue
      per §5.5 (rows 502–508, holds 3.2/3.4/3.2/3.2/3.0/3.4, save first).
      Needs `IsPenUp()` on the ledger actor (a `decision_ledger` tag or a
      subsystem query) — the ledger itself is Phase 4.
- [ ] `AFloorManager`: assist-hold in the 3.0 s watch (mercy 2) — Phase 4
      per LAW-9 spec §5.5; listed so the rule is not lost.
- [ ] `ALiveProduction::Timed`: ×1.5 (mercy 3) — the finale port (C11).
- [ ] `ObjectiveText()`: rungs 1–4 of §6 with rows 181–184 (the ladder is
      STATE §6's item; these rows are its Day-1 half).
- [ ] Tests (from LAW-9 spec §5.4): `Assist.BeatWindow`, `Assist.HoldStill`;
      plus, for this unit: `Screening.Timeline` (window opens at 5.2 s ± a
      frame, closes at 8.4, `bScreeningActive` false at 9.6),
      `Screening.FirstPressWins`, `Screening.NeverLunges`,
      `Merle.Schedule` (four states → four targets), `Merle.PenUp` (ledger
      hover moves her to the doorway and back).

---

## 10 · OPEN (canon is silent or contradicts itself; the owner rules)

1. **HOLD sign.** Canon lights both signs in windows; code lights RESPOND
   only and never HOLD. Port dark HOLD, or author its cue?
2. **Lights down.** T1.7's "lights down" has no code and no EV anywhere in
   canon (ROOM-BRIEFS-3.1-3.5 §0). Which fixtures dim, to what, CUT or fade?
3. **Vess's after-line** at T1.7 ("The sign. Over the door. You saw it
   light.") is not built. Add in UE, or leave canon-only?
4. **Screening audio.** The reference plays no audio for the on-tape Chum
   line (toasts only). The audio bible / C15 decide; LAW 5 must be read
   against pre-fire tape content (band-limited, per motion & sound canon).
5. **Merle's route.** Straight line at 1.6 m/s through walls, or nav-mesh
   walk? Canon silent.
6. **Merle's night post.** Casualty ledger says nights have her "DOORWAY
   watch" and M1 escalates night trips; code has neither.
7. **M2 THE HOME SINGER.** Canon death with no code; the ledger's "All ten
   deaths" is nine in source.
8. **Dead Merle's body.** Invisible but moving and prompting. Faithful port
   or hide-and-disable?
9. **Lockdown-day prompt.** `at the kettle` while she sits in her chair.
   Faithful port or read `lockdown_done` in the prompt?
10. **Toast queue vs replace.** Canon says queue; code replaces. The UE HUD
    (5.2) picks; this unit ports the replace.
11. **Inline literals into `Timings.csv`.** 2.4 / 1.4 / 1.4 / 1.2 / 9.2 /
    0.3 / 0.05 / 0.1 / +10 / +5 / 3.0 / 9.0 — table them or leave in code?
12. **Re-runnable screening.** The projector runs any number of times, any
    day; A04/A05 re-attemptable. Canon treats T1.7 as a once-per-act set
    piece. Faithful port, or gate after `screening_done`?
13. **Screening judged by mode.** Demo plan says Matinee softens the
    stances; code reads ASSIST only.
