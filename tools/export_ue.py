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
elif "--all-meshes" in argv:
    out = arg("--out")
    if not out:
        raise SystemExit("need --out with --all-meshes")
    ## 1.2 finding: bevelled CURVES (the throat ring and cables, the mouth's
    ## lips) never reached the engine — this list took meshes only. Convert
    ## every render-visible curve to a mesh first, then collect.
    _curves = [o for o in bpy.data.objects if o.type == "CURVE" and not o.hide_render]
    for _c in _curves:
        bpy.ops.object.select_all(action="DESELECT")
        _c.select_set(True)
        bpy.context.view_layer.objects.active = _c
        try:
            bpy.ops.object.convert(target="MESH")
        except RuntimeError as _ex:
            print("UE-CURVE-SKIP", _c.name, _ex)
    print("UE-CURVES converted", len(_curves))
    ## UCX_ collision boxes are hidden from render on purpose (1.5) — they
    ## must still travel; the importer takes them by name
    objs = [o for o in bpy.data.objects
            if o.type == "MESH" and (not o.hide_render or o.name.startswith("UCX_"))]
    print("UE-UCX", len([o for o in objs if o.name.startswith("UCX_")]), "collision boxes in the export")
    ## the importer matches UCX_ names against one node and drops the rest
    ## (1.5: four conventions, zero hulls) — so the boxes ALSO go out as data:
    ## <out>.collision.json, world centre and full size in metres, and the
    ## import script builds box collision from it
    import json as _json
    _boxes = []
    for _u in objs:
        if not _u.name.startswith("UCX_"):
            continue
        _mw = _u.matrix_world
        _loc = _mw.translation
        _dim = [abs(v) for v in _u.dimensions]   # dimensions are in local scale; boxes are axis-aligned
        _boxes.append({"name": _u.name, "center_m": [_loc.x, _loc.y, _loc.z], "size_m": [_dim[0], _dim[1], _dim[2]]})
    _cpath = os.path.splitext(out)[0] + ".collision.json"
    _cpath = _cpath.replace(".fbx", "")
    with open(_cpath, "w") as _cf:
        _json.dump(_boxes, _cf, indent=1)
    print("UE-COLLISION-JSON", len(_boxes), _cpath)
    if not os.path.isabs(out):
        out = os.path.join(ROOT, out)
    ## packed images (the bakes) have no disk file, so FBX COPY silently
    ## drops them — write them out beside the export first
    texdir = os.path.join(os.path.dirname(out), "textures")
    os.makedirs(texdir, exist_ok=True)
    for img in bpy.data.images:
        if img.packed_file is not None:
            img.filepath_raw = os.path.join(texdir, img.name.split(".")[0] + ".png")
            img.file_format = "PNG"
            try:
                img.save()
            except Exception as ex:
                print("UE-TEX-FAIL", img.name, ex)
    ## flatten: parent empties do not survive FBX combine — keep world
    ## transforms explicitly so no part lands at the origin
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    ## manifest: material -> texture image names, for the UE-side wiring
    ## (FBX imports textures but never connects them to the instances)
    import json
    manifest = {}
    for o in objs:
        for ms in o.data.materials:
            if not ms or not ms.use_nodes or ms.name in manifest:
                continue
            entry = {}
            for n in ms.node_tree.nodes:
                if n.type != "TEX_IMAGE" or not n.image:
                    continue
                nm = n.image.name
                for lk in n.outputs["Color"].links:
                    tgt = lk.to_node
                    if tgt.type == "BSDF_PRINCIPLED" and lk.to_socket.name == "Base Color":
                        entry["diff"] = nm
                    elif tgt.type == "MIX_RGB":
                        ## scan_dress: TexImage -> Multiply -> Base Color. The
                        ## MULTIPLY's Color2 is the tint the engine must apply too
                        ## (1.2 finding: without it a dark steel ring and rubber
                        ## cables rendered WHITE in Unreal — the raw scans)
                        for lk2 in tgt.outputs["Color"].links:
                            if (lk2.to_node.type == "BSDF_PRINCIPLED"
                                    and lk2.to_socket.name == "Base Color"):
                                entry.setdefault("diff", nm)
                                if tgt.blend_type == "MULTIPLY" and not tgt.inputs["Color2"].is_linked:
                                    c = tgt.inputs["Color2"].default_value
                                    entry["tint"] = [round(float(c[0]), 4), round(float(c[1]), 4), round(float(c[2]), 4)]
                    elif tgt.type == "NORMAL_MAP":
                        entry["nrm"] = nm
                    elif tgt.type == "BSDF_PRINCIPLED" and lk.to_socket.name == "Roughness":
                        entry["rgh"] = nm
            if entry:
                manifest[ms.name] = entry
    ## scan_dress tints, BAKED INTO A TEXTURE COPY (1.2 finding): the FBX Phong
    ## master lerps DiffuseColor -> DiffuseColorMap by DiffuseColorMapWeight=1,
    ## so a colour parameter cannot multiply a map. Do what the Cycles graph
    ## does, in pixels: write <material>_tint.png = scan x tint, and point the
    ## manifest at it. (Metals since 0.3, the throat ring and cables rendered
    ## as their raw light scans in the engine before this.)
    _tinted = 0
    for _mname, _entry in manifest.items():
        _t = _entry.get("tint")
        if not _t or not _entry.get("diff"):
            continue
        _src = bpy.data.images.get(_entry["diff"])
        if _src is None:
            continue
        _safe = _mname.replace(".", "_")
        _dst = bpy.data.images.new(_safe + "_tint", _src.size[0], _src.size[1], alpha=False)
        _dst.colorspace_settings.name = "sRGB"
        _px = list(_src.pixels)
        for _i in range(0, len(_px), 4):
            _px[_i] = min(_px[_i] * _t[0], 1.0)
            _px[_i + 1] = min(_px[_i + 1] * _t[1], 1.0)
            _px[_i + 2] = min(_px[_i + 2] * _t[2], 1.0)
        _dst.pixels = _px
        _dst.filepath_raw = os.path.join(texdir, _safe + "_tint.png")
        _dst.file_format = "PNG"
        try:
            _dst.save()
            _entry["diff"] = _safe + "_tint"
            _tinted += 1
        except Exception as _ex:
            print("UE-TINT-FAIL", _mname, _ex)
    print("UE-TINTED", _tinted, "scan-dressed materials pre-multiplied")
    ## 1.7: ORM packing (PIPELINE §STANDARDS "ORM packed"): R = AO (1.0 — the
    ## bakes carry soot in the albedo), G = roughness (the baked map, else the
    ## material's constant), B = metallic (the material's constant). Full-res
    ## where a roughness bake exists, an 8x8 constant otherwise. Linear.
    import numpy as _np
    _packed = 0
    for _mname, _entry in list(manifest.items()):
        _mat = bpy.data.materials.get(_mname)
        if _mat is None or not _mat.use_nodes:
            continue
        _pb = next((n for n in _mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if _pb is None:
            continue
        _metal = float(_pb.inputs["Metallic"].default_value)
        _rough_c = float(_pb.inputs["Roughness"].default_value) if not _pb.inputs["Roughness"].is_linked else 0.55
        _safe = _mname.replace(".", "_")
        _rimg = bpy.data.images.get(_entry["rgh"]) if _entry.get("rgh") else None
        if _rimg is not None and _rimg.size[0] > 0:
            _w, _h = _rimg.size
            _src = _np.empty(_w * _h * 4, dtype=_np.float32)
            _rimg.pixels.foreach_get(_src)
            _g = _src.reshape(-1, 4)[:, 0]
        else:
            _w = _h = 8
            _g = _np.full(_w * _h, _rough_c, dtype=_np.float32)
        _orm = _np.empty((_w * _h, 4), dtype=_np.float32)
        _orm[:, 0] = 1.0
        _orm[:, 1] = _g
        _orm[:, 2] = _metal
        _orm[:, 3] = 1.0
        _oimg = bpy.data.images.new(_safe + "_orm", _w, _h, alpha=False)
        _oimg.colorspace_settings.name = "Non-Color"
        _oimg.pixels.foreach_set(_orm.reshape(-1))
        _oimg.file_format = "PNG"
        _oimg.filepath_raw = os.path.join(texdir, _safe + "_orm.png")
        try:
            _oimg.save()
            _entry["orm"] = _safe + "_orm"
            _packed += 1
        except Exception as _ex:
            print("UE-ORM-FAIL", _mname, _ex)
    print("UE-ORM", _packed, "materials packed (R=AO G=rough B=metal)")
    mpath = os.path.splitext(out)[0] + ".manifest.json"
    with open(mpath, "w") as fh:
        json.dump(manifest, fh, indent=1)
    print("UE-MANIFEST", mpath, len(manifest), "materials")
    export(objs, out)
else:
    names = (arg("--objects") or "").split(",")
    out = arg("--out")
    if not names or not out:
        raise SystemExit("need --objects and --out (or --cube / --all-meshes)")
    objs = [bpy.data.objects[n] for n in names]
    if not os.path.isabs(out):
        out = os.path.join(ROOT, out)
    export(objs, out)
