"""0.9 bite: the invariant harness. Spawn a Rundown (bTestInvariants) + a
tagged target; the Rundown holds the target at 6m (WARN) then pulls it to
1.5m (STRIKE) with clear line of sight (no THRU-WALL). Then the parser reads
the decision log and rules I01/I02/I22."""
import os
import subprocess
import unreal

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
les.load_level("/Game/Greybox")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "Restoration", "Saved", "decision_log.txt")
if os.path.exists(LOG):
    os.remove(LOG)

rundown_cls = unreal.load_class(None, "/Script/Restoration.Rundown")
rd = eas.spawn_actor_from_class(rundown_cls, unreal.Vector(0, -1600, 0))
rd.set_editor_property("bTestInvariants", True)
cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
tgt = eas.spawn_actor_from_object(cube, unreal.Vector(0, -1000, 100))
tgt.set_actor_scale3d(unreal.Vector(0.4, 0.4, 1.8))
tgt.static_mesh_component.set_editor_property("mobility", unreal.ComponentMobility.MOVABLE)
tgt.tags = [unreal.Name("RundownTestTarget")]
## 0.9b: a wall between hunter (0,-1600) and prey pulled to (0,-1450) — the
## strike raycast must hit it and the brain must mark THRU-WALL
wall = eas.spawn_actor_from_object(cube, unreal.Vector(0, -1525, 150))
wall.set_actor_scale3d(unreal.Vector(3.0, 0.2, 3.0))

state = {"t": 0.0, "ticks": 0, "started": False, "h": None}

def _tick(dt):
    state["ticks"] += 1
    if state["ticks"] == 20 and not state["started"]:
        state["started"] = True
        les.editor_play_simulate()
    if state["started"]:
        state["t"] += dt
    if state["t"] >= 5.0:
        unreal.unregister_slate_post_tick_callback(state["h"])
        # the parser as a test step, on the identical log file
        parser = os.path.join(ROOT, "..", "tools", "invariant_parser.py")
        parser = os.path.normpath(parser)
        try:
            r = subprocess.run(["python3", parser, LOG], capture_output=True, text=True)
            for line in (r.stdout + r.stderr).strip().splitlines():
                unreal.log_warning("INVLOG| " + line)
            unreal.log_warning("INVLOG| PARSER-EXIT %d" % r.returncode)
        except Exception as ex:
            unreal.log_error("INVLOG| parser failed: %s" % ex)
        unreal.SystemLibrary.quit_editor()

state["h"] = unreal.register_slate_post_tick_callback(_tick)
