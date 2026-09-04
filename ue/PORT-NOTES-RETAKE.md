# PORT NOTES · RETAKE — the capture presentation and the dailies loop, transcribed

**Unit C9 (CLOUD-OK).** What happens between the Rundown's hand closing and
the player standing at the last signed station again, and the errand that
every survivable capture leaves behind in the library stacks. Source of
truth, at the commit this file landed in:

| Script | Lines | Owns |
|---|---|---|
| `scripts/game_state.gd` | 777 | `strike()`, `pick_daily()`, `burn_daily()`, `mint_shortcut_daily()`, `respawn_point()`, the four signals, the save keys |
| `scripts/hud.gd` | 561 | the retake presentation (`_on_captured`) and the run death (`_on_run_ended`) |
| `scenes/main.tscn` | — | the `HUD/Retake` control: blackout + two labels |
| `scripts/dailies_manager.gd` | 46 | canister spawn slots, spawn-on-load and spawn-on-signal |
| `scripts/dailies_canister.gd` | 18 | the pickup |
| `scripts/degausser.gd` | 16 | the burn |
| `scripts/dresser.gd` | 46 | the seven items, one gone per capture |
| `scripts/casting_sheet_prop.gd` | 14 | the sheet on the Studio A wall |
| `scripts/rejected_edit.gd` | 68 | the only other way a daily is minted |
| `scripts/coverage_director.gd` | 95 | `reset_read()`, the burn's second effect |
| `scripts/rundown.gd` | — | the two `GameState.strike()` call sites and the third-line widening |
| `scripts/title.gd` | — | where a run death lands |

Where these notes and those files disagree, THE CODE IS THE INTENT
(`docs/packet/portbrief/PORT-BRIEF.md` law); fix the notes. Every string
quoted below is verbatim from source; where it also lives in the shipped
string table it is cited as `Data/GameText.csv` row N
(`ue/Restoration/Data/GameText.csv`). Where canon is silent the entry says
OPEN. Nothing here is a ruling.

UE home (`docs/packet/portbrief/UE5-MIGRATION-MAP.md:17`: HUD → UMG
widgets): the state half lives on `URestorationState`
(`ue/Restoration/Source/Restoration/RestorationState.h`), the presentation
is a UMG widget bound to the same delegates, the canisters / degausser /
dresser / sheet are actors placed from data. §10 is the delta checklist.

---

## 1 · CONSTANTS THAT ARE CANON (never change the numbers)

| Constant | Value | Where |
|---|---|---|
| Full sheet | `strikes >= 4` after the increment, or any strike in `ONE_TAKE` | `scripts/game_state.gd:492` |
| Take number | `take = strikes` *after* `strikes += 1` — the first capture is TAKE 1 | `scripts/game_state.gd:486-487` |
| `ITEM_ORDER` | `WATCH, PEN, PHOTOGRAPH, LIGHTER, COMPACT, KEYS, LOUPE` (7) | `scripts/game_state.gd:133` |
| Item loss | `if items_lost < 7: lost = ITEM_ORDER[items_lost]; items_lost += 1` — runs on EVERY strike, run deaths included, before the full check | `scripts/game_state.gd:489-491` |
| Respawn | last signature's station point, else `Vector3(0, 1.0, 2.5)` | `scripts/game_state.gd:238-244` |
| Station point | registered `pos + Vector3(0, 0.5, 1.2)` (Godot m) | `scripts/game_state.gd:234-235` |
| Burn | `strikes -= 1` only if `strikes > 0`; the canister burns either way | `scripts/game_state.gd:280-284` |
| Shortcut daily | `take = -1` | `scripts/game_state.gd:97` |
| Canister slots | 4 absolute positions in the TAPE LIBRARY: `(-3.5, 0.35, -14.0)`, `(2.5, 0.35, -18.5)`, `(4.0, 0.35, -13.0)`, `(-4.5, 0.35, -19.0)` | `scripts/dailies_manager.gd:5-8` |
| Slot rule | `SLOTS[id % 4] + (0.4 * (id / 4), 0, 0)` — integer division; the 5th canister sits 0.4 m +x of the 1st | `scripts/dailies_manager.gd:21-22` |
| Canister body | cylinder r 0.30 m, h 0.16 m; collision the same; tag `TAKE %d` 0.4 m above | `scripts/dailies_manager.gd:24-42` |
| Degausser | `(14.25, 0.55, -17.6)`, CLIMATE room; collision box 1.2 × 1.1 × 0.8 | `scripts/world_builder.gd:812-816` |
| Degausser hum | `ToneEmitter` 120 Hz + 240 Hz, noise 0.05, −16 dB | `scripts/world_builder.gd:848-852` |
| Dresser | `(-11.5, 0.28, -1.8)`, DORMS; 7 item boxes at `x = -0.66 + 0.22·i`, `y = 0.62` | `scripts/world_builder.gd:641-642`, `scripts/dresser.gd:17` |
| Casting sheet | `(-20.9, 1.5, -30.0)`, STUDIO A wall | `scripts/world_builder.gd:547` |
| Third-line widening | Rundown strike radius `2.6` when `strikes >= 3`, else `STRIKE_RADIUS` 2.2 — read at each ON AIR | `scripts/rundown.gd:150` |
| Strike pose | `_strike_pose_t = 0.9` s on both night strike paths | `scripts/rundown.gd:320`, `scripts/rundown.gd:222` |
| Retake card, capture | `0.7` + `0.9` + `14 × 0.06` + (`1.2` if an item was lost) + `0.9` s | `scripts/hud.gd:280-302` |
| Retake card, run death | `1.0` + `10 × 0.07` + `1.4` + `2.2` s, then the title | `scripts/hud.gd:316-328` |
| Timecode text | `"TC 00:03:%02d:00"`, counting 13→0 (capture) and 9→0 (run death) | `scripts/hud.gd:286`, `scripts/hud.gd:319` |
| Toast hold | 3.0 s for every `notify` text | `scripts/hud.gd:553` |

None of the presentation timings is a named constant, so none of them is
in `ue/Restoration/Data/Timings.csv` (which `tools/extract_data.py` builds
from `const` declarations only). They are literals in `hud.gd`. See O11.

---

## 2 · THE STRIKE — `GameState.strike(player)`, order of effects

`scripts/game_state.gd:482-506`. Called from exactly two places, both in
`scripts/rundown.gd`: the night hunt (`:321`, after the I02 raycast and the
`STRIKE seg … d=…` director line at `:316-319`) and the After-Fire
tally-cool path (`:286`, `STRIKE af tally-cool`). Nothing else strikes.

1. `if in_retake: return` — the re-entrancy guard (`:483`). `in_retake` is
   session-only, not saved (PORT-NOTES-STATE §2).
2. `in_retake = true` (`:485`).
3. `strikes += 1; take = strikes` (`:486-487`).
4. Item loss (`:488-491`): `lost = ITEM_ORDER[items_lost]` if fewer than 7
   are gone, then `items_lost += 1`. This runs BEFORE the full-sheet check,
   so the run-death strike also takes an item, silently (§4, O10).
5. `full = strikes >= 4 or mode == ONE_TAKE` (`:492`).
6. **Full sheet** (`:493-498`): `strikes = 0` → `save_log()` →
   `sheet_changed.emit(0)` → `run_ended.emit(take)` → return. No daily is
   minted. `in_retake` is left TRUE (O1). `dailies`, `carried_id`,
   `carried_take`, `items_lost` are untouched and were just saved.
7. **Survivable** (`:499-504`): `daily_seq += 1` → `dailies.append({id:
   daily_seq, take: take})` → `daily_added.emit(daily_seq, take)` →
   `save_log()` → `sheet_changed.emit(strikes)` →
   `captured.emit(take, full, lost, respawn_point())`.
   `full` is always `false` on this branch: the `sheet_full` parameter of
   `captured` is dead in practice (O2).
8. `if player: pass` (`:505-506`) — the comment says it: repositioning
   happens inside the retake presentation, not here.

The save is written on both branches before any presentation runs. What a
reload sees after a survivable capture: `strikes` up one, `items_lost` up
one, one more entry in `dailies`, `daily_seq` up one. Signatures, keys,
assets, read props: unchanged — the prototype loses nothing on a capture
except the item and the line (canon agrees: walkthrough "What Each Capture
Takes", `docs/canon/restoration-walkthrough-levels-endings.md:182-183`).

---

## 3 · THE RETAKE PRESENTATION — `hud._on_captured(take, sheet_full, lost_item, respawn)`

`scripts/hud.gd:273-306`, bound at `:28`. The whole thing is one coroutine
on the HUD; the world keeps ticking underneath (the Rundown, the ON AIR
clock, Harriet) — only the player is frozen and `in_retake` refuses a
second strike.

**The control** (`scenes/main.tscn:179-215`): `HUD/Retake`, full-rect,
`mouse_filter = 2` (ignore), hidden by default. Children, in order:
`Blackout` — a full-rect `ColorRect`, `Color(0.02, 0.018, 0.012, 1)`, fully
opaque (the card is on black, not over the world); `Line1` — full-rect
`Label`, centred both ways, `offset_top = -60`, font 40, colour
`(0.85, 0.93, 0.77)`; `Line2` — same, `offset_top = 40`, font 24, colour
`(0.58, 0.65, 0.5)`. Both labels get the HUD's outline pass (black 0.85,
size 6, `scripts/hud.gd:157-158`) and scale with `ui_scale`.

**Player lock**: `player.locked = true` (`scripts/hud.gd:276`). In
`scripts/player.gd` the flag short-circuits `_input` (`:31`, mouse look),
`_unhandled_input` (`:41` — so ESC/pause, `T`/TBC and `E`/interact are all
dead during the card) and `_physics_process` (`:52` — movement AND gravity
stop). Unlocked at `:305`.

**Frame by frame** (times are the `_wait()` arguments, `scripts/hud.gd:518-519`):

| # | Line1 | Line2 | Hold | Source |
|---|---|---|---|---|
| 1 | `◼ CAPTURED` | (empty) | 0.7 s | `:278-280`; GameText row 253 |
| 2 | `THE GLADHOUSE` | `SCENE 4 · TAKE %d` (take) | 0.9 s | `:281-283`; rows 254-255 |
| 3 | `◀◀ REWINDING` | `TC 00:03:13:00` … `TC 00:03:00:00`, 14 frames | 14 × 0.06 = 0.84 s | `:284-287`; row 256 |
| — | *player teleported to `respawn`, velocity zeroed* | | | `:288-290` |
| 4 | `ITEM MISSING` | `your %s is gone from the dresser. it will be in the footage.` (item lower-cased) | 1.2 s — ONLY if `lost_item != ""` | `:291-294`; rows 257-258 |
| 5a | `THE SHEET IS FULL` | `the rewind would not stop. (prototype: the sheet resets.)` | 1.4 s — never reached, see O2 | `:295-298`; rows 259-260 |
| 5b | `PRESENTATION KEPT` | `resume from your last signature.` | 0.9 s | `:299-302`; rows 261-262 |
| — | card hidden; `player.locked = false`; `GameState.in_retake = false` | | | `:303-306` |

Total: 4.54 s with an item lost (captures 1–7), 3.34 s once the dresser is
empty. The teleport lands at frame 3's end, under black, before the item
card — the player is already at the station when the card lifts.

Two things the card does NOT do, per source: it plays no sound (no `Sfx`
call anywhere in `_on_captured`) and it does not pass its strings through
`tr()` or `glyphs()` — unlike `_say()` at `scripts/hud.gd:331-334`, which
the endings use (O3). The SCENE number is the literal `4`; nothing varies
it (O4).

**What else fires on a survivable capture**, in emission order (§2 step 7):
`daily_added` → the canister appears in the stacks before the card is even
visible (`scripts/dailies_manager.gd:14`); `sheet_changed` → the HUD's
`SHEET · %d/4` label (`scripts/hud.gd:522-523`) and the dresser hides one
box (`scripts/dresser.gd:27`, `:31-33`). The Rundown holds its strike pose
for 0.9 s (`scripts/rundown.gd:386-388`) and then simply continues; it is
not relocated. Canon has nothing to say about where he is when the card
lifts (O12).

---

## 4 · THE RUN DEATH — `hud._on_run_ended(take)`

`scripts/hud.gd:309-328`, bound at `:29`. Fires from `strike()` on a full
sheet (or any strike in ONE TAKE), and from one more place: the After-Fire
crossing, `scripts/rundown.gd:220-224`, which toasts `A hand the size of a
door closes the distance. NEXT WEEK'S EPISODE.` (GameText row 573) and emits
`run_ended.emit(GameState.dailies.size())` — the argument is the dailies
count, not a take (O8).

| # | Line1 | Line2 | Hold | Source |
|---|---|---|---|---|
| 1 | `◼ CAPTURED` | `TAKE %d` | 1.0 s | `:314-316` |
| 2 | `◀◀ REWINDING` | `TC 00:03:09:00` … `TC 00:03:00:00`, 10 frames | 10 × 0.07 = 0.7 s | `:317-319` |
| 3 | `THE REWIND DOES NOT STOP` | (empty) | 1.4 s | `:321-323`; row 263 |
| 4 | `NEXT WEEK'S EPISODE` | `STARRING RITA IVORI` | 2.2 s | `:324-326`; rows 17, 264 |
| — | mouse released; `change_scene_to_file("res://scenes/title.tscn")` | | | `:327-328` |

Total 5.3 s. No teleport, no item card, no credits — `QA-08`
(`docs/production/restoration-qa-regression.md:14`) says exactly this:
"NEXT WEEK'S EPISODE · STARRING RITA IVORI, then straight to title, no
credits." The gap audit reaffirms the single card with no per-location
variants (`docs/production/restoration-gap-audit.md:13`).

Also on `run_ended`: achievement **A18 NEXT WEEK'S EPISODE** unlocks
(`scripts/achievements.gd:38`; `docs/production/restoration-achievements-design.md:28`).

**After the title.** `CONTINUE` (`scripts/title.gd:60-61`) just loads
`main.tscn`; `GameState` is an autoload and keeps its in-memory state,
which equals the save written in §2 step 6: `strikes = 0`, `items_lost`
one higher, the dailies still in the stacks, a carried canister still
carried. `in_retake` is still `true`, and nothing on the CONTINUE path
clears it — only `reset_new_game()` (`scripts/game_state.gd:726`) and the
end of a survivable card (`scripts/hud.gd:306`) do. See O1.

**ONE TAKE**: mode is set from the binder's form page, keys 1/2/3
(`scripts/hud.gd:211-221`), with the toasts `MODE · ONE TAKE` and `ONE TAKE ·
any capture ends the run. (Prototype honors sheet rules until run flow
exists.)` (`scripts/game_state.gd:295-298`). In ONE TAKE the first strike
runs §4 with `TAKE 1`.

---

## 5 · DAILIES — mint, spawn, pick, carry, burn

**Mint (two ways).**
- Every survivable strike: `{id: daily_seq, take: take}` (§2 step 7).
- The splicing block, once Vess's cut has been seen: `RejectedEdit._splice()`
  (`scripts/rejected_edit.gd:32-40`) toasts `You join the takes. The tape
  accepts the cut the way water accepts a stone.`, waits 2.6 s, calls
  `mint_shortcut_daily()` (`scripts/game_state.gd:95-99`: `daily_seq += 1`,
  append `{id, take: -1}`, `daily_added.emit(id, -1)`, save), toasts `DAILY
  MINTED · no capture, no bench, no twelve seconds. Cheaper than you
  thought.` (row 551), waits 2.4 s, toasts `The second take, in passing,
  again: THE SONG, HARRIET LEFT OF FRAME.` and sets `h2_pending`. A shortcut
  daily is a real daily in every later step, labelled `TAKE -1` (O7).

**Spawn.** `DailiesManager` is added at the world root by `_spawn_burn_loop()`
(`scripts/world_builder.gd:809-810`), so its SLOTS are world coordinates
inside TAPE LIBRARY (`Rooms.csv`: centre `(0, -16)`, 12 × 10). On `_ready`
it spawns one canister per entry in `GameState.dailies` and binds
`daily_added` to `_spawn` (`scripts/dailies_manager.gd:11-14`): dailies
survive reloads by construction, which is the burn-in rule
(`docs/canon/restoration-walkthrough-levels-endings.md:147`: "dailies
canisters already created" persist through retakes and reloads). Each
canister: `DailiesCanister` (an `Interactable`), cylinder r 0.3 h 0.16,
albedo `(0.55, 0.53, 0.5)`, a billboard `Label3D` `TAKE %d` (font 28,
`(0.76, 0.23, 0.18)`) at +0.4 m (`scripts/dailies_manager.gd:17-46`).

**Pick.** Prompt `DAILIES · SCENE 4 TAKE %d · pick up (E)` (row 79;
`scripts/dailies_canister.gd:9-10`). Interact (`:13-18`): if
`carried_id >= 0` → toast `Hands full. One canister at a time.` (row 80)
and nothing else; otherwise `pick_daily(daily_id, take)` and the node frees
itself. `pick_daily` (`scripts/game_state.gd:265-273`): remove the first
`dailies` entry with that id → `carried_id = id; carried_take = take` →
save → toast `CARRYING · SCENE 4 TAKE %d. The degausser is in the climate
room.` (row 159). One canister at a time is a hard rule; there is no drop.

**Carry.** `carried_id` / `carried_take` are v16 keys 15 and 16
(`ue/PORT-NOTES-STATE.md:62-72` table rows 15–16): the carried canister
survives a reload, a survivable capture (`strike()` never touches it) and a
run death; only `reset_new_game()` clears it (`scripts/game_state.gd:731-732`).
While carrying, the night objective reads `NIGHT · optional: burn your
dailies (library to climate room) · sleep when ready`
(`scripts/game_state.gd:696-698`, row 179 — shown when `dailies.size() > 0
or carried_id >= 0`), and the binder shows `DAILIES IN THE STACKS: %d ·
carrying: %s` with `TAKE %d` or `nothing` (`scripts/hud.gd:256`, row 243).

**Burn.** The degausser (`scripts/degausser.gd`) prompts `THE DEGAUSSER ·
burn TAKE %d (E)` when carrying, else `THE DEGAUSSER · humming · bring it a
daily` (`:6-9`; rows 96-97). Interact with nothing carried → toast `It hums,
felt-throated. It wants a canister.` (`:13-14`; row 98). Otherwise
`burn_daily()` (`scripts/game_state.gd:276-287`), in order:
1. `t = carried_take; carried_id = -1; carried_take = 0`
2. if `strikes > 0`: `strikes -= 1`, toast `BURNED · TAKE %d. Her name fades
   from the line. Its read on you resets.` (row 160); else toast `BURNED ·
   TAKE %d. The sheet was already clean. The canister burns anyway.` (row 161)
3. `save_log()` → `sheet_changed.emit(strikes)` → `daily_burned.emit()`

`daily_burned` has one listener: `CoverageDirector.reset_read`
(`scripts/coverage_director.gd:20`, `:86-95`) — zeroes the three read
counters and `_watched`, sets `coverage_label = "AUDIENCE"`, logs `READ
RESET · dailies burned` (row 64). It fires on BOTH branches of step 2 (O9).
This is the design doc's second function of the burn, verbatim: "erasing a
strike also resets its read on you" (`docs/canon/restoration-design-doc.md:249`).

Burning is not per-line: any canister, including a `TAKE -1` shortcut
daily, takes one strike off whatever the count is. The items on the
dresser never come back (canon: "permanently",
`docs/canon/restoration-walkthrough-levels-endings.md:183`; code: nothing
decrements `items_lost` except `reset_new_game`).

---

## 6 · THE PROPS THAT READ THE SHEET

| Surface | Reads | Text (verbatim) | Source |
|---|---|---|---|
| HUD `Sheet` label | `sheet_changed` + boot | `SHEET · %d/4` | `scripts/hud.gd:522-523`, `:66` |
| Binder page 1 | `strikes` | `CASTING SHEET: %d of 4 guest lines` | `scripts/hud.gd:253`; row 240 |
| Binder page 1 | `dailies`, `carried_*` | `DAILIES IN THE STACKS: %d · carrying: %s` | `scripts/hud.gd:256`; row 243 |
| Binder page 2 | mode | `2 LATE NIGHT · three lines per station, four sheet lines` / `3 ONE TAKE · any capture is final` / `1 MATINEE · unlimited paper, gentler sheet` | `scripts/hud.gd:230-232` (O6) |
| Casting sheet prop | `strikes` | `FINAL EPISODE · CAST: ALDER · BELL · PRICE · MERRICK · %d of 4 guest lines filled. The club dusts it.` | `scripts/casting_sheet_prop.gd:11-14`; row 57 |
| Dresser | `items_lost` via `sheet_changed` | boxes `i >= items_lost` visible; `Seven things, squared to the dresser's edge. Everything where you left it.` / `%d of seven remain. Gone: %s. They will be in the footage.` | `scripts/dresser.gd:27-33`, `:40-46`; rows 112-113 |
| Objective line (night) | `dailies`, `carried_id` | `NIGHT · optional: burn your dailies (library to climate room) · sleep when ready` | `scripts/game_state.gd:696-698`; row 179 |
| Rundown | `strikes >= 3` | strike radius 2.6; warn toast `It is not hurrying anymore.` instead of the segment line; ` savor` suffix on `WARN`/`STRIKE` director lines | `scripts/rundown.gd:150`, `:316-319`, `:326-330` |
| Achievements | `items_lost >= 7` | A19 EMPTY DRAWER | `scripts/achievements.gd:75`; `docs/production/restoration-achievements-design.md:29` |

The casting sheet is the physical death counter canon asked for
(`docs/canon/restoration-walkthrough-levels-endings.md:177`; room inventory
`docs/canon/restoration-room-inventory.md:100`, `:117`, `:194`). The
prototype's sheet text names the cast; the "AND INTRODUCING ______" lines
that canon describes are not in the prop's text (O13).

---

## 7 · SIGNALS AND LISTENERS (the retake slice of PORT-NOTES-STATE §3)

| Signal | Params | Emitted by | Listeners | UE (`RestorationState.h`) |
|---|---|---|---|---|
| `captured` | `take:int, sheet_full:bool, lost_item:String, respawn:Vector3` | `strike` (survivable only) | `hud._on_captured` | **not declared** |
| `run_ended` | `take:int` | `strike` (full), `rundown` crossing (`:224`) | `hud._on_run_ended`, `achievements` (A18) | `FOnRunEnded` present (`:113`, `:195`) |
| `daily_added` | `id:int, take:int` | `strike`, `mint_shortcut_daily` | `dailies_manager._spawn` | **not declared** |
| `daily_burned` | — | `burn_daily` | `coverage_director.reset_read` | **not declared** |
| `sheet_changed` | `count:int` | `strike` (both branches), `burn_daily` | `hud._on_sheet`, `dresser` | `FOnSheetChanged` present (`:114`, `:196`) |
| `notify` | `text:String` | every toast above | `hud._on_notify` (3.0 s) | see PORT-NOTES-STATE |

Delegate signatures for the three missing ones, same names:
`FOnCaptured(int32 Take, bool bSheetFull, const FString& LostItem, const FVector& Respawn)`,
`FOnDailyAdded(int32 Id, int32 Take)`, `FOnDailyBurned()`.

---

## 8 · SAVE KEYS THIS SLICE TOUCHES (v16, `ue/PORT-NOTES-STATE.md:45`)

| Key | Row | Written by | Survives capture | Survives run death | Cleared by new game |
|---|---|---|---|---|---|
| `strikes` | 8 | `strike` (+1, or →0), `burn_daily` (−1) | +1 | reset to 0 | yes |
| `items_lost` | 9 | `strike` (+1, cap 7) | +1 | +1 (silent) | yes |
| `dailies` | 13 | `strike`, `mint_shortcut_daily` (append), `pick_daily` (remove) | +1 entry | unchanged | yes |
| `daily_seq` | 14 | `strike`, `mint_shortcut_daily` | +1 | unchanged | yes |
| `carried_id` | 15 | `pick_daily`, `burn_daily` | unchanged | unchanged | yes (−1) |
| `carried_take` | 16 | `pick_daily`, `burn_daily` | unchanged | unchanged | yes (0) |
| `signatures` | 6 | — (read by `respawn_point`) | unchanged | unchanged | yes |

`in_retake` is not saved (`ue/PORT-NOTES-STATE.md:130` section). New Game+
relic: `reset_new_game()` keeps `ITEM_ORDER[items_lost - 1]` as `ng_relic`
when `finale_done and items_lost > 0` (`scripts/game_state.gd:716-717`) —
the last item a capture took becomes the relic; the loupe only if all seven
went.

---

## 9 · CANON CROSS-CHECK

Agrees with code:
- Captures as retakes, "From the top", never gore — `docs/canon/restoration-design-doc.md:114`. Code: text card, no gore, no sting, no `Sfx`.
- "From the top means the scene, never the night" — `docs/canon/restoration-walkthrough-levels-endings.md:174`. Code: the clock, the day and the schedule are untouched by `strike()`; only the player moves.
- One item per capture, the loupe last, permanent — walkthrough `:183`; `QA-07` (`docs/production/restoration-qa-regression.md:13`); playtest P3 (`docs/production/restoration-playtest-protocol.md:39`: "watch first, loupe last, respawn at last signed station"). Code: `ITEM_ORDER`, §2 step 4, §3 frame 4.
- Four survivable captures on Late Night, zero in One Take — walkthrough `:177`. Code: `strikes >= 4 or ONE_TAKE`.
- A canister per capture, labelled scene/take, in the library stacks; degauss in the climate room; burning fades a line and resets the director's read — walkthrough `:180`; design doc `:249`; room inventory `:100`, `:117`. Code: §5.
- Dailies survive retakes and reloads — walkthrough `:147`. Code: `dailies` is saved and re-spawned on `_ready`.
- Run death: the single card, straight to title, no credits — `QA-08`; gap audit ruling 6. Code: §4.
- Every death has a signature (LAW 7, `docs/packet/portbrief/THE-LAWS.md:8`): Rita's captures are takes, not casualties; `mark_casualty` is never called by this slice. The retake card names no cause; the sheet counts. Canon does not ask the card to name the cause.
- LAW 5 (`THE-LAWS.md:6`): no retake or dailies string names Chum. Verified by grep in the PR.

Where canon says more than the code does, or differently — every one is an
OPEN in §11, not a ruling here:
- The presentation canon describes (walkthrough `:174`): bars, head-switch noise, playback of Rita's final seconds from an angle no camera occupied, rewind squeal, slate `SCENE n, TAKE k`, the Floor Manager's count, fade up at the slate point. Code has: a black card with two labels and a text timecode (O4).
- The run death canon describes (walkthrough `:186`): the rewind past the slate, past Rita's arrival, next week's episode with Rita on set waving, the sign-off card, then "the binder opens itself to the last signed log page: continue from log. True game over; everything unsaved is gone." Code: four text cards, then the title screen; the run-death save is written with `strikes = 0` (O5).
- Matinee "seven survivable captures" (walkthrough `:177`, "Defaults, tunable") — code caps every non-ONE-TAKE mode at 4 (O6).

---

## 10 · UE DELTAS — current C++ vs this slice (the checklist)

`ue/Restoration/Source/Restoration/RestorationState.cpp:159-193` already
ports `Strike()` with the 7-item clamp, `bFull`, and the full branch's
save → `OnSheetChanged` → `OnRunEnded`. Against §2–§7 it still lacks:

- [ ] `Strike()` survivable branch: compute `Lost` (the C++ increments
      `ItemsLost` but never reads `ITEM_ORDER[ItemsLost]`), `SaveToSlot()`
      after the append (Godot saves; C++ does not), then broadcast
      `OnDailyAdded(DailySeq, Take)` and
      `OnCaptured(Take, false, Lost, RespawnPoint())` in that order after
      `OnSheetChanged`. `RespawnPoint()` / `RegisterStation()` exist
      (`RestorationState.h:210-211`; the offset is `(0, 1.2 m, 0.5 m)` in
      UE axes, `RestorationState.cpp:90` — that is Godot's `(0, 0.5, 1.2)`
      with y↔z swapped, correct).
- [ ] `Strike()` full branch: the C++ sets `bInRetake = false`
      (`RestorationState.cpp:181`); Godot leaves it true (§2 step 6, O1).
      This is a deliberate-looking divergence from the reference; it needs
      the Mac lane's ruling recorded, not silently kept.
- [ ] `ITEM_ORDER` as a static array on the subsystem (the C++ has only
      the comment and the number 7).
- [ ] Declare `FOnCaptured`, `FOnDailyAdded`, `FOnDailyBurned` (§7).
- [ ] Port `PickDaily(Id, Take)`, `BurnDaily()`, `MintShortcutDaily()`
      with the exact order of effects and toasts in §5 (toast text through
      the string table + glyphs, per PORT-NOTES-STATE §6).
- [ ] `bInRetake` must also be cleared where the UMG card ends (§3 last
      row) — in Godot the HUD owns that write, not `strike()`.
- [ ] The retake widget: `Blackout` opaque `(0.02, 0.018, 0.012)`; two
      centred text blocks at −60 / +40 px, 40 / 24 px, colours §3; the
      frame table of §3 and §4 with the exact holds; the teleport between
      frames 3 and 4; player input, look, movement AND gravity frozen for
      the card's duration; the run-death card returns to the title map with
      the cursor shown.
- [ ] Actors from data: `DailiesManager` (4 slots + integer-division
      overflow rule, spawn-on-load + `OnDailyAdded`), `DailiesCanister`
      (prompt/interact of §5), `Degausser` at `(14.25, 0.55, -17.6)` with
      the 120/240 Hz hum, `Dresser` with 7 hideable items bound to
      `OnSheetChanged`, `CastingSheetProp`. Their positions belong in the
      Landmarks table (C7) — this file only records them.
- [ ] `ARundown` (`Rundown.cpp:394`) adds `StrikeCooldown = 3.0f` after a
      strike; `rundown.gd` has no cooldown — Godot relies on `in_retake`
      and the 0.9 s pose. Drift for C17's audit; noted here because it
      interacts with the guard.
- [ ] `ARundown` crossing path must emit `OnRunEnded` with the dailies
      count exactly as `rundown.gd:224` does, until O8 is ruled.
- [ ] Coverage director's `reset_read` on `OnDailyBurned` — the director
      does not exist in C++ yet (C8's finding); when it lands, bind it.
- [ ] Achievements: `OnRunEnded → A18` and `items_lost >= 7 → A19` per
      `docs/production/UE-ACCESS-SPEC-LAW9.md:301`.

---

## 11 · OPEN (canon silent or contradicted; the lane does not rule)

- **O1 · `in_retake` after a run death.** Godot: `strike()` sets it, the
  full branch returns without clearing it, `_on_run_ended` changes scene
  without clearing it, and CONTINUE reloads `main.tscn` with the autoload
  intact — so after one run death and CONTINUE, `strike()` returns at its
  first line for the rest of the process (`scripts/game_state.gd:483`,
  `:493-498`; `scripts/hud.gd:309-328`; `scripts/title.gd:60-61`). The
  C++ clears it (`RestorationState.cpp:181`). PORT-BRIEF says the code is
  the intent; the invariant suite (`docs/production/restoration-invariant-suite.md:5`,
  I01 warn-precedes-strike) assumes strikes keep landing. Ruling needed:
  port the clear, and say so in the ledger.
- **O2 · The `THE SHEET IS FULL` card is unreachable.** `captured` is only
  emitted on the survivable branch with `full == false`
  (`scripts/game_state.gd:492-504`). GameText rows 259-260 are dead text.
  Drop the branch in UE, or keep the parameter for parity? Canon does not
  describe a "sheet full but survived" card at all.
- **O3 · Retake card strings bypass `tr()`.** `_on_captured` and
  `_on_run_ended` assign literals (`scripts/hud.gd:278-326`) while `_say`
  wraps `tr()` + `glyphs()` (`:331-334`). The strings are in the table
  (rows 253-264) so the extraction commit found them, but the code path
  does not use them. Localization plan L01 names "the HUD say pair" as a
  chokepoint (`docs/production/restoration-localization-plan.md:11`); the
  retake card is not on it. Route through the table in UE (system text,
  `:8`) — or rule that the card is world text (a slate) and stays English.
- **O4 · The AAA presentation.** Canon (walkthrough `:174`) specifies bars,
  head-switch noise, an impossible-angle playback, rewind squeal, a slate
  `SCENE n, TAKE k`, the Floor Manager's count and a fade up at the slate.
  The prototype is a text card with `SCENE 4` hard-coded and no audio. The
  audio bible has no retake entry (grep `rewind|retake` in
  `docs/production/restoration-audio-bible.md`: none). Numbers in §3 are
  the prototype's; the built presentation needs its own spec (Phase 4/5),
  and `n` needs a source — canon never says what scene a capture is.
- **O5 · Run-death landing and "everything unsaved is gone".** Canon: the
  binder opens to the last signed log page, continue from log; true game
  over; everything unsaved is gone (walkthrough `:186`). Code: title
  screen, and since the prototype saves on every mutation (PORT-NOTES-STATE
  §1) the run-death branch itself writes `strikes = 0` and the extra
  `items_lost`. `QA-08` matches the code. Whether "continue from log"
  means the title's CONTINUE button (it does today) or an in-fiction binder
  page is OPEN; whether a run death should revert unsaved state (there is
  none) is moot until save-on-sign exists, which canon calls for at
  walkthrough `:141-143` and the code does not do.
- **O6 · Matinee cap.** Canon: seven survivable captures on Matinee
  ("Defaults, tunable", walkthrough `:177`); binder form: "gentler sheet"
  (`scripts/hud.gd:230`). Code: 4 in every mode but ONE TAKE
  (`scripts/game_state.gd:492`). The HUD label is `SHEET · %d/4` regardless.
- **O7 · `TAKE -1`.** A shortcut daily carries `take = -1` and every surface
  prints it: canister tag `TAKE -1`, prompt `SCENE 4 TAKE -1`, carry and
  burn toasts. Canon names the second take `THE SONG, HARRIET LEFT OF
  FRAME` (`scripts/rejected_edit.gd:17`) but gives the canister no label.
- **O8 · Crossing `run_ended` argument.** `rundown.gd:224` passes
  `dailies.size()`; the card prints it as `TAKE %d`. A player with two
  canisters in the stacks dies "TAKE 2" whatever their strike count. Canon
  is silent on what the crossing card says.
- **O9 · Burn with a clean sheet still resets the read.** `daily_burned`
  fires on both branches (`scripts/game_state.gd:287`) though only the
  first toast promises it. Code is the intent; recorded so the port does
  not "fix" it.
- **O10 · The run-death strike takes an item silently.** `items_lost`
  increments before the full check (`scripts/game_state.gd:489-491`) and
  no card shows it. A19 can therefore be reached partly through run
  deaths. Code is the intent; recorded.
- **O11 · Timings are literals.** None of §1's presentation timings is a
  `const`, so `Timings.csv` cannot carry them. Promote to named constants
  (and rows) or leave as widget-authored values: OPEN.
- **O12 · The Rundown during the card.** After `strike()` the Rundown
  holds its pose 0.9 s and keeps hunting from where it stands
  (`scripts/rundown.gd:320-322`, `:386-389`); the player reappears at the
  station under black. Canon says nothing about his position when the card
  lifts, or about the card's effect on the schedule clock (it has none).
- **O13 · The sheet's text.** Canon's sheet has typed lines, LELAND, blank
  lines ending "AND INTRODUCING ______" and Rita's name typed per capture
  (walkthrough `:177`). The prop's toast names ALDER · BELL · PRICE ·
  MERRICK and a count. Which names are canon for the three Playmates is
  for the cast dossier (C2) and the prop manifest (C6); the realism-bar
  note that the canister, degausser and dresser are naked primitives
  (r 0.3 m × 0.16 m cylinder, boxes, a torus) is for C6 — real film-can
  dimensions are not in canon.
