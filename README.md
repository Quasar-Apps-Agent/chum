# RESTORATION · Godot Prototype v0.7 · Commit 024 · THE CLUB IS HELPING
## The engine's from-here debt list is now EMPTY.

## Run it
Godot 4.3+ · Import · F5.

## New in 024 · systemic sabotage
The premiere now carries continuous pressure. After the cold open, a
sabotage loop rolls incidents from a table: tally lights that lie about
program, house lights dropping to a murmured apology, the boom drifting
into frame, cue cards shuffling themselves. One incident at a time, each
announced, each with a fixture that fixes it (aux panel, boom winch, card
stand), and each escalating: failed takes shorten the interval between
incidents. Fail-forward is guaranteed three ways: the tally caps at two
refusals then lets you call it blind, the boom holds exactly one press,
and any incident older than 40 seconds is fixed by the club themselves,
apologizing. Every incident and resolution logs to user://premiere_log.txt
with timings, which is the soak harness's food.

## Standing
Twenty-four commits, 71 files. Everything the spike briefs marked
"owner: from here" is retired. What remains is hardware-bound (Spike 2),
asset-bound (footage, audio, VO, scans), tuning-bound (your verdicts), or
lives in the document queue. The zip owes nothing it can pay from here.

## Commit 025 · THE HARNESS (the zip tests itself)
The invariant suite's machine-side plan now ships in the box:
- scenes/soak.tscn + soak_runner.gd: headless soak entry.
  godot --headless res://scenes/soak.tscn -- --bot=wanderer --minutes=240
- Bots: wanderer (random legal movement, feeds I01/I02/I22), checker
  (monitor camping, feeds the Director), fail (seeds a PERFORM premiere,
  ignores every incident for two minutes, then stands the mark; feeds I06).
- Telemetry upgrade: the Rundown now logs WARN and STRIKE with segment,
  distance, savor flag, and a wall raycast at strike time (THRU-WALL flags),
  making I01 and I02 machine-checkable instead of aspirational.
- InvariantParser reads coverage, liveness, and premiere logs and writes
  user://INVARIANTS.txt, the per-build scorecard the milestone gates staple.

## Commit 027 · DEMO MODE (the cut plan's E1-E10, in the box)
Flip one line for the Tape 1 free demo: const DEMO := true in
scripts/game_state.gd. Demo build: Day 1 only (the bed declines), paper at
S1 and S5, every door past the library sealed with in-fiction reasons, no
Rundown, nights, dock, crate, seance, assets, or ledger. Capture completion
plays the end sequence: the sign lights alone, the protected card, any key
to title. The save writer whitelists under DEMO: it cannot write decision,
assets, answers, or ending fields. Local demo funnel at
user://demo_funnel.txt (disclosed here, never networked).

## Commit 028 · THE BOOTH (options)
O in game, or OPTIONS at the title: master volume, mouse sensitivity,
fullscreen, and the two access switches (TBC, photo-safe) in one panel.
Settings persist in user://settings.cfg, deliberately apart from the
transmitter log, so NEW GAME never resets your hands or your ears. The
loader guards headless mode so the soak harness stays indifferent.

## Commit 029 · ACCESS (remediation R1-R3 from the conformance pass)
UI TEXT SIZE and CAPTIONS join the booth. Every HUD label now carries a
black outline (dynamic-background contrast) and scales live from a cached
base size. The bell, doors, and pen announce themselves in text when
captions are on. The conformance pass lives at
docs/production/restoration-accessibility-conformance-pass.md and, per its
own methodology, still describes commit 028 until a device retest.

## Commit 030 · FILED (achievements)
The design doc's autoload, live: idempotent unlocks to
user://achievements.cfg, a Steam-ready unlock signal, and the DEFERRAL RULE
in code: nothing surfaces during play; the queue flushes only at the
morning toast (FILED · ...) or the title screen (FILED WHILE YOU WERE
OUT). Twenty-five of twenty-six wired to existing state; FULL ACCESSION
waits on prop read-flags. Disabled entirely under DEMO. The build check
that forbids the once-ever moment's name in this file caught its author's
own comment on the first run, which is exactly what it is for.

## Commit 031 · ACCESS WAVE TWO (R4-R7)
Focus rings everywhere focus goes. One ASSIST switch, three mercies:
wider beats, slower premiere clocks, hold E to be still. First run opens
the booth before the show. And REMAP: click an action, press a key; five
actions, conflict-refused, persisted. Residue named: prompts still print
letters, pending the glyph pass shared with localization.

## Commit 032 · THE EXTRACTION (localization L01)
tr() at the four chokepoints plus the booth, source-strings-as-keys:
byte-identical behavior until a locale column fills. tools/extract_strings.py
regenerates translations/strings.csv on demand, preserving prior
translations by key. Percent-templates are the counted residue: translate
the template, keep the placeholders.

## Commit 033 · FULL ACCESSION (the ledger closes)
The props packet's four missing documents are now physical readables (the
1974 clipping behind shrine glass, the welcome packet at the dorms, the
marshal report in control from Day 2, Iris Bell's letter in the dock after
filing), and six existing interactions mark their documents, so all ten
carry read-flags and A26 is live at 10 of 10. The glyph layer renders bound
keys for the five remappable actions at every text surface. Save v16.

## Commit 034 · INTERMISSION AND SIGN-OFF (past-zero, elective)
Escape now pauses: the world and its clocks hold, audio mutes, and the
intermission offers RESUME, THE BOOTH, or RETURN TO TITLE, refused only
mid-sequence. Endings roll a real credits crawl (CHUM, as himself; the
Floor Manager uncredited by request; the ending you reached, named), also
reachable from the title. Deaths and the demo still cut straight to title,
as they should. Edit the byline card in scripts/credits.gd.
