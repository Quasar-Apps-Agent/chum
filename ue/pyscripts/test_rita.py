"""0.8b-1 smoke: Rita's feel. Auto-walk 3s flat (expect ~3.1 m/s), crouch,
3s more (expect ~1.7 m/s, cam drop 0.6m). Via UE_RUN_PYSCRIPT gate."""
import os
import unreal

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
les.load_level("/Game/Greybox")
import os as _o
LOG = _o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))), "Restoration", "Saved", "decision_log.txt")
if os.path.exists(LOG):
    os.remove(LOG)
cls = unreal.load_class(None, "/Script/Restoration.RitaCharacter")
## spawn in the YARD facing open ground: (0, 14) meters, +y walkable space
rita = eas.spawn_actor_from_class(cls, unreal.Vector(-800, 1400, 100))
rita.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
rita.set_editor_property("bTestAutoWalk", True)
state = {"t": 0.0, "ticks": 0, "started": False, "h": None}

def _tick(dt):
    state["ticks"] += 1
    if state["ticks"] == 20 and not state["started"]:
        state["started"] = True
        les.editor_play_simulate()
    if state["started"]:
        state["t"] += dt
    if state["t"] >= 9.0:
        unreal.unregister_slate_post_tick_callback(state["h"])
        if os.path.exists(LOG):
            with open(LOG) as fh:
                for line in fh.read().strip().splitlines():
                    unreal.log_warning("RITALOG| " + line)
        else:
            unreal.log_error("RITALOG| MISSING")
        unreal.SystemLibrary.quit_editor()

state["h"] = unreal.register_slate_post_tick_callback(_tick)
