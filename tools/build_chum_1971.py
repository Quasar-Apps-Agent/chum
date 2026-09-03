"""CHUM · 1971 PILOT · mesh build (design doc era table: the prototype)

Run:  /Applications/Blender.app/Contents/MacOS/Blender --background --python tools/build_chum_1971.py

Cruder, endearing: hand-cut patches, frayed yarn whiskers, a faintly
uneven grin, no collar and no bell yet, the amber eye already viewer-left.
Rougher wool, lumpier remesh — somebody made this at a kitchen table and
you can tell. Exports assets/models/chum_1971.glb.
"""
import bpy
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "models", "chum_1971.glb")

bpy.ops.wm.read_factory_settings(use_empty=True)
col = bpy.context.collection


def srgb_to_linear(x):
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4


def mat(name, rgb, rough=0.95, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*[srgb_to_linear(c) for c in rgb], 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


M = {
    "WoolBrown":  mat("WoolBrown",  (0.36, 0.27, 0.18), 0.97),
    "TanBelly":   mat("TanBelly",   (0.55, 0.44, 0.28), 0.97),
    "Mustard":    mat("Mustard",    (0.72, 0.55, 0.18), 0.95),
    "Navy":       mat("Navy",       (0.16, 0.20, 0.35), 0.95),
    "Rust":       mat("Rust",       (0.55, 0.25, 0.15), 0.95),
    "GreenP":     mat("GreenP",     (0.28, 0.38, 0.25), 0.95),
    "BlueP":      mat("BlueP",      (0.25, 0.32, 0.50), 0.95),
    "Plum":       mat("Plum",       (0.40, 0.22, 0.35), 0.95),
    "AmberGlass": mat("AmberGlass", (0.79, 0.60, 0.20), 0.12),
    "ButtonBlk":  mat("ButtonBlk",  (0.08, 0.08, 0.10), 0.35),
    "NoseDark":   mat("NoseDark",   (0.10, 0.08, 0.07), 0.6),
    "Thread":     mat("Thread",     (0.12, 0.10, 0.09), 0.8),
    "StringStr":  mat("StringStr",  (0.62, 0.53, 0.34), 0.85),
    "CollarBr":   mat("CollarBr",   (0.30, 0.18, 0.10), 0.7),
    "Brass":      mat("Brass",      (0.70, 0.58, 0.28), 0.3, 0.9),
}

lump = bpy.data.textures.new("lump", type="CLOUDS")
lump.noise_scale = 0.09
fiber = bpy.data.textures.new("fiber", type="CLOUDS")
fiber.noise_scale = 0.03


def sphere(loc, r, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=24, ring_count=16)
    o = bpy.context.active_object
    o.scale = scale
    return o


def cone(loc, r, h, scale=(1, 1, 1), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(radius1=r, depth=h, location=loc, vertices=16)
    o = bpy.context.active_object
    o.scale = scale
    o.rotation_euler = rot
    return o


def cyl(loc, r, h, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=loc, vertices=10)
    o = bpy.context.active_object
    o.rotation_euler = rot
    return o


def torus(loc, R, r, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(location=loc, major_radius=R, minor_radius=r,
                                     major_segments=24, minor_segments=8)
    o = bpy.context.active_object
    o.rotation_euler = rot
    return o


def join(objs, name):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    j = bpy.context.active_object
    j.name = name
    return j


def organic(obj, material, voxel=0.02, lump_str=0.014, fiber_str=0.005, decimate=0.5):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    rm = obj.modifiers.new("remesh", "REMESH")
    rm.mode = "VOXEL"
    rm.voxel_size = voxel
    d1 = obj.modifiers.new("lump", "DISPLACE")
    d1.texture = lump
    d1.strength = lump_str
    d2 = obj.modifiers.new("fiber", "DISPLACE")
    d2.texture = fiber
    d2.strength = fiber_str
    dc = obj.modifiers.new("decimate", "DECIMATE")
    dc.ratio = decimate
    obj.data.materials.clear()
    obj.data.materials.append(material)
    return obj


def simple(obj, material):
    obj.data.materials.clear()
    obj.data.materials.append(material)
    return obj


def patch(name, material, target, loc, rot_z, size):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    p = bpy.context.active_object
    p.name = name
    p.rotation_euler = (math.radians(90), 0, rot_z)
    sub = p.modifiers.new("sub", "SUBSURF")
    sub.levels = 3
    sw = p.modifiers.new("wrap", "SHRINKWRAP")
    sw.target = target
    sw.wrap_method = "TARGET_PROJECT"
    sw.wrap_mode = "ABOVE_SURFACE"
    sw.offset = 0.006
    so = p.modifiers.new("thick", "SOLIDIFY")
    so.thickness = 0.008
    simple(p, material)
    return p


# ---- body: round, loved, brown -----------------------------------------------------
body = join([
    sphere((0, 0, 0.40), 0.30, (1.0, 0.95, 1.05)),
    sphere((0, 0, 0.62), 0.22),
], "Body")
organic(body, M["WoolBrown"])

# the big tan belly circle, his most huggable feature
patch("BellyCircle", M["TanBelly"], body, (0, -0.3, 0.38), 0.0, 0.26)
patch("RustChest", M["Rust"], body, (-0.1, -0.27, 0.56), 0.25, 0.11)
patch("GreenSide", M["GreenP"], body, (0.26, -0.12, 0.42), -0.4, 0.12)

# ---- head, seam, ears ------------------------------------------------------------------
head = join([
    sphere((0, 0, 0.86), 0.24),
    sphere((0, -0.13, 0.8), 0.13, (1.15, 0.8, 0.75)),   # soft muzzle
], "Head")
organic(head, M["WoolBrown"])
# the visible center seam
seam = torus((0, 0, 0.86), 0.243, 0.006, rot=(math.radians(4), math.radians(90), math.radians(6)))
seam.name = "HeadSeam"
simple(seam, M["Thread"])

for sx, tiltd in ((-1, 22), (1, 7)):
    e = cone((0.145 * sx, 0.01, 1.09), 0.11, 0.2, scale=(1, 0.4, 1),
             rot=(0, math.radians(tiltd * sx), 0))
    e.name = "Ear" + ("L" if sx < 0 else "R")
    organic(e, M["WoolBrown"], 0.012, 0.01, 0.004, 0.55)

# ---- the face -----------------------------------------------------------------------------
amber = sphere((-0.078, -0.215, 0.9), 0.032)
amber.name = "AmberEye"
simple(amber, M["AmberGlass"])
button = sphere((0.078, -0.215, 0.9), 0.03, (1, 0.6, 1))
button.name = "ButtonEye"
simple(button, M["ButtonBlk"])
nose = cone((0, -0.25, 0.845), 0.028, 0.03, scale=(1, 0.6, 1), rot=(math.radians(90), 0, 0))
nose.name = "Nose"
simple(nose, M["NoseDark"])

# the cross-stitched grin: small X ticks along the smile curve
jit = [0.006, -0.004, 0.008, -0.006, 0.003, -0.008, 0.005]
for i in range(7):
    t = (i - 3) / 3.0
    px = 0.11 * t + jit[i]
    pz = 0.775 + 0.028 * (t * t) + jit[(i + 3) % 7]
    py = -0.235 + 0.02 * abs(t)
    for ang in (45 + 14 * jit[i] * 100, -45 - 10 * jit[(i + 2) % 7] * 100):
        tick = cyl((px, py, pz), 0.0032, 0.028,
                   rot=(0, math.radians(ang), 0))
        tick.name = f"GrinX{i}_{int(ang)}"
        simple(tick, M["Thread"])

# frayed yarn whiskers: thicker, kinked, drooping unevenly
for sx in (-1, 1):
    for k in range(3):
        w = cyl((0.18 * sx, -0.17, 0.82 + 0.03 * k), 0.006, 0.14,
                rot=(math.radians(9 * (k - 1)), math.radians(-64 * sx), 0))
        w.name = f"Yarn{'L' if sx < 0 else 'R'}{k}"
        simple(w, M["StringStr"])
        w2 = cyl((0.26 * sx, -0.19, 0.8 + 0.033 * k), 0.005, 0.1,
                 rot=(math.radians(-14 * (k - 1)), math.radians(-84 * sx), 0))
        w2.name = f"YarnFray{'L' if sx < 0 else 'R'}{k}"
        simple(w2, M["StringStr"])

# ---- arms and legs, stubby and huggable -------------------------------------------------
for sx, nm in ((-1, "ArmL"), (1, "ArmR")):
    a = join([
        sphere((0.26 * sx, -0.02, 0.52), 0.085),
        sphere((0.3 * sx, -0.07, 0.43), 0.07),
    ], nm)
    organic(a, M["WoolBrown"], 0.01, 0.005, 0.002, 0.55)
patch("BlueArm", M["BlueP"], bpy.data.objects["ArmL"], (-0.3, -0.12, 0.5), 0.3, 0.07)

for sx, nm in ((-1, "LegL"), (1, "LegR")):
    l = join([
        sphere((0.12 * sx, 0, 0.16), 0.095),
        sphere((0.13 * sx, -0.06, 0.08), 0.095, (1.0, 1.35, 0.6)),
    ], nm)
    organic(l, M["WoolBrown"], 0.01, 0.005, 0.002, 0.55)
    # mustard toe caps
    cap = sphere((0.13 * sx, -0.17, 0.065), 0.05, (1.0, 0.7, 0.75))
    cap.name = nm + "ToeCap"
    simple(cap, M["Mustard"])
patch("PlumThigh", M["Plum"], bpy.data.objects["LegR"], (0.17, -0.08, 0.2), -0.3, 0.08)

# ---- tail, curled, navy at the tip ---------------------------------------------------------
tail = join([
    sphere((0.04, 0.26, 0.3), 0.055),
    sphere((0.12, 0.36, 0.42), 0.05),
    sphere((0.2, 0.4, 0.55), 0.045),
], "Tail")
organic(tail, M["WoolBrown"], 0.01, 0.005, 0.002, 0.55)
tip = sphere((0.25, 0.41, 0.63), 0.042)
tip.name = "TailTip"
simple(tip, M["Navy"])

# no collar yet, no bell yet: the bell arrives with the 1974 rebuild

# ---- export -----------------------------------------------------------------------------------
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_apply=True)
print("WROTE", OUT)
