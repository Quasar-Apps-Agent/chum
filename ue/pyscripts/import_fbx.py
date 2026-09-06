"""Import FBX(s) from ue/exports into /Game/Imported, enforcing the naming
law, and verify the scale contract (1m = 100uu) plus UCX collision pickup.

Run headless:
  UnrealEditor-Cmd <uproject> -run=pythonscript -script=".../import_fbx.py"
Optional env: UE_IMPORT_FILES=comma,separated,paths (default: all FBX in
ue/exports). Prints IMPORT-OK/IMPORT-FAIL lines the driver greps.
"""
import os
import unreal

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EXPORTS = os.path.join(ROOT, "ue", "exports")
DEST = "/Game/Imported"

files = os.environ.get("UE_IMPORT_FILES")
if files:
    paths = [p for p in files.split(",") if p.strip()]
else:
    paths = [os.path.join(EXPORTS, f) for f in sorted(os.listdir(EXPORTS))
             if f.lower().endswith(".fbx")]

ok_all = True
for path in paths:
    base = os.path.splitext(os.path.basename(path))[0]
    if not (base.startswith("SM_") or base.startswith("SK_")):
        unreal.log_error("IMPORT-FAIL naming-law %s (need SM_/SK_ prefix)" % base)
        ok_all = False
        continue
    opts = unreal.FbxImportUI()
    opts.import_mesh = True
    opts.import_as_skeletal = base.startswith("SK_")
    opts.import_materials = True
    opts.import_textures = True
    opts.static_mesh_import_data.set_editor_property("combine_meshes", True)
    opts.static_mesh_import_data.set_editor_property("auto_generate_collision", False)
    task = unreal.AssetImportTask()
    task.filename = path
    task.destination_path = DEST
    task.destination_name = base
    task.automated = True
    task.save = True
    task.replace_existing = True
    task.options = opts
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    asset_path = "%s/%s" % (DEST, base)
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if asset is None:
        unreal.log_error("IMPORT-FAIL load %s" % asset_path)
        ok_all = False
        continue
    if isinstance(asset, unreal.StaticMesh):
        b = asset.get_bounding_box()
        size = (b.max.x - b.min.x, b.max.y - b.min.y, b.max.z - b.min.z)
        try:
            sms = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
            nconvex = len(asset.get_editor_property("body_setup").get_editor_property("agg_geom").get_editor_property("convex_elems"))
        except Exception:
            nconvex = -1
        ## 1.5: box collision from <fbx>.collision.json (world metres, Blender
        ## axes: UE Y is the negative of Blender Y after the importer's
        ## handedness flip — Y_SIGN below is verified against the mesh bounds)
        _cj = os.path.splitext(path)[0] + ".collision.json"
        if os.path.exists(_cj):
            import json as _json
            Y_SIGN = -1.0
            _bs = asset.get_editor_property("body_setup")
            _ag = _bs.get_editor_property("agg_geom")
            _elems = []
            for _b in _json.load(open(_cj)):
                _e = unreal.KBoxElem()
                _c = _b["center_m"]; _d = _b["size_m"]
                _e.set_editor_property("center", unreal.Vector(_c[0] * 100.0, Y_SIGN * _c[1] * 100.0, _c[2] * 100.0))
                _e.set_editor_property("x", _d[0] * 100.0)
                _e.set_editor_property("y", _d[1] * 100.0)
                _e.set_editor_property("z", _d[2] * 100.0)
                _elems.append(_e)
            _ag.set_editor_property("box_elems", _elems)
            _bs.set_editor_property("agg_geom", _ag)
            _bs.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AS_COMPLEX)
            asset.set_editor_property("body_setup", _bs)
            unreal.EditorAssetLibrary.save_asset(asset.get_path_name())
            unreal.log_warning("IMPORT-COLLISION %d box elems from %s" % (len(_elems), os.path.basename(_cj)))
        unreal.log_warning("IMPORT-OK %s size_uu=(%.1f,%.1f,%.1f) convex=%d"
                           % (base, size[0], size[1], size[2], nconvex))
    else:
        unreal.log_warning("IMPORT-OK %s (%s)" % (base, type(asset).__name__))

unreal.log_warning("IMPORT-DONE all_ok=%s" % ok_all)
