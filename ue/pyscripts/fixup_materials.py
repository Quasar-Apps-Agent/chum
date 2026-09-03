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
            if eal.does_asset_exist("/Game/Imported/Tex/" + tname):
                continue
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
