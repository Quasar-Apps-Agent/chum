"""Debug: render the skull's baked albedo as emission, suspects hidden.
Run: /Applications/Blender.app/Contents/MacOS/Blender --background --python tools/debug_face.py
"""
import bpy
import math
import os
import mathutils

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BLEND = os.path.join(ROOT, "blend", "chum_af.blend")
OUTDIR = os.path.join(ROOT, "renders")

bpy.ops.wm.open_mainfile(filepath=BLEND)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    scene.cycles.device = "GPU"
except Exception:
    pass
scene.cycles.samples = 32
scene.cycles.use_denoising = True

HIDE_PREFIXES = ("FacePanel", "SkullPatch", "BurnField", "ScorchRay", "SocketL",
                 "GearTooth", "ButtonEye", "BtnHole", "MeltDrip")
for ob in bpy.data.objects:
    if "Fur" in ob.name or "Fuzz" in ob.name:
        ob.hide_render = True
    if ob.name.startswith(HIDE_PREFIXES):
        ob.hide_render = True

## skull: emit its own baked diffuse — the literal albedo, no lighting story
skull = bpy.data.objects["Skull"]
img = bpy.data.images.get("Skull_diff")
m = bpy.data.materials.new("DebugAlbedo")
m.use_nodes = True
nt = m.node_tree
nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial")
em = nt.nodes.new("ShaderNodeEmission")
tex = nt.nodes.new("ShaderNodeTexImage")
tex.image = img
nt.links.new(tex.outputs["Color"], em.inputs["Color"])
em.inputs["Strength"].default_value = 1.0
nt.links.new(em.outputs[0], out.inputs["Surface"])
skull.data.materials.clear()
skull.data.materials.append(m)

## flat white world so emission reads true
world = bpy.data.worlds.new("Debug")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.05, 0.05, 0.05, 1.0)
bg.inputs["Strength"].default_value = 1.0

scene.render.resolution_x = 760
scene.render.resolution_y = 950
scene.render.image_settings.file_format = "PNG"
camd = bpy.data.cameras.new("DbgCam")
camd.lens = 85
cam = bpy.data.objects.new("DbgCam", camd)
bpy.context.collection.objects.link(cam)
scene.camera = cam
cam.location = mathutils.Vector((0.06, -2.65, 2.5))
d = cam.location - mathutils.Vector((0.0, -0.05, 2.35))
cam.rotation_mode = "QUATERNION"
cam.rotation_quaternion = d.to_track_quat("Z", "Y")
scene.render.filepath = os.path.join(OUTDIR, "debug_face.png")
bpy.ops.render.render(write_still=True)
print("RENDERED debug")
