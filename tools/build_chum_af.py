"""AFTER-FIRE CHUM · mesh build (dossier: docs/canon/art/after-fire-chum-dossier.png)

Run:  /Applications/Blender.app/Contents/MacOS/Blender --background --python tools/build_chum_af.py

Builds the eleven-footer as a real sculpted mesh. Authored numbers are in the
2.6 m base space; ONE uniform FINAL_SCALE (3.35/2.6) is applied and frozen before
the bake (OWNER RULING 2026-09-05: true 3.35 m, eye at 3 m, actor scale 1.0).
Coordinate contract with the game (Godot Y-up, character faces +Z):
Blender Z-up, front is -Y. Head empty at (0, 0, 2.28); Jaw empty child of
Head at the hinge; the right eye socket is left empty for the tally eye,
which rundown.gd parents at Godot head-local (0.13, 0.06, 0.30).
"""
import bpy
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "models", "chum_af.glb")

# ---- clean scene -----------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
col = bpy.context.collection

BAKES = []

# ---- materials --------------------------------------------------------------------
def srgb_to_linear(x):
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4

def void_black(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    em.inputs["Strength"].default_value = 0.0
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    return m


def mat(name, rgb, rough=0.95, metal=0.0, spec=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    # authored in sRGB (matching the Godot palette); stored linear per glTF
    b.inputs["Base Color"].default_value = (*[srgb_to_linear(c) for c in rgb], 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if spec is not None:
        for key in ("Specular IOR Level", "Specular"):
            try:
                b.inputs[key].default_value = spec
                break
            except Exception:
                continue
    return m

M = {
    "BurntWool":   mat("BurntWool",   (0.14, 0.115, 0.09), 0.97),
    "BellyWool":   mat("BellyWool",   (0.20, 0.16, 0.12), 0.97),
    "CharDark":    mat("CharDark",    (0.05, 0.045, 0.04), 0.9),
    "NoseWax":    mat("NoseWax",    (0.045, 0.038, 0.032), 0.92, 0.0, 0.05),
    "ButtonBrown": mat("ButtonBrown", (0.055, 0.042, 0.033), 0.9, 0.0, 0.04),
    "Brass":       mat("Brass",       (0.62, 0.5, 0.24), 0.35, 0.9),
    "RodMetal":    mat("RodMetal",    (0.35, 0.33, 0.30), 0.4, 0.85),
    "CableDark":   mat("CableDark",   (0.12, 0.11, 0.10), 0.55),
    "LeatherCol":  mat("LeatherCol",  (0.25, 0.15, 0.10), 0.6),
    "StitchSteel": mat("StitchSteel", (0.2, 0.185, 0.165), 0.55, 0.75),
    "PatchRust":   mat("PatchRust",   (0.30, 0.13, 0.09), 0.95),
    "PatchGreen":  mat("PatchGreen",  (0.20, 0.30, 0.20), 0.95),
    "PatchFlannel":mat("PatchFlannel",(0.45, 0.45, 0.47), 0.95),
    "PatchLeather":mat("PatchLeather",(0.10, 0.08, 0.07), 0.15),
    "WireWhisker": mat("WireWhisker", (0.11, 0.1, 0.09), 0.7),
    "StubWhisker": mat("StubWhisker", (0.22, 0.16, 0.09), 0.9),
    "EarFelt":    mat("EarFelt",    (0.14, 0.115, 0.09), 0.97),
    "PatchMustard": mat("PatchMustard", (0.19, 0.135, 0.045), 0.97),
    "PatchNavy":  mat("PatchNavy",  (0.055, 0.08, 0.16), 0.97),
    "MawBlack":   void_black("MawBlack"),
    "FiberFuzz":  mat("FiberFuzz",  (0.2, 0.16, 0.11), 1.0),
    "FurDark":    mat("FurDark",    (0.1, 0.08, 0.06), 1.0),
    "BronzeBand": mat("BronzeBand", (0.13, 0.078, 0.038), 0.68, 0.8),
    "BronzeChar": mat("BronzeChar", (0.1, 0.07, 0.045), 0.85, 0.45),
    "CopperRing": mat("CopperRing", (0.13, 0.08, 0.045), 0.7, 0.85),
    "GrilleDark": mat("GrilleDark", (0.17, 0.16, 0.14), 0.5, 0.75),
    "ToothBone":  mat("ToothBone",  (0.63, 0.56, 0.44), 0.75),
    "LipLeather": mat("LipLeather", (0.12, 0.075, 0.05), 0.9),
    "PanelA":     mat("PanelA",     (0.13, 0.105, 0.075), 0.97),
    "PanelB":     mat("PanelB",     (0.16, 0.125, 0.09), 0.97),
    "PanelC":     mat("PanelC",     (0.11, 0.09, 0.065), 0.97),
    "FurMid":     mat("FurMid",     (0.19, 0.15, 0.1), 1.0),
    "FurRust":    mat("FurRust",    (0.27, 0.15, 0.09), 1.0),
    "Thread":     mat("Thread",     (0.10, 0.09, 0.08), 0.8),
}

# ---- displacement textures ---------------------------------------------------------
import random
random.seed(58)

folds = bpy.data.textures.new("folds", type="MARBLE")
folds.noise_scale = 0.45
folds.turbulence = 7.0

lump = bpy.data.textures.new("lump", type="CLOUDS")
lump.noise_scale = 0.18
fiber = bpy.data.textures.new("fiber", type="CLOUDS")
fiber.noise_scale = 0.045

# ---- helpers ------------------------------------------------------------------------
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

def cyl(loc, r, h, rot=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=loc, vertices=12)
    o = bpy.context.active_object
    o.rotation_euler = rot
    o.scale = scale
    return o

def torus(loc, R, r, rot=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(location=loc, major_radius=R, minor_radius=r,
                                     major_segments=24, minor_segments=10)
    o = bpy.context.active_object
    o.rotation_euler = rot
    o.scale = scale
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

def organic(obj, material, voxel=0.03, lump_str=0.02, fiber_str=0.006, decimate=0.45, fold_str=0.0, smooth=0):
    """voxel-remesh the fused masses, displace twice (felt lump + fiber), decimate"""
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
    if fold_str > 0.0:
        d3 = obj.modifiers.new("folds", "DISPLACE")
        d3.texture = folds
        d3.strength = fold_str
    dc = obj.modifiers.new("decimate", "DECIMATE")
    dc.ratio = decimate
    if smooth > 0:
        ## the decimated surface must never facet at 1 m (BRIEF 1.1 step 1)
        sm = obj.modifiers.new("smooth", "SMOOTH")
        sm.factor = 0.5
        sm.iterations = smooth
    bpy.ops.object.convert(target="MESH")   # apply now: baking needs real topology
    obj = bpy.context.active_object
    obj.data.materials.clear()
    obj.data.materials.append(material)
    BAKES.append(obj)
    return obj

## the fur-card texture: real Cycles hair tufts rendered to an alpha atlas
## by tools/make_fur_cards.py — the standard game-fur technique
FUR_ATLAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "texsrc", "fur_tuft_atlas.png")
FURCARDS = bpy.data.materials.new("FurCards")
FURCARDS.use_nodes = True
_fb = FURCARDS.node_tree.nodes["Principled BSDF"]
_ft = FURCARDS.node_tree.nodes.new("ShaderNodeTexImage")
_ft.image = bpy.data.images.load(FUR_ATLAS)
try:
    _ft.image.pack()
except Exception:
    pass
FURCARDS.node_tree.links.new(_ft.outputs["Color"], _fb.inputs["Base Color"])
FURCARDS.node_tree.links.new(_ft.outputs["Alpha"], _fb.inputs["Alpha"])
_fb.inputs["Roughness"].default_value = 0.9
for _attr, _val in (("blend_method", "CLIP"), ("alpha_threshold", 0.35),
                    ("shadow_method", "CLIP"), ("surface_render_method", "DITHERED"),
                    ("use_backface_culling", False)):
    try:
        setattr(FURCARDS, _attr, _val)
    except Exception:
        pass


def feltify(mm, scale=170.0, strength=0.4):
    """Procedural felt grain: noise bump so raw cloth reads woven, not plastic."""
    fnt = mm.node_tree
    fb = fnt.nodes["Principled BSDF"]
    fnz = fnt.nodes.new("ShaderNodeTexNoise")
    fnz.inputs["Scale"].default_value = scale
    fbp = fnt.nodes.new("ShaderNodeBump")
    fbp.inputs["Strength"].default_value = strength
    fbp.inputs["Distance"].default_value = 0.002
    fnt.links.new(fnz.outputs["Fac"], fbp.inputs["Height"])
    fnt.links.new(fbp.outputs["Normal"], fb.inputs["Normal"])


for _k in ("PatchMustard", "PatchNavy", "PanelA", "PanelB", "PanelC",
           "CharDark", "PatchRust"):
    feltify(M[_k])
feltify(M["NoseWax"], scale=230.0, strength=0.15)


def fur(host, count, lmin, lmax, name, mats, along=0.85, lift=0.14, mask=None):
    """Fur cards: curved quads wearing the tuft atlas — rendered hair with
    alpha, so both the viewport and the game show tufts, not paper strips.
    `count` is legacy strand count; cards are ~0.38x of it. One bmesh, fast."""
    import bmesh
    import mathutils
    mesh = host.data
    mesh.calc_loop_triangles()
    tris = list(mesh.loop_triangles)
    if not tris:
        return None
    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")
    out = bpy.data.meshes.new(name)
    n_cards = max(12, int(count * 0.38))
    for i in range(n_cards):
        tri = tris[random.randrange(len(tris))]
        vs = [mesh.vertices[v].co for v in tri.vertices]
        a, b = random.random(), random.random()
        if a + b > 1.0:
            a, b = 1.0 - a, 1.0 - b
        base = vs[0] + a * (vs[1] - vs[0]) + b * (vs[2] - vs[0])
        if mask is not None and mask(host.matrix_world @ base):
            continue
        n = mathutils.Vector(tri.normal).normalized()
        ref = mathutils.Vector((random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)))
        t = n.cross(ref)
        if t.length < 0.05:
            continue
        t.normalize()
        ln = random.uniform(lmin, lmax)
        segs = 3
        seg = ln / segs
        d = (t * along + n * lift).normalized()
        w = ln * random.uniform(0.24, 0.36)
        pts = [base + n * 0.004]
        for k in range(segs):
            droop = mathutils.Vector((0, 0, -0.42 * (k + 1) / segs))
            d = (d * 0.8 + t * 0.15 + droop * 0.3).normalized()
            pts.append(pts[-1] + d * seg)
        side = d.cross(n)
        if side.length < 0.05:
            side = t.cross(n)
        side.normalize()
        row = []
        for pt in pts:
            v1 = bm.verts.new(pt - side * w)
            v2 = bm.verts.new(pt + side * w)
            row.append((v1, v2))
        colu = random.randrange(4)
        u0, u1 = colu * 0.25 + 0.03, colu * 0.25 + 0.22
        for k in range(segs):
            f = bm.faces.new((row[k][0], row[k][1], row[k + 1][1], row[k + 1][0]))
            f.material_index = 0
            v0f, v1f = k / segs, (k + 1) / segs
            for lp, uv in zip(f.loops, ((u0, v0f), (u1, v0f), (u1, v1f), (u0, v1f))):
                lp[uv_layer].uv = uv
    bm.to_mesh(out)
    bm.free()
    ob = bpy.data.objects.new(name, out)
    col.objects.link(ob)
    ob.matrix_world = host.matrix_world.copy()
    ob.data.materials.append(FURCARDS)
    return ob


def fuzz(host, count, lmin, lmax, material, name):
    import mathutils
    mesh = host.data
    mesh.calc_loop_triangles()
    tris = list(mesh.loop_triangles)
    if not tris:
        return None
    fibers = []
    for i in range(count):
        tri = tris[random.randrange(len(tris))]
        vs = [mesh.vertices[v].co for v in tri.vertices]
        a, b = random.random(), random.random()
        if a + b > 1.0:
            a, b = 1.0 - a, 1.0 - b
        pos = vs[0] + a * (vs[1] - vs[0]) + b * (vs[2] - vs[0])
        n = mathutils.Vector(tri.normal)
        ln = random.uniform(lmin, lmax)
        bpy.ops.mesh.primitive_cone_add(radius1=0.003, depth=ln, vertices=3,
                                        location=host.matrix_world @ (pos + n * (ln / 2.0)))
        f = bpy.context.active_object
        jitter = mathutils.Vector((random.uniform(-0.35, 0.35), random.uniform(-0.35, 0.35), random.uniform(-0.35, 0.35)))
        f.rotation_mode = "QUATERNION"
        f.rotation_quaternion = (n + jitter).normalized().to_track_quat("Z", "Y")
        fibers.append(f)
    fz = join(fibers, name)
    simple(fz, material)
    return fz


def simple(obj, material):
    obj.data.materials.clear()
    obj.data.materials.append(material)
    return obj

def empty(name, loc, parent=None):
    e = bpy.data.objects.new(name, None)
    col.objects.link(e)
    e.location = loc
    if parent:
        e.parent = parent
        e.matrix_parent_inverse = parent.matrix_world.inverted()
    return e

def parent_to(child, parent):
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()

## the PLATE's patch palette (mascot canon). The stage puppet's flannel and
## leather deltas are STRIPPED per owner ruling 2026-09-05. Tints over real scans.
M["PatchOlive"] = mat("PatchOlive", (0.20, 0.28, 0.17), 0.95)
M["PatchNavy"]  = mat("PatchNavy",  (0.10, 0.12, 0.20), 0.95)
M["PatchOchre"] = mat("PatchOchre", (0.42, 0.32, 0.16), 0.95)
M["PatchBrown"] = mat("PatchBrown", (0.16, 0.11, 0.08), 0.95)
M["PatchPlaid"] = mat("PatchPlaid", (0.55, 0.45, 0.35), 0.95)

# ---- the body: round-bellied, patched, burnt ---------------------------------------
## PLATE silhouette: belly forward, chest sagging over the collar line (BRIEF 1.1 step 1)
body = join([
    sphere((0, -0.05, 1.38), 0.47, (1.0, 0.96, 1.20)),   # the belly mass, forward
    sphere((0, -0.01, 1.78), 0.37, (0.98, 0.92, 0.86)),  # chest, sagging
    sphere((0, 0.02, 0.98), 0.34, (1.05, 0.95, 0.8)),    # pelvis
    sphere((-0.40, 0.01, 1.78), 0.16),                   # shoulders
    sphere((0.40, 0.01, 1.78), 0.16),
    sphere((-0.24, 0, 1.0), 0.2, (1, 1, 0.9)),           # hips
    sphere((0.24, 0, 1.0), 0.2, (1, 1, 0.9)),
], "BodyCore")
organic(body, M["BurntWool"], 0.02, 0.018, 0.006, 0.4, smooth=4)
## BRIEF 1.1 step 6: singed rims only — cards survive on the shoulder and hip
## crests; the fused bouclé scan carries the pile everywhere else so the quilt
## can read. mask=True excludes.
body_fur = fur(body, 900, 0.02, 0.04, "BodyFur",
               [M["FurDark"], M["FurMid"], M["FurRust"]],
               mask=lambda wp: not ((wp.z > 1.72 and abs(wp.x) > 0.25) or
                                    (0.85 < wp.z < 1.15 and abs(wp.x) > 0.20)))

## SOLID PATCHES (BRIEF 1.1 step 2): a copy of the fused body pushed proud along
## its normals, boolean-INTERSECTED with a cutter, then voxel-remeshed — real
## sewn-on mass that follows the body's curvature. Never a shrinkwrapped shell
## (they collapsed into slivers; banned).
def solid_patch(name, material, cutter, proud=0.014, voxel=0.006, decimate=0.5):
    bpy.ops.object.select_all(action="DESELECT")
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.duplicate(linked=False)
    p = bpy.context.active_object
    p.name = name
    p.modifiers.clear()
    dp = p.modifiers.new("proud", "DISPLACE")
    dp.direction = "NORMAL"
    dp.mid_level = 0.0
    dp.strength = proud
    bo = p.modifiers.new("cut", "BOOLEAN")
    bo.operation = "INTERSECT"
    bo.object = cutter
    bo.solver = "EXACT"
    bpy.ops.object.convert(target="MESH")
    p = bpy.context.active_object
    bpy.data.objects.remove(cutter, do_unlink=True)
    rm = p.modifiers.new("remesh", "REMESH")
    rm.mode = "VOXEL"
    rm.voxel_size = voxel
    dc = p.modifiers.new("decimate", "DECIMATE")
    dc.ratio = decimate
    sm = p.modifiers.new("smooth", "SMOOTH")
    sm.factor = 0.4
    sm.iterations = 2
    bpy.ops.object.convert(target="MESH")
    p = bpy.context.active_object
    simple(p, material)
    BAKES.append(p)
    print("PATCH", name, "verts", len(p.data.vertices))
    return p

def rounded_prism(loc, rot_z, w, h, depth=0.36, bevel=0.03):
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=loc)
    c = bpy.context.active_object
    c.scale = (w / 2.0, depth / 2.0, h / 2.0)
    c.rotation_euler = (0, 0, rot_z)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bv = c.modifiers.new("bevel", "BEVEL")
    bv.width = bevel
    bv.segments = 4
    bpy.ops.object.convert(target="MESH")
    return bpy.context.active_object

# the belly: a sewn-in oval PANEL of the body, 20 mm proud (PLATE: a lighter tan
# oval with a dark border; the stage's resewn scar is OPEN, not built)
belly_cut = sphere((0, -0.36, 1.34), 0.30, (1.0, 0.55, 1.28))
belly = solid_patch("Belly", M["BellyWool"], belly_cut, proud=0.02, voxel=0.008, decimate=0.5)

# ---- legs and weighted paw feet ------------------------------------------------------
for sx, nm in ((-1, "LegL"), (1, "LegR")):
    hip = empty("Hip" + nm[-1], (0.20 * sx, 0, 0.92))
    leg = join([
        sphere((0.20 * sx, 0, 0.78), 0.155, (1, 1, 1.25)),
        sphere((0.20 * sx, 0, 0.46), 0.135, (1, 1, 1.2)),
        sphere((0.20 * sx, -0.02, 0.2), 0.125),
        sphere((0.20 * sx, -0.09, 0.11), 0.185, (1.05, 1.45, 0.62)),   # the weighted foot
        sphere((0.13 * sx, -0.3, 0.09), 0.062),                        # toe lobes
        sphere((0.20 * sx, -0.32, 0.09), 0.062),
        sphere((0.27 * sx, -0.3, 0.09), 0.062),
    ], nm)
    organic(leg, M["BurntWool"], 0.025, 0.018, 0.006, 0.45)
    parent_to(leg, hip)
    leg_fur = fur(leg, 700, 0.03, 0.07, nm + "Fur", [M["FurDark"], M["FurMid"]],
                  mask=lambda wp: wp.z < 0.08)
    if leg_fur:
        parent_to(leg_fur, hip)
    # leg control rod, exposed (dossier detail 5)
    rod = cyl((0.31 * sx, 0.05, 0.45), 0.016, 0.62)
    rod.name = nm + "Rod"
    simple(rod, M["RodMetal"])
    parent_to(rod, hip)

# ---- arms: tendon-driven, clawed ------------------------------------------------------
for sx, nm in ((-1, "ArmL"), (1, "ArmR")):
    shoulder = empty("Shoulder" + nm[-1], (0.47 * sx, 0, 1.72))
    ## the limb: shoulder mass, upper arm, a distinct elbow, forearm, wrist
    arm = join([
        sphere((0.47 * sx, 0, 1.68), 0.135),
        sphere((0.51 * sx, -0.02, 1.46), 0.11, (1, 1, 1.2)),
        sphere((0.55 * sx, -0.03, 1.26), 0.1),                          # elbow
        sphere((0.58 * sx, -0.05, 1.08), 0.09, (1, 1, 1.15)),
        sphere((0.6 * sx, -0.06, 0.97), 0.085),                         # wrist
    ], nm)
    organic(arm, M["BurntWool"], 0.022, 0.016, 0.006, 0.45)
    parent_to(arm, shoulder)
    arm_fur = fur(arm, 650, 0.025, 0.06, nm + "Fur", [M["FurDark"], M["FurMid"], M["FurRust"]])
    if arm_fur:
        parent_to(arm_fur, shoulder)
    ## the hand: palm, three two-lobed fingers, claw sheaths
    hand_parts = [sphere((0.62 * sx, -0.07, 0.9), 0.115, (1.0, 0.8, 1.05))]
    finger_x = (0.53, 0.62, 0.71)
    for fi, fx in enumerate(finger_x):
        hand_parts.append(sphere((fx * sx, -0.1, 0.8), 0.052))
        hand_parts.append(sphere((fx * sx + 0.012 * sx, -0.13, 0.73), 0.045))
    hand = join(hand_parts, nm + "Hand")
    organic(hand, M["BurntWool"], 0.016, 0.012, 0.005, 0.5)
    parent_to(hand, shoulder)
    for fi, fx in enumerate(finger_x):
        c = cone((fx * sx + 0.02 * sx, -0.16, 0.675), 0.019, 0.1, rot=(math.radians(197), 0, 0))
        c.name = f"{nm}Claw{fi}"
        simple(c, M["CharDark"])
        parent_to(c, shoulder)
    ## the shoulder seam: a stitched ring where the arm was sewn back on
    sring = torus((0.45 * sx, -0.01, 1.71), 0.11, 0.014, rot=(0, math.radians(75 * sx), 0))
    sring.name = nm + "SeamRing"
    simple(sring, M["Thread"])
    parent_to(sring, shoulder)
    for st in range(5):
        sa = math.radians(72 * st)
        stt = cyl((0.45 * sx + 0.02 * sx, -0.01 + 0.1 * math.cos(sa), 1.71 + 0.1 * math.sin(sa)), 0.005, 0.05,
                  rot=(sa, math.radians(75 * sx), 0))
        stt.name = f"{nm}SeamStitch{st}"
        simple(stt, M["Thread"])
        parent_to(stt, shoulder)
    ## the elbow wrap: a fabric bandage band, tied
    wrap = torus((0.55 * sx, -0.03, 1.26), 0.105, 0.03, rot=(math.radians(10), math.radians(70 * sx), 0))
    wrap.name = nm + "ElbowWrap"
    simple(wrap, M["BellyWool"])
    parent_to(wrap, shoulder)
    ## tendon cables with metal guide staples: dense on the left (the dossier
    ## plate's exposed side), a single survivor on the right
    tendon_count = 3 if sx < 0 else 1
    for k in range(tendon_count):
        toff = 0.02 * k
        t1 = cyl((0.49 * sx + toff * sx, -0.105 - toff, 1.49), 0.008, 0.4, rot=(math.radians(6), math.radians(11 * sx), 0))
        t1.name = f"{nm}TendonA{k}"
        simple(t1, M["CableDark"])
        parent_to(t1, shoulder)
        t2 = cyl((0.565 * sx + toff * sx, -0.115 - toff, 1.11), 0.008, 0.32, rot=(math.radians(9), math.radians(9 * sx), 0))
        t2.name = f"{nm}TendonB{k}"
        simple(t2, M["CableDark"])
        parent_to(t2, shoulder)
    for gz in (1.55, 1.26, 1.0):
        guide = torus((0.545 * sx + (0.03 * sx if gz < 1.3 else 0.0), -0.115, gz), 0.028, 0.007,
                      rot=(math.radians(90), 0, math.radians(10 * sx)))
        guide.name = f"{nm}Guide{gz}"
        simple(guide, M["RodMetal"])
        parent_to(guide, shoulder)

# ---- tail, dragging low ----------------------------------------------------------------
tail_pivot = empty("TailPivot", (0.04, 0.36, 0.76))
tail = join([
    sphere((0.06, 0.4, 0.72), 0.085),
    sphere((0.16, 0.62, 0.5), 0.075),
    sphere((0.28, 0.78, 0.3), 0.065),
    sphere((0.4, 0.88, 0.14), 0.055),
    sphere((0.5, 0.94, 0.08), 0.05),
], "Tail")
organic(tail, M["BurntWool"], 0.02, 0.014, 0.005, 0.5)
parent_to(tail, tail_pivot)
tail_fur = fur(tail, 500, 0.03, 0.075, "TailFur", [M["FurDark"], M["FurMid"], M["FurRust"]])
if tail_fur:
    parent_to(tail_fur, tail_pivot)

# ---- collar and the bell ----------------------------------------------------------------
collar = torus((0, 0, 2.02), 0.27, 0.038, rot=(math.radians(6), 0, 0))
collar.name = "Collar"
simple(collar, M["LeatherCol"])
bell = sphere((0, -0.27, 1.94), 0.06)
bell.name = "Bell"
simple(bell, M["Brass"])

# ---- throat speaker (dossier detail 2) ---------------------------------------------------
spk = cyl((0, -0.37, 1.74), 0.09, 0.05, rot=(math.radians(78), 0, 0))
spk.name = "ThroatSpeaker"
simple(spk, M["CharDark"])

# ---- patches: the PLATE's quilt as SOLID sewn-on mass (BRIEF 1.1 step 2) ----------
## Count/placement read from the PLATE: rust-red left shoulder, olive right
## chest, navy flank, tan/ochre, small dark browns, one checked cloth. The
## stage's "fourteen" is OPEN. Flannel + leather: STRIPPED (owner ruling).
for _pn, _pm, _loc, _rz, _w, _h in (
        ("PatchRust",   M["PatchRust"],  (-0.27, -0.36, 1.66),  0.30, 0.24, 0.22),
        ("PatchOlive",  M["PatchOlive"], ( 0.29, -0.33, 1.52), -0.20, 0.21, 0.19),
        ("PatchNavy",   M["PatchNavy"],  (-0.38, -0.20, 1.20),  0.55, 0.19, 0.17),
        ("PatchOchre",  M["PatchOchre"], ( 0.36, -0.22, 1.30),  0.10, 0.17, 0.15),
        ("PatchBrownA", M["PatchBrown"], (-0.37, -0.16, 0.98),  0.05, 0.13, 0.11),
        ("PatchBrownB", M["PatchBrown"], ( 0.15, -0.38, 1.88), -0.10, 0.12, 0.10),
        ("PatchPlaid",  M["PatchPlaid"], (-0.05, -0.30, 1.90),  0.00, 0.15, 0.13)):
    solid_patch(_pn, _pm, rounded_prism(_loc, _rz, _w, _h))

# ---- THE HEAD (dossier-matched, iteration 2) -----------------------------------------
head = empty("Head", (0, 0, 2.28))
head.rotation_euler = (0, 0.045, 0)

skull = join([
    sphere((0, 0, 2.34), 0.375, (1.08, 0.98, 0.88)),
    sphere((0, -0.24, 2.2), 0.2, (1.1, 0.8, 0.7)),
    sphere((0, 0.16, 2.3), 0.24, (0.9, 0.8, 0.8)),
    sphere((-0.27, -0.1, 2.18), 0.15),
    sphere((0.27, -0.1, 2.18), 0.15),
    sphere((0, -0.26, 2.44), 0.17, (1.7, 0.5, 0.42)),
], "Skull")
organic(skull, M["BurntWool"], 0.022, 0.016, 0.006, 0.4, fold_str=0.012)
parent_to(skull, head)
def face_mask(wp):
    ## keep the muzzle, the maw, and both eye assemblies worn bald
    if wp.y < -0.24 and 2.02 < wp.z < 2.46 and abs(wp.x) < 0.34:
        return True
    return False

skull_fur = fur(skull, 5600, 0.03, 0.08, "SkullFur",
                [M["FurDark"], M["FurMid"], M["FurRust"]], mask=face_mask)
if skull_fur:
    parent_to(skull_fur, head)
skull_fuzz = fuzz(skull, 160, 0.008, 0.022, M["FiberFuzz"], "SkullFuzz")
if skull_fuzz:
    parent_to(skull_fuzz, head)

def head_patch(name, material, loc, rot_z, size):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    hp = bpy.context.active_object
    hp.name = name
    hp.rotation_euler = (math.radians(90), 0, rot_z)
    sub = hp.modifiers.new("sub", "SUBSURF")
    sub.levels = 3
    sw = hp.modifiers.new("wrap", "SHRINKWRAP")
    sw.target = skull
    sw.wrap_method = "NEAREST_SURFACEPOINT"
    sw.wrap_mode = "ABOVE_SURFACE"
    sw.offset = 0.007
    so = hp.modifiers.new("thick", "SOLIDIFY")
    so.thickness = 0.01
    bpy.ops.object.convert(target="MESH")
    hp = bpy.context.active_object
    simple(hp, material)
    ## NOT baked: thin shrinkwrap shells bake garbage-bright (the white-shard
    ## artifact); their raw panel tones are already the plate's quilt palette
    parent_to(hp, head)
    return hp

head_patch("SkullPatchRust", M["PatchRust"], (-0.24, -0.28, 2.54), 0.35, 0.13)
## the face is a quilt: panels staggered so their seams cross the whole face
head_patch("FacePanelFL", M["PanelA"], (-0.11, -0.35, 2.54), 0.2, 0.12)
head_patch("FacePanelFR", M["PanelB"], (0.14, -0.34, 2.5), -0.15, 0.16)
head_patch("FacePanelCL", M["PanelC"], (-0.21, -0.33, 2.28), 0.4, 0.16)
head_patch("FacePanelCR", M["PanelA"], (0.22, -0.32, 2.29), -0.35, 0.15)

def stitch_run(pts, prefix):
    for i in range(len(pts) - 1):
        ax, ay, az = pts[i]
        bx, by, bz = pts[i + 1]
        mx, my, mz = (ax + bx) / 2, (ay + by) / 2, (az + bz) / 2
        ang = 42 if i % 2 == 0 else -42
        st = cyl((mx, my - 0.006, mz), 0.0045, 0.032, rot=(0, math.radians(ang), 0))
        st.name = f"{prefix}{i}"
        simple(st, M["StitchSteel"])
        parent_to(st, head)

## the center seam, forehead to nose, and the cheek seams
stitch_run([(0, -0.21, 2.56), (0, -0.29, 2.49), (0, -0.345, 2.43), (0, -0.38, 2.37)], "SeamC")
stitch_run([(-0.32, -0.22, 2.32), (-0.24, -0.3, 2.3), (-0.15, -0.35, 2.28), (-0.07, -0.38, 2.27)], "SeamL")
stitch_run([(0.32, -0.22, 2.32), (0.24, -0.3, 2.3), (0.15, -0.35, 2.28), (0.07, -0.38, 2.27)], "SeamR")
stitch_run([(-0.28, -0.26, 2.48), (-0.2, -0.31, 2.45)], "SeamBL")
stitch_run([(0.28, -0.26, 2.5), (0.2, -0.31, 2.47)], "SeamBR")
head_patch("SkullPatchTan",  M["PanelB"], (0.27, -0.22, 2.32), -0.3, 0.15)
head_patch("SkullPatchChar", M["CharDark"], (0.16, -0.24, 2.5), 0.1, 0.12)
head_patch("BurnField", M["CharDark"], (0.18, -0.29, 2.37), -0.15, 0.2)

# the center seam over the crown, front to back: staple stitches crossing the
# seam line (the bead spheres read as warts in-engine; staples read as sewing)
crown_sts = []
for k in range(11):
    ang = -0.9 + 0.18 * k
    stc = cyl((0, 0.35 * math.sin(ang), 2.335 + 0.345 * math.cos(ang)), 0.0045, 0.034,
              rot=(0, math.radians(90 + random.uniform(-14, 14)),
                   math.radians(random.uniform(-10, 10))))
    stc.name = f"CrownSeam{k}"
    crown_sts.append(stc)
crownj = join(crown_sts, "CrownSeamStitches")
simple(crownj, M["StitchSteel"])
parent_to(crownj, head)
# scattered X-ticks where panels meet
for tx, tz, ty, ry in ((-0.3, 2.42, -0.185, 0.5), (0.31, 2.44, -0.17, -0.4), (-0.12, 2.56, -0.14, 0.2)):
    for ang in (45, -45):
        tick = cyl((tx, ty, tz), 0.0045, 0.045, rot=(0, math.radians(ang), ry))
        tick.name = f"XT{tx}_{tz}_{ang}"
        simple(tick, M["Thread"])
        parent_to(tick, head)

# the face panel's sewn border: staples tracing the fur boundary
for i in range(18):
    ba = math.radians(200 + (140.0 / 17) * i)
    bx = 0.335 * math.cos(ba)
    bz = 2.3 - 0.26 * math.sin(ba)
    byy = -(0.36 - 0.14 * abs(math.cos(ba)))
    bst = cyl((bx, byy, bz), 0.005, 0.036,
              rot=(0, math.radians(90) + ba, 0))
    bst.name = f"BorderStitch{i}"
    simple(bst, M["StitchSteel"])
    parent_to(bst, head)

# ---- EARS, fully HD -----------------------------------------------------------------
# Thick felt slabs at fine voxel with double displacement (ragged burnt edges over a
# woven wrinkle), steel staples sewn along both long edges, a tattered inner patch
# shrinkwrapped to the felt (mustard viewer-left, navy viewer-right) ringed with
# blanket stitches, and a charred melt cap on the singed left tip.
for sx, nm, hscale, tipmat in ((-1, "EarL", 0.74, "PatchMustard"), (1, "EarR", 1.0, "PatchNavy")):
    th = math.radians(13 * sx)
    C = (0.24 * sx, 0.03, 2.78)
    r_e, h_e = 0.2, 0.52 * hscale
    ear_staples = []
    ear_ticks = []
    e = cone(C, r_e, h_e, scale=(1.0, 0.34, 1.0))
    e.rotation_euler = (0, th, 0)
    e.name = nm
    rm = e.modifiers.new("remesh", "REMESH")
    rm.mode = "VOXEL"
    rm.voxel_size = 0.007
    d = e.modifiers.new("rag", "DISPLACE")
    d.texture = lump
    d.strength = 0.034 if sx < 0 else 0.018
    d2 = e.modifiers.new("weave", "DISPLACE")
    d2.texture = fiber
    d2.strength = 0.009
    dc = e.modifiers.new("dec", "DECIMATE")
    dc.ratio = 0.65
    bpy.ops.object.convert(target="MESH")
    e = bpy.context.active_object
    simple(e, M["EarFelt"])
    BAKES.append(e)
    parent_to(e, head)

    ## the sewn edge: staples tracing both long edges, base corner to tip
    for side in (-1, 1):
        cx, cz = side * r_e * 0.88, -h_e / 2
        tx, tz = 0.0, h_e / 2 - 0.015
        dxe, dze = tx - cx, tz - cz
        plen = math.hypot(dze, dxe)
        pxl, pzl = dze / plen, -dxe / plen
        nst = 7 if hscale < 1.0 else 9
        for i in range(nst):
            t = (i + 0.5) / nst
            lx = cx + dxe * t
            lz = cz + dze * t
            wx = C[0] + lx * math.cos(th) + lz * math.sin(th)
            wz = C[2] - lx * math.sin(th) + lz * math.cos(th)
            pxw = pxl * math.cos(th) + pzl * math.sin(th)
            pzw = -pxl * math.sin(th) + pzl * math.cos(th)
            phi = math.atan2(pxw, pzw)
            st = cyl((wx, C[1] - 0.035, wz), 0.005, 0.05,
                     rot=(math.radians(random.uniform(-9, 9)), phi,
                          math.radians(random.uniform(-6, 6))))
            st.name = f"{nm}Edge{side}_{i}"
            ssw = st.modifiers.new("snap", "SHRINKWRAP")
            ssw.target = e
            ssw.wrap_method = "NEAREST_SURFACEPOINT"
            ssw.wrap_mode = "ABOVE_SURFACE"
            ssw.offset = 0.004
            bpy.ops.object.convert(target="MESH")
            ear_staples.append(bpy.context.active_object)

    ## tattered inner panel: a solid felt triangle embedded in the ear's front
    ## face (no shrinkwrap — thin wrapped shells collapse into slivers)
    r_p, h_p = 0.1 * hscale, 0.24 * hscale
    plx, ply, plz = -sx * 0.012, -0.058, 0.0
    ppx = C[0] + plx * math.cos(th) + plz * math.sin(th)
    ppy = C[1] + ply
    ppz = C[2] - plx * math.sin(th) + plz * math.cos(th)
    pt = cone((ppx, ppy, ppz), r_p, h_p, scale=(1.0, 0.13, 1.0),
              rot=(math.radians(-8), th, 0))
    pt.name = nm + "Panel"
    prm = pt.modifiers.new("remesh", "REMESH")
    prm.mode = "VOXEL"
    prm.voxel_size = 0.006
    pdd = pt.modifiers.new("tatter", "DISPLACE")
    pdd.texture = lump
    pdd.strength = 0.016
    pdd2 = pt.modifiers.new("crinkle", "DISPLACE")
    pdd2.texture = fiber
    pdd2.strength = 0.005
    bpy.ops.object.convert(target="MESH")
    pt = bpy.context.active_object
    simple(pt, M[tipmat])
    parent_to(pt, head)

    ## blanket stitches: thread ticks crossing the panel's two long edges
    ca = math.radians(-8)
    for pside in (-1, 1):
        pcx, pcz = pside * r_p * 0.87, -h_p / 2
        ptx, ptz = 0.0, h_p / 2 - 0.01
        pdx, pdz = ptx - pcx, ptz - pcz
        pl = math.hypot(pdx, pdz)
        qx, qz = pdz / pl, -pdx / pl
        for i in range(4):
            t = (i + 0.5) / 4
            llx = pcx + pdx * t
            llz = pcz + pdz * t
            lly = -0.009
            ry = lly * math.cos(ca) - llz * math.sin(ca)
            rz = lly * math.sin(ca) + llz * math.cos(ca)
            bwx = ppx + llx * math.cos(th) + rz * math.sin(th)
            bwy = ppy + ry
            bwz = ppz - llx * math.sin(th) + rz * math.cos(th)
            qxw = qx * math.cos(th) + qz * math.sin(th)
            qzw = -qx * math.sin(th) + qz * math.cos(th)
            tick = cyl((bwx, bwy, bwz), 0.0024, 0.017,
                       rot=(math.radians(random.uniform(-8, 8)),
                            math.atan2(qxw, qzw), 0))
            tick.name = f"{nm}Blanket{pside}_{i}"
            ear_ticks.append(tick)

    ## one object per stitch family: a clean outliner, no parent-line spider web
    stj = join(ear_staples, nm + "EdgeStitches")
    simple(stj, M["StitchSteel"])
    parent_to(stj, head)
    tkj = join(ear_ticks, nm + "BlanketStitches")
    simple(tkj, M["ButtonBrown"])
    parent_to(tkj, head)

    ## fur crowding the back and rim; the felt front stays bald to show its sewing
    efur = fur(e, 2200, 0.024, 0.052, nm + "Fur", [M["FurDark"], M["FurMid"], M["FurRust"]],
               mask=lambda wp: wp.y < -0.005)
    if efur:
        parent_to(efur, head)



# LEFT EYE: gear-rosette button sitting PROUD of the cloth (surface y≈-0.35),
# four holes, scorch rays hugging the fabric, one melt drip
lring = cyl((-0.15, -0.365, 2.38), 0.085, 0.014, rot=(math.radians(80), 0, 0))
lring.name = "SocketL"
simple(lring, M["BronzeChar"])
parent_to(lring, head)
for gb in range(10):
    ga = math.radians(36 * gb)
    gear = sphere((-0.15 + 0.082 * math.cos(ga), -0.365, 2.38 + 0.082 * math.sin(ga) * 0.95), 0.007)
    gear.name = f"GearTooth{gb}"
    simple(gear, M["BronzeChar"])
    parent_to(gear, head)
btn = cyl((-0.15, -0.375, 2.38), 0.054, 0.014, rot=(math.radians(80), 0, 0))
btn.name = "ButtonEye"
simple(btn, M["ButtonBrown"])
parent_to(btn, head)
for hx, hz in ((-0.016, 0.016), (0.016, 0.016), (-0.016, -0.016), (0.016, -0.016)):
    hole = cyl((-0.15 + hx, -0.384, 2.38 + hz), 0.006, 0.008, rot=(math.radians(80), 0, 0))
    hole.name = f"BtnHole{hx}_{hz}"
    simple(hole, M["CharDark"])
    parent_to(hole, head)
for st in range(6):
    sa = math.radians(60 * st + 22)
    ray = cyl((-0.15 + 0.095 * math.cos(sa), -0.352, 2.38 + 0.095 * math.sin(sa) * 0.9), 0.009, 0.05,
              rot=(math.radians(90), 0, -sa))
    ray.name = f"ScorchRay{st}"
    simple(ray, M["CharDark"])
    parent_to(ray, head)
melt = sphere((-0.165, -0.36, 2.33), 0.02, (1.0, 0.5, 1.6))
melt.name = "MeltDrip"
simple(melt, M["ButtonBrown"])
parent_to(melt, head)

# RIGHT EYE: the tally lens assembly, sitting PROUD of the face cloth like the
# plate's camera lens — the face surface is at y≈-0.35, so the ring fronts at ~-0.39
oring = torus((0.13, -0.37, 2.34), 0.085, 0.024, rot=(math.radians(80), 0, 0))
oring.name = "LensRing"
simple(oring, M["CopperRing"])
parent_to(oring, head)
## the barrel is a REAL salvaged camera lens — Poly Haven Camera_01 (CC0),
## appended, cut down to the barrel alone (front glass removed so the tally
## core burns visibly inside), scaled up and seated in the sewn copper mount
CAM_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "modelsrc", "Camera_01", "Camera_01_1k.blend")
with bpy.data.libraries.load(CAM_SRC) as (_df, _dt):
    _dt.objects = ["Camera_01"]
lens_ob = _dt.objects[0]
col.objects.link(lens_ob)
lens_ob.name = "TallyLens"
import bmesh as _bmesh
lm = lens_ob.data
keep_idx = {i for i, ms in enumerate(lm.materials) if "lens_body" in ms.name}
bm2 = _bmesh.new()
bm2.from_mesh(lm)
bm2.faces.ensure_lookup_table()
doomed = []
for f in bm2.faces:
    c = f.calc_center_median()
    in_barrel = (f.material_index in keep_idx and c.y < -0.005
                 and ((c.x - 0.008) ** 2 + (c.z - 0.034) ** 2) ** 0.5 < 0.033)
    if not in_barrel:
        doomed.append(f)
_bmesh.ops.delete(bm2, geom=doomed, context="FACES")
bm2.to_mesh(lm)
bm2.free()
_ls = 2.75
lens_ob.scale = (_ls, _ls, _ls)
lens_ob.location = (0.13 - 0.008 * _ls, -0.2425, 2.34 - 0.034 * _ls)
parent_to(lens_ob, head)
for _lmat in lens_ob.data.materials:
    if _lmat and _lmat.use_nodes:
        for _n in _lmat.node_tree.nodes:
            if _n.type == "TEX_IMAGE" and _n.image:
                try:
                    _n.image.pack()
                except Exception:
                    pass
        ## soot the salvaged barrel: dims the donor lens's crisp white
        ## engraving to fire-worn ghosts (and keeps stray branding illegible)
        if "lens_body" in _lmat.name:
            _nt = _lmat.node_tree
            _b = next((n for n in _nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
            _link = next((l for l in _nt.links
                          if _b is not None and l.to_node == _b
                          and l.to_socket.name == "Base Color"), None)
            if _link is not None:
                _src = _link.from_socket
                _mx = _nt.nodes.new("ShaderNodeMixRGB")
                _mx.blend_type = "MULTIPLY"
                _mx.inputs["Fac"].default_value = 0.8
                _mx.inputs["Color2"].default_value = (0.3, 0.26, 0.24, 1.0)
                _nt.links.new(_src, _mx.inputs["Color1"])
                _nt.links.new(_mx.outputs["Color"], _b.inputs["Base Color"])
for rv in range(8):
    ra = math.radians(45 * rv)
    rivet = sphere((0.13 + 0.092 * math.cos(ra), -0.375, 2.34 + 0.092 * math.sin(ra) * 0.96), 0.01)
    rivet.name = f"LensRivet{rv}"
    simple(rivet, M["RodMetal"])
    parent_to(rivet, head)

# nose: the plate's wide felt triangle pad, apex down, softened by remesh
nose = cone((0, -0.415, 2.322), 0.05, 0.05, scale=(1.1, 0.62, 1.0), rot=(math.radians(180), 0, 0))
nose.name = "Nose"
nrm_ = nose.modifiers.new("remesh", "REMESH")
nrm_.mode = "VOXEL"
nrm_.voxel_size = 0.005
nd_ = nose.modifiers.new("soft", "DISPLACE")
nd_.texture = lump
nd_.strength = 0.0035
bpy.ops.object.convert(target="MESH")
nose = bpy.context.active_object
nose.name = "Nose"
simple(nose, M["NoseWax"])
bpy.ops.object.shade_smooth()
parent_to(nose, head)

# ---- THE MAW: recessed void, rolled leather lips, rooted teeth --------------------------
# The void hugs just inside the lip line — oversized, it used to bulge past
# the corners and read as a shapeless blob
maw = sphere((0, -0.29, 2.19), 0.24, (1.06, 0.47, 0.44))
maw.name = "MawVoid"
simple(maw, M["MawBlack"])
parent_to(maw, head)

def maw_pt(ang_deg):
    a = math.radians(ang_deg)
    px = 0.24 * math.cos(a)
    b = 0.095 if math.sin(a) > 0.0 else 0.06
    pz = 2.18 + b * math.sin(a) + 0.032 * math.cos(a) ** 2
    py = -(0.415 - 0.1 * abs(math.cos(a)))   # wrap onto the muzzle's curve
    return px, py, pz

# THE MOUTH, per the plate: continuous rolled leather lips, dense staples,
# teeth rooted in the lip, dark machinery behind
def lip_tube(prefix, angs, parent_obj, dy=0.0, dz=0.0, r=0.02):
    """One bevelled curve along the maw edge — a rolled leather lip, replacing
    the box-chain that read as a run of bronze bricks."""
    pts = [maw_pt(a) for a in angs]
    cu = bpy.data.curves.new(prefix + "Curve", type="CURVE")
    cu.dimensions = "3D"
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for i, (px, py, pz) in enumerate(pts):
        sp.points[i].co = (px, py + dy, pz + dz, 1.0)
    cu.bevel_depth = r
    cu.bevel_resolution = 6
    cu.use_fill_caps = True
    ob = bpy.data.objects.new(prefix, cu)
    col.objects.link(ob)
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.convert(target="MESH")
    ob = bpy.context.active_object
    ob.name = prefix
    simple(ob, M["LipLeather"])
    parent_to(ob, parent_obj)
    return ob

upper_angs = [10 + (160.0 / 31) * i for i in range(32)]
lip_tube("LipU", upper_angs, head, dy=-0.004, r=0.012)
## dense staples crossing the upper lip
staple_angs = [12 + (156.0 / 25) * i for i in range(26)]
staples_u = []
for i, ang in enumerate(staple_angs):
    px, py, pz = maw_pt(ang)
    st = cyl((px, py - 0.014, pz), 0.004, 0.028,
             rot=(math.radians(random.uniform(-6, 6)), 0, math.radians(random.uniform(-8, 8))))
    st.name = f"StapleU{i}"
    staples_u.append(st)
stj_u = join(staples_u, "LipStaplesU")
simple(stj_u, M["StitchSteel"])
parent_to(stj_u, head)
## TEETH: pale slats rooted in the upper lip, hanging into the dark —
## uneven, two knocked out, one snapped to a stub
tooth_angs = [24 + (132.0 / 12) * i for i in range(13)]
for i, ta in enumerate(tooth_angs):
    if i in (2, 10):
        continue
    px, py, pz = maw_pt(ta)
    tl = random.uniform(0.075, 0.11)
    if i == 4:
        tl = 0.036
    ty = py + 0.008
    bpy.ops.mesh.primitive_cube_add(size=1, location=(px * 0.97, ty, pz - 0.016 - tl / 2))
    ob = bpy.context.active_object
    ob.scale = (random.uniform(0.013, 0.019), 0.011, tl)
    ob.rotation_euler = (math.radians(random.uniform(-4, 4)), 0, math.radians(random.uniform(-7, 7)))
    ob.name = f"ToothU{i}"
    simple(ob, M["ToothBone"])
    parent_to(ob, head)
## the machinery glimpsed inside: dark slats just proud of the void's face
for gi in range(7):
    gx = -0.15 + 0.05 * gi
    bpy.ops.mesh.primitive_cube_add(size=1, location=(gx, -0.378, 2.1))
    ob = bpy.context.active_object
    ob.scale = (0.016, 0.02, 0.1)
    ob.name = f"Grille{gi}"
    simple(ob, M["GrilleDark"])
    parent_to(ob, head)

## the hand lever inside the mouth (dossier detail 4): the grip Chum works
## his own jaw with, glimpsed behind the staple bands when the maw hangs open
lrod = cyl((0.115, -0.355, 2.075), 0.01, 0.13, rot=(math.radians(-14), 0, 0))
lrod.name = "MouthLeverRod"
simple(lrod, M["RodMetal"])
parent_to(lrod, head)
lgrip = sphere((0.115, -0.372, 2.14), 0.021, (1.0, 0.8, 0.7))
lgrip.name = "MouthLeverGrip"
simple(lgrip, M["LeatherCol"])
parent_to(lgrip, head)

# whiskers: kinked straw bundles rooted on the muzzle, per the plate.
# Each is two chained segments with a bend; the left side burned shorter.
def whisker(sx, k, base_len, matname):
    rooty = -0.33
    rootz = 2.21 + 0.038 * k
    rootx = 0.29 * sx
    a1 = math.radians((62 + 5 * k) * sx)
    tilt1 = math.radians(9 * (k - 1.5))
    seg1 = cyl((rootx + 0.5 * base_len * 0.5 * math.sin(a1), rooty, rootz + 0.5 * base_len * 0.5 * math.sin(tilt1)),
               0.0042, base_len * 0.5, rot=(tilt1, a1, 0))
    seg1.name = f"Whisk{matname}{sx}_{k}a"
    simple(seg1, M[matname])
    parent_to(seg1, head)
    a2 = a1 + math.radians(14 * sx)
    tilt2 = tilt1 - math.radians(13)
    bx = rootx + base_len * 0.44 * math.sin(a1)
    bz = rootz + base_len * 0.44 * math.sin(tilt1)
    seg2 = cyl((bx + 0.5 * base_len * 0.55 * math.sin(a2), rooty, bz + 0.5 * base_len * 0.55 * math.sin(tilt2)),
               0.0028, base_len * 0.55, rot=(tilt2, a2, 0))
    seg2.name = f"Whisk{matname}{sx}_{k}b"
    simple(seg2, M[matname])
    parent_to(seg2, head)

for k in range(4):
    whisker(-1, k, 0.24 + 0.05 * (k % 2), "StubWhisker")
for k in range(4):
    whisker(1, k, 0.4 + 0.08 * (k % 3), "WireWhisker")

# ---- THE JAW ------------------------------------------------------------------------------
jaw = empty("Jaw", (0, 0.06, 2.1), parent=head)
jawvoid = sphere((0, -0.27, 2.135), 0.21, (0.98, 0.4, 0.25))
jawvoid.name = "JawVoid"
simple(jawvoid, M["MawBlack"])
parent_to(jawvoid, jaw)
jawmesh = sphere((0, -0.24, 2.03), 0.19, (1.12, 0.9, 0.26))
jawmesh.name = "JawMesh"
rmj = jawmesh.modifiers.new("remesh", "REMESH")
rmj.mode = "VOXEL"
rmj.voxel_size = 0.022
dj = jawmesh.modifiers.new("lump", "DISPLACE")
dj.texture = lump
dj.strength = 0.012
bpy.ops.object.convert(target="MESH")
jawmesh = bpy.context.active_object
simple(jawmesh, M["BurntWool"])
BAKES.append(jawmesh)
parent_to(jawmesh, jaw)
jaw_fur = fur(jawmesh, 320, 0.02, 0.05, "JawFur", [M["FurDark"], M["FurMid"]],
              mask=lambda wp: wp.z > 2.05 and wp.y < -0.26)
if jaw_fur:
    parent_to(jaw_fur, jaw)
lower_angs = [200 + (140.0 / 27) * i for i in range(28)]
lip_tube("LipL", lower_angs, jaw, dy=-0.002, dz=0.045, r=0.011)
staple_angs_l = [204 + (132.0 / 19) * i for i in range(20)]
staples_l = []
for i, ang in enumerate(staple_angs_l):
    px, py, pz = maw_pt(ang)
    st = cyl((px * 0.96, py - 0.012, pz + 0.045), 0.004, 0.026,
             rot=(math.radians(random.uniform(-6, 6)), 0, math.radians(random.uniform(-8, 8))))
    st.name = f"StapleL{i}"
    staples_l.append(st)
stj_l = join(staples_l, "LipStaplesL")
simple(stj_l, M["StitchSteel"])
parent_to(stj_l, jaw)
## a few lower teeth rising from the jaw lip, shorter, crooked
for i, ta in enumerate((236, 265, 292, 318)):
    px, py, pz = maw_pt(ta)
    tl = random.uniform(0.035, 0.052)
    ty = py + 0.014
    bpy.ops.mesh.primitive_cube_add(size=1, location=(px * 0.95, ty, pz + 0.035 + tl / 2))
    ob = bpy.context.active_object
    ob.scale = (random.uniform(0.012, 0.017), 0.011, tl)
    ob.rotation_euler = (math.radians(random.uniform(-4, 4)), 0, math.radians(random.uniform(-8, 8)))
    ob.name = f"ToothL{i}"
    simple(ob, M["ToothBone"])
    parent_to(ob, jaw)
## the riveted chin strap (manual jaw hinge assembly)
for ci in range(9):
    ca = math.radians(210 + 15 * ci)
    cx = 0.24 * math.cos(ca)
    cz = 2.1 + 0.075 * math.sin(ca)
    cyy = -(0.4 - 0.1 * abs(math.cos(ca)))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cyy, cz - 0.035))
    ob = bpy.context.active_object
    ob.scale = (0.05, 0.016, 0.024)
    ob.rotation_euler = (0, math.radians(math.degrees(ca) * 0.06), 0)
    ob.name = f"ChinBand{ci}"
    simple(ob, M["BronzeBand"])
    parent_to(ob, jaw)
    if ci % 2 == 0:
        rv = sphere((cx, cyy - 0.012, cz - 0.035), 0.008)
        rv.name = f"ChinRivet{ci}"
        simple(rv, M["CopperRing"])
        parent_to(rv, jaw)
## hinge bolts at the mouth corners
for sx in (-1, 1):
    bolt = cyl((0.28 * sx, -0.3, 2.17), 0.02, 0.05, rot=(0, math.radians(90), 0))
    bolt.name = f"HingeBolt{sx}"
    simple(bolt, M["CopperRing"])
    parent_to(bolt, head)
for bz, brad in ((2.1, 0.17), (2.06, 0.14)):
    bar = torus((0, -0.24, bz), brad, 0.011, rot=(math.radians(84), 0, 0))
    bar.name = f"JawBar{bz}"
    simple(bar, M["RodMetal"])
    parent_to(bar, jaw)
lever = cyl((0.09, -0.16, 1.95), 0.014, 0.3, rot=(math.radians(20), 0, 0))
lever.name = "JawLever"
simple(lever, M["RodMetal"])
parent_to(lever, jaw)

# ---- THE BAKE: procedural burlap, scorch, and grime, baked to textures -----------------
# Every fabric part gets a real Cycles material — woven fiber, dye mottling,
# soot pooling in the crevices — UV-unwrapped and baked to maps the glb carries.

TEXSRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "texsrc")
SCANS = {
    "wool":    ("Fabric031/Fabric031_1K-JPG_Color.jpg", "Fabric031/Fabric031_1K-JPG_NormalGL.jpg", "Fabric031/Fabric031_1K-JPG_Roughness.jpg"),
    "weave":   ("Fabric030/Fabric030_1K-JPG_Color.jpg", "Fabric030/Fabric030_1K-JPG_NormalGL.jpg", "Fabric030/Fabric030_1K-JPG_Roughness.jpg"),
    "leather": ("Leather030/Leather030_1K-JPG_Color.jpg", "Leather030/Leather030_1K-JPG_NormalGL.jpg", "Leather030/Leather030_1K-JPG_Roughness.jpg"),
    ## Phase 1 scans (tools/fetch_scans.py; CC0; credited in texsrc/CREDITS.md)
    "boucle":    ("wool_boucle/wool_boucle_Diffuse_2k.jpg", "wool_boucle/wool_boucle_nor_gl_2k.jpg", "wool_boucle/wool_boucle_Rough_2k.jpg"),
    "teddy":     ("curly_teddy_natural/curly_teddy_natural_Diffuse_2k.jpg", "curly_teddy_natural/curly_teddy_natural_nor_gl_2k.jpg", "curly_teddy_natural/curly_teddy_natural_Rough_2k.jpg"),
    "hessian":   ("hessian_230/hessian_230_Diffuse_2k.jpg", "hessian_230/hessian_230_nor_gl_2k.jpg", "hessian_230/hessian_230_Rough_2k.jpg"),
    "corduroy":  ("ribbed_corduroy/ribbed_corduroy_Diffuse_2k.jpg", "ribbed_corduroy/ribbed_corduroy_nor_gl_2k.jpg", "ribbed_corduroy/ribbed_corduroy_Rough_2k.jpg"),
    "denim":     ("denim_fabric_06/denim_fabric_06_Diffuse_2k.jpg", "denim_fabric_06/denim_fabric_06_nor_gl_2k.jpg", "denim_fabric_06/denim_fabric_06_Rough_2k.jpg"),
    "plate":     ("metal_plate_02/metal_plate_02_Diffuse_2k.jpg", "metal_plate_02/metal_plate_02_nor_gl_2k.jpg", "metal_plate_02/metal_plate_02_Rough_2k.jpg"),
    "plaid":     ("Fabric080/Fabric080_2K-JPG_Color.jpg", "Fabric080/Fabric080_2K-JPG_NormalGL.jpg", "Fabric080/Fabric080_2K-JPG_Roughness.jpg"),
    "greenwool": ("Fabric018/Fabric018_2K-JPG_Color.jpg", "Fabric018/Fabric018_2K-JPG_NormalGL.jpg", "Fabric018/Fabric018_2K-JPG_Roughness.jpg"),
    "bark":      ("Bark015/Bark015_2K-JPG_Color.jpg", "Bark015/Bark015_2K-JPG_NormalGL.jpg", "Bark015/Bark015_2K-JPG_Roughness.jpg"),
    "rustleak":  ("Rust009/Rust009_2K-JPG_Color.jpg", "Rust009/Rust009_2K-JPG_NormalGL.jpg", "Rust009/Rust009_2K-JPG_Roughness.jpg"),
}
SCORCH_MASK = os.path.join(TEXSRC, "Metal058A/Metal058A_1K-JPG_Color.jpg")
_img_cache = {}

def scan_img(rel, noncolor=False):
    path = rel if os.path.isabs(rel) else os.path.join(TEXSRC, rel)
    key = (path, noncolor)
    if key in _img_cache:
        return _img_cache[key]
    img = bpy.data.images.load(path, check_existing=False)
    if noncolor:
        img.colorspace_settings.name = "Non-Color"
    _img_cache[key] = img
    return img


## dress a flat material in a scan, box-projected: the same Metal058A grime
## ages every alloy; Leather030 wraps the grips. Pure asset reuse — the tint
## multiply keeps each material's authored palette.
def scan_dress(mm, col_rel, nrm_rel, val_mult=2.2, scale=5.0, nstr=0.8):
    dnt = mm.node_tree
    db = dnt.nodes["Principled BSDF"]
    base = tuple(db.inputs["Base Color"].default_value)[:3]
    dco = dnt.nodes.new("ShaderNodeTexCoord")
    dmp = dnt.nodes.new("ShaderNodeMapping")
    dmp.inputs["Scale"].default_value = (scale, scale, scale)
    dnt.links.new(dco.outputs["Object"], dmp.inputs["Vector"])
    dtc = dnt.nodes.new("ShaderNodeTexImage")
    dtc.image = scan_img(col_rel)
    dtc.projection = "BOX"
    dtc.projection_blend = 0.3
    dnt.links.new(dmp.outputs["Vector"], dtc.inputs["Vector"])
    dmx = dnt.nodes.new("ShaderNodeMixRGB")
    dmx.blend_type = "MULTIPLY"
    dmx.inputs["Fac"].default_value = 1.0
    dnt.links.new(dtc.outputs["Color"], dmx.inputs["Color1"])
    dmx.inputs["Color2"].default_value = (base[0] * val_mult, base[1] * val_mult,
                                          base[2] * val_mult, 1.0)
    dnt.links.new(dmx.outputs["Color"], db.inputs["Base Color"])
    dtn = dnt.nodes.new("ShaderNodeTexImage")
    dtn.image = scan_img(nrm_rel, noncolor=True)
    dtn.projection = "BOX"
    dtn.projection_blend = 0.3
    dnt.links.new(dmp.outputs["Vector"], dtn.inputs["Vector"])
    dnm = dnt.nodes.new("ShaderNodeNormalMap")
    dnm.inputs["Strength"].default_value = nstr
    dnt.links.new(dtn.outputs["Color"], dnm.inputs["Color"])
    dnt.links.new(dnm.outputs["Normal"], db.inputs["Normal"])


for _mk in ("BronzeBand", "BronzeChar", "CopperRing", "StitchSteel",
            "RodMetal", "Brass"):
    scan_dress(M[_mk], "Metal058A/Metal058A_1K-JPG_Color.jpg",
               "Metal058A/Metal058A_1K-JPG_NormalGL.jpg", 2.2, 5.0, 0.8)
## the mouth grille stays SHADOW machinery: same scan, a third the value —
## at 2.2 it rendered as cream pickets inside the maw
scan_dress(M["GrilleDark"], "Metal058A/Metal058A_1K-JPG_Color.jpg",
           "Metal058A/Metal058A_1K-JPG_NormalGL.jpg", 0.7, 5.0, 0.8)
for _mk in ("LeatherCol", "PatchLeather"):
    scan_dress(M[_mk], "Leather030/Leather030_1K-JPG_Color.jpg",
               "Leather030/Leather030_1K-JPG_NormalGL.jpg", 2.6, 8.0, 1.0)
## the lips: same leather scan, kept burnt-dark
scan_dress(M["LipLeather"], "Leather030/Leather030_1K-JPG_Color.jpg",
           "Leather030/Leather030_1K-JPG_NormalGL.jpg", 1.1, 10.0, 1.0)


def burlap_nodes(matr, tint_srgb, scorch, scan_key, scale):
    """Scanned cloth (CC0, ambientCG) layered with procedural age: tinted
    albedo, real weave normals, smudge-scan burn blotches, AO soot."""
    tint = tuple(srgb_to_linear(c) for c in tint_srgb)
    matr.use_nodes = True
    nt = matr.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (scale, scale, scale)
    nt.links.new(coord.outputs["Object"], mapping.inputs["Vector"])

    col_rel, nrm_rel, rgh_rel = SCANS[scan_key]
    tcol = nt.nodes.new("ShaderNodeTexImage")
    tcol.image = scan_img(col_rel)
    tcol.projection = "BOX"
    tcol.projection_blend = 0.3
    nt.links.new(mapping.outputs["Vector"], tcol.inputs["Vector"])
    tnrm = nt.nodes.new("ShaderNodeTexImage")
    tnrm.image = scan_img(nrm_rel, noncolor=True)
    tnrm.projection = "BOX"
    tnrm.projection_blend = 0.3
    nt.links.new(mapping.outputs["Vector"], tnrm.inputs["Vector"])
    trgh = nt.nodes.new("ShaderNodeTexImage")
    trgh.image = scan_img(rgh_rel, noncolor=True)
    trgh.projection = "BOX"
    trgh.projection_blend = 0.3
    nt.links.new(mapping.outputs["Vector"], trgh.inputs["Vector"])

    ## tint the scan: multiply toward the palette, keep the weave's variance
    tinted = nt.nodes.new("ShaderNodeMixRGB")
    tinted.blend_type = "MULTIPLY"
    tinted.inputs["Fac"].default_value = 1.0
    nt.links.new(tcol.outputs["Color"], tinted.inputs["Color1"])
    tinted.inputs["Color2"].default_value = (tint[0] * 0.9, tint[1] * 0.9, tint[2] * 0.9, 1.0)

    ## the burn: the smudge scan, box-projected large, thresholded
    mmap = nt.nodes.new("ShaderNodeMapping")
    mmap.inputs["Scale"].default_value = (0.55, 0.55, 0.55)
    nt.links.new(coord.outputs["Object"], mmap.inputs["Vector"])
    tmask = nt.nodes.new("ShaderNodeTexImage")
    tmask.image = scan_img(SCORCH_MASK, noncolor=True)
    tmask.projection = "BOX"
    tmask.projection_blend = 0.3
    nt.links.new(mmap.outputs["Vector"], tmask.inputs["Vector"])
    ## TEXEL FINDING (unit 1.1b): the mask is a BRIGHT copper smudge, so the old
    ## thresholds burned 40-100% of every texel whatever `scorch` was — every
    ## bake on the puppet measured the same (0.05, 0.04, 0.03), the head 0.02.
    ## Now `scorch` IS the burn fraction: only the brightest smudges fire, and
    ## the ramp is scaled by scorch, so a 0.2 patch keeps its colour and a
    ## 0.88 body still chars in mottled zones.
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.55
    ramp.color_ramp.elements[1].position = 0.85
    nt.links.new(tmask.outputs["Color"], ramp.inputs["Fac"])
    burnfac = nt.nodes.new("ShaderNodeMath")
    burnfac.operation = "MULTIPLY"
    nt.links.new(ramp.outputs["Color"], burnfac.inputs[0])
    burnfac.inputs[1].default_value = scorch
    burn = nt.nodes.new("ShaderNodeMixRGB")
    burn.blend_type = "MIX"
    burn.inputs["Color2"].default_value = (0.01, 0.008, 0.006, 1.0)
    nt.links.new(burnfac.outputs["Value"], burn.inputs["Fac"])
    nt.links.new(tinted.outputs["Color"], burn.inputs["Color1"])

    ## soot in the crevices
    ao = nt.nodes.new("ShaderNodeAmbientOcclusion")
    ao.inputs["Distance"].default_value = 0.08
    soot = nt.nodes.new("ShaderNodeMixRGB")
    soot.blend_type = "MULTIPLY"
    soot.inputs["Fac"].default_value = 0.30 + 0.35 * scorch   # soot follows the burn
    nt.links.new(burn.outputs["Color"], soot.inputs["Color1"])
    nt.links.new(ao.outputs["Color"], soot.inputs["Color2"])

    ## mid-scale grime: the smudge scan again, larger, as handled-for-decades dirt
    gmap = nt.nodes.new("ShaderNodeMapping")
    gmap.inputs["Scale"].default_value = (1.7, 1.7, 1.7)
    nt.links.new(coord.outputs["Object"], gmap.inputs["Vector"])
    gtex = nt.nodes.new("ShaderNodeTexImage")
    gtex.image = scan_img(SCORCH_MASK, noncolor=True)
    gtex.projection = "BOX"
    gtex.projection_blend = 0.3
    nt.links.new(gmap.outputs["Vector"], gtex.inputs["Vector"])
    grime = nt.nodes.new("ShaderNodeMixRGB")
    grime.blend_type = "MULTIPLY"
    grime.inputs["Fac"].default_value = 0.2
    nt.links.new(soot.outputs["Color"], grime.inputs["Color1"])
    nt.links.new(gtex.outputs["Color"], grime.inputs["Color2"])
    nt.links.new(grime.outputs["Color"], bsdf.inputs["Base Color"])

    ## roughness: the scan, pushed matte, charred zones fully rough
    rmath = nt.nodes.new("ShaderNodeMath")
    rmath.operation = "MULTIPLY_ADD"
    nt.links.new(trgh.outputs["Color"], rmath.inputs[0])
    rmath.inputs[1].default_value = 0.22
    rmath.inputs[2].default_value = 0.74
    nt.links.new(rmath.outputs["Value"], bsdf.inputs["Roughness"])

    ## normals: the scanned weave, with grunge bump layered on top
    nmap = nt.nodes.new("ShaderNodeNormalMap")
    nmap.inputs["Strength"].default_value = 2.1
    nt.links.new(tnrm.outputs["Color"], nmap.inputs["Color"])
    bmp = nt.nodes.new("ShaderNodeBump")
    bmp.inputs["Strength"].default_value = 0.3
    bmp.inputs["Distance"].default_value = 0.003
    nt.links.new(tmask.outputs["Color"], bmp.inputs["Height"])
    nt.links.new(nmap.outputs["Normal"], bmp.inputs["Normal"])
    nt.links.new(bmp.outputs["Normal"], bsdf.inputs["Normal"])
    return bsdf


BAKE_TINTS = {
    "BurntWool": ((0.13, 0.1, 0.07), 0.88, "boucle", 7.0),   # fused, matted wool (BRIEF 1.1)
    "EarFelt": ((0.075, 0.058, 0.042), 0.92, "wool", 7.0),
    "BellyWool": ((0.36, 0.29, 0.18), 0.3, "boucle", 8.0),
    "PatchRust": ((0.62, 0.24, 0.13), 0.22, "boucle", 12.0),
    "PatchGreen": ((0.22, 0.32, 0.22), 0.5, "weave", 14.0),
    "PatchOlive": ((0.75, 0.85, 0.65), 0.2, "corduroy", 14.0),   # near-neutral: the scan carries the green
    "PatchNavy": ((0.8, 0.85, 1.0), 0.22, "denim", 14.0),
    "PatchOchre": ((0.68, 0.5, 0.24), 0.22, "boucle", 12.0),
    "PatchBrown": ((0.26, 0.18, 0.12), 0.35, "weave", 14.0),
    "PatchPlaid": ((0.85, 0.8, 0.75), 0.2, "plaid", 12.0),
    "PatchFlannel": ((0.48, 0.48, 0.5), 0.35, "weave", 16.0),   # stage delta — unused on the mascot
    "PatchLeather": ((0.35, 0.28, 0.22), 0.2, "leather", 12.0), # stage delta — unused on the mascot
    "CharDark": ((0.12, 0.1, 0.085), 0.82, "wool", 10.0),
    "PanelA": ((0.17, 0.13, 0.09), 0.72, "wool", 11.0),
    "PanelB": ((0.2, 0.16, 0.11), 0.66, "wool", 12.0),
    "PanelC": ((0.15, 0.115, 0.08), 0.76, "wool", 10.0),
}

def bake_all():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 2
    scene.render.bake.margin = 6
    for obj in BAKES:
        mname = obj.data.materials[0].name.split(".")[0]
        if mname not in BAKE_TINTS:
            continue
        tint, scorch, scan_key, wscale = BAKE_TINTS[mname]
        res = 2048 if len(obj.data.vertices) > 1500 else 1024
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.03)   # BRIEF 1.1 step 7: kill the black-glass margins
        bpy.ops.object.mode_set(mode="OBJECT")
        matr = bpy.data.materials.new(obj.name + "_baked_src")
        burlap_nodes(matr, tint, scorch, scan_key, wscale)
        obj.data.materials.clear()
        obj.data.materials.append(matr)
        nt = matr.node_tree
        imgs = {}
        for kind, cs in (("diff", "sRGB"), ("nrm", "Non-Color"), ("rgh", "Non-Color")):
            img = bpy.data.images.new(f"{obj.name}_{kind}", res, res, alpha=False)
            img.colorspace_settings.name = cs
            imgs[kind] = img
        tex_node = nt.nodes.new("ShaderNodeTexImage")
        # bake the three maps
        for kind, btype, extra in (("diff", "DIFFUSE", {"pass_filter": {"COLOR"}}),
                                   ("nrm", "NORMAL", {}),
                                   ("rgh", "ROUGHNESS", {})):
            tex_node.image = imgs[kind]
            nt.nodes.active = tex_node
            bpy.ops.object.bake(type=btype, margin=6, **extra)
        # the export material: baked maps into a clean Principled
        final = bpy.data.materials.new(mname)   # keep the canonical name
        final.use_nodes = True
        fnt = final.node_tree
        fb = fnt.nodes["Principled BSDF"]
        td = fnt.nodes.new("ShaderNodeTexImage")
        td.image = imgs["diff"]
        fnt.links.new(td.outputs["Color"], fb.inputs["Base Color"])
        tr = fnt.nodes.new("ShaderNodeTexImage")
        tr.image = imgs["rgh"]
        fnt.links.new(tr.outputs["Color"], fb.inputs["Roughness"])
        tn = fnt.nodes.new("ShaderNodeTexImage")
        tn.image = imgs["nrm"]
        nm = fnt.nodes.new("ShaderNodeNormalMap")
        fnt.links.new(tn.outputs["Color"], nm.inputs["Color"])
        fnt.links.new(nm.outputs["Normal"], fb.inputs["Normal"])
        obj.data.materials.clear()
        obj.data.materials.append(final)
        print("BAKED", obj.name, res)

# ---- THE SCALE LAW: one uniform scale, frozen BEFORE the bake --------------------------
## OWNER RULING 2026-09-05: the puppet is authored at the true 3.35 m with the
## tally eye at 3.0 m, actor scale 1.0. Every number above is in the 2.6 m base
## space the build was written in; this applies 3.35/2.6 to the whole assembly
## and freezes it into the mesh data — never per-bone. Before the bake, so the
## box-projected scans keep their physical repeat (a 3.35 m coat carries more
## weave than a 2.6 m one — that is scale truth).
import mathutils
FINAL_SCALE = 3.35 / 2.6
_S = mathutils.Matrix.Scale(FINAL_SCALE, 4)
_all = list(bpy.context.scene.objects)
_target = {o: _S @ o.matrix_world.copy() for o in _all}
def _assign(o):
    o.matrix_world = _target[o]
    for c in o.children:
        _assign(c)
for _r in [o for o in _all if o.parent is None]:
    _assign(_r)
for o in _all:
    if o.type in ("MESH", "CURVE", "EMPTY"):
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        try:
            if o.type != "EMPTY" and o.data.users > 1:
                bpy.ops.object.make_single_user(type="SELECTED_OBJECTS", obdata=True)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        except RuntimeError as _ex:
            print("SCALE-APPLY skipped", o.name, _ex)
_bz = max((o.matrix_world @ mathutils.Vector(c)).z for o in _all if o.type == "MESH" for c in o.bound_box)
print("FINAL_SCALE %.4f applied; tallest mesh point z=%.3f m" % (FINAL_SCALE, _bz))

bake_all()

# ---- the real coat lives in the file: particle hair grown post-bake --------------------
# (bake_all clears material slots, so hair mats attach after; glTF export
# ignores particle hair, so the game glb only carries the cards)
def hair_mat(hname, melanin):
    hm = bpy.data.materials.new(hname)
    hm.use_nodes = True
    hnt = hm.node_tree
    hnt.nodes.clear()
    ho = hnt.nodes.new("ShaderNodeOutputMaterial")
    hb = hnt.nodes.new("ShaderNodeBsdfHairPrincipled")
    try:
        hb.parametrization = "MELANIN"
    except Exception:
        pass
    for nm_i, v in (("Melanin", melanin), ("Melanin Redness", 0.55), ("Roughness", 0.35),
                    ("Radial Roughness", 0.4), ("Random Color", 0.5), ("Random Roughness", 0.3)):
        try:
            hb.inputs[nm_i].default_value = v
        except Exception:
            pass
    hnt.links.new(hb.outputs[0], ho.inputs["Surface"])
    return hm

HAIR_DARK = hair_mat("CoatDark", 0.96)
HAIR_RUST = hair_mat("CoatRust", 0.82)

def hface_mask(wp):
    return wp.y < -0.26 and 2.02 < wp.z < 2.44 and abs(wp.x) < 0.3
def hjaw_mask(wp):
    return wp.z > 2.04
def hear_mask(wp):
    return wp.y < -0.005
def hbelly_mask(wp):
    return wp.y < -0.3 and 1.0 < wp.z < 1.8 and abs(wp.x) < 0.32
def hsole_mask(wp):
    return wp.z < 0.08

## 1.1b: no guide hair on the front of the torso (the quilt must read);
## the belly exclusion is kept. Masks are evaluated in 2.6 space.
hbody_mask = lambda wp: (wp.y < -0.10) or bool(hbelly_mask(wp))
BUILD_HAIR_PLAN = [
    ("Skull", 2600, 0.05, HAIR_DARK, hface_mask),
    ("EarL", 1400, 0.05, HAIR_RUST, hear_mask),
    ("EarR", 1600, 0.055, HAIR_RUST, hear_mask),
    ("JawMesh", 300, 0.03, HAIR_DARK, hjaw_mask),
    ("BodyCore", 1000, 0.03, HAIR_DARK, hbody_mask),
    ("ArmL", 700, 0.045, HAIR_DARK, None),
    ("ArmR", 700, 0.045, HAIR_DARK, None),
    ("LegL", 800, 0.05, HAIR_DARK, hsole_mask),
    ("LegR", 800, 0.05, HAIR_DARK, hsole_mask),
    ("Tail", 600, 0.055, HAIR_RUST, None),
]
for hnm, hcount, hlen, hmat, hmask in BUILD_HAIR_PLAN:
    hob = bpy.data.objects.get(hnm)
    if hob is None or hob.type != "MESH":
        continue
    hob.data.materials.append(hmat)
    hmat_index = len(hob.data.materials)
    if hmask is not None:
        vg = hob.vertex_groups.new(name="furdensity")
        mw = hob.matrix_world
        for v in hob.data.vertices:
            vg.add([v.index], 0.0 if hmask((mw @ v.co) / FINAL_SCALE) else 1.0, "REPLACE")   # masks are written in 2.6 space
    bpy.context.view_layer.objects.active = hob
    hob.modifiers.new("hair", "PARTICLE_SYSTEM")
    ps = hob.particle_systems[-1]
    st = ps.settings
    st.type = "HAIR"
    st.count = hcount
    st.hair_length = hlen * FINAL_SCALE
    st.material = hmat_index
    st.child_type = "INTERPOLATED"
    st.child_percent = 6
    try:
        st.rendered_child_count = 24
    except Exception:
        pass
    st.clump_factor = 0.72
    st.child_length = 0.9
    try:
        st.child_length_threshold = 0.3
    except Exception:
        pass
    try:
        st.root_radius = 0.7
        st.tip_radius = 0.15
        st.radius_scale = 0.0016
    except Exception:
        pass
    for attr, val in (("roughness_endpoint", 0.015), ("roughness_end_shape", 1.0),
                      ("roughness_2", 0.008), ("roughness_2_size", 1.4),
                      ("kink", "CURL"), ("kink_amplitude", 0.004), ("kink_frequency", 3.0)):
        try:
            setattr(st, attr, val)
        except Exception:
            pass
    if hmask is not None:
        ps.vertex_group_density = "furdensity"
    print("HAIR", hnm, hcount)

## short singed fuzz on the felt face plate itself — the plate's face is
## worn nap, not smooth cloth (reuses the same particle-hair machinery)
HAIR_FUZZ = hair_mat("CoatFuzz", 0.55)
fz_ob = bpy.data.objects.get("Skull")
if fz_ob:
    fz_ob.data.materials.append(HAIR_FUZZ)
    fzi = len(fz_ob.data.materials)
    fvg = fz_ob.vertex_groups.new(name="facefuzz")
    fmw = fz_ob.matrix_world
    for v in fz_ob.data.vertices:
        wp = fmw @ v.co
        inface = wp.y < -0.3 and 2.05 < wp.z < 2.42 and abs(wp.x) < 0.28
        fvg.add([v.index], 1.0 if inface else 0.0, "REPLACE")
    bpy.context.view_layer.objects.active = fz_ob
    fz_ob.modifiers.new("fuzzhair", "PARTICLE_SYSTEM")
    ps = fz_ob.particle_systems[-1]
    st = ps.settings
    st.type = "HAIR"
    st.count = 700
    st.hair_length = 0.011 * FINAL_SCALE
    st.material = fzi
    st.child_type = "INTERPOLATED"
    st.child_percent = 4
    try:
        st.rendered_child_count = 10
    except Exception:
        pass
    st.clump_factor = 0.3
    try:
        st.root_radius = 0.5
        st.tip_radius = 0.1
        st.radius_scale = 0.0012
    except Exception:
        pass
    ps.vertex_group_density = "facefuzz"
    print("HAIR FaceFuzz")

# ---- export ---------------------------------------------------------------------------------
os.makedirs(os.path.dirname(OUT), exist_ok=True)
BLEND = OUT.replace("chum_af.glb", "chum_af.blend").replace("assets/models", "blend")
os.makedirs(os.path.dirname(BLEND), exist_ok=True)
## pack the baked images into the .blend: without this, reopening the file
## loses every bake (black albedo, zero roughness — the black-glass face)
for img in bpy.data.images:
    if img.packed_file is None and not img.filepath:
        try:
            img.pack()
        except Exception:
            pass
## the file should OPEN looking like the puppet, not a grey thornbush:
## Material Preview shading, parent relationship lines off
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.shading.type = "MATERIAL"
                    space.overlay.show_relationship_lines = False
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print("SAVED", BLEND)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_apply=True)
print("WROTE", OUT)
