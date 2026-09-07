"""THE AFTER-FIRE RIG (unit 1.9, tranche 1) — a hand-built minimal armature,
rigid weights, no physics, no cloth, no jiggle (MOTION §PRODUCTION NOTES).

Runs on blend/chum_af.blend AFTER the build:
  Blender --background blend/chum_af.blend --python tools/rig_chum_af.py
Writes blend/chum_af_rig.blend with:
  * armature SK_ChumAF — bones per docs/production/CHUM-RIG-AND-ANIMATION-SPEC.md,
    positions from the spec's 2.6 m base numbers x the frozen 3.35/2.6
    (the build's nested pivot empties carry wrong world transforms after
    the scale pass, so they are NOT trusted for positions — only for
    ancestry);
  * every mesh bound with an Armature modifier and vertex groups at 1.0
    ("wool baked stiff"), split by height at hip / knee / shoulder / elbow /
    neck with 3 cm blend bands; fingers one bone each in this tranche;
  * SOCKET_ empties re-parented to bones (UE makes sockets from them);
  * the build's pivot empties removed (they would export as stray nodes).
Bone side law: the build's -X (LegL, ArmL, the iron hand) is the rig's _r.
"""
import bpy
import math
import os
import mathutils

K = 3.35 / 2.6
BAND = 0.03 * K          # blend band half-width, metres (scaled)


def V(x, y, z):
    return mathutils.Vector((x * K, y * K, z * K))


## ---- bone table: name -> (parent, head, tail)  [2.6 m base numbers] --------------
BONES = {}
def bone(name, parent, head, tail):
    BONES[name] = (parent, V(*head), V(*tail))

## the ROOT is the armature OBJECT itself, named "root": the engine turns the
## armature node into the top bone anyway (1.9 finding: an "sk_chumaf" bone
## appeared above "root"), and an object-level translation gets the unit
## scale that bone curves never do — so root motion is keyed on the object
bone("pelvis",   None,       (0, 0, 0.98),     (0, 0, 1.40))
bone("spine_01", "pelvis",   (0, 0, 1.40),     (0, 0.02, 1.80))
bone("spine_02", "spine_01", (0, 0.02, 1.80),  (0, 0, 2.02))
bone("neck",     "spine_02", (0, 0, 2.02),     (0, 0, 2.28))
bone("head",     "neck",     (0, 0, 2.28),     (0, 0, 2.80))
bone("jaw",      "head",     (0, 0.06, 2.10),  (0, -0.26, 2.04))
bone("eye_tally","head",     (0.13, -0.37, 2.34), (0.13, -0.47, 2.34))
bone("bell",     "neck",     (0, -0.33, 1.99), (0, -0.33, 1.90))
bone("ear_r",    "head",     (-0.24, 0.03, 2.60), (-0.30, 0.03, 3.05))
bone("ear_l",    "head",     (0.24, 0.03, 2.60),  (0.30, 0.03, 3.05))
bone("tail_01",  "pelvis",   (0.04, 0.36, 0.76), (0.28, 0.76, 0.31))
bone("tail_02",  "tail_01",  (0.28, 0.76, 0.31), (0.57, 0.98, 0.06))
for side, sx in (("r", -1), ("l", 1)):
    bone(f"clavicle_{side}", "spine_02", (0.18 * sx, 0, 1.82),   (0.47 * sx, 0, 1.72))
    bone(f"upperarm_{side}", f"clavicle_{side}", (0.47 * sx, 0, 1.72), (0.55 * sx, -0.03, 1.26))
    bone(f"lowerarm_{side}", f"upperarm_{side}", (0.55 * sx, -0.03, 1.26), (0.60 * sx, -0.06, 0.97))
    bone(f"hand_{side}",     f"lowerarm_{side}", (0.60 * sx, -0.06, 0.97), (0.62 * sx, -0.07, 0.84))
    bone(f"thigh_{side}",    "pelvis",           (0.20 * sx, 0, 0.92),  (0.20 * sx, 0, 0.46))
    bone(f"calf_{side}",     f"thigh_{side}",    (0.20 * sx, 0, 0.46),  (0.20 * sx, -0.02, 0.20))
    bone(f"foot_{side}",     f"calf_{side}",     (0.20 * sx, -0.02, 0.20), (0.20 * sx, -0.22, 0.10))
    bone(f"ball_{side}",     f"foot_{side}",     (0.20 * sx, -0.22, 0.10), (0.20 * sx, -0.38, 0.085))

## the build's pivot empty -> rig bone (ancestry only; build -X is rig _r)
PIVOT_BONE = {
    "Head": "head", "Jaw": "jaw", "TailPivot": "tail_01",
    "HipL": "thigh_r", "HipR": "thigh_l", "ShoulderL": "upperarm_r", "ShoulderR": "upperarm_l",
    "calf_r": "calf_r", "calf_l": "calf_l", "foot_r": "foot_r", "foot_l": "foot_l",
    "ball_r": "ball_r", "ball_l": "ball_l", "hand_r": "hand_r", "hand_l": "hand_l",
}

## heights of the splits (scaled metres)
Z_HIP = 1.40 * K      # pelvis | spine_01
Z_CHEST = 1.80 * K    # spine_01 | spine_02
Z_NECK = 2.02 * K     # spine_02 | neck
Z_HEAD = 2.28 * K     # neck | head
Z_KNEE = 0.46 * K
Z_ANKLE = 0.20 * K
Z_ELBOW = 1.26 * K
Z_WRIST = 0.97 * K
Y_TAIL = 0.76 * K


def blend(z, z_split, lo_bone, hi_bone):
    """weights for a vertex at height z across a split: (bone, w) pairs"""
    t = (z - (z_split - BAND)) / (2.0 * BAND)
    if t <= 0.0:
        return [(lo_bone, 1.0)]
    if t >= 1.0:
        return [(hi_bone, 1.0)]
    return [(lo_bone, 1.0 - t), (hi_bone, t)]


def ancestry_pivot(ob):
    """the first build pivot empty above this object, and the finger pivot if any"""
    finger = None
    p = ob.parent
    while p is not None:
        if p.type == "EMPTY":
            if p.name.startswith("finger_") and finger is None:
                finger = p.name
            if p.name in PIVOT_BONE:
                return p.name, finger
        p = p.parent
    return None, finger


def finger_bone_name(pivot_name):
    # finger_a_02_r -> finger_a_r (one bone per finger this tranche)
    parts = pivot_name.split("_")
    return f"finger_{parts[1]}_{parts[3]}"


def vertex_bones(ob, wpos, pivot, finger):
    """rule per vertex: (bone, weight) pairs"""
    n = ob.name
    z = wpos.z
    if finger:
        return [(finger_bone_name(finger), 1.0)]
    if pivot == "Head":
        if n.startswith(("TallyLens", "TallyCore", "LensRing", "LensRivet", "Camera_01")):
            return [("eye_tally", 1.0)]
        if n.startswith("EarL"):
            return [("ear_r", 1.0)]
        if n.startswith("EarR"):
            return [("ear_l", 1.0)]
        return [("head", 1.0)]
    if pivot == "Jaw":
        return [("jaw", 1.0)]
    if pivot == "TailPivot":
        t = (wpos.y - (Y_TAIL - BAND)) / (2.0 * BAND)
        if t <= 0: return [("tail_01", 1.0)]
        if t >= 1: return [("tail_02", 1.0)]
        return [("tail_01", 1.0 - t), ("tail_02", t)]
    if pivot in ("HipL", "HipR"):
        side = "r" if pivot == "HipL" else "l"
        if z > Z_KNEE + BAND:
            return [(f"thigh_{side}", 1.0)]
        if z > Z_ANKLE - BAND:
            return blend(z, Z_KNEE, f"calf_{side}", f"thigh_{side}") if z > Z_KNEE - BAND else blend(z, Z_ANKLE, f"foot_{side}", f"calf_{side}")
        return [(f"foot_{side}", 1.0)]
    if pivot in ("calf_r", "calf_l"):
        side = pivot[-1]
        return blend(z, Z_ANKLE, f"foot_{side}", f"calf_{side}")
    if pivot in ("foot_r", "foot_l", "ball_r", "ball_l"):
        side = pivot[-1]
        return [(pivot if pivot.startswith("ball") else f"foot_{side}", 1.0)]
    if pivot in ("ShoulderL", "ShoulderR"):
        side = "r" if pivot == "ShoulderL" else "l"
        if z > Z_ELBOW + BAND:
            return [(f"upperarm_{side}", 1.0)]
        if z > Z_WRIST + BAND:
            return blend(z, Z_ELBOW, f"lowerarm_{side}", f"upperarm_{side}")
        return blend(z, Z_WRIST, f"hand_{side}", f"lowerarm_{side}")
    if pivot in ("hand_r", "hand_l"):
        return [(pivot, 1.0)]
    ## unparented: the torso and its dressings, the collar, the bell
    if n.startswith(("Bell",)):
        return [("bell", 1.0)]
    if n.startswith(("Collar", "Throat")):
        return [("neck", 1.0)]
    if z > Z_NECK - BAND:
        return blend(z, Z_NECK, "spine_02", "neck")
    if z > Z_CHEST - BAND:
        return blend(z, Z_CHEST, "spine_01", "spine_02")
    if z > Z_HIP - BAND:
        return blend(z, Z_HIP, "pelvis", "spine_01")
    return [("pelvis", 1.0)]


def main():
    scene = bpy.context.scene
    ## curves -> meshes (an armature deforms curves too, but the export and
    ## the engine want meshes)
    for o in [o for o in bpy.data.objects if o.type == "CURVE" and not o.hide_render]:
        bpy.ops.object.select_all(action="DESELECT")
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        try:
            bpy.ops.object.convert(target="MESH")
        except RuntimeError as ex:
            print("RIG-CURVE-SKIP", o.name, ex)

    ## the armature
    arm_data = bpy.data.armatures.new("SK_ChumAF")
    arm = bpy.data.objects.new("root", arm_data)   # the object node IS the root bone in the engine
    scene.collection.objects.link(arm)
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    eb = {}
    for name, (parent, head, tail) in BONES.items():
        b = arm_data.edit_bones.new(name)
        b.head = head
        b.tail = tail
        eb[name] = b
    for name, (parent, head, tail) in BONES.items():
        if parent:
            eb[name].parent = eb[parent]
            eb[name].use_connect = False
    ## finger bones: one per finger, from the finger meshes' world bounds
    finger_meshes = {}
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        pivot, finger = ancestry_pivot(o)
        if finger:
            finger_meshes.setdefault(finger_bone_name(finger), []).append(o)
    for fb, meshes in sorted(finger_meshes.items()):
        pts = [o.matrix_world @ mathutils.Vector(c) for o in meshes for c in o.bound_box]
        top = max(pts, key=lambda p: p.z)
        bot = min(pts, key=lambda p: p.z)
        cx = sum(p.x for p in pts) / len(pts)
        cy = sum(p.y for p in pts) / len(pts)
        b = arm_data.edit_bones.new(fb)
        b.head = mathutils.Vector((cx, cy, top.z))
        b.tail = mathutils.Vector((cx, cy, max(bot.z, top.z - 0.05)))
        b.parent = eb["hand_" + fb[-1]]
        eb[fb] = b
    bpy.ops.object.mode_set(mode="OBJECT")
    print("RIG bones", len(arm_data.bones), "+ the object node as root")

    ## UCX_ boxes are static-mesh collision; a skeletal mesh takes a physics
    ## asset (tranche 2) — drop them so they neither bind nor export as geometry
    for o in [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith("UCX_")]:
        bpy.data.objects.remove(o, do_unlink=True)
    ## bind every mesh: vertex groups from the rule, rigid, then the modifier
    bound = 0
    for o in [o for o in bpy.data.objects if o.type == "MESH"]:
        pivot, finger = ancestry_pivot(o)
        mw = o.matrix_world.copy()
        groups = {}
        for v in o.data.vertices:
            for bname, w in vertex_bones(o, mw @ v.co, pivot, finger):
                if bname not in arm_data.bones:
                    bname = "head" if pivot == "Head" else "pelvis"
                groups.setdefault(bname, []).append((v.index, w))
        for g in list(o.vertex_groups):
            o.vertex_groups.remove(g)
        for bname, entries in groups.items():
            vg = o.vertex_groups.new(name=bname)
            for idx, w in entries:
                vg.add([idx], w, "REPLACE")
        ## world transform frozen; parent to the armature, keep the mesh where it is
        o.parent = arm
        o.matrix_parent_inverse = arm.matrix_world.inverted()
        o.matrix_world = mw
        for m in [m for m in o.modifiers if m.type == "ARMATURE"]:
            o.modifiers.remove(m)
        am = o.modifiers.new("Armature", "ARMATURE")
        am.object = arm
        bound += 1
    print("RIG bound meshes", bound)

    ## sockets ride their bones; the build's pivots go
    sock_bone = {"SOCKET_EyeTally": "eye_tally", "SOCKET_JawLever": "head",
                 "SOCKET_Bell": "bell", "SOCKET_ThroatSpeaker": "spine_02"}
    for name, bname in sock_bone.items():
        e = bpy.data.objects.get(name)
        if e is None:
            continue
        mw = e.matrix_world.copy()
        e.parent = arm
        e.parent_type = "BONE"
        e.parent_bone = bname
        e.matrix_world = mw
    for e in [o for o in bpy.data.objects if o.type == "EMPTY" and not o.name.startswith("SOCKET_")]:
        bpy.data.objects.remove(e, do_unlink=True)
    print("RIG sockets", sum(1 for o in bpy.data.objects if o.name.startswith("SOCKET_")))

    out = os.path.join(os.path.dirname(bpy.data.filepath), "chum_af_rig.blend")
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print("RIG-SAVED", out)


main()
