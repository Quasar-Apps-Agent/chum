"""0.8a smoke: AF tally contract end to end. Rundown forced into AF+recording,
target 8m out; expect approach at 0.8 m/s to the 1.2m loom, then the
scripted recording cutoff, the cool, and STRIKE af tally-cool. Plus the v16
save round-trip. Run via UE_RUN_PYSCRIPT gate.
"""
import os
import unreal

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
les.load_level("/Game/Greybox")

import os as _o
LOG = _o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))), "Restoration", "Saved", "decision_log.txt")
if os.path.exists(LOG):
    os.remove(LOG)

rundown_cls = unreal.load_class(None, "/Script/Restoration.Rundown")
rd = eas.spawn_actor_from_class(rundown_cls, unreal.Vector(0, -1600, 0))
rd.set_editor_property("bTestForceNight", False)
rd.set_editor_property("bTestForceAF", True)
rd.set_editor_property("bTestForceRecording", True)
rd.set_editor_property("TestRecordingOffAfter", 14.0)
rd.set_editor_property("bTestSaveRoundtrip", True)

cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
tgt = eas.spawn_actor_from_object(cube, unreal.Vector(0, -800, 100))
tgt.set_actor_scale3d(unreal.Vector(0.4, 0.4, 1.8))
tgt.tags = [unreal.Name("RundownTestTarget")]

state = {"t": 0.0, "ticks": 0, "started": False, "h": None}

def _tick(dt):
    state["ticks"] += 1
    if state["ticks"] == 20 and not state["started"]:
        state["started"] = True
        les.editor_play_simulate()
    if state["started"]:
        state["t"] += dt
    if state["t"] >= 24.0:
        unreal.unregister_slate_post_tick_callback(state["h"])
        if os.path.exists(LOG):
            with open(LOG) as fh:
                for line in fh.read().strip().splitlines():
                    unreal.log_warning("AFLOG| " + line)
        else:
            unreal.log_error("AFLOG| decision_log.txt MISSING")
        unreal.SystemLibrary.quit_editor()

state["h"] = unreal.register_slate_post_tick_callback(_tick)
