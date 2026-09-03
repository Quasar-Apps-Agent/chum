"""0.8b-2 smoke: the bench loop. BenchA + stationary Rita -> 12s clean
signal. BenchB + auto-walking Rita -> tether abort. One 16s simulate."""
import os
import unreal

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
les.load_level("/Game/Greybox")
import os as _o
LOG = _o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))), "Restoration", "Saved", "decision_log.txt")
if os.path.exists(LOG):
    os.remove(LOG)
rita_cls = unreal.load_class(None, "/Script/Restoration.RitaCharacter")
bench_cls = unreal.load_class(None, "/Script/Restoration.BenchCapture")
## A: bench room (9,-16), Rita adjacent and still
ba = eas.spawn_actor_from_class(bench_cls, unreal.Vector(900, -1600, 50))
ba.set_editor_property("bTestAutoStart", True)
ra = eas.spawn_actor_from_class(rita_cls, unreal.Vector(950, -1650, 100))
## B: yard, Rita walks away immediately
bb = eas.spawn_actor_from_class(bench_cls, unreal.Vector(-600, 1400, 50))
bb.set_editor_property("bTestAutoStart", True)
rb = eas.spawn_actor_from_class(rita_cls, unreal.Vector(-650, 1400, 100))
rb.set_editor_property("bTestAutoWalk", True)
state = {"t": 0.0, "ticks": 0, "started": False, "h": None}

def _tick(dt):
    state["ticks"] += 1
    if state["ticks"] == 20 and not state["started"]:
        state["started"] = True
        les.editor_play_simulate()
    if state["started"]:
        state["t"] += dt
    if state["t"] >= 16.0:
        unreal.unregister_slate_post_tick_callback(state["h"])
        if os.path.exists(LOG):
            with open(LOG, errors="replace") as fh:
                for line in fh.read().strip().splitlines():
                    unreal.log_warning("BENCHLOG| " + line)
        unreal.SystemLibrary.quit_editor()

state["h"] = unreal.register_slate_post_tick_callback(_tick)
