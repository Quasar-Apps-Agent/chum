"""AFTER-FIRE CHUM · beauty render (Cycles, real hair, the plate's language)

Run:  /Applications/Blender.app/Contents/MacOS/Blender --background --python tools/render_chum_af_beauty.py

Opens blend/chum_af.blend (the live build), swaps the game's ribbon fur for
real particle hair with a Principled Hair BSDF, adds subsurface to the cloth,
lights it like the dossier plate (HDRI + warm key + rim), and renders two
Cycles stills to renders/. This is the design-review image; the game keeps
its baked glb. Design in Cycles, ship baked.
"""
import bpy
import math
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BLEND = os.path.join(ROOT, "blend", "chum_af.blend")
HDRI = os.path.join(ROOT, "assets", "env", "workshop_1k.hdr")
OUTDIR = os.path.join(ROOT, "renders")
os.makedirs(OUTDIR, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=BLEND)
scene = bpy.context.scene

## the jaw hangs open the way the plate holds it
jaw_open = bpy.data.objects.get("Jaw")
if jaw_open:
    jaw_open.rotation_euler = (0.2, 0, 0)

# ---- Cycles on the GPU -----------------------------------------------------------
scene.render.engine = "CYCLES"
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    scene.cycles.device = "GPU"
    print("CYCLES: Metal GPU")
except Exception as ex:
    scene.cycles.device = "CPU"
    print("CYCLES: CPU fallback", ex)
scene.cycles.samples = 256
scene.cycles.use_denoising = True

# ---- hide the game's ribbon fur; Cycles grows the real coat -----------------------
for ob in bpy.data.objects:
    if "Fur" in ob.name or "Fuzz" in ob.name:
        ob.hide_render = True

# ---- hair material: burnt plush -----------------------------------------------------
def hair_mat(name, col, rand):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    h = nt.nodes.new("ShaderNodeBsdfHairPrincipled")
    try:
        h.parametrization = "COLOR"
    except Exception:
        pass
    try:
        h.parametrization = "MELANIN"
    except Exception:
        pass
    for nm_i, v in (("Color", (*col, 1.0)), ("Melanin", 0.96), ("Melanin Redness", 0.55),
                    ("Roughness", 0.35), ("Radial Roughness", 0.4),
                    ("Random Color", rand), ("Random Roughness", 0.3)):
        try:
            h.inputs[nm_i].default_value = v
        except Exception:
            pass
    nt.links.new(h.outputs[0], out.inputs["Surface"])
    return m

FUR_DARK = hair_mat("HairDark", (0.035, 0.024, 0.016), 0.4)
FUR_RUST = hair_mat("HairRust", (0.14, 0.05, 0.02), 0.55)

# ---- masks (world-space bald zones) -------------------------------------------------
def face_mask(wp):
    return wp.y < -0.26 and 2.02 < wp.z < 2.44 and abs(wp.x) < 0.3

def jaw_mask(wp):
    return wp.z > 2.04

def ear_front_mask(wp):
    return wp.y < -0.005

def belly_mask(wp):
    return wp.y < -0.3 and 1.0 < wp.z < 1.8 and abs(wp.x) < 0.32

def sole_mask(wp):
    return wp.z < 0.08

HAIR_PLAN = [
    ("Skull", 2600, 0.05, FUR_DARK, face_mask),
    ("EarL", 1400, 0.05, FUR_RUST, ear_front_mask),
    ("EarR", 1600, 0.055, FUR_RUST, ear_front_mask),
    ("JawMesh", 300, 0.03, FUR_DARK, jaw_mask),
    ("BodyCore", 3600, 0.06, FUR_DARK, belly_mask),
    ("ArmL", 700, 0.045, FUR_DARK, None),
    ("ArmR", 700, 0.045, FUR_DARK, None),
    ("LegL", 800, 0.05, FUR_DARK, sole_mask),
    ("LegR", 800, 0.05, FUR_DARK, sole_mask),
    ("Tail", 600, 0.055, FUR_RUST, None),
]

for nm, count, length, mat, mask in HAIR_PLAN:
    ob = bpy.data.objects.get(nm)
    if ob is None or ob.type != "MESH":
        print("skip", nm)
        continue
    if ob.particle_systems:
        print("hair already grown in build", nm)
        continue
    ob.data.materials.append(mat)
    mat_index = len(ob.data.materials)
    if mask is not None:
        vg = ob.vertex_groups.new(name="furdensity")
        mw = ob.matrix_world
        for v in ob.data.vertices:
            w = 0.0 if mask(mw @ v.co) else 1.0
            vg.add([v.index], w, "REPLACE")
    bpy.context.view_layer.objects.active = ob
    mod = ob.modifiers.new("hair", "PARTICLE_SYSTEM")
    ps = ob.particle_systems[-1]
    st = ps.settings
    st.type = "HAIR"
    st.count = count
    st.hair_length = length
    st.material = mat_index
    st.child_type = "INTERPOLATED"
    st.child_percent = 6
    try:
        st.rendered_child_count = 24
    except Exception:
        pass
    st.clump_factor = 0.72
    st.child_length = 0.9
    st.child_length_threshold = 0.3
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
    if mask is not None:
        ps.vertex_group_density = "furdensity"
    print("HAIR", nm, count, "x children")

# ---- cloth (only cloth) gets a whisper of subsurface, at fiber radius ------------------
CLOTH_PREFIXES = ("BurntWool", "BellyWool", "EarFelt", "Panel", "PatchRust", "PatchGreen", "PatchFlannel", "CharDark")
for m in bpy.data.materials:
    if not m.use_nodes:
        continue
    if not any(m.name.startswith(pfx) for pfx in CLOTH_PREFIXES):
        continue
    for n in m.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            for key in ("Subsurface Weight", "Subsurface"):
                try:
                    n.inputs[key].default_value = 0.04
                    break
                except Exception:
                    continue
            try:
                n.inputs["Subsurface Radius"].default_value = (0.015, 0.009, 0.006)
            except Exception:
                pass

# ---- the tally eye, burning -------------------------------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.017, location=(0.13, -0.4, 2.34))
eye = bpy.context.active_object
eye.name = "TallyEyeLive"
em = bpy.data.materials.new("TallyGlow")
em.use_nodes = True
nt = em.node_tree
nt.nodes.clear()
o = nt.nodes.new("ShaderNodeOutputMaterial")
e = nt.nodes.new("ShaderNodeEmission")
e.inputs["Color"].default_value = (1.0, 0.025, 0.008, 1.0)
e.inputs["Strength"].default_value = 20.0
nt.links.new(e.outputs[0], o.inputs["Surface"])
eye.data.materials.append(em)

# ---- the world and the portrait light -----------------------------------------------------
world = bpy.data.worlds.new("Plate")
scene.world = world
world.use_nodes = True
wn = world.node_tree
wn.nodes.clear()
wo = wn.nodes.new("ShaderNodeOutputWorld")
bg = wn.nodes.new("ShaderNodeBackground")
envt = wn.nodes.new("ShaderNodeTexEnvironment")
envt.image = bpy.data.images.load(HDRI)
bg.inputs["Strength"].default_value = 0.15
wn.links.new(envt.outputs["Color"], bg.inputs["Color"])
wn.links.new(bg.outputs["Background"], wo.inputs["Surface"])

def area(name, loc, rot, power, size, col=(1.0, 0.82, 0.6)):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = power
    ld.size = size
    ld.color = col
    lo = bpy.data.objects.new(name, ld)
    bpy.context.collection.objects.link(lo)
    lo.location = loc
    lo.rotation_euler = rot
    return lo

area("Key", (-1.2, -1.9, 3.6), (math.radians(48), 0, math.radians(-25)), 110, 0.85, (1.0, 0.72, 0.45))
area("Rim", (1.6, 1.4, 3.0), (math.radians(120), 0, math.radians(150)), 110, 0.7, (0.75, 0.8, 1.0))
area("Fill", (1.2, -1.8, 1.6), (math.radians(75), 0, math.radians(30)), 25, 1.4)
## the face gets its own soft light: the plate lights the machinery
area("Face", (0.0, -1.7, 2.3), (math.radians(88), 0, 0), 4, 0.6)
## and the tally's red spill kisses the fur rim
rl = bpy.data.lights.new("TallySpill", "POINT")
rl.energy = 3.0
rl.color = (1.0, 0.1, 0.05)
rl.shadow_soft_size = 0.05
rlo = bpy.data.objects.new("TallySpill", rl)
bpy.context.collection.objects.link(rlo)
rlo.location = (0.13, -0.47, 2.34)

# ---- cameras and the two stills --------------------------------------------------------------
scene.render.resolution_x = 1216
scene.render.resolution_y = 1520
scene.render.image_settings.file_format = "PNG"

camd = bpy.data.cameras.new("PlateCam")
camd.lens = 85
camd.dof.use_dof = True
camd.dof.aperture_fstop = 2.8
cam = bpy.data.objects.new("PlateCam", camd)
bpy.context.collection.objects.link(cam)
scene.camera = cam

def aim(obj, target):
    d = obj.location - target
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = d.to_track_quat("Z", "Y")

import mathutils
## SHOT 1: the head, plate framing
cam.location = mathutils.Vector((0.06, -2.65, 2.5))
aim(cam, mathutils.Vector((0.0, -0.05, 2.35)))
camd.dof.focus_distance = 2.35
camd.dof.aperture_fstop = 4.0
scene.render.filepath = os.path.join(OUTDIR, "chum_af_head.png")
bpy.ops.render.render(write_still=True)
print("RENDERED head")

## SHOT 1b: the ears, close — sewn edges, tattered panels, the singed left tip
cam.location = mathutils.Vector((0.08, -1.85, 2.98))
aim(cam, mathutils.Vector((0.0, 0.0, 2.86)))
camd.dof.focus_distance = 1.85
camd.dof.aperture_fstop = 4.0
scene.render.filepath = os.path.join(OUTDIR, "chum_af_ears.png")
bpy.ops.render.render(write_still=True)
print("RENDERED ears")

## SHOT 2: full figure, low angle, the eleven-footer looking down at you
camd.lens = 50
cam.location = mathutils.Vector((-1.15, -3.4, 1.15))
aim(cam, mathutils.Vector((0.0, -0.1, 1.55)))
camd.dof.focus_distance = 3.4
camd.dof.aperture_fstop = 4.0
scene.render.filepath = os.path.join(OUTDIR, "chum_af_full.png")
bpy.ops.render.render(write_still=True)
print("RENDERED full")
