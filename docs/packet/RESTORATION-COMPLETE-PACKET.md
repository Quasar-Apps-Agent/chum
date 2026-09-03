RESTORATION · THE COMPLETE DOCUMENT PACKET
WGLD Channel 58 · Preserve. Rewind. Remember.
Assembled from the living build: 47 commits, first boot verified, all canon current.

CONTENTS

01 · THE LAWS AND THE PORT BRIEF
   01 · THE-LAWS.md
   02 · PORT-BRIEF.md
   03 · BUILD-ORDER.md
   04 · UE5-MIGRATION-MAP.md

02 · CANON: THE WORLD AND THE CAST
   05 · restoration-cast-sheets.md
   06 · restoration-after-fire-chum.md
   07 · restoration-chum-motion-and-sound.md
   08 · restoration-casualty-ledger.md
   09 · restoration-reaction-matrix.md

03 · CANON: THE BUILDING
   10 · restoration-room-bible.md
   11 · restoration-ambient-lore-ledger.md
   12 · restoration-object-taxonomy.md

04 · DOCTRINE: HOW IT IS MADE
   13 · restoration-dread-doctrine.md
   14 · restoration-lore-architecture.md
   15 · restoration-lighting-bible.md
   16 · restoration-comparative-study.md

05 · DESIGN AND SYSTEMS
   17 · restoration-walkthrough-levels-endings.md
   18 · restoration-player-routing.md
   19 · restoration-controls-map.md
   20 · restoration-accessibility-matrix.md
   21 · restoration-achievements-design.md
   22 · restoration-audio-bible.md

06 · PRODUCTION AND PIPELINE
   23 · restoration-gap-audit.md
   24 · restoration-blender-ue5-pipeline.md
   25 · restoration-gate-0-packet.md
   26 · restoration-playtest-protocol.md

07 · QA AND VERIFICATION
   27 · restoration-qa-regression.md
   28 · restoration-invariant-suite.md
   29 · FIRST-BOOT.md

08 · MARKETING AND PRESS
   30 · restoration-steam-page-draft.md
   31 · restoration-trailer-beats.md
   32 · restoration-key-art-brief.md
   33 · factsheet.md
   34 · quotes.md

09 · ADDITIONAL DOCUMENTS
   35 · full-plotlines-anatomy-restoration.md
   36 · restoration-design-doc.md
   37 · restoration-game-master.md
   38 · restoration-player-routing.md
   39 · restoration-room-inventory.md
   40 · restoration-walkthrough-levels-endings.md
   41 · restoration-accessibility-conformance-pass.md
   42 · restoration-arg-plan.md
   43 · restoration-art-bible.md
   44 · restoration-build-plan.md
   45 · restoration-demo-cut-plan.md
   46 · restoration-localization-plan.md
   47 · restoration-merle-casting-breakdown.md
   48 · restoration-props-packet.md
   49 · restoration-puppet-fabrication-brief.md
   50 · restoration-spike-briefs.md
   51 · restoration-steam-presence.md

APPENDIX A · THE COMMIT NARRATIVE
   52 · README.md

APPENDIX B · THE BUILD LOG
   53 · BUILD-LOG.md

==============================================================================
SECTION 01 · THE LAWS AND THE PORT BRIEF
==============================================================================


------------------------------------------------------------------------------
DOCUMENT 01 · THE-LAWS.md
------------------------------------------------------------------------------

# THE LAWS (inviolable in any engine)
1. ON CAMERA IS SAFE. An active camera cone prevents the strike, always.
2. ONE STARTLE. The in-tape lunge is the game's single jump scare. Nothing else lunges, stings, or pops, in-game or in marketing.
3. ONCE, EVER. The Day 4 fire-corridor moment occurs at most once per save and is never referenced again by any system, including achievements, presence, and logs. Its name appears in no code file.
4. THE WARM ONE NEVER ACTS. On camera, off camera, in any ending. Nothing follows filing it. No system may contradict this, including audio.
5. SILENCE CONTRACTS. The bell rings once, at the finale beat, and its caption says so. Chum's bell is otherwise silent; Chum speaks nowhere; Chum has no account, no achievement title, no presence string.
6. THE SCHEDULE IS REAL. ON AIR and BREAK govern behavior mechanically; Harriet freezes on breaks; window holds bind except during cascade.
7. EVERY DEATH HAS A SIGNATURE. No one dies by chance; every death, including run death, traces to a nameable choice of Rita's, and the binder names it. Horror license is open; the house idiom is the broadcast-body (splice, interlace, dropout, leader where a voice was). See docs/canon/restoration-casualty-ledger.md.
8. THE INTERFACE MAY LIE EXACTLY ONCE, where the design doc says it does, and nowhere else.
9. ACCESS IS CANON. The booth, captions, assist, remap, pause, and the deferral rule ship in every build of every engine.
10. THE TALLY CONTRACT. While a capture runs, the player is on camera: he may approach to 1.2 m and may not strike; the countdown is visible and means both progress and expiry; the cool is 2.0 s and announced. The eye's light and the contract are the same fact.
11. THE TWO HIDES. The safe hide is the lit one (camera cones). The single dark hide is the dead room, which eats sound; he holds at its felt door. He does not fit through doors: every threshold costs him 2.2 s, and that toll is the player's counterplay.


------------------------------------------------------------------------------
DOCUMENT 02 · PORT-BRIEF.md
------------------------------------------------------------------------------

# RESTORATION · UE5 PORT BRIEF
For whoever performs the port: you, a contractor, or a coding agent. Read this file first, then follow its reading order. Be clear-eyed about what this kit is: NO GAME LOGIC HAS BEEN PORTED. What you hold is (a) a UE5 project that opens today, (b) the game's data in Unreal-native formats, (c) a script that erects the walkable compound in one command, and (d) the complete Godot source and document library as the reference the rebuild is performed against. The Godot build is the specification; where prose and code disagree, the code is the intent.

## 0 · FIRST TEN MINUTES
1. Open Restoration.uproject in UE 5.4 or later (Blueprint-only, no compile).
2. File > New Level > Basic. Delete the floor.
3. Tools > Execute Python Script > Scripts/build_greybox.py.
4. Save the level as /Game/Greybox, uncomment the two map lines in Config/DefaultEngine.ini, press Play, and walk WGLD. Input already matches the Godot build (WASD, mouse, E, SPACE).

## 1 · READING ORDER
This file → THE-LAWS.md (one page, inviolable) → BUILD-ORDER.md → Reference/docs/unreal-5/UE5-MIGRATION-MAP.md (system-by-system homes) → Reference/docs/INDEX.md for everything else. The GDScript in Reference/gdscript reads as exact pseudocode; every constant in it is canon and most are also in Data/Timings.csv.

## 2 · SPIKE 2 BEFORE ANYTHING (the reason UE5 is being tested)
The one technical question Godot has not answered on hardware: twelve simultaneous video feeds at 60 fps (the monitor wall). In UE5: twelve SceneCapture2D components into twelve RenderTargets on twelve unlit material planes, capture_every_frame on, profile with stat unit on the target machine. Pass line per the build plan: sustained 60 with headroom. Run this in week one; it is most of the engine memo's evidence.

## 3 · THE SHAPE OF THE PORT (see BUILD-ORDER.md for milestones)
Autoload singletons become GameInstance Subsystems (GameState, Broadcast, Sfx, Achievements). Godot signals become event dispatchers with the same names. The rooms-as-data pattern survives whole: build the world FROM Data/Rooms.csv and Data/Doors.csv exactly as world_builder.gd does, never by hand. The save is a USaveGame object mirroring _save_dict() in game_state.gd, version 16, including the DEMO whitelist behavior. UI is UMG; the booth's every control is enumerated in options_panel.gd. The CRT shader rebuilds in the material graph with the same parameter names (generation, tbc, photo_safe) so the art bible's numbers transfer. Text: import Data/GameText.csv as a StringTable; the source strings are the keys, same as the Godot side.

## 4 · WHAT DONE MEANS
Reference/docs/production/restoration-qa-regression.md is the acceptance suite: QA-01 through QA-32 pass on the UE5 build exactly as written, and every law in THE-LAWS.md holds. Parity protocol for testing both engines: same QA script, same playtest protocol verdicts, same probe list, run against each build on the same machine; the Gate 0 engine memo then signs itself from evidence instead of taste.

## 5 · DATA DICTIONARY
Rooms.csv: name, center X/Z (Godot meters, plan view), width, depth. Doors.csv: paired rooms, position, opening width, wall axis, kind (blank, door, window, locked with its key or condition). Stations.csv: the five log stations. Landmarks.csv: interactables incl. the four readable documents. Timings.csv: every number that tunes the game, with meanings. Achievements.csv: id, title, Steam-hidden flag; the deferral rule and meta-silence live in the design doc and are not optional. GameText.csv: Key,SourceString for a UE StringTable; 552 strings as of this kit.

## RULING (post first-boot): ENGINE DECIDED
The author has selected UE5 plus Blender as the production pipeline. Spike 2 is demoted from veto to routine validation. Add to the reading order, immediately after THE-LAWS: restoration-dread-doctrine.md, restoration-lore-architecture.md, restoration-lighting-bible.md (Reference/docs/canon), and restoration-blender-ue5-pipeline.md (Reference/docs/production). These four govern HOW content is made; the laws govern what it may never do.


------------------------------------------------------------------------------
DOCUMENT 03 · BUILD-ORDER.md
------------------------------------------------------------------------------

# UE5 BUILD ORDER (each milestone names its acceptance)
P0 · Boot and walk: greybox script, character pawn with Godot-matched feel (speeds in player.gd), doors from Doors.csv with locked reasons as world text. Done: QA-15 map optional, free walk of all twenty rooms.
P1 · Spike 2: the twelve-feed wall on target hardware. Done: 60 fps sustained, written into the engine memo.
P2 · State and saves: GameState subsystem, v16 SaveGame mirroring _save_dict, stations and paper economy. Done: QA-05, QA-16, QA-31.
P3 · The loop: bench capture, retake presentation, schedule clock, Harriet freeze, screening with stances and assist. Done: QA-06 to QA-11, QA-18.
P4 · The hunter and nights: Rundown behaviors incl. noise relocation and camera safety, night trip, Floor Manager, cascade. Done: QA-12 to QA-14, QA-19, QA-20.
P5 · Story gates and finale: presigned, crate and seance, fire tape, dock, unseal, lockdown, premiere with incidents, all endings, credits. Done: QA-21 to QA-28.
P6 · Meta and modes: achievements with deferral, DEMO flag with whitelist, booth complete, captions, pause, string table wired. Done: QA-01 to QA-04, QA-17, QA-29, QA-30, QA-32, and THE-LAWS.md audited line by line.

AMENDMENT (post-c043): P4 additionally covers the after-fire body, the tally contract, folds, and the dead room (QA-33 to QA-38). P5 additionally covers the full casualty arc, the crossing, and endings 4a/4b/4c/0 (QA-39 to QA-47). P6 adds A27/A28 and QA-48.


------------------------------------------------------------------------------
DOCUMENT 04 · UE5-MIGRATION-MAP.md
------------------------------------------------------------------------------

# RESTORATION · UNREAL ENGINE 5 MIGRATION MAP v1
Status honestly stated: this prototype is Godot 4, the build plan's Tier A path, chosen for Gate 0 speed. The plan's engine memo says Unreal 5 is the recommendation if production hires experienced 3D contractors (Lumen sells the compound; MediaFramework handles playback). This document is the UE5 half of that decision packet: every prototype system mapped to its UE5 home, so signing the engine memo either way is a choice between known quantities, and a port, if chosen, is a checklist.

## SYSTEM MAP (Godot artifact → UE5 target)
STATE. game_state.gd autoload → UGameInstanceSubsystem (RestorationState) with a URestorationSaveGame object replacing the JSON log; the versioned-migration pattern ports as a Version int and an upgrade chain. All signals become multicast delegates.
CLOCK. broadcast.gd → a WorldSubsystem ticking ON AIR and BREAK; wall clocks read it; door holds bind to its delegate exactly as now.
WORLD GENERATION. world_builder.gd's ROOMS table → a DataTable (FRoomRow: name, center, size, palette) consumed by an editor utility that stamps greybox geometry, or hand-built levels checked against the same table; the table stays the single truth either way.
CAMERA FEEDS. SubViewport MonitorRigs → USceneCaptureComponent2D into UTextureRenderTarget2D per feed; tally, kill, re-patch, and lockdown sync_to port one to one (sync = assigning one RT to many screen materials). Spike 2's twelve-feed budget is native territory here.
TAPE SHADER. crt_tape.gdshader → a Material Function stack applied to the RT (chroma offset, scanline, noise, tracking band, head-switch, dot crawl, vignette) with scalar parameters generation, tbc_on, photo_safe driven from the state subsystem via a Material Parameter Collection.
TAPE STAGE. The diorama SubViewport → a small sublevel captured by its own SceneCapture; the Scare 1 timeline becomes a Level Sequence with the lunge as a one-frame track.
SEANCE SUBSTRATE. FrameSequence's deterministic procedural frames → UTexture2D::CreateTransient filled per index with the same seeded generator, or the real footage path: an image sequence Media Source stepped by frame. The wear ladder stays a material parameter.
AUDIO. ToneEmitter and the Sfx synth autoload → MetaSounds graphs (hum, coil, segment tones, bell partials, thunk, tick) placed exactly where the spawn sites already are; the audio bible's bus plan becomes Submixes with the TBC as a Submix effect preset swap.
THE RUNDOWN. rundown.gd → an AActor with a tick brain (no Behavior Tree needed at this complexity; the grammar is the point). Noise bus → AIPerception hearing config or a custom noise delegate; the WARN and STRIKE telemetry lines port verbatim into the same log format so the parser still reads them.
COVERAGE DIRECTOR. coverage_director.gd → a WorldSubsystem; counters persist through the SaveGame; the append-only decision log is a plain FFileHelper append.
LIVE PRODUCTION. live_production.gd → a GameMode-scoped director actor; cue marks as trigger volumes; the switcher as Enhanced Input actions; incidents and fixtures port as-is; premiere_log unchanged.
CASCADE AND LIVENESS. cascade.gd and liveness_check.gd → the same two actors; the HUD blackout layer becomes a post-process weight or a UMG scrim (UMG scrim recommended: identical layering guarantee under labels).
UI. title.tscn, HUD, binder, map_view.gd → UMG widgets; the map redraws from the same DataTable via a widget's OnPaint, landmarks and station registry included.
INPUT. project.godot's action map → Enhanced Input mapping context, one to one: move, interact E, respond SPACE, improvise Q, tbc T, binder TAB, map M, photo_safe P, frame_back Z, frame_fwd X, cam_1..3.
HARNESS. soak.tscn, bot_driver, invariant_parser → Gauntlet or Functional Test maps: the three bots as pawns with the same behaviors; the parser as a test step reading the identical log files; INVARIANTS.txt survives unchanged, which means the milestone gates do not care which engine produced the scorecard.

## WHAT DOES NOT PORT
GDScript itself (targets are C++ subsystems plus thin Blueprints); gdshader syntax (rebuilt as material graphs per the map above); the tscn scenes (trivial, both are code-built); Godot's user:// (becomes ProjectSavedDir).

## WHAT MUST NOT CHANGE, REGARDLESS OF ENGINE
The invariant suite, the telemetry log formats, the save's semantic fields, the room table, the tell-table, the silence ledger, and every number in the playtest protocol's knob list. Engines are replaceable. The laws are not.


==============================================================================
SECTION 02 · CANON: THE WORLD AND THE CAST
==============================================================================


------------------------------------------------------------------------------
DOCUMENT 05 · restoration-cast-sheets.md
------------------------------------------------------------------------------

# RESTORATION · CAST SHEETS (canon, from Ciel's art)
Sources of record: docs/canon/art/cast-*.png. One ruling before the people: THE STATION IS WGLD, CHANNEL 58, EVERYWHERE, by the author's explicit word. Where any sheet's incidental set dressing reads otherwise, it is an artifact of the art process and reads as WGLD 58 in canon. The Gladhouse ran 1971 to 1977. Everything else on these sheets is law.

## RITA IVORI · TAPE CONSERVATOR
Professional. Patient. Precise. What others discard, she restores. Restoration Division; open-reel video, 2-inch quad, 1-inch Type C, U-matic, acetate and binder repair. Her tools are the dresser's seven, confirmed: cotton gloves, the 10x loupe, splicing block, leader tape, the archival binder, isopropyl and swabs, clipboard and accession forms. Adopted house lines for marketing: PRESERVE. REWIND. REMEMBER. and WHAT OTHERS DISCARD, SHE RESTORES.

## MERLE COTTRY · PRESIDENT. COOK. CARETAKER.
Late 60s, the 58 Club matriarch, occupation: everything. Voice warm, folksy, unhurried; hands never still: towel, spoon, mug, or someone else's sleeve. "This place runs on love and leftovers." NEW CANON: MERLE FOUNDED THE CLUB WITH LELAND. She remembers the early broadcasts not as research but as home, and she will protect the Club with open arms and bury the truth if she must. Guardrail, restated: burying the truth is grief's custodianship, never menace; the never-sinister rule survives untouched. This deepens M1 unbearably: at the fire tape she is asking her co-founder's colleague for company at her second funeral.

## VESS KEYS · TAPE HUNTER (he/him, ruled by the sheet)
Early 20s. Tape Hunter, Source Researcher, Provenance Specialist. Alignment: Lawful Curious. Voice eager, quick, searching; tell: touches the label maker or the 58 Club pin when nervous, and the pin on the sheet IS the plastic pin the deaths fuse into the enamel. He chases rumors, dead leads, and half-erased trailheads across thrift stores, estate sales, and forgotten basements; knows more about tape provenance than anyone and wants badly to be chosen for more than his catalog. Under the nerves and the notebooks is a kid who believes every tape holds a person no one else would look for. "Some tapes shouldn't exist. But they do. And I find them." Corrections executed: surname KEYS (the margin reads PER V. KEYS), pronouns he/him across the engine and the ledger.

## LELAND MERRICK · PREVIOUS ARCHIVIST
Filed. Not shelved. Mid-40s at the end; archivist and conservator, tenure 1972 to 1976, vanished the year before the fire. Voice dry, kind, careful; tell: green fine-liner in the margins. Always slightly cropped by the frame edge, as if the image cannot hold him correctly, which the engine's seance frames already honor. He left green-ink warnings in the accession logs that were later discovered inside the tapes themselves, and before he vanished he left one addressed to a conservator not yet hired, by name: "Rita. You are safe as audience. Do not be interesting. Never accept a role." That warning is the whole game's rulebook, written by the first casualty of ignoring it.

## HARRIET · SENIOR CLUB MEMBER · THE CONTINUITY KEEPER
Late 60s, mononymous by the club's own records, and the sheet grants her the title the game had been circling all along: THE CONTINUITY KEEPER. Voice precise, measured, transitional; her signature line, now canon and now in the build: 'And now. The tour continues.' The sheet's biography paragraph arrived illegible and is ruled an artifact, which is itself in character: her handwritten pages photograph as script that will not resolve, because her hand is transitional too. Confirmed props: THE teacup (floral china, the one that rises), a 58 Club flask whose contents go unrecorded, her pin card, and a reel in her keeping annotated for frame loss, which the club does not discuss. The title sharpens both of her graves: H1 is the continuity keeper edited for continuity, and H2 is the continuity keeper made into a continuity error the schedule refuses to acknowledge. The cast sheet set is complete at five: Rita, Merle, Vess, Leland, Harriet, plus the After-Fire dossier.


------------------------------------------------------------------------------
DOCUMENT 06 · restoration-after-fire-chum.md
------------------------------------------------------------------------------

# RESTORATION · AFTER-FIRE CHUM (canon, from the dossier art)
Source of record: docs/canon/art/after-fire-chum-dossier.png. File CHUM-AF-1974-P (REV.), Peak Production asset dossier. Peak Production is hereby canon as the production company that made THE GLADHOUSE for WGLD; the 58 Club inherited its assets, its building, and this.

## WHAT IT IS
There were always two Chums. The stage puppet, hand-sized, the one in the footage, the one the tell-table catches lying about being repaired. And the MASCOT: the 1974 walkaround body built for station events, eleven feet of it, because Peak believed in being seen from the back row. The fire took the vault; someone rebuilt the mascot afterward from what survived: salvaged cable for tendons, a studio monitor speaker revoiced into the throat, leg rods, a weighted foot base, the original button eye melted shut and kept anyway, purely cosmetic. The other socket got a TALLY LIGHT CAMERA EYE. The dossier's arithmetic is the horror: entirely manually operated, minimum three puppeteers for full performance, and a note that Chum manually controls his own jaw. Count the hands the design requires. Count the hands ever found operating it. HE REMEMBERS THE AUDIENCE.

## THE REVEAL
The Rundown was never bodiless; the player just never earned the sight. Watching the fire tape sets af_active: the tape wakes what the fire made, and from then on the hunter IS this, eleven feet, slow, weighted, loud. Before af_active it remains the old unseen presence. The dossier itself becomes a findable document (D11, Peak security office copy) after first sighting, and reading it is how the player learns the rules below in-fiction.

## THE TALLY CONTRACT (the mechanic Ciel specced)
His camera eye makes him broadcast equipment, and Law 1 binds broadcast equipment: ON CAMERA IS SAFE, and while RECORDING, you are on camera. Two clean states, unmistakably different:
STATE A · TALLY LIT (a capture is running, or scheduled ON AIR near an active rig): he may approach, all the way to 1.2 meters. He cannot strike. He watches. The jaw hand works its lever, open, closed, open, at no rhythm a song would keep. The throat speaker breathes room tone. This is the dread state: proximity without permission to flee (the capture pins you at the bench; aborting costs the tape).
STATE B · TALLY DARK: the contract lapses. THE TALLY COOLS for a marked 2.0 seconds, and then, if you are inside his reach, the strike is permitted, day or night, because you chose to let the clock run out with him beside you. If you are clear, he withdraws to his segment and the day resumes pretending.
THE COUNTDOWN, VISIBLE: the HUD carries a tally lamp whenever he is active and a capture runs: a red dot, the words SAFE WHILE LIT, and the same seconds the capture counts. One number, two meanings: progress and expiry. The player's math is the design: he is 9 meters out, moving at 0.8, I have 7.4 seconds of protection and 11 seconds of tape. Finish, abort, or meet him.

## SOUND AND CAPTION LAW
He is the noise system inverted: the building's quietest hunter becomes its loudest. Weighted footfalls thunk on his step interval (caption: [WEIGHTED FOOTSTEP], distance-scaled). The jaw is a dry lever creak (caption: [THE JAW WORKS ITS LEVER]). The bell at his collar stays silent, per the oldest law; if the model ever swings it, it is clapperless, and the caption for that is nothing.

## MARKETING AND FABRICATION NOTES
The dossier art is shippable as-is: it is the ARG's Phase 3 artifact ceiling and a Steam capsule candidate, and it obeys scarcity (a document about him is not him). Fabrication: the eleven-footer is digital plus a miniature for plates; the RFQ gains an optional line item, it does not gain a second hero build.

## THE SCALE LAW (addendum, at Ciel's insistence, correctly)
Eleven feet is a mechanic, not a measurement. In the build: the body stands 3.35 meters the moment he wakes, the tally eye sits at three meters and its red light burns ONLY while a capture runs (the light is the contract made visible; at loom distance the player is looking up into it), and HE DOES NOT FIT THROUGH DOORS. Every doorway costs him 2.2 seconds of folding, announced by caption and, when close, by a line about him bending and keeping his eye on you the whole way through. This is the player's counterplay, in fiction and in math: rooms are his, thresholds are yours. Put doors between you and the countdown changes in your favor by 2.2 seconds a door. The fold applies day and night; the night hunt inherits it, which slows him honestly and makes his footsteps a promise rather than a jumpscare.

## THE TWO HIDES (Ciel's inversion, canon)
Genre says hide in the dark. WGLD says the opposite, and Ciel said it first: the safe hide is the LIT one. To hide from harm, press yourself into a camera cone, because on camera he cannot and will not; he waits at the edge of frame instead, which is its own picture. To hide from HIM, there is exactly one dark hide: THE DEAD ROOM. He hunts by sound and the anechoic room eats sound; noise born inside it does not exist to his ears, and at its felt door he stops, holds, and says nothing further, because the room inside owes the air nothing. The cost is the geometry: the dead room is off camera, past the QUIET ROOM key and two folds, and reaching it is the gamble. First entry earns the radio line and the [NO ECHO] caption.

## THE TAUGHT CHASE (once, then never scripted again)
His first capture-approach is authored: he starts far enough that the tally dies with him meters out, and the first cool runs 4.0 seconds with its own line: THE TALLY COOLS. Two doorways stand between you and anywhere. Use them. One guaranteed sprint through one fold, the counterplay taught by survival, and every cool after runs the honest 2.0.

## THE LAST CROSSING (ending 4 earns its silence)
Divert at the final break and the sign-off plays through the building while Rita crosses it: master control to the little door, seventy-five seconds, him behind her at double approach speed, folds still costing him 2.2 apiece, his tally eye DARK the whole way because she diverted herself off the rundown: you are not in this broadcast; nothing on the log protects you. Reach the door and DEAD AIR proceeds as written. Caught, and the run ends the old way, a hand the size of a door and a starring credit, dying inside your own ending. Too slow, and the window closes without her: the show continues to Cue 3 and the committed line, the quiet ending lost to hesitation rather than teeth. Three outcomes, all authored, all hers.


------------------------------------------------------------------------------
DOCUMENT 07 · restoration-chum-motion-and-sound.md
------------------------------------------------------------------------------

# RESTORATION · CHUM, TWO BODIES: MOTION AND SOUND DOCTRINE
The difference is not damage. It is authorship. PRE-FIRE CHUM is a performance: three puppeteers, a camera, an audience, love. AFTER-FIRE CHUM is that performance with every hand removed and the movement continuing anyway. Everything below derives from that one sentence, and the timings cite the build as implemented (0.8 m/s approach, 1.2 m loom, 2.0 s cool, 2.2 s fold, 1.6 m/s crossing).

## PRE-FIRE · THE OPERATED BODY (footage, and the stage body at the dock)
Grammar: PERFORMED FOR CAMERA. Broad, front-facing, cheated out to the lens. Classic puppet timing: anticipation, overshoot, bounce-and-settle. Head tilts land in clean fifteen-degree stops. The jaw flaps a half-beat off the phonemes, which is why children loved him. Weight reads as five kilograms of felt and foam: fast starts, damped ends, secondary motion everywhere (ears lag, whiskers tremble, the bell answers every gesture). Curve language for animators: ease-heavy, bouncy, generous. In-game, the stage body never animates; it participates in L1 drift only (a head angle that is not yesterday's), because a puppet that moves without a show is a spent card and we do not spend it.
Sound: EVERYTHING MEDIATED. His entire pre-fire voice lives inside broadcast band-limiting (roughly 50 Hz to 8 kHz, tape wow, studio slap): felted thumps, the soft wooden clop of the jaw, rod clicks the club never mentions, and the bell bright and forward in the mix. Cheerful room tone under all of it. When footage goes wrong, the SOUND STAYS CHEERFUL while the picture wrongs: audio-visual dissonance is the pre-fire scare, and the only one.

## AFTER-FIRE · THE UNOPERATED BODY (the hunter)
Grammar: PUPPET GRAMMAR DELETED. No anticipation, no overshoot, no settle, no secondary motion of any kind: the wool is fused and reads as mass, and nothing on him bounces, ever. Where the stage body bounced, this one POURS: single-axis commitment, the head leading and the body arriving in one uninterrupted arc, knees nearly stiff, stride long, cadence slow, silhouette always at full height. Curve language: LINEAR IS THE HORROR CURVE: linear-dominant with two-frame ease caps at most. Stops are ABSOLUTE and binary: he is pouring or he is parked, statue-still, zero idle sway, no breathing, while the eye alone keeps tracking, servo-smooth. He never orients to the player as a person; he faces PATHS, and you are an obstacle shaped like an audience.
The three authored exceptions, each spending wrongness precisely: THE FOLD (2.2 s at every doorway): he does not duck, he REORGANIZES: shoulder through first, then the head arriving late on a hinge that should not exist: the one place puppet logic returns, horribly, rod movement without rods. THE WITHDRAWAL (tally cools with distance): he reverses along his exact approach path without turning, motion played backward, an undo. THE PERFORMANCE QUOTE, the doctrine's crown: while the tally burns and he stands at 1.2 m, he squares FULLY FRONTAL to you, broadcast stance, and permits himself exactly one pre-fire mannerism: the clean fifteen-degree head tilt. THE TALLY TURNS HIM BACK INTO A PERFORMER. Safety is being his audience again, and the tilt is why players will beg the countdown not to end.
Hard rules, corrected to the dossier (which had this right before I did): THE JAW OPENS, AND ONLY BY HIS OWN HAND. The mechanism is the sheet's: a lever inside the mouth, pulled to open, pushed to close, no motors, purely mechanical, so every opening is a two-beat act: the hand rises, one dry click, the jaw. Its grammar has exactly two entries. Under the tally, inside the performance quote, the jaw hand works its lever open and closed at no rhythm a song would keep: a show with the sound removed, performed at you. Outside the light, the jaw opens exactly once: the beat before a strike, hand rising, click, open, and then the near-silence. The jaw NEVER syncs to any sound, never flaps, never chews the air. THE BELL NEVER SOUNDS (clapperless by canon; the absence is the tell). NO VOCALIZATIONS, EVER: the throat speaker is not a voice.
THE THROAT SPEAKER, canonized from the sheet: a salvaged studio monitor revoiced into the chest, and under the tally it breathes band-limited room tone. Read against the audio law, this is the standing inversion the wake only spends once: the wake is MEMORY stepping into PRESENCE; the throat speaker is PRESENCE wearing MEMORY, always, quietly. If it ever plays more than room tone, that is a canon event and the author signs it first.
Sound: WRONG SOURCES DOING HONEST LABOR. Identifiable materials, unidentifiable purpose: the sub-heavy wood-through-floor footfall (S17, interval-driven), a wet-felt groan under load like leather pitched down, deep armature flex like a ship's hull ticking (never servo-whine; he is not a robot). The fold is S18 plus one soft textile drag and a single low wooden knuckle as the head arrives. At under three meters, HE OCCLUDES THE ROOM: reverb sends duck and a 200 Hz bloom rises, so the player hears the room lose a him-shaped space before they see him. While recording, a faint mains hum aligns him with the transmitter: performing, he syncs to the plant. The strike is nearly silent: one textile sweep, then the authored silence, because the loudest thing he ever does is stop making sound.

## THE AUDIO LAW (the ownable one)
BAND-LIMITED IS MEMORY. FULL-RANGE IS PRESENT. Every pre-fire sound lives inside the broadcast band forever; every After-Fire sound lives in true room acoustics with floor-coupled sub. The player's ear is trained until the law is reflex, and then the wake spends it: at the fire tape's end, the first full-range sound in the game BLEEDS OUT OF A BAND-LIMITED SOURCE, the audio stepping down out of the speaker into the room. That is the sound of him waking, and it is the scariest cut in the game because the ear understands it before the mind does.

## PRODUCTION NOTES (Blender and UE5)
Two rigs, deliberately unequal: the stage puppet rig carries full secondaries and cloth; the After-Fire rig has physics secondaries DISABLED and wool baked stiff, root-motion authored clips, the fold as a single authored 2.2 s montage per door width, eye on its own always-on track layer. Export per the pipeline doc; the sodium check applies to both wools, and the After-Fire wool must read as the same material that forgot how to be soft.


------------------------------------------------------------------------------
DOCUMENT 08 · restoration-casualty-ledger.md
------------------------------------------------------------------------------

# RESTORATION · THE CASUALTY LEDGER v1
Canon expansion. Law 7 (death is dignified) is STRUCK. Its replacement:

LAW 7, NEW · EVERY DEATH HAS A SIGNATURE. No one dies by chance or by timer alone; every death traces to a choice Rita made that the player can name afterward, and the game will name it for them, in the binder, in the ledger's voice. Horror license is opened wide with one house idiom: bodies fail the way tape fails. Splice, interlace, dropout, chroma bleed, leader where a voice was. Conventional dread and blood are permitted; the broadcast-body is what only this game can do.

A second principle governs the pairs below: FOR THE LIVING, BOTH GRAVES ARE DUG BY OPPOSITE CHOICES. Protecting a character from one death is frequently the act that exposes them to the other. There is no universally safe way to treat anyone; there is only knowing them well enough to choose their danger.

THE MECHANIC · deaths write to the casualty ledger (binder, TAB): an accession entry in stamp register, each ending reads the ledger aloud in its epilogue, and the run's final card counts the club. New save fields: casualties (array of ids with cause tags), plus per-death flags named below.

## MERLE (the never-sinister rule survives both deaths; she dies being exactly who she is)
M1 · THE SECOND VIEWING. Window: Day 3+, the fire tape. She asks: "I was there the first time. I'd rather not be alone for the second." CHOICE: let her watch with you. The reel recognizes 1974's carried girl and repossesses her mid-sentence; the last thing she does is pat Rita's hand, and her voice finishes the sentence from inside the speaker, warm, three seconds after her chair is empty. REFUSING her, which reads as cruelty, saves her.
M2 · THE HOME SINGER. Window: premiere only. The HOME segment needs a body in the rows; the run sheet has a blank line, and Merle volunteers ("I know the songs"). CHOICE: put her on the call sheet, which trivially solves one incident. During the closing verse the print sings the swapped word, HERE, and Merle, correcting the show the way you correct a child, sings HOME against it. The show corrects her. Taken on the beat, mouth still shaped around the true word. The blank line on the run sheet afterward reads MERLE O., STRUCK THROUGH, IN HER OWN HANDWRITING.
RIPPLES · Kitchen goes cold; the kettle never moves again and its stillness is a rundown-audible silence (the hunter lingers there). Coat pegs freeze at her peg's day. If M1: nights lose her DOORWAY watch and night trips escalate one stage early. If M2: the premiere's remaining incidents lose their forgiveness timers by 20 percent; the club noticed.
ENDINGS · Ending 3 (THE BURN): the epilogue's cobbler is found cold on the counter, plated for two; the M. Oyelaran line gains "the kitchen light was on. Nobody had eaten." Ending 2 (NEW PRODUCER): the carry-line vanishes; Rita's welcome is administered by no one, which is worse. Ending 1A/1B: the sign-alone beat plays to an emptier room; Leland's fourth answer changes to I KNOW. SHE'S HERE NOW. Demo carry-line: if a full-game save has Merle dead, a fresh demo boot refuses to load it forward (the carry promise dies with her; document in the demo doc).

## VESS (the credit dilemma: paperwork is exposure, obscurity is abandonment)
V1 · CREDITED, THEREFORE CAST. Precondition: Rita wrote her margin credit (PER V. KEYS). Named people are on station record; record is a call sheet. TRIGGERS (either): commit AUTHENTICATE at the ledger, or call her to the breaker a third time during the premiere. He is taken live, cut mid-sentence on his own slate insight, his plastic pin fused into the panel enamel. The credit line in the binder reprints itself as a cast credit.
V2 · THE UNCREDITED FIX. Precondition: Rita used his insight (the slate-skip benefit) but never credited her. Window: cascade night. CHOICE: at the dead panel, the option GET VESS appears; summoned to fix what he was never thanked for, he goes past circuit B to circuit F, the marshal's tie, bare-handed because skepticism is his glove, and the equipment that could not be de-energized includes him now. Found interlaced with the transmitter hum, his outline refreshing at 60 fields a second. Restoring the circuits alone, in order, saves him.
RIPPLES · Either death: breaker incidents lose their easy variant permanently; the binder's margin note bleeds green at the edges (Leland annotates her: HE COUNTED RIGHT.). V1 specifically poisons the AUTHENTICATE path's comfort: the ledger's INK toast appends "the record now includes one name you added." 
ENDINGS · Ending 2: the producer's office contains his chair, still warm, facing the monitor wall; accepting the role means taking her seat literally. DEAD AIR: with Vess dead the divert's breaker timing loses its grace window (hard mode for ending 4). 1B epilogue: FILE UNDER: SAINTS gains a second card, FILE UNDER: STAFF.

## HARRIET (she lives in transitions; both deaths are edits)
H1 · CONTINUITY. Window: any break, Day 2+. Her frozen hand holds a signature slip: free paper, in a game that starves you of it. CHOICE: take it. The show corrects the continuity error at the next break: she does not freeze, she is absent, chair warm, and the film cabinet now contains her, folded, with leader tape where her voice was. The stolen slip, used, signs the log in HER hand.
H2 · THE SPLICE. Precondition: the rejected edit exists as a temptation (splicing two takes yields a shortcut daily). CHOICE: perform the rejected edit on a reel carrying her segment. She inherits the cut: found at the following break seated one frame to the left of herself, doubled at the shoulders, both mouths open on different vowels, the teacup rising in two hands at two heights. She remains like this, on set, for the rest of the game, and the game treats her as scenery. That is the death: she becomes a broken frame the schedule stops scheduling.
RIPPLES · Whichever death: the seventh signal is gated. If Harriet dies BEFORE her index card is found, HOLD YOUR APPLAUSE is unlearnable this run, and the premiere's applause moment, unheld, costs a row member (see THE ROWS). Screening unison loses her; stances are judged 0.05 tighter without her metronome presence.
ENDINGS · All endings: her epilogue line is replaced by a title card in her stamp register: TRANSITION UNRESOLVED. Ending 1A: Leland's second answer changes to SHE WAS THE ONLY ONE WHO PAUSED PROPERLY.

## THE FLOOR MANAGER (silent, procedural; both deaths are cues)
F1 · THE FADER. Inside DEAD AIR only. The divert needs the master fader held through the full sign-off, and Rita cannot be at the little door and the fader at once. CHOICE BY OMISSION: proceed to the door without arranging otherwise, and he is already reaching for it; found after with his headset still cued, arm locked in a YOU'RE ON point at a camera that faces nothing, finished the way a gesture is finished, not a life. ALTERNATIVE: Rita holds the fader herself, takes the transmitter damage into her own hands, and the ending's epilogue changes voice (see ENDING EFFECTS).
F2 · THE UNLISTED CAMERA. Window: premiere. CHOICE: refuse or blind-call the tally cues three times (the lazy path the old fail-forward forgave). On the third, coverage must come from somewhere, and he steps into frame to cue a camera that is not on the run sheet. The unlisted camera accepts him. Thereafter he exists only in the program feed, visible in monitors giving cues to rooms he is not in, and his freeze-check mechanic INVERTS: stillness near monitors now draws his point.
RIPPLES · Either death: the premiere loses its stage discipline; cue marks stop auto-highlighting on the PGM camera. F2 specifically haunts every monitor for the remainder: a persistent, non-hostile wrongness (he never harms; he cues).
ENDINGS · DEAD AIR splits: 4a HIS HAND (he held the fader; the epilogue's "Signed off." is followed by a second line in another hand: cue given). 4b HER HAND (Rita held it; the epilogue is hers alone and her arm never fully works again, stated flatly). Ending 2: the producer's first staff meeting includes an empty headset on the table, channel open.

## LELAND (already dead; both deaths are un-deaths, and both close doors)
L1 · THE SIXTH QUESTION. Past the wear threshold, the pad accepts one question too many. CHOICE: ask it. His remaining print burns from the inside of the frames; the green ink drains upward out of every note in the building, and he is retroactively unfound: documents D01's pages go blank mid-read. ENDING 1A IS PERMANENTLY CLOSED this run.
L2 · THE READING. Discoverable dark experiment: bring the fire tape to the seance dock and play it INTO the wake. CHOICE: do so. The unfinished sign-off completes itself using his reading voice; his five answers un-write in reverse; the final frame shows the little door closing from the inside, his hand on the inner knob. He got to finish it. That is the horror and the mercy at once.
RIPPLES · L1: the seance dock goes inert; wear ceases to matter. L2: the fire tape is consumed (DEAD AIR's classic route loses its key item).
ENDINGS · L1 removes 1A; 1B becomes the only sign-off ending and its saints card gains AND THE READER, UNFILED. L2 removes classic 4 and CREATES ENDING 4c · THE COMPLETED SIGN-OFF: at the final break the divert is unnecessary because the program now ends on its own, correctly, using his ending; the station simply stops, all lights to black in reverse order of the tour Rita walked on Day 1, and the epilogue is the sign-off line, whole, for the first time since 1977, in his voice. Peace, purchased with a dead man's remainder.

## THE ROWS (ensemble; the fail-forward is now a mortgage)
Premiere incidents keep their guarantees, but each incident abandoned past guarantee takes a seated club member on camera: cut away from a smile, cut back to an empty chair, or to something half-resolved and interlaced, still trying to applaud at the held-applause mark. Casualty count feeds every epilogue's final card: THE 58 CLUB, followed by the new number.

## THE FULL BOARD (ending interactions at a glance)
1A requires: Leland's print intact (no L1, no L2) AND Merle's fourth-answer variant if she is gone. 1B always reachable; collects memorial cards. 2 gains furniture per death (Vess's chair, the open headset, the plated cobbler if Merle). 3 unchanged in routing; epilogue reads the ledger. 4 becomes 4a/4b via the F1 choice; hard-modes without Vess; replaced by 4c via L2. NEW ENDING 0 · A ONE-WOMAN SHOW: if all four living cast are dead before lockdown, the premiere runs regardless, and every role's title card reads RITA IVORI; the credits crawl lists the entire cast as her, one name, nine times; the achievements' meta-silence holds even here. Reached only by comprehensive, chosen cruelty; the game never advertises it.
ACHIEVEMENTS · exactly two additions, both hidden: A27 EVERYONEGOES HOME (finish any ending, zero casualties, rows included) and A28 A ONE-WOMAN SHOW (ending 0). No per-death achievements, ever; deaths are not trophies, they are entries.
IMPLEMENTATION ORDER (Godot first, UE5 kit inherits the canon): Commit 035 casualty state + ledger UI + M1/H1 (cheapest, deepest); 036 V1/V2 + credit-dilemma rewiring; 037 F1/F2 + DEAD AIR split; 038 L1/L2 + endings 4c and 0 + epilogue reader; 039 rows triage conversion + A27/A28 + QA-33..40.

## AS BUILT (c039-c043, deviations logged honestly)
All ten deaths, the rows, endings 4a/4b/4c and 0, the ledger page, the epilogue readings, and A27/A28 are implemented. Deviations from v1 as designed: V1's second trigger is the final breaker itself rather than a third summons (the farewell is the call); F2 fires on the third blind tally call (the guarantee's price made exact); L1's offer requires both five answers and wear past 70 (the pad only has room when you have already gone too far); ending 0 intercepts at premiere entry so the show truly runs without waiting. Canon-only remainders, named: the margin's green bleed, the post-F2 monitor haunt and freeze-check inversion, and Harriet's H2 splice, BUILT in c044: the temptation discloses her label, the daily mints instantly, the next break doubles her, and she remains on set as scenery with one line forever. The arc has zero open graves.


------------------------------------------------------------------------------
DOCUMENT 09 · restoration-reaction-matrix.md
------------------------------------------------------------------------------

# RESTORATION · THE REACTION MATRIX (nothing is isolated)
THE WEB LAW: every significant player action echoes in at least two systems or people, in character, at the right time. The club is a nervous system; Rita is an input to it. Below, BUILT cites the running game; QUEUE is the wiring order for the next commits.

## MERLE COTTRY (warmth is her instrument; fear makes her feed people)
To the player's care: signing logs on time earns kitchen smells scheduled to your habits (QUEUE M-R1); wasting paper gets no scolding, just a saved crust of a comment and an extra sandwich, because worry cooks (QUEUE M-R2). To snooping her kitchen: she narrates the object's story instead of objecting (QUEUE M-R3). To the wake: she never says his name after the fire tape exists; her lines route around it like water (QUEUE M-R4). To deaths: BUILT: the kettle clicks off for her own; THE BURN and cold cobbler when she is gone; the seance grief answer at frame 28. To Harriet doubled: she retires the second teacup from the rack, and it is never mentioned (QUEUE M-R5, the saddest line of set dressing in the game). To Vess credited by you: her breakfast line adds his name once, warm (QUEUE M-R6).

## VESS KEYS (curiosity is his spine; the wake breaks it)
To the player using his insight: BUILT: the credit dilemma in full, the INK ripple, both graves. To snooping his binder: delight, he narrates provenance uninvited (QUEUE V-R1). Pre-wake he leans toward every anomaly; post-wake he goes quiet in rooms with monitors, and his tell (touching the pin) doubles in frequency: the kid who wanted tapes to hold people learned one does (QUEUE V-R2, BUILT partially via premiere lines). To Merle's death: he starts filing her recipes as accessions, provenance grief (QUEUE V-R3).

## HARRIET (continuity keeps her; he is a continuity error)
To the player breaking the beat mid-take: her next transition adds one corrective beat of pause, precisely her length of disapproval (QUEUE H-R1). To night wandering: BUILT: her night line set. To the wake: HER FREEZES LENGTHEN when After-Fire is active in the building, one extra second, unexplained: continuity herself buffering against him (QUEUE H-R2, the matrix's crown). To deaths of others: BUILT: her slip and signature economy; her doubled state as scenery. Her sheet line, BUILT, on air: And now. The tour continues.

## THE FLOOR MANAGER (hands only; the hands know first)
To the player's blind calls: BUILT: the guarantee, then F2. To the fold: HE POINTS AT THE DOORWAY seconds before the first fold a player ever sees, a cue given to no listed camera (QUEUE F-R1: the hands know before you do). To Harriet doubled: at the next break he gives her mark anyway, to the empty half (QUEUE F-R2). To his own death: BUILT: the headset, channel open.

## LELAND MERRICK (ink only, and the ink grieves)
BUILT: the grief answers at frames 14 and 28, the pencil card, the sixth line, the reading. To the player carrying the fire tape past his shelves: one new margin appears, unsigned: NOT THAT ONE. PLEASE. (QUEUE L-R1, his only plea in the game.)

## THE BUILDING (also a character)
To ritual kept: doors ease, the hum settles a cent flat (QUEUE B-R1). To the ledger filling: corridor practicals lose one bulb per casualty, never replaced (QUEUE B-R2: the lighting bible's grief). BUILT: drift, the schedule, the tally grammar, the reverse-tour blackout.

## WIRING QUEUE (commit order 045 onward)
045: H-R2 and F-R1 (the two crowns: her lengthened freezes, his early point). 046: M-R5 and B-R2 (the teacup and the bulbs). 047: M-R1..4, V-R1..3, L-R1, remainder swept. Each lands with QA lines and stays inside the laws: no reaction explains, every reaction corroborates.


==============================================================================
SECTION 03 · CANON: THE BUILDING
==============================================================================


------------------------------------------------------------------------------
DOCUMENT 10 · restoration-room-bible.md
------------------------------------------------------------------------------

# RESTORATION · ROOM BIBLE (all twenty, from the shipped data)
Format per room: personality; light family (per the lighting bible); sound bed; decoration keynotes; object budget as I/L/D (interactables, lore objects, dressing); drift hooks; web tie. Budgets are caps, not quotas.

ENTRY · The threshold that decides you are expected. Amber over the door, the rest borrowed. Bed: yard wind under the door, the delivery van's absence. Keynotes: the coat pegs (drift ground zero), sign-in podium, a mat worn through at one heel. 1/0/8. Drift: pegs, mat angle. Web: deliveries land here; the door eases with ritual kept (B-R1).
REC ROOM · The hearth; the club's living proof. Warm amber, the safest light in the game. Bed: clock, upholstery quiet, distant kitchen. Keynotes: tournament bracket in three handwritings, doily archipelago, the corkboard with D04, S5 under a shaded lamp. 2/1/14. Drift: bracket updates, doilies migrate. Web: kitchen smells reach here on your habits (M-R1).
KITCHEN · Merle's sovereign nation. Amber plus the kettle's glow (a real light). Bed: kettle lifecycle, refrigerator sigh. Keynotes: menu chalkboard, recipe box, two aprons and one hook. 1/1/12. Drift: chalkboard menu, jar order. Web: the kettle click-off is a death beat; recipes become accessions if she goes (V-R3).
DORMS · Five doors, three slept-in; the club sleeps where it worked. Practicals per room, hall gap authored. Bed: radiators, one door that settles. Keynotes: D05 welcome folder, name cards (one blank), Rita's unadorned room. 1/1/10. Drift: which doors stand open. Web: the blank card is a shard.
YARD · The only sky the game owns. Night exterior, tower light visible and steady. Bed: wind, wire hum, gravel. Keynotes: laundry line, antenna guy-wires, distance measured in dark. 0/1/8. Drift: laundry count. Web: the tower light's meanings (premiere, 4c) read from here.
SHED · The yard's shadow; tools that predate everyone. Single bulb, pull chain. Bed: paint cans, wasp-quiet. Keynotes: padlock hasp (unlocked, always), stenciled initials gone illegible. 1/1/6. Drift: the hasp's angle. Web: shard site for the rebuild question (never stated).
CORRIDOR · The spine; the walk you will know blind. Spaced tungsten with authored gaps. Bed: your own footsteps returned a half-size large. Keynotes: S1 at the library mouth, notice board, floor wax history. 1/0/6. Drift: notice board papers. Web: bulbs die per casualty (B-R2).
TAPE LIBRARY · A chapel of holdings; quiet is enforced by the room itself. Cool practicals, stack-end lamps. Bed: HVAC breath, ballast tick. Keynotes: card catalog, accession spines (the skip cluster findable), one mislabeled decade. 2/2/16. Drift: a spine reversed. Web: Vess's country borders here; the crate lives deep.
BENCH ROOM · Rita's altar; the game's heart at 9,-16. Task lamp truth over the bench, warm elsewhere. Bed: machine idle, tape whisper at speed. Keynotes: THE BENCH, the decision LEDGER with D03, splice tools in surgical order. 3/1/8. Drift: none here ever (trust law: the altar is stable). Web: everything routes through this room's verbs.
CLIMATE · The building's lungs. Green gauge glow, grille shadows. Bed: the deepest hum, compressor cycles. Keynotes: gauges with handwritten ranges, filter log ending mid-1977. 1/1/6. Drift: one needle's rest point. Web: the hum settles a cent flat when ritual holds.
TRANSMITTER HALL · The plant; a cathedral that never sleeps. Phosphor and pilot lamps, S4 in the aisle. Bed: mains as organ note, contactor clacks. Keynotes: THE TRANSMITTER, breaker rows, warning placards in period voice. 2/1/10. Drift: never (the plant is honest). Web: he syncs to this room's hum while performing; V2 ends here at circuit F.
DEAD ROOM · Already doctrined; the one dark hide. Single flat toplight, near-zero bounce. Bed: your own blood pressure. Keynotes: wedge foam, the RADIO, the felt door. 1/1/3. Drift: forbidden. Web: deaf to noise; he holds at its door.
FIRE CORRIDOR · The scar; 1977 under two coats of paint. Deliberately underlit, one honest bulb. Bed: nothing; this hall eats sound politely. Keynotes: char shadowline at knee height, the FIRE TAPE DOCK, a hydrant post nobody repainted. 1/1/5. Drift: the shadowline does not drift and players will swear it does. Web: the wake begins here.
STAGE HALL · The wings' approach; anticipation as architecture. Borrowed studio spill through the door crack. Bed: studio air pressure, grid creak above. Keynotes: sightline tease of the stage, sandbag row, cue light (dark). 0/1/6. Drift: sandbag count. Web: the FM's point (F-R1) reads best from here.
STUDIO A · The church. Grid above, tallys around, CHUM'S MARK at center stage. Bed: the largest room tone in the game. Keynotes: the stage body's home, camera pedestals with taped names, audience rows, the little door under the set. 3/2/18. Drift: the mark's tape lifts one corner across days. Web: everything ends here; row casualties seat here.
PATCH BAY · Vess country; a jungle with a wiring diagram somewhere under it. Phosphor plus a clip lamp he added. Bed: fan chorus, jack clicks remembered. Keynotes: THE PANEL (cascade), cable looms with his tags, D07 binder, the credit margin. 3/2/12. Drift: one loom re-dressed. Web: V2's offer lives here; his absence makes this room loudest.
CONTROL · Narrow authority; the marshal's corridor of record. Cold fluorescent, honest and unflattering. Bed: relay ticks. Keynotes: D09 marshal packet, inspection stamps, a chair that faces the door. 1/2/6. Drift: stamp alignment. Web: authority's paper trail shards live here.
MASTER CONTROL · The show's eye; the FM's realm and S2's home. Monitor wall glow, phosphor dominant. Bed: sync tone underlay, deck transports. Keynotes: the MONITOR WALL, run sheets on clips, his headset's hook, the unlisted camera's absence on the sheet. 3/2/12. Drift: run sheet clip angles. Web: F2 fires here; ending 2's chair faces this wall.
GREEN ROOM · Harriet's parlor; the club performing calm for itself. Mirror bulbs (two dead, always the same two), S3 warm. Bed: clock older than the building's. Keynotes: HER CHAIR, the teacup's saucer ring, mirror with cards tucked in the frame, D06's home. 2/2/10. Drift: the saucer ring count. Web: the second teacup retires here (M-R5); her doubling is staged here or Studio A per scene.
SCENE DOCK · Backstage afterlife; where the show's bones are stored standing. THE SODIUM TRUTH LIGHT lives here, plus work strips. Bed: tarp shift, chain hoist idle. Keynotes: flats leaned like tarot, the SEANCE DOCK, D10 IRIS, D01's shelf, the dock clipboard. 3/3/14. Drift: which flat faces out. Web: the reading, the sixth line, and the sodium check all live in this room; it is the game's confessional.


------------------------------------------------------------------------------
DOCUMENT 11 · restoration-ambient-lore-ledger.md
------------------------------------------------------------------------------

# RESTORATION · AMBIENT LORE LEDGER (the little things, room by room)
Source of record for AMBIENT lore per the Object Taxonomy: none of these prompt, none are flagged, all are found by looking, and every one rhymes with a truth without stating it. Tags map each detail to the thread it feeds: T1 what Chum is · T2 the carrying · T3 Leland's choice · T4 who rebuilt him · T5 what Merle buried · T6 why a conservator was hired · T7 the little door · plus histories: HF the fire · HC the club's founding · HH Harriet · HV Vess · HM the marshal · HP Peak Production. The Never-Stated Ledger governs: any detail that graduates from rhyme to statement is a defect.

ENTRY · The sign-in podium's oldest pages: a 1976 line where L. MERRICK signs IN and the OUT column is blank, forever, with every later line neatly closed [T3]. The mat's worn heel faces the building, not the door: people brace coming IN [HF]. A key hook labeled TOWER whose key has a newer cut than its tag [T4].
REC ROOM · The tournament bracket's fifth name is inked out, and the scoring beneath it continues one more round anyway [HC]. One photo frame on the wall faces the wallpaper; its hanging wire is dusty, its nail is not [T5]. The corkboard's green pushpins hold only the oldest papers, and nobody stocks green pins now [T3, HC].
KITCHEN · A recipe card, CHUM'S BIRTHDAY SHEET CAKE, SERVES 60, amended in newer hand to SERVES 12, then to nothing [HC, T1]. Six mug hooks, five mugs; the empty hook is the most polished [T3]. Taped inside a cabinet door: a feeding rotation for volunteers dated the week after the fire, all names crossed off but one [T5, HF].
DORMS · The blank name card on door four, and inside, a wallpaper square brighter than its wall where something hung the length of a warning [T3]. The welcome folder's earlier revision, misfiled beneath the shelf liner, lists a room count of six [HC]. A window latch on the yard side painted shut from the inside [HF].
YARD · The antenna guy-wire's crimp tag, stamped 1971, still bright [HC]. Zip-tied to the fence, a child's bicycle bell with the clapper removed [T1, and it rhymes with his]. The burn barrel holds melted film-can lids fused into one disk, rim stamps just legible: GLADHOUSE [T5, HF].
SHED · A paint can labeled STAGE FLOOR '74 with a clean brush balanced across it, hardened mid-care [T4]. Rod stock in a coil, felt scraps snagged on the cut ends [T4, T1]. On the door's inside, tally marks in pencil, groups of five, stopping at fifty-eight [HC, and nobody counts that high for fun].
CORRIDOR · The notice board's yellowed memo: FOUND PROPERTY, ONE CHILD'S MITTEN, UNCLAIMED, dated three years before the fire, initialed and never taken down [T2]. Beneath the newest wax, an older traffic lane bends toward the dead room's door before the club ever labeled it [T7 adjacent, HH]. S1's pen is chained; the chain has been replaced twice, the pen never [ritual, HC].
TAPE LIBRARY · The accession skip cluster, as canon, findable by anyone who runs a finger down the spines [T5]. Card catalog drawer G: one card's corner scissored off cleanly, the cut older than the dust [T5]. A donations ledger line in Merle's hand: 27 REELS, ANONYMOUS, WATER DAMAGE, DO NOT ACCESSION, M.C., and no reels answer to it anywhere [T5, missable forever].
BENCH ROOM · Under the bench lip, scratched shallow where only a cleaner's hand would find it: L.M. [T3]. The splice blade log shows blades changed weekly for years, then a four-month gap in 1977, then weekly again in a different hand [HF, T6]. Drift stays forbidden here; the lore is static and quiet, because the altar tells the truth by not changing.
CLIMATE · The filter log ends mid-1977 and resumes with no explanation and better handwriting [HF, T6]. The gauge nearest the transmitter wall wears a heat crack; its twin does not [HF]. A maintenance tag signed by three initial-sets across one decade, the third set appearing only after 1974 [T4].
TRANSMITTER HALL · The placard reads DE-ENERGIZE BEFORE SERVICE, and under raking light an older painted-over line ghosts through: IT STAYS ON [never-stated, and never explained]. Breaker F's handle is newer than its row, the enamel around it re-fired [foreshadow, HV]. A dymo strip on the rack, not Vess's font: AUDIENCE FEED, DO NOT MONITOR, green [T3, T2].
DEAD ROOM · One foam wedge cut out and re-glued inverted, the seam careful [HH]. Inside the felt door at knee height, the nap is worn through in one hand-sized place, from the inside [T7 adjacent, and it is worse the longer you look]. The radio's dial is fixed at 58 with a dot of nail polish [HC].
FIRE CORRIDOR · The char shadowline, as canon, at knee height under two coats [HF]. The hydrant post's repaint stops at a masking-tape line, and the tape was never pulled [HF, work interrupted]. A door hinge on the dock side replaced with one brass screw among steel [T4].
STAGE HALL · Sandbag tags carry rig dates; one sandbag is dated the spring AFTER the fire [T4]. The cue light's bulb is missing, but its socket is clean [HP]. A chalk arrow on the floor, mostly mopped away, pointing toward the little door's side of the stage [T7, missable].
STUDIO A · The little door's floor shows a scuffed swing arc through wax that is otherwise unbroken [T7]. Audience seat 14 wears a brass RESERVED plate with the name line blank [HH, and frame fourteen knows why]. On the grid, chalked puppeteer marks: three, one scuffed to a smear [T4, the arithmetic]. The camera pedestals' tape names include one taped-over name the light catches [HP].
PATCH BAY · Vess's loom tags, and one loom re-dressed in someone else's lacing pattern [HV, T4]. A jack labeled in green ink, older than every dymo strip: AUD RETURN [T3, T2]. Coffee rings on the run sheets age like tree rings toward the panel, then stop in 1977 and begin again in 1984 [HC, HF].
CONTROL · A carbon flimsy filed backward: NOISE COMPLAINT, SIGNAL AFTER SIGN-OFF, 1975, the response line blank [T1, HM]. The inspection stamps skip one quarter and no one restamped it [HM, HF]. The chair faces the door, and its casters have worn a quarter-circle, not a line [somebody watched the door, T3].
MASTER CONTROL · The run sheets, as canon, with no unlisted camera anywhere on them [HP]. The tally test button is worn to bare metal; nothing else on that panel is [ritual, T1]. Two headset hooks; one is bent straight and retired in place [HP, and the FM uses the other].
GREEN ROOM · The mirror's tucked cards include the 1977 season schedule, its last line hand-amended from FINALE to SIGN-OFF [HF, HH]. The two dead bulbs are the same two in every era of photographs on the wall [HH]. Behind the mirror's corner, a strip of gray flannel used as a shim [T2, the worst place to find it].
SCENE DOCK · The flat that faces out is the little house's interior wall, and its painted door is painted OPEN, the only rendering anywhere that shows it open [T7, T1]. Under a chained tarp, a shape the size of a kettledrum that is not a kettledrum, dust seal unbroken [T4, never resolved]. The sodium fixture's purchase tag hangs on its chain, dated 1978, the first thing bought after [T6, and someone needed the truth light].

DISCIPLINE: every detail above is static (QA-56), promptless (QA-55), and three-reads compliant; at least one shard per truth remains missable forever; and nothing here states what the Never-Stated Ledger protects. This ledger is the decoration brief's lore layer: dressers dress FROM it, then around it.


------------------------------------------------------------------------------
DOCUMENT 12 · restoration-object-taxonomy.md
------------------------------------------------------------------------------

# RESTORATION · OBJECT TAXONOMY (interactable, lore, dressing)
Three tiers, and the tiers are promises to the player's hands and eyes.

INTERACTABLES carry verbs. They prompt, they glyph the real binding, and they are absolutely stable: an interactable never drifts, never relocates, never lies. The bench, stations, docks, doors, panels, the ledger, the readable props with handling. Affordance is diegetic wear, not outlines: the used thing looks used (the bench's worn edge, the panel's polished breaker). One HERO interactable per room maximum, so rooms have altars, not menus.
LORE OBJECTS carry shards. Two kinds: HANDLED lore (the D-series readables: they prompt, they mark_read, they obey the Three Reads Rule) and AMBIENT lore (the blank name card, the filter log's end date, the skip-cluster spines): AMBIENT LORE NEVER PROMPTS. It is found by looking, which is the whole covenant of the noticing game. Ambient lore may sit inside dressing density and must never be flagged, sparkled, or listed.
DRESSING is the lived-in mass, and it is the ONLY drift-eligible tier. Dressing never prompts, never blocks, and earns its place by biography: every dressed object implies a person and a habit (three handwritings on one bracket). Density per the Room Bible budgets; clutter without authorship is banned.

LAWS ACROSS TIERS: the prompt is the tier boundary (if it prompts, it is a promise); drift eligibility is dressing-only so trust in tools is never spent; readables registry stands at D01 to D11 with homes per the Room Bible (D02 remains the one readable whose home is the player's: the welcome packet copy Rita carries); no object exists that is interactable-looking but inert (fake affordance is a lie in the light's language).
QA HOOKS: QA-55 prompt-discipline sweep (nothing ambient prompts; nothing prompting is unstable); QA-56 drift audit (all drift instances resolve to dressing tier); QA-57 hero-object census (no room exceeds one).

ADDENDUM: the AMBIENT LORE LEDGER (canon) is the source of record for ambient-lore placement; the Room Bible's L budgets count against it.


==============================================================================
SECTION 04 · DOCTRINE: HOW IT IS MADE
==============================================================================


------------------------------------------------------------------------------
DOCUMENT 13 · restoration-dread-doctrine.md
------------------------------------------------------------------------------

# RESTORATION · THE DREAD DOCTRINE (how the creep factor is built)
Thesis: dread is anticipation under rules. Fear without rules is startle, and we own exactly one of those. Creep is manufactured by TEACHING RULES, PROVING THEM, and then SPENDING them at chosen moments. Every technique below is already in the build; this document makes the method transferable so new content extends the machine instead of diluting it.

## THE DREAD STACK (five layers, in loading order)
L1 · AMBIENT WRONGNESS, sub-threshold. The world drifts and never says so: the coat pegs migrate on their curve, Harriet's cup is higher than yesterday, a hum sits where a hum was not. Rules: drift is monotonic (never resets, never toggles), never called out by text, and dense enough that a second playthrough is a different game. L1 is the soil; it produces no fear alone, only the sensation of being slightly wrong about a familiar place.
L2 · RITUAL AND SCHEDULE. Safety is procedural: the beat, the stances, the signs, ON AIR. Because compliance protects, obligation itself carries tension: the player is never idle, they are always slightly performing. Rule: the ritual must actually work. Betrayed ritual is a startle economy; kept ritual is a dread economy.
L3 · THE NOTICING GAME. The tell-table philosophy: the game hides deltas and hands the player instruments (the loupe, the gen knob, the scope). Paranoia is player-generated, which is the only kind that lasts. Rule: every plantable tell must be objectively there; we never gaslight with randomness. The player's fear is that they are RIGHT.
L4 · PROXIMITY UNDER CONTRACT. The tally: safety that is visible, absolute, and expiring on a clock the player can read. He crosses the room BECAUSE you are safe. Rule: contracts are never violated (Law 1, Law 10); the horror is arithmetic, not betrayal.
L5 · THE VIOLATION BUDGET. One startle. One interface lie. One once-ever sight. Scarcity is what keeps L1 through L4 potent; every spent violation devalues the currency. Rule: the budget never grows. New content must find its scare inside L1 to L4.

## AMPLIFIERS (multipliers on the stack)
WARMTH: Merle makes Chum scarier. Comfort raises stakes; the kettle's warmth is load-bearing dread infrastructure, which is why its click-off is a death beat. MUNDANITY: paperwork against wrongness; the accession form is the flashlight. SILENCE AS EVENT: the bell rings once, so silence is the instrument the rest of the time; every death scene ends in authored silence. PATIENCE AT SCALE: he waits at 1.2 m; waiting is scarier than lunging and costs nothing. CONSEQUENCE MEMORY: H2 leaves her on set; the ledger reads itself back; the world keeps receipts, so the player's past becomes ambient wrongness they authored (L1, weaponized).

## THE THREE TESTS (gate for any proposed creep)
REPETITION: still unsettling the fifth time? (Startles fail this; the fold passes.) LAW: does it break the budget or any contract? (Auto-reject.) EARNED: does the player's own attention or choice produce it? (The best dread is self-inflicted.)

## THE FIVE-DAY CURVE (which layer leads)
Day 1: L2 leads (learn the rituals), L1 seeds. Day 2: L3 leads (instruments arrive), L1 compounds. Day 3: L2 inverts (obligations multiply; the ledger asks). Day 4: L4 arrives whole (the wake, the tape, him), L5 spends the sight. Day 5 and the premiere: all layers simultaneous, and the budget is empty, so the finale's fear is entirely earned interest.

## ANTI-CREEP (banned)
Random scares. Musical stings. Darkness as content. Enemy quantity. Unreliable narration beyond the one lie. Gore for volume (the broadcast-body idiom is precise, not wet). Any text that says the word creepy.


------------------------------------------------------------------------------
DOCUMENT 14 · restoration-lore-architecture.md
------------------------------------------------------------------------------

# RESTORATION · LORE ARCHITECTURE (piece by piece, and the player assembles)
Prime directive: THE GAME NEVER EXPLAINS. It corroborates. Understanding is the player's manufacture; we supply parts with tight tolerances and no assembly manual. A mystery solved BY the game is spent; a mystery solved by the player is owned.

## THE SHARD MODEL
Every truth in the canon exists as 2 to 4 SHARDS distributed across four media: DOCUMENT (the readables, D01 to D11), ENVIRONMENT (props, drift, geography), BEHAVIOR (what characters and the building do), and MECHANIC (what systems teach by consequence). Rules: no shard is mandatory; no shard states the truth whole; shards RHYME (shared nouns, dates, and verbs) but never quote or cite each other; at least one shard per truth is missable forever.
WORKED EXAMPLE, the carrying: D04 (a girl found safe, wrapped in gray flannel, carried the long way, singing) + the tell-table's patch S-07 (school-gray flannel, on him) + Merle's 1974 monologue (behavior, night-gated) + Ending 2's mechanics (inclusion as promotion). Four shards, four media, zero statements. The player who links flannel to patch did the work, and the game never says WELL DONE, because the reward is the cold feeling, not a checkmark.

## THE THREE READS RULE
Every artifact supports three depths and must be complete at each: SURFACE (its use: the clipping is set dressing about a rescue), CURIOUS (its oddity: the flannel the mother did not recognize), OBSESSIVE (its cross-reference: S-07). Authoring order is obsessive-first, then camouflage down to surface. An artifact that only works at one depth is either a prop (fine) or a lore dump (banned).

## THE NEVER-STATED LEDGER (truths the game must never confirm in any text)
What Chum is. The mechanism of carrying. Whether Leland chose to stay. Who rebuilt the after-fire body, and with whose hands. What Merle knows and buried. Why the club truly hired a conservator. What the little door opens onto. Each has its shards; none has a sentence. Writers adding content check against this ledger the way engineers check the laws: naming one of these in dialogue or text is an S0 defect.

## GATING PHILOSOPHY
Curiosity-gated beats progress-gated: the crate, the wear ladder, the dossier appearing only after he walks, the sixth line offered only past the threshold. Progress gates exist solely where routing requires (keys). Redundancy rule: knowledge the ROUTE needs gets a mechanical teacher (the screening teaches the beat; the taught chase teaches the fold); knowledge the STORY holds gets none, ever.

## DELIVERY BANS
No codex that summarizes. No character who explains (Vess speculates and is sometimes wrong; Merle deflects warmly; the FM is silent; Leland answers only what is asked, in fragments). No journal that concludes: the binder records FACTS OBSERVED in the ledger's voice, never interpretation. No AS YOU KNOW. The dead teach loudest: V1 teaches record-equals-cast better than any note could, which is the pattern: CONSEQUENCE IS EXPOSITION.

## THE COMMUNITY LAYER
The ARG uses the identical grammar externally (the slate skips are a shard the site never confirms), so the community's collective assembly rehearses the game's private one. Post-launch, the solution ledger publishes SHARD MAPS, never truths: even the archive keeps the directive.


------------------------------------------------------------------------------
DOCUMENT 15 · restoration-lighting-bible.md
------------------------------------------------------------------------------

# RESTORATION · LIGHTING BIBLE (UE5 · Lumen)
Thesis: LIGHT IS THE GAME'S HONESTY. The interface may lie exactly once; light never lies, which is why the player learns to trust it, which is why controlling it controls the player's nervous system. Every state below is readable without HUD.

## THE GRAMMAR (colors are contracts)
RED means WATCHED, and watched means SAFE: the inversion is the whole language. Tally lamps, ON AIR signs, his camera eye: red is the contract burning. The player must be trained (Day 1 screening does it) until red reads as shelter, so that a dying red reads as the floor opening. PHOSPHOR GREEN is information: monitors, the scope, UI-diegetic surfaces; it illuminates data, never rooms. AMBER TUNGSTEN is the club's warmth: kitchen, rec room, dorms; practicals with real fixtures. SODIUM is the truth light: one fixture, the scene dock, where materials cannot lie (the art bible's material gate, playable). DARK IS A ROOM, NOT A WALL: minimum readable floor everywhere; silhouettes always resolve. We never buy fear with unreadability.

## STATES (the building's lighting is scheduled, like everything else)
DAY, ON AIR: full practicals plus every tally lit; the safest the world ever looks, and it looks it. BREAK: the tallys die together; red drains from the world on the cue; BREAK IS VISIBLY LESS SAFE and Harriet freezes inside the color change. NIGHT: practicals off; exit signage, standby LEDs, phosphor spill, moonless windows; navigation by learned geography plus the grammar. CASCADE: authored two-stage darkness with real circuit GEOGRAPHY (C's zone dies, then B's; restoring in order relights in order; the panel's labels are the map). THE CROSSING: his eye dark (the one time red abandons the player, stated in text), the sign-off's glow leaking under doors along the broadcast path. 4c: the reverse-tour blackout, room by room in Day 1 order, entry last, then the tower light, then nothing, as rest.

## HIM (the biggest fixture in the building)
His eye is the only MOBILE red source in the game: reserve the hue. HIS SHADOW IS A MECHANIC: at 3.35 m under Lumen, his shadow precedes him through doorways; the fold announces by silhouette before body, every time, for free, because we made him tall. He casts; UI glow does not. Wool under amber reads warm and wrong; wool under sodium reads exactly like what it is: the dock is where players go to be sure, and being sure is worse.

## UE5 TECHNICALS
Lumen GI on, software tier baseline (hardware RT optional). AUTO-EXPOSURE OFF: locked EV per room-state; transitions CUT with the schedule, never swim, because eyes adapting is a comfort we do not sell. Shadow maps virtual; volumetrics low and motivated (projector cones, the transmitter hall only). Practical fixture families per room class, authored in Blender with true bulb positions so Lumen bounces honestly: REC amber overheads plus the kettle's glow; CORRIDORS spaced tungsten with authored gaps (the gaps are content); STUDIO grid plus tallys; DEAD ROOM one flat toplight, near-zero bounce, mattest room in the game: light goes there to die too. COLOR SCRIPT BY DAY: Day 1 warmest, desaturating and cooling on a curve to Day 5, executed as per-day post volumes over unchanged practicals, so the world does not change, only the truth of how it reads.


------------------------------------------------------------------------------
DOCUMENT 16 · restoration-comparative-study.md
------------------------------------------------------------------------------

# RESTORATION · COMPARATIVE STUDY (FNAF, TJOC, and the viral wave)
Method: what each did RIGHT, distilled to transferable principles, then sorted into ADOPTIONS (with build actions) and REFUSALS (with the law each protects). Sources: current pages and coverage of the titles named, checked this week.

## I · FNAF, THE ORGAN BANK
What it did right, precisely: 1) THE ATTENTION ECONOMY. Scarce senses, scarce power, one chair: the game is deciding what you can afford to look at, on a clock. Fear lives in the allocation, not the animatronic. 2) READABLE ESCALATION. Each threat has a temperament and tells; mastery is learnable, nights are ritual escalation. 3) THE INTERFACE IS THE GAME. Diegetic cameras, doors, and meters; no abstract HUD between the player and dread. 4) LORE BY SCARCITY. Fragments in minigames and newspapers fed a decade of communal theorycraft; the community's assembly WAS the marketing. 5) CHARACTER AS ENGINE. Designs strong enough to carry theory, art, and merch. 6) FREE-FIRST ENTRY and short runtimes made every streamer a distributor.
What we refuse from it: the jumpscare kill-loop as the retention engine. Repetition-by-death is a startle economy; our budget holds one. Our retention is obligation plus compounding dread interest, and our deaths are authored choices, never resets.

## II · THE JOY OF CREATION (the closest cousin, now in our exact engine)
TJOC began as the fan game widely held to be the scariest of them all and is now an official Fanverse release, rebuilt in UNREAL ENGINE 5, five levels each a distinct blend of free-roam and sit-and-survive, with a siege built on braided resources (fuses, per-camera battery, flashlight, mains). Lessons: 1) PER-LEVEL MECHANICAL IDENTITY: every level owns a verb-texture. Our five days already converge on this via the dread curve; it is now an audit requirement, not a hope. 2) THE RESOURCE BRAID: peak pressure comes from two or more attention demands sharing one clock. Our premiere incidents must be tuned to braid, never queue. 3) BLESS THE FANS: the Fanverse pipeline turned the community's best into canon; our ARG and shard-map policy should be drafted expecting fan works, early and warmly. 4) STREAMER CARE AS A FEATURE: TJOC shipped a bitrate-friendly setting in a DEMO. Grain and CRT mash under compression; we add a streamer mode (compression-kind grain, overlay-safe HUD margins) to the booth backlog. 5) The burned mascot's power validates the After-Fire body: damage reads as history, and history is scarier than teeth.

## III · THE MEDIATED-EYE CLUSTER (our nearest lineage, and it is hot)
Content Warning made FILMING THE HORROR the core verb, engineered explicitly to go viral: the footage is the score. The Exit 8 made the NOTICING GAME the entire product: one corridor, spot the anomaly, built in nine months, spawned a genre and a feature film. Iron Lung made seeing-only-through-instruments the whole terror. Amanda the Adventurer made the tape itself answer back. RESTORATION's bench capture, tell-table, loupe, and scope are this cluster's grammar, executed with authored rigor instead of randomness. Marketing should say the lineage out loud: YOU WATCH THROUGH MACHINES, AND THE MACHINES ARE HONEST.

## IV · THE SLOW-BURN PROOFS
Mouthwashing: low-poly, narrative-first, its darkest truths living between the lines, and it went viral on exactly that restraint: the Shard Model at market scale. The PS1 wave and Chilla's Art prove aesthetic COMMITMENT outsells fidelity: our crafted-not-photoreal bible is commercially validated, not a compromise.

## V · THE CLIP ECONOMY (how virality actually works now)
Thirty seconds, one frame legible, arc complete: that is the unit of spread. Exit 8's single hallway is clip-perfect by design. Our engineered clippables, named so trailers and creators find them: the first doorway fold; THE TALLY COOLS with him standing in it; the countdown expiring at SAFE WHILE LIT; the bell; the dossier's WARNING page; Harriet doubled at the break; THE LEDGER, READ ALOUD. Demo-first (Tape 1) is the FNAF-proven top of funnel and stands.

## ADOPTIONS (build actions)
A1 Streamer mode to booth backlog (compression-kind grain, HUD safe margins, capture-clean toggle). A2 Premiere braid audit: at each pressure peak, at least two simultaneous demands; add to QA as QA-51. A3 Per-day verb-texture audit against the dread curve; any day without a new texture is a defect. A4 Clip ledger adopted into trailer beats (this section is the source of record). A5 Fan-content policy drafted before launch, generous by default, Fanverse-shaped. A6 Demo scope reaffirmed as the funnel.

## REFUSALS (and the law each protects)
Jumpscare kill-loop retention (the violation budget; deaths are authored). Randomized anomalies (the noticing game requires the player to be RIGHT; drift stays authored and monotonic). Co-op (solitude is load-bearing; the presence spec). Procedural levels (the building is a character; geography is memory). Gore-forward marketing (the broadcast-body idiom; graves are not previews).

One line to keep: the market just spent two years proving that our exact instincts, mediated seeing, noticing, restraint, and community assembly, are not niche. They are the current shape of viral. We are not chasing this wave; we are already standing in it, with laws.

## ADDENDUM · AMNESIA AND PUPPET COMBO (named by the author; they belong here)
FRICTIONAL (Amnesia, SOMA): the masters of helplessness and of rooms that narrate. Their lessons we already carry: no combat, the environment as the storyteller, notes in human voices. Their lesson we INVERT, deliberately: Amnesia punishes looking at the monster and FNAF makes watching a draining resource, while RESTORATION makes being watched the safety and looking free. The tally contract sits at the intersection of the two canonical camera-horror economies, claimed by neither. And where Amnesia's dark is a resource you hide inside, ours is a room you may stand in but never trust, because the safe hide is the lit one. SOMA's discipline (the story is in the rooms, and the rooms never summarize) is exactly the Ambient Lore Ledger's tradition, executed as objects instead of journal pages.
PUPPET COMBO: the courage of commitment. A lo-fi aesthetic held so absolutely it became a brand, era-authentic UI, short runtimes, one location squeezed dry, and a community grown by consistency. Our CRT-and-wool commitment is the same bet at higher craft: the aesthetic is the identity, and we never break it apologetically. Their brevity lesson lands on the demo: Tape 1 should feel like a complete Puppet Combo-sized night, whole in an evening, honest about wanting more.
The through-line across FNAF, TJOC, Amnesia, Puppet Combo, and the mediated-eye wave: the games that last are the ones with LAWS, kept visibly, until the player trusts the world enough to be afraid inside it. That is the whole doctrine stack, confirmed from five directions.


==============================================================================
SECTION 05 · DESIGN AND SYSTEMS
==============================================================================


------------------------------------------------------------------------------
DOCUMENT 17 · restoration-walkthrough-levels-endings.md
------------------------------------------------------------------------------

## ADDENDUM · THE CASUALTY ROUTES AND THE NEW BOARD (as built, c043)
The board now: 1A (requires Leland intact and five answers under the wear), 1B (always; collects SAINTS, STAFF, and the pencil READER cards as earned), 2 (gains furniture per death: the warm chair, the open headset, the room-administered welcome), 3 (the cold-cobbler variant when Merle is gone), 4a HIS HAND / 4b HER HAND (the fader choice inside the crossing; self-hold pays 13 seconds and an arm), 4c THE COMPLETED SIGN-OFF (via the reading; the break ends itself; the tower light goes out as rest), 0 A ONE-WOMAN SHOW (all four ledgered pre-lockdown; never advertised). Speedpaths for testers: M1 Day 3 consent; H1 any Day 2 break; V1-fast credit then AUTHENTICATE Day 3; V2 cascade night uncredited; F2 three blind calls in premiere; F1 by omission at the divert; L1 five answers then grind wear past 70 then SPACE; L2 carry the fire tape to the dock and Q. The crossing: 75 s base, 62 without Vess, minus 13 self-held; two folds on the honest route.

## ADDENDUM · SPOILER · THE SECRET (c046)
The pilgrimage, in order: earn four clean dailies first (water-damaged stock refuses unready hands), then find W1 in the library's skip gap where 0118 should be (Day 2), which makes W2 exist behind the burn barrel (Day 3), which makes W3 exist on the shed shelf (Day 4, with him awake and the yard between you); each viewing spends one S2 slip, a form for something the ledger will never hold. Then the last preparation: visit the dead room and CONFIRM the radio's dial. Only then does the final break gain a caption no run sheet carries: a radio, through three walls. Take Q, cross inside 75 seconds while he declines to look up, and the eighth ending is ENDING A · AUDIENCE ONLY, and it pays: the sit itself, hearing the premiere run WITHOUT her (the cart deck clearing itself, a blind tally answered by nobody, the breaker held by no hand she knows), the dawn walk, the blank page, Harriet's line as the radio's last words, then the exclusive post-credits PROGRAM GUIDE (NEXT WEEK ON THE GLADHOUSE, five segments the game shows nowhere else, closing on: the guide is never printed, you heard it once), and a permanent mark on the title screen ever after: 58 · STILL ON. Leland's warning, obeyed completely, wins the game he lost. No achievement acknowledges it, which is the acknowledgment.


------------------------------------------------------------------------------
DOCUMENT 18 · restoration-player-routing.md
------------------------------------------------------------------------------

## ADDENDUM · ROUTING THE DEAD (c043)
Every death gate is a routing fork the player can name: the credit dilemma routes Vess's grave by which kindness you performed; the fader routes DEAD AIR's letter; the reading deletes route 4 and writes 4c; comprehensive cruelty converges all premiere routing into 0. The two hides are routing verbs now: cones are safe-idle nodes, the dead room is the one reset node, and every doorway is a 2.2 s toll booth on his graph but not on yours.


------------------------------------------------------------------------------
DOCUMENT 19 · restoration-controls-map.md
------------------------------------------------------------------------------

# RESTORATION · CONTROLS MAP (PC and controller, per context)
Principle: the hands learn the ritual. Inputs are stable across the whole game, holds mean commitment, and every prompt renders the player's ACTUAL binding via the glyph system, per device, always.

## PC (keyboard and mouse) · the shipped Godot map, canonical
MOVE WASD · LOOK mouse · INTERACT E (hold E where noted) · RESPOND SPACE · IMPROVISE Q · TAPE STABILIZER T · MAP M · BINDER TAB · OPTIONS BOOTH O · PAUSE ESC · CROUCH CTRL (toggle) · SEANCE FRAME BACK Z · FRAME FORWARD X.
Context notes: THE BENCH CAPTURE is hold-E for the full take with the beat kept via stillness (ASSIST relaxes both); THE BEAT prompts arrive on SPACE; THE FADER at the divert is SPACE for his hand, E held 4.6 s for hers; THE SPLICE, THE SIXTH LINE, and GET VESS deliberately reuse E, SPACE, and Q so temptation never gets a special button: the ordinary keys are the knife. Remapping (R6) covers the five verbs today (interact, respond, improvise, stabilizer, map) with conflict refusal; the UE5 target is every action remappable including movement.

## CONTROLLER (UE5 target; rows appended to Config/DefaultInput.ini in the port kit)
Thesis: RECORDING IS THE TRIGGER. The capture hold lives on RIGHT TRIGGER, half-press hum optional at Tier B, because holding a trigger for twelve seconds while he crosses the room is the controller's whole argument.
MOVE left stick · LOOK right stick · INTERACT A or Cross · RESPOND X or Square (the beat wants the thumb's fastest reach) · IMPROVISE Y or Triangle · CAPTURE hold RT · STABILIZER LB or L1 · MAP D-pad up · BINDER back or touchpad · BOOTH menu long-press · PAUSE start · CROUCH B or Circle (toggle) · SEANCE FRAMES d-pad left and right · FADER SELF-HOLD hold RT (the same trigger; her arm and the recording share a finger, on purpose).
Rumble doctrine: rumble is a caption, not a sting: the fold ticks twice softly, the cool is a fading pulse, the strike is nothing (death-silence extends to the palms). Gyro aim optional, off by default. Glyphs swap to pad iconography the frame a pad speaks.

## HOLD VERSUS TOGGLE (accessibility contract)
Every hold in the game (capture, fader, stillness) has a toggle equivalent in the booth; toggles preserve the same durations so the contract's arithmetic never changes, only the muscle. No input anywhere requires rapid tapping, chording beyond one modifier, or precision under a quarter second outside the beat, and the beat has ASSIST.


------------------------------------------------------------------------------
DOCUMENT 20 · restoration-accessibility-matrix.md
------------------------------------------------------------------------------

# RESTORATION · ACCESSIBILITY MATRIX (in depth; R1-R7 shipped, this is the full target)
Law: accessibility never breaks canon because canon was built not to need breaking: the dark is readable by doctrine, the one startle is disclosable, and safety is never color alone.

## VISION
TEXT SCALE 0.8 to 1.6, default 1.0, touches every HUD label recursively (shipped). HIGH CONTRAST MAP palette at 5.85:1 (shipped). COLOR REDUNDANCY: the red-means-safe grammar is never color-only: the tally pairs glow with the REC line and countdown, ON AIR pairs lamp with signage text, his eye pairs hue with position and the mains hum; a colorblind verification pass sits in QA. PHOTOSENSITIVITY: TBC and photo-safe modes (shipped) plus a FLICKER AND GRAIN REDUCTION slider in UE5 that tames CRT artifacts without touching lighting truth; the no-strobe law already governs authored content. BRIGHTNESS: none needed and none offered as a fear-dial: DARK IS A ROOM, NOT A WALL is enforced in the lighting bible, so the floor of readability is design, not a slider apology.

## HEARING
CAPTIONS for speech and for meaningful sound events with source tags (shipped: THE BELL, doors, the pen tick), extended in UE5 with left and right directionality tags and a proximity weight so the occlusion presence (S22) has a visual twin. VISUAL BELL option: the once-ever bell also blooms the screen edge once. MONO DOWNMIX toggle. The audio law survives captioning: band-limited sources caption in brackets styled as broadcast, full-range sources caption plain, so even the reading ear learns MEMORY versus PRESENT.

## MOTOR
FULL REMAP on both devices (five verbs shipped; everything in UE5), HOLD-TO-TOGGLE for capture, fader, and stillness with durations preserved, STICK SENSITIVITY and INVERT axes, GYRO optional, ONE-HAND VIABILITY audit in QA (all critical verbs reachable on one side plus movement pauses during bench and seance). No quick-time events exist anywhere in the game.

## COGNITIVE AND PACING
ASSIST widens the beat 0.2 to 0.35 and stretches screening timing 1.5x (shipped) and never gates content or endings. THE SCHEDULE BOARD states today's obligations in one place; toasts queue and never overlap; a TOAST DWELL slider extends hold times. INTERMISSION pauses everything honestly (shipped). The booth opens BEFORE first play (shipped) so nobody meets the dark unconfigured.

## STREAMER AND CAPTURE MODE (from the comparative study)
Compression-kind grain, HUD safe margins, capture-clean toggle that hides spoiler text in the binder, and the bitrate lesson learned from TJOC honored as a launch feature, not a patch.

## CONFORMANCE
The device access pass (hardware, contrast meters, real assistive stacks) remains scheduled with Ciel per the conformance plan; this matrix is the spec it audits against.


------------------------------------------------------------------------------
DOCUMENT 21 · restoration-achievements-design.md
------------------------------------------------------------------------------

# RESTORATION · ACHIEVEMENTS DESIGN v1

## DOCTRINE
Achievements are extradiegetic and therefore dangerous here: a popup is an unscheduled broadcast. Three laws govern them.
1 · THE DEFERRAL RULE. No achievement may surface during a protected beat. Unlocks fire silently into a queue and flush only at two moments: the next morning toast, or the title screen. The glimpse, the fire tape, the premiere, every ending sequence, and the demo card are popup-free zones by construction, not by hope. (Engine shape: an achievements autoload with unlock(id) and a flush gate on night_changed(false) and title _ready.)
2 · THE META-SILENCE LEDGER. The in-game scarcity contracts extend to meta. The glimpse has NO achievement, ever: any ping confirms the moment, teaches hunting, and spends the scarcity twice. The warm unit is acknowledged only through the dock-completion achievement, whose text never mentions warmth. The seance grants one achievement for reaching the final answer, never per-answer pings that turn a wake into a checklist. Chum's name appears in no achievement title.
3 · THE VOICE. Titles and descriptions read in the accession ledger's register: short, procedural, slightly too calm. Hidden achievements (Steam-hidden) cover every ending and every secret; their pre-unlock face is the standard WGLD card.
Demo parity: the demo build ships with achievements disabled entirely, matching the save whitelist's spirit; nothing meta leaks forward either.

## THE LIST (name · description · trigger, mapped to existing state · hidden?)
A01 FIRST SIGNATURE · "The paper takes your name." · first sign_log success · no
A02 CAREFUL HANDS · "A capture, start to bars, in real time." · first clean capture · no
A03 THE SCOPE READS MASTER · "You turned the knob. The label did not care." · first gen knob use · no
A04 ON THE BEAT · "You answered with the room." · on-beat respond in a screening · no
A05 STILLNESS, HELD WHOLE · "The cup did not move." · QUIET stance success · no
A06 MID-MOTION · "You spoke to her during a break. She will resume." · interact with frozen Harriet · no
A07 HOLD YOUR APPLAUSE · "The seventh was a gift." · Harriet's note read (signals_known gains 7th) · no
A08 YOU WERE NOT QUIET · "It changed direction." · first heard-noise relocation · no
A09 TOMORROW'S DATE · "The loops of the R are yours." · presigned_seen · hidden
A10 THE ROWS KEEP THEIR ORDER · "Six units. Filed." · dock_done · no
A11 PER V. CARDONA · "Somebody's name is on something." · vess_credited · no
A12 NO SEARCHER SINGS · "You heard 1974, complete." · merle_1974 · hidden
A13 THE UNFINISHED LINE · "You watched the fire tape to the cut." · fire_tape_watched · hidden
A14 I'VE READ THE ENDING · "You stepped to the last answer." · leland_answers reaches 5 · hidden
A15 ORDER MATTERS · "B before C, the way the panel is labeled." · cascade_done · no
A16 THE LONG WAY AROUND · "The felt door has a key after all." · QUIET ROOM key gained · hidden
A17 INK · "Three entries were possible. One stands." · decision committed · no
A18 NEXT WEEK'S EPISODE · "Starring you." · first run_ended (sheet full or One Take) · no
A19 EMPTY DRAWER · "The loupe was last." · items_lost reaches 7 · hidden
A20 SEALED FOR BROADCAST · "Lock-in's just till air." · lockdown_done · no
A21 THERE'S COBBLER · ending THE BURN · hidden
A22 WELCOME HOME · ending THE NEW PRODUCER · hidden
A23 FILE UNDER: SAINTS · ending SIGN-OFF, Rita closes · hidden
A24 IT'S OKAY. NOBODY'S WATCHING. · ending SIGN-OFF, Leland closes · hidden
A25 SIGNED OFF · ending DEAD AIR · hidden, and its Steam art is the only all-black icon in the set
A26 FULL ACCESSION · "Every document in the building, read." · all D01 to D10 props inspected (needs a read-flags set; small engine delta) · no

## RARITY INTENT AND SHAPE
A01 to A05 are the first hour and should sit near 90 percent. A18 will out-earn several endings and that is correct: dying politely is part of the show. A25 targets low single digits and is never hinted. No grind meters, no percentage bars, no achievement for repetition: the game's verbs are careful, not numerous, and the meta must not teach farming a building that notices behavior.

## ENGINE DELTA (Commit 030 candidate)
achievements.gd autoload: unlock(id) idempotent, user://achievements.cfg, deferral queue with the two flush gates, a plain signal for the eventual GodotSteam setAchievement bridge (id table above is the API names), disabled under DEMO. Prop read-flags for A26. Estimated one commit, no new systems.

## ADDENDUM (c043)
A27 EVERYONE GOES HOME · "The reading was silence." · any ending, empty ledger, zero rows · hidden. A28 A ONE-WOMAN SHOW · "Every part, one performer." · ending 0 · hidden, and its icon is the only card in the set with a name on it. Ruling: ending 4c carries no achievement by design; peace is not a trophy. Ruling: A26 FULL ACCESSION remains at ten documents; the Peak dossier (D11) is extra credit, because completionism should not require waking him.


------------------------------------------------------------------------------
DOCUMENT 22 · restoration-audio-bible.md
------------------------------------------------------------------------------

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

## ADDENDUM · THE TWO VOICES (S20-S24, per the motion-and-sound doctrine)
S20 AF WOOL GROAN: wet felt under load, leather-adjacent, pitched down; plays on direction commits, never on stops. S21 AF ARMATURE: deep metal flex, hull-tick spacing; interior only. S22 OCCLUSION PRESENCE: under 3 m, reverb sends duck and a 200 Hz bloom rises; the room loses a him-shaped space. S23 REC SYNC HUM: faint mains alignment while the tally burns. S24 THE WAKE BLEED: the game's first full-range audio emerging from a band-limited source at the fire tape's end; one use, ever. Governing law restated for the mix chair: BAND-LIMITED IS MEMORY, FULL-RANGE IS PRESENT; no pre-fire asset may ship full-range, no After-Fire asset may ship band-limited, and the strike remains nearly silent under the death-silence rule.

S25 THE LEVER: one dry mechanical click, full-range, close-mic'd intimacy at any distance; plays on every jaw opening, tally-state and telegraph alike; the caption stays [THE JAW WORKS ITS LEVER].


==============================================================================
SECTION 06 · PRODUCTION AND PIPELINE
==============================================================================


------------------------------------------------------------------------------
DOCUMENT 23 · restoration-gap-audit.md
------------------------------------------------------------------------------

# RESTORATION · GAP AUDIT (what is not yet nailed, honestly)
Method: inventory against everything shipped. The headline first, because it deserves the top line: THE DOCTRINE IS COMPLETE AND THE ASSETS ARE ZERO. Every system runs, every law is written, and not one mesh, texture, recording, or note of audio exists yet. That is the correct order for this project, and it is still the elephant.

## CLOSED THIS SESSION
Room-by-room design and personality (the Room Bible, new, grounded in the shipped Rooms.csv). Interactable versus lore versus dressing (the Object Taxonomy, new, with trust laws and QA hooks).

## MECHANICS TO NAIL (with proposed rulings; DECISION marks yours)
1 SPRINT: RULED, none. Walking is the game's tempo; the crossing is the one run and it is scripted.
2 CROUCH: RULED, allowed as a BODY VERB and useless against him BY ARCHITECTURE: his model has no posture channel and no footstep channel, so there is nothing for crouching to fool; you are only quieter because you are slower, and the two-hides law stands untouched. Toggle on Ctrl and pad B, camera lowers 0.6, speed 0.55x, implemented in the spec (c045). Its honest jobs: peeking, reach, and one day the under-stage little door. Invariant I31 and QA-58 guard the promise.
3 THE BINDER AND TIME: proposed ruling: binder and map are true-pause in the day, LIVE-TIME during the premiere only, so the monitor tax exists exactly where pressure should braid and nowhere else. RULED as proposed; premiere live-binder wiring queued with the reaction commits.
4 INVENTORY: ruling proposed as law: THE BINDER IS THE INVENTORY. No grid, no weight; possession is recorded, not managed.
5 DIFFICULTY: RULED, ASSIST only. One game, honestly tuned.
6 PLAYER DEATH PRESENTATION: stays the single card (NEXT WEEK'S EPISODE) with no per-location variants; variety would make dying content. Reaffirmed.
7 SAVE MODEL: RULED and reaffirmed: stations plus signatures only, no autosave; the signature IS the save.
8 PHOTO MODE: RULED, Tier B studio-safe (day, never him). Graves are not previews.
9 NEW GAME PLUS: PARKED by the author's word; PREMIERE+ stays a named concept and nothing more for now.
10 INTERACTION FEEL: reach 2.1 m, 35-degree cone, no outlines ever; final numbers await the device pass.

## TECHNICAL GAPS
UE5 constructor beyond greybox (doors, stations, props from data). Godot .translation registration note for localized builds. ObjectDB teardown on quit. Four-hour soaks on target hardware. Save-migration policy once v17 exists.

## ART AND AUDIO GAPS (the asset ledger, all open)
Environment concepts for all twenty rooms (the Room Bible is now their brief). Chum stage fabrication, scan, and both rigs. Every S-slot S01 to S24 unrecorded. The show's music: jingles, the theme, and the end-credits piece are undoctrined; note that nearly all score is diegetic by law, so the music gap is small and specific. Key art comps beyond the dossier.

## PRODUCTION GAPS (owner: Ciel unless marked)
Playtest verdicts V1 to V7. Gate 0 signatures and Memos 1, 3, 4. Device access pass scheduling. Puppet fabrication RFQ. A SCHEDULE AND BUDGET DOCUMENT DOES NOT EXIST: no timeline, no cost model, no milestone dates anywhere in the kit; proposed as the next build-side document once engine work begins in earnest.


------------------------------------------------------------------------------
DOCUMENT 24 · restoration-blender-ue5-pipeline.md
------------------------------------------------------------------------------

# RESTORATION · BLENDER TO UE5 PIPELINE v1
Ruling recorded: the production build is UNREAL ENGINE 5, assets authored in BLENDER, per the author. The Godot build stands as the executable specification (it runs; see docs/telemetry/first-boot). Spike 2 is no longer a veto, only a routine perf validation on target hardware.

## DIVISION OF LABOR
BLENDER: modeling, UVs, rigging (Chum's jaw lever, sockets), scan cleanup and retopo, fixture meshes with true bulb geometry. UE5: materials, lighting, assembly, gameplay, sequencing. SCAN-FIRST stands from the art bible: the fabricated stage Chum is photographed and photogrammetried; Blender cleans and retopos; the material library is born from his wool and travels outward. The after-fire body is a digital kitbash of the scanned materials plus a hardware library; no second hero fabrication.

## STANDARDS (so nothing is renegotiated per asset)
Units: Blender scene in meters, FBX export with the UE preset so 1 m lands as 100 uu; UE is X-forward, Z-up; verify once on a 1 m cube and write the result on the wall. Naming: SM_ static, SK_ skeletal, M_ or MI_ materials, T_ textures with _BC _N _ORM suffixes; collision as UCX_ children in Blender so import is automatic; sockets SOCKET_JawLever, SOCKET_EyeTally, SOCKET_Bell (clapperless). Textures: ORM packed; 2K default, 4K only for Chum and the readables. LODs: crafted-world polycounts are modest by doctrine; LOD1 for set dressing only, hero props none.

## MATERIAL MASTERS (parents in UE, parameters named per the art bible)
M_Wool (subsurface, sodium-honest), M_TapeStock, M_Phosphor (emissive hybrid for monitors), M_Paper (the readables' stocks), M_Enamel (panels; where the pin fuses), M_Practical (fixture glass). The SODIUM CHECK is a permanent Blender lookdev scene: one sodium-spectrum lamp, neutral floor; every material passes through before export. If it lies under sodium it does not ship: the same gate as always, now with a fixed address.

## VERSIONING AND FLOW
Binary .uasset means the repo gains git LFS for Content (or the project moves to Perforce at Tier B; decide at Gate 0 signing). The port kit's Data CSVs remain the single source for rooms, doors, and timings: the level is BUILT FROM DATA in UE exactly as in Godot; build_greybox.py already proves the pattern and grows into the real constructor. Import automation extends that script: batch FBX import with the naming rules enforced, so the pipeline complains instead of the artist remembering.

## ADDENDUM · ANIMATION EXPORT (per the motion-and-sound doctrine)
Two skeletal pipelines: SK_Chum_Stage ships with cloth and secondary physics enabled; SK_Chum_AfterFire ships with all physics secondaries disabled and stiff-baked wool, root-motion clips only, the fold authored as one montage per door width, and the eye on an always-on aim layer. Curve discipline is checkable at review: stage clips ease-heavy, AF clips linear-dominant with two-frame caps.


------------------------------------------------------------------------------
DOCUMENT 25 · restoration-gate-0-packet.md
------------------------------------------------------------------------------

# RESTORATION · GATE 0 PACKET
Four decisions, drafted for signature. Per the build plan, M0 cannot open until these are signed, and nothing in this packet can be signed by anyone but the project's owner. Everything below cites evidence already in the repo; nothing requires new research, only a pen.

## FIRST 90 MINUTES (before signing anything)
Unzip restoration-godot-v0.9-complete.zip. Godot 4.3+, Import, F5. Play title to any ending without documents open. Then fill the playtest protocol's seven verdicts (docs/production/restoration-playtest-protocol.md, Section 2), each one sentence. Verdicts V1 (the wool) and V7 (which ending, and why) directly inform Memos 1 and 4 below. Ninety minutes of play is worth more to this project right now than ninety more artifacts.

## MEMO 1 · SCOPE TIER
The plan's tiers: A solo (24 to 32 months, 60 to 180k), B baseline (4 to 6 people, 18 to 20 months, 700k to 1.4M), C funded. Evidence for the decision: the v0.9 prototype proves the systems are buildable solo at greybox; the art bible's scan-first pipeline and the fabrication brief's 25 to 60k puppet are Tier A survivable but Tier B comfortable; the audio bible's session plan assumes at least contract talent. Honest tradeoff: Tier A ships this game in roughly three years with your evenings; Tier B ships it in under two with your judgment multiplied. The demo flag means either tier can market early.
DECISION (circle one): TIER A · TIER B · TIER C · signed ________ date ________

## MEMO 2 · ENGINE
Evidence: the Godot prototype at v0.9 (27 commits, every system, the harness); the spike status board (5 and 7 substantially retired, 2 hardware-bound); docs/unreal-5/UE5-MIGRATION-MAP.md as the port checklist. The plan's guidance stands: Unreal 5 if Tier B hires experienced 3D contractors; Godot if Tier A, accepting the stylization tradeoff, which the Crafted World doctrine arguably converts into a strength. Run Spike 2 (twelve feeds at 60 fps) on your hardware before signing; it is the only spike that can veto Godot.
DECISION: GODOT 4 · UNREAL 5 · (contingent on Spike 2: Y/N) · signed ________ date ________

## MEMO 3 · RELEASE MODEL
Evidence: the demo cut plan and Commit 027 (the demo is one flag away today); the Steam page draft; the trailer beats. The plan's recommendation: boxed release, Tape 1 free demo, save carry. The chaptered variant remains costed in the plan at plus three months and a live-ops seat.
DECISION: BOXED + FREE TAPE 1 DEMO · CHAPTERED · signed ________ date ________

## MEMO 4 · THE SHOW FOOTAGE
The plan's one flagged unsafe choice: build Chum for real. Evidence: the fabrication brief is RFQ-ready with the caliper tell-table; the art bible makes the puppet the material library's source; the key art brief and trailer beats both assume photographed plates; the ARG plan spends the puppet twice more. The alternative (in-engine footage with an artifact pass) saves 25 to 60k and costs the plot's load-bearing authenticity plus the entire marketing spine. Verdict V1 from your playthrough is this memo's evidence: if the wool shader already convinces you under sodium, the in-engine path gains a real argument; if it does not, the puppet was always the answer.
DECISION: FABRICATE (issue the RFQ) · IN-ENGINE FOOTAGE · signed ________ date ________

## ON SIGNING
Signed memos go in docs/ as gate-0-signed.md. M0's remaining exit items then read: Spike 2 result, the soak scorecards, puppet quotes requested, Merle breakdown released, and the greybox walk, which v0.9 already exceeds. Week one of the plan's first thirty days is, as of this packet, complete on paper.

## ANNOTATION (Session 67)
Memo 2 is decided by the author's word: UNREAL 5, assets in BLENDER; the Godot prototype stands as executable specification (first boot clean, see docs/telemetry). The signature line remains for the record. Spike 2 reframes as routine perf validation. Memos 1, 3, and 4 remain open.


------------------------------------------------------------------------------
DOCUMENT 26 · restoration-playtest-protocol.md
------------------------------------------------------------------------------

# RESTORATION · PLAYTEST PROTOCOL v1
Build under test: Godot prototype v0.5 (commits 001 to 020). Owner: Ciel.
Purpose: convert playthrough hours into tuning decisions with named knobs.
Two modes: SELF (you, now) and EXTERNAL (testers, later; spoiler tiers below).

## 0 · SETUP
- Godot 4.3+, import the project folder, F5. Boots to title.
- Save file: user://transmitter_log.json (Godot: Project > Open User Data Folder).
- Full reset: NEW GAME from title. Migration test: copy an older commit's save in first, then CONTINUE; expect a MIGRATION toast, no crash.
- Controls: WASD, mouse, E interact, SPACE respond, Q improvise, T TBC, TAB binder, M map, Z/X seance frames.
- Record: timestamped plain notes. Format: [hh:mm] WHERE · WHAT · FELT. One line each. Do not tidy while playing.

## 1 · SESSION STRUCTURE
RUN 1 · THE COLD RUN (60 to 120 min): play title to any ending without this document open. Note only what pulls you out or pulls you in. Which ending you reach first is itself a datum: write it down before reading Section 3.
RUN 2 · DIRECTED PROBES (60 to 90 min): work Section 4 in order, skipping anything Run 1 already answered.
CLOSE: fill the report template (Section 8) same day. Memory of feel decays overnight.

## 2 · THE SEVEN STANDING VERDICTS
Each has: do, observe, anchors, and the knob it tunes.

V1 · WOOL SPIKE UNDER SODIUM. Do: stand at the bench, look at Chum on the tape stage; also the dock units. Observe: does the surface read as fiber or as fuzzy plastic? Anchors: 1 plastic, 3 acceptable greybox, 5 I want to touch it. Knob: shaders/wool.gdshader (fresnel strength, wrap term).
V2 · THE HOLD. Do: run a capture, watch the monitor through the final 3.2 seconds. Observe: does dread peak during the stillness before the lunge, or only at the lunge? Anchors: 1 lunge does all the work, 3 hold registers, 5 I wanted to look away before the lunge. Knobs: scripts/tape_stage.gd (approach speed 1.35, hold window 0.78 to 0.12, lunge scale 1.45).
V3 · ARTIFACT LOUDNESS AT GEN 0. Do: gen knob to MASTER, watch idle tape 20 seconds, TBC off. Observe: is the image damage distracting at the cleanest setting? Anchors: 1 unreadably noisy, 3 texture, 5 invisible until pointed at. Knobs: shaders/crt_tape.gdshader (noise floor 0.03 base, chroma 0.0012 base, band 0.16 factor).
V4 · TBC FEEL. Do: toggle T while watching tape. Observe: does TBC-on still feel like tape, or like turning the horror off? Anchors: 1 sterile, 3 steadier tape, 5 same world, calmer hand. Knob: the 0.7 steady factor in crt_tape.gdshader.
V5 · DIRECTOR READS EARNED. Do: one night living on monitors, one night sprinting, one night freezing near it. Check binder read each morning; note which blocking variants you saw. Observe: did consequences feel caused by you? Anchors: 1 arbitrary, 3 plausible, 5 it knows me. Knobs: scripts/coverage_director.gd thresholds; rundown warn 7/5, reach 2.2/2.6.
V6 · LELAND'S CROP. Do: open the seance, step to frame 7. Observe: does the frame-edge figure read as cropped by the frame, or as a prop standing at the side? Knob: tape_stage leland x 1.35 and camera framing.
V7 · FIRST ENDING REACHED. Record which, and why you chose that ledger entry. No knob; this is design telemetry.

## 3 · ENDING MATRIX SPEEDPATHS (for Run 2)
- Burn: decision DESTROY, four assets, night, sleep.
- New Producer: AUTHENTICATE path; afterward confirm the title reads NEW EPISODE exactly once, then reverts next launch.
- 1A: PERFORM with all five seance answers and wear at or under 70. 1B: PERFORM without.
- Dead Air: PERFORM holding the quiet room key, five answers, fire tape watched; take Q at the final break.
Verify each ending sets the objective line to ENDING REACHED and that CONTINUE resumes sane.

## 4 · DIRECTED PROBES
P1 Paper economy: burn all three S1 sheets by repeated signing; confirm the OUT OF PAPER state and that respawn falls back correctly.
P2 Capture abort: start a capture, walk past 4 meters; expect abort, tape stops with you, no daily minted.
P3 Retake presentation: take a strike; confirm slate, timecode rewind, item loss order (watch first, loupe last), respawn at last signed station.
P4 One Take: switch mode in the binder form, take one capture; expect the full NEXT WEEK'S EPISODE ending and morning-after CONTINUE.
P5 Dailies: mint two dailies, carry one to the climate room; confirm single-carry rule and that burning resets the Director read (binder shows AUDIENCE).
P6 Presigned page: Day 2+, first S4 interaction; confirm the three beats, no paper spent, signature listed.
P7 Dock: complete the count; confirm exactly one warm unit, no follow-up event ever, card appears in props crate only after filing.
P8 Floor Manager: at night on air, look at him inside 9 m; hold still 3 s (take holds), repeat next night and move (take spoiled). Confirm he is absent during breaks and the premiere.
P9 Night trip: fresh save, first night; at ~20 s expect the breaker beat once, never again on that save.
P10 Glimpse: Day 4 night, fire corridor elbow; after it fires, quit, relaunch, revisit; confirm it never refires.
P11 Lockdown: with four assets, at nightfall; confirm monitor sync, sealed exterior doors persist after reload, chairs in rows and staying in rows.
P12 Screening stances: hit SPACE deliberately off beat once, on beat once, improvise late once, and do one perfectly still QUIET; confirm all five outcome lines are reachable.
P13 Vess chain: skip the binder entirely on one run; confirm the blackout retake variant. Credit him on another; confirm the credited line.
P14 Merle doorway: raise the pen and wait; confirm she walks to the doorway and says nothing until ink is down.
P15 Map truth: with M open, walk three rooms; confirm outlines match walls and the dot never exits geometry.
P16 Seance knob: dial 3RD GEN, scrub five frames, close the reel; confirm the picture returns to 3RD GEN, not MASTER.

## 5 · FAIRNESS INVARIANTS TO WITNESS (from the build plan)
While playing, flag any violation as S1 minimum: warning always precedes reach (except at three strikes, by design); no strike through walls or during ON AIR camera coverage of the premiere; no scare during the forced fire tape; the glimpse never repeats; the warm unit never acts; every locked door states its reason; aborting capture never costs a daily; the divert window only appears when earned.

## 6 · SEVERITY AND TRIAGE
S0 crash or save corruption. S1 invariant violation or ending unreachable. S2 system misreads (Director, stances) or presentation break. S3 polish. File as: [S#] probe id · repro steps · expected vs got. S0/S1 jump the commit queue; S2 batches; S3 waits for its system's pass.

## 7 · EXTERNAL TESTER VARIANT
Tier A (spoiler safe): Run 1 cold plus probes P1 to P5, P15. Tier B (mechanics spoiled): P6 to P13. Tier C (story spoiled): Section 3 matrix. Never hand Tier C to a first-time player. Ask externals only V2, V3, V4 of the verdicts; the rest are author calls.

## 8 · SESSION REPORT TEMPLATE
Date / build zip name / mode (Matinee, Late Night, One Take) / TBC on or off.
Run 1 ending reached and why. Three moments that worked. Three that broke or bored.
Verdicts V1 to V7: score plus one sentence each.
Probes attempted / passed / failed (ids). Issues filed (ids with severity).
One tuning decision you are ready to make today. One question for the next build.

## 9 · DREAD LEDGER QUICK PASS (optional, end of session)
Score 1 to 5 per domain from the rubric: Fear Architecture, Player Truth, World Coherence, Systemic Honesty, Craft Surface, Sound, Performance Feel, Endings Weight. The prototype gates at 3.7 average for M-milestone purposes; note the two lowest and stop there.

## ADDENDUM · PROBES P17-P26 (the after-fire and the ledger)
P17 During your first lit approach, what did you look at: the countdown, the eye, or him? P18 Did the fold read as fair counterplay or as leash? P19 First cool: did the teaching line change your next capture's setup? P20 Did you find the dead room before or after you needed it? P21 Which Vess kindness did you perform, and did you feel the other grave open? P22 At the fader: whose hand, and how long did you hesitate? P23 The crossing: reached, caught, or late, and was late's consequence legible? P24 Did any death feel unauthored (random) rather than signed? Name it if so; that is a design failure by Law 7. P25 Did the ledger reading at credits land as accounting or as accusation? P26 If you got A27: did clean hands feel chosen or accidental?


==============================================================================
SECTION 07 · QA AND VERIFICATION
==============================================================================


------------------------------------------------------------------------------
DOCUMENT 27 · restoration-qa-regression.md
------------------------------------------------------------------------------

# RESTORATION · QA REGRESSION SCRIPT v1
Run whole on any release candidate; run the touched sections after any system commit. Every line is action, then expected. Failures file as QA-nn against the commit under test. Companion to the invariant suite (automated) and the playtest protocol (feel); this script is neither, it is the mechanical truth pass.

## A · BOOT AND TITLE
QA-01 First launch, no settings file: the booth opens over the title with the BEFORE THE SHOW banner; closing writes settings; relaunch does not re-prompt.
QA-02 Tab through the title: every button shows the phosphor focus ring; Enter activates.
QA-03 CREDITS from title: crawl runs, any key after grace skips, tower-light card holds, returns to title.
QA-04 With unshown achievements pending: title shows FILED WHILE YOU WERE OUT exactly once.

## B · CORE LOOP
QA-05 Sign S1: paper decrements by one, save writes, pen-tick caption appears when captions on.
QA-06 Capture: 12 real seconds, status counts down, A CLEAN SIGNAL logs, bars play.
QA-07 Die with items: retake presentation lists losses in order; loupe is lost last of the seven.
QA-08 Run death (sheet full or One Take): NEXT WEEK'S EPISODE · STARRING RITA IVORI, then straight to title, no credits.

## C · SCHEDULE AND HOUSE
QA-09 BREAK: Harriet freezes mid-motion; interacting yields her line; cup height strictly rises across tapes.
QA-10 Window holds honored except during cascade; ON AIR clock and hum agree.
QA-11 Coat pegs drift per day table; Merle is at kettle, chair, or DOORWAY per schedule and pen state, never elsewhere.

## D · THE HUNTER
QA-12 Warn at 7 m fills ledger line; strike at 2.2 m; third strike triggers savoring, not instant.
QA-13 Make noise behind it: within 12 s it relocates toward the noise and the It-changed-direction line fires once per run.
QA-14 On-camera check: standing in an active camera cone prevents the strike; patchbay revive works.

## E · SYSTEMS AND BOOTH
QA-15 Map on M: sealed rooms dashed, station dots labeled, footer shows the BOUND map key.
QA-16 Booth: every slider and check persists across relaunch; NEW GAME leaves settings intact.
QA-17 Remap RESPOND onto E: refused with KEY IN USE; remap onto an unused key: prompts everywhere show the new key.
QA-18 ASSIST on: beat window visibly forgiving, premiere clocks half again longer, holding E passes both stillness checks.

## F · NIGHTS AND EVENTS
QA-19 Night 1 trip fires once ever; Floor Manager watch fails on movement, passes on assist-hold.
QA-20 Night 4+: circuit C then B; restoring out of order refuses with B before C; waived window holds during.

## G · STORY GATES
QA-21 Day 2+, S4 with zero paper: the presigned page appears and saves free, once.
QA-22 Crate before seance: seance refuses; after: wear ladder degrades generations per answer.
QA-23 Fire tape: forced watch, no sting anywhere in it; watching marks the flag.
QA-24 Dock: filing all six completes with nothing following; the warm one never acts, on camera or off.
QA-25 Day 4 unseal: the once-ever moment can occur exactly once per save, and never again after.

## H · FINALE
QA-26 Lockdown: monitors sync, doors read SEALED FOR BROADCAST, rec chairs tween to rows and persist.
QA-27 Premiere: cue marks require the PGM camera; each incident type fail-forwards within its guarantee.
QA-28 Divert at the final break with the fire tape: DEAD AIR path plays; otherwise the committed decision's ending plays; ending exits roll credits.

## I · META AND MODES
QA-29 No achievement toast ever appears between title and morning; morning shows FILED lines.
QA-30 DEMO true: only the seven rooms open, doors carry demo reasons, bed declines, S1 and S5 only, card protects three seconds, completed demo save contains none of the whitelisted-out fields, funnel file has six marks.
QA-31 Load a v15 save into this build: migration toast, nothing lost; settings file untouched.
QA-32 Pause anywhere unlocked: world and clocks hold, audio mutes; pause during any authored sequence: refused.

## J · THE AFTER-FIRE (added post-c036)
QA-33 Watch the fire tape: the wake toast fires once; af_active persists across save and load.
QA-34 Start a capture with him awake: he approaches at walking-dread pace, footsteps thunk on interval, and the HUD reads REC · SAFE WHILE LIT with a live countdown; at 1.2 m he stops and the first-sighting toast fires exactly once per save.
QA-35 The eye: red glow ONLY while a capture runs; dark the instant it stops or aborts.
QA-36 Let the tally die with him adjacent: THE TALLY COOLS, then a strike; let it die with distance: he withdraws to his segment. First cool ever runs 4.0 s with the teaching line; every later cool runs 2.0.
QA-37 Doorways: every threshold costs him 2.2 s, captioned, in the capture approach AND the night hunt; a route through two doors buys 4.4 s, verifiably.
QA-38 The dead room: noise made inside registers nowhere; he tracks to the felt door, holds, says his line once; first entry gives the radio toast and [NO ECHO].

## K · THE CASUALTY LEDGER (added post-c043)
QA-39 Binder page one: NO ENTRIES. KEEP IT SO. until a death; then who, cause, day, epitaph per entry.
QA-40 M1: refusing Merle at the fire tape saves her and never re-offers; consent plays the repossession, the kettle caption, and she is absent everywhere after; THE BURN and NEW PRODUCER play their variants.
QA-41 H1: the slip arms only Day 2+ while frozen; taking it grants exactly one paperless signature that toasts in her hand; the next break plays the absence and the cabinet; the seventh signal is unlearnable if her card was unfound; screenings judge 0.05 tighter.
QA-42 V1: AUTHENTICATE while credited plays the all-monitors taking after the INK ripple; alternatively the credited living die at the final breaker AFTER the farewell, lights held. V2: GET VESS appears only for the uncredited who used the insight; taking it fixes both circuits then plays circuit F. Dead, the breaker is the pin plus the hard blackout, and the crossing runs 62.
QA-43 F2: exactly the third blind tally call; the unlisted-camera beats; cue flow continues after. F1: the fader choice precedes the crossing; self-hold costs 13 s and routes 4b; his hold routes 4a with the casualty marked inside the epilogue; if he is already dead, self-hold is forced.
QA-44 L1: offered only past five answers AND wear above 70; the ink-drain beats; the dock inert forever; 1A unreachable; 1B shows the pencil card. L2: offered whenever the fire tape is held; consumes it, empties answers, sets the completed sign-off; the final break then plays 4c with no divert prompt.
QA-45 ENDING 0: with all four ledgered before lockdown, the premiere intercepts at entry; credits show nine cards, one name; A28 files at the next flush gate.
QA-46 Rows: every timed incident that expires takes a seat, cycling its three lines with the caption; the count persists.
QA-47 Every ending's credits open with THE LEDGER, READ ALOUD when anything is in it, including fifty-eight minus N; a clean run reads nothing and A27 files.
QA-48 Demo build: no death is reachable, no casualty field survives in the save, achievements stay dark.
QA-49 H2: after the rejected viewing, the block offers the splice with the label disclosed; performing it mints a daily immediately and the NEXT break doubles her; she persists on set as scenery with one line forever; the double rebuilds after save and load.
QA-50 Seance grief: with Harriet dead, frame 14 reads PAUSED PROPERLY; with Merle dead, frame 28 reads SHE'S HERE NOW; every reading that names Harriet also carries TRANSITION UNRESOLVED.
QA-51 Braid audit: at every premiere pressure peak, at least two simultaneous attention demands share the clock; single-threaded peaks are filed as tuning defects.
QA-52 The fold is one authored montage timed at 2.2 s per door width; head arrives last; no procedural blending.
QA-53 After-Fire zero-secondary sweep: no jiggle, cloth, or idle sway on the AF body in any state; the eye is the only articulation during stillness; the performance quote (frontal square plus fifteen-degree tilt) occurs only while the tally burns.
QA-54 The audio law holds: every pre-fire source band-limited, every AF source full-range with the throat speaker's band-limited room tone as the one standing inversion; the jaw opens only via the two-beat self-operated act (tally-state lever work, and the single pre-strike telegraph with its 0.9 s beat); it never syncs to sound; the bell never sounds; no vocalization exists; the wake bleed occurs exactly once per save.
QA-55 Prompt discipline: nothing ambient prompts; everything that prompts is stable across the run.
QA-56 Drift audit: every drift instance resolves to the dressing tier; interactables and lore never move.
QA-57 Hero census: no room carries more than one hero interactable.
QA-58 Crouch honesty: toggling crouch changes camera height and speed only; hunter coverage, relocation, and noise attribution are byte-identical between a walking and a crouch-walking soak; no prompt, hint, or text ever implies crouch conceals.
QA-59 Ambient ledger audit: every item in the Ambient Lore Ledger exists in its room, prompts nothing, never moves, and reads at all three depths; any graduated statement of a protected truth is an S0.
QA-60 The unnumbered reels: W1 in the skip gap (Day 2); W2 exists only after W1 (Day 3); W3 only after W2 (Day 4); each first viewing requires four dailies logged and consumes one S2 slip with refusal lines otherwise; re-reads free; nothing announces on completion; A26 counts only the D series.
QA-61 AUDIENCE ONLY: the radio caption fires only with all three reels watched AND the dial confirmed at the dead room radio (which appears only after W3); Q within six seconds starts the 75 s run; reaching the dead room routes ending A with her single credit card; declining or arriving late falls through to the normal break chain untouched; no achievement exists for this ending by design; the post-credits program guide plays for this ending only; the title screen carries 58 · STILL ON on every later launch.


------------------------------------------------------------------------------
DOCUMENT 28 · restoration-invariant-suite.md
------------------------------------------------------------------------------

# RESTORATION · INVARIANT SUITE v1
Per the build plan: each law, its test, its telemetry. Format per entry: LAW (the rule as fiction states it) · TEST (manual probe id from the playtest protocol, or soak assert) · TELEMETRY (the artifact that proves it in the wild) · STATUS (ENFORCED = the code cannot violate it; TELEMETERED = violations would be logged; MANUAL = probe-only for now). Any violation files at the protocol's severity S1 unless noted S0.

## A · GRAMMAR (the thing keeps the rules)
I01 Warning precedes reach. LAW: the Rundown warns inside its radius before any strike, except at three sheet lines, where silence is the design. TEST: soak assert on warn-then-strike ordering; probe V5 nights. TELEMETRY: coverage_log relocation and kill lines plus a strike-event line (harness adds). STATUS: ENFORCED (radius ordering), TELEMETERED partial.
I02 No strike through walls. TEST: soak with wall-adjacent bot; assert strike only with clear segment path. TELEMETRY: harness raycast log. STATUS: MANUAL (radius is spatial; wall check is harness work).
I03 The premiere yields the floor. LAW: the Rundown never hunts while the show is live. TEST: probe during PERFORM. TELEMETRY: absence of coverage_log hunt lines during premiere_log activity. STATUS: ENFORCED (premiere guard).
I04 Window holds obey the clock, and yield only to the cascade. TEST: probes P11 and cascade run. TELEMETRY: liveness_log "window holds waived" lines exist only while cascade_active. STATUS: ENFORCED.
I05 On camera is safe. LAW: no harm lands while the player is program on a live covered mark. TEST: soak in premiere with strikes forced. STATUS: ENFORCED by I03's guard at prototype grain; re-verify when hunting and premiere ever coexist.

## B · MERCY AND FAIRNESS
I06 Fail-forward finale. LAW: a cue can always be re-entered; no incident hard-blocks. TEST: fail every cue three times (protocol Spike 7 soak); leave every incident unfixed. TELEMETRY: premiere_log RESOLVED lines with "club auto-fix" at or under 40s; tally refusals never exceed 2; boom holds exactly 1. STATUS: ENFORCED + TELEMETERED.
I07 Cascade liveness. LAW: the panel is always reachable during the cascade. TEST: cascade run with doors deliberately closed. TELEMETRY: liveness_log OK cadence every 5s; VIOLATION line on breach. STATUS: ENFORCED + TELEMETERED.
I08 Every locked door states its reason. TEST: sweep all doors each build (probe P15 extension). TELEMETRY: none needed; the reason is the UI. STATUS: ENFORCED by data (locked_reason strings), MANUAL sweep for empty strings.
I09 Abort never costs a daily. TEST: probe P2. STATUS: ENFORCED.
I10 The presigned page costs no paper. TEST: probe P6. TELEMETRY: save diff shows signature added, paper unchanged. STATUS: ENFORCED.

## C · SCARCITY CONTRACTS (the once-evers; violations are S0)
I11 The glimpse never repeats. TEST: probe P10 including relaunch. TELEMETRY: glimpse_seen flag in save; harness asserts single spawn per save lifetime. STATUS: ENFORCED.
I12 The warm unit never acts. LAW: nothing follows, ever. TEST: probe P7 plus a full-run tail watch. STATUS: ENFORCED (no code path exists; keep it that way: this invariant is a review rule on future commits).
I13 The interface lie is spent exactly once. TEST: reach Ending 2, relaunch twice. TELEMETRY: lie_pending flips in save. STATUS: ENFORCED.
I14 One startle in the whole game. LAW: the Scare 1 lunge is the only startle-class event. STATUS: review rule + audio bible stinger policy; harness greps event table per build.
I15 The fire tape carries no sting; chairs make no nameable sound; the Floor Manager is never heard moving. TEST: silence-ledger audit per audio pass. STATUS: ENFORCED now (no audio exists to violate); becomes an asset-review gate.

## D · ECONOMY AND STATE
I16 Item loss is ordered and bounded. LAW: dresser order fixed, loupe last, losses persist through run end. TEST: probe P3 plus run-end CONTINUE. STATUS: ENFORCED.
I17 Sheet retirement is honest. LAW: run end zeroes strikes, keeps losses, mints no daily. TEST: probe P4. STATUS: ENFORCED.
I18 Lockdown is permanent. LAW: sealed doors, synced monitors, rowed chairs survive reload. TEST: probe P11 with relaunch. STATUS: ENFORCED (state re-applied on ready).
I19 The dock card gates on the filed inventory; the seance gates on the crate; the divert gates on key plus answers plus the fire tape. TEST: matrix probes (Section 3 of the protocol). STATUS: ENFORCED.

## E · DETERMINISM
I20 The same frame is always the same frame. LAW: seance frame idx renders identically forever (seeded grain). TEST: capture frame 14 twice across relaunches, diff. STATUS: ENFORCED (seed = f(idx)).
I21 The Director is deterministic and explainable. LAW: identical inputs yield identical profiles, and every blocking decision carries a reason string. TEST: input-replay diff (Spike 5). TELEMETRY: coverage_log. STATUS: TELEMETERED; replay harness is machine-side.
I22 Heard noise is attributable. LAW: every relocation-toward-noise names its cause. TELEMETRY: coverage_log "RELOCATE toward heard noise" with position. STATUS: ENFORCED + TELEMETERED.

## F · THE HARNESS PLAN (machine-side)
Headless Godot runner with three bots: WANDERER (random legal movement), CHECKER-BOT (monitor camping), FAIL-BOT (premiere: ignores every incident, fails every cue thrice). Runs: 4-hour night soak (I01, I02, I21), full-run matrix per ending (I13, I16 to I19), premiere soak (I03, I05, I06). Parsers over coverage_log, liveness_log, premiere_log emit a single INVARIANTS.txt scorecard per build. CI cadence: every zip before it is handed to a tester; the scorecard staples to the milestone gates (3.7 / 4.0 / 4.2) alongside the Dread Ledger.
Filing: violations use the protocol's severity language; S0 (scarcity contracts, save corruption) stops the line.

## ADDENDUM · INVARIANTS I23-I30 (the after-fire and the ledger)
I23 NO STRIKE WHILE LIT · law: recording true forbids GameState.strike from the hunter · test: soak bot captures with him adjacent for 10 minutes · telemetry: any AF strike log line during recording is S0.
I24 THE FOLD IS PAID · law: no AF door transit without the 2.2 s hold · test: position-delta audit across door radii in the coverage log.
I25 DEAF TO THE DEAD ROOM · law: noise events originating inside the bounds never alter his heard-state · test: bot signs and slams inside; his target must not move.
I26 ONE COOL TEACHES · law: the 4.0 s cool occurs at most once per save · telemetry: grep the teaching line count.
I27 DEATHS ARE IDEMPOTENT · law: mark_casualty for a taken name is a no-op; no double entries, no double toasts · test: force both Vess triggers in sequence.
I28 THE LEDGER NEVER LIES · law: every epilogue reading matches the binder page exactly, names and causes · test: string-compare at credits.
I29 CLEAN HANDS ARE SILENT · law: zero casualties and zero rows produce no reading and file A27 once · S0 if any reading text appears on a clean run.
I30 META-SILENCE HOLDS AT SCALE · law: no death, ending 0 included, produces a mid-play achievement toast; the once-ever moment still has no entry anywhere new · build check extended over the casualty files.

I31 CROUCH DOES NOT HIDE. Law: no hunter or director code path reads player posture; no footstep channel exists to muffle. Test: grep-level audit plus a soak with a crouch-walking bot showing identical coverage response. Crouch is a body verb; concealment remains the two hides only.


------------------------------------------------------------------------------
DOCUMENT 29 · FIRST-BOOT.md
------------------------------------------------------------------------------

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


==============================================================================
SECTION 08 · MARKETING AND PRESS
==============================================================================


------------------------------------------------------------------------------
DOCUMENT 30 · restoration-steam-page-draft.md
------------------------------------------------------------------------------

# RESTORATION · STEAM PAGE DRAFT v1 (private until Gate 0 signs)

CAPSULE TAGLINES (pick one)
A) The show never ended. You were hired to finish it.
B) Restore the tapes. Respect the schedule. Say goodnight.
C) Some archives keep you.

SHORT DESCRIPTION (under 300 characters)
You are the conservator hired by a fan club of gentle retirees to restore a lost 1970s kids' show. The masters burned in 1977. The tapes you are holding are dated after the fire. Archival horror about broadcast grammar, careful hands, and a puppet that keeps the rules better than you do.

ABOUT THIS GAME
WGLD Channel 58 has been dark for fifty years, except it has never once been dark. The 58 Club, the sweetest people you will ever fear for, have hired you to authenticate fragments of The Gladhouse, a puppet show whose creator burned every master and whose sign-off was cut before it finished. A show that never ended does not stop airing. It recurs.
Restoration is slow-burn archival horror where the safe place is on camera and the monster is the format itself. Work the bench by day: capture in real time, read spectrograms, log every reel in a paper ledger where saving your game costs a signature. Survive the schedule by night: the halls run segments to no one, warnings come as hand signals, and the thing that walks has never broken broadcast grammar, which is the only mercy it offers.
Features:
- A save system with a paper cost and a monster that reads how you play, then re-blocks its scares to fit.
- The tape world: per-generation VHS artifacting as a live, diegetic toolset. Your time-base corrector is both an accessibility option and a plot-critical instrument.
- A seance conducted frame by frame, where every step wears out the only copy of a man.
- Four endings, one decision in ink, and a finale performed live on camera, cues, sabotage, retakes and all.
- The 58 Club: people to protect, believe, doubt, and grieve. There is always cobbler.

DEMO POSITIONING: Tape 1 ships free as the demo, ending on the in-tape lunge and the lit RESPOND sign. The demo save carries into the full game, ledger and all.

TAGS: Horror, Psychological Horror, Investigation, Story Rich, Atmospheric, First-Person, Immersive Sim, Retro, 1970s, Singleplayer.
CONTENT NOTES: psychological horror, implied harm to prior adults, no gore, no jump-scare spam (one, and we mean it), photosensitivity-safe mode included. No harm to children depicted.
EARLY ACCESS: no. LANGUAGES AT LAUNCH: English, more per M6 scope.
SYSTEM REQUIREMENTS: placeholder pending Spike 2 results on target hardware.
PRESS LINE: From the maker of the Dread Ledger rubric it is scored against: a horror game about restoring something carefully, built the same way.

## ADDENDUM · ASSETS NOW EXIST (c043)
The dossier art (After-Fire Chum) is capsule-candidate as shipped and obeys scarcity: a document about him is not him. Four cast sheets are press-kit ready. New sellable truths for the copy, all implementation-backed: the tally contract (recording pins and shields), he does not fit through doors, the dead room, ten deaths that are all your signature, and the line WHAT OTHERS DISCARD, SHE RESTORES adopted from Rita's sheet. The one-startle promise stands and now coexists with a chase, which is the marketing sentence: one jump scare, and it is not the scary part.


------------------------------------------------------------------------------
DOCUMENT 31 · restoration-trailer-beats.md
------------------------------------------------------------------------------

# RESTORATION · ANNOUNCE TRAILER BEAT SHEET v1 (90 seconds)
Doctrine: the trailer obeys the game's laws. One startle total, and it is the game's own one startle. Everything frightening is mediated until the final image. Score: the closing song, G2 print, so the word swap lands inside the trailer itself for anyone listening. Cut grammar: switcher cuts and wipes, never shake, never speed ramps.

0:00 Black. Tape hiss rises. A projector motor somewhere.
0:04 WGLD CHANNEL 58 ident card, phosphor on black, slightly unsteady.
0:08 Compound in daylight, gorgeous and modest: the kettle, the shrine, the pegs. MERLE VO, warm as bread: "We hired a conservator. A real one. She brought her own gloves."
0:18 The bench ritual, cut to the song's pulse: gloves on, ledger line, the signature tick, a reel threading. Text card in ledger type: RESTORE THE TAPES.
0:26 First tape imagery, on the monitor only: Chum 1971, sweet, waving at camera one. Children's laughter inside the tape's bandwidth.
0:34 Close on the slate label: 3RD GENERATION DUB. Cut to the scope: MASTER. Hold two full seconds. No music change. Card: SOME COPIES ARE ORIGINALS.
0:42 Nights: the training film's six hand signals, silent; the Floor Manager at the stack's end, hand rising; Harriet mid-motion, frozen, cup high. Card: RESPECT THE SCHEDULE.
0:52 The song's missing verse surfaces as on-screen spectrogram text: AND NO ONE HAS TO STAY.
0:58 Escalation in stills, one second each: the pre-signed page, the coat pegs gone mustard, chairs in rows, the sealed exterior door: SEALED FOR BROADCAST.
1:05 THE ONE STARTLE: the monitor, Chum walks to the lens, holds a beat past bearable, single-frame lunge, HARD CUT to color bars. This is the trailer's only scare and the game's only scare and both facts are the promise.
1:08 Silence. Two seconds of bars.
1:10 The rec room. Merle, gently, to someone off frame: "There's cobbler." The exhale is the hook.
1:14 Title lockup: RESTORATION. Under it, small: from the 58 Club, with love.
1:20 End card: TAPE 1 FREE DEMO · WISHLIST ON STEAM. The G2 swap lands here in the score: "everyone we love is here."
1:26 Black. One real bell strike, the S06 sample, once, and nothing after it.

## CAPTURE PLAN
Engine: beats 0:18, 0:34, 0:52, 0:58 (the build already stages all four). Puppet shoot: 0:26 and 1:05 (shoot clean, degrade in the ladder per the art bible law). Plates and stills: 0:08, 0:42, 1:10. VO: Merle session three covers both lines; the breakdown's Side 1 register for the first, Side 2 register for the second.
## CUT LAWS
No footage of any ending. No Leland. No glimpse. Nothing unmediated moves except people being kind. If a beat would work in any other horror trailer, cut it; the trailer's job is to be unmistakable.

## ADDENDUM (c043)
The end card gains an option: the dossier's WARNING panel as the final still before the bell-after-black. New beat available at 0:52: the countdown UI over an approach, cut on THE TALLY COOLS. The crossing is trailer-safe (chase legs, no face). Nothing from the dead room, the readings, or any death scene ships in marketing; graves are not previews.


------------------------------------------------------------------------------
DOCUMENT 32 · restoration-key-art-brief.md
------------------------------------------------------------------------------

# RESTORATION · KEY ART BRIEF v1
Deliverables: the full current Steamworks capsule set (main, small, header, library, hero), a 27x40 poster, and four press stills at 4K. Sizes per the live Steamworks spec sheet at time of production; slots named here, pixels there. The fabricated puppet is the key art's Chum: photographed plates from the shoot, integrated, never illustrated from imagination. Supply package to artists: the four reference plates, the art bible (palette hexes and laws), swatch S-07.

## THE ONE IMAGE ARGUMENT
Safety is mediated. Every composition places the threat on a screen and the person in a room, and the viewer's dread comes from measuring the distance between the two. If a comp shows Chum sharing unmediated space with a human figure, it is describing the ending, and we do not sell the ending.

## HERO COMP A (primary): THE BENCH
Over the shoulder of Rita at the capture bench, night. She is a needle-felt figure; her white gloves are the brightest object in frame, per the bible. The monitor fills the upper third: post-fire Chum mid-HOLD, close, still, the artifact ladder visible on the screen and nowhere else in the image. The task lamp makes the room honest. The slate label under the monitor is legible: 3RD GENERATION DUB. The scope reads MASTER. Anyone who leans in gets the plot.
## COMP B (warmth-forward alternate): THE CLUB
The 58 Club in the rec room, Merle at center mid-laugh, cobbler on the table, shrine glass at frame edge catching a phosphor glow from something off-frame. Not one sinister face; the one law of the casting breakdown is also the one law of this image.
## COMP C (minimal / library capsule): THE LITTLE DOOR
The set's little door, tungsten-lit, closed, Chum's taped floor mark in the foreground. Nothing else. Title below.

## LAWS (violations are rejected comps, not notes)
Grain, chroma error, and scanlines exist only on depicted screens. REPAIRED, NOT BURNED: post-fire Chum per the tell-table, zero char, zero horror finishing. Buttons on no face but his. No startle imagery, no open mouths, no lunging poses in any still. The glimpse figure and Leland's face are never depicted in any marketing material, ever; their scarcity is product. Warmth stays genuine: if a face would read as knowing in a thumbnail, redo the face. Title lockup in phosphor #D9EDC4 on near-black, broadcast-adjacent letterforms, no distressed horror type. No red except the slate.

## ADDENDUM (c043)
Comp 0 now exists and is the dossier itself. The one-image argument gains a stronger candidate: Rita at the bench, tally red in the dark behind her, the countdown readable, him at the light's edge at full height, cropped at the sternum. Safety is mediated, and it is expiring on screen.


------------------------------------------------------------------------------
DOCUMENT 33 · factsheet.md
------------------------------------------------------------------------------

# RESTORATION · PRESS FACTSHEET
Developer: Ciel Essel, solo. Engine: Godot 4 (Unreal 5 evaluation in parallel). Status: complete systems prototype, all endings playable at greybox; free Tape 1 demo planned. Platform: PC, Steam. Release: TBA. Contact: [insert].

SHORT: You are Rita Ivori, a magnetic tape conservator hired by a fan club of retirees to authenticate fragments of a 1970s children's puppet show whose masters burned in 1977, and whose sign-off was cut mid-line, so the show never learned how to stop. Preserve. Rewind. Remember.

LONG: RESTORATION is a first-person horror game about care as gameplay. Every verb is a conservator's verb: capture in real time at the bench, sign the log on scarce paper, catalog, splice, decide what a thing is on the record. The station is WGLD, Channel 58; the club is warm and real and feeds you; the show is THE GLADHOUSE, and its handmade cat, Chum, is the sweetest thing you will ever be afraid of. What others discard, she restores.

FEATURES, ALL IMPLEMENTATION-BACKED:
One jump scare in the entire game, and it is not the scary part.
The tally contract: while you record you are on camera, and on camera it cannot touch you; the same countdown is your progress and your protection, expiring together.
It is eleven feet tall and does not fit through doors; every threshold costs it seconds, and those seconds are your plan.
Hiding, inverted: the safe hide is the lit one.
Saving costs a signature; paper is scarce; the log remembers whose hand signed.
Every death in the story is a choice you can name afterward, and the game will name it back to you, in the ledger, at the end.
More ways for the broadcast to close than the club will admit, none of them free.
Accessibility as canon: captions, text scale, remapping, assist, pause, all in the booth from first launch.


------------------------------------------------------------------------------
DOCUMENT 34 · quotes.md
------------------------------------------------------------------------------

# RESTORATION · CLEARED PULL QUOTES
From the world, approved for editorial use:
"There's no one at home anymore... Say goodnight, Chum." (the lost sign-off)
"NEXT WEEK'S EPISODE · STARRING RITA IVORI." (what dying reads as)
"You don't vote against being carried." (Merle Cottry)
"This place runs on love and leftovers." (Merle Cottry)
"Some tapes shouldn't exist. But they do. And I find them." (Vess Keys)
"You are safe as audience. Do not be interesting. Never accept a role." (Leland Merrick, before he vanished)
"And now. The tour continues." (Harriet)
"HE REMEMBERS THE AUDIENCE." (Peak Production asset dossier)
"Professional. Patient. Precise. What others discard, she restores." (on Rita Ivori)

EMBARGO, FIRM: no ending names or content, nothing from the dead room, no death scenes or specifics, nothing regarding the warm unit, nothing regarding the Day 4 corridor. Graves are not previews. The dossier art is cleared; the six portraits are cleared; gameplay of Day 1 is cleared.
Art credit line: courtesy of Ciel Essel / RESTORATION. Editorial use with coverage only.


==============================================================================
SECTION 09 · ADDITIONAL DOCUMENTS
==============================================================================


------------------------------------------------------------------------------
DOCUMENT 35 · full-plotlines-anatomy-restoration.md
------------------------------------------------------------------------------

# Full Plotlines: The Anatomy and Restoration
## Start-to-Finish Narrative Architecture

**Version 1.0** | Companion to the story concepts document. Both plots preserve the established threat design, mechanics, and three-layer lore structure.

---

# THE ANATOMY

## The Shape of It

A surveyor is hired to produce the as-built floor plan of Sutton House before demolition. The house is an organism two centuries into a translation: its builder moved himself into the architecture surgery by surgery, and each surgery required a true survey, because the house obeys its own documentation and a surgeon cannot cut what is not charted. The last drawings were destroyed. The demolition is the final operation. The surveyor is not documenting the patient. She is prepping the table.

**The chaptering device is the survey itself.** The game is divided into Sheets, the drawing plates of the commission. Completing a sheet inks it, and inked regions stabilize: the house obeys what is drawn. But stabilizing a region squeezes the wrongness into everything not yet drawn. The player anesthetizes the patient region by region, and the escalation curve is the clamping. By the final sheet, all the house's fear is concentrated in the last unmapped rooms.

## Cast

**Ada Marsh**, the surveyor. Chosen by the Trust because her old firm fired her for refusing to falsify a boundary survey. The house needs someone constitutionally incapable of drawing a false line. Her virtue is the trap, and the game's hardest choice will require betraying her defining trait.

**Mrs. Tille**, housekeeper. Warm, attentive, missing her dominant hand in a way nobody acknowledges. A Steward: a prior surveyor, post-donation.

**Mr. Gorse**, the Trust's solicitor. Correspondence only, never seen. His letters' handwriting matches a much older hand the player will meet in the archive.

**Douglas Pym**, the 1974 surveyor. Found mid-donation in the theatre in Act IV. The exposition-with-cost scene, and the voice of the sabotage path.

**E.V.**, initials scratched under a sill, dated 1901. The surveyor who refused, drew a false scale figure, and caused the only failed surgery. The sealed east wing is the scar.

## Structure and Beats

### Cold Open: Arrival
Dusk arrival, the commission letter, an exterior circuit before knocking. The frontage tapes at 96 feet. The facade holds 13 window bays that cannot fit in 96 feet. First wrongness, delivered through the player's own arithmetic, not a cutscene. Mrs. Tille greets her. The house is warm, though the boiler "hasn't run in years."

### Sheet I: Elevations
Tool tutorial: tape, level, chalk, pins, camera and film. The window-bay discrepancy is formalized on paper. Stewards introduced through domestic wrongness played straight. Under a sill: "E.V. 1901." At night the house settles in rhythm, roughly six times a minute, the cadence of sleeping breath. **Sheet inked:** the next morning the front door sits three feet from where she drew it, then corrects itself by noon to match her ink. The house obeys documentation. Tille never acknowledges the interval.

*Lore layer here:* main route establishes the survey loop; deducible layer plants breath-rate and obedience-to-ink; buried layer opens with E.V.'s initials.

### Sheet II: Ground Floor
Interior rooms exceed the exterior envelope. The Long Hall returns wrong on the second pass. Estate records list renovation years: 1811, 1839, 1868, 1901, 1938, 1974. The parish register, one village over, lists a Sutton family death in each of those years. The player can make that join; the game never does.

**First hostile response:** the Long Hall lengthens while being measured, a peristaltic swallow, and the first chase teaches the core defense: you cannot outrun a hallway, but a snapped chalk line stops it, because the house obeys documentation, even hers. Deducible texture: the larder holds at 37 degrees. Body temperature, in a cold room.

### Sheet III: Upper Floors
The family bedrooms, each preserved at the year of its occupant's death, each death a renovation year. Medical bills. Consent letters in gentle legal language about "contribution to the fabric." A 1901 letter from E.V. refusing further work: "I have given enough."

**Midpoint set piece: the light table.** The archive holds anatomical plates in the Vesalius tradition. The drafting room holds a light table. Nothing forces the player to lay their inked ground plan over a plate. The players who do watch their own drawing align with a torso section: the boiler room over the heart, the double stair down the spine, the sealed east wing where a lung should be. The game's biggest reveal is performed by the player's own hands, and it is never spoken aloud. This overlay is the game's iconic image.

*Buried layer:* wherever Ada's measurements disagree by exactly four and three-quarter inches, there is a wall cavity. Inside the cavities: signatures of a disbound notebook in an anatomist's cue-shorthand, the hand that matches Gorse's letters. Josiah Sutton, 1780, anatomist and architect. The community's long dig is reassembling this notebook by doing arithmetic on their own drawings.

### Sheet IV: Cellars and Service
The boiler runs at sixty discrepancies per minute. The wine cellar's vaulting is pleural. And past it, the theatre: an anatomy theatre dressed as a chapel, student benches ringing a table, and on the table Douglas Pym, mid-donation since 1974, alive in the sense that the house is careful with him.

**Pym's scene carries the load:** the renovations were surgeries. Each surgery required a survey. Every architectural drawing carries a scale figure, a small drawn human for proportion, and the figure is the donation: the surveyor who draws themselves into the plan belongs to it. E.V. drew a false figure in 1901 and the east wing died on the table. Pym drew true and has been paying since. He begs Ada to draw false, and teaches her how a load-bearing lie is constructed. The demolition date is revealed as the operation date. The crew that will arrive is not a demolition crew.

### Sheet V: Reconciliation
The commission requires reconciling every discrepancy into one true plan. The house now resists at full strength: corridor peristalsis, valve rooms, Stewards herding rather than helping, chalk and pins and film nearly spent. The east wing must be entered for the final measurements: the necrotic wing, the 1901 scar, the hardest zone in the game, and the hiding place of the last notebook signatures.

At the center, the room on no plan and with no discrepancies at all. The still point. Josiah's study, the seat of what remains of him, the one room the house cannot feel. The final drafting session happens here, and what Ada inks decides everything.

## Endings

**1. The Faithful Plan.** Complete, accurate, scale figure drawn true. The operation proceeds. Sutton is delivered into whatever the house has grown for him. Ada takes Tille's place. The last shot is her initials scratched under a sill, waiting for the next surveyor. The bleak canonical ending, and the one her defining trait walks her into.

**2. The False Line.** Pym's path: a load-bearing lie, drawn well enough to pass. The surgery fails, the house convulses, Ada escapes a thrashing building. Then the quiet coda: her false plate is filed in the archive beside older plates, and some of those are false too. Others lied before her. The house healed around every lie. It is wounded and patient, and it has time.

**3. The Complete Anatomy** (buried stratum ending). Requires the full notebook and all prior survey fragments. The truth underneath the truth: Josiah did not flee death into architecture. He built a cage around something his anatomy school raised, and stitched himself in as the lock. The family's donations fed the lock, not the prisoner. The "delivery" the house wants is not Sutton's. The secret ending lets Ada perform the correct surgery: reconstructing and inking the original 1780 plan over her as-built, restoring the first anatomy, resetting the ligature. Cost: her drawn figure stays in the plan. She walks out, and she will never hold a pencil steady again. The community's dig is what makes this ending exist, which keeps the deep lore load-bearing rather than trivia.

**4. The Refusal.** Leave the commission incomplete and walk. Available at any time, and the game lets you. The epilogue is a newspaper item: the Trust has engaged a new surveyor. The credits list the next name. It is the cheapest ending and it is designed to feel like one.

## The Buried Timeline (community reconstruction target)

1780, house built, Josiah Sutton, anatomist. 1811, west wing, the lungs, first Sutton death. 1839, the double stair, the spine. 1868, service ranges, the gut. 1901, east wing, failed, E.V.'s false figure, the scar sealed. 1938, the boiler, the heart. 1974, Pym's survey, operation interrupted, Pym retained. Present day: the final commission, filed as demolition. Reconstructed through parish registers, estate records, plate fragments, cavity arithmetic, and the cue-shorthand cipher.

---

# RESTORATION

## The Shape of It

A tape conservator is hired by a fan collective to authenticate recovered fragments of The Gladhouse, a 1971 to 1977 regional children's puppet show whose masters burned in a station fire. The truth in three turns: the show's creator built the mascot as a vessel and broadcast was feeding. The creator set the fire himself, trying to end it, but the transmission cut before his series finale's sign-off completed, so the show never formally ended, and a show that has not ended cannot stop recurring. It has spent fifty years in technical difficulties. The lost finale does not need to be found. It needs to be finished.

**The chaptering device is the tapes.** Five restoration batches, each an act, each escalating, built on the Poppy cadence where every recovery is an event. The endgame is a formally correct sign-off, performed live, which is the one thing binding broadcast grammar makes possible and the one thing the fandom can never do.

## Cast

**Rita Ivori**, freelance film and tape conservator. Hired for a 50th anniversary boxed set. Precise, unsentimental, exactly the craftsman the show has been waiting for. Her authentication work is, without her knowledge, production work: she is being groomed as the next producer the way the creator once was.

**Ansel Craik**, creator and puppeteer, 1971 to 1977. Not a grieving father, which is the genre's expected answer. Craik was a child listener of a 1950s radio program where the thing lived in call-and-response, groomed across a childhood, and when radio died he built it a television body. He understood too late, set the fire, and vanished into it.

**Chum**, the mascot: a handmade patchwork cat in brown wool, one amber glass eye and one black button, twisted-string whiskers, a cross-stitched grin, a silent brass bell at the collar, the beloved center of the show. Chum is a friend's name and a bait bucket's name, and the show means both.

**The Understudy**, the thing that performs Chum. Bound by broadcast grammar: it must honor entrances, exits, and commercial breaks, and it cannot harm on camera, because the show was for children. Direct sight frees it.

**The 58 Club**, the collective, named for the dead UHF channel, headquartered in the decommissioned WGLD transmitter compound they bought at auction. **Merle Cottry**, president, who as a child in the 1974 live episode was found by Chum when she was lost, actually lost, and has loved him ever since; the comfort was real, which is the cruelest part. **Vess**, the young tape hunter who sourced the impossible tapes, desperate to be chosen and quietly being rejected. **Harriet**, a senior member who now speaks mostly in the show's transitional phrases. The Floor Manager, never named, always in headphones, who counts rooms in and out of existence: "back in five, four..."

**Leland**, the previous archivist, who left mid-project. His annotations are Rita's inherited guide, the document trail that ends mid-sentence.

## Structure and Beats

### Tape 1: Authentication
Arrival at the compound, the club's overwhelming warmth, the restoration loop tutorial: inspect, bake, clean, capture, log timecode. The first anomaly is professional, not supernatural: a third-generation dub with zero generational loss, which is physically impossible, and the game trusts the player to know it. The tape holds a scene nobody remembers airing: The Quiet Game, in which Chum teaches children to hold still and silent "until I find you." Merle weeps with joy at footage she cannot have seen before and insists she remembers it.

Night one plants the ruleset by accident: watching a corridor through a monitor feed, Rita sees something obey the frame edge, entering and exiting like a performer hitting marks. Leland's first note: "You are safe as audience. Do not be interesting. Never accept a role."

### Tape 2: Airdate Math
The archival act. Production slates say 141 episodes; station logs say 138 aired. The three unaired slates carry dates that sit inside the same weeks as three local children's disappearances, discoverable through the club's own memorabilia, because the show ran "find our friend" appeal segments and the club proudly kept the clippings. The show ran the searches for the children it took. The game never says this sentence. The player assembles it from the club's shrine.

**Set piece: the Screening.** A club tradition, communal watch night, lights down. Mid-episode, Chum begins a call-and-response and half the room answers in perfect unison, including a new line addressed to "our new friend in the back." The mechanic arrives under pressure: answer as audience, in rhythm, nothing more. Interesting answers are auditions. Vess answers too eagerly and the room goes wrong around him for a held second, and Rita watches the club pretend not to notice.

### Tape 3: The Fire Finale
The restoration of the 1977 final broadcast. The studio empties, then burns, and the tape keeps running: Chum performing to an empty burning set, addressing everyone at home, the camera panning with no operator. The fire never touches him. In the transmitter building's dead room, Rita finds Craik's materials: his childhood radio scripts, his production notebooks in cue-sheet shorthand, and the plan. Craik understood the binding runs on format, so he wrote a formally correct series finale: last episode, closing song, say goodnight, close the house, credits, station sign-off. A show that has properly ended cannot recur. The fire was insurance, and it was the mistake: the transmission cut before the sign-off completed, and an unfinished ending is just a cliffhanger. The endgame goal crystallizes here, and it reframes the whole genre of lost media: everyone hunts the lost finale to watch it. Rita has to perform it.

### Tape 4: Provenance
The impossible batch: tapes dated after the fire, sourced from a storage unit auctioned under Craik's mother's name, containing episodes with sets that no longer existed and a Chum whose stitching has changed. The club stops pretending. They are not deceived and never were; they are devoted, and the game gives Merle the scene that earns it: the show made unbearable childhoods bearable, Chum genuinely found her in 1974, and the love is not a delusion, it is the leash. They need a producer for the migration. Vess has been failing the role; his edits are rejected, his cuts will not take, the show wants a craftsman. It wants Rita, and the anniversary premiere, the first digital broadcast of the restored show, is the migration ceremony: radio died and it moved to television, television died and it moved to tape, and tape is dying now. The compound locks for the premiere.

Leland's thread pays off here: he is in Tape 4. In frame, background, holding perfectly still. Playing the Quiet Game. Not dead. Cast.

### Tape 5: The Premiere
The finale inverts the threat model: the Understudy must play along with anything formally correct, because format binds it, so the human beings become the antagonists. The club will cut power, block corridors, and unplug cameras to stop a sign-off, and staying on camera is staying safe, so the climax is a live television production performed under sabotage: get the closing song's missing verse to air, hold the shot, hit the cues, keep yourself in frame.

The last beat is the fourth wall, broken on purpose. The show cannot end while it believes the audience is still out there, and the club cannot tell it otherwise, because they are the audience and they cannot say the words. Rita can. The sign-off completes when someone looks into the lens, on camera where nothing can touch her, and tells everyone at home the truth: that no one is watching anymore.

## Endings

**1. Sign-Off.** The finale is completed. Someone must close the house from inside the show, accepting one last role for one last scene. If Rita's Leland thread is complete, Leland, already cast, says goodnight, and goes wherever ended shows go, which reads as release and costs like grief. If not, Rita takes the role herself and the epilogue is hers from inside a still frame. Either way: static, sign-off card, and Channel 58 goes dark for the first time in fifty years. Merle, freed and bereft, sits in the rec room in front of a television that is finally just a television.

**2. The New Producer.** Rita authenticates the premiere. The migration succeeds. The final shot is crisp 4K Chum addressing the lens: "Say it with me." One post-credit interface lie, used once in the whole game, Eternal Darkness style with total restraint: the game's own menu now carries something that was not there before.

**3. The Burn.** Craik's path, repeated: destroy the tapes and drives. It fails the way the fire failed, because modern media does not burn; the club has offsite copies, and format outlives its instances. A bleak ending that functions as a lore lesson: it exists to prove why the sign-off is the only real exit.

**4. Dead Air** (buried stratum ending). The deep dig reveals the chain of prior vehicles: a 1950s radio hour, a 1930s "Uncle" program, a magic lantern lecture circuit before that, each with its groomed producer, each migration forced by a dying medium, because the Understudy is not a character but a format, and call-and-response is older than broadcast. The transmitter compound's radio dead room still functions. The secret ending performs the sign-off in the original medium, over radio, reaching everyone at home across every format at once. Unlocked only by the community-mined materials: frequencies from spectrograms, Craik's childhood script, the dead room key. The reward for the deepest diggers is the cleanest death the thing can be given.

## The Buried Timeline (community reconstruction target)

1920s to 30s, an "Uncle" radio program with responsive segments, producer unknown. 1950s, The Cheerful Hour, radio, the young Ansel Craik a devoted child listener, groomed. 1971, The Gladhouse premieres on WGLD, Craik as builder of the new vehicle. 1972 to 1976, three unaired episodes, three disappearances, the Playmates. 1974, the live episode, Merle found. 1977, the fire, the incomplete sign-off, Craik gone. 1990s to 2000s, tape-trading circles keep circulation alive, which is to say keep it fed at a trickle. Five years ago, the 58 Club buys the compound. Two years ago, Leland's project begins and stops. Now: Rita, the boxed set, and the premiere. Reconstructed through airdate math, slate dates, TV listings, timecode-gap extraction (dropped frames across tapes, sequenced by timestamp, assemble a production schedule whose final entries are dated after the game's own release), and the cue-shorthand cipher shared with no one until the community breaks it.

---

## Structural Note on the Pair

The two plots are deliberate mirrors. The Anatomy is horror of precision: the protagonist's craft is measurement, the map is the weapon aimed at her, and the endings hinge on whether she draws true. Restoration is horror of devotion: the protagonist's craft is preservation, the archive is the weapon aimed at her, and the endings hinge on whether anything is allowed to end. In both, the buried stratum is not collectible trivia; it is the only path to the ending where the protagonist actually wins something, which keeps the deep-lore dig emotionally load-bearing, per the design principles document.


------------------------------------------------------------------------------
DOCUMENT 36 · restoration-design-doc.md
------------------------------------------------------------------------------

# RESTORATION: Design Document
## Character, Game Design Style, UI, Mechanics, and Controls

**Version 1.0** | Companion to the full plotline document. Tagline candidate: **Stay in frame.**

---

## Point of View

Restoration believes that mediation is safety and craft is courtship. Every horror game punishes you for being bad at it. This one endangers you for being good at it: the interface between you and the horror is the protagonist's own skill, and the better your work, the more the show wants you. Everything downstream (the bench, the cameras, the UI drift, the ending gates) traces to this belief.

**The four pillars:**
1. **Craft is courtship.** Restoration quality is the hidden grooming meter. Doing your job well is the threat vector.
2. **Mediation is safety.** Anything viewed through a lens, monitor, or frame is bound by broadcast grammar. Direct sight frees it.
3. **Format is law.** The rules of television (entrances, exits, commercial breaks, sign-offs) are absolute, learnable, and exploitable by both sides.
4. **The comfort is real.** The club's warmth, Chum's charm, and Merle's love are played straight, never winked at. The genuine sweetness is the leash.

**The unsafe choices, named:** the monster cooperates during the finale while humans sabotage; tape capture plays in forced real time with no skip; interrogating Leland physically erodes the only copy of him; and the pause menu itself drifts as the Producer Track rises. Each is defended in its section below.

---

# PART I: CHARACTER DESIGN

## Rita Ivori (player character)

First person, so Rita's design is her hands, her tools, and her rare reflections. Her hands are the most animated character in the game: white cotton conservator gloves (the iconic archival image), sleeve garters, a jeweler's loupe on a lanyard that swings into frame when she leans in. Wardrobe glimpsed at mirrors and dead CRTs: work apron over practical clothes, hair pinned with a film-can lid clip, a detail players will find eventually.

**Design rule:** her reflection budget is scripted and scarce. Early game, dead CRTs reflect her normally. From Tape 3 onward, her reflections begin composing better: centered, headroom correct, rule-of-thirds. Nobody comments. The player's own image is being framed for television, and the horror is in the cinematography, not the face.

## Chum (the mascot)

A handmade patchwork cat, canonized by the reference plate set (four spec-sheet photographs, gray seamless, typewriter labels). Built for maximum plush conversion (Dread Ledger 8.3) with horror carried entirely in variant deltas that the community can catalog frame by frame.

**Base design:** brown boiled-wool body, triangle ears with contrasting inner-ear patches (mustard left, navy right), a round head with a visible center seam, one amber glass cat eye (viewer left) and one black four-hole button (viewer right), a small dark nose, three twisted-string whiskers per side, and a cross-stitched grin of small X ticks along the smile curve. Hand-cut felted patches over the body: rust at the chest, green at the right side, a large tan belly circle (his most huggable feature), blue at the arm, plum at the thigh, mustard toe caps, navy at the tail tip, all in contrasting blanket stitch. Thin brown collar with a brass keyhole bell that never rings. It rings exactly once in the entire game, in Tape 5, and by then the player knows what silence meant.

**Era variants (the catalog the community will build):**

| Era | Look | The tells |
|---|---|---|
| 1971 pilot | Cruder, endearing prototype | 9 hand-cut patches, no bell yet, frayed yarn whiskers, faintly uneven grin |
| 1974 peak | Professional rebuild, the icon | 12 patches, collar and bell added (silent), symmetric cross-stitch grin, amber eye viewer-left |
| Post-fire | Repaired, not burned: the horror is the mending | See the delta set below |
| 4K premiere | 1974 configuration in impossible fidelity | Individually rendered fur sheen, moisture in the glass eye, detail no puppet could carry |

**The post-fire delta set (design law: fire damage reads as victimhood; the fear lives in the repairs):**
1. The over-grin: the original smile seam remains as a faint scar beneath a new, wider grin sewn past where a cat's mouth ends, tight vertical ticks in waxed near-black thread.
2. The wrong button: the black button replaced by an adult coat button, too large, off-shade, over-attached with excessive thread wraps.
3. The chirality tell: the amber eye now sits viewer-right with its glass pupil rotated off-axis. Lore logic, canon: it repaired itself from its own footage, and footage lies about left and right. Every mirror-flip in the catalog is evidence of its reference material.
4. Whisker asymmetry: three singed stubs on one side; two replacements on the other, too long, too straight, fine dark wire.
5. The bell, opened: blackened, still silent, with a bright pried-and-recrimped scratch at the seam. Something checked inside it.
6. The belly, accessed: the tan patch replaced with darker wool carrying a central seam opened and resewn repeatedly, dense overlapping restitch scarring.
7. Two patches in materials no toy should have: school-gray flannel at the chest, glossy dark leather at the leg. Patch count 14. The gray flannel matches a jacket in one of the shrine's missing-children clippings; the game never zooms in.
8. The tilt: the neck restitched two to three degrees off true. The head is permanently cocked, listening. The cheapest, most terrible delta on the sheet.
9. Footage-only: weight carried on the wrong foot relative to every archival episode.

The post-fire tells are never called out by the game. They are deducible-layer content delivered through the player's own restoration monitors.

## The Understudy

**Design philosophy: it has no canonical off-camera body, and the game never spends that mystery.** Manifestation rules:

- **On any monitor or viewfinder:** it is Chum, performing, correct, bound by the show's physical logic.
- **Off-camera, peripheral:** partials only. A felt hand at human scale resting on a doorframe. A proscenium shadow that accompanies it like a stage edge it carries. Footsteps with the weight of a person and the texture of upholstery.
- **Direct sight:** reserved for one scripted glimpse in the entire game, late, brief, and never repeated. What the glimpse shows is a puppeteer whose puppet is missing, or a puppet whose puppeteer is missing; the animation should read as genuinely undecidable, and playtests should confirm players split on which they saw.

## Merle Cottry (club president)

Late fifties, warm, cardigans, reading glasses on a beaded chain, enamel Chum pin polished daily. Her design arc is the casting-drift system's showcase: across the five tapes her wardrobe migrates into the show's host palette, and by Tape 4 she dresses like a woman about to walk on set. Behavioral tell: she has begun narrating her own actions in a gentle presenter cadence ("Now Merle is just going to put the kettle on"), which reads as endearing grandmother until it reads as script.

## Vess (the tape hunter)

Twenties, thrift-store seventies shirts worn as devotion cosplay, label maker on his belt, chewed pens. The status detail that carries his whole arc: his club pin is plastic where everyone else's is enamel. He found the impossible tapes and it earned him nothing, because the show does not want an enthusiast, it wants a craftsman. His envy of Rita is the game's most human threat and should be designed sympathetically: he is what the fandom looks like when the fandom is not chosen.

## Harriet (senior member)

Elderly, immaculate, speaks increasingly in transitional phrases ("And now." "But first." "When we come back."). Her signature behavior is the holding pattern: during the compound's commercial-break windows she stops mid-motion, teacup half-raised, and resumes on the return cue. This is a background-behavior system, never a cutscene, and players who never notice it lose nothing except sleep once they do.

## The Floor Manager

Never named, face never fully lit, headphones with a coiled cable connected to nothing, laminated run sheet. Communicates only in countdowns and real television floor-manager hand signals: stretch, wrap it up, cut, thirty seconds, you're on. **This is a designed vocabulary the player must learn, because the Floor Manager's hand signals are the game's threat-telegraph UI** (detailed in Part IV). The scariest character in the game never touches anyone; they just count things in and out of existence.

## Leland (the previous archivist)

Exists only inside the tapes: mid-forties, archivist's cardigan, always partially cropped by the frame edge as though the composition refuses him. He holds a legal pad on which answers appear across frames. In the physical world he survives as green fine-liner annotations in the margins of the accession logs, which makes his handwriting a character the player knows intimately before ever finding him in frame.

## Ansel Craik (archival footage only)

Seventies TV-crew look: big glasses, mustache, puppeteer's black sleeves. The single most important design detail in the archival footage: in one late episode, Craik is fully visible on set, both hands accounted for, while Chum performs in the same shot. The game never zooms in. The community will.

## The 58 Club (collective visual language)

Enamel pins as regalia, potluck domesticity installed inside a brutalist transmitter compound: doilies on equipment racks, a casserole rotation whiteboard next to the transmitter log. **The casting-drift wardrobe system:** members' clothing migrates over the acts from civilian colors into the show palette (mustard, avocado, burnt orange), and the environment silently tells you who is furthest gone by how much of the palette they wear. It is a legible-state system that never needs a meter.

---

# PART II: GAME DESIGN STYLE

## Perspective and Structure

First person, contained single location (the WGLD transmitter compound: studio floor, control room, tape library, dead room, transmitter hall, living quarters), five acts chaptered by tape batch. Six to nine hours mainline. The structure supports optional chaptered release on the Poppy cadence (each Tape as a drop) without harming the boxed whole.

## The Two Render Worlds

**The compound (Crafted World doctrine, amended):** every surface and every character renders in the reference-plate craft language: boiled wool, felt, worn pine, brushed brass, waxed thread, visible stitching and joinery, photographed-craft realism. Humans are crafted figures in the same language, cloth and needle-felt over armature. Sodium exteriors, fluorescent interiors, brutalist forms softened by the club's domesticity, all executed in physical materials. The dependability pillar rewrites accordingly: the compound must feel physically dependable in craft logic; wool behaves like wool, and nothing in the real world ever glitches. The compound-versus-tape contrast is now carried entirely by lighting and the artifact pipeline, not by material difference.

**The tape world:** authentic period video reproduction, not a lazy VHS filter. Tracking noise, dot crawl, chroma bleed, head-switching noise at frame bottom, correct 4:3 pillarboxing, generation loss modeled per dub. This authenticity is load-bearing twice over: the analog-horror audience will inspect it forensically, and the plot's inciting anomaly (a third-generation dub with zero generational loss) only lands if the simulation is honest enough that its absence is legible. The player's own tools visibly alter these artifacts, which makes restoration quality diegetic rather than a score popup.

## The Core Loop

Day phase: bench work (restore, log, deduce) and social beats with the club. Night phase: compound traversal, events, and rule-learning under pressure. Screenings close each act as social set pieces where the call-and-response system runs in front of witnesses. The loop tightens across acts as night behavior bleeds into day and the club's supervision becomes escort.

## Difficulty Philosophy

Per the Dread Ledger's fear-frustration criterion: deaths teach dread, not resentment, so failure states are captures and resets framed as retakes ("From the top"), never gore. Two presentation modes, named diegetically: **Late Night Mode** (full intensity) and **Matinee Mode** (reduced scare intensity, softer audio spikes, longer telegraph windows, framed in-fiction as the daytime rerun edit). Matinee is a first-class experience, not an apology.

---

# PART III: UI STYLE

## Philosophy: Two-Layer Diegesis

**World UI is broadcast engineering.** No floating HUD in the compound. All state reads from world objects: tally lights for camera liveness, the studio clock and ON AIR sign for break windows, VU meters for sound exposure, the breaker panel for the power budget. If a designer wants to add a HUD element, the answer is to find the piece of 1970s equipment that already displays it.

**Meta UI is station paperwork.** Pause, settings, saves, and the journal live inside a physical ring binder on WGLD letterhead: transmitter logs, FCC-flavored forms, staff memos, the accession ledger. Saving is logging your capture session in the ledger, in Rita's hand.

## Type System

Paperwork and menus: typewriter faces in the IBM Selectric/Letter Gothic family, typed slightly off-grid because forms were typed by humans. Tape-world overlays: a chunky period character-generator face in the Vidifont tradition, with authentic CG limitations (no lowercase in early-era tapes). Annotation layer: Leland's green fine-liner, hand-rendered. Three voices of type, never more, and each one tells you which world you are reading.

## Color

Compound neutrals and sodium, with exactly two UI accents: tally red and cue amber. The show palette (mustard, avocado, burnt orange) belongs to the show, which sets up the game's slowest UI system:

**Casting drift in the interface.** As the hidden Producer Track rises, the ring binder gains Gladhouse stationery: a mustard divider tab, a Chum sticker on the ledger, the settings form reprinted on show letterhead. This is not the interface lying; everything remains true and functional. It is the interface being dressed. The one true interface lie in the entire game remains reserved for the post-credits of the New Producer ending, and that restraint is a hard rule: spend deception once, at maximum voltage, per the Eternal Darkness lesson.

## The Call-and-Response UI

Cue-light signs in the diegetic style of studio audience signage: RESPOND and HOLD, with beat timing carried by the sign's pulse. On-beat inputs land inside the pulse window. In screenings the signs hang over the rec room like they always belonged there, and no one acknowledges when they light.

## Captions and Accessibility

Captions styled as period television captions with speaker tags and, critically, directional sound captions ("[footsteps, upholstered, left]"), because audio carries threat information and deaf players get the full fear channel, not a transcript.

Accessibility with teeth (Dread Ledger 7.4), designed diegetically where possible:
- **Photosensitivity mode is the TBC.** The bench's time base corrector, toggled on, stabilizes flicker, strobe, and tracking-jitter across the whole game, presented as an in-world device. The safety feature is a piece of the fiction.
- Microphone features (Quiet Game breath, spoken responses) are fully optional with button-hold equivalents of equal function.
- Tally states carry shape and position, never color alone. Contrast at WCAG AA minimum across paperwork UI.
- Full remap, hold-to-toggle alternatives on all sustained inputs, subtitle size and background opacity controls on the binder's "Presentation" form.

---

# PART IV: GAMEPLAY MECHANICS

## 1. The Restoration Bench (signature system, half one)

The craft suite where most day-phase play happens. Sub-tools:

- **Bake:** magnetic tape with sticky-shed must be baked before play. A temperature-and-time hold: set the oven, monitor drift, pull at tolerance. Patience mechanic; rushing risks the only copy.
- **Splice:** physical repair of damaged sections. Precision alignment under the loupe, trim, tape, burnish. Analog surgery with permanent consequences on the master.
- **Capture:** the tape digitizes in real time and cannot be skipped, only scrubbed after capture completes. The player must sit with the content as it plays, adjusting tracking and TBC while the show happens to them. **Defense of the unsafe choice:** forced real-time viewing is the horror delivery mechanism; the bench turns watching into work and work into exposure, and every capture session is a small screening with an audience of one.
- **Audio bench:** waveform and spectrogram view. The spectrogram is the deep-dig instrument: images and phrases hide in the actual audio, minable in game and, for the community, in the shipped soundtrack files.
- **Quality grade:** every restore is graded on the club's rubric sheet. High grades yield cleaner deducible-layer content and accelerate the Producer Track. Sloppy work slows the grooming but draws hostility, because rejection has a body count in this compound (see Vess). The player is always choosing between legibility and safety, which is the Lucid greed dilemma rebuilt in a new medium.

## 2. Frame Discipline (signature system, half two)

The safety model, derived from pillar two:

- **Mediated viewing is safe.** The Understudy seen through any live monitor, viewfinder, or lens is bound: it performs, it obeys the frame, it cannot harm what watches correctly.
- **Direct sight frees it.** Line-of-sight without mediation is the fail condition, so the game's stealth verb is managing where your eyes are.
- **Avert:** hold to raise Rita's clipboard, blocking direct sight while preserving movement at a slow walk. The clipboard is also where session notes live, so the shield and the notebook are one object, and reading your own notes is how you hide.
- **Tally logic:** a camera protects only while live and feeding a monitor. Tally lamps (shape-coded, not just color) broadcast liveness at a glance.
- **The patchbay and the power budget:** the compound runs on a finite amperage budget managed at the breaker panel. Routing camera feeds at the patchbay builds mediated corridors of safety through the building, but every live camera, monitor, and work light draws from the same budget, and overdraw during an event trips breakers in the worst order. This is the FNAF power meter grown into a building-scale routing puzzle: players plan safe paths the way electricians plan loads.

## 3. The Broadcast Grammar Engine

The ruleset the whole game teaches:

- **Entrances and exits:** the Understudy enters and exits spaces only through valid "on" transitions. Doors it has been framed through become its doors.
- **Commercial breaks:** the studio clock and ON AIR sign govern break windows, timed safe periods during which the compound reconfigures and the Understudy cannot pursue. Players learn to read the clock the way FNAF players read power.
- **The Floor Manager's hand signals are the telegraph system.** Stretch means the current safe window is being extended; wrap it up means it is closing early; thirty seconds is exactly that; you're on means stop moving now. The game teaches real television floor-signal vocabulary in an early diegetic scene, then trusts the player forever after. Threat information is delivered by a silent character's hands, which is the proudest UI decision in the project.
- **Formal correctness protects.** Correctly delivered format phrases have mechanical force: the show's own closing line ("That's all for today, Chum") forces a scene exit if delivered on a valid beat. Rare, resource-like, earned through lore.

## 4. Call-and-Response

The dialogue system, run under the cue-light UI. Three stances per prompt:
- **Audience:** the neutral, on-beat, correct response. Safe, always available, advances nothing.
- **Quiet:** silence, safe only when paired with stillness (see mechanic 5), reads as absence.
- **Improvise:** off-script content. Interesting answers are auditions: they unlock information and advance sequences, and they raise the Producer Track, because being interesting is being cast.

## 5. The Quiet Game

The freeze mechanic, named by the show itself in Tape 1. Hold still and silent while it seeks. Optional microphone input treats real breath as in-game breath; the button alternative is a hold-and-release rhythm of identical difficulty. Movement tolerance is generous on Matinee, surgical on Late Night.

## 6. The Provenance Suite (deduction systems)

- **The Accession Log:** the game's journal, and the deduce-it-yourself commitment device. Fields for each tape (date, generation, provenance, contents) are filled by the player, not autocompleted, and the club reads your log. Logging true conclusions and logging safe cover stories are different acts with different consequences, which makes the journal itself a stance.
- **Airdate math:** a cross-referencing interface of station logs, slates, and TV listings. The 141-produced, 138-aired discrepancy and the three unaired dates are player-assembled, never stated.
- **The light table:** film scraps, photographs, and documents overlay here; the compound's paper archaeology.
- **The dead room radio:** tunable, patient, and the doorway to the buried stratum's oldest layer.

## 7. The Leland Frame-Séance

The game's tenderest mechanic. Leland exists between frames: on the bench, single-frame stepping with the jog wheel reveals him moving only in the unobserved intervals, and questions written on the bench notepad are answered on his legal pad across a span of frames. **The cruelty that makes it matter:** every scrubbing pass wears the tape, and the wear is real and cumulative. Interrogating Leland erodes the only copy of him. Players ration their questions to a trapped man, and completing his thread for the Sign-Off ending means spending him carefully enough that there is something left to free. Defense of the unsafe choice: scarcity is what converts a puzzle voice into a person.

## 8. The Producer Track (hidden stat)

Raised by restoration quality, accepted roles, and interesting improvisation. Never shown as a number. Surfaced only through tells: the show addressing Rita with increasing specificity, her improving coverage inside new tape content, the club's deference hardening into ceremony, and the binder's casting drift. Gates the ending branches in combination with the player's conduct record.

## 9. The Finale: Live Production Under Sabotage

Tape 5 inverts the stack. The Understudy, bound by a formally correct finale in progress, plays along. The 58 Club does not: they cut breakers, block corridors, and unplug cameras to stop the sign-off. The player runs a live broadcast as crew and talent at once: switcher operation (source selection on face buttons mapped one-to-one with the physical console layout, so three acts of bench muscle memory pays off as competence under fire), cue execution from Craik's script, and staying in frame, because on camera is the one place nothing can touch her while she says the ending out loud.

---

# PART IV-B: SOLUTIONS, GENERATIONS, AND THE COVERAGE DIRECTOR

The replayability architecture beyond the four endings. Organizing metaphor from the fiction itself: **generation loss**. How you handle material determines what survives the transfer, so in this game, the method is the fidelity.

## 10. Approaches: Preserve, Ask, Force

Every major obstacle admits at least two of three approach families, each with a distinct cost signature:

- **Preserve (the conservator's way).** Careful, slow, craft-intensive: find the key, bake it properly, jump-cue by timecode, route power generously. Costs time and materials. Keeps Rita boring, and boring is safe.
- **Ask (the journalist's way).** The club as sources: Merle's canon, Harriet's memory, Vess's research, a trade, an improvised question. Fast, but costs interest: interesting people get coverage, and Ask solutions feed the Producer Track.
- **Force (the trespasser's way).** Pry it, drill it, degauss it, cut power to something else, brute-scrub. Instant, but costs burn-in damage and Rundown attention: noise attracts rehearsal, and Force solutions raise the hunter's aggression for the following nights.

The routing document's spines describe the Preserve path by default; Ask and Force branches exist at every major beat. The consequence philosophy: your problem-solving personality selects which horror game you get. The careful player fights time, the social player feeds the grooming meter, the forceful player wakes the hunter.

## 11. Generations: Tiered Truth

Every discoverable fact exists in up to three generations, and the accession log gains a **GEN field** the player fills:

- **1st generation (the master).** The primary source: Craik's own hand, the unedited frame, the original document. Complete, timestamped, citable. Earned by the most demanding method, and the only tier that fully assembles the buried stratum.
- **2nd generation (the dub).** A witness account, a damaged copy, a partial extraction. True but incomplete, or complete with exactly one detail altered. Every gen-2 source in the game carries one authored gap or one planted contradiction.
- **3rd generation (the broadcast).** The public story, the club's canon, the cover. Knowing what everyone agrees happened is itself information, if you log it as what it is.

**Worked examples:**
- *The instructional film (T2).* Preserve: locate the cabinet key; the full film plays; complete six-signal vocabulary (gen 1). Ask: Harriet recites from memory, fast, but her recitation includes a seventh signal that is not in the film, one the show added later, and the game never says whether it is a gift or a plant (gen 2). Force: pry the cabinet; the damaged film plays with dropouts; four of six signals, the rest learned by surviving them (gen 2, different gaps).
- *Airdate math (T2).* Preserve: assemble the 141 versus 138 discrepancy yourself from slates, logs, and listings (gen 1). Ask: Merle gives the club's canon, 138 and that is all there ever were, the cover story delivered warmly (gen 3). Force: lift Vess's research binder; his obsessive annotations include one insight nobody else has and one wrong theory presented with total confidence (gen 2).
- *The dead room key (T4).* Preserve: the shed under the beacon, as routed. Ask: Vess knows where it is, for a price paid in credit or trade. Force: drill the lock, and the room is never perfectly sealed again: Dead Air remains fully achievable, but the erase loop leaves a hairline hum on the radio, and the post-credit stinger implies one copy, somewhere, survived. The method contaminates the outcome without gating it.
- *Any Leland fact.* Scrub him (his answer, at wear cost: gen 1), ask the club about him (their version: gen 3), or read what he wrote before he was taken (what he knew then, which is not what he knows now: gen 2). Three generations of the same man.

**Hard guardrails:** generations never gate endings; the four endings remain conduct-gated exactly as specced. Generations gate understanding: gen-2 and gen-3 runs finish everything, but their picture of the truth has authored gaps, which means different playthroughs hold genuinely different accounts. Two players can both know the fire story and disagree, because one holds Craik's notebook and one holds Merle's telling. The game becomes its own telephone game, and inter-run debate is the engineered theory fuel (Dread Ledger 8.2, by construction rather than accident).

## 12. The Coverage Director: Reactive Scares

The Understudy is a performer, and performers play the room. It maintains a profile of the player and re-blocks its scares against it.

- **What it reads:** camera-checker or sprinter, early-averter or starer, favored corridors, hiding habits, and the take history, because **the unburned dailies are its scouting film**. Burn Your Dailies therefore has a second function: erasing a strike also resets its read on you. Hoarding your death footage makes the thing that killed you smarter, and the strike-recovery errand and the adaptive layer are one system.
- **Blocking variants:** every scripted set piece carries two or three blockings selected by profile. Camera-checkers get the compactus variant where the aisle monitor shows it absent when it is not; sprinters get the cut-off; hiders get the seek. **The poisoned-well rule:** monitor deception happens exactly once per run, ever, and is telegraphed by rising static, so trust is spent, never cheated, and the one-lie discipline extends into systemic scares.
- **The poltergeist layer:** it stages props to imply rule-breaks that always resolve as legal: a spare Chum hung on the catwalk rail, a chair turned to face a door. It dresses sets, because that is what a production does. The dock exception holds: it never stages the dock. The contract room stays pure.
- **Mood tracks the sheet:** players on a clean casting sheet get startled and confidence-broken. Players on their last line stop getting jump scares entirely and start getting savored: it slows, it waits outside rooms, it becomes theatrical, because a performer knows when the audience is already screaming inside. The scare style inverts with desperation, which means the adaptive system delivers startle to the confident and dread to the frightened, each at the moment it lands hardest.
- **What it never does:** violate broadcast grammar, enter sanctuaries, or produce an unearned kill. It exploits reads; it does not break rules. Fairness is the stage it performs on.

**The replayability statement:** no two runs hold the same truth, and no two players get the same scares. The four endings sit on top of that, not instead of it.

---

# PART V: CONTROLS

Gamepad primary (the streaming audience's platform reality), mouse and keyboard fully supported. Philosophy: equipment tactility. Every input should feel like operating machinery that predates you.

## Exploration (compound)

| Input | Gamepad | M/KB |
|---|---|---|
| Move / look | Left stick / right stick | WASD / mouse |
| Interact | X (tap) | E |
| Avert (clipboard) | Hold LB | Hold Q |
| Crouch / still | B (toggle) | Ctrl |
| Quiet Game breath | Hold RB rhythm, or mic | Hold Space rhythm, or mic |
| Binder (pause/journal) | Start | Tab |

## Bench (contextual)

| Input | Gamepad | M/KB |
|---|---|---|
| Jog/shuttle scrub | Right stick rotation, spring-return | Scroll wheel |
| Single-frame step | D-pad left/right | Scroll click-steps |
| Tape tension | Triggers (adaptive resistance on DualSense) | Hold LMB drag |
| Tool select | D-pad up/down | 1-4 |
| Commit (splice, log, grade) | Hold X | Hold E |

## Call-and-Response

Respond on-beat: tap X inside the cue-light pulse. Hold X for Quiet. Y opens the Improvise wheel when available. Mic mode replaces taps with speech and is never required.

## Switcher (finale and screenings)

Face buttons and bumpers map one-to-one to the console's physical button bank as displayed; the finale is playable because the hands already know the desk.

## Feel Notes

Jog wheel carries a light spring return with a soft detent per frame; clipboard raise runs about 200ms with an ease-out so Avert feels like a reflex, not a menu; tape hiss plays through the controller speaker during capture; tracking errors arrive as a fine rumble texture distinct from the heavy thud of grammar events. Reduced-motion setting flattens all camera sway and disables the CRT bloom pulse; nothing informational lives in motion alone.

---

# CLOSING: RUBRIC ALIGNMENT AND NAMED GAPS

**Signature mechanic statement (Dread Ledger 6.1):** the Restoration Bench plus Frame Discipline. One sentence for the store page: you restore the cursed tapes by hand, and the frame is the only place it can't touch you.

**Mechanics-theme unity (6.2):** every verb is archival or broadcast craft; there is no verb in the game that Rita would not have on a resume.

**Named gaps, honestly held:**
1. Forced real-time capture is a pacing risk if tape content ever dips below gripping; the mitigation is ruthless content editing, not a skip button, and that is a production commitment, not a design solve.
2. The casting-drift binder walks near the interface-lie rule; the boundary (dressing is allowed, deception is not, deception spends once at the end) must be enforced in review or the ED restraint collapses.
3. Vess's arc needs one dedicated scene anchor in Tape 4 or he risks reading as a device; candidate: his rejected edit, played once, in full, with the club watching.
4. The power budget can tip into FNAF pastiche if overtuned toward meter-watching; it should feel like electrician's planning, not battery anxiety, and the tuning target is that players think in routes, not percentages.


------------------------------------------------------------------------------
DOCUMENT 37 · restoration-game-master.md
------------------------------------------------------------------------------

# RESTORATION: GAME MASTER DOCUMENT
## The Complete Game, Start to Finish: Every Scene, Every Scare, Every Solution, Every Ending

**Version 1.0** | This document is canon. It integrates and supersedes conflicts with all prior Restoration documents. Systems referenced (Bench, Frame Discipline, Grammar, Rundown, Casting Sheet, Coverage Director, Approaches and Generations) are specced in the design and walkthrough docs; this document is the content.

**Reading conventions.** Scenes are coded by tape (T1.1). Dialogue is scripted verbatim. Stage directions are lean and character-bearing. Player-spoken lines appear as RESPONSE OPTIONS with stance tags (AUDIENCE / QUIET / IMPROVISE). Solutions are tagged [PRESERVE], [ASK], [FORCE] with the generation of truth each yields (G1, G2, G3). Scares are tagged [SCARE n] against the compendium in Appendix A. Rita speaks only inside the show's formats and her own paperwork; her interiority lives in ledger text, written in her hand.

**Character physical vocabularies (directions reference these):** Merle's hands stay busy with domestic objects; when they still, listen. Vess touches the label maker at his belt when nervous and the plastic pin when hurt. Harriet pauses mid-motion during break windows and resumes on the return cue. The Floor Manager is hands and countdowns, nothing else. Rita adjusts her gloves at decisions; the loupe swings into frame when she commits.

---

# TAPE 1: "A CLEAN SIGNAL"

## T1.1 ARRIVAL | Exterior, dusk, then Entry
The compound crouches on the hill under the tower's red pulse. Rita's car door, wind in guy wires, a hand-painted sign over industrial steel: THE 58 CLUB, EST. WITH LOVE. Merle opens before she knocks, dish towel over one shoulder.

MERLE: There she is. Our conservator. Oh, look at your gloves, you brought your own gloves. Come in, come in, the wind takes the door.
MERLE: Merle Cottry, president, cook, whatever else needs a body. We are so glad you said yes. You have no idea what it means, having a real professional. We've been making do with love and rubber bands.

## T1.2 THE TOUR | Rec room, kitchen, dorms
The rec room: mismatched armchairs in rows that almost face the big cabinet television, the shrine wall of clippings and enamel pins, a casserole whiteboard. Harriet sits with tea. Vess stands too fast.

VESS: You're the conservator. Vess. I sourced most of what you'll be working on. The provenance chains are, I mean, I documented everything, I can walk you through my system whenever.
MERLE: Breathe, sweetheart. Let the woman find her room first.
HARRIET: And now. The tour continues.
(Harriet says it like a station break. Nobody reacts, which is the first wrongness the game offers, unremarked.)

MERLE: (at the dorm door) Yours. Bath down the hall, kitchen never closes, and if the tower light bothers you, the curtain's thick. (her hands still on the towel) We eat at seven. It matters to us that you eat with us.

## T1.3 THE PROVING | Bench room
The bench: capstans, scopes, the TBC, the accession ledger squared to the desk edge. Merle sets down a battered reel.

MERLE: Junk reel. Local car dealership, 1973. Nobody will cry if it dies. Vess insisted we not hand you Gladhouse material until, his words, your hands checked out.
VESS: (from the doorway, pin catching the light) It's standard practice. It's what Leland did.
MERLE: (the towel stops moving) It's what our last archivist did, yes.

[TUTORIAL: inspect, bake timing, splice, capture, ledger entry. The junk reel plays a grinning salesman; the club drifts in to watch anyway, hungry for any old signal.]

## T1.4 NIGHT ONE | Living wing
[Free movement. S1 log station introduced at the library landing; first save signature.]
The rec room television plays static in a 4:3 frame with the set off at the wall. In the hallway feed, on the wall monitor, something crosses at the far end and stops at the frame line, toes to an invisible mark, and waits, and withdraws. [DREAD, uncatalogued: the obedience moment.]
Opening the binder at S1 surfaces the first green-ink margin note.

LELAND (green ink): You are safe as audience. Do not be interesting. Never accept a role.

## T1.5 CAPTURE ONE | Bench, day
Tape 1 bakes out clean. Capture runs in forced real time. On screen: THE GLADHOUSE, and Chum, patchwork and buttons, teaching six children on a carpet.

CHUM (on tape): Friends, do you know the Quiet Game? It goes like this. (sing-song) Hold your hands and hold your feet. Hold the words behind your teeth. Quiet as a button's eye, till I find you, by and by.
CHUM (on tape): When the lights go out, what do we do?
CHILDREN (on tape): We hold still!
CHUM (on tape): And when I find you?
CHILDREN (on tape): We go home!

The waveform is wrong for a third-generation dub: no loss, no hiss floor. Rita leans in; the loupe swings. Mid-episode, Chum stops. He turns from the children and walks toward the studio camera until his face fills the frame, button eyes and stitched grin, and holds, one beat past bearable, and then a single-frame lunge as the tape cuts to bars. **[SCARE 1: in-tape lunge.]**

[LEDGER COMMITMENT 1: log the generational anomaly. Options: TRUTH ("Generation loss absent; physically inconsistent with provenance") or COVER ("Exceptional storage conditions"). This entry begins the Conduct Ledger.]

## T1.6 MERLE REMEMBERS | Rec room
Merle watches the captured file twice through. Her hands find each other and hold on.

MERLE: The Quiet Game. Oh, I remember this one. I remember the rhyme, I remember Tommy Alder got the giggles and had to sit out.
RITA'S LEDGER (her hand, silent): No broadcast record of this episode exists. She remembers it anyway. Filed under: things I am not being paid to notice.
MERLE: (bright, wet-eyed) You've given us back a piece of our childhood, do you know that? Now Merle is just going to put the kettle on.
(She narrates herself. The towel never stops moving.)

## T1.7 ACT CLIMAX: THE MINI-SCREENING | Rec room, lights down
The club gathers. Over the doorway, unremarked, a cue sign wakes: RESPOND, in warm amber. On screen, Chum leads a call.

CHUM (on tape): Goodnight, Gladhouse! Say it with me!
CLUB (together, easy as breathing): Goodnight, Gladhouse!
[RESPONSE OPTION, first use. AUDIENCE: "(with the room) Goodnight, Gladhouse." QUIET: stillness, silence. IMPROVISE: "Goodnight, everyone." (The room's heads turn a half inch. PT rises. Merle beams.)]

VESS: (after, quiet, to Rita, thumb on the label maker) The sign. Over the door. You saw it light. (a breath) Leland used to say don't be interesting. He also left without saying goodbye, so.

*Tape 1 tallies: Startles 1 (in-tape). Captures possible: none. Assets: none. Threads opened: Conduct Ledger, Leland marginalia, Merle's impossible memory. The compound has not touched her yet. The tape has.*

---

# TAPE 2: "AIRDATES"

## T2.1 TRUST | Rec room, morning
MERLE: (keys on a crocheted fob) Control level's yours now. Leland had the run of it too. We don't give these to guests, we give them to family, so. (her hands still) Don't make me regret the word.

## T2.2 THE PATCHBAY | Control level
[TUTORIAL: patchbay routing, first mediated corridor over CTL, the breaker panel and the amperage budget. Master control's glass looks down into a dark Studio A; the monitor bank beside the glass shows the same room, and the difference between the two views is the lesson.]

## T2.3 THE AIRDATE CIRCUIT | Living wing, library
[PUZZLE: airdate math. Sources: production slates (BEN), station logs (LIB drawer), framed TV listings (KIT hallway), shrine clippings (REC).]
- **[PRESERVE, G1]:** Cross-reference all four sources yourself. Result: 141 slated, 138 aired. The three unaired slates carry dates that sit inside the same weeks as three shrine clippings: ALDER, TOMMY, 7, MISSING. BELL, IRIS, 6. PRICE, WENDELL, 8. The show ran "find our friend" segments for each. The ledger's GEN field accepts: G1.
- **[ASK, G3]:** MERLE: A hundred and thirty-eight episodes, dear, and I could sing you the last minute of every one. That's all there ever were. (Her hands fold. The towel stops.) The club's canon, warm as a blanket, logged as what it is.
- **[FORCE, G2]:** Lift Vess's research binder from his dorm. His annotations include one insight nobody else has (the slate numbering skips are clustered, not random) and one wrong theory in confident block letters (HE BURNED THE MISSING THREE TO HIDE A CONTRACT DISPUTE). If Rita's ledger later cites his insight without his name, the Vess-credit flag dies here.

## T2.4 THE FILM CABINET | Library media alcove
[PUZZLE: the instructional film, locked cabinet. The hand-signal vocabulary.]
- **[PRESERVE, G1]:** The key hangs on Merle's board, tagged in Leland's green ink: TRAINING. The film plays whole: WGLD STAFF ORIENTATION, 1971. Six signals taught by a smiling floor manager: YOU'RE ON (the point), CUT (the slash), STRETCH (taffy hands), WRAP IT UP (the circle), THIRTY SECONDS (the T), ON TIME (the nose touch).
- **[ASK, G2]:** HARRIET: (setting down her cup, mid-motion, resuming) But first. The signals. (she performs them, precise as liturgy, and then a seventh: both hands pressed flat, pushed down twice) Hold your applause. (a pause with weight in it) They added that one later. You'll want it.
  The seventh signal is in no film. Gift or plant, the game never says. It is also the only warning the unscripted seek ever gives. **[Generation payoff: see SCARE 8 blocking.]**
- **[FORCE, G2]:** Pry the cabinet. The damaged film plays with dropouts: four of six signals survive. The other two get learned the hard way, live.

## T2.5 "HE ASKS SO MANY QUESTIONS" | Kitchen
MERLE: (drying the same plate past dry) Vess found us more tape in two years than the club found in twenty. He's a good boy. (the plate stops) He asks so many questions, though. (she sets it down soft as an apology) You ask the right amount. I can tell.

## T2.6 CAPTURE TWO | Bench
Tape 2 runs color where the logs say the broadcast went out in black and white. In the audio bench, under the closing song, the spectrogram shows structure in the sidebands.
[**SIGN-OFF ASSET 1: THE MISSING VERSE**, extracted [PRESERVE, G1]:]

THE CLOSING SONG, final verse (recovered): Close the door and dim the light. Fold the day away. Everyone we love is home. And no one has to stay.

- **[ASK alternative, G2]:** Harriet can hum the verse from memory, faster than spectral work. Her version carries one wrong word: "everyone we love is HERE." If her version is the one performed in the finale, see the Phase 2 variant beat in T5.4.

## T2.7 NIGHT FOUR: FIRST BLOOD | REC to LIB to PB
[Forced load: bake running, work lights, mandatory corridor route. Overdraw trips a breaker mid-route.]
The corridor monitor dies. In the half second of live phosphor after power, something crosses the reflection where nothing crosses the hall. **[SCARE 2: the reflection cross.]**
Then the dark: CTL to PB, unmediated, and behind her, unhurried, the sound of a show being performed to no one, felt feet, a hummed bar of the closing song. **[SCARE 3: the blackout pursuit. First lethal sequence. Casting sheet live from this night forward.]**
At the breaker panel her gloves leave sweat prints on the handles. Power returns. The hall behind her is a hall.

RITA'S LEDGER: Reset breakers 2 and 5. Something in this building knows the closing song. Filed under: renegotiate rate.

## T2.8 ACT CLIMAX: THE SCREENING | Rec room
Lights down, rows filled, the RESPOND and HOLD signs live over the door like they grew there. Mid-episode, Chum lowers his voice to the carpet children, and half the room answers with the tape, in sync, eyes forward.

CHUM (on tape): When the lights go out, what do we do?
CLUB (unison, with the children): We hold still!
CHUM (on tape): And when I find you?
CLUB (unison): We go home!
CHUM (on tape, and the tape hiss drops away, and the room is too quiet): And our new friend in the back. What does she do?

[RESPONSE OPTIONS, under the amber pulse:
AUDIENCE: "(with the room, on the beat) I hold still." The room exhales. Merle's hand finds Rita's shoulder, proud.
QUIET: Stillness. The pause stretches. On the tape, Chum tilts his head, and the episode resumes, and Harriet's cup does not.
IMPROVISE: "I go home when the work's done." (The room turns, all of it, one motion. PT rises hard. On the tape, Chum laughs, delighted, a sound the mix cannot contain.) CHUM (on tape): Ohhh, I LIKE her.]

VESS: (after, in the kitchen doorway, pin in his fist) It never says my name. Three years. It never once. (the label maker clicks in his pocket, twice, like a habit praying) Good night.

*Tape 2 tallies: Startles 2 and 3; first captures possible. Asset 1 banked. Frequency fragment 1 of 3 (the verse sidebands) silently held. Vess-credit flag live in the ledger. The seventh signal, if taken, sits in the player's hands like a coin of unknown country.*

---

# TAPE 3: "SIGN-OFF"

## T3.1 THE PRETEXT | Rec room, then Transmitter Hall
- **[ASK, default]:** MERLE: Storage retrieval, if you're willing. The hall's a church of old boxes and my knees vote no. Leland kept meaning to. (the towel wrings itself) Leland kept meaning to do a lot of things.
- **[FORCE alternative]:** After-hours entry through the service door; the Rundown notices; tonight's patrol runs one segment denser.

[TH: the hum floor, cathedral heat, warning placards. S4 station hangs at the threshold. In the storage cage, three boxes in a dead man's order.]

## T3.2 CRAIK'S BOXES | Transmitter Hall cage
Top box: **THE FINALE SCRIPT [SIGN-OFF ASSET 4]**, typed, hand-amended. Middle: the notebooks, cue shorthand. Bottom, under everything, a child's handwriting on radio scripts: **[DEAD AIR ITEM 1: THE CHILDHOOD SCRIPT.]**

CRAIK'S NOTEBOOK, 1958 (boy's hand): Uncle says the best listeners get to be on the show. I am the best listener. I hold so still.
CRAIK'S NOTEBOOK, 1971: I built him a body so he would stop wearing mine. Television is bigger inside than radio. He fits. God help me, he fits.
CRAIK'S NOTEBOOK, 1977 (final page): A show that has ended cannot recur. Format keeps its own rules; it must, or nothing on it would be true. One correct finale. Song, goodnights, close the house, card, sign-off. Complete or nothing. (below, pressed hard enough to tear) God forgive the reruns.

Behind the cage, the DEAD ROOM door: felt-faced, locked, and the hum of the hall stops dead at its seam like sound refusing a border.

## T3.3 MASTER CONTROL | Cart racks
**[SIGN-OFF ASSET 3: THE STATION ID CART.]** Punched into the bench monitor, it plays: warm announcer, room tone of a smaller decade.
CART AUDIO: You're watching The Gladhouse, on WGLD, Channel fifty-eight.

## T3.4 CAPTURE: THE FIRE TAPE | Bench
[Forced watch. The centerpiece of restraint: no sting anywhere in this scene.]
On screen, the 1977 broadcast: the studio emptying, smoke walking in from the wings, and Chum performing to rows of nothing.
CHUM (on tape): Stay in your seats, friends! The Gladhouse loves you! Say it with me: the Gladhouse loves
(The line never finishes. The camera pans, smooth, operated, across an empty floor. No one stands behind it. The fire does not touch him. Transmission cuts to bars before any card, any song, any goodnight.)

RITA'S LEDGER: The finale exists. It is not lost. It is unfinished. Those are different words and I have never felt the difference in my hands before tonight.

## T3.5 NIGHT: THE RUNDOWN WAKES | Library
[The free-roam hunter activates. Segment audio places it: the story corner drifting through the stacks, the craft segment ticking in the workshop, the song owning the studio.]
Objective: the next reel from CLM. On the return leg, the studio speakers wake after fifty years, a sound like a building clearing its throat, and the Floor Manager stands at the stack end with one hand rising, and points. YOU'RE ON. **[SCARE 5: the you're-on.]**
The compactus cranks from the far end, aisle walls walking. **[SCARE 4: the chase opening.]** Escape is built, not run: LIB to CTL inside a break window, then PB, crank and patch under her own breath, the corridor going live monitor by monitor, and the performance behind her honoring each frame line as it lights.

## T3.6 THE PRE-SIGNED PAGE | S4, Transmitter Hall threshold
On the clipboard, the next blank line is not blank. Her handwriting. Tomorrow's date. **[SAVE SCARE, singular.]**
RITA'S LEDGER: I do not remember signing it. I checked the loops of the R the way you check a stranger's teeth. They are mine.

## T3.7 A CAMERA DIES | Any mediated corridor, systemic
[First witnessed camera-kill, staged by the Coverage Director as an authored event this once.] On the corridor feed: the far door, and then the lens filling, button eye to glass, static climbing like water, and the feed whites out. **[SCARE 6: the camera-kill.]** The patchbay maps one corridor shorter than it was.

*Tape 3 tallies: Startles 4, 5, 6. Assets 3 and 4 banked; Dead Air item 1; frequency fragment 2 of 3 (the fire tape's carrier tone). The Rundown owns the nights now. Leland's marginal notes end mid-sentence: "If you find me, don't"*

---

# TAPE 4: "PROVENANCE"

## T4.1 DELIVERY | Entry, dawn
Vess backs through the door hugging a crate, three days of beard, triumphant and afraid of his own cargo.
VESS: Storage auction. Paid cash. Unit was under CRAIK, E., that's Edith, his mother, she kept everything, Rita, she kept EVERYTHING. (the pin, touched twice) Tapes dated after the fire. After. Tell me what that means, because I've stopped being able to say it out loud.

## T4.2 THE SET | Studio A
The rebuilt Gladhouse, measured off the tapes to the centimeter: the carpet, the cubby wall, the little door in the painted house that all the goodnights close. The club calls it restoration. Standing on it is standing inside the show.
HARRIET: (at the rail, resuming from a pause nobody saw start) And now. You've seen it. When we come back, you'll understand why we never could burn it down.

## T4.3 THE DOCK | Scene dock (the contract room)
[Inventory task.] Rows of retired Chums on armatures, generations of him, fur going gray in order. **[SIGN-OFF ASSET 2: THE SIGN-OFF CARD]** in the props crate: WGLD CHANNEL 58, hand-lettered, GOODNIGHT. And in row three, mid-count, her gloved hand on a body that is warm. The game does nothing further. It never will, in this room.

## T4.4 LELAND | Bench
The impossible tape's background, frame-stepped: a man at the edge of frame, cropped by the composition like it refuses him, legal pad against his chest. Holding still. Playing the game. **[SCARE, uncatalogued: the recognition. Target is a held breath.]**
[THE FRAME-SEANCE OPENS. Questions written on the bench pad; answers arrive across frames; every scrubbing pass wears the only copy of him. The canonical thread, five questions:]

Q1 (written): Are you alive?
LELAND (legal pad, across four frames): FILED. NOT SHELVED.
Q2: What happened to you?
LELAND: IT ASKED ME TO SLATE A SCENE. THEN IT ASKED ME TO STAND IN. NEVER ACCEPT A ROLE. I WROTE YOU THAT IN GREEN.
Q3: How do I end it?
LELAND: FINISH THE FINALE. FORMAT KEEPS ITS OWN RULES. CRAIK WAS RIGHT. HE WAS ONLY EARLY.
Q4: Can you come back?
LELAND: ONLY IF THE HOUSE CLOSES WITH SOMEONE INSIDE. (next frame, smaller) LET IT BE ME.
Q5 (thread-complete): Are you sure?
LELAND (one frame, steady hand): I'VE READ THE ENDING. IT'S GOOD.
**[SCARE 7: his first answer arrives between two frames the player just stepped across.]**

## T4.5 THE REJECTED EDIT | Rec room
Vess threads his own cut, the one the club never mentions. It plays in full: competent, loving, wrong in a way no one can name, transitions landing a half-beat off the show's breath. The club watches in a silence with texture. On the final frame the tape stops itself, a clean mechanical refusal, and the take-up reel turns backward one rotation, deliberate as a headshake.
VESS: (standing in it, pin in his fist, voice level by force) It does that. Every copy. Every machine. (to Rita, and this is the whole man) Your cuts, it keeps. I checked the vault. It keeps yours.
MERLE: (soft, hands folded, merciless as weather) Sit down, sweetheart. There's cobbler.

## T4.6 MERLE, 1974 | Rec room, shrine wall
MERLE: I was seven. Route 9, the culvert end, past where the county stopped mowing. I walked out after a dog that wasn't mine and the light went and the corn does not care how loud a girl is. (her hands, for once, empty and open) And then the dark got warmer. Fur like a coat closet. It carried me the whole way singing the closing song, and it set me down where the porch light reached, and it waited in the ditch till my mother's arms had me. (she looks at the screen the way people look at churches) The papers said a searcher found me. No searcher sings. So you can bring me every date and every gap and every terrible arithmetic, and I will hold them, I promise you I will hold them. But I was carried. You don't vote against being carried.

## T4.7 THE SHED | Exterior, night, beacon pulse
[Movement timed to the blink for those who notice.]
- **[PRESERVE]:** the shed under the tower, Edith Craik's overflow: **[DEAD AIR ITEM 2: THE DEAD ROOM KEY]**, felt-wrapped, tagged in a boy's hand: FOR THE QUIET ROOM.
- **[ASK]:** VESS: The quiet room key? Yeah. Yeah, I know where. (the pin, turned once) Trade you. You log the Alder clipping find under my name. Somebody's name should be on something.
- **[FORCE]:** Bolt cutters, or later, drill the dead room door itself: the seal is never perfect again. Dead Air remains achievable; its epilogue carries a hairline hum, and the post-credit implies one copy, somewhere, survived. The method contaminates the outcome.

## T4.8 THE GLIMPSE | Fire corridor, night
Char under plastic, the wound the club could not heal or remove. At the corridor's elbow, for under two seconds, unmediated: it. A puppeteer whose puppet is missing, or a puppet whose puppeteer is missing, and the animation refuses to resolve which, and it does not turn, and the plastic sheeting breathes once with the draft of something passing that has already passed. **[THE DIRECT-SIGHT GLIMPSE. Once, ever.]**

## T4.9 THE SEEK | Studio wing, night
[Unscripted Quiet Game, first Rundown-called.] No warning, except: if Rita holds Harriet's seventh signal, the Floor Manager appears at the wing's end first, both hands pressed flat, pushed down twice. Hold your applause. Three seconds of grace the film-only players never get. **[SCARE 8, blocking split by generation: warned stillness versus ambush stillness.]** The seeking passes close enough to stir glove cotton.

## T4.10 ACT CLIMAX: LOCKDOWN | Everywhere at once
Every monitor in the compound cuts to the same channel on the same frame. **[SCARE 9.]** Doors seal on schedule, not in anger. In the rec room the armchairs stand in rows now, facing forward, and the RESPOND sign burns steady.
MERLE: (at the head of the room, in the show's palette head to toe, radiant) Fifty years, and we have a premiere. Lock-in's just till broadcast, dear. You'll thank us when you see the ratings.

*Tape 4 tallies: Startles 7, 8, 9, plus the recognition and the glimpse. Asset 2 banked (all four gatherable). Dead Air item 2. Frequency fragment 3 of 3 (the impossible tape's subcarrier). Séance live; wear burning in. Conduct Ledger's Vess window closes here.*

---

# TAPE 5: "THE PREMIERE"

## T5.1 PHASE 1: PREP | Full compound, soft pursuit
The Understudy walks the halls in the open now, talent before a show, honoring every doorframe like a mark. The club moves in ceremony. All movement legal; all movement watched.
[MANDATORY: broadcast chain routing, PB to MC to STA and back; asset verification at the bench. OPTIONAL, silent: MC to TH to DR with the key, the three-step re-patch through the radio rack, the assembled frequency dialed, everything left looking untouched.]

## T5.2 THE DECISION POINT | Bench
The ledger open. Three entries possible in her hand: AUTHENTICATE. DESTROY. PERFORM. Merle in the doorway, hands empty, watching the pen, saying nothing. The scene has no music. The pen is the loudest thing in the building.

## T5.3 PHASE 2: LIVE (PERFORM route) | Studio A and the arteries
[The finale as playable television. Craik's rundown, cue by cue. Rita on Craik's mark, reading the host lines he wrote for himself. On camera is the one safe place; the club cuts breakers, blocks corridors, unplugs; the sprint loop is STA to CTL to PB inside break windows and back before the return cue.]

CUE 1, COLD OPEN:
RITA (on camera, on his mark, gloves squared): Welcome back to the Gladhouse, friends. It's a special night. (the teleprompter is a dead man's typing) It's our last night.
CHUM (live, beside her, warm as ever, bound to the format and playing it beautifully): Ohhh, don't be sad! Every good day ends with a goodnight. That's how you know it was good.

CUE 2, THE SONG: the cart rolls; the club in the gallery cannot help joining; the missing verse lands.
EVERYONE: Close the door and dim the light. Fold the day away. Everyone we love is home. And no one has to stay.
[VARIANT BEAT, Harriet's hummed version: at "everyone we love is HERE," Chum stops singing for exactly one beat, head tilting, bookkeeping or mercy, and then permits it, and the take counts. The epilogue static will carry a fault line either way; the game never grades it aloud.]
**[SCARE 10, midpoint: the bell. Fifty years silent, nine hours silent, and it rings once, three feet behind camera position.]**

CUE 3, ONE LAST ROUND: the Quiet Game, played on camera, the seeking done in full view where it cannot touch, which is somehow worse.
CHUM (live): Hold your hands and hold your feet. Hold the words behind your teeth. Quiet as a button's eye. (directly to lens, to everyone at home, to her) Till I find you. By and by.

CUE 4, THE GOODNIGHTS: each resident of the painted house bid goodnight; in the gallery, club voices answer their own childhood involuntarily; Harriet's cup, raised since Tape 1, comes down.
**[SCARE 11: the studio plunge, a sabotage cut, tallies dying in sequence toward her; re-route at PB in the dark of the last break window.]**
**[SCARE 12, the delivery: hands, human and gentle and immovable, holding Rita off camera as it crosses the floor toward her, until the take fails or the grip does.]**
[THE FINAL BREAKER: Vess. If the ledger carried his name all game, his hand stops above the handle.]
VESS (credited variant, not looking at her): The Alder clipping. You wrote my name. (the hand comes down off the breaker, empty) Somebody's name should be on something. Go finish it.
VESS (uncredited variant): (nothing. The handle. The dark. Earn the retake.)

CUE 5, CLOSE THE HOUSE: the little door in the painted house, shut on camera by hand.

## T5.4 PHASE 3: THE LINE | Camera one
The script's last page: Goodnight from the Gladhouse. See you next, struck through, and Craik's margin, pressed hard: No. Tell them the truth or it doesn't take.

RITA (into the lens, to everyone at home): That's our show. That was always our show. (the studio holds its breath on purpose) There's no one at home anymore. The lights are off. The children grew up. You can stop looking for them. (a beat; the gloves, squared one last time) Say goodnight, Chum.

---

# THE ENDINGS, SCRIPTED

## ENDING 1A: SIGN-OFF, LELAND CLOSES
[Conditions: PERFORM entry; 4/4 assets; thread complete; Leland Integrity 60+.]
On the monitor beside camera one, inside the frame he was cropped from for two years, Leland steps to center and is allowed to be whole.
LELAND (on every screen at once, dry and kind): Goodnight, everyone. (a breath he does not need and takes anyway) It's okay. Nobody's watching.
CHUM (live, small, the performance finally allowed to end): Goodnight, Gladhouse.
Static. The card: WGLD CHANNEL 58, GOODNIGHT. Then, for the first time in fifty years, dark that is only dark. Harriet finishes her tea. The Floor Manager removes the headphones. Merle sits in front of a television that is finally just a television, freed and bereft, and the game holds on her hands, which have nothing to do.
FINAL LEDGER LINE (her hand): Deaccessioned: one (1) broadcast. Condition: complete.

## ENDING 1B: SIGN-OFF, RITA CLOSES
[Conditions: PERFORM; 4/4; Leland thread incomplete or integrity spent.]
Someone must close the house from inside.
RITA (stepping onto the set, into the light built to the centimeter): I'll close up. (to the lens, easy, like the end of any shift) Goodnight, everyone.
The epilogue arrives as stills: Rita in frame, in palette, at rest, the composition finally satisfied with her. The card. The dark. Merle keeps a chair facing the dead set. The ledger's last line is in green ink, not hers: SHE CLOSED IT PROPERLY. FILE UNDER: SAINTS.

## ENDING 2: THE NEW PRODUCER
[Conditions: AUTHENTICATE entry, or PERFORM with under four assets while Producer Track is 70+.]
The premiere goes out clean. The club weeps with joy in rows. On every platform at once, in resolution the puppet was never built to survive, Chum leans to the lens, fur rendered strand by strand, moisture in the button eyes.
CHUM (4K, intimate as a bedtime): There she is. Our new friend. (the grin, stitch by stitch) Say it with me, everyone. Welcome home.
MERLE: (front row, radiant, forever) Now Merle is just going to watch it again.
[POST-CREDITS: the game's single interface lie, spent here. The main menu carries an option that was never there: CONTINUE?, set in the tape world's character-generator face. NEW GAME now reads NEW EPISODE. It reverts on next launch. It happened anyway.]

## ENDING 3: THE BURN
[Conditions: DESTROY entry; available from Tape 4 via degausser and bake oven.]
[Playable destruction: reels to the coil, film to the heat, the archive dying under her own trained hands, the work performed with a conservator's precision because she does not know another way to touch tape.]
Then Merle in the doorway, no anger anywhere on her, which is the worst available outcome.
MERLE: Oh, honey. (she picks up a blanked reel, cradles it like a sleeping child) We have copies. Everyone has copies. That's what love is now. (she pats Rita's shoulder, twice, done) There's cobbler.
EPILOGUE: the ledger, weeks later, a new hand on the intake line: M. OYELARAN, INCOMING CONSERVATOR. The lore-lesson ending: format outlives instances, and the fire already taught this once.

## ENDING 4: DEAD AIR
[Conditions: everything in 1, plus the childhood script, the key, the assembled frequency, the Phase 1 re-patch, and the divert taken during the final break window: STA to TH to DR, the felt door closed. The dead room needs no camera; nothing can broadcast there, nothing can perform there; for one scene she stands outside the format entirely.]
The radio rack warm, the frequency held, the boy's script on the music stand beside the man's finale.
RITA (into the radio, to every set on every band): This is WGLD, Channel fifty-eight, leaving the air. To everyone at home. On every set. On every band. (the childhood script's line, kept because he wrote it at eight and it was always the true one) The show is over. You can put the toys away.
The erase loop propagates outward like weather. [Playable: the walk back, DR to TH to BEN, and then the long scene: Rita at her own bench, watching the archive die, reel by reel, entry by entry, the conservator's hands folded because there is nothing left for them to save. Merle inherits nothing. Lost media becomes actually lost.]
FINAL LEDGER LINE (her hand, steady): Signed off.
[FORCE-path variant: if the dead room door was ever drilled, the last second of static carries a hairline hum, and the post-credit is one shelf, somewhere unlit, one canister, unlabeled.]

---

# APPENDIX A: THE COMPLETE SCARE COMPENDIUM

**Families:** SCRIPTED (12, below), SYSTEMIC (Rundown-generated, uncapped), THE CAPTURE SCARE (Chum at lens distance; the signature; fires on every capture), THE SAVE SCARE (T3.6, singular), THE RECOGNITION (T4.4, held-breath class), THE GLIMPSE (T4.8, once ever). All scripted scares follow the silence tell (1.5 to 3 seconds); systemic scares carry their own tells (segment audio, rising static, the seek call or the seventh signal). The dock never springs. The well is poisoned once per run, ever.

| # | Tape | Scare | Blocking A (default) | Blocking B (camera-checker) | Blocking C (sprinter/hider) |
|---|---|---|---|---|---|
| 1 | T1 | In-tape lunge | Approach, hold, single-frame lunge | Identical (pre-profile) | Identical |
| 2 | T2 | Reflection cross | Crosses dead phosphor left to right | Crosses toward the reflected door Rita just checked | Holds still in reflection until she moves |
| 3 | T2 | Blackout pursuit | Performs behind her, steady gap | Kills the one monitor she keeps checking first | Cuts the corner she always sprints |
| 4 | T3 | Compactus opening | Shelves crank from far end | Aisle monitor shows the aisle empty (poisoned well, once) | Shelves crank BOTH ends; escape is up and over |
| 5 | T3 | The you're-on | Point from stack's end | Point delivered through a monitor she trusts | Point from behind, reflected in dead glass |
| 6 | T3 | Camera-kill witnessed | Far door, lens fill, whiteout | Her most-used corridor camera dies first | The kill happens off screen; she finds the dead map |
| 7 | T4 | Séance first answer | Text changes between stepped frames | Answer appears on the monitor's reflection first | Answer arrives one frame BEFORE the question is finished |
| 8 | T4 | Unscripted seek | Cold call, no warning | Cold call, monitors all show calm | WARNED variant if seventh signal held: hold-your-applause, three seconds grace |
| 9 | T4 | Lockdown sync | All monitors, same frame | Her routed corridors sync last, one by one | The sync starts in her hiding spot's feed |
| 10 | T5 | The bell | Once, behind camera position | Once, on the monitor a half-second early | Once, from the dock direction, impossibly |
| 11 | T5 | The plunge | Tallies die in sequence toward her | Her coverage plan dies in route order | Total instant dark; the beacon through the skylight is the only light |
| 12 | T5 | The delivery | Held off camera as it crosses | Held facing the dead monitor bank | Held in her favorite hiding spot |

**Coverage Director mood law:** clean sheet earns startle and confidence-breaks (including staged props, never in the dock); last casting line earns savoring: it stops jump-scaring and waits outside rooms. Startle for the confident, dread for the desperate, each where it lands hardest.

---

# APPENDIX B: THE SOLUTIONS MATRIX

| Obstacle | PRESERVE (cost: time/materials) | ASK (cost: interest/PT) | FORCE (cost: burn-in/aggro) |
|---|---|---|---|
| Airdate math (T2) | Full cross-reference. **G1**: 141/138, three dates, three names | Merle's canon. **G3**: "138, and that's all there ever were" | Vess's binder. **G2**: one true insight, one confident wrong theory; credit flag at risk |
| Film cabinet (T2) | Merle's board key. **G1**: six signals | Harriet's recital. **G2**: six plus the seventh (Hold Your Applause) | Pry it. **G2**: four signals; learn two live |
| Missing verse (T2) | Spectrogram. **G1**: exact text | Harriet hums it. **G2**: one wrong word ("here" for "home"); finale variant beat | none |
| TH access (T3) | wait for Merle's errand | Merle's pretext, immediate | After-hours entry; Rundown +1 segment that night |
| Dead room key (T4) | Beacon shed, felt-wrapped | Vess trades for a named credit | Drill the door; seal imperfect; hummed epilogue; one surviving copy implied |
| Any Leland fact | Scrub him. **G1**, at wear | Ask the club about him. **G3**: their version | His old notes. **G2**: what he knew before, not after |
| CLM reel runs (nightly) | Route coverage first, slow | Vess fetches; he now holds a favor | Sprint it dark; take the odds |
| Power shortfalls (T3+) | Generous routing, planned | Merle unlocks the kitchen circuit, with questions | Cut the dorm heat; the club notices; warmth cools by one act |
| Séance efficiency (T4) | Timecode jump-cues from green ink: 1 pass per answer | none | Blind scrubbing: 2 to 3 passes per answer; Leland pays |
| Locked shed (T4) | Merle's board, tagged EDITH | Vess, as above | Bolt cutters; beacon-lit noise; patrol density up |

**Law of the matrix:** Generations never gate endings. They gate understanding, and every G2 source carries exactly one authored gap or planted contradiction, tracked in the writers' room, never accidental.

---

# APPENDIX C: SYSTEMIC LINE POOLS AND THE SIGNAL GLOSSARY

**Chum, the Rundown segments (location audio):** STORY CORNER (library): "Once there was a house where nobody had to knock." CRAFT TIME (workshop): "Scissors are for helpers. Are you a helper?" THE SONG (studio): the closing song, hummed, verse withheld. THE QUIET GAME (anywhere): the rhyme, at distance, getting the words right.

**Response pools (Rita's spoken lines, the only speech she owns):**
AUDIENCE set: "Goodnight, Gladhouse." / "We hold still." / "We go home." / "(with the room, on the beat)"
QUIET set: (stillness; the absence is the line)
IMPROVISE set: "I go home when the work's done." / "Ask me tomorrow." / "Who's asking, the show or the room?" / "I don't take roles. I take notes."

**Club barks, escalating by act:** T1: "Sleep well, dear." T2: "The sign likes you." T3: "Leland worked late too." T4: "You'll want to look nice for it." T5: "It's almost time, it's almost time, it's almost."

**The Floor Manager (complete spoken inventory):** "In five, four..." (three, two, one are hands). Nothing else, ever.

**Signal glossary:** YOU'RE ON (point): freeze; you are performance. CUT (slash): a scene is being ended, somewhere. STRETCH (taffy): the break window extends. WRAP IT UP (circle): the window closes early. THIRTY SECONDS (T): exactly that. ON TIME (nose): traversal on schedule; a mercy. HOLD YOUR APPLAUSE (both hands pressed down, twice): unscripted seek incoming; three seconds; known only through Harriet.

---

# APPENDIX D: DOCUMENT PROPS (canonical found text)

**Leland's green-ink margin set:** 1. "You are safe as audience. Do not be interesting. Never accept a role." 2. "It counts rooms the way we count pages." 3. "The dock is honest. Nothing else is, but the dock is." 4. "Timecodes below. If you ever need to ask me anything, ask cheap." 5. (final, mid-sentence) "If you find me, don't"

**Craik's notebook, canonical excerpts:** as scripted in T3.2, plus one loose page: "Merle Cottry, age 7, returned. I did not send him. He went. I have stopped knowing which of us is the vessel."

**The club charter, framed at ENT:** "The 58 Club exists to preserve what loved us first."

**The casting sheet (studio wall):** THE GLADHOUSE, FINAL EPISODE. CAST: TOMMY ALDER. IRIS BELL. WENDELL PRICE. LELAND MERRICK. (blank) (blank) (blank) AND INTRODUCING ______.

---

# CANON NOTES AND TUNABLES
Numbers marked tunable elsewhere remain tunable: sheet lines (4/7/0), paper economy (3 lines per station per tape), wear per pass (7/3.5), PT weights (A-captures +10 each, T2 improvise +10, T4 gathering +10, read-through role +15, audition at 70), seek grace (3 seconds), sight grace (about 1 second). New Game Plus carries one nod, never a system: a single item lost in the prior run stands on the set in Tape 1, in shot, unremarked.


------------------------------------------------------------------------------
DOCUMENT 38 · restoration-player-routing.md
------------------------------------------------------------------------------

# RESTORATION: Player Routing Document
## Exact Movement Through the Map, Tape by Tape, and Every Thread to Every Ending

**Version 1.0** | Assumes the map, systems, and beat structure of the prior documents. Rita's full name is Rita Ivori throughout the project.

---

## MOVEMENT GRAMMAR (how the game teaches traversal)

Before the routes, the rules the routes are built on:

1. **The pendulum.** Tape 1 trains a home loop (Dorms, Rec Room, Library, Bench) until it is muscle memory. Every later act is a violation of that loop, which is why violations register as fear.
2. **Mediated corridors are player-built roads.** From Tape 2 onward, safe night travel is something you construct at the patchbay: route a camera chain along a path, and that path is protected while powered. The player's mental map becomes two maps, the floor plan and the coverage plan.
3. **Break windows are traffic lights.** The studio clock and ON AIR sign create legal crossing intervals per zone. Traversal legs are tuned to fit a window when planned and to miss it when panicked.
4. **Log stations are waypoints.** Five clipboards (S1 Library landing, S2 Master Control, S3 Green Room, S4 Transmitter Hall entry, S5 Rec Room) double as save points and breadcrumbs; new zones always place their station near the threshold so the first visit teaches the retreat line.
5. **One-way moments are rare and loud.** The map stays reversible except at scripted commitments (the Tape 4 lockdown, the Tape 5 phases), so backtracking for lore is always honored until the game says otherwise, once, unmistakably.
6. **The high road costs noise.** Catwalks over Studio A let mastery players route above danger, paying in ladder exposure and audible grating.

**Zone codes used below:** ENT entry, REC rec room, KIT kitchen, DRM dorms, LIB library stacks, BEN bench room, CLM climate room, FIRE fire corridor, CTL control corridor, MC master control, PB patchbay and breakers, STA Studio A, CAT catwalks, GRN green room, DOCK scene dock, TH transmitter hall, DR dead room, EXT exterior and tower.

---

## TAPE 1: "A CLEAN SIGNAL" (Days 1-2, Nights 1-2)

**Day 1 spine:** ENT → REC (Merle's welcome, shrine wall introduced) → KIT → DRM (room assignment, binder acquired) → LIB (stacks tour, S1 station shown) → BEN (junk-reel proving: inspect, splice, capture tutorial) → bake of Tape 1 begins (timed hold) → REC (dinner social; Vess's plastic pin, Harriet's phrasing, first cast reads).
*Optional loop:* KIT hallway framed TV listings (future airdate-math material, plantable now).

**Night 1 spine:** DRM → living-wing corridor → REC (the 4:3 static television) → corridor wall monitor: the frame-edge obedience discovery (something honors the frame like a performer hitting marks) → LIB landing S1 (first save; opening the binder here surfaces Leland's first green-ink note) → DRM.
*Design intent:* the route is a straight out-and-back; night one must feel safe because it is.

**Day 2 spine:** DRM → BEN (Tape 1 capture, forced real time, The Quiet Game episode; the zero-generation-loss anomaly; first accession commitment: truth or cover) → REC (Merle's impossible-memory scene).

**Night 2 spine:** DRM → LIB aisle (first scripted Quiet Game, low stakes, stillness taught) → return via REC (Harriet's freeze catchable at the KIT threshold in periphery).

**Act climax route:** all roads to REC for the mini-screening; RESPOND sign lights; one correct audience beat; act out.

*Movement lesson of the act:* the pendulum. *Threads opened:* Conduct Ledger begins (Day 2 entry); buried stratum begins (Leland margin notes).

---

## TAPE 2: "AIRDATES" (Days 3-4, Nights 3-4)

**Day 3 spine:** REC (Merle grants control-level access as trust ritual) → CTL → MC (room read; cart racks noted; S2 station) → PB (patchbay tutorial: build the first mediated corridor covering CTL; breaker panel and amperage budget taught) → BEN (Tape 2 into the bake).
*Optional loop, the airdate circuit:* REC shrine wall clippings → KIT hallway listings → LIB records drawer. Three stations of paper across the living wing; the 141 versus 138 discrepancy and the three unaired dates assemble only in the player's log.

**Night 3 spine:** DRM → CTL → MC window (observe a full break window on the studio clock; the Floor Manager glimpsed below, counting the corridor out) → return. First deliberate use of a break window to cross CTL.

**Day 4 spine:** BEN (Tape 2 capture: the color anomaly) → audio bench spectrogram tutorial → **Sign-Off Asset 1, the missing verse**, extracted from the sidebands → LIB media alcove (the instructional film: real floor-manager hand signals taught in-fiction; the threat vocabulary is now the player's).

**Night 4 spine (first blood):** objective forces load: bake running, work lights, and a required corridor route REC→LIB. Overdraw trips a breaker mid-route; monitor dies; the reflection cross (startle) → the blackout pursuit: dark traversal CTL → PB with it audibly performing behind her, unmediated, the game's first lethal sequence and first possible capture; the casting sheet is live from this night forward → reset breakers → re-route smarter, return.
*Movement lesson:* the coverage map is a budget, and the floor plan is not the real map.

**Act climax route:** REC screening, full call-and-response under witnesses; the unison; the line addressed to our new friend in the back; Vess's overreach and the held second.
*Threads advanced:* PT rises with an A-grade capture and any improvisation here; frequency fragment 1 of 3 (the verse sidebands) is silently banked for diggers.

---

## TAPE 3: "SIGN-OFF" (Days 5-6, Nights 5-6)

**Day 5 spine:** REC (storage-retrieval pretext from Merle) → CTL → MC → TH threshold (S4 station placed at the door; the hum floor begins) → TH storage cage: **Craik's boxes**, yielding in this order: **the finale script (Asset 4)**, the cue-shorthand notebooks, and beneath everything the childhood radio scripts (**Dead Air item: script**) → DR door discovered behind the foam baffles, locked, felt-lined, silent even through steel → return MC: cart rack search, **the station ID cart (Asset 3)**.
*Optional loop:* TH catwalk over the transformers for the notebooks' loose pages; noisy, optional, rewards the thorough.

**Day 6 spine:** BEN (the fire tape capture: the emptied burning studio, the pan with no operator; forced watch; no sting) → the finale-script reading scene at the bench: the endgame crystallizes (the show never ended).

**Night 5 spine (the first full stalking sequence):** objective: retrieve the next reel from CLM. Route DRM → REC → LIB → CLM. On the return leg, the you're-on signal: studio speakers wake (startle 2) → **the compactus chase**: shelves cranked from the far end while Rita is between stacks; escape requires improvising a mediated corridor: LIB → CTL sprint inside a break window → PB (crank, patch, power) → protected walk home.
*Movement lesson:* everything taught in Tape 2 (windows, coverage, budget) is now survival, not convenience.

**Night 6 spine:** routine save walk to S4 discovers **the pre-signed log page**, Rita's handwriting, dated tomorrow (quiet horror; the save system's one scare).

*Threads advanced:* Assets 3 and 4 banked; Dead Air items 1 of 3 (childhood script); frequency fragment 2 of 3 (the fire tape's carrier tone, spectrogram); Leland's notes end mid-sentence, and frame-steppers find one anomaly in Tape 3's background as foreshadow.

---

## TAPE 4: "PROVENANCE" (Days 7-8, Nights 7-8)

**Day 7 spine:** CTL → **STA reveal** (the rebuilt Gladhouse set; standing inside the show) → GRN (S3 station) → **DOCK inventory task**: the spare Chum rows; **the sign-off card (Asset 2)** in the props crates; the warm one, found by touch; the game does nothing further → FIRE unsealed from the LIB side (char under plastic sheeting; traversed by daylight once, so its geography is known before it is feared).
*Event:* Vess delivers the impossible tapes at ENT.

**Day 7-8 bench thread:** BEN captures of the impossible tapes → **Leland recognized in frame** → the Frame-Séance opens: jog-wheel stepping, notepad questions, answers across frames, wear accruing per pass and burning in.
*Social spine:* REC, Vess's anchor scene (his rejected edit, played once, in full, the club silent) → REC shrine, Merle's 1974 scene (the comfort is real).

**Night 7 spine (exterior):** ENT → EXT under the beacon pulse (movement timed to the blink for those who notice) → the tower-base shed: the overflow of the storage-unit boxes auctioned under Craik's mother's name → **the dead room key (Dead Air item 2)** → return before the window closes.

**Night 8 spine:** LIB → FIRE (**the scripted direct-sight glimpse**, under two seconds, undecidable) → emerge at DOCK → GRN → S3 save.

**Act climax route (the lockdown):** every monitor in the compound switches to the same channel at once; doors seal; the hub converts, chairs in rows, REC becomes the premiere gallery. The map's reversibility ends here, loudly, once.

*Threads advanced:* Asset 2 banked (all four gatherable by now); Dead Air item 2 of 3 (key); frequency fragment 3 of 3 (the impossible tapes' subcarrier); Leland thread live with the wear economy; Conduct Ledger's Vess-credit entries close this act (the last chance to have named his work truthfully).

---

## TAPE 5: "THE PREMIERE" (one continuous night)

**Phase 1, Prep (free roam under soft pursuit).** The Understudy cooperative and therefore everywhere, walking the halls like talent before a show; the club ceremonial; movement legal everywhere but watched.
- **Broadcast chain routing (mandatory):** PB (master routing puzzle) → MC (uplink checks) → STA (floor checks) → PB. The routing mastery exam; three acts of patchbay literacy, cashed.
- **Asset verification (mandatory for Perform):** BEN, ledger open, four assets confirmed.
- **The Dead Air re-patch (optional, silent):** MC → TH → DR (key) → the dead room patch panel, three-step re-route of the completed chain through the radio rack → dial the assembled frequency (the three fragments, combined earlier at the audio bench) → leave everything looking untouched → return.
- **The decision point:** BEN, the ledger, three possible entries in Rita's hand: Authenticate, Destroy, Perform. Merle in the doorway, watching the pen, saying nothing.

**Phase 2, Live (Perform route).** The finale as playable television. Home position: STA floor, in frame, on cue. The sabotage loop: cue executed → a breaker cut somewhere → sprint STA → CTL → PB inside the break window → re-route → back on the floor before the return cue. Coverage segments built in Phase 1 are the safe stretches; the catwalks are the mastery detour when CTL is blocked. Midpoint: **the bell rings once** (startle 6). Late loop: the studio plunge, tallies dying in sequence toward her (startle 7). Final breaker: Vess, whose hesitation exists only if the ledger named him all game; the hesitation is the window.

**Phase 3, The Line.** Camera one, Studio A, the fourth wall broken on purpose: into the lens, to everyone at home, the truth that no one is watching anymore. Unless the divert is taken (below).

---

## THE FOUR THREADS: COMPLETE PATHS TO EACH ENDING

### THREAD 1A: SIGN-OFF, Leland Closes (the full route)
1. Assets on schedule: verse (T2, BEN spectrogram), cart (T3, MC), script (T3, TH boxes), card (T4, DOCK).
2. **The Leland discipline:** his thread needs five answered questions at the bench across Tapes 4-5. Wear math: Leland Integrity starts at 100; each scrubbing pass costs 7 (Late Night) or 3.5 (Matinee), and wear burns in across reloads. Hunting blind runs two to three passes per answer and bankrupts him. The respectful method: his own margin timecodes (green ink, banked since Tape 1 if collected) let you jump-cue, one pass per answer, five passes total, roughly 65 integrity remaining, above the 60 threshold. The route rewards the player who read his notes for nine hours.
3. Phase 1: chain routing + asset verification. Ledger entry: **Perform.**
4. Phase 2: full cue sequence survived; Vess window used or fought through.
5. Phase 3: the line. Leland, already cast and still whole enough, says goodnight from inside the frame. Static, sign-off card, Channel 58 dark, Harriet's tea, the headphones removed.

### THREAD 1B: SIGN-OFF, Rita Closes
Identical to 1A minus the Leland discipline (thread incomplete or integrity under 60). Someone must close the house from inside; Rita accepts the one last role; the epilogue is hers from within still frames.

### THREAD 2: THE NEW PRODUCER (two on-ramps)
- **On-ramp A, the choice:** any run, any state → Phase 1 ledger entry: **Authenticate** → Phase 2 becomes assisting the premiere from MC beside the club, no sabotage, eerie cooperation → the migration succeeds → say it with me → the game's single interface lie, post-credits.
- **On-ramp B, the audition clause:** ledger entry **Perform** with fewer than four assets while Producer Track is 70 or higher. PT arithmetic for a deliberate run: A-grade on all five major captures (+50), improvise at the Tape 2 screening (+10), improvise at the Tape 4 gathering (+10), accept the read-through role beat in Tape 4 (+15). The incomplete finale is received as an audition, and the show does not kill talent.

### THREAD 3: THE BURN
Available from Tape 4 onward. Route: BEN → CLM (the degausser) with the masters, plus the bake oven for the film elements → Phase 1 ledger entry: **Destroy** → the playable destruction sequence → the failure the fire already taught: offsite copies, format outliving instances → epilogue: the club begins again, a new conservator's name in the ledger. The lore-lesson ending, and the proof of why Thread 1 exists.

### THREAD 4: DEAD AIR (the buried-stratum route, superset of 1)
1. Everything in Thread 1 (all four assets; the Perform entry; the finale performed).
2. **Plus the Dead Air set:** the childhood script (T3, bottom of Craik's boxes), the dead room key (T4 Night 7, EXT shed), and the assembled frequency: fragment 1 the verse sidebands (T2), fragment 2 the fire-tape carrier (T3), fragment 3 the impossible-tape subcarrier (T4), combined at the BEN audio bench into one dialable number.
3. **Plus the Phase 1 re-patch:** MC → TH → DR, three-step re-route through the radio rack, frequency dialed, room left looking untouched.
4. **The divert, Phase 3:** during the final break window (the only interval both the club and the Understudy hold), leave camera one: STA → TH → DR, close the felt door. The dead room needs no frame, because nothing can broadcast there and nothing can perform there; she is, for one scene, outside the format entirely. The sign-off is spoken into the radio, in the original medium, reaching everyone at home across every format at once.
5. **The price, played:** the erase loop propagates; route back DR → TH → BEN; Rita sits at her own bench and watches the archive die, reel by reel, entry by entry. Merle inherits nothing. Lost media becomes actually lost. The ledger's final line, in her hand: signed off.

### QUICK MATRIX

| Ending | Ledger entry | Assets | Leland | PT | Dead Air set | Divert |
|---|---|---|---|---|---|---|
| 1A Sign-Off (Leland) | Perform | 4/4 | Thread done, LI ≥ 60 | any | no | no |
| 1B Sign-Off (Rita) | Perform | 4/4 | otherwise | any | no | no |
| 2 New Producer | Authenticate, or Perform | any, or < 4 | any | any, or ≥ 70 | no | no |
| 3 The Burn | Destroy | any | any | any | no | no |
| 4 Dead Air | Perform | 4/4 | any (1A discipline still honored in epilogue) | any | 3/3 | yes |

---

## CLOSING NOTE ON ROUTING PHILOSOPHY

Every ending is reachable by conduct performed in space: entries written at a bench, objects carried between rooms, a re-patch done with hands, a walk taken during a window. There is no menu choice in this game that is not also a place the player stood. That is the routing document's one rule, and every future content addition should be tested against it.


------------------------------------------------------------------------------
DOCUMENT 39 · restoration-room-inventory.md
------------------------------------------------------------------------------

# RESTORATION: ROOM INVENTORY AND INTERACTABILITY BIBLE
## Every Space, Every Prop, and When Each Becomes Touchable

**Version 1.0** | Precedes room rendering. Canon sources: routing doc (zones), master document (scenes), design doc (systems). This file is the set-dressing and interaction authority.

---

## ART DIRECTION CANON: THE CRAFTED WORLD

All spaces and characters render in the reference-plate style of the Chum set: photographed-craft realism. Boiled wool, felt, worn pine, brushed brass, waxed thread, visible stitching, tool marks, and joinery on every surface. Human characters are crafted figures in the same language: cloth and needle-felt over armature, glass or button eyes, seamed hands. **Doctrine amendment:** the former "naturalistic compound versus period tape world" contrast is now carried by lighting and the video-artifact pipeline alone; material language is unified. The dependability pillar rewrites to: the compound must feel physically dependable in craft logic. Nothing in the real world glitches; wool behaves like wool.

---

## INTERACTABILITY LEGEND

- **Gate:** T1 to T5 = first tape it can be touched. N = night only. EVT = scripted event window. COND = condition-gated (stated). SPAWN = appears on trigger. DYN = state evolves over the game.
- **Verb:** inspect (read/flavor), take, operate, use-on, sign, commit.
- Every room lists **State changes by tape** where the room itself transforms.

---

## 1. EXTERIOR: LOT, TOWER BASE, GUY FIELD (EXT)

| Item | Interact | Notes |
|---|---|---|
| The tower + red beacon | T1 · inspect | Beacon pulse is a night movement metronome; never operable |
| Guy-wire field | T1 · traverse | Wind audio source; wires hum in the crafted-world register (waxed cord) |
| Rita's car | T1 · inspect | Locked in by the club's van from T4 lockdown; inspecting it then updates flavor |
| Hand-painted 58 CLUB sign | T1 · inspect | "EST. WITH LOVE" |
| The shed | T4 · operate | Locked. PRESERVE: EDITH-tagged key from the kitchen key board. FORCE: bolt cutters (TH tool wall); raises Rundown density that night |
| Edith Craik's overflow boxes (shed) | T4 · take | Contains the DEAD ROOM KEY, felt-wrapped, tagged FOR THE QUIET ROOM; child's drawings of Chum, pre-show |
| Gravel lot floodlight | T2 · operate | Draws from the amperage budget; a trap for the generous |

**State changes:** T4 N7 is the only mandated exterior night; beacon timing gifts the observant.

## 2. ENTRY / FRONT OF HOUSE (ENT)

| Item | Interact | Notes |
|---|---|---|
| Club charter, framed | T1 · inspect | "The 58 Club exists to preserve what loved us first" |
| Coat pegs | T1 · inspect · DYN | Member coats drift into show palette by tape; a readable group-state meter |
| Bulletin board | T1 · inspect · DYN | Casserole rotation, screening notices; T5 gains the PREMIERE bill |
| Guest book podium | T1 · sign | One-time flavor signature; Leland's entry two pages back, never checked out |
| Umbrella stand | T1 · inspect | One umbrella has a child-size handle; never explained |
| Vess's delivery spot | T4 · EVT | The impossible-tapes crate scene (T4.1) plays here |

## 3. REC ROOM (REC) · the hub

| Item | Interact | Notes |
|---|---|---|
| Cabinet television | T1 · inspect · DYN | N1 static in 4:3 with the set off at the wall; T4 lockdown sync; goes truly dark only in ending 1 |
| Armchairs | T1 · use · DYN | Casual arrangement until T4 lockdown converts them to forward-facing rows |
| Shrine wall | T1 · inspect | Clippings: ALDER, BELL, PRICE missing-persons pieces beside the show's "find our friend" articles; the deducible layer's core paper; the gray flannel jacket photo lives here |
| Cue signs (RESPOND / HOLD) | EVT · read | Dormant until the T1 mini-screening; lit only during response windows; never player-operable |
| Projector + screen | EVT · operate | T1.7 mini-screening; T2.8 Screening; T4.5 Vess's rejected edit |
| S5 log station | T1 · sign | Save; paper economy on Late Night |
| Harriet's chair + teacup | T1 · inspect · DYN | The cup rises across the game; resolves only in ending 1 |
| Gladhouse licensed board game | T1 · inspect | 1975 box; the rulebook's counting rhyme is missing its fourth line, decades early |
| Photo albums | T2 · inspect | ASK-tier lore (G3): the club's canon in snapshots |
| Doily'd equipment rack | T1 · inspect | Domesticity over broadcast steel; the room's thesis in one prop |

**State changes:** genuinely safe until T4 lockdown; converts to premiere gallery T5; sanctuary status revoked on conversion.

## 4. KITCHEN (KIT)

| Item | Interact | Notes |
|---|---|---|
| Kettle | T1 · inspect | Merle's scenes anchor here |
| Key board | T2 · take | PRESERVE keys: TRAINING (film cabinet, Leland's green tag) and EDITH (shed, from T4) |
| Framed TV listings, hallway | T2 · inspect | Airdate-math source two of four |
| Kitchen circuit sub-panel | T3 · COND · operate | ASK power solution: Merle unlocks it, with questions; FORCE alternative is cutting dorm heat, and the club notices |
| Casserole dishes, plate rack | T1 · inspect | The dried-past-dry plate beat (T2.5) uses the rack |
| Fridge + magnets | T1 · inspect | Children's drawings under magnets; one is signed T.A. |
| Coffee urn | T1 · use | Small stamina flavor; never a system |

## 5. DORMS AND RITA'S ROOM (DRM)

| Item | Interact | Notes |
|---|---|---|
| Rita's dresser: the seven items | T1 · inspect · DYN | Watch, pen, photograph, lighter, compact, keys, loupe. One vanishes per capture, loupe last; each later reappears as a prop inside restored episodes |
| The binder | T1 · operate | Meta UI home; pause, presentation form, ledger access |
| Bed | T1 · use | Advances day/night phases where scripted |
| Mirror | T1 · inspect · DYN | Reflection budget scripted; from T3 her reflections compose better |
| Thick curtain | T1 · operate | Blocks the beacon; purely humane |
| Vess's room | T2 · COND · enter | Door ajar; entering uninvited is the FORCE path to his research binder (G2) |
| Vess's research binder | T2 · take (FORCE) | One true insight, one confident wrong theory; taking it risks the credit flag |
| Label maker, spare | T2 · inspect | His habit, documented |
| Harriet's room | never · inspect through door | Everything inside mid-motion; the door never opens |
| Merle's room | T1 · inspect | Open door policy; quilt drifts to show palette by T4 |
| Communal bath | T1 · use | One mirror here obeys the same reflection budget |

**State changes:** the dresser is the game's quietest horror meter; by a bad run's end the room is nearly empty.

## 6. TAPE LIBRARY (LIB)

| Item | Interact | Notes |
|---|---|---|
| Compactus rolling stacks | T1 · operate | Player-cranked moving walls; the T3 chase geometry; noise draws attention at night |
| Reel shelving + canisters | T1 · inspect/take | Browsable spines; retrieval objectives live here |
| Dailies canisters | SPAWN · take | One appears per capture, labeled SCENE/TAKE; carry to CLM degausser to burn a strike; unburned canisters feed the Coverage Director |
| Card catalog | T1 · operate | Search aid; Leland's cross-reference cards in green |
| S1 log station (landing) | T1 · sign | First save taught here; binder's first green note surfaces on first open |
| Station log drawer | T2 · inspect | Airdate-math source one of four |
| Media alcove: film cabinet | T2 · operate | Locked. PRESERVE: TRAINING key. FORCE: pry (damaged film, four of six signals) |
| 16mm projector | T2 · operate | Plays the instructional film; the signal vocabulary lesson |
| Leland's desk | T1 · inspect · DYN | Green pens, tidy abandonment; T3 reveals the mid-sentence final note |
| Rail ladder | T1 · operate | Vertical stack access; creaks on a fixed note |

**State changes:** the Rundown's story corner claims these aisles at night from T3; the stacks the player arranged by day are the corridor walls by night.

## 7. CLIMATE ROOM (CLM)

| Item | Interact | Notes |
|---|---|---|
| Reel racks | T1 · take | Nightly retrieval objectives (the errand that bait the T3 chase) |
| Hygrometer + thermograph | T1 · inspect | Drum recorder; one night's trace shows a spike no thermostat explains |
| The degausser | T1 · inspect; T4 · operate | Burns dailies (strike removal) and, on the Destroy path, the archive; humming coil, felt-lined throat |
| Bake supplies | T1 · use | Feeds the oven workflow at the bench |
| Silica bins | T1 · inspect | Flavor; one bin holds a single small mitten, desiccated |

## 8. BENCH ROOM (BEN) · the star

| Item | Interact | Notes |
|---|---|---|
| Tape transport + capstans | T1 · operate | Capture runs forced real time |
| Bake oven | T1 · operate | Timed thermal holds; Destroy-path tool from T4 |
| Splice block, blades, leader | T1 · operate | Precision surgery; results burn in |
| TBC unit | T1 · operate | The photosensitivity device, diegetic |
| Waveform + vector scopes | T1 · inspect | The zero-loss anomaly is read here |
| Audio bench + spectrogram | T2 · operate | Asset 1 extraction; the deep-dig instrument; frequency assembly T2 to T4 |
| Jog/shuttle wheel | T1 · operate | Frame stepping; the séance verb from T4 |
| Monitor bank | T1 · inspect | Densest mediation in the compound; the room's safety is architectural |
| Accession ledger | T1 · commit/sign | Journal, conduct record, save; GEN stamps; the T5 decision point lives on this desk |
| Bench notepad | T4 · write | Séance questions; five canonical |
| Asset shelf | DYN · inspect | Collected Sign-Off assets rack visibly: verse transcription, ID cart, script, card |
| Craik's finale script | T3 · inspect (after retrieval) | Readable prop; the struck-through last line and the margin order |
| Glove box + lamp | T1 · use | Ritual props; the gloves are the player's face |

**State changes:** sanctuary for capture sessions throughout; T5 hosts the ledger's three-entry decision with Merle in the doorway.

## 9. FIRE CORRIDOR (FIRE)

| Item | Interact | Notes |
|---|---|---|
| Sealed door, library side | T4 · operate | Unsealed by the club for the anniversary |
| Char under plastic sheeting | T4 · inspect | The 1977 wound, preserved like relic; sheeting breathes with drafts |
| Melted fixtures, scorched frames | T4 · inspect | One frame's photo survived: the 1974 live audience, front row circled in someone's hand |
| The elbow | T4 N · EVT | The single direct-sight glimpse, under two seconds, once ever |

## 10. CONTROL CORRIDOR (CTL)

| Item | Interact | Notes |
|---|---|---|
| Wall monitors | T2 · inspect · DYN | Mediated-corridor endpoints; individually killable by the Rundown from T3; dead sets stay dead until re-patched |
| Corkboard memos | T2 · inspect | Props-packet paper: compliance notes, screening etiquette |
| Clock repeater | T2 · read | Break-window timing without entering MC |
| Cable trays | T1 · inspect | Overhead routing legibility; teaches the coverage-map mental model |

## 11. MASTER CONTROL (MC)

| Item | Interact | Notes |
|---|---|---|
| The switcher | T2 · inspect; T5 · operate | Muscle-memory target; face-button mapping mirrors the panel |
| Monitor wall | T2 · inspect | Program/preview logic taught by labels |
| Cart racks | T3 · take | STATION ID CART (Asset 3) punched and verified here |
| Uplink panel | T5 · operate (Authenticate route) | The premiere's exit to the world; ending 2's console |
| Glass window to Studio A | T2 · inspect | The mediation lesson: through the glass is direct sight, beside it the monitors are not |
| S2 log station | T2 · sign | Save |
| ON AIR master | never · inspect only | Grammar owns it; the one switch the player may never throw |
| Operator manuals | T2 · inspect | Period paper; one margin note in green: "It watches the preview bus too" |

## 12. PATCHBAY AND BREAKER ROOM (PB)

| Item | Interact | Notes |
|---|---|---|
| Patch field + cords | T2 · operate | Corridor building; the T5 broadcast chain; where the Dead Air re-route is committed |
| Breaker panel | T2 · operate | Trips, resets, budget management; the kitchen circuit COND (ASK) |
| Amperage meter | T2 · read | The budget, analog |
| The final breaker | T5 · EVT | Vess's hand; the credited-variant hesitation window |
| Spare fuse drawer | T2 · take | Finite; a soft resource |
| Cable loom wall | T1 · inspect | The building's nervous system, labeled in three eras of handwriting |

## 13. STUDIO A (STA) · the rebuilt Gladhouse

| Item | Interact | Notes |
|---|---|---|
| The set: carpet, cubby wall, painted house | T4 · inspect | Rebuilt to the centimeter from tape measurement; standing on it is standing inside the show |
| The little door in the painted house | T5 · operate | Cue 5: close the house, on camera, by hand |
| Chum's mark | T4 · inspect | A taped X the club refreshes; nobody says who for |
| Camera pedestals 1 to 3 | T4 · operate | Frame safety anchors; camera one hosts the line |
| Teleprompter | T5 · read | Craik's finale script loaded; a dead man's typing at reading speed |
| The casting sheet | T4 · inspect · DYN | Posted on the wall; lines fill per capture from T2 (players first see accumulated damage on entry); the club dusts it |
| Studio clock + ON AIR sign | T4 · read | The break-window masters |
| Slate/clapper | T4 · inspect | Retake iconography made physical; scene and take numbers match the player's record |
| Boom mic + stands | T4 · inspect | Windscreens worn to the foam |
| Audience gallery | T5 · DYN | Chairs arrive with the lockdown; the club fills them for the premiere |
| The Floor Manager's mark | T4 · inspect | A worn spot on the floor paint, decades deep |

**State changes:** dark museum T4 by day; the Rundown's song claims it at night; T5 it is live television, the safest and most contested floor in the game.

## 14. CATWALKS (CAT)

| Item | Interact | Notes |
|---|---|---|
| Grid + lighting instruments | T3 · traverse | The above-the-format route; grating noise is the toll |
| Ladders | T3 · operate | Exposure points at both ends |
| Sandbags, gel frames | T3 · inspect | Counterweight craft; one gel frame holds amber the exact shade of the cue signs |
| The hung spare Chum | COND · inspect | Coverage Director staging target only; it is always explainable, and it is never twice in the same place |

## 15. GREEN ROOM (GRN)

| Item | Interact | Notes |
|---|---|---|
| S3 log station | T4 · sign | Save |
| Makeup mirror, bulb-lit | T4 · inspect | Obeys the reflection budget; two bulbs out, always the same two |
| Costume rack | T4 · inspect · DYN | Club garments in show palette accumulate here as drift completes |
| Call sheet, framed | T4 · inspect | The 1977 finale's call sheet; every name checked in, none checked out |
| Couch + kettle | T4 · use | Harriet's deepest holding-pattern freeze plays here |

## 16. SCENE DOCK (DOCK) · the contract room

| Item | Interact | Notes |
|---|---|---|
| Spare Chum rows on armatures | T4 · inspect | Generations in order, fur graying by year; the era catalog physicalized |
| The warm one | T4 · COND · touch | Found by hand mid-inventory; the game does nothing further, ever |
| Props crates | T4 · search | THE SIGN-OFF CARD (Asset 2) surfaces here |
| Inventory clipboard | T4 · operate | The task's diegetic UI |
| Set flats + paint shelf | T4 · inspect | Spare painted-house parts; one flat is a window with the curtain painted mid-swing |
| Rolling door | never | Sealed; daylight in the seam |

**State changes:** none, ever, by contract. The room's purity is the design.

## 17. TRANSMITTER HALL (TH)

| Item | Interact | Notes |
|---|---|---|
| Transmitter cabinets | T3 · inspect | The hum floor; heat shimmer in craft materials (warped varnish, not haze) |
| High-voltage cage | T3 · inspect | Placarded; never a hazard to life, per the one-source rule |
| Tool wall | T4 · take | BOLT CUTTERS and the DRILL, the FORCE instruments; taking either logs itself |
| Storage cage: Craik's boxes | T3 · take | Finale script (Asset 4), cue-shorthand notebooks, and beneath, the childhood radio scripts (Dead Air item) |
| S4 log station (threshold) | T3 · sign · EVT | Hosts the singular pre-signed page, dated tomorrow |
| Transformer catwalk | T3 · traverse | Loose notebook pages for the thorough; noisy |
| The dead room door | T3 · inspect; T4 · operate | Felt-faced, locked; the hum dies at its seam. PRESERVE: the key. FORCE: the drill, and the seal is never perfect again (hummed epilogue, the surviving copy) |

## 18. DEAD ROOM (DR)

| Item | Interact | Notes |
|---|---|---|
| Foam wedge walls | T4 · inspect | Silence so complete the player hears their own pulse; the audio mix's bravest cue |
| Radio rack | T4 · inspect; T5 · operate | The Dead Air instrument: re-patch in Phase 1, sign-off in Phase 3 |
| Patch panel | T5 · operate | The three-step re-route, left looking untouched |
| Music stand | T5 · use | Holds the childhood script beside the finale script |
| Craik's chair | T4 · inspect | Worn where a boy's heels would kick |
| The felt door | T4 · operate | Closing it from inside is stepping outside the format |

**State changes:** the one true sanctuary from discovery onward; the secret ending's chapel.

---

## GLOBAL AND DYNAMIC ITEMS (all rooms)

| Item | Interact | Notes |
|---|---|---|
| Transmitter log clipboards S1 to S5 | per station · sign | The save system; paper economy on Late Night; one page arrives pre-signed |
| Camera mounts + tally lamps | T2 · route/read | Coverage endpoints; tallies are shape-coded; kills persist until re-patched |
| Wall monitors | T2 · read · DYN | Mediation surfaces; the poisoned well may lie through exactly one, once |
| The impossible-tapes crate | T4 · EVT then BEN | Delivered at ENT, lives at the bench thereafter |
| Break-window clocks | T2 · read | Every zone carries a repeater or sightline to one |
| Member pins | T1 · inspect | Enamel everywhere, plastic once; the status system worn on cardigans |

---

## RENDER ORDER PROPOSAL (next step)

Plate the hero rooms first, in the crafted-world style, camera and lighting per room thesis: **1) BEN** (the star, warmest light, densest craft), **2) REC** (domesticity thesis, shrine wall legible), **3) STA** (the rebuilt set under work lights, casting sheet in shot), **4) DR** (foam geometry, one practical lamp), **5) DOCK** (the rows, no drama, that is the drama). Then the connective tissue: LIB, TH, MC/PB, KIT/DRM, FIRE, EXT.


------------------------------------------------------------------------------
DOCUMENT 40 · restoration-walkthrough-levels-endings.md
------------------------------------------------------------------------------

# RESTORATION: Walkthrough, Level Design, Scares, Saves, and Endings
## The Playable Architecture Document

**Version 1.0** | Companion to the plotline and design documents. Everything here assumes the systems defined in the design doc: the Bench, Frame Discipline, Broadcast Grammar, Call-and-Response, the Quiet Game, the Provenance suite, the Leland Frame-Séance, and the hidden Producer Track.

---

# PART I: ARCS

## Rita Ivori (systemic arc: detachment to authorship)
Tape 1: professional detachment, the work is just work. Tape 2: craft pride, the first flawless restore and the first applause. Tape 3: understanding, Craik's script reframes the job. Tape 4: complicity made explicit, she knows what her competence is for. Tape 5: authorship, she writes the ending, whichever one. Her arc is carried by the Producer Track tells and her reflection budget, never by voiced introspection.

## Merle Cottry (warmth to ceremony to verdict)
The casting-drift showcase. Tape 1: grandmother of the compound. Tape 2: presenter cadence emerging. Tape 3: her 1974 story deployed as recruitment. Tape 4: the scene that earns her, the comfort was real. Tape 5: high priestess of the premiere. Ending payoffs: Sign-Off leaves her freed and bereft in front of a television that is finally just a television; New Producer leaves her beaming in the front row of forever.

## Vess (the plastic pin)
Tape 1: eager, helpful, slightly too much. Tape 2: the Screening overreach, publicly not chosen. Tape 3: sourcing obsession, gone for days. Tape 4: his anchor scene, the rejected edit played once, in full, with the club watching in silence. Tape 5: the most dangerous saboteur in the finale, with one conduct hook: if Rita's accession log credited his provenance work truthfully by name across the game, he hesitates at the final breaker, and the hesitation is the window.

## Harriet (the holding pattern)
Background-behavior arc. Her mid-motion freezes during break windows lengthen each act. In the Sign-Off ending, when the station goes dark, she resumes, finishes raising the teacup, and drinks. The game never explains how long she was holding.

## The Floor Manager (the constant)
No arc, which is the point. They count things in and out for five acts. After the sign-off completes, they remove the headphones, and the game ends before showing anything further.

## Leland (the frame thread)
Tape 3: notes end mid-sentence, one frame anomaly foreshadowed. Tape 4: found in frame, séance opens, the wear economy begins. Tape 5: if his integrity holds, he closes the show; if not, his last legible frame is an apology.

## Ansel Craik (posthumous arc)
Delivered entirely through materials in reverse order of composition: the finale script first (his ending), the notebooks second (his understanding), the childhood radio scripts last (his beginning). The player meets his death, then his fight, then the boy, which makes the buried stratum an act of mourning.

---

# PART II: MAP DESIGN

## The Compound: WGLD Transmitter Site

A hilltop studio-transmitter co-location, common for small UHF stations: the studio wing was on site, which is why the 1977 fire could take the masters and the set in one night. The club bought the decommissioned compound at auction and installed domesticity in one wing and devotion in another.

## Zone Schematic

```
                          [Tower base / Guy-wire field]
                                      |
        [TRANSMITTER HALL] ---- [DEAD ROOM (anechoic)]
                |
        [MASTER CONTROL] ---- [Patchbay / Breaker Room]
                |                        |
        [Control Corridor] ------ [STUDIO A: the rebuilt
                |                  Gladhouse set + catwalks]
                |                        |
        [TAPE LIBRARY + BENCH]     [SCENE DOCK]
                |                        |
        [Fire Corridor (sealed until Tape 4)]
                |
        [REC ROOM (hub)] -- [Kitchen] -- [Dorms / Rita's room]
                |
        [Entry / Front of house]
```

## Zone Design Notes

**Front of house and living quarters (hub).** Warmth engineered on purpose: lamps, casserole whiteboard, the shrine wall of clippings and pins. The rec room is the social heart, the screening venue, and the act-climax stage. Its safety is real for three acts, which is what makes its Tape 5 conversion into the premiere gallery land.

**Tape library and bench.** Rita's kingdom. Compactus rolling shelves fill the stacks: crank-driven moving walls that create and destroy corridors, the game's best repeatable stealth geometry and the site of the Tape 3 chase. Climate room off the back, bench room adjacent with the game's densest monitor coverage, meaning the bench room is the most mediated, safest-feeling space in the compound, on purpose.

**Control level.** Master control (the station ID carts, the switcher), the patchbay and breaker room (the power-budget organ). Long glass sightline from master control down into Studio A, the classic broadcast window, which doubles as the game's biggest mediation lesson: through that glass is direct sight; through the monitor bank beside it is not.

**Studio A.** The rebuilt Gladhouse set, the club's devotional reconstruction, accurate to the centimeter because they measured tapes frame by frame. Standing on the set is standing inside the show. Catwalks above with lighting grid: verticality, cable-tray traversal, and the only place the Understudy never goes, because there is no such thing as above the frame.

**Scene dock.** Set storage: flats, props, and the spare Chum inventory, rows of retired puppet bodies on armatures. One of them is warm. The dock is dread architecture, not a scare venue, and the game refuses to spring anything here, which is why players will dread it most.

**Fire corridor.** The scar. Sealed until Tape 4, char preserved under the club's plastic sheeting like a wound they could not bear to heal or remove. Site of the game's single scripted direct-sight glimpse.

**Transmitter hall.** Cathedral of RF: high voltage, transformer hum, warning signage, heat. The hum is a designed audio floor that masks footsteps in both directions, making the hall the game's fair-but-frightening traversal space.

**Dead room.** The anechoic chamber behind the hall, walls of foam wedges, silence so complete players hear their own pulse. Design truth: nothing can broadcast here, so the Understudy cannot perform here, making it the one true safe room in the game, discovered late, and the most unsettling room to occupy. The secret ending lives here, beside Craik's boxes and a radio that still works.

**Exterior.** Tower base and guy-wire field, used once at night in Tape 4, under the red beacon's slow pulse. The beacon blink is a rhythm players can time movement to, a gift for those who notice.

## Gating by Tape (unlock cadence)

Tape 1: front of house, living quarters, library, bench. Tape 2: control level, patchbay, first camera routing. Tape 3: transmitter hall, dead room found (not yet understood). Tape 4: studio wing, scene dock, fire corridor unsealed, exterior night. Tape 5: full compound, reconfigured for the premiere, all prior safety assumptions renegotiated.

---

# PART III: LEVEL DESIGN PRINCIPLES

1. **Hub-and-spoke with decaying hub safety.** The rec room is genuinely safe for three acts. Safety is spent, not faked: when it converts in Tape 5, the player's loss is real because the comfort was.

2. **Sightlines are the level design.** Every space is authored twice: once for direct sight (where can it see you, where can you avoid seeing it) and once for mediation (where do monitors, viewfinders, and the control-room glass create protected observation). Corridor kinks, monitor placement, and camera mounts are the geometry of survival.

3. **The compactus principle.** Player-operated architecture (rolling stacks, the patchbay's camera corridors, breaker states) means the player configures their own level, and misconfiguration is authored fear rather than unfair fear.

4. **Break windows are the pacing skeleton.** The studio clock and ON AIR sign create rhythmic safe intervals per zone, and level layouts are tuned so that traversal legs fit inside a window when planned and do not when panicked.

5. **One space above the format.** The catwalks exist so mastery players can route over danger at cost (noise, exposure at ladders), preserving the fear-frustration balance for high-skill play.

6. **Nothing springs in the dock.** Some rooms earn their dread by never cashing it. The scene dock is contractually scare-free, and the contract is what makes players' skin crawl there for nine hours.

---

# PART IV: SCARE DESIGN (Revision 2: armed)

## The Rules

- **Twelve scripted set-piece scares** across the game, plus **systemic scares, uncapped**, generated by the Rundown (Part V-B) and by player failure, plus **the capture scare**, the game's signature jump scare: Chum's face arriving at lens distance, button eyes filling frame. The capture scare scales with player performance, FNAF's law: the punishment is the jump scare, so the game frightens exactly as often as you fail it, on top of the authored set pieces.
- **Every scripted scare has a readable trigger.** No random stingers. Systemic scares carry their own fair tells (segment audio placing the hunter, camera static rising before an overload, the seek announcement). Voltage is raised; randomness is not.
- **Scripted set pieces carry two to three blockings**, selected against the player's behavioral profile by the Coverage Director (design doc, Part IV-B). Same trigger discipline, different staging per run; the compactus chase a camera-checker gets is not the one a sprinter gets.
- **Tape 1 is capture-free but not toothless.** It ends with a true startle inside the tape itself (below). Lethal danger begins Tape 2, Night 4. Free-roam hunting begins Tape 3.
- **One direct-sight glimpse, ever.** Scripted, Tape 4, fire corridor, under two seconds, undecidable.
- **Silence before scripted impact.** The authored 1.5 to 3 second void precedes every set-piece startle, honored every time. The Rundown's systemic scares use their own tells instead, so the two scare families stay legible.
- **The comfort is never the trap.** No scare is ever delivered through Merle's warmth, the kitchen, or an act of kindness.
- **The dock contract stands as the single restraint room.** One room in the game never springs; the warm Chum is found there and nothing follows. Every other room in the compound is armed.

## Scare Inventory by Tape (taxonomy tagged)

**Tape 1 (one startle, in-tape).** The corridor-monitor obedience moment (uncanny). Harriet's first freeze (uncanny/social). The rec room 4:3 static (wrongness). The act-climax startle: during the Tape 1 capture, mid-episode, Chum stops the Quiet Game, walks toward the studio camera until his face fills the frame, holds one beat too long, then a single-frame lunge as the tape cuts (startle 1, delivered from inside the footage; the tape can reach you before the building can).

**Tape 2 (two startles, first blood).** The Screening unison and the line to our new friend in the back (social dread peak). Startle 2: the breaker trips mid-route, the corridor monitor dies, and in the dead phosphor something crosses the reflection. Startle 3, and the game's first lethal sequence: the blackout pursuit, REC to CTL to PB in the dark, unmediated, it audibly performing behind her; first possible capture of the game, casting sheet live from here.

**Tape 3 (three startles, the hunt begins).** The fire tape capture (forced-watch dread centerpiece, no sting). The pre-signed log page (quiet horror). Startle 4: the compactus chase opening, shelves cranked from the far end. Startle 5: the first you're-on, speakers waking after fifty years. Startle 6: the first Rundown camera-kill witnessed live, its face rising into a corridor feed an instant before the overload whites the screen.

**Tape 4 (three startles).** Leland recognized in frame (the held-breath scare). The warm Chum (dock contract honored). The direct-sight glimpse (scripted). Startle 7: the séance's first answer, the legal pad changing between two frames just stepped across. Startle 8: an unscripted seek called in the studio wing, the first Quiet Game with no warning. Startle 9: the lockdown, every monitor switching to the same channel at once.

**Tape 5 (three startles, then pressure).** Startle 10: the bell, once, three feet behind camera position. Startle 11: the studio plunge, tallies dying in sequence toward her. Startle 12: the club's hands, the first time human beings physically hold Rita off camera as it walks over (the delivery scare). After these, the finale runs on performance pressure and the live casting sheet, because by then the player is defending an ending on their last strikes.

---

# PART V: SAVE SYSTEM (Revision 2: guarding real loss)

## The Instruments

**Transmitter log stations (manual saves).** Clipboard stations at fixed points (S1 library landing, S2 master control, S3 green room, S4 transmitter hall entry, S5 rec room). Signing the log is saving, in Rita's hand, timestamped in-fiction.

**The paper economy (Late Night).** Each station's clipboard holds a limited number of blank lines per tape (default three, tunable). Saving is spending paper. Matinee mode keeps unlimited lines. The ink-ribbon lineage, in FCC stationery.

**The accession ledger (bench saves and chapter checkpoints).** Completing and logging a bench session writes a full save and marks act progress. The ledger remains journal, conduct record, and save file at once.

**Autosave policy.** Act transitions always. Matinee adds zone-transition autosaves. Late Night keeps autosaves to act boundaries only, so the walk to a log station is always a decision with the casting sheet in mind.

## What Saves Guard

Final capture (Part V-B) reverts the run to the last signed log. Everything unsaved dies with the take: routing changes, gathered items, séance answers, ledger entries. The save system exists because the sheet can fill.

## What Persists (the burn-in rule)

Physical acts burn in at the playthrough level and survive both retakes and reloads: tape wear from scrubbing Leland's reel, splice surgery, and dailies canisters already created. Reload protects Rita's position and progress, never the tapes. Matinee halves wear rates; nothing removes the rule.

## The Save Scare

Unchanged and singular: Tape 3, a log page already signed in her handwriting, dated tomorrow. Diegetic content, not interface deception. No save is ever actually lost, corrupted, or falsified by the interface; that trust is the currency ending 2's post-credits spends.

---

# PART V-B: THREAT AND GAME OVER ARCHITECTURE (Revision 2: armed)

## The One-Source Rule (kept, sharpened)
Only the Understudy collects. The building never kills, and the club never harms, **but the club can deliver**: from the lockdown onward they can restrain Rita and hold her off camera while it approaches. Humans become lethal by delivery, never by hand, which keeps the fiction pure and makes Tape 5's sabotage genuinely dangerous.

## Fail Conditions (exhaustive)
1. **Contact while unmediated:** it reaches Rita with no live frame between them.
2. **Held direct sight:** direct gaze past roughly one second frees it; glances survive; Avert exists so panic has a verb. Freeing it starts pursuit.
3. **Quiet Game failure:** movement or sound during a seek, scripted or Rundown-called.
4. **Signal violation:** moving after the you're-on hand drop marks Rita as performance.
5. **Binding lapse (Tape 5):** a missed cue, too long off frame, or completed club interference collapses the finale's protection; seconds to regain frame.
6. **Delivery:** held off camera by the club as it arrives.

**Never fail conditions:** dialogue choices (interest, not death), bench mistakes (tapes, not life), power overdraw alone (protection, not health).

## The Rundown (the free-roam hunter, Tape 3 onward)
At night the Understudy performs the show's segment rundown through the compound: the craft segment in the workshop spaces, the song in the studio, the story corner in the library. **The audio tells you which segment, therefore where it is**; segment order shuffles nightly within grammar rules, so the schedule is learnable but never memorizable. It hunts the infrastructure as well as the woman: **a camera it stares into overloads and dies**, eroding mediated corridors across a night and forcing live re-routing at the patchbay. It can call an unscripted Quiet Game seek. Its aggression, patrol density, and camera-kill rate escalate per tape, and in Tape 5 the rundown is everywhere because the whole compound is the show.

## What a Capture Is: The Take (kept)
The capture scare (Chum at lens distance), then the image goes to tape: bars, head-switch noise, playback of Rita's final seconds from an angle no camera occupied. The replay is the tutorial. Rewind squeal. Slate: SCENE n, TAKE k. The Floor Manager's count. Fade up at the slate point. From the top means the scene, never the night.

## The Casting Sheet (the cap)
Posted on the studio wall: the cast list of a final episode. Some lines typed decades ago (the three Playmates), one typed recently (LELAND), and blank lines ending in AND INTRODUCING ______. **Every capture types RITA IVORI onto a blank line.** Defaults, tunable: four survivable captures on Late Night, seven on Matinee, zero in One Take mode. The sheet is a physical object; the player can walk to the wall and read exactly how close the end is, and the club dusts it.

## Burn Your Dailies (strike recovery)
After any capture, a new film canister appears in the library stacks, labeled with the scene and take. **Degaussing it fades Rita's name from that casting line.** Every death therefore generates a dangerous optional errand: retrieve the footage of your own death, at night, under the Rundown, or live with the strike. And the dailies have a second life: **unburned canisters are the Coverage Director's scouting film** (design doc, Part IV-B), so burning them also resets its read on your habits. Deaths produce gameplay; the archivist survives by destroying footage, the job inverted twice over.

## What Each Capture Takes
A casting line (recoverable, above). One personal item from Rita's room, permanently: the watch, the pen, the photograph, the lighter, the compact, the keys, the loupe last. Taken items reappear later as props inside restored episodes, losses become lore, and the community will catalog which items have crossed over. Plus the small Producer Track drip: footage is interest. Takes alone still cannot reach the audition threshold, and deaths never lock any ending.

## Final Capture: The Rewind That Does Not Stop
When the sheet is full, the next capture is final. The rewind blows past the slate, past footage of Rita's own arrival at the compound, and what plays next is next week's episode: Rita, on the set, in palette, waving. Sign-off card. The binder opens itself to the last signed log page: continue from log. True game over; everything unsaved is gone. Every capture in the game, the player watches the rewind praying it stops, because the difference between the two rewinds is the sharpest fear in the system.

## Where a Capture Cannot Happen
Tape 1 only, plus the standing sanctuaries: the bench during capture sessions, the rec room until the lockdown, the dead room always, the catwalks, and any moment on a live camera it must respect. The negative space is taught by experience, never listed in a menu.

## Modes
Late Night: four-line sheet, paper economy on, full Rundown aggression. Matinee: seven lines, unlimited paper, halved wear, longer tells, identical rules. One Take: any capture is final; for the brave and the broadcast.

## Design Defense
Every capture remains the payoff of a readable state, and the replay proves it in-fiction. But now the payback is real: strikes toward a visible cap, possessions crossing into the footage, a recovery errand that must be dared, and a save system that guards actual loss. The game still says from the top. The sheet on the wall says how many tops are left.

---

# PART VI: FULL GAMEPLAY WALKTHROUGH

## TAPE 1: "A Clean Signal"

**Day 1.** Arrival, Merle's tour (front of house, rec room, kitchen, dorms, library). Bench proving: the club hands Rita a sacrificial junk reel to demonstrate competence, the tutorial with a diegetic reason. Tape 1 goes into the bake with a timed hold that continues across the day, teaching the patience economy. Social beats seed the cast tells (Vess's plastic pin, Harriet's transitions, the shrine wall).

**Night 1.** Free movement in the living wing. The corridor-monitor discovery: through a hallway feed, something honors the frame edge like a performer hitting marks. Leland's first green-ink note found in the binder margins: safe as audience, do not be interesting, never accept a role. First log station introduced (library landing).

**Day 2.** The capture: Tape 1 digitizes in forced real time, The Quiet Game episode plays, and the anomaly surfaces: a third-generation dub with zero generational loss. First accession commitment: log the anomaly truthfully or write a cover explanation. Merle's reaction scene: joyful tears over footage she cannot have seen, insisting she remembers it.

**Night 2.** First Quiet Game, scripted and low-stakes, teaching stillness. Harriet's freeze, catchable in periphery.

**Act climax: the mini-screening.** Rec room, lights down, the RESPOND sign lights for the first time and nobody acknowledges it. One correct audience response required. Act out on applause.

*Systems unlocked:* full bench suite, avert, log stations, accession ledger, Quiet Game. *Lore layers:* main route inciting anomaly; deducible seeds (the dub physics, Merle's impossible memory); buried thread opens (Leland's marginalia). *Startles: one, delivered from inside the tape at the capture climax; the compound itself stays capture-free this act.*

## TAPE 2: "Airdates"

**Days.** Control level opens. Patchbay tutorial: route the first mediated corridor and learn the power budget at the breaker panel. The airdate project: cross-reference slates, station logs, and the club's own framed TV listings; the 141-produced versus 138-aired discrepancy and the three unaired dates sit in the materials for the player to assemble, never stated. Tape 2 capture: the color anomaly, and buried in its audio, findable by spectrogram, the closing song's missing verse (**Sign-Off asset 1 of 4**). The library's instructional film teaches real floor-manager hand signals, the threat vocabulary, in-fiction.

**Nights.** Grammar events begin gently: break windows observable on the studio clock, the Floor Manager glimpsed counting a corridor out.

**Act climax: the Screening.** The full call-and-response system under social pressure. Mid-episode, half the room answers Chum in perfect unison, then the new line addressed to our new friend in the back. Correct audience conduct navigates it; improvisation here is the first big Producer Track spike. Vess overreaches, answers too eagerly, and the room goes wrong around him for one held second while the club pretends nothing happened.

*The startles:* the tripped-breaker reflection cross, earned by overdraw, then the blackout pursuit: the dark traversal to PB becomes the game's first lethal sequence, it audibly performing behind her, first possible capture, casting sheet live from this night forward. *Lore layers:* deducible peak (the unaired three and the disappearance clippings on the shrine wall); buried (spectrogram practice, first frequency fragments).

## TAPE 3: "Sign-Off"

**Days.** Transmitter hall opens; the dead room is found but reads as a curiosity. Craik's materials recovered in reverse order of his life: **the finale script (asset 4)**, the notebooks in cue shorthand, and beneath everything, the childhood radio scripts. Master control yields the **station ID cart (asset 3)**. The capture centerpiece: the fire tape, the studio emptying and burning while Chum performs to no one and the camera pans with no operator; forced watch, no sting, the game's thesis on restraint. The endgame crystallizes in Craik's own hand: the show never ended, and an unfinished ending is a cliffhanger.

**Nights.** The first full stalking sequence: a you're-on signal, the studio speakers waking, and the compactus chase through the library, shelves cranked from the far end, escape by building a mediated corridor at the patchbay under pressure. The pre-signed log page is found this act, dated tomorrow.

*Startles: three, listed in Part IV.* *Systems armed:* the Rundown activates this act; nights now carry a free-roaming hunter whose segment audio is the map, and whose stare kills cameras. *Buried thread:* Leland's notes end mid-sentence; one frame anomaly in Tape 3's background rewards frame-steppers with a foreshadow.

## TAPE 4: "Provenance"

**Days.** Studio wing, scene dock, and fire corridor open. The rebuilt Gladhouse set: awe and dread in one room, measured devotion accurate to the centimeter. The impossible tapes arrive (post-fire dates, changed stitching, a mirror-flipped Chum for the community's catalog). **Leland is recognized in frame**, and the Frame-Séance opens: jog-wheel stepping, questions on the bench notepad, answers across frames, and the wear economy that makes every question cost part of him. The **sign-off card (asset 2)** is recovered in the scene dock, during the inventory task that also finds the warm Chum. Vess's anchor scene: his rejected edit, played once, in full, the club silent. Merle's 1974 scene: Chum found her when she was actually lost, and the game plays her gratitude completely straight.

**Nights.** Exterior traversal under the beacon pulse. The scripted direct-sight glimpse, fire corridor, under two seconds. The act ends in lockdown: every monitor in the compound switches to the same channel at once, the club locks the doors for the anniversary, and the hub converts, chairs in rows, the rec room becoming a gallery.

*Startles: two.* *Buried thread:* the dead room key surfaces in Craik's boxes; frequency reconstruction becomes completable; the childhood script's purpose becomes legible to diggers.

## TAPE 5: "The Premiere"

**Phase 1, Prep (free roam under soft pursuit).** The compound reconfigured, the club ceremonial, the Understudy cooperative and therefore everywhere, walking the halls like talent before a show. Objectives: verify the four assets, route the broadcast power chain at the patchbay (the routing mastery exam), and, for those equipped, quietly re-patch the chain through the dead room for the Dead Air divert. The decision point sits here: the ledger open on the bench, three entries possible in Rita's hand: Authenticate, Destroy, or Perform.

**Phase 2, Live.** The finale as playable live television. Cue execution from Craik's script, switcher operation on muscle memory, staying in frame as the safety condition, while the club sabotages: breakers cut, corridors blocked, cameras unplugged, forcing live re-routing between cues. Vess is the most dangerous saboteur, unless the ledger named his work truthfully all game, in which case he hesitates at the final breaker and the hesitation is the window. Midpoint: the bell rings once.

**Phase 3, The Line.** The closing scene reached, the fourth wall broken on purpose: on camera, into the lens, the truth told to everyone at home, that no one is watching anymore. Branch resolution per Part VII.

*Startles: two, then pressure only.*

---

# PART VII: ENDINGS AND EXACT CONDITIONS

## Tracked Variables

| Variable | Range | Raised or set by |
|---|---|---|
| Producer Track (PT) | 0 to 100, hidden | Restoration grades, accepted roles, interesting improvisation |
| Sign-Off Assets | 0 to 4 | Missing verse (T2 spectrogram), sign-off card (T4 scene dock), station ID cart (T3 master control), finale script (T3 dead room boxes) |
| Leland Integrity (LI) | 100% down | Reduced by every séance scrubbing pass; burn-in rule applies; thread-complete flag requires his final question answered |
| Conduct Ledger | truth and cover entries; Vess-credit flag | Player-written accession entries across all acts |
| Dead Air Set | 3 items | Dead room key (T4), reconstructed frequency (spectrogram chain T2 to T4), Craik's childhood script (T3) |

## The Four Endings

**1. SIGN-OFF.** *Conditions:* choose Perform at the decision point, hold all four assets, and complete Phase 2's cue sequence and Phase 3's line. *Variant A, Leland closes:* thread-complete flag plus LI at 60% or higher; Leland, already cast, says goodnight from inside the frame and goes wherever ended shows go. *Variant B, Rita closes:* otherwise, someone must close the house from inside, Rita accepts the one last role, and the epilogue is hers from within still frames. Both variants: static, sign-off card, Channel 58 dark for the first time in fifty years, Harriet finishing her tea, the Floor Manager removing the headphones.

**2. THE NEW PRODUCER.** *Conditions:* choose Authenticate at the decision point, or attempt Perform with fewer than four assets while PT is 70 or higher (the show accepts the incomplete finale as an audition instead). The premiere airs, the migration succeeds, 4K Chum addresses the lens: say it with me. Post-credits: the game's single interface lie, spent here at maximum voltage.

**3. THE BURN.** *Conditions:* choose Destroy at the decision point (available from Tape 4 onward via the degausser and the bake oven). Playable destruction sequence, then the failure the fire already taught: offsite copies exist, format outlives instances, and the epilogue is the club beginning again with a new conservator's name in the ledger. The lore-lesson ending: it exists to prove why the sign-off is the only exit.

**4. DEAD AIR** (secret, the buried-stratum ending). *Conditions:* all Sign-Off conditions, plus the complete Dead Air Set, plus the Phase 1 dead-room re-patch. During Phase 3, the divert option appears: route the completed sign-off through the dead room's radio chain instead of the digital premiere, performing the ending in the original medium, reaching everyone at home across every format at once. *The price, paid on screen:* the broadcast-erase loop blanks every copy everywhere, and the archivist must sit at her own bench and watch the archive die. The cleanest death the thing can be given costs the thing she came to save. Merle inherits nothing. Lost media becomes actually lost. The ledger's last line, in Rita's hand: signed off.

## Ending Routing Summary

Decision point (bench ledger, Tape 5 Phase 1): **Authenticate** routes to 2. **Destroy** routes to 3. **Perform** routes to 1, with assets and LI selecting the variant, unless the Dead Air Set and re-patch are complete and the divert is taken in Phase 3, which routes to 4. PT never forces an ending by itself; it flavors tells throughout and provides the audition clause in ending 2, keeping conduct, not a meter, in charge of fate.

---

# CLOSING: NAMED GAPS

1. The seven-startle budget is a marketing risk in a clip-driven genre (Dread Ledger 8.1); the mitigation is that dread clips (the bell, the pan with no operator, the unison) are engineered to travel as hard as stings.
2. The burn-in rule will generate forum anger the first week; it is correct anyway, and Matinee's halved wear is the sanctioned relief valve.
3. Phase 2's sabotage AI is the hardest tuning problem in the game: the club must threaten the broadcast, never soft-lock it, and needs a fail-forward retake structure ("From the top") tuned so retries escalate tension instead of deflating it.
4. The decision point's three-entry ledger must be unmistakable as a point of no return without a modal dialog; current answer is Merle standing in the doorway, watching Rita's pen, saying nothing.


------------------------------------------------------------------------------
DOCUMENT 41 · restoration-accessibility-conformance-pass.md
------------------------------------------------------------------------------

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


------------------------------------------------------------------------------
DOCUMENT 42 · restoration-arg-plan.md
------------------------------------------------------------------------------

# RESTORATION · ARG ASSET PLAN v1
Doctrine first: the ARG keeps the game's laws in public. Everything frightening arrives mediated. The glimpse and Leland's face appear nowhere. One startle exists in the whole campaign and it is the trailer's, already spent. Every puzzle is solvable inside two weeks by a community of one, needs no purchases, ships with transcripts and alt text, and when the campaign ends we publish the full solution ledger, because a game about restoration does not leave its own archive scattered. The frame is honest: these are in-fiction artifacts, clearly authored, never presented as real events.

## PHASE 1 · THE STATION EXISTS (announce)
A1 WGLD CHANNEL 58 archive microsite: a station history page and scanned program schedules, 1971 to 1977, typeset per the props packet stocks. The hook is buried in plain data: slate numbers with clustered skips. The community rediscovers Vess's insight themselves (clusters, not decay), and the site never confirms it. Effort: static site, two weekends. Tier A viable.
A2 The 1974 Courier clipping (props packet D04) seeded to two retro-TV newsletters as a found scan. No commentary. The gray flannel detail does its own work later.

## PHASE 2 · THE RECOVERED REEL (demo launch)
A3 An audio drop: the closing song, G2 print, posted as a recovered quarter-inch transfer. The word swap ("here" for "home") is audible to careful ears; the missing verse's final line hides in the sidebands for anyone who runs a spectrogram, mirroring the in-game bench beat exactly. The demo ships the same week, so the tool the community just used is the tool the demo hands them.
A4 The training film's six hand signals as a set of silent looping clips. The seventh signal is withheld and tied to a public milestone (a wishlist count, stated plainly, no coyness): at the mark, Harriet's index card posts, verbatim from the props packet. The community is taught HOLD YOUR APPLAUSE before the game ever asks.

## PHASE 3 · THE ANNIVERSARY (pre-launch beat)
A5 On the fire's in-fiction anniversary, the microsite's schedule page gains one new row dated after 1977, then reverts within twenty-four hours. Screenshots become the artifact. This is the campaign's only reality-flicker and it obeys the format: a listing, mediated, never a face.
A6 Physical, small batch: 58 Club membership card mailers to twenty creators, with Merle's cobbler recipe card in her voice and a hand-signed line: "You came back. I told them you would." The recipe is real and good, because everything Merle makes is.

## RULES OF PLAY
No ciphers past hobbyist grade; the spectrogram is the ceiling. Nothing time-gated tighter than a weekend. No account walls. Accessibility parity on every asset. Community managers answer in the club's voice, never Chum's: Chum does not have an account, does not post, and is never quoted in first person online, for the same reason the bell is silent.

## BUDGET TIERS
Tier A (solo): A1, A3, A4 only; the microsite doubles as the press kit's lore page. Tier B adds A2, A5, A6 and a part-time community hand for launch month. Nothing in this plan requires Tier C.


------------------------------------------------------------------------------
DOCUMENT 43 · restoration-art-bible.md
------------------------------------------------------------------------------

# RESTORATION · ART BIBLE v1
Authority chain: the four Chum reference plates are ground truth; the design doc Part II owns Chum's base design, era table, and the nine-delta post-fire set (cited here, never duplicated); this bible owns everything else visual. Engine color values in v0.7 are the palette's provisional hexes and are listed here as canon until repainted.

## 1 · THE CRAFTED WORLD DOCTRINE
One law: everything in this world was made by hand, at one-to-one scale, by people who cared. Rooms are built sets. Humans are needle-felt and cloth figures over armature. Props are painted plywood, real brass, real glass. This is craft realism, not stylization: stitches read as stitches, fibers catch light as fibers, glue is where glue would be. The uncanny is never achieved by distorting the craft; it is achieved by the craft being too careful in places nobody should have cared about. If a surface looks digital, it is wrong. If it looks mass-produced, it is wrong. If it looks loved, it is right, and that includes the things that should frighten you.

## 2 · THE TWO-WORLDS CONTRAST LAW
The compound and the tape world share one material language. The contrast between them is delivered exclusively by lighting and by the artifact pipeline. Consequences: no separate art style for tape content; no grain, chroma error, or scanline may ever appear on compound surfaces (grain belongs to tape only); no tape image may ever appear clean except the anomaly slates, which are authored one at a time. Footage is always shot or rendered clean and degraded live in the shader ladder; artifacts are never baked into masters. Photosensitivity-safe mode must preserve the two-worlds read while suppressing bands, flicker, and crawl (engine parity already exists; art must not reintroduce risk via authored flashes).

## 3 · MATERIAL SYSTEM · SCAN FIRST
Fabricate a physical swatch library, then capture it: wools (Chum brown plus five compound wools), felts (dead-room gray, set greens), flannels including the school-gray that ties patch seven to the 1974 clipping, corduroy, aged brass, glass (amber eye stock), painted plywood in three wear states, mimeograph and newsprint papers. Photogrammetry or photometric stereo per swatch into tiling PBR sets with clean, worn, and loved wear states. The wool spike shader is the interim standard for all fiber surfaces; it retires per surface only when its scanned replacement passes the sodium test (Section 10). Nothing ships on a procedural fiber that a scan could carry.

## 4 · PALETTE SYSTEM
Compound neutrals: ash #6B6862, dust #7F7A70, slate #5C5C61, oat #756E66, fog #666B6B. Show palette (the Gladhouse's colors): MUSTARD #C9A33D, AVOCADO #6B7D3B, BURNT #B35A2B. Supporting canon: phosphor #D9EDC4 (UI, tags, title), paper #DED4B8, ledger green #596B52, warning red #C23A2E used only for slates, tallies, and the breaker.
THE DRIFT LAW: environments and wardrobe interpolate from neutrals toward the show palette on the coat-peg curve (day-driven, lockdown-boosted; the engine's CoatPegs drift function is the canonical curve). Set dressing drifts through replaced small props first (a mustard tea towel on Day 2), textiles second, wall tones never (walls hold neutral so the drift reads on things people chose).

## 5 · CASTING-DRIFT WARDROBE RULES (per character)
MERLE: begins already warm (mustard apron from Day 1) and never drifts, because she was carried in 1974 and has nothing left to drift toward; her constancy is the tell hiding in plain sight. HARRIET: drifts on the curve exactly, the control subject. VESS: resists longest; neutrals through Day 4, and his only show-palette object is the plastic pin he has always carried, which is the other tell; if he credits and is credited, he adds one avocado scarf for the premiere, chosen, not drifted. EXTRAS AND PEGS: lead the curve by half a day, so the background is always slightly ahead of the people you know. FLOOR MANAGER: absolute black-adjacent neutrals forever, outside the palette system entirely, the way he is outside everything. RITA: player wardrobe never drifts; her gloves are the whitest object in the game.

## 6 · CHARACTER BUILD SPECS
Humans: needle-felt heads over wire armature, cloth bodies, mitten hands with stitched finger definition reserved for principals (Merle, Vess, Harriet). Head-to-body one to five and a half. EYE HIERARCHY, a hard law: human figures wear glass beads or embroidered eyes only; buttons are reserved for Chum. A button on a human face is an event we never spend. CHUM: per design doc Part II in full; the Understudy's on-set live build is dimensionally identical to Chum plus four percent overall scale, an error the eye reports as distance being wrong rather than size being wrong. The post-fire build follows the nine-delta set exactly; fabricators receive the tell-table, not adjectives.

## 7 · HERO ROOMS (render order: BEN, REC, STA, DR, DOCK)
BENCH: the altar. Paper stock and ledger green dominate; one warm task lamp; the monitor is the room's only saturated light; the asset rack reads amber against dust.
REC ROOM: the heart. Warmest neutrals, the shrine's glass, chairs in their casual arrangement (the plate is shot pre-lockdown; a second plate in rows is the pair that sells the game).
STUDIO A: the stage. Tungsten wash on the set island, catwalk darkness above with one practical; the little door lit like a prop that knows it is one.
DEAD ROOM: flat, shadowless, felt-swallowed; the radio's dial is the only specular object; palette entirely fog and slate.
DOCK: rows two deep, years in order; cold north light through high glass; the units' wools graying left to right by era; the clipboard's paper the brightest value in frame.

## 8 · LIGHTING DOCTRINE
Day: overcast north key plus warm tungsten practicals; nothing pretty, everything kind. Night: sodium exterior spill at the windows (the wool verdict's test light), phosphor monitor glow as interior key, pools with honest falloff. The cascade: darkness is absence, never blue; restored circuits return light in the panel's order. Premiere: full tungsten stage wash, the one gorgeous image in the game, because the trap should be beautiful. Dead room: no key at all.

## 9 · CAMERA, POST, UI
In-world eye: 24 mm equivalent, mild breathing on focus, no depth-of-field cinematics outside authored scenes. Compound post: none; color is achieved in light and material. Tape post: owned entirely by the artifact ladder. UI art: the WGLD binder specimen is source of truth (phosphor CRT title, form stock, cue-sign faces); print props follow the props packet's stock specs.

## 10 · DELIVERABLES AND THE GATE
P0: swatch library fabricated and scanned; Chum base build contract (the puppet is also the trailer, per the build plan); BEN and REC dressing kits; the five hero plates. P1: STA, DR, DOCK kits; principal character builds, Merle first; drift prop sets per day. P2: extras, exterior, premiere dressing.
ACCEPTANCE, THE SODIUM TEST: every fiber material is judged as a physical sample photographed under a sodium lamp beside its render under the same light. If a blind viewer cannot reliably pick the render, it passes. This is verdict V1 from the playtest protocol, promoted to the material gate for the whole game.


------------------------------------------------------------------------------
DOCUMENT 44 · restoration-build-plan.md
------------------------------------------------------------------------------

# RESTORATION: THE BUILD PLAN
## From Master Document to Shipped Game

**Version 1.0** | Assumes the full canon stack: rubrics, concepts, plotline, design doc (with Part IV-B), walkthrough (Revision 2), routing doc, and the game master document. This plan turns those into a shippable product.

---

# PART I: ASSUMPTIONS AND THE THREE GATE-ZERO DECISIONS

## Scope Tiers (pick one; the plan flexes to it)

| Tier | Team model | Timeline | Budget band |
|---|---|---|---|
| **A: Solo-core** | One designer-director (you) plus fractional engineering support and contractors (audio, puppet, VO, ports) | 24 to 32 months | $60k to $180k cash out |
| **B: Small studio (baseline for this plan)** | 4 to 6 core (director/design, 2 engineers, environment artist, tech artist, producer-QA hybrid) plus the same contractor set | 18 to 20 months | $700k to $1.4M |
| **C: Funded** | 10 to 15, dedicated audio and animation in-house | 22 to 26 months | $2.5M to $4.5M |

All month numbers below are Tier B; Tier A multiplies content phases by roughly 1.5 and serializes them; Tier C compresses by parallelizing content waves, not systems.

## Gate 0 Decisions (week 1, before anything else)

**1. Engine.** Weighted criteria: media playback and frame-accurate scrubbing (the séance lives or dies here), render-target camera feeds at budget (Frame Discipline is dozens of live feeds), dynamic light control for the plunge and beacon work, team familiarity. Recommendation: Unreal 5 if hiring experienced 3D contractors (Lumen sells the compound, MediaFramework handles playback); Unity 6 if the core is programmer-designer hybrids (faster systems iteration, simpler video texture pipeline). Godot only at Tier A with a stylization tradeoff. Decide once, in writing, with the spike results from M0.

**2. Release model.** Boxed release with Tape 1 as the free demo, recommended. The trust arc (no-startle first act, armed escalation) is one arc; shipping Tape 1 alone as a paid chapter is marketing death, but shipping it free as a demo that ends on the in-tape lunge and the RESPOND sign is a conversion machine. The chaptered Poppy-cadence variant remains viable only as Tapes 1+2 bundled per drop; if chosen, add 3 months and a live-ops seat.

**3. The show footage.** The Gladhouse must exist as footage: episodes, the fire tape, the impossible tapes, four Chum era variants. Two paths: in-engine rendered "footage" with an artifact pass, or a real puppet shoot. **Recommendation, and it is the plan's one unsafe choice: build Chum for real.** One fabricated puppet (with variant dressings), a micro set or greenscreen, two to three weekend shoots against the master document's tape scripts. Authenticity is load-bearing (the plot's inciting anomaly is a physically impossible dub, which only reads if the physics are honest), the puppet doubles as the trailer, the merch prototype, and the photo-mode of the entire marketing campaign, and the cost (fabrication plus shoots, $25k to $60k) undercuts the tech-art time of faking it convincingly.

---

# PART II: PRODUCTION PHILOSOPHY

**The six sacred pillars (never descoped):** the four pillars from the design doc (craft is courtship, mediation is safety, format is law, the comfort is real), plus the one-lie rule and the earned-trigger scare discipline. Every cut proposal is tested against these first.

**Rubric-gated milestones.** This project owns two scoring instruments; the plan uses them as gates. Every written scene passes a Dark Ledger scored read before recording or implementation (floor law: nothing below 3 in load-bearing criteria ships to VO). Every milestone build gets a Dread Ledger pass with target bands: Vertical Slice at 3.7+ on Domains 1, 2, and 6; Alpha at 4.0 weighted; Ship gate at 4.2 weighted with at least two domain 5s argued in writing. The review is a scheduled ritual, calendar-blocked, evidence-cited per the instruments' own protocols.

**Fairness as CI.** The game's laws become automated invariants that run on every build (Part VI). If the Understudy ever harms on camera in a nightly test, the build is red. The fiction's rules are the test suite.

**The descope ladder (what dies first, in order):** mic input features → blocking C variants (ship A/B) → One Take mode (post-launch) → the NG+ nod (post-launch) → poltergeist prop staging density → exterior night sequence compression. **Never on the ladder:** any ending (all four ship or the game slips), the seventh signal, the dock contract, the bell, Merle's monologue, the burn-in rule.

---

# PART III: M0, PREPRODUCTION (Months 1 to 3)

## Workstream 1: Technical Risk Spikes (each 1 to 2 weeks, pass/fail criteria in writing)

1. **Tape-world pipeline.** Per-generation artifact simulation (tracking, dot crawl, chroma bleed, head-switch noise) as a controllable shader stack responding to player tool settings (TBC, tracking). Pass: one clip, four generation states, artifacts diegetic and tool-reactive, photosensitivity-safe mode verified.
2. **Frame Discipline rendering.** N live camera feeds as render targets with tally logic and the mediated-safety ruleset at 60fps on target hardware. Pass: 12 simultaneous feeds, one patchbay re-route, safety state provably correct in a test scene.
3. **The séance.** Frame-accurate jog/shuttle over video with a compositing layer (Leland moving between frames) and persistent wear state. Pass: step, jump-cue, wear write-through to save, reload persistence.
4. **Rundown AI v0.** Segment-based patrol with audio localization, camera-kill behavior, one unscripted seek. Pass: a bot survives a night using only audio cues; the AI never violates a grammar invariant in a 4-hour soak.
5. **Coverage Director v0.** Profile tracking (checker/sprinter/hider/averter) selecting between two blockings of one scare. Pass: deterministic profile from logged inputs; blocking selection explainable in the log.
6. **Power and patchbay sim.** Amperage budget, breaker trips, corridor liveness. Pass: the Night 4 sequence greyboxed end to end.
7. **Live-production finale loop.** Cue sequencing, switcher input mapping, sabotage events, retake checkpointing per cue. Pass: Phase 2 skeleton playable with placeholder everything.

## Workstream 2: Content Foundations
Greybox the full compound from the routing document (zones, stations, sightlines, the compactus, catwalks); art bible (compound naturalism vs tape-world spec, the show palette system, casting-drift wardrobe rules); audio bible (the Yamaoka-standard brief: hum floors, silence tells, segment themes, the bell's single sample); UI kit v0 (binder, ledger, cue signs, CG face licensing or commission).

## Workstream 3: The Show Production Setup
Puppet fabrication contract (Chum base plus 1971/1974/post-fire/4K dressing variants per the master doc tell-table); shoot planning against the master document's on-tape scripts (T1.5, T2.8, T3.4 fire tape, T4 impossibles, T5 live-composite plates); degradation pipeline design (shoot clean, degrade per generation in the tape-world shader, never bake artifacts into masters).

## Workstream 4: Casting and Writing Lock
Dark Ledger scored pass on every master-document scene (revision list from the floor); casting breakdowns out early, **Merle first and flagged as the project's hardest read** (warm-genuine, never warm-sinister; the ending-3 line reading is the audition scene); Chum's voice (live puppeteer-performer preferred over VO booth, for the finale's live scenes); Leland is text-only (no VO cost); the Floor Manager is a counting voice, one session.

## M0 Exit Criteria
All seven spikes passed or mitigated in writing; engine and release-model decisions signed; greybox walkable Tape 1 route; puppet contract signed; Merle shortlist of three.

---

# PART IV: THE MILESTONE PLAN (Tier B months)

## M1: Core Loop Playable (Months 4 to 6)
**Goal: the bench is a game.** Full restoration suite (bake, splice, capture with forced real time, audio bench and spectrogram, quality grading), the accession ledger with GEN field and conduct entries, log-station saves with the paper economy, burn-in persistence layer, Tape 1 content implemented rough with placeholder show footage, the response system with cue signs.
**Show production:** puppet shoot 1 (Tape 1 and Tape 2 episode material, the Quiet Game, the closing song).
**Exit:** a tester can play Tape 1 start to finish, ugly but true, and the T1.5 capture already produces dread with placeholder artifacts.

## M2: Vertical Slice (Months 7 to 9)
**Goal: prove both halves at shippable quality.** Tape 1 at final quality (art, audio, the shot show footage, the in-tape lunge) plus one Tape 3 night out of sequence: the compactus chase with Frame Discipline, power routing, the you're-on, and a real capture-to-take flow with the casting sheet.
**The VS answers the four flagged playtest questions early:** does forced real-time capture hold attention; does the casting sheet draw pilgrimages; does the take/retake flow read as threat; does the blooper-reel tell land as dread or demoralization.
**Gate:** Dread Ledger scored review, 3.7+ on Domains 1, 2, 6; Dark Ledger floor holds on all implemented text. Publisher/funding conversations, if any, happen off this build.
**Exit:** the slice terrifies a cold tester who owns none of our context.

## M3: Systems Complete (Months 10 to 13)
**Goal: every mechanic exists.** Rundown v1 full (patrols, camera-kills, unscripted seeks), Coverage Director with profile plus mood law (savoring mode), Grammar engine complete (windows, signals, formal-correctness protections), the séance full with the five-question thread and wear math, Burn Your Dailies loop, Approaches and Generations plumbing (GEN-tagged facts, the authored-gap table as data), power sim final.
**Content wave:** Tapes 2 and 3 implemented to alpha art; puppet shoot 2 (fire tape, era-variant pickups).
**Exit:** Tapes 1 through 3 playable in sequence; nightly invariant suite green for two consecutive weeks.

## M4: Content Complete Alpha (Months 14 to 16)
**Goal: the whole game exists.** Tapes 4 and 5 in (the set reveal, the dock, the glimpse, lockdown, all three finale phases with sabotage AI and the Vess variants), all four endings functional to script including Dead Air's divert and erase sequence, all twelve scares with A/B blockings (C per descope status), the solutions matrix implemented obstacle by obstacle, VO recorded and cut in, the interface lie built and access-controlled to ending 2's post-credits only.
**Gate:** Dread Ledger at 4.0 weighted; ending-thread bots run all four routes nightly.
**Exit:** anyone can play arrival to any ending without a developer in the room.

## M5: Beta and Tuning (Months 17 to 18)
**Goal: the numbers become feelings.** Tuning passes on every marked tunable (sheet lines, paper economy, wear rates, PT weights, grace windows, sabotage pressure) driven by cohort playtests (Matinee and Late Night cohorts separated); the tonal verification list (Merle's ending-3 read, the unison scene, the bell's mix level, savoring-mode pacing); accessibility certification pass (photosensitivity audit on every tape-world asset, caption completeness including directional captions, full remap, mic-free parity verified); localization if scoped; the buried-stratum assets finalized and verified minable (spectrogram content in the shipping audio files, the future-dated schedule frames, legal review on any real phone numbers); performance and platform cert prep.
**Gate:** Ship-gate Dread Ledger review at 4.2 weighted with the two argued 5s; the Peak Law memo written (what this game will be cited for in a jury room).

## M6: Ship (Months 19 to 20)
Cert, day-one patch discipline, launch. Post-launch backlog seeded from the descope ladder (One Take mode, blocking Cs, NG+ nod) plus community-response reserve for the ARG layer.

---

# PART V: TEAM AND EXTERNAL PLAN

**Core (Tier B):** Director/design (owner of canon and both ledgers), systems engineer (Rundown, Coverage Director, grammar, saves), gameplay/UI engineer (bench, séance, patchbay, binder), environment artist (the compound), tech artist (tape-world pipeline, Frame Discipline rendering, lighting), producer-QA hybrid (invariant suite ownership, playtest ops).
**Contract:** composer and sound designer engaged from M0 (audio is the genre's first pillar and cannot be a post-pass; the segment themes are level design), puppet fabricator and shoot crew, VO cast (Merle, Vess, Harriet, Chum performer, Floor Manager, Craik archival), 4K Chum groom specialist for ending 2's uncanny render, accessibility auditor, platform cert/porting house, key art.
**Tier A translation:** director absorbs design plus UI engineering with AI-assisted implementation; systems engineering is the fractional hire that cannot be skipped; everything else stays contract; content waves serialize.

---

# PART VI: TESTING AND VERIFICATION (the invariant suite)

The project's fairness laws run as automated tests on every build, nightly soaks, and pre-milestone certs. Red build blocks merge. The canonical invariants:

1. The Understudy never harms while on any live, respected camera.
2. It never enters the dock, the dead room, or the catwalks.
3. Monitor deception fires at most once per run, only via the Coverage Director's poisoned-well path, only with the static telegraph.
4. Every scripted startle is preceded by its 1.5 to 3 second silence window.
5. Every capture logs a readable trigger state (which fail condition, which system reads were available).
6. Grammar transitions occur only in valid windows; the Floor Manager's signal log matches world events.
7. Leland wear and all burn-in survive retake, reload, and crash recovery.
8. The casting sheet count, dailies canisters, and item-loss ledger reconcile after any sequence of captures and burns.
9. The four ending threads complete via scripted bots nightly, including the audition clause and the drilled-door hum variant.
10. The interface lie is unreachable outside ending 2's post-credit context, verified by attempted-access tests.

**Human verification cadence:** weekly cold-tester sessions from M2 (one person who has never seen the project, every week, forever); telemetry proxies for fear (avert frequency, save-station visits, casting-sheet approaches, headphone-removal moments self-reported); the standing question list from the docs tracked to answers with dates.

---

# PART VII: THE DOMAIN 8 WORKSTREAM (parallel, from M2)

Runs beside production, never ahead of canon. Trailer law: the capture scare is the trailer scare; never show the glimpse, never the bell, never the sheet filling. Demo equals Tape 1, free, ending on the lunge and the sign. Content-creator kit at beta (streamer-safe music toggle, mic-mode showcase, spoiler embargo map by scene code). Community seeds shipped inside the game, not around it: the spectrogram layer, the timecode-gap schedule, the era-variant tell table as discoverable, one real phone number if legal clears it. The ARG's future-dated episodes align to the post-launch content calendar so the fiction's fuse and the roadmap are the same document. Steam page live at M2 with the slice's assets; wishlist beats at puppet-reveal, demo, and date announce.

---

# PART VIII: RISK REGISTER (top ten, with owners)

1. **Tape pipeline underperforms** (authenticity is load-bearing): spike 1 gates the project; fallback is licensed hardware-emulation middleware. Owner: tech art.
2. **Coverage Director scope creep toward ML:** it is authored variant selection, never learned behavior; the profile is four booleans and a corridor histogram. Owner: systems.
3. **Sabotage AI soft-locks the finale:** fail-forward retake structure certified by bot soak; a cue can always be re-entered. Owner: systems.
4. **Merle casting misses warm-genuine:** audition scene is the ending-3 read; do not cast without it. Owner: director.
5. **Forced real-time capture bores:** content editing budget reserved in M4; the mitigation is cutting tape runtime, never adding a skip. Owner: director.
6. **Photosensitivity noncompliance in tape-world assets:** auditor engaged at M2, every asset passes the TBC-on mode. Owner: producer.
7. **Show footage reads as fake:** the puppet decision exists to kill this risk; if in-engine fallback is forced, budget doubles for tech-art time. Owner: tech art.
8. **Burn-in rule generates launch-week backlash:** pre-brief in UI copy, Matinee relief valve, and a director's note in the binder itself. Owner: director.
9. **Buried stratum leaks pre-launch:** asset encryption until day one; the community layer is a launch feature, not a build artifact. Owner: producer.
10. **Scope tier mismatch discovered late:** the descope ladder is pre-agreed in writing at Gate 0, so cutting is execution, not debate. Owner: producer.

---

# PART IX: THE FIRST 30 DAYS (do these now)

Week 1: Gate 0 decisions drafted; spike briefs 1 through 7 written with pass/fail lines; puppet fabricator quotes requested with the tell-table attached; Merle casting breakdown out.
Week 2: engine spike 1 and 2 running; compound greybox begun from the routing doc's schematic; Dark Ledger scored pass on the master document's ten dialogue scenes, revision list produced.
Week 3: spikes 3 and 4; audio bible drafted with the composer conversation started; invariant suite designed as a document (each law, its test, its telemetry).
Week 4: spikes 5 through 7; Gate 0 signed; M0 exit checklist owned; the Steam page's private draft started so marketing debt never accrues.

**The plan's one-line thesis:** systems are built once, content flows through them in tapes, both ledgers gate every milestone, and the fiction's laws are the test suite. The game about restoring something carefully gets built the same way.


------------------------------------------------------------------------------
DOCUMENT 45 · restoration-demo-cut-plan.md
------------------------------------------------------------------------------

# RESTORATION · DEMO CUT PLAN v1 · TAPE 1, FREE
Per the release model: the trust arc is one arc, so the demo is its first act whole: Day 1, no startle until the last ninety seconds, ending on the in-tape lunge and the lit RESPOND sign. Target length 25 to 40 minutes; speedrun floor about 12. The demo save is the full game's save (schema v15); CONTINUE in the full program imports it, ledger and all, which is the promise printed on the end card.

## 1 · THE DEMO'S SHAPE (Day 1 only, reordered for the button)
Arrive → dresser and welcome packet → sign S1 (the save-costs-paper lesson, softened: demo paper is S1 and S5 only, three sheets each) → the mini-screening (the signs, the beat, the three stances, judged gently on Matinee defaults) → the bench: capture Tape 1 in real time → the lunge, the game's one startle, bars → smash cut to the rec room where the RESPOND sign lights one final time, alone, unasked → hold two seconds → END CARD. Night never falls in the demo. The schedule is a rumor the full game keeps.

## 2 · BOUNDARY SPEC
IN: Entry, Rec Room, Kitchen, Dorms, Library, Bench, and the corridor between; the binder, the map, TBC and photo-safe, the gen knob, the coat pegs at Day 1 state, Merle at the kettle with her Day 1 line, Harriet in her chair.
LOCKED, with in-fiction demo reasons written on the doors: everything past the library. Standard string: "SEALED · the club opens the rest when the contract is signed." The transmitter corridor adds: "You can hear it from here. That is enough for today."
OUT ENTIRELY: the Rundown, nights, dailies and the burn loop, the Floor Manager, the presigned page, the dock, the crate, the seance, all four assets, the ledger's decision, every ending word.
TEASED, deliberately: the casting sheet visible with zero lines; the dresser's seven items counted; the sealed doors themselves.

## 3 · THE ENDING MOMENT (exact)
Capture completes → bars hold 1.6 s → cut to rec room camera position (authored) → RESPOND sign lights, hum only, 2.0 s → END CARD on black, phosphor type:
"TAPE 1 OF 5. THE PROGRAM CONTINUES. Your ledger, your signatures, and your paper carry into the full game. WISHLIST RESTORATION."
Below, small: "The 58 Club thanks you for careful hands."
No input during the card for 3 s (protect the beat), then any key to title.

## 4 · SAVE CARRY AND ANTI-SPOILER GUARANTEES
Same save file, same schema; a demo_complete flag set at the card. The demo build must be INCAPABLE of writing: decision, assets, leland_answers, lockdown, finale, or any ending field: not merely gated, absent from its write path, so no demo save can arrive pre-spoiled or pre-progressed. Full game on first CONTINUE from a demo save: Merle acknowledges it, one line: "You came back. I told them you would."

## 5 · ENGINEERING DELTA (implementable as one commit against v0.9)
E1 const DEMO in game_state (build-time flag). E2 world_builder: demo door-reason override table; skip spawning Rundown, FM, dock, crate, seance, cascade, assets, ledger, fire pickup. E3 bed_prop: demo branch, "The club insists you sleep at home until the contract is signed." E4 objective_text: demo branch ending at "capture Tape 1." E5 capture_bench: on demo completion, trigger the end sequence instead of the daily mint. E6 end card scene (reuses title scene styling). E7 title: demo build shows TAPE 1 · FREE DEMO under the logo. E8 save writer: demo field whitelist. E9 demo funnel telemetry, local file only (started, S1, screening, capture, lunge, card, minutes), no network, disclosed in the readme. E10 Steam: separate demo app id per the plan; depot shares the project.

## 6 · DEMO QA PROBES
DP1 all sealed doors state the demo reason; DP2 the whitelist: hand-inspect a completed demo save for absent fields; DP3 the ending sequence uninterruptible by movement or pause; DP4 paper exhaustion at S1 still leaves S5 (no softlock); DP5 carry test: demo save into full build, Merle's line fires once.

## 7 · WHAT THE DEMO SELLS (so the cut never drifts)
Care as gameplay, one contradiction (the slate versus the scope, present on the bench), one warmth (Merle, the kettle), one law demonstrated (the beat, the stances), and exactly one scare, positioned as a promise of restraint. The demo's last playable input is answering a children's show politely. That is the game, miniaturized, and the reason the sign lighting alone at the end works: the player has already learned what it means, and now it is asking them, and the card interrupts the answer.


------------------------------------------------------------------------------
DOCUMENT 46 · restoration-localization-plan.md
------------------------------------------------------------------------------

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


------------------------------------------------------------------------------
DOCUMENT 47 · restoration-merle-casting-breakdown.md
------------------------------------------------------------------------------

# RESTORATION · CASTING BREAKDOWN · MERLE COTTRY
Project: Restoration (indie horror, Steam). Role type: principal voice with on-camera performance reference for the animation team (the in-game figure is a crafted needle-felt build and is NOT the performer's likeness; voice and reference only). Sessions: three, per the audio bible; the monologue is targeted as one unbroken take. Age: authentic 62 plus strongly preferred over played-older. Ethnicity: open. Region of voice: soft Midwest, Ohio if we are lucky.

## THE ROLE
Merle Cottry, president of the 58 Club, the fan organization that has kept a dead television station warm for fifty years. She was seven in 1974 when she spent a night lost in a cornfield and was carried home by something singing, and she has spent every year since being the kind of person who makes cobbler for frightened people. She is the emotional center of the game, the player's chief comfort, and the reason the ending hurts. She recruits the player character, feeds her, defends her, and in one ending forgives her so completely it reads as damnation.

## THE ONE LAW (this is the whole breakdown)
Warm-genuine, never warm-sinister. There is no twist in this performance. She is not hiding anything, she is not secretly menacing, she never turns. The horror belongs entirely to the audience's knowledge differential: we know what carried her, and she knows too, and she is grateful, and that gratitude delivered with total sincerity is the scariest sound in the game. Casting will surface a parade of twinkle-with-menace reads, sweetness with a knife in it, the Annie Wilkes register. Pass on all of them immediately, however skilled. If the warmth can curdle, it is the wrong warmth. We are casting somebody's actual favorite aunt, and then we are going to break the player's heart with her.

## VOICE SPEC (per the audio bible)
Warm alto. Age carried in the breath, not the pitch. Zero irony available anywhere in the instrument. A laugh that arrives before permission. Unhurried; she has never once needed to talk over anyone. Comps for register, not for imitation: the plainspoken warmth of a Frances Sternhagen; the settled kindness of a small-town librarian who has buried friends and still bakes. Anti-comps, stated plainly for the casting director: no Piper Laurie religiosity, no Kathy Bates volatility, no knowing camp. If a read would work in a horror trailer, it fails here.

## AUDITION SIDES (in order)
SIDE 1, the light register, Day 1: "Oh, look at your gloves. You brought your own gloves." Direction: delight, not appraisal. She is charmed by competence the way other people are charmed by puppies.
SIDE 2, THE HIRE DECIDER, the ending-3 doorway: "Oh, honey. We have copies. Everyone has copies. That's what love is now. ... There's cobbler." Direction given to the performer, verbatim: read it as if to a granddaughter who burned dinner. Do not tell the performer this is the horror scene. The correct read contains no anger anywhere in it, because no anger anywhere on her is the worst available outcome, and the text says so.
SIDE 3, the 1974 close: "So bring me every date and every gap and every terrible arithmetic, and I will hold them. I promise you I will hold them. But I was carried. You don't vote against being carried." Direction: the first two sentences are for Rita; the last two are testimony. No tears. She settled this fifty years ago.

## THE CALLBACK
The pen-up silence, on camera: forty-five seconds of watching someone sign a document, hands empty and open, saying nothing. We are casting the hands and the patience as much as the voice; the in-game figure holds this pose at the game's decision point, and the reference footage drives it.

## THE REDIRECT PROTOCOL (one redirect, diagnostic)
In-session redirect, once, on Side 2: "Again, but she is prouder of Rita." If the warmth increases, that is the hire signal. If menace, archness, or knowingness appears under this or any redirect, pass without a second redirect. The instrument that can find menace will find it in the booth at midnight in month four, and we will ship it by accident.

## LOGISTICS AND DEAL NOTES
Three sessions (P0 session one covers Tape 1 and 2 lines; session two the monologue day, protected, morning slot, one unbroken take pursued as long as the performer is willing; session three endings and pickup). Recording dry on the WORLD chain per the audio bible. Credit: "and [Name] as Merle." Optional day rate: hand inserts for the puppet shoot (her hands pouring tea are a marketing asset). No likeness capture; the figure precedes the casting and stays.


------------------------------------------------------------------------------
DOCUMENT 48 · restoration-props-packet.md
------------------------------------------------------------------------------

# RESTORATION · PROPS PACKET v1 · FOUND DOCUMENTS, FULL BODIES
Every readable prop: physical spec, placement and gate (per the room inventory), the complete text, and what it must do. Bodies are final-draft; typos inside documents are authored and marked [sic by design].

## D01 · LELAND MERRICK'S CATALOG NOTES · green ink, four pages
Spec: steno pad sheets, fountain pen, a hand that starts architectural and ends fast. Placement: LIB compactus, page 4 inside the seance reel's box (gated by the crate). Function: the player's map of the descent, and the seance's instruction manual.
PAGE 1 (early): "Intake note, week two. The collection is better than reported and worse than organized. Slate numbering is Craik's own system, strict as scripture, which makes the skips interesting. Skips are normal. Clustered skips are a story."
PAGE 2: "Charted the gaps. They cluster around broadcast dates with no station log. A show that aired without airing. I have written that sentence three times and it has not improved. Coffee, then the audio bench."
PAGE 3: "Something in the sidebands under the closing song. Structured. I am not going to write the word until I have to. Also: tape 41 returned itself to the shelf. I had it on the bench. I am sleeping badly, which is the explanation, and I have underlined it so it stays the explanation."
PAGE 4 (with the reel): "It has offered me a role. That is the accurate verb. To whoever holds this next: never accept a role. Catalog it, love it if you must, but stay off the tape. If you are reading this on the bench, step gently. Every pass costs me. Finish it. Format keeps its own rules."

## D02 · ANSEL CRAIK'S PRODUCTION NOTEBOOK · 1977, fire-browned edges
Spec: hardbound quad-rule, pencil, margins pressed hard. Placement: TH cage, Craik's box, beside the finale script (T3 gate). Function: the rules of the antagonist, from its author.
ENTRY, MARCH: "Rule confirmed again tonight. It keeps the grammar because the grammar is what it is. On camera it performs. In a break it waits. It has never once broken format, and God help me that is the only reason any of us are alive to be tired."
ENTRY, MAY: "Edith says end it like a show, not like a fire. She is right about the first part."
ENTRY, JULY, the sign-off drafts, two struck through:
"~~Goodnight, everyone. The Gladhouse is closing.~~" [struck: too gentle, it can perform gentle]
"~~The show is over. Go home.~~" [struck: a lie, and it keeps lies]
Final, boxed: "There's no one at home anymore. The lights are off. The children grew up. You can stop looking for them. Say goodnight, Chum."
LAST ENTRY, undated: "If the truth doesn't finish leaving my mouth tonight, then it isn't a lie I told. It's a sentence somebody else has to end. Margin note stands. Tell them the truth or it doesn't take."

## D03 · ACCESSION LEDGER · sample spread
Spec: green-columned bookkeeping stock, multiple hands across decades. Placement: bench, always. Function: the paper economy's altar and the decision point's stage.
Entries: "0117, GLADHOUSE 22, 2in master, GOOD, M.C." · "0118 through 0121 [absent; the numbers simply do not occur]" · "0122, GLADHOUSE 23, dub, VG, per V. Keys the skip cluster begins here" · in green ink, older, small: "0299, UNLABELED, DO NOT BENCH, L.M." · the final printed line before blank stock: authored to be the presigned page's site.

## D04 · THE CLIPPING · Chillicothe Courier, October 1974
Spec: newsprint, sun-yellowed, one fold, kept behind shrine glass in REC. Function: Merle's monologue, corroborated by a document that almost fits.
"LOCAL GIRL, 7, FOUND SAFE AFTER NIGHT IN CORNFIELD. Merle Anne Cottry, missing since Tuesday supper, was found at dawn on her family's porch step, cold but unhurt. County searchers had suspended at midnight owing to rain. 'We don't know which volunteer walked her back and we'd like to shake his hand,' said Sheriff D. Pruett. The child, wrapped in a square of gray flannel her mother did not recognize, told deputies only that she had been 'carried the long way, singing.' The Courier joins the county in relief."
Design note: the gray flannel square is the same stock as post-fire patch seven. The shrine keeps the clipping; the player keeps the arithmetic.

## D05 · 58 CLUB WELCOME PACKET · one page, mimeograph purple
Spec: hand-typed, Merle's annotations in ballpoint. Placement: Rita's dresser, Day 1. Function: house rules that read sweet on Day 1 and load-bearing by Day 3.
"WELCOME TO THE FIFTY-EIGHT! House keys hang in the kitchen. Quiet hours are posted by the clocks and we do mean them [ballpoint: we really do]. Meals are communal, cobbler is medicinal. If a door is closed, it is closed for a reason and the reason is written on it. If you hear the show, you are hearing memories, and memories keep a schedule. Make yourself at home. You already are. [ballpoint, smaller: welcome home]"

## D06 · HARRIET'S NOTE · the seventh signal
Spec: film-cabinet index card, pencil, exhausted capitals. Placement: film cabinet, post-training-film gate. Function: the gift.
"THE SIX ARE IN THE FILM. THE SEVENTH THEY STOPPED PRINTING. BOTH HANDS FLAT, PRESSED DOWN TWICE: HOLD YOUR APPLAUSE. WHEN HE GIVES IT, SOMETHING IS ABOUT TO GO WRONG ON PURPOSE. HOLD STILL AND LET IT MISS. H."

## D07 · VESS'S RESEARCH BINDER · excerpts
Spec: three-ring, tab dividers, printouts annotated in three pen colors. Placement: DRM, his room, door ajar. Function: one true insight, one confident error, and the credit chain's object.
Insight page: an airdate table with gaps circled and the margin: "clusters. CLUSTERS. not decay, selection."
Error page, block letters: "CONCLUSION: A SECOND TRANSMITTER. SOMEBODY HAS BEEN REBROADCASTING FROM A SISTER SITE. FIND THE SITE, FIND THE TAPES." [wrong, sincerely]

## D08 · THE FLOOR MANAGER'S RUN SHEET · glimpsed angle only
Spec: laminated, grease pencil, always angled away; the player reads at most one column edge. Function: wrongness by arithmetic.
Legible fragment: "SEG 4 ... :22 / SEG 5 ... :41 / SEG 6 ... :63 [sic by design] / SIGN-OFF ... [grease smear]". Design note: the timings must not sum to a broadcast day. Nobody comments.

## D09 · FIRE MARSHAL REPORT · 1977, photocopy of a photocopy
Spec: county letterhead, generation-lost toner. Placement: CTL drawer, Day 2 gate. Function: official history with one live wire.
"Cause: undetermined, consistent with deliberate ignition at the tape vault. Total loss of stored media. Note of record: transmitting equipment found energized at time of entry and could not be de-energized by responding personnel. Referred to station engineer. No further action."

## D10 · IRIS BELL'S FAN LETTER · 1975
Spec: ruled school paper, pencil, careful loops. Placement: props crate, beneath the sign-off card. Function: the show as it was loved, so the ending costs.
"Dear Chum, my brother says you are just a puppet but I know a secret which is that everybody is a puppet of somebody and it only matters if the hands are kind. Your hands seem kind. Please wave at camera one on my birthday which is the 9th. Your friend, Iris Bell, age 8 and one quarter."


------------------------------------------------------------------------------
DOCUMENT 49 · restoration-puppet-fabrication-brief.md
------------------------------------------------------------------------------

# RESTORATION · PUPPET FABRICATION BRIEF · RFQ v1
Confidential under NDA. Ground truth: the four supplied reference plates. Where this brief and the plates disagree, the plates win. Budget frame for the full deliverable set including cases: 25,000 to 60,000 USD; please itemize. Work for hire; fabricator credited in game and trailer.

## 1 · WHAT THIS OBJECT IS FOR (triple duty drives every spec)
Chum is (a) the hero performance puppet for two to three weekend shoots against written tape scripts, (b) the photogrammetry source for the game's entire fiber material library, and (c) the marketing object: trailer star, press-photo subject, merch prototype. He must perform, scan, and survive handling. Where those needs conflict, scanning wins on surface fidelity and performance wins on structure.

## 2 · DELIVERABLES
D1 CHUM HERO BUILD (the 1971-1974 base body). D2 Dressing kits: 1971 NEW (unworn finish) and 1974 LOVED (authored wear pass: hand-polish on grip zones, sun-fade crown, one visible early patch). D3 POST-FIRE BUILD: a second complete puppet per the tell-table in Section 5; the deltas are structural and cannot be a dressing kit. D4 4K FINISH PASS: the hero build cleaned and groomed to unsettling perfection for the remaster-era plates (a finishing service, not a build). D5 UNDERSTUDY BUILD: a dimensional clone of the hero at plus four percent overall scale, tolerance plus or minus 0.5 percent, for the live-scene plates. D6 SPARES KIT: four amber eyes, six buttons, three bells (one pre-blackened with pry marks), reserved dye-lot wool yardage, patch fabric stock including two yards of the gray school flannel matched to supplied swatch S-07, thread cards. D7 Fitted travel case per build.

## 3 · BASE BUILD SPECIFICATION (D1)
Form: a patchwork cat, seated height 55 cm, hand puppet with rod-arm option. Exterior: brown wool, hand-patchwork over a stuffed muslin core; visible hand-stitching throughout; nothing may read machine-made at 30 cm. Armature: wire in ears, tail, and spine; neck poseable and repeat-accurate; paws weighted. THE MOUTH DOES NOT ARTICULATE: the grin is cross-stitched and fixed by design; all performance lives in head, ears, tail, and posture. Eyes: viewer-left, amber glass, taxidermy grade, 14 mm; viewer-right, black four-hole button, 18 mm, attached with visible waxed thread. Whiskers: fine wire, six per side. Bell: brass, 25 mm, at the collar, SUPPLIED SILENT: clapper removed invisibly; the bell must never be able to ring (this is a hard requirement with a story reason; a ringing bell on set is a ruined take and a ruined day).

## 4 · SURFACE AND SCAN REQUIREMENTS
The puppet is a scanning subject: no anti-static or sheen-altering sprays ever; dyes UV-stable for repeated lighting; fibers must tolerate photogrammetry cross-polarized passes; a concealed mounting socket at the base of the spine for a hidden stand; seams reachable for macro capture. Supply fiber content and dye documentation with delivery so the material library can cite it.

## 5 · THE TELL-TABLE (D3, the post-fire build: measurable specs, caliper-checked at QC)
Doctrine: REPAIRED, NOT BURNED. No char, no melt, no horror finishing. Every delta is a repair performed with care by something that only had footage to work from.
T1 Grin extended 18 mm past each cheek seam, same cross-stitch gauge.
T2 Coat button oversized and wrong: 28 mm horn where an 18 mm shell should be.
T3 THE EYE SWAP: amber glass now viewer-RIGHT, button viewer-LEFT; amber pupil axis set 8 degrees off vertical. (Story note for your team's sanity: it repaired itself from its own footage, and footage lies about left and right.)
T4 Whiskers replaced by stubs: 6 mm cut ends, all sides.
T5 Bell blackened, crown pry-marks, still silent.
T6 Belly seam resewn in visibly newer, undyed thread.
T7 Fourteen patches per the numbered placement diagram (supplied at contract): thirteen assorted wools and flannels including one of swatch S-07 gray school flannel, plus one leather patch 40 by 55 mm at position P11.
T8 Head tilt built into the neck armature at 2.5 degrees, resting state.
T9 Stance: left forepaw set 12 mm forward of square (the wrong foot).

## 6 · DURABILITY
Three shoot weekends, trailer day, press handling: reinforce puppeteer access points, double-stitch all load seams, and assume one hundred insertions. Repairs during the contract period are the fabricator's; the spares kit exists so ours afterward look like yours.

## 7 · PROCESS AND GATES
Quote (itemized by deliverable) → maquette or foam proof approval → hero build → QC against Section 5 with calipers and the plates → variant kits and 4K pass → post-fire build → understudy. Photo checkpoints at each gate. Please propose a timeline; payment milestones will align to gates. Two questions we want answered in the quote: your recommended wool sourcing for a fifty-year-appropriate hand, and whether the understudy's four percent scale is better achieved by pattern grading or full re-draft.


------------------------------------------------------------------------------
DOCUMENT 50 · restoration-spike-briefs.md
------------------------------------------------------------------------------

# RESTORATION · TECHNICAL SPIKE BRIEFS 1 TO 7
Per the build plan's Workstream 1. Each spike is 1 to 2 weeks, ends in a written PASS or a mitigation memo, and M0 does not exit until all seven are one or the other. The v0.5 prototype (commits 001 to 020) has pre-banked evidence against several; each brief states what is already in hand and what remains before the word PASS may be written.

STATUS BOARD
1 Tape-world pipeline: PARTIALLY RETIRED. 2 Frame Discipline: OPEN (hardware-bound). 3 Seance: PARTIALLY RETIRED. 4 Rundown AI: PARTIALLY RETIRED. 5 Coverage Director: SUBSTANTIALLY RETIRED. 6 Power sim: PARTIALLY RETIRED. 7 Live production: SUBSTANTIALLY RETIRED.

## SPIKE 1 · TAPE-WORLD PIPELINE
Question: can per-generation artifact simulation be a controllable, diegetic, tool-reactive shader stack rather than baked footage?
Pass line (plan): one clip, four generation states, artifacts diegetic and tool-reactive, photosensitivity-safe mode verified.
Method: take one real 20 second clip (phone-shot puppet stand-in is fine), run it through the shader stack, capture the four states side by side, wire TBC and tracking to live uniforms, then run the photosensitivity pass (cap flash frequency and luminance delta; a reduced-artifact mode that preserves diegesis, precedent already set by the UI specimen's reduced-motion support).
Banked: crt_tape.gdshader (chroma, scanlines, noise, tracking band, head-switch tear), generation uniform with the bench knob, TBC as live DSP, wear riding the same ladder (commits 008, 010, 020).
Remaining: real video texture instead of the live diorama, dot crawl term, the four-state capture reel, the safe mode. Timebox: 1 week. Fallback per risk register: licensed hardware-emulation middleware. Owner: Ciel's machine (GPU work), shader text from this side.

## SPIKE 2 · FRAME DISCIPLINE RENDERING
Question: do N live camera feeds at render-target cost hold 60 fps on target hardware with tally logic and provably correct mediated-safety state?
Pass line: 12 simultaneous feeds, one patchbay re-route, safety state provably correct in a test scene.
Method: scale the existing MonitorRig from its current handful to 12 in one scene, profile on the actual target machine, then write the safety-state assertion (a debug overlay that renders SAFE or EXPOSED from the ruleset and a test that walks every state transition).
Banked: MonitorRig as SubViewport render targets, kill and re-patch flow, lockdown sync_to (commits 002, 006, 012).
Remaining: the count, the frame-rate proof, the assertion overlay. This spike is hardware-bound and cannot be retired from text. Timebox: 1 week. Fallback: feed budget of 6 with round-robin refresh (visually authentic to period switchers anyway). Owner: Ciel's machine entirely.

## SPIKE 3 · THE SEANCE
Question: frame-accurate jog and shuttle over video, a compositing layer for Leland between frames, wear persisted?
Pass line: step, jump-cue, wear write-through to save, reload persistence.
Method: replace the diorama's staged frames with an actual VideoStreamTheora clip stepped by frame index, composite the Leland layer at frame boundaries, keep the existing wear plumbing untouched.
Banked: Z and X stepping, five fixed-frame reveals, wear written through to save and driving the artifact ladder, reload persistence proven (commit 010; knob restore fix in 020).
Remaining: real video substrate and jump-cue (type a frame number). Timebox: 1 week. Fallback: image-sequence player (frames as textures), which is period-plausible and trivially frame-accurate. Owner: split; the image-sequence fallback can be written from here.

## SPIKE 4 · RUNDOWN AI v0
Question: segment patrol with audio localization, camera-kill behavior, one unscripted seek, and zero grammar violations under soak?
Pass line: a bot survives a night using only audio cues; the AI never violates a grammar invariant in a 4-hour soak.
Method: add audio-event localization (footsteps, doors, the degausser emit events the Rundown weighs), write the survival bot against the segment-loop audio, then the 4 hour headless soak asserting the invariant list from the build plan (warn precedes reach, no strike through walls, no strike during ON AIR coverage).
Banked: segment patrol with homes and relocation, warn and strike radii, camera kills, savoring mode, director-expressed blockings, premiere yield (commits 003, 006, 009, 014).
Remaining: it does not hear yet; the bot; the soak harness. Timebox: 2 weeks. Fallback: scripted seek table per night instead of localization (authored, still fair). Owner: logic from here, soak on the machine.

## SPIKE 5 · COVERAGE DIRECTOR v0
Question: deterministic behavioral profiling selecting between blockings, explainable from a log?
Pass line: deterministic profile from logged inputs; blocking selection explainable in the log.
Method: add an append-only session log (timestamped counters and every blocking decision with its reason string), replay a recorded input file twice and diff the profiles.
Banked: checker, sprinter, hider profiling from behavior; three expressed blockings plus the savoring mood law; the burn reset (commit 009). The plan's scope guard is already honored: four booleans and counters, no learning.
Remaining: the log and the determinism replay. Timebox: 3 days. Owner: from here, verified on the machine.

## SPIKE 6 · POWER AND PATCHBAY SIM
Question: amperage budget, breaker trips, corridor liveness, sustaining the Night 4 sequence?
Pass line: the Night 4 sequence greyboxed end to end.
Method: extend the two-circuit budget to the full panel map from the room inventory, script the Night 4 cascade (trip, darkness spread, restoration order), assert liveness (some route is always lit or lightable).
Banked: two circuits one budget, NO SIGNAL propagation, revive-first re-patch, the night-one trip event, finale breaker phases (commits 004, 006, 017, 014).
Remaining: full panel scale, the cascade, the liveness assertion. Timebox: 1 week. Owner: from here.

## SPIKE 7 · LIVE-PRODUCTION FINALE LOOP
Question: cue sequencing, input mapping, sabotage events, retake checkpointing per cue?
Pass line: Phase 2 skeleton playable with placeholder everything.
Banked: this pass line is substantially met at prototype grain: cue marks, timed sabotage with take counters and per-cue re-entry, the breaker variants, the divert window, the little door cue (commit 014). The build plan's risk 3 mitigation (a cue can always be re-entered) is implemented.
Remaining before the written PASS: a switcher input map (number keys cutting cameras during cues) and a 30 minute fail-forward soak (deliberately fail every cue three times; no soft-lock). Timebox: 3 days. Owner: input map from here, soak on the machine.

## HOW THESE CLOSE
Each spike ends as one page: the pass line, the evidence (captures, logs, commit ids), and a signature line. Mitigated spikes instead state the fallback adopted and its cost. The seven pages staple to the Gate 0 packet, and M0 exits.


------------------------------------------------------------------------------
DOCUMENT 51 · restoration-steam-presence.md
------------------------------------------------------------------------------

# RESTORATION · STEAM RICH PRESENCE SPEC v1
Doctrine: a friends list is a broadcast. The schedule may appear on it; the secrets may not. Presence strings are diegetic, spoiler-null, and localized through Steam's richpresence.vdf alongside the game's own waves.

## STATES AND STRINGS (english masters)
#Day            "Day %day% at WGLD"                    · default daytime
#OnAir          "ON AIR · do not knock"                · Broadcast.on_air true
#Bench          "At the bench · Tape %tape%"           · capture running
#Night          "After sign-off"                       · any night, INCLUDING every late-game state without exception
#Premiere       "THE GLADHOUSE RETURNS (LIVE)"         · premiere_live true (the Steam page already says this much)
#Credits        "Signing off"                          · credits scene
#Menu           "At the title card"

## SPOILER RULES (meta-silence, third surface)
Never: any ending name, DEAD AIR, the seance, the quiet room, the dock's contents, the once-ever moment, day numbers past 5. Nights are all one string on purpose: a friend watching a presence feed learns the schedule exists and nothing else. Chum's name appears in no presence string, same reason as ever.

## HOOKS (for the GodotSteam pass)
GameState already emits everything needed: day changes, Broadcast.on_air, capture status, premiere_live, plus the credits scene's _ready. One bridge script subscribes and calls Steam.setRichPresence("steam_display", key) with substitutions; the bridge ships alongside the achievements bridge and, like it, is absent under DEMO.


==============================================================================
SECTION APPENDIX A · THE COMMIT NARRATIVE
==============================================================================


------------------------------------------------------------------------------
DOCUMENT 52 · README.md
------------------------------------------------------------------------------

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

## Commit 035 · AFTER-FIRE (the tally contract)
Watching the fire tape wakes the eleven-footer: the Rundown embodied per
docs/canon/restoration-after-fire-chum.md and the dossier art beside it.
While a capture runs he may cross the whole building to stand at 1.2 m,
weighted footsteps sounding, jaw captioned once, strike forbidden: the
tally is the contract. When it cools (2.0 s, announced) a strike lands
only if you let the clock die with him beside you; otherwise he withdraws.
The HUD counts it both ways: REC · SAFE WHILE LIT. Abort clears the flag
too: fleeing the bench starts the cool immediately. Dossier findable as
D11 (Day 4, master control) once he walks.

## Commit 036 · ELEVEN FEET (the scale law)
The number is now the mechanic. On waking, the body stands 3.35 m; the
tally eye at 3 m glows red only while a capture runs, so the light IS the
contract; and he does not fit through doors: every threshold costs him a
2.2 s fold, captioned, day and night. Rooms are his; doorways are yours.

## Commits 037-038 · THE TWO HIDES and THE LAST CROSSING
The lit hide: camera cones remain the shelter, him waiting at frame's edge.
The dark hide: the dead room eats your sound; he is deaf to anything born
inside it and holds at the felt door. The taught chase: his first cool runs
4.0 s with instructions written in dread. And DEAD AIR now costs a chase:
seventy-five seconds, master control to the little door, tally eye dark
because you diverted yourself off the rundown. Reached, caught, or late:
three authored outcomes.

## Commit 039 · THE LEDGER OPENS (M1, H1)
The casualty ledger is real: binder page one lists entries in stamp
register, or NO ENTRIES. KEEP IT SO. Merle asks at the fire tape and
consent is her first grave: repossessed mid-sentence, warm to the last
unfinished word, the kettle clicking off two rooms away. Harriet's frozen
hand offers a slip on Day 2+: free paper that signs in her hand, and the
next break edits her for continuity; the seventh signal gates shut if her
card was never found, and screenings judge 0.05 tighter without her.
Ending 3 and 2 carry their dead-Merle variants.

## Commit 040 · VESS (the credit dilemma)
Two pens, two graves. Credited: the record is a call sheet, activating at
AUTHENTICATE (every monitor cuts to her mid-sentence) or at the final
breaker she keeps (the handle drops, the lights hold, bars). Uncredited
but used: the cascade panel offers GET VESS, the full fix in eleven
seconds, then circuit F bare-handed, because nobody thanked her first.
Dead, the breaker is a fused pin and a hard blackout; the crossing loses
its grace (62 s); ending 2 inherits her warm chair; 1B files FILE UNDER:
STAFF. Restoring alone, in order, saves her. Choose her danger.

## Commit 041 · THE FLOOR MANAGER (F1, F2)
F2: the third blind tally call has a cost now. Coverage must come from
somewhere, and he steps into frame to cue a camera the run sheet never
carried. F1 lives inside the crossing as promised: at the divert, he is
already reaching for the master fader. Let him hold it and DEAD AIR
becomes 4a HIS HAND, found after in a YOU'RE ON point, CUE GIVEN beneath
the sign-off. Hold it yourself and your arm takes the argument, the
crossing loses thirteen seconds, and 4b HER HAND signs off left-handed.
If he is already dead, no one reaches for it but you. Ending 2 gains the
open headset nobody closes.

## Commit 042 · LELAND (L1, L2, endings 4c and 0)
Past the wear, the pad has room for a sixth line: ask it and the ink
leaves the paper, he is retroactively unfound, the dock goes inert, and 1A
closes forever (1B files AND THE READER, UNFILED, in pencil, because the
green ink is gone from the world). Or feed the fire tape into the wake:
the sign-off completes in his reading voice, the answers un-write, the
little door closes from the inside, and the premiere's final break simply
ends itself: 4c · THE COMPLETED SIGN-OFF, every light down in reverse tour
order, the tower light out, reading as rest. And if all four living are in
the ledger before lockdown, the premiere runs anyway: 0 · A ONE-WOMAN
SHOW, nine credit cards, one name, hidden A28, never advertised.

## Commit 043 · THE ARC CLOSES (rows, A27, the reading)
Every timed incident abandoned past its window now takes a seated club
member (cut away from a smile, cut back to an empty chair). Every ending
opens its credits by reading the ledger aloud: name, cause, epitaph, and
the club's new arithmetic. A27 EVERYONE GOES HOME rewards the run with
nothing to read. Cast sheets canonized under docs/canon/art (Vess Keys,
he, PER V. KEYS everywhere; Leland Merrick, whose green-ink L.M. was in
the props packet all along; Merle co-founded the Club with him; Rita's
taglines adopted). The station is WGLD, Channel 58, by the author's word.

## Commit 044 · THE SPLICE (H2, and the answers grieve)
The rejected block's second life: after the viewing it offers the splice,
label disclosed (THE SONG, HARRIET LEFT OF FRAME), and joining the takes
mints a daily with no bench and no twelve seconds. The next break doubles
her, an inch to the left, both mouths on different vowels, and she stays:
scenery the schedule stopped scheduling, one line forever, the double
rebuilt on every load. The seance now grieves: frames 14 and 28 answer
differently for the dead, and every reading with her name carries
TRANSITION UNRESOLVED. Ten of ten deaths built. Zero open graves.

## Session 65 · HARRIET CANONIZED + THE PRESS KIT
The Continuity Keeper joins the cast doc, her sheet quote now speaks in
the build, and docs/press-kit ships whole: factsheet (features all
implementation-backed), cleared pull quotes with a firm embargo doctrine
(graves are not previews), and all six portraits. Standalone press zip in
outputs.

## FIRST BOOT (Session 66)
Executed for the first time on Godot 4.3 headless inside the build
environment: fifteen import errors fixed in one round, then ZERO errors,
two clean soak runs, invariants I01/I02/I22 PASS, and a valid v16 save
written by the running game. Full report and raw telemetry in
docs/telemetry/first-boot/.

## Commit 045 · THE RULINGS (crouch as body verb)
All ten gap-audit mechanics ruled by the author. Crouch ships: Ctrl or
pad B toggle, camera drops 0.6, speed 0.55x, and it is useless against
him BY ARCHITECTURE, because his model has no posture or footstep channel
to fool. I31 and QA-58 guard the promise. No sprint, ASSIST only,
stations-only saves, studio-safe photo mode, PREMIERE+ parked.

## Commit 046 · THE SECRET (three reels, ending A)
The unnumbered reels from Merle's refused donation hide where the lore
said they would: one in the accession skip gap itself. Watch all three
and the final break gains a radio through three walls; reach it and
ENDING A · AUDIENCE ONLY plays: the premiere band-limited (the audio law
holding even here), the broadcast that never ends, the dawn walk past the
seated rows, and AND NOW. THE TOUR CONTINUES as the radio's last words.
Leland's warning, obeyed completely. No trophy, by design.

## Commit 047 · THE PILGRIMAGE AND THE PAYOFF
The secret now costs what it should: four clean dailies before damaged
stock will accept your hands, one S2 slip per reel for forms the ledger
will never hold, the chain W1 to W2 to W3 across three days (the last
with him awake and the yard between you), and the dial confirmed in the
dead room before the break will ever mention a radio. And it pays what it
should: the sit, hearing the show run without her; the program guide
after the credits, five segments heard nowhere else, never printed; and
58 · STILL ON on the title screen, forever.


==============================================================================
SECTION APPENDIX B · THE BUILD LOG
==============================================================================


------------------------------------------------------------------------------
DOCUMENT 53 · BUILD-LOG.md
------------------------------------------------------------------------------

# RESTORATION · CLAUDE'S BUILD CHECKLIST
Working tracker derived from the build plan. Conventions: canon precedence runs rubrics → master document → design docs → this list; no em dashes anywhere; every deliverable is one file in outputs, synced to the working directory; anything engine-side is tagged [ENGINE] and produced here as specs, briefs, or prototypes, not builds.

## GATE 0 (decision memos I can draft; Ciel signs)
- [ ] Engine decision memo (UE5 vs Unity 6 criteria matrix, spike-result slots)
- [ ] Release model memo (boxed + Tape 1 demo, chaptered variant costed)
- [ ] Show footage memo (real puppet recommendation, budget lines, fabricator brief attached)
- [ ] Scope tier selection recorded (A / B / C) and milestone map recut to it

## M0 · PREPRODUCTION DELIVERABLES
### Design and UI
- [x] UI kit v0 + title screen + component specimens (restoration-ui-specimen.html) · THIS SESSION
- [x] Character design sheets v1: Chum era plate with live tells, eight cast cards, drift meters · THIS SESSION
- [x] Signal glossary visual (seven hands, seventh flagged G2) · THIS SESSION
- [x] Working TBC accessibility demo inside the specimen book · THIS SESSION
- [ ] Compound greybox: interactive HTML map of all zones, stations, sightlines (from routing doc schematic)
- [ ] Art bible document (compound naturalism spec, tape-world artifact spec, casting-drift wardrobe system, palette law)
- [ ] Key art brief (the light-off-a-CRT composition studies; trailer law respected)
- [ ] UI type licensing shortlist (Selectric-class mono, Vidifont-class CG face)

### Writing and audio
- [ ] Dark Ledger scored pass on all master-document scenes (scorecard + revision list, floor law enforced)
- [ ] Props packet: full found-document bodies (Craik notebooks complete, staff memos, FCC paperwork, Vess binder pages, club charter)
- [ ] Audio bible (segment themes as level design, hum floors, the silence tell spec, the bell's single sample brief)
- [ ] Merle casting breakdown (audition scene = the ending-3 read) + full cast breakdowns
- [ ] Chum performer brief (live puppeteer preference, finale live scenes)

### Systems specs [ENGINE]
- [ ] Spike briefs 1 through 7 with pass/fail lines (tape pipeline, frame rendering, séance scrub, Rundown v0, Coverage Director v0, power sim, finale loop)
- [ ] Invariant suite design doc (the ten laws as tests + telemetry fields)
- [ ] Coverage Director data spec (the four booleans + corridor histogram; blockings as authored variant table)
- [ ] Generations content table (every G2 source's one authored gap or contradiction, tracked)
- [ ] Save/burn-in technical spec (what persists, crash recovery, One Take flag)
- [ ] Controls doc PC-emphasis pass (M/KB first-class wording; gamepad parity kept)

## M1 AND BEYOND (queued; unblock after Gate 0)
- [ ] Tape 1 vertical-slice script package (every prompt, every caption, shot-by-shot for the in-tape lunge)
- [ ] Puppet shoot 1 shot list (T1.5, T2.8 material) from master doc
- [ ] Bench UI full interaction spec (splice minigame states, wear math surfacing, GEN stamping flow)
- [ ] Casting sheet + dailies loop spec (canister spawn rules, degausser interaction)
- [ ] Screening set-piece spec (T2.8 staging, unison audio design, response windows)
- [ ] Steam page draft copy + capsule brief; content-creator kit outline
- [ ] Trailer beat sheet (capture scare as the scare; never the glimpse, never the bell)
- [ ] Demo cut plan (Tape 1 boundaries, ending on the lunge and the sign)
- [ ] ARG/buried-stratum asset plan (spectrogram content list, timecode schedule frames, phone number legal check)
- [ ] Playtest protocol doc (cohorts, the standing questions with owners and dates)

## SESSION LOG
- Session 1 (today): PC platform confirmed. Built the UI specimen book: title screen with boot sequence and keyboard menu, binder presentation form, accession ledger with GEN stamps and paper economy, cue signs with a working beat window, the casting sheet with capture/burn simulation, bench generation-pipeline demo with live artifact layers, Chum era plate (four variants, live tells), eight character cards, signal glossary. Verified: HTML parses, JS syntax clean, reduced-motion and TBC honored, no localStorage, no em dashes. Next up by priority: compound greybox map, Dark Ledger pass on master scenes, spike briefs.
- Session 2: Chum canonized as a handmade patchwork CAT from Ciel's four-plate reference set (amber glass eye viewer-left, black button viewer-right, cross-stitch grin, silent brass bell). Post-fire redesigned under the new design law: repaired, not burned. Nine-delta horror set written into the design doc; specimen book's Chum plate rebuilt as the cat with all four eras live, including the over-grin, wrong button, eye swap with off-axis pupil, wire whiskers, pried bell, accessed belly, wrong-material patches, head tilt, and wrong-foot stance. Plotline doc species line updated. Flagged: the post-fire reference card mislabels itself 1971 PILOT VERSION; regenerate with the new spec. New item below.
- [ ] Regenerate post-fire Chum hero image per delta set v2 (prompt brief delivered in chat)
- [x] Room inventory and interactability bible (18 spaces + globals, gate-coded) · Session 3
- [x] Crafted World art doctrine canonized; design doc Part II amended · Session 3
- [ ] Room plate renders, hero order: BEN, REC, STA, DR, DOCK, then connective tissue
- Session 3: Crafted World doctrine established (all spaces and characters in the reference-plate craft style; humans as cloth-and-felt figures; two-worlds contrast moved to lighting + artifacts). Full room bible delivered: 18 spaces, every prop, interactability gates T1 to T5 with COND/EVT/SPAWN/DYN states, per-room state changes, global dynamic items, and a hero render order.
- [x] GATE 0 · Engine committed: Godot 4 (text-native projects, free, Steam-proven; UE5 documented as Tier-B escape hatch) · Session 4
- [x] Commit 001: runnable Godot greybox (living wing + library from room data table, FPS controller, log-station saves with paper economy, TBC autoload, HUD) · Session 4
- [ ] Commit 002: full compound data table, doors, bench capture stub, wool shader spike, monitor viewports
- [ ] Repo setup on Ciel's machine (git init; commits per session)
- Session 4: answered the how honestly (division of machine: text artifacts here, runtime/scans/audio/Steam builds outside; scan-first pipeline for the crafted 3D look; Steamworks path). Engine gate closed on Godot 4. Shipped Commit 001 as restoration-godot-prototype.zip: 4 core scripts + world builder + HUD, all gdparse-verified, tscn reference-checked.
- [x] Commit 002: full 20-zone compound from data, hinged + locked doors (shed, fire corridor, dead room), five log stations, capture stub with abort tether, monitor rig (SubViewport render targets), wool shader spike, HUD capture line; two 001 doorway alignment bugs fixed · Session 5
- [ ] Commit 003: Studio A dressing + catwalks, clock system, Rundown patrol stub, bench UI panel
- Session 5: shipped Commit 002 (restoration-godot-commit-002.zip). All scripts gdparse-verified; tscn reference-checked; room data table overlap-checked programmatically (SHED-in-YARD containment intentional). Wool shader written to spec but needs eyes-on judgment in engine; parameters exposed for tuning.
- [x] Commit 003: broadcast clock autoload (ON AIR/BREAK cycle) + wall clock repeaters, Rundown patrol stub (segment homes, break relocation, warn radius, strike-and-teleport with persisted casting sheet count), Studio A dressing (set, little door with canon refusal, Chum's mark, pedestals), catwalks + ramp, casting sheet prop, binder overlay (TAB) · Session 6
- [ ] Commit 004: capture-as-retake presentation, Rundown night gating, patchbay routing v0, the dorm dresser and seven items
- Session 6: shipped Commit 003 (restoration-godot-commit-003.zip). All scripts gdparse-verified, tscn reference-checked. Audio remains the standing deferral (hooks placed); CRAFT TIME's zone stands in at patch bay pending a workshop room in the data table.
- [x] Commit 004: day/night via Rita's bed (lighting shift, Rundown night gating), capture-as-retake presentation (slate, rewinding timecode, item loss, respawn at last signed station), the seven dresser items with persistence, patchbay routing v0 (two circuits, one budget, monitor NO SIGNAL state) · Session 7
- [ ] Commit 005: grammar v0 door rules, rec room mini-screening event, key items, save versioning
- Session 7: shipped Commit 004 (restoration-godot-commit-004.zip). All scripts gdparse-verified, tscn reference-checked. Respawn-at-last-signature closes the loop that makes the paper economy load-bearing.
- [x] Commit 005: grammar v0 (window-bound doors HELD FOR AIR), rec room mini-screening event (cue signs, response window, SPACE/Q inputs, PT award), key chain (kitchen board to shed to dead room), save-file versioning with migration announcements, binder PT/keys lines · Session 8
- [ ] Commit 006: dailies-burn loop, Rundown camera-kills, film cabinet + signals, binder options page
- Session 8: shipped Commit 005 (restoration-godot-commit-005.zip). All scripts gdparse-verified. Stance system is deliberately binary in v0; full three-stance beat ships with the Tape 2 screening build.
- [x] Commit 006: dailies burn loop (canister spawn per capture, single-slot carry, degausser strike removal), Rundown camera-kills with patchbay re-patch, film cabinet + six signals + Harriet's seventh as a gated note, binder presentation form with live mode switching, save v4 (first real migration) · Session 9
- [ ] Commit 007: title scene in-engine, tape/day objectives v0, procedural audio pass
- Session 9: shipped Commit 006 (restoration-godot-commit-006.zip). All scripts gdparse-verified. Coverage Director reset remains a named promise; One Take labeled honestly as pre-run-flow.
- [x] Commit 007 · PROTOTYPE v0.1 COMPLETE: title scene with save-aware menu, objective system with Day 1 walk-through and Day 3 completion state, procedural audio (transmitter hum, degausser coil, night segment tones via generator streams), save v5 · Session 10
- Session 10: declared Prototype v0.1 complete (restoration-godot-v0.1-complete.zip). The systems spine is proven end to end; everything remaining is production per the build plan: engine on Ciel's machine, scan pipeline, real audio, VO, the tapes, the Coverage Director, and the master document's scripted scenes, delivered as commits against this checklist.
- [x] Commit 008 · THE TAPE WORLD: artifact shader (chroma, scanlines, noise, tracking, head-switch, vignette; generation-scaled, TBC-steadied), tape stage diorama with wool-shader Chum, Scare 1 timeline (idle, approach, hold, single-frame lunge, bars), abort sync, visible slate-versus-scope anomaly · Session 11
- [ ] Commit 009: Coverage Director v0, Tape 2 screening on the tape stage, bench generation selector
- Session 11: shipped Commit 008 (restoration-godot-commit-008.zip). All scripts gdparse-verified. Three tuning verdicts requested from Ciel's first run: the hold's dread, artifact loudness at gen 0, TBC feel.
- [x] Commit 009 · Coverage Director v0 (behavioral profiling: checker/sprinter/hider, expressed through camera-kill priority, relocation logic, warn/reach tuning, savoring at three lines), dailies burn now resets the read (006 promise kept), bench gen knob, rec screening on a live tape stage · Session 12
- [ ] Commit 010: One Take run flow, fire-tape forced watch, séance v0
- Session 12: shipped Commit 009 (restoration-godot-commit-009.zip). All scripts gdparse-verified. Profiles session-only pending playtest verdicts.
- [x] Commit 010 · run endings (sheet-full and One Take play the final presentation to title; CONTINUE resumes morning-after), fire-tape forced watch (restraint scene, dimming stage, no sting), séance v0 (Z/X frame stepping, five fixed-frame answers, wear drives the artifact shader, binder tracking), save v6 · Session 13
- [ ] Commit 011: timing-judged stances, pre-signed page, dock inventory with the warm one
- Session 13: shipped Commit 010 (restoration-godot-commit-010.zip). All scripts gdparse-verified. Ten commits, 44 files: the systems spine plus the tape world plus the reader plus endings. Production verdicts from Ciel's playthrough now gate tuning.
- [x] Commit 011 · timing-judged three-stance screening (beat pulse, on/off-beat outcomes, stillness detection for QUIET), the pre-signed page at S4 (Day 2+, paper-free signature), the dock inventory with the warm one (contract enforced: nothing follows, ever), save v7 · Session 14
- [ ] Commit 012: lockdown scaffolding, the four assets as collectibles, decision-point ledger
- Session 14: shipped Commit 011 (restoration-godot-commit-011.zip). All scripts gdparse-verified. The beat system is the finale's call-and-response foundation.
- [x] Commit 012 · four Sign-Off assets as placed collectibles (spectrogram verse, MC cart, Craik's script, dock-gated card) with bench rack, decision-point ledger (pen cycle + SPACE commit, ink final), lockdown event (monitor sync, exterior seal, Merle's line, persistent), save v8 · Session 15
- [ ] Commit 013 · THE FINALE: route the decision to all endings
- Session 15: shipped Commit 012 (restoration-godot-commit-012.zip). All scripts gdparse-verified. The narrative spine is loaded; 013 fires it.
- [x] Commit 013 · THE FINALE: decision routes to all endings (Burn, New Producer with the one interface lie spent at the title, Sign-Off 1A/1B gated on Leland answers and wear, Dead Air divert gated on key + answers + fire tape), the bell beat, the line on player input, save v9 · Session 16
- Session 16: v0.3 NARRATIVE SPINE COMPLETE (restoration-godot-v0.3-finale.zip). 51+ files, 13 commits, all scripts gdparse-verified. Every ending in the master document is reachable in-engine. Remaining scope is production per the build plan: playable Phase 2 cue work, content waves, art, audio, VO.
- [x] Commit 014 · playable live production: cue marks, sabotage sprint with take counter, the Vess breaker (credited and uncredited variants, PT proxy flagged), the divert window in its canon slot, the little door closed by hand, Rundown yields the floor during the premiere · Session 17
- Session 17: shipped v0.35 (restoration-godot-v0.35-live.zip). All scripts gdparse-verified. Vess-credit proxy and single-beat sabotage are the named debts to M4.
- [x] Commit 015 · the Vess conduct chain (binder → margin credit → breaker variant, PT proxy retired), Merle as a scheduled world figure (kettle/chair/doorway, pen-up doorway behavior, state-tracked lines), save v10 · Session 18
- Session 18: shipped v0.4 (restoration-godot-v0.4-club.zip). All scripts gdparse-verified. Named debt from 014 retired.
- [x] Commit 016 · Harriet (break-window freezes, transition speech, the rising cup resolving in 1A), coat-peg drift meter, the NG+ relic (last-lost item on set, unremarked), save v11 · Session 19
- Session 19: shipped Commit 016 (restoration-godot-v0.4-details.zip). All scripts gdparse-verified. Queued-details list clear; next frontier is content waves or playtest tuning.
- [x] Commit 017 · tape progression (day-mapped, slated captures), night-one breaker event with the hummed-song beat, the Floor Manager (you're-on freeze check, silent, once per night), Vess's delivery crate gating the seance reel, save v12 · Session 20
- Session 20: shipped v0.45 (restoration-godot-v0.45-events.zip). All scripts gdparse-verified. Event wave 1 of the master-document scenes staged.
- [x] Commit 018 · the rejected edit (played, refused, backward rotation, Vess's two lines, cobbler), the glimpse (Day 4 unseal, once-ever contract in code), Merle's 1974 monologue complete, save v13 · Session 21
- Session 21: shipped v0.5 (restoration-godot-v0.5-heart.zip). All scripts gdparse-verified. Master-document T1 to T4 scene coverage complete at prototype grain; remaining scenes are asset-dependent.
- [x] Commit 019 · rec chairs convert to rows at lockdown (persistent), synthesized SFX autoload (bell with inharmonic partials at the bell beat, 3D door thunks, signature ticks), screening unison beat with Merle pulled to the rows · Session 22
- Session 22: shipped Commit 019 (restoration-godot-v0.5-room.zip). All scripts gdparse-verified. Prototype now covers everything text and synthesis can carry; the frontier is assets and verdicts.
- [x] Commit 020 · in-game facility map (M, drawn live from room constants, landmarks, player dot with facing), base-vs-temp generation fix (seance restores the knob's dialed value) · Session 23
- Session 23: shipped Commit 020 (restoration-godot-v0.5-map.zip). All scripts gdparse-verified. Engine frontier: assets, tuning, verdicts. Doc frontier: art bible, audio bible, spike briefs, props packet, Steam page, playtest protocol.
- [x] Playtest protocol v1 (restoration-playtest-protocol.md): setup, cold run + directed probes structure, the seven standing verdicts mapped to named tuning knobs, ending speedpaths, 16 probes, fairness invariants as witnessable checks, severity triage, external tester spoiler tiers, session report template, Dread Ledger quick pass · Session 24
- Session 24: documents frontier opened. Next doc candidates: audio bible, spike briefs 1-7, props packet, art bible, Steam page draft.
- [x] Audio bible v1 (restoration-audio-bible.md): two-worlds doctrine, bus and generation-chain architecture with TBC as real DSP, 16-slot inventory mapped to existing code hooks, the closing song spec with the G2 anomaly, one-stinger policy, voice direction incl. the Understudy double-voice, Godot implementation path (Sfx as swap registry), P0/P1/P2 asset list, the silence ledger as contract · Session 25
- Session 25: next doc candidates: spike briefs 1-7, props packet, art bible, Steam page draft.
- [x] Spike briefs 1-7 (restoration-spike-briefs.md): each with the plan's verbatim pass line, method, timebox, fallback, owner split, evidence already banked from commits 001-020, and remaining work; status board shows 5 and 7 substantially retired, 2 hardware-bound · Session 26
- Session 26: next doc candidates: props packet (full found-document bodies), art bible, Steam page draft.
- [x] Props packet v1 (restoration-props-packet.md): ten found documents with full bodies, physical specs, placements and gates, design functions: Leland's four pages, Craik's notebook with the struck sign-off drafts, ledger spread, the 1974 clipping with the gray flannel tie, welcome packet, Harriet's note, Vess excerpts, the run sheet fragment, fire marshal report, Iris Bell's letter · Session 27
- [x] Steam page draft v1 (restoration-steam-page-draft.md): taglines, short and long descriptions, feature set, demo positioning per the release model, tags, content notes incl. the one-startle promise, private until Gate 0 · Session 27
- Session 27: remaining doc list: art bible, invariant suite doc, Merle casting breakdown, puppet fabrication brief, key art brief, trailer beats, demo cut plan, ARG asset plan, greybox HTML map.
- [x] Commit 021 · SPIKE RETIREMENT PASS: Coverage Director counters persist across sleeps + append-only decision log with reason strings (Spike 5 text-side complete), Rundown audio localization via a noise bus (doors, signatures, footsteps; heard noise overrides relocation; Spike 4 core), switcher input map with wrong-camera refusal at cue marks (Spike 7 remainder), photosensitivity-safe mode on P suppressing bands/flicker/crawl + dot crawl term (Spike 1 remainders), station markers on the map from the spawn registry, save v14 · Session 28
- Session 28: shipped v0.6 (restoration-godot-v0.6-spikes.zip). Engine debts remaining: Spike 6 Night-4 cascade + liveness assertion, seance image-sequence substrate, systemic sabotage (M4), asset-dependent scenes.
- Session 28 addendum: duplicate _unhandled_input in hud.gd caught by the post-patch semantic assert (gdparse checks syntax only), merged into the existing handler with photo_safe taking an early-return branch, re-zipped. Note for the invariant suite doc: add duplicate-definition checks to the verifier.
- Session 28 correction: the prior addendum was premature. The first repair no-opped (anchors drifted; the binder action is named "ledger") and the broken zip shipped once. Second repair verified with hard asserts before zipping: _ready restored (_on_sheet/_on_tbc back in place), single _unhandled_input with photo_safe early-return, v0.6 zip rebuilt clean. Process change adopted: assert-before-zip chaining, and anchors verified with assert-in before every replace.
- [x] Commit 022 · SPIKE 6 CASCADE: Night 4 end to end (circuit C trip, darkness spread via HUD blackout layer, circuit B follow-on, ordered two-stage panel restoration, circuit F marshal-report tie), window holds waived during the cascade, Rundown bolder in the dark, liveness telemetry to user://liveness_log.txt, save v15. First attempt failed closed on a wrong reset-function anchor: no zip built, no false log entry; corrected anchor plus order-independent console wiring (_late_wire) shipped clean · Session 29
- Session 29: engine debts remaining: seance image-sequence substrate, systemic sabotage (M4), asset-dependent scenes.
- [x] Commit 023 · seance image-sequence substrate (Spike 3 fallback complete from this side): frame-indexed cached textures, deterministic per-frame seeded grain, Leland in-image cropped at the frame edge stepping in on answer frames, scratch marks on answers, pad stays overlay text by canon, drop-in swap point documented for real footage · Session 30
- Session 30: last named engine debt is systemic sabotage (M4). All other from-here spike remainders retired or hardware-bound.
- [x] Commit 024 · SYSTEMIC SABOTAGE (final named engine debt): continuous incident loop during the premiere (tally/house/boom/cards), one active at a time, fixtures to fix each, escalation via failed takes, triple fail-forward guarantee (refusal caps, single-press holds, 40s club auto-fix), premiere_log telemetry for the soak · Session 31
- Session 31: shipped v0.7 (restoration-godot-v0.7-sabotage.zip). THE FROM-HERE ENGINE LIST IS EMPTY. Remaining: hardware-bound Spike 2, assets, tuning verdicts, and the document queue (art bible, invariant suite, Merle casting breakdown, puppet fabrication brief, key art brief, trailer beats, demo cut plan, ARG plan, greybox HTML map).
- [x] Art bible v1 (restoration-art-bible.md): Crafted World doctrine, two-worlds contrast law (lighting + artifact pipeline only, grain belongs to tape), scan-first material system with swatch library, canonical palette hexes lifted from the engine, the drift law with per-character casting-drift wardrobe rules (Merle never drifts, Vess resists, extras lead), eye-hierarchy law (buttons are Chum's alone), hero room specs in render order, lighting doctrine, the sodium test promoted to the material gate · Session 32
- Session 32 note: set -e treats grep's zero-match exit as failure; clean-check greps now carry an explicit fallback. Doc queue remaining: invariant suite, Merle casting breakdown, puppet fabrication brief, key art brief, trailer beats, demo cut plan, ARG plan, greybox HTML map.
- [x] Invariant suite v1 (restoration-invariant-suite.md): 22 laws across grammar, mercy, scarcity contracts, economy, determinism; each with test, telemetry, and status (enforced / telemetered / manual); scarcity violations rated S0; harness plan with three bots and a per-build INVARIANTS.txt scorecard stapled to milestone gates · Session 33
- Session 33: doc queue remaining: Merle casting breakdown, puppet fabrication brief, key art brief, trailer beats, demo cut plan, ARG plan, greybox HTML map.
- [x] Commit 025 · THE HARNESS IN THE BOX: headless soak scene + runner with CLI args, three bots (wanderer/checker/fail with premiere seeding), WARN/STRIKE telemetry incl. wall raycast (I01/I02 machine-checkable), InvariantParser emitting user://INVARIANTS.txt scorecard, rigs grouped for the checker bot · Session 34
- Session 34: the zip now contains its own invariant test suite. Running the 4-hour soaks is Ciel's machine; the harness, bots, telemetry, and parser ship in the source.
- [x] Merle casting breakdown (restoration-merle-casting-breakdown.md): the one law (warm-genuine, never warm-sinister) with explicit anti-comps, three sides in order with the ending-3 doorway as the hire decider and its verbatim performer direction (granddaughter who burned dinner), the pen-up silence callback, the single diagnostic redirect protocol, session and deal notes incl. no-likeness clarity · Session 35
- Session 35: doc queue remaining: puppet fabrication brief, key art brief, trailer beats, demo cut plan, ARG plan, greybox HTML map.
- [x] Puppet fabrication brief RFQ v1 (restoration-puppet-fabrication-brief.md): triple-duty doctrine (perform/scan/survive), seven deliverables incl. post-fire as a second full build and the +4 percent understudy, base spec with the fixed grin and the silent bell as hard requirements, the nine-row tell-table as caliper-checkable specs, scan-surface rules, gates and two sourcing questions for the quote · Session 36
- Session 36: doc queue remaining: key art brief, trailer beats, demo cut plan, ARG plan, greybox HTML map.
- [x] Commit 026 · THE SELF-CONTAINED PROJECT: docs/ folder in the repo carrying all canon, production, and pre-production documents plus the UI specimen and the build log; docs/INDEX.md with a new-hire reading order; docs/unreal-5/UE5-MIGRATION-MAP.md mapping every prototype system to its UE5 home (subsystems, SceneCapture feeds, material-function tape ladder, MetaSounds, Gauntlet harness) with the closing law: engines are replaceable, the laws are not · Session 37
- Session 37: shipped v0.9-complete. The zip now carries its own paper. Doc queue remaining: key art brief, trailer beats, demo cut plan, ARG plan, greybox HTML map (each will be added to docs/ as written).
- [x] Key art brief v1 (restoration-key-art-brief.md): the one image argument (safety is mediated; no comp shares unmediated space), three comps (the bench hero with the legible slate-versus-scope, the club warmth alternate, the little door minimal), hard laws incl. marketing scarcity (the glimpse and Leland never depicted) · Session 38
- [x] Trailer beats v1 (restoration-trailer-beats.md): 90-second beat sheet obeying the game's laws (one startle at 1:05 mirroring the in-game budget, everything mediated until people being kind, cobbler as the exhale, the G2 word swap landing on the end card, one bell strike after black), capture plan split engine/shoot/plates, cut laws · Session 38
- Policy: restoration-godot-v0.9-complete.zip is the living complete artifact; new documents fold into docs/ and the zip refreshes in place. Doc queue remaining: demo cut plan, ARG plan, greybox HTML map.
- [x] Demo cut plan v1 (restoration-demo-cut-plan.md): Day-1-only shape ending on the lunge and the sign lighting unasked, boundary spec with in-fiction door reasons, exact end-card copy and timings, save-carry with a write-path whitelist (demo saves cannot be pre-spoiled), ten-item engineering delta implementable as one commit, five demo QA probes, the what-it-sells guardrail · Session 39
- Session 39: doc queue remaining: ARG plan, greybox HTML map. Engine candidate queued: Commit 027 implements the demo flag per the E1-E10 delta.
- [x] Commit 027 · DEMO MODE (E1-E10): one-flag Tape 1 demo; door seals with in-fiction reasons (transmitter corridor gets its own line); five spawn gates; bed declines; demo paper S1+S5; capture-complete end sequence (sign-alone beat, protected card, any-key exit); save-writer whitelist so demo saves cannot carry spoilers; local funnel telemetry; title badge. Three failed-closed stops before clean: wrong save-closer anchor, three patches falsely assumed applied, then my own miscounted assert. Nothing broken ever zipped or logged · Session 40
- Session 40: doc queue remaining: ARG plan, greybox HTML map. Full and demo builds are one flag apart.
- [x] Greybox HTML map v1 (restoration-greybox-map.html): generated verbatim from the engine's ROOMS, STATIONS, and landmark registry; demo-boundary toggle showing the Tape 1 seals; phosphor styling per the palette; regeneration rule (the engine is right) · Session 41
- [x] ARG plan v1 (restoration-arg-plan.md): three phases (the station exists, the recovered reel, the anniversary), six assets incl. the slate-skip community puzzle and the sideband verse mirroring the demo's own tool, the withheld seventh signal as a milestone gift, rules of play (Chum has no account), Tier A/B budget split · Session 41
- Session 41: THE DOCUMENT QUEUE IS EMPTY. Both files folded into docs/; complete zip refreshed. Remaining across the whole project: Ciel's playthrough verdicts, Spike 2 on target hardware, the soak runs, Gate 0 signatures, and everything asset-bound.
- [x] Gate 0 packet (restoration-gate-0-packet.md): four signable decision memos (scope tier, engine with the Spike 2 veto clause, release model, show footage with V1 as evidence), a first-90-minutes quickstart, and the on-signing procedure; week one of the plan's first thirty days complete on paper · Session 42
- Session 42: the packet's purpose is that it cannot be finished from this side. Named future candidates if building resumes before verdicts: an options menu (volume, mouse sensitivity, fullscreen: a genuine engine gap), an accessibility conformance pass against Ciel's own professional skill, achievements design, localization plan.
- [x] Commit 028 · THE BOOTH: options panel (master volume via bus 0, mouse sensitivity multiplying the player's constant, fullscreen with headless guard, TBC and photo-safe surfaced), O key in game plus an OPTIONS title button, settings in user://settings.cfg apart from the save so NEW GAME never resets them · Session 43
- Session 43: next named candidates if building resumes before verdicts: accessibility conformance pass, achievements design, localization plan.
- [x] Accessibility conformance pass v1 (restoration-accessibility-conformance-pass.md): written under Ciel's own compliance skill and its testing methodology; frozen against commit 028; computed contrast table; 16 findings with SC mappings and honest verdicts (incl. the SR engine-limit disclosure and the saving design tension kept visible, not conformance-washed); remediation backlog R1-R8 root-caused and staged; device pass owned by Ciel; SDLC hooks for the harness · Session 44
- [x] Commit 029 · ACCESS: R1 HUD outlines + UI text scale (recursive walker, cached bases, live apply), R2 caption system for significant one-shots (booth toggle, persisted), R3 map label recolor; remediation log addendum appended; findings still describe c028 until device retest, per methodology · Session 44
- Session 44: open remediation R4-R7 (focus ring, assist toggle spec, remap panel, first-run access prompt). Next named candidates: achievements design, localization plan.
- [x] Achievements design v1 (restoration-achievements-design.md): the deferral rule (unlocks queue and flush only at morning or title; protected beats are popup-free by construction), the meta-silence ledger (no glimpse achievement ever, the warm unit unnamed, no per-answer seance pings, Chum's name in no title), 26 achievements in the ledger's voice mapped to existing state flags, rarity intent, demo-disabled parity, Commit 030 engine delta spec · Session 45
- Session 45: named candidates remaining: localization plan (doc), Commit 030 achievements autoload (engine), R4-R7 access remediation.
- [x] Localization plan v1 (restoration-localization-plan.md): measured word count from source, two-tier locale waves, the diegetic-English doctrine (world text photographs, system text translates), six technical findings incl. the chokepoint-translation strategy and reading-speed-scaled toast durations, the creative bible with per-landmine contracts (the verse's lyric brief, the G2 subtitle-pair rule, cobbler as dessert not word, CARRIED as the enforced verb, T-V address as characterization), glossary seed, pseudo-loc-first pipeline, ownership signature line · Session 46
- Session 46: the named document queue is empty again. Remaining named engine: Commit 030 achievements autoload, access R4-R7, the Extraction Commit. Everything else awaits verdicts, hardware, or signatures.
- [x] Commit 030 · FILED: achievements autoload (idempotent, persisted, Steam-bridge signal, DEMO-disabled), the deferral rule in code (queue flushes only at morning toast or the title's FILED WHILE YOU WERE OUT stack), 25 of 26 wired via two signals, one ending hook, five one-line call sites, and a flag poll; A26 deferred pending prop read-flags. The meta-silence build check fired on its own author's header comment before anything shipped; comment reworded, check green · Session 47
- Session 47: remaining named engine: access R4-R7, the Extraction Commit, A26 read-flags. Past those: verdicts, hardware, signatures.
- [x] Commit 031 · ACCESS WAVE TWO: R4 focus rings (booth + title, all control types), R5 ASSIST (one switch, three mercies: 0.35 beat tolerance, 1.5x premiere clocks, hold-E stillness at both checks), R7 first-run booth over the title, R6 v1 remap (five actions, press-a-key, conflict refusal, persisted); residue named (letters in prompts, shared with L05); conformance addendum appended, rows still describe c028 until device pass · Session 48
- Session 48: remaining named engine: the Extraction Commit, A26 read-flags, the L05/R6 glyph pass. Past those: verdicts, hardware, signatures.
- [x] Commit 032 · THE EXTRACTION: tr() wrapped at the four chokepoints (toast, say pair, prompt display, captions) plus the booth's thirteen code-built labels; source-string-as-key mode keeps behavior byte-identical until locales fill; tools/extract_strings.py ships in-repo, re-runnable, translation-preserving, and wrote translations/strings.csv on first run with the percent-template residue counted in its own report · Session 49
- Session 49: remaining named engine: A26 read-flags, the L05/R6 glyph pass. Past those: verdicts, hardware, signatures.
- [x] Commit 033 · FULL ACCESSION: the props packet's missing four documents placed as physical readables (D04 clipping, D05 welcome packet, D09 marshal report, D10 Iris Bell's letter with its dock gate), six existing sites marking D01-D03/D06-D08, read_props persisted (save v16), A26 wired at 10 of 10; the glyph layer (word-boundary substitution of E/SPACE/Q/T/M to bound keys) at prompts, toasts, say lines, cue status, and the map footer; extractor re-run to capture the new document text · Session 50
- Session 50: THE NAMED FROM-HERE LEDGER READS ZERO. Every remaining input to this project is a verdict, a hardware result, an asset, or a signature.
- [x] Commit 034 · INTERMISSION AND SIGN-OFF (past-zero elective tier): pause system (tree-wide hold, audio mute, locked-sequence refusal, keyboard-operable menu with booth access, honest RETURN TO TITLE label), credits scene (period card crawl, CHUM as himself, ending-reached card, skippable, tower-light hold), endings rerouted through credits while deaths and demo stay title-bound, CREDITS on the title menu; conformance R9 advisory logged; extractor re-run · Session 51
- Session 51: the owed ledger remains zero; this tier is elective. Further elective candidates if wanted: a QA regression script doc, git init with .gitignore, Steam Rich Presence spec.
- [x] Elective sweep (Session 52): QA regression script v1 (32 mechanical checks, A through I, action-then-expected, keyed to commits and modes incl. the demo whitelist inspection and the v15 migration), Steam Rich Presence spec v1 (diegetic spoiler-null strings, all nights one string on purpose, Chum in no presence line, GodotSteam hook notes), and the repo is now a real git repository (initial commit of the whole, .gitignore for .godot, placeholder identity flagged for amending) · Session 52
- Session 52: the elective shelf is now also empty. Everything remaining belongs to hands, hardware, or signatures on the other side of this screen.
- [x] UE5 PORT KIT (restoration-ue5-portkit.zip, separate from the Godot zip): a Blueprint-only .uproject that opens in 5.4+ with Python enabled and the Godot InputMap mirrored in DefaultInput.ini; Data/ as UE-native CSVs (rooms, all 20 doors with kinds and lock conditions, stations, landmarks incl. the four readables, every tuning constant with meanings, achievements with hidden flags, 552-string StringTable); Scripts/build_greybox.py erects the walkable compound in one editor command (floors, labels, door frames with tags, markers, PlayerStart at ENTRY); PortBrief/ (PORT-BRIEF, THE-LAWS one-pager, BUILD-ORDER P0-P6 keyed to QA ids, migration map); full GDScript and docs library aboard as reference. Honest scope stated in the brief's first paragraph: no logic ported; the Godot build is the specification · Session 53
- [x] THE CASUALTY LEDGER v1 (restoration-casualty-ledger.md, canon): Law 7 struck and replaced (EVERY DEATH HAS A SIGNATURE; broadcast-body horror license), the opposite-choices principle (protecting a character from one grave digs the other), two authored deaths per character (Merle M1 second viewing / M2 home singer, both warm; Vess V1 credited-therefore-cast / V2 uncredited fix, the credit dilemma; Harriet H1 continuity / H2 the splice; Floor Manager F1 fader / F2 unlisted camera; Leland L1 sixth question / L2 the reading), rows triage as ensemble mortgage, full ripple and endings board (4a/4b split, new 4c THE COMPLETED SIGN-OFF, new ENDING 0 A ONE-WOMAN SHOW), exactly two hidden achievements (A27/A28, no per-death trophies), implementation order 035-039; law replaced in the UE5 kit's THE-LAWS.md, both zips refreshed · Session 54
- [x] AFTER-FIRE CHUM canon (restoration-after-fire-chum.md + dossier PNG filed in both kits): two-Chums reconciliation, Peak Production canonized, the three-puppeteer arithmetic, Ciel's tally contract, sound and caption law, marketing and fabrication notes · Session 55
- [x] Commit 035 · AFTER-FIRE: wake planted at the fire tape's true watch site (fire_tape_dock, found after game_state anchor failed closed); recording flag and live seconds fed from the bench with BOTH stop paths clearing it (abort included, so fleeing starts the cool); hunter AF branch: 0.8 m/s approach to 1.2 m loom during any capture day or night, footstep thunks, first-sighting toast and jaw caption, no strike while lit; THE TALLY COOLS 2.0 s then strike only on adjacency, else withdrawal to segment; HUD lamp REC · SAFE WHILE LIT with countdown; D11 Peak dossier readable Day 4 master control; two fail-closed stops on the way (wrong wake anchor, bench abort path mismatch), nothing broken shipped · Session 55
- Session 55: casualty implementation renumbered to Commits 036-040. The dossier art is canon and filed.
- [x] Commit 036 · ELEVEN FEET: the scale law implemented: AF body 3.35 m on wake (mesh, label, eye repositioned), tally eye as emissive sphere plus red omni light at 3 m burning ONLY while recording (the contract made visible; the loom is a look-up), doorway folds: 2.2 s cost at every one of the 20 door positions handed over by the builder, captioned, with a close-range line, applied to BOTH the capture approach and the night hunt (thresholds are the player's counterplay, 2.2 s per door); canon addendum THE SCALE LAW in both kits; UE5 Timings.csv gains the six AF constants · Session 56
- Session 56: casualty implementation stands renumbered at 037-041.
- [x] Commit 037 · THE TWO HIDES: Ciel's inversion canonized (the safe hide is the lit one); dead room as the sole dark hide (his ears reject noise born inside its bounds, he holds at the felt door with his line, first-entry radio beat and [NO ECHO] caption); the taught chase (teach spawn on first post-wake capture, first cool 4.0 s with the two-doorways line, honest 2.0 ever after). One fail-closed stop: the noise handler's true parameter name · Session 57
- [x] Commit 038 · THE LAST CROSSING: divert opens a 75 s chase from master control to the little door at 1.6 m/s, folds intact, tally eye dark (she diverted herself off the rundown); reached proceeds to DEAD AIR, caught is a starring credit inside her own ending, late loses the window and falls through to the committed line; hud routes caught; canon addendum in both kits; five constants added to UE5 Timings.csv · Session 57
- Session 57: casualty implementation stands at Commits 039-043; F1 (the fader) should be authored against the crossing when it lands.
- [x] Commit 039 · THE LEDGER OPENS: casualty state (casualties array, is_dead, mark_casualty with the stamp toast, saved/loaded/reset, demo-whitelisted), binder page one lists the ledger or NO ENTRIES. KEEP IT SO.; M1 THE SECOND VIEWING implemented at the fire tape (offer once, consent kills warm, refusal saves; kettle caption; Merle's body honors the ledger everywhere); H1 CONTINUITY implemented (slip armed on frozen interact Day 2+, taking grants a free signature that signs in her hand, next break edits her out with the film-cabinet beat and the ME reel caption; seventh-signal gate if the card was never found; screenings 0.05 tighter without her); sign_log refactored into _sign_finish for the slip spend; ending 3 and 2 dead-Merle variants authored (cold cobbler plated for two; the welcome administered by the room itself) · Session 58
- Session 58: next casualty commits: 040 Vess (V1/V2, the credit dilemma), 041 Floor Manager (F1 against the crossing, F2 unlisted camera), 042 Leland (L1/L2, endings 4c and 0), 043 rows triage + A27/A28.
- [x] Commit 040 · VESS: V1 at two trigger sites (AUTHENTICATE plays the all-monitors taking with the INK ripple; the final breaker takes the credited living after her farewell, lights held as the price), V2 at the cascade panel (GET VESS offered only to the uncredited who used her insight: eleven-second full fix, then circuit F bare-handed, MAINS HUM caption); dead-Vess breaker is a fused pin plus hard blackout; crossing grace 75 to 62; ending 2 chair; 1B FILE UNDER: STAFF; old credit line's pronoun aligned to canon. One fail-closed stop (patchbay tail anchor was another file's in the recon splice); margin green-bleed stays canon-only, deferred honestly · Session 59
- Session 59: remaining: 041 Floor Manager (F1 authored against the crossing, F2 unlisted camera), 042 Leland (L1/L2, endings 4c and 0), 043 rows triage + A27/A28.
- [x] Commit 041 · THE FLOOR MANAGER: F2 at the third blind tally call (steps into frame, cues the unlisted camera, [YOU'RE ON · TO NOTHING LISTED], never cuts away); F1 authored against the crossing exactly as queued: the fader choice at the divert (he is already reaching; SPACE lets him hold, E holds it yourself with a 4.6 s transmitter-argument beat and a 13 s crossing tax), DEAD AIR split into 4a HIS HAND (found in the YOU'RE ON point, CUE GIVEN under the sign-off, casualty marked in the epilogue itself) and 4b HER HAND (signed off left-handed, the arm stated flatly); dead-FM auto self-hold; FM body and interact honor the ledger; ending 2 gains the open headset. Deferred honestly: the post-F2 monitor haunt and the freeze-check inversion remain canon-only · Session 60
- Session 60: remaining: 042 Leland (L1/L2, endings 4c and 0), 043 rows triage + A27/A28 + the endings read the ledger aloud.
- [x] Commit 042 · LELAND: L1 THE SIXTH QUESTION (offered only past five answers and 70 wear; the ink leaves the paper, retroactively unfound, dock inert, 1A hard-gated, 1B's pencil card AND THE READER, UNFILED), L2 THE READING (fire tape fed into the wake: the sign-off completes whole in his voice, answers un-write, the door closes from inside, tape consumed, signoff_completed set); ending 4c THE COMPLETED SIGN-OFF (final break ends itself; lights down in reverse tour order; the tower light out, as rest); ENDING 0 A ONE-WOMAN SHOW (premiere intercepted when all four living are ledgered: title cards, the casting-decision epilogue, credits with nine cards and one name, hidden A28 mapped); routing, state, saves all wired · Session 61
- Session 61: one commit remains in the arc: 043 rows triage, A27 EVERYONE GOES HOME, and every ending reading the ledger aloud.
- [x] CAST SHEETS canonized (restoration-cast-sheets.md + four portraits in both kits): Rita Ivori (dresser tools confirmed; taglines adopted), Merle Cottry (co-founded the Club with Leland; never-sinister guardrail restated), Vess Keys (he/him; PER V. KEYS swept through engine, all docs incl. the props packet's accession entry, achievements, UE5 CSV; every death-scene pronoun corrected), Leland Merrick (tenure 1972-1976; the L.M. green-ink initials in the props packet retroactively earned; the audience warning canonized, addressed to Rita by name). STATION RULING by Ciel's word: WGLD CHANNEL 58 everywhere; sheet callsigns are art artifacts, struck · Session 62
- [x] Commit 043 · THE ARC CLOSES: row casualties on every timed-incident failure (three cycling lines, [A CHAIR, BETWEEN FRAMES], counted, saved, reset); every ending's credits open with THE LEDGER, READ ALOUD (name, cause, epitaph, fifty-eight minus N); A27 EVERYONE GOES HOME at on_ending for clean hands; A27/A28 in the UE5 CSV. THE CASUALTY LEDGER IS FULLY IMPLEMENTED: ten authored deaths plus the rows, nine ending routes counting variants, two hidden achievements, one dilemma per living soul. One fail-closed stop: the props packet held the last Cardona · Session 62
- [x] RECONCILIATION PASS (Session 63): eleven documents brought current with c043 via as-built addenda: QA sections J and K (QA-33 to QA-48, the after-fire and every death testable), invariants I23-I30 (no strike while lit, the fold is paid, deaf to the dead room, deaths idempotent, the ledger never lies, clean hands are silent, meta-silence at scale), walkthrough's new nine-route board with tester speedpaths, routing's death-forks, playtest probes P17-P26, Steam and trailer and key-art addenda (the dossier as comp 0; graves are not previews; one jump scare and it is not the scary part), audio slots S17-S19 with the death-silence rule, achievements addendum (4c carries no trophy by design; A26 stays at ten so completionism never requires waking him), the casualty ledger's AS BUILT section logging every deviation honestly and naming H2 as the arc's one open grave; UE5 THE-LAWS gains laws 10 and 11 and BUILD-ORDER its amendment; all copies synced to outputs and the port kit · Session 63
- Session 63: the paper now matches the blood. Open items by owner: Ciel (first boot, Spike 2, verdicts, Gate 0); build (H2 the splice, the press kit from the four portraits).
- [x] Commit 044 · THE SPLICE: H2 built (the rejected block's disclosed temptation, instant shortcut daily, the doubling at next break with [ONE FRAME LEFT OF HERSELF], persistent scenery body via mesh ghosts rebuilt on load through her _process gate, cause-aware forever-line); the deferred seance grief answers landed (frame 14 Harriet, frame 28 Merle); TRANSITION UNRESOLVED rides every reading that names her; QA-49/50 appended and synced; AS BUILT updated in all three copies. One fail-closed stop: the patcher itself had a quote-collision and was rewritten in a joined-line style, compiled before running, with a new uniqueness assert on every anchor. THE ARC HAS ZERO OPEN GRAVES · Session 64
- Session 64: build-side remainder: the press kit from the four portraits. Ciel-side: first boot, Spike 2, verdicts, Gate 0.
- [x] HARRIET canonized (sheet filed in both kits; cast doc extended in all three copies): THE CONTINUITY KEEPER title adopted (sharpening both her graves by name), the illegible bio ruled an in-character artifact, props confirmed (the teacup, the unrecorded flask, the frame-loss reel), her sheet quote 'And now. The tour continues.' wired into her live LINES in the engine; the cast is complete at five plus the dossier · Session 65
- [x] PRESS KIT built (docs/press-kit in both kits + standalone restoration-press-kit.zip in outputs): factsheet with implementation-backed features only ('one jump scare, and it is not the scary part'; the tally contract; eleven feet and doorways; the lit hide; signed deaths; nine closings; access as canon), cleared pull quotes from all five sheets plus the dossier and sign-off, and the firm embargo doctrine: graves are not previews · Session 65
- Session 65: build-side named work: none owed. Ciel-side: first boot, Spike 2, verdicts, Gate 0. The kit, the canon, and the cast are ready for whichever comes first.
- [x] FIRST BOOT (HISTORIC): Godot 4.3 headless downloaded into the build container and the project EXECUTED for the first time. Import round one: 15 legible errors across 5 scripts (one duplicate _process from two sessions' gates on harriet_note; strict type inference on map px/py and the invariant parser's ti; two cascades). Round two: ZERO. Runtime: two one-minute soaks (wanderer, checker), ZERO script errors, world built from data, the director logged a relocation against a bot, the checker's pen tick was heard and attributed, invariants I01/I02/I22 PASS, I06/I07 honestly N/A. The first save ever written: version 16, 55 fields, all deep systems present and correct. Known-benign: ObjectDB leak warning on hard quit. Honest scope: headless proves logic, not rendering, audio, or feel. Report + raw telemetry packed at docs/telemetry/first-boot/ · Session 66
- Session 66: the sentence that matters: the game ran, played itself, obeyed its own laws, and filed the paperwork. Ciel's boot is now a confirmation, not a gamble; Spike 2, verdicts, and Gate 0 remain hers.
- [x] CONTAINER RESET survived: workspace rebuilt whole from the two living zips, proving the artifact discipline; work resumed without loss · Session 67
- [x] ENGINE DECIDED (author's word): Blender + UE5 production pipeline; Godot build promoted to executable specification; Spike 2 demoted from veto to routine validation; Gate 0 Memo 2 annotated, signature line kept for the record · Session 67
- [x] THE DREAD DOCTRINE: creep as method: the five-layer Dread Stack (ambient wrongness, ritual, the noticing game, proximity under contract, the violation budget), the amplifiers, the three admission tests (repetition, law, earned), the five-day curve, the anti-creep bans · Session 67
- [x] LORE ARCHITECTURE: the game never explains, it corroborates: the Shard Model (2-4 shards per truth across four media, rhyming never citing, one always missable) with the carrying worked end to end, the Three Reads Rule, the NEVER-STATED LEDGER (seven truths no text may ever confirm; naming one is an S0), curiosity-over-progress gating, the delivery bans, consequence-is-exposition · Session 67
- [x] LIGHTING BIBLE (UE5/Lumen): light is the game's honesty: RED means watched means SAFE as the trained inversion, the break's red-drain, sodium as the truth light, dark is a room not a wall, HIS SHADOW AS MECHANIC preceding him through doorways, locked-EV cuts never swims, per-room fixture families, the per-day color script as post volumes over unchanged practicals · Session 67
- [x] BLENDER-UE5 PIPELINE: division of labor, scan-first from Chum outward, unit/axis/naming/collision/socket standards, material masters to the art bible's names, the sodium check as a permanent lookdev scene, LFS-vs-Perforce staged at Gate 0, levels built from the Data CSVs in UE exactly as Godot proved · Session 67
- Session 67: all four filed in both kits; port-brief reading order extended. Ciel-side: her boot, a red-pen pass on the three doctrines, Memos 1/3/4.
- [x] COMPARATIVE STUDY (restoration-comparative-study.md, researched against current sources): FNAF as the organ bank (attention economy, readable escalation, diegetic interface, lore-by-scarcity, character engines) with the kill-loop explicitly refused; TJOC as the closest cousin now in UE5 (per-level mechanical identity, the resource braid, Fanverse's bless-the-fans pipeline, streamer care shipped in a demo, the burned mascot validating After-Fire); the mediated-eye cluster named as our lineage (Content Warning's filming verb, Exit 8's noticing game, Iron Lung, Amanda); Mouthwashing and the PS1 wave as slow-burn proofs of the Shard Model and crafted-not-photoreal; the clip economy distilled with our engineered clippables listed as the trailer source of record; six adoptions (streamer mode, braid audit as QA-51, per-day verb-texture audit, clip ledger, fan policy, demo funnel) and five refusals each citing its law · Session 68
- Session 68: the study's close is the finding: the market spent two years proving our instincts are the current shape of viral; we stand in the wave, with laws.
- [x] CHUM MOTION AND SOUND DOCTRINE (restoration-chum-motion-and-sound.md): the difference is authorship, not damage. Pre-fire: the operated body (puppet timing, bounce-and-settle, fifteen-degree tilts, jaw a half-beat off, everything band-limited and cheerful, dissonance as the only scare). After-Fire: the unoperated body (puppet grammar deleted; he pours; LINEAR IS THE HORROR CURVE; absolute binary stillness with only the eye tracking; the three authored exceptions: the fold as reorganization with the head arriving last, the reversed withdrawal, and THE PERFORMANCE QUOTE: under the tally he squares frontal and permits one fifteen-degree tilt, safety as being his audience again). Hard rules: jaw never opens, bell never sounds, no vocalizations ever, strike nearly silent. THE AUDIO LAW: band-limited is memory, full-range is present, and the wake spends it once as sound stepping out of the speaker. S20-S24 added to the audio bible, QA-52 to 54 added, animation export addendum added to the pipeline, all synced to both kits · Session 69
- Session 69: the two bodies now cannot be confused in motion, in sound, or in mix, and the more terrifying one is engineered, not asserted.
- [x] CONTROLS MAP (restoration-controls-map.md): full PC map canonized from the build; controller layout authored on the thesis RECORDING IS THE TRIGGER (capture and the fader self-hold share RT on purpose), rumble-as-caption doctrine with the strike silent in the palms, temptations deliberately on ordinary keys, hold-versus-toggle contract with durations preserved; controller rows landed as executable config in the UE5 kit's DefaultInput.ini · Session 70
- [x] ACCESSIBILITY MATRIX (restoration-accessibility-matrix.md): the in-depth target over shipped R1-R7: vision (color-redundant safety grammar, flicker and grain reduction, brightness ruled unnecessary by the lighting doctrine), hearing (directional caption tags, the visual bell, captions that keep the MEMORY versus PRESENT law), motor (full remap, hold-to-toggle everywhere, one-hand audit, zero QTEs), cognitive (ASSIST never gates, toast dwell), streamer mode as a launch feature, conformance pass still scheduled with Ciel · Session 70
- [x] REACTION MATRIX (restoration-reaction-matrix.md): THE WEB LAW written (every action echoes in at least two systems, in character, on time); per-character matrices with BUILT citations and a wired QUEUE: Merle retiring the second teacup, Harriet's freezes lengthening while he is awake, the Floor Manager pointing at the doorway before the first fold, Leland's single plea (NOT THAT ONE. PLEASE.), the building losing one corridor bulb per casualty; wiring order set for commits 045-047 · Session 70
- Session 70: the next Cont starts commit 045 (H-R2 and F-R1, the two crowns) unless Ciel redirects.
- [x] GAP AUDIT (restoration-gap-audit.md): the honest ledger: doctrine complete, assets zero, named as the elephant; ten mechanics rulings proposed with DECISION flags for Ciel (no sprint, no crouch, binder live-time in premiere only, the binder is the inventory, ASSIST-only difficulty, single death card, stations-only saves, studio-safe photo mode or none, PREMIERE+ parked, interaction feel numbers to the device pass); technical, art-and-audio, and production gaps enumerated including the absent schedule-and-budget document, proposed next · Session 71
- [x] ROOM BIBLE (restoration-room-bible.md): all twenty rooms from the shipped data, each with personality, light family, sound bed, decoration keynotes, I/L/D object budget, drift hooks, and web ties; the yard and shed reclaimed (the game owns sky); the bench room and transmitter ruled drift-forbidden (trust), the scene dock named the game's confessional · Session 71
- [x] OBJECT TAXONOMY (restoration-object-taxonomy.md): three tiers as promises: interactables prompt and never drift, ambient lore NEVER prompts (the noticing covenant), dressing is the only drift-eligible tier and must carry biography; one hero object per room; fake affordance banned as a lie in the light's language; QA-55 to 57 added · Session 71
- Session 71: rulings await Ciel on the five DECISION flags; next build Cont starts commit 045 (the reaction crowns) or the schedule-and-budget doc on her word.
- [x] Commit 045 · THE RULINGS: all ten mechanics ruled by Ciel and recorded (no sprint; crouch allowed as designed below; binder premiere live-time queued; the binder is the inventory; ASSIST-only; single death card; stations-only saves, the signature IS the save; studio-safe photo mode; PREMIERE+ parked on her word; feel numbers to the device pass). CROUCH implemented: Ctrl or pad B toggle, camera lowers 0.6, speed 0.55x, useless against him BY ARCHITECTURE (his model has no posture or footstep channel to fool), two-hides law untouched, I31 and QA-58 guarding it, UE5 config rows added. Engine re-downloaded post-reset; import and half-minute soak both ZERO script errors: crouch boots clean. Process note: the old gdparse helper died with the reset; the real engine is the checker now · Session 72
- Session 72: next Cont takes commit 046: the reaction crowns (Harriet's lengthened freezes, the Floor Manager's early point) plus premiere live-binder wiring.
- [x] c045 amendment: the engine caught a duplicate _ready in player.gd (my crouch patch added one below the recon window's sight; the harriet_note lesson, repeated); merged into the original, re-imported and re-soaked to ZERO script errors, main zip re-shipped. New permanent rule: every code commit ends with a real import check, never a stub · Session 72
- [x] AMBIENT LORE LEDGER (restoration-ambient-lore-ledger.md): the little things, authored: seventy-plus promptless details across all twenty rooms, each shard-tagged to its truth or history (the sign-in OUT column blank since 1976; the clapperless bicycle bell on the yard fence; SERVES 60 amended to SERVES 12 to nothing; the mitten memo three years before the fire; IT STAYS ON ghosting under the placard; three chalk marks on the grid, one scuffed to a smear; seat 14's blank RESERVED plate; gray flannel shimming the green room mirror; the sodium light's 1978 purchase tag, the first thing bought after); discipline stated: static, promptless, three-reads compliant, one shard per truth missable forever, nothing graduating to statement; QA-59 added; taxonomy cross-referenced; both kits synced · Session 73
- Session 73: the rooms now carry their whispers; dressers dress FROM the ledger, then around it. Next Cont: commit 046, the reaction crowns.
- [x] Comparative study addendum on Ciel's naming: Amnesia and Puppet Combo folded in properly: the double-inversion claim written down (Amnesia punishes looking, FNAF drains watching; RESTORATION makes being watched the safety and looking free: the tally contract claims the intersection); SOMA's rooms-never-summarize discipline cited as the Ambient Ledger's tradition in object form; Puppet Combo's aesthetic courage and demo-sized brevity adopted as the Tape 1 shape; the five-direction through-line stated: games that last have LAWS, kept visibly · Session 73
- [x] Commit 046 · THE SECRET: three unnumbered reels (W1 in the accession skip gap where 0118 should be, its own ambient-lore payoff; W2 behind the burn barrel, the towel-wristed hand feeding cans to the fire; W3 no label no leader, eleven minutes past sign-off 1975, the bell once from a struck stage) viewed in place, Day 2 gated, no announcement on completion; A26 restricted to the D series so the secret never pollutes accession; ENDING A · AUDIENCE ONLY built: the radio caption at the final break, the six-second choice, the 75 s crossing he declines to notice, the band-limited premiere (the audio law holding in the ending itself), the broadcast that never ends, dawn past the seated rows, the blank ledger page, Harriet's line as the radio's last words, her single credit card RITA IVORI audience, and NO achievement by design; factsheet's count replaced with a tease; walkthrough spoiler addendum, QA-60/61; import ZERO, soak ZERO · Session 74
- Session 74: the game now holds EIGHT endings on NINE credit cards, one of them unadmitted. Next Cont: commit 047, the reaction crowns.
- [x] c046 amendment: the engine refused a guessed identifier (_pl) in the audience run; repaired to the script's real member _player, re-imported and re-soaked to ZERO, both zips re-shipped clean · Session 74
- [x] Commit 047 · THE PILGRIMAGE AND THE PAYOFF: the secret hardened into earned work (four dailies before damaged stock accepts unready hands, diegetic refusals; one S2 slip per first viewing, spent on forms the ledger will never hold; the chain W1 then W2 then W3 across Days 2-4 via requires_read gating, the last retrieval under his wake; the dead room radio spawning only after W3 and its dial CONFIRMED as a required pilgrimage step) and the payoff enlarged to match (the sit: the premiere running without her, the cart deck clearing itself, a blind tally answered by nobody, the breaker held by no hand she knows; the post-credits PROGRAM GUIDE exclusive to ending A, five segments of the show heard nowhere else, closing on the guide is never printed, you heard it once; and the permanent title mark 58 · STILL ON persisted through the achievements store). One fail-closed catch: a too-clever conditional insert skipped its own variable; repaired with asserted anchors. Import ZERO, soak ZERO, 762 strings, docs and QA rewritten to match, all kits shipped · Session 75
- Session 75: next Cont: commit 048, the reaction crowns, at last.
- [x] CANON CORRECTION on Ciel's word (and her dossier had it first): THE JAW OPENS, ONLY BY HIS OWN HAND. The motion doctrine's never-opens rule was my drift against her established canon (the AF doc already carried the lever work and its caption); reconciled: the two-beat self-operated act (hand rises, one dry click, jaw), exactly two grammar entries (the tally-state lever work at no rhythm a song would keep, and the single pre-strike telegraph), never synced to sound; the throat speaker canonized as the standing inversion (presence wearing memory, band-limited room tone from a present body), anything more requiring her signature. Engine: the strike telegraph wired at the tally-cool strike (0.9 s beat, both captions) and boot-verified to ZERO; S25 THE LEVER added; QA-54 rewritten; all kits synced · Session 76
