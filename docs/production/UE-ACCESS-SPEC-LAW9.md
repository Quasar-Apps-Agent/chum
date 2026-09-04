# UE ACCESS SPEC · LAW 9 — "ACCESS IS CANON"
Implementation spec for Unreal Engine 5.8, written against the Godot reference build (the code is the intent: `docs/packet/portbrief/PORT-BRIEF.md` §preamble). Prepared for the 0.10 gate ruling (`ue/GATE-0.10.md` §2 row 9 and §4 item 4). This document proposes; it edits no tracker.

Status of the evidence: every rule below is cited to a document and section, or to a Godot script and line. Where canon is silent the word is **OPEN** and nothing is invented. Every file path is repo-relative to `/Users/christianabowen/Desktop/restoration-godot 3/`.

---

## 0 · THE LAW, VERBATIM, AND ITS NEIGHBORS

`docs/packet/portbrief/THE-LAWS.md` line 10:

> 9. ACCESS IS CANON. The booth, captions, assist, remap, pause, and the deferral rule ship in every build of every engine.

Laws that touch the same interface surface:

- Law 8 (`THE-LAWS.md` line 9): "THE INTERFACE MAY LIE EXACTLY ONCE, where the design doc says it does, and nowhere else." The design doc places that one lie post-credits of THE NEW PRODUCER (`docs/canon/restoration-design-doc.md` §Casting drift in the interface; `docs/canon/restoration-walkthrough-levels-endings.md` §2. THE NEW PRODUCER). Consequence for this spec: the booth, the caption strip, the intermission menu and every toast are TRUE surfaces. Binder "drift" as the Producer Track rises is dressing, "not the interface lying" (design doc, same section). No access surface may ever misreport a setting, a binding, or a clock.
- Law 10 (`THE-LAWS.md` line 11): the tally countdown "is visible and means both progress and expiry; the cool is 2.0 s and announced." The visible countdown is HUD text and therefore subject to UI TEXT SIZE and the HUD outline rule (§4 below). The announcement of the cool is a toast; toasts are glyph-substituted (§6).

What the six words mean, in canon and in code (each expanded in its own section):

| Obligation | Canon home | Reference implementation |
|---|---|---|
| THE BOOTH | `docs/canon/restoration-controls-map.md` §PC ("OPTIONS BOOTH O"); `docs/canon/restoration-accessibility-matrix.md` §COGNITIVE AND PACING ("The booth opens BEFORE first play"); `PORT-BRIEF.md` §3 ("the booth's every control is enumerated in options_panel.gd") | `scripts/options_panel.gd` (whole file), `scripts/title.gd` lines 48–51 |
| CAPTIONS | `docs/canon/restoration-design-doc.md` §Captions and Accessibility; `docs/canon/restoration-accessibility-matrix.md` §HEARING; `docs/canon/restoration-after-fire-chum.md` §SOUND AND CAPTION LAW | `scripts/game_state.gd` lines 395–402, `scripts/hud.gd` lines 36–46 and 179–186, 15 call sites |
| ASSIST | `docs/canon/restoration-accessibility-matrix.md` §COGNITIVE AND PACING; `docs/production/restoration-accessibility-conformance-pass.md` §3 R5 and addendum c031; `docs/production/restoration-gap-audit.md` §5 | `scripts/screening_event.gd` lines 82, 90; `scripts/floor_manager.gd` line 65; `scripts/live_production.gd` line 350 |
| REMAP | `docs/canon/restoration-controls-map.md` §PC and §HOLD VERSUS TOGGLE; `docs/canon/restoration-accessibility-matrix.md` §MOTOR; `docs/production/restoration-localization-plan.md` L05 + addendum (033) | `scripts/game_state.gd` lines 125, 193–200, 305, 370–392; `scripts/options_panel.gd` lines 105–134 |
| PAUSE | `docs/production/restoration-accessibility-conformance-pass.md` addendum c034; `docs/production/restoration-qa-regression.md` QA-32; `docs/canon/restoration-accessibility-matrix.md` §COGNITIVE AND PACING ("INTERMISSION pauses everything honestly") | `scripts/hud.gd` lines 87–141 and 189–193; `scripts/player.gd` lines 41–44 |
| THE DEFERRAL RULE | `docs/production/restoration-achievements-design.md` §DOCTRINE 1; `PORT-BRIEF.md` §5 ("the deferral rule and meta-silence live in the design doc and are not optional") | `scripts/achievements.gd` (whole file), `scripts/title.gd` lines 29–39 |

A note on the phrase "deferral rule": in canon it is the ACHIEVEMENT deferral rule (unlocks queue and surface only at two gates). No canon document defines a rule for deferring a scare or a beat under an assist setting. If the owner intended that second meaning, it is **OPEN** (see §10).

---

## 1 · SHARED FOUNDATION (what every section below leans on)

### 1.1 `URestorationSettings` — the settings store
- Class: `URestorationSettings : public UGameInstanceSubsystem` in `ue/Restoration/Source/Restoration/RestorationSettings.h/.cpp`. Persisted through `URestorationSettingsSave : public USaveGame` in slot `"settings"`, user index 0. PORT-NOTES offered either a `UGameUserSettings` subclass or a second SaveGame slot (`ue/PORT-NOTES-STATE.md` §4, "Keep the keys."). The SaveGame slot is chosen because the v16 round-trip harness that proved `URestorationSaveGame` (PROGRESS 0.8b-3) tests it for free, headless.
- Settings are NOT part of the log: Godot keeps `user://settings.cfg` apart from `user://restoration.log` so NEW GAME never touches them (`scripts/options_panel.gd` lines 8–10; QA-16). `URestorationState::SaveToSlot/LoadFromSlot` and `ResetNewGame` must not read or write the `"settings"` slot. `user://` becomes ProjectSavedDir (`docs/packet/portbrief/UE5-MIGRATION-MAP.md` §WHAT DOES NOT PORT).
- Schema (property names carry the Godot section and key so the mapping is greppable):

| Godot section.key | UE property | Type | Default | Clamp | Applied to |
|---|---|---|---|---|---|
| `audio.master` | `Audio_Master` | float linear | 1.0 | 0..1 (slider range; load clamps to `max(v, 0.001)` before dB) | master SoundClass / Submix volume (`linear_to_db(maxf(vol, 0.001))`, `game_state.gd` 312–313) |
| `input.sensitivity` | `Input_Sensitivity` | float | 1.0 | **0.2..3.0 on load** (`game_state.gd` 314) and again at use (`player.gd` 34) | look multiplier over `MOUSE_SENS = 0.0022` (`Data/Timings.csv`) |
| `access.ui_scale` | `Access_UiScale` | float | 1.0 | **0.8..1.6 on set** (`game_state.gd` 360); NOT clamped on load in Godot (line 315) — UE clamps on load too, a deliberate hardening, not a semantic change | every HUD text block (§4.2) |
| `access.captions` | `Access_Captions` | bool | false | — | `ShowCaption` gate (§4) |
| `access.assist` | `Access_Assist` | bool | false | — | the three mercies (§5) |
| `keys.<action>` | `Keys` : `TMap<FName, FName>` action → FKey name | 5 entries max | absent = default binding | rebind refuses a key bound to another of the five (§6) | `IMC_Remap` (§6.2) |
| `video.fullscreen` | `Video_Fullscreen` | bool | false | skipped when headless (`game_state.gd` 322) | `UGameUserSettings::SetFullscreenMode` + `ApplySettings` |

Deviation, disclosed: Godot stores a physical keycode integer per action; UE stores the `FKey` name string. The section/key names survive; the value type does not (there is no physical keycode in UE's key model). `docs/packet/portbrief/UE5-MIGRATION-MAP.md` §WHAT MUST NOT CHANGE protects the SAVE's semantic fields, not the settings file's encoding; this is within bounds but is listed in §10 for the owner to acknowledge.

- Not settings (do not move them): `TBC` and `PHOTOSENSITIVITY-SAFE` are surfaced in the booth but persist in the SAVE (`_save_dict` keys 3 `tbc` and 41 `photo_safe`; `ue/PORT-NOTES-STATE.md` §1; `URestorationSaveGame::Tbc`, `::PhotoSafe` already exist). The booth reads and writes them through `URestorationState::SetTbc / SetPhotoSafe`.
- First-run detection: Godot opens the first-run booth when `settings.cfg` does not exist (`scripts/title.gd` line 48) and writes the file the moment the first-run booth constructs (`scripts/options_panel.gd` lines 26–27) so it never re-prompts (QA-01). UE: `UGameplayStatics::DoesSaveGameExist(TEXT("settings"), 0)`; `URestorationSettings::bFirstRun` is true iff the slot is absent at `Initialize`.
- Delegates (names per `ue/PORT-NOTES-STATE.md` §3, which lists `ui_scale_changed`, `caption`, `pause_requested` as subsystem signals): `FOnUiScaleChanged(float)`, `FOnCaption(const FText&)`, `FOnPauseRequested()`, plus `FOnNotify(const FText&)` for toasts (`notify`). They live on the subsystem "so the HUD has one place to bind" (PORT-NOTES §3 closing paragraph).

### 1.2 Text pipeline — `RestorationText.h`
- `Data/GameText.csv` (714 keys, `Key,SourceString`, source string is the key) imports as a StringTable `/Game/Data/ST_GameText` (`PORT-BRIEF.md` §3; PROGRESS 0.5).
- `FText URestorationText::Tr(const FString& Key)` = `FText::FromStringTable(TEXT("/Game/Data/ST_GameText"), Key)`, falling back to `FText::FromString(Key)` when the key is absent (Godot's `tr()` "falls back to its input", `docs/production/restoration-localization-plan.md` §addendum L01).
- `FString URestorationText::Glyphs(const FString&)` = `game_state.gd` lines 193–200: for each token in `GLYPH_MAP = {E→interact, SPACE→respond, Q→improvise, T→toggle_tbc, M→map}` (line 125) replace whole-word matches (`\bTOKEN\b`, `FRegexPattern`) with the CURRENT bound key's display name upper-cased (`key_name`, lines 388–392; returns `"?"` when unbound).
- Order of operations, verbatim from the chokepoints: toast = `glyphs(tr(text))` (`game_state.gd` 212); prompt = `glyphs(tr(prompt))` (`hud.gd` 529); say pair = `glyphs(tr(a))` (`hud.gd` 332–333); capture status = `glyphs(text)` with no `tr` (`game_state.gd` 219–221); caption = `tr(text)` with NO glyph pass (`game_state.gd` 402). Translators keep the five tokens verbatim (`restoration-localization-plan.md` L05 addendum 033).
- Chokepoints in UE: `URestorationState::Toast`, `::SetCaptureStatus`, `::ShowCaption`, `URestorationHUDWidget::SetPrompt`, `::Say`. Nothing else composes player-facing strings.

### 1.3 Enhanced Input, enabled for real
`Config/DefaultInput.ini` already names `EnhancedPlayerInput` / `EnhancedInputComponent` (lines 97–98) but `Restoration.Build.cs` does not link `EnhancedInput` and `ARitaCharacter::SetupPlayerInputComponent` binds legacy axis/action names (`RitaCharacter.cpp` lines 52–57). The migration map's INPUT row is unambiguous: "Enhanced Input mapping context, one to one" (`UE5-MIGRATION-MAP.md` §SYSTEM MAP · INPUT). §6 depends on this; it is the first unit of work.

---

## 2 · BOOTH

### 2.1 Canon
- Name and key: "OPTIONS BOOTH O · PAUSE ESC" (`docs/canon/restoration-controls-map.md` §PC line 5). Controller: "BOOTH menu long-press · PAUSE start" (§CONTROLLER line 10).
- Opens before first play: "The booth opens BEFORE first play (shipped) so nobody meets the dark unconfigured." (`docs/canon/restoration-accessibility-matrix.md` §COGNITIVE AND PACING). Remediation R7 (`restoration-accessibility-conformance-pass.md` §3) and QA-01.
- Content enumerated in code, by port-brief mandate (`PORT-BRIEF.md` §3): `scripts/options_panel.gd`. The docstring is the canon one-liner: "The booth: master volume, mouse feel, the window, and the two access switches." (lines 8–10).
- Every hold has a toggle equivalent in the booth, durations preserved (`restoration-controls-map.md` §HOLD VERSUS TOGGLE) — a UE5 TARGET, not shipped in Godot (no hold-to-toggle control exists in `options_panel.gd`; `docs/canon/restoration-accessibility-matrix.md` §MOTOR lists HOLD-TO-TOGGLE as the full target).
- Diegesis: the design doc places settings inside the binder's "Presentation" form (`restoration-design-doc.md` §Philosophy: "Pause, settings, saves, and the journal live inside a physical ring binder"; §Captions and Accessibility: "subtitle size and background opacity controls on the binder's 'Presentation' form"). The shipped booth is a centered overlay panel. Per `PORT-BRIEF.md` (code is the intent) the CONTROL SET is canon; the letterhead skin is Phase 5 dressing. Listed in §10.
- Persistence: QA-16 "every slider and check persists across relaunch; NEW GAME leaves settings intact."
- Focus: an explicit phosphor focus ring on every button, check and slider (conformance addendum c031, R4; QA-02 for the title). `_focusize` (`options_panel.gd` 137–143): transparent fill, border `(0.85, 0.93, 0.77)`, width 2, radius 2.

### 2.2 UE plan
- Class: `URestorationBoothWidget : public UUserWidget` (C++ base; `WBP_Booth` for layout only). Constructed by `URestorationSettings::OpenBooth(bool bFirstRun)` so both the title and the intermission menu open the same object.
- Layout from `options_panel.gd`, in order (row = label 240 px wide, dim green `(0.58, 0.65, 0.5)`, control 220 px slider or check; panel min width 520; separation 14; dim scrim `(0,0,0,0.65)`):
  1. Title `OPTIONS · THE BOOTH` (phosphor `(0.85,0.93,0.77)`, size 22).
  2. First-run only: `BEFORE THE SHOW · set your hands and eyes. O reopens this anytime.` (amber `(0.89,0.64,0.24)`, size 14).
  3. `MASTER VOLUME` slider 0..1 step 0.01.
  4. `MOUSE SENSITIVITY` slider 0.2..3.0 step 0.01.
  5. `FULLSCREEN` check.
  6. `TBC · steadier tape (T)` check → `URestorationState::SetTbc`.
  7. `PHOTOSENSITIVITY-SAFE (P)` check → `URestorationState::SetPhotoSafe` (its toast `PHOTOSENSITIVITY-SAFE MODE · %s` is in the CSV, key 168).
  8. `UI TEXT SIZE` slider 0.8..1.6 step 0.01 → `SetUiScale` (live-applied).
  9. `CAPTIONS · significant sounds` check.
  10. `ASSIST · wider beats, slower clocks, hold E to be still` check.
  11. `REMAP · click, then press a key` header, then five rows (§6).
  12. `CLOSE (O)` flat button, size 18, receives initial focus (`options_panel.gd` line 83).
  Every label is `Tr(key)`; items 6, 10 and 12 pass through `Glyphs` so a remapped T/E shows the bound key (they contain tokens). Godot did not glyph the booth labels; UE should, since "every prompt renders the player's ACTUAL binding" (`restoration-controls-map.md` §Principle). Minor and disclosed.
- Every change writes immediately (`GameState.save_settings()` per control, `options_panel.gd` 44, 49, 56, 63, 65, 67). No Apply button exists; do not add one.
- Closes on the `Options` action or Escape (`options_panel.gd` 161–166), unless a remap capture is pending (line 162–163).
- First run: `ARestorationTitle` (title widget host) checks `Settings->bFirstRun` and opens the booth over the title before focusing NEW GAME (`title.gd` 48–52); the booth writes the slot on construction so a crash before CLOSE still counts as done (`options_panel.gd` 26–27).
- Focus ring: one `FButtonStyle` / `FSliderStyle` / `FCheckBoxStyle` with the phosphor 2 px border in a `URestorationSlateStyle` set; keyboard traversal must reach every control (conformance F06/F07; device pass §5).
- Hold-to-toggle (UE target only): a `HOLD INPUTS · toggle instead of hold` check row, `Access_HoldToggle` bool, default false, consumed by the bench capture hold, the fader hold and the stillness checks; "toggles preserve the same durations so the contract's arithmetic never changes" (`restoration-controls-map.md` §HOLD VERSUS TOGGLE). Data key and default are proposed here; the label text is **OPEN** (no canon string exists) — see §10.
- Matrix items beyond the shipped booth (FLICKER AND GRAIN REDUCTION slider, VISUAL BELL, MONO DOWNMIX, TOAST DWELL slider, STICK SENSITIVITY / INVERT, GYRO; `restoration-accessibility-matrix.md` §VISION, §HEARING, §MOTOR, §COGNITIVE) are the "full target" the matrix names for UE5; none has a canon label string, default or range. Each is **OPEN** on data and is listed in §10 as a scope question, not silently dropped.

### 2.3 Data
- `URestorationSettingsSave` per §1.1; slot `"settings"`.
- Strings: 13 booth keys are in `Data/GameText.csv` (rows 514–523 plus `PRESS A KEY`, `CLOSE (O)`, `KEY IN USE · that key already answers to %s.`). **`FULLSCREEN` is absent from the CSV** (grep count 0) although `options_panel.gd` line 51 wraps it in `tr()`. Add it in the next `tools/extract_data.py` run; the coverage test in §2.4 fails until it exists.

### 2.4 Acceptance
- `Restoration.Access.Settings.RoundTrip` (automation test, headless): set every property to a non-default (Audio 0.37, Sensitivity 2.6, UiScale 1.45, Captions true, Assist true, Fullscreen false, Keys {respond→F}); `Save`; construct a fresh subsystem; `Load`; assert equality on all seven. Then set Sensitivity 9.0 and UiScale 0.1 through the setters and assert 3.0 and 0.8 (clamps).
- `Restoration.Access.Settings.NewGameLeavesSettings` (QA-16 second clause): load settings, call `URestorationState::ResetNewGame` and `SaveToSlot`, reload settings, assert unchanged.
- `Restoration.Access.Booth.FirstRun` (QA-01): delete slot; boot title in simulate; assert `bFirstRun == true`, the booth widget is live with the BEFORE THE SHOW row visible, and the `"settings"` slot exists BEFORE close; relaunch title; assert no booth.
- `Restoration.Access.Text.BoothKeys`: every literal in the booth widget's label list resolves in `ST_GameText` (fails today on `FULLSCREEN`).
- Visual (device pass, `restoration-accessibility-conformance-pass.md` §5): keyboard-only traversal of the booth, focus ring photographed, sliders operable with arrow keys.

### 2.5 Schedule
- BUILD-ORDER puts "booth complete" in P6 (`BUILD-ORDER.md` P6). PROGRESS.md's equivalent is **5.2 UI/menus/accessibility**. Proposal: split a new box **5.2a THE BOOTH** (settings subsystem + widget + first run) and pull §1.1 (`URestorationSettings`) forward into **0.8b-5** as a sub-box, because the screening/assist half of 0.8b-5 cannot read `assist_on` without it. See §9.

---

## 3 · CAPTIONS

### 3.1 Canon
- Design intent: "Captions styled as period television captions with speaker tags and, critically, directional sound captions ("[footsteps, upholstered, left]"), because audio carries threat information and deaf players get the full fear channel, not a transcript." (`docs/canon/restoration-design-doc.md` §Captions and Accessibility).
- Shipped scope and UE5 extension: "CAPTIONS for speech and for meaningful sound events with source tags (shipped: THE BELL, doors, the pen tick), extended in UE5 with left and right directionality tags and a proximity weight so the occlusion presence (S22) has a visual twin. VISUAL BELL option ... The audio law survives captioning: band-limited sources caption in brackets styled as broadcast, full-range sources caption plain, so even the reading ear learns MEMORY versus PRESENT." (`docs/canon/restoration-accessibility-matrix.md` §HEARING).
- Law 5 crosses here: "The bell rings once, at the finale beat, and its caption says so." (`THE-LAWS.md` line 6). The shipped caption is `[THE BELL RINGS · once]` (`scripts/sfx.gd` line 17). The AF bell is silent and "the caption for that is nothing" (`docs/canon/restoration-after-fire-chum.md` §SOUND AND CAPTION LAW).
- After-fire captions are canon text: `[WEIGHTED FOOTSTEP]` "distance-scaled" and `[THE JAW WORKS ITS LEVER]` (`restoration-after-fire-chum.md` §SOUND AND CAPTION LAW); the fold is "announced by caption" (same doc §ELEVEN FEET); the lever's caption "stays [THE JAW WORKS ITS LEVER]" (`docs/production/restoration-audio-bible.md` S25). Code ships the lever and the fold captions (`rundown.gd` 267, 343) but NOT `[WEIGHTED FOOTSTEP]` — a canon-vs-code gap; per PORT-BRIEF the code is the intent, but the after-fire doc is also canon. Listed in §10.
- Toggle and persistence: "toggleable in the booth, persisted" (conformance addendum c029, R2). QA-05: "pen-tick caption appears when captions on." QA-37 and QA-38 name the fold caption and `[NO ECHO]`.
- Localization: "the accessibility caption set localizes with system text at full parity" (`restoration-localization-plan.md` §rollout paragraph); captions are one of the four `tr()` chokepoints (L01 addendum).

### 3.2 UE plan
- `URestorationState::ShowCaption(const FString& Key)`: `if (Settings->Access_Captions) OnCaption.Broadcast(URestorationText::Tr(Key));` — the gate is in the emitter, not the widget, exactly as `game_state.gd` 400–402. No glyph pass.
- `URestorationCaptionWidget : public UUserWidget` owned by the HUD widget, bound to `OnCaption`. Geometry and timing from `hud.gd` 36–46 and 179–186: anchored bottom-right, box from −420 to −18 px horizontally and −64 to −30 px vertically, right-aligned, phosphor `(0.85,0.93,0.77)`, base size 18, outline per §4.2; on caption: alpha 1.0, hold 1.4 s, fade to 0 over 0.6 s. A new caption restarts the tween. Single line; queueing is **OPEN** (Godot overwrites; the matrix's "toasts queue and never overlap" is stated for toasts, not captions).
- Sound-event sources call `ShowCaption` at the same sites as Godot (the "same spawn sites" principle, `UE5-MIGRATION-MAP.md` §AUDIO). Parity set, 15 strings: `[THE BELL RINGS · once]`, `[pen tick]`, `[door]` (`sfx.gd` 17, 22, 27); `[BARS, ALL MONITORS]` (`live_production.gd` 96, `decision_ledger.gd` 62); `[A CHAIR, BETWEEN FRAMES]`, `[YOU'RE ON · TO NOTHING LISTED]` (`live_production.gd` 178, 188); `[THE JAW WORKS ITS LEVER]`, `[IT FOLDS THROUGH THE DOORWAY]` (`rundown.gd` 267, 343); `[ONE FRAME LEFT OF HERSELF]`, `[A REEL, LABELED IN HER HAND: ME]` (`harriet.gd` 105, 115); `[THE INK LEAVES THE PAPER]`, `[THE SIGN-OFF, WHOLE]` (`seance_dock.gd` 100, 119); `[THE KETTLE, TWO ROOMS AWAY, CLICKS OFF]` (`fire_tape_dock.gd` 68); `[MAINS HUM, SHAPED LIKE A STANDING PERSON]` (`patchbay_console.gd` 92); `[NO ECHO]` (`hud.gd` 171).
- Two of the fifteen belong to systems already in UE: the lever caption fires at the 1.2 m loom in `ARundown` (PROGRESS 0.8a already logs "the jaw works its lever") and the fold caption at the 2.2 s door toll (0.7). Wiring those two to `ShowCaption` is a one-line change each and is the cheapest possible proof that the caption pipeline exists.
- UE5 extension (matrix §HEARING): `ShowCaptionAt(Key, WorldPos)` appends a directionality tag and applies a proximity weight; `Access_VisualBell`; MONO DOWNMIX as a Submix effect. Format of the tag, weight curve and the bracket-vs-plain rule for band-limited vs full-range sources have no shipped numbers → **OPEN** (§10); design them with the audio bible, not here.

### 3.3 Data
- `Access_Captions` bool, default false (§1.1).
- Keys: 14 of the 15 parity captions are in `Data/GameText.csv` (rows 93, 142, 209, 214, 224, 445, 449, 541, 575, 586, 619, 627, 631, 632). **`[door]` is absent** (grep count 0; also absent from `translations/strings.csv`). Add it. `[WEIGHTED FOOTSTEP]` is not in the CSV and not in code (§3.1 gap).
- A caption manifest is recommended as data: `ue/Restoration/Data/Captions.csv` with columns `key, emitter, band (bracket|plain), directional (0|1)` — 15 rows today. It gives the coverage test a denominator that is not a grep.

### 3.4 Acceptance
- `Restoration.Access.Captions.KeyCoverage` (headless): every row of `Captions.csv` resolves in `ST_GameText`; count equals the number of `ShowCaption(` call sites in `Source/` (a script assertion, like `tools/extract_data.py`'s row-count asserts). Today the reference count is 15; the CSV holds 14.
- `Restoration.Access.Captions.GateOff` / `.GateOn`: with `Access_Captions=false`, `ShowCaption` broadcasts nothing; with true, exactly one broadcast carrying `Tr(key)`.
- `Restoration.Access.Captions.LeverAndFold` (simulate, extends the existing 0.8a AF fixture): captions on; run the approach-to-loom and a door fold; assert `[THE JAW WORKS ITS LEVER]` and `[IT FOLDS THROUGH THE DOORWAY]` each broadcast once, in that order relative to the telemetry lines already asserted.
- Visual: QA-05 (pen tick on S1 sign), QA-37, QA-38; device pass item "the finale bell with sound muted (does the caption carry the beat)" (`conformance-pass.md` §5).

### 3.5 Schedule
- Pipeline (`ShowCaption`, widget, the two AF captions): with **0.8b-5** (the HUD half is already open there: "visible countdown"). Remaining 13 call sites land with the systems that own them (P3–P5 / PROGRESS Phases 4–5). Matrix extension (directional, visual bell, mono): **5.2**. BUILD-ORDER places "captions" in P6; this proposal pulls the pipeline forward because it is the smallest surface that proves Law 9 is not vaporware at the gate.

---

## 4 · UI TEXT SIZE AND THE HUD OUTLINE (a caption dependency, so it lives here)

### 4.1 Canon
"TEXT SCALE 0.8 to 1.6, default 1.0, touches every HUD label recursively (shipped)." (`restoration-accessibility-matrix.md` §VISION). R1: "outlines on every HUD label (backplate-equivalent for dynamic backgrounds) plus a UI text scale control" (`conformance-pass.md` §3 R1; addendum c029). SDLC hook: "a hardcoded-font-size grep that fails when a label bypasses the text-preference system" (`conformance-pass.md` §4).

### 4.2 UE plan
- `URestorationTextBlock : public UTextBlock`: caches `BaseSize` on construct, exposes `ApplyScale(float)` = `Font.Size = round(BaseSize * Scale)`; sets `Font.OutlineSettings` to black at 0.85 alpha, size 6 (`hud.gd` 157–158; UE outline units are Slate units, so verify visually that 6 reads as Godot's 6 px at 1080p and pin the number in the widget).
- `URestorationHUDWidget::ApplyTextPrefs()` walks its `WidgetTree` (`ForEachWidget`) and calls `ApplyScale` on every `URestorationTextBlock`; bound to `OnUiScaleChanged` and run once on construct (`hud.gd` 32, 145–159).
- Lint (the SDLC hook): an automation test that constructs every `WBP_*` under `/Game/UI` and fails if any plain `UTextBlock` (not the subclass) exists in the tree.

### 4.3 Data
`Access_UiScale` float, default 1.0, clamp 0.8..1.6 (§1.1).

### 4.4 Acceptance
- `Restoration.Access.UiScale.Applies`: construct the HUD widget, set scale 1.6, assert every `URestorationTextBlock` reports `Font.Size == round(Base*1.6)`; set 0.8, assert again; set 3.0, assert 1.6 (clamp).
- `Restoration.Access.UiScale.NoPlainTextBlocks`: the lint above.
- Visual: device pass "one full Day 1 with captions on and text at 1.4x" (`conformance-pass.md` §5).

### 4.5 Schedule
With **0.8b-5** (the HUD widget is created there for the countdown); the lint joins 0.9's automation set.

---

## 5 · ASSIST

### 5.1 Canon
- "ASSIST widens the beat 0.2 to 0.35 and stretches screening timing 1.5x (shipped) and never gates content or endings." (`restoration-accessibility-matrix.md` §COGNITIVE AND PACING).
- The shipped definition, more precise: "R5 (a single ASSIST switch carrying three mercies: beat tolerance 0.2 to 0.35, premiere clocks times 1.5, and hold-E-counts-as-still at both stillness checks, disclosed in its own label)" (`conformance-pass.md` addendum c031). Note the discrepancy: the matrix says "screening timing 1.5x"; the code applies 1.5x to the PREMIERE clocks (`live_production.gd` 350) and nothing in `screening_event.gd` is stretched. Code is the intent (`PORT-BRIEF.md`); the matrix sentence is a paraphrase.
- Difficulty ruling: "DIFFICULTY: RULED, ASSIST only. One game, honestly tuned." (`docs/production/restoration-gap-audit.md` §5). There is no difficulty menu; ASSIST is the only knob.
- Controls map: "THE BENCH CAPTURE is hold-E for the full take with the beat kept via stillness (ASSIST relaxes both)" (`restoration-controls-map.md` §PC context notes). `scripts/capture_bench.gd` contains no assist reference (grep), so "relaxes both" at the bench is prose without code → **OPEN** whether the bench capture participates (§10).
- QA-18: "ASSIST on: beat window visibly forgiving, premiere clocks half again longer, holding E passes both stillness checks." QA-19: "Floor Manager watch fails on movement, passes on assist-hold."
- Screening is a P3 acceptance ("screening with stances and assist", `BUILD-ORDER.md` P3) and an open 0.8b-5 sub-box in PROGRESS.md.

### 5.2 UE plan — the three mercies, each at its exact site
1. **Beat tolerance** (`screening_event.gd` 89–94): `tol = Assist ? 0.35 : 0.20; if Harriet dead: tol = max(0.1, tol - 0.05); phase = fmod(elapsed, BEAT); on_beat = phase < tol || phase > BEAT - tol` with `BEAT = 0.8`, `WINDOW = 3.2` (`Data/Timings.csv` rows screening_event.gd). Home: `AScreeningEvent::OnBeat()` (an `IRestorationInteractable` actor, the P3 screening port).
2. **Hold-E counts as still** (`screening_event.gd` 82–86 and `floor_manager.gd` 65–66, identical rule): `held_still = Assist && InteractPressed; moved = velocity > 0.4 m/s && !held_still`, screening accumulates 0.3 s of motion before ruling `moved`; the Floor Manager rules instantly. Homes: `AScreeningEvent::Tick` and `AFloorManager::Tick`. "InteractPressed" must read the Enhanced Input action value of `IA_Interact` (so a remapped interact key still counts — the label says "hold E" but the rule is the ACTION).
3. **Premiere clocks × 1.5** (`live_production.gd` 349–360): `t = dur * (Assist ? 1.5 : 1.0)` for the 45 s cue-2 clock and the two 30 s blackout clocks (lines 76, 104, 111). Home: `ALiveProduction::Timed(Dur, Label)`. The status line format `"%s · 0:%02d"` with `ceil(t)` is glyph-substituted capture status (§1.2).
- Constants live in `URestorationAssist` (a header of `static constexpr`): `BeatTolerance = 0.20f`, `BeatToleranceAssist = 0.35f`, `HarrietDeadPenalty = 0.05f`, `BeatToleranceFloor = 0.10f`, `StillSpeed = 0.4f`, `ScreeningMoveGrace = 0.3f`, `PremiereClockAssist = 1.5f`. Add the four that are not yet in `Data/Timings.csv` (0.2, 0.35, 0.4, 1.5) so the port's numbers stay in one table (`UE5-MIGRATION-MAP.md` §WHAT MUST NOT CHANGE: "every number in the playtest protocol's knob list").
- "Never gates content or endings": no achievement, ending, PT award or ledger entry reads `Access_Assist`. Enforce by grep-lint (§5.4).
- Hold-to-toggle (§2.2) is a separate switch, not part of ASSIST; the canon keeps them apart (one is timing mercy, the other is muscle).

### 5.3 Data
`Access_Assist` bool, default false (§1.1); the seven constants above.

### 5.4 Acceptance
- `Restoration.Access.Assist.BeatWindow` (headless, pure function): for elapsed values 0.00, 0.19, 0.21, 0.34, 0.36, 0.45, 0.61, 0.79 assert on-beat results for Assist off (`T,T,F,F,F,F,T,T`) and on (`T,T,T,T,F,F,T,T`); with Harriet dead and Assist off assert 0.16 → F (tol 0.15); with Harriet dead and Assist on assert 0.31 → F (tol 0.30).
- `Restoration.Access.Assist.HoldStill` (simulate): Floor Manager watch armed; move the pawn at 1.0 m/s with `IA_Interact` held and Assist on → watch passes ("The hand lowers. The take holds."); same with Assist off → "You moved on camera. Somewhere, a take is ruled spoiled." (QA-19).
- `Restoration.Access.Assist.PremiereClock`: `Timed(45, ...)` with Assist on must run 67.5 s ± one frame before the row is taken; off, 45.0.
- `Restoration.Access.Assist.NeverGates` (static): grep `Source/` for `Access_Assist` and assert the only readers are the three homes above.
- Visual: QA-18 (the sign's pulse window "visibly forgiving").

### 5.5 Schedule
With **0.8b-5 "screening + assist"** (already an open sub-box) for mercies 1 and 2 at the screening; mercy 2 at the Floor Manager with the night trip (Phase 4 / BUILD-ORDER P4); mercy 3 with the premiere (BUILD-ORDER P5, PROGRESS 4.FINALE). Cloud unit C10 (PORT-NOTES SCREENING) is the transcription this port reads from; C10 should cite this section rather than re-derive it.

---

## 6 · REMAP

### 6.1 Canon
- "Every prompt renders the player's ACTUAL binding via the glyph system, per device, always." (`restoration-controls-map.md` §Principle). "Remapping (R6) covers the five verbs today (interact, respond, improvise, stabilizer, map) with conflict refusal; the UE5 target is every action remappable including movement." (§PC context notes). "Glyphs swap to pad iconography the frame a pad speaks." (§CONTROLLER).
- "FULL REMAP on both devices (five verbs shipped; everything in UE5)" (`restoration-accessibility-matrix.md` §MOTOR). Design doc: "Full remap, hold-to-toggle alternatives on all sustained inputs" (§Captions and Accessibility).
- Conflict rule and message: `rebind()` refuses a key already bound to another remappable action with `KEY IN USE · that key already answers to %s.` (`game_state.gd` 370–377; `ue/PORT-NOTES-STATE.md` §4 keys row). QA-17: "Remap RESPOND onto E: refused with KEY IN USE; remap onto an unused key: prompts everywhere show the new key."
- Glyph substitution: word-boundary replacement of `E, SPACE, Q, T, M` for exactly the five remappable actions (conformance addendum c033; localization L05 addendum 033). "Remaining residue: Z, X, O, P, and the number keys remain literal (outside the remap set)" (c033) — in UE, once every action is remappable, those letters become residue that MUST be fixed (they would lie about a remapped key, and Law 8 forbids a second lie). Listed in §10 as scope.
- QA-15: the map footer "shows the BOUND map key."

### 6.2 UE plan
- Module: add `"EnhancedInput"` to `PublicDependencyModuleNames` in `Restoration.Build.cs`; enable the plugin in `Restoration.uproject` (it is engine-default-enabled but declare it).
- Actions (`/Game/Input/IA_*`), one per Godot action (`project.godot` §[input]): `IA_Move` (Axis2D from `ui_left/right/up/down` — WASD and arrows), `IA_Look` (mouse), `IA_Interact` (E), `IA_Respond` (Space), `IA_Improvise` (Q), `IA_ToggleTbc` (T), `IA_Map` (M), `IA_Ledger` (Tab), `IA_Options` (O), `IA_PhotoSafe` (P), `IA_Cam1/2/3` (1/2/3), `IA_FrameBack` (Z), `IA_FrameFwd` (X), `IA_Crouch` (LeftControl; pad B per `DefaultInput.ini` line 86), `IA_Pause` (Escape = Godot `ui_cancel`). Defaults in `Config/DefaultInput.ini` today cover only Crouch, Interact and the move/look axes (lines 85–95); the rest is new.
- Two mapping contexts: `IMC_Restoration` (priority 0) holds every NON-remappable action; `IMC_Remap` (priority 10) holds ONLY the five `REMAP_ACTIONS` (`game_state.gd` 305: `interact, respond, improvise, toggle_tbc, map`) and is rebuilt at runtime by `URestorationSettings::ApplyBindings()` from `Keys` (default key when absent). The five never appear in `IMC_Restoration`, so a rebind cannot leave a stale default firing beside the new key. Rebuild = `NewObject<UInputMappingContext>` + `MapKey` ×5, then `RemoveMappingContext`/`AddMappingContext` on the `UEnhancedInputLocalPlayerSubsystem`, then `RequestRebuildControlMappings`.
- `bool URestorationSettings::Rebind(FName Action, FKey Key, bool bPersist = true)` — verbatim order of effects from `game_state.gd` 370–385: (1) for each OTHER remap action, if its bound key equals `Key` → `Toast("KEY IN USE · that key already answers to %s.", ActionUpper)` and return false; (2) set `Keys[Action] = Key.GetFName()`; (3) `ApplyBindings()`; (4) if `bPersist`, save. Called with `bPersist=false` from load for each stored key (lines 318–321).
- `FString URestorationSettings::KeyName(FName Action)`: the bound `FKey`'s display name (`FKey::GetDisplayName(false)`), upper-cased; `"?"` when unbound. A tiny override table keeps the five defaults reading as Godot does (`SpaceBar` → `SPACE`, not `SPACE BAR`) so shipped strings such as `THE SIGN PULSES · SPACE on the beat` are byte-identical at default bindings. Pad glyphs: **OPEN** (no canon glyph set; "pad iconography" is named, not drawn).
- Booth rows (§2.2 item 11), from `options_panel.gd` 105–134: label = action name upper-cased (`INTERACT`, `RESPOND`, `IMPROVISE`, `TOGGLE_TBC`, `MAP` — Godot prints the raw action id; a display-name column is **OPEN**), button text = `KeyName(action)`; on press → button reads `PRESS A KEY`, the widget captures the next key-down (not a repeat) via `NativeOnKeyDown`/`NativeOnPreviewKeyDown`, calls `Rebind`, restores the button text, and swallows the event. Escape does not close the booth while a capture is pending.
- "Everything remappable" (UE target): the mechanism above generalizes by making `IMC_Remap` carry every action and `Keys` unbounded; the conflict check then spans all actions. The five-verb v1 is what the law demands at parity; the full set is scope for §10.
- Movement sensitivity: `Input_Sensitivity` multiplies the look delta exactly as `player.gd` 34–36 (`MOUSE_SENS * clamp(sens, 0.2, 3.0)`). Note `DefaultInput.ini` line 13–14 sets engine mouse sensitivity 0.07 — the port must derive the multiplier so that 1.0 reproduces Godot's 0.0022 rad/px (parity was proven "to the digit" for walk speed in 0.8b-1; do the same here).

### 6.3 Data
- `Keys : TMap<FName, FName>` (§1.1). Defaults: `interact=E, respond=SpaceBar, improvise=Q, toggle_tbc=T, map=M` (`project.godot` physical keycodes 69, 32, 81, 84, 77).
- Proposed `ue/Restoration/Data/Input.csv` (`action, default_key, remappable, glyph_token`) — 18 rows from `project.godot` §[input] — generated by `tools/extract_data.py` so the mapping contexts can be stamped by `ue/pyscripts/` like the greybox is (world-from-data principle, `UE5-MIGRATION-MAP.md` §WORLD GENERATION).
- Strings: 63 CSV keys contain at least one glyph token (script count over `Data/GameText.csv`); these are the strings QA-17's "prompts everywhere show the new key" covers.

### 6.4 Acceptance
- `Restoration.Access.Remap.RoundTrip` (headless): `Rebind(respond, F)`; save; fresh subsystem; load; assert `Keys[respond]==F` and `KeyName(respond)=="F"`; assert `IMC_Remap` maps `IA_Respond` to F and nothing to SpaceBar.
- `Restoration.Access.Remap.Conflict` (QA-17 first clause): `Rebind(respond, E)` returns false; `OnNotify` fired once with `KEY IN USE · that key already answers to INTERACT.`; `Keys` unchanged.
- `Restoration.Access.Remap.Glyphs`: with respond→F, `Glyphs("THE SIGN PULSES · SPACE on the beat · Q improvises · or hold still")` == `"THE SIGN PULSES · F on the beat · Q improvises · or hold still"`; with defaults, `Glyphs(s) == s` for every one of the 63 token-bearing keys (byte-identity at defaults is the localization contract, L05 addendum).
- `Restoration.Access.Remap.NoDefaultLeak`: after `Rebind(interact, G)`, pressing E in simulate does not fire `IA_Interact` (proves the two-context split).
- Visual: QA-15 map footer, QA-17 second clause on the bench prompt and the screening toast.

### 6.5 Schedule
- Enhanced Input conversion (§1.3, §6.2 contexts): **0.8b-1 follow-up** — it touches `ARitaCharacter`, which 0.8b-1 owns; propose sub-box **0.8b-1b Enhanced Input parity**. `Rebind`/`KeyName`/`Glyphs` with `URestorationSettings` (§1.1) in **0.8b-5**. The booth rows with **5.2a** (§2.5). "Everything remappable" and pad glyphs: **5.2**.

---

## 7 · PAUSE

### 7.1 Canon
- "INTERMISSION pauses everything honestly (shipped)." (`restoration-accessibility-matrix.md` §COGNITIVE AND PACING).
- Shipped definition: "Escape holds the whole simulation with audio muted, refused only while the player is locked in an authored sequence; the intermission menu is keyboard-operable with visible focus and opens the booth in place." (`conformance-pass.md` addendum c034; also `docs/BUILD-LOG.md` Commit 034 entry, which adds "honest RETURN TO TITLE label").
- QA-32: "Pause anywhere unlocked: world and clocks hold, audio mutes; pause during any authored sequence: refused."
- Design doc: pause lives in the binder ("Pause, settings, saves, and the journal live inside a physical ring binder", §Philosophy); "the pause menu itself drifts as the Producer Track rises" is a named unsafe choice (§The unsafe choices, named) and is dressing, not a lie (§Casting drift in the interface). The binder is TRUE-PAUSE in the day and LIVE-TIME during the premiere (`restoration-gap-audit.md` §3) — that ruling is about the BINDER; the Escape intermission is refused only by `locked` (code), which the premiere's walking phases do not set. Whether the premiere should refuse Escape is **OPEN** (§10).
- Demo: "DP3 the ending sequence uninterruptible by movement or pause" (`docs/production/restoration-demo-cut-plan.md` §DP). The demo end card locks the player (`hud.gd` `_on_demo_end`), so the refusal rule covers it.
- Law 6 is the reason the clock matters: "THE SCHEDULE IS REAL. ON AIR and BREAK govern behavior mechanically" (`THE-LAWS.md` line 7). A pause that let the 50/18 s clock run would be the interface lying about the schedule.

### 7.2 UE plan
- Request path (`player.gd` 41–44): `IA_Pause` in `ARitaCharacter` → `if (bLocked) return; State->OnPauseRequested.Broadcast();`. **`ARitaCharacter` has no lock flag yet** (grep); add `bool bLocked` and set it exactly where `hud.gd` sets `player.locked`: the retake presentation (276→305), run end (312), demo end (364), finale and ending sequences (384, 433→439). Those are the "authored sequences".
- Toggle (`hud.gd` 87–141), in `URestorationHUDWidget::TogglePause()` bound to `OnPauseRequested`:
  - If paused: `UGameplayStatics::SetGamePaused(World, false)`; unmute; mouse captured (`SetInputMode_GameOnly`, hide cursor); destroy the menu.
  - Else: if `Rita->bLocked` return silently (no toast — Godot shows nothing). `SetGamePaused(true)`; mute; cursor visible; build the INTERMISSION menu: header `INTERMISSION · WGLD holds its breath` (phosphor, 20), buttons `RESUME`, `THE BOOTH`, `RETURN TO TITLE · progress holds at your last signature` (flat, 16, phosphor focus ring); initial focus on RESUME (`hud.gd` 141: child index 1 after the header). Scrim `(0,0,0,0.7)`.
  - `THE BOOTH` opens the booth widget as a child of the intermission menu, ticking while paused.
  - `RETURN TO TITLE`: unpause, unmute, cursor visible, open the title level. No save is written (the label promises progress holds at the last SIGNATURE, which is the last `SaveToSlot`, `game_state.gd` 184).
  - Escape while paused resumes (`hud.gd` 189–193).
- "Holds the whole simulation": `SetGamePaused` stops actor tick for everything without `bTickEvenWhenPaused` and stops the World `FTimerManager`. `URestorationClock` arms its phase timer on the World timer manager (`RestorationClock.h` `GetWorld()->GetTimerManager()`), so it holds — but this is asserted in §7.4, not assumed; if it ever moves to the GameInstance timer manager it would keep running while paused, which is the one implementation that violates Law 6. The intermission widget and the booth set `bIsFocusable` and use `UUserWidget` ticking under pause (widgets tick while paused by default; Slate is not the game world).
- "Audio muted": `SetGamePaused` pauses non-UI sounds natively; additionally push a `USoundMix` `SM_Intermission` overriding `SC_Master` to 0.0 with 0 s fade (`UGameplayStatics::PushSoundMixModifier`), popped on resume, so hum beds and MetaSound loops flagged as UI sounds are also silent. Godot mutes bus 0 outright (`hud.gd` 91, 100); mute, not duck.
- Pad: `PAUSE start`, `BOOTH menu long-press` (`restoration-controls-map.md` §CONTROLLER) — the long-press is an Enhanced Input `Hold` trigger on `IA_Options`; duration **OPEN**.

### 7.3 Data
- No new setting. Strings: `INTERMISSION · WGLD holds its breath`, `THE BOOTH`, `RETURN TO TITLE · progress holds at your last signature` are in the CSV (rows 220–222). **`RESUME` is absent** (grep count 0; `hud.gd` 118 wraps it in `tr()`). Add it.
- `ARitaCharacter::bLocked` (live, not saved; PORT-NOTES §2 lists `in_retake` etc. as session-only — `locked` is a player-node field, same class of thing).

### 7.4 Acceptance
- `Restoration.Access.Pause.ClockHolds` (simulate, headless): read `URestorationClock` remaining time (add a `TimeLeft()` accessor, as `broadcast.gd` 23 has); pause 5 s of wall time; assert remaining unchanged to the frame and no `OnPhaseChanged` fired; resume; assert the flip lands 50.0 s after the unpaused elapsed total. Also assert `ARundown` position unchanged across the pause (the hunt held).
- `Restoration.Access.Pause.RefusedWhenLocked`: set `bLocked=true`; fire `IA_Pause`; assert not paused and no menu; `bLocked=false`; fire; assert paused (QA-32 both clauses).
- `Restoration.Access.Pause.AudioSilent`: while paused, the master submix's measured output (`USubmixEffect` spectrum/envelope analyzer, or `FAudioDevice::GetMaxVolume`-style probe) is 0.
- `Restoration.Access.Pause.MenuKeyboard`: with the menu open, Tab/arrow traversal reaches all three buttons and Enter on `THE BOOTH` spawns the booth as a child; Escape resumes.
- Visual: focus ring photographed on the intermission menu (device pass).

### 7.5 Schedule
- `bLocked` + request path + `TogglePause` core (pause, mute, clock hold, refusal): **0.8b-5** — the retake presentation sub-box is where `locked` first exists, and the clock-holds test is a Law 6 guard the gate should already have. Menu layout and booth-in-place: **5.2a**. BUILD-ORDER's placement of "pause" in P6 is the one this proposal most disagrees with; §10 asks the owner to rule.

---

## 8 · THE DEFERRAL RULE

### 8.1 Canon (quoted in full)
`docs/production/restoration-achievements-design.md` §DOCTRINE, rule 1:

> THE DEFERRAL RULE. No achievement may surface during a protected beat. Unlocks fire silently into a queue and flush only at two moments: the next morning toast, or the title screen. The glimpse, the fire tape, the premiere, every ending sequence, and the demo card are popup-free zones by construction, not by hope. (Engine shape: an achievements autoload with unlock(id) and a flush gate on night_changed(false) and title _ready.)

Companions: rule 2 THE META-SILENCE LEDGER (no glimpse achievement ever; the warm unit acknowledged only through the dock achievement; one seance achievement; Chum's name in no title) and rule 3 THE VOICE; "the demo build ships with achievements disabled entirely" (same §DOCTRINE). `PORT-BRIEF.md` §5: "the deferral rule and meta-silence live in the design doc and are not optional." Law 3 (`THE-LAWS.md` line 4) and `achievements.gd` line 5: "The once-ever moment has no entry here, on purpose." Law 5: "Chum has ... no achievement title" (`THE-LAWS.md` line 6). QA-04, QA-29. BUILD-ORDER P6: "achievements with deferral"; amendment adds A27/A28.

The reference implementation defers EVERY unlock unconditionally — there is no protected-beat detector; the two flush gates are the only exits (`achievements.gd` 39–43 flush on `night_changed(false)`; `title.gd` 29 `flush_silent()` into the `FILED WHILE YOU WERE OUT:` stack). "By construction" means exactly that: no code path can toast an achievement anywhere else. The port must preserve this shape rather than add beat detection; a detector would be a second, weaker mechanism.

### 8.2 UE plan
- Class: `URestorationAchievements : public UGameInstanceSubsystem`, persisted in `URestorationAchievementsSave : USaveGame` slot `"achievements"` (Godot: `user://achievements.cfg`, apart from the log — surviving NEW GAME is intended: A-ids are per profile, not per save).
- API, verbatim from `achievements.gd`:
  - `void Unlock(FName Id)` — no-op if `Id` empty, `DEMO`, already unlocked, or not in `TITLES` (line 46); else mark, save, `OnAchievementUnlocked.Broadcast(Id)` (the Steam bridge; ids are the API names, `restoration-achievements-design.md` §ENGINE DELTA). Never toasts.
  - `void OnEnding(const FString& Name)` — `A27` if `Casualties.IsEmpty() && RowCasualties == 0`; then `ENDING_MAP[Name]` (lines 53–56; map at lines 25–30).
  - `TArray<FText> Pending()` — unlocked and not yet shown, as titles (80–85).
  - `void FlushToToasts()` — if pending ≤ 2: one toast `FILED · <title>` each; else one toast `FILED · %d entries, %s among them.`; then mark all shown (88–97). Bound to `URestorationState::OnNightChanged` with `bNow == false` (the morning; 39–43).
  - `TArray<FText> FlushSilent()` — returns pending and marks shown (100–103); called by the title widget, which renders `FILED WHILE YOU WERE OUT:\n` + titles bottom-left (`title.gd` 29–39; QA-04 "exactly once").
  - The two wiring signals: `OnLogSigned → A01`, `OnRunEnded → A18` (36–38). The remaining unlock sites are the call sites the achievements doc lists; they port with their systems.
- Where the rule is DOCUMENTED as a gate in code: a comment block at the top of `RestorationAchievements.h` quoting §8.1, and a static test (§8.4) that fails if any `Toast(`/`OnNotify` call exists in the subsystem outside `FlushToToasts`. The prompt for this spec suggested `ARundown`/state as the home; the rule has nothing to read from the brain (it does not detect beats), so the achievements subsystem is the only correct home, with `URestorationState::OnNightChanged` as its one gameplay input.
- LAW 3 and LAW 5 guards: `TITLES` contains 28 entries (A01–A28, `achievements.gd` 11–24); a static test asserts no title contains the forbidden Day 4 name (owner supplies the string out of band; the test reads it from an untracked file, so the name still "appears in no code file"), and no title or description contains `CHUM`. Cloud unit C14 (PROGRESS §CLOUD LANE) is the audit; this is the automated twin.
- DEMO: `Unlock` is a no-op under `DEMO` (line 46). The demo card is popup-free because nothing can be unlocked, not because the card is detected.

### 8.3 Data
- `URestorationAchievementsSave`: `TSet<FName> Unlocked`, `TSet<FName> Shown`.
- `Data/Achievements.csv` (`id, title, hidden`) — named in `PORT-BRIEF.md` §5 but NOT in `ue/Restoration/Data/` today (0.5 extracted seven tables; Achievements is missing). Generate it from `achievements.gd` `TITLES` plus the hidden flags in `restoration-achievements-design.md` §THE LIST and §ADDENDUM (c043).
- Strings: `FILED · ` prefix and `FILED WHILE YOU WERE OUT` are in the CSV (grep count 1 each). Titles are their own keys (rows 2–5 begin the list: `FIRST SIGNATURE`, `CAREFUL HANDS`, …).

### 8.4 Acceptance
- `Restoration.Access.Deferral.NeverSurfacesDuringPlay` (simulate): bind a counter to `OnNotify`; set `bRecording=true`, `bScreeningActive=true`, `bPremiereLive=true` in turn and call `Unlock(A02)`, `Unlock(A04)`, `Unlock(A20)`; assert the counter is 0 after each; call `SetNight(true)` then `SetNight(false)`; assert exactly ONE toast, text `FILED · 3 entries, CAREFUL HANDS among them.`; call `SetNight(false)` again; assert no further toast (QA-29).
- `Restoration.Access.Deferral.TwoOrFewer`: unlock A01 only; morning; assert one toast `FILED · FIRST SIGNATURE`.
- `Restoration.Access.Deferral.TitleOnce` (QA-04): unlock A05 with no morning; `FlushSilent()` returns `[STILLNESS, HELD WHOLE]`; a second `FlushSilent()` returns empty.
- `Restoration.Access.Deferral.Idempotent`: `Unlock(A01)` twice → `OnAchievementUnlocked` once.
- `Restoration.Access.Deferral.DemoSilent`: with `DEMO` true, `Unlock(A01)` leaves `Unlocked` empty.
- `Restoration.Access.Deferral.OnlyTwoExits` (static): the subsystem's source contains exactly one `Toast(` site, inside `FlushToToasts`.
- `Restoration.Access.Deferral.MetaSilence` (static): no title contains `CHUM`; the once-ever name is absent from every file under `Source/` and `Data/` (Law 3, `THE-LAWS.md` line 4: "Its name appears in no code file").

### 8.5 Schedule
- The subsystem, its save, the two gates, the two wired signals (A01, A18) and every test in §8.4: **0.8b-5** or a new **0.8c ACHIEVEMENTS (deferral)** box directly after it — it is one commit ("Estimated one commit, no new systems", `restoration-achievements-design.md` §ENGINE DELTA) and it needs only `OnNightChanged`, `OnLogSigned`, `OnRunEnded`, all of which exist since 0.8b-4. Remaining unlock call sites land with their systems. BUILD-ORDER P6 places it last; there is no technical reason to wait, and the Law 3/5 static tests are cheap gate evidence.

---

## 9 · PROPOSED SCHEDULE (for the owner to splice into PROGRESS.md; nothing here edits it)

| Unit (proposed id) | Contents | Depends on | Gate evidence it yields |
|---|---|---|---|
| **0.8b-1b Enhanced Input parity** | `EnhancedInput` module; `IA_*` set; `IMC_Restoration` + `IMC_Remap`; `Input.csv`; sensitivity parity to Godot 0.0022 | 0.8b-1 | Law 9 REMAP substrate; migration map INPUT row honored |
| **0.8b-5 (extend the open box)** | `URestorationSettings` + `"settings"` slot; `Tr`/`Glyphs`/`KeyName`; `Rebind` (no UI); `ShowCaption` + caption widget; `URestorationTextBlock` + `ApplyTextPrefs`; the two AF captions; `bLocked` + pause core with clock-hold test; screening assist (mercies 1, 2); tests §2.4 (RoundTrip, NewGameLeavesSettings), §3.4, §4.4, §5.4 BeatWindow, §6.4, §7.4 | 0.8b-4 | Every law-9 noun exists as code before 0.10; the gate row flips from "NOT YET — flagged" to "EXERCISED (substrate) / NOT YET (widgets)" |
| **0.8c ACHIEVEMENTS (deferral)** | `URestorationAchievements`, save slot, both gates, A01/A18 wiring, `Achievements.csv`, tests §8.4 | 0.8b-4 | Law 9 DEFERRAL RULE exercised; Law 3/5 static guards live |
| **0.10 PHASE GATE** | add the §2.4–§8.4 automation names to the gate's fixture list | above | `GATE-0.10.md` row 9 can be signed on evidence |
| Phase 4 (4.ENCOUNTERS, 4.FINALE) | Floor Manager assist-hold; premiere ×1.5; the 13 remaining captions at their emitters; remaining unlock sites | 0.8b-5, 0.8c | QA-18, QA-19, QA-29 |
| **5.2a THE BOOTH** (new, first in 5.2) | `URestorationBoothWidget`; first-run flow; remap rows; intermission menu layout with booth-in-place; hold-to-toggle switch; string additions (`FULLSCREEN`, `RESUME`, `[door]`) | 0.8b-5 | QA-01, QA-02, QA-16, QA-17, QA-32 |
| **5.2b ACCESS FULL TARGET** (new) | directional captions, visual bell, mono downmix, flicker/grain slider, toast dwell, everything-remappable, pad glyphs, stick/invert/gyro | 5.2a | matrix "full target"; device pass |

Reading against BUILD-ORDER (`docs/packet/portbrief/BUILD-ORDER.md`): P3 already owns "screening with stances and assist"; P6 owns "achievements with deferral, booth complete, captions, pause". This proposal keeps P6 as the place where the WIDGETS are completed and audited, but moves the SUBSYSTEMS (settings, captions, pause core, deferral) into Phase 0 so the 0.10 gate is signed on code rather than on a promise. The AAA plan's rule 2 ("Take the FIRST unchecked box ... No skipping beyond that", `AAA_BUILD_PLAN.md` §0 item 2) means this reordering is the owner's call, not the loop's.

---

## 10 · GATE RULING NEEDED (the owner decides; the loop does not)

1. **When does access land?** (`GATE-0.10.md` §4 item 4: "agree it is scheduled into the UI phase, or demand it earlier.") Options on the table: (a) as BUILD-ORDER wrote it — all six in P6 / PROGRESS 5.2; (b) as §9 proposes — subsystems in 0.8b-5/0.8c before 0.10, widgets in 5.2a; (c) everything before 0.10. §9 argues for (b): the gate cannot honestly sign "ACCESS IS CANON" on a build where the words are not yet identifiers.
2. **Pause during the live premiere.** Code refuses Escape only while `locked`; the gap audit's live-time ruling covers the binder, not the intermission. Should the premiere refuse pause (making it an authored sequence), or hold honestly? Law 6 and the matrix's "pauses everything honestly" pull toward holding; the braid audit (QA-51) pulls toward refusing.
3. **The second meaning of "deferral rule".** Canon defines it for achievements only. If a rule for deferring a scare or beat under ASSIST was intended, it does not exist in any document and must be authored; the current ASSIST never defers or removes a beat, it widens tolerance and stretches clocks.
4. **`[WEIGHTED FOOTSTEP]`.** Canon (`restoration-after-fire-chum.md` §SOUND AND CAPTION LAW) names it "distance-scaled"; the Godot code never emits it. Ship it in UE (canon wins) or strike it (code is the intent)? If shipped: the distance-scaling rule is undefined.
5. **Bench capture under ASSIST.** The controls map says "ASSIST relaxes both" at the bench; `capture_bench.gd` reads no assist flag. Port the code (no bench mercy) or the prose (define what relaxes — the 4 m tether? the 12 s? Law 10 says the countdown "means both progress and expiry", so the 12 s cannot stretch without changing the contract).
6. **Hold-to-toggle: label text and which holds.** Canon promises the switch (`restoration-controls-map.md` §HOLD VERSUS TOGGLE) and names capture, fader, stillness; the booth string does not exist. Approve `HOLD INPUTS · toggle instead of hold` or supply the line.
7. **Scope of the matrix "full target" in 5.2b** — flicker/grain slider, visual bell, mono downmix, toast dwell, stick/invert/gyro, everything-remappable, pad glyphs. Each needs a label, a default and a range; none has one. Which are launch (`restoration-accessibility-matrix.md` §STREAMER says the streamer items are "a launch feature, not a patch") and which are backlog?
8. **Settings encoding deviation** (§1.1): key bindings stored as `FKey` names, not physical keycodes; file lives in ProjectSavedDir as a SaveGame slot, not an INI. Acknowledge, or demand an INI at the same path shape.
9. **Three missing string keys** (`[door]`, `FULLSCREEN`, `RESUME`) and the missing `Achievements.csv`: re-run `tools/extract_data.py` with the extractor fixed (it is the cloud lane's C12 GAMETEXT AUDIT territory) — rule whether the Mac lane may do it inline with 0.8b-5 or must wait for C12.
10. **Booth skin.** Overlay panel (shipped, code) vs binder "Presentation" form (design doc). Controls are canon either way; the skin decision belongs to Phase 5, but say so now so 5.2a does not build the wrong frame.
11. **Remap display names.** Godot prints raw action ids (`TOGGLE_TBC`). Keep, or supply five display names (the controls map calls the fourth "TAPE STABILIZER" / "STABILIZER")?
12. **Residue letters under full remap.** Once Z, X, O, P, 1–3 and movement are remappable, every literal mention of them in the 714 keys is a potential Law 8 violation. Approve extending `GLYPH_MAP` tokens (and the translator contract in `restoration-localization-plan.md` L05) to the full action set, with the extraction commit that adds them.
