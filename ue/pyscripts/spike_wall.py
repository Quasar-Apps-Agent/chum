"""SPIKE 2 (unit 0.6b · BUILD-ORDER P1): twelve SceneCapture2D feeds at
60fps — the monitor wall, built where canon puts it: MASTER CONTROL.

Twelve captures spread across the stamped studio, each into its own
RenderTarget, each RT on an emissive plane in a 4x3 wall. Then PIE runs
while a slate callback measures real frame times. The pass line per the
build plan: sustained 60 with headroom.

Run: UE_RUN_PYSCRIPT=<this> UnrealEditor <proj> -unattended -RenderOffscreen
Prints SPIKE2-* lines; writes the verdict; quits.
"""
import os
import time
import unreal

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
mel = unreal.MaterialEditingLibrary

les.load_level("/Game/Greybox")

## twelve vantage points: a camera per canon-significant room
FEEDS = [
    ("CORRIDOR", (0, -750, 240), (0, -1600, 120)),
    ("TAPE_LIB", (0, -1600, 240), (300, -1900, 100)),
    ("REC", (0, 0, 240), (400, 200, 100)),
    ("KITCHEN", (800, 0, 240), (900, 100, 100)),
    ("DORMS", (-900, 0, 240), (-1100, 100, 100)),
    ("ENTRY", (0, 700, 240), (0, 900, 100)),
    ("BENCH", (900, -1600, 240), (1000, -1700, 100)),
    ("TRANS", (1675, -650, 240), (1700, -900, 100)),
    ("STUDIO_A", (-1550, -3000, 260), (-1300, -3200, 100)),
    ("PATCH", (-550, -2950, 240), (-600, -3100, 100)),
    ("GREEN", (-2450, -2700, 240), (-2500, -2800, 100)),
    ("DOCK", (-1550, -3950, 240), (-1600, -4100, 100)),
]

## the wall lives in MASTER CONTROL (5.5, -29.5 in meters)
WALL_CX, WALL_CY = 550.0, -2950.0

mats = []
for i, (name, pos, look) in enumerate(FEEDS):
    rt_path = "/Game/Core/RT_Feed%02d" % i
    if not eal.does_asset_exist(rt_path):
        rt = at.create_asset("RT_Feed%02d" % i, "/Game/Core",
                             unreal.TextureRenderTarget2D,
                             unreal.TextureRenderTargetFactoryNew())
        rt.set_editor_property("size_x", 256)
        rt.set_editor_property("size_y", 256)
        eal.save_asset(rt_path)
    else:
        rt = eal.load_asset(rt_path)
    cap = eas.spawn_actor_from_class(unreal.SceneCapture2D, unreal.Vector(*pos))
    rotr = unreal.MathLibrary.find_look_at_rotation(unreal.Vector(*pos), unreal.Vector(*look))
    cap.set_actor_rotation(rotr, False)
    cc = cap.capture_component2d
    cc.set_editor_property("texture_target", rt)
    cc.set_editor_property("capture_every_frame", True)
    cc.set_editor_property("fov_angle", 70.0)
    mat_path = "/Game/Core/M_Feed%02d" % i
    if not eal.does_asset_exist(mat_path):
        m = at.create_asset("M_Feed%02d" % i, "/Game/Core", unreal.Material,
                            unreal.MaterialFactoryNew())
        m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
        ts = mel.create_material_expression(m, unreal.MaterialExpressionTextureSample, -400, 0)
        ts.set_editor_property("texture", rt)
        mel.connect_material_property(ts, "RGB", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
        mel.recompile_material(m)
        eal.save_asset(mat_path)
    else:
        m = eal.load_asset(mat_path)
    mats.append(m)

PLANE = eal.load_asset("/Engine/BasicShapes/Plane")
for i, m in enumerate(mats):
    col, row = i % 4, i // 4
    px = WALL_CX + (col - 1.5) * 110.0
    pz = 230.0 - row * 78.0
    a = eas.spawn_actor_from_object(PLANE, unreal.Vector(px, WALL_CY, pz))
    a.set_actor_rotation(unreal.Rotator(90.0, 0.0, 0.0), False)
    a.set_actor_scale3d(unreal.Vector(1.0, 0.72, 1.0))
    a.static_mesh_component.set_material(0, m)

unreal.log_warning("SPIKE2-WALL built: 12 feeds live")

## measure: PIE + slate frame deltas
state = {"t": 0, "times": [], "last": None, "started": False}


def _tick(dt):
    state["t"] += 1
    if state["t"] == 30 and not state["started"]:
        state["started"] = True
        les.editor_play_simulate()
        unreal.log_warning("SPIKE2-PIE started")
    if 90 <= state["t"] <= 690:
        state["times"].append(dt)
    if state["t"] >= 700:
        unreal.unregister_slate_post_tick_callback(state["h"])
        ts = sorted(state["times"])
        n = len(ts)
        avg = sum(ts) / n
        p95 = ts[int(n * 0.95)]
        unreal.log_warning("SPIKE2-RESULT frames=%d avg_ms=%.2f avg_fps=%.1f p95_ms=%.2f p95_fps=%.1f verdict=%s"
                           % (n, avg * 1000, 1.0 / avg, p95 * 1000, 1.0 / p95,
                              "PASS" if 1.0 / p95 >= 60.0 else ("MARGINAL" if 1.0 / avg >= 60.0 else "FAIL")))
        unreal.SystemLibrary.quit_editor()


state["h"] = unreal.register_slate_post_tick_callback(_tick)
