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
