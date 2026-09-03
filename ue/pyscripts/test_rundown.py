"""Unit 0.7 smoke: spawn ARundown + a tagged target in the greybox, simulate
through a full ON AIR (50s) + BREAK (18s) cycle, then read the decision log.
Expect: WARN (target sits at ~6m, inside warn radius 7) and a RELOCATE at
the phase flip. Run via: UE_RUN_PYSCRIPT=<this> UnrealEditor ... -RenderOffscreen
"""
import os
import unreal

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

les.load_level("/Game/Greybox")

## clear any previous decision log so the read is this run's evidence
import os as _o
LOG = _o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))), "Restoration", "Saved", "decision_log.txt")
if os.path.exists(LOG):
    os.remove(LOG)

rundown_cls = unreal.load_class(None, "/Script/Restoration.Rundown")
rd = eas.spawn_actor_from_class(rundown_cls, unreal.Vector(0, -1600, 0))
unreal.log_warning("RDTEST spawned Rundown: %s" % rd.get_name())

cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
tgt = eas.spawn_actor_from_object(cube, unreal.Vector(0, -1000, 100))
tgt.set_actor_scale3d(unreal.Vector(0.4, 0.4, 1.8))
tgt.tags = [unreal.Name("RundownTestTarget")]

state = {"t": 0.0, "ticks": 0, "started": False, "h": None}

def _tick(dt):
    state["ticks"] += 1
    if state["ticks"] == 20 and not state["started"]:
        state["started"] = True
        les.editor_play_simulate()
        unreal.log_warning("RDTEST simulate started")
    if state["started"]:
        state["t"] += dt
    if state["t"] >= 76.0:
        unreal.unregister_slate_post_tick_callback(state["h"])
        if os.path.exists(LOG):
            with open(LOG) as fh:
                for line in fh.read().strip().splitlines():
                    unreal.log_warning("RDLOG| " + line)
        else:
            unreal.log_error("RDLOG| decision_log.txt MISSING")
        unreal.SystemLibrary.quit_editor()

state["h"] = unreal.register_slate_post_tick_callback(_tick)
