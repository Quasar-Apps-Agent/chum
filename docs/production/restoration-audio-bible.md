# RESTORATION · AUDIO BIBLE v1
Scope: full sound direction for production, mapped to the v0.5 prototype's existing hooks so the sound pass is a checklist, not a vibe. Companion to the design doc and build plan.

## 1 · DOCTRINE
TWO WORLDS. The compound is acoustically honest: dry, close, wood and concrete, real distances. The tape world is heard only through the format: band-limited, saturated, wowed, hissed, scaled by generation. Nothing from the tape world may ever sound full-range. If the player hears full-range Gladhouse audio, something has come through, and that is an event we author exactly once (the hummed bar, and it is a human voice, not the recording).
MEDIATION IS SAFETY. The safety rule must be audible: mediated sound is survivable sound. Monitors and the bench always carry the format chain. Unmediated show-sound in a hallway is the threat channel and is rationed like the glimpse.
SILENCE IS A BUDGET. Breaks are negative space: room tone thins, Harriet's fabric loop halts on the exact frame. The forced fire-tape watch contains no sting by law. Dread is subtraction before it is ever addition.
BROADCAST GRAMMAR. ON AIR and BREAK are two room tones, not one. The whole building breathes on the clock.

## 2 · MIX ARCHITECTURE (Godot buses)
MASTER > WORLD (dry compound: foley, doors, machines) · TAPE (format chain: HP 80 Hz, LP by generation, tape saturation, wow and flutter, hiss bed, dropout gates) · ARCHIVE VOICE (in-tape VO recorded through a period chain, then routed into TAPE) · UI (diegetic paper, pen, binder only; no abstract bleeps).
TBC (key T) is a real DSP switch on the TAPE bus: reduces flutter depth and dropout rate by 70 percent, steadies pitch. It never removes content, hiss bed, or the generation bandwidth. Accessibility and fiction share one switch.
GENERATION CHAIN: G0 master 60 Hz to 12 kHz, hiss -54 dB, dropouts 0/min, flutter 0.05 percent. G1 dub 80 to 9k, -48, 1/min, 0.1. G2 80 to 7k, -42, 4/min, 0.2. G3 100 to 5.5k, -36, 10/min, 0.35 plus chroma-noise crosstalk bleed. Seance wear rides this same ladder continuously.

## 3 · SLOT INVENTORY (current stub, target, law)
S01 Transmitter hall bed. Now: 55/110 sines. Target: 60 Hz mains with transformer chorus and slow amplitude weather; loudest room in the building by law; audible two rooms out, filtered.
S02 Degausser coil. Now: 120/240 plus noise. Target: coil whine that rises through the wipe, snaps off; a magnet-pop tail.
S03 Rundown segment loops. Now: three sine tones. Target: three performance loops heard through walls: STORY CORNER page turns and felt movement; THE SONG a music-box bed on tape; CRAFT TIME scissors and paper. Each duckable by distance; at three strikes all three fall silent and only footsteps of nothing remain (the savoring mix: remove, do not add).
S04 Door thunks. Now: synth 85 Hz. Target: three door classes: standard wood, steel (fire, control), and the dead room's felt door, which closes at the loudness of a held breath.
S05 Signature tick. Now: 1.6 kHz blip. Target: pen scratch, three takes rotated, plus one dry page turn.
S06 THE BELL. Now: synth partials at the finale beat. Target: one real brass handbell strike recorded in a studio-sized room, single take, never reused anywhere, true peak allowed to -3. Fifty years of silence buys one strike.
S07 Capture transport. Target: reel motor start, a 12 second running bed, stop clunk; abort adds a tape-slap.
S08 Tape stage program audio. Target: the Gladhouse scene beds (audience murmur, felt movement, Chum's bell on tape which is DIFFERENT from S06: small, sweet, frequent) through the TAPE bus at the stage's generation.
S09 Monitor sync (lockdown). Target: every speaker in the compound collapses to one phase-aligned mono frame; the moment of sync is a comb-filter bloom, then unified program. Exterior seals: two steel thunks, distant, polite.
S10 Chairs converting. LAW: no sound worth naming. Implementation: a 1 dB room-tone presence dip while they move, nothing else. The absence is the foley.
S11 The glimpse. LAW: no sting. Before: nothing. After: one breath of plastic sheeting, close, dry.
S12 Floor Manager. LAW: never heard moving. No footsteps, no cloth. His only audio is the room refusing to acknowledge him.
S13 Harriet. A gentle fabric-and-breath sway loop that hard-stops on break windows and resumes phase-accurate on the return cue; the teacup gains a single porcelain tick per day at first touch.
S14 The hummed bar (night one). A human contralto, unaccompanied, two rooms behind the player, dry (unmediated: this is the one rationed breach). G2 wording.
S15 Dead room. Anechoic treatment: kill reverb sends, raise player breath and cloth, the radio is the only source; Ending 4 is performed into a close dynamic mic sound.
S16 Premiere cues. Cue pips through the studio talkback (band-limited squawk), applause card rustle, the little door's latch: small, wooden, final.

## 4 · MUSIC
The closing song is the entire score. Master recording pastiche, 1971: celesta, nylon guitar, bass clarinet, four-voice children's choir, 76 bpm, F major with a Lydian lift on the third line. Structure: two verses, the missing verse, tag. Generations G1 to G3 as pure renders of the master through the format chain, no re-performance.
THE G2 ANOMALY: identical performance except one word, where "home" becomes "here," recorded by the same voice slightly off-axis and 15 cents flat, comped invisibly. The wrongness must survive casual listening and reward spectral listening (this is the VERSE asset's source).
STINGER POLICY: one startle in the whole game: the Scare 1 lunge is a single 33 ms broadband frame, band-limited to the TAPE bus. Nothing else in the game may exceed a 6 dB swell. Dread swells are LFE-lean and rationed to one per night.
No exploration music. No chase music ever; the Rundown is scored by its own segment loops thinning.

## 5 · VOICE
Rita: minimal lines, breath-first acting; recorded dry on the WORLD bus.
Merle: warm alto, seventies, zero irony available; the monologue is one unbroken take if it kills us.
Vess: fast, precise, a man narrating to keep his hands steady.
Harriet: transitions only, always mid-cadence, as if resuming.
Floor Manager: silent, contractually.
Chum / the Understudy: double-voice: warm children's-host falsetto with a chest resonance underneath that the period chain cannot quite hide; ALL Chum lines recorded through dynamic mic, tube pre, tape emulation, then the TAPE bus. He must never exist on the WORLD bus until the finale's live set, and there he is quieter than expected, which is worse.
Leland: never voiced. The legal pad is text by canon; his silence is load-bearing.
Craik: archival only, optical-track character, 8 mm sound.

## 6 · GODOT IMPLEMENTATION NOTES
Buses in project settings as named in Section 2. TAPE chain: AudioEffectEQ, AudioEffectDistortion (tape mode low drive), AudioEffectChorus at 0.15 Hz shallow for wow (approximation, revisit with a flutter plugin at M3), AudioEffectCompressor glue. TBC toggles a second preset via the existing GameState.tbc_changed signal. The Sfx autoload becomes the one-shot registry: swap synth streams for samples slot by slot, keeping function names, so no call sites change. ToneEmitters retire in place: each _spawn site is already positioned where its sample bed belongs. Loudness: dialog anchor -16 LUFS integrated, true peak -1 except S06 at -3.

## 7 · ASSET LIST v1 (48 kHz 24 bit; P0 = demo cut)
P0: S01, S03 all three loops, S04 wood and steel, S05, S07, S08 beds, closing song G0 and G2, Scare 1 frame, Chum session one (Tape 1 lines), Merle session one.
P1: S02, S06 the bell, S09, S13, S14, premiere cue set, Vess and Harriet sessions, song G1 G3.
P2: S15 treatment pass, S16 detail set, Craik archival build, Rita breath library, felt door.

## 8 · THE SILENCE LEDGER (contracts; violations are S1 bugs)
Fire tape ends without a sting. The glimpse carries no sting. The warm unit makes no sound. The chairs make no nameable sound. The Floor Manager is never heard moving. Ending 1A closes on four seconds of true digital silence before the title.

## ADDENDUM · SLOTS S17-S19 (c043)
S17 AF FOOTFALL: sub-heavy single hit, wood-through-floor, interval-driven; the current thunk stands in. S18 THE FOLD: dry frame creak, 2.2 s envelope, no sting. S19 THE CROSSING BED: the sign-off playing through wall filters, phase-drifting by room; his footfalls at doubled cadence layer over it. Silence ledger extension: every death scene ends in at least 1.5 s of authored silence before the next toast; the ledger reading at credits is unscored.
