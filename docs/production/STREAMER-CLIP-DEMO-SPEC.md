# RESTORATION · STREAMER MODE + CLIP LEDGER + TAPE 1 DEMO SPEC (C16)

Implementable UE 5.8 specs for the three comparative-study adoptions that
PROGRESS.md §PHASE 5 lists as units **5.6 Streamer mode (A1)**, **5.7 Clip
ledger pass (A4)** and **5.8 Demo — Tape 1 (A6)**. Written against the Godot
reference build, because "the Godot build IS the specification; where prose
and code disagree, THE CODE IS THE INTENT" [AAA_BUILD_PLAN.md §1 THE PORT KIT,
citing docs/packet/portbrief/PORT-BRIEF.md]. Every rule below carries a
citation `[KEY §section]` or `[file:line]` (keys in §0.1). Where canon is
silent the word is **OPEN** and the question is numbered in §6. Nothing here
invents canon; where two canon documents disagree the disagreement is
recorded and the code's reading is proposed, never silently chosen.

This is a paper deliverable from the cloud lane: no Blender, no UE, no capture
and no encoder was run. It is read by the Mac lane before units 5.6, 5.7 and
5.8, and by 5.2 (booth) for the two new booth rows it proposes.

---

## 0 · CONVENTIONS

### 0.1 Source keys

| Key | Path |
|---|---|
| STUDY | `docs/canon/restoration-comparative-study.md` (26 lines; the production copy at `docs/production/restoration-comparative-study.md` adds an ADDENDUM on Amnesia and Puppet Combo, lines 28–31, cited as STUDY-ADD) |
| LAWS | `docs/packet/portbrief/THE-LAWS.md` |
| PLAN | `AAA_BUILD_PLAN.md` |
| PROGRESS | `PROGRESS.md` |
| DEMO-PLAN | `docs/production/restoration-demo-cut-plan.md` |
| TRAILER | `docs/production/restoration-trailer-beats.md` |
| STEAM-PAGE | `docs/production/restoration-steam-page-draft.md` |
| PRESENCE | `docs/production/restoration-steam-presence.md` |
| ACH | `docs/production/restoration-achievements-design.md` |
| ARG | `docs/production/restoration-arg-plan.md` |
| MATRIX | `docs/canon/restoration-accessibility-matrix.md` |
| CONFORM | `docs/production/restoration-accessibility-conformance-pass.md` |
| ACCESS-SPEC | `docs/production/UE-ACCESS-SPEC-LAW9.md` (the booth/settings precedent this spec extends) |
| ART | `docs/production/restoration-art-bible.md` |
| AUDIO | `docs/production/restoration-audio-bible.md` |
| DREAD | `docs/canon/restoration-dread-doctrine.md` |
| AF | `docs/canon/restoration-after-fire-chum.md` |
| DOSSIER-ART | `docs/canon/art/after-fire-chum-dossier.png` (source of record for AF, per AF line 2) |
| CASUALTY | `docs/canon/restoration-casualty-ledger.md` |
| REACT | `docs/canon/restoration-reaction-matrix.md` |
| WALK | `docs/canon/restoration-walkthrough-levels-endings.md` |
| MASTER | `docs/canon/restoration-game-master.md` |
| DESIGN | `docs/canon/restoration-design-doc.md` |
| LIGHT | `docs/canon/restoration-lighting-bible.md` |
| QA | `docs/production/restoration-qa-regression.md` |
| INV | `docs/production/restoration-invariant-suite.md` |
| BUILD-ORDER | `docs/packet/portbrief/BUILD-ORDER.md` |
| PORT-BRIEF | `docs/packet/portbrief/PORT-BRIEF.md` |
| MIGRATION | `docs/packet/portbrief/UE5-MIGRATION-MAP.md` |
| PN-STATE / PN-SCREENING / PN-BROADCAST | `ue/PORT-NOTES-STATE.md`, `ue/PORT-NOTES-SCREENING.md`, `ue/PORT-NOTES-BROADCAST.md` |
| AUDIT | `ue/PORT-AUDIT-1.md` |
| README | `README.md` (the ledger) |
| GT | `ue/Restoration/Data/GameText.csv` (714 keys; line = key row) |
| TIMINGS | `ue/Restoration/Data/Timings.csv` |
| DEMO-OPEN | `ue/Restoration/Data/DemoOpen.csv` |
| Godot files | `scripts/*.gd`, `scenes/main.tscn`, `shaders/crt_tape.gdshader` — cited `file:line` |
| UE files | `ue/Restoration/Source/Restoration/*.h/.cpp`, `ue/pyscripts/*.py` — cited `file:line` |

### 0.2 The three units, verbatim

PROGRESS §PHASE 5 (lines 430–432):

> - [ ] 5.6 Streamer mode (A1: compression-kind grain, safe HUD margins)
> - [ ] 5.7 Clip ledger pass (A4: all named clippables verified capturable)
> - [ ] 5.8 Demo — Tape 1 (A6: the funnel)

PLAN §5 PHASE 5 (lines 384–389):

> **5.6 STREAMER MODE** (study A1: compression-kind grain, overlay-safe HUD margins, capture-clean toggle) · **5.7 CLIP LEDGER pass** (study A4: the named clippables — first doorway fold, THE TALLY COOLS, SAFE WHILE LIT countdown, the bell, the WARNING page, Harriet doubled, THE LEDGER read aloud — each verified capturable in ≤30s with one legible frame) · **5.8 DEMO — TAPE 1** (study A6: the funnel).

STUDY §ADOPTIONS (line 21):

> A1 Streamer mode to booth backlog (compression-kind grain, HUD safe margins, capture-clean toggle). … A4 Clip ledger adopted into trailer beats (this section is the source of record). … A6 Demo scope reaffirmed as the funnel.

The C16 box itself (PROGRESS lines 253–256) asks for these "as implementable
UE specs". The plan's 5.6 text carries a third item (capture-clean toggle)
that the PROGRESS box omits; the study and MATRIX both name it, so it is in
scope here and the omission is recorded as a tracker nit (§6 R1).

### 0.3 Status vocabulary

- **CANON** — quoted or cited; binds.
- **CODE** — the reference implementation's behaviour; the intent where prose differs [PORT-BRIEF].
- **STAND-IN** — a number or method proposed here because canon has none; its source is named; the Mac lane may ship it only after a ruling.
- **OPEN** — canon is silent and no stand-in is safe; numbered in §6.
- **ABSENT** — not yet in the UE C++ per AUDIT.

---

## 1 · THE LAWS THAT BIND ALL THREE UNITS

| Law | Verbatim (LAWS) | Consequence for 5.6 / 5.7 / 5.8 |
|---|---|---|
| 2 ONE STARTLE | "The in-tape lunge is the game's single jump scare. Nothing else lunges, stings, or pops, in-game or in marketing." [LAWS line 3] | The clip ledger (5.7) contains no startle; the demo (5.8) ends on the one that exists; streamer mode (5.6) must not add a flash or a pop to anything. INV I14 is the harness check ("harness greps event table per build") [INV line 22]. |
| 3 ONCE, EVER | "The Day 4 fire-corridor moment … is never referenced again by any system, including achievements, presence, and logs. Its name appears in no code file." [LAWS line 4] | Not a clippable, not a trailer beat, not a streamer-mode exception. The capture-clean toggle (5.6) has nothing to hide here because nothing may exist to hide. |
| 5 SILENCE CONTRACTS | "The bell rings once, at the finale beat, and its caption says so. Chum's bell is otherwise silent; Chum speaks nowhere; Chum has no account, no achievement title, no presence string." [LAWS line 6] | CL-4 (the bell) is capturable exactly once per run; no clip-ledger fixture may ring it twice in one session. Nothing in 5.6–5.8 names Chum in a UI string, a presence string [PRESENCE §SPOILER RULES] or a demo card. |
| 8 THE INTERFACE MAY LIE EXACTLY ONCE | [LAWS line 9] | Streamer mode and capture-clean are TRUE surfaces: they may HIDE a spoiler, never MISREPORT a setting, a clock or a binding [ACCESS-SPEC §0]. Hidden text must read as hidden (a visible redaction), not as absent. |
| 9 ACCESS IS CANON | "The booth, captions, assist, remap, pause, and the deferral rule ship in every build of every engine." [LAWS line 10] | The demo build ships the whole booth; streamer mode's rows live in the booth and therefore ship in the demo too [MATRIX §STREAMER: "a launch feature, not a patch"]. |
| 10 THE TALLY CONTRACT | "the countdown is visible and means both progress and expiry; the cool is 2.0 s and announced. The eye's light and the contract are the same fact." [LAWS line 11] | Capture-clean may NEVER hide the tally lamp, the countdown or the cool toast. Safe margins move the lamp inward, never off. CL-2 and CL-3 are this law, clipped. |
| 11 THE TWO HIDES | "every threshold costs him 2.2 s, and that toll is the player's counterplay." [LAWS line 12] | CL-1 (the fold) is this law, clipped. |
| DREAD L5 | "One startle. One interface lie. One once-ever sight. … the budget never grows." [DREAD line 9] | The clip ledger is a list of DREAD, not scares: every entry passes the three tests (repetition, law, earned) [DREAD line 15] — "the fold passes" is the doctrine's own example. |
| ART two-worlds | "no grain, chroma error, or scanline may ever appear on compound surfaces (grain belongs to tape only) … Footage is always shot or rendered clean and degraded live in the shader ladder" [ART line 8]; "Compound post: none … Tape post: owned entirely by the artifact ladder." [ART line 34] | Streamer grain (5.6) is a change INSIDE the artifact ladder, applied only where the ladder already applies. It is not a full-screen post effect. |
| AUDIO law | band-limited = memory, full-range = present; the bell S06 "single take, never reused anywhere" [AUDIO line 21] | Clip fixtures capture with the game's own mix; nothing is re-scored for a clip. |

---

## 2 · UNIT 5.6 — STREAMER MODE (study A1)

### 2.1 Canon

- Origin: "STREAMER CARE AS A FEATURE: TJOC shipped a bitrate-friendly setting in a DEMO. Grain and CRT mash under compression; we add a streamer mode (compression-kind grain, overlay-safe HUD margins) to the booth backlog." [STUDY §II item 4]
- Adoption: "A1 Streamer mode to booth backlog (compression-kind grain, HUD safe margins, capture-clean toggle)." [STUDY §ADOPTIONS]
- The access matrix makes it a launch obligation and adds the toggle's purpose: "Compression-kind grain, HUD safe margins, capture-clean toggle that hides spoiler text in the binder, and the bitrate lesson learned from TJOC honored as a launch feature, not a patch." [MATRIX §STREAMER AND CAPTURE MODE]
- Its neighbour in the matrix, distinct from it: "a FLICKER AND GRAIN REDUCTION slider in UE5 that tames CRT artifacts without touching lighting truth" [MATRIX §VISION]. That slider is an accessibility control (ACCESS-SPEC §2.2 lists it OPEN under the booth's "full target"); streamer mode is a capture control. They may share a material parameter; they are not the same row.
- What the tape ladder is in code: `shaders/crt_tape.gdshader` — chroma shift, scanlines, noise floor, dot crawl, tracking band, head-switch tear, vignette; scaled by `generation`, steadied by `tbc_on`, suppressed by `photo_safe` [crt_tape.gdshader:1–3, 7–10]. In UE: "crt_tape.gdshader → a Material Function stack applied to the RT … with scalar parameters generation, tbc_on, photo_safe driven from the state subsystem via a Material Parameter Collection." [MIGRATION line 9]
- Where the ladder is applied: "Applied to any screen that plays tape." [crt_tape.gdshader:3] — `scripts/bench_tv.gd:21` loads it for the bench monitor; `scripts/monitor_rig.gd` and `frame_sequence.gd` carry the same grammar for the wall and the seance.
- Photosensitivity precedent, which streamer mode must not regress: "the tracking band and head-switch flicker are the only rhythmic luminance elements and both are suppressed by photo-safe mode" [CONFORM F08]; "Reduced-motion setting flattens all camera sway and disables the CRT bloom pulse; nothing informational lives in motion alone." [DESIGN line 294]
- The booth is enumerated by code [ACCESS-SPEC §2.1 citing PORT-BRIEF §3]; no streamer row exists in `scripts/options_panel.gd` (lines 20–85 enumerate volume, sensitivity, fullscreen, TBC, photo-safe, text size, captions, assist, remap, close). Streamer mode is therefore a UE5 TARGET row, like hold-to-toggle [ACCESS-SPEC §2.2].
- HUD geometry in the reference (Godot pixels at the 1152×648-class design size the scene assumes; anchors from `scenes/main.tscn`, dynamic labels from `scripts/hud.gd`):

| HUD element | Anchor | Offsets (L, T, R, B) | Source |
|---|---|---|---|
| Prompt | bottom-centre (preset 7) | −420, −110, +420, −80 | main.tscn:83–91 |
| Toast | top-centre (preset 5) | −420, +40, +420, +70 | main.tscn:97–103 |
| TBC | top-right (preset 1) | −220, +16, −20, +44 | main.tscn:109–115 |
| Capture status | top-centre (preset 5) | −420, +80, +420, +112 | main.tscn:121–127 |
| Clock (ON AIR / BREAK) | top-left | +20, +16, +360, +44 | main.tscn:133–136 |
| Sheet (strikes) | top-right (preset 1) | −220, +48, −20, +76 | main.tscn:141–147 |
| Binder | centre (preset 8) | −300, −200, +300, +200 | main.tscn:154–162 |
| Objective | top-centre (preset 5) | −460, +118, +460, +146 | main.tscn:168–174 |
| Retake / end-card lines | full-rect, Line1 top −60, Line2 top +40 | — | main.tscn:189–211 |
| Caption strip | bottom-right | −420, −64, −18, −30 | hud.gd:39–44 |
| Tally lamp `● REC · SAFE WHILE LIT · %04.1f` | top-right | −340, +46, −16 | hud.gd:49–53, 174 |

Reading: the reference puts contract-critical text in the TOP-RIGHT corner (tally lamp, TBC, sheet) and the bottom-right (captions); those are the corners a streaming overlay most often occupies. The canon gives no margin number anywhere (grep of all docs for "safe margin" hits only STUDY §II/§ADOPTIONS and MATRIX §STREAMER, none with a value).

### 2.2 What streamer mode is NOT (by law)

1. Not a fear dial: "BRIGHTNESS: none needed and none offered as a fear-dial" [MATRIX §VISION]; streamer mode changes no lighting, no exposure, no EV [LIGHT line 14: "AUTO-EXPOSURE OFF: locked EV per room-state"].
2. Not photo-safe and not TBC: those persist in the SAVE and are diegetic instruments [ACCESS-SPEC §1.1 "Not settings (do not move them)"]; streamer mode is a settings-slot booth row and touches neither `tbc` nor `photo_safe`.
3. Not a compound post effect [ART line 8, 34].
4. Never a Law 8 lie: the capture-clean toggle redacts visibly (§2.3 c).
5. Never a Law 10 breach: tally lamp, countdown, cool toast, ON AIR clock, captions and the pause menu are exempt from hiding [LAWS line 10–11; MATRIX §COGNITIVE "toasts queue and never overlap"].

### 2.3 UE plan — three controls, one settings row each

**(a) Compression-kind grain.**
- Where: inside the tape material function stack only [MIGRATION line 9], on the noise-floor and dot-crawl terms of the ladder [crt_tape.gdshader:35–41]; the chroma shift, scanlines, tracking band, head-switch and vignette terms are untouched, so the two-worlds read and the generation grammar survive [ART line 8].
- Mechanism: a new scalar `StreamerGrain` (0/1) in the same Material Parameter Collection that carries `generation`, `tbc_on`, `photo_safe` [MIGRATION line 9]. When 1, the per-pixel white-noise hash (`hash2(uv * (200 + 40g) + t·…)`, crt_tape.gdshader:36) is replaced by a coarser, temporally coherent grain: the noise is sampled on a lower-frequency lattice and held across frames, so that an encoder's macroblocks are not fed a new random field every frame. That is the only meaning "compression-kind" is given anywhere in canon ("Grain and CRT mash under compression" [STUDY §II]); the numbers are not in canon.
- STAND-IN parameters (source: none in canon; these are the author's proposal from the shader's own constants, to be tuned by the Mac lane under an encoder — §2.5): lattice frequency 200 + 40g → 48 + 8g (¼ the reference density); temporal hold 1 frame → 4 frames at 60 fps; amplitude unchanged (`0.03 + 0.06g`, crt_tape.gdshader:37) so the ladder's generation read is preserved; dot-crawl amplitude `0.014·(0.5+g)` (line 41) halved. Every number here is STAND-IN and is listed in §6 R2.
- Interaction with photo-safe: photo-safe already halves the noise term and zeroes crawl, band and tear (crt_tape.gdshader:37, 41, 46, 49); streamer grain composes with it (multiplies, never overrides) so a viewer with both on sees the quieter of the two. The FLICKER AND GRAIN REDUCTION slider [MATRIX §VISION], when it exists, drives the same amplitude term; streamer grain drives frequency and coherence. Two rows, one function.
- Not applied to: the seance frames' seeded grain — "I20 The same frame is always the same frame. LAW: seance frame idx renders identically forever (seeded grain)" [INV line 32]; `frame_sequence.gd:46` "the same frame is always the same frame". Streamer grain must not touch the seance substrate [MIGRATION line 11: "the wear ladder stays a material parameter"]. Listed in §6 R3 for the owner to confirm the exemption.

**(b) Overlay-safe HUD margins.**
- Mechanism: one `USizeBox`/`UCanvasPanel` inset applied to the HUD's root canvas (the UMG equivalent of the reference `HUD` full-rect Control, main.tscn:73–75) when `StreamerSafeMargins` is on. Every element in the §2.1 table keeps its anchor and moves inward by the inset; the binder (centre) and the retake/end-card overlay (full-rect, centred lines) are unaffected by construction.
- The tally lamp is the hard case: it is top-right at 16 px [hud.gd:49–53] and it IS the contract [LAWS line 11]. Under safe margins it moves inward with everything else; it never hides, never shrinks below the UI TEXT SIZE floor (0.8, ACCESS-SPEC §1.1) and keeps its outline (ACCESS-SPEC §4).
- Inset value: **OPEN**. No canon number exists. STAND-IN, clearly external: the broadcast convention of a 90 % action-safe and 80 % title-safe area (SMPTE ST 2046-1 / EBU R95 practice), i.e. a 5 % inset per edge for everything and 10 % for text the streamer's own overlay must not cover. The station diegesis makes the broadcast convention a natural fit, but that is an argument, not canon. §6 R4.
- Captions: the strip is bottom-right [hud.gd:39–44]; under safe margins it moves inward like every other element and additionally may be re-anchored bottom-centre (the conventional caption position) — OPEN, §6 R4, because MATRIX §HEARING adds "left and right directionality tags", which a centred strip serves better than a right-aligned one.

**(c) Capture-clean toggle.**
- Canon purpose: "capture-clean toggle that hides spoiler text in the binder" [MATRIX §STREAMER].
- What the binder shows in the reference: page one "lists the ledger or NO ENTRIES. KEEP IT SO." [README Commit 039 via docs/BUILD-LOG.md line 183]; the binder is the inventory and the journal [PLAN §1 gap-audit rulings: "binder IS the inventory"]; the ending words, the decision ("ENTRY STANDS: …", game_state.gd objective_text) and the objective line are HUD, not binder.
- The nearest canon list of what counts as a spoiler is the presence spec: "Never: any ending name, DEAD AIR, the seance, the quiet room, the dock's contents, the once-ever moment, day numbers past 5." [PRESENCE §SPOILER RULES]. Proposal: capture-clean hides exactly that class wherever it appears in the binder and in the objective line — the casualty ledger page, the decision line, ending names, seance/dock/quiet-room references, the day number past 5 — and replaces each with a visible redaction in the ledger's register (STAND-IN string: `[REDACTED FOR BROADCAST]`, no canon string exists; §6 R5).
- What it never hides (Law 9/10 exemptions): the tally lamp and countdown, the ON AIR/BREAK clock, the sheet (strikes), captions, toasts that announce the cool ("The tally cools." rundown.gd:275; GT 578), prompts, the pause menu, the booth.
- Casualty stamps and the ledger reading at credits (CL-7): capture-clean does NOT suppress THE LEDGER, READ ALOUD — it is an ending sequence, not the binder, and QA-47 requires it [QA line 71]. A streamer who wants the reading off camera ends the capture; the game does not lie about its own ending. §6 R5 asks the owner to confirm.

**(d) Booth rows and settings.**
- Extend `URestorationSettings` (ACCESS-SPEC §1.1) with three booleans, all default false, persisted in the `"settings"` slot, never in the save:

| Proposed UE property | Godot section.key (none exists; proposed for `settings.cfg` parity) | Default | Applies to |
|---|---|---|---|
| `Access_StreamerGrain` | `streamer.grain` | false | MPC scalar `StreamerGrain` |
| `Access_SafeMargins` | `streamer.safe_margins` | false | HUD root inset |
| `Access_CaptureClean` | `streamer.capture_clean` | false | binder + objective redaction |

- Booth placement: after `ASSIST …` (row 10) and before `REMAP …` (row 11) in the ACCESS-SPEC §2.2 order — one header `STREAMER` and three check rows, or a single `STREAMER MODE` check that sets all three. Canon names ONE mode with three properties ("we add a streamer mode (compression-kind grain, overlay-safe HUD margins)") [STUDY §II], so a single row is the faithful reading; three rows is the accessible reading (a streamer may want margins without grain). **OPEN**, §6 R6. Label strings: none exist in GT (grep `STREAMER` = 0 rows); OPEN, §6 R6.
- Every change writes immediately, no Apply button [ACCESS-SPEC §2.2].
- Ships in the DEMO build: yes — the booth ships in every build [LAWS line 10] and the study's precedent is precisely "TJOC shipped a bitrate-friendly setting in a DEMO" [STUDY §II].

### 2.4 Data

- MPC: add `StreamerGrain` beside `generation`, `tbc_on`, `photo_safe` [MIGRATION line 9].
- Settings: three keys above; `tools/extract_data.py` gains nothing until the strings are ruled (§6 R6), then the booth labels join GT.
- No CSV, no save field, no telemetry.

### 2.5 Acceptance

- `Restoration.Streamer.GrainOnlyOnTape` (headless, HighResShot): capture one frame of the look-dev level with a bench monitor in view, streamer grain off then on; assert pixel variance in a compound-surface region is unchanged (tolerance 0) and in the monitor region is changed. Enforces ART line 8.
- `Restoration.Streamer.SeanceFrameStable` (I20 extension): with streamer grain on, render seance frame 14 twice across relaunches; diff = 0 [INV line 32].
- `Restoration.Streamer.SafeMarginsGeometry`: with safe margins on, walk every HUD widget's cached geometry and assert it lies inside the inset rectangle; assert the tally lamp is visible while `bRecording` [RestorationState.h:131].
- `Restoration.Streamer.CaptureCleanNeverHidesContract`: force `bAfActive && bRecording`, capture-clean on; assert the tally widget's visibility and text `● REC · SAFE WHILE LIT · %04.1f` [GT 225]; force a casualty, open the binder; assert the ledger page renders the redaction string and NOT the casualty's `who`/`cause` [RestorationState.h:101].
- `Restoration.Streamer.SettingsRoundTrip`: extend ACCESS-SPEC §2.4's round-trip test with the three new booleans.
- The bitrate proof (the point of A1): **OPEN as a method** — no canon states a target bitrate, codec or metric. STAND-IN: record 30 s of the bench capture (CL-3's fixture, §3.3) via Movie Render Queue at 1080p60, encode with the platform's H.264 at 6 Mbps (Twitch's documented ceiling for non-partners at the time of writing; external, not canon), compute SSIM of the monitor region against the uncompressed MRQ frames with grain off vs on, and record both numbers in the ledger. Ship the grain only if on ≥ off. §6 R2.
- Visual: the Mac lane looks at the monitor under streamer grain at 1 m and gameplay distance [PLAN §R item 5] and confirms the ladder still reads as generation loss, not as a filter.

### 2.6 Schedule

- BUILD-ORDER puts "booth complete" in P6 [BUILD-ORDER P6]; PROGRESS puts streamer mode at 5.6, after 5.2 (booth) — consistent. The MPC scalar can be added when the tape material function is built (MIGRATION line 9; PROGRESS Phase 0/3 monitor work), at no cost, so that 5.6 is a booth row plus a tuning pass rather than a shader rewrite. Proposal only; nothing here edits PROGRESS.

---

## 3 · UNIT 5.7 — THE CLIP LEDGER (study A4)

### 3.1 Canon

- The source of record, verbatim: "Thirty seconds, one frame legible, arc complete: that is the unit of spread. Exit 8's single hallway is clip-perfect by design. Our engineered clippables, named so trailers and creators find them: the first doorway fold; THE TALLY COOLS with him standing in it; the countdown expiring at SAFE WHILE LIT; the bell; the dossier's WARNING page; Harriet doubled at the break; THE LEDGER, READ ALOUD. Demo-first (Tape 1) is the FNAF-proven top of funnel and stands." [STUDY §V]
- Adoption: "A4 Clip ledger adopted into trailer beats (this section is the source of record)." [STUDY §ADOPTIONS]
- The unit's acceptance: "each verified capturable in ≤30s with one legible frame" [PLAN §5 5.7].
- The trailer's own cut laws bind any clip the studio publishes: "No footage of any ending. No Leland. No glimpse. Nothing unmediated moves except people being kind." [TRAILER §CUT LAWS]; "Nothing from the dead room, the readings, or any death scene ships in marketing; graves are not previews." [TRAILER §ADDENDUM]; the trailer already adopted two ledger entries: "the dossier's WARNING panel as the final still" and "the countdown UI over an approach, cut on THE TALLY COOLS" [TRAILER §ADDENDUM].
- Community rule that applies to any clip captioning or posting: "Chum does not have an account, does not post, and is never quoted in first person online, for the same reason the bell is silent." [ARG §RULES OF PLAY]
- The dread test each entry must pass: "REPETITION: still unsettling the fifth time? (Startles fail this; the fold passes.) LAW: does it break the budget or any contract? (Auto-reject.) EARNED: does the player's own attention or choice produce it?" [DREAD line 15]
- Animation-unit verification rule the fixtures inherit: "Animation units: capture sequences (≥8 frames or MRQ clip), review motion." [PLAN §4]

### 3.2 The ledger

Seven entries, the study's order. "Arc" is the ≤30 s shape (setup → turn → the frame). "Frame" is the one legible still. "Demo" says whether the Tape 1 build can reach it (§4). "Marketing" applies the trailer cut laws to the studio's own use; creators are not bound by them.

| # | Clippable (STUDY §V name) | Where / when | Reference trigger (CODE) | UE home | Arc, ≤30 s | The one legible frame | On-screen text (GT row) | Sound | Laws | Demo | Marketing |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CL-1 | **the first doorway fold** | Any of the 20 door positions the builder hands the Rundown (README Commit 036 via BUILD-LOG line 178); the FIRST fold a player sees is authored to happen in the taught chase, TAPE LIBRARY, first post-wake capture: "Two doorways stand between you and anywhere. Use them." [AF line 29] | `rundown.gd:333–345` `_door_fold_check`: within `AF_DOOR_NEAR` 1.0 m of a door, 6 s per-door cooldown, `_fold_t = AF_FOLD_SECONDS` 2.2 [TIMINGS], `Sfx.thunk`, caption, close-range toast ≤12 m | `Rundown.cpp:195–213` `DoorFoldCheck` (2.2 s toll; **no caption, no thunk, no toast** — ABSENT, AUDIT §rundown) | 0–10 s: he approaches a doorway at 0.8 m/s with the eye lit (capture running) or dark (night); 10–12.2 s: the fold — "he compresses, ducks, pulls the arms in" [rundown.gd:459–461], "shoulder first, head late on an impossible hinge" [PLAN §1 Motion law]; 12.2–30 s: the player's counterplay, two rooms gained | Mid-fold: 3.35 m of him bent inside a 2.2 m door leaf [ROOM-BRIEFS 3.1 §0.1 OPEN 0-A on leaf height], eye on the player | `[IT FOLDS THROUGH THE DOORWAY]` (GT 586); toast `A doorway. It stops, and bends, and keeps its eye on you the whole way through.` (rundown.gd:345) | S18 THE FOLD "dry frame creak, 2.2 s envelope, no sting" [AUDIO line 61] | 11; DREAD "the fold passes" | No (no Rundown in DEMO: `world_builder.gd:572–574`) | Yes — chase legs are trailer-safe [TRAILER §ADDENDUM]; the REACT F-R1 cue ("HE POINTS AT THE DOORWAY seconds before the first fold") is part of the arc if the FM is alive [REACT line 14] |
| CL-2 | **THE TALLY COOLS with him standing in it** | Bench room, capture just ended or aborted with him at the 1.2 m loom, day (the cool branch is `not is_night`, rundown.gd:270) | `rundown.gd:270–285`: `_af_cool = 4.0` first time with the teaching line, `AF_COOL_SECONDS` 2.0 after; at ≤0 strike if within `_strike_r + 0.4`, else withdrawal | `Rundown.cpp:313–325` (`AfCoolSeconds` 2.0, taught 4.0; log `AF tally cools (taught)` / `AF tally cools`) — present | 0–12 s: capture runs, lamp lit, he arrives at 1.2 m and looms [AF line 13–14]; 12 s: capture ends, eye goes dark "the instant it stops" [QA-35]; 12–14 s (or 16 s first time): the cool, toast up; then the strike ("nearly silent" [PLAN §1 Audio law]) or the withdrawal ("reverse along the exact approach path, motion played backward" [PLAN §1]) | Him at 1.2 m, eye DARK, the toast on screen, the lamp gone | `THE TALLY COOLS. Two doorways stand between you and anywhere. Use them.` (GT 578) first time; `The tally cools.` after (rundown.gd:275) | Withdrawal: no sting; strike: nearly silent [PLAN §1]; occlusion bloom <3 m [AUDIO/PLAN §1] | 10, 11 | No | Yes — TRAILER §ADDENDUM already cuts on THE TALLY COOLS |
| CL-3 | **the countdown expiring at SAFE WHILE LIT** | Bench room, any capture with him awake (`af_active && recording`) | `hud.gd:172–176`: `● REC · SAFE WHILE LIT · %04.1f` from `GameState.recording_left`, capture 12.0 s [TIMINGS `CAPTURE_SECONDS`]; both stop paths clear the flag (BUILD-LOG line 176) | `BenchCapture.cpp:50–54, 98–127` (`CaptureSeconds` 12, `Tether` 4 m, `RecordingLeft`) — present; HUD lamp ABSENT (UMG not built) | 0–12 s: the whole capture; the arithmetic is the design — "he is 9 meters out, moving at 0.8, I have 7.4 seconds of protection and 11 seconds of tape. Finish, abort, or meet him." [AF line 14]; 12 s: `00.0`, lamp off, eye off; the clip ends on CL-2's first second | The lamp reading a single digit with him filling the doorway behind the bench | `● REC · SAFE WHILE LIT · %04.1f` (GT 225); `CAPTURE · TAPE %d · 00:%05.2f` (capture_bench.gd:37) | S17 footfalls on interval [AUDIO line 61]; tape hiss | 10 | No (capture runs in DEMO but `af_active` is never set: the fire tape and the Rundown are stripped, `world_builder.gd:390, 572`) | Yes — the countdown UI beat [TRAILER §ADDENDUM] |
| CL-4 | **the bell** | The finale, after the live premiere resolves to a sign-off route (not `caught`, `one_woman`, `signoff_4c`, `dead_air`: hud.gd:436–452) | `hud.gd:452–453`: `Sfx.bell()` then `Fifty years silent.` / `The bell rings once, three feet behind camera position.`; `sfx.gd:16–17` captions `[THE BELL RINGS · once]` | ABSENT (finale not ported; PN-FINALE is C11's, PR #19) | The clip must start ≤30 s before the strike inside the sign-off sequence: the last cue line → bell → 2.8 s card → `CAMERA ONE · SPACE · deliver the line` | The caption card `[THE BELL RINGS · once]` over the studio, or the two lines at GT 306–307 | GT 306, 307; caption from sfx.gd:17 | S06 "one real brass handbell strike … single take, never reused anywhere" [AUDIO line 21]; VISUAL BELL "blooms the screen edge once" [MATRIX §HEARING] | 5 (once per run; a fixture may ring it once per session and never loop it) | No | **No footage of any ending** [TRAILER §CUT LAWS] — the bell is INSIDE an ending sequence. The trailer uses the S06 SAMPLE over black at 1:26, not footage. The studio may publish the sound, not the scene; creators may clip it. §6 R7 |
| CL-5 | **the dossier's WARNING page** | D11 `PEAK ASSET DOSSIER · CHUM-AF-1974-P`, master control, readable from Day 4 (`world_builder.gd:1174`: day 4; "D11 Peak dossier readable Day 4 master control" [BUILD-LOG line 176]); "becomes a findable document (D11, Peak security office copy) after first sighting" [AF line 8] | `ReadableProp` pages, world_builder.gd:1175–1177: three pages, 3.2 / 3.6 / 3.6 s | ABSENT (readables are Landmarks.csv territory, C7) | 0–10 s: the walk to the desk; 10–20 s: the three pages; the third is the frame | The dossier art's WARNING panel — `⚠ WARNING · DO NOT APPROACH ALONE. SUBJECT IS SENTIENT, OPPORTUNISTIC, AND UNPREDICTABLE. REPORT ALL SIGHTINGS TO PEAK SECURITY.` [DOSSIER-ART, bottom-right panel, read by eye] — **which the in-game readable does not render**: the reference shows three TEXT pages whose third reads `Handwritten beneath: he works his own jaw. Count the hands. Report all sightings to Peak Security. HE REMEMBERS THE AUDIENCE.` (GT 715). The clippable frame in canon is the art panel; the code shows prose. §6 R8 | GT 715 and the two pages before it (world_builder.gd:1175–1176; GT keys adjacent) | Page-turn only; no sting | 3 is untouched (the dossier is not the fire-corridor moment); "a document about him is not him" [AF line 20] | No | Yes — "the dossier's WARNING panel as the final still" [TRAILER §ADDENDUM]; the art "is shippable as-is … a Steam capsule candidate" [AF line 20] |
| CL-6 | **Harriet doubled at the break** | Rec room, her chair, the BREAK after the player splices a reel carrying her segment (`h2_pending`) | `harriet.gd:100–108`: toast `The break comes. Harriet freezes, and one frame later, freezes again, an inch to the left.` → 2.8 s → toast `Doubled at the shoulders. Both mouths open on different vowels. The teacup rises in two hands at two heights.` → caption `[ONE FRAME LEFT OF HERSELF]` → `_splice_visual` (ghost rig +0.13 m x, +0.06 rad, harriet.gd:29–33) → `mark_casualty HARRIET H2` | `Harriet.cpp:33` "the slip-arming and H1/H2 flows land with the presentation half" — ABSENT (AUDIT §9 H2/H3) | 0–10 s: ON AIR, she sways, cup high; 10 s: BREAK, the tallies die together [LIGHT line 8]; 10–13 s: the freeze, then the second freeze; 13–16 s: the double resolves; the clip ends on the caption | Two Harriets an inch apart, "both mouths open on different vowels, the teacup rising in two hands at two heights" [CASUALTY §HARRIET via CAST-BUILD-BRIEFS line 214] | GT rows for the two toasts and the caption (harriet.gd:102, 104, 105) | "no sound worth naming" is the rec room's chairs law [AUDIO S10]; the splice itself: OPEN in AUDIO (no S-number names it) | 6 (BREAK is mechanical), 7 (a signature death: "the schedule stopped scheduling her", harriet.gd:107) | No (casualties are demo-whitelisted: `game_state.gd:518–523`) | **No** — "any death scene" [TRAILER §ADDENDUM]; H2 is a casualty. The M-R5 aftermath (the second teacup retired) is set dressing and may show. §6 R7 |
| CL-7 | **THE LEDGER, READ ALOUD** | Every ending's credits when the ledger has anything in it [QA-47] | `hud.gd:348–356`: `THE LEDGER, READ ALOUD, because that is what ledgers are for:` 2.4 s, then per casualty `who · cause` / `line` 2.6 s (+2.4 s `HER CARD, HER OWN STAMP REGISTER: TRANSITION UNRESOLVED.` after HARRIET), then `THE 58 CLUB: fifty-eight, minus N.` 2.6 s | ABSENT (endings not ported) | 2.4 s opener + 2.6 s per entry: a ≤30 s clip holds the opener plus at most ten entries only if none is Harriet; a full ten-death ledger runs ≈ 31.4 s + rows. "Arc complete" therefore means opener → first entries → the fifty-eight line, and a clip may not fit every name. §6 R9 | `THE LEDGER, READ ALOUD, because that is what ledgers are for:` on the retake overlay, phosphor on black | GT 266; `fifty-eight, minus %d.` (hud.gd:356) | "the ledger reading at credits is unscored" [AUDIO line 61] | 7 ("the binder names it"); 5 (Chum is never an entry) | No (casualties and `finale_done` are whitelisted out) | **No** — an ending [TRAILER §CUT LAWS]. Creators will; that is the design ("named so trailers and creators find them") |

Not on the ledger, and why: the in-tape lunge (Tape 1) is the game's ONE STARTLE [LAWS line 2] and the trailer's [TRAILER 1:05]; it is the demo's closing beat (§4) and is clippable by every demo player by construction, but the study does not list it among the "engineered clippables" and this spec does not add to a canon list. The glimpse, the dead room, the readings and every death scene are marketing-barred [TRAILER §ADDENDUM]. The once-ever moment is barred from everything [LAWS line 4].

### 3.3 Verification fixtures (the Mac lane runs these; the cloud cannot)

Pattern: `ue/pyscripts/test_state_af.py` (force state through the actor's `bTest*` properties, simulate, read `Saved/decision_log.txt`) plus `capture_gate.py` (place, frame, HighResShot). Each fixture is one script, `ue/pyscripts/clip_<id>.py`, that:

1. Loads the look-dev level and forces the entry's state (table above) through existing test properties where they exist (`bTestForceAF`, `bTestForceRecording`, `TestRecordingOffAfter` — test_state_af.py:22–26) and new ones where they do not (a `bTestForceHarrietH2`, a `TestForceEnding` — proposals, not canon).
2. Starts a wall clock at the first player-visible setup beat and captures ≥8 frames or an MRQ clip [PLAN §4] through the frame.
3. Asserts: (i) the frame's on-screen text equals the GT row named in the table (string-table lookup, `URestorationText::Tr`, ACCESS-SPEC §1.2); (ii) elapsed ≤ 30.0 s from setup to frame; (iii) the log line the entry owns exists exactly once (`AF tally cools` for CL-2, Rundown.cpp:319–323; a fold log line for CL-1 — **ABSENT today**, Rundown.cpp:195–213 logs nothing; propose `AF fold door=%d` in the parser format [PORT-BRIEF §telemetry]); (iv) for CL-4, the bell fired once per session (I14's grep of the event table [INV line 22] extended to S06).
4. Writes the frame to `chum-clip-<id>-current.png` for the Desktop copy step [PLAN §0 rule 5] and prints `CLIP-<id>-OK t=<s>`.

Fixture-specific notes:
- CL-1 needs a door position list on the actor (`DoorPositions`, Rundown.cpp:201) and a spawn 1.5 m from a doorway with the prey beyond it.
- CL-2/CL-3 share one fixture: the AF capture end to end already in test_state_af.py (recording off after 14 s → cool → `STRIKE af tally-cool`); add the HUD widget assertion once the tally lamp exists in UMG.
- CL-4, CL-6, CL-7 cannot run until P5 (finale, casualties, endings) is ported [BUILD-ORDER P5]; the fixtures are written against PN-FINALE / C11 when it merges. Until then the entries are verified on the Godot reference (`scenes/soak.tscn` harness, PLAN §1) — that is a legitimate step 5 of the verification loop "only while the Godot game is still the live spec for the ported system" [PLAN §4].
- CL-5 needs a ruling first (§6 R8): the fixture asserts either the art panel or the GT 715 page.

### 3.4 Data

- No new CSV. If the owner wants the ledger machine-readable for the trailer/creator kit, a `docs/press-kit/CLIP-LEDGER.csv` (id, name, room, day, gt_row, marketing_ok) is a one-line export of the table above — proposal, not part of this deliverable (one file per unit).
- Each entry's strings are already in GT (rows named in the table); no new keys.

### 3.5 Acceptance for the unit

Unit 5.7 ticks when all seven fixtures print `CLIP-<id>-OK` with `t ≤ 30`, the seven frames have been looked at [PLAN §0 rule 4] and pass the realism bar next to the canon plate [PLAN §R], and the ledger paragraph records the seven timings. Entries blocked on P5 are ticked on the reference harness with the UE fixture filed as a sub-box (proposal, §6 R10).

---

## 4 · UNIT 5.8 — DEMO: TAPE 1 (study A6, "the funnel")

### 4.1 Canon

- "A6 Demo scope reaffirmed as the funnel." [STUDY §ADOPTIONS]; "Demo-first (Tape 1) is the FNAF-proven top of funnel and stands." [STUDY §V]; "FREE-FIRST ENTRY and short runtimes made every streamer a distributor." [STUDY §I item 6]; "Their brevity lesson lands on the demo: Tape 1 should feel like a complete Puppet Combo-sized night, whole in an evening, honest about wanting more." [STUDY-ADD line 30]
- The cut, whole: DEMO-PLAN §1–7 — shape (Day 1 only; arrive → dresser → S1 → mini-screening → capture → lunge → bars → RESPOND sign → END CARD; 25–40 min, speedrun floor ≈12), boundary (IN / LOCKED / OUT / TEASED), the ending moment (exact timings), save carry and anti-spoiler guarantees, the engineering delta E1–E10, the QA probes DP1–DP5, and what the demo sells.
- Release model: "shipping it free as a demo that ends on the in-tape lunge and the RESPOND sign is a conversion machine" [`docs/production/restoration-build-plan.md` line 24].
- Marketing surfaces that already promise it: "DEMO POSITIONING: Tape 1 ships free as the demo, ending on the in-tape lunge and the lit RESPOND sign. The demo save carries into the full game, ledger and all." [STEAM-PAGE line 21]; trailer end card `TAPE 1 FREE DEMO · WISHLIST ON STEAM` [TRAILER 1:20]; ARG A3 "The demo ships the same week" as the recovered-reel audio drop [ARG §PHASE 2].
- Meta parity: "the demo build ships with achievements disabled entirely, matching the save whitelist's spirit; nothing meta leaks forward either." [ACH §DOCTRINE]; the presence bridge "is absent under DEMO" [PRESENCE §HOOKS]; the demo card is a popup-free zone [ACH §DOCTRINE 1].
- The port contract: "The save is a USaveGame object mirroring _save_dict() in game_state.gd, version 16, including the DEMO whitelist behavior." [PORT-BRIEF §3]; "P6 · Meta and modes: achievements with deferral, DEMO flag with whitelist, booth complete, captions, pause, string table wired. Done: QA-01 to QA-04, QA-17, QA-29, QA-30, QA-32" [BUILD-ORDER P6]; PN-STATE §5 (the stripped keys, verbatim); PN-SCREENING line 434–438 (the screening is in the demo; judged by ASSIST only).
- Acceptance already written: "QA-30 DEMO true: only the seven rooms open, doors carry demo reasons, bed declines, S1 and S5 only, card protects three seconds, completed demo save contains none of the whitelisted-out fields, funnel file has six marks." [QA line 50]; "QA-48 Demo build: no death is reachable, no casualty field survives in the save, achievements stay dark." [QA line 72]
- The reference implementation landed as README Commit 027 ("the cut plan's E1-E10, in the box") [README lines 39–47].

### 4.2 Code is the intent — E1–E10 against the reference and the port

| E | DEMO-PLAN §5 says | Reference (CODE) | UE today (AUDIT) | Note |
|---|---|---|---|---|
| E1 | `const DEMO` build-time flag | `game_state.gd:6` `const DEMO := false  ## flip true for the Tape 1 demo build` | ABSENT [AUDIT line 56] | §4.3 (a) |
| E2 | door-reason override table; skip Rundown, FM, dock, crate, seance, cascade, assets, ledger, fire pickup | `world_builder.gd:60` `DEMO_OPEN` (7 rooms); `:262–266` reasons (transmitter variant); `:390`, `:572`, `:976`, `:1010`, `:1114` early returns | `DemoOpen.csv` exists (7 rows, matches) but `build_greybox.py` never reads it (grep `demo` = 0) | §4.3 (b); QA-30 "only the seven rooms open" |
| E3 | bed declines | `bed_prop.gd:13–15` → GT 40 | ABSENT | — |
| E4 | objective ends at "capture Tape 1" | `game_state.gd:688–689` → GT 175 `TAPE 1 · captured. Thank you for careful hands.` | ABSENT | — |
| E5 | capture completion triggers the end sequence | `capture_bench.gd:60–62` `demo_mark("capture_done")`, `demo_ended.emit()` | `BenchCapture.cpp:115–122` completes without the DEMO branch [AUDIT line 489] | — |
| E6 | end card scene (reuses title styling) | Not a scene: `hud.gd:361–380` runs the card on the HUD's retake overlay: lock player → 1.6 s → `THE RESPOND SIGN LIGHTS.` / `Alone. Unasked.` 2.0 s → `demo_mark("card")` → GT 273 / 274 → 3.0 s → append GT 275 `(any key)` → any of respond/interact/ui_accept → title | ABSENT (`demo_ended` ABSENT, AUDIT line 258) | **DEMO-PLAN §1 and §3 say "smash cut to the rec room where the RESPOND sign lights" / "cut to rec room camera position (authored)"; the code does NOT cut the camera — it prints the sign lighting as two lines over the current view.** Code is the intent; whether UE authors the camera cut is §6 R11 |
| E7 | title shows TAPE 1 · FREE DEMO | `title.gd:27–28` → GT 642 `TAPE 1 · FREE DEMO · the tower light stays on` | ABSENT | — |
| E8 | save writer whitelist | `game_state.gd:515–524`: erases 15 keys before writing (PN-STATE §5 lists them) | `RestorationState.cpp:151` comment only | §4.3 (c) |
| E9 | funnel telemetry, local file, no network | `game_state.gd:344–356` `demo_mark` → `user://demo_funnel.txt`, `[min %.1f] event` | ABSENT | **Seven marks exist in code**: `started` (game_state.gd:714), `s1_signed` (:187), `screening` (screening_event.gd:70), `capture_start` (capture_bench.gd:32), `lunge` (bench_tv.gd:63), `capture_done` (capture_bench.gd:61), `card` (hud.gd:368). DEMO-PLAN §5 E9 lists seven ("started, S1, screening, capture, lunge, card, minutes"); **QA-30 says "funnel file has six marks"**. §6 R12 |
| E10 | separate Steam demo app id; depot shares the project | No code | No code | OPEN, outside the repo (§6 R13) |

Further prose-versus-code deltas, recorded, code proposed:

- DEMO-PLAN preamble: "The demo save is the full game's save (schema v15)". Code: `SAVE_VERSION := 16` [game_state.gd:7; TIMINGS `SAVE_VERSION,16`]. v16 is the port's contract [PORT-BRIEF §3; PN-STATE]. The plan's number is stale.
- DEMO-PLAN §4: "a demo_complete flag set at the card" and "Full game on first CONTINUE from a demo save: Merle acknowledges it, one line: 'You came back. I told them you would.'" Code: **no `demo_complete` field exists in `_save_dict` (PN-STATE §1 lists 55 fields; none is it) and the line appears in no script and no GT row** (grep = 0). DP5 ("carry test: demo save into full build, Merle's line fires once") therefore cannot pass on the reference. The same line is also ARG A6's mailer text [ARG §PHASE 3]. §6 R14: add the field and the line to the port (a save-schema addition, which the migration map protects — "WHAT MUST NOT CHANGE: … save semantics" — so it needs the owner), or strike DP5.
- DEMO-PLAN §1: "judged gently on Matinee defaults". Code: `mode` is unread by `screening_event.gd`; ASSIST only [PN-SCREENING line 436–438]. Code is the intent.
- DEMO-PLAN §2 TEASED: "the casting sheet visible with zero lines; the dresser's seven items counted". Code: no DEMO branch mentions the casting sheet or the dresser (grep of `world_builder.gd` DEMO branches). Whether those props spawn in the seven open rooms in the reference is not established by this audit — **OPEN-verify** for the Mac lane (§6 R15), not a claim either way.
- DEMO-PLAN §3: "bars hold 1.6 s" — code `hud.gd:365` `_wait(1.6)` and `tape_stage.gd:246–249` bars 1.6 s: agree. "RESPOND sign lights, hum only, 2.0 s" — code `_say(…, 2.0)`: agree (the hum is AUDIO's, not asserted here). "No input during the card for 3 s" — code `_wait(3.0)` before `(any key)`: agree; QA-30 "card protects three seconds".
- DEMO-PLAN §1: "sign S1 (the save-costs-paper lesson, softened: demo paper is S1 and S5 only, three sheets each)" — code `paper = {"S1": 3, "S5": 3} if DEMO` [game_state.gd:719]: agree.
- DEMO-PLAN §2 LOCKED strings — code `world_builder.gd:263–266` → GT 661 (`SEALED · you can hear it from here. That is enough for today.`) and GT 662 (`SEALED · the club opens the rest when the contract is signed.`): agree, with one wording difference: the plan writes the transmitter line as `"You can hear it from here. That is enough for today."` without the `SEALED ·` prefix; code prefixes it. Code is the intent; I08 requires every locked door to state its reason [INV line 14].

### 4.3 UE plan

**(a) The flag — compiled out, not gated.** DEMO-PLAN §4 requires the demo binary to be "INCAPABLE of writing: decision, assets, leland_answers, lockdown, finale, or any ending field: not merely gated, absent from its write path". A runtime bool cannot satisfy "absent". Proposal: a UBT define `RESTORATION_DEMO=1` set by a dedicated target (`RestorationDemo.Target.cs`, same module, same Content), surfaced as `URestorationState::IsDemo()` (`constexpr`), with the fifteen whitelisted-out fields wrapped in `#if !RESTORATION_DEMO` inside `SaveToSlot`'s write path so that the demo build's save writer has no code that can write them. The load path stays whole (a full-game save loaded by the demo is a support case, not a design case — OPEN, §6 R16). Godot's `const DEMO` [game_state.gd:6] is the same idea at GDScript's level of enforcement.

**(b) World from data.** `DemoOpen.csv` (7 rows: REC ROOM, KITCHEN, DORMS, ENTRY, CORRIDOR, TAPE LIBRARY, BENCH ROOM; extracted from `DEMO_OPEN` by `tools/extract_data.py:71–77`) is the whitelist; `build_greybox.py` must, under `IsDemo()`, (i) stamp every Doors.csv row whose either room is not in DemoOpen with `locked:` + GT 662, or GT 661 when either room name contains `TRANSMITTER` [world_builder.gd:262–266], (ii) skip spawning the Rundown/CoverageDirector [world_builder.gd:572–574; PN-BROADCAST §3.1 "The director is null in DEMO"], the docks (fire, seance), the dock task, assets/decision, the night trip, crate and event wave [world_builder.gd:390, 976, 1010, 1114]. The screening projector spawns unconditionally [PN-SCREENING line 434–435]. "The world is BUILT FROM DATA in UE exactly as in Godot" [PLAN §1].

**(c) Save whitelist.** The fifteen keys, verbatim from PN-STATE §5: `decision, assets, leland_answers, lockdown_done, finale_done, ending_reached, lie_pending, seance_wear, has_fire_tape, fire_tape_watched, dock_done, crate_opened, presigned_seen, cascade_done, casualties`. Paper `{S1:3, S5:3}` [RestorationState.cpp:151 already comments it]. `URestorationSaveGame` field numbers per PN-STATE §1 (Casualties is field 46, RestorationState.h:101).

**(d) The end sequence.** `FOnDemoEnded` delegate on the state subsystem (PN-STATE §3 lists `demo_ended` as external-only, emitted by the bench, consumed by the HUD); `ABenchCapture` emits it on clean completion under `IsDemo()` [capture_bench.gd:60–62]; the HUD widget runs the card exactly as hud.gd:361–380: lock Rita (`RitaCharacter` `locked`), 1.6 s, GT 271 / `Alone. Unasked.` for 2.0 s, funnel `card`, GT 273 / GT 274, 3.0 s of ignored input, append GT 275, then any of respond/interact/accept → title. The card is a popup-free zone by construction: achievements are compiled out in the demo (`UAchievements` absent under `IsDemo()`, ACH §DOCTRINE; `achievements.gd:46`).

**(e) Title foot.** GT 642 under the logo when `IsDemo()` [title.gd:27–28]; the first-run booth still opens [title.gd:48–52; QA-01] — the booth ships in every build [LAWS line 10].

**(f) Funnel.** `ProjectSavedDir()/demo_funnel.txt` (Godot `user://` → ProjectSavedDir [MIGRATION §WHAT DOES NOT PORT]); format `[min %.1f] event`; seven events at the seven sites in §4.2 E9; "no network, disclosed in the readme" [DEMO-PLAN §5 E9; README line 46–47]. No analytics SDK, no Steam stats. The bed and every sealed door do not mark (they are not in the reference's list).

**(g) Meta.** Achievements compiled out [ACH §DOCTRINE]; presence bridge compiled out [PRESENCE §HOOKS]; the streamer rows (§2) compiled IN.

**(h) The demo as clip machine.** The demo's last thirty seconds are: capture ends → bars 1.6 s → the sign lights 2.0 s → the card. The one startle precedes them by ≤12 s (the lunge lands in the last 0.12 s of the 12 s capture, `tape_stage.gd:235–240`: hold, then a one-frame ×1.45 scale). A creator's clip of the demo's end is therefore the study's unit of spread by construction ("Thirty seconds, one frame legible, arc complete" [STUDY §V]) and contains the game's one startle, which is the marketing promise ("one jump scare, and it is not the scary part" [STEAM-PAGE §ADDENDUM]). Nothing to build; recorded so 5.8's ledger paragraph can say it.

### 4.4 Data

| Datum | Value | Source |
|---|---|---|
| DemoOpen.csv rows | 7 | DEMO-OPEN; `world_builder.gd:60` |
| Demo paper | `{S1:3, S5:3}` | game_state.gd:719; PN-STATE §1 |
| Capture length | 12.0 s | TIMINGS `CAPTURE_SECONDS`; BenchCapture.h:19 |
| Bars hold | 1.6 s | hud.gd:365; tape_stage.gd:247 |
| Sign beat | 2.0 s | hud.gd:367 |
| Card protection | 3.0 s | hud.gd:371; QA-30 |
| Funnel marks | 7 (see §4.2 E9) | code; vs QA-30 "six" — §6 R12 |
| Whitelisted-out keys | 15 | game_state.gd:518–523; PN-STATE §5 |
| GT rows | 40 (bed), 175 (objective), 271 (sign), 273–275 (card), 642 (title foot), 661–662 (door reasons) | GT |
| Save version | 16 | game_state.gd:7; PORT-BRIEF §3 (DEMO-PLAN's "v15" is stale) |

### 4.5 Acceptance

Mapped from QA-30, QA-48 and DEMO-PLAN §6 DP1–DP5 to fixtures (names proposed):

- `Restoration.Demo.RoomsAndDoors` (QA-30 clause 1–2; DP1): build the level under `IsDemo()`; assert exactly the seven DemoOpen rooms are reachable from ENTRY through unlocked doors and every other door's locked reason equals GT 662 or (transmitter) GT 661; no empty reason (I08).
- `Restoration.Demo.BedDeclines` (QA-30 clause 3; E3): interact bed → toast GT 40; day unchanged.
- `Restoration.Demo.Paper` (QA-30 clause 4; DP4): fresh game → paper `{S1:3,S5:3}`; sign S1 three times → S1 refused, S5 still signs (no softlock).
- `Restoration.Demo.CardProtects` (QA-30 clause 5; DP3): trigger `FOnDemoEnded`; inject respond/interact/pause for 2.9 s → still on card; at 3.1 s → title. Movement locked throughout.
- `Restoration.Demo.SaveWhitelist` (QA-30 clause 6; QA-48; DP2): complete the demo, then force every one of the fifteen fields non-default through the test setters and `SaveToSlot`; read the slot raw; assert none of the fifteen keys is present (absence, not default). Under `RESTORATION_DEMO` the test additionally asserts by compile: the write symbols do not exist (a `static_assert` or a build-graph grep of the demo binary's strings).
- `Restoration.Demo.Funnel` (QA-30 clause 7): after a scripted run, `demo_funnel.txt` has one line per event in the order `started, s1_signed, screening, capture_start, lunge, capture_done, card` (seven; if the owner rules six per QA-30, the test changes with the ruling, §6 R12).
- `Restoration.Demo.NoDeath` (QA-48): soak the demo world 60 min with the WANDERER bot [INV line 37]; assert zero strike/death log lines and no Rundown actor.
- `Restoration.Demo.MetaDark` (QA-48; ACH): assert no achievement subsystem, no presence bridge, in the demo target.
- `Restoration.Demo.Carry` (DP5): **blocked** on §6 R14 (no field, no line).
- The realism bar for the demo is the whole realism bar: the demo is the store page [PLAN §R]. The 60-min packaged soak of 5.5 runs again on the demo target (proposal).

### 4.6 Schedule

- BUILD-ORDER P6 holds the DEMO flag; PROGRESS 5.8 is the demo unit. The flag, the whitelist and the DemoOpen stamp in `build_greybox.py` are cheap to land early (they are data and `#if`), and P2 "State and saves … QA-31" cannot fully claim "including the DEMO whitelist behavior" [PORT-BRIEF §3] without them. Proposal only (§6 R17); nothing here edits PROGRESS.

---

## 5 · CROSS-CUTTING

- Streamer mode ships in the demo (§2.3 d) — the TJOC precedent is the reason the feature exists [STUDY §II].
- Capture-clean has nothing to redact in the demo: the fifteen spoiler fields do not exist in its save and the ledger page reads `NO ENTRIES. KEEP IT SO.` The toggle still ships (Law 9; one booth).
- The clip ledger's seven entries are all full-game (§3.2 Demo column); the demo's clippable is the one startle (§4.3 h). A creator kit that lists the seven must not list the lunge as a scare to hunt: "any ping confirms the moment, teaches hunting" is the meta-silence reasoning for the glimpse [ACH §DOCTRINE 2] and the study's refusal of "jumpscare kill-loop retention" [STUDY §REFUSALS] applies to marketing copy too.
- Chum's name appears in no streamer-mode string, no clip caption the studio writes, no demo card [LAWS line 6; PRESENCE §SPOILER RULES; ARG §RULES OF PLAY]. The reference's demo strings comply (GT 40, 175, 271, 273–275, 642, 661–662: none names him).

---

## 6 · GATE RULINGS NEEDED (the owner decides; the loop does not)

R1. **Tracker nit.** PROGRESS 5.6 omits the capture-clean toggle that PLAN 5.6, STUDY A1 and MATRIX §STREAMER all name. The Mac lane may add it to the box text when it ticks C16 (this spec cannot edit PROGRESS).

R2. **Streamer grain numbers and the bitrate method.** Canon says "compression-kind" and nothing more. Approve the §2.3 (a) STAND-IN lattice/hold values as a starting point and the §2.5 STAND-IN measurement (1080p60, H.264 6 Mbps, SSIM on the monitor region), or supply a target.

R3. **Seance exemption.** Confirm streamer grain never touches the seance frames (I20) — proposed here from the invariant, not stated in the study.

R4. **Safe-margin inset.** No canon number. Approve the broadcast convention STAND-IN (5 % / 10 %) or supply one. Rule also whether captions re-anchor to bottom-centre under safe margins (MATRIX §HEARING's directionality tags argue for it).

R5. **Capture-clean scope and string.** Approve the PRESENCE §SPOILER RULES class as the redaction list, the visible-redaction rule (Law 8), the exemption list (Law 9/10), the STAND-IN string `[REDACTED FOR BROADCAST]`, and that THE LEDGER, READ ALOUD is never suppressed.

R6. **Booth rows.** One `STREAMER MODE` check (the study's single-mode reading) or three checks (grain / margins / capture-clean). Supply the label string(s); none exists in GT.

R7. **Marketing-barred ledger entries.** CL-4 (inside an ending), CL-6 (a death scene) and CL-7 (an ending) are barred from studio marketing by TRAILER's cut laws while the study names them as "engineered clippables … so trailers and creators find them". Confirm the reading here: creators may, the studio's own trailers may not (the S06 sample over black is the trailer's only bell).

R8. **CL-5's frame.** The study names "the dossier's WARNING page"; the art's WARNING panel exists only in the PNG; the in-game D11 readable shows three text pages (GT 715 is the third). Rule: does the UE readable render the dossier art (the panel legible at 1 m) or the text pages? The clip fixture asserts one or the other.

R9. **CL-7 and the 30-second unit.** A full ledger overruns 30 s. Rule that "arc complete" for CL-7 means opener → entries → `fifty-eight, minus N`, and that a clip need not fit every name; or shorten the per-entry dwell (2.6 s, hud.gd:352) — a timing change to an ending, which the migration map protects ("every knob number").

R10. **P5-blocked fixtures.** CL-4, CL-6, CL-7 cannot be verified in UE before the finale and casualties port. Approve verifying them on the Godot harness for 5.7's tick with a UE sub-box filed, or hold 5.7 until P5.

R11. **The demo's camera cut.** DEMO-PLAN §1/§3 cut to an authored rec-room camera for the sign; the code prints the sign lighting over the current view. Code is the intent by default; say whether UE authors the cut (a Phase 5 dressing decision) or keeps the text beat.

R12. **Funnel mark count.** Code writes seven marks; QA-30 says six; DEMO-PLAN E9 lists seven. Rule seven (code) and correct QA-30, or name the mark to drop.

R13. **Steam demo app id** (E10) — outside the repo; record the decision in the ledger when made.

R14. **Save carry (DP5).** No `demo_complete` field and no Merle carry line exist in code or GT. Add both to the port (a save-schema addition; the migration map protects save semantics, so this is the owner's) or strike DP5 and the STEAM-PAGE sentence "The demo save carries into the full game, ledger and all" keeps only its literal truth (the file loads; nothing acknowledges it).

R15. **TEASED props** (casting sheet with zero lines, the dresser's seven items) — not established either way by this audit; the Mac lane verifies on the reference before 5.8.

R16. **Full-game save loaded by the demo binary.** Unspecified everywhere. Proposed: the demo loads it whole and simply cannot write the fifteen fields back; or refuse with a toast. Owner's call.

R17. **Schedule.** Land the flag, whitelist and DemoOpen stamp with P2/P6 groundwork rather than at 5.8, so PORT-BRIEF §3's "including the DEMO whitelist behavior" is true when P2 claims it.

---

## 7 · WHAT THIS SPEC DOES NOT DO

It edits no tracker, ledger or plan [PLAN §0 rule 0]. It ran no engine, no encoder and no capture. It adds no canon: every number not cited is marked STAND-IN with its source, and every silence is OPEN. Its citations are line-checked by the script whose output is in the C16 PR body (`## Verification`).
