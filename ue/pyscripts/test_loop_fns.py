"""0.8b-4 smoke: the loop's connective tissue. A Rundown (for the noise
subscription) + direct subsystem calls exercising day/night, stations,
the sign flow, paper, respawn. Reads decision_log."""
import os
import unreal

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
les.load_level("/Game/Greybox")
LOGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Restoration", "Saved")
LOG = os.path.join(LOGDIR, "decision_log.txt")
if os.path.exists(LOG):
    os.remove(LOG)

## the Rundown carries the test hook: run a scripted loop-fn sequence at BeginPlay
rundown_cls = unreal.load_class(None, "/Script/Restoration.Rundown")
rd = eas.spawn_actor_from_class(rundown_cls, unreal.Vector(0, -1600, 0))
rd.set_editor_property("bTestLoopFns", True)

state = {"t": 0.0, "ticks": 0, "started": False, "h": None}

def _tick(dt):
    state["ticks"] += 1
    if state["ticks"] == 20 and not state["started"]:
        state["started"] = True
        les.editor_play_simulate()
    if state["started"]:
        state["t"] += dt
    if state["t"] >= 4.0:
        unreal.unregister_slate_post_tick_callback(state["h"])
        if os.path.exists(LOG):
            with open(LOG, errors="replace") as fh:
                for line in fh.read().strip().splitlines():
                    unreal.log_warning("LOOPFN| " + line)
        unreal.SystemLibrary.quit_editor()

state["h"] = unreal.register_slate_post_tick_callback(_tick)
