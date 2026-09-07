"""THE POUR — After-Fire locomotion clips (unit 1.9, tranche 2).

Runs on blend/chum_af_rig.blend:
  Blender --background blend/chum_af_rig.blend --python tools/anim_chum_af.py
Authors actions on SK_ChumAF and saves blend/chum_af_anim.blend:
  A_ChumAF_Parked      one held frame — the statue (zero idle, no breathing)
  A_ChumAF_Pour_Walk   root motion 0.8 m/s, stride STRIDE m per cycle,
                       knees <= KNEE_MAX, the head leads each plant by
                       LEAD frames, torso follows in one arc
  A_ChumAF_Pour_Cross  the walk at 1.6 m/s (time-scaled; nothing added)
  A_ChumAF_Stop / A_ChumAF_Start   absolute, <= 2 frames each
Every key is LINEAR; only the two frames around each foot plant are
BEZIER caps ("LINEAR IS THE HORROR CURVE ... two-frame ease caps at most").
No anticipation, no overshoot, no settle, no secondary — nothing is keyed
that the canon forbids (tail, arms swing, bob beyond the stride geometry).
The eye is NOT keyed: the engine drives eye_tally on its own layer.
Writes renders/anim_curve_audit.txt: per action, key count, LINEAR vs
BEZIER counts, root speed, max head-height variation.
Forward is the build's -Y (the face); the root translates along -Y.
"""
import bpy
import math
import os

FPS = 30
K = 3.35 / 2.6
SPEED_WALK = 0.8            # m/s (MOTION §1)
SPEED_CROSS = 1.6           # m/s (double approach speed)
STRIDE = 1.40               # m per full cycle (two plants) — PROPOSAL, OPEN for the owner
SWING = math.radians(17.0)  # hip swing amplitude (± about X) that yields the stride on a 1.19 m leg
KNEE_MAX = math.radians(9.0)
LEAD = 3                    # frames the head leads each plant
LEG_LEN = 0.92 * K          # hip to ankle, scaled metres

arm = bpy.data.objects.get("root") or bpy.data.objects["SK_ChumAF"]
scene = bpy.context.scene
scene.render.fps = FPS


def new_action(name, frames):
    act = bpy.data.actions.new(name)
    act.use_fake_user = True
    scene.frame_start = 1
    scene.frame_end = frames
    return act


def key(pb, frame, rot=None, loc=None):
    if rot is not None:
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = rot
        pb.keyframe_insert("rotation_euler", frame=frame)
    if loc is not None:
        pb.location = loc
        pb.keyframe_insert("location", frame=frame)


def all_fcurves(act):
    """Blender 5.x layered actions: curves live in each strip's channel bags"""
    fcs = []
    if hasattr(act, "fcurves"):
        try:
            return list(act.fcurves)
        except Exception:
            pass
    for layer in act.layers:
        for strip in layer.strips:
            for cb in strip.channelbags:
                fcs.extend(cb.fcurves)
    return fcs


def set_interp(act, contact_frames):
    """LINEAR everywhere; BEZIER only within 1 frame of a contact (2-frame caps)"""
    lin = bez = 0
    for fc in all_fcurves(act):
        for kp in fc.keyframe_points:
            if any(abs(kp.co.x - c) <= 1 for c in contact_frames):
                kp.interpolation = "BEZIER"
                kp.easing = "AUTO"
                bez += 1
            else:
                kp.interpolation = "LINEAR"
                lin += 1
    return lin, bez


def reset_pose():
    for pb in arm.pose.bones:
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = (0, 0, 0)
        pb.location = (0, 0, 0)
    arm.location = (0, 0, 0)


def key_root(frame, y):
    """root motion on the armature OBJECT (world -Y forward); the object node
    is the engine's root bone and its translation carries the unit scale"""
    arm.location = (0.0, y, 0.0)
    arm.keyframe_insert("location", frame=frame)


bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
pb = arm.pose.bones
if arm.animation_data is None:
    arm.animation_data_create()

audit = []

## ---- A_ChumAF_Parked: one frame, everything at rest -----------------------------------
reset_pose()
act = new_action("A_ChumAF_Parked", 1)
arm.animation_data.action = act
for name in ("pelvis", "spine_01", "head", "jaw", "thigh_r", "thigh_l"):
    key(pb[name], 1, rot=(0, 0, 0), loc=(0, 0, 0))
key_root(1, 0.0)
lin, bez = set_interp(act, [])
audit.append(("A_ChumAF_Parked", 1, len(all_fcurves(act)), lin, bez, 0.0, 0.0))


## ---- the walk cycle ------------------------------------------------------------------
def author_walk(name, speed):
    reset_pose()
    cycle_s = STRIDE / speed
    frames = max(4, int(round(cycle_s * FPS)))
    act = new_action(name, frames)
    arm.animation_data.action = act
    half = frames // 2
    contacts = [1, half + 1, frames + 1]
    ## root motion: -Y forward, constant speed (root is the only bone that translates)
    ## Blender bone-local: the root bone's tail points +Y, so its local Y axis is
    ## world Y; a negative local-Y translation is forward.
    for f in (1, frames + 1):
        key_root(f, -(STRIDE * (f - 1) / frames))
    ## hips: a compass gait — plant at the extremes, straight legs, knees the
    ## canon's "nearly stiff"; the swing leg passes at mid-step
    for f in range(1, frames + 2):
        t = (f - 1) / frames                # 0..1 over the cycle
        ph = 2.0 * math.pi * t
        thigh_r = SWING * math.cos(ph)      # +: leg forward (rotation about X toward -Y)
        thigh_l = -thigh_r
        ## knee flex only on the swing leg near mid-swing, capped
        kr = KNEE_MAX * max(0.0, -math.sin(ph))
        kl = KNEE_MAX * max(0.0, math.sin(ph))
        if f in (1, half + 1, frames + 1) or (f - 1) % 3 == 0:
            key(pb["thigh_r"], f, rot=(thigh_r, 0, 0))
            key(pb["thigh_l"], f, rot=(thigh_l, 0, 0))
            key(pb["calf_r"], f, rot=(-kr, 0, 0))
            key(pb["calf_l"], f, rot=(-kl, 0, 0))
            ## the weighted foot stays level to the floor: counter the hip
            key(pb["foot_r"], f, rot=(-thigh_r + kr, 0, 0))
            key(pb["foot_l"], f, rot=(-thigh_l + kl, 0, 0))
            ## the pelvis rides the stance leg: height = L cos(swing) — the
            ## geometry's own bob, nothing added; keyed so the audit can read it
            dz = -(LEG_LEN * (1.0 - math.cos(SWING * abs(math.cos(ph)))))
            key(pb["pelvis"], f, loc=(0, 0, dz))
    ## the head leads each plant by LEAD frames: a small forward pitch of the
    ## neck peaking LEAD frames before contact, the torso arriving on the plant
    for c in contacts:
        key(pb["neck"], max(1, c - LEAD), rot=(math.radians(4.0), 0, 0))
        key(pb["spine_01"], c, rot=(math.radians(2.0), 0, 0))
        key(pb["neck"], min(frames + 1, c + LEAD), rot=(0, 0, 0))
        key(pb["spine_01"], min(frames + 1, c + 2 * LEAD), rot=(0, 0, 0))
    lin, bez = set_interp(act, contacts)
    ## audit: root speed and head-height variation from the keyed pelvis dz
    bob = LEG_LEN * (1.0 - math.cos(SWING))
    audit.append((name, frames, len(all_fcurves(act)), lin, bez, STRIDE / (frames / FPS), bob))
    return act


author_walk("A_ChumAF_Pour_Walk", SPEED_WALK)
author_walk("A_ChumAF_Pour_Cross", SPEED_CROSS)

## ---- stop / start: absolute, two frames -------------------------------------------------
for name, a, b in (("A_ChumAF_Stop", SWING * 0.5, 0.0), ("A_ChumAF_Start", 0.0, SWING * 0.5)):
    reset_pose()
    act = new_action(name, 2)
    arm.animation_data.action = act
    key(pb["thigh_r"], 1, rot=(a, 0, 0)); key(pb["thigh_l"], 1, rot=(-a, 0, 0))
    key(pb["thigh_r"], 2, rot=(b, 0, 0)); key(pb["thigh_l"], 2, rot=(-b, 0, 0))
    key_root(1, 0.0); key_root(2, 0.0)
    lin, bez = set_interp(act, [])
    audit.append((name, 2, len(all_fcurves(act)), lin, bez, 0.0, 0.0))

bpy.ops.object.mode_set(mode="OBJECT")
arm.animation_data.action = bpy.data.actions["A_ChumAF_Parked"]

root = os.path.dirname(os.path.dirname(os.path.abspath(bpy.data.filepath)))
os.makedirs(os.path.join(root, "renders"), exist_ok=True)
with open(os.path.join(root, "renders", "anim_curve_audit.txt"), "w") as f:
    f.write("action frames fcurves linear_keys bezier_keys root_speed_mps head_bob_m\n")
    for row in audit:
        f.write("%s %d %d %d %d %.3f %.3f\n" % row)
        print("ANIM", *row)
out = os.path.join(os.path.dirname(bpy.data.filepath), "chum_af_anim.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("ANIM-SAVED", out, "actions", [a.name for a in bpy.data.actions if a.name.startswith("A_ChumAF")])
