# RESTORATION · GAMETEXT AUDIT (C12)

The 714 keys of `translations/strings.csv` (mirrored 1:1 into
`ue/Restoration/Data/GameText.csv` by `tools/extract_data.py`, PROGRESS.md
§0.5), each classified by the display path it actually flows through in the
reference implementation, with the glyph-substitution map, the LAW 5 check and
a localization-readiness ledger measured from source. Every rule asserted
carries a citation `[KEY §section]` (keys in §0.1); where canon is silent the
line says **OPEN** and the question is numbered in §6. Nothing here invents
canon; where a canon document and the code disagree, both are quoted and the
disagreement is an OPEN, because the code is the intent [PORT ¶1].

This is a paper deliverable from the cloud lane: no Godot, Blender or UE was
run. Verification is by the script in Appendix B, run against the tree at
`origin/main` d7a6877; its full per-key output is Appendix A.

---

## 0 · CONVENTIONS

### 0.1 Source keys

| Key | Path |
|---|---|
| LAWS | `docs/packet/portbrief/THE-LAWS.md` |
| PORT | `docs/packet/portbrief/PORT-BRIEF.md` |
| LOC | `docs/production/restoration-localization-plan.md` |
| ACH | `docs/production/restoration-achievements-design.md` |
| PRESENCE | `docs/production/restoration-steam-presence.md` |
| CONTROLS | `docs/canon/restoration-controls-map.md` |
| ACCESS | `docs/canon/restoration-accessibility-matrix.md` |
| MOTION | `docs/canon/restoration-chum-motion-and-sound.md` |
| MASTER | `docs/canon/restoration-game-master.md` |
| LORE | `docs/canon/restoration-lore-architecture.md` |
| PLAN | `AAA_BUILD_PLAN.md` |
| CODE | `scripts/*.gd` at origin/main d7a6877 (file:line) |
| CSV | `translations/strings.csv` (714 keys) · `ue/Restoration/Data/GameText.csv` |

### 0.2 Method

The extractor harvests every quoted literal in `scripts/*.gd` that is at
least four characters, contains a word of three or more letters and contains a
space or a `·` [CODE tools/extract_strings.py:16-21]. It does not know what
the literal is for. This audit finds every occurrence of each key in the
scripts and classifies it by the call it sits in, using the four translation
chokepoints the Extraction Commit named — `GameState.toast`, the HUD `_say`
pair, the prompt display and `show_caption` — plus the booth's code-built
labels [LOC Addendum 032]. The rules are the `classify_occ` function in
Appendix B; four sites the rules cannot see are hand-ruled there with their
line numbers.

### 0.3 Verdict codes

**Class** (primary; a key used on several paths lists all of them in Appendix A,
first is primary):

| Class | Meaning |
|---|---|
| TOAST | `GameState.toast()` → `notify` signal → HUD toast label [CODE game_state.gd:211-212] |
| CAPTION | `GameState.show_caption()` → `caption` signal → HUD caption label, only when `captions_on` [CODE game_state.gd:400-402] |
| ACHIEVEMENT | an entry of `Achievements.TITLES` / `ENDING_MAP` [CODE achievements.gd:11-28] |
| LORE | a found-document line delivered by `ReadableProp._run()` (D04, D05, D09, D10, D11) [CODE readable_prop.gd:33-36, world_builder.gd:1151-1178] |
| UI-PROMPT | an `Interactable.get_prompt()` return or a label fed into one [CODE hud.gd:529] |
| UI-SAY | the ending / retake / demo card `_say(a, b, t)` pair or a direct `r1/r2.text =` [CODE hud.gd:331-334] |
| UI-MENU | the booth (`options_panel.gd`), the pause menu (`hud.gd:_toggle_pause`) and the title screen (`title.gd`) |
| UI-OBJECTIVE | `GameState.objective_text()` → HUD objective label [CODE game_state.gd:687, hud.gd:533] |
| UI-BINDER | the TAB binder / presentation form lines and the casualty-ledger fields [CODE hud.gd:224-271] |
| UI-CAPTURE | `set_capture_status()` → HUD capture line (bench countdown, premiere cues) [CODE game_state.gd:219-221] |
| UI-CLOCK | `Broadcast.phase_text()` and the DAY/NIGHT prefix [CODE broadcast.gd:27-31, hud.gd:531-532] |
| UI-CREDITS | the credits crawl and the `_roll_credits` ending label [CODE credits.gd, hud.gd:347] |
| UI-MAP | the facility map footer [CODE map_view.gd:77] |
| WORLD | a `Label3D` or door/slate text that exists as an object in the fiction [LOC §2 WORLD TEXT] |
| IDENTIFIER | a state key compared in code (ending names, casualty ids, key ids, signal names, mode names, segment names) |
| NON-PLAYER | telemetry, the invariant scorecard, the premiere/liveness/coverage logs |

**tr status** (does the key reach `tr()` intact?):

| Code | Meaning |
|---|---|
| TR | the exact key is passed to `tr()` — translatable today |
| TR-FMT | the key is a `%` template that is formatted BEFORE `tr()` sees it; the formatted string never matches the CSV row, so the row is dead at runtime |
| TR-CAT | the key is concatenated or placeholder-fed into another string before `tr()` (e.g. `"FILED · " + title`, `"HARRIET · %s" % line`); same effect |
| NO-TR | displayed on a path that never calls `tr()` |
| N/A | not displayed as itself (identifier, world text by doctrine, log line) |

---

## 1 · THE COUNT

| Check | Result |
|---|---|
| keys in `translations/strings.csv` | 714 |
| keys in `ue/Restoration/Data/GameText.csv` | 714, identical content and order |
| duplicate keys | 0 |
| keys with no occurrence in `scripts/*.gd` | 0 (the CSV is in sync with source) |
| keys that are `%` templates | 104 (extractor's own count: 104 template sites [CODE extract_strings.py:44]) |
| keys with an embedded `\n` | 19 |
| all-caps keys (≥4 letters, no lowercase) | 167 |
| keys over 120 characters (longest 148) | 10 |

---

## 2 · THE CLASSES

### 2.1 Rollup to the five classes the unit names

| Class | Keys | Reaches `tr()` intact | Glyph layer applied |
|---|---|---|---|
| UI (all UI-* rows below) | 307 | 111 of 307 | prompt, say, capture only |
| TOAST | 236 | 200 | yes [CODE game_state.gd:212] |
| LORE | 15 | 15 | yes (delivered as toasts) |
| ACHIEVEMENT | 31 | 0 (all TR-CAT, see G03) | yes, via toast |
| CAPTION | 14 | 14 | **no** [CODE game_state.gd:402] |
| — residue the CSV also carries — | | | |
| WORLD | 63 | N/A — stays English by doctrine [LOC §2] | no |
| IDENTIFIER | 12 | N/A | no |
| NON-PLAYER | 36 | N/A — should not be in the CSV (G05) | no |

### 2.2 The UI subclasses

| Subclass | Keys | tr status | Notes |
|---|---|---|---|
| UI-PROMPT | 79 | 40 TR · 18 TR-FMT · 19 TR-CAT · 2 NO-TR | `hud.gd:529` wraps `tr()` around the already-formatted prompt, so every prompt template is TR-FMT |
| UI-SAY | 110 | 91 TR · 2 TR-FMT · 17 NO-TR | the 17 NO-TR are direct `r1.text =` / `r2.text =` writes in `_on_captured`, `_on_run_ended`, `_on_demo_end`, `_end_perform` [CODE hud.gd:278-325, 369-372, 454-455] |
| UI-MENU | 19 | 15 TR · 4 NO-TR | booth + pause are wrapped [LOC Addendum 032]; `title.gd:13,17,28,32` are not |
| UI-OBJECTIVE | 12 | 12 NO-TR | `objective_text()` returns raw English; `hud.gd:533` assigns it without `tr()` |
| UI-BINDER | 46 | 46 NO-TR | `_fill_form` / `_fill_binder` build lines without `tr()`; also the casualty-ledger `cause` / `note` fields of every `mark_casualty()` call |
| UI-CAPTURE | 16 | 16 NO-TR | `set_capture_status()` applies `glyphs()` but not `tr()` [CODE game_state.gd:219-221] |
| UI-CLOCK | 4 | 4 NO-TR | `● ON AIR · break in 0:%02d`, `○ BREAK · window closes 0:%02d`, `NIGHT · `, `DAY %d · ` |
| UI-CREDITS | 20 | 20 NO-TR | `credits.gd` crawl entries and the seven `_roll_credits("…")` ending labels |
| UI-MAP | 1 | NO-TR | `FACILITY MAP · %s to close · …` [CODE map_view.gd:77] |

### 2.3 Register (a heuristic column in Appendix A, for the translators)

| Register | Keys | Rule |
|---|---|---|
| DIALOGUE | 56 | key opens with `SPEAKER · '…'`, `SPEAKER, aside: '…'` or a bare `'…'` |
| TAPE | 3 | key opens `ON TAPE ·` (archival playback; memory, band-limited by the audio law [PLAN §1 Motion & sound law]) |
| DOCUMENT | 15 | = LORE |
| (blank) | 640 | system text |

The register column is heuristic; the loc style guide rules case by case
[LOC §3 L06].

---

## 3 · THE GLYPH-SUBSTITUTION MAP

**Mechanism** [CODE game_state.gd:124-125, 193-200]: after `tr()`, the
chokepoint calls `glyphs(text)`, which replaces each whole-word token
(`\bTOKEN\b`, case-sensitive) with the upper-cased current binding of the
mapped action. Translators keep the tokens verbatim in target strings and the
engine substitutes at display [LOC L05 addendum 033].

| Token | Action | Canon verb [CONTROLS §PC] | Keys carrying it | Applied on |
|---|---|---|---|---|
| `E` | `interact` | INTERACT E (hold E where noted) | 51 | toast · say · prompt · capture-status |
| `SPACE` | `respond` | RESPOND SPACE | 9 | same |
| `Q` | `improvise` | IMPROVISE Q | 6 | same |
| `T` | `toggle_tbc` | TAPE STABILIZER T | 3 | same |
| `M` | `map` | MAP M | 2 | same |

Paths that name keys but never pass through `glyphs()` — the text is
hard-wired to the physical letter, the L05 residue:

| Key named | Keys | Path | Example |
|---|---|---|---|
| TAB | 2 | UI-BINDER | `THE BINDER · TAB closes` |
| 1 / 2 / 3 | 1 | UI-BINDER | `MODE · press 1 / 2 / 3` |
| WASD | 1 | UI-BINDER | `CONTROLS · WASD move · E interact · SPACE respond · Q improvise` (E/SPACE/Q also unsubstituted here, the binder skips `glyphs()`) |
| P | 4 | UI-BINDER, UI-MENU, TOAST | `PHOTOSAFE: %s (P)` |
| O | 2 | UI-MENU | `CLOSE (O)` |
| Z, X | 1 each | TOAST | seance frame keys [CONTROLS §PC: SEANCE FRAME BACK Z · FORWARD X] |
| T | 2 | UI-BINDER, WORLD | `TBC · %s · toggle with T anywhere` (binder, no glyphs), `TBC: %s  (T)` |
| SPACE | 5 | UI-CAPTURE, UI-SAY(NO-TR) | premiere cue lines; `SPACE · deliver the line` [CODE hud.gd:455] |

These are the five remappable verbs today [CONTROLS §PC: "Remapping (R6)
covers the five verbs"]; the UE5 target is every action remappable including
movement [CONTROLS §PC, ACCESS §MOTOR], so the residue rows above become
glyph tokens in the port.

**Collisions found** (the regex is a whole-word match on a single capital
letter, so prose that contains a lone capital is rewritten):

| Key | Path | What happens |
|---|---|---|
| `The ledger, weeks later, a new hand: M. OYELARAN, INCOMING CONSERVATOR.` (and its longer sibling) [CODE hud.gd:401, 406] | UI-SAY, through `glyphs()` | `\bM\b` matches the initial; with the map key rebound to N the epilogue reads "N. OYELARAN" |
| `VESS · 'Storage auction. Paid cash. Unit was under CRAIK, E. That's Edith. …'` [CODE vess.gd LINES] | TOAST, through `glyphs()` | `\bE\b` matches the initial; rebinding interact rewrites Edith's initial |

Invisible today because the default bindings are the letters themselves;
visible the moment a player remaps. Translated text widens the exposure:
Italian upper-case "E" (and) inside any all-caps string is a whole-word `E`.
A remediation is proposed in §7 (PROPOSAL, not canon).

---

## 4 · THE LAW 5 CHECK (and a LAW 3 note)

LAW 5: "SILENCE CONTRACTS. The bell rings once, at the finale beat, and its
caption says so. Chum's bell is otherwise silent; Chum speaks nowhere; Chum
has no account, no achievement title, no presence string." [LAWS 5]

| Clause | Checked how | Result |
|---|---|---|
| no achievement title names Chum | the 28 `TITLES` + 6 `ENDING_MAP` keys, regex `chum` [CODE achievements.gd:11-28]; ACH §DOCTRINE 2 "Chum's name appears in no achievement title" | **PASS** — 0 of 31 |
| no presence string names Chum | the seven PRESENCE §STATES masters; and the CSV | **PASS by absence** — no presence bridge exists in the reference build (no `setRichPresence`, no presence string in the CSV); the seven masters in PRESENCE name no Chum. When the bridge lands its strings must be added to the extraction (OPEN-4) |
| the bell caption says so, once | `Sfx.bell()` emits `[THE BELL RINGS · once]`; single caller [CODE sfx.gd:16-18, hud.gd:452 in `_end_perform`] | **PASS** — one caption key, one call site, at the sign-off beat |
| no `creepy` in any text | regex over the 714 keys [PLAN §1 Design law: BANNED … any text containing "creepy"] | **PASS** — 0 |
| never-stated ledger | not machine-checkable; the seven truths [LORE §THE NEVER-STATED LEDGER] were read against the 56 DIALOGUE and 15 DOCUMENT keys by eye | no key states one whole; D11's "he works his own jaw. Count the hands." rhymes with "who rebuilt the after-fire body" and is a shard, not a sentence — **judgement, not proof**; the S0 review stays with the author [LORE §NEVER-STATED: "naming one of these in dialogue or text is an S0 defect"] |
| "Chum speaks nowhere" | the 15 keys that contain `chum`, with their path | see the table below and **OPEN-1** |

The fifteen keys naming Chum:

| # | Key (abridged) | Class | Site | Reading |
|---|---|---|---|---|
| 1 | `and CHUM\nas himself` | UI-CREDITS | credits.gd:27 | a credit, not speech |
| 2 | `and CHUM\nas RITA IVORI` | UI-CREDITS | credits.gd:34 | a credit (ending 0) |
| 3 | `ON TAPE · CHUM: 'Stay in your seats, friends! …'` | TOAST (TAPE) | fire_tape_dock.gd:50 | archival playback — memory [PLAN §1: "band-limited is memory"] |
| 4 | `ON TAPE · CHUM: 'Goodnight, Gladhouse! Say it with me!'` | TOAST (TAPE) | screening_event.gd:40 | archival playback |
| 5 | `RITA · 'It's our last night.'  CHUM, warm as ever: 'Ohhh, don't be sad!'` | TOAST | live_production.gd:64 | **premiere, live** — scripted verbatim in MASTER §T5.3 CUE 1: "CHUM (live, beside her, warm as ever …)" |
| 6 | `CHUM · 'Every good day ends with a goodnight. …'` | TOAST | live_production.gd:66 | same cue |
| 7 | `CHUM · 'There she is. Our new friend.'` | UI-SAY | hud.gd:418 | ending 2 epilogue text |
| 8 | `'Say goodnight, Chum.'` | UI-SAY | hud.gd:459, 483 | Rita/Leland's sign-off line, addressed to him |
| 9 | `CHUM, small, the performance finally allowed to end:` (+ `'Goodnight, Gladhouse.'`) | UI-SAY | hud.gd:463 | ending 1B (Leland closes) |
| 10 | `'There's no one at home anymore. … Say goodnight, Chum.'` | TOAST | seance_dock.gd:116 | the sign-off script read from the legal pad |
| 11 | `CHUM · ON HIS MARK` | WORLD | live_production.gd:262 | stage tag, not speech |
| 12 | `CHUM'S MARK` | WORLD | world_builder.gd:479 | floor mark |
| 13 | `Dear Chum, my brother says you are just a puppet …` | LORE | world_builder.gd:1169 | D10, a fan letter |
| 14 | `PEAK ASSET DOSSIER · CHUM-AF-1974-P` | UI-PROMPT | world_builder.gd:1174 | D11's label |
| 15 | `PEAK PRODUCTION ASSET DOSSIER. FILE CHUM-AF-1974-P …` | LORE | world_builder.gd:1175 | D11 |

Rows 5, 6, 7 and 9 put words in Chum's mouth in the present tense of the
fiction. LAWS 5 says "Chum speaks nowhere"; MOTION ¶THE THROAT SPEAKER says
"If it ever plays more than room tone, that is a canon event and the author
signs it first"; MASTER §T5.3 scripts CUE 1 with "CHUM (live …)" in so many
words, and the code carries it. The code is the intent [PORT ¶1], so the port
carries rows 5–9 as they stand; whether they are the author-signed canon event
or a LAW 5 defect is **OPEN-1**, the owner's to rule. This audit does not
rule it.

**LAW 3 note** (outside C12's string scope, recorded because the scan touched
it): no key names the once-ever moment — the 4 keys in `glimpse.gd` describe
the corridor without naming it [CODE glimpse.gd:18, 31, 66, 68]. But LAW 3
says "Its name appears in no code file" [LAWS 3], and the reference build has
`scripts/glimpse.gd` and `GameState.glimpse_seen` [CODE game_state.gd:128].
`ue/PORT-NOTES-STATE.md` carries the save key; the UE port names its actor and
flag per CAST-BUILD-BRIEFS §10 / OPEN-15. Flagged to C14 (achievements +
presence audit vs LAW 3/5) — **OPEN-2**.

---

## 5 · LOCALIZATION READINESS (measured from source)

Status of the plan's six findings [LOC §3], then what this scan adds.

| Plan item | Status at d7a6877 |
|---|---|
| L01 chokepoint translation | Landed for toast, say, prompt, caption, booth, pause [LOC Addendum 032; CODE tr() sites: game_state.gd:212,402; hud.gd:114-123,332-333,529; options_panel.gd:29-118]. **124 displayed keys (17 %) sit on paths with no `tr()` at all** (G02) and **104 more are templates or concatenations that never match a row** (G01, G03) — so 375 of 714 keys (53 %) are translatable as shipped |
| L02 CJK font fallback | not in scope (assets); unchanged |
| L03 fixed widths, +35 % budget | 10 keys over 120 chars, longest 148 (credits blocks, D11 lines, the epilogue); 19 keys carry their own `\n` line breaks, i.e. layout baked into the string (G08) |
| L04 toast durations | every `ReadableProp` line and `_say` pair carries a hard-coded seconds value in code (e.g. `["…", 3.2]`, `_say(a, b, 2.8)`); no per-locale characters-per-second table exists (G09) |
| L05 physical letters in prompts | glyph layer in for E/SPACE/Q/T/M on four paths; 14 keys still hard-wire TAB, O, P, Z, X, WASD, 1/2/3 or sit on non-glyph paths (§3); two collisions (§3) |
| L06 all-caps registers | 167 keys are all-caps (23 %); the loc style guide has to rule caps-as-voice vs caps-as-styling per key (the register column in Appendix A is the seed) |

### 5.1 Findings this scan adds

| ID | Finding | Count | Evidence |
|---|---|---|---|
| G01 | **Templates are formatted before `tr()`.** Every `%` key on a translated path is passed to the chokepoint already formatted, so the CSV row can never match. The plan's claim that "those templates translate with their placeholders intact" [LOC Addendum 032] does not hold in the code as written. | 42 keys TR-FMT (23 toast, 18 prompt, 1 say) | `toast("READ · filed to memory. (%d of 10 documents)" % n)` [CODE game_state.gd:208] → `tr("READ · filed to memory. (3 of 10 documents)")`; `hud.gd:529` `tr(t.get_prompt())` after `get_prompt()` has formatted |
| G02 | **Display paths with no `tr()`.** Binder/form, objective, capture status, clock, credits, title screen, map footer, the direct `r1/r2.text =` cards, and three toasts that bypass `toast()` via `notify.emit()` directly | 124 keys NO-TR | e.g. `objective.text = GameState.objective_text()` [CODE hud.gd:533]; `notify.emit("CAPTURED · %s · presentation kept" % …)` [CODE game_state.gd:231]; `notify.emit("LOG MIGRATED …")` [game_state.gd:773, 777] |
| G03 | **Concatenation before `tr()`.** Achievement titles flush as `"FILED · " + title`; Harriet's lines as `"HARRIET · %s" % line`; the legal-pad answers as `"LEGAL PAD · " + a`; incidents as `"THE CLUB IS HELPING · " + text`; readable labels as `"%s · read (E)" % label`; door prompts as `"%s · %s" % [door_label, locked_reason]` | 62 keys TR-CAT | [CODE achievements.gd:94; harriet.gd:120; seance_dock.gd:82; live_production.gd:406; readable_prop.gd:21-22; door.gd:28] |
| G04 | **Identifiers displayed through placeholders.** Ending names, mode names, casualty causes, key ids and room names are compared in code and then shown via `%s` untranslated (`ENDING REACHED: %s`, `MODE · %s`, the casualty-ledger row) | 12 IDENTIFIER keys, 6 of them also ACHIEVEMENT ending names | [CODE game_state.gd:689-696, 296; hud.gd:251] |
| G05 | **Non-player text in the CSV.** The invariant scorecard, the coverage/liveness/premiere logs and Rundown's decision-log lines are in the translation table; translating them would break the parsers, which match these literals (`invariant_parser.gd` matches `"WARN "`, `"STRIKE "`, `"club auto-fix"`) [CODE invariant_parser.gd:33-70]. These are the log formats the migration map says MUST NOT CHANGE [PLAN §1 THE PORT KIT: "WHAT MUST NOT CHANGE: … log formats"] | 36 keys | Appendix A rows tagged NON-PLAYER |
| G06 | **World text in the CSV.** `Label3D` tags, slates, floor marks, door labels: by doctrine they stay English and their meaning reaches the player through the inspection toast [LOC §2] | 63 keys | Appendix A rows tagged WORLD |
| G07 | **Extractor drops short player-facing literals.** The "must contain a space or `·`" rule [CODE extract_strings.py:20] excludes single-word strings that do reach a chokepoint | 5 strings absent from the CSV | `tr("RESUME")` hud.gd:118 · `_say("EPILOGUE", …)` hud.gd:401,406 · `toast("PLACES.")` live_production.gd:55 · `tr("FULLSCREEN")` options_panel.gd:51 · `show_caption("[door]")` sfx.gd:27 |
| G08 | **Line breaks baked into keys** (credits blocks, the title's FILED list header, the scorecard) | 19 keys | Appendix A |
| G09 | **Timings live beside the text in code**, not in data: readable lines `[text, seconds]`, `_say(a, b, seconds)`, toast dwell 3.0 s fixed [CODE hud.gd:553] | every LORE and UI-SAY key | L04 remediation is still to do |
| G10 | **Do-not-translate terms inside translatable keys** [LOC §5: WGLD, Chum, The Gladhouse, RESTORATION, slate codes] | CHUM/Chum 15 · WGLD 7 · Gladhouse/GLADHOUSE 9 · RESTORATION 2 | glossary enforcement, not a defect |
| G11 | **Captions are all bracketed.** ACCESS §HEARING: "band-limited sources caption in brackets styled as broadcast, full-range sources caption plain, so even the reading ear learns MEMORY versus PRESENT". All 14 shipped captions are bracketed, including present-tense ones (`[THE JAW WORKS ITS LEVER]`, `[IT FOLDS THROUGH THE DOORWAY]`, `[door]`) | 14 keys | whether the bracket rule is a UE5 extension or already binding on these is **OPEN-3** |
| G12 | **`GameText.csv` has no namespace or key column.** It is `Key,SourceString` with the English as both [CODE extract_data.py:102-106]; UE's localization pipeline keys on namespace + key + source. Whether the port keeps source-as-key (Godot's mode) or mints ids is **OPEN-5** |
| G13 | **A11's title drifted from its design.** ACH lists `A11 PER V. CARDONA`; the code ships `"A11": "PER V. KEYS"` [CODE achievements.gd:15] and the ledger-margin prompt says `'per V. Keys'` [CODE credit_entry.gd:11]. The cast is Vess Keys throughout PROGRESS.md and the plates; code is the intent [PORT ¶1] — noted for C14 |
| G14 | **Demo-only strings share the table** (`TAPE 1 · FREE DEMO …`, the demo end card) with no marker; DEMO ships achievements disabled [ACH §Demo parity] but its strings are not partitioned | 4 keys (title.gd:28, hud.gd:369-372) | informational |

---

## 6 · OPEN (numbered; owner or a later unit rules, this audit does not)

| # | Question | Where it bites |
|---|---|---|
| OPEN-1 | Are the premiere lines (live_production.gd:64, 66) and the ending lines (hud.gd:418, 463) the author-signed canon event MOTION ¶THROAT SPEAKER allows, or a LAW 5 "Chum speaks nowhere" defect? MASTER §T5.3 scripts them as live speech; the code carries them. | §4 rows 5–9; Phase 4 finale port; 1.12 (throat-speaker room tone) |
| OPEN-2 | LAW 3 "Its name appears in no code file" vs `scripts/glimpse.gd`, `GameState.glimpse_seen` and the v16 save key. C14's question; recorded here because the string scan crossed it. | C14; UE naming of the corridor actor/flag (CAST-BUILD-BRIEFS OPEN-15) |
| OPEN-3 | Is the bracket-vs-plain caption grammar [ACCESS §HEARING] binding on the 14 shipped captions, or a UE5 extension only? Three present-tense captions are bracketed today. | 5.2 accessibility; caption style guide |
| OPEN-4 | Presence strings: the seven PRESENCE masters are not in the CSV because no bridge exists in the reference build. Do they enter `GameText.csv` at extraction time (with a class of their own) or live in `richpresence.vdf` only [PRESENCE ¶Doctrine]? | Phase 6 credits/meta; C14 |
| OPEN-5 | UE key scheme: keep source-as-key (Godot's mode, zero churn on the 375 TR keys) or mint stable ids with a namespace per class (survives copy edits, matches UE tooling)? Canon is silent; LOC §6 only names the pipeline stages. | 0.8/Phase 4 UI port; `extract_data.py` |
| OPEN-6 | The L06 caps ruling per key ("caps-as-voice versus caps-as-styling case by case" [LOC §3]) — 167 keys await the per-locale style guide; the register column is only a seed. | Wave 1 loc kickoff |

---

## 7 · PROPOSED REMEDIATION (PROPOSAL — engineering shape, not canon)

Ordered by the number of keys each unblocks. None of these change a string;
they change where `tr()` sits.

1. **Translate-then-format** at every template site (unblocks 42 TR-FMT + most
   of the 62 TR-CAT): give the chokepoints a `(template, args)` form
   (`toast_f(template, args)` → `glyphs(tr(template) % args)`), and have
   `get_prompt()` implementations return `tr(template) % args`. Identifier
   placeholders (G04) then need a display map (`tr(ending_name)`) at the
   `%s` — the identifiers stay English in state and saves, per the
   save-semantics freeze [PLAN §1 THE PORT KIT: "WHAT MUST NOT CHANGE: … save
   semantics"].
2. **Wrap the eight untranslated paths** (unblocks 124 NO-TR): `_fill_form`,
   `_fill_binder`, `objective_text`, `set_capture_status`, `phase_text` + the
   DAY/NIGHT prefix, `credits.gd`, `title.gd`, the direct `r1/r2.text =` writes
   and the three `notify.emit()` calls — or route the last through `toast()`.
3. **Partition the extractor** (fixes G05, G06, G07): exclude
   `invariant_parser.gd`, `soak_runner.gd`, `bot_driver.gd`,
   `coverage_director.gd`, `log_line` / `_plog` / `_log` / `store_line` call
   sites; tag `Label3D`/slate/`locked_reason` literals WORLD in a second
   column instead of dropping them (they are still needed as source text for
   the inspection toasts); drop the space-or-`·` rule in favour of "reaches a
   chokepoint". A class column in `strings.csv` / `GameText.csv` (the
   Appendix A `class` column) makes the CSV self-describing.
4. **Glyph tokens with delimiters** (fixes the two collisions and the Italian
   exposure): substitute `{E}`, `{SPACE}`, … rather than bare words, and
   extend the map to every remappable action in UE5 [CONTROLS §PC target].
   Translators keep the braces.
5. **Timings to data** (L04): move the `[text, seconds]` and `_say(…, t)`
   seconds into a per-locale characters-per-second rule at the chokepoint,
   with the current seconds as the English floor.

---

## APPENDIX A · THE 714 KEYS

Columns: `#` CSV row order · `class` (all paths, primary first) · `tr` status
(§0.3) · `%` placeholder count · `glyph` tokens present · `register` · `source`
(first two file:line sites) · `key` (verbatim; `|` shown as `\|`).

| # | class | tr | % | glyph | register | source | key |
|---|---|---|---|---|---|---|---|
| 1 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:12 | `FIRST SIGNATURE` |
| 2 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:12 | `CAREFUL HANDS` |
| 3 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:12 | `THE SCOPE READS MASTER` |
| 4 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:13 | `ON THE BEAT` |
| 5 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:13 | `STILLNESS, HELD WHOLE` |
| 6 | ACHIEVEMENT+IDENTIFIER | TR-CAT | 0 |  |  | achievements.gd:14 harriet_note.gd:5 | `HOLD YOUR APPLAUSE` |
| 7 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:14 | `YOU WERE NOT QUIET` |
| 8 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:14 | `TOMORROW'S DATE` |
| 9 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:15 | `THE ROWS KEEP THEIR ORDER` |
| 10 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:15 | `PER V. KEYS` |
| 11 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:15 | `NO SEARCHER SINGS` |
| 12 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:16 | `THE UNFINISHED LINE` |
| 13 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:16 | `I'VE READ THE ENDING` |
| 14 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:16 | `ORDER MATTERS` |
| 15 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:17 | `THE LONG WAY AROUND` |
| 16 | ACHIEVEMENT+UI-SAY | TR-CAT | 0 |  |  | achievements.gd:17 hud.gd:324 | `NEXT WEEK'S EPISODE` |
| 17 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:18 | `EMPTY DRAWER` |
| 18 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:18 | `SEALED FOR BROADCAST` |
| 19 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:18 | `THERE'S COBBLER` |
| 20 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:19 | `WELCOME HOME` |
| 21 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:19 | `FILE UNDER: SAINTS` |
| 22 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:19 | `IT'S OKAY. NOBODY'S WATCHING.` |
| 23 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:20 | `SIGNED OFF` |
| 24 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:20 | `FULL ACCESSION` |
| 25 | ACHIEVEMENT | TR-CAT | 0 |  |  | achievements.gd:21 | `EVERYONE GOES HOME` |
| 26 | ACHIEVEMENT+UI-CREDITS+IDENTIFIER | TR-CAT | 0 |  |  | achievements.gd:21 achievements.gd:27 | `A ONE-WOMAN SHOW` |
| 27 | ACHIEVEMENT+IDENTIFIER | TR-CAT | 0 |  |  | achievements.gd:24 hud.gd:407 | `THE BURN` |
| 28 | ACHIEVEMENT+IDENTIFIER | TR-CAT | 0 |  |  | achievements.gd:24 hud.gd:424 | `THE NEW PRODUCER` |
| 29 | ACHIEVEMENT+IDENTIFIER | TR-CAT | 0 |  |  | achievements.gd:25 hud.gd:476 | `SIGN-OFF · RITA CLOSES` |
| 30 | ACHIEVEMENT+IDENTIFIER | TR-CAT | 0 |  |  | achievements.gd:25 hud.gd:466 | `SIGN-OFF · LELAND CLOSES` |
| 31 | ACHIEVEMENT+IDENTIFIER | TR-CAT | 0 |  |  | achievements.gd:26 hud.gd:506 | `DEAD AIR` |
| 32 | WORLD+IDENTIFIER | N/A | 0 |  |  | achievements.gd:73 live_production.gd:124 | `QUIET ROOM` |
| 33 | TOAST | TR-CAT | 0 |  |  | achievements.gd:94 | `FILED · ` |
| 34 | TOAST | TR-FMT | 2 |  |  | achievements.gd:96 | `FILED · %d entries, %s among them.` |
| 35 | UI-PROMPT | TR-CAT | 0 |  |  | asset_pickup.gd:6 | `an asset` |
| 36 | UI-PROMPT | TR-FMT | 1 | E |  | asset_pickup.gd:17 key_item.gd:10 | `%s · take (E)` |
| 37 | UI-PROMPT | TR | 0 | E |  | bed_prop.gd:8 | `RITA'S BED · sleep until morning (E)` |
| 38 | UI-PROMPT | TR | 0 | E |  | bed_prop.gd:9 | `RITA'S BED · end the day (E)` |
| 39 | TOAST | TR | 0 |  |  | bed_prop.gd:14 | `The club insists you sleep at home until the contract is signed.` |
| 40 | TOAST | TR | 0 |  |  | bed_prop.gd:17 | `The show is over here. NEW GAME threads a fresh reel.` |
| 41 | TOAST | TR | 0 |  |  | bed_prop.gd:20 | `PLACES. The premiere begins.` |
| 42 | WORLD | N/A | 0 |  |  | bench_tv.gd:6 | `SLATE: 3RD GENERATION DUB · SCOPE READS: MASTER` |
| 43 | TOAST | TR | 0 |  | TAPE | bench_tv.gd:64 | `ON TAPE · it walked to the lens. It held. One frame.` |
| 44 | UI-CLOCK | NO-TR | 1 |  |  | broadcast.gd:30 | `● ON AIR · break in 0:%02d` |
| 45 | UI-CLOCK | NO-TR | 1 |  |  | broadcast.gd:31 | `○ BREAK · window closes 0:%02d` |
| 46 | UI-PROMPT | TR | 0 |  |  | capture_bench.gd:18 | `TAPE ROLLING · stay with it` |
| 47 | UI-PROMPT | TR-FMT | 1 | E |  | capture_bench.gd:19 | `THE BENCH · begin capture, Tape %d (E) · runs real time` |
| 48 | UI-CAPTURE | NO-TR | 2 |  |  | capture_bench.gd:37 capture_bench.gd:65 | `CAPTURE · TAPE %d · 00:%05.2f` |
| 49 | TOAST | TR | 0 |  |  | capture_bench.gd:52 | `CAPTURE ABORTED · the take is lost. The bench keeps no half-truths.` |
| 50 | TOAST | TR-FMT | 1 |  |  | capture_bench.gd:59 | `TAPE %d · A CLEAN SIGNAL` |
| 51 | TOAST | TR | 0 |  |  | cascade.gd:24 | `PANEL EVENT · circuit C lets go. The stage end of the building drops dark.` |
| 52 | TOAST | TR | 0 |  |  | cascade.gd:26 | `The dark spreads room to room, patient, like it is reading the labels.` |
| 53 | TOAST | TR | 0 |  |  | cascade.gd:32 | `Circuit B follows. The dark is administrative now. The panel is in the patch bay.` |
| 54 | TOAST | TR | 0 |  |  | cascade.gd:40 | `The panel holds. Circuit F never so much as flickered. It cannot be de-energized. You have read that somewhere.` |
| 55 | UI-PROMPT | TR | 0 | E |  | casting_sheet_prop.gd:7 | `THE CASTING SHEET · read (E)` |
| 56 | TOAST | TR-FMT | 1 |  |  | casting_sheet_prop.gd:12 | `FINAL EPISODE · CAST: ALDER · BELL · PRICE · MERRICK · %d of 4 guest lines filled. The club dusts it.` |
| 57 | UI-PROMPT | TR | 0 | E |  | coat_pegs.gd:67 | `COAT PEGS · the club's palette (E)` |
| 58 | TOAST | TR | 0 |  |  | coat_pegs.gd:72 | `Cardigans in sensible grays. One mustard scarf, early to the party.` |
| 59 | TOAST | TR | 0 |  |  | coat_pegs.gd:74 | `The palette is drifting. Nobody has said anything about it, which is itself the thing.` |
| 60 | TOAST | TR | 0 |  |  | coat_pegs.gd:76 | `Show palette, head to toe, every peg. Somebody ironed.` |
| 61 | NON-PLAYER | N/A | 3 |  |  | coverage_director.gd:24 | `SESSION OPEN · restored counters m=%.1f mv=%.1f st=%.1f` |
| 62 | NON-PLAYER | N/A | 3 |  |  | coverage_director.gd:34 | `[day %d %s] %s` |
| 63 | NON-PLAYER | N/A | 0 |  |  | coverage_director.gd:95 | `READ RESET · dailies burned` |
| 64 | UI-PROMPT | TR | 0 | E |  | credit_entry.gd:11 | `LEDGER MARGIN · credit the insight (E) · 'per V. Keys'` |
| 65 | TOAST | TR | 0 |  |  | credit_entry.gd:17 | `You write his name where findings live. Somewhere, a label maker clicks twice.` |
| 66 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:23 | `an accession of the 58 CLUB` |
| 67 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:24 | `written, designed, and built by\nCIEL ESSEL` |
| 68 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:25 | `with THE GLADHOUSE (1971 to 1977)\nappearing courtesy of the estate of A. CRAIK` |
| 69 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:26 | `MERLE ······ herself\nVESS ······ himself\nHARRIET ······ mid-motion\nTHE FLOOR MANAGER ······ uncredited, by request` |
| 70 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:27 | `and CHUM\nas himself` |
| 71 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:28 | `made with GODOT\ncaptured to tape at WGLD, channel 58` |
| 72 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:29 | `for everyone who was carried` |
| 73 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:30 | `WGLD signs off.` |
| 74 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:33 | `MERLE ······ RITA IVORI\nVESS ······ RITA IVORI\nHARRIET ······ RITA IVORI\nTHE FLOOR MANAGER ······ RITA IVORI` |
| 75 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:34 | `and CHUM\nas RITA IVORI` |
| 76 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:36 | `ENDING REACHED\n` |
| 77 | UI-CREDITS | NO-TR | 0 |  |  | credits.gd:66 | `the tower light stays on` |
| 78 | UI-PROMPT | TR-FMT | 1 | E |  | dailies_canister.gd:10 | `DAILIES · SCENE 4 TAKE %d · pick up (E)` |
| 79 | TOAST | TR | 0 |  |  | dailies_canister.gd:15 | `Hands full. One canister at a time.` |
| 80 | UI-SAY+UI-BINDER+WORLD | NO-TR | 1 |  |  | dailies_manager.gd:40 hud.gd:256 | `TAKE %d` |
| 81 | TOAST | TR | 0 |  |  | decision_ledger.gd:7 | `AUTHENTICATE. The premiere will go out clean. The club will weep in rows.` |
| 82 | TOAST | TR | 0 |  |  | decision_ledger.gd:8 | `DESTROY. The degausser is warm already. Your hands know how to touch tape.` |
| 83 | TOAST | TR | 0 |  |  | decision_ledger.gd:9 | `PERFORM. Merle, in the doorway, says nothing. The pen was the loudest thing in the building.` |
| 84 | UI-PROMPT | TR-FMT | 1 |  |  | decision_ledger.gd:25 | `ACCESSION LEDGER · entry stands: %s · the ink does not entertain appeals` |
| 85 | UI-PROMPT | TR | 0 |  |  | decision_ledger.gd:27 | `ACCESSION LEDGER · three entries possible · the decision ripens Day 3` |
| 86 | UI-PROMPT | TR | 0 | E |  | decision_ledger.gd:29 | `ACCESSION LEDGER · take up the pen (E)` |
| 87 | UI-PROMPT | TR-FMT | 1 | E,SPACE |  | decision_ledger.gd:30 | `LEDGER · pen over: %s · E next · SPACE commit` |
| 88 | TOAST | TR | 0 |  |  | decision_ledger.gd:37 | `The entry stands. The ink does not entertain appeals.` |
| 89 | TOAST | TR | 0 |  |  | decision_ledger.gd:57 | `INK · the record now includes one name you added.` |
| 90 | TOAST | TR | 0 |  |  | decision_ledger.gd:59 | `Across the building, every monitor cuts to the patch bay. VESS, mid-sentence about slate clusters,` |
| 91 | TOAST | TR | 0 |  |  | decision_ledger.gd:61 | `holds one frame too long. Then bars. His plastic pin is fused into the panel enamel, still warm.` |
| 92 | CAPTION | TR | 0 |  |  | decision_ledger.gd:62 live_production.gd:96 | `[BARS, ALL MONITORS]` |
| 93 | UI-BINDER | NO-TR | 0 |  |  | decision_ledger.gd:63 live_production.gd:97 | `V1 · CREDITED, THEREFORE CAST` |
| 94 | UI-BINDER | NO-TR | 0 |  |  | decision_ledger.gd:63 | `cut mid-sentence; the record includes one name you added` |
| 95 | UI-PROMPT | TR-FMT | 1 | E |  | degausser.gd:8 | `THE DEGAUSSER · burn TAKE %d (E)` |
| 96 | UI-PROMPT | TR | 0 |  |  | degausser.gd:9 | `THE DEGAUSSER · humming · bring it a daily` |
| 97 | TOAST | TR | 0 |  |  | degausser.gd:14 | `It hums, felt-throated. It wants a canister.` |
| 98 | UI-PROMPT | TR-FMT | 1 |  |  | dock_chum.gd:12 | `UNIT %d · counted` |
| 99 | UI-PROMPT | TR-FMT | 1 | E |  | dock_chum.gd:13 | `UNIT %d · count (E)` |
| 100 | TOAST | TR | 0 |  |  | dock_chum.gd:21 | `Your gloved hand rests on it. It is warm. You write the number down anyway.` |
| 101 | TOAST | TR-FMT | 1 |  |  | dock_chum.gd:23 | `UNIT %d · fur gone gray in order.` |
| 102 | TOAST | TR | 0 |  |  | dock_task.gd:27 | `Inventory complete: six units, one anomaly, zero incidents. The dock keeps its word.` |
| 103 | UI-PROMPT | TR | 0 |  |  | dock_task.gd:32 | `INVENTORY CLIPBOARD · filed · the rows keep their order` |
| 104 | UI-PROMPT | TR-FMT | 2 |  |  | dock_task.gd:33 | `INVENTORY CLIPBOARD · count the units (%d of %d)` |
| 105 | TOAST | TR | 0 |  |  | dock_task.gd:38 | `Filed. Six units. The dock keeps its word.` |
| 106 | TOAST | TR | 0 | E |  | dock_task.gd:40 | `Count them by hand. E on each unit. Rows two deep, years in order.` |
| 107 | UI-PROMPT | TR-FMT | 1 |  |  | door.gd:30 | `%s · HELD FOR AIR · moves on the break` |
| 108 | TOAST | TR | 0 |  |  | door.gd:41 | `HELD FOR AIR · the door moves during the break window.` |
| 109 | TOAST | TR-FMT | 1 |  |  | door.gd:45 | `The %s key turns. It was cut for this.` |
| 110 | UI-PROMPT | TR | 0 | E |  | dresser.gd:37 | `RITA'S DRESSER · take stock (E)` |
| 111 | TOAST | TR | 0 |  |  | dresser.gd:43 | `Seven things, squared to the dresser's edge. Everything where you left it.` |
| 112 | TOAST | TR-FMT | 2 |  |  | dresser.gd:46 | `%d of seven remain. Gone: %s. They will be in the footage.` |
| 113 | WORLD+IDENTIFIER | N/A | 0 |  |  | film_cabinet.gd:5 floor_manager.gd:82 | `YOU'RE ON` |
| 114 | IDENTIFIER | N/A | 0 |  |  | film_cabinet.gd:5 | `WRAP IT UP` |
| 115 | IDENTIFIER | N/A | 0 |  |  | film_cabinet.gd:5 | `THIRTY SECONDS` |
| 116 | IDENTIFIER | N/A | 0 |  |  | film_cabinet.gd:5 | `ON TIME` |
| 117 | UI-PROMPT | TR | 0 |  |  | film_cabinet.gd:12 | `FILM CABINET · LOCKED · the key is tagged TRAINING, in green` |
| 118 | UI-PROMPT | TR | 0 | E |  | film_cabinet.gd:14 | `FILM CABINET · run the orientation film again (E)` |
| 119 | UI-PROMPT | TR | 0 | E |  | film_cabinet.gd:15 | `FILM CABINET · run the 1971 orientation film (E)` |
| 120 | TOAST | TR | 0 |  |  | film_cabinet.gd:20 | `Locked. Somewhere, a key is tagged TRAINING in green ink.` |
| 121 | TOAST | TR | 0 |  |  | film_cabinet.gd:29 | `WGLD STAFF ORIENTATION, 1971. A floor manager smiles at you across fifty years.` |
| 122 | TOAST | TR-FMT | 1 |  |  | film_cabinet.gd:33 | `SIGNAL · %s` |
| 123 | TOAST | TR | 0 |  |  | film_cabinet.gd:38 | `Six signals. The film rattles out. It never mentions a seventh.` |
| 124 | TOAST | TR | 0 |  |  | film_cabinet.gd:40 | `The film rattles out, patient as ever.` |
| 125 | UI-PROMPT | TR-CAT | 0 | E |  | finale_breaker.gd:6 live_production.gd:75 | `CART DECK BREAKER · restore (E)` |
| 126 | TOAST | TR | 0 |  |  | finale_breaker.gd:16 | `RESTORED. The board hums agreement.` |
| 127 | UI-PROMPT | TR | 0 | E |  | fire_tape_dock.gd:16 | `DOCK · 1977 · watch it again (E)` |
| 128 | UI-PROMPT | TR | 0 | E |  | fire_tape_dock.gd:17 | `DOCK · 1977 · thread the fire tape (E)` |
| 129 | TOAST | TR | 0 |  | DIALOGUE | fire_tape_dock.gd:31 | `MERLE, from the doorway: 'I was there the first time. I'd rather not be alone for the second.'` |
| 130 | UI-CAPTURE | NO-TR | 0 | E,Q |  | fire_tape_dock.gd:32 | `E · let her stay for it · Q · turn her away` |
| 131 | TOAST | TR | 0 |  |  | fire_tape_dock.gd:42 | `She pulls a chair to the edge of the light and folds her hands. 'Well then.'` |
| 132 | TOAST | TR | 0 |  |  | fire_tape_dock.gd:44 | `She nods. 'That's kind, in its way.' The door closes softly behind her.` |
| 133 | TOAST | TR | 0 |  |  | fire_tape_dock.gd:48 | `1977. The studio is emptying.` |
| 134 | TOAST | TR | 0 |  | TAPE | fire_tape_dock.gd:50 | `ON TAPE · CHUM: 'Stay in your seats, friends! The Gladhouse loves you! Say it with me: the Gladhouse loves'` |
| 135 | TOAST | TR | 0 |  |  | fire_tape_dock.gd:52 | `The line never finishes. The camera pans across an empty floor. No one stands behind it.` |
| 136 | TOAST | TR | 0 |  |  | fire_tape_dock.gd:54 | `Transmission ends before any card, any song, any goodnight.` |
| 137 | TOAST | TR | 0 |  |  | fire_tape_dock.gd:59 | `Something answers the tape from three rooms away. A weighted step. Another.` |
| 138 | TOAST | TR | 0 |  |  | fire_tape_dock.gd:63 | `Merle pats your hand once, warm, and says 'there, that wasn't so'` |
| 139 | TOAST | TR | 0 |  |  | fire_tape_dock.gd:65 | `Her chair is empty. Her voice finishes the sentence from inside the speaker: 'bad.'` |
| 140 | TOAST | TR | 0 |  |  | fire_tape_dock.gd:67 | `Warm to the last unfinished word. The kettle, two rooms away, clicks off by itself.` |
| 141 | CAPTION | TR | 0 |  |  | fire_tape_dock.gd:68 | `[THE KETTLE, TWO ROOMS AWAY, CLICKS OFF]` |
| 142 | UI-BINDER | NO-TR | 0 |  |  | fire_tape_dock.gd:69 | `M1 · THE SECOND VIEWING` |
| 143 | UI-BINDER | NO-TR | 0 |  |  | fire_tape_dock.gd:69 | `carried a second time, mid-sentence` |
| 144 | UI-PROMPT | TR | 0 | E |  | fire_tape_pickup.gd:7 | `REEL · 1977 · THE FINALE, UNFINISHED · take (E)` |
| 145 | TOAST | TR | 0 |  |  | fire_tape_pickup.gd:13 | `TAKEN · the fire tape. The bench has a dock for it now.` |
| 146 | WORLD+IDENTIFIER | N/A | 0 |  |  | floor_manager.gd:16 floor_manager.gd:36 | `FLOOR MANAGER` |
| 147 | TOAST | TR | 0 |  |  | floor_manager.gd:69 | `You moved on camera. Somewhere, a take is ruled spoiled.` |
| 148 | TOAST | TR | 0 |  |  | floor_manager.gd:72 | `The hand lowers. The take holds.` |
| 149 | TOAST | TR | 0 |  |  | floor_manager.gd:83 | `YOU'RE ON. The point. Freeze: you are performance now.` |
| 150 | UI-PROMPT | TR | 0 |  |  | floor_manager.gd:87 | `THE FLOOR MANAGER · headphones connected to nothing` |
| 151 | TOAST | TR | 0 |  |  | floor_manager.gd:94 | `The laminated run sheet is angled away from you. It was always going to be.` |
| 152 | TOAST | TR | 0 |  |  | game_state.gd:118 | `THE LEDGER TAKES IT DOWN.` |
| 153 | TOAST | TR | 0 |  |  | game_state.gd:168 | `Signed. The hand on the slip is not yours, and the log accepts it anyway.` |
| 154 | TOAST | TR-FMT | 1 |  |  | game_state.gd:208 | `READ · filed to memory. (%d of 10 documents)` |
| 155 | TOAST | NO-TR | 1 |  |  | game_state.gd:231 | `CAPTURED · %s · presentation kept` |
| 156 | TOAST | TR-FMT | 1 |  |  | game_state.gd:253 | `You already carry %s.` |
| 157 | TOAST | TR-FMT | 1 |  |  | game_state.gd:257 | `TAKEN · %s` |
| 158 | TOAST | TR-FMT | 1 |  |  | game_state.gd:273 | `CARRYING · SCENE 4 TAKE %d. The degausser is in the climate room.` |
| 159 | TOAST | TR-FMT | 1 |  |  | game_state.gd:282 | `BURNED · TAKE %d. Her name fades from the line. Its read on you resets.` |
| 160 | TOAST | TR-FMT | 1 |  |  | game_state.gd:284 | `BURNED · TAKE %d. The sheet was already clean. The canister burns anyway.` |
| 161 | IDENTIFIER | N/A | 0 |  |  | game_state.gd:295 hud.gd:225 | `LATE NIGHT` |
| 162 | IDENTIFIER | N/A | 0 |  |  | game_state.gd:295 hud.gd:225 | `ONE TAKE` |
| 163 | TOAST | TR-FMT | 1 |  |  | game_state.gd:296 | `MODE · %s` |
| 164 | TOAST | TR | 0 |  |  | game_state.gd:298 | `ONE TAKE · any capture ends the run. (Prototype honors sheet rules until run flow exists.)` |
| 165 | NON-PLAYER | N/A | 2 |  |  | game_state.gd:355 | `[min %.1f] %s` |
| 166 | TOAST | TR-FMT | 1 |  |  | game_state.gd:376 | `KEY IN USE · that key already answers to %s.` |
| 167 | TOAST | TR-FMT | 1 |  |  | game_state.gd:417 | `PHOTOSENSITIVITY-SAFE MODE · %s` |
| 168 | TOAST | TR-CAT | 0 |  |  | game_state.gd:417 | `ON · bands and flicker suppressed` |
| 169 | TOAST | TR-FMT | 2 |  |  | game_state.gd:440 | `ASSET BANKED · %s (%d of 4)` |
| 170 | TOAST | TR | 0 |  |  | game_state.gd:442 | `All four. The finale has everything it needs, when night falls.` |
| 171 | TOAST | TR-FMT | 2 |  |  | game_state.gd:472 | `MORNING · Day %d · Tape %d. The building pretends nothing happened.` |
| 172 | TOAST | TR | 0 |  |  | game_state.gd:475 | `PROTOTYPE COMPLETE · the loop is proven. The rest is production.` |
| 173 | TOAST | TR | 0 |  |  | game_state.gd:477 | `NIGHT · the building belongs to the schedule.` |
| 174 | UI-OBJECTIVE | NO-TR | 0 |  |  | game_state.gd:689 | `TAPE 1 · captured. Thank you for careful hands.` |
| 175 | UI-OBJECTIVE | NO-TR | 1 |  |  | game_state.gd:691 | `ENDING REACHED: %s · thank you for watching · NEW GAME threads a fresh reel` |
| 176 | UI-OBJECTIVE | NO-TR | 1 |  |  | game_state.gd:693 | `ENTRY STANDS: %s · sleep to begin the premiere` |
| 177 | UI-OBJECTIVE | NO-TR | 1 |  |  | game_state.gd:695 | `DAY %d · the ledger waits: AUTHENTICATE · DESTROY · PERFORM` |
| 178 | UI-OBJECTIVE | NO-TR | 0 |  |  | game_state.gd:698 | `NIGHT · optional: burn your dailies (library to climate room) · sleep when ready` |
| 179 | UI-OBJECTIVE | NO-TR | 0 |  |  | game_state.gd:699 | `NIGHT · the schedule owns the halls · sleep when ready` |
| 180 | UI-OBJECTIVE | NO-TR | 0 |  |  | game_state.gd:702 | `DAY 1 · sign the log at S1, the library landing` |
| 181 | UI-OBJECTIVE | NO-TR | 0 |  |  | game_state.gd:704 | `DAY 1 · run the mini-screening at the rec room projector` |
| 182 | UI-OBJECTIVE | NO-TR | 0 |  |  | game_state.gd:706 | `DAY 1 · capture Tape 1 at the bench · it runs real time` |
| 183 | UI-OBJECTIVE | NO-TR | 0 |  |  | game_state.gd:707 | `DAY 1 · end the day at Rita's bed` |
| 184 | UI-OBJECTIVE | NO-TR | 1 |  |  | game_state.gd:709 | `DAY %d · gather the four assets · the ledger ripens` |
| 185 | UI-OBJECTIVE | NO-TR | 1 |  |  | game_state.gd:710 | `DAY %d · the compound is yours: keys, signals, the sheet, the dark` |
| 186 | TOAST | NO-TR | 2 |  |  | game_state.gd:773 | `LOG MIGRATED · format v%d to v%d. Nothing was lost.` |
| 187 | TOAST | NO-TR | 2 |  |  | game_state.gd:777 | `LOG FROM A NEWER BUILD · v%d read by v%d. Proceed gently.` |
| 188 | IDENTIFIER | N/A | 0 |  |  | gen_knob.gd:5 | `1ST DUB` |
| 189 | IDENTIFIER | N/A | 0 |  |  | gen_knob.gd:5 | `3RD GEN` |
| 190 | UI-PROMPT | TR-FMT | 1 | E |  | gen_knob.gd:13 | `GEN KNOB · showing %s · cycle (E)` |
| 191 | TOAST | TR-FMT | 1 |  |  | gen_knob.gd:21 | `GEN SET · the picture agrees to look %s. The scope still reads MASTER.` |
| 192 | TOAST | TR | 0 |  |  | glimpse.gd:18 | `The club unseals the fire corridor for the anniversary. Nobody goes first.` |
| 193 | TOAST | TR | 0 |  |  | glimpse.gd:31 | `At the corridor's elbow, unmediated:` |
| 194 | TOAST | TR | 0 |  |  | glimpse.gd:66 | `A puppeteer whose puppet is missing, or a puppet whose puppeteer is missing. The animation refused to resolve which.` |
| 195 | TOAST | TR | 0 |  |  | glimpse.gd:68 | `The plastic sheeting breathes once, with the draft of something that has already passed.` |
| 196 | TOAST | TR-CAT | 0 |  |  | harriet.gd:8 | `And now. The tour continues.` |
| 197 | TOAST | TR-CAT | 0 |  | DIALOGUE | harriet.gd:8 | `'And now.'` |
| 198 | TOAST | TR-CAT | 0 |  | DIALOGUE | harriet.gd:8 | `'But first.'` |
| 199 | TOAST | TR-CAT | 0 |  | DIALOGUE | harriet.gd:8 | `'When we come back.'` |
| 200 | UI-PROMPT | TR | 0 |  |  | harriet.gd:79 | `HARRIET · mid-motion` |
| 201 | UI-PROMPT | TR | 0 | E |  | harriet.gd:80 | `HARRIET · in her chair (E)` |
| 202 | TOAST | TR | 0 |  |  | harriet.gd:86 | `Two of her. Neither resumes. The schedule has stopped scheduling this chair.` |
| 203 | TOAST | TR | 0 |  |  | harriet.gd:92 | `You slide the slip from her fingers. They do not close on the absence. Nothing does, yet.` |
| 204 | TOAST | TR | 0 |  |  | harriet.gd:95 | `She does not resume until the return cue. Her cup has been rising since Tape 1.` |
| 205 | TOAST | TR | 0 | E |  | harriet.gd:98 | `Her hand holds a signature slip. Paper, free, unmoving. (E again to take it)` |
| 206 | TOAST | TR | 0 |  |  | harriet.gd:102 | `The break comes. Harriet freezes, and one frame later, freezes again, an inch to the left.` |
| 207 | TOAST | TR | 0 |  |  | harriet.gd:104 | `Doubled at the shoulders. Both mouths open on different vowels. The teacup rises in two hands at two heights.` |
| 208 | CAPTION | TR | 0 |  |  | harriet.gd:105 | `[ONE FRAME LEFT OF HERSELF]` |
| 209 | UI-BINDER | NO-TR | 0 |  |  | harriet.gd:107 | `H2 · THE SPLICE` |
| 210 | UI-BINDER | NO-TR | 0 |  |  | harriet.gd:107 | `doubled; the schedule stopped scheduling her` |
| 211 | TOAST | TR | 0 |  |  | harriet.gd:112 | `The break ends. Harriet's chair is warm. Harriet is not in it, or anywhere.` |
| 212 | TOAST | TR | 0 |  |  | harriet.gd:114 | `The film cabinet will not fully close. Inside, folded small, with leader tape where her voice was.` |
| 213 | CAPTION | TR | 0 |  |  | harriet.gd:115 | `[A REEL, LABELED IN HER HAND: ME]` |
| 214 | UI-BINDER | NO-TR | 0 |  |  | harriet.gd:116 | `H1 · CONTINUITY` |
| 215 | UI-BINDER | NO-TR | 0 |  |  | harriet.gd:116 | `edited for continuity; the slip signs in her hand` |
| 216 | TOAST | TR-FMT | 1 |  |  | harriet.gd:120 | `HARRIET · %s` |
| 217 | UI-PROMPT | TR | 0 | E |  | harriet_note.gd:16 | `A FOLDED NOTE · Harriet's hand · read (E)` |
| 218 | TOAST | TR | 0 |  | DIALOGUE | harriet_note.gd:24 | `'Hold your applause.' Both hands pressed down, twice. They added that one later. You'll want it.` |
| 219 | UI-MENU | TR | 0 |  |  | hud.gd:114 | `INTERMISSION · WGLD holds its breath` |
| 220 | UI-MENU | TR | 0 |  |  | hud.gd:119 | `THE BOOTH` |
| 221 | UI-MENU | TR | 0 |  |  | hud.gd:123 | `RETURN TO TITLE · progress holds at your last signature` |
| 222 | TOAST | TR | 0 |  |  | hud.gd:170 | `The room eats every sound you make. The radio, somehow, keeps its own.` |
| 223 | CAPTION | TR | 0 |  |  | hud.gd:171 | `[NO ECHO]` |
| 224 | WORLD | N/A | 1 |  |  | hud.gd:174 | `● REC · SAFE WHILE LIT · %04.1f` |
| 225 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:227 | `THE BINDER · PRESENTATION FORM · TAB closes` |
| 226 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:229 | `MODE · press 1 / 2 / 3` |
| 227 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:230 | `  1 MATINEE · unlimited paper, gentler sheet` |
| 228 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:231 | `  2 LATE NIGHT · three lines per station, four sheet lines` |
| 229 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:232 | `  3 ONE TAKE · any capture is final` |
| 230 | UI-BINDER | NO-TR | 1 |  |  | hud.gd:233 | `  current: %s` |
| 231 | UI-BINDER | NO-TR | 1 | T |  | hud.gd:235 | `TBC · %s · toggle with T anywhere` |
| 232 | UI-BINDER | NO-TR | 0 | E,SPACE,Q |  | hud.gd:237 | `CONTROLS · WASD move · E interact · SPACE respond · Q improvise` |
| 233 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:243 | `THE BINDER · TAB closes` |
| 234 | UI-BINDER | NO-TR | 1 |  |  | hud.gd:245 | `MODE: LATE NIGHT · TBC: %s` |
| 235 | UI-BINDER | NO-TR | 1 |  |  | hud.gd:246 | `SIGNATURES ON FILE: %d` |
| 236 | UI-BINDER | NO-TR | 1 |  |  | hud.gd:248 | `CASUALTY LEDGER · %s` |
| 237 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:248 | `NO ENTRIES. KEEP IT SO.` |
| 238 | UI-BINDER | NO-TR | 4 |  |  | hud.gd:251 | `  %s · %s · Day %d · %s` |
| 239 | UI-BINDER | NO-TR | 1 |  |  | hud.gd:253 | `CASTING SHEET: %d of 4 guest lines` |
| 240 | UI-BINDER | NO-TR | 1 |  |  | hud.gd:254 | `PRODUCER TRACK: %d` |
| 241 | UI-BINDER | NO-TR | 1 |  |  | hud.gd:255 | `KEYS: %s` |
| 242 | UI-BINDER | NO-TR | 2 |  |  | hud.gd:256 | `DAILIES IN THE STACKS: %d · carrying: %s` |
| 243 | UI-BINDER | NO-TR | 1 |  |  | hud.gd:257 | `COVERAGE READS YOU AS: %s (this session)` |
| 244 | UI-BINDER | NO-TR | 2 |  |  | hud.gd:258 | `LELAND · wear %.0f%% · answers %d of 5` |
| 245 | UI-BINDER | NO-TR | 1 |  |  | hud.gd:259 | `PHOTOSAFE: %s (P)` |
| 246 | UI-BINDER | NO-TR | 1 |  |  | hud.gd:260 | `VESS · %s` |
| 247 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:260 | `credited in the margin` |
| 248 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:260 | `insight held, uncredited` |
| 249 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:260 | `his door is ajar` |
| 250 | UI-BINDER | NO-TR | 2 |  |  | hud.gd:261 | `SIGNALS KNOWN: %d%s` |
| 251 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:266 | `  none yet. the bench is patient.` |
| 252 | UI-SAY | NO-TR | 0 |  |  | hud.gd:278 hud.gd:314 | `◼ CAPTURED` |
| 253 | UI-SAY | NO-TR | 0 |  |  | hud.gd:281 | `THE GLADHOUSE` |
| 254 | UI-SAY | NO-TR | 1 |  |  | hud.gd:282 | `SCENE 4 · TAKE %d` |
| 255 | UI-SAY | NO-TR | 0 |  |  | hud.gd:284 hud.gd:317 | `◀◀ REWINDING` |
| 256 | UI-SAY | NO-TR | 0 |  |  | hud.gd:292 | `ITEM MISSING` |
| 257 | UI-SAY | NO-TR | 1 |  |  | hud.gd:293 | `your %s is gone from the dresser. it will be in the footage.` |
| 258 | UI-SAY | NO-TR | 0 |  |  | hud.gd:296 | `THE SHEET IS FULL` |
| 259 | UI-SAY | NO-TR | 0 |  |  | hud.gd:297 | `the rewind would not stop. (prototype: the sheet resets.)` |
| 260 | UI-SAY | NO-TR | 0 |  |  | hud.gd:300 | `PRESENTATION KEPT` |
| 261 | UI-SAY | NO-TR | 0 |  |  | hud.gd:301 | `resume from your last signature.` |
| 262 | UI-SAY | NO-TR | 0 |  |  | hud.gd:321 | `THE REWIND DOES NOT STOP` |
| 263 | UI-SAY | NO-TR | 0 |  |  | hud.gd:325 | `STARRING RITA IVORI` |
| 264 | UI-SAY | TR | 0 |  |  | hud.gd:348 | `ENDING · ` |
| 265 | UI-SAY | TR | 0 |  |  | hud.gd:350 | `THE LEDGER, READ ALOUD, because that is what ledgers are for:` |
| 266 | UI-SAY | TR | 0 |  |  | hud.gd:354 | `HER CARD, HER OWN STAMP REGISTER:` |
| 267 | UI-SAY | TR | 0 |  |  | hud.gd:354 | `TRANSITION UNRESOLVED.` |
| 268 | UI-SAY | TR | 0 |  |  | hud.gd:356 | `THE 58 CLUB:` |
| 269 | UI-SAY | TR-FMT | 1 |  |  | hud.gd:356 | `fifty-eight, minus %d.` |
| 270 | UI-SAY | TR | 0 |  |  | hud.gd:367 | `THE RESPOND SIGN LIGHTS.` |
| 271 | UI-SAY | TR | 0 |  |  | hud.gd:367 | `Alone. Unasked.` |
| 272 | UI-SAY | NO-TR | 0 |  |  | hud.gd:369 | `TAPE 1 OF 5. THE PROGRAM CONTINUES.` |
| 273 | UI-SAY | NO-TR | 0 |  |  | hud.gd:370 | `Your ledger, your signatures, and your paper carry into the full game. WISHLIST RESTORATION.` |
| 274 | UI-SAY | NO-TR | 0 |  |  | hud.gd:372 | `  ·  The 58 Club thanks you for careful hands. (any key)` |
| 275 | UI-SAY | TR | 0 |  |  | hud.gd:396 | `You work through the night.` |
| 276 | UI-SAY | TR | 0 |  |  | hud.gd:396 | `Reel by reel. Entry by entry.` |
| 277 | UI-SAY | TR | 0 |  |  | hud.gd:397 | `Your hands know no other way to touch tape.` |
| 278 | UI-SAY | TR | 0 |  |  | hud.gd:399 | `No one comes to the doorway.` |
| 279 | UI-SAY | TR | 0 |  |  | hud.gd:399 | `You keep working because the alternative is the doorway.` |
| 280 | UI-SAY | TR | 0 |  |  | hud.gd:400 | `In the kitchen, later: cobbler, cold on the counter,` |
| 281 | UI-SAY | TR | 0 |  |  | hud.gd:400 | `plated for two.` |
| 282 | UI-SAY | TR | 0 | M |  | hud.gd:401 | `The ledger, weeks later, a new hand: M. OYELARAN, INCOMING CONSERVATOR. Beneath it, smaller: THE KITCHEN LIGHT WAS ON. NOBODY HAD EATEN.` |
| 283 | UI-SAY | TR | 0 |  |  | hud.gd:403 | `MERLE, in the doorway.` |
| 284 | UI-SAY | TR | 0 |  |  | hud.gd:403 | `No anger anywhere on her, which is the worst available outcome.` |
| 285 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:404 | `'Oh, honey. We have copies.'` |
| 286 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:404 | `'Everyone has copies. That's what love is now.'` |
| 287 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:405 | `'There's cobbler.'` |
| 288 | UI-SAY | TR | 0 | M |  | hud.gd:406 | `The ledger, weeks later, a new hand: M. OYELARAN, INCOMING CONSERVATOR.` |
| 289 | UI-CREDITS | NO-TR | 0 |  |  | hud.gd:408 | `3 · THE BURN` |
| 290 | UI-SAY | TR | 0 |  |  | hud.gd:412 | `The premiere goes out clean.` |
| 291 | UI-SAY | TR | 0 |  |  | hud.gd:412 | `The club weeps with joy, in rows.` |
| 292 | UI-SAY | TR | 0 |  |  | hud.gd:414 | `In the office you inherit: a chair, still warm,` |
| 293 | UI-SAY | TR | 0 |  |  | hud.gd:414 | `facing the monitor wall. You do not move it.` |
| 294 | UI-SAY | TR | 0 |  |  | hud.gd:416 | `At the first staff meeting: an empty headset on the table,` |
| 295 | UI-SAY | TR | 0 |  |  | hud.gd:416 | `channel open. Nobody closes it.` |
| 296 | UI-SAY | TR | 0 |  |  | hud.gd:417 | `In resolution the puppet was never built to survive,` |
| 297 | UI-SAY | TR | 0 |  |  | hud.gd:417 | `it leans to the lens.` |
| 298 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:418 | `CHUM · 'There she is. Our new friend.'` |
| 299 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:418 | `'Say it with me, everyone.'` |
| 300 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:419 | `'WELCOME HOME.'` |
| 301 | UI-SAY | TR | 0 |  |  | hud.gd:421 | `No one says the welcome twice.` |
| 302 | UI-SAY | TR | 0 |  |  | hud.gd:421 | `It is administered by the room itself, which is worse.` |
| 303 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:423 | `MERLE · 'Now Merle is just going to watch it again.'` |
| 304 | UI-CREDITS | NO-TR | 0 |  |  | hud.gd:425 | `2 · THE NEW PRODUCER` |
| 305 | UI-SAY | TR | 0 |  |  | hud.gd:453 | `Fifty years silent.` |
| 306 | UI-SAY | TR | 0 |  |  | hud.gd:453 | `The bell rings once, three feet behind camera position.` |
| 307 | UI-SAY | NO-TR | 0 |  |  | hud.gd:454 | `CAMERA ONE` |
| 308 | UI-SAY | NO-TR | 0 | SPACE |  | hud.gd:455 | `SPACE · deliver the line` |
| 309 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:457 | `'That's our show. That was always our show.'` |
| 310 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:458 | `'There's no one at home anymore. The lights are off.'` |
| 311 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:458 | `'The children grew up. You can stop looking for them.'` |
| 312 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:459 hud.gd:483 | `'Say goodnight, Chum.'` |
| 313 | UI-SAY | TR | 0 |  |  | hud.gd:461 | `On every screen at once, inside the frame he was cropped from,` |
| 314 | UI-SAY | TR | 0 |  |  | hud.gd:461 | `he steps to center and is allowed to be whole.` |
| 315 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:462 | `LELAND · 'Goodnight, everyone.'` |
| 316 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:462 | `'It's okay. Nobody's watching.'` |
| 317 | UI-SAY | TR | 0 |  |  | hud.gd:463 | `CHUM, small, the performance finally allowed to end:` |
| 318 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:463 | `'Goodnight, Gladhouse.'` |
| 319 | UI-SAY | TR | 0 |  |  | hud.gd:464 | `The card. Then, for the first time in fifty years,` |
| 320 | UI-SAY | TR | 0 |  |  | hud.gd:464 | `dark that is only dark.` |
| 321 | UI-SAY | TR | 0 |  |  | hud.gd:465 | `Harriet's cup, rising since Tape 1,` |
| 322 | UI-SAY | TR | 0 |  |  | hud.gd:465 | `comes down.` |
| 323 | UI-CREDITS | NO-TR | 0 |  |  | hud.gd:467 | `1A · SIGN-OFF` |
| 324 | UI-SAY | TR | 0 |  |  | hud.gd:469 | `Someone must close the house from inside.` |
| 325 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:470 | `RITA · 'I'll close up.'` |
| 326 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:470 | `'Goodnight, everyone.'` |
| 327 | UI-SAY | TR | 0 |  |  | hud.gd:471 | `The ledger's last line is in green ink, not hers:` |
| 328 | UI-SAY | TR | 0 |  |  | hud.gd:471 | `SHE CLOSED IT PROPERLY. FILE UNDER: SAINTS.` |
| 329 | UI-SAY | TR | 0 |  |  | hud.gd:473 | `Beneath it, the same green ink, smaller:` |
| 330 | UI-SAY | TR | 0 |  |  | hud.gd:473 | `FILE UNDER: STAFF.` |
| 331 | UI-SAY | TR | 0 |  |  | hud.gd:475 | `Beneath everything, in pencil, because the green ink is gone from the world:` |
| 332 | UI-SAY | TR | 0 |  |  | hud.gd:475 | `AND THE READER, UNFILED.` |
| 333 | UI-CREDITS | NO-TR | 0 |  |  | hud.gd:477 | `1B · SIGN-OFF` |
| 334 | UI-SAY | TR | 0 |  |  | hud.gd:481 | `Every light in the building goes down in reverse order` |
| 335 | UI-SAY | TR | 0 |  |  | hud.gd:481 | `of the tour you walked on Day 1. Entry last.` |
| 336 | UI-SAY | TR | 0 |  |  | hud.gd:482 | `From every speaker at once, a reading voice, patient:` |
| 337 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:482 | `'There's no one at home anymore. The lights are off in the little house.'` |
| 338 | UI-SAY | TR | 0 |  |  | hud.gd:483 | `Fifty years late, and exactly on time.` |
| 339 | UI-SAY | TR | 0 |  |  | hud.gd:484 | `The transmitter unclenches. The tower light, for the first time,` |
| 340 | UI-SAY | TR | 0 |  |  | hud.gd:484 | `goes out, and it reads as rest.` |
| 341 | WORLD+IDENTIFIER | N/A | 0 |  |  | hud.gd:485 world_builder.gd:1239 | `THE COMPLETED SIGN-OFF` |
| 342 | UI-CREDITS | NO-TR | 0 |  |  | hud.gd:486 | `4c · THE COMPLETED SIGN-OFF` |
| 343 | UI-SAY | TR | 0 |  |  | hud.gd:490 | `The show runs whole. Every part, one performer.` |
| 344 | UI-SAY | TR | 0 |  |  | hud.gd:490 | `The rows applaud on the mark you taught them by dying politely near it.` |
| 345 | UI-SAY | TR | 0 |  |  | hud.gd:491 | `At sign-off, the card:` |
| 346 | UI-SAY | TR | 0 |  |  | hud.gd:491 | `STARRING RITA IVORI. And beneath it: AND RITA IVORI. AND RITA IVORI.` |
| 347 | UI-SAY | TR | 0 |  |  | hud.gd:492 | `The ledger's last page is full,` |
| 348 | UI-SAY | TR | 0 |  |  | hud.gd:492 | `and every line of it is a casting decision you made.` |
| 349 | UI-CREDITS | NO-TR | 0 |  |  | hud.gd:494 | `0 · A ONE-WOMAN SHOW` |
| 350 | UI-SAY | TR | 0 |  |  | hud.gd:498 | `You close the felt door from inside.` |
| 351 | UI-SAY | TR | 0 |  |  | hud.gd:498 | `Outside the format entirely.` |
| 352 | UI-SAY | TR | 0 |  |  | hud.gd:499 | `RITA, into the radio, to every set on every band:` |
| 353 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:499 | `'This is WGLD, Channel fifty-eight, leaving the air.'` |
| 354 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:500 | `'The show is over.'` |
| 355 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:500 | `'You can put the toys away.'` |
| 356 | UI-SAY | TR | 0 |  |  | hud.gd:501 | `The erase loop propagates outward like weather.` |
| 357 | UI-SAY | TR | 0 |  |  | hud.gd:502 | `You watch the archive die, reel by reel,` |
| 358 | UI-SAY | TR | 0 |  |  | hud.gd:502 | `your hands folded, because there is nothing left for them to save.` |
| 359 | UI-SAY | TR | 0 |  |  | hud.gd:504 | `Your right arm answers slowly now, and will from here on.` |
| 360 | UI-SAY | TR | 0 |  |  | hud.gd:504 | `The ledger states it flatly, because that is how the ledger states things.` |
| 361 | UI-SAY | TR | 0 |  |  | hud.gd:505 | `FINAL LEDGER LINE, steady, left-handed:` |
| 362 | UI-SAY | TR | 0 |  | DIALOGUE | hud.gd:505 hud.gd:512 | `'Signed off.'` |
| 363 | UI-CREDITS | NO-TR | 0 |  |  | hud.gd:507 | `4b · DEAD AIR · HER HAND` |
| 364 | UI-SAY | TR | 0 |  |  | hud.gd:510 | `In master control, after: the Floor Manager, headset still cued,` |
| 365 | UI-SAY | TR | 0 |  |  | hud.gd:510 | `arm locked in a YOU'RE ON point at a camera that faces nothing.` |
| 366 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:511 | `F1 · THE FADER` |
| 367 | UI-BINDER | NO-TR | 0 |  |  | hud.gd:511 | `held it through sign-off; finished the way a gesture is finished` |
| 368 | UI-SAY | TR | 0 |  |  | hud.gd:512 | `FINAL LEDGER LINE, steady:` |
| 369 | UI-SAY | TR | 0 |  |  | hud.gd:513 | `Beneath it, another hand, block capitals:` |
| 370 | UI-SAY | TR | 0 |  |  | hud.gd:513 | `CUE GIVEN.` |
| 371 | UI-CREDITS | NO-TR | 0 |  |  | hud.gd:515 | `4a · DEAD AIR · HIS HAND` |
| 372 | WORLD | N/A | 1 |  |  | hud.gd:523 | `SHEET · %d/4` |
| 373 | UI-CLOCK | NO-TR | 0 |  |  | hud.gd:531 | `NIGHT · ` |
| 374 | UI-CLOCK | NO-TR | 1 |  |  | hud.gd:531 | `DAY %d · ` |
| 375 | WORLD | N/A | 2 |  |  | hud.gd:542 | `SIGNED · %s · %s line(s) of paper left` |
| 376 | WORLD | N/A | 1 |  |  | hud.gd:547 | `%s · NO PAPER. The log does not forgive on Late Night.` |
| 377 | WORLD | N/A | 1 | T |  | hud.gd:561 | `TBC: %s  (T)` |
| 378 | UI-PROMPT | TR | 0 | E |  | impossible_crate.gd:12 | `A CRATE · Vess is hovering (E)` |
| 379 | TOAST | TR | 0 | E | DIALOGUE | impossible_crate.gd:20 | `VESS · 'Storage auction. Paid cash. Unit was under CRAIK, E. That's Edith. She kept everything.'` |
| 380 | TOAST | TR | 0 |  | DIALOGUE | impossible_crate.gd:22 | `VESS · 'Tapes dated after the fire. After. Tell me what that means, because I've stopped being able to say it out loud.'` |
| 381 | TOAST | TR | 0 |  |  | impossible_crate.gd:24 | `The seance reel is on the bench now. He would not carry it further than that.` |
| 382 | NON-PLAYER | N/A | 2 |  |  | invariant_parser.gd:6 | `RESTORATION · INVARIANTS SCORECARD · bot=%s minutes=%.0f\n` |
| 383 | NON-PLAYER | N/A | 0 |  |  | invariant_parser.gd:27 | `I01 warn-precedes-strike: N/A (no coverage log)\nI02 no-strike-thru-wall: N/A\nI22 heard-noise-attribution: N/A\n` |
| 384 | NON-PLAYER | N/A | 0 |  |  | invariant_parser.gd:33 | `WARN ` |
| 385 | NON-PLAYER | N/A | 0 |  |  | invariant_parser.gd:35 | `STRIKE ` |
| 386 | NON-PLAYER | N/A | 0 |  |  | invariant_parser.gd:41 | `toward heard noise` |
| 387 | NON-PLAYER | N/A | 1 |  |  | invariant_parser.gd:43 | `I01 warn-precedes-strike: %s\n` |
| 388 | NON-PLAYER | N/A | 1 |  |  | invariant_parser.gd:43 invariant_parser.gd:44 | `FAIL x%d` |
| 389 | NON-PLAYER | N/A | 1 |  |  | invariant_parser.gd:44 | `I02 no-strike-thru-wall: %s\n` |
| 390 | NON-PLAYER | N/A | 2 |  |  | invariant_parser.gd:45 | `I22 heard-noise-attribution: %s (%d attributed)\n` |
| 391 | NON-PLAYER | N/A | 0 |  |  | invariant_parser.gd:52 | `I07 cascade-liveness: N/A (cascade did not run)\n` |
| 392 | NON-PLAYER | N/A | 0 |  |  | invariant_parser.gd:55 | `I07 cascade-liveness: FAIL (violation logged)\n` |
| 393 | NON-PLAYER | N/A | 1 |  |  | invariant_parser.gd:56 | `I07 cascade-liveness: PASS (%d checks)\n` |
| 394 | NON-PLAYER | N/A | 1 |  |  | invariant_parser.gd:62 | `I06 fail-forward-finale: %s\n` |
| 395 | NON-PLAYER | N/A | 0 |  |  | invariant_parser.gd:62 | `FAIL (fail bot produced no premiere log)` |
| 396 | IDENTIFIER+NON-PLAYER | N/A | 0 |  |  | invariant_parser.gd:70 live_production.gd:400 | `club auto-fix` |
| 397 | NON-PLAYER | N/A | 1 |  |  | invariant_parser.gd:77 | `FAIL (slow fixes x%d)` |
| 398 | NON-PLAYER | N/A | 0 |  |  | invariant_parser.gd:77 | `WEAK (no incidents rolled)` |
| 399 | NON-PLAYER | N/A | 3 |  |  | invariant_parser.gd:78 | `I06 fail-forward-finale: %s (%d incidents, %d auto-fixed)\n` |
| 400 | UI-PROMPT | TR-CAT | 0 |  |  | key_item.gd:6 | `a key` |
| 401 | TOAST | TR | 0 |  |  | live_production.gd:9 | `The tally lights swap. Camera one claims it is not program.` |
| 402 | TOAST | TR | 0 |  |  | live_production.gd:10 | `Half the house lights drop. The club murmurs an apology.` |
| 403 | TOAST | TR | 0 |  |  | live_production.gd:11 | `The boom drifts into frame. Somebody's grandson is so sorry.` |
| 404 | TOAST | TR | 0 |  |  | live_production.gd:12 | `The cue cards shuffle themselves. Vess swears he stacked them.` |
| 405 | TOAST | TR | 0 |  |  | live_production.gd:15 | `TALLY BUS RESET · the lights agree with reality again.` |
| 406 | TOAST | TR | 0 |  |  | live_production.gd:16 | `HOUSE DIMMER RESTORED · the room comes back, embarrassed.` |
| 407 | TOAST | TR | 0 |  |  | live_production.gd:17 | `BOOM WINCHED · the frame is clean.` |
| 408 | TOAST | TR | 0 |  |  | live_production.gd:18 | `CARDS RESTACKED · in Vess's order, which was right.` |
| 409 | TOAST | TR | 0 |  | DIALOGUE | live_production.gd:57 | `THE FLOOR MANAGER · 'In five, four...' The hands do the rest.` |
| 410 | UI-CAPTURE | NO-TR | 0 | SPACE |  | live_production.gd:61 | `CUE 1 · COLD OPEN · cut to camera one (1) · stand the mark · SPACE` |
| 411 | TOAST | TR | 0 |  | DIALOGUE | live_production.gd:62 | `RITA · 'Welcome back to the Gladhouse, friends. It's a special night.'` |
| 412 | TOAST | TR | 0 |  | DIALOGUE | live_production.gd:64 | `RITA · 'It's our last night.'  CHUM, warm as ever: 'Ohhh, don't be sad!'` |
| 413 | TOAST | TR | 0 |  | DIALOGUE | live_production.gd:66 | `CHUM · 'Every good day ends with a goodnight. That's how you know it was good.'` |
| 414 | TOAST | TR | 0 |  |  | live_production.gd:72 | `The cart deck loses power. The club is helping.` |
| 415 | UI-CAPTURE | NO-TR | 0 |  |  | live_production.gd:76 | `CUE 2 · RESTORE THE CART DECK AT THE PATCH BAY` |
| 416 | TOAST | TR-FMT | 1 |  |  | live_production.gd:80 | `TAKE %d · from the top of the cue.` |
| 417 | UI-CAPTURE | NO-TR | 0 | SPACE |  | live_production.gd:81 | `CUE 2 · THE SONG · camera one (1) · back to the mark · SPACE` |
| 418 | TOAST | TR | 0 |  | DIALOGUE | live_production.gd:82 | `EVERYONE · 'Close the door and dim the light. Fold the day away.'` |
| 419 | TOAST | TR | 0 |  | DIALOGUE | live_production.gd:84 spectro_dock.gd:28 | `'Everyone we love is home. And no one has to stay.'` |
| 420 | TOAST | TR | 0 |  |  | live_production.gd:89 | `VESS, at the final breaker, not looking at you.` |
| 421 | TOAST | TR | 0 |  | DIALOGUE | live_production.gd:91 | `VESS · 'The margin. You wrote my name. Somebody's name should be on something. Go finish it.'` |
| 422 | TOAST | TR | 0 |  |  | live_production.gd:93 | `The handle drops. The lights hold. On every monitor at once: VESS at the breaker, mid-` |
| 423 | TOAST | TR | 0 |  |  | live_production.gd:95 | `bars. The pin, fused into the enamel. The record was a call sheet all along.` |
| 424 | UI-BINDER | NO-TR | 0 |  |  | live_production.gd:97 | `taken at the breaker she kept; the credit was the casting` |
| 425 | TOAST | TR | 0 |  |  | live_production.gd:100 | `The final breaker. A plastic pin, fused in the enamel, marks where a hand was.` |
| 426 | UI-PROMPT | TR-CAT | 0 | E |  | live_production.gd:103 live_production.gd:110 | `MAIN BUS · earn the retake (E)` |
| 427 | UI-CAPTURE | NO-TR | 0 |  |  | live_production.gd:104 live_production.gd:111 | `BLACKOUT · EARN THE RETAKE AT THE PATCH BAY` |
| 428 | TOAST | TR | 0 |  |  | live_production.gd:107 | `The final breaker. VESS. The handle. The dark.` |
| 429 | TOAST | TR | 0 |  |  | live_production.gd:113 | `Again. The dark is patient.` |
| 430 | TOAST | TR | 0 |  |  | live_production.gd:118 | `The final break arrives, and the rundown simply ends.` |
| 431 | TOAST | TR | 0 |  |  | live_production.gd:120 | `The program closes itself, correctly, using the ending it was given.` |
| 432 | UI-CAPTURE | NO-TR | 0 | SPACE,Q |  | live_production.gd:125 | `FINAL BREAK · SPACE places for cue three · Q divert to the dead room` |
| 433 | TOAST | TR | 0 |  |  | live_production.gd:137 | `The sign-off ends three rooms away. The window is gone. Places.` |
| 434 | UI-CAPTURE | NO-TR | 0 |  |  | live_production.gd:143 | `CUE 3 · CLOSE THE HOUSE · the little door, by hand` |
| 435 | TOAST | TR | 0 |  |  | live_production.gd:146 | `Now close it. On camera.` |
| 436 | TOAST | TR | 0 |  |  | live_production.gd:149 | `The house is closed. The studio holds its breath on purpose.` |
| 437 | TOAST | TR | 0 |  |  | live_production.gd:157 | `The premiere begins on schedule, because it was never waiting on anyone.` |
| 438 | TOAST | TR | 0 |  |  | live_production.gd:159 | `The monitors put up the first title card: HOSTED BY RITA IVORI.` |
| 439 | TOAST | TR | 0 |  |  | live_production.gd:161 | `SONGS BY RITA IVORI. CRAFT BY RITA IVORI. AUDIENCE: RITA IVORI.` |
| 440 | TOAST | TR | 0 |  |  | live_production.gd:163 | `You are the only name left, and the show has never once had a casting problem.` |
| 441 | TOAST | TR | 0 |  |  | live_production.gd:169 | `Cut away from a smile. Cut back to an empty chair.` |
| 442 | TOAST | TR | 0 |  |  | live_production.gd:170 | `Cut back to something half-resolved, interlaced, still trying to applaud.` |
| 443 | TOAST | TR | 0 |  |  | live_production.gd:171 | `A seat empties between frames. The applause continues at former strength.` |
| 444 | CAPTION | TR | 0 |  |  | live_production.gd:178 | `[A CHAIR, BETWEEN FRAMES]` |
| 445 | TOAST | TR | 0 |  |  | live_production.gd:183 | `Coverage must come from somewhere. THE FLOOR MANAGER steps into frame` |
| 446 | TOAST | TR | 0 |  |  | live_production.gd:185 | `and gives YOU'RE ON to a camera that is not on the run sheet.` |
| 447 | TOAST | TR | 0 |  |  | live_production.gd:187 | `The unlisted camera accepts him. The frame he entered never cuts away, because nothing is switched to it.` |
| 448 | CAPTION | TR | 0 |  |  | live_production.gd:188 | `[YOU'RE ON · TO NOTHING LISTED]` |
| 449 | UI-BINDER | NO-TR | 0 |  |  | live_production.gd:189 | `F2 · THE UNLISTED CAMERA` |
| 450 | UI-BINDER | NO-TR | 0 |  |  | live_production.gd:189 | `cued a camera the run sheet never carried` |
| 451 | TOAST | TR | 0 |  |  | live_production.gd:196 | `No one reaches for the master fader. So you do, first, before the run.` |
| 452 | TOAST | TR | 0 |  |  | live_production.gd:200 | `The sign-off needs the master fader held through to black. He is already reaching for it.` |
| 453 | UI-CAPTURE | NO-TR | 0 | E,SPACE |  | live_production.gd:201 | `SPACE · let him hold it · E · hold it yourself first, then run late` |
| 454 | TOAST | TR | 0 |  |  | live_production.gd:205 | `His hand settles on the fader. The other rises: YOU'RE ON. Go.` |
| 455 | UI-CAPTURE | NO-TR | 0 |  |  | live_production.gd:216 | `HOLD THE FADER · the transmitter argues through your arm` |
| 456 | TOAST | TR | 0 |  |  | live_production.gd:218 | `Your right arm takes the argument. It will keep a little of it. Now run.` |
| 457 | UI-CAPTURE | NO-TR | 0 |  |  | live_production.gd:228 | `THE LAST CROSSING · reach the little door · you are not in this broadcast; nothing on the log protects you` |
| 458 | WORLD | N/A | 0 |  |  | live_production.gd:262 | `CHUM · ON HIS MARK` |
| 459 | UI-PROMPT | TR-CAT | 0 | E |  | live_production.gd:288 | `AUX PANEL · resets (E)` |
| 460 | UI-PROMPT | TR-CAT | 0 | E |  | live_production.gd:289 | `BOOM WINCH · crank (E)` |
| 461 | UI-PROMPT | TR-CAT | 0 | E |  | live_production.gd:290 | `CARD STAND · restack (E)` |
| 462 | UI-CAPTURE | NO-TR | 1 |  |  | live_production.gd:322 | ` · PGM CAM %d` |
| 463 | UI-CAPTURE | NO-TR | 0 |  |  | live_production.gd:324 | ` · INCIDENT: ` |
| 464 | UI-CAPTURE | NO-TR | 0 |  |  | live_production.gd:326 | ` · ON MARK` |
| 465 | TOAST | TR | 0 |  |  | live_production.gd:331 | `The tally is lying. Camera one IS program. Trust the mark, not the light.` |
| 466 | TOAST | TR | 0 |  |  | live_production.gd:338 | `You call it blind. Correctly.` |
| 467 | TOAST | TR | 0 |  |  | live_production.gd:341 | `Hold. The boom is in frame. Winch it, or wait it out.` |
| 468 | TOAST | TR | 0 |  |  | live_production.gd:346 | `Wrong camera is program. The Floor Manager's hand does not move.` |
| 469 | TOAST | TR | 0 |  |  | live_production.gd:376 | `Nothing wrong here right now. The club appreciates the diligence.` |
| 470 | IDENTIFIER | N/A | 0 |  |  | live_production.gd:378 | `fixed by hand` |
| 471 | NON-PLAYER | N/A | 3 |  |  | live_production.gd:384 | `RESOLVED %s (%s) t=%.1f` |
| 472 | NON-PLAYER | N/A | 3 |  |  | live_production.gd:405 | `INCIDENT %s (fail_takes %d, interval %.0f)` |
| 473 | TOAST | TR-CAT | 0 |  |  | live_production.gd:406 | `THE CLUB IS HELPING · ` |
| 474 | TOAST | TR | 0 |  |  | liveness_check.gd:21 | `LIVENESS VIOLATION · the panel is gone. File this.` |
| 475 | NON-PLAYER | N/A | 0 |  |  | liveness_check.gd:22 | `VIOLATION · console invalid` |
| 476 | NON-PLAYER | N/A | 1 |  |  | liveness_check.gd:24 | `OK · console valid · window holds waived · stage %d` |
| 477 | NON-PLAYER | N/A | 2 |  |  | liveness_check.gd:34 | `[day %d] %s` |
| 478 | TOAST | TR | 0 |  |  | lockdown.gd:27 | `Every monitor in the compound cuts to the same channel, on the same frame.` |
| 479 | TOAST | TR | 0 |  |  | lockdown.gd:30 | `Doors seal on schedule, not in anger.` |
| 480 | TOAST | TR | 0 |  | DIALOGUE | lockdown.gd:32 | `MERLE · 'Fifty years, and we have a premiere. Lock-in's just till broadcast, dear.'` |
| 481 | UI-PROMPT | TR-CAT | 0 |  |  | lockdown.gd:43 | `SEALED FOR BROADCAST · lock-in's just till air` |
| 482 | UI-PROMPT+WORLD | TR-CAT | 0 |  |  | log_station.gd:6 world_builder.gd:64 | `LIBRARY LANDING` |
| 483 | UI-PROMPT | TR-FMT | 2 |  |  | log_station.gd:12 | `%s · %s · no paper. walk to the next station.` |
| 484 | UI-PROMPT | TR-FMT | 2 | E |  | log_station.gd:14 | `%s · %s · sign the log (E) · unlimited paper` |
| 485 | UI-PROMPT | TR-FMT | 3 | E |  | log_station.gd:15 | `%s · %s · sign the log (E) · %d line(s) left` |
| 486 | TOAST | TR | 0 |  |  | log_station.gd:26 | `The next line is not blank.` |
| 487 | TOAST | TR | 0 |  |  | log_station.gd:28 | `Your handwriting. Tomorrow's date.` |
| 488 | TOAST | TR | 0 |  |  | log_station.gd:30 | `You check the loops of the R the way you check a stranger's teeth. They are yours.` |
| 489 | UI-MAP | NO-TR | 1 |  |  | map_view.gd:77 | `FACILITY MAP · %s to close · amber: landmarks · dot: you` |
| 490 | UI-PROMPT | TR | 0 |  |  | merle.gd:35 | `in the doorway` |
| 491 | UI-PROMPT | TR | 0 |  |  | merle.gd:35 | `in her chair` |
| 492 | UI-PROMPT | TR | 0 |  |  | merle.gd:35 | `at the kettle` |
| 493 | UI-PROMPT | TR-FMT | 1 | E |  | merle.gd:36 | `MERLE · %s (E)` |
| 494 | TOAST | TR | 0 |  |  | merle.gd:48 | `She says nothing. Her hands are empty and open, watching the pen.` |
| 495 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:54 | `MERLE · 'You'll be wonderful. You were always going to be.'` |
| 496 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:56 | `MERLE · 'The whole world gets to be carried now.'` |
| 497 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:58 | `MERLE · 'The degausser hums at night. I hear it too.' Her hands keep drying the plate.` |
| 498 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:60 | `MERLE · 'Oh, look at your gloves. You brought your own gloves.'` |
| 499 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:62 | `MERLE · 'He asks so many questions. You ask the right amount. I can tell.'` |
| 500 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:64 | `MERLE · 'You've given us back a piece of our childhood, do you know that?'` |
| 501 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:70 | `MERLE · 'I was seven. Route 9, the culvert end, past where the county stopped mowing.'` |
| 502 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:72 | `'I walked out after a dog that wasn't mine, and the light went, and the corn does not care how loud a girl is.'` |
| 503 | TOAST | TR | 0 |  |  | merle.gd:74 | `Her hands, for once, empty and open. 'And then the dark got warmer. Fur like a coat closet.'` |
| 504 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:76 | `'It carried me the whole way singing the closing song, and it set me down where the porch light reached.'` |
| 505 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:78 | `'The papers said a searcher found me. No searcher sings.'` |
| 506 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:80 | `'So bring me every date and every gap and every terrible arithmetic, and I will hold them. I promise you I will hold them.'` |
| 507 | TOAST | TR | 0 |  | DIALOGUE | merle.gd:82 | `'But I was carried. You don't vote against being carried.'` |
| 508 | WORLD | N/A | 0 |  |  | monitor_rig.gd:54 monitor_rig.gd:106 | `NO SIGNAL` |
| 509 | WORLD | N/A | 0 |  |  | monitor_rig.gd:106 | `KILLED · RE-PATCH AT PB` |
| 510 | TOAST | TR | 0 |  |  | night_trip.gd:25 | `A breaker lets go somewhere below. A feed drops off the board.` |
| 511 | TOAST | TR | 0 |  |  | night_trip.gd:27 | `Behind you, unhurried: a hummed bar of the closing song.` |
| 512 | TOAST | TR | 0 |  |  | night_trip.gd:29 | `The hall behind you is a hall. The patch bay can fix the rest.` |
| 513 | UI-MENU | TR | 0 |  |  | options_panel.gd:29 | `OPTIONS · THE BOOTH` |
| 514 | UI-MENU | TR | 0 |  |  | options_panel.gd:35 | `BEFORE THE SHOW · set your hands and eyes. O reopens this anytime.` |
| 515 | UI-MENU | TR | 0 |  |  | options_panel.gd:40 | `MASTER VOLUME` |
| 516 | UI-MENU | TR | 0 |  |  | options_panel.gd:46 | `MOUSE SENSITIVITY` |
| 517 | UI-MENU | TR | 0 | T |  | options_panel.gd:58 | `TBC · steadier tape (T)` |
| 518 | UI-MENU | TR | 0 |  |  | options_panel.gd:60 | `PHOTOSENSITIVITY-SAFE (P)` |
| 519 | UI-MENU | TR | 0 |  |  | options_panel.gd:62 | `UI TEXT SIZE` |
| 520 | UI-MENU | TR | 0 |  |  | options_panel.gd:64 | `CAPTIONS · significant sounds` |
| 521 | UI-MENU | TR | 0 | E |  | options_panel.gd:66 | `ASSIST · wider beats, slower clocks, hold E to be still` |
| 522 | UI-MENU | TR | 0 |  |  | options_panel.gd:69 | `REMAP · click, then press a key` |
| 523 | UI-MENU | TR | 0 |  |  | options_panel.gd:78 | `CLOSE (O)` |
| 524 | UI-MENU | TR | 0 |  |  | options_panel.gd:118 | `PRESS A KEY` |
| 525 | UI-PROMPT | TR | 0 | E |  | patchbay_console.gd:21 | `PANEL · RESTORE CIRCUIT B (E) · order matters` |
| 526 | UI-PROMPT | TR | 0 | E |  | patchbay_console.gd:23 | `PANEL · RESTORE CIRCUIT C (E)` |
| 527 | UI-PROMPT | TR | 0 | E |  | patchbay_console.gd:25 | `PATCHBAY · dead feed on the board · re-patch (E)` |
| 528 | UI-PROMPT | TR-CAT | 0 |  |  | patchbay_console.gd:26 patchbay_console.gd:68 | `CONTROL RUN` |
| 529 | UI-PROMPT+WORLD+IDENTIFIER | TR-CAT | 0 |  |  | patchbay_console.gd:26 patchbay_console.gd:68 | `STAGE HALL` |
| 530 | UI-PROMPT | TR-FMT | 1 | E |  | patchbay_console.gd:27 | `PATCHBAY · %s live · re-route (E)` |
| 531 | UI-CAPTURE | NO-TR | 0 | E,Q |  | patchbay_console.gd:43 | `E · restore circuit B yourself · Q · GET VESS, he knows the order` |
| 532 | TOAST | TR | 0 |  |  | patchbay_console.gd:55 | `CIRCUIT B RESTORED · half the dark stands down. B before C, the way the panel is labeled.` |
| 533 | TOAST | TR | 0 |  |  | patchbay_console.gd:60 | `CIRCUIT C RESTORED · the building remembers its own light.` |
| 534 | TOAST | TR | 0 |  |  | patchbay_console.gd:64 | `RE-PATCHED · the feed climbs back onto the board.` |
| 535 | TOAST | TR-FMT | 2 |  |  | patchbay_console.gd:70 | `PATCHED · %s live · %s dark. The budget is the budget.` |
| 536 | TOAST | TR | 0 |  |  | patchbay_console.gd:83 | `You call down the dark corridor. He comes because someone finally asked.` |
| 537 | TOAST | TR | 0 |  | DIALOGUE | patchbay_console.gd:85 | `'B before C,' he says, 'obviously,' and both circuits close under his hands in eleven seconds.` |
| 538 | TOAST | TR | 0 |  |  | patchbay_console.gd:89 | `Then he keeps walking. Past B. Past C. To circuit F, the one with the marshal's tie, bare-handed, to prove the theory.` |
| 539 | TOAST | TR | 0 |  |  | patchbay_console.gd:91 | `The transmitter that could not be de-energized includes him now. His outline refreshes at sixty fields a second.` |
| 540 | CAPTION | TR | 0 |  |  | patchbay_console.gd:92 | `[MAINS HUM, SHAPED LIKE A STANDING PERSON]` |
| 541 | UI-BINDER | NO-TR | 0 |  |  | patchbay_console.gd:93 | `V2 · THE UNCREDITED FIX` |
| 542 | UI-BINDER | NO-TR | 0 |  |  | patchbay_console.gd:93 | `interlaced at circuit F; nobody thanked her first` |
| 543 | UI-PROMPT | TR-CAT | 0 |  |  | readable_prop.gd:6 | `A DOCUMENT` |
| 544 | UI-PROMPT | TR-FMT | 1 | E |  | readable_prop.gd:21 | `%s · read (E again)` |
| 545 | UI-PROMPT | TR-FMT | 1 | E |  | readable_prop.gd:22 | `%s · read (E)` |
| 546 | TOAST | TR | 0 |  |  | rec_chairs.gd:55 | `Behind you, without a sound worth naming, the armchairs stand in rows now. Facing forward.` |
| 547 | UI-PROMPT | TR | 0 | E |  | rejected_edit.gd:17 | `THE SPLICING BLOCK STANDS READY · joined takes yield a daily without a capture · second take labeled: THE SONG, HARRIET LEFT OF FRAME (E)` |
| 548 | UI-PROMPT | TR | 0 | E |  | rejected_edit.gd:18 | `VESS'S CUT · he is asking without asking (E)` |
| 549 | TOAST | TR | 0 |  |  | rejected_edit.gd:34 | `You join the takes. The tape accepts the cut the way water accepts a stone.` |
| 550 | TOAST | TR | 0 |  |  | rejected_edit.gd:37 | `DAILY MINTED · no capture, no bench, no twelve seconds. Cheaper than you thought.` |
| 551 | TOAST | TR | 0 |  |  | rejected_edit.gd:39 | `The second take, in passing, again: THE SONG, HARRIET LEFT OF FRAME.` |
| 552 | TOAST | TR | 0 |  |  | rejected_edit.gd:47 | `He threads it without meeting anyone's eye. His cut. The one the club never mentions.` |
| 553 | TOAST | TR | 0 |  |  | rejected_edit.gd:51 | `Competent. Loving. Wrong in a way no one can name: transitions landing a half-beat off the show's breath.` |
| 554 | TOAST | TR | 0 |  |  | rejected_edit.gd:55 | `On the final frame the tape stops itself. A clean mechanical refusal. The take-up reel turns backward one rotation, deliberate as a headshake.` |
| 555 | TOAST | TR | 0 |  | DIALOGUE | rejected_edit.gd:57 | `VESS · 'It does that. Every copy. Every machine.' The pin is in his fist.` |
| 556 | TOAST | TR | 0 |  | DIALOGUE | rejected_edit.gd:59 | `VESS · 'Your cuts, it keeps. I checked the vault. It keeps yours.'` |
| 557 | TOAST | TR | 0 |  |  | rejected_edit.gd:61 | `MERLE · soft, hands folded, merciless as weather: 'Sit down, sweetheart. There's cobbler.'` |
| 558 | IDENTIFIER | N/A | 0 |  |  | rundown.gd:10 | `STORY CORNER` |
| 559 | WORLD+IDENTIFIER | N/A | 0 |  |  | rundown.gd:10 world_builder.gd:19 | `TAPE LIBRARY` |
| 560 | IDENTIFIER | N/A | 0 |  |  | rundown.gd:11 | `THE SONG` |
| 561 | WORLD+IDENTIFIER | N/A | 0 |  |  | rundown.gd:11 world_builder.gd:26 | `STUDIO A` |
| 562 | IDENTIFIER | N/A | 0 |  |  | rundown.gd:12 | `CRAFT TIME` |
| 563 | WORLD+IDENTIFIER | N/A | 0 |  |  | rundown.gd:12 world_builder.gd:27 | `PATCH BAY` |
| 564 | NON-PLAYER | N/A | 0 |  |  | rundown.gd:159 | `KILL most-watched rig (CHECKER read)` |
| 565 | TOAST | TR | 0 |  |  | rundown.gd:160 | `The feed you trust went dark first.` |
| 566 | TOAST | TR | 0 |  |  | rundown.gd:164 | `Somewhere, a camera dies. The map is shorter tonight.` |
| 567 | NON-PLAYER | N/A | 2 |  |  | rundown.gd:177 | `RELOCATE toward heard noise at %s -> segment %d` |
| 568 | TOAST | TR | 0 |  |  | rundown.gd:181 | `It changed direction. You were not quiet.` |
| 569 | NON-PLAYER | N/A | 1 |  |  | rundown.gd:191 | `RELOCATE sprinter-bias -> segment %d` |
| 570 | NON-PLAYER | N/A | 2 |  |  | rundown.gd:195 | `RELOCATE cycle -> segment %d (profile %s)` |
| 571 | WORLD | N/A | 0 |  |  | rundown.gd:197 | `· in transit ·` |
| 572 | TOAST | TR | 0 |  |  | rundown.gd:223 | `A hand the size of a door closes the distance. NEXT WEEK'S EPISODE.` |
| 573 | TOAST | TR | 0 |  |  | rundown.gd:255 | `It stops at the felt door. The room inside owes the air nothing, and it knows.` |
| 574 | CAPTION | TR | 0 |  |  | rundown.gd:267 | `[THE JAW WORKS ITS LEVER]` |
| 575 | TOAST | TR | 0 |  |  | rundown.gd:268 | `It stands at the edge of the bench light. Eleven feet of salvage, watching the tally. The jaw hand moves. Nothing else does.` |
| 576 | TOAST | TR | 0 |  |  | rundown.gd:275 | `The tally cools.` |
| 577 | TOAST | TR | 0 |  |  | rundown.gd:279 | `THE TALLY COOLS. Two doorways stand between you and anywhere. Use them.` |
| 578 | NON-PLAYER | N/A | 0 |  |  | rundown.gd:285 | `STRIKE af tally-cool` |
| 579 | NON-PLAYER | N/A | 4 |  |  | rundown.gd:316 | `STRIKE seg %d d=%.1f%s%s` |
| 580 | NON-PLAYER | N/A | 0 |  |  | rundown.gd:318 rundown.gd:326 | ` savor` |
| 581 | NON-PLAYER | N/A | 0 |  |  | rundown.gd:319 | ` THRU-WALL` |
| 582 | NON-PLAYER | N/A | 3 |  |  | rundown.gd:326 | `WARN seg %d d=%.1f%s` |
| 583 | TOAST | TR | 0 |  |  | rundown.gd:328 | `It is not hurrying anymore.` |
| 584 | TOAST | TR-FMT | 1 |  |  | rundown.gd:330 | `You can hear it. %s, performed to no one.` |
| 585 | CAPTION | TR | 0 |  |  | rundown.gd:343 | `[IT FOLDS THROUGH THE DOORWAY]` |
| 586 | TOAST | TR | 0 |  |  | rundown.gd:345 | `A doorway. It stops, and bends, and keeps its eye on you the whole way through.` |
| 587 | UI-PROMPT | TR | 0 |  |  | screening_event.gd:23 | `THE PROJECTOR · reel running` |
| 588 | UI-PROMPT | TR | 0 | E |  | screening_event.gd:24 | `THE PROJECTOR · run the mini-screening (E)` |
| 589 | TOAST | TR | 0 |  |  | screening_event.gd:38 | `The club settles into the rows. The reel threads itself true.` |
| 590 | TOAST | TR | 0 |  | TAPE | screening_event.gd:40 | `ON TAPE · CHUM: 'Goodnight, Gladhouse! Say it with me!'` |
| 591 | TOAST | TR | 0 |  |  | screening_event.gd:42 | `Half the room answers with the tape. In sync. Eyes forward.` |
| 592 | TOAST | TR | 0 | SPACE,Q |  | screening_event.gd:51 | `THE SIGN PULSES · SPACE on the beat · Q improvises · or hold still` |
| 593 | TOAST | TR | 0 |  |  | screening_event.gd:62 | `You said nothing, but you shifted. On tape, the head tilts toward the shift.` |
| 594 | TOAST | TR | 0 |  |  | screening_event.gd:65 | `Stillness, held whole. Harriet's cup does not move. The episode resumes.` |
| 595 | TOAST | TR | 0 |  |  | screening_event.gd:68 | `The reel runs out. Somebody is already asking to watch it again.` |
| 596 | TOAST | TR | 0 |  | DIALOGUE | screening_event.gd:104 | `ON THE BEAT · 'Goodnight, Gladhouse.' The room exhales; a hand finds your shoulder.` |
| 597 | TOAST | TR | 0 |  |  | screening_event.gd:106 | `OFF THE BEAT · the room turns, all of it, one motion.` |
| 598 | TOAST | TR | 0 |  | DIALOGUE | screening_event.gd:111 | `'Goodnight, everyone.' On the beat. On tape, a delighted laugh. (PT +10)` |
| 599 | TOAST | TR | 0 |  |  | screening_event.gd:114 | `The improvisation lands late. Somewhere, a pencil notes it. (PT +5)` |
| 600 | TOAST | TR | 0 |  |  | seance_dock.gd:7 | `FILED. NOT SHELVED.` |
| 601 | TOAST | TR | 0 |  |  | seance_dock.gd:8 | `IT ASKED ME TO STAND IN. NEVER ACCEPT A ROLE.` |
| 602 | TOAST | TR | 0 |  |  | seance_dock.gd:9 | `FINISH THE FINALE. FORMAT KEEPS ITS OWN RULES.` |
| 603 | TOAST | TR | 0 |  |  | seance_dock.gd:10 | `ONLY IF THE HOUSE CLOSES WITH SOMEONE INSIDE. LET IT BE ME.` |
| 604 | TOAST | TR | 0 |  |  | seance_dock.gd:11 | `I'VE READ THE ENDING. IT'S GOOD.` |
| 605 | UI-PROMPT | TR | 0 | Q |  | seance_dock.gd:32 | ` · Q feed the fire tape into the wake` |
| 606 | UI-PROMPT | TR | 0 | SPACE |  | seance_dock.gd:34 | ` · SPACE the pad has room for a sixth line` |
| 607 | UI-PROMPT | TR | 0 | E |  | seance_dock.gd:35 | `SEANCE REEL · close (E) · Z back · X forward` |
| 608 | UI-PROMPT | TR | 0 | E |  | seance_dock.gd:36 | `SEANCE REEL · the impossible tape · open (E)` |
| 609 | TOAST | TR | 0 |  |  | seance_dock.gd:41 | `The dock is a box with a window now. Nothing reads.` |
| 610 | TOAST | TR-CAT | 0 |  |  | seance_dock.gd:79 | `SHE WAS THE ONLY ONE WHO PAUSED PROPERLY.` |
| 611 | TOAST | TR-CAT | 0 |  |  | seance_dock.gd:81 | `I KNOW. SHE'S HERE NOW.` |
| 612 | TOAST | TR-CAT | 0 |  |  | seance_dock.gd:82 | `LEGAL PAD · ` |
| 613 | TOAST | TR | 0 |  |  | seance_dock.gd:84 | `The frame tears a little more each pass.` |
| 614 | UI-CAPTURE | NO-TR | 2 |  |  | seance_dock.gd:91 | `SEANCE · FRAME %d · WEAR %.1f%%` |
| 615 | TOAST | TR | 0 |  |  | seance_dock.gd:95 | `The pad takes a sixth line. The wear takes the rest.` |
| 616 | TOAST | TR | 0 |  |  | seance_dock.gd:97 | `His print burns from the inside of the frames, whitening as you watch.` |
| 617 | TOAST | TR | 0 |  |  | seance_dock.gd:99 | `Green ink drains upward out of every note in the building, back into nowhere.` |
| 618 | CAPTION | TR | 0 |  |  | seance_dock.gd:100 | `[THE INK LEAVES THE PAPER]` |
| 619 | TOAST | TR | 0 |  |  | seance_dock.gd:102 | `He is retroactively unfound. The reel is blank leader, end to end.` |
| 620 | UI-BINDER | NO-TR | 0 |  |  | seance_dock.gd:103 | `L1 · THE SIXTH QUESTION` |
| 621 | UI-BINDER | NO-TR | 0 |  |  | seance_dock.gd:103 | `asked past the wear; unfound, retroactively` |
| 622 | TOAST | TR | 0 |  |  | seance_dock.gd:112 | `You feed 1977 into the wake.` |
| 623 | TOAST | TR | 0 |  |  | seance_dock.gd:114 | `The unfinished sign-off completes itself, in a reading voice you know from green ink:` |
| 624 | TOAST | TR | 0 |  | DIALOGUE | seance_dock.gd:116 | `'There's no one at home anymore. The lights are off in the little house. Say goodnight, Chum.'` |
| 625 | TOAST | TR | 0 |  |  | seance_dock.gd:118 | `The five answers un-write, last to first. The final frame: the little door, closing from the inside. A hand on the inner knob.` |
| 626 | CAPTION | TR | 0 |  |  | seance_dock.gd:119 | `[THE SIGN-OFF, WHOLE]` |
| 627 | TOAST | TR | 0 |  |  | seance_dock.gd:121 | `He got to finish it.` |
| 628 | UI-BINDER | NO-TR | 0 |  |  | seance_dock.gd:125 | `L2 · THE READING` |
| 629 | UI-BINDER | NO-TR | 0 |  |  | seance_dock.gd:125 | `finished it; the door closed from the inside` |
| 630 | CAPTION | TR | 0 |  |  | sfx.gd:17 | `[THE BELL RINGS · once]` |
| 631 | CAPTION | TR | 0 |  |  | sfx.gd:22 | `[pen tick]` |
| 632 | NON-PLAYER | N/A | 2 |  |  | soak_runner.gd:34 | `SOAK START · bot=%s · minutes=%.1f` |
| 633 | UI-PROMPT | TR | 0 |  |  | spectro_dock.gd:10 | `SPECTROGRAM · the verse is banked` |
| 634 | UI-PROMPT | TR | 0 |  |  | spectro_dock.gd:12 | `SPECTROGRAM · needs a captured tape first` |
| 635 | UI-PROMPT | TR | 0 | E |  | spectro_dock.gd:13 | `SPECTROGRAM · pull the sidebands (E)` |
| 636 | TOAST | TR | 0 |  |  | spectro_dock.gd:24 | `Structure in the sidebands. Not noise. Words.` |
| 637 | TOAST | TR | 0 |  | DIALOGUE | spectro_dock.gd:26 | `RECOVERED · 'Close the door and dim the light. Fold the day away.'` |
| 638 | UI-PROMPT | TR-CAT | 0 |  |  | spectro_dock.gd:29 | `the missing verse` |
| 639 | UI-MENU | NO-TR | 0 |  |  | title.gd:13 | `NEW EPISODE` |
| 640 | UI-MENU | NO-TR | 0 |  |  | title.gd:17 | `CONTINUE · no log on file` |
| 641 | UI-MENU | NO-TR | 0 |  |  | title.gd:28 | `TAPE 1 · FREE DEMO · the tower light stays on` |
| 642 | UI-MENU | NO-TR | 0 |  |  | title.gd:32 | `FILED WHILE YOU WERE OUT:\n` |
| 643 | UI-PROMPT | TR | 0 | E |  | vess_binder.gd:11 | `VESS'S RESEARCH BINDER · read (E) · his door was ajar` |
| 644 | TOAST | TR | 0 |  |  | vess_binder.gd:18 | `His insight, real: the slate-number skips are clustered, not random. Nobody else saw it.` |
| 645 | TOAST | TR | 0 |  |  | vess_binder.gd:20 | `Also, in confident block letters, a theory that is wrong. You close the binder the way you found it.` |
| 646 | WORLD | N/A | 0 |  |  | world_builder.gd:12 world_builder.gd:37 | `REC ROOM` |
| 647 | WORLD | N/A | 0 |  |  | world_builder.gd:20 world_builder.gd:44 | `BENCH ROOM` |
| 648 | WORLD | N/A | 0 |  |  | world_builder.gd:22 world_builder.gd:46 | `TRANSMITTER HALL` |
| 649 | WORLD+IDENTIFIER | N/A | 0 |  |  | world_builder.gd:23 world_builder.gd:47 | `DEAD ROOM` |
| 650 | WORLD+IDENTIFIER | N/A | 0 |  |  | world_builder.gd:24 world_builder.gd:48 | `FIRE CORRIDOR` |
| 651 | WORLD+IDENTIFIER | N/A | 0 |  |  | world_builder.gd:29 world_builder.gd:53 | `MASTER CONTROL` |
| 652 | WORLD+IDENTIFIER | N/A | 0 |  |  | world_builder.gd:30 world_builder.gd:55 | `GREEN ROOM` |
| 653 | WORLD+IDENTIFIER | N/A | 0 |  |  | world_builder.gd:31 world_builder.gd:56 | `SCENE DOCK` |
| 654 | WORLD | N/A | 0 |  |  | world_builder.gd:41 | `locked:PADLOCKED · the tag reads EDITH · a key exists\|EDITH` |
| 655 | WORLD | N/A | 0 |  |  | world_builder.gd:47 | `locked:LOCKED · felt-faced · the hum stops at the seam\|QUIET ROOM` |
| 656 | WORLD | N/A | 0 |  |  | world_builder.gd:48 | `locked:SEALED · reopens for the anniversary (Tape 4)` |
| 657 | WORLD | N/A | 0 |  |  | world_builder.gd:67 | `TRANSMITTER THRESHOLD` |
| 658 | WORLD | N/A | 0 |  |  | world_builder.gd:72 | `CAM 1 · CORRIDOR` |
| 659 | WORLD | N/A | 0 |  |  | world_builder.gd:73 | `CAM 2 · STACKS` |
| 660 | UI-PROMPT | TR-CAT | 0 |  |  | world_builder.gd:264 | `SEALED · you can hear it from here. That is enough for today.` |
| 661 | UI-PROMPT | TR-CAT | 0 |  |  | world_builder.gd:266 | `SEALED · the club opens the rest when the contract is signed.` |
| 662 | WORLD | N/A | 0 |  |  | world_builder.gd:298 | ` LOG` |
| 663 | WORLD | N/A | 0 |  |  | world_builder.gd:360 | `THE BENCH` |
| 664 | WORLD | N/A | 0 |  |  | world_builder.gd:395 | `1977 DOCK` |
| 665 | WORLD | N/A | 0 |  |  | world_builder.gd:400 | `SEANCE REEL` |
| 666 | WORLD | N/A | 0 |  |  | world_builder.gd:405 | `REEL · 1977` |
| 667 | WORLD | N/A | 0 |  |  | world_builder.gd:441 | `WOOL SPIKE 001` |
| 668 | WORLD | N/A | 0 |  |  | world_builder.gd:463 | `THE LITTLE DOOR` |
| 669 | UI-PROMPT | TR-CAT | 0 |  |  | world_builder.gd:464 | `Not yet. It closes on camera, in Tape 5.` |
| 670 | WORLD | N/A | 0 |  |  | world_builder.gd:479 | `CHUM'S MARK` |
| 671 | WORLD | N/A | 1 |  |  | world_builder.gd:496 | `CAM %d` |
| 672 | WORLD | N/A | 0 |  |  | world_builder.gd:562 | `CASTING SHEET` |
| 673 | WORLD | N/A | 0 |  |  | world_builder.gd:633 | `RITA'S BED` |
| 674 | WORLD | N/A | 0 |  |  | world_builder.gd:723 | `THE GLADHOUSE · CLUB PRINT` |
| 675 | WORLD | N/A | 0 |  |  | world_builder.gd:778 | `the EDITH key, felt-tagged in a child's hand` |
| 676 | WORLD | N/A | 0 |  |  | world_builder.gd:778 world_builder.gd:780 | `KEY BOARD` |
| 677 | WORLD | N/A | 0 |  |  | world_builder.gd:780 | `the TRAINING key, tagged in green ink` |
| 678 | WORLD | N/A | 0 |  |  | world_builder.gd:782 | `the quiet room key · felt-wrapped` |
| 679 | WORLD | N/A | 0 |  |  | world_builder.gd:782 | `FOR THE QUIET ROOM` |
| 680 | WORLD | N/A | 0 |  |  | world_builder.gd:891 | `FILM CABINET` |
| 681 | WORLD | N/A | 1 |  |  | world_builder.gd:998 | `UNIT %d` |
| 682 | WORLD | N/A | 0 |  |  | world_builder.gd:1021 | `ACCESSION LEDGER` |
| 683 | WORLD | N/A | 0 |  |  | world_builder.gd:1026 | `the station ID cart` |
| 684 | WORLD | N/A | 0 |  | DIALOGUE | world_builder.gd:1027 | `CART AUDIO · 'You're watching The Gladhouse, on WGLD, Channel fifty-eight.'` |
| 685 | WORLD | N/A | 0 |  |  | world_builder.gd:1029 | `CART RACK` |
| 686 | WORLD | N/A | 0 |  |  | world_builder.gd:1035 | `the finale script` |
| 687 | WORLD | N/A | 0 |  |  | world_builder.gd:1036 | `Typed, hand-amended. The margin, pressed hard: 'No. Tell them the truth or it doesn't take.'` |
| 688 | WORLD | N/A | 0 |  |  | world_builder.gd:1038 | `CRAIK'S BOX` |
| 689 | WORLD | N/A | 0 |  |  | world_builder.gd:1043 | `the sign-off card` |
| 690 | WORLD | N/A | 0 |  |  | world_builder.gd:1045 | `Hand-lettered. WGLD CHANNEL 58. GOODNIGHT.` |
| 691 | WORLD | N/A | 0 |  |  | world_builder.gd:1047 | `PROPS CRATE` |
| 692 | WORLD | N/A | 0 |  |  | world_builder.gd:1054 | `VESS'S ROOM` |
| 693 | WORLD | N/A | 0 |  |  | world_builder.gd:1058 | `LEDGER MARGIN` |
| 694 | WORLD | N/A | 0 |  |  | world_builder.gd:1129 | `VESS'S CUT` |
| 695 | UI-PROMPT | TR-CAT | 0 |  |  | world_builder.gd:1153 | `THE CLIPPING · 1974, behind glass` |
| 696 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1154 | `COURIER, OCTOBER 1974 · LOCAL GIRL, 7, FOUND SAFE AFTER NIGHT IN CORNFIELD.` |
| 697 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1155 | `'We don't know which volunteer walked her back and we'd like to shake his hand,' said Sheriff D. Pruett.` |
| 698 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1156 | `The child, wrapped in a square of gray flannel her mother did not recognize, said only that she was 'carried the long way, singing.'` |
| 699 | UI-PROMPT | TR-CAT | 0 |  |  | world_builder.gd:1158 | `WELCOME PACKET · mimeograph purple` |
| 700 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1159 | `WELCOME TO THE FIFTY-EIGHT! Quiet hours are posted by the clocks and we do mean them. [ballpoint: we really do]` |
| 701 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1160 | `If a door is closed, it is closed for a reason and the reason is written on it. Make yourself at home. You already are.` |
| 702 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1161 | `[ballpoint, smaller] welcome home` |
| 703 | UI-PROMPT | TR-CAT | 0 |  |  | world_builder.gd:1163 | `FIRE MARSHAL REPORT · 1977, photocopy` |
| 704 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1164 | `Cause: undetermined, consistent with deliberate ignition at the tape vault. Total loss of stored media.` |
| 705 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1165 | `Note of record: transmitting equipment found energized at time of entry and could not be de-energized by responding personnel.` |
| 706 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1166 | `Referred to station engineer. No further action.` |
| 707 | UI-PROMPT | TR-CAT | 0 |  |  | world_builder.gd:1168 | `A FAN LETTER · ruled paper, careful loops` |
| 708 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1169 | `Dear Chum, my brother says you are just a puppet but I know a secret which is that everybody is a puppet of somebody` |
| 709 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1170 | `and it only matters if the hands are kind. Your hands seem kind.` |
| 710 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1171 | `Please wave at camera one on my birthday which is the 9th. Your friend, Iris Bell, age 8 and one quarter.` |
| 711 | UI-PROMPT | TR-CAT | 0 |  |  | world_builder.gd:1174 | `PEAK ASSET DOSSIER · CHUM-AF-1974-P` |
| 712 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1175 | `PEAK PRODUCTION ASSET DOSSIER. FILE CHUM-AF-1974-P (REV.). STATUS: ACTIVE / HAZARDOUS.` |
| 713 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1176 | `Rebuilt from the 1974 mascot body and salvaged studio materials. Entirely manually operated. Requires minimum three puppeteers for full performance.` |
| 714 | LORE | TR | 0 |  | DOCUMENT | world_builder.gd:1177 | `Handwritten beneath: he works his own jaw. Count the hands. Report all sightings to Peak Security. HE REMEMBERS THE AUDIENCE.` |

## APPENDIX B · THE SCRIPT

Read-only. Run from the repo root; `--table` prints Appendix A as TSV.
Output at d7a6877 is in the PR body under `## Verification`.

```python
#!/usr/bin/env python3
"""C12 GAMETEXT AUDIT (cloud unit). Read-only.
Classifies every key in translations/strings.csv by the display path it
flows through in scripts/*.gd, records whether that path reaches tr()
with the key intact, lists glyph-token keys, and runs the LAW 5 checks.
Run from the repo root:  python3 gametext_audit.py [--table]
"""
import csv, glob, os, re, sys, collections

ROOT = os.getcwd()
CSV = os.path.join(ROOT, 'translations', 'strings.csv')
GT = os.path.join(ROOT, 'ue', 'Restoration', 'Data', 'GameText.csv')
GLYPH_TOKENS = ['E', 'SPACE', 'Q', 'T', 'M']          # game_state.gd GLYPH_MAP
UNMAPPED_KEYS = ['WASD', 'TAB', 'ESC', 'Z', 'X', 'O', 'P', '1 / 2 / 3']  # named in text, not in GLYPH_MAP
DNT = ['WGLD', 'Chum', 'CHUM', 'Gladhouse', 'GLADHOUSE', 'RESTORATION']  # loc plan §5 do-not-translate

keys = [r[0] for r in csv.reader(open(CSV, newline='', encoding='utf-8')) if r and r[0] != 'keys']
gt = [r[0] for r in csv.reader(open(GT, newline='', encoding='utf-8')) if r and r[0] != 'Key']

src = {}
for fpath in sorted(glob.glob(os.path.join(ROOT, 'scripts', '*.gd'))):
    src[os.path.basename(fpath)] = open(fpath, encoding='utf-8').read().split('\n')

NON_PLAYER_FILES = {'soak_runner.gd', 'bot_driver.gd', 'invariant_parser.gd', 'coverage_director.gd'}
WORLD_FILES = {'prop_kit.gd', 'character_kit.gd'}

def enclosing_func(lines, i):
    for j in range(i, -1, -1):
        m = re.match(r'\s*(?:static\s+)?func\s+(\w+)', lines[j])
        if m:
            return m.group(1)
    return '<top>'

def call_context(lines, i):
    """For a bare string line inside a multi-line call or const table, fold
    in the opening line so the classifier sees the call / const name."""
    line = lines[i].strip()
    if not (line.startswith(('"', "'", '[')) or re.match(r'^\s*\d+:\s*"', line)):
        return line
    for j in range(i - 1, max(-1, i - 12), -1):
        t = lines[j].strip()
        if re.match(r'^(const|var)\s+\w+\s*:?=\s*[\[{]\s*$', t) or re.search(r'[\(\[]\s*$', t) or re.search(r'\.(toast|_say|log_line|append)\(\s*$', t):
            return t + ' ⏎ ' + line
        if re.match(r'^(func|\S)', lines[j]) and not lines[j].startswith(('\t"', "\t[", '\t\t')):
            break
    return line

def occurrences(key):
    needle = '"%s"' % key
    out = []
    for fname, lines in src.items():
        for i, line in enumerate(lines):
            if needle in line:
                out.append((fname, i + 1, enclosing_func(lines, i), call_context(lines, i)))
    return out

# Each rule returns (class, tr_status). tr_status:
#   TR       key reaches tr() intact (toast/say/prompt/caption/booth/pause)
#   TR-FMT   key is a %-template formatted BEFORE tr() -> never matches the CSV
#   TR-CAT   key is concatenated/placeholder-fed into another string before tr()
#   NO-TR    displayed on a path that never calls tr()
#   N/A      not displayed as-is (identifier, world text, log line)
def classify_occ(fname, func, line, key):
    is_fmt = bool(re.search(r'"\s*%\s*[\[\(\w"]', line.split('"%s"' % key)[1] if ('"%s"' % key) in line else ''))
    has_pct = '%' in key
    if 'show_caption(' in line:
        return 'CAPTION', 'TR'
    if fname == 'world_builder.gd' and func == '_spawn_readables' and re.search(r'\["[^"]*",\s*[\d.]+\],?$', line):
        return 'LORE', 'TR'
    if fname == 'achievements.gd' and func == '<top>' and (':' in line):
        return 'ACHIEVEMENT', 'TR-CAT'
    if re.search(r'\b(log_line|print|push_warning|push_error|printerr|store_line)\(', line) or fname in NON_PLAYER_FILES:
        return 'NON-PLAYER', 'N/A'
    if re.search(r'\b(_plog|_log)\(', line):
        return 'NON-PLAYER', 'N/A'
    if re.search(r'const SEGMENTS', line):
        return 'IDENTIFIER', 'N/A'
    if re.search(r'const (ROW_LINES|FIX_LINES|INCIDENTS|COMMIT_LINES|LINES|ANSWERS)', line):
        return 'TOAST', ('TR-CAT' if fname == 'harriet.gd' else 'TR')
    if re.search(r'(_on_mark_press|_timed)\(', line) or 'suffix' in line or 'set_capture_status' in line:
        return 'UI-CAPTURE', 'NO-TR'
    if re.search(r'\.label\s*=|var label :=|_spawn_fixture\(|locked_reason\s*=|gain_asset\(|var live :=', line):
        return 'UI-PROMPT', 'TR-CAT'
    if re.search(r'var prefix :=', line):
        return 'UI-CLOCK', 'NO-TR'
    if re.search(r'\b(mark_ending|is_dead|has_key|_resolve|signals_known\.has|add_show_signal)\(', line) or ' in l:' in line \
            or 'ENDING_MAP' in line or re.search(r'^"%s":' % re.escape(key), line) or re.search(r'const (SIX|SEVENTH|NAMES) :=', line) \
            or re.search(r'var names := \[', line) or re.search(r'mark_casualty\("%s"' % re.escape(key), line):
        return 'IDENTIFIER', 'N/A'
    if 'mark_casualty(' in line:
        return 'UI-BINDER', 'NO-TR'
    if 'toast(' in line or 'notify.emit(' in line or 'log_capture(' in line:
        if 'toast(' in line and (('"' + key + '"') in line) and re.search(r'toast\(\s*(tr\()?"%s"\s*\)' % re.escape(key), line):
            return 'TOAST', ('TR-FMT' if has_pct else 'TR')
        if 'notify.emit(' in line:
            return 'TOAST', 'NO-TR'
        return 'TOAST', ('TR-FMT' if (has_pct and is_fmt) else 'TR-CAT')
    if func == 'get_prompt' or 'get_prompt' in line or (fname == 'readable_prop.gd'):
        return 'UI-PROMPT', ('TR-FMT' if has_pct else 'TR')
    if fname == 'world_builder.gd' and func == '_spawn_readables':
        return 'UI-PROMPT', 'TR-CAT'
    if '_say(' in line or func == '_say':
        return 'UI-SAY', ('TR-FMT' if (has_pct and is_fmt) else 'TR')
    if re.search(r'\br[12]\.text\s*=', line):
        return 'UI-SAY', 'NO-TR'
    if func == 'objective_text':
        return 'UI-OBJECTIVE', 'NO-TR'
    if func == 'phase_text' or fname == 'broadcast.gd':
        return 'UI-CLOCK', 'NO-TR'
    if 'capture_status' in line or 'set_capture_status' in line:
        return 'UI-CAPTURE', 'NO-TR'
    if func in ('_fill_form', '_fill_binder') or 'lines.append(' in line:
        return 'UI-BINDER', 'NO-TR'
    if func == '_toggle_pause' or fname == 'options_panel.gd':
        return 'UI-MENU', ('TR' if 'tr(' in line else 'NO-TR')
    if fname == 'title.gd':
        return 'UI-MENU', 'NO-TR'
    if fname in ('credits.gd', 'credit_entry.gd') or '_roll_credits(' in line:
        return 'UI-CREDITS', 'NO-TR'
    if fname == 'map_view.gd':
        return 'UI-MAP', 'NO-TR'
    if 'Label3D' in line or re.search(r'\b\w+\.text\s*=', line) \
            or 'label_text' in line or 'slate_text' in line or fname in WORLD_FILES or fname == 'world_builder.gd':
        return 'WORLD', 'N/A'
    if re.match(r'@export var', line):
        return 'UI-PROMPT', 'TR-CAT'
    if fname == 'hud.gd' and re.search(r'\.text\s*=', line):
        return 'UI-HUD', 'NO-TR'
    if func == '<top>' and fname in ('decision_ledger.gd', 'live_production.gd', 'harriet.gd', 'vess.gd', 'merle.gd'):
        # const tables consumed by GameState.toast(TABLE[i]) — table entry reaches tr intact
        # except harriet.gd LINES, which is fed through "HARRIET · %s" first
        return 'TOAST', ('TR-CAT' if fname == 'harriet.gd' else 'TR')
    if fname in ('live_production.gd',) and func == '<top>':
        return 'TOAST', 'TR'
    return 'UNRESOLVED', '?'

PRIORITY = ['CAPTION', 'ACHIEVEMENT', 'LORE', 'TOAST', 'UI-PROMPT', 'UI-SAY', 'UI-MENU', 'UI-OBJECTIVE', 'UI-BINDER',
            'UI-CAPTURE', 'UI-CLOCK', 'UI-CREDITS', 'UI-MAP', 'UI-HUD', 'WORLD', 'IDENTIFIER', 'NON-PLAYER', 'UNRESOLVED']
TR_PRIORITY = ['TR', 'TR-FMT', 'TR-CAT', 'NO-TR', 'N/A', '?']

# Hand rulings for the four sites the rules cannot see (each cited):
#  patchbay_console.gd:26,68  var live := "CONTROL RUN" ... -> "PATCHBAY · %s live · re-route (E)" (prompt, placeholder-fed)
#  seance_dock.gd:79,81       a = "..." -> GameState.toast("LEGAL PAD · " + a)            (toast, concatenated)
OVERRIDES = {
    'CONTROL RUN': ('UI-PROMPT', 'TR-CAT'), 'STAGE HALL': ('UI-PROMPT', 'TR-CAT'),
    'SHE WAS THE ONLY ONE WHO PAUSED PROPERLY.': ('TOAST', 'TR-CAT'), "I KNOW. SHE'S HERE NOW.": ('TOAST', 'TR-CAT'),
}

def register(k, cls):
    if cls == 'LORE':
        return 'DOCUMENT'
    if k.startswith('ON TAPE'):
        return 'TAPE'
    if re.match(r"^(?:[A-Z][A-Z .',]+ · |\[[a-z ]+\] )?'", k) or re.match(r"^[A-Z][A-Z .']+ · '", k) or re.match(r"^[A-Z][A-Z .']+(, [a-z ,]+)?: '", k):
        return 'DIALOGUE'
    return ''

report = {}
for k in keys:
    occs = occurrences(k)
    cl = [classify_occ(f, fn, ln, k) for (f, l, fn, ln) in occs]
    cl = [(c if c != 'UNRESOLVED' else OVERRIDES[k][0], t if c != 'UNRESOLVED' else OVERRIDES[k][1]) for c, t in cl]
    # tr() is only ever called on the already-formatted string at the chokepoints
    # (game_state.gd:212,402; hud.gd:332-333,529), so a %-template never reaches
    # the table as its key: any TR/TR-CAT verdict on a template is really TR-FMT.
    cl = [('%s' % c, ('TR-FMT' if ('%' in k and t in ('TR', 'TR-CAT')) else t)) for c, t in cl]
    classes = sorted({c for c, _ in cl}, key=PRIORITY.index)
    trs = sorted({t for _, t in cl}, key=TR_PRIORITY.index)
    report[k] = (occs, classes, trs)

def metrics(k):
    return dict(
        pct=len(re.findall(r'%(?:\d*\.?\d*[dfs])', k)),
        newline='\\n' in k,
        allcaps=(lambda L: bool(L) and L.isupper() and len(L) >= 4)(re.sub(r'[^A-Za-z]', '', k)),
        length=len(k),
        glyph=[t for t in GLYPH_TOKENS if re.search(r'\b%s\b' % t, k)],
        unmapped=[t for t in UNMAPPED_KEYS if re.search(r'(?<![\w/])%s(?![\w/])' % re.escape(t), k)],
        dnt=[t for t in DNT if t in k],
    )

# ---------------- report ----------------
print('KEYS strings.csv=%d GameText.csv=%d identical_order=%s' % (len(keys), len(gt), keys == gt))
print('DUPLICATE KEYS %d' % sum(1 for c in collections.Counter(keys).values() if c > 1))
print('KEYS WITH NO SOURCE OCCURRENCE %d' % sum(1 for k in keys if not report[k][0]))
tot = collections.Counter(report[k][1][0] if report[k][1] else 'MISSING' for k in keys)
print('PRIMARY CLASS TOTALS (%d keys):' % len(keys))
for c in PRIORITY:
    if tot[c]:
        print('   %-12s %d' % (c, tot[c]))
grp = collections.Counter()
for k in keys:
    c = report[k][1][0]
    grp['UI' if c.startswith('UI-') else c] += 1
print('FIVE-CLASS ROLLUP + residue:', dict(grp))
trt = collections.Counter(report[k][2][0] for k in keys)
print('TR STATUS (best path per key):', dict(trt))
print('UNRESOLVED KEYS:', [k for k in keys if 'UNRESOLVED' in report[k][1]])
print('MULTI-CLASS KEYS %d' % sum(1 for k in keys if len(report[k][1]) > 1))
print('PERCENT-TEMPLATE KEYS %d' % sum(1 for k in keys if metrics(k)['pct']))
print('EMBEDDED-NEWLINE KEYS %d' % sum(1 for k in keys if metrics(k)['newline']))
print('ALL-CAPS KEYS %d' % sum(1 for k in keys if metrics(k)['allcaps']))
print('KEYS OVER 120 CHARS %d (longest %d)' % (sum(1 for k in keys if metrics(k)['length'] > 120), max(len(k) for k in keys)))
print('NO-TR DISPLAY KEYS %d' % sum(1 for k in keys if report[k][2][0] == 'NO-TR'))
print('TR-FMT KEYS %d' % sum(1 for k in keys if report[k][2][0] == 'TR-FMT'))
gl = collections.defaultdict(list)
for k in keys:
    for t in metrics(k)['glyph']:
        gl[t].append(k)
print('GLYPH-TOKEN KEYS', {t: len(gl[t]) for t in GLYPH_TOKENS})
um = collections.defaultdict(list)
for k in keys:
    for t in metrics(k)['unmapped']:
        um[t].append(k)
print('KEYS NAMING UNMAPPED KEYS', {t: len(v) for t, v in um.items()})
dn = collections.defaultdict(list)
for k in keys:
    for t in metrics(k)['dnt']:
        dn[t].append(k)
print('DO-NOT-TRANSLATE TERM KEYS', {t: len(v) for t, v in dn.items()})
print('LAW 5 — achievement titles naming Chum:', [k for k in keys if 'ACHIEVEMENT' in report[k][1] and re.search('chum', k, re.I)])
print('LAW 5 — keys naming Chum: %d' % sum(1 for k in keys if re.search('chum', k, re.I)))
for k in keys:
    if re.search('chum', k, re.I):
        o = report[k][0][0]
        print('   %-11s %s:%d %s | %s' % (report[k][1][0], o[0], o[1], o[2], k[:100]))
print('LAW 5 — bell caption keys:', [k for k in keys if 'BELL' in k.upper() and 'CAPTION' in report[k][1]])
print('BANNED WORD creepy:', [k for k in keys if 'creepy' in k.lower()])
print('LAW 3 — keys containing glimpse/once-ever:', [k for k in keys if re.search(r'glimpse|once.ever|once, ever', k, re.I)])

if '--table' in sys.argv:
    print('\n#\tclass\ttr\tpct\tglyph\tregister\tsource\tkey')
    for i, k in enumerate(keys, 1):
        occs, classes, trs = report[k]
        m = metrics(k)
        where = ' '.join('%s:%d' % (o[0], o[1]) for o in occs[:2])
        print('\t'.join([str(i), '+'.join(classes), trs[0], str(m['pct']), ','.join(m['glyph']), register(k, classes[0]), where, k]))
```
