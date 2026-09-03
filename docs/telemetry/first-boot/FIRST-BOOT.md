# RESTORATION · FIRST BOOT REPORT
Date of record: sixty-five sessions and forty-four commits after the first line was written, the project executed for the first time, inside the build environment itself, on Godot v4.3.stable.official (headless, Linux x86_64).

## WHAT HAPPENED
IMPORT, ROUND ONE: fifteen error lines across five scripts. All were real, all were legible, none were architectural: one duplicate _process in harriet_note.gd (two sessions had each added a visibility gate), and four strict type-inference failures the offline parser never enforced (px/py in the map's draw loop, ti in the invariant parser, plus two cascades that cleared themselves). ROUND TWO: zero errors. Every script in the project compiles under the real engine.

EXECUTION: two one-minute soak runs, wanderer and checker bots. ZERO script errors at runtime in both. The world built all twenty rooms from data, the autoload chain came up in order, the schedule ran, the hunter relocated on its coverage read (the log's second line: RELOCATE sprinter-bias, written by the director watching a bot), the checker signed a station and its pen tick was heard and attributed (I22: one attribution, correctly), and the invariant parser graded its own game: I01 warn-precedes-strike PASS, I02 no-strike-thru-wall PASS, I22 heard-noise-attribution PASS. I06 and I07 correctly reported N/A, since no bot reached a cascade or the finale in sixty seconds.

THE SAVE: transmitter_log.json exists, version 16, fifty-five fields, and the deep systems are all present in it on day one: paper at full, casualties empty, read_props empty, af_active false. The save schema built blind across forty-four commits serializes correctly on first contact with reality.

## HONEST SCOPE
Headless proves logic, not experience. Untested here: rendering (the CRT shader, the wool, the eye's glow), audio audibility, input feel, and every SubViewport surface (monitors, the spectrogram). The one warning, ObjectDB instances leaked at exit, is the hard-quit path not freeing the world; benign for soaks, worth a teardown pass before shipping builds. Longer soaks (the four-hour runs) remain queued for target hardware, as does everything the device pass owns.

## THE SENTENCE THAT MATTERS
The game is no longer code that should work. It is a program that ran, played itself for two minutes, obeyed its own laws, and filed the paperwork to prove it.
