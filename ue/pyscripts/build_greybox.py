"""P0 · Stamp the studio into /Game/Greybox FROM Data/*.csv — the same
tables and the same wall-splitting algorithm as world_builder.gd (the code
is the spec). Godot meters/plan(x,z) -> UE cm/plan(x,y); height -> z.

Run: UnrealEditor-Cmd <proj> -run=pythonscript -script=.../build_greybox.py
Prints GREYBOX-* lines. Saves the level.
"""
import csv
import os
import unreal

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DATA = os.path.join(ROOT, "ue", "Restoration", "Data")
WALL_H = 3.0
WALL_T = 0.24
S = 100.0  # meters -> uu

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
mel = unreal.MaterialEditingLibrary

rooms = list(csv.DictReader(open(os.path.join(DATA, "Rooms.csv"))))
doors = list(csv.DictReader(open(os.path.join(DATA, "Doors.csv"))))
stations = list(csv.DictReader(open(os.path.join(DATA, "Stations.csv"))))

les.new_level("/Game/Greybox")
## strip template daylight for the club's dim interior
for a in list(eas.get_all_level_actors()):
    if a.get_class().get_name() in ("DirectionalLight", "SkyAtmosphere",
                                    "ExponentialHeightFog", "VolumetricCloud",
                                    "StaticMeshActor"):
        eas.destroy_actor(a)

CUBE = eal.load_asset("/Engine/BasicShapes/Cube")


def flat_mat(name, rgb, rough=0.9):
    full = "/Game/Core/%s" % name
    if eal.does_asset_exist(full):
        return eal.load_asset(full)
    m = at.create_asset(name, "/Game/Core", unreal.Material, unreal.MaterialFactoryNew())
    c = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -350, 0)
    c.set_editor_property("constant", unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1.0))
    mel.connect_material_property(c, "", unreal.MaterialProperty.MP_BASE_COLOR)
    r = mel.create_material_expression(m, unreal.MaterialExpressionConstant, -350, 250)
    r.set_editor_property("r", rough)
    mel.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.recompile_material(m)
    eal.save_asset(full)
    return m


M_FLOOR = flat_mat("M_GreyFloor", (0.055, 0.052, 0.05))
M_WALL = flat_mat("M_GreyWall", (0.12, 0.11, 0.10))
M_DOOR = flat_mat("M_GreyDoor", (0.10, 0.075, 0.045), 0.7)
M_STATION = flat_mat("M_Station", (0.30, 0.24, 0.09), 0.5)


def box(pos_m, size_m, mat):
    a = eas.spawn_actor_from_object(CUBE, unreal.Vector(pos_m[0] * S, pos_m[1] * S, pos_m[2] * S))
    a.set_actor_scale3d(unreal.Vector(size_m[0], size_m[1], size_m[2]))
    a.static_mesh_component.set_material(0, mat)
    return a


def cut(segments, lo, hi):
    out = []
    for a, b in segments:
        if hi <= a or lo >= b:
            out.append((a, b))
        else:
            if lo > a:
                out.append((a, lo))
            if hi < b:
                out.append((hi, b))
    return out


def wall_run(cx, cz, length, axis):
    segments = [(-length / 2.0, length / 2.0)]
    for d in doors:
        gx, gz, gw = float(d["gap_x"]), float(d["gap_z"]), float(d["width"])
        if d["axis"] != axis:
            continue
        if axis == "x" and abs(gz - cz) < 0.3 and abs(gx - cx) <= length / 2.0 + 0.01:
            g = gx - cx
        elif axis == "z" and abs(gx - cx) < 0.3 and abs(gz - cz) <= length / 2.0 + 0.01:
            g = gz - cz
        else:
            continue
        segments = cut(segments, g - gw / 2.0, g + gw / 2.0)
    n = 0
    for a, b in segments:
        if b - a < 0.05:
            continue
        mid, seg = (a + b) / 2.0, b - a
        if axis == "x":
            box((cx + mid, cz, WALL_H / 2.0), (seg, WALL_T, WALL_H), M_WALL)
        else:
            box((cx, cz + mid, WALL_H / 2.0), (WALL_T, seg, WALL_H), M_WALL)
        n += 1
    return n


nwalls = 0
for r in rooms:
    cx, cz = float(r["center_x"]), float(r["center_z"])
    sx, sz = float(r["width"]), float(r["depth"])
    box((cx, cz, -0.1), (sx, sz, 0.2), M_FLOOR)
    nwalls += wall_run(cx, cz - sz / 2.0, sx, "x")
    nwalls += wall_run(cx, cz + sz / 2.0, sx, "x")
    nwalls += wall_run(cx - sx / 2.0, cz, sz, "z")
    nwalls += wall_run(cx + sx / 2.0, cz, sz, "z")
    if r["name"] != "YARD":
        ld = unreal.PointLight
        lamp = eas.spawn_actor_from_class(ld, unreal.Vector(cx * S, cz * S, 275.0))
        lamp.light_component.set_intensity(9.0)
        lamp.light_component.set_editor_property("intensity_units",
                                                 unreal.LightUnits.CANDELAS)
        lamp.light_component.set_light_color(unreal.LinearColor(0.95, 0.72, 0.45, 1.0))
        lamp.light_component.set_editor_property("attenuation_radius",
                                                 max(sx, sz) * S * 0.75)
        lamp.light_component.set_editor_property("cast_shadows", False)

## door slabs + locked reasons as world text (kind: door|window|locked:reason)
ndoors = 0
for d in doors:
    kind = d["kind"].strip()
    if kind == "":
        continue
    gx, gz, gw = float(d["gap_x"]), float(d["gap_z"]), float(d["width"])
    horiz = d["axis"] == "x"
    if kind == "window":
        size = (gw, 0.12, 1.1) if horiz else (0.12, gw, 1.1)
        box((gx, gz, 1.9), size, M_DOOR)
        size2 = (gw, 0.12, 0.9) if horiz else (0.12, gw, 0.9)
        box((gx, gz, 0.45), size2, M_DOOR)
    else:
        size = (gw, 0.1, 2.6) if horiz else (0.1, gw, 2.6)
        box((gx, gz, 1.3), size, M_DOOR)
    if kind.startswith("locked:"):
        reason = kind.split("locked:", 1)[1].split("|")[0]
        t = eas.spawn_actor_from_class(unreal.TextRenderActor,
                                       unreal.Vector(gx * S, gz * S, 290.0))
        tr = t.text_render
        tr.set_text(unreal.Text.cast(reason))
        tr.set_editor_property("horizontal_alignment",
                               unreal.HorizTextAligment.EHTA_CENTER)
        tr.set_editor_property("world_size", 22.0)
        tr.set_editor_property("text_render_color",
                               unreal.Color(240, 200, 140, 255))
    ndoors += 1

## stations: amber markers with ids
for s_row in stations:
    x, z = float(s_row["x"]), float(s_row["z"])
    box((x, z, 0.55), (0.5, 0.5, 1.1), M_STATION)
    t = eas.spawn_actor_from_class(unreal.TextRenderActor,
                                   unreal.Vector(x * S, z * S, 150.0))
    t.text_render.set_text(unreal.Text.cast(s_row["id"]))
    t.text_render.set_editor_property("world_size", 30.0)

## player starts in REC ROOM, eye height
ps = eas.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(0, 0, 160.0))

## faint ambience so unlit corners still read as rooms, not voids
sky = eas.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0, 0, 500))
sky.light_component.set_intensity(0.12)

les.save_current_level()
unreal.log_warning("GREYBOX-DONE rooms=%d walls=%d doors=%d stations=%d"
                   % (len(rooms), nwalls, ndoors, len(stations)))
if os.environ.get("UE_QUIT_AFTER") == "1":
    unreal.SystemLibrary.quit_editor()
