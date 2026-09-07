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


## 1.9: the same fixup serves SM_ (static) and SK_ (skeletal) meshes. Static
## meshes expose static_materials + set_material; skeletal meshes expose a
## materials array that must be written back whole.
def _slots_of(mesh):
    if isinstance(mesh, unreal.SkeletalMesh):
        return list(mesh.get_editor_property("materials"))
    return mesh.get_editor_property("static_materials")

def _set_slot(mesh, i, mat):
    if isinstance(mesh, unreal.SkeletalMesh):
        mats = list(mesh.get_editor_property("materials"))
        sm_ = mats[i]
        sm_.set_editor_property("material_interface", mat)
        mats[i] = sm_
        mesh.set_editor_property("materials", mats)
    else:
        mesh.set_material(i, mat)


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
## 1.8 step 6: roughness breaks with the tuft alpha (dense core matte,
## wisps glossier) so the pile breaks light more than one way
if tex is not None and mel.get_num_material_expressions(m_fur) < 6:
    _ra = mel.create_material_expression(m_fur, unreal.MaterialExpressionConstant, -450, 320)
    _ra.set_editor_property("r", 0.92)
    _rb = mel.create_material_expression(m_fur, unreal.MaterialExpressionConstant, -450, 380)
    _rb.set_editor_property("r", 0.55)
    _lerp = mel.create_material_expression(m_fur, unreal.MaterialExpressionLinearInterpolate, -300, 340)
    mel.connect_material_expressions(_ra, "", _lerp, "A")
    mel.connect_material_expressions(_rb, "", _lerp, "B")
    mel.connect_material_expressions(ts, "A", _lerp, "Alpha")
    mel.connect_material_property(_lerp, "", unreal.MaterialProperty.MP_ROUGHNESS)
else:
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
            ## 1.7: every scan normal (NormalGL / nor_gl) imported as sRGB colour
            ## until now; ORM and the scan roughness/metal maps are linear masks
            _low = nm.lower()
            if nm.endswith("_nrm") or "normalgl" in _low or "nor_gl" in _low or _low.endswith("_normal"):
                tx = eal.load_asset(p)
                tx.set_editor_property("compression_settings",
                                       unreal.TextureCompressionSettings.TC_NORMALMAP)
                tx.set_editor_property("srgb", False)
                eal.save_asset(p)
            elif (nm.endswith("_orm") or nm.endswith("_rgh") or "roughness" in _low or "_rough" in _low
                  or "metalness" in _low or "_metal" in _low or "displacement" in _low or _low.endswith("_ao")):
                tx = eal.load_asset(p)
                tx.set_editor_property("compression_settings",
                                       unreal.TextureCompressionSettings.TC_MASKS)
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
    _slots = _slots_of(_sm)
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
            _set_slot(_sm, _i, _new)
            _mi = _new
            made += 1
            unreal.log_warning("FIXUP-MADE slot %d %s -> clone of %s" % (_i, _slotname, _good.get_name()))
        _d = find_tex(_entry.get("diff", "")) if _entry.get("diff") else None
        _n = find_tex(_entry.get("nrm", "")) if _entry.get("nrm") else None
        if _d is not None:
            mel.set_material_instance_texture_parameter_value(_mi, "DiffuseColorMap", _d)
            ## 1.3 finding: IMPORTER-MADE instances (RodMetal, BronzeBand...) carry
            ## the map but no DiffuseColorMapWeight, so the Phong master lerps to
            ## its flat DiffuseColor — pale rivet balls, a tan bronze band. Weight 1.
            mel.set_material_instance_scalar_parameter_value(_mi, "DiffuseColorMapWeight", 1.0)
        if _n is not None:
            mel.set_material_instance_texture_parameter_value(_mi, "NormalMap", _n)
            mel.set_material_instance_scalar_parameter_value(_mi, "NormalMapWeight", 1.0)
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

## 1.7: THE BASE MASTER — BaseColor / Normal / ORM, wired to the physical
## inputs (roughness and metallic finally used; the importer's Phong master
## lerped a flat colour and had neither). Instances per manifest entry that
## carries an ORM; slots without one keep their importer material for now.
if os.path.exists(manifest_path):
    m_base = make_material("M_ChumAF_Base")
    if not mel.get_num_material_expressions(m_base):
        _bc = mel.create_material_expression(m_base, unreal.MaterialExpressionTextureSampleParameter2D, -600, -200)
        _bc.set_editor_property("parameter_name", "BaseColor")
        _bc.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
        _nm = mel.create_material_expression(m_base, unreal.MaterialExpressionTextureSampleParameter2D, -600, 100)
        _nm.set_editor_property("parameter_name", "Normal")
        _nm.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
        _orm = mel.create_material_expression(m_base, unreal.MaterialExpressionTextureSampleParameter2D, -600, 400)
        _orm.set_editor_property("parameter_name", "ORM")
        _orm.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
        _dflt_bc = _dflt_n = _dflt_o = None
        for _p in eal.list_assets("/Game/Imported/Tex", recursive=True, include_folder=False):
            _an = str(eal.find_asset_data(_p).asset_name)
            if _dflt_bc is None and _an.endswith("_diff"):
                _dflt_bc = eal.load_asset(_p)
            if _dflt_n is None and _an.endswith("_nrm"):
                _dflt_n = eal.load_asset(_p)
            if _dflt_o is None and _an.endswith("_orm"):
                _dflt_o = eal.load_asset(_p)
        if _dflt_bc: _bc.set_editor_property("texture", _dflt_bc)
        if _dflt_n: _nm.set_editor_property("texture", _dflt_n)
        if _dflt_o: _orm.set_editor_property("texture", _dflt_o)
        mel.connect_material_property(_bc, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)
        mel.connect_material_property(_nm, "RGB", unreal.MaterialProperty.MP_NORMAL)
        mel.connect_material_property(_orm, "R", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
        mel.connect_material_property(_orm, "G", unreal.MaterialProperty.MP_ROUGHNESS)
        mel.connect_material_property(_orm, "B", unreal.MaterialProperty.MP_METALLIC)
        mel.recompile_material(m_base)
        eal.save_asset("/Game/Core/M_ChumAF_Base")
        unreal.log_warning("FIXUP-MASTER M_ChumAF_Base built (BaseColor/Normal/ORM)")
    _sm2 = eal.load_asset(MESH)
    _slots2 = _slots_of(_sm2)
    _norm2 = {k.replace(".", "_"): v for k, v in manifest.items()}
    _ormed = 0
    for _i, _sl in enumerate(_slots2):
        _slotname = str(_sl.get_editor_property("material_slot_name"))
        _cands = [_slotname]
        _c = _slotname
        while re.search(r"_\d+$", _c):
            _c = re.sub(r"_\d+$", "", _c)
            _cands.append(_c)
        _entry = next((_norm2[c] for c in _cands if c in _norm2), None)
        if _entry is None or not _entry.get("orm") or not _entry.get("diff"):
            continue
        _d = find_tex(_entry["diff"]); _n = find_tex(_entry.get("nrm", "")) if _entry.get("nrm") else None; _o = find_tex(_entry["orm"])
        if _d is None or _o is None:
            continue
        _dst = "/Game/Imported/MIB_" + _slotname
        if eal.does_asset_exist(_dst):
            eal.delete_asset(_dst)
        _mi = at.create_asset("MIB_" + _slotname, "/Game/Imported", unreal.MaterialInstanceConstant,
                              unreal.MaterialInstanceConstantFactoryNew())
        mel.set_material_instance_parent(_mi, m_base)
        mel.set_material_instance_texture_parameter_value(_mi, "BaseColor", _d)
        if _n is not None:
            mel.set_material_instance_texture_parameter_value(_mi, "Normal", _n)
        mel.set_material_instance_texture_parameter_value(_mi, "ORM", _o)
        eal.save_asset(_dst)
        _set_slot(_sm2, _i, _mi)
        _ormed += 1
    eal.save_asset(MESH)
    unreal.log_warning("FIXUP-ORM %d of %d slots on M_ChumAF_Base" % (_ormed, len(_slots2)))

## 1.8: the tally core — an emissive material with a scalar the game drives
## 0 (dark) <-> lit; MI_TallyCore_Lit is the capture rig's lit variant
m_tally = make_material("M_TallyCore")
if not mel.get_num_material_expressions(m_tally):
    m_tally.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    _tc = mel.create_material_expression(m_tally, unreal.MaterialExpressionConstant3Vector, -700, 0)
    _tc.set_editor_property("constant", unreal.LinearColor(1.0, 0.03, 0.008, 1.0))
    _ti = mel.create_material_expression(m_tally, unreal.MaterialExpressionScalarParameter, -700, 250)
    _ti.set_editor_property("parameter_name", "TallyIntensity")
    _ti.set_editor_property("default_value", 0.0)
    _tm = mel.create_material_expression(m_tally, unreal.MaterialExpressionMultiply, -450, 100)
    mel.connect_material_expressions(_tc, "", _tm, "A")
    mel.connect_material_expressions(_ti, "", _tm, "B")
    mel.connect_material_property(_tm, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    mel.recompile_material(m_tally)
    eal.save_asset("/Game/Core/M_TallyCore")
    unreal.log_warning("FIXUP-TALLY M_TallyCore built (TallyIntensity 0 default)")
if not eal.does_asset_exist("/Game/Core/MI_TallyCore_Lit"):
    _tl = at.create_asset("MI_TallyCore_Lit", "/Game/Core", unreal.MaterialInstanceConstant,
                          unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(_tl, m_tally)
    mel.set_material_instance_scalar_parameter_value(_tl, "TallyIntensity", 40.0)
    eal.save_asset("/Game/Core/MI_TallyCore_Lit")

## swap onto the mesh slots
sm = eal.load_asset(MESH)
mats = _slots_of(sm)
swapped = 0
for i, sl in enumerate(mats):
    iface = sl.get_editor_property("material_interface")
    nm = iface.get_name() if iface else ""
    if "MawBlack" in nm:
        _set_slot(sm, i, m_maw)
        swapped += 1
        unreal.log_warning("FIXUP-SLOT %d MawBlack -> M_MawBlack" % i)
    elif "TallyCore" in nm or "TallyCore" in str(sl.get_editor_property("material_slot_name")):
        _set_slot(sm, i, m_tally)
        swapped += 1
        unreal.log_warning("FIXUP-SLOT %d TallyCore -> M_TallyCore" % i)
    elif "FurCards" in nm:
        _set_slot(sm, i, m_fur)
        swapped += 1
        unreal.log_warning("FIXUP-SLOT %d FurCards -> M_FurCards" % i)
eal.save_asset(MESH)
unreal.log_warning("FIXUP-DONE %d slots swapped" % swapped)
