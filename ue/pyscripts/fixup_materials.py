"""Post-import material fixup v2. The 5.8 FBX path imports materials as
MaterialInstanceConstant (no expression editing possible), so the specials
are authored fresh under /Game/Core and swapped onto the mesh slots:
- M_MawBlack : unlit absolute black (the lightproof maw)
- M_FurCards : masked, two-sided, tuft atlas -> BaseColor + OpacityMask
Env: UE_FIXUP_MESH (default /Game/Imported/SM_ChumAF)
"""
import os
import unreal

mel = unreal.MaterialEditingLibrary
eal = unreal.EditorAssetLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()

MESH = os.environ.get("UE_FIXUP_MESH", "/Game/Imported/SM_ChumAF")


def make_material(name):
    path = "/Game/Core"
    full = "%s/%s" % (path, name)
    if eal.does_asset_exist(full):
        return eal.load_asset(full)
    return at.create_asset(name, path, unreal.Material, unreal.MaterialFactoryNew())


## the lightproof maw
m_maw = make_material("M_MawBlack")
m_maw.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
c = mel.create_material_expression(m_maw, unreal.MaterialExpressionConstant3Vector, -400, 0)
c.set_editor_property("constant", unreal.LinearColor(0, 0, 0, 1))
mel.connect_material_property(c, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
mel.recompile_material(m_maw)
eal.save_asset("/Game/Core/M_MawBlack")

## the fur cards
m_fur = make_material("M_FurCards")
m_fur.set_editor_property("blend_mode", unreal.BlendMode.BLEND_MASKED)
m_fur.set_editor_property("two_sided", True)
tex = None
for p in eal.list_assets("/Game/Imported", recursive=True, include_folder=False):
    ad = eal.find_asset_data(p)
    if "fur_tuft" in str(ad.asset_name).lower():
        tex = eal.load_asset(p)
        break
if tex is not None:
    ts = mel.create_material_expression(m_fur, unreal.MaterialExpressionTextureSample, -500, 0)
    ts.set_editor_property("texture", tex)
    mel.connect_material_property(ts, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(ts, "A", unreal.MaterialProperty.MP_OPACITY_MASK)
    unreal.log_warning("FIXUP-FUR atlas wired")
r = mel.create_material_expression(m_fur, unreal.MaterialExpressionConstant, -400, 300)
r.set_editor_property("r", 0.9)
mel.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
mel.recompile_material(m_fur)
eal.save_asset("/Game/Core/M_FurCards")

## wire the bake textures per the Blender-side manifest (FBX imports the
## textures but leaves every instance's map parameters at defaults)
import json
import re
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
manifest_path = os.environ.get(
    "UE_FIXUP_MANIFEST",
    os.path.join(ROOT, "ue", "exports", "SM_ChumAF.manifest.json"))
wired = 0
if os.path.exists(manifest_path):
    with open(manifest_path) as fh:
        manifest = json.load(fh)

    ## import the exported PNGs directly — the FBX importer reuses existing
    ## textureless materials on re-import and never brings the maps along
    tex_dir = os.path.join(os.path.dirname(manifest_path), "textures")
    if os.path.isdir(tex_dir):
        tasks = []
        for f in sorted(os.listdir(tex_dir)):
            if not f.lower().endswith(".png"):
                continue
            tname = os.path.splitext(f)[0]
            ## ALWAYS re-import: bakes change every rebuild but keep their
            ## names; skipping existing assets left the whole puppet on stale
            ## maps (1.1c). replace_existing below overwrites in place.
            t = unreal.AssetImportTask()
            t.filename = os.path.join(tex_dir, f)
            t.destination_path = "/Game/Imported/Tex"
            t.automated = True
            t.save = True
            t.replace_existing = True
            tasks.append(t)
        if tasks:
            at.import_asset_tasks(tasks)
        unreal.log_warning("FIXUP-TEXIMPORT %d textures" % len(tasks))
        ## normal maps need TC_Normalmap + linear
        for p in eal.list_assets("/Game/Imported/Tex", recursive=True, include_folder=False):
            ad = eal.find_asset_data(p)
            nm = str(ad.asset_name)
            if nm.endswith("_nrm"):
                tx = eal.load_asset(p)
                tx.set_editor_property("compression_settings",
                                       unreal.TextureCompressionSettings.TC_NORMALMAP)
                tx.set_editor_property("srgb", False)
                eal.save_asset(p)

    tex_by_name = {}
    for p in eal.list_assets("/Game/Imported", recursive=True, include_folder=False):
        ad = eal.find_asset_data(p)
        tex_by_name[str(ad.asset_name)] = p

    def find_tex(img_name):
        base = os.path.splitext(img_name)[0].replace(".", "_")
        for cand in (base, base.replace("-", "_")):
            if cand in tex_by_name:
                return eal.load_asset(tex_by_name[cand])
        return None

    for mat_name, entry in manifest.items():
        inst_name = mat_name.replace(".", "_")
        inst_path = "/Game/Imported/%s" % inst_name
        if not eal.does_asset_exist(inst_path):
            continue
        mi = eal.load_asset(inst_path)
        d = find_tex(entry.get("diff", "")) if entry.get("diff") else None
        n = find_tex(entry.get("nrm", "")) if entry.get("nrm") else None
        if d is not None:
            mel.set_material_instance_texture_parameter_value(mi, "DiffuseColorMap", d)
        if n is not None:
            mel.set_material_instance_texture_parameter_value(mi, "NormalMap", n)
        if d or n:
            eal.save_asset(inst_path)
            wired += 1
unreal.log_warning("FIXUP-WIRED %d instances from manifest" % wired)

## 1.1c: the importer suffixes instances (_1, _001...) and may place them
## anywhere; the manifest loop above only finds /Game/Imported/<name>. Wire
## by the MESH'S OWN SLOTS instead: each slot's instance -> strip numeric
## suffixes -> manifest entry -> textures. Suffix-tolerant, path-agnostic.
if os.path.exists(manifest_path):
    norm = {k.replace(".", "_"): v for k, v in manifest.items()}
    _sm = eal.load_asset(MESH)
    slotwired = 0
    _slots = _sm.get_editor_property("static_materials")
    ## a known-good IMPORTER-MADE baked instance to clone: a bare factory
    ## instance with the same parent and the same texture params rendered
    ## flat white (1.1c) — the importer sets something inside the Phong master
    ## a fresh instance lacks. Duplicating a working one inherits it.
    _good = None
    for _sl in _slots:
        _m = _sl.get_editor_property("material_interface")
        if (isinstance(_m, unreal.MaterialInstanceConstant) and not _m.get_name().startswith("MI_")
                and any(str(tp.get_editor_property("parameter_info").get_editor_property("name")) == "DiffuseColorMap"
                        for tp in _m.get_editor_property("texture_parameter_values"))):
            _good = _m
            break
    _parent = _good.get_editor_property("parent") if _good else None
    made = 0
    tinted = 0
    for _i, _sl in enumerate(_slots):
        _mi = _sl.get_editor_property("material_interface")
        _slotname = str(_sl.get_editor_property("material_slot_name"))
        ## match the manifest by SLOT NAME (PatchNavy_002 <-> PatchNavy.002),
        ## then suffix-stripped, then any key sharing the base (same object,
        ## same bake — a leftover _001 slot still gets its patch's maps)
        _cands = [_slotname]
        _c = _slotname
        while re.search(r"_\d+$", _c):
            _c = re.sub(r"_\d+$", "", _c)
            _cands.append(_c)
        _entry = next((norm[c] for c in _cands if c in norm), None)
        if _entry is None:
            _base = _cands[-1]
            _entry = next((v for k, v in norm.items() if k.startswith(_base + "_") or k == _base), None)
        if _entry is None:
            continue
        if not isinstance(_mi, unreal.MaterialInstanceConstant) or _mi.get_name().startswith("MI_"):
            ## 1.1c: the importer left WorldGridMaterial (the checkerboard) on
            ## six new patch slots; a bare factory instance rendered white.
            ## Clone a working importer instance and override its textures.
            if _good is None:
                unreal.log_warning("FIXUP-MADE skipped %s: no good instance to clone" % _slotname)
                continue
            _dst = "/Game/Imported/MI_" + _slotname
            if eal.does_asset_exist(_dst):
                eal.delete_asset(_dst)
            _new = eal.duplicate_asset(_good.get_path_name().split(".")[0], _dst)
            if _new is None:
                unreal.log_warning("FIXUP-MADE duplicate failed for %s" % _slotname)
                continue
            _sm.set_material(_i, _new)
            _mi = _new
            made += 1
            unreal.log_warning("FIXUP-MADE slot %d %s -> clone of %s" % (_i, _slotname, _good.get_name()))
        _d = find_tex(_entry.get("diff", "")) if _entry.get("diff") else None
        _n = find_tex(_entry.get("nrm", "")) if _entry.get("nrm") else None
        if _d is not None:
            mel.set_material_instance_texture_parameter_value(_mi, "DiffuseColorMap", _d)
        if _n is not None:
            mel.set_material_instance_texture_parameter_value(_mi, "NormalMap", _n)
        ## tints arrive pre-multiplied in the texture (export writes <mat>_tint.png):
        ## the Phong master LERPs DiffuseColor -> map by DiffuseColorMapWeight=1,
        ## so a colour parameter cannot tint a map here (1.2 finding)
        if _entry.get("tint") and _entry.get("diff", "").endswith("_tint"):
            tinted += 1
        if _d or _n:
            eal.save_asset(_mi.get_path_name())
            slotwired += 1
    if made:
        eal.save_asset(MESH)
    unreal.log_warning("FIXUP-SLOTWIRED %d of %d mesh slots (%d instances created, %d tints applied)" % (slotwired, len(_slots), made, tinted))

## swap onto the mesh slots
sm = eal.load_asset(MESH)
mats = sm.get_editor_property("static_materials")
swapped = 0
for i, sl in enumerate(mats):
    iface = sl.get_editor_property("material_interface")
    nm = iface.get_name() if iface else ""
    if "MawBlack" in nm:
        sm.set_material(i, m_maw)
        swapped += 1
        unreal.log_warning("FIXUP-SLOT %d MawBlack -> M_MawBlack" % i)
    elif "FurCards" in nm:
        sm.set_material(i, m_fur)
        swapped += 1
        unreal.log_warning("FIXUP-SLOT %d FurCards -> M_FurCards" % i)
eal.save_asset(MESH)
unreal.log_warning("FIXUP-DONE %d slots swapped" % swapped)
