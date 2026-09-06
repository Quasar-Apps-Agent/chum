# RESTORATION · SOUND MANIFEST (unit C15, cloud lane)

Every sound event the canon names, in one registry: the audio bible's slots
S01–S25, the After-Fire body's sound doctrine, the dread doctrine's audio
amplifiers and bans, the twenty room beds, every caption the reference build
emits, the bell rule in full, the silence ledger consolidated, and a CC0 / Fab
source candidate with its licence for every recordable row. Every rule carries
a citation; where canon is silent the cell says **OPEN** and §9 lists the
ruling needed. Nothing here invents canon, and nothing here is a mix decision:
the manifest is the checklist the audio pass (PHASE 5.1) and the UE port
(MetaSounds + submixes) work from.

Sources read: docs/canon/restoration-chum-motion-and-sound.md (the two bodies,
the audio law), restoration-dread-doctrine.md (stack, amplifiers, bans),
restoration-room-bible.md (twenty "Bed:" lines), restoration-after-fire-chum.md
(SOUND AND CAPTION LAW, THE TWO HIDES, THE LAST CROSSING),
restoration-accessibility-matrix.md (HEARING), restoration-casualty-ledger.md,
restoration-design-doc.md, restoration-controls-map.md (rumble doctrine),
restoration-game-master.md (Appendix A scare compendium, Appendix C segment
audio), restoration-walkthrough-levels-endings.md, restoration-room-inventory.md,
restoration-ambient-lore-ledger.md, restoration-reaction-matrix.md;
docs/production/restoration-audio-bible.md (the slot registry, buses, silence
ledger, addenda), restoration-invariant-suite.md, restoration-qa-regression.md,
restoration-gap-audit.md, restoration-trailer-beats.md,
restoration-achievements-design.md, restoration-accessibility-conformance-pass.md;
docs/packet/portbrief/THE-LAWS.md and UE5-MIGRATION-MAP.md; AAA_BUILD_PLAN.md
§1 and §2; and the reference implementation (scripts/sfx.gd, tone_emitter.gd,
rundown.gd, door.gd, noise_tracker.gd, world_builder.gd, hud.gd, game_state.gd
and every script that calls show_caption), which is the spec for hooks
(PORT-BRIEF via AAA_BUILD_PLAN.md §1: where prose and code disagree, THE CODE IS
THE INTENT).

---

## 0 · CONVENTIONS

### 0.1 Citation codes
| Code | Document |
|---|---|
| MS ¶PRE / ¶AF / ¶LAW / ¶PROD | docs/canon/restoration-chum-motion-and-sound.md, the named section (PRE-FIRE, AFTER-FIRE, THE AUDIO LAW, PRODUCTION NOTES) |
| DD ¶Ln / ¶AMP / ¶TESTS / ¶CURVE / ¶BAN | docs/canon/restoration-dread-doctrine.md (the stack layer, AMPLIFIERS, THE THREE TESTS, THE FIVE-DAY CURVE, ANTI-CREEP) |
| RB ROOM | docs/canon/restoration-room-bible.md, the named room's paragraph, its "Bed:" clause |
| AF ¶SOUND / ¶HIDES / ¶SCALE / ¶CHASE / ¶CROSSING | docs/canon/restoration-after-fire-chum.md, the named section |
| AB §n / AB Snn | docs/production/restoration-audio-bible.md, section n, or slot Snn (§3 and the two addenda) |
| LAWS n | docs/packet/portbrief/THE-LAWS.md, law n |
| ACC ¶HEARING / ¶VISION | docs/canon/restoration-accessibility-matrix.md |
| CL NAME | docs/canon/restoration-casualty-ledger.md, the named character's block |
| DDOC ¶title | docs/canon/restoration-design-doc.md, the named section |
| CM ¶rumble | docs/canon/restoration-controls-map.md, the rumble doctrine line |
| GM Tn.n / GM App A / GM App C | docs/canon/restoration-game-master.md, the scene id or appendix |
| WT ¶title | docs/canon/restoration-walkthrough-levels-endings.md |
| RI ZONE | docs/canon/restoration-room-inventory.md, the zone's table row |
| LL ROOM | docs/canon/restoration-ambient-lore-ledger.md |
| RM | docs/canon/restoration-reaction-matrix.md (queue ids B-R1, B-R2, M-R1) |
| Inn | docs/production/restoration-invariant-suite.md, invariant nn |
| QA-nn | docs/production/restoration-qa-regression.md |
| GAP n | docs/production/restoration-gap-audit.md, ruling n or the named section |
| TB m:ss | docs/production/restoration-trailer-beats.md, the timestamp line |
| ACH | docs/production/restoration-achievements-design.md |
| A11Y-PASS Fnn/Rn | docs/production/restoration-accessibility-conformance-pass.md |
| CS ¶spread | docs/production/restoration-comparative-study.md, the clip-ledger paragraph ("Thirty seconds, one frame legible…") |
| ARG An | docs/production/restoration-arg-plan.md, artifact n |
| PB §n | docs/packet/portbrief/PORT-BRIEF.md, section n |
| MAP ¶AUDIO / ¶HARNESS | docs/packet/portbrief/UE5-MIGRATION-MAP.md, the AUDIO or HARNESS paragraph |
| PLAN §n | AAA_BUILD_PLAN.md |
| file.gd:n | scripts/, the reference implementation, line n at origin/main 38e5c6b |

### 0.2 The bus law (column `bus`)
| Bus (Godot, AB §2) | UE home (MAP ¶AUDIO) | Carries | Law |
|---|---|---|---|
| WORLD | Submix `WORLD` | dry compound: foley, doors, machines, room beds, every After-Fire source | full-range, true room acoustics, floor-coupled sub [MS ¶LAW; AB §1 TWO WORLDS] |
| TAPE | Submix `TAPE` with the format chain; TBC as a submix effect preset | everything heard through the format: tape program audio, in-tape voice, the segment loops' on-tape beds, pre-fire Chum entirely | band-limited, saturated, wowed, hissed, scaled by generation; HP 80 Hz, LP by generation [AB §2 GENERATION CHAIN]; nothing from the tape world may ever sound full-range [AB §1] |
| ARCHIVE VOICE | Submix routed into `TAPE` | in-tape VO recorded through a period chain | [AB §2] |
| UI | Submix `UI` | diegetic paper, pen, binder only; no abstract bleeps | [AB §2; DDOC ¶Philosophy: Two-Layer Diegesis] |
| (master) | Master | pause mutes the whole bus [hud.gd:100; QA-32]; master volume is the only slider [game_state.gd:313] | |

TBC (key T, GameState.tbc_changed) is a real DSP switch on TAPE: flutter depth and dropout rate −70 %, pitch steadied; never removes content, hiss bed or generation bandwidth [AB §2; game_state.gd:511].

Generation ladder (AB §2): G0 60 Hz–12 kHz, hiss −54 dB, 0 dropouts/min, flutter 0.05 % · G1 80–9k, −48, 1/min, 0.1 · G2 80–7k, −42, 4/min, 0.2 · G3 100–5.5k, −36, 10/min, 0.35 + chroma-noise crosstalk. Seance wear rides the same ladder continuously.

### 0.3 The MEMORY / PRESENT column (`law`)
BAND-LIMITED IS MEMORY. FULL-RANGE IS PRESENT [MS ¶LAW]. Every pre-fire sound lives inside the broadcast band forever (≈50 Hz–8 kHz, tape wow, studio slap [MS ¶PRE]); every After-Fire sound lives in true room acoustics [MS ¶AF]. No pre-fire asset may ship full-range, no After-Fire asset may ship band-limited [AB S20–S24 restatement]. The one standing inversion is the throat speaker (PRESENCE wearing MEMORY) and the one spent inversion is the wake bleed S24 (MEMORY stepping into PRESENCE) [MS ¶AF THROAT SPEAKER; MS ¶LAW]. Cells read MEMORY, PRESENT, INVERSION-STANDING, INVERSION-ONCE, or DRY (compound foley that is neither body's: doors, player, machines, per AB §1).

### 0.4 Captions (column `caption`)
Captions exist for speech and for meaningful sound events with source tags [ACC ¶HEARING; DDOC ¶Captions and Accessibility: directional sound captions, because audio carries threat information]. UE extends them with left/right directionality tags and a proximity weight so S22 has a visual twin [ACC ¶HEARING]. Styling law: band-limited sources caption in brackets styled as broadcast, full-range sources caption plain, so the reading ear learns MEMORY versus PRESENT [ACC ¶HEARING]. The reference build brackets every caption (game_state.gd:400 show_caption, gated on captions_on): the styling split is a UE port item, §8. Cells give the caption verbatim as canon or code states it; `none` is a canon statement of silence; OPEN means canon names the event but no caption text exists.

### 0.5 Source candidates and licences (columns `source`, `licence`)
- Policy: freesound.org CC0 and the Sonniss GDC packs for audio [PLAN §2 "Audio later"]; Fab for anything Unreal-side, logged in ue/CREDITS-FAB.md [PLAN §2; ue/FAB-IMPORT.md]; everything gets a credits line, CC0 or Fab-standard licences only, no ripped content [PLAN §2]. Poly Haven and AmbientCG carry no audio.
- Licence codes: **CC0** = Creative Commons Zero (Freesound filter `license:"Creative Commons 0"`; attribution not required but logged anyway per PLAN §2). **SONNISS-GDC** = the Sonniss GDC Game Audio Bundle licence: royalty-free for commercial games, no redistribution of the raw library, attribution not required. **FAB** = Fab Standard Licence, this UE game. **RECORD** = must be recorded in-house; no library asset may stand in (the bell, all voice, the song, anything the bible says "single take").
- **Every source entry is a SEARCH TERM, not an id.** This container's network policy denied freesound.org, sonniss.com, api.polyhaven.com and ambientcg.com (the agent proxy answered 403 to CONNECT on 2026-09-06; see the PR's verification). Ids are read off the site at pull time and logged in tools/audiosrc/CREDITS.md (path proposed; OPEN 9-P1).
- Loudness targets carried from AB §6: dialog anchor −16 LUFS integrated, true peak −1 dBTP, except S06 at −3.

### 0.6 The reference hooks (column `hook`)
The reference build ships five synthesized stand-ins, and the port places MetaSounds graphs exactly where these spawn sites already are [MAP ¶AUDIO; AB §6 "ToneEmitters retire in place"]:
| Stand-in | Where | Spec of the stand-in |
|---|---|---|
| Sfx.bell() | sfx.gd:16; called hud.gd:452 at the finale beat | three inharmonic partials 880/1244/2217 Hz, 2.2 s, −6 dB, captions `[THE BELL RINGS · once]` |
| Sfx.tick() | sfx.gd:21; called game_state.gd:185 on every station signature | 1.6 kHz blip 60 ms, −16 dB, captions `[pen tick]` |
| Sfx.thunk(pos) | sfx.gd:26; called door.gd:48 (every door), rundown.gd:230 and rundown.gd:264 (AF footfalls), rundown.gd:342 (the fold) | 85 + 140 Hz, 160 ms, 3D, −8 dB, max 14 m, captions `[door]` on every call |
| ToneEmitter hum | world_builder.gd:920 `_spawn_room_tones`, at (16.75, 1.6, −6.5), 55 + 110 Hz, −8 dB, reach 26 | the transmitter hall floor |
| ToneEmitter coil | world_builder.gd:848, child of the degausser, 120 + 240 Hz + noise 0.05, −16 dB, reach 10 | S02 |
| ToneEmitter segment | rundown.gd:111, on the hunter, SEGMENT_FREQS 220/262/196 Hz ×1.5, −16 dB, reach 22, active at night only; an empty AudioStreamPlayer3D (max 24 m) reserved for the loops at rundown.gd:108 | S03 |
| Noise attribution | game_state.gd:409 noise(pos, loudness) → noise_event; emitters door.gd:49 (8.0), noise_tracker.gd:19 (player footsteps at night, 6.0 every 0.6 s while moving > 0.5 m/s), game_state.gd:189 (respawn, 4.0) | I22 |

---

## 1 · THE BELL RULE (the box's named rule, in full)

There are four bells in the canon and they must never be confused. The rule is a hierarchy, and the manifest row for each is in §2.

| # | Bell | Sounds? | When | Caption | Canon |
|---|---|---|---|---|---|
| B1 | The stage puppet's collar bell, ON TAPE (pre-fire footage) | YES, often | inside every Gladhouse scene bed, through TAPE at the tape's generation; "the bell answers every gesture", "bright and forward in the mix" | broadcast-bracket style per ACC ¶HEARING; text OPEN 9-B1 | MS ¶PRE; AB S08 ("Chum's bell on tape which is DIFFERENT from S06: small, sweet, frequent") |
| B2 | The After-Fire body's collar bell, IN THE BUILDING | NEVER | never; clapperless by canon; if the model ever swings it, the caption for that is nothing | none, by law | MS ¶AF HARD RULES ("THE BELL NEVER SOUNDS (clapperless by canon; the absence is the tell)"); AF ¶SOUND; DDOC ¶Chum era table ("collar and bell added (silent)"); DDOC ¶post-fire delta 5 ("blackened, still silent"); QA-54 |
| B3 | THE BELL, the finale beat, once per game | ONCE, EVER | the finale beat, Scare 10, "fifty years silent, nine hours silent, and it rings once, three feet behind camera position" | `[THE BELL RINGS · once]` (sfx.gd:17); the caption must say so [LAWS 5]; VISUAL BELL option blooms the screen edge once [ACC ¶HEARING] | LAWS 5; AB S06 (one real brass handbell strike, studio-sized room, single take, never reused anywhere, true peak −3); DD ¶AMP SILENCE AS EVENT; GM T5.4 SCARE 10; GM App A row 10 (blocking A behind camera position, B on the monitor a half-second early, C from the dock direction) |
| B4 | The child's bicycle bell zip-tied to the yard fence, clapper removed | NEVER | a prop; "it rhymes with his" | none (ambient lore never prompts) | LL YARD [T1] |

Consequences the manifest enforces:
- B2 is absolute in the hunt: no footfall, fold, lever, groan or armature row may carry a bell partial [MS ¶AF]. The reference rig ships no bell sound at all outside hud.gd:452 (verified: Sfx.bell has one call site).
- B3 is the whole game's one bell strike and the one Chum-sourced sound on the WORLD bus before the live set that the audio law permits by exception [AB S06; AB §5 "never exist on the WORLD bus until the finale's live set"]. Its physical source is not attributed by any canon text (his collar, a handbell in the studio, or the room itself): OPEN 9-B2.
- "Never reused anywhere" [AB S06] versus the trailer's 1:26 beat, "one real bell strike, the S06 sample, once, and nothing after it" [TB 1:26], and the comparative study's clip ledger naming "the bell" as a clippable [CS ¶spread; PLAN §5.7]: the marketing reuse of the S06 take is a ruling, OPEN 9-B3.
- LAWS 2 (nothing else lunges, stings or pops, in-game or in marketing) governs the bell's placement in the trailer: after black, once, nothing after [TB 1:26] is compliant by construction because it follows silence and is not a lunge.
- The pre-fire bell B1 never leaves the TAPE bus; it is band-limited MEMORY and may not be reused as B3 [MS ¶LAW; AB S08].

---

## 2 · THE MANIFEST

Columns: **id** · **Event** (what happens, in whose body) · **Where / when** · **bus** · **law** (§0.3) · **caption** (§0.4) · **hook** (§0.6) · **Target asset** (the bible's or doctrine's spec) · **source · licence** (§0.5) · **Canon** · **OPEN**.

### 2.1 The audio bible's slots S01–S25 (the registry of record)

| id | Event | Where / when | bus | law | caption | hook | Target asset | source · licence | Canon | OPEN |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 | Transmitter hall bed: 60 Hz mains with transformer chorus and slow amplitude weather; the loudest room in the building by law; audible two rooms out, filtered | TRANSMITTER HALL, always; "mains as organ note" [RB]; masks footsteps in both directions [WT ¶Transmitter hall] | WORLD | DRY | none (bed) | ToneEmitter 55/110 Hz at world_builder.gd:920 | loop ≥ 60 s, 48 kHz 24-bit, seamless; two-rooms-out filtered send | Freesound search `transformer hum 60Hz substation`, `mains hum large transformer` · CC0; Sonniss GDC `electrical hum` · SONNISS-GDC | AB S01; RB TRANSMITTER HALL; WT ¶Transmitter hall | settles a cent flat when ritual holds [RM B-R1; RB CLIMATE web]: pitch-shift parameter, amount OPEN 9-R1 |
| S02 | Degausser coil: whine rises through the wipe, snaps off, magnet-pop tail | the degausser (TAPE LIBRARY per RI LIB "humming coil, felt-lined throat"), on burn_daily | WORLD | DRY | OPEN 9-C1 | ToneEmitter 120/240 Hz + noise at world_builder.gd:848; degausser.gd:14 toast "It hums, felt-throated" | rise 1–2 s, snap, pop tail | Freesound `degausser`, `CRT degauss`, `coil whine rising`, `solenoid snap` · CC0 | AB S02; RI LIB degausser | |
| S03 | Rundown segment loops, three performance loops heard through walls: STORY CORNER page turns and felt movement; THE SONG a music-box bed on tape; CRAFT TIME scissors and paper; each duckable by distance; at three strikes all three fall silent and only "footsteps of nothing" remain (the savoring mix: remove, do not add) | on the hunter at night; segment→room per rundown.gd:9–13: STORY CORNER→TAPE LIBRARY, THE SONG→STUDIO A, CRAFT TIME→PATCH BAY; "the audio tells you which segment, therefore where it is" [WT ¶Rundown] | TAPE for the on-tape beds (music box), WORLD for the felt/paper/scissors foley: split OPEN 9-S3a | MEMORY (the beds) | toast "You can hear it. %s, performed to no one." (rundown.gd:330); caption OPEN 9-C2 | ToneEmitter at rundown.gd:111; empty 3D player rundown.gd:108 | three seamless loops, 3D-attenuated, wall-filtered; a "savor" state that mutes all three [rundown.gd:326 logs " savor" at strikes ≥ 3] | page turns/felt: Freesound `page turn slow`, `felt cloth movement` · CC0; music box: RECORD (it is the closing song's bed; AB §4) or Freesound `music box melody` as a temp only · CC0; scissors/paper: Freesound `scissors cutting paper` · CC0 | AB S03; WT ¶The Rundown; GM T3.5; MS ¶PRE (pre-fire sound is mediated) | GM App C gives the segments SPOKEN lines ("Once there was a house…", "Scissors are for helpers…", the rhyme) while MS ¶AF says NO VOCALIZATIONS EVER and LAWS 5 says Chum speaks nowhere: whether the hunt's segment audio may carry voice is OPEN 9-V1. Canon places CRAFT TIME in "the workshop" [WT; GM App C]; the reference puts it in PATCH BAY: code is the intent, but OPEN 9-S3b records the drift |
| S04 | Door thunks, three classes: standard wood; steel (fire, control); the dead room's felt door, which closes at the loudness of a held breath | every door on toggle; the felt door at the dead room | WORLD | DRY | `[door]` (sfx.gd:27) | Sfx.thunk at door.gd:48; noise 8.0 at door.gd:49 | three one-shots × open/close; felt door near-silent | Freesound `wooden door close heavy`, `steel door slam industrial`, `padded door close soft` · CC0; Sonniss GDC `door` · SONNISS-GDC | AB S04; RB DEAD ROOM (the felt door); QA-38 | which doors are steel is data (ue/Restoration/Data/Doors.csv has no material column): OPEN 9-D1 |
| S05 | Signature tick: pen scratch, three takes rotated, plus one dry page turn | every station signature | UI | DRY | `[pen tick]` (sfx.gd:22); QA-05 requires the pen-tick caption with captions on | Sfx.tick at game_state.gd:185 | 3 pen takes + 1 page turn | Freesound `ballpoint pen writing paper`, `page turn single` · CC0 | AB S05; QA-05; DD ¶L2 (the ritual must actually work) | |
| S06 | THE BELL: one real brass handbell strike recorded in a studio-sized room, single take, never reused anywhere, true peak −3 | the finale beat, once (§1 B3) | WORLD | PRESENT (exception, §1) | `[THE BELL RINGS · once]` | Sfx.bell at hud.gd:452 | one take | RECORD | AB S06; LAWS 5; GM T5.4; TB 1:26 | 9-B2, 9-B3 |
| S07 | Capture transport: reel motor start, a 12 s running bed, stop clunk; abort adds a tape-slap | the bench, every capture (12 s per AF ¶COUNTDOWN "11 seconds of tape" arithmetic) | WORLD (the machine) | DRY | OPEN 9-C3 | capture_bench.gd (no sound hook yet) | start / 12 s bed / stop / abort-slap | Freesound `reel to reel tape start`, `tape deck stop clunk`, `tape slap` · CC0 | AB S07; DDOC ¶Capture (forced real time) | |
| S08 | Tape stage program audio: Gladhouse scene beds (audience murmur, felt movement, Chum's bell on tape, small, sweet, frequent) through TAPE at the stage's generation | every capture and screening; the pre-fire body entirely | TAPE | MEMORY | broadcast-bracket style [ACC ¶HEARING]; texts OPEN 9-B1 | bench_tv.gd (visual only today) | beds per tape at G0–G3 | RECORD (the show is authored); murmur temp Freesound `small audience murmur` · CC0 | AB S08; MS ¶PRE (felted thumps, wooden jaw clop, rod clicks, bell bright and forward, cheerful room tone; the sound STAYS CHEERFUL while the picture wrongs) | |
| S09 | Monitor sync (lockdown): every speaker collapses to one phase-aligned mono frame; the sync moment is a comb-filter bloom, then unified program; exterior seals: two steel thunks, distant, polite | T4.10 LOCKDOWN, everywhere at once | WORLD (speakers as sources) carrying TAPE program | MEMORY through PRESENT speakers | OPEN 9-C4 | GameState.lockdown_done (game_state.gd:51); no sound hook | bloom + program + two thunks | thunks: Freesound `steel door distant slam` · CC0; bloom: DSP, no asset | AB S09; GM T4.10; GM App A row 9 | |
| S10 | Chairs converting: LAW no sound worth naming; a 1 dB room-tone presence dip while they move, nothing else; the absence is the foley | REC ROOM, the armchairs standing in rows | WORLD | DRY | none (toast only: rec_chairs.gd:55 "without a sound worth naming") | rec_chairs.gd:55 | a −1 dB dip automation, no asset | none | AB S10; AB §8; I15 | |
| S11 | The glimpse: LAW no sting; before: nothing; after: one breath of plastic sheeting, close, dry | FIRE CORRIDOR, T4.8, once ever | WORLD | PRESENT | none (LAWS 3: its name appears in no code file; the caption must not name it): OPEN 9-C5 | glimpse.gd (no sound hook) | one plastic-sheeting breath | Freesound `plastic sheet rustle short` · CC0 | AB S11; LAWS 3; ACH §2 (no achievement, ever); I30 | |
| S12 | Floor Manager: LAW never heard moving; no footsteps, no cloth; his only audio is the room refusing to acknowledge him | wherever he stands | — | — | none | floor_manager.gd:4 "Complete spoken inventory: nothing" | no asset; a presence-dip automation only if the mix chair wants one (OPEN 9-F1) | none | AB S12; AB §8; AB §5 (silent, contractually); LAWS 4 (the warm one never acts, including audio) | |
| S13 | Harriet: fabric-and-breath sway loop that hard-stops on break windows and resumes phase-accurate on the return cue; the teacup gains one porcelain tick per day at first touch | GREEN ROOM / REC ROOM, ON AIR only; freezes on BREAK [LAWS 6] | WORLD | DRY | OPEN 9-C6 | harriet.gd (freeze logic; no sound hook) | loop + phase-accurate resume + 1 tick/day | Freesound `fabric rustle breathing loop`, `porcelain cup saucer tick` · CC0 | AB S13; LAWS 6; AB §1 SILENCE IS A BUDGET | H2 doubled Harriet: two loops? OPEN 9-H1 |
| S14 | The hummed bar (night one): a human contralto, unaccompanied, two rooms behind the player, dry, unmediated: the one rationed breach; G2 wording ("here") | Night 1 / the night trip | WORLD | PRESENT (the once-only full-range Gladhouse audio, and it is a human voice) | OPEN 9-C7 (toast: night_trip.gd:27 "Behind you, unhurried: a hummed bar of the closing song.") | night_trip.gd:27 | one take, contralto | RECORD | AB S14; AB §1 ("we author exactly once (the hummed bar, and it is a human voice, not the recording)"); GM T2.7 | AB §1 says night one; the reference fires it in night_trip.gd (Night 4 first blood per GM T2.7): OPEN 9-N1 |
| S15 | Dead room: anechoic treatment; kill reverb sends, raise player breath and cloth, the radio is the only source; Ending 4 is performed into a close dynamic mic sound | DEAD ROOM; "your own blood pressure" [RB]; "hears their own pulse" [RI DR] | WORLD | DRY | `[NO ECHO]` on first entry (hud.gd:171) + radio toast | hud.gd:168–171; GameState.in_dead_room | reverb-kill zone + breath/cloth layer + radio | player breath/cloth: RECORD or Freesound `breathing close quiet`, `clothing rustle close` · CC0; radio: Freesound `AM radio static tuning 1970s` · CC0 | AB S15; RB DEAD ROOM; AF ¶HIDES; QA-38; I25 | |
| S16 | Premiere cues: cue pips through the studio talkback (band-limited squawk), applause card rustle, the little door's latch: small, wooden, final | STUDIO A, T5.3 live | talkback pips: TAPE-style band-limit but a live source: OPEN 9-S16; rustle and latch: WORLD | pips MEMORY-styled; latch PRESENT | OPEN 9-C8 | live_production.gd (no sound hook) | pip set, rustle, latch | Freesound `intercom beep`, `card stock rustle`, `small wooden latch` · CC0 | AB S16; GM T5.3 | |
| S17 | AF FOOTFALL: sub-heavy single hit, wood-through-floor, interval-driven; the current thunk stands in | the hunter's every step: approach interval 1.1 s (rundown.gd:264), crossing interval 0.7 s (rundown.gd:230) | WORLD | PRESENT | canon: `[WEIGHTED FOOTSTEP]`, distance-scaled [AF ¶SOUND]; code today emits `[door]` via Sfx.thunk: drift, §5 row P-1 | rundown.gd:230, :264 | one-shot family, floor-coupled sub, distance-scaled | Freesound `heavy wooden thud floor`, `subwoofer impact wood` · CC0; Sonniss GDC `giant footstep` as layer · SONNISS-GDC | AB S17; MS ¶AF SOUND (sub-heavy wood-through-floor); AF ¶SOUND; MS ¶AF (0.8 m/s approach, 1.6 m/s crossing) | the plinth under each paw is metal in the 1.5 build where canon says wood-through-floor (README ledger, unit 1.5): OPEN 9-P2 |
| S18 | THE FOLD: dry frame creak, 2.2 s envelope, no sting; plus one soft textile drag and a single low wooden knuckle as the head arrives | every doorway, day and night; 2.2 s [LAWS 11; QA-37] | WORLD | PRESENT | `[IT FOLDS THROUGH THE DOORWAY]` (rundown.gd:343); toast when < 12 m (rundown.gd:345) | rundown.gd:337–346 `_door_fold_check` | 2.2 s authored envelope per door width [MS ¶PROD]; rumble ticks twice softly [CM ¶rumble] | Freesound `wood frame creak slow`, `heavy fabric drag`, `wooden knock single low` · CC0 | AB S18; MS ¶AF (shoulder first, head late on a hinge that should not exist); AF ¶SCALE; LAWS 11; QA-37 | |
| S19 | THE CROSSING BED: the sign-off playing through wall filters, phase-drifting by room; his footfalls at doubled cadence layer over it | ENDING 4 DEAD AIR divert, 75 s, MC → the little door | TAPE (sign-off) + WORLD (S17 at 0.7 s) | MEMORY under PRESENT | none beyond S17's; the strike toast rundown.gd:223 | rundown.gd:215–231 | the sign-off program + per-room wall filter + phase drift | RECORD (the sign-off is authored program) | AB S19; AF ¶CROSSING; CL FLOOR MANAGER F1 | |
| S20 | AF WOOL GROAN: wet felt under load, leather-adjacent, pitched down; plays on direction commits, never on stops | the hunter, on each pour's commit | WORLD | PRESENT | OPEN 9-C9 | none (rundown.gd has no commit event; §8 port item) | one-shot family | Freesound `wet leather creak`, `felt stretch`, pitched down · CC0 | AB S20; MS ¶AF SOUND (wet-felt groan under load like leather pitched down) | |
| S21 | AF ARMATURE: deep metal flex, hull-tick spacing; interior only; never servo-whine (he is not a robot) | the hunter, at rest and in motion, from inside the body | WORLD | PRESENT | OPEN 9-C9 | none | sparse tick family, hull spacing | Freesound `ship hull creak tick`, `metal contraction tick` · CC0 | AB S21; MS ¶AF SOUND | |
| S22 | OCCLUSION PRESENCE: under 3 m, reverb sends duck and a 200 Hz bloom rises; the room loses a him-shaped space; the player hears the room lose him before they see him | any time the hunter is < 3 m | WORLD (DSP) | PRESENT | visual twin: caption with directionality + proximity weight [ACC ¶HEARING]; text OPEN 9-C10 | none (distance is computed at rundown.gd:224, :247) | DSP automation, no asset | none | AB S22; MS ¶AF SOUND; ACC ¶HEARING | |
| S23 | REC SYNC HUM: faint mains alignment while the tally burns; performing, he syncs to the plant | the hunter, while GameState.recording and af_active (the tally eye lit, rundown.gd:240) | WORLD | PRESENT | none stated; the eye's hue pairs with the mains hum for colourblind players [ACC ¶VISION]: caption OPEN 9-C11 | rundown.gd:240 (eye light) | S01-derived layer on the body | derived from S01 | AB S23; MS ¶AF SOUND; RB TRANSMITTER HALL web; ACC ¶VISION | |
| S24 | THE WAKE BLEED: the game's first full-range audio emerging from a band-limited source at the fire tape's end; one use, ever | BENCH ROOM, the fire tape capture's last second (fire_tape_dock.gd) | TAPE → WORLD crossfade | INVERSION-ONCE | OPEN 9-C12 | fire_tape_dock.gd (no sound hook) | one authored transition | DSP + RECORD | AB S24; MS ¶LAW; QA-54 (exactly once per save); QA-23 (the fire tape carries no sting: the bleed is not a sting, it is a step down out of the speaker) | |
| S25 | THE LEVER: one dry mechanical click, full-range, close-mic'd intimacy at any distance; on every jaw opening, tally-state and telegraph alike | the performance quote at 1.2 m (rundown.gd:265–269) and the single pre-strike telegraph (0.9 s beat, QA-54; `_strike_pose_t = 0.9` rundown.gd:222) | WORLD | PRESENT | `[THE JAW WORKS ITS LEVER]` (rundown.gd:267) | rundown.gd:267 `_work_jaw` | one click, no distance attenuation | Freesound `mechanical latch click dry`, `lever click metal small` · CC0 | AB S25; MS ¶AF HARD RULES (hand rises, one dry click, the jaw; never syncs to sound, never flaps); AF ¶SOUND; QA-54 | |

### 2.2 Chum's two bodies: events the doctrine names beyond the slots
Ids SM-nn are this manifest's; the audio bible has not slotted them (OPEN 9-S1 asks the audio bible to assign S26+ or fold them into the rows above).

| id | Event | Where / when | bus | law | caption | hook | Target asset | source · licence | Canon | OPEN |
|---|---|---|---|---|---|---|---|---|---|---|
| SM-01 | THE THROAT SPEAKER: a salvaged studio monitor revoiced into the chest; under the tally it breathes band-limited room tone; presence wearing memory, always, quietly; more than room tone is a canon event the author signs first | the performance quote at 1.2 m while the tally burns | WORLD source playing a TAPE-chained bed | INVERSION-STANDING | OPEN 9-C13 | rundown.gd:265 (`_af_seen_once`) | band-limited cheerful room tone loop (the pre-fire studio's, S08's floor) | derived from S08 · RECORD | MS ¶AF THROAT SPEAKER; QA-54 (the one standing inversion); AB S20–S24 restatement | |
| SM-02 | THE STRIKE: nearly silent; one textile sweep, then the authored silence; the loudest thing he ever does is stop making sound; rumble is nothing (death-silence extends to the palms) | strike radius 2.2 m (rundown.gd:24) after the 0.9 s telegraph | WORLD | PRESENT then silence | toast "A hand the size of a door closes the distance. NEXT WEEK'S EPISODE." (rundown.gd:223); caption none by law (OPEN 9-C14 whether the silence itself captions) | rundown.gd:219–224, :285 | one textile sweep; ≥ 1.5 s authored silence before the next toast [AB S17–S19 addendum] | Freesound `heavy cloth sweep whoosh soft` · CC0 | MS ¶AF SOUND; AB S17–S19 addendum (every death scene ends in ≥ 1.5 s authored silence); CM ¶rumble; I01 (warning precedes reach) | |
| SM-03 | THE WITHDRAWAL: he reverses along his exact approach path without turning, motion played backward | tally cools with distance; `_af_cool` rundown.gd:273–279 | WORLD | PRESENT | toast "The tally cools." / the taught 4.0 s "THE TALLY COOLS…" (rundown.gd:275, :279); rumble: a fading pulse [CM ¶rumble] | rundown.gd:273–279 | canon states no sound for the withdrawal itself: S17 at reverse cadence is the honest reading, but it is a ruling | S17 | MS ¶AF (THE WITHDRAWAL); AF ¶CHASE (first cool 4.0 s, every cool after 2.0); CM ¶rumble | sound of the undo: OPEN 9-W1 |
| SM-04 | THE PERFORMANCE QUOTE: fully frontal broadcast stance, one clean 15° head tilt; the jaw hand works its lever open and closed at no rhythm a song would keep; a show with the sound removed, performed at you | 1.2 m under a burning tally | WORLD | PRESENT (S25 clicks) over INVERSION-STANDING (SM-01) | `[THE JAW WORKS ITS LEVER]` per opening | rundown.gd:265–269 | S25 × n + SM-01 bed; NO music, NO voice | as S25, SM-01 | MS ¶AF (THE PERFORMANCE QUOTE, HARD RULES); LAWS 10 | |
| SM-05 | THE EYE: servo-smooth tracking on its own always-on layer; the armature is never servo-whine | always, while parked or pouring | — | — | none | rundown.gd:240 (light only) | canon gives the eye no sound and bans servo-whine on the body: treat as silent | none | MS ¶AF (servo-smooth), MS ¶AF SOUND (never servo-whine), MS ¶PROD | whether the eye has any sound at all: OPEN 9-E1 (default: none) |
| SM-06 | PARKED: statue-still, zero idle sway, no breathing | any stop | — | — | none | rundown.gd:371 `_idle_t` (visual) | no idle bed; S21 hull ticks are the only permitted interior sound at rest | none | MS ¶AF (stops are ABSOLUTE) | |
| SM-07 | Pre-fire stage body at the dock: never animates in-game; L1 drift only; no sound in-game | SCENE DOCK | — | — | none | dock_chum.gd | none | none | MS ¶PRE ("a puppet that moves without a show is a spent card"); RB SCENE DOCK; WT ¶Scene dock (the dock never springs) | |
| SM-08 | The warm one: nothing follows filing it; no system may contradict this, including audio | SCENE DOCK row three, T4.3 | — | — | none | dock_task.gd | none, by law | none | LAWS 4; AB §8 ("the warm unit makes no sound"); GM T4.3 | |
| SM-09 | Pre-fire footage grammar: felted thumps, the soft wooden clop of the jaw a half-beat off the phonemes, rod clicks the club never mentions, the bell bright and forward, cheerful room tone; when footage goes wrong the SOUND STAYS CHEERFUL (audio-visual dissonance is the pre-fire scare, and the only one) | every tape, through TAPE | TAPE | MEMORY | broadcast-bracket | bench_tv.gd | folded into S08's scene beds | RECORD | MS ¶PRE; AB S08 | |
| SM-10 | Chum's in-tape VOICE: warm children's-host falsetto with a chest resonance underneath; dynamic mic, tube pre, tape emulation, then TAPE; never on WORLD until the finale's live set, and there quieter than expected | tapes; T5.3 live | ARCHIVE VOICE → TAPE; live set WORLD | MEMORY; PRESENT at the live set | speaker-tagged captions | hud.gd:418, :463 (text) | sessions per AB §7 | RECORD | AB §5; GM T1.5, T2.8, T5.3–T5.4 | LAWS 5 "Chum speaks nowhere" versus the scripted CHUM (on tape) and CHUM (live) lines: OPEN 9-V1 |
| SM-11 | THE CAPTURE SCARE / Scare 1, the in-tape lunge: a single 33 ms broadband frame, band-limited to TAPE; the game's one startle | T1.5 capture one; every capture per GM App A "fires on every capture" | TAPE | MEMORY | broadcast-bracket; text OPEN 9-C15 | bench_tv.gd (visual) | one 33 ms frame; nothing else in the game may exceed a 6 dB swell; dread swells LFE-lean, one per night | RECORD / DSP | AB §4 STINGER POLICY; LAWS 2; DD ¶L5; I14; GM App A row 1 | GM App A says the capture scare "fires on every capture" while LAWS 2 / I14 say one startle: OPEN 9-V2 (the manifest ships one frame asset either way) |
| SM-12 | The studio speakers wake after fifty years: "a sound like a building clearing its throat"; then YOU'RE ON | T3.5, the return leg | WORLD | PRESENT | OPEN 9-C16 | floor_manager.gd (the point) | one throat-clear of PA/relay/transformer inrush | Freesound `PA system power on hum`, `relay click amplifier inrush` · CC0 | GM T3.5 SCARE 5; WT ¶Tape 3 startle 5 | |

### 2.3 Dread doctrine: audio amplifiers, rituals and bans
| id | Rule or event | Sound consequence | bus / law | caption | hook | Canon |
|---|---|---|---|---|---|---|
| DD-01 | SILENCE AS EVENT: the bell rings once, so silence is the instrument the rest of the time; every death scene ends in authored silence | the mix subtracts before it adds; ≥ 1.5 s authored silence before the next toast after every death; ending 1A closes on 4 s of true digital silence before the title | all | none | live_production.gd `_wait` gaps; hud.gd credits | DD ¶AMP; AB §1; AB §8; AB S17–S19 addendum |
| DD-02 | WARMTH: the kettle's click-off is a death beat | one kettle click, two rooms away, at Merle's M1 | WORLD · DRY | `[THE KETTLE, TWO ROOMS AWAY, CLICKS OFF]` (fire_tape_dock.gd:68) | fire_tape_dock.gd:66–69 | DD ¶AMP; RB KITCHEN web; CL MERLE M1 |
| DD-03 | The kettle never moves again: its stillness is a rundown-audible silence (the hunter lingers there) | KITCHEN's "kettle lifecycle" bed [RB] stops for the rest of the run after M1/M2 | WORLD | none | GameState.is_dead("MERLE") | CL MERLE RIPPLES; RB KITCHEN |
| DD-04 | L1 AMBIENT WRONGNESS: "a hum sits where a hum was not"; drift is monotonic, never called out by text | a drift-eligible hum layer that appears and never resets; no caption ever | WORLD | none, by law | none (§8 port item) | DD ¶L1; PLAN §1 (Object taxonomy: DRESSING is the only drift-eligible tier) |
| DD-05 | L2 RITUAL: the ritual must actually work; kept ritual is a dread economy | S05 pen tick on every signature; doors ease and the hum settles a cent flat when ritual holds | UI / WORLD | `[pen tick]` | game_state.gd:185; RM B-R1 | DD ¶L2; RM B-R1 |
| DD-06 | L3 THE NOTICING GAME: instruments (loupe, gen knob, scope, the audio bench spectrogram) | diegetic UI sounds only; the spectrogram is a deep-dig instrument, images and phrases hide in the actual audio | UI / TAPE | none | gen_knob.gd, bench_tv.gd | DD ¶L3; DDOC ¶Audio bench; AB §4 THE G2 ANOMALY |
| DD-07 | L4 PROXIMITY UNDER CONTRACT: the countdown is visible and the cool is announced | S23 while the tally burns; the cool's toast; rumble fading pulse | WORLD | "THE TALLY COOLS" (toast) | rundown.gd:275, :279 | DD ¶L4; LAWS 10; AF ¶COUNTDOWN; CM ¶rumble |
| DD-08 | L5 THE VIOLATION BUDGET: one startle (SM-11), one interface lie, one once-ever sight (S11) | no second sting exists; no swell over 6 dB | TAPE | — | — | DD ¶L5; AB §4; LAWS 2, 3, 8 |
| DD-09 | BANNED: random scares, musical stings, darkness-as-content, enemy quantity, unreliable narration beyond the one lie, gore for volume, any text containing the word creepy | no stinger asset may exist in the project; no exploration music; no chase music ever; the Rundown is scored by its own loops thinning | — | — | I14 harness grep | DD ¶BAN; AB §4; PLAN §1 Design law |
| DD-10 | THE THREE TESTS gate any new sound: repetition, law, earned | every new asset passes before it ships | — | — | review | DD ¶TESTS |
| DD-11 | THE FIVE-DAY CURVE: Day 1 L2 leads (rituals audible), Day 2 L3 (instruments), Day 3 L2 inverts, Day 4 L4 arrives whole (the wake, S24; the sight, S11), Day 5 all layers, budget empty | which sound families are live per day | — | — | GameState.day | DD ¶CURVE |
| DD-12 | Silence before scripted impact: the authored 1.5–3 s void precedes every set-piece startle; systemic scares use their own tells (segment audio, rising static, the seek call, the seventh signal) | the twelve scripted scares each open with silence; none opens with a sting | — | — | GM App A | GM App A; WT ¶Silence before scripted impact |
| DD-13 | Broadcast grammar: ON AIR and BREAK are two room tones; the whole building breathes on the clock; breaks are negative space (room tone thins, Harriet's loop halts on the exact frame) | every room bed has an ON AIR and a BREAK variant | WORLD | none | Broadcast.phase_changed (rundown.gd:122); QA-10 (ON AIR clock and hum agree) | AB §1 BROADCAST GRAMMAR, SILENCE IS A BUDGET; LAWS 6 |
| DD-14 | MEDIATION IS SAFETY: monitors and the bench always carry the format chain; unmediated show-sound in a hallway is the threat channel, rationed like the glimpse | S14 is the one breach; segment loops through walls are mediated by distance and wall filtering, never full-range Gladhouse program | TAPE / WORLD | — | — | AB §1; MS ¶LAW |
| DD-15 | Matinee Mode "softer audio spikes" [DDOC ¶Difficulty Philosophy] | STRUCK by ruling: difficulty is ASSIST only, one game honestly tuned; no audio-intensity dial exists | — | — | GAP 5 | GAP 5 (rulings bind: PLAN §1 "Consult the gap audit's rulings before re-deciding anything") |

### 2.4 The twenty room beds (the room bible's "Bed:" line, verbatim, with hooks and sources)
Each bed ships as ON AIR and BREAK variants (DD-13). All beds are WORLD / DRY, captionless, unless a row says otherwise.

| Room (unit) | Bed (RB, verbatim) | Hook today | Target | source · licence | OPEN |
|---|---|---|---|---|---|
| ENTRY (3.1) | yard wind under the door, the delivery van's absence | none | wind-under-door loop; "absence" = no engine, ever | Freesound `wind under door draft`, `wind gap whistle low` · CC0 | |
| REC ROOM (3.2) | clock, upholstery quiet, distant kitchen | none; S10 chairs; kitchen smells on habits (RM M-R1) | mantel clock tick loop; distant kettle send from KITCHEN | Freesound `mantel clock ticking room`, `upholstery creak soft` · CC0 | |
| KITCHEN (3.3) | kettle lifecycle, refrigerator sigh | none; DD-02/03 | kettle heat-up / boil / click-off; fridge compressor cycle; the click-off is the death beat | Freesound `electric kettle boil click off`, `refrigerator compressor cycle 1970s` · CC0 | |
| DORMS (3.4) | radiators, one door that settles | none | radiator tick loop; a single door-settle one-shot on a long timer | Freesound `radiator pipe ticking`, `door settle creak` · CC0 | |
| YARD (3.5) | wind, wire hum, gravel | none; guy-wire field "wind audio source; wires hum in the crafted-world register (waxed cord)" [RI EXT] | exterior wind; guy-wire hum (cord, not steel: RI); gravel player-footstep surface | Freesound `wind night exterior`, `wire hum aeolian`, `gravel footsteps` · CC0 | wire hum is "waxed cord" register: sound design ruling OPEN 9-R2 |
| SHED (3.6) | paint cans, wasp-quiet | none | near-silence; a paint-can tick on temperature | Freesound `tin can tick contraction` · CC0 | |
| CORRIDOR (3.7) | your own footsteps returned a half-size large | none (player has no footstep audio; noise_tracker.gd only emits attribution) | player footstep with an early reflection a half-size large; bulbs die per casualty (RM B-R2; lighting, not sound) | RECORD player footsteps on wax-floor; Sonniss GDC `footsteps wood hallway` · SONNISS-GDC | |
| TAPE LIBRARY (3.8) | HVAC breath, ballast tick | none; S02 lives here; rail ladder "creaks on a fixed note" [RI LIB] | HVAC loop; fluorescent ballast tick; ladder creak one-shot on a fixed pitch | Freesound `HVAC air handler room tone`, `fluorescent ballast tick`, `ladder creak` · CC0 | |
| BENCH ROOM (3.9) | machine idle, tape whisper at speed | none; S07 | deck idle loop; tape-at-speed whisper | Freesound `tape machine idle motor`, `tape hiss running reel` · CC0 | |
| CLIMATE (3.10) | the deepest hum, compressor cycles; the hum settles a cent flat when ritual holds (web) | none | sub-heavy compressor loop with a ritual pitch parameter | Freesound `industrial compressor cycle`, `HVAC plant room hum` · CC0 | RM B-R1 amount: 9-R1 |
| TRANSMITTER HALL (3.11) | mains as organ note, contactor clacks | ToneEmitter world_builder.gd:920 (S01) | S01 + contactor one-shots; the hum dies at the dead room door's seam [GM T3.2; RI TH] | S01 sources; Freesound `contactor clack electrical` · CC0 | |
| DEAD ROOM (3.12) | your own blood pressure | hud.gd:168–171 (S15) | S15 treatment | S15 sources | |
| FIRE CORRIDOR (3.13) | nothing; this hall eats sound politely | none | a reverb-poor, dry zone; S11 lives here | none | |
| STAGE HALL (3.14) | studio air pressure, grid creak above | none | pressure loop; occasional grid creak | Freesound `large room air pressure tone`, `wooden beam creak` · CC0 | |
| STUDIO A (3.15) | the largest room tone in the game | none; S16; the plunge (GM App A row 11) | biggest room tone; talkback pips | Freesound `large studio room tone empty` · CC0 | |
| PATCH BAY (3.16) | fan chorus, jack clicks remembered | none; CRAFT TIME loop here per rundown.gd:12 | rack-fan chorus; sparse jack clicks | Freesound `rack fans chorus`, `patch cable jack click` · CC0 | |
| CONTROL (3.17) | relay ticks | none | relay tick loop | Freesound `relay click sparse` · CC0 | |
| MASTER CONTROL (3.18) | sync tone underlay, deck transports | none; S09 fires here (lockdown) | sync tone (band-limited, it is program) + transport one-shots | Freesound `video sync tone`, `VTR transport mechanism` · CC0 | sync tone bus: TAPE-styled? OPEN 9-S16 sibling |
| GREEN ROOM (3.19) | clock older than the building's | none; S13 | second clock, slower and older than REC's | Freesound `antique wall clock tick slow` · CC0 | |
| SCENE DOCK (3.20) | tarp shift, chain hoist idle | none; SM-07/08 (nothing springs, nothing follows) | tarp shift one-shots; hoist chain idle tick | Freesound `tarp plastic shift`, `chain sway idle` · CC0 | |

### 2.5 Player, world foley and attribution
| id | Event | Rule | Hook | Target | source · licence | Canon |
|---|---|---|---|---|---|---|
| W-01 | Player footsteps | the only player sound canon names is the corridor's returned footstep (2.4); at night every 0.6 s of movement > 0.5 m/s emits noise 6.0 to the hunter, byte-identical walking or crouching | noise_tracker.gd:14–19; player.gd:9 | per-surface set (wax floor, concrete, gravel, carpet, stage boards) | RECORD or Sonniss GDC footstep sets · SONNISS-GDC | RB CORRIDOR; I22; QA-58; GAP 2 (crouch has no footstep channel to fool) |
| W-02 | Doors as noise | every door toggle emits noise 8.0 and a thunk; doors held for air refuse silently with a toast | door.gd:40–49 | S04 | S04 | I22; LAWS 6 |
| W-03 | Respawn noise | the retake re-entry emits noise 4.0 at the respawn point | game_state.gd:189 | none (attribution only) | none | I22 |
| W-04 | Noise attribution | every relocation-toward-noise names its cause in coverage_log ("RELOCATE toward heard noise at …"); the toast "It changed direction. You were not quiet." fires once per run | rundown.gd:177–181 | telemetry, no asset | none | I22; QA-13 |
| W-05 | Dead room deafness | noise born inside the dead room never alters his heard-state; he tracks to the felt door and holds; the reference's line there is a narrator toast, not a vocalization | rundown.gd:249–255; game_state.gd:121 | S15 | none | I25; AF ¶HIDES ("says nothing further"); QA-38 ("says his line once": the line is the toast at rundown.gd:255) |
| W-06 | Rumble doctrine | rumble is a caption, not a sting: the fold ticks twice softly, the cool is a fading pulse, the strike is nothing | none (port item) | haptic curves | none | CM ¶rumble |
| W-07 | Pause | audio mutes on pause; refused inside authored sequences | hud.gd:100, :125 | master mute | none | QA-32 |
| W-08 | Degausser interaction | "It hums, felt-throated. It wants a canister." | degausser.gd:14 | S02 | S02 | RI LIB; AB S02 |
| W-09 | Breaker board | "RESTORED. The board hums agreement." | finale_breaker.gd:16 | S01-family hum settle | S01 | RB TRANSMITTER HALL; CL VESS V2 (interlaced with the transmitter hum) |
| W-10 | The little door's latch | small, wooden, final | none | S16 latch | S16 | AB S16; GM ENDING 4 |

### 2.6 Voice (AB §5), for completeness of the registry
| Speaker | Rule | bus | Canon |
|---|---|---|---|
| Rita | minimal lines, breath-first; recorded dry on WORLD; the response pools are the only speech she owns | WORLD | AB §5; GM App C |
| Merle | warm alto, seventies, zero irony; the monologue one unbroken take; M1: her voice finishes the sentence from inside the speaker three seconds after her chair is empty | WORLD; M1's last word through the bench speaker (TAPE) | AB §5; CL MERLE M1; fire_tape_dock.gd:63–66 |
| Vess | fast, precise | WORLD | AB §5 |
| Harriet | transitions only, always mid-cadence; hums the verse with one wrong word ("here") | WORLD; the hummed bar S14 is contralto, dry | AB §5; GM T2.6; AB §4 THE G2 ANOMALY |
| Floor Manager | silent, contractually; never heard moving | — | AB §5; AB S12 |
| Chum / the Understudy | SM-10 | ARCHIVE VOICE → TAPE | AB §5 |
| Leland | never voiced; the legal pad is text; his silence is load-bearing; L2 completes the sign-off "in a reading voice you know from green ink" and 4c's epilogue is "in his voice" | — / RECORD for L2 and 4c | AB §5; CL LELAND L2; seance_dock.gd:113–121 |
| Craik | archival only, optical-track character, 8 mm sound | ARCHIVE VOICE | AB §5 |

Conflict: AB §5 says Leland is never voiced; CL LELAND L2 and ending 4c give him a reading voice. OPEN 9-V3.

### 2.7 Music
| id | Asset | Rule | Canon |
|---|---|---|---|
| M-01 | The closing song: the entire score; master recording pastiche 1971: celesta, nylon guitar, bass clarinet, four-voice children's choir, 76 bpm, F major with a Lydian lift on the third line; two verses, the missing verse, tag | G1–G3 are pure renders of the master through the format chain, no re-performance; RECORD | AB §4 |
| M-02 | THE G2 ANOMALY: identical performance except "home" → "here", same voice off-axis and 15 cents flat, comped invisibly; survives casual listening, rewards spectral listening (the VERSE asset's source) | RECORD; the ARG's A3 audio drop is this G2 print | AB §4; ARG A3; GM T2.6 |
| M-03 | No exploration music, no chase music ever; the Rundown is scored by its loops thinning | no asset | AB §4; DD ¶BAN |
| M-04 | Jingles, the theme, the end-credits piece | UNDOCTRINED per the gap audit; the ledger reading at credits is unscored | GAP ¶ART AND AUDIO GAPS; AB S17–S19 addendum · OPEN 9-M1 |

---

## 3 · THE SILENCE LEDGER, CONSOLIDATED (contracts; violations are S1 bugs)
| # | Contract | Source | Test |
|---|---|---|---|
| SL-01 | The fire tape ends without a sting | AB §8; QA-23; LAWS 2 | asset review + QA-23 |
| SL-02 | The glimpse carries no sting; before nothing, after one plastic breath | AB §8; AB S11; I15 | silence-ledger audit |
| SL-03 | The warm unit makes no sound; nothing follows filing it, including audio | AB §8; LAWS 4 | I15 gate |
| SL-04 | The chairs make no nameable sound (a 1 dB dip only) | AB §8; AB S10; I15 | I15 gate |
| SL-05 | The Floor Manager is never heard moving | AB §8; AB S12; I15 | I15 gate |
| SL-06 | Ending 1A closes on four seconds of true digital silence before the title | AB §8 | capture the credits' first 4 s |
| SL-07 | Every death scene ends in ≥ 1.5 s of authored silence before the next toast | AB S17–S19 addendum | script gaps (live_production.gd `_wait`) |
| SL-08 | The ledger reading at credits is unscored | AB S17–S19 addendum | asset review |
| SL-09 | The After-Fire collar bell never sounds (§1 B2) | MS ¶AF; AF ¶SOUND; QA-54 | grep the AF MetaSound graph for any bell partial |
| SL-10 | The bell rings once, at the finale beat, and its caption says so (§1 B3) | LAWS 5; AB S06 | Sfx.bell has one call site (verified: hud.gd:452) |
| SL-11 | No vocalization exists on the After-Fire body; the throat speaker is not a voice; more than room tone is a signed canon event | MS ¶AF; QA-54 | asset review |
| SL-12 | The strike is nearly silent; the loudest thing he does is stop making sound; rumble nothing | MS ¶AF SOUND; CM ¶rumble | asset review |
| SL-13 | One startle in the whole game (the 33 ms frame); nothing else exceeds a 6 dB swell; dread swells one per night | AB §4; I14; LAWS 2; DD ¶L5 | harness greps the event table per build |
| SL-14 | The wake bleed occurs exactly once per save | QA-54; AB S24 | QA-54 |
| SL-15 | The once-ever moment's name appears in no code file and is referenced by no system, including logs | LAWS 3; I30 | build grep over the casualty files |
| SL-16 | Chum has no presence string, no achievement title, no account; no per-death achievements | LAWS 5; ACH §2; CL ACHIEVEMENTS | I30 |
| SL-17 | Musical stings, exploration music and chase music do not exist | AB §4; DD ¶BAN | asset review |
| SL-18 | Noise inside the dead room registers nowhere | I25; QA-38 | soak: bot signs and slams inside; his target must not move |
| SL-19 | Pause mutes; no audio leaks through the intermission | QA-32 | QA-32 |
| SL-20 | The dock never springs: no sound event is authored in SCENE DOCK beyond its bed | WT ¶The dock contract; GM App A ("The dock never springs") | asset review |

---

## 4 · THE BUS CENSUS (every row's bus, so the submix plan is complete)
| bus | rows |
|---|---|
| WORLD | S01 S02 S04 S06 S07 S09 S10 S11 S13 S14 S15 S17 S18 S20 S21 S22 S23 SM-01 SM-02 SM-03 SM-04 SM-12 DD-02 DD-03 DD-04 all twenty beds W-01 W-02 W-08 W-09 W-10 |
| TAPE | S03 (beds) S08 S19 (program) SM-09 SM-10 SM-11 S24 (source side) M-01 M-02; the MASTER CONTROL sync tone (OPEN) |
| ARCHIVE VOICE | SM-10, Craik |
| UI | S05 DD-06 |
| none by law | S12 SM-05 SM-06 SM-07 SM-08 DD-09 M-03 |

---

## 5 · REFERENCE-BUILD DRIFT FROM CANON (port notes, not rulings)
| # | Drift | Canon | Code | Port action |
|---|---|---|---|---|
| P-1 | The AF footfall and the fold reuse Sfx.thunk and therefore caption `[door]` | `[WEIGHTED FOOTSTEP]`, distance-scaled [AF ¶SOUND] | rundown.gd:230, :264, :342 → sfx.gd:27 | S17 gets its own graph and caption; the fold's thunk becomes S18 and keeps `[IT FOLDS THROUGH THE DOORWAY]` (rundown.gd:343 already emits it, so the fold today double-captions `[door]` + the fold line) |
| P-2 | The reference has no player footstep audio | RB CORRIDOR names the returned footstep | noise_tracker.gd emits attribution only | W-01 |
| P-3 | All captions are bracketed | band-limited in broadcast brackets, full-range plain [ACC ¶HEARING] | game_state.gd:400 | style by bus in the UE caption widget |
| P-4 | CRAFT TIME anchors in PATCH BAY | "the workshop" [WT ¶Rundown; GM App C] | rundown.gd:12 | code is the intent [PLAN §1]; recorded as 9-S3b |
| P-5 | The hummed bar fires on the night trip (first blood) | "night one" [AB S14] | night_trip.gd:27 | 9-N1 |
| P-6 | The throat speaker, S20–S23, S07, S09, S13, S16, the beds: no hooks exist | AB §3, §addenda | none | MetaSounds at the anchors §0.6 names; new events for pour-commit (S20) and proximity (S22) |
| P-7 | The accessibility pass names captions `[BELL RINGS]`, `[DOOR]`, `[PEN]` | A11Y-PASS R2 | shipped as `[THE BELL RINGS · once]`, `[door]`, `[pen tick]` | the shipped strings are canon by PLAN §1 (code is the intent) |
| P-8 | `[door]` is emitted through tr() (sfx.gd:27 via game_state.gd:400) but is in neither translations/strings.csv nor GameText.csv; the other fourteen captions are in both | every significant sound captions [ACC ¶HEARING] and localizes | tools/extract_strings.py does not pick it up | add the key to the string table when S04 gets its graph; the GAMETEXT AUDIT (unit C12) owns the extractor question |

---

## 6 · THE CAPTION REGISTRY (every caption the reference build emits, and every one canon names but code lacks)
| Caption | Emitter | Event | Status |
|---|---|---|---|
| `[THE BELL RINGS · once]` | sfx.gd:17 | S06 | shipped; GameText.csv row |
| `[pen tick]` | sfx.gd:22 | S05 | shipped |
| `[door]` | sfx.gd:27 | S04 (and, by drift P-1, S17/S18) | shipped, but ABSENT from translations/strings.csv and ue/Restoration/Data/GameText.csv although emitted through tr() (P-8) |
| `[THE JAW WORKS ITS LEVER]` | rundown.gd:267 | S25 | shipped; canon text [AF ¶SOUND; AB S25] |
| `[IT FOLDS THROUGH THE DOORWAY]` | rundown.gd:343 | S18 | shipped |
| `[NO ECHO]` | hud.gd:171 | S15 first entry | shipped; canon [AF ¶HIDES; QA-38] |
| `[THE KETTLE, TWO ROOMS AWAY, CLICKS OFF]` | fire_tape_dock.gd:68 | DD-02 | shipped; QA-40 |
| `[MAINS HUM, SHAPED LIKE A STANDING PERSON]` | patchbay_console.gd:92 | V2 (S01 as a body) | shipped |
| `[BARS, ALL MONITORS]` | live_production.gd:96; decision_ledger.gd:62 | V1 (the broadcast-body idiom, LAWS 7) | shipped |
| `[A CHAIR, BETWEEN FRAMES]` | live_production.gd:178 | THE ROWS | shipped; QA-46 |
| `[YOU'RE ON · TO NOTHING LISTED]` | live_production.gd:188 | F2 | shipped |
| `[ONE FRAME LEFT OF HERSELF]` | harriet.gd:105 | H2 | shipped |
| `[A REEL, LABELED IN HER HAND: ME]` | harriet.gd:115 | H1 | shipped |
| `[THE INK LEAVES THE PAPER]` | seance_dock.gd:100 | L1 | shipped |
| `[THE SIGN-OFF, WHOLE]` | seance_dock.gd:119 | L2 | shipped |
| `[WEIGHTED FOOTSTEP]` | none | S17 | canon [AF ¶SOUND], not in code (P-1) |
| the fold "when close, by a line about him bending and keeping his eye on you" | rundown.gd:345 (toast) | S18 | shipped as a toast |
| S22 directional caption with proximity weight | none | S22 | canon [ACC ¶HEARING], UE item |
| the clapperless collar bell | none, by law | B2 | "the caption for that is nothing" [AF ¶SOUND] |

---

## 7 · SOURCE PLAN (what gets recorded, what gets pulled, what is DSP)
| Class | Rows | Note |
|---|---|---|
| RECORD (in-house, no library stand-in permitted) | S06, S08/SM-09 beds, S14, S19 program, S24, SM-01, SM-10, all voice (§2.6), M-01, M-02, W-01 if the Sonniss sets fail the crafted-world register | the bible's "single take", "never reused", "one take" rows and every human voice |
| CC0 pull (freesound.org, filter CC0; log id + author + URL in tools/audiosrc/CREDITS.md) | S01–S05 stand-ins, S07, S09 thunks, S11, S13, S15 radio, S16, S17, S18, S20, S21, S25, SM-02, SM-12, all beds in §2.4 | search terms per row; every pull gets the wear pass equivalent (the format chain or room convolution) and a credits line [PLAN §2] |
| SONNISS-GDC | footstep sets (W-01, S17 layer), doors, electrical hum layers | the pack's licence forbids redistributing the raw files: keep sources out of the repo, ship only processed assets (mirror of the texture policy: only baked results ship) |
| FAB | none required today; if a Fab audio pack is used, log in ue/CREDITS-FAB.md | PLAN §2 |
| DSP, no asset | S10 dip, S22 duck + 200 Hz bloom, S23 (derived from S01), S24 crossfade, the TBC preset, the generation ladder, the dead room reverb kill, the corridor's half-size reflection, the ritual cent-flat | MetaSounds / submix effects [MAP ¶AUDIO] |

Format: 48 kHz 24-bit [AB §7]. Priority inherits AB §7: P0 (demo) S01, S03 ×3, S04 wood + steel, S05, S07, S08 beds, song G0 + G2, the Scare 1 frame, Chum session one, Merle session one · P1 S02, S06, S09, S13, S14, premiere cue set, Vess and Harriet sessions, song G1 + G3 · P2 S15 pass, S16 detail, Craik build, Rita breath library, the felt door. The S17–S25 and SM rows have no bible priority: OPEN 9-S2 (proposed: S17, S18, S25, SM-01, SM-02 at P0 because the After-Fire body is Phase 1's acceptance subject and PLAN §5.1 hangs foley on anim events).

---

## 8 · THE PORT (what UE must carry; MAP ¶AUDIO governs)
- ToneEmitter and the Sfx autoload → MetaSounds graphs (hum, coil, segment tones, bell partials, thunk, tick) placed exactly where the spawn sites already are [MAP ¶AUDIO; §0.6]; Sfx → a GameInstance Subsystem with the same function names [PB §3].
- Buses → Submixes with the same names; TBC → a submix effect preset toggled by the same tbc_changed delegate [MAP ¶AUDIO; AB §6].
- New events the reference lacks and canon requires: pour-commit (S20), proximity < 3 m (S22), tally-lit (S23, exists as the eye light), the wake bleed (S24), the throat speaker under the tally (SM-01), the performance-quote lever loop (S25 × n), per-door material class (S04, 9-D1), ON AIR / BREAK bed variants (DD-13), per-day sound-family gates (DD-11).
- Captions: keep every string in §6 byte-identical (GameText.csv is the source of record); add directionality + proximity tags; style by bus (P-3).
- Harness: the silence ledger §3 becomes asset-review gates and I14/I15/I25/I30 Gauntlet steps reading the same log formats [MAP ¶HARNESS; PLAN §1 WHAT MUST NOT CHANGE].
- Rumble curves per W-06.

---

## 9 · OPEN RULINGS (canon is silent or contradicts itself; nothing here is decided)
| id | Question | Where it bites |
|---|---|---|
| 9-B1 | Caption text for the on-tape bell and the Gladhouse scene beds (broadcast-bracket style is law; the words are not) | S08, B1 |
| 9-B2 | The physical source of the once-ever finale strike (his collar, a handbell, the room) | S06, B3 |
| 9-B3 | "Never reused anywhere" [AB S06] versus the trailer's use of "the S06 sample" [TB 1:26] and the clip ledger's "the bell" [CS; PLAN §5.7] | marketing |
| 9-C1…C16 | Caption texts for S02, S03, S07, S09, S11 (must not name the once-ever moment: LAWS 3), S13, S14, S16, S20/S21, S22, S23, S24, SM-01, SM-02 (whether silence captions), SM-11, SM-12 | §2 |
| 9-D1 | Which doors are steel and which wood (Doors.csv has no material column); the felt door is fixed | S04 |
| 9-E1 | Whether the tally eye's servo tracking has any sound (default: none; "never servo-whine") | SM-05 |
| 9-F1 | Whether the Floor Manager gets a presence-dip automation like the chairs, or true nothing | S12 |
| 9-H1 | H2's doubled Harriet: one sway loop or two, phase-offset | S13 |
| 9-M1 | Jingles, theme, end-credits piece: undoctrined | §2.7 |
| 9-N1 | The hummed bar: "night one" [AB S14] versus the reference's night-trip firing | S14 |
| 9-P1 | Where audio sources and credits live in the repo (proposed tools/audiosrc/CREDITS.md, mirroring tools/texsrc) | §0.5 |
| 9-P2 | The 1.5 build's metal plinths versus the wood-through-floor footfall canon (already OPEN for the owner in the README ledger) | S17 |
| 9-R1 | The ritual-kept hum "a cent flat": amount, rooms (CLIMATE, TRANSMITTER HALL), and whether it persists | S01, CLIMATE bed |
| 9-R2 | The guy-wire hum in the "waxed cord" register: what a waxed-cord aeolian hum sounds like is a design call | YARD bed |
| 9-S1 | The audio bible should assign slot numbers (S26+) to SM-01, SM-02, SM-03, SM-11, SM-12 or fold them | §2.2 |
| 9-S2 | Priorities for S17–S25 and the SM rows (none in AB §7) | §7 |
| 9-S3a | Segment loops: which layers ride TAPE (the music-box bed) and which ride WORLD (felt, paper, scissors heard through walls) | S03 |
| 9-S3b | CRAFT TIME's room: "the workshop" (canon) versus PATCH BAY (code) | S03 |
| 9-S16 | Talkback pips and the MASTER CONTROL sync tone: live sources that are band-limited by nature; TAPE-styled captions or plain | S16, MASTER CONTROL bed |
| 9-V1 | LAWS 5 "Chum speaks nowhere" versus the scripted CHUM (on tape) and CHUM (live) lines [GM] and the Rundown's spoken segment lines [GM App C] against MS ¶AF NO VOCALIZATIONS; the manifest ships the hunt's S03 as foley-only until ruled | S03, SM-10 |
| 9-V2 | GM App A "the capture scare fires on every capture" versus LAWS 2 / I14 one startle | SM-11 |
| 9-V3 | Leland "never voiced" [AB §5] versus L2's reading voice and 4c's epilogue "in his voice" [CL LELAND] | §2.6 |
| 9-W1 | The withdrawal's sound (motion played backward: reversed S17 cadence, or silence) | SM-03 |

---

## 10 · VERIFICATION (what was checked, and how)
Checked by a scratchpad script against origin/main 38e5c6b (output in the PR body):
1. every show_caption string in scripts/*.gd appears verbatim in §6 and in GameText.csv;
2. every Sfx.* and ToneEmitter call site in scripts/ is cited in §0.6 with its line;
3. S01–S25 each have exactly one row in §2.1 and no slot is skipped;
4. every row in §2.x carries a Canon cell that is non-empty and every citation code used is defined in §0.1;
5. all twenty room-bible rooms appear in §2.4 with the bible's "Bed:" text verbatim;
6. the eleven laws that touch sound (2, 3, 4, 5, 6, 10, 11) are each cited at least once;
7. the word the dread doctrine bans does not appear in this file outside the ban's own row;
8. every OPEN id referenced in §2–§7 is defined in §9 and vice versa;
9. Sfx.bell() has exactly one call site (SL-10).
Not verifiable here: any freesound / Sonniss id (network denied, §0.5); anything that needs an ear (no audio exists yet: GAP headline "THE ASSETS ARE ZERO").
