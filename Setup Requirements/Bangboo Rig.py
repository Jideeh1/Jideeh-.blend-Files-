# Bangboo_Rig.py
# ---------------------------------------------------------------------------
# Builds a simple FK rig for the Bangboo and sorts bones into two collections:
#   "Body"   - the character (skeleton, ears, tail, face-expression bones)
#   "Others" - everything unrelated to the body (weapon/turret, stands, guns,
#              doors, pedestals, corners, structural roots)
#
# WHY NOT RIGIFY: a Bangboo has a 1-bone spine and no neck/fingers/toes, so the
# Rigify human metarig can't be extracted from it. This gives clean FK controls
# (widgets on the deform bones, chain-parented as imported) which is the right
# fit for a simple mascot. Ask if you want IK arms/legs on top.
#
# HOW TO USE: select the Bangboo armature (or just run - it finds it), paste
# into the Text Editor, Run Script. Re-running is safe.
# ---------------------------------------------------------------------------

import bpy
import math
import mathutils

# ============================ CONFIG =======================================
RIG_NAME = ""          # "" = active armature, else set the object name
BODY_WIDGET_SCALE = 0.6
ROOT_WIDGET_SCALE = 1.6
HIDE_OTHERS = False    # True = start with the "Others" collection hidden
# ===========================================================================

V = mathutils.Vector

# Bones that count as "the body" (everything else -> Others).
BODY = {
    "Bip001",
    "Skin_Pelvis", "Skin_Spine", "Skin_Head",
    "Skin_Clavicle_L", "Skin_UpperArm_L", "Skin_Forearm_L", "Skin_Hand_L",
    "Skin_Clavicle_R", "Skin_UpperArm_R", "Skin_Forearm_R", "Skin_Hand_R",
    "Skin_Thigh_L", "Skin_Calf_L", "Skin_Foot_L",
    "Skin_Thigh_R", "Skin_Calf_R", "Skin_Foot_R",
    "Skn_L_Clavicle_Fix", "Skn_R_Clavicle_Fix",
    "Ctr_Tail",
    "Ctr_L_EarA_01", "Ctr_L_EarA_02", "Ctr_L_EarA_03",
    "Ctr_R_EarA_01", "Ctr_R_EarA_02", "Ctr_R_EarA_03",
    "Ext_Bn_Fac_Angry", "Ext_Bn_Fac_Happy", "Ext_Bn_Fac_Normal",
    "Ext_Bn_Fac_Sad", "Ext_Bn_Fac_Sluggish",
}
ROOT_BONE = "Bip001"


def find_rig():
    if RIG_NAME:
        o = bpy.data.objects.get(RIG_NAME)
        if o and o.type == 'ARMATURE':
            return o
        raise Exception(f"'{RIG_NAME}' is not an armature.")
    ao = bpy.context.active_object
    if ao and ao.type == 'ARMATURE':
        return ao
    a = [o for o in bpy.data.objects if o.type == 'ARMATURE']
    if not a:
        raise Exception("No armature found.")
    return a[0]


def ring_widget(name, radius=1.0):
    ob = bpy.data.objects.get(name)
    if ob:
        return ob
    n = 16
    verts = [(radius * math.cos(2 * math.pi * i / n), 0.0, radius * math.sin(2 * math.pi * i / n))
             for i in range(n)]
    edges = [(i, (i + 1) % n) for i in range(n)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, edges, [])
    me.update()
    ob = bpy.data.objects.new(name, me)
    wcoll = bpy.data.collections.get("WGTS_Bangboo")
    if wcoll is None:
        wcoll = bpy.data.collections.new("WGTS_Bangboo")
        bpy.context.scene.collection.children.link(wcoll)
        wcoll.hide_viewport = True
    wcoll.objects.link(ob)
    ob.hide_render = True
    return ob


def main():
    rig = find_rig()
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    rig.show_in_front = True
    if rig.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    cols = rig.data.collections
    body_col = cols.get("Body") or cols.new("Body")
    others_col = cols.get("Others") or cols.new("Others")

    ring = ring_widget("WGT-bangboo_ring", 1.0)
    root_ring = ring_widget("WGT-bangboo_root", 1.0)

    bpy.ops.object.mode_set(mode='POSE')

    body_count = others_count = 0
    for pb in rig.pose.bones:
        # (re)assign cleanly to exactly one of the two collections
        for c in (body_col, others_col):
            try:
                c.unassign(pb)
            except Exception:
                pass

        if pb.name in BODY:
            body_col.assign(pb)
            body_count += 1
            pb.rotation_mode = 'XYZ'
            pb.lock_scale = (True, True, True)
            if pb.name == ROOT_BONE:
                pb.custom_shape = root_ring
                scale = ROOT_WIDGET_SCALE
            else:
                pb.custom_shape = ring
                scale = BODY_WIDGET_SCALE
            try:
                pb.custom_shape_scale_xyz = (scale, scale, scale)
            except Exception:
                pb.custom_shape_scale = scale
        else:
            others_col.assign(pb)
            others_count += 1

    bpy.ops.object.mode_set(mode='OBJECT')

    # visibility
    try:
        for c in cols:
            c.is_visible = True
        if HIDE_OTHERS:
            others_col.is_visible = False
    except Exception:
        pass

    print("=" * 55)
    print(f"Rig:            {rig.name}")
    print(f"Body bones:     {body_count}  -> 'Body' collection")
    print(f"Other bones:    {others_count} -> 'Others' collection")
    print("FK: select a bone in Pose Mode and rotate. Bip001 is the root.")
    print("=" * 55)


main()