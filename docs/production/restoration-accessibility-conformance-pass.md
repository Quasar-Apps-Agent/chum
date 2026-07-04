# RESTORATION · ACCESSIBILITY CONFORMANCE PASS v1
Internal conformance pass and remediation plan. This is not a VPAT/ACR and makes no procurement-grade claim; it exists so that when an ACR is eventually authored, every row traces to evidence. Method per the compliance skill: test a frozen build, document it, remediate separately, retest before updating any claim.

BUILD UNDER TEST (frozen): restoration-godot v0.9, commit 028, file restoration-godot-v0.9-complete.zip as of this document's date. Any remediation landing after this pass is logged in the addendum and DOES NOT change the findings below until a retest on device.

TARGET STANDARD (stated assumption): WCAG 2.2 AA applied directly to the 2D UI surfaces (title, options, HUD text, binder, map) and by analogy to the 3D game layer, supplemented by game-layer criteria (captions for significant audio, remappable input, timing assists, photosensitivity). Say the word if the framing should instead be EN 301 549 or a strict 508 read; the findings barely move, the vocabulary does.

## METHOD, WITH ITS HOLES NAMED
A credible pass has three layers: automated scan, manual inspection, assistive-technology testing. Layer 1 has no standard scanner for a native Godot canvas; its substitute here is a repeatable code-inspection scan (color pairs computed below with the WCAG relative-luminance formula; every hardcoded font size and focus call grepped). Layer 2 is performed at code level only: keyboard reachability and focus behavior are read from source, not driven on a device. Layer 3 is not performed and mostly cannot be: no screen reader has access to this canvas. Therefore: nothing below is marked Supports on runtime behavior that only a device session can prove; those rows say Not Evaluated and the device test plan is Section 5. That candor is the point.

## 1 · COMPUTED CONTRAST (code-inspection scan)
phosphor on app black: #D9EDC4 on #070705 = 16.19:1
amber on app black: #C9A33D on #070705 = 8.44:1
HUD dim green on map bg: #8A9480 on #0B0C09 = 6.19:1
room label on room fill: #8A9480 on #12140F = 5.85:1
sealed label on sealed fill: #565B50 on #0D0E0C = 2.77:1
ledger green on room fill: #596B52 on #12140F = 3.22:1
objective green (engine) on mid-scene gray: #94A680 on #3A3A3A = 4.35:1
Reading: the primary phosphor and amber pairs clear AA for normal text with room to spare. The dim-green secondary text clears large-text AA only; the sealed-room label in the greybox map fails outright and is a defect (F02). HUD text rendered over the live 3D scene has NO guaranteed backdrop, so its effective contrast is unbounded below (F03); the computed engine pair above is illustrative of a mid-gray wall worst case.

## 2 · FINDINGS (each: SC mapping, level, verdict, location)
F01 · 1.4.3 Contrast, menus/UI · AA · SUPPORTS by computation for primary text; secondary dim-green limited to large text. Location: title.tscn, options_panel.gd, map_view.gd.
F02 · 1.4.3 · AA · DOES NOT SUPPORT: sealed-room labels in docs/canon/restoration-greybox-map.html at 2.x:1. Severity low (companion doc, not shipped UI).
F03 · 1.4.3 applied to HUD-over-scene · AA · PARTIALLY SUPPORTS: toast, objective, clock, capture line render over arbitrary scene luminance with no outline or backplate. Severity high (core loop text). Location: scenes/main.tscn HUD labels.
F04 · 1.4.4 Resize Text · AA · DOES NOT SUPPORT: all UI font sizes hardcoded; no scale control. Severity high. Root cause shared with F03 (per-label hardcoding).
F05 · Captions for significant audio (1.2.x analog / game-layer) · DOES NOT SUPPORT: the bell, door thunks, pen ticks, and hum beds have no visual equivalent; a deaf player misses the finale's bell entirely, and the bell is a story beat. Severity high.
F06 · 2.1.1 Keyboard · A · PARTIALLY SUPPORTS by inspection: menus are button/slider native controls with an explicit grab_focus; gameplay requires mouse for camera (industry-typical, disclosed). NOT EVALUATED at runtime: full keyboard traversal of the options panel and title needs a device session.
F07 · 2.4.7 Focus Visible · AA · NOT EVALUATED: flat buttons rely on the default theme's focus stylebox; visibility unproven off-device. Backlog item regardless (explicit focus ring costs little).
F08 · 2.3.1 Three Flashes · A · SUPPORTS with analysis: the single startle is a one-frame geometric scale, not a luminance flash; the tracking band and head-switch flicker are the only rhythmic luminance elements and both are suppressed by photo-safe mode. Photo-safe itself SUPPORTS (commit 021) but defaults off (F10).
F09 · 2.2.1 Timing Adjustable · A analog · PARTIALLY SUPPORTS: Matinee mode reduces consequence but the screening beat tolerance (0.2 s) and premiere timers (45/30 s) are fixed. A timing-assist toggle is absent.
F10 · Safe defaults (game-layer) · ADVISORY: photo-safe and any future assist should be offered at first run, not buried. 
F11 · 4.1.2 Name/Role/Value; screen readers · A · DOES NOT SUPPORT, candidly: the Godot canvas exposes no accessibility tree; menus are not SR-operable. This is an engine-level limit shared by most shipped games; mitigation is everything else in this document, and the limit is disclosed rather than dressed up.
F12 · Remappable input (game-layer; 2.5.x-adjacent) · DOES NOT SUPPORT: bindings fixed in project.godot. Runtime InputMap remapping is feasible.
F13 · Motor stillness required (game-layer) · PARTIALLY SUPPORTS: the QUIET stance and the Floor Manager check demand physical stillness with no alternative input path. The fiction wants stillness; access wants an equivalent (a held key that counts as still).
F14 · Sensitivity, volume, fullscreen · SUPPORTS as of commit 028 (the booth), persisted apart from saves.
F15 · Subtitles for speech · SUPPORTS BY ARCHITECTURE: every voice in the build is rendered text; when VO lands, this row must be retested, and the audio bible already reserves the obligation.
F16 · Restricted saving (stations, paper) · DISCLOSED DESIGN TENSION, not claimed conformant: save flexibility is a core mechanic. Mitigations on record: Matinee economy, the presigned page, respawn anchors. An eventual assist tier may add a free-save; that is a design decision, and this document's job is to keep it visible, not to make it.

## 3 · REMEDIATION BACKLOG (separate act; mapped, prioritized by impact, root-caused)
R1 (F03, F04 shared root: per-label hardcoding) · HUD text preference system: outlines on every HUD label (backplate-equivalent for dynamic backgrounds) plus a UI text scale control. Stage: quick win, this repo.
R2 (F05) · Caption system for significant one-shots: [BELL RINGS], [DOOR], [PEN], surfaced bottom-of-screen, toggleable, persisted. Stage: quick win, this repo.
R3 (F02) · Recolor the map's sealed labels to clear 4.5:1. Quick win.
R4 (F07) · Explicit focus ring theme on all buttons. Quick, device-verify after.
R5 (F09, F13) · ASSIST toggle: widened beat tolerance, +50 percent premiere timers, hold-E-counts-as-still. Design-touching; spec before build.
R6 (F12) · Runtime input remapping panel. Structural; M-milestone item.
R7 (F10) · First-run access prompt (photo-safe, captions, text size) before the title menu. Small, high dignity.
R8 (F11) · Tracked as engine-limit disclosure; revisit if Godot's accessibility work or a middleware bridge matures.

## 4 · SDLC HOOKS
Add to the invariant harness: a contrast lint (the Section 1 script, run per build over the palette table) and a hardcoded-font-size grep that fails when a label bypasses the text-preference system R1 installs. Acceptance criterion for future UI commits: operable by keyboard, sized by the preference system, captioned if it sounds.

## 5 · THE DEVICE PASS (owner: Ciel; the layers this document cannot claim)
Environment: the target machine, a windowed and a fullscreen session, keyboard-only for all menus (mouse unplugged, per the methodology), 200 percent OS scaling spot-check. Script: title traversal, options traversal incl. slider arrows, focus visibility photographed, one full Day 1 with captions on and text at 1.4x, photo-safe on, the finale bell with sound muted (does the caption carry the beat). Findings feed back as F-numbers; only then do the rows above move.

## ADDENDUM · REMEDIATION LOG
(Entries appended as remediation lands. The findings above continue to describe commit 028 until the device retest.)
2026-07-03 · Commit 029 landed R1 (HUD outline plus UI TEXT SIZE 0.8 to 1.6, base sizes cached, live-applied via a recursive label walker), R2 (caption system: [THE BELL RINGS · once], [door], [pen tick], toggleable in the booth, persisted), and R3 (map sealed-label recolor to 5.85:1). Per methodology: the findings above still describe commit 028; rows F03, F04, F05, F02 move only after the Section 5 device pass confirms the remediation on hardware. R4 through R7 remain open.
2026-07-03 · Commit 031 landed R4 (explicit phosphor focus ring on every button, check, and slider in the booth and the title menu), R5 (a single ASSIST switch carrying three mercies: beat tolerance 0.2 to 0.35, premiere clocks times 1.5, and hold-E-counts-as-still at both stillness checks, disclosed in its own label), R7 (first-run booth: no settings file means the booth opens over the title with a one-line banner and writes the file so it never re-prompts), and R6 in a v1 scope: runtime remap for the five contested actions with press-a-key capture, cross-action conflict refusal, and persistence in settings.cfg. Named residue: prompts still print letters (E, SPACE, Q) rather than bound glyphs; that work is shared with localization finding L05 and remains open. Per methodology, rows F07, F09, F10, F12, F13 continue to describe commit 028 until the device pass.
2026-07-03 · Commit 033 delivered the glyph pass at the chokepoints: prompts, toasts, say lines, and cue status now render the BOUND key for the five remappable actions via word-boundary substitution, closing the letters-in-prompts residue for exactly the actions R6 governs. Remaining residue: Z, X, O, P, and the number keys remain literal (outside the remap set); rows still describe c028 until the device pass.
2026-07-03 · Commit 034 added a pause (advisory R9, timing and interruption access): Escape holds the whole simulation with audio muted, refused only while the player is locked in an authored sequence; the intermission menu is keyboard-operable with visible focus and opens the booth in place. Rows continue to describe c028 until the device pass.
