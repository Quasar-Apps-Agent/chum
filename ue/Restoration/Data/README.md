# RESTORATION · Data/ — the port kit's data deliverable
GENERATED — do not hand-edit. Rebuild with `python3 tools/extract_port_data.py`
(unit 0.5). Transcribed from the reference Godot implementation, which is the
specification; where this dir and the GDScript disagree, THE CODE IS THE INTENT
— fix the generator, never the CSV. Units: Godot meters, plan view (X east,
Z south, Y up); UE conversion is 1 m = 100 uu per the pipeline doc.

- **Rooms.csv** — the twenty zones: name, center X/Z, width (size_x), depth
  (size_z). Source: `ROOMS` in world_builder.gd.
- **Doors.csv** — wall openings: paired rooms, gap center X/Z, opening width,
  wall axis, kind (open gap / door / window / locked), locked reason as world
  text, required key id. Source: `DOORS` in world_builder.gd.
- **Stations.csv** — the five transmitter-log stations (id, display name,
  position). The station body sits +0.55 m above this floor point (code).
  Source: `STATIONS` in world_builder.gd.
- **Landmarks.csv** — interactables and named set pieces with literal spawn
  positions, incl. the readable documents (doc_id) and key items (key_id);
  `room` is derived by point-in-room lookup. Spawns whose positions are
  computed in loops (dock Chum units, felt runs, shelf ranks) stay in code.
  Source: the spawn functions of world_builder.gd.
- **Timings.csv** — every numeric `const` across scripts/*.gd with its source
  line and comment. Tunables written as inline literals (e.g. the 75 s / 62 s
  crossing window, live_production.gd) remain in the reference scripts.
- **GameText.csv** — Key,SourceString for a UE StringTable, source-string-as-
  key mode, from translations/strings.csv (tools/extract_strings.py output).

The `.gdignore` here keeps the Godot reference build's importer from eating
these CSVs as translation files.
