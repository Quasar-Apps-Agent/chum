"""Open a saved level and screenshot it from an env-specified camera.
Env: UE_CAP_LEVEL (/Game/Greybox), UE_CAP_POS "x,y,z" (uu),
     UE_CAP_LOOK "x,y,z", UE_CAP_OUT (png path), UE_CAP_FOV (default 70)
Run via init_unreal gate: UE_RUN_PYSCRIPT=<this file> UnrealEditor ...
"""
import os
import unreal

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

LEVEL = os.environ.get("UE_CAP_LEVEL", "/Game/Greybox")
POS = [float(v) for v in os.environ.get("UE_CAP_POS", "0,0,160").split(",")]
LOOK = [float(v) for v in os.environ.get("UE_CAP_LOOK", "0,-400,160").split(",")]
OUT = os.environ["UE_CAP_OUT"]
FOV = float(os.environ.get("UE_CAP_FOV", "70"))

les.load_level(LEVEL)
cam = eas.spawn_actor_from_class(unreal.CameraActor, unreal.Vector(*POS))
cam.camera_component.set_field_of_view(FOV)
look = unreal.MathLibrary.find_look_at_rotation(unreal.Vector(*POS), unreal.Vector(*LOOK))
cam.set_actor_rotation(look, False)

state = {"t": 0, "shot": False, "h": None}

def _tick(dt):
    state["t"] += 1
    if state["t"] == 60 and not state["shot"]:
        state["shot"] = True
        unreal.AutomationLibrary.take_high_res_screenshot(1600, 1000, OUT, camera=cam)
        unreal.log_warning("LEVELCAP-REQUESTED " + OUT)
    if state["t"] >= 200:
        unreal.unregister_slate_post_tick_callback(state["h"])
        unreal.log_warning("LEVELCAP-%s %s" % ("SAVED" if os.path.exists(OUT) else "MISSING", OUT))
        unreal.SystemLibrary.quit_editor()

state["h"] = unreal.register_slate_post_tick_callback(_tick)
unreal.log_warning("LEVELCAP-STAGED " + LEVEL)
