# PORT NOTES · STATE (unit 0.8b-spec · the v16 save schema + game_state.gd inventory)

Source of truth: `scripts/game_state.gd` (autoload `GameState`, 777 lines) at
repo HEAD 5296190. Per PORT-BRIEF: THE CODE IS THE INTENT. Where this document
and the GDScript disagree, the GDScript wins and this document is the defect.

Target: `URestorationState` (UGameInstanceSubsystem) + `URestorationSaveGame`
in `ue/Restoration/Source/Restoration/RestorationState.{h,cpp}`. Migration map
law: save semantics, field names and every knob number MUST NOT CHANGE.

This is the 0.8b implementation checklist. Every row is a thing the C++ must
carry; §8 lists exactly what 0.8a already carries and where it diverges.

---

## 1 · THE SAVE FILE (the transmitter log)

| property | value (from source) |
|---|---|
| path | `user://transmitter_log.json` (`SAVE_PATH`) → UE: one slot, name `restoration`, index 0 (0.8a's choice, keep) |
| format | JSON, `JSON.stringify(data, "\t")` (tab-indented, one object) |
| version | `SAVE_VERSION := 16` — written as key `version`, an int |
| written by | `save_log()` — called by nearly every mutator (see §5, column SAVES) |
| read by | `load_log()` in `_ready()` after `load_settings()` |
| missing file | `load_log()` returns silently; defaults stand |
| non-dict JSON | returns silently; defaults stand |
| missing keys | every key is `data.get(k, default)` — a partial save NEVER fails to load |
| number coercion | Godot's parser returns floats; every int field is wrapped `int(...)`, every float `float(...)`, bool `bool(...)`, string `str(...)` |
| array/dict guards | array fields are only assigned when `typeof(...) == TYPE_ARRAY`; `paper` only when `TYPE_DICTIONARY` (else the default stays) |
| `paper` merge law | loaded per key INTO the default dict (`paper[k] = int(p[k])`): a save carrying only S1/S5 (demo) loaded by a full build keeps S2–S4 at 3 |
| older version | `v < 16` → `save_log()` immediately (rewrites as v16), then deferred `notify` "LOG MIGRATED · format v%d to v%d. Nothing was lost." |
| newer version | `v > 16` → deferred `notify` "LOG FROM A NEWER BUILD · v%d read by v%d. Proceed gently." (still loaded) |
| version default | absent `version` key reads as 1 → migrates |
| DEMO scrub | when `DEMO == true`, `save_log()` ERASES these keys before writing: `decision, assets, leland_answers, lockdown_done, finale_done, ending_reached, lie_pending, seance_wear, has_fire_tape, fire_tape_watched, dock_done, crate_opened, presigned_seen, cascade_done, casualties` (15 keys) |

Save-and-load asymmetry to preserve: `is_night` is NOT in the save (see §3).
A reloaded game always wakes in daytime state with `day` intact.

---

## 2 · THE v16 `_save_dict` SCHEMA — 55 keys, in written order

Column KEY is the JSON key (the contract). VAR is the GDScript field. TYPE is
the JSON value type as written. DEFAULT is the field's declared default (what
a missing key loads as). NEW GAME is the value after `reset_new_game()`
("carry" = NOT reset — survives NEW GAME, by the code's intent).

| # | KEY | VAR | TYPE | DEFAULT | NEW GAME | notes |
|---|---|---|---|---|---|---|
| 1 | `version` | `SAVE_VERSION` | int | 16 | 16 | const |
| 2 | `mode` | `mode` | int (enum Mode) | 1 (`LATE_NIGHT`) | carry | `MATINEE=0, LATE_NIGHT=1, ONE_TAKE=2` |
| 3 | `tbc` | `tbc_enabled` | bool | false | carry | time-base corrector toggle |
| 4 | `tape` | `current_tape` | int | 1 | 1 | `= mini(day, 5)` on each morning |
| 5 | `paper` | `paper` | dict String→int | `{"S1":3,"S2":3,"S3":3,"S4":3,"S5":3}` | same (demo: `{"S1":3,"S5":3}`) | lines left per station; loaded by per-key merge |
| 6 | `signatures` | `signatures` | array of Signature (§2.1) | `[]` | `[]` | append-only |
| 7 | `captures` | `captures` | array of Capture (§2.1) | `[]` | `[]` | append-only |
| 8 | `strikes` | `strikes` | int | 0 | 0 | the sheet; full at 4 |
| 9 | `items_lost` | `items_lost` | int | 0 | 0 | index into `ITEM_ORDER`; max 7 |
| 10 | `day` | `day` | int | 1 | 1 | |
| 11 | `keys` | `keys` | array of String | `[]` | `[]` | key ids, e.g. `"QUIET ROOM"` |
| 12 | `pt` | `pt` | int | 0 | 0 | points (`add_pt`) |
| 13 | `dailies` | `dailies` | array of Daily (§2.1) | `[]` | `[]` | |
| 14 | `daily_seq` | `daily_seq` | int | 0 | 0 | monotonic id source for dailies |
| 15 | `carried_id` | `carried_id` | int | -1 | -1 | -1 = carrying nothing |
| 16 | `carried_take` | `carried_take` | int | 0 | 0 | |
| 17 | `film_watched` | `film_watched` | bool | false | false | |
| 18 | `signals_known` | `signals_known` | array of String | `[]` | `[]` | show-signal names, e.g. `"HOLD YOUR APPLAUSE"`; 7 unlocks A07 |
| 19 | `screening_done` | `screening_done` | bool | false | false | |
| 20 | `run_complete` | `run_complete` | bool | false | false | set on the morning of day ≥ 3 |
| 21 | `has_fire_tape` | `has_fire_tape` | bool | false | false | demo-scrubbed |
| 22 | `fire_tape_watched` | `fire_tape_watched` | bool | false | false | demo-scrubbed |
| 23 | `seance_wear` | `seance_wear` | float | 0.0 | 0.0 | percent; 70.0 threshold lives in seance_dock/hud; demo-scrubbed |
| 24 | `leland_answers` | `leland_answers` | array of int | `[]` | `[]` | seance FRAME indices (0..MAX_FRAME); 5 = complete; demo-scrubbed |
| 25 | `presigned_seen` | `presigned_seen` | bool | false | false | demo-scrubbed |
| 26 | `dock_done` | `dock_done` | bool | false | false | demo-scrubbed |
| 27 | `assets` | `assets` | array of String | `[]` | `[]` | asset ids; 4 = all; demo-scrubbed |
| 28 | `decision` | `decision` | String | `""` | `""` | ledger entry: `AUTHENTICATE / DESTROY / PERFORM` per `objective_text`; demo-scrubbed |
| 29 | `lockdown_done` | `lockdown_done` | bool | false | false | demo-scrubbed |
| 30 | `finale_done` | `finale_done` | bool | false | false | demo-scrubbed |
| 31 | `ending_reached` | `ending_reached` | String | `""` | `""` | ending name; demo-scrubbed |
| 32 | `lie_pending` | `lie_pending` | bool | false | **carry** | THE ONE INTERFACE LIE: set by `mark_ending(lie=true)`, consumed by title.gd on next boot; demo-scrubbed |
| 33 | `vess_insight` | `vess_insight` | bool | false | false | |
| 34 | `vess_credited` | `vess_credited` | bool | false | false | |
| 35 | `ng_relic` | `ng_relic` | String | `""` | computed | NG+ relic: `ITEM_ORDER[min(items_lost,7)-1]` if `finale_done and items_lost>0`, else `""` |
| 36 | `crate_opened` | `crate_opened` | bool | false | false | demo-scrubbed |
| 37 | `night_tripped` | `night_tripped` | bool | false | false | the once-ever trip (night_trip.gd) |
| 38 | `cov_monitor` | `cov_monitor` | float | 0.0 | 0.0 | coverage tallies |
| 39 | `cov_move` | `cov_move` | float | 0.0 | 0.0 | |
| 40 | `cov_still` | `cov_still` | float | 0.0 | 0.0 | |
| 41 | `photo_safe` | `photo_safe` | bool | false | **carry** | photosensitivity mode — lives in the LOG, not settings.cfg (as coded) |
| 42 | `cascade_done` | `cascade_done` | bool | false | false | demo-scrubbed |
| 43 | `read_props` | `read_props` | array of String | `[]` | `[]` | document ids; toast counts "of 10" |
| 44 | `af_active` | `af_active` | bool | false | **carry** | after-fire body live |
| 45 | `af_taught` | `af_taught` | bool | false | **carry** | the taught cool has happened once |
| 46 | `casualties` | `casualties` | array of Casualty (§2.1) | `[]` | `[]` | demo-scrubbed |
| 47 | `merle_offered` | `merle_offered` | bool | false | false | |
| 48 | `signoff_completed` | `signoff_completed` | bool | false | **carry** | |
| 49 | `row_casualties` | `row_casualties` | int | 0 | 0 | "fifty-eight, minus N" |
| 50 | `h2_pending` | `h2_pending` | bool | false | false | Harriet beat 2 armed |
| 51 | `deadroom_seen` | `deadroom_seen` | bool | false | **carry** | |
| 52 | `rejected_seen` | `rejected_seen` | bool | false | false | |
| 53 | `glimpse_seen` | `glimpse_seen` | bool | false | false | the once-ever sight (glimpse.gd) |
| 54 | `merle_1974` | `merle_1974` | bool | false | false | |
| 55 | `fire_unsealed` | `fire_unsealed` | bool | false | false | |

Written order is the order above (`_save_dict`); `load_log` reads in a
slightly different order and reads `version` LAST — order is irrelevant to
the contract but the C++ should keep `Version` first for the log line.

CARRY audit (fields `reset_new_game()` leaves alone — 8): `mode`, `tbc`,
`lie_pending`, `photo_safe`, `af_active`, `af_taught`, `signoff_completed`,
`deadroom_seen`. Port these AS-IS. Whether
any of them should reset is a canon question for the author, not a port fix
(the code is the intent; `lie_pending` carrying is the interface-lie law).

### 2.1 Record schemas (elements of the array fields)

**Signature** (`signatures[]`) — appended by `_sign_finish` and `mark_presigned`:

| key | type | source |
|---|---|---|
| `station` | String | `"S1".."S5"` |
| `tape` | int | `current_tape` at signing |
| `signed` | String | `Time.get_datetime_string_from_system()` — OR the literal `"TOMORROW"` for the presigned entry |
| `presigned` | bool | ONLY present on the `mark_presigned` entry (`true`); absent otherwise |

The LAST signature's `station` is the respawn anchor (`respawn_point()`).

**Capture** (`captures[]`) — appended by `log_capture(name)`:

| key | type | source |
|---|---|---|
| `name` | String | capture name |
| `tape` | int | `current_tape` |
| `at` | String | datetime string |

**Daily** (`dailies[]`) — appended by `strike()` and `mint_shortcut_daily()`:

| key | type | source |
|---|---|---|
| `id` | int | `daily_seq` after increment |
| `take` | int | the take number, OR **-1** for a shortcut daily |

0.8a's `FRestorationDaily {Id, Take}` matches. Keep -1 legal.

**Casualty** (`casualties[]`) — appended by `mark_casualty(who, cause, epitaph)`:

| key | type | source |
|---|---|---|
| `who` | String | `"MERLE" / "VESS" / "HARRIET" / "FLOOR MANAGER" / "LELAND"` (names used by callers) |
| `cause` | String | |
| `line` | String | the epitaph (note the key is `line`, not `epitaph`) |
| `day` | int | `day` at death |

One entry per `who` (guarded by `is_dead`). `all_cast_dead()` = MERLE, VESS,
HARRIET, FLOOR MANAGER all present (LELAND does not count).

---

## 3 · RUNTIME-ONLY FIELDS (public, NOT in the save)

| VAR | type | default | reset on NEW GAME | written by |
|---|---|---|---|---|
| `is_night` | bool | false | false | `set_night` |
| `in_retake` | bool | false | false | `strike` (sets true); **hud.gd:306 clears it** after the retake presentation |
| `station_points` | Dictionary String→Vector3 | `{}` | — | `register_station` (pos + (0, 0.5, 1.2)) |
| `premiere_live` | bool | false | false | `mark_ending` (false); live_production.gd (true) |
| `screening_active` | bool | false | — | screening_event.gd |
| `map_points` | Array of `[id, Vector2(x, z)]` | `[]` | — | world_builder.gd:288; read by map_view.gd |
| `cascade_active` | bool | false | false | cascade.gd |
| `recording` | bool | false | — | capture_bench.gd |
| `recording_left` | float | 0.0 | — | capture_bench.gd (seconds) |
| `crossing` | bool | false | — | live_production.gd |
| `crossing_caught` | bool | false | — | rundown.gd:221 (true), live_production.gd (false) |
| `harriet_slip` | bool | false | false | harriet.gd (true); `sign_log` consumes it |
| `fader_self` | bool | false | — | live_production.gd; read by hud.gd:503 |
| `_demo_t0` | int (private) | 0 | — | `demo_mark` |
| `_glyph_re` | Dictionary (private) | `{}` | — | `glyphs` regex cache |

Brain-relevant subset already on `URestorationState` (0.8a): `bIsNight,
bAfActive, bRecording, RecordingLeft, bAfTaught, bPremiereLive, bCrossing,
bCrossingCaught, bCascadeActive, bInRetake`.

---

## 4 · SETTINGS (a SEPARATE store: `user://settings.cfg`, `ConfigFile`)

Not the save. Loaded before the log. UE home: GameUserSettings subclass or
a second slot — but keep the section/key names for the parity of intent.

| section | key | type | default | field | clamp / note |
|---|---|---|---|---|---|
| `audio` | `master` | float (linear) | 1.0 | bus 0 volume | `linear_to_db(max(v, 0.001))` |
| `input` | `sensitivity` | float | 1.0 | `mouse_sens` | clamp 0.2..3.0 |
| `access` | `ui_scale` | float | 1.0 | `ui_scale` | setter clamps 0.8..1.6 |
| `access` | `captions` | bool | false | `captions_on` | |
| `access` | `assist` | bool | false | `assist_on` | assist-only difficulty (gap-audit ruling) |
| `keys` | `<action>` | int physical keycode | 0 (= unset) | InputMap | for each of `REMAP_ACTIONS` |
| `video` | `fullscreen` | bool | false | window mode | skipped when headless |

`REMAP_ACTIONS := ["interact", "respond", "improvise", "toggle_tbc", "map"]`.
`GLYPH_MAP := {"E": interact, "SPACE": respond, "Q": improvise, "T": toggle_tbc,
"M": map}` — `glyphs(text)` replaces whole-word tokens in UI text with the
CURRENT bound key name, upper-cased (the controls-map law: real binding glyphs).
`rebind` refuses a key already bound to another remap action ("KEY IN USE").

---

## 5 · PUBLIC METHOD INVENTORY (the API surface the port must expose)

SAVES = calls `save_log()`. EMITS = signals fired. TOAST = user-facing text via
`notify` (all toasts pass through `glyphs(tr(text))`).

| method | args → return | SAVES | EMITS | behavior (verbatim intent) |
|---|---|---|---|---|
| `paper_for` | (station) → int | | | 99 in MATINEE, else `paper[station]` (0 if unknown) |
| `sign_log` | (station) → bool | via `_sign_finish` | `log_refused` on refusal | non-MATINEE: no paper → if `harriet_slip` consume it and sign anyway (toast), else refuse; else `paper -= 1`. Then `_sign_finish` |
| `_sign_finish` | (station) → true | ✓ | `log_signed(station, remaining)`, `noise_event(respawn_point(), 4.0)` | append Signature; `Sfx.tick()`; `demo_mark("s1_signed")` if S1 |
| `respawn_point` | () → Vector3 | | | `station_points[last signature.station]`, fallback `(0, 1.0, 2.5)` |
| `register_station` | (id, pos) | | | `station_points[id] = pos + (0, 0.5, 1.2)` |
| `strike` | (player: Node3D) | ✓ | see §6 | the retake economy — full listing in §6 |
| `burn_daily` | () | ✓ | `sheet_changed(strikes)`, `daily_burned` | clear carried; if `strikes > 0` decrement (toast "Her name fades…") else toast "already clean" |
| `pick_daily` | (id, take) | ✓ | | remove daily by id; set carried; toast "CARRYING · SCENE 4 TAKE %d…" |
| `mint_shortcut_daily` | () | ✓ | `daily_added(seq, -1)` | daily with take -1 |
| `mark_casualty` | (who, cause, epitaph) | ✓ | | no-op if already dead; toast "THE LEDGER TAKES IT DOWN." |
| `is_dead` / `cause_of` / `all_cast_dead` | (who) → bool / String / () → bool | | | casualty lookups |
| `in_dead_room` | (pos) → bool | | | `|x-19| ≤ 2.2 and |z-2.5| ≤ 2.7` (Godot meters) — 0.8a has it in uu |
| `mark_read` | (id) | ✓ | | dedupe; toast "READ · filed to memory. (%d of 10 documents)" |
| `log_capture` | (name) | ✓ | `notify` | append Capture; "CAPTURED · %s · presentation kept" |
| `take_key` | (id, display) | ✓ | | dedupe (toast "You already carry"); toast "TAKEN · %s" |
| `has_key` | (id) → bool | | | |
| `add_show_signal` | (sig) | ✗ | | dedupe append — NOTE: does NOT save |
| `gain_asset` | (id, display) | ✓ | | dedupe; toast "ASSET BANKED · %s (%d of 4)"; at 4 a second toast |
| `mark_presigned` | () | ✓ | `log_signed("S4", paper_for("S4"))` | set flag; append the TOMORROW/presigned Signature (no paper spent) |
| `add_wear` | (n: float) | ✓ | | `seance_wear += n` |
| `add_pt` | (n: int) | ✓ | | `pt += n` |
| `set_night` | (on) | ✓ | `night_changed(on)` | on=false: `day += 1`, `current_tape = min(day, 5)`, MORNING toast; if `day ≥ 3 and not run_complete` → `run_complete = true` + toast. on=true: NIGHT toast |
| `set_mode` | (m) | ✓ | | no-op if same; toast "MODE · %s"; ONE_TAKE extra toast |
| `set_tbc` | (on) | ✗ | `tbc_changed(on)` | NOT saved here (persists on the next save_log) |
| `set_photo_safe` | (on) | ✓ | `photo_changed(on)` | toast ON/OFF |
| `start_finale` | () | | `finale_started(decision)` | |
| `mark_ending` | (name, lie=false) | ✓ | `ending_marked(name)` | `premiere_live=false; finale_done=true; ending_reached=name`; `Achievements.on_ending(name)`; `lie` → `lie_pending=true` |
| `toast` | (text) | | `notify(glyphs(tr(text)))` | |
| `set_capture_status` / `_raw` | (text) | | `capture_status(text)` | glyph-substituted / raw |
| `show_caption` | (text) | | `caption(tr(text))` only if `captions_on` | |
| `set_blackout` | (alpha) | | `blackout_changed(alpha)` | |
| `noise` | (pos, loudness) | | `noise_event(pos, loudness)` | the noise bus (I22 attribution) |
| `glyphs` | (text) → String | | | see §4 |
| `key_name` | (action) → String | | | current physical key name or `"?"` |
| `rebind` | (action, keycode, persist=true) | settings | | see §4 |
| `set_ui_scale` | (v) | settings | `ui_scale_changed(clamped)` | clamp 0.8..1.6 |
| `set_captions` / `set_assist` | (on) | settings | | |
| `load_settings` / `save_settings` | () | | | §4 |
| `demo_mark` | (event) | | | DEMO only: appends `[min %.1f] event` to `user://demo_funnel.txt` |
| `objective_text` | () → String | | | the HUD objective line — priority order: DEMO+captured → finale_done → decision set → run_complete∧day≥3 → night (dailies/carried variant) → day 1 chain (S1 signed → screening → capture → bed) → day≥3 gather → default |
| `save_log` / `load_log` | () | | | §1 |
| `reset_new_game` | () | ✓ | | `demo_mark("started")`; compute `ng_relic`; reset per §2 NEW GAME column |

Private helpers: `_signed_station(id)`, `_save_dict()`, `_announce_migration(v)`,
`_announce_newer(v)`.

---

## 6 · `strike(player)` — the retake economy, line by line

```
if in_retake: return
in_retake = true
strikes += 1; take = strikes
lost = ""
if items_lost < 7: lost = ITEM_ORDER[items_lost]; items_lost += 1   # cap 7
full = strikes >= 4 or mode == ONE_TAKE
if full:
    strikes = 0; save_log(); sheet_changed(0); run_ended(take); return
    # NOTE: in_retake stays TRUE here; hud clears it after the presentation
daily_seq += 1; dailies.append({id: daily_seq, take: take})
daily_added(daily_seq, take)
save_log()
sheet_changed(strikes)
captured(take, full=false, lost, respawn_point())
```

`ITEM_ORDER := ["WATCH", "PEN", "PHOTOGRAPH", "LIGHTER", "COMPACT", "KEYS", "LOUPE"]`
(7 items; `items_lost` therefore ranges 0..7). rundown.gd ALSO emits
`run_ended(dailies.size())` directly (rundown.gd:224) — the signal has two
emitters.

---

## 7 · SIGNAL INVENTORY (20) → UE multicast delegates with the SAME names

| signal | params | emitted by | connected by |
|---|---|---|---|
| `tbc_changed` | (enabled: bool) | `set_tbc` | hud, bench_tv |
| `log_signed` | (station: String, remaining: int) | `_sign_finish`, `mark_presigned` | hud, achievements |
| `log_refused` | (station: String) | `sign_log` | hud |
| `notify` | (text: String) | `toast`, `log_capture`, `_announce_*` | hud |
| `capture_status` | (text: String) | `set_capture_status(_raw)` | hud |
| `sheet_changed` | (count: int) | `burn_daily`, `strike` | hud, dresser |
| `night_changed` | (now_night: bool) | `set_night`; ALSO emitted raw by soak_runner.gd and live_production.gd (`emit(true)` without `set_night`) | world_builder, rundown, floor_manager, achievements |
| `captured` | (take: int, sheet_full: bool, lost_item: String, respawn: Vector3) | `strike` | hud |
| `daily_added` | (id: int, take: int) | `strike`, `mint_shortcut_daily` | dailies_manager |
| `daily_burned` | () | `burn_daily` | coverage_director |
| `run_ended` | (take: int) | `strike`; rundown.gd (raw) | hud, achievements |
| `finale_started` | (decision: String) | `start_finale` | hud |
| `noise_event` | (pos: Vector3, loudness: float) | `noise`, `_sign_finish` | rundown (`_on_noise`) |
| `photo_changed` | (on: bool) | `set_photo_safe` | bench_tv |
| `blackout_changed` | (alpha: float) | `set_blackout` | hud |
| `ui_scale_changed` | (scale: float) | `set_ui_scale` | hud |
| `caption` | (text: String) | `show_caption` | hud |
| `pause_requested` | () | player.gd (raw) | hud |
| `demo_ended` | () | capture_bench.gd (raw) | hud |
| `ending_marked` | (ending_name: String) | `mark_ending` | world_builder |

Raw emitters (`GameState.<signal>.emit(...)` from other scripts) are part of
the contract: the UE delegates must be public-broadcastable, not owned by the
subsystem's mutators alone.

0.8a carries `OnRunEnded(int32)` and `OnSheetChanged(int32)` — the remaining
18 are 0.8b's (`OnNoiseEvent` feeds the ARundown `ReportNoise` API already
built in 0.7).

---

## 8 · 0.8a C++ vs THIS SCHEMA — the delta list (0.8b work items)

Read against `RestorationState.h/.cpp` at HEAD. Each row is a divergence
from the code-as-spec, to be closed in 0.8b — not a criticism of 0.8a, which
declared itself "the brain-relevant core + save skeleton".

**Save fields (URestorationSaveGame)**

1. Carries 23 of 55 keys. Missing: `carried_id, carried_take, signals_known,
   presigned_seen, dock_done, assets, decision, lie_pending, vess_insight,
   vess_credited, ng_relic, crate_opened, night_tripped, cov_monitor,
   cov_move, cov_still, photo_safe, cascade_done, read_props, af_active,
   af_taught, casualties, merle_offered, signoff_completed, row_casualties,
   h2_pending, deadroom_seen, rejected_seen, glimpse_seen, merle_1974,
   fire_unsealed, pt` (32).
2. `Paper` is `int32` — schema is a String→int map (`TMap<FString,int32>`,
   5 stations, default 3 each; per-key merge on load).
3. `Signatures` is `int32` — schema is an array of Signature records
   (`station, tape, signed, presigned?`). The LAST one drives respawn.
4. `Captures` is `int32` — schema is an array of Capture records.
5. `SeanceWear` is `int32` — schema is `float`.
6. `LelandAnswers` is `int32` — schema is an array of int frame indices
   (membership is tested: `has(_frame)`, so a count is not equivalent).
7. `Mode` default is 0 (`MATINEE`) — schema default is 1 (`LATE_NIGHT`).
8. `CurrentTape` default is 0 — schema default is 1.
9. `SaveToSlot` writes only `Version, Strikes, ItemsLost, DailySeq, Dailies`;
   `LoadFromSlot` reads the same four. Every declared field must round-trip.
10. Migration: Godot re-saves immediately on `v < 16`; C++ only logs. Godot
    surfaces both migration/newer lines as `notify` toasts; C++ only logs.

**Strike()**

11. `ItemsLost` clamps at 6 (`FMath::Min(ItemsLost+1, 6)`) — Godot caps at
    `ITEM_ORDER.size()` = **7** (and only increments while below it). Off by
    one; also `ng_relic` indexes `ITEM_ORDER[min(items_lost,7)-1]`, so LOUPE
    is unreachable at 6.
12. The non-full path does not `SaveToSlot()` — Godot saves on every strike.
13. `bInRetake` is cleared inside `Strike()` on both paths — Godot leaves it
    TRUE and the retake presentation (hud.gd:306) clears it. Acceptable
    scaffold until P3 lands (the comment says so); the presentation must own
    it when it arrives, and the brain must not double-strike in the window.
14. No `captured(take, full, lost, respawn)` and no `daily_added` broadcast.
15. `mode == ONE_TAKE` does not force `full` (mode not ported yet).

**Runtime / API**

16. No `station_points` / `RegisterStation` / `RespawnPoint` (fallback
    `(0, 1.0, 2.5)` m → `(0, 250, 100)` uu under the stamping's axis swap —
    verify against build_greybox's PlayerStart before trusting this line).
17. Settings store (§4) not ported — `mouse_sens`, `ui_scale`, captions,
    assist, rebinds, fullscreen; pawn feel parity (3.1 m/s, crouch c045) is
    the other half of 0.8b and reads `mouse_sens` from here.
18. `InDeadRoom` is correct in uu; keep.

Close-out rule for 0.8b: the round-trip test must write a save with EVERY
key non-default, reload, and compare field-by-field (the 0.8a test compared
`strikes` alone — that is how items 2–9 stayed invisible).

---

## 9 · KNOB NUMBERS OWNED BY game_state.gd (must not change)

| knob | value |
|---|---|
| save version | 16 |
| paper per station (Late Night) | 3 |
| paper in MATINEE | 99 (never decremented) |
| full sheet | `strikes >= 4` (or any strike in ONE_TAKE) |
| items | 7, in `ITEM_ORDER` order |
| max tape | 5 (`min(day, 5)`) |
| run_complete morning | day ≥ 3 |
| signing noise | loudness 4.0 at `respawn_point()` |
| respawn fallback | `(0, 1.0, 2.5)` |
| station anchor offset | `(0, 0.5, 1.2)` |
| dead room | center (19, 2.5), half-extents (2.2, 2.7) |
| documents | 10 (`read_props` toast) |
| assets | 4 |
| Leland answers | 5 (consumers); wear gate 70.0 (consumers) |
| ui_scale clamp | 0.8..1.6 |
| mouse_sens clamp | 0.2..3.0 |
| demo scrub | 15 keys (§1) |
