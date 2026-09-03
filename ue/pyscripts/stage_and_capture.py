"""Stage a look-dev level around an imported asset and take a rendered
screenshot, unattended. Needs rendering, so run with the FULL editor:

  UnrealEditor <uproject> -ExecutePythonScript=".../stage_and_capture.py"

Env: UE_CAPTURE_ASSET (default /Game/Imported/SM_UnitCube)
     UE_CAPTURE_OUT   (default <repo>/renders/ue_capture.png)
Prints CAPTURE-SAVED <path> on success; the editor quits itself.
"""
import os
import unreal

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ASSET = os.environ.get("UE_CAPTURE_ASSET", "/Game/Imported/SM_UnitCube")
OUT = os.environ.get("UE_CAPTURE_OUT", os.path.join(ROOT, "renders", "ue_capture.png"))

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

les.new_level("/Game/Dev/L_AutoCapture")

## UE_CAPTURE_DARK=1: strip the template's daylight — the lighting bible's
## world is a dim interior; our own rig does the modelling
if os.environ.get("UE_CAPTURE_DARK") == "1":
    for a in list(eas.get_all_level_actors()):
        cn = a.get_class().get_name()
        if cn in ("DirectionalLight", "SkyLight", "SkyAtmosphere",
                  "ExponentialHeightFog", "VolumetricCloud", "StaticMeshActor"):
            eas.destroy_actor(a)

## floor
floor = eas.spawn_actor_from_object(
    unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Plane"),
    unreal.Vector(0, 0, 0))
floor.set_actor_scale3d(unreal.Vector(40, 40, 1))
fmesh = floor.static_mesh_component
fmat = unreal.EditorAssetLibrary.load_asset("/Engine/EngineMaterials/PersistentLevelMaterial")

## lights: warm key, cool rim, skylight — the look-dev grammar's skeleton
dark = os.environ.get("UE_CAPTURE_DARK") == "1"
key = eas.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0, 0, 300))
key.set_actor_rotation(unreal.Rotator(-42, 35, 0), False)
key.light_component.set_intensity(1.6 if dark else 6.0)
key.light_component.set_light_color(unreal.LinearColor(1.0, 0.82, 0.6, 1.0))
sky = eas.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0, 0, 400))
sky.light_component.set_intensity(0.25 if dark else 0.6)
rim = eas.spawn_actor_from_class(unreal.SpotLight, unreal.Vector(-260, 300, 260))
rim.set_actor_rotation(unreal.Rotator(-35, -125, 0), False)
rim.light_component.set_intensity(9000.0 if dark else 120000.0)
rim.light_component.set_light_color(unreal.LinearColor(0.6, 0.7, 0.95, 1.0))
## LOCKED EV (lighting bible: exposure never swims) — manual metering
ppv = eas.spawn_actor_from_class(unreal.PostProcessVolume, unreal.Vector(0, 0, 0))
ppv.set_editor_property("unbound", True)
pps = ppv.get_editor_property("settings")
pps.set_editor_property("override_auto_exposure_method", True)
pps.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
pps.set_editor_property("override_auto_exposure_bias", True)
pps.set_editor_property("auto_exposure_bias", 11.5 if dark else 12.5)
ppv.set_editor_property("settings", pps)

## the subject (UE_CAPTURE_YAW turns it to face the camera)
subj_asset = unreal.EditorAssetLibrary.load_asset(ASSET)
subj = eas.spawn_actor_from_object(subj_asset, unreal.Vector(0, 0, 0))
try:
    yaw = float(os.environ.get("UE_CAPTURE_YAW", "0"))
except ValueError:
    yaw = 0.0
subj.set_actor_rotation(unreal.Rotator(0, 0, yaw), False)
b_origin, b_extent = subj.get_actor_bounds(False)
size = max(b_extent.x, b_extent.y, b_extent.z)

## camera framing: full figure by default; UE_CAPTURE_FRAME=head frames the
## upper quarter (the portrait the plate uses)
frame = os.environ.get("UE_CAPTURE_FRAME", "full")
if frame == "head":
    b_origin = unreal.Vector(b_origin.x, b_origin.y,
                             b_origin.z + b_extent.z * 0.62)
    size = size * 0.42
dist = max(size * 3.2, 120.0)
cam_loc = unreal.Vector(b_origin.x - dist * 0.72, b_origin.y - dist * 0.6,
                        b_origin.z + size * 0.25)
cam = eas.spawn_actor_from_class(unreal.CameraActor, cam_loc)
look = unreal.MathLibrary.find_look_at_rotation(cam_loc, b_origin)
cam.set_actor_rotation(look, False)

les.save_current_level()

## screenshot after the renderer has had frames to warm up, then quit
state = {"ticks": 0, "shot": False, "handle": None}

def _tick(dt):
    state["ticks"] += 1
    if state["ticks"] == 90 and not state["shot"]:
        state["shot"] = True
        unreal.AutomationLibrary.take_high_res_screenshot(1600, 900, OUT, camera=cam)
        unreal.log_warning("CAPTURE-REQUESTED " + OUT)
    if state["ticks"] >= 240:
        unreal.unregister_slate_post_tick_callback(state["handle"])
        if os.path.exists(OUT):
            unreal.log_warning("CAPTURE-SAVED " + OUT)
        else:
            unreal.log_error("CAPTURE-MISSING " + OUT)
        unreal.SystemLibrary.quit_editor()

state["handle"] = unreal.register_slate_post_tick_callback(_tick)
unreal.log_warning("STAGE-OK subject=%s size=%.1f" % (ASSET, size))
