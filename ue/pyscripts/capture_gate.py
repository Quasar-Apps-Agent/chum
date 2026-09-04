"""GATE 0.10 capture: the stamped greybox with the After-Fire puppet PLACED
at the TAPE LIBRARY anchor, shot from an env camera. Self-contained (does
not exec capture_level.py, whose load_level would wipe the placed puppet).
Env: UE_CAP_OUT (png path, required); UE_CAP_POS / UE_CAP_LOOK / UE_CAP_FOV
optional. The puppet is placed, not driven — see ue/GATE-0.10.md §3.
"""
import os
import unreal

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

LEVEL = "/Game/Greybox"
ANCHOR = unreal.Vector(0, -1600, 0)  # TAPE LIBRARY, the brain's first anchor
# INSIDE the room: TAPE LIBRARY is x -6..6 m, y -21..-11 m (Rooms.csv). A
# camera at y=-10.4 m sat outside the north wall and shot a lit slab.
POS = [float(v) for v in os.environ.get("UE_CAP_POS", "-420,-1240,175").split(",")]
LOOK = [float(v) for v in os.environ.get("UE_CAP_LOOK", "0,-1600,140").split(",")]
OUT = os.environ["UE_CAP_OUT"]
FOV = float(os.environ.get("UE_CAP_FOV", "70"))

les.load_level(LEVEL)
puppet_mesh = unreal.EditorAssetLibrary.load_asset("/Game/Imported/SM_ChumAF")
puppet = eas.spawn_actor_from_object(puppet_mesh, ANCHOR)
puppet.set_actor_rotation(unreal.Rotator(0, 0, 200), False)  # 3/4 toward camera
o, ext = puppet.get_actor_bounds(False)
unreal.log_warning("GATECAP puppet placed at %s (%s) bounds origin=%s extent=%s" % (ANCHOR, puppet.get_name(), o, ext))

cam = eas.spawn_actor_from_class(unreal.CameraActor, unreal.Vector(*POS))
cam.camera_component.set_field_of_view(FOV)
look = unreal.MathLibrary.find_look_at_rotation(unreal.Vector(*POS), unreal.Vector(*LOOK))
cam.set_actor_rotation(look, False)

state = {"t": 0, "shot": False, "h": None}

def _tick(dt):
    state["t"] += 1
    if state["t"] == 90 and not state["shot"]:  # a few extra frames for Lumen to settle
        state["shot"] = True
        unreal.AutomationLibrary.take_high_res_screenshot(1600, 1000, OUT, camera=cam)
        unreal.log_warning("GATECAP-REQUESTED " + OUT)
    if state["t"] >= 240:
        unreal.unregister_slate_post_tick_callback(state["h"])
        unreal.log_warning("GATECAP-%s %s" % ("SAVED" if os.path.exists(OUT) else "MISSING", OUT))
        unreal.SystemLibrary.quit_editor()

state["h"] = unreal.register_slate_post_tick_callback(_tick)
unreal.log_warning("GATECAP-STAGED " + LEVEL)
