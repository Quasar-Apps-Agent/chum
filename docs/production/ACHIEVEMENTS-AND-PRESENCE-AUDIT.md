# RESTORATION · ACHIEVEMENTS + PRESENCE AUDIT vs LAW 3 / LAW 5 (C14)

Audit of every achievement and every rich-presence string against LAW 3
(ONCE, EVER: the Day 4 fire-corridor moment is never referenced again by any
system, including achievements, presence and logs, and its name appears in no
code file) and LAW 5 (SILENCE CONTRACTS: Chum has no account, no achievement
title, no presence string), with the companion rules those laws lean on: the
deferral rule and the meta-silence ledger, the casualty ledger's "no per-death
achievements", the invariant suite's I11/I29/I30 and the QA regression's
QA-04/QA-25/QA-29/QA-45/QA-47/QA-48. Every rule asserted carries a citation
`[KEY §section]` (keys in §0.1). Where canon is silent the cell says **OPEN**
and the question is numbered in §9. Nothing here invents canon; where two canon
documents disagree the disagreement is recorded, not resolved.

This is a paper deliverable from the cloud lane: no Blender, no UE, no Godot
was run. Verification is by inspection and by the read-only script in
Appendix A, whose output is reproduced verbatim in Appendix B. It is read by
the Mac lane before the achievements subsystem lands in UE (the proposed
**0.8c** box, `UE-ACCESS-SPEC-LAW9.md` §8.5) and by the LAW 3 / LAW 5 rows of
`ue/GATE-0.10.md`.

---

## 0 · CONVENTIONS

### 0.1 Source keys

| Key | Path |
|---|---|
| LAWS | `docs/packet/portbrief/THE-LAWS.md` |
| PORT-BRIEF / BUILD-ORDER | `docs/packet/portbrief/PORT-BRIEF.md`, `BUILD-ORDER.md` |
| ACH | `docs/production/restoration-achievements-design.md` |
| PRESENCE | `docs/production/restoration-steam-presence.md` |
| STEAMPAGE | `docs/production/restoration-steam-page-draft.md` |
| CASUALTY | `docs/canon/restoration-casualty-ledger.md` |
| INVARIANTS | `docs/production/restoration-invariant-suite.md` |
| QA | `docs/production/restoration-qa-regression.md` |
| MASTER | `docs/canon/restoration-game-master.md` |
| DESIGN | `docs/canon/restoration-design-doc.md` |
| WALK | `docs/canon/restoration-walkthrough-levels-endings.md` |
| DREAD | `docs/canon/restoration-dread-doctrine.md` |
| LORE | `docs/canon/restoration-lore-architecture.md` |
| KEYART | `docs/production/restoration-key-art-brief.md` |
| LOCAL | `docs/production/restoration-localization-plan.md` |
| DEMO | `docs/production/restoration-demo-cut-plan.md` |
| ACCESS | `docs/production/UE-ACCESS-SPEC-LAW9.md` |
| DOSSIER | `docs/production/CAST-DOSSIER.md` (§2.11, §7 C-11/C-13, OPEN-15) |
| GATE | `ue/GATE-0.10.md` |
| PN-STATE / PN-FINALE / PN-SCREENING / PN-BROADCAST / PN-RETAKE | `ue/PORT-NOTES-*.md` |
| ACH.gd | `scripts/achievements.gd` (the reference implementation; "the code is the intent", `AAA_BUILD_PLAN.md` §1 quoting PORT-BRIEF) |
| TITLE.gd / GLIMPSE.gd / GS.gd / BED.gd / CREDITS.gd | `scripts/title.gd`, `glimpse.gd`, `game_state.gd`, `bed_prop.gd`, `credits.gd` |
| GAMETEXT | `ue/Restoration/Data/GameText.csv` (715 rows, from `translations/strings.csv` via `tools/extract_data.py`) |
| STRINGS.py | `tools/extract_strings.py` (the harvester that feeds `translations/strings.csv`) |
| UE-STATE | `ue/Restoration/Source/Restoration/RestorationState.h`, `.cpp` |

### 0.2 Verdict vocabulary

- **PASS** — the rule holds in the reference implementation and the canon
  documents, by inspection or by script.
- **FINDING Fn** — something in the repo contradicts, or cannot be shown to
  satisfy, a rule. Each finding names the rule, the evidence and the smallest
  fix; none is applied here (one deliverable file, no code edits).
- **NOT BUILT** — the surface does not exist yet (in Godot or in UE), so the
  rule is satisfied by absence and must be re-audited when it lands.
- **OPEN On** — canon is silent or two canon documents disagree; the owner
  rules (§9).

### 0.3 Surfaces audited

| Surface | Where it lives | Status |
|---|---|---|
| Achievement ids, titles, ending map, triggers, flush gates | ACH.gd (whole file), TITLE.gd 29–39, five call sites (§2) | built (Godot) |
| Achievement descriptions, hidden flags, rarity, icons | ACH §THE LIST, §ADDENDUM (c043) only — not in code, not in any CSV | canon only |
| `Data/Achievements.csv` | named in PORT-BRIEF §5; absent from `ue/Restoration/Data/` | NOT BUILT (F5) |
| Rich-presence strings and hooks | PRESENCE (7 strings); no bridge script exists in `scripts/`; nothing in UE | canon only |
| The once-ever moment in code | GLIMPSE.gd, GS.gd 129/582/669/758, `world_builder.gd` 1131, UE-STATE h108/h193/cpp236/cpp286 | built (Godot), ported (UE save field) |
| Credits cards that name CHUM | CREDITS.gd 27, 34; GAMETEXT 71, 76 | built; adjacent to LAW 5 (§4.3) |
| Marketing (key art, Steam page) | KEYART §LAWS; STEAMPAGE | canon only; no art in repo |
| UE achievements / presence code | none (`grep -i achiev|presence` over `Source/`: no hits) | NOT BUILT — GATE row 5 "BY ABSENCE" |

---

## 1 · THE RULES, QUOTED

### 1.1 The two laws

> 3. ONCE, EVER. The Day 4 fire-corridor moment occurs at most once per save
> and is never referenced again by any system, including achievements,
> presence, and logs. Its name appears in no code file. [LAWS 3]

> 5. SILENCE CONTRACTS. The bell rings once, at the finale beat, and its
> caption says so. Chum's bell is otherwise silent; Chum speaks nowhere; Chum
> has no account, no achievement title, no presence string. [LAWS 5]

This audit covers the meta clauses of both: LAW 3's "achievements, presence,
and logs" and "no code file"; LAW 5's "no account, no achievement title, no
presence string". The bell, the voice and the strike are DOSSIER §7 C-11/C-12
territory and are not re-audited here.

### 1.2 The companion rules

| Rule | Text | Source |
|---|---|---|
| Deferral | "No achievement may surface during a protected beat. Unlocks fire silently into a queue and flush only at two moments: the next morning toast, or the title screen. The glimpse, the fire tape, the premiere, every ending sequence, and the demo card are popup-free zones by construction, not by hope." | ACH §DOCTRINE 1; LAWS 9 ("the deferral rule ship[s] in every build of every engine"); PORT-BRIEF §5 ("the deferral rule and meta-silence live in the design doc and are not optional") |
| Meta-silence | "The glimpse has NO achievement, ever … The warm unit is acknowledged only through the dock-completion achievement, whose text never mentions warmth. The seance grants one achievement for reaching the final answer, never per-answer pings … Chum's name appears in no achievement title." | ACH §DOCTRINE 2 |
| Voice | "Titles and descriptions read in the accession ledger's register: short, procedural, slightly too calm. Hidden achievements (Steam-hidden) cover every ending and every secret; their pre-unlock face is the standard WGLD card." | ACH §DOCTRINE 3 |
| Demo | "the demo build ships with achievements disabled entirely"; "Demo build: … achievements stay dark." | ACH §DOCTRINE (Demo parity); QA-48 |
| No per-death | "exactly two additions, both hidden: A27 EVERYONE GOES HOME … and A28 A ONE-WOMAN SHOW (ending 0). No per-death achievements, ever; deaths are not trophies, they are entries." | CASUALTY §ACHIEVEMENTS |
| 4c | "Ruling: ending 4c carries no achievement by design; peace is not a trophy." | ACH §ADDENDUM (c043) |
| A26 | "Ruling: A26 FULL ACCESSION remains at ten documents; the Peak dossier (D11) is extra credit" | ACH §ADDENDUM (c043) |
| Presence doctrine | "a friends list is a broadcast. The schedule may appear on it; the secrets may not. Presence strings are diegetic, spoiler-null" | PRESENCE §Doctrine |
| Presence spoilers | "Never: any ending name, DEAD AIR, the seance, the quiet room, the dock's contents, the once-ever moment, day numbers past 5. Nights are all one string on purpose … Chum's name appears in no presence string" | PRESENCE §SPOILER RULES |
| I11 | "The glimpse never repeats. TEST: probe P10 including relaunch. TELEMETRY: glimpse_seen flag in save; harness asserts single spawn per save lifetime." | INVARIANTS §C I11 |
| I29 | "zero casualties and zero rows produce no reading and file A27 once" | INVARIANTS §ADDENDUM I29 |
| I30 | "no death, ending 0 included, produces a mid-play achievement toast; the once-ever moment still has no entry anywhere new · build check extended over the casualty files" | INVARIANTS §ADDENDUM I30 |
| QA | QA-04 title shows FILED WHILE YOU WERE OUT exactly once; QA-25 the once-ever moment exactly once per save; QA-29 no achievement toast between title and morning; QA-45 A28 files at the next flush gate; QA-47 clean run files A27; QA-48 demo achievements dark | QA |
| Marketing | "The glimpse figure and Leland's face are never depicted in any marketing material, ever; their scarcity is product." | KEYART §LAWS |
| Violation budget | "One startle. One interface lie. One once-ever sight … the budget never grows." | DREAD §L5 |
| Localization | "SYSTEM TEXT: toasts, prompts, objectives, menus, captions, achievements: fully localized." | LOCAL §world text vs system text |

### 1.3 What "its name" is — the audit's limit

Canon never states the forbidden name. The law calls the moment "the Day 4
fire-corridor moment" [LAWS 3]; the game master heads the scene "T4.8 THE
GLIMPSE" [MASTER T4.8] and every production document uses "the glimpse" as
its working label [ACH §DOCTRINE 1–2; INVARIANTS I11; DREAD §L5 "one once-ever
sight"; WALK "the direct-sight glimpse"]. The UE access spec reads the law as
withholding the name on purpose: the static guard "reads it from an untracked
file, so the name still 'appears in no code file'" and "owner supplies the
string out of band" [ACCESS §8.2]; the gate says "the loop does not know it by
design" [GATE row 3]. So this audit cannot rule whether the working label IS
the name. It does the auditable thing: §5.4 lists every code-file occurrence
of the label, and §9 O1 carries the question, already opened as DOSSIER §7
C-13 and OPEN-15.

---

## 2 · THE ROSTER · A01–A28

Titles are the code's (`TITLES`, ACH.gd 11–22). Description and hidden flag
are canon only (ACH §THE LIST, §ADDENDUM). Trigger is canon → code, with the
line that fires it. LAW 3 = does it reference the once-ever moment; LAW 5 =
does title or description carry CHUM; GT = title present as a key in
GAMETEXT.

| Id | Title (code) | Description (canon) | Trigger (canon) → code | Hidden | LAW 3 | LAW 5 | GT | Notes |
|---|---|---|---|---|---|---|---|---|
| A01 | FIRST SIGNATURE | "The paper takes your name." | first sign_log success → `log_signed` (ACH.gd 37) | no | ok | ok | yes | |
| A02 | CAREFUL HANDS | "A capture, start to bars, in real time." | first **clean** capture → `captures.size() > 0` (ACH.gd 64) | no | ok | ok | yes | code fires on ANY capture, not a clean one — **O9** |
| A03 | THE SCOPE READS MASTER | "You turned the knob. The label did not care." | first gen knob use → `gen_knob.gd` 17 | no | ok | ok | yes | |
| A04 | ON THE BEAT | "You answered with the room." | on-beat respond → `screening_event.gd` 103 | no | ok | ok | yes | PN-SCREENING §8 |
| A05 | STILLNESS, HELD WHOLE | "The cup did not move." | QUIET stance success → `screening_event.gd` 64 | no | ok | ok | yes | |
| A06 | MID-MOTION | "You spoke to her during a break. She will resume." | interact with frozen Harriet → `harriet.gd` 94 (on BREAK) | no | ok | ok | **no** | title not harvested — **F6** |
| A07 | HOLD YOUR APPLAUSE | "The seventh was a gift." | Harriet's note read → `signals_known.size() >= 7` (ACH.gd 65) | no | ok | ok | yes | |
| A08 | YOU WERE NOT QUIET | "It changed direction." | first heard-noise relocation → `rundown.gd` 180 | no | ok | ok | yes | fires inside the hunt; queued, never surfaces (§3) |
| A09 | TOMORROW'S DATE | "The loops of the R are yours." | `presigned_seen` (ACH.gd 66) | hidden | ok | ok | yes | |
| A10 | THE ROWS KEEP THEIR ORDER | "Six units. Filed." | `dock_done` (ACH.gd 67) | no | ok | ok | yes | the warm unit's only acknowledgement; text never says warm [ACH §DOCTRINE 2] — PASS |
| A11 | PER V. KEYS | "Somebody's name is on something." | `vess_credited` (ACH.gd 68) | no | ok | ok | yes | canon list says PER V. CARDONA; cast sheet and GAMETEXT say Keys — **O8** (DOSSIER §7 C-5) |
| A12 | NO SEARCHER SINGS | "You heard 1974, complete." | `merle_1974` (ACH.gd 69) | hidden | ok | ok | yes | |
| A13 | THE UNFINISHED LINE | "You watched the fire tape to the cut." | `fire_tape_watched` (ACH.gd 70) | hidden | ok (the fire TAPE, T3.4, not the corridor moment) | ok | yes | |
| A14 | I'VE READ THE ENDING | "You stepped to the last answer." | `leland_answers.size() >= 5` (ACH.gd 71) | hidden | ok | ok | yes | the one seance achievement; no per-answer pings — PASS [ACH §DOCTRINE 2] |
| A15 | ORDER MATTERS | "B before C, the way the panel is labeled." | `cascade_done` (ACH.gd 72) | no | ok | ok | yes | |
| A16 | THE LONG WAY AROUND | "The felt door has a key after all." | QUIET ROOM key → `has_key("QUIET ROOM")` (ACH.gd 73) | hidden | ok | ok | yes | |
| A17 | INK | "Three entries were possible. One stands." | decision committed → `decision != ""` (ACH.gd 74) | no | ok | ok | **no** | title not harvested — **F6** |
| A18 | NEXT WEEK'S EPISODE | "Starring you." | first run_ended → `run_ended` (ACH.gd 38) | no | ok | ok | yes | run death; canon keeps it ("dying politely is part of the show" [ACH §RARITY]) — see §6 |
| A19 | EMPTY DRAWER | "The loupe was last." | `items_lost >= 7` (ACH.gd 75) | hidden | ok | ok | yes | |
| A20 | SEALED FOR BROADCAST | "Lock-in's just till air." | `lockdown_done` (ACH.gd 76) | no | ok | ok | yes | |
| A21 | THERE'S COBBLER | — (none in canon) | ending THE BURN → `ENDING_MAP` (ACH.gd 24) | hidden | ok | ok | yes | no description text exists — **O11** |
| A22 | WELCOME HOME | — | ending THE NEW PRODUCER → `ENDING_MAP` | hidden | ok | ok | yes | **O11** |
| A23 | FILE UNDER: SAINTS | — | SIGN-OFF, Rita closes → `"SIGN-OFF · RITA CLOSES"` | hidden | ok | ok | yes | **O11** |
| A24 | IT'S OKAY. NOBODY'S WATCHING. | — | SIGN-OFF, Leland closes → `"SIGN-OFF · LELAND CLOSES"` | hidden | ok | ok | yes | Leland's line [MASTER ENDING 1A]; **O11** |
| A25 | SIGNED OFF | — | ending DEAD AIR (4a and 4b both map to `"DEAD AIR"`) | hidden; "the only all-black icon in the set" | ok | ok | yes | **O11** |
| A26 | FULL ACCESSION | "Every document in the building, read." | D01–D10 read → `read_props.size() >= 10` (ACH.gd 77) | no | ok | ok | yes | ten, D11 excluded — matches the ruling |
| A27 | EVERYONE GOES HOME | "The reading was silence." | any ending, empty ledger, zero rows → `on_ending` (ACH.gd 54–55) | hidden | ok | ok | yes | I29, QA-47 |
| A28 | A ONE-WOMAN SHOW | "Every part, one performer." | ending 0 → `"A ONE-WOMAN SHOW"` in `ENDING_MAP` | hidden; "the only card in the set with a name on it" | ok | ok (title) | yes | whose name is on the icon is not stated — **O4** |
| — | (4c THE COMPLETED SIGN-OFF) | — | no entry in `ENDING_MAP` | — | — | — | — | matches the ruling [ACH §ADDENDUM]; PN-FINALE §6.1 |

Roster checks (Appendix B): 28 ids, contiguous A01–A28; every id has a
trigger (two signals, one ending hook, five call sites, fourteen 1 s polls);
ending map has six names and they match the six `mark_ending` strings in
PN-FINALE §6.1; no title contains CHUM; no description contains Chum; the
only title drift between canon and code is A11.

---

## 3 · THE DEFERRAL RULE (LAW 9's meta clause)

| Check | Evidence | Verdict |
|---|---|---|
| `unlock()` never surfaces anything | ACH.gd 45–50: mark, save, emit `achievement_unlocked`; no toast. Nothing in `scripts/` or UE listens to `achievement_unlocked` (Appendix B) | PASS |
| Exactly two exits | Toast sites in ACH.gd: 2, both inside `flush_to_toasts` (88–97); `flush_silent` (100–103) returns titles to TITLE.gd 29–39 for the `FILED WHILE YOU WERE OUT:` stack | PASS |
| Morning gate is the morning | `flush_to_toasts` is bound to `night_changed(false)` (ACH.gd 39–43); `set_night` is called from exactly one place, BED.gd 23 (sleep), and BED.gd 13–22 refuses the bed under DEMO, after `finale_done`, and diverts to `start_finale()` once `decision` and `lockdown_done` are set. So no morning can fall inside the premiere or an ending | PASS |
| The glimpse is popup-free | It fires only at night (GLIMPSE.gd 19); the morning flush is the next `set_night(false)` | PASS |
| The fire tape is popup-free | A13 is polled (ACH.gd 70) and queued; surfaces at the next morning or title | PASS |
| The premiere / endings are popup-free | `mark_ending` → `Achievements.on_ending` queues (GS.gd 424–432); credits never flush (I30; PN-FINALE §6.6); the title is a canonical gate [ACH §DOCTRINE 1] | PASS |
| The demo card is popup-free | `unlock` is a no-op under `GameState.DEMO` (ACH.gd 46); DEMO §E1–E7 | PASS (QA-48) |
| Idempotent, persisted apart from the save | `_unlocked` guard (46); `user://achievements.cfg` (9, 112–126); survives NEW GAME by design [ACCESS §8.2] | PASS |
| UE | no subsystem, no save slot, no gates; proposed as 0.8c with tests §8.4 [ACCESS §8.2–8.5]; GATE row 9 "NOT YET — flagged, spec ready" | NOT BUILT |

Observation (not a law finding): the morning flush concatenates
`"FILED · " + title` before `GameState.toast` calls `tr()` (GS.gd 211–212),
so no locale can match the assembled string; the GAMETEXT keys are `FILED · `
and the bare title. That is the Extraction Commit's residue class ("format
strings and inline concatenations", LOCAL L01) and belongs to C12.

---

## 4 · LAW 5 · NO ACCOUNT, NO ACHIEVEMENT TITLE, NO PRESENCE STRING

### 4.1 Achievement titles and descriptions

- 28 titles: none contains CHUM (script assertion, Appendix B). PASS.
- 23 canon descriptions (A01–A20, A26 in §THE LIST; A27, A28 in §ADDENDUM):
  none contains Chum. PASS. A21–A25 have no description text anywhere (O11).
- The flush strings the player sees (`FILED · <title>`, `FILED · %d entries,
  %s among them.`, `FILED WHILE YOU WERE OUT:`) carry only titles. PASS.

### 4.2 Presence strings

The seven english masters [PRESENCE §STATES]:

| Key | String | Chum? | Ending name / secret? |
|---|---|---|---|
| #Day | Day %day% at WGLD | no | no (but see §7 F8 on %day% past 5) |
| #OnAir | ON AIR · do not knock | no | no |
| #Bench | At the bench · Tape %tape% | no | no |
| #Night | After sign-off | no | shares a word with ending 1's name "SIGN-OFF"; it is the nightly broadcast sign-off, authored by the spec itself — observation only, **O12** |
| #Premiere | THE GLADHOUSE RETURNS (LIVE) | no | no (spec: "the Steam page already says this much" — the page draft does not contain the phrase, **O7**) |
| #Credits | Signing off | no | no |
| #Menu | At the title card | no | no |

PASS on LAW 5 and on every item of the spoiler list except the two OPENs.
No bridge exists in the reference (`Steam.setRichPresence` appears in no
script; Appendix B) and nothing exists in UE, so the strings are canon only.

### 4.3 "No account"

Canon defines "account" nowhere: the word occurs in no other canon document
in this sense (Appendix B grep: DESIGN 88 "both hands accounted for", DESIGN
234 "a witness account"). The DOSSIER reads it as "the compound outside the
format (no presence, no account)" [DOSSIER §7 C-11]. The auditable readings
are: no platform / Steam persona, no in-fiction account (no ledger line in
his name, no credit as a person). Checked against the repo under the second
reading:

- Credits cards: `"and CHUM\nas himself"` (CREDITS.gd 27; GAMETEXT 71) on
  every run, and `"and CHUM\nas RITA IVORI"` for ending 0 (CREDITS.gd 34;
  GAMETEXT 76; QA-45 "nine cards, one name"). PN-FINALE §6.5 flagged these
  for this audit as "a credit line, not an achievement or presence string".
  Verdict: outside LAW 5's three named surfaces; whether a CREDIT is an
  "account" is **O2** (it is the same scope question as DOSSIER C-11).
- The binder / ledger: no ledger entry, casualty row or save key is in his
  name (`mark_casualty` names VESS, FLOOR MANAGER, LELAND, MERLE, HARRIET
  only — PN-FINALE §6.4). PASS.
- Save file: no key names him (PN-STATE key table). PASS.

### 4.4 Where CHUM's name legitimately appears in text

For the record, GAMETEXT carries fifteen rows with his name (tape lines,
`CHUM · ON HIS MARK`, `CHUM'S MARK`, the fan letter, the Peak dossier title,
the two credits cards). All are in-fiction text or credits; none is an
achievement title, a presence string or a system notification. This is the
inventory the UE static guard (`Restoration.Access.Deferral.MetaSilence`,
ACCESS §8.4) should be scoped against: it must check `Achievements.csv`
titles and the presence table, not GameText at large.

---

## 5 · LAW 3 · NEVER REFERENCED AGAIN · NO NAME IN CODE

### 5.1 Achievements

No entry triggers on `glimpse_seen`; the file does not contain the token
(script assertion) and says so in its header: "The once-ever moment has no
entry here, on purpose" (ACH.gd 5). A13 THE UNFINISHED LINE is the fire TAPE
(T3.4, `fire_tape_watched`), A16 is the QUIET ROOM key — neither is the
corridor moment. PASS. I30's "no entry anywhere new" holds for A27/A28.

### 5.2 Presence

No presence state reads the moment; nights are one string by design
[PRESENCE §SPOILER RULES]. PASS (canon only; nothing built).

### 5.3 Logs

| Log | Evidence | Verdict |
|---|---|---|
| Director / soak log lines (`director.log_line`, `rundown.gd`) | no line mentions the moment (grep, Appendix B: the only `glimpse` tokens in `scripts/` are GS.gd 129/582/669/758, GLIMPSE.gd, `world_builder.gd` 1131) | PASS |
| The save ("the log" in-fiction: `save_log()`, "CONTINUE · no log on file") | carries `glimpse_seen` as v16 key 53 (GS.gd 582; PN-STATE key table row 53) | **F1** / **O1** — see below |
| First-boot telemetry dump | `docs/telemetry/first-boot/transmitter_log.json` 25 `"glimpse_seen": false` (a save dump; data, not code) | same as the save |
| In-moment toasts | GLIMPSE.gd 31, 66, 68 narrate the moment while it happens; nothing toasts it afterwards | PASS ("never referenced AGAIN") |
| The unseal toast | GLIMPSE.gd 18 "The club unseals the fire corridor for the anniversary. Nobody goes first." keyed on `fire_unsealed` — the corridor's unsealing, a different fact; GATE row 3 already rules `has_fire_tape` / `fire_unsealed` "canonical v16 keys, not the moment's name" | PASS |

The save key is a real tension between two canon rules: LAWS 3 says the
moment is never referenced by "logs", and INVARIANTS I11 REQUIRES
"glimpse_seen flag in save; harness asserts single spawn per save lifetime"
(it is also how QA-25 "exactly once per save" is enforceable at all: GLIMPSE.gd
19 reads the flag as its guard). The UE port carried the key faithfully
(`GlimpseSeen`, UE-STATE h108 "// 53") under the migration map's "WHAT MUST
NOT CHANGE: … save semantics" [`AAA_BUILD_PLAN.md` §1 THE PORT KIT]. Recorded
as **F1**, ruled by **O1**; not resolved here.

### 5.4 "Its name appears in no code file" — every occurrence of the canon label

Scope: `scripts/*.gd`, `scenes/*.tscn`, `tools/*.py`, `ue/Restoration/Source/
Restoration/*`, `ue/Restoration/Data/*.csv`, `ue/pyscripts/*.py`,
`project.godot`, `translations/strings.csv`. Pattern `/glimpse/i`.

| File:line | Token | Class |
|---|---|---|
| `scripts/glimpse.gd` (filename), :1 `class_name Glimpse` | the actor and its class | label as an identifier |
| `scripts/glimpse.gd:19`, `:64` | `GameState.glimpse_seen` | label as a state key |
| `scripts/game_state.gd:129`, `:582`, `:669`, `:758` | `glimpse_seen` declare / save / load / reset | label as a state key (v16 key 53) |
| `scripts/world_builder.gd:1131` | `Glimpse.new()` | label as an identifier |
| `ue/Restoration/Source/Restoration/RestorationState.h:108`, `:193` | `GlimpseSeen`, `bGlimpseSeen` | label as a state key (ported) |
| `ue/Restoration/Source/Restoration/RestorationState.cpp:236`, `:286` | save / load of the same | label as a state key (ported) |
| `tools/build_chum_af.py:1537`, `:1548` | "glimpsed inside", "glimpsed behind" | the English verb in comments about the After-Fire maw; NOT the moment — no action |
| `ue/Restoration/Data/*.csv`, `translations/strings.csv`, `scenes/*.tscn`, `ue/pyscripts/*.py`, `project.godot` | — | no hits |

Twelve occurrences of the label as an identifier or key across five code
files (three Godot, the UE header and its source). This is DOSSIER §7 C-13
restated with the UE pair added; it is **F2** if the owner rules under O1
that the label is the name, and a PASS if the owner rules the name is
something canon has never written down. The UE name for the once-ever actor,
its asset and its flag is OPEN-15 [DOSSIER; `CAST-BUILD-BRIEFS.md` §10]; the
brief's working asset name `SK_Cast_Unresolved` is "deliberately meaningless"
and is the pattern to follow if O1 rules against the label.

### 5.5 Once per save

GLIMPSE.gd 12–27: fires only when `not glimpse_seen`, `is_night`, `not
premiere_live`, player inside the FIRE CORRIDOR rect; sets the flag at 64 and
saves. `reset_new_game` clears it (GS.gd 758). PASS on "at most once per
save" (I11, QA-25). Nothing else reads the flag (Appendix B). PASS on "never
referenced again by any system".

### 5.6 Marketing

"The glimpse figure and Leland's face are never depicted in any marketing
material, ever" [KEYART §LAWS]; the Steam page draft and its c043 addendum
describe neither [STEAMPAGE]. No art exists in the repo to check. PASS by
absence; re-audit at the key-art unit.

---

## 6 · LAW 7's COMPANION · NO PER-DEATH ACHIEVEMENTS

- No `Achievements.unlock` sits within 400 characters of any of the seven
  `mark_casualty` sites (`live_production.gd` 97, 189; `decision_ledger.gd`
  63; `patchbay_console.gd` 93; `seance_dock.gd` 103, 125; `hud.gd` 511) —
  script check, Appendix B. PASS [CASUALTY §ACHIEVEMENTS].
- A27 rewards the ABSENCE of deaths (I29). PASS.
- A18 NEXT WEEK'S EPISODE fires on `run_ended`, Rita's own run death. The
  casualty ledger's ban is written about the cast ("deaths are not trophies,
  they are entries") and its addendum says "exactly two additions" without
  striking A18; the achievements doc keeps it on purpose ("A18 will out-earn
  several endings and that is correct: dying politely is part of the show"
  [ACH §RARITY]). Canon-consistent as written; noted as **O10** only so the
  owner sees the two sentences side by side.

---

## 7 · FINDINGS

| # | Rule | Evidence | Smallest fix (not applied) |
|---|---|---|---|
| **F1** | LAWS 3 "logs" vs INVARIANTS I11 | the save carries `glimpse_seen` (GS.gd 582; UE key 53) | none until **O1** rules; if the key must be renamed, it is a v16 schema change and needs the save-migration note the port kit forbids doing silently |
| **F2** | LAWS 3 "no code file" (conditional on **O1**) | twelve label occurrences in four code files (§5.4) | Godot: reference implementation, leave; UE: rename `GlimpseSeen`/`bGlimpseSeen` per OPEN-15 before 0.8c, with the CSV/save key decision from O1 |
| **F3** | ACH §DOCTRINE 3 + LOCAL "achievements: fully localized" | A21–A25 have no description text anywhere in canon or code | owner authors five descriptions in the ledger's voice (**O11**); until then the Steamworks table cannot be filled |
| **F4** | ACH list vs cast canon | A11 title reads PER V. CARDONA in canon, PER V. KEYS in code and GAMETEXT | correct ACH §THE LIST to KEYS (**O8**; DOSSIER C-5) |
| **F5** | PORT-BRIEF §5 names `Achievements.csv` (id, title, Steam-hidden) | not in `ue/Restoration/Data/`; ACCESS §8.3 already flags it | generate from `TITLES` + the hidden column of §2 (this file); extend `tools/extract_data.py` |
| **F6** | LOCAL "achievements: fully localized" | A06 MID-MOTION and A17 INK are not in `translations/strings.csv` or GAMETEXT: STRINGS.py 18–21 drops literals shorter than 4 chars (`INK`) and literals with no space or `·` (`MID-MOTION`) | whitelist `TITLES` in the harvester (C12 territory); also see the §3 observation on the `FILED ·` concatenation |
| **F7** | ACH §THE LIST A02 "first clean capture" | code fires on any capture (`captures.size() > 0`) | **O9**: either the doc means "first capture" or the code needs a clean flag; the code is the intent by default |
| **F8** | PRESENCE §SPOILER RULES "day numbers past 5" | `set_night(false)` increments `day` without bound (GS.gd 470); `current_tape` is capped at 5 but `%day%` is not; a Day 6 morning would render "Day 6 at WGLD" | the bridge must cap or switch the #Day string past 5; canon gives no wording — **O6** |
| **F9** | PRESENCE §HOOKS "GameState already emits … day changes" | there is no `day_changed` signal; the day increments inside `set_night` and only `night_changed(false)` carries it (GS.gd 136, 467–479) | the bridge reads `day` on `night_changed(false)`; PRESENCE §HOOKS wording to be corrected |
| **F10** | PRESENCE precedence | `premiere_live` and `is_night` and `recording` can co-exist; the spec gives no ordering between #Premiere, #Night, #Bench, #OnAir | **O5** |

No finding is a LAW 5 violation. Two are LAW 3 tensions (F1, F2) that
canon already carries as open (C-13, OPEN-15) and that this audit could not
close without the name it is forbidden to know.

---

## 8 · WHAT THE MAC LANE SHOULD DO WITH THIS (0.8c and GATE-0.10)

1. Build `URestorationAchievements` exactly as ACCESS §8.2 (two gates, no
   beat detector, `Unlock` never toasts). The §8.4 tests are sufficient; add
   one static assertion from this audit: `ENDING_MAP` has six keys and no
   key for `THE COMPLETED SIGN-OFF`.
2. Generate `Data/Achievements.csv` (F5) with the hidden column from §2:
   hidden = A09, A12, A13, A14, A16, A19, A21–A25, A27, A28 (thirteen);
   visible = the other fifteen.
3. Scope the `MetaSilence` static guard to `Achievements.csv` titles and the
   presence table (§4.4), and read the forbidden name from the untracked
   file as ACCESS §8.2 specifies — do not commit it.
4. Before porting `GlimpseSeen` into any new file, get **O1** ruled; the
   field already exists in `RestorationState.h` and is the one place LAW 3's
   code clause is currently exposed in UE.
5. GATE-0.10 row 3 ("Owner to confirm the forbidden name appears in no UE
   file") can cite §5.4 of this file as the inventory; row 5's LAW 5
   evidence can cite §4.1–4.3.
6. Presence is P6 [BUILD-ORDER P6]; when it lands, F8–F10 are its acceptance
   list, plus: strings from a table, `%day%` capped per O6, DEMO absent
   [PRESENCE §HOOKS].

---

## 9 · OPEN · rulings needed (the owner decides; the loop does not)

| # | Question | Where it bites |
|---|---|---|
| **O1** | Is the canon working label ("the glimpse") the forbidden name of LAW 3? If yes: F2 applies to twelve occurrences, and the v16 save key 53 (`glimpse_seen`) conflicts with "save semantics must not change" — which rule yields? If no: what IS the name, so the untracked guard file can exist? (= DOSSIER C-13, OPEN-15) | UE-STATE h108; 0.8c static guard; GATE row 3 |
| **O2** | LAW 5 "no account": does a CREDIT card ("and CHUM as himself" / "as RITA IVORI") count? (same scope question as DOSSIER C-11) | CREDITS.gd 27, 34; QA-45 |
| **O3** | What does "no account" name in canon — platform persona, in-fiction ledger identity, or both? One sentence would close §4.3 | STEAM setup; binder |
| **O4** | A28's icon is "the only card in the set with a name on it" — whose name? If CHUM's, it is a name on an achievement surface (icon, not title); RITA IVORI is the reading that keeps LAW 5 untouched | Steam art brief |
| **O5** | Presence precedence when #Premiere, #Night, #Bench, #OnAir are simultaneously true | presence bridge |
| **O6** | Presence past Day 5: cap `%day%`, hold "Day 5", or a new string? Canon bans the number and offers no replacement | presence bridge |
| **O7** | PRESENCE says the Steam page "already says" THE GLADHOUSE RETURNS (LIVE); STEAMPAGE v1 + c043 addendum do not contain the phrase — add it to the page or drop the parenthetical | STEAMPAGE |
| **O8** | A11 title: KEYS (cast sheet, code, GAMETEXT) vs CARDONA (ACH list, UI specimen) | ACH doc |
| **O9** | A02 "first clean capture" vs code "any capture" | ACH.gd 64 or ACH doc |
| **O10** | A18 (run death) beside "no per-death achievements, ever" — confirm A18 stands (canon reads as yes) | none unless struck |
| **O11** | Descriptions for A21–A25 (none exist); and the descriptions' home — Steamworks only, or a `description` column in `Achievements.csv` for localization (LOCAL says achievements are fully localized) | Achievements.csv schema |
| **O12** | #Night "After sign-off" shares a word with ending 1's name; keep (it is the broadcast term and the spec's own choice) or reword | presence table |

---

## APPENDIX A · the verification script (read-only; run from the repo root)

```python
#!/usr/bin/env python3
"""C14 verification: achievements + presence vs LAW 3 / LAW 5.
Read-only. Run from the repo root. Exits 0; every line is evidence."""
import csv, glob, os, re, sys

ROOT = os.getcwd()
def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()

ach = rd("scripts/achievements.gd")
titles = dict(re.findall(r'"(A\d\d)":\s*"([^"]+)"', ach.split("const ENDING_MAP")[0]))
ending_map = dict(re.findall(r'"([^"]+)":\s*"(A\d\d)"', ach.split("const ENDING_MAP")[1].split("var _unlocked")[0]))
print("TITLES entries:", len(titles), "ids", min(titles), "..", max(titles))
assert len(titles) == 28 and set(titles) == {"A%02d" % i for i in range(1, 29)}
print("ENDING_MAP entries:", len(ending_map), sorted(ending_map))

# LAW 5: no title carries his name
bad = [k for k, v in titles.items() if "CHUM" in v.upper()]
print("LAW5 titles containing CHUM:", bad or "none")
assert not bad

# design doc descriptions (only source of descriptions)
design = rd("docs/production/restoration-achievements-design.md")
descs = dict(re.findall(r'^(A\d\d) [^·]+· "([^"]+)"', design, re.M))
print("design descriptions found:", len(descs), "| containing CHUM:",
      [k for k, v in descs.items() if "chum" in v.lower()] or "none")
design_titles = dict(re.findall(r'^(A\d\d) (.+?) ·', design, re.M))
drift = {k: (design_titles[k], titles[k]) for k in titles if k in design_titles and design_titles[k].strip() != titles[k]}
print("title drift design vs code:", drift or "none")

# LAW 3: once-ever moment has no achievement entry; nothing in the file reads glimpse_seen
print("achievements.gd mentions glimpse_seen:", "glimpse_seen" in ach)
assert "glimpse_seen" not in ach

# Deferral: exactly one toast region in achievements.gd, inside flush_to_toasts
toast_sites = [m.start() for m in re.finditer(r"GameState\.toast\(", ach)]
f2t = ach.index("func flush_to_toasts")
nxt = ach.index("func flush_silent")
print("toast sites in achievements.gd:", len(toast_sites), "| all inside flush_to_toasts:",
      all(f2t < s < nxt for s in toast_sites))
assert all(f2t < s < nxt for s in toast_sites)
# unlock() itself never toasts
unlock_body = ach[ach.index("func unlock"):ach.index("func on_ending")]
print("unlock() toasts:", "toast(" in unlock_body)
assert "toast(" not in unlock_body

# flush gates: night_changed(false) and title.gd
print("flush gate night_changed in achievements.gd:", "night_changed.connect" in ach)
title = rd("scripts/title.gd")
print("title.gd calls flush_silent:", "Achievements.flush_silent()" in title)
callers = [(f, i + 1) for f in glob.glob("scripts/*.gd") for i, l in enumerate(rd(f).splitlines())
           if "set_night(" in l and "func set_night" not in l]
print("set_night callers (the morning gate's only trigger):", callers)

# every unlock call site in the codebase
sites = []
for f in sorted(glob.glob("scripts/*.gd")):
    for i, l in enumerate(rd(f).splitlines()):
        m = re.search(r'unlock\("(A\d\d)"\)', l)
        if m: sites.append((os.path.basename(f), i + 1, m.group(1)))
print("unlock call sites:", sites)
polled = re.findall(r'if .+?: unlock\("(A\d\d)"\)', ach)
print("polled ids:", polled)
covered = {s[2] for s in sites} | set(polled) | set(ending_map.values()) | {"A27"}
print("ids with no trigger anywhere:", sorted(set(titles) - covered) or "none")

# LAW 7 companion: no unlock at any mark_casualty site
cas = []
for f in sorted(glob.glob("scripts/*.gd")):
    src = rd(f)
    for m in re.finditer(r"mark_casualty\(", src):
        window = src[max(0, m.start() - 400): m.end() + 400]
        if "Achievements.unlock" in window: cas.append((os.path.basename(f), m.start()))
print("unlock within 400 chars of a mark_casualty:", cas or "none")

# GameText coverage of titles
keys = [r[0] for r in csv.reader(open("ue/Restoration/Data/GameText.csv", encoding="utf-8"))]
missing = [k + " " + v for k, v in titles.items() if v not in keys]
print("titles missing from GameText.csv:", missing or "none")
print("Achievements.csv present in Data:", os.path.exists("ue/Restoration/Data/Achievements.csv"))

# Presence spec strings
pres = rd("docs/production/restoration-steam-presence.md")
strings = re.findall(r'^#(\w+)\s+"([^"]+)"', pres, re.M)
print("presence strings:", len(strings))
forbidden = ["chum", "dead air", "seance", "séance", "quiet room", "glimpse", "burn", "producer", "sign-off", "saints"]
hits = [(k, s) for k, s in strings if any(w in s.lower() for w in forbidden)]
print("presence strings carrying a forbidden word:", hits or "none")
print("presence bridge in scripts (Steam.setRichPresence):",
      any("setRichPresence" in rd(f) for f in glob.glob("scripts/*.gd")))

# LAW 3: code-file occurrences of the canon label for the moment
code_globs = ["scripts/*.gd", "scenes/*.tscn", "tools/*.py", "ue/Restoration/Source/Restoration/*",
              "ue/Restoration/Data/*.csv", "ue/pyscripts/*.py", "project.godot", "translations/strings.csv"]
occ = []
for g in code_globs:
    for f in sorted(glob.glob(g)):
        try: src = rd(f)
        except Exception: continue
        for i, l in enumerate(src.splitlines()):
            if re.search(r"glimpse", l, re.I):
                occ.append("%s:%d: %s" % (f, i + 1, l.strip()[:90]))
print("code-file lines matching /glimpse/i (%d):" % len(occ))
for o in occ: print("   ", o)
print("UE Source mentions of achievement/presence:",
      [f for f in glob.glob("ue/Restoration/Source/Restoration/*") if re.search(r"achiev|presence", rd(f), re.I)] or "none")
print("VERIFY-C14 OK")
```

## APPENDIX B · script output (origin/main at 38e5c6b, 2026-09-06)

```
TITLES entries: 28 ids A01 .. A28
ENDING_MAP entries: 6 ['A ONE-WOMAN SHOW', 'DEAD AIR', 'SIGN-OFF · LELAND CLOSES', 'SIGN-OFF · RITA CLOSES', 'THE BURN', 'THE NEW PRODUCER']
LAW5 titles containing CHUM: none
design descriptions found: 21 | containing CHUM: none
title drift design vs code: {'A11': ('PER V. CARDONA', 'PER V. KEYS')}
achievements.gd mentions glimpse_seen: False
toast sites in achievements.gd: 2 | all inside flush_to_toasts: True
unlock() toasts: False
flush gate night_changed in achievements.gd: True
title.gd calls flush_silent: True
set_night callers (the morning gate's only trigger): [('scripts/bed_prop.gd', 23)]
unlock call sites: [('achievements.gd', 37, 'A01'), ('achievements.gd', 38, 'A18'), ('achievements.gd', 55, 'A27'), ('achievements.gd', 64, 'A02'), ('achievements.gd', 65, 'A07'), ('achievements.gd', 66, 'A09'), ('achievements.gd', 67, 'A10'), ('achievements.gd', 68, 'A11'), ('achievements.gd', 69, 'A12'), ('achievements.gd', 70, 'A13'), ('achievements.gd', 71, 'A14'), ('achievements.gd', 72, 'A15'), ('achievements.gd', 73, 'A16'), ('achievements.gd', 74, 'A17'), ('achievements.gd', 75, 'A19'), ('achievements.gd', 76, 'A20'), ('achievements.gd', 77, 'A26'), ('gen_knob.gd', 17, 'A03'), ('harriet.gd', 94, 'A06'), ('rundown.gd', 180, 'A08'), ('screening_event.gd', 64, 'A05'), ('screening_event.gd', 103, 'A04')]
polled ids: ['A02', 'A07', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A19', 'A20', 'A26']
ids with no trigger anywhere: none
unlock within 400 chars of a mark_casualty: none
titles missing from GameText.csv: ['A06 MID-MOTION', 'A17 INK']
Achievements.csv present in Data: False
presence strings: 7
presence strings carrying a forbidden word: [('Night', 'After sign-off')]
presence bridge in scripts (Steam.setRichPresence): False
code-file lines matching /glimpse/i (14):
    scripts/game_state.gd:129: var glimpse_seen: bool = false
    scripts/game_state.gd:582: "glimpse_seen": glimpse_seen,
    scripts/game_state.gd:669: glimpse_seen = bool(data.get("glimpse_seen", false))
    scripts/game_state.gd:758: glimpse_seen = false
    scripts/glimpse.gd:1: class_name Glimpse
    scripts/glimpse.gd:19: if GameState.glimpse_seen or _firing or not GameState.is_night or GameState.premiere_live:
    scripts/glimpse.gd:64: GameState.glimpse_seen = true
    scripts/world_builder.gd:1131: var gl := Glimpse.new()
    tools/build_chum_af.py:1537: ## the machinery glimpsed inside: dark slats just proud of the void's face
    tools/build_chum_af.py:1548: ## his own jaw with, glimpsed behind the staple bands when the maw hangs open
    ue/Restoration/Source/Restoration/RestorationState.cpp:236: S->RejectedSeen = bRejectedSeen;  S->GlimpseSeen = bGlimpseSeen;
    ue/Restoration/Source/Restoration/RestorationState.cpp:286: bRejectedSeen = S->RejectedSeen;  bGlimpseSeen = S->GlimpseSeen;
    ue/Restoration/Source/Restoration/RestorationState.h:108: UPROPERTY() bool GlimpseSeen = false;                 // 53
    ue/Restoration/Source/Restoration/RestorationState.h:193: bool bGlimpseSeen = false;
UE Source mentions of achievement/presence: none
VERIFY-C14 OK
```

Notes on the output: the "design descriptions found: 21" count is the
§THE LIST rows with a quoted description (A01–A20, A26); A27 and A28 carry
theirs inline in the addendum and were checked by eye (no Chum). The
"forbidden word" hit on #Night is the script's over-broad `sign-off` term
matching the nightly broadcast sign-off, recorded as O12, not a finding. The
`build_chum_af.py` lines are the English verb in comments, not the label.
Fourteen matching lines minus those two is the twelve occurrences of §5.4.
