"""Blender → UE FBX export, per docs/canon/restoration-blender-ue5-pipeline.md.

Standards enforced here so nothing is renegotiated per asset:
meters in, 1m = 100uu out (apply_unit_scale, FBX_SCALE_NONE); SM_ naming;
UCX_ collision children travel with the mesh.

Usage:
  Blender --background --python tools/export_ue.py -- --cube
      exports the 1m calibration cube to ue/exports/SM_UnitCube.fbx
  Blender --background <file.blend> --python tools/export_ue.py -- \
      --objects Obj1,Obj2 --out ue/exports/SM_Name.fbx
      exports named objects (+ any UCX_* children) to one FBX
"""
import bpy
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EXPORTS = os.path.join(ROOT, "ue", "exports")
os.makedirs(EXPORTS, exist_ok=True)

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default=None):
    if name in argv:
        i = argv.index(name)
        return argv[i + 1] if i + 1 < len(argv) else default
    return default


def export(objs, out_path):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
        for ch in o.children:
            if ch.name.startswith("UCX_"):
                ch.select_set(True)
    bpy.ops.export_scene.fbx(
        filepath=out_path,
        use_selection=True,
        apply_unit_scale=True,
        apply_scale_options="FBX_SCALE_NONE",
        bake_space_transform=True,
        object_types={"MESH", "EMPTY"},
        use_mesh_modifiers=True,
        add_leaf_bones=False,
        bake_anim=False,
        path_mode="COPY",
        embed_textures=True,
    )
    print("UE-EXPORTED", out_path)


if "--cube" in argv:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    cube = bpy.context.active_object
    cube.name = "SM_UnitCube"
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    ucx = bpy.context.active_object
    ucx.name = "UCX_SM_UnitCube_00"
    ucx.parent = cube
    ucx.matrix_parent_inverse = cube.matrix_world.inverted()
    ucx.display_type = "WIRE"
    export([cube], os.path.join(EXPORTS, "SM_UnitCube.fbx"))
else:
    names = (arg("--objects") or "").split(",")
    out = arg("--out")
    if not names or not out:
        raise SystemExit("need --objects and --out (or --cube)")
    objs = [bpy.data.objects[n] for n in names]
    if not os.path.isabs(out):
        out = os.path.join(ROOT, out)
    export(objs, out)
