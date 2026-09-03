#!/usr/bin/env python3
"""RESTORATION port-kit data extractor (unit 0.5).

Rebuilds the port kit's Data/*.csv deliverable from the reference
implementation — the same truth the kit names. THE CODE IS THE INTENT
(PORT-BRIEF.md): nothing here is hand-typed world data; every row is
parsed out of the GDScript at generation time, so re-running after a
scripts/ change refreshes the data and drift is impossible.

Outputs (docs/packet/portbrief/Data/, schemas per PORT-BRIEF.md §Data):
  Rooms.csv      name, center X/Z (Godot meters, plan view), width, depth
  Doors.csv      paired rooms, position, opening width, wall axis, kind
  Stations.csv   the five log stations
  Landmarks.csv  interactables incl. the readable documents (room derived
                 from the ROOMS rects; DEMO-gated spawns flagged)
  Timings.csv    every number that tunes the game, with meanings
  GameText.csv   Key,SourceString for a UE StringTable (source-as-key)

Deterministic: same scripts in, byte-identical CSVs out. Self-checking:
curated Timings rows are asserted against the source before they are
emitted, and basic invariants (20 rooms, 20 doors, 5 stations) are
enforced at the end.
"""
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
OUT_DIR = os.path.join(ROOT, "docs", "packet", "portbrief", "Data")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_strings import harvest  # the proven string harvester


def read(name: str) -> str:
    with open(os.path.join(SCRIPTS, name), encoding="utf-8") as f:
        return f.read()


def num(s: str) -> str:
    """Normalize a GDScript numeric literal for CSV (strip trailing .0 noise
    is deliberately NOT done: constants are canon, keep them verbatim)."""
    return s.strip()


# ---------------------------------------------------------------- Rooms ----
def parse_rooms(wb: str):
    block = re.search(r"const ROOMS := \{(.*?)\n\}", wb, re.S).group(1)
    rooms = []
    for m in re.finditer(
        r'"([^"]+)":\s*\[([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\]', block
    ):
        rooms.append([m.group(1)] + [num(g) for g in m.groups()[1:]])
    return rooms


# ---------------------------------------------------------------- Doors ----
def parse_doors(wb: str):
    block = re.search(r"const DOORS := \[(.*?)\n\]", wb, re.S).group(1)
    doors = []
    for m in re.finditer(
        r'\["([^"]+)",\s*"([^"]+)",\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*'
        r'"([xz])",\s*"((?:[^"\\]|\\.)*)"\]',
        block,
    ):
        a, b, gx, gz, gw, axis, kind_raw = m.groups()
        if kind_raw == "":
            kind, reason, key = "blank", "", ""
        elif kind_raw == "door":
            kind, reason, key = "door", "", ""
        elif kind_raw == "window":
            kind, reason, key = "window", "", ""
        elif kind_raw.startswith("locked:"):
            kind = "locked"
            payload = kind_raw[len("locked:"):]
            parts = payload.split("|")
            reason = parts[0]
            key = parts[1] if len(parts) > 1 else ""
        else:
            raise ValueError(f"unknown door kind: {kind_raw!r}")
        doors.append([a, b, num(gx), num(gz), num(gw), axis, kind, reason, key])
    return doors


def parse_demo_open(wb: str):
    block = re.search(r"const DEMO_OPEN := \[(.*?)\]", wb, re.S).group(1)
    return re.findall(r'"([^"]+)"', block)


# ------------------------------------------------------------- Stations ----
def parse_stations(wb: str):
    block = re.search(r"const STATIONS := \[(.*?)\n\]", wb, re.S).group(1)
    out = []
    for m in re.finditer(
        r'\["([^"]+)",\s*"([^"]+)",\s*Vector3\(([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\)\]',
        block,
    ):
        out.append([m.group(1), m.group(2)] + [num(g) for g in m.groups()[2:]])
    return out


# ------------------------------------------------------------ Landmarks ----
def room_of(x: float, z: float, rooms) -> str:
    """Containing room from the ROOMS rects (plan view). Smallest rect wins
    where rects touch (e.g. a shed inside the yard span)."""
    best, best_area = "", 1e18
    for name, cx, cz, sx, sz in rooms:
        cx, cz, sx, sz = float(cx), float(cz), float(sx), float(sz)
        if abs(x - cx) <= sx / 2.0 + 1e-6 and abs(z - cz) <= sz / 2.0 + 1e-6:
            area = sx * sz
            if area < best_area:
                best, best_area = name, area
    return best


def parse_landmarks(wb: str, rooms):
    """Interactable spawns: `var v := Class.new()` followed by
    `v.position = Vector3(...)`, enriched by the identity fields the class
    exposes (doc_id/key_id/asset_id/display/label/door_label/sign_text/
    station ids) and the `_dock_body(v, "TEXT", ...)` plaque. Purely
    dressing meshes (MeshInstance3D/OmniLight3D/StaticBody3D boxes) are not
    interactables and are skipped, as are manager nodes with no position."""
    skip_classes = {
        "MeshInstance3D", "OmniLight3D", "StaticBody3D", "CollisionShape3D",
        "BoxShape3D", "BoxMesh", "CylinderMesh", "SphereMesh", "TorusMesh",
        "CapsuleShape3D", "Label3D", "StandardMaterial3D", "ShaderMaterial",
        "Node3D", "RegEx", "InputEventKey", "ConfigFile",
    }
    lm = []

    # pass 1: var-bound spawns. Bindings are scoped PER FUNCTION: the same
    # short names (rig, c, d, ...) recur across spawn functions, and letting
    # a binding leak lets an unrelated `.position =` claim it.
    entries = {}  # (func, var name) -> row dict
    current_fn = ""
    lines = wb.splitlines()
    for i, line in enumerate(lines, 1):
        m = re.match(r"func (\w+)\(", line)
        if m:
            current_fn = m.group(1)
            continue
        m = re.match(r"\s*var (\w+) :?= (\w+)\.new\(\)", line)
        if m and m.group(2) not in skip_classes:
            entries[(current_fn, m.group(1))] = {
                "class": m.group(2), "line": i, "id": "", "label": "",
                "pos": None, "demo_gated": False,
            }
            continue
        m = re.match(
            r"\s*(\w+)\.position = Vector3\(([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\)",
            line,
        )
        if m:
            key = (current_fn, m.group(1))
            if key in entries and entries[key]["pos"] is None:
                entries[key]["pos"] = tuple(num(g) for g in m.groups()[1:])
            continue
        m = re.match(
            r'\s*(\w+)\.(doc_id|key_id|asset_id|station_id|read_id) = "([^"]*)"',
            line,
        )
        if m:
            key = (current_fn, m.group(1))
            if key in entries and not entries[key]["id"]:
                entries[key]["id"] = m.group(3)
            continue
        m = re.match(
            r'\s*(\w+)\.(display|label|door_label|sign_text|station_name|slate_text)'
            r' = "((?:[^"\\]|\\.)*)"',
            line,
        )
        if m:
            key = (current_fn, m.group(1))
            if key in entries and not entries[key]["label"]:
                entries[key]["label"] = m.group(3)
            continue
        m = re.match(r'\s*_dock_body\((\w+), "([^"]*)"', line)
        if m:
            key = (current_fn, m.group(1))
            if key in entries and not entries[key]["label"]:
                entries[key]["label"] = m.group(2)

    # DEMO gating: functions that bail out under GameState.DEMO gate every
    # spawn after the bail; approximate per function body.
    for fm in re.finditer(r"func (\w+)\([^)]*\)[^\n]*:\n((?:\t.*\n|\n)*)", wb):
        body = fm.group(2)
        gate = re.search(r"if GameState\.DEMO:\n\t+return", body)
        if not gate:
            continue
        after = body[gate.end():]
        for vm in re.finditer(r"var (\w+) :?= (\w+)\.new\(\)", after):
            key = (fm.group(1), vm.group(1))
            if key in entries:
                entries[key]["demo_gated"] = True

    for key, e in entries.items():
        if e["pos"] is None:
            continue
        x, y, z = e["pos"]
        lm.append([
            e["class"], e["id"], e["label"], x, y, z,
            room_of(float(x), float(z), rooms),
            "yes" if e["demo_gated"] else "",
        ])

    # pass 2: the readable documents (defs array in _spawn_readables)
    for m in re.finditer(
        r'\["(D\d+)", "([^"]+)", Vector3\(([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\)',
        wb,
    ):
        did, label, x, y, z = m.groups()
        lm.append([
            "ReadableProp", did, label, num(x), num(y), num(z),
            room_of(float(x), float(z), rooms), "",
        ])

    # pass 3: the keys (helper-spawned: _spawn_key(id, display, pos, label))
    for m in re.finditer(
        r'_spawn_key\("([^"]+)", "([^"]+)", Vector3\(([-\d.]+),\s*([-\d.]+),'
        r"\s*([-\d.]+)\)",
        wb,
    ):
        kid, disp, x, y, z = m.groups()
        lm.append([
            "KeyItem", kid, disp, num(x), num(y), num(z),
            room_of(float(x), float(z), rooms), "",
        ])

    # pass 4: the monitor rigs — data-driven from the MONITORS const
    # ([cam_pos, cam_look, monitor_pos, yaw, label]); the monitor screen's
    # position is the interactable's place in the world.
    mon_block = re.search(r"const MONITORS := \[(.*?)\n\]", wb, re.S).group(1)
    for m in re.finditer(
        r"\[Vector3\([^)]*\),\s*Vector3\([^)]*\),\s*"
        r'Vector3\(([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\),\s*[^,]+,\s*"([^"]+)"\]',
        mon_block,
    ):
        x, y, z, label = m.groups()
        lm.append([
            "MonitorRig", "", label, num(x), num(y), num(z),
            room_of(float(x), float(z), rooms), "",
        ])

    lm.sort(key=lambda r: (r[0], r[1], r[2], float(r[3]), float(r[5])))
    return lm


# -------------------------------------------------------------- Timings ----
MEANINGS = {
    ("player.gd", "SPEED"): "player walk speed, m/s (deliberate weight)",
    ("player.gd", "ACCEL"): "player acceleration toward target velocity",
    ("player.gd", "MOUSE_SENS"): "base mouse-look radians per pixel",
    ("player.gd", "REACH"): "interaction raycast length, meters",
    ("player.gd", "CROUCH_MULT"):
        "crouch speed multiplier (gap-audit ruling c045: body verb; camera drops 0.6)",
    ("rundown.gd", "MOVE_SPEED"): "Chum relocation speed between segments, m/s",
    ("rundown.gd", "AF_APPROACH_SPEED"):
        "after-fire approach speed, m/s (the pour)",
    ("rundown.gd", "AF_LOOM_DIST"):
        "loom distance, meters — the performance-quote range",
    ("rundown.gd", "AF_COOL_SECONDS"): "cool-down hold after the loom, seconds",
    ("rundown.gd", "AF_HEIGHT"):
        "after-fire body height, meters (his shadow is a mechanic)",
    ("rundown.gd", "AF_FOLD_SECONDS"): "the fold: doorway montage duration, seconds",
    ("rundown.gd", "AF_DOOR_NEAR"): "doorway proximity that can trigger a fold, meters",
    ("rundown.gd", "AF_CROSSING_SPEED"): "the crossing traversal speed, m/s",
    ("rundown.gd", "WARN_RADIUS"):
        "warn radius, meters (I01: warn precedes strike)",
    ("rundown.gd", "STRIKE_RADIUS"): "strike radius, meters",
    ("rundown.gd", "BASE_HEIGHT"):
        "built rig height to the ear tips, meters (the scale law measures the body)",
    ("rundown.gd", "HEAD_TILT"):
        "resting head tilt, radians (delta 8: the restitched neck, never straight)",
    ("world_builder.gd", "WALL_H"): "wall height, meters",
    ("world_builder.gd", "WALL_T"): "wall thickness, meters",
    ("game_state.gd", "SAVE_VERSION"): "transmitter-log save format version",
}

# rows whose numbers live inline in code, each verified against its source
# before it is emitted (anchor regex must match or generation FAILS).
CURATED = [
    ("game_state.gd", "STRIKE_SHEET_CAP", "4",
     "captures before the sheet is full and the run ends",
     r"strikes >= 4"),
    ("game_state.gd", "PAPER_PER_STATION", "3",
     "Late Night log-paper lines per station per tape",
     r'"S1": 3, "S2": 3, "S3": 3, "S4": 3, "S5": 3'),
    ("game_state.gd", "MATINEE_PAPER", "99",
     "Matinee mode: paper effectively unlimited",
     r"return 99"),
    ("game_state.gd", "DOCUMENT_COUNT", "10",
     "readable documents tracked by the read-progress toast",
     r"%d of 10 documents"),
    ("game_state.gd", "ASSET_COUNT", "4",
     "finale assets to bank",
     r"%d of 4"),
    ("game_state.gd", "TAPE_MAX", "5",
     "tape number ceiling (day advances, tape caps at 5)",
     r"mini\(day, 5\)"),
    ("game_state.gd", "SIGN_NOISE", "4.0",
     "noise loudness emitted by signing a log",
     r"noise_event\.emit\(respawn_point\(\), 4\.0\)"),
    ("player.gd", "CROUCH_CAM_DROP", "0.6",
     "camera height drop while crouched, meters",
     r"camera drops 0\.6"),
]


def parse_timings():
    rows = []
    for fname in ["player.gd", "rundown.gd", "game_state.gd", "world_builder.gd"]:
        src = read(fname)
        for m in re.finditer(r"^const (\w+) := ([-\d.]+)\s*(?:##.*)?$", src, re.M):
            name, value = m.group(1), num(m.group(2))
            meaning = MEANINGS.get((fname, name))
            if meaning is None:
                continue  # non-tuning consts (paths, enums) stay out
            rows.append([name, value, fname, meaning])
    for fname, name, value, meaning, anchor in CURATED:
        src = read(fname)
        if not re.search(anchor, src):
            raise SystemExit(
                f"FAIL: curated timing {name} anchor {anchor!r} not found in {fname}"
            )
        rows.append([name, value, fname, meaning])
    rows.sort(key=lambda r: (r[2], r[0]))
    return rows


# ---------------------------------------------------------------- write ----
def write_csv(name: str, header, rows):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"WROTE {os.path.relpath(path, ROOT)} · {len(rows)} rows")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    # Godot auto-imports loose CSVs as translations; shield the folder so the
    # reference implementation's importer never chokes on port data (the same
    # .gdignore law the blend/ and tools/ source dirs live by).
    with open(os.path.join(OUT_DIR, ".gdignore"), "w", encoding="utf-8") as f:
        f.write("")
    wb = read("world_builder.gd")

    rooms = parse_rooms(wb)
    doors = parse_doors(wb)
    stations = parse_stations(wb)
    demo_open = set(parse_demo_open(wb))
    landmarks = parse_landmarks(wb, rooms)
    timings = parse_timings()
    strings, fmt_sites = harvest()

    # invariants: the world the bible promises
    assert len(rooms) == 20, f"expected 20 rooms, parsed {len(rooms)}"
    assert len(doors) == 20, f"expected 20 doors, parsed {len(doors)}"
    assert len(stations) == 5, f"expected 5 stations, parsed {len(stations)}"
    room_names = {r[0] for r in rooms}
    for d in doors:
        assert d[0] in room_names and d[1] in room_names, f"door names ghost room: {d}"
    readable_ids = {r[1] for r in landmarks if r[0] == "ReadableProp"}
    assert {"D04", "D05", "D09", "D10", "D11"} <= readable_ids, (
        f"readables missing: {readable_ids}"
    )
    assert {"EDITH", "TRAINING", "QUIET ROOM"} <= {
        r[1] for r in landmarks if r[0] == "KeyItem"
    }, "keys missing"
    assert len(strings) > 500, f"suspiciously few strings: {len(strings)}"

    write_csv("Rooms.csv",
              ["Name", "CenterX", "CenterZ", "Width", "Depth", "DemoOpen"],
              [r + ["yes" if r[0] in demo_open else ""] for r in rooms])
    write_csv("Doors.csv",
              ["RoomA", "RoomB", "GapX", "GapZ", "OpeningWidth", "WallAxis",
               "Kind", "LockedReason", "RequiredKey"],
              doors)
    write_csv("Stations.csv",
              ["Id", "Name", "X", "Y", "Z"],
              stations)
    write_csv("Landmarks.csv",
              ["Class", "Id", "Label", "X", "Y", "Z", "Room", "FullGameOnly"],
              landmarks)
    write_csv("Timings.csv",
              ["Name", "Value", "Source", "Meaning"],
              timings)
    write_csv("GameText.csv",
              ["Key", "SourceString"],
              [[s, s] for s in strings])
    print(f"GameText: {len(strings)} strings ({fmt_sites} % templates — "
          f"translate the template, keep the placeholders)")
    print("PORT-DATA-OK · units: Godot meters, plan view (X east, Z south), "
          "1m = 100uu per the recorded scale contract")


if __name__ == "__main__":
    main()
