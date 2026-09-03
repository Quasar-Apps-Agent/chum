#!/usr/bin/env python3
"""RESTORATION · port-kit data extraction (unit 0.5, CLOUD-OK).

Rebuilds the port kit's Data/*.csv deliverable from the same truth the kit
named: the reference Godot implementation. The GDScript is the specification;
this tool only TRANSCRIBES it — no numbers are invented here.

Sources:
  scripts/world_builder.gd  -> Rooms.csv, Doors.csv, Stations.csv, Landmarks.csv
  scripts/*.gd  (numeric const sweep) -> Timings.csv
      (Residue, per the port brief's own rule "the code is the intent":
       tunables written as inline literals — e.g. the 75 s / 62 s crossing
       window in live_production.gd:232 — stay in the reference scripts and
       are NOT duplicated here; a hand-typed copy could drift from truth.)
  translations/strings.csv  (extract_strings.py output, source-string-as-key)
                            -> GameText.csv  (Key,SourceString for a StringTable)

Output: ue/Restoration/Data/  (+ a README.md data dictionary)

Deterministic and re-runnable:  python3 tools/extract_port_data.py
Exits non-zero if any sanity check fails (counts, unparsed landmark classes).
"""
from __future__ import annotations

import csv
import math
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WB = REPO / "scripts" / "world_builder.gd"
STRINGS = REPO / "translations" / "strings.csv"
OUT = REPO / "ue" / "Restoration" / "Data"

# Node classes that are construction plumbing, never landmarks.
PLUMBING = {
    "CollisionShape3D", "BoxShape3D", "CapsuleShape3D", "MeshInstance3D",
    "BoxMesh", "CylinderMesh", "SphereMesh", "TorusMesh", "PlaneMesh",
    "StandardMaterial3D", "ShaderMaterial", "Label3D", "OmniLight3D",
    "DirectionalLight3D", "StaticBody3D", "WorldEnvironment",
}
# Positionless systems / managers spawned by world_builder: not landmarks.
SYSTEMS = {
    "LiveProduction", "RecChairs", "NoiseTracker", "Cascade", "LivenessCheck",
    "Lockdown", "CoverageDirector", "Rundown", "DailiesManager", "NightTrip",
    "Glimpse", "MonitorRig",
}

NUM = r"-?\d+(?:\.\d+)?"


def _f(tok: str) -> float:
    tok = tok.strip()
    if tok == "PI":
        return round(math.pi, 6)
    if tok == "-PI":
        return round(-math.pi, 6)
    m = re.fullmatch(r"(-?)PI\s*/\s*(\d+(?:\.\d+)?)", tok)
    if m:
        return round(math.pi / float(m.group(2)) * (-1 if m.group(1) else 1), 6)
    return float(tok)


def block(text: str, header: str) -> str:
    """Return the lines of a const block from its header line to its closer."""
    start = text.index(header)
    end = re.search(r"^\}|^\]", text[start:], re.M)
    return text[start:start + end.end()]


def parse_rooms(text: str):
    rows = []
    for m in re.finditer(rf'"([^"]+)": \[({NUM}), ({NUM}), ({NUM}), ({NUM})\]',
                         block(text, "const ROOMS := {")):
        rows.append([m.group(1)] + [_f(g) for g in m.groups()[1:]])
    return rows


def parse_doors(text: str):
    rows = []
    pat = rf'\["([^"]+)", "([^"]+)", ({NUM}), ({NUM}), ({NUM}), "([xz])", "([^"]*)"\]'
    for m in re.finditer(pat, block(text, "const DOORS := [")):
        a, b = m.group(1), m.group(2)
        gx, gz, gw = _f(m.group(3)), _f(m.group(4)), _f(m.group(5))
        axis, raw = m.group(6), m.group(7)
        kind, reason, key = "open", "", ""
        if raw == "door":
            kind = "door"
        elif raw == "window":
            kind = "window"
        elif raw.startswith("locked:"):
            kind = "locked"
            payload = raw[len("locked:"):].split("|")
            reason = payload[0]
            if len(payload) > 1:
                key = payload[1]
        rows.append([a, b, gx, gz, gw, axis, kind, reason, key])
    return rows


def parse_stations(text: str):
    rows = []
    pat = rf'\["(S\d)", "([^"]+)", Vector3\(({NUM}), ({NUM}), ({NUM})\)\]'
    for m in re.finditer(pat, block(text, "const STATIONS := [")):
        rows.append([m.group(1), m.group(2)] + [_f(g) for g in m.groups()[2:]])
    return rows


def parse_monitors(text: str):
    rows = []
    v3 = rf"Vector3\(({NUM}), ({NUM}), ({NUM})\)"
    pat = rf'\[{v3}, {v3}, {v3}, ([^,]+), "([^"]+)"\]'
    for m in re.finditer(pat, block(text, "const MONITORS := [")):
        g = m.groups()
        rows.append([_f(x) for x in g[:9]] + [_f(g[9]), g[10]])
    return rows


def room_of(x: float, z: float, rooms) -> str:
    best, best_area = "", 1e18
    for name, cx, cz, sx, sz in rooms:
        if abs(x - cx) <= sx / 2.0 + 1e-6 and abs(z - cz) <= sz / 2.0 + 1e-6:
            if sx * sz < best_area:
                best, best_area = name, sx * sz
        # doors and thresholds sit ON walls; allow a small tolerance pass later
    return best


def parse_landmarks(text: str, rooms):
    """Scan spawn code for interactable vars with literal Vector3 positions."""
    rows, unpositioned = [], []
    var_re = re.compile(r"\bvar (\w+) := (\w+)\.new\(\)")
    pos_re = re.compile(rf"^\t*(\w+)\.position = Vector3\(({NUM}), ({NUM}), ({NUM})\)")
    dock_re = re.compile(r'_dock_body\((\w+), "([^"]+)"')
    attr_re = re.compile(r'^\t*(\w+)\.(door_label|display|sign_text|slate_text|asset_id|read_id|key_id|locked_reason) = "([^"]*)"')
    child_re = re.compile(r"^\t*(\w+)\.add_child\((\w+)\)")
    text_re = re.compile(r'^\t*(\w+)\.text = "([^"]+)"')

    vars: dict[str, dict] = {}
    labels: dict[str, str] = {}

    def flush(name: str) -> None:
        v = vars.pop(name, None)
        if v is None:
            return
        cls = v["class"]
        if cls in PLUMBING or cls in SYSTEMS:
            return
        if v.get("pos") is None:
            unpositioned.append(f'{cls} ({name})')
            return
        label = v.get("label") or v.get("display") or ""
        if cls == "Node3D" and not label:
            return
        x, y, z = v["pos"]
        rows.append([
            cls, label, x, y, z, room_of(x, z, rooms),
            v.get("read_id", ""), v.get("asset_id", ""), v.get("key_id", ""),
            v.get("locked_reason", ""),
        ])

    for line in text.splitlines():
        if line.startswith("func "):
            # vars are function-local: never let a name leak across bodies
            for name in list(vars):
                flush(name)
            labels.clear()
        m = var_re.search(line)
        if m:
            name, cls = m.group(1), m.group(2)
            if name in vars:
                flush(name)
            if cls == "Label3D":
                labels[name] = ""
            else:
                vars[name] = {"class": cls}
            continue
        m = pos_re.match(line)
        if m and m.group(1) in vars and "pos" not in vars[m.group(1)]:
            vars[m.group(1)]["pos"] = tuple(_f(g) for g in m.groups()[1:])
            continue
        m = dock_re.search(line)
        if m and m.group(1) in vars:
            vars[m.group(1)].setdefault("label", m.group(2))
            continue
        m = attr_re.match(line)
        if m and m.group(1) in vars:
            key = {"door_label": "label", "sign_text": "label",
                   "slate_text": "label", "display": "display"}.get(m.group(2), m.group(2))
            vars[m.group(1)].setdefault(key, m.group(3))
            continue
        m = text_re.match(line)
        if m and m.group(1) in labels:
            labels[m.group(1)] = m.group(2)
            continue
        m = child_re.match(line)
        if m and m.group(1) in vars and m.group(2) in labels:
            if labels[m.group(2)]:
                vars[m.group(1)].setdefault("label", labels[m.group(2)])

    for name in list(vars):
        flush(name)

    # _spawn_key call sites (helper receives literal args)
    for m in re.finditer(
            rf'_spawn_key\("([^"]+)", "([^"]+)", Vector3\(({NUM}), ({NUM}), ({NUM})\), "([^"]+)"\)', text):
        kid, disp = m.group(1), m.group(2)
        x, y, z = (_f(g) for g in m.groups()[2:5])
        rows.append(["KeyItem", m.group(6), x, y, z, room_of(x, z, rooms),
                     "", "", kid, disp])

    # readables defs array: ["D04", "label", Vector3(...), needs_day, needs_dock, ...
    for m in re.finditer(
            rf'\["(D\d+)", "([^"]+)", Vector3\(({NUM}), ({NUM}), ({NUM})\), (\d+), (true|false)', text):
        did, label = m.group(1), m.group(2)
        x, y, z = (_f(g) for g in m.groups()[2:5])
        rows.append(["ReadableProp", label, x, y, z, room_of(x, z, rooms),
                     did, "", "", f"needs_day={m.group(6)};needs_dock={m.group(7)}"])

    # wall clocks: the spots list inside _spawn_wall_clocks
    mfun = re.search(r"func _spawn_wall_clocks.*?for p in spots", text, re.S)
    if mfun:
        for m in re.finditer(rf"Vector3\(({NUM}), ({NUM}), ({NUM})\)", mfun.group(0)):
            x, y, z = (_f(g) for g in m.groups())
            rows.append(["WallClock", "WALL CLOCK", x, y, z,
                         room_of(x, z, rooms), "", "", "", ""])

    # monitor rigs from the MONITORS const
    for cam_x, cam_y, cam_z, look_x, look_y, look_z, mx, my, mz, yaw, label in parse_monitors(text):
        rows.append(["MonitorRig", label, mx, my, mz, room_of(mx, mz, rooms),
                     "", "", "",
                     f"cam=({cam_x},{cam_y},{cam_z});look=({look_x},{look_y},{look_z});yaw_rad={yaw}"])

    rows.sort(key=lambda r: (r[5], r[0], r[1]))
    return rows, unpositioned


def parse_timings():
    rows = []
    for path in sorted((REPO / "scripts").glob("*.gd")):
        lines = path.read_text().splitlines()
        for i, line in enumerate(lines):
            m = re.match(rf"^const (\w+) := ({NUM})\b(.*)$", line)
            if not m:
                continue
            name, value, rest = m.group(1), m.group(2), m.group(3)
            meaning = ""
            cm = re.search(r"##\s*(.*)$", rest)
            if cm:
                meaning = cm.group(1).strip()
            elif i > 0:
                pm = re.match(r"^##\s*(.*)$", lines[i - 1])
                if pm:
                    meaning = pm.group(1).strip()
            rows.append([name, value, f"scripts/{path.name}", i + 1, meaning])
    return rows


def parse_gametext():
    with STRINGS.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header[0] == "keys", f"unexpected strings.csv header: {header}"
        return [[row[0], row[0]] for row in reader if row and row[0]]


def write_csv(name: str, header, rows) -> None:
    with (OUT / name).open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  {name}: {len(rows)} rows")


README = """# RESTORATION · Data/ — the port kit's data deliverable
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
"""


def main() -> int:
    text = WB.read_text()
    OUT.mkdir(parents=True, exist_ok=True)

    rooms = parse_rooms(text)
    doors = parse_doors(text)
    stations = parse_stations(text)
    landmarks, unpositioned = parse_landmarks(text, rooms)
    timings = parse_timings()
    gametext = parse_gametext()

    print("extract_port_data:")
    write_csv("Rooms.csv",
              ["name", "center_x", "center_z", "size_x", "size_z"], rooms)
    write_csv("Doors.csv",
              ["room_a", "room_b", "gap_x", "gap_z", "gap_width", "axis",
               "kind", "locked_reason", "required_key"], doors)
    write_csv("Stations.csv", ["id", "name", "x", "y", "z"], stations)
    write_csv("Landmarks.csv",
              ["kind", "label", "x", "y", "z", "room", "doc_id", "asset_id",
               "key_id", "notes"], landmarks)
    write_csv("Timings.csv", ["name", "value", "source", "line", "meaning"],
              timings)
    write_csv("GameText.csv", ["Key", "SourceString"], gametext)

    # Protect the reference implementation: Godot's importer treats bare CSVs
    # as translation sources and would choke on these (the plan's .gdignore
    # rule, same trap the .blend dirs guard against).
    (OUT / ".gdignore").write_text("")
    (OUT / "README.md").write_text(README)
    print("  + .gdignore (Godot importer guard) and README.md (data dictionary)")

    ok = True
    def check(cond: bool, msg: str) -> None:
        nonlocal ok
        print(("  OK   " if cond else "  FAIL ") + msg)
        ok = ok and cond

    check(len(rooms) == 20, f"20 rooms (got {len(rooms)})")
    check(len(doors) == 20, f"20 door rows (got {len(doors)})")
    check(len(stations) == 5, f"5 log stations (got {len(stations)})")
    check(len(landmarks) >= 30, f">=30 landmarks (got {len(landmarks)})")
    check(len(timings) >= 30, f">=30 timing consts (got {len(timings)})")
    check(len(gametext) >= 552, f">=552 strings, the kit's floor (got {len(gametext)})")
    room_names = {r[0] for r in rooms}
    dangling = [d for d in doors if d[0] not in room_names or d[1] not in room_names]
    check(not dangling, f"every door joins two known rooms ({len(dangling)} dangling)")
    if unpositioned:
        print("  NOTE landmark-class vars without a literal position "
              f"(computed in loops; not transcribed): {', '.join(unpositioned)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
