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

## 1.1c finding: with /Game/Greybox as the startup map, new_level() failed
## silently and the rig was staged INTO the Greybox. Verify, or refuse.
_ok = les.new_level("/Game/Dev/L_AutoCapture")
if not _ok and unreal.EditorAssetLibrary.does_asset_exist("/Game/Dev/L_AutoCapture"):
    les.load_level("/Game/Dev/L_AutoCapture")
_world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
if _world is None or _world.get_name() != "L_AutoCapture":
    unreal.log_error("CAPTURE-STAGE-FAIL: loaded level is %s, not L_AutoCapture — refusing to stage"
                     % (_world.get_name() if _world else None))
    unreal.SystemLibrary.quit_editor()
    raise SystemExit("stage refused")

## a clean stage: nothing survives from the template or a previous capture
## (the template daylight goes with it — our own rig does the modelling).
## Full strip, unconditional: a class-filtered strip once ran inside the
## Greybox and deleted every wall (1.1c).
for _a in list(eas.get_all_level_actors()):
    eas.destroy_actor(_a)

## floor
floor = eas.spawn_actor_from_object(
    unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Plane"),
    unreal.Vector(0, 0, 0))
floor.set_actor_scale3d(unreal.Vector(40, 40, 1))
fmesh = floor.static_mesh_component
fmat = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/BasicShapeMaterial")   # 1.2: PersistentLevelMaterial printed PREVIEW on the floor

## lights: warm key, cool rim, skylight — the look-dev grammar's skeleton
dark = os.environ.get("UE_CAPTURE_DARK") == "1"
key = eas.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0, 0, 300))
key.set_actor_rotation(unreal.Rotator(-42, 35, 0), False)
key.light_component.set_intensity(1.6 if dark else 6.0)
key.light_component.set_light_color(unreal.LinearColor(1.0, 0.82, 0.6, 1.0))
sky = eas.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0, 0, 400))
sky.light_component.set_intensity(0.25 if dark else 0.6)
## 1.2: the rim is placed and AIMED from the subject's bounds (the fixed
## (-260,300,260)/-35° placement lit the floor beside a 4 m puppet). Spawned
## here, positioned once the subject's bounds are known (below).
rim = eas.spawn_actor_from_class(unreal.SpotLight, unreal.Vector(-260, 300, 260))
rim.set_actor_rotation(unreal.Rotator(-35, -125, 0), False)
rim.light_component.set_intensity(120.0 if dark else 1500.0)   # 1.2: on the order of the key; 9000 cd only looked sane because it missed the subject
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
## 1.8: UE_CAPTURE_TALLY=1 lights the tally core (the game drives the same
## scalar); the dark portrait stays the baseline
if os.environ.get("UE_CAPTURE_TALLY") == "1":
    _lit = unreal.EditorAssetLibrary.load_asset("/Game/Core/MI_TallyCore_Lit")
    _is_sk = isinstance(subj_asset, unreal.SkeletalMesh)
    _smc = subj.skeletal_mesh_component if _is_sk else subj.static_mesh_component
    for _i, _sl in enumerate(subj_asset.get_editor_property("materials") if _is_sk else subj_asset.get_editor_property("static_materials")):
        if "TallyCore" in str(_sl.get_editor_property("material_slot_name")) and _lit:
            _smc.set_material(_i, _lit)
            unreal.log_warning("CAPTURE-TALLY lit on slot %d" % _i)
try:
    yaw = float(os.environ.get("UE_CAPTURE_YAW", "0"))
except ValueError:
    yaw = 0.0
subj.set_actor_rotation(unreal.Rotator(0, 0, yaw), False)
b_origin, b_extent = subj.get_actor_bounds(False)
size = max(b_extent.x, b_extent.y, b_extent.z)
## rim: behind-left and above, looking at the subject's centre (cool edge light)
_rim_loc = unreal.Vector(b_origin.x - size * 1.1, b_origin.y + size * 1.3, b_origin.z + size * 0.9)
rim.set_actor_location(_rim_loc, False, False)
rim.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(_rim_loc, b_origin), False)

## camera framing: full figure by default; UE_CAPTURE_FRAME=head frames the
## upper quarter (the portrait the plate uses)
frame = os.environ.get("UE_CAPTURE_FRAME", "full")
if frame == "head":
    b_origin = unreal.Vector(b_origin.x, b_origin.y,
                             b_origin.z + b_extent.z * 0.62)
    size = size * 0.42
elif frame == "chest":
    ## 1.2: the throat speaker under the collar at ~1.3 m
    b_origin = unreal.Vector(b_origin.x, b_origin.y,
                             b_origin.z + b_extent.z * 0.12)
    size = size * 0.22
elif frame == "collar":
    ## 1.3: the collar band and the dead bell at ~1 m, front-on like the chest
    b_origin = unreal.Vector(b_origin.x, b_origin.y,
                             b_origin.z + b_extent.z * 0.25)
    size = size * 0.17
elif frame in ("handr", "handl"):
    ## 1.4: a hand at ~1 m, front-on; handr = the mitt (+X), handl = the iron hand
    _hs = -1.0 if frame == "handr" else 1.0   # the rig yaws the actor 180: build +X is frame -X (1.4 pass 3 swapped them)
    b_origin = unreal.Vector(b_origin.x + _hs * b_extent.x * 0.72, b_origin.y,
                             b_origin.z - b_extent.z * 0.50)
    size = size * 0.19
elif frame == "legs":
    ## 1.5: the legs, feet and plinths at ~1.6 m, front-on
    b_origin = unreal.Vector(b_origin.x, b_origin.y, b_origin.z - b_extent.z * 0.68)
    size = size * 0.30
elif frame == "tail":
    ## 1.6: the tail from behind, low — one continuous mass grounded, no gaps
    b_origin = unreal.Vector(b_origin.x, b_origin.y, b_origin.z - b_extent.z * 0.62)
    size = size * 0.42
elif frame == "torso":
    ## 1.1c: the belly and patches at ~1.3 m — the seam maps must hold here
    b_origin = unreal.Vector(b_origin.x, b_origin.y,
                             b_origin.z - b_extent.z * 0.10)
    size = size * 0.26   # ~1.5 m: belly, rims and three patches in frame
dist = max(size * 3.2, 120.0)
## per-frame bearing: the full/head/torso 3/4 view, the chest frame front-on so
## the throat speaker (centre chest, facing -Y after the 180 yaw) is framed
import math as _math
## 1.2: bracketed at 200/240/280 — 280 is the front (speaker centred). Default it for the chest.
_bear = os.environ.get("UE_CAPTURE_BEARING") or ("280" if frame in ("chest", "collar", "handr", "handl", "legs") else ("100" if frame == "tail" else None))
if _bear:
    _bx, _by = _math.cos(_math.radians(float(_bear))), _math.sin(_math.radians(float(_bear)))
else:
    _bx, _by = (-0.72, -0.6)
cam_loc = unreal.Vector(b_origin.x + dist * _bx, b_origin.y + dist * _by,
                        b_origin.z + size * 0.25)
cam = eas.spawn_actor_from_class(unreal.CameraActor, cam_loc)
look = unreal.MathLibrary.find_look_at_rotation(cam_loc, b_origin)
cam.set_actor_rotation(look, False)
## 1.1c: the torso closeup gets its own warm fill at the camera — the rig's
## key models the head and leaves the torso in shadow at 1.5 m. Look-dev
## practice for a closeup; full/head frames stay comparable with 0.3.
if frame in ("torso", "chest", "collar", "handr", "handl", "legs", "tail"):
    fill = eas.spawn_actor_from_class(unreal.PointLight, cam_loc)
    ## 1.3 finding: 6 cd at a metre is four times the 1.6-lux key — the plaid
    ## whites out and brass clips to pale yellow. The collar frame meters BELOW
    ## the key; torso/chest keep their baselines. UE_CAPTURE_FILL overrides.
    _fill_default = {"collar": 1.5, "handr": 1.5, "handl": 1.5, "legs": 1.5, "tail": 1.5}.get(frame, 6.0)
    _fill_cd = float(os.environ.get("UE_CAPTURE_FILL") or _fill_default)
    fill.light_component.set_intensity(_fill_cd if dark else 20.0)   # 900 cd blew the frame to white
    unreal.log_warning("CAPTURE-FILL %s %.2f cd" % (frame, _fill_cd))
    fill.light_component.set_editor_property("intensity_units", unreal.LightUnits.CANDELAS)
    fill.light_component.set_light_color(unreal.LinearColor(1.0, 0.85, 0.65, 1.0))
    fill.light_component.set_editor_property("attenuation_radius", 600.0)
    fill.light_component.set_editor_property("cast_shadows", False)

if unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_name() == "L_AutoCapture":
    les.save_current_level()   # never save any other level from here

## 1.9: UE_CAPTURE_ANIM=<AnimSequence path> plays the clip on the skeletal
## subject in single-node mode and UE_CAPTURE_SEQ=N takes N evenly spaced
## frames (<out>_f00.png ...) — the frame-sequence acceptance capture
## (PLAN §4: >= 8 frames). Root motion stays in the component, so the
## figure crosses the frame; that is the point of the overlay.
_anim_path = os.environ.get("UE_CAPTURE_ANIM")
_seq_n = int(os.environ.get("UE_CAPTURE_SEQ", "0") or 0)
_anim = None
_anim_len = 0.0
_lseq = None
_lseq_fps = 30
if _anim_path and isinstance(subj_asset, unreal.SkeletalMesh):
    _anim = unreal.EditorAssetLibrary.load_asset(_anim_path)
    if _anim is not None:
        _anim_len = float(_anim.get_editor_property("sequence_length"))
        ## an unticked editor world never evaluates a skeletal pose; Sequencer
        ## does (it is how Movie Render Queue works) — a throwaway level
        ## sequence binds the subject with an animation section, and the
        ## capture scrubs its time per frame
        _at = unreal.AssetToolsHelpers.get_asset_tools()
        _lseq_path = "/Game/Dev/LS_AutoCapture"
        if unreal.EditorAssetLibrary.does_asset_exist(_lseq_path):
            unreal.EditorAssetLibrary.delete_asset(_lseq_path)
        _lseq = _at.create_asset("LS_AutoCapture", "/Game/Dev", unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
        _lseq.set_display_rate(unreal.FrameRate(_lseq_fps, 1))
        _total = int(round(_anim_len * _lseq_fps)) + 1
        _lseq.set_playback_start(0)
        _lseq.set_playback_end(_total)
        _bind = _lseq.add_possessable(subj)
        _trk = _bind.add_track(unreal.MovieSceneSkeletalAnimationTrack)
        _sec = _trk.add_section()
        _sec.set_range(0, _total)
        _params = _sec.get_editor_property("params")
        _params.set_editor_property("animation", _anim)
        _sec.set_editor_property("params", _params)
        unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(_lseq)
        unreal.LevelSequenceEditorBlueprintLibrary.set_current_time(0)
        unreal.log_warning("CAPTURE-ANIM %s length=%.3f frames=%d via Sequencer (%d frames @%d)" % (_anim_path, _anim_len, _seq_n, _total, _lseq_fps))

## screenshot after the renderer has had frames to warm up, then quit
state = {"ticks": 0, "shot": False, "handle": None, "seq_i": 0}
_seq_stride = 20

def _seq_name(i):
    _b, _e = os.path.splitext(OUT)
    return "%s_f%02d%s" % (_b, i, _e)

def _tick(dt):
    state["ticks"] += 1
    if _anim is not None and _seq_n > 0:
        _i = state["seq_i"]
        if _i < _seq_n and state["ticks"] >= 90 and (state["ticks"] - 90) % _seq_stride == 0:
            _t = _anim_len * _i / float(_seq_n)
            unreal.LevelSequenceEditorBlueprintLibrary.set_current_time(int(round(_t * _lseq_fps)))
            try:
                _c = subj.skeletal_mesh_component
                unreal.log_warning("CAPTURE-SEQ-DIAG actor=%s cam=%s root=%s head=%s pelvis=%s" % (
                    subj.get_actor_location(), cam.get_actor_location(),
                    _c.get_socket_location("root"), _c.get_socket_location("head"), _c.get_socket_location("pelvis")))
            except Exception as _ex:
                unreal.log_warning("CAPTURE-SEQ-DIAG err %s" % _ex)
            unreal.AutomationLibrary.take_high_res_screenshot(1600, 900, _seq_name(_i), camera=cam)
            unreal.log_warning("CAPTURE-SEQ %d t=%.3f %s" % (_i, _t, _seq_name(_i)))
            state["seq_i"] = _i + 1
        if state["ticks"] >= 90 + _seq_stride * (_seq_n + 3):
            unreal.unregister_slate_post_tick_callback(state["handle"])
            _have = sum(1 for k in range(_seq_n) if os.path.exists(_seq_name(k)))
            unreal.log_warning("CAPTURE-SEQ-SAVED %d of %d" % (_have, _seq_n))
            unreal.SystemLibrary.quit_editor()
        return
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
