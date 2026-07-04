# RESTORATION · LOCALIZATION PLAN v1
Measured, not guessed: a source scan of the v0.9 build finds 822 literals, ~3959 words of player-facing text in the scripts alone (heuristic count, excludes paths and identifiers; final extraction will land within about 15 percent of this). For scale, that is a short-story-sized translation per locale before the props packet's found documents, which add roughly 2,500 words of the hardest register in the game.

## 1 · SCOPE AND TIERS
Launch: English. Wave 1 (with the full release or fast-follow): French, Italian, German, Spanish (LatAm-leaning neutral), Brazilian Portuguese. Wave 2 (post-launch, sales-gated): Japanese, Simplified Chinese, Korean, Polish, Russian. Text localization only, forever: THE GLADHOUSE AIRED IN ENGLISH IN OHIO IN 1971, so all VO and all in-tape speech stays English as a matter of authenticity, with per-locale subtitles carrying meaning. This is also the budget's best friend, and for once the fiction and the finance agree.

## 2 · THE DIEGETIC-ENGLISH DOCTRINE (two string classes)
WORLD TEXT: anything that exists as an object in the fiction stays English: slates, the SCOPE READS MASTER line, WGLD cards, ledger stamps, door signage, the legal pad, the run sheet. These are props. Their meaning reaches the player through the localized inspection toast, exactly as a traveler reads a foreign sign through a companion. SYSTEM TEXT: toasts, prompts, objectives, menus, captions, achievements: fully localized. The test for any string: could a camera photograph it inside the world? Then it is world text and it keeps its English, and the localized layer sits beside it, never over it.

## 3 · TECHNICAL READINESS FINDINGS (honest, from source)
L01 · Every string is hardcoded across roughly 70 scripts. Remediation strategy: CHOKEPOINT TRANSLATION. The overwhelming majority of player-facing text flows through a handful of functions (GameState.toast, the HUD say pair, Interactable.get_prompt, caption). Wrapping tr() at those chokepoints plus a key-extraction pass converts the problem from 70 files to 4 call sites and one CSV. Named as the Extraction Commit; format strings and inline concatenations are the residue that needs hand work.
L02 · Label3D and the UI have no CJK-capable font fallback; wave 2 requires a per-locale font stack that keeps the phosphor register (a mono-adjacent CJK face, licensed, tested on the map and the binder).
L03 · Fixed widths everywhere (options rows at 240 px, HUD offsets, the map legend). Expansion budget: plus 35 percent for German and Russian; an autowrap-and-clip audit rides the pseudo-loc build.
L04 · Toast durations are hardcoded seconds tuned to English reading speed. Remediation: duration = base plus characters over a per-locale characters-per-second table, so Merle's monologue does not sprint in German.
L05 · Prompts name physical letters (E, SPACE, Q, Z, X). Keyboards disagree, and access item R6 (remapping) makes letters doubly wrong. Remediation shared with R6: prompts reference actions and render the bound glyph.
L06 · The all-caps registers (the legal pad, signage-styled toasts) collide with capitalization grammar in German and others; the per-locale style guide rules on caps-as-voice versus caps-as-styling case by case.

## 4 · THE CREATIVE BIBLE (the landmines, each with its contract)
THE VERSE: delivered to translators as a lyric brief, not a string: four lines, lullaby meter, rhyme optional, and the final line MUST carry the exact meaning "and no one has to stay," because the plot detonates on it.
THE G2 ANOMALY: the audio swap (home becomes here) never re-records. Each locale selects its own domestic-warmth word pair for the SUBTITLE swap, close enough to slip past a tired reader, wrong enough to reward a careful one, and documents the pair in the loc log because the ARG's recovered reel must match.
THERE'S COBBLER: translate the dessert, not the word. Each locale substitutes its own grandmother-canonical baked comfort (crumble, Streuselkuchen, torta della nonna class); the line's job is warmth with flour on it.
FILE UNDER: SAINTS: archival stamp register, verb-first where the language allows; the loc note explains it is a cataloging instruction that becomes an epitaph.
CARRIED: the load-bearing verb. One rendering per locale, used for the 1974 monologue, Merle's thesis, and Ending 2's WELCOME HOME orbit, enforced by glossary; if the verb drifts, the theme unthreads.
ADDRESS AND WARMTH: the T-V decision is characterization. Merle uses the informal or endearing register from her first line in every language that has one; Vess stays formal until the margin is credited, then shifts, and the shift is the translation of the scene. The Floor Manager translates to nothing, everywhere, by contract.
THE TITLE: RESTORATION remains untranslated on the box; a localized subtitle line is permitted below it.

## 5 · GLOSSARY SEED (extraction ships with definitions)
capture, take, the sheet, strike, dailies, the burn, generation (G0 to G3), TBC, the schedule, ON AIR, BREAK, sign-off, the club, the bench, accession, the missing verse, mediated, the little door, PLACES, HOLD YOUR APPLAUSE. Do-not-translate set: WGLD, Chum, The Gladhouse, RESTORATION, slate codes.

## 6 · PIPELINE AND QA
Pseudo-localization build first (accented, bracketed, plus 35 percent padded) run against the playtest protocol's probe subset; per-wave LQA uses native players on the Day 1 and finale scripts specifically; every locale build re-runs the invariant harness because a translated string must never break a silence contract or widen a protected beat; the accessibility caption set localizes with system text at full parity per the conformance pass.

## 7 · OWNERSHIP
Locale tiers are a Gate-0-adjacent signature: WAVE 1 AT LAUNCH · WAVE 1 FAST-FOLLOW · ENGLISH ONLY AT LAUNCH · signed ________. The Extraction Commit is engineering; the creative bible is authorial and stays under the same pen as the master document, which is to say: yours.

## ADDENDUM · THE EXTRACTION COMMIT (032)
Landed as specced under L01: tr() now wraps the four chokepoints (toast, the say pair, the prompt display, captions) plus the booth's code-built labels, using Godot's source-string-as-key mode, so behavior is byte-identical today (tr falls back to its input) and fully translatable the moment a locale column fills. The extractor ships in the repo (tools/extract_strings.py), is re-runnable, preserves existing translations by key, and its first run wrote translations/strings.csv. Its own report counts the percent-template call sites: those templates translate with their placeholders intact, which is the documented residue. Editor step on import: Godot generates .translation resources from the CSV and they register under Project Settings, Internationalization; nothing else changes.
L05 addendum (033): input references now pass through the glyph layer post-translation for the remappable five; translators keep the tokens E, SPACE, Q, T, M verbatim in target strings and the engine substitutes at display.
