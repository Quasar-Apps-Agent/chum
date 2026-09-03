"""THE SODIUM CHECK (plan doctrine; canon: restoration-blender-ue5-pipeline.md)
One sodium-spectrum lamp, a neutral floor, every material on a shader ball.
Monochromatic light kills hue; what remains is VALUE and TEXTURE — a
material that reads wrong here is lying and does not ship.

Run: Blender --background <file.blend> --python tools/sodium_check.py [-- --out X.png]
Default blend: opened file; default out: renders/sodium_check.png
Renders the most-used materials (by face count) as a labeled contact sheet.
"""
import bpy
import math
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.join(ROOT, "renders", "sodium_check.png")
if "--out" in argv:
    OUT = argv[argv.index("--out") + 1]
    if not os.path.isabs(OUT):
        OUT = os.path.join(ROOT, OUT)

## --subject: the whole opened asset under the lamp (REQUIRED for baked
## materials — on foreign ball UVs their empty bake margins read as black
## glass; only their own mesh tells the truth)
if "--subject" in argv:
    scene = bpy.context.scene
    import mathutils
    mn = mathutils.Vector((1e9, 1e9, 1e9))
    mx = mathutils.Vector((-1e9, -1e9, -1e9))
    for ob in bpy.data.objects:
        if ob.type != "MESH" or ob.hide_render:
            continue
        for c in ob.bound_box:
            w = ob.matrix_world @ mathutils.Vector(c)
            mn = mathutils.Vector(map(min, mn, w))
            mx = mathutils.Vector(map(max, mx, w))
    ctr = (mn + mx) / 2
    size = max((mx - mn).length, 1.0)
    ld = bpy.data.lights.new("Sodium", "AREA")
    ld.energy = 2600
    ld.size = 2.2
    ld.color = (1.0, 0.55, 0.08)
    lamp = bpy.data.objects.new("Sodium", ld)
    lamp.location = (ctr.x - size * 0.35, ctr.y - size * 0.5, mx.z + size * 0.4)
    lamp.rotation_euler = (math.radians(35), 0, math.radians(-20))
    bpy.context.collection.objects.link(lamp)
    world = bpy.data.worlds.new("DockWorld")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.004, 0.002, 0.0005, 1)
    camd = bpy.data.cameras.new("DockCam")
    camd.lens = 60
    cam = bpy.data.objects.new("DockCam", camd)
    cam.location = (ctr.x + size * 0.5, ctr.y - size * 1.05, ctr.z + size * 0.28)
    dd = cam.location - ctr
    cam.rotation_mode = "QUATERNION"
    cam.rotation_quaternion = dd.to_track_quat("Z", "Y")
    bpy.context.collection.objects.link(cam)
    scene.camera = cam
    scene.render.engine = "CYCLES"
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "METAL"
        prefs.get_devices()
        for dv in prefs.devices:
            dv.use = True
        scene.cycles.device = "GPU"
    except Exception:
        scene.cycles.device = "CPU"
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1100
    scene.render.resolution_y = 1400
    scene.render.filepath = OUT
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.render.render(write_still=True)
    print("SODIUM-RENDERED", OUT)
    raise SystemExit(0)

## rank materials by how much geometry wears them
usage = {}
for ob in bpy.data.objects:
    if ob.type != "MESH":
        continue
    for sl in ob.data.materials:
        if sl is None:
            continue
        usage[sl.name] = usage.get(sl.name, 0) + max(len(ob.data.polygons), 1)
ranked = sorted(usage, key=usage.get, reverse=True)[:24]
mats = [bpy.data.materials[n] for n in ranked]
print("SODIUM materials:", len(mats))

## a fresh scene: the dock
dock = bpy.data.scenes.new("SodiumDock")
bpy.context.window.scene = dock

def link(ob):
    dock.collection.objects.link(ob)

## neutral floor (18% grey, matte)
fm = bpy.data.materials.new("DockFloor")
fm.use_nodes = True
fb = fm.node_tree.nodes["Principled BSDF"]
fb.inputs["Base Color"].default_value = (0.18, 0.18, 0.18, 1.0)
fb.inputs["Roughness"].default_value = 0.9
fmesh = bpy.data.meshes.new("floor")
import bmesh
bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=6)
bm.to_mesh(fmesh)
bm.free()
floor = bpy.data.objects.new("Floor", fmesh)
floor.data.materials.append(fm)
link(floor)

## the sodium lamp: one warm-orange near-monochrome source, nothing else
ld = bpy.data.lights.new("Sodium", "AREA")
ld.energy = 900
ld.size = 1.4
ld.color = (1.0, 0.55, 0.08)
lamp = bpy.data.objects.new("Sodium", ld)
lamp.location = (0, -1.2, 3.2)
lamp.rotation_euler = (math.radians(28), 0, 0)
link(lamp)
world = bpy.data.worlds.new("DockWorld")
dock.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)

## shader balls in a grid, labeled
COLS = 6
SPACE = 0.42
rows = (len(mats) + COLS - 1) // COLS
lm = bpy.data.materials.new("LabelGlow")
lm.use_nodes = True
lnt = lm.node_tree
lnt.nodes.clear()
lo_ = lnt.nodes.new("ShaderNodeOutputMaterial")
le_ = lnt.nodes.new("ShaderNodeEmission")
le_.inputs["Color"].default_value = (0.8, 0.8, 0.8, 1.0)
le_.inputs["Strength"].default_value = 0.5
lnt.links.new(le_.outputs[0], lo_.inputs["Surface"])
for i, m in enumerate(mats):
    cx = (i % COLS - (COLS - 1) / 2.0) * SPACE
    cy = (i // COLS) * SPACE * 1.15
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(cx, cy, 0.14),
                                         segments=48, ring_count=32)
    ball = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    ball.data.materials.append(m)
    bpy.ops.object.text_add(location=(cx - 0.17, cy - 0.21, 0.005))
    txt = bpy.context.active_object
    txt.data.body = m.name[:16]
    txt.data.size = 0.05
    txt.data.materials.append(lm)

## camera: high front, ortho-ish framing of the grid
camd = bpy.data.cameras.new("DockCam")
camd.lens = 50
cam = bpy.data.objects.new("DockCam", camd)
grid_h = rows * SPACE * 1.15
cam.location = (0, -2.6 - grid_h * 0.35, 1.9 + grid_h * 0.3)
import mathutils
d = cam.location - mathutils.Vector((0, grid_h * 0.35, 0.1))
cam.rotation_mode = "QUATERNION"
cam.rotation_quaternion = d.to_track_quat("Z", "Y")
link(cam)
dock.camera = cam

dock.render.engine = "CYCLES"
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"
    prefs.get_devices()
    for dv in prefs.devices:
        dv.use = True
    dock.cycles.device = "GPU"
except Exception:
    dock.cycles.device = "CPU"
dock.cycles.samples = 96
dock.cycles.use_denoising = True
dock.render.resolution_x = 1600
dock.render.resolution_y = max(700, int(rows * 340))
dock.render.filepath = OUT
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.render.render(write_still=True)
print("SODIUM-RENDERED", OUT)
