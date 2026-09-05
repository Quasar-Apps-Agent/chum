# PORT NOTES · FINALE — the premiere, the cascade, the endings and LOCKDOWN, transcribed

**Unit C11 (CLOUD-OK).** This is the implementation checklist for the last
night: `live_production.gd` (the premiere with its incidents and the
`INCIDENT` / `RESOLVED t=` log that invariant I06 reads), `cascade.gd` +
`liveness_check.gd` (the Night 4 cascade and the liveness log that I07
reads), `lockdown.gd` (Tape 4's turn), the `start_finale` / `mark_ending`
seam in `game_state.gd`, the ending scripts in `hud.gd`, and every gate in
other scripts that the premiere flips. Source of truth: those files at
`origin/main` 0e8166d — `live_production.gd` (434 lines), `cascade.gd` (50),
`liveness_check.gd` (35), `lockdown.gd` (45), `finale_breaker.gd` (16),
`finale_fixture.gd` (16), `patchbay_console.gd` (93), `invariant_parser.gd`
(78), `bot_driver.gd` (105), `soak_runner.gd` (42), plus the cited lines of
`hud.gd` (561), `rundown.gd` (482), `game_state.gd` (777),
`world_builder.gd` (1446), `decision_ledger.gd`, `bed_prop.gd`,
`achievements.gd`, `credits.gd`, `title.gd`, `door.gd`, `seance_dock.gd`.
Where these notes and that code disagree, THE CODE IS THE INTENT
(`docs/packet/portbrief/PORT-BRIEF.md` line 2: "where prose and code
disagree, the code is the intent"); fix the notes. Where canon prose goes
further than the code (§9), the code is still the intent; the prose is
listed so nobody re-invents it by accident.

UE homes per `docs/packet/portbrief/UE5-MIGRATION-MAP.md`:
- LIVE PRODUCTION (line 15): "live_production.gd → a GameMode-scoped
  director actor; cue marks as trigger volumes; the switcher as Enhanced
  Input actions; incidents and fixtures port as-is; premiere_log unchanged."
- CASCADE AND LIVENESS (line 16): "cascade.gd and liveness_check.gd → the
  same two actors; the HUD blackout layer becomes a post-process weight or
  a UMG scrim (UMG scrim recommended: identical layering guarantee under
  labels)."
- LOCKDOWN (line 8, under CAMERA FEEDS): "tally, kill, re-patch, and
  lockdown sync_to port one to one (sync = assigning one RT to many screen
  materials)."
- The endings (`hud.gd` `_end_*`) have no named home in the map. OPEN (O1):
  they are HUD-driven text sequences today; the UMG retake panel from unit
  C9 (`ue/PORT-NOTES-RETAKE.md`, in flight) is their natural host.
- The harness (line 17 territory, already built): every telemetry line lands
  in one `Saved/decision_log.txt` and `tools/invariant_parser.py` reads the
  coverage / liveness / premiere sections from it (PROGRESS.md 0.9a; the
  parser's docstring lines 3–7). So `user://premiere_log.txt` and
  `user://liveness_log.txt` become line PREFIXES in the unified log, not
  files (§8.4).

The laws these systems serve, verbatim from `docs/packet/portbrief/THE-LAWS.md`:
- LAW 1 (line 2) "ON CAMERA IS SAFE. An active camera cone prevents the
  strike, always." — the premiere yield (§4.13) is its Tape 5 form
  (invariants I03/I05, `docs/production/restoration-invariant-suite.md`
  lines 7, 9).
- LAW 5 (line 6) "SILENCE CONTRACTS. The bell rings once, at the finale
  beat, and its caption says so." — `hud.gd:452` `Sfx.bell()`, whose body
  captions `[THE BELL RINGS · once]` (`sfx.gd:17`). §6.2.
- LAW 6 (line 7) "...window holds bind except during cascade." — `door.gd:29,40`
  (§2.5).
- LAW 7 (line 8) "EVERY DEATH HAS A SIGNATURE..." — every `mark_casualty`
  in this file is tabled in §6.4 with its cause tag.
- LAW 8 (line 9) "THE INTERFACE MAY LIE EXACTLY ONCE, where the design doc
  says it does, and nowhere else." — `mark_ending("THE NEW PRODUCER", true)`
  is the only `lie=true` call in the codebase (§6.3, §6.5).
- LAW 11 (line 12) "...every threshold costs him 2.2 s, and that toll is the
  player's counterplay." — kept during the crossing (§5).

Constants that are canon (never change the numbers). None of these is in
`ue/Restoration/Data/Timings.csv` except the three `rundown.gd` rows noted;
the rest are literals in the scripts and should be added to the CSV by the
unit that ports them (OPEN O2 — the CSV is `tools/extract_data.py` output and
this unit does not touch tools):

| Constant | Value | Source | Notes |
|---|---|---|---|
| Cue 2 clock (cart deck) | 45.0 s | live_production.gd:76 | re-entered on expiry, forever |
| Blackout clock (main bus) | 30.0 s | live_production.gd:104, 111 | uncredited / dead-Vess branches |
| ASSIST clock multiplier | ×1.5 | live_production.gd:350 | QA-18 "premiere clocks half again longer" |
| Pressure interval | `max(14.0, 26.0 − 4.0·fail_takes)` s | live_production.gd:393 | first roll 26 s after cue 1 clears |
| Club auto-fix threshold | incident age `> 40.0` s at a pressure tick | live_production.gd:399 | the I06 guarantee |
| I06 slow-fix verdict | `RESOLVED ... t=` value `> 41.0` | invariant_parser.gd:75; tools/invariant_parser.py:66 | 1 s of grace over the 40 |
| Tally refusals per incident | 2 | live_production.gd:329 | "tally refusals never exceed 2" (I06) |
| Blind calls to F2 | `>= 3` (cumulative, whole premiere) | live_production.gd:335 | QA-43 "exactly the third" |
| Boom holds per incident | 1 | live_production.gd:339-342 | "boom holds exactly 1" (I06) |
| THE MARK | `(-15.5, 1.0, -26.5)`; on-mark `< 1.6` m | live_production.gd:6, 321 | Studio A |
| Player placed at | `(-15.5, 1.0, -28.5)` | live_production.gd:53 | 2 m behind the mark |
| Chum on his mark | `(-15.5, 0, -31.2)` | live_production.gd:259 | the stage body, `CharacterKit.chum_mini()` |
| Cart deck breaker | `(-5.5, 0.9, -28.2)`, box 0.5×0.9×0.4 | live_production.gd:272-275 | `FinaleBreaker` |
| AUX PANEL (TALLY_HOUSE) | `(-5.0, 0.9, -29.4)` | live_production.gd:288 | fixes TALLY or HOUSE |
| BOOM WINCH | `(-13.4, 0.9, -30.4)` | live_production.gd:289 | |
| CARD STAND | `(-16.9, 0.9, -27.4)` | live_production.gd:290 | |
| Program camera required | `1`, at every cue mark | live_production.gd:61, 81 | `need_cam` is never ≠ 1 |
| Switcher keys | `cam_1/2/3` = physical 1/2/3 | project.godot:101-115 | Enhanced Input in UE |
| HOUSE blackout | scrim alpha 0.35 | live_production.gd:408 | cleared on resolve / cleanup |
| Crossing clock | 75.0 s; 62.0 if VESS dead; −13.0 if `fader_self` | live_production.gd:232-234 | canon: walkthrough addendum line 289 |
| Crossing goal radius | `< 2.0` m to the little door | live_production.gd:242 | fallback goal `(-15.5, 0, -31.2)` |
| He starts the crossing at | `(5.5, 0.0, -29.5)` | live_production.gd:227 | ~21 m behind her |
| Crossing speed | `AF_CROSSING_SPEED` 1.6 m/s | rundown.gd:21; Timings.csv row 23 | present in `ARundown` |
| Crossing strike radius | `_strike_r` = 2.2 (2.6 if `strikes >= 3`) | rundown.gd:24, 150 | set on the last ON AIR flip |
| Crossing fold | 2.2 s at `< 1.0` m of a door, 6.0 s per-door cool | rundown.gd:333-347; Timings.csv rows 21-22 | LAW 11 |
| Crossing footfall | `Sfx.thunk` every 0.7 s | rundown.gd:227-230 | |
| Caught pose | 0.9 s | rundown.gd:222 | then `run_ended` |
| Fader self-hold | 4.6 s | live_production.gd:217 | controls map line 6: "E held 4.6 s for hers" |
| Cascade blackout stages | 0.55 → 0.75; restore B → 0.55; C → 0.0 | cascade.gd:22, 30; patchbay_console.gd:54, 59 | |
| Cascade beats | 4.0 s, then 16.0 s | cascade.gd:25, 27 | |
| Cascade kills | `rigs[2:4]` then `rigs[4:6]` | cascade.gd:23, 31 | indices into `world_builder._rigs` |
| Cascade trigger | `is_night && day >= 4` | cascade.gd:15 | once per save (`cascade_done`) |
| Rundown warn narrowing | `max(3.5, warn_r − 1.5)` while `cascade_active` | rundown.gd:152-153 | already in C8's checklist |
| Liveness cadence | every 5.0 s of physics time | liveness_check.gd:17 | I07 |
| Lockdown trigger | `assets.size() >= 4 && is_night` | lockdown.gd:21 | once per save |
| Lockdown beats | 2.2 s, 2.2 s | lockdown.gd:29, 31 | |
| Rec chairs tween | 1.6 s, cubic in-out | rec_chairs.gd:52-55 | on `lockdown_done` |
| Coat-peg drift bump | `+0.35` when `lockdown_done` | coat_pegs.gd:52-53 | |
| Blackout scrim tween | 1.2 s | hud.gd:78 | UMG scrim |
| Decision ripens | `day >= 3` | decision_ledger.gd:27, 35, 43 | |
| Divert gate | `has_key("QUIET ROOM") && leland_answers.size() >= 5 && fire_tape_watched` | live_production.gd:124 | I19 |
| 1A gate | `leland_answers.size() >= 5 && seance_wear <= 70.0 && !is_dead("LELAND")` | hud.gd:460 | |
| Asset ids | `VERSE`, `CART`, `SCRIPT`, `CARD` | spectro_dock.gd:29; world_builder.gd:1024-1053 | 4 of 4 |
| Decision strings | `AUTHENTICATE`, `DESTROY`, `PERFORM` | decision_ledger.gd:5 | anything else = PERFORM in `hud._on_finale` |
| Premiere log | `user://premiere_log.txt` | live_production.gd:412 | → unified log (§8.4) |
| Liveness log | `user://liveness_log.txt` | liveness_check.gd:6 | → unified log (§8.4) |

---

## 0 · THE SEAM — who calls whom, in order

```
bed_prop.gd:19-22   decision != "" && lockdown_done  →  toast "PLACES. The premiere begins."  →  GameState.start_finale()
game_state.gd:420-421   start_finale()  →  finale_started.emit(decision)
hud.gd:30, 381-392      _on_finale(decision): lock player, show retake panel, match decision
                          "DESTROY"      → _end_burn()      → mark_ending("THE BURN")
                          "AUTHENTICATE" → _end_producer()  → mark_ending("THE NEW PRODUCER", lie=true)
                          _ (PERFORM)    → _end_perform()   → LiveProduction.run() → outcome string
live_production.gd:45   run(): all_cast_dead() → _one_woman() → "one_woman"
                          else the cue script (§4) → "signoff_4c" | "dead_air" | "caught" | "line"
hud.gd:441-477          outcome → _end_4c | _end_zero | _end_dead_air | (caught: return, no ending)
                          | the line → 1A or 1B
game_state.gd:424-432   mark_ending(name, lie): premiere_live=false, finale_done=true, ending_reached=name,
                          ending_marked.emit(name), Achievements.on_ending(name), lie_pending |= lie, save_log()
world_builder.gd:1238   ending_marked → tower beacon off iff "THE COMPLETED SIGN-OFF"
achievements.gd:53-56   on_ending → A27 if clean, then ENDING_MAP[name]
hud.gd:347-358          _roll_credits(label): the ledger read aloud, then credits.tscn
```

The soak's FAIL bot enters at the same seam, pre-seeded (`soak_runner.gd:20-27`):
`day=3, current_tape=3, assets=[VERSE,CART,SCRIPT,CARD], decision="PERFORM",
lockdown_done=true, is_night=true`, then `start_finale()`. Note it does NOT
emit `night_changed` (the non-fail bots do, line 30) — the premiere's own
`run()` emits it (§4.1).

`objective_text()` (game_state.gd:690-693) reads this seam back: `finale_done`
→ `"ENDING REACHED: %s · thank you for watching · NEW GAME threads a fresh
reel"`; else `decision != ""` → `"ENTRY STANDS: %s · sleep to begin the
premiere"`. `bed_prop.gd:16-18` refuses sleep after `finale_done` with `"The
show is over here. NEW GAME threads a fresh reel."`.

---

## 1 · LOCKDOWN (`scripts/lockdown.gd`) — Tape 4's turn

Canon: `docs/canon/restoration-game-master.md` T4.10 (line 234-235): "Every
monitor in the compound cuts to the same channel on the same frame. [SCARE
9.] Doors seal on schedule, not in anger. In the rec room the armchairs stand
in rows now, facing forward..." Invariant I18 (invariant-suite line 28):
"Lockdown is permanent. LAW: sealed doors, synced monitors, rowed chairs
survive reload... STATUS: ENFORCED (state re-applied on ready)." QA-26,
probe P11 (playtest-protocol line 47).

### 1.1 Wiring (`world_builder.gd:141-144`)
`Lockdown.new()` with `rigs = _rigs` (every `MonitorRig`, creation order) and
`exterior_doors = _ext_doors`. `_ext_doors` = every `CompoundDoor` whose
pair has `ENTRY` on either side (`world_builder.gd:258-259`). The row count
comes from `Data/Doors.csv` (0.5): the doors touching ENTRY. OPEN (O3): the
Godot list is built by name match at stamp time; the UE greybox stamp should
tag the same doors so the actor can find them without a hard-coded list.

### 1.2 Trigger and sequence
| Step | Effect | Line |
|---|---|---|
| `_ready` | if `lockdown_done` already: `_apply(true)` and arm `_fired` (the reload path, I18) | 12-15 |
| `_process` | once: `assets.size() >= 4 && is_night` → `_fire()` | 18-24 |
| `_fire` 1 | toast `"Every monitor in the compound cuts to the same channel, on the same frame."` | 27 |
| 2 | `_apply(false)` (sync + seal, below) | 28 |
| 3 | wait 2.2 s; toast `"Doors seal on schedule, not in anger."` | 29-30 |
| 4 | wait 2.2 s; toast `"MERLE · 'Fifty years, and we have a premiere. Lock-in's just till broadcast, dear.'"` | 31-32 |
| 5 | `lockdown_done = true; save_log()` — the flag is set AFTER the beats (a quit mid-sequence replays it) | 33-34 |

`_apply(silent)`: if any rigs, `tex = rigs[0].get_feed_texture()` and every
rig `sync_to(tex)` (`monitor_rig.gd:71-83`); every exterior door
`locked_reason = "SEALED FOR BROADCAST · lock-in's just till air"` (QA-26's
string). `silent` is accepted and ignored (line 44-45) — no behaviour differs.
Note the trigger does not gate on `day` — four assets at ANY night fires it;
the assets themselves are Tape 2–4 gated by the world.

### 1.3 Who reads `lockdown_done` (saved key 29, PORT-NOTES-STATE §1)
| Reader | Effect | Line |
|---|---|---|
| `bed_prop.gd` | with `decision != ""` the bed starts the finale instead of sleeping | 19-22 |
| `rec_chairs.gd` | chairs snap to `ROWS` on `_ready` if set; else tween 1.6 s once, toast `"Behind you, without a sound worth naming, the armchairs stand in rows now. Facing forward."` | 38-56 |
| `coat_pegs.gd` | drift `+0.35` (clamped 0..1) | 52-53 |
| `merle.gd` | `_where()` → CHAIR at night OR after lockdown (she stops going to the kettle) | 22-23 |
| `achievements.gd` | A20 SEALED FOR BROADCAST (poll, 1 s) | 76 |
| `soak_runner.gd` | fail bot pre-sets it | 25 |

---

## 2 · THE CASCADE (`scripts/cascade.gd` + the panel's cascade branch)

Canon: lighting bible (`docs/canon/restoration-lighting-bible.md` line 8):
"CASCADE: authored two-stage darkness with real circuit GEOGRAPHY (C's zone
dies, then B's; restoring in order relights in order; the panel's labels are
the map)." Room bible line 19: PATCH BAY "Keynotes: THE PANEL (cascade)";
line 14: TRANSMITTER HALL "V2 ends here at circuit F". Spike 6 brief
(`docs/production/restoration-spike-briefs.md` line 42-47): "script the Night
4 cascade (trip, darkness spread, restoration order), assert liveness (some
route is always lit or lightable)." Invariant I04 (line 8), I07 (line 13),
QA-10, A15 ORDER MATTERS.

### 2.1 Wiring (`world_builder.gd:133-139, 1136-1148`)
`Cascade.new()` with `rigs = _rigs`; `console` is the one `PatchbayConsole`
(`world_builder.gd:673-697`, at `(-5.5, 0.55, -31.8)`), assigned by
`_wire_cascade_console` or `_late_wire` whichever runs second. The same
console is handed to `LivenessCheck`. In UE: one director actor holding a
pointer to the panel actor; the order-of-creation dance goes away.

### 2.2 Trigger (`cascade.gd:12-17`)
Every frame, once: NOT `_fired`, NOT `cascade_done`, NOT `premiere_live`,
and `is_night && day >= 4` → `_run()`. `premiere_live` is the guard that
keeps a Day 5 premiere night from tripping a cascade that never ran (the
FAIL bot seeds `day=3`, so it never sees one). There is no minimum
time-into-night; it fires the frame night begins on Day 4+.

### 2.3 Sequence (`cascade.gd:20-40`)
| Step | Effect | Line |
|---|---|---|
| 1 | `cascade_active = true` (live, unsaved; PORT-NOTES-STATE §2) | 21 |
| 2 | `set_blackout(0.55)`; kill `rigs[2..3]` | 22-23 |
| 3 | toast `"PANEL EVENT · circuit C lets go. The stage end of the building drops dark."` | 24 |
| 4 | wait 4.0 s; toast `"The dark spreads room to room, patient, like it is reading the labels."` | 25-26 |
| 5 | wait 16.0 s; if `cascade_done` became true meanwhile (a load), return | 27-29 |
| 6 | `set_blackout(0.75)`; kill `rigs[4..5]`; toast `"Circuit B follows. The dark is administrative now. The panel is in the patch bay."` | 30-32 |
| 7 | `console.cascade_stage = 1`; spin until the console reports `cascade_stage == 0` | 33-36 |
| 8 | `cascade_active = false; cascade_done = true; save_log()` | 37-39 |
| 9 | toast `"The panel holds. Circuit F never so much as flickered. It cannot be de-energized. You have read that somewhere."` | 40 |

`_kill_range(a, b)` kills `rigs[i]` for `i in [a, min(b, size))` only if not
already killed (`set_killed(true)`, `monitor_rig.gd:89`). Kills are NOT
undone by the restore — re-patching a killed feed is the panel's ordinary
`_any_killed` branch (§2.4), one feed at a time, `control_rig` only. OPEN
(O4): rigs 2–5 that the cascade kills stay `killed` after restoration
unless the ordinary `MonitorRig` kill/re-patch loop (C8's domain) revives
them; the code never revives them here. Port as-is.

### 2.4 The panel during the cascade (`patchbay_console.gd:16-60, 82-94`)
| `cascade_stage` | Prompt | On `interact` | Line |
|---|---|---|---|
| 1 | `"PANEL · RESTORE CIRCUIT B (E) · order matters"` | (V2 offer, below) then `cascade_stage = 2; set_blackout(0.55)`; toast `"CIRCUIT B RESTORED · half the dark stands down. B before C, the way the panel is labeled."` | 21, 40-56 |
| 2 | `"PANEL · RESTORE CIRCUIT C (E)"` | `cascade_stage = 0; set_blackout(0.0)`; toast `"CIRCUIT C RESTORED · the building remembers its own light."` | 23, 57-60 |
| 0 | ordinary prompts (`_any_killed` re-patch / re-route) | ordinary two-circuit budget | 24-27, 62-70 |

Order is enforced by construction: stage 1 can only become 2, 2 only 0.
There is no wrong-order branch to port — "order matters" is the prompt, and
the only order the panel accepts.

**The V2 offer** (stage 1 only, once per console instance; `_vess_offered`
is NOT saved): if `vess_insight && !vess_credited && !is_dead("VESS")`, set
capture status `"E · restore circuit B yourself · Q · GET VESS, he knows the
order"` and wait: `interact` (E) → fall through to restore B yourself;
`improvise` (Q) → `_v2_taken()`: four toasts 2.8 / 2.8 / 3.2 s apart
(`"You call down the dark corridor. He comes because someone finally asked."`
· `"'B before C,' he says, 'obviously,' and both circuits close under his
hands in eleven seconds."` · `"Then he keeps walking. Past B. Past C. To
circuit F, the one with the marshal's tie, bare-handed, to prove the
theory."` · `"The transmitter that could not be de-energized includes him
now. His outline refreshes at sixty fields a second."`), with
`cascade_stage = 0; set_blackout(0.0)` after the second toast, caption
`[MAINS HUM, SHAPED LIKE A STANDING PERSON]`, and
`mark_casualty("VESS", "V2 · THE UNCREDITED FIX", "interlaced at circuit F;
nobody thanked her first")`. Canon: casualty ledger V2 (§VESS); QA-42.
Because stage goes to 0 here, the cascade's spin (§2.3 step 7) releases and
step 8 runs — V2 completes the cascade.

### 2.5 What else the cascade changes
- Window holds are WAIVED: `door.gd:29` (prompt) and `:40` (interact) both
  test `window_bound and Broadcast.on_air and not GameState.cascade_active`.
  LAW 6; I04; QA-10. This is the only waiver in the codebase; the premiere
  does NOT waive them (§4.13).
- The hunter's warn radius narrows: `rundown.gd:152-153` — applied at the
  next ON AIR flip, not instantly.
- The brain-relevant flag `bCascadeActive` already exists in
  `URestorationState` (0.8a); nothing in `Rundown.cpp` reads it yet (§10).
- A15 ORDER MATTERS unlocks on `cascade_done` (`achievements.gd:72`).

### 2.6 Reload semantics
`cascade_done` is saved (key 42). `cascade_active` is not. A save during the
cascade (there is none — `save_log()` is called only at step 8, but any
OTHER mutation saves) reloads with `cascade_done=false`, so the cascade
re-fires from step 1 on the next Day 4+ night. Step 5's `cascade_done` check
exists for the in-session case where a load lands mid-wait. Port exactly.

---

## 3 · LIVENESS CHECK (`scripts/liveness_check.gd`) — invariant I07's witness

Canon: I07 (invariant-suite line 13): "Cascade liveness. LAW: the panel is
always reachable during the cascade. TEST: cascade run with doors
deliberately closed. TELEMETRY: liveness_log OK cadence every 5s; VIOLATION
line on breach. STATUS: ENFORCED + TELEMETERED." I04 (line 8): "liveness_log
'window holds waived' lines exist only while cascade_active."

### 3.1 Behaviour (`liveness_check.gd:13-25`)
`_physics_process`: return unless `cascade_active`. Accumulate `_t`; every
5.0 s: if `console == null` or invalid → toast `"LIVENESS VIOLATION · the
panel is gone. File this."` and log `VIOLATION · console invalid`; else log
`OK · console valid · window holds waived · stage %d` with the panel's
`cascade_stage`.

### 3.2 Log format (line 34), verbatim
```
[day %d] OK · console valid · window holds waived · stage %d
[day %d] VIOLATION · console invalid
```
Appended to `user://liveness_log.txt` (open READ_WRITE, seek_end, else
WRITE). In UE: the same text appended to `Saved/decision_log.txt`
(§8.4); the Python parser selects liveness lines by the substring
`"LIVENESS"` or `"VIOLATION"` (`tools/invariant_parser.py:41`) — NOTE the
Godot OK line contains NEITHER substring, so the UE emitter MUST prefix the
line so the unified parser can find it (e.g. `LIVENESS [day 4] OK · console
valid · window holds waived · stage 1`). The Godot parser reads the whole
file, so it never needed a prefix. This is the one place the unified-log
port changes the line text; §8.4 states the rule.

### 3.3 What "reachable" means as built
The check is EXISTENCE of the console node, not path reachability. The
reachability the law describes is delivered by construction — window holds
are waived while `cascade_active` (§2.5), so no door can hold the player off
the panel — and the log line says so ("window holds waived"). I07's TEST
"with doors deliberately closed" is therefore a door-open test on the
waiver, not a navmesh query. OPEN (O5): whether UE should additionally
assert a nav path from the player to the panel every 5 s. The code does not;
port the code, and add the nav assert only as a UE-labelled extra check (the
way UE-R1 was added in 0.9d), never as I07 itself.

---

## 4 · THE PREMIERE (`scripts/live_production.gd`)

Canon: design doc §9 (`docs/canon/restoration-design-doc.md` line 209-211):
"The player runs a live broadcast as crew and talent at once: switcher
operation..., cue execution from Craik's script, and staying in frame,
because on camera is the one place nothing can touch her while she says the
ending out loud." Game master T5.3–T5.4 (lines 251-280). Walkthrough Tape 5
(lines 241-249). I03/I05/I06; QA-27, QA-28, QA-43, QA-46; casualty ledger
§THE ROWS ("each incident abandoned past guarantee takes a seated club
member on camera").

### 4.1 Entry: `run()` (lines 45-59)
1. If `all_cast_dead()` (MERLE, VESS, HARRIET, FLOOR MANAGER all in
   `casualties`, `game_state.gd:102-103`) → `return await _one_woman()` —
   the premiere is skipped entirely (ENDING 0 "intercepts at premiere entry";
   casualty ledger §AS BUILT; QA-45).
2. `premiere_live = true; is_night = true; night_changed.emit(true)`.
   `premiere_live` is live-only (PORT-NOTES-STATE §2); its readers are §4.13.
3. Player teleported to `(-15.5, 1.0, -28.5)`; `_spawn_stage()` (§4.7).
4. toast `"PLACES."`; wait 2.4; toast `"THE FLOOR MANAGER · 'In five,
   four...' The hands do the rest."`; wait 2.6.

### 4.2 The cue script, in order (lines 60-153)
Every `toast` goes through `GameState.toast` (glyph-substituted + `tr()`);
`_wait(t)` is a scene-tree timer. Text is canon (PORT-BRIEF: the code is the
intent; the game master's lines are the same words where they overlap).

| # | Beat | Effect | Line |
|---|---|---|---|
| C1 | CUE 1 · COLD OPEN | `_on_mark_press("CUE 1 · COLD OPEN · cut to camera one (1) · stand the mark · SPACE", 1)` (§4.4) | 61 |
| | | toast `"RITA · 'Welcome back to the Gladhouse, friends. It's a special night.'"` · 2.8 | 62-63 |
| | | toast `"RITA · 'It's our last night.'  CHUM, warm as ever: 'Ohhh, don't be sad!'"` · 3.0 | 64-65 |
| | | toast `"CHUM · 'Every good day ends with a goodnight. That's how you know it was good.'"` · 2.8 | 66-67 |
| | | `_pressure_on = true; _pressure()` — incidents begin (§4.5), un-awaited | 68-69 |
| C2 | CUE 2 · THE SONG | toast `"The cart deck loses power. The club is helping."`; `take = 1; restored = false; _breaker.label = "CART DECK BREAKER · restore (E)"` | 72-75 |
| | | `while not await _timed(45.0, "CUE 2 · RESTORE THE CART DECK AT THE PATCH BAY")`: `take += 1; _fail_takes += 1; restored = false`; toast `"TAKE %d · from the top of the cue."` (§4.6) | 76-80 |
| | | `_on_mark_press("CUE 2 · THE SONG · camera one (1) · back to the mark · SPACE", 1)` | 81 |
| | | toast `"EVERYONE · 'Close the door and dim the light. Fold the day away.'"` · 3.0; toast `"'Everyone we love is home. And no one has to stay.'"` · 3.0 | 82-85 |
| FB | THE FINAL BREAKER | three branches, §4.8 | 87-114 |
| FBk | THE FINAL BREAK | the divert window, §4.9 — may `return "signoff_4c" / "dead_air" / "caught"` | 116-137 |
| C3 | CUE 3 · CLOSE THE HOUSE | the little door, §4.10 | 139-150 |
| end | | `set_capture_status(""); _cleanup(); return "line"` | 151-153 |

Between C2 and the final breaker nothing awaits the mark; the game master's
CUE 3 (the Quiet Game) and CUE 4 (the goodnights) and SCARES 10–12 are prose
only (§9). The bell (LAW 5) rings in `hud._end_perform` AFTER `run()`
returns `"line"` (§6.2), i.e. after the house is closed, not at the "midpoint"
the prose names — the code is the intent.

### 4.3 The switcher (lines 36-42)
`_unhandled_input`: `cam_1` → `_pgm = 1`, `cam_2` → 2, `cam_3` → 3. `_pgm`
starts at 1 (line 22). There is no bus, no preview, no take button: the
number keys ARE program. Design doc line 288-290 ("Switcher (finale and
screenings): Face buttons and bumpers map one-to-one to the console's
physical button bank") — UE: three Enhanced Input actions; the pad mapping
is OPEN (O6, controls map line 10 lists no switcher buttons for pad).

### 4.4 The cue mark: `_on_mark_press(label, need_cam)` (lines 316-346)
Per frame while waiting:
- `near = distance(player, MARK) < 1.6`.
- capture status = `label + " · PGM CAM %d" % _pgm` + (`" · INCIDENT: " +
  _incident` if one is live) + (`" · ON MARK"` if near). The status line is
  the premiere HUD; QA-27 "cue marks require the PGM camera".
- If `near && _pgm == need_cam && respond just pressed`:
  1. If `_incident == "TALLY"` and `_tally_refusals < 2`: `_tally_refusals
     += 1`; toast `"The tally is lying. Camera one IS program. Trust the mark,
     not the light."`; keep waiting. (Refusals cap at 2 — I06.)
  2. If `_incident == "TALLY"` (third press): `_blind_calls += 1`; if
     `_blind_calls >= 3 && !is_dead("FLOOR MANAGER")` → `await _f2_unlisted()`
     (§6.4); else toast `"You call it blind. Correctly."`.
  3. If `_incident == "BOOM"` and not `_boom_held`: `_boom_held = true`;
     toast `"Hold. The boom is in frame. Winch it, or wait it out."`; keep
     waiting. (Exactly one hold — I06.)
  4. Otherwise clear status and return — the cue is taken. NOTE the TALLY
     incident does not clear on a blind call; it stays until fixed or
     auto-fixed. `_tally_refusals` and `_boom_held` reset only in
     `_resolve` (line 387-388), so a TALLY that persists across two cue marks
     costs two refusals at the first mark and none at the second (already
     spent). `_blind_calls` never resets (F2 is cumulative, QA-43 "exactly
     the third").
- If `near && _pgm != need_cam && respond`: toast `"Wrong camera is program.
  The Floor Manager's hand does not move."` (no cost).
- HOUSE and CARDS incidents do not touch the mark at all: they are fixed at
  fixtures or auto-fixed; their only cost is the rows if the surrounding
  clock expires. (They are still "live" in the status suffix.)

### 4.5 Incidents: `_pressure()` (lines 391-408) and the log
Runs as an un-awaited coroutine from cue 1 until `_pressure_on` is false
(`_cleanup`).
```
loop while _pressure_on:
    interval = max(14.0, 26.0 - 4.0 * _fail_takes)
    wait interval; if not _pressure_on: return
    if an incident is live:
        if now - _incident_started > 40.0: _resolve(_incident, "club auto-fix")
        continue                                   # no new roll while one is live
    _incident = random key of INCIDENTS            # uniform over TALLY/HOUSE/BOOM/CARDS
    _incident_started = now (Time.get_ticks_msec()/1000)
    _plog("INCIDENT %s (fail_takes %d, interval %.0f)" % [_incident, _fail_takes, interval])
    toast "THE CLUB IS HELPING · " + INCIDENTS[_incident]
    if _incident == "HOUSE": set_blackout(0.35)
```
Consequences of that shape, which the port must keep:
- The auto-fix is checked only at pressure ticks, and the loop WAITS first,
  then checks. An abandoned incident rolled at tick T is therefore examined
  at ages that are sums of consecutive intervals (each ∈ {26, 22, 18, 14}
  plus timer slop): one interval is never `> 40`; the first sum that is
  `> 40` is at least 42 (14+14+14) and typically 48–54 (26+22, 26+26,
  22+18+14). So every `club auto-fix` line the code can write carries
  `t=42.x` or more, and the parser's `> 41.0` rule (invariant_parser.gd:75;
  tools/invariant_parser.py:66) rules every one of them a SLOW FIX. Read
  literally, I06's text ("club auto-fix at or under 40s") and the code
  cannot both hold on any auto-fixed incident. The README ledger's recorded
  "fail-bot premiere I06 PASS" lines (README.md:225, 663, 684, 701, 720,
  739, 755, 776) are consistent with this only when the soak ended after
  the first `INCIDENT` (≈26 s after cue 1, itself ≈122 s in for the FAIL bot)
  and before the first auto-fix was due (≥ 42 s later): `incidents > 0`,
  `slow_fix == 0` → PASS. The guarantee itself has not been exercised by
  the machine. This is checkable on the Mac in one run: a FAIL-bot soak of
  ≥ 5 minutes on the Godot build should report `FAIL (slow fixes x1)`.
  OPEN (O7): whether UE ports the tick-gated check verbatim (and the
  parser reports FAIL on every auto-fix) or checks the 40 s age every frame
  (which makes `t` ≈ 40.0 always and satisfies both the invariant text and
  the parser), or the parser's line moves. The code is the intent, but this
  is the code disagreeing with its own parser; the Mac lane should rule
  before 0.9's I06 goes live. Recorded, not decided here.
- `_resolve(inc, how)` (lines 381-388): if HOUSE → `set_blackout(0.0)`;
  `_plog("RESOLVED %s (%s) t=%.1f" % [inc, how, now - _incident_started])`;
  toast `FIX_LINES[inc]`; clear `_incident`, `_tally_refusals = 0`,
  `_boom_held = false`.
- Fixing by hand: `fix(fid)` (lines 373-378): matched iff `_incident == fid`
  or (`fid == "TALLY_HOUSE"` and `_incident in [TALLY, HOUSE]`); unmatched
  → toast `"Nothing wrong here right now. The club appreciates the
  diligence."`; matched → `_resolve(_incident, "fixed by hand")`.

The four incidents and their fix lines (lines 8-19), verbatim:

| id | `INCIDENTS` toast (after `"THE CLUB IS HELPING · "`) | `FIX_LINES` | Fixture |
|---|---|---|---|
| TALLY | `The tally lights swap. Camera one claims it is not program.` | `TALLY BUS RESET · the lights agree with reality again.` | AUX PANEL (`TALLY_HOUSE`) or two refusals + a blind call at the mark |
| HOUSE | `Half the house lights drop. The club murmurs an apology.` | `HOUSE DIMMER RESTORED · the room comes back, embarrassed.` | AUX PANEL; scrim 0.35 while live |
| BOOM | `The boom drifts into frame. Somebody's grandson is so sorry.` | `BOOM WINCHED · the frame is clean.` | BOOM WINCH, or one hold at the mark then press again |
| CARDS | `The cue cards shuffle themselves. Vess swears he stacked them.` | `CARDS RESTACKED · in Vess's order, which was right.` | CARD STAND |

Log lines (`_plog`, lines 411-419; the I06 contract), verbatim formats:
```
INCIDENT %s (fail_takes %d, interval %.0f)
RESOLVED %s (%s) t=%.1f
```
`how` ∈ {`fixed by hand`, `club auto-fix`}. Appended to
`user://premiere_log.txt`; in UE the same lines go to the unified log with
NO prefix — the Python parser already selects them by `startswith("INCIDENT")`
/ `startswith("RESOLVED")` (`tools/invariant_parser.py:51`), so the line must
begin at column 0 with those words.

### 4.6 Timed clocks and the rows: `_timed(dur, label)` (lines 349-360)
`t = dur × (1.5 if assist_on else 1.0)`; per frame `t -= delta`, capture
status `"%s · 0:%02d" % [label, ceil(t)]`; if `restored` → clear status,
return true. On expiry: clear status, `await _row_taken()`, return false.
Callers loop until true, so the cue is re-entered forever (I06 "a cue can
always be re-entered"). Each expiry is one row casualty:

`_row_taken()` (lines 175-179): `row_casualties += 1` (saved key 49; NOT via
`save_log` here — it persists at the next save); toast
`ROW_LINES[(row_casualties − 1) % 3]`; caption `[A CHAIR, BETWEEN FRAMES]`;
wait 1.8. `ROW_LINES` (lines 168-172), verbatim:
1. `Cut away from a smile. Cut back to an empty chair.`
2. `Cut back to something half-resolved, interlaced, still trying to applaud.`
3. `A seat empties between frames. The applause continues at former strength.`

QA-46: "every timed incident that expires takes a seat, cycling its three
lines with the caption; the count persists." NOTE as built the seat is
taken when a CUE CLOCK expires (cue 2's 45 s, the blackout's 30 s), not when
an INCIDENT passes its guarantee — the incident's overrun is forgiven by the
club auto-fix (§4.5). The casualty ledger's prose ("each incident abandoned
past guarantee takes a seated club member") is therefore delivered through
the clocks, not the incidents. Code is the intent; port the clocks.

`restored` is set only by `FinaleBreaker.interact` (§4.7).

### 4.7 The stage: `_spawn_stage()` / fixtures (lines 256-313; `finale_breaker.gd`; `finale_fixture.gd`)
- Chum on his mark at `(-15.5, 0, -31.2)`: `CharacterKit.chum_mini()` + a
  billboard `Label3D` `"CHUM · ON HIS MARK"` (size 30, `(0, 1.4, 0)`, colour
  `(0.85, 0.93, 0.77)`). This is the STAGE body (pre-fire, "the stage body
  never animates", motion doctrine) — not the Rundown. In UE it is a static
  placement of the puppet at his mark for the premiere only.
- `FinaleBreaker` at `(-5.5, 0.9, -28.2)`, collision box `0.5×0.9×0.4`, mesh
  `0.45×0.85×0.35` albedo `(0.76, 0.23, 0.18)` (red — LAW/lighting "red =
  watched"; OPEN O8 whether the breaker should be red in UE, the greybox
  colour is programmer art). `get_prompt()` returns `label` (mutable:
  `"CART DECK BREAKER · restore (E)"` at cue 2, `"MAIN BUS · earn the retake
  (E)"` at the final breaker); `interact` → `live.restored = true`; toast
  `"RESTORED. The board hums agreement."`.
- Three `FinaleFixture`s (collision `0.5×0.7×0.4`, mesh `0.45×0.65×0.35`):
  `TALLY_HOUSE` `"AUX PANEL · resets (E)"` `(-5.0, 0.9, -29.4)` colour
  `(0.3, 0.34, 0.4)`; `BOOM` `"BOOM WINCH · crank (E)"` `(-13.4, 0.9, -30.4)`
  `(0.4, 0.34, 0.24)`; `CARDS` `"CARD STAND · restack (E)"` `(-16.9, 0.9,
  -27.4)` `(0.87, 0.83, 0.72)`. `interact` → `live.fix(fix_id)`.
- All spawned nodes are freed in `_cleanup()`.

Migration map line 15 says "cue marks as trigger volumes" — as built the
mark is a distance test (`< 1.6` m) polled every frame, and the fixtures are
`Interactable`s reached by the player's 2.6 m reach ray (0.8b-1). A trigger
volume of radius 1.6 m at MARK is equivalent; keep the number.

### 4.8 The final breaker (lines 87-114)
| Branch | Condition | Sequence |
|---|---|---|
| V1 credited, living | `vess_credited && !is_dead("VESS")` | toasts `"VESS, at the final breaker, not looking at you."` · 2.4 · `"VESS · 'The margin. You wrote my name. Somebody's name should be on something. Go finish it.'"` · 3.0 · `"The handle drops. The lights hold. On every monitor at once: VESS at the breaker, mid-"` · 2.6 · `"bars. The pin, fused into the enamel. The record was a call sheet all along."`; caption `[BARS, ALL MONITORS]`; `mark_casualty("VESS", "V1 · CREDITED, THEREFORE CAST", "taken at the breaker she kept; the credit was the casting")`; · 2.4. NO clock. |
| Vess already dead | `is_dead("VESS")` | toast `"The final breaker. A plastic pin, fused in the enamel, marks where a hand was."` · 2.6; `restored = false; label = "MAIN BUS · earn the retake (E)"`; `while not await _timed(30.0, "BLACKOUT · EARN THE RETAKE AT THE PATCH BAY"): _fail_takes += 1` (no toast, no reset of `restored` — the loop re-arms on the same flag) |
| Uncredited, living | else | toast `"The final breaker. VESS. The handle. The dark."` · 2.6; same 30 s loop but each expiry also toasts `"Again. The dark is patient."` and resets `restored = false` |

Canon: casualty ledger §VESS V1 ("TRIGGERS (either): commit AUTHENTICATE at
the ledger, or call her to the breaker") and §AS BUILT ("V1's second trigger
is the final breaker itself rather than a third summons (the farewell is the
call)"); QA-42. The other V1 trigger lives in `decision_ledger.gd:52-63`
(`_v1_taken`, on AUTHENTICATE while credited) with a different epitaph
(`"cut mid-sentence; the record includes one name you added"`) — both are
tabled in §6.4. `mark_casualty` is idempotent (I27), so a V1 at the ledger
makes the breaker take the dead-Vess branch.

NOTE the dead-Vess branch's loop never resets `restored`, so if the player
had pressed the breaker during the preceding toast the loop exits
immediately. Harmless; port verbatim.

### 4.9 The final break — the divert window (lines 116-137)
Canon: walkthrough Part VII ending 4 ("During Phase 3, the divert option
appears") and the addendum (line 289: "4c THE COMPLETED SIGN-OFF (via the
reading; the break ends itself)"); after-fire-chum §THE LAST CROSSING (line
31-32); I19 ("the divert gates on key plus answers plus the fire tape");
QA-28, QA-44 ("L2 ... sets the completed sign-off; the final break then
plays 4c with no divert prompt"); playtest protocol line 55 ("the divert
window only appears when earned").

1. If `signoff_completed` (set only by `seance_dock.gd:124`, the L2
   reading): toast `"The final break arrives, and the rundown simply ends."`
   · 2.6 · `"The program closes itself, correctly, using the ending it was
   given."` · 2.4; `_cleanup(); return "signoff_4c"`. No prompt, no choice.
2. Else if `has_key("QUIET ROOM") && leland_answers.size() >= 5 &&
   fire_tape_watched`: capture status `"FINAL BREAK · SPACE places for cue
   three · Q divert to the dead room"`; `pick = await _choice("respond",
   "improvise")` (first of the two actions just-pressed, line 363-370);
   clear status.
   - `"improvise"` → `await _fader_choice()` (below) → `res = await
     _last_crossing()` (§5.1): `"reached"` → `_cleanup(); return "dead_air"`;
     `"caught"` → `_cleanup(); return "caught"`; `"late"` → toast `"The
     sign-off ends three rooms away. The window is gone. Places."` and fall
     through to cue 3.
   - `"respond"` → fall through to cue 3.
3. Else: no window; cue 3.

Note: L2 CONSUMES the fire tape (`has_fire_tape = false`,
`seance_dock.gd:122`) but `fire_tape_watched` stays true and
`leland_answers` is emptied (`:123`), so a post-L2 save cannot satisfy gate
2 either — branch 1 is reached first regardless. The divert gate does not
check `has_fire_tape`; the walkthrough's "Dead Air Set" (key, frequency,
childhood script) is represented by exactly the three flags in the gate.
OPEN (O9): the "Phase 1 dead-room re-patch" the prose requires (walkthrough
line 273, game master T5.1) does not exist in code; the gate is the code's.

**`_fader_choice()`** (lines 193-212; canon: casualty ledger §FLOOR MANAGER
F1; QA-43; controls map line 6 "THE FADER at the divert is SPACE for his
hand, E held 4.6 s for hers"):
- `fader_self = false`.
- If `is_dead("FLOOR MANAGER")`: toast `"No one reaches for the master
  fader. So you do, first, before the run."`; `fader_self = true`; `await
  _hold_fader()`; return. (Self-hold is forced — QA-43.)
- Else toast `"The sign-off needs the master fader held through to black.
  He is already reaching for it."`; status `"SPACE · let him hold it · E ·
  hold it yourself first, then run late"`; wait for `respond` (toast `"His
  hand settles on the fader. The other rises: YOU'RE ON. Go."`, his hand →
  F1 is marked later, in the ending, §6.3) or `interact` (`fader_self =
  true`; `_hold_fader()`); clear status.
- `_hold_fader()` (215-219): status `"HOLD THE FADER · the transmitter argues
  through your arm"`; wait 4.6 s; toast `"Your right arm takes the argument.
  It will keep a little of it. Now run."`; clear status. As built the 4.6 s
  is a WAIT, not a held input (the controls map says "E held 4.6 s"); OPEN
  (O10) whether UE implements it as a hold-to-commit ("holds mean
  commitment", doctrine §1 Interaction law) — the code is a timer.

### 4.10 Cue 3 · close the house (lines 139-150)
`door = first node in group "little_door"` (`world_builder.gd:465`: a
`CompoundDoor` labelled `"THE LITTLE DOOR"` at `(-12.6, 0, -33.35)`, locked
with reason `"Not yet. It closes on camera, in Tape 5."`). If present:
`locked_reason = ""`; status `"CUE 3 · CLOSE THE HOUSE · the little door, by
hand"`; wait until `door.is_open()`; toast `"Now close it. On camera."`;
wait until closed; toast `"The house is closed. The studio holds its breath
on purpose."`; wait 2.6. If no little door exists, the cue is skipped
silently. The door is the same one the crossing runs to (§5.1) and the same
one L2's last frame shows closing from inside.

### 4.11 `_one_woman()` (lines 156-165)
Four toasts (2.8 / 2.6 / 2.8 / 2.6): `"The premiere begins on schedule,
because it was never waiting on anyone."` · `"The monitors put up the first
title card: HOSTED BY RITA IVORI."` · `"SONGS BY RITA IVORI. CRAFT BY RITA
IVORI. AUDIENCE: RITA IVORI."` · `"You are the only name left, and the show
has never once had a casting problem."`; `return "one_woman"`. No stage is
spawned, `premiere_live` is never set, no `night_changed`. Canon: casualty
ledger §THE FULL BOARD ("NEW ENDING 0 · A ONE-WOMAN SHOW: if all four living
cast are dead before lockdown, the premiere runs regardless"); QA-45.

### 4.12 `_cleanup()` (lines 422-430)
`_pressure_on = false`; if a HOUSE incident is live → `set_blackout(0.0)`;
`_incident = ""`; free every spawned node. `premiere_live` is NOT cleared
here — `mark_ending` clears it (§7). On the `"caught"` outcome nothing calls
`mark_ending`, so `premiere_live` stays true until the scene changes to the
title (§5.2) and a fresh boot resets it (live field).

### 4.13 What the premiere silences (the yield — I03, I05, LAW 1)
Every reader of `premiere_live` outside this file:

| Reader | Effect while `premiere_live` | Line |
|---|---|---|
| `rundown.gd` `_physics_process` | the whole hunt brain is bypassed: `visible = false` and return — unless `crossing` (§5) | 204-233 |
| `rundown.gd` `_on_noise` | ignores all noise | 130 |
| `rundown.gd` `_process` | no idle "performance" animation | 415 |
| `floor_manager.gd` | invisible (`visible = is_night && on_air && !premiere_live`) — probe P8 "absent during breaks and the premiere" | 49 |
| `glimpse.gd` | never fires | 19 |
| `night_trip.gd` | never fires, timer reset | 12 |
| `noise_tracker.gd` | no footstep noise | 10 |
| `cascade.gd` | never fires | 13 |
| `game_state.gd` | reset on new game; cleared by `mark_ending` | 748, 425 |

NOT silenced: `Broadcast` keeps flipping ON AIR / BREAK (C8's domain; nothing
in this file reads it), and `door.gd` window holds still bind during the
premiere (only `cascade_active` waives them). Harriet still freezes on
breaks. `NightTrip`/`Glimpse` gates matter only if the premiere is entered
before they fired. OPEN (O11): the prose says the club "blocks corridors"
(design doc §9); the only corridor pressure in code is the ordinary window
hold and the incidents. Port the code.

---

## 5 · THE LAST CROSSING (`live_production.gd:222-247` + `rundown.gd:204-231`)

Canon: after-fire-chum §THE LAST CROSSING (line 32): "master control to the
little door, seventy-five seconds, him behind her at double approach speed,
folds still costing him 2.2 apiece, his tally eye DARK the whole way...
Reach the door and DEAD AIR proceeds as written. Caught, and the run ends
the old way... Too slow, and the window closes without her: the show
continues to Cue 3 and the committed line." Walkthrough addendum line 289:
"75 s base, 62 without Vess, minus 13 self-held; two folds on the honest
route." Lighting bible line 8: "THE CROSSING: his eye dark (the one time red
abandons the player, stated in text)". Gap audit ruling 1: "the crossing is
the one run and it is scripted." Probe P23.

### 5.1 The director's side (`_last_crossing`, lines 222-247)
1. `crossing = true; crossing_caught = false` (both live, brain-relevant;
   present in `URestorationState`).
2. Rundown teleported to `(5.5, 0.0, -29.5)`.
3. Status `"THE LAST CROSSING · reach the little door · you are not in this
   broadcast; nothing on the log protects you"` (the "stated in text").
4. `goal = little door position` (else `(-15.5, 0, -31.2)`).
5. `t = 62.0 if is_dead("VESS") else 75.0; if fader_self: t -= 13.0`.
6. Per frame: `t -= delta`; `crossing_caught` → `"caught"`; `distance(player,
   goal) < 2.0` → `"reached"`; `t <= 0` → `"late"`.
7. `crossing = false`; clear status; return.

Note the player is NOT teleported to master control; she runs from wherever
the fader choice left her (the mark, ≈5 m from the door) while he starts 21
m away at 1.6 m/s with folds. The "two folds on the honest route" is the
door count between `(5.5, -29.5)` and the little door in `Data/Doors.csv`
— OPEN (O12) to confirm on the stamped greybox, since the Godot doors list
`rundown.doors` is the same CSV.

### 5.2 The hunter's side (`rundown.gd:204-231`, inside `if premiere_live:`)
```
if crossing:
    visible = true; eye light_energy = 0.0          # the dark eye
    resolve player; if none return
    if _fold_t > 0: _fold_t -= delta; return          # mid-fold
    if _door_fold_check(): return                     # LAW 11: 2.2 s at < 1.0 m of any door, 6 s per-door cool,
                                                      #   thunk + caption "[IT FOLDS THROUGH THE DOORWAY]" (+ toast if < 12 m)
    cd = distance(self, player)
    if cd < _strike_r:
        if not crossing_caught:
            crossing_caught = true; _strike_pose_t = 0.9
            toast "A hand the size of a door closes the distance. NEXT WEEK'S EPISODE."
            run_ended.emit(dailies.size())             # NOT GameState.strike(): no sheet line, no item, no daily
        return
    move_toward(player, AF_CROSSING_SPEED * delta); footfall thunk every 0.7 s
    return
visible = false; return                               # the yield, every other premiere frame
```
The catch emits `run_ended(take = dailies.size())` directly. It does not
call `strike()`, so no casting line, no item, no daily is minted; the take
number shown is the daily count. `hud._on_run_ended` (`hud.gd:309-328`)
plays the rewind-that-does-not-stop card and changes scene to the title. No
`mark_ending`, so `finale_done` stays false and `objective_text` still reads
`"ENTRY STANDS: PERFORM · sleep to begin the premiere"`: the player CONTINUEs
from the last log and the bed offers the premiere again. This is the
"dying inside your own ending" the canon describes; there is no save
scrub. The retake card itself is C9's (`ue/PORT-NOTES-RETAKE.md`).

No WARN precedes this strike and no `STRIKE` telemetry line is written
(`rundown.gd:222-224` logs nothing), so I01 is not implicated. OPEN (O13):
the UE port should log a line for the crossing catch so the harness can see
it; the format is not canon (no Godot line exists). Suggest
`STRIKE crossing caught t=<remaining>` ONLY if the parser's I01 rule is
taught to ignore it — otherwise it would count as a strike without a warn.
Do not emit `STRIKE ` for it until 0.9's parser gains the rule.

---

## 6 · THE ENDINGS (`scripts/hud.gd:381-516`, `credits.gd`, `title.gd`)

Canon: walkthrough Part VII (lines 265-277) and its addendum (line 289);
game master §THE ENDINGS, SCRIPTED (lines 282-320); casualty ledger §THE
FULL BOARD; achievements design lines 31-35, 45; QA-28, QA-44, QA-45, QA-47;
I13, I28, I29, I30.

### 6.1 Routing table
Entered from `hud._on_finale(decision)` (§0). `_say(a, b, t)` puts `a`/`b`
through `glyphs(tr())` onto the retake panel's two lines and waits `t`.

| Route | Condition | Function | `mark_ending(name, lie)` | Credits label | Achievement (`ENDING_MAP`, achievements.gd:27-33) |
|---|---|---|---|---|---|
| 3 | `decision == "DESTROY"` | `_end_burn` (395-408) | `"THE BURN"` | `3 · THE BURN` | A21 THERE'S COBBLER |
| 2 | `decision == "AUTHENTICATE"` | `_end_producer` (411-425) | `"THE NEW PRODUCER"`, **lie=true** | `2 · THE NEW PRODUCER` | A22 WELCOME HOME |
| 0 | PERFORM route, `all_cast_dead()` | `_end_zero` (489-494) | `"A ONE-WOMAN SHOW"` | `0 · A ONE-WOMAN SHOW` | A28 |
| 4c | PERFORM, `signoff_completed` | `_end_4c` (480-486) | `"THE COMPLETED SIGN-OFF"` | `4c · THE COMPLETED SIGN-OFF` | none, by ruling (achievements design line 45) |
| 4b | PERFORM, divert reached, `fader_self` | `_end_dead_air` (497-507) | `"DEAD AIR"` | `4b · DEAD AIR · HER HAND` | A25 SIGNED OFF |
| 4a | PERFORM, divert reached, not `fader_self` | `_end_dead_air` (508-515) | `"DEAD AIR"` | `4a · DEAD AIR · HIS HAND` | A25 SIGNED OFF |
| — | PERFORM, crossing caught | return with no ending (§5.2) | — | — | A18 via `run_ended` |
| 1A | PERFORM, the line, `leland_answers.size() >= 5 && seance_wear <= 70.0 && !is_dead("LELAND")` | `_end_perform` (460-467) | `"SIGN-OFF · LELAND CLOSES"` | `1A · SIGN-OFF` | A24 |
| 1B | PERFORM, the line, otherwise | `_end_perform` (468-477) | `"SIGN-OFF · RITA CLOSES"` | `1B · SIGN-OFF` | A23 FILE UNDER: SAINTS |

Any `decision` other than the two named strings takes the PERFORM branch
(`match ... _:`), including `""` — the bed never starts the finale with an
empty decision (`bed_prop.gd:19`), but the soak can.

Things the prose lists that the code does NOT gate on (code is the intent):
- Ending 2's "PERFORM with under four assets while PT is 70+" audition
  clause (walkthrough line 269): not built; PERFORM always plays the
  premiere. `pt` is saved (key 12) and unread here.
- 1A's "Leland Integrity 60+": built as `seance_wear <= 70.0` (the wear
  economy inverted), plus the L1 death gate.
- Assets: nothing in the finale checks `assets.size()`; four assets gate
  LOCKDOWN (§1.2), and lockdown gates the bed's finale. So "4/4" is
  transitively required for every ending except via the soak seed.

### 6.2 The line (1A/1B, `_end_perform`, lines 428-477)
After `run()` returns `"line"`: `Sfx.bell()` — captions `[THE BELL RINGS ·
once]` (`sfx.gd:17`) and plays `_bell` at −6 dB — then `_say("Fifty years
silent.", "The bell rings once, three feet behind camera position.", 2.8)`.
This is LAW 5's one ring, its caption included. Then `r1 = "CAMERA ONE"`,
`r2 = "SPACE · deliver the line"`, wait for `respond`; then the three
`_say`s of the line (`"'That's our show. That was always our show.'"` ·
`"'There's no one at home anymore. The lights are off.'"` / `"'The children
grew up. You can stop looking for them.'"` · `"'Say goodnight, Chum.'"`),
then the 1A / 1B fork with the texts at lines 461-477 (1B adds `"FILE UNDER:
STAFF."` if VESS is dead and `"AND THE READER, UNFILED."` if LELAND is dead —
casualty ledger §VESS ENDINGS, §LELAND ENDINGS).

### 6.3 Variant lines by casualty (verbatim in `hud.gd`)
| Ending | Condition | Line(s) |
|---|---|---|
| THE BURN | `is_dead("MERLE")` | 399-401 (`"No one comes to the doorway."` … `"THE KITCHEN LIGHT WAS ON. NOBODY HAD EATEN."`) else 403-406 |
| NEW PRODUCER | `is_dead("VESS")` | 414 (the warm chair) |
| NEW PRODUCER | `is_dead("FLOOR MANAGER")` | 416 (the open headset) |
| NEW PRODUCER | `is_dead("MERLE")` | 421 (`"administered by the room itself"`) else 423 |
| 1B | `is_dead("VESS")` / `is_dead("LELAND")` | 473 / 475 |
| DEAD AIR 4a | `!is_dead("FLOOR MANAGER")` | 510-511: the F1 line, then `mark_casualty("FLOOR MANAGER", "F1 · THE FADER", "held it through sign-off; finished the way a gesture is finished")` — a death marked INSIDE the epilogue, before `mark_ending` (QA-43 "with the casualty marked inside the epilogue"). It therefore appears in the same credits' ledger read. |
| DEAD AIR 4b | `fader_self` | 504-507 (the arm) |

`_end_producer` is the only `lie=true` (line 424). `mark_ending` sets
`lie_pending` (saved key 32, NOT reset by new game — PORT-NOTES-STATE §2),
and `title.gd:12-15` spends it: `new_btn.text = "NEW EPISODE"`, then
`lie_pending = false; save_log()`. LAW 8; I13; the design doc's
"CONTINUE?" half of the lie (game master line 303) is not built — the code
lies once, with one button. OPEN (O14): whether UE adds the CONTINUE? face;
canon says the lie is spent "where the design doc says it does", the code
says the NEW button. Port the code; do not add a second lie.

### 6.4 Every `mark_casualty` reachable from this file's systems (LAW 7)
| Who | Cause tag | Epitaph | Where |
|---|---|---|---|
| VESS | `V1 · CREDITED, THEREFORE CAST` | `taken at the breaker she kept; the credit was the casting` | live_production.gd:97 |
| VESS | `V1 · CREDITED, THEREFORE CAST` | `cut mid-sentence; the record includes one name you added` | decision_ledger.gd:63 |
| VESS | `V2 · THE UNCREDITED FIX` | `interlaced at circuit F; nobody thanked her first` | patchbay_console.gd:93 |
| FLOOR MANAGER | `F2 · THE UNLISTED CAMERA` | `cued a camera the run sheet never carried` | live_production.gd:189 |
| FLOOR MANAGER | `F1 · THE FADER` | `held it through sign-off; finished the way a gesture is finished` | hud.gd:511 |
| LELAND | `L2 · THE READING` | `finished it; the door closed from the inside` | seance_dock.gd:125 (sets `signoff_completed`, the 4c key) |
| (rows) | `row_casualties += 1` | `[A CHAIR, BETWEEN FRAMES]` | live_production.gd:176 |

`mark_casualty` (game_state.gd:113-118): no-op if already dead (I27);
appends `{who, cause, line, day}`; `save_log()`; toast `"THE LEDGER TAKES IT
DOWN."`. Every one of the above is preceded by a `show_caption` line
(`[BARS, ALL MONITORS]`, `[MAINS HUM, SHAPED LIKE A STANDING PERSON]`,
`[YOU'RE ON · TO NOTHING LISTED]`, `[THE SIGN-OFF, WHOLE]`, `[A CHAIR,
BETWEEN FRAMES]`) except F1, which is narrated by `_say`. M1/M2/H1/H2 are
outside this file (H2's `h2_pending` is set by `rejected_edit.gd:40` and
resolved by `harriet.gd:100-107`; M2 is not built, §9).

`_f2_unlisted()` (lines 182-190): toasts `"Coverage must come from
somewhere. THE FLOOR MANAGER steps into frame"` · 2.6 · `"and gives YOU'RE
ON to a camera that is not on the run sheet."` · 2.8 · `"The unlisted camera
accepts him. The frame he entered never cuts away, because nothing is
switched to it."`; caption; `mark_casualty(... F2 ...)`; · 2.0. The cue then
proceeds (QA-43 "cue flow continues after"). The post-F2 monitor haunt and
freeze-check inversion are "canon-only remainders" (casualty ledger §AS
BUILT) — not built, do not port.

### 6.5 Credits (`_roll_credits`, hud.gd:347-358; `credits.gd:21-36`)
`_say("ENDING · " + label, "RESTORATION", 2.6)`; if any casualties or rows:
`_say("THE LEDGER, READ ALOUD, because that is what ledgers are for:", "",
2.4)`, then per casualty `_say("%s · %s" % [who, cause], line, 2.6)` (+ for
HARRIET: `"HER CARD, HER OWN STAMP REGISTER:" / "TRANSITION UNRESOLVED."`),
then if rows `"THE 58 CLUB:" / "fifty-eight, minus %d."`. A clean run reads
NOTHING (I29, QA-47). Mouse shown; scene → `credits.tscn`. The reading is
the binder's array verbatim (I28).

`credits.tscn` cards: nine base cards; for `ending_reached == "A ONE-WOMAN
SHOW"` cards 4 and 5 become the four roles `······ RITA IVORI` and `"and
CHUM\nas RITA IVORI"` (QA-45 "nine cards, one name"); any non-empty
`ending_reached` inserts `"ENDING REACHED\n<name>"` at index 6. Speed 42
(Timings.csv row 6). Note the ONE-WOMAN card names CHUM as a role played by
Rita — the credits are the only place CHUM's name appears in this file's
systems, and it is a credit line, not an achievement or presence string
(LAW 5 second sentence; C14 audits this).

### 6.6 World reactions to `ending_marked`
`world_builder.gd:1238-1243`: iff `"THE COMPLETED SIGN-OFF"`, the yard
tower's beacon material has `emission_enabled = false` and albedo
`(0.25, 0.1, 0.08)` — "the tower light goes out as rest" (4c; lighting bible
line 8). The reverse-tour blackout the prose describes (Day 1 order, entry
last) is `_say` text only (hud.gd:481); OPEN (O15) as a UE lighting
sequence — canon gives the ORDER (entry last) but no timing.
`Achievements.on_ending` (achievements.gd:53-56): A27 if `casualties` empty
AND `row_casualties == 0`; then the ending's card. Unlocks queue and flush
only at morning / title (deferral rule, achievements design line 5) — the
credits never toast (I30).

---

## 7 · THE `game_state.gd` SEAM (fields and functions this unit owns)

| Member | Kind | Written here by | Read here by | Save |
|---|---|---|---|---|
| `start_finale()` | fn (420-421) | bed_prop, soak_runner | — | emits `finale_started(decision)` |
| `mark_ending(name, lie=false)` | fn (424-432) | hud `_end_*` (7 calls) | — | `premiere_live=false; finale_done=true; ending_reached=name; ending_marked.emit; Achievements.on_ending; lie_pending|=lie; save_log()` |
| `finale_started` | signal | `start_finale` | hud:30 | — |
| `ending_marked` | signal | `mark_ending` | world_builder:1238 | — |
| `decision` | String | decision_ledger:47 (+ `save_log`), soak | bed_prop, hud, merle:53-57, achievements A17, objective_text | key 28 |
| `lockdown_done` | bool | lockdown:33 (+ save), soak | §1.3 | key 29 |
| `finale_done` | bool | `mark_ending` | bed_prop:16, objective_text:690, reset_new_game relic rule | key 30 |
| `ending_reached` | String | `mark_ending` | credits:32-36, objective_text | key 31 |
| `lie_pending` | bool | `mark_ending(lie)`; cleared title:14 | title:12 | key 32, survives new game |
| `cascade_done` | bool | cascade:38 (+ save) | cascade:13, 28; achievements A15 | key 42 |
| `cascade_active` | bool | cascade:21, 37 | door:29,40; rundown:152; liveness:14 | live |
| `premiere_live` | bool | live_production:48; `mark_ending` | §4.13 | live |
| `crossing`, `crossing_caught` | bool | live_production:223-224, 245; rundown:221 | rundown:205, 220; live_production:239 | live |
| `fader_self` | bool | live_production:194, 197, 208 | live_production:233; hud:503 | live |
| `signoff_completed` | bool | seance_dock:124 | live_production:117 | key 48, survives new game |
| `row_casualties` | int | live_production:176 | hud:349-356; achievements:54 | key 49 |
| `assets` | Array | `gain_asset` | lockdown:21; soak seed | key 27 |
| `set_blackout(a)` | fn (405-406) | cascade, patchbay_console, live_production | hud:65-78 (scrim tween 1.2 s) | emits `blackout_changed` |

Save points inside these systems: `lockdown._fire` end, `cascade._run` end,
`decision_ledger` commit, `mark_ending`, every `mark_casualty`, `title` lie
spend. `row_casualties` and `fader_self` have none of their own.

---

## 8 · TELEMETRY AND THE HARNESS — what makes I06 / I07 implementable

### 8.1 The Godot parser, verbatim rules (`invariant_parser.gd:49-78`)
```
I07 (liveness_log):  no lines → "N/A (cascade did not run)"
                     any line containing "VIOLATION" → "FAIL (violation logged)"
                     else → "PASS (%d checks)" % line count
I06 (premiere_log):  no lines → bot=="fail" ? "FAIL (fail bot produced no premiere log)" : "N/A"
                     per line: begins_with("INCIDENT") → incidents += 1
                               begins_with("RESOLVED") → "club auto-fix" in line → auto += 1;
                                                         t = float(after "t="); t > 41.0 → slow_fix += 1
                     verdict: slow_fix == 0 && incidents > 0 → PASS
                              slow_fix > 0 → "FAIL (slow fixes x%d)"
                              else → "WEAK (no incidents rolled)"
                     output: "I06 fail-forward-finale: %s (%d incidents, %d auto-fixed)"
```
`tools/invariant_parser.py:40-76` implements the same rules on the unified
log, with two deltas already noted in its docstring: liveness lines are
selected by substring `LIVENESS` / `VIOLATION` (§3.2), and I06's empty case
reads `"N/A (premiere not yet ported)"`. Both parsers already agree on the
verdict logic; nothing in the parser needs to change for this unit.

### 8.2 What the UE director must emit
| Event | Line (column 0) | Source of truth |
|---|---|---|
| incident rolled | `INCIDENT <TALLY\|HOUSE\|BOOM\|CARDS> (fail_takes <n>, interval <int>)` | live_production.gd:405 |
| incident resolved | `RESOLVED <id> (fixed by hand\|club auto-fix) t=<%.1f>` | live_production.gd:384 |
| liveness OK | `LIVENESS [day <d>] OK · console valid · window holds waived · stage <s>` | liveness_check.gd:24, 34 + §3.2 prefix |
| liveness breach | `LIVENESS [day <d>] VIOLATION · console invalid` | liveness_check.gd:22, 34 + prefix |

`t` is seconds since `_incident_started`, ONE decimal. `interval` is `%.0f`.
The parser tolerates trailing text after `t=<float>` (it splits on
whitespace) but NOT a missing space before `t=`.

### 8.3 The FAIL bot, so the fixture can be rebuilt (`bot_driver.gd:84-105`; `soak_runner.gd:20-27`)
Seed per §0. Phase 0: stand still for 120 s (every incident that rolls is
abandoned — the auto-fix must carry them). Then press `cam_1` once, walk to
`MARK` at 3.0 m/s, and toggle `respond` every 0.5 s forever (spamming the
cue through, burning tally refusals and boom holds, failing nothing on
purpose — the cue-2 clock is what fails, because the bot never touches the
breaker). Invariant suite line 37: "FAIL-BOT (premiere: ignores every
incident, fails every cue thrice)". The bot as built fails cue 2 until the
premiere is abandoned by the soak timer; "thrice" is not enforced. The
`tools/test_failbot.py` precedent (0.9d) is the UE shape: pin a target,
simulate N seconds, run the parser. For I06 the UE fixture needs: the
director actor with `bTestForceFinale` (seed §0), a scripted pawn that never
interacts, ≥ 120 s, then `tools/invariant_parser.py <log> --bot fail`.
Expected on the code as-is: see O7 — PASS only if the run ends before the
first auto-fix; FAIL (slow fixes) on any run long enough to contain one.

### 8.4 The unified-log rule
Every Godot `user://*_log.txt` write becomes an append to
`Saved/decision_log.txt` (`URestorationState::LogLine`, the format the
parser reads — 0.7 ledger; `tools/invariant_parser.py` docstring lines
5-7). Premiere lines keep their exact text (the parser anchors on
`startswith`). Liveness lines gain the `LIVENESS ` prefix (the parser anchors
on substring; the Godot text has none). Coverage lines are C8's. Nothing
else changes; the Godot parser's per-file semantics are reproduced by the
prefixes.

### 8.5 The other invariants these systems carry
| Inv | Holds by | Where |
|---|---|---|
| I03 premiere yields the floor | `rundown.gd:204-233` early return | §4.13 |
| I04 holds yield only to the cascade | `door.gd:29,40` | §2.5 |
| I05 on camera is safe (premiere) | same as I03 at prototype grain (suite line 9: "re-verify when hunting and premiere ever coexist") | — |
| I13 the lie spent once | `title.gd:12-15` | §6.3 |
| I18 lockdown permanent | `lockdown.gd:12-15`, `rec_chairs.gd:38-42`, doors' `locked_reason` re-applied | §1 |
| I19 divert gates | `live_production.gd:124` | §4.9 |
| I27 deaths idempotent | `game_state.gd:114-115` | §6.4 |
| I28/I29 ledger read exact / silent when clean | `hud.gd:349-356` | §6.5 |
| I30 meta-silence | `Achievements.unlock` queues; flush gates only | §6.6 |

---

## 9 · CODE vs CANON — prose the code does not implement (do NOT invent it)

The code is the intent (PORT-BRIEF line 2). Listed so the UE port neither
adds nor "fixes" these without an owner ruling:

| Prose | Where | As built |
|---|---|---|
| CUE 3 the Quiet Game on camera; CUE 4 the goodnights; SCARE 11 the studio plunge; SCARE 12 the delivery (hands holding Rita off camera) | game master lines 263-268; walkthrough line 158 | none; the cue script is C1 → C2 → final breaker → final break → C3 close the house |
| "Midpoint: the bell rings once" | walkthrough line 245; game master line 261 | rings after `run()` returns `"line"`, before the line (§6.2) |
| M2 THE HOME SINGER (Merle on the call sheet) | casualty ledger §MERLE | not built; no premiere Merle branch |
| M2 ripple: "remaining incidents lose their forgiveness timers by 20 percent" | casualty ledger §MERLE RIPPLES | not built |
| "Vess is the most dangerous saboteur... hesitates at the final breaker and the hesitation is the window" | walkthrough line 245 | the credited branch has no clock at all (§4.8) |
| PT ≥ 70 audition clause into ending 2 | walkthrough line 269 | not built |
| Leland Integrity 60% | walkthrough line 267 | `seance_wear <= 70.0` + not L1 (§6.1) |
| Phase 1 dead-room re-patch as a divert precondition | walkthrough lines 243, 273; game master T5.1 | not built; gate is key + 5 answers + tape watched (§4.9) |
| DEAD AIR "playable walk back DR to TH to BEN" | game master line 316 | `_say` text only |
| 4c reverse-tour blackout as lighting | game master / casualty ledger §LELAND | `_say` text + tower beacon off (§6.6) |
| Post-F2 monitor haunt, freeze-check inversion | casualty ledger §FLOOR MANAGER | "canon-only remainders" per §AS BUILT |
| The interface lie's CONTINUE? face | game master line 303 | NEW EPISODE only (§6.3) |
| Premiere binder is live-time | gap audit ruling 3 | not in these scripts (binder port's concern) |
| Fader "E held 4.6 s" | controls map line 6 | a 4.6 s wait after one press (§4.9, O10) |
| Crossing "from master control" | after-fire-chum line 32 | from wherever the fader choice ends (§5.1) |

---

## 10 · DELTAS: the current C++ skeleton vs this transcript (the checklist)

Present in `ue/Restoration/Source/Restoration/` today (grep at 0e8166d):
`URestorationState` carries `bPremiereLive`, `bCrossing`, `bCrossingCaught`,
`bCascadeActive` (live) and `Decision`, `bLockdownDone`, `bFinaleDone`,
`EndingReached`, `bLiePending`, `bCascadeDone`, `bSignoffCompleted`,
`RowCasualties`, `Casualties`, `Assets` (saved, round-tripped in
`SaveToSlot`/`LoadFromSlot`). `ARundown` has `AfCrossingSpeed`,
`AfFoldSeconds`, `AfDoorNear`, `StrikeRadius`, `DoorFoldCheck`, and an
`OnRunEnded` binding. Nothing else below exists.

- [ ] `ARundown::Tick` does not read `bPremiereLive` / `bCrossing`: add the
      premiere yield (§4.13) ABOVE the AF layer and the night gate, and the
      crossing branch (§5.2) inside it, in `rundown.gd`'s order (lines
      204-233 come before everything else in `_physics_process`).
- [ ] `ARundown` warn narrowing under `bCascadeActive` (rundown.gd:152-153)
      — also in C8's checklist; one of the two PRs lands it.
- [ ] `ARundown` crossing catch: set `bCrossingCaught`, 0.9 s pose,
      the toast, `OnRunEnded.Broadcast(Dailies.Num())` — no `Strike()`.
- [ ] `URestorationState`: `StartFinale()` → `OnFinaleStarted(Decision)`;
      `MarkEnding(Name, bLie)` verbatim order (§7); `MarkCasualty` /
      `IsDead` / `AllCastDead` / `CauseOf` (game_state.gd:88-118); delegates
      `OnFinaleStarted`, `OnEndingMarked`, `OnBlackoutChanged`, `OnCaption`,
      `OnNotify` (the last three are HUD-wide; PORT-NOTES-STATE §3 lists all
      20).
- [ ] `bFaderSelf` (live) is missing from `URestorationState`.
- [ ] `SetBlackout(float)` → `OnBlackoutChanged`; a UMG scrim tweening 1.2 s
      (migration map line 16 recommends the scrim).
- [ ] `ALockdown` actor: §1 verbatim; needs the exterior-door list (O3) and
      the monitor-feed `sync_to` (one RT to all screen materials, map line
      8) — which needs the SceneCapture rigs from 0.6b to be persistent
      (they are ephemeral today: PROGRESS 0.6b "rig is ephemeral").
- [ ] `ACascade` actor: §2 verbatim; needs the rig list in creation order
      (kill indices 2–5) and a pointer to the panel.
- [ ] `APatchbayConsole` cascade branch (§2.4) incl. the V2 offer; the
      two-circuit budget itself is not this unit's (no PORT-NOTES box
      names it — OPEN O16, probably C17's audit or a new box).
- [ ] `ALivenessCheck` actor: §3 verbatim, `LIVENESS ` prefix on the log.
- [ ] `ALiveProduction` director (GameMode-scoped): §4 verbatim — the cue
      coroutine as a latent/state machine, `_pressure` as a second timer,
      `INCIDENT`/`RESOLVED` lines through `URestorationState::LogLine`.
- [ ] `AFinaleBreaker`, `AFinaleFixture` (`IRestorationInteractable`) with
      the prompts/positions of §4.7.
- [ ] The little door: `CompoundDoor` port with group/tag `little_door`,
      `IsOpen()`, mutable `LockedReason` (world_builder.gd:462-470).
- [ ] Three Enhanced Input actions `Cam1/2/3` (physical 1/2/3); `_pgm` on
      the director.
- [ ] Endings (§6) on the retake UMG (C9) — `_say` = two labels + wait;
      `_roll_credits` → a credits level with the card list of §6.5.
- [ ] `title`: spend `bLiePending` into the NEW button text (§6.3).
- [ ] `Achievements.on_ending` + `ENDING_MAP` (C14's audit covers the
      strings; the mechanism is achievements.gd:53-56).
- [ ] `bed_prop`: the finale branch (`bed_prop.gd:19-22`) ahead of
      `SetNight`.
- [ ] Data: add the §Constants literals to `Timings.csv` via
      `tools/extract_data.py` (O2).
- [ ] Harness: `bTestForceFinale` seed (§0) on the director + a
      no-interaction pawn; `tools/invariant_parser.py --bot fail` expects
      I06 PASS — after O7 is ruled.

When every box is ticked and the FAIL-bot fixture reports `I06
fail-forward-finale: PASS` and a Day 4 cascade fixture reports `I07
cascade-liveness: PASS (n checks)` from the unified log, 0.9d's "HONEST
SCOPE" note (I06/I07 N/A) is retired.

---

## 11 · OPEN (consolidated; none decided here)

| # | Question | Where |
|---|---|---|
| O1 | UE home for the ending sequences (retake UMG from C9?) | header |
| O2 | Add the finale literals to `Data/Timings.csv` via `extract_data.py` | constants |
| O3 | How the UE stamp tags the exterior (ENTRY-adjacent) doors for LOCKDOWN | §1.1 |
| O4 | Cascade-killed rigs 2–5 are never revived by the restore; port as-is? | §2.3 |
| O5 | Add a UE-labelled nav-path assert to the liveness check (never as I07 itself) | §3.3 |
| O6 | Gamepad mapping for `cam_1/2/3` (controls map lists none) | §4.3 |
| O7 | Auto-fix checked only at pressure ticks, so every auto-fix logs `t ≥ 42` vs the parser's 41 s line: a verbatim port FAILS I06 on any run containing an auto-fix; the ledger's PASSes predate the first auto-fix; rule before 0.9's I06 goes live | §4.5 |
| O8 | Breaker/fixture colours are greybox; real props per C6 | §4.7 |
| O9 | The prose's Phase 1 dead-room re-patch is not a divert precondition in code | §4.9 |
| O10 | Fader self-hold: 4.6 s timer (code) vs held input (controls map) | §4.9 |
| O11 | "Club blocks corridors" has no code beyond window holds + incidents | §4.13 |
| O12 | Confirm "two folds on the honest route" against the stamped door CSV | §5.1 |
| O13 | Telemetry line for the crossing catch (none in Godot; must not read as an un-warned STRIKE) | §5.2 |
| O14 | The lie's CONTINUE? face (design doc) vs NEW EPISODE only (code) | §6.3 |
| O15 | 4c reverse-tour blackout as a lighting sequence: order is canon, timing is not | §6.6 |
| O16 | Which unit ports the two-circuit patch-bay budget (not named in any CLOUD-OK box) | §10 |
