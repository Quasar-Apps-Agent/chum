#!/usr/bin/env python3
"""Unit 0.5 — rebuild the port kit's Data/*.csv from the Godot source
(the PORT-BRIEF: "the GDScript reads as exact pseudocode; every constant
in it is canon"). Deterministic, re-runnable; run from anywhere.

Outputs to ue/Restoration/Data/:
  Rooms.csv      name, center_x, center_z, width, depth   (Godot meters)
  Doors.csv      room_a, room_b, gap_x, gap_z, width, axis, kind
  Stations.csv   id, label, x, y, z
  Monitors.csv   cam_pos, look_at, monitor_pos, yaw_rad, label
  DemoOpen.csv   room (the DEMO whitelist)
  Timings.csv    file, constant, value  (every tuning number, with its home)
  GameText.csv   Key,SourceString (from translations/strings.csv keys)
"""
import csv
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "ue", "Restoration", "Data")
os.makedirs(OUT, exist_ok=True)

wb = open(os.path.join(ROOT, "scripts", "world_builder.gd")).read()


def block(name, opener="[", closer="]"):
    pat = r"const %s\s*:=\s*%s(.*?)\n%s" % (name, re.escape(opener), re.escape(closer))
    m = re.search(pat, wb, re.S)
    return m.group(1) if m else ""


## Rooms
rooms = re.findall(r'"([^"]+)":\s*\[([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\]',
                   block("ROOMS", "{", "}"))
with open(os.path.join(OUT, "Rooms.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "center_x", "center_z", "width", "depth"])
    for r in rooms:
        w.writerow(r)

## Doors
doors = re.findall(
    r'\["([^"]+)",\s*"([^"]+)",\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*"([xz])",\s*"([^"]*)"\]',
    block("DOORS"))
with open(os.path.join(OUT, "Doors.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["room_a", "room_b", "gap_x", "gap_z", "width", "axis", "kind"])
    for d in doors:
        w.writerow(d)

## Stations
stations = re.findall(
    r'\["([^"]+)",\s*"([^"]+)",\s*Vector3\(([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\)\]',
    block("STATIONS"))
with open(os.path.join(OUT, "Stations.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "label", "x", "y", "z"])
    for s in stations:
        w.writerow(s)

## Monitors
monitors = re.findall(
    r'\[Vector3\(([^)]+)\),\s*Vector3\(([^)]+)\),\s*Vector3\(([^)]+)\),\s*([^,\]]+),\s*"([^"]+)"\]',
    block("MONITORS"))
with open(os.path.join(OUT, "Monitors.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["cam_pos", "look_at", "monitor_pos", "yaw_rad", "label"])
    for m in monitors:
        w.writerow([x.strip() for x in m])

## Demo whitelist (single-line const — match on its own line only)
demo = re.findall(r'"([^"]+)"',
                  re.search(r"const DEMO_OPEN\s*:=\s*\[([^\]]*)\]", wb).group(1))
with open(os.path.join(OUT, "DemoOpen.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["room"])
    for d in demo:
        w.writerow([d])

## Timings: every tuning constant across scripts, with its home
rows = []
for fn in sorted(os.listdir(os.path.join(ROOT, "scripts"))):
    if not fn.endswith(".gd"):
        continue
    for i, line in enumerate(open(os.path.join(ROOT, "scripts", fn)), 1):
        m = re.match(r"\s*const\s+([A-Z][A-Z0-9_]*)\s*:?=\s*([-\d.]+)\s*(?:#.*)?$", line)
        if m:
            rows.append([fn, m.group(1), m.group(2)])
with open(os.path.join(OUT, "Timings.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["file", "constant", "value"])
    w.writerows(rows)

## GameText: keys from the shipped translations table
keys = []
with open(os.path.join(ROOT, "translations", "strings.csv"), newline="") as f:
    rd = csv.reader(f)
    header = next(rd)
    for row in rd:
        if row and row[0].strip():
            keys.append(row[0])
with open(os.path.join(OUT, "GameText.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Key", "SourceString"])
    for k in keys:
        w.writerow([k, k])

print("DATA-EXTRACTED rooms=%d doors=%d stations=%d monitors=%d demo=%d timings=%d text=%d"
      % (len(rooms), len(doors), len(stations), len(monitors), len(demo), len(rows), len(keys)))
