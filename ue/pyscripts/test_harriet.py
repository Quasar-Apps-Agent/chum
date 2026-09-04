"""0.8b-5 bite: Harriet's freeze. Self-driving hook samples her sway at 0.5s
and 1.0s (should differ — she's swaying), forces break at 1.0s, samples at
2.0s (should equal the 1.0s value — frozen mid-motion)."""
import os
import unreal

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
les.load_level("/Game/Greybox")
LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Restoration", "Saved", "decision_log.txt")
if os.path.exists(LOG):
    os.remove(LOG)
cls = unreal.load_class(None, "/Script/Restoration.Harriet")
h = eas.spawn_actor_from_class(cls, unreal.Vector(-2450, -2700, 100))
h.set_editor_property("bTestFreeze", True)
state = {"t": 0.0, "ticks": 0, "started": False, "h": None}

def _tick(dt):
    state["ticks"] += 1
    if state["ticks"] == 20 and not state["started"]:
        state["started"] = True
        les.editor_play_simulate()
    if state["started"]:
        state["t"] += dt
    if state["t"] >= 3.5:
        unreal.unregister_slate_post_tick_callback(state["h"])
        if os.path.exists(LOG):
            with open(LOG, errors="replace") as fh:
                for line in fh.read().strip().splitlines():
                    unreal.log_warning("HARRIETLOG| " + line)
        unreal.SystemLibrary.quit_editor()

state["h"] = unreal.register_slate_post_tick_callback(_tick)
