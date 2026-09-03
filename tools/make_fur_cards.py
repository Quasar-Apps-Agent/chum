"""Fur tuft atlas: four tuft variants rendered from real Cycles hair onto
transparent film -> tools/texsrc/fur_tuft_atlas.png (1024x512, 4 columns).

The game's fur cards wear this texture. Shading is unlit emission in the
coat's palette (dark char -> rust singe) so the engine's own lights model
the tufts; alpha comes from the film.

Run: /Applications/Blender.app/Contents/MacOS/Blender --background --python tools/make_fur_cards.py
"""
import bpy
import math
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "tools", "texsrc", "fur_tuft_atlas.png")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 64
scene.render.film_transparent = True
scene.render.resolution_x = 1024
scene.render.resolution_y = 512
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"

## unlit tuft shading: strand-random ramp from char to rust
m = bpy.data.materials.new("TuftEmit")
m.use_nodes = True
nt = m.node_tree
nt.nodes.clear()
out_n = nt.nodes.new("ShaderNodeOutputMaterial")
em = nt.nodes.new("ShaderNodeEmission")
hi = nt.nodes.new("ShaderNodeHairInfo")
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.0
ramp.color_ramp.elements[0].color = (0.011, 0.007, 0.0045, 1)
ramp.color_ramp.elements[1].position = 1.0
ramp.color_ramp.elements[1].color = (0.085, 0.03, 0.011, 1)
mid = ramp.color_ramp.elements.new(0.6)
mid.color = (0.032, 0.019, 0.011, 1)
nt.links.new(hi.outputs["Random"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
em.inputs["Strength"].default_value = 1.0
nt.links.new(em.outputs[0], out_n.inputs["Surface"])

for ci in range(4):
    bpy.ops.mesh.primitive_plane_add(size=0.42, location=(ci * 1.0, 0, 0.01))
    p = bpy.context.active_object
    p.data.materials.append(m)
    p.modifiers.new("hair", "PARTICLE_SYSTEM")
    ps = p.particle_systems[-1]
    st = ps.settings
    st.type = "HAIR"
    st.count = 60 + ci * 22
    st.hair_length = 1.45
    st.material = 1
    st.child_type = "INTERPOLATED"
    st.child_percent = 5
    try:
        st.rendered_child_count = 5
    except Exception:
        pass
    st.clump_factor = 0.82
    st.child_length = 0.85
    try:
        st.child_length_threshold = 0.45
    except Exception:
        pass
    try:
        st.root_radius = 1.0
        st.tip_radius = 0.1
        st.radius_scale = 0.014
    except Exception:
        pass
    for attr, val in (("kink", "CURL"), ("kink_amplitude", 0.09 + 0.03 * ci),
                      ("kink_frequency", 2.2), ("roughness_endpoint", 0.06),
                      ("roughness_2", 0.05), ("roughness_2_size", 1.6)):
        try:
            setattr(st, attr, val)
        except Exception:
            pass

camd = bpy.data.cameras.new("cam")
camd.type = "ORTHO"
camd.ortho_scale = 4.0
cam = bpy.data.objects.new("cam", camd)
bpy.context.collection.objects.link(cam)
scene.camera = cam
cam.location = (1.5, -5.0, 0.85)
cam.rotation_euler = (math.radians(90), 0, 0)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("WROTE", OUT)
