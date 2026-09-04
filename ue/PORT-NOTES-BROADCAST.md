# PORT NOTES · BROADCAST — the ON AIR / BREAK clock and the coverage director, transcribed

**Unit C8 (CLOUD-OK).** This is the implementation checklist for LAW 6 and the
thing that watches how you watch: every surface `broadcast.gd` exposes, every
reader of it, the whole of `coverage_director.gd` (counters, the four labels,
the log), and every signal each one emits or consumes. Source of truth:
`scripts/broadcast.gd` (31 lines) and `scripts/coverage_director.gd` (95
lines) at `origin/main` 0e8166d, plus the listener sites named by
`file:line` below. Where these notes and that code disagree, THE CODE IS THE
INTENT (`docs/packet/portbrief/PORT-BRIEF.md` line 2: "where prose and code
disagree, the code is the intent"); fix the notes.

UE homes per `docs/packet/portbrief/UE5-MIGRATION-MAP.md`:
- CLOCK (line 6): "broadcast.gd → a WorldSubsystem ticking ON AIR and BREAK;
  wall clocks read it; door holds bind to its delegate exactly as now." This
  already exists from unit 0.7 as `URestorationClock : UWorldSubsystem`
  (`ue/Restoration/Source/Restoration/RestorationClock.h`; PROGRESS.md 0.7).
  §6 lists what it still lacks.
- COVERAGE DIRECTOR (line 14): "coverage_director.gd → a WorldSubsystem;
  counters persist through the SaveGame; the append-only decision log is a
  plain FFileHelper append." Not yet ported in any form (no source file in
  `ue/Restoration/Source/Restoration/` mentions coverage). §6 is its
  checklist. The subsystem's class name is OPEN (O4).

The law these two serve, verbatim: "6. THE SCHEDULE IS REAL. ON AIR and BREAK
govern behavior mechanically; Harriet freezes on breaks; window holds bind
except during cascade." (`docs/packet/portbrief/THE-LAWS.md` line 7.)

Constants that are canon (never change the numbers; all are in
`ue/Restoration/Data/Timings.csv` rows 2–3 except where noted):

| Constant | Value | Source | Home |
|---|---|---|---|
| `ON_AIR_SECONDS` | 50.0 | broadcast.gd:5 | `URestorationClock::OnAirSeconds` (present) |
| `BREAK_SECONDS` | 18.0 | broadcast.gd:6 | `URestorationClock::BreakSeconds` (present) |
| Boot phase | ON AIR, timer full (`on_air = true`, `_t = 50.0`) | broadcast.gd:8,10 | `bOnAir = true`, first `ArmTimer()` at 50 (present) |
| Monitor watch radius | `< 3.5` m from `monitor_position` | coverage_director.gd:51 | not ported |
| Monitor facing dot | `> 0.6` (player forward · to-monitor) | coverage_director.gd:53 | not ported |
| Moving threshold | `velocity.length() > 0.5` m/s | coverage_director.gd:44 | not ported |
| Counter flush cadence | every 5.0 s of night physics time | coverage_director.gd:58 | not ported |
| AUDIENCE floor | `m < 2.0 && mv < 4.0 && st < 4.0` s | coverage_director.gd:66 | not ported |
| HIDER warn radius | 5.0 m (else `WARN_RADIUS` 7.0) | rundown.gd:151 | not ported (§6) |
| CHECKER kill reach | most-watched rig's `cam_position` `< 14.0` m from him | rundown.gd:157 | not ported (§6) |
| Blanket kill reach | any rig's `cam_position` `< 9.0` m from him | rundown.gd:162 | not ported (§6) |
| Cascade warn narrowing | `max(3.5, warn_r - 1.5)` | rundown.gd:152-153 | not ported (§6) |
| Heard-noise window | `now - _heard_t < 12.0` s | rundown.gd:167 | present (`Now - HeardT < 12.0f`) |
| Coverage log path | `user://coverage_log.txt` | coverage_director.gd:9 | `Saved/decision_log.txt` (unified; §3.4) |

---

## 1 · THE CLOCK (`scripts/broadcast.gd`, autoload `Broadcast`)

Autoload order (`project.godot` [autoload]): `GameState`, `Broadcast`, `Sfx`,
`Achievements`. It is a plain `Node`; nothing in it depends on GameState.

### 1.1 Surface

| Member | Kind | Value / behaviour | Line |
|---|---|---|---|
| `on_air` | `bool` var, public | `true` at boot; flips at each expiry. Read directly (never written) by 6 scripts (§2) | 8 |
| `_t` | `float` private | seconds left in the current phase; starts at `ON_AIR_SECONDS` | 10 |
| `phase_changed(now_on_air: bool)` | signal | emitted once per flip, AFTER `on_air` and `_t` are already updated | 12, 20 |
| `time_left()` | `float` | `max(_t, 0.0)` | 23-24 |
| `phase_text()` | `String` | `s = int(ceil(time_left()))`; ON AIR → `"● ON AIR · break in 0:%02d" % s`; BREAK → `"○ BREAK · window closes 0:%02d" % s` | 27-31 |

Both phase strings are in the string table already:
`ue/Restoration/Data/GameText.csv` rows 45 and 46, byte-identical (the glyphs
are U+25CF BLACK CIRCLE and U+25CB WHITE CIRCLE; the separator is U+00B7).
The format is minutes-colon-seconds with the minute hard-coded to `0`, which
is correct only because both phases are under 60 s. Keep it that way.

### 1.2 Tick, verbatim order of effects (`_process`, lines 15-20)

1. `_t -= delta` (frame delta, `_process`, NOT `_physics_process`).
2. If `_t <= 0.0`: (a) `on_air = not on_air`; (b) `_t = 50.0 if on_air else
   18.0` — the overshoot below zero is DISCARDED, every phase runs its full
   length from the flip frame; (c) `phase_changed.emit(on_air)`.

So each phase is exactly its constant measured from the frame of the flip,
and a listener that reads `Broadcast.on_air` or `time_left()` inside its
`phase_changed` handler sees the NEW phase and a full timer. The existing
`URestorationClock::Flip()` (flag, broadcast, re-arm timer at the full
constant) preserves that order and the no-carry semantics. Godot processes
autoloads before scene nodes in the same frame, so readers in `_process`
normally see the flipped state on the flip frame; that ordering is not a
contract anything depends on.

### 1.3 What the clock does NOT do (each verified by grep over `scripts/`)

- **Never gated.** It runs by day, by night, in DEMO, during the premiere and
  the cascade. Every gate is on the listener side (§2). No script writes
  `on_air` or `_t`, none emits `phase_changed` from outside, no bench/soak
  script forces a phase. (The UE harness's `AHarriet::bTestForceBreak` is a
  local test override that bypasses the clock; keep it out of the production
  read path — `Harriet.cpp` 19-23 already does.)
- **Never saved.** Neither `on_air` nor `_t` is a v16 key
  (`ue/PORT-NOTES-STATE.md` §1 lists all 55). Every boot and every reload
  starts ON AIR with 50 s on the clock, whatever phase the log was written
  in. Code is intent; whether that is a design ruling or an accident is OPEN
  (O5).
- **Pauses with the tree.** The autoload keeps the default
  `process_mode` (INHERIT), so `get_tree().paused = true` (hud.gd:124, 190)
  stops it. README ledger (line 97): "Escape now pauses: the world and its
  clocks hold". `docs/production/UE-ACCESS-SPEC-LAW9.md` line 252: "A pause
  that let the 50/18 s clock run would be the interface lying about the
  schedule." UE: the phase timer lives on the world `FTimerManager`, which is
  expected to hold while the world is paused — VERIFY in-engine (O8); do not
  assume.

### 1.4 The two readout colours

Both readers of `phase_text()` also colour the label from `on_air`
(hud.gd:534, wall_clock.gd:43, identical literals):

| Phase | `Color(r, g, b)` | Reads as |
|---|---|---|
| ON AIR | `(0.89, 0.64, 0.24)` | amber |
| BREAK | `(0.55, 0.78, 0.50)` | green |

These are code constants, therefore canon by the port brief. The lighting
bible's grammar (RED = watched = safe; phosphor green = information, never
room light — `docs/canon/restoration-lighting-bible.md`, cited via
`docs/production/ROOM-BRIEFS-3.1-3.5.md` line 46) is about room light and
tallies, not these two label tints; whether the label tints should follow
the grammar is OPEN (O1). Port the literals; raise the ruling.

### 1.5 Where the clock is read in the world

- Four `WallClock` repeaters, `scripts/world_builder.gd` 537: at Godot
  metres `(0, 2.3, -24.5)`, `(-15.5, 2.5, -24.6)`, `(5.5, 2.3, -26.6)`,
  `(0, 2.3, 0)`. Each is a housing plus a billboard `Label3D` (font 44) at
  `(0, -0.55, 0.05)` under the face, text and tint per §1.1/§1.4 every frame.
- The HUD clock label (hud.gd:531-534): `prefix + phase_text()` where prefix
  is `"NIGHT · "` at night, else `"DAY %d · " % day`.
- Canon on the objects: "Studio clock + ON AIR sign · T4 · read · The
  break-window masters" and "ON AIR master · never · inspect only · Grammar
  owns it; the one switch the player may never throw"
  (`docs/canon/restoration-room-inventory.md` lines 193, 169). The design doc
  (`docs/canon/restoration-design-doc.md` line 122): "the studio clock and ON
  AIR sign for break windows" as world UI, no floating HUD in the compound.
  Note the reference build DOES draw the HUD clock; code is intent for the
  port, the doctrine is the direction — OPEN whether the HUD clock survives
  into UE (O10).

---

## 2 · EVERY READER OF THE CLOCK (complete: grep `Broadcast\.` over `scripts/`)

| Site | Reads | Rule, verbatim from code | Gates besides the clock |
|---|---|---|---|
| rundown.gd:122 | subscribes `phase_changed` → `_on_phase` | §2.1 | — |
| rundown.gd:295 | `on_air` in `_physics_process` | BREAK: (AF) fold timer / door-fold check, else `move_toward(_target, MOVE_SPEED 2.4)`; ON AIR: the hunt (warn/strike ladder) | `is_night` (291); premiere branch first (204) |
| rundown.gd:415 | `on_air` | ON AIR idle: "the segment, performed to no one" — sway, jaw `sin`-flap, shoulder wave, tail | `visible && is_night && !looming && !premiere_live` |
| harriet.gd:71 | `on_air` | `_physics_process`: if not ON AIR, `return` before `_t += delta` — THE FREEZE, mid-motion; sway is `rotation.z = sin(_t*0.9)*0.04` | none (day and night) |
| harriet.gd:78 | `on_air` | `get_prompt()`: BREAK → `"HARRIET · mid-motion"`, ON AIR → `"HARRIET · in her chair (E)"` (GameText rows 201, 202) | — |
| harriet.gd:88 | `on_air` | `interact()` on BREAK: if slip armed and not taken → take the slip (H1 arms); else `Achievements.unlock("A06")`, toast `"She does not resume until the return cue. Her cup has been rising since Tape 1."`, and on `day >= 2` arm the slip with its toast | dead-Harriet branch first (84) |
| door.gd:29 | `on_air` | `get_prompt()`: `"%s · HELD FOR AIR · moves on the break"` (GameText row 108) | `window_bound && !cascade_active` |
| door.gd:40 | `on_air` | `interact()`: toast `"HELD FOR AIR · the door moves during the break window."` (row 109) and RETURN — the door does not move | `window_bound && !cascade_active`; lock check first (37) |
| floor_manager.gd:49 | `on_air` | `visible = is_night && on_air && !premiere_live`; everything else in his tick is behind `visible` | — |
| wall_clock.gd:42-43 | `phase_text()`, `on_air` | label text + tint per §1.4, every frame | — |
| hud.gd:532-534 | `phase_text()`, `on_air` | clock label text + tint per §1.5/§1.4 | — |

Already in C++: `Rundown.cpp` 157 (`OnPhaseChanged`), 348 (`IsOnAir()` in
Tick), `Harriet.cpp` 22 (`IsOnAirEffective`). The four remaining readers
(door, floor manager, wall clock, HUD) have no UE class yet.

**Window-bound doors** are exactly the `Doors.csv` rows with `kind = window`
(`world_builder.gd` 256-257 sets `door.window_bound = true`): `STAGE HALL /
STUDIO A` (gap −12.0, −24.0, width 1.6, axis x) and `STUDIO A / SCENE DOCK`
(gap −15.5, −36.0, width 1.6, axis x) — two doors, both in the stage end.
Canon: "window holds bind except during cascade" (LAW 6); "QA-10 Window
holds honored except during cascade; ON AIR clock and hum agree" and "QA-20
… waived window holds during" (`docs/production/restoration-qa-regression.md`
lines 18, 34); invariant "I04 Window holds obey the clock, and yield only to
the cascade … TELEMETRY: liveness_log 'window holds waived' lines exist only
while cascade_active" (`docs/production/restoration-invariant-suite.md` line
8; the line is `liveness_check.gd` 24, behind `cascade_active` at 14). The
door hold has NO premiere gate and NO night gate: it binds by day too.

### 2.1 `Rundown._on_phase(now_on_air)` — verbatim order (rundown.gd 146-200)

**ON AIR (`now_on_air == true`):**
1. `_label.text = SEGMENTS[_idx][0]` (the segment name returns).
2. `_warned = false` (the warn-once latch re-arms every ON AIR).
3. `_strike_r = 2.6 if strikes >= 3 else 2.2` (the savor widening).
4. `_warn_r = 5.0 if director.profile() == "HIDER" else 7.0`.
5. If `cascade_active`: `_warn_r = max(3.5, _warn_r - 1.5)`.
6. If `is_night` (the only night gate in this handler):
   a. If `director.profile() == "CHECKER"`: `m = director.most_watched_rig()`;
      if `m` exists, is not killed, and `m.cam_position` is within 14.0 m of
      him → `m.set_killed(true)`, log `"KILL most-watched rig (CHECKER
      read)"`, toast `"The feed you trust went dark first."`.
   b. Then for EVERY rig not killed whose `cam_position` is within 9.0 m of
      him → `set_killed(true)`, toast `"Somewhere, a camera dies. The map is
      shorter tonight."` (one toast per rig; the last one wins the HUD).

**BREAK (`now_on_air == false`)** — NOT night-gated; `_idx` changes by day
too, but by day he does not move (`_physics_process` returns at 291-292) and
`_on_night` re-anchors him at `_anchor(_idx)` when night begins (142):
1. If a noise was heard within the last 12.0 s (`_heard_t` set by `_on_noise`,
   which itself refuses dead-room noise, daytime and premiere): `_idx` = the
   segment whose anchor is nearest `_heard_pos`; log `"RELOCATE toward heard
   noise at %s -> segment %d"` with the rounded position; the FIRST time
   ever this session: `Achievements.unlock("A08")` and toast `"It changed
   direction. You were not quiet."`.
2. Else if `director.profile() == "SPRINTER"` and a player exists: `_idx` =
   the segment whose anchor is nearest the PLAYER; log `"RELOCATE
   sprinter-bias -> segment %d"`.
3. Else `_idx = (_idx + 1) % 3`; log `"RELOCATE cycle -> segment %d (profile
   %s)"` with the current profile string.
4. `_target = _anchor(_idx)`; `_label.text = "· in transit ·"`; segment tone
   `freq_a = SEGMENT_FREQS[_idx]`, `freq_b = freq_a * 1.5`
   (`SEGMENT_FREQS = [220.0, 262.0, 196.0]`, rundown.gd 65).

`_anchor(i)` is the room centre `(x, 0, z)` of `SEGMENTS[i][1]` from the
`rooms` table (rundown.gd 350-355): STORY CORNER → TAPE LIBRARY, THE SONG →
STUDIO A, CRAFT TIME → PATCH BAY (rundown.gd 9-13; the C++ `SegmentAnchors`
comment agrees).

Everything in step 6 and steps 2–4 is gated on `director` being non-null.
The director is null in DEMO (§3.1), so DEMO has no rundown at all — the
whole `_spawn_rundown` returns early.

### 2.2 The ON AIR idle at rundown.gd:415 — a known canon conflict

`docs/production/CHUM-RIG-AND-ANIMATION-SPEC.md` line 45 already tables this
branch against the motion canon: 'ON AIR idle "the segment, performed to
no one": jaw `sin`-flap, sway, shoulder wave, tail (GD 414-428)' versus
"The jaw NEVER ... flaps"; "zero idle sway" (MOTION §AFTER-FIRE). That
ruling belongs to the rig spec and Phase 1.9/1.12, not here; this file only
records that the branch exists, what gates it, and that the C++ port must
not reproduce it for the After-Fire body. Whether the PRE-fire (stage) body
performs the segment ON AIR is OPEN in that spec, not re-opened here.

---

## 3 · THE COVERAGE DIRECTOR (`scripts/coverage_director.gd`, `class_name CoverageDirector extends Node`)

Header comment, verbatim (lines 3-5): "v0 of the thing that watches how you
watch. Profiles the player at night (checker, sprinter, hider) from
behavior, never from menus. Burning dailies resets its read, honoring the
promise the burn message has made since 006."

### 3.1 Construction and wiring (`scripts/world_builder.gd` 571-584)

```
func _spawn_rundown() -> void:
	if GameState.DEMO:
		return                      # DEMO: no director, no rundown
	var cd := CoverageDirector.new()
	cd.rigs = _rigs                 # every MonitorRig the world stamped
	add_child(cd)
	var r := Rundown.new()
	... r.rigs = _rigs ; r.director = cd
```

`_rigs` is the list of `MonitorRig` nodes from `Monitors.csv` (two rows today:
CAM 1 · CORRIDOR, CAM 2 · STACKS; `world_builder.gd` 316-324). The director
holds the SAME array object the rundown, cascade, liveness check and night
trip hold.

### 3.2 Fields

| Var | Type | Default | Saved? | Notes |
|---|---|---|---|---|
| `rigs` | `Array[MonitorRig]` | `[]` | no | injected by world_builder |
| `LOG_PATH` | const String | `user://coverage_log.txt` | — | §3.4 |
| `_player` | `Node3D` | null | no | resolved lazily from group `"player"` on the first night physics frame — that frame is otherwise skipped (lines 41-43) |
| `_monitor_s` | float s | restored from `GameState.cov_monitor` | via GameState (§3.5) | seconds facing a monitor |
| `_moving_s` | float s | restored from `GameState.cov_move` | via GameState | seconds moving |
| `_still_s` | float s | restored from `GameState.cov_still` | via GameState | seconds still |
| `_watched` | `Dictionary[MonitorRig → float s]` | `{}` | **no** — session only; lost on reload even though the three sums survive | per-rig watch time, feeds `most_watched_rig()` |
| `_save_t` | float | 0.0 | no | 5 s flush accumulator |

### 3.3 `_ready()` — verbatim order (lines 19-24)

1. `GameState.daily_burned.connect(reset_read)`.
2. Restore the three sums from `GameState.cov_monitor / cov_move / cov_still`
   (these are v16 keys 38-40; `ue/PORT-NOTES-STATE.md` §1).
3. Log `"SESSION OPEN · restored counters m=%.1f mv=%.1f st=%.1f"`.

### 3.4 `log_line(text)` — the telemetry contract (lines 27-35)

Appends one line to `user://coverage_log.txt`, creating the file if absent:

```
[day %d %s] %s        # %s = "night" if GameState.is_night else "day"
```

Writers (complete; grep `director.log_line` in `scripts/`): the director
itself (`SESSION OPEN`, `READ RESET · dailies burned`) and the rundown —
`KILL most-watched rig (CHECKER read)` (159), `RELOCATE toward heard noise at
%s -> segment %d` (177), `RELOCATE sprinter-bias -> segment %d` (191),
`RELOCATE cycle -> segment %d (profile %s)` (195), `STRIKE af tally-cool`
(285), `STRIKE seg %d d=%.1f[ savor][ THRU-WALL]` (316-319), `WARN seg %d
d=%.1f[ savor]` (326).

Readers: `scripts/invariant_parser.gd` `_coverage()` (lines 24-45) scans the
file for substrings `"WARN "` (sets the latch), `"STRIKE "` (I02 fails on
`"THRU-WALL"`; I01 fails if no WARN since the last STRIKE unless the line
contains `"savor"`; then clears the latch) and `"toward heard noise"` (I22
count). `tools/invariant_parser.py` applies the identical rules (lines 23-34)
to ONE file, `Saved/decision_log.txt`, which is where every UE class already
appends (`Rundown.cpp` 411-419, `Harriet.cpp` 81-88, and the 0.9a ledger:
"the same parser, the same verdict"). Invariants that name this log:
I01, I03, I21 ("The Director is deterministic and explainable … every
blocking decision carries a reason string. TELEMETRY: coverage_log"), I22
(`docs/production/restoration-invariant-suite.md` lines 5, 7, 33, 34).

Two format facts the port must keep: the parser matches by substring, so
the `[day N night]` prefix is optional to it but IS the Godot format
(§6 lists the drift); and the reason strings are the invariant's evidence,
so they are canon text — port them byte for byte, outside localisation (O3).

### 3.5 `_physics_process(delta)` — verbatim order (lines 38-62)

Fixed-step (Godot default 60 Hz; `project.godot` sets no override — O6).

1. If not `GameState.is_night`: return. **The director counts only at
   night**; by day nothing accumulates and the label does not update.
2. If `_player == null`: resolve from group `"player"` and return (one frame).
3. `moving = _player.velocity.length() > 0.5`. Moving → `_moving_s += delta`;
   else `_still_s += delta`. Every night frame lands in exactly one of the
   two.
4. For each rig in `rigs`: `to_mon = rig.monitor_position - player.position`;
   if `|to_mon| < 3.5` and `(-player.basis.z) · normalize(to_mon) > 0.6`:
   `_monitor_s += delta` and `_watched[rig] += delta`. Note this is per rig,
   so two monitors within 3.5 m in the same 53° cone both count the same
   frame (O9 — code is intent, record it). Distance and facing use the full
   3D vector, including height.
5. `GameState.coverage_label = profile()` — every night physics frame.
6. `_save_t += delta`; when `> 5.0`: reset it and copy the three sums into
   `GameState.cov_monitor / cov_move / cov_still`. This does NOT call
   `save_log()`; the values reach disk with whatever mutation next saves
   (PORT-NOTES-STATE §1 "Save-write contract"). A crash within 5 s of the
   last flush loses up to 5 s of counters and up to one unsaved flush.

### 3.6 `profile()` — the four labels, verbatim precedence (lines 65-72)

```
if _monitor_s < 2.0 and _moving_s < 4.0 and _still_s < 4.0: return "AUDIENCE"
if _monitor_s >= _moving_s and _monitor_s >= _still_s:      return "CHECKER"
if _moving_s >= _still_s:                                    return "SPRINTER"
return "HIDER"
```

Ties resolve toward CHECKER, then SPRINTER. AUDIENCE is the only label that
depends on absolute seconds; the other three are pure ordering. With the
sums restored at boot, a returning player is never AUDIENCE for long — but
the binder line says otherwise (O2).

Consumers of the label string: `GameState.coverage_label` (default
`"AUDIENCE"`, session-only, PORT-NOTES-STATE §2) read by the binder,
hud.gd:257: `"COVERAGE READS YOU AS: %s (this session)"` (GameText row 244);
the rundown reads `director.profile()` directly for HIDER (warn 5.0),
CHECKER (the kill), SPRINTER (the bias) and the cycle log (§2.1). No other
script reads it. Achievements do not read it.

### 3.7 `most_watched_rig()` (lines 75-83)

Strict `>` over `_watched`, starting from `best_t = 0.0` → returns the rig
with the greatest watch time this SESSION, or `null` when nothing has been
watched (or after a reload, since `_watched` is not saved). Return type is
`MonitorRig`; the caller uses `.killed`, `.cam_position`, `.set_killed()`.

### 3.8 `reset_read()` (lines 86-95) and its trigger

Zero the three sums, `_watched.clear()`, zero the three `GameState.cov_*`,
`GameState.coverage_label = "AUDIENCE"`, log `"READ RESET · dailies burned"`.
Trigger: `GameState.daily_burned` (game_state.gd 139), emitted by
`burn_daily()` (game_state.gd 276-287) as its LAST act — after `carried_id =
-1`, the conditional `strikes -= 1`, the toast, `save_log()` and
`sheet_changed`. Toast canon, verbatim: `"BURNED · TAKE %d. Her name fades
from the line. Its read on you resets."` (only when a strike was removed;
the clean-sheet toast does not promise a reset but the reset still fires).
Playtest canon: "P5 … confirm single-carry rule and that burning resets the
Director read (binder shows AUDIENCE)"
(`docs/production/restoration-playtest-protocol.md` line 41).

Because `reset_read` zeroes `GameState.cov_*` but does not save, and
`burn_daily` saved BEFORE emitting, the zeroed counters are on disk only
after the next `save_log()` from anyone. Code is intent; note it.

---

## 4 · SIGNAL AND STATE INVENTORY

| Name | Owner | Params | Emitted by | Listeners | UE |
|---|---|---|---|---|---|
| `phase_changed` | Broadcast | `now_on_air: bool` | `_process` flip only | rundown `_on_phase` (only subscriber; every other reader polls `on_air`) | `FOnPhaseChanged` present; `ARundown::OnPhaseChanged` bound |
| `daily_burned` | GameState | — | `burn_daily()` | coverage_director `reset_read` (only subscriber) | delegate NOT declared in `RestorationState.h` (only `FOnRunEnded`, `FOnSheetChanged`, `FOnNoise` exist) |
| `coverage_label` | GameState var | String | director every night physics frame; `reset_read` | hud binder | not in C++ |
| `cov_monitor / cov_move / cov_still` | GameState vars, v16 keys 38-40 | float s | director flush (5 s) and `reset_read` | director `_ready` | `CovMonitor / CovMove / CovStill` present in `URestorationSaveGame` and the subsystem (`RestorationState.h` 93-95, 176-178); only the save round-trip touches them (`RestorationState.cpp` 215 save, 265 load) — no gameplay writer yet |
| `is_night`, `day` | GameState | — | — | director (gate, log prefix), every rundown gate | `bIsNight` present |
| `cascade_active` | GameState | — | cascade.gd 21/37 | door hold waiver; rundown warn narrowing | present |
| `premiere_live` | GameState | — | — | floor manager, rundown idle, rundown `_on_noise` | — |

---

## 5 · LAWS, INVARIANTS AND QA THIS FILE MAKES IMPLEMENTABLE

- LAW 6 (THE-LAWS.md line 7): clock (§1), Harriet freeze (§2 harriet.gd:71),
  window holds and the cascade waiver (§2 door.gd).
- Dread doctrine L2 (`docs/canon/restoration-dread-doctrine.md` line 6):
  "Safety is procedural: the beat, the stances, the signs, ON AIR … the
  ritual must actually work." The clock must never lie: no phase may be
  extended, skipped or forced by any system except the tree pause.
- Audio bible (`docs/production/restoration-audio-bible.md` line 8):
  "BROADCAST GRAMMAR. ON AIR and BREAK are two room tones, not one. The
  whole building breathes on the clock." No reference-implementation code
  switches a room tone on `phase_changed` today (the rundown's segment tone
  changes frequency on BREAK, §2.1 step 4, which is the location tell, not a
  room tone). The room-tone swap is OPEN for the audio unit (O11).
- Invariants I01, I02, I04, I21, I22 (§3.4); QA-10, QA-20 (§2).
- Player routing (`docs/canon/restoration-player-routing.md` line 14):
  "Break windows are traffic lights … Traversal legs are tuned to fit a
  window when planned and to miss it when panicked." The 18 s window is the
  tuning target for the stage-end legs; not a code rule.

---

## 6 · DELTAS: current C++ vs this transcription (the checklist)

**`URestorationClock` (present, `RestorationClock.h`)** — semantics match
(§1.2). Missing surface:
- [ ] `TimeLeft()` — `FMath::Max(remaining, 0.f)` from `GetTimerRemaining(PhaseTimer)`.
- [ ] `PhaseText()` — `ceil` the seconds, then GameText rows 45/46 through
      the string table: `● ON AIR · break in 0:%02d` / `○ BREAK · window
      closes 0:%02d`.
- [ ] The two label tints (§1.4) as constants beside the clock so wall clocks
      and the HUD share them.
- [ ] Pause behaviour verified in-engine (O8); a functional test that pauses
      the world across a flip and asserts no flip occurred.

**`ARundown::OnPhaseChanged` (present, `Rundown.cpp` 157-189)** — against
§2.1:
- [ ] ON AIR step 4: HIDER → `WarnR = 5.0f` (currently always `WarnRadius`).
- [ ] ON AIR step 5: cascade narrowing `FMath::Max(3.5f, WarnR - 1.5f)`.
- [ ] ON AIR step 6a: CHECKER kill of the most-watched rig within 14 m, with
      its log line and toast.
- [ ] ON AIR step 6b: blanket kill of every rig within 9 m, with its toast.
      Both need a rig class with `bKilled` / `SetKilled` / `CamPosition`
      (the Monitors.csv rows).
- [ ] BREAK step 1: `A08` + toast `"It changed direction. You were not
      quiet."` on the first heard-noise relocation.
- [ ] BREAK step 2: the SPRINTER bias branch and its log line (currently the
      cycle follows the noise branch directly).
- [ ] BREAK step 3: log `(profile %s)` with the real profile — the placeholder
      `(profile UNKNOWN)` at `Rundown.cpp` 186 is drift the parser tolerates
      but the ledger should not keep.
- [ ] BREAK step 4: the `· in transit ·` label and the segment-tone
      frequency change (MetaSounds per the migration map, line 12).
- [ ] Do NOT port the rundown.gd:415 idle for the After-Fire body (§2.2).

**Coverage director (absent)** — new `UWorldSubsystem` (name OPEN, O4):
- [ ] Fields per §3.2; restore the three sums from `URestorationState`
      `CovMonitor/CovMove/CovStill` in `OnWorldBeginPlay`; log `SESSION OPEN`.
- [ ] Declare `FOnDailyBurned` on `URestorationState`, broadcast at the end
      of `BurnDaily()` (§3.8 order), bind `ResetRead`.
- [ ] Tick per §3.5 in the same order; night gate first; the 5 s flush into
      the subsystem's three floats (no save call).
- [ ] `Profile()` verbatim (§3.6); write `CoverageLabel` on the state
      subsystem (add the field: session-only, default `"AUDIENCE"`).
- [ ] `MostWatchedRig()` and `ResetRead()` per §3.7–3.8, including the
      `READ RESET · dailies burned` line.
- [ ] `LogLine` appends to `Saved/decision_log.txt` (the unified UE log; the
      Godot path `user://coverage_log.txt` is NOT reproduced — 0.9a ledger).
      Prefix each line `[day %d night|day] ` as `coverage_director.gd` 34
      does; today's C++ writers (`Rundown.cpp` 411, `Harriet.cpp` 81) emit
      bare text, which the substring parser accepts — bring them to the
      same prefix or rule the prefix dropped (O12). Do not route these
      strings through the StringTable (O3).
- [ ] Wire `ARundown::Director` and read `Profile()` at the four sites in
      §2.1; keep every branch null-safe as the GDScript is, because DEMO
      spawns neither (§3.1).

**Readers with no UE class yet** (§2): the window-bound door (two Doors.csv
rows; prompt row 108, toast row 109; `!cascade_active` waiver), the floor
manager visibility gate, the four wall clocks (§1.5), the HUD clock line.

---

## 7 · OPEN (canon is silent; do not invent)

- **O1** Are the ON AIR amber / BREAK green label tints (§1.4) canon, or
  should they follow the lighting bible's grammar? Code has the literals;
  no canon doc names them.
- **O2** The binder says `"(this session)"` but the three sums are restored
  from the save at boot (§3.3), so the read spans sessions; only `_watched`
  is per session. Which is intended: the text or the persistence?
- **O3** GameText.csv rows 62, 64, 565 are telemetry reason strings
  (`SESSION OPEN…`, `READ RESET…`, `KILL most-watched rig…`) inside the
  StringTable source. Localising them would break the invariant parser.
  Ruling needed: exclude telemetry from the table (recommended by the
  parser contract) or keep and never translate.
- **O4** Class name for the coverage subsystem in UE (the migration map says
  only "a WorldSubsystem").
- **O5** The clock is not saved; every reload boots ON AIR at 50 s (§1.3).
  Design ruling or accident?
- **O6** Godot physics tick is the 60 Hz default (no override in
  `project.godot`); the director's sums are delta-integrals so the UE
  variable tick reproduces the seconds, but the `> 0.5` m/s moving test is
  sampled per frame — confirm no fixed-tick assumption is wanted.
- **O7** rundown.gd:415 ON AIR idle vs the motion canon — ruled in
  `CHUM-RIG-AND-ANIMATION-SPEC.md` line 45 for After-Fire; the pre-fire body
  is that spec's question, not this file's.
- **O8** UE pause: does the world `FTimerManager` hold across the LAW 9
  pause? Verify, then record in the ledger.
- **O9** Per-rig monitor counting can double-count one frame when two
  monitors share the 3.5 m / 0.6-dot cone. Code is intent; flagging so the
  port does not "fix" it silently.
- **O10** Does the HUD clock line (hud.gd:531-534) survive into UE, given
  the design doc's "No floating HUD in the compound" (line 122)? The
  reference build shows both HUD and wall clocks.
- **O11** The audio bible's two room tones on the clock (§5) have no code in
  the reference implementation; audio unit's call.
- **O12** Telemetry line prefix `[day N night|day]`: Godot writes it, UE
  does not; the parser is indifferent. Rule one format for the ledger.
