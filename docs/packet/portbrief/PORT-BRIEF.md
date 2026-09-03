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
