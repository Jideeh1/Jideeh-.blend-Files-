# FaceRig_Add_Drivers.py
# ---------------------------------------------------------------------------
# Your face panel + control bones already exist, but the shape keys have no
# drivers (so moving the controls does nothing). This wires them up: for every
# "<name> Bone" control in the FaceRig, it finds the matching shape key and
# adds a driver  value = bone_local_X / DRIVE_RANGE.
#
# It matches names loosely (ignores the "Fac_" prefix and case), finds the
# FaceRig even if it was renamed, and searches every mesh's shape keys - so it
# works no matter why the original driver step failed.
#
# HOW TO USE: paste into the Text Editor, Run Script. Read the console: it
# reports how many drivers it added and lists any bones with no matching key.
# Safe to re-run (it replaces existing value drivers).
# ---------------------------------------------------------------------------

import bpy

# ============================ CONFIG =======================================
FACERIG_NAME  = "FaceRig"   # falls back to any armature made of "... Bone" bones
DRIVE_RANGE   = 0.1         # bone local-X travel that maps to full shape-key value
BIDIRECTIONAL = True        # True: drag -X..+X -> value -1..+1 ; False: 0..1
# ===========================================================================


def find_facerig():
    o = bpy.data.objects.get(FACERIG_NAME)
    if o and o.type == 'ARMATURE':
        return o
    return next((a for a in bpy.data.objects
                 if a.type == 'ARMATURE'
                 and any(b.name.endswith(" Bone") for b in a.data.bones)), None)


def norm(s):
    if s.startswith("Fac_"):
        s = s[4:]
    return s.strip().lower()


def make_driver(sk, rig, bone_name, transform_type, expr, slider_min):
    try:
        sk.driver_remove("value")
    except Exception:
        pass
    sk.slider_min = slider_min
    sk.slider_max = 1.0
    d = sk.driver_add("value").driver
    d.type = 'SCRIPTED'
    v = d.variables.new()
    v.name = "var"
    v.type = 'TRANSFORMS'
    t = v.targets[0]
    t.id = rig
    t.bone_target = bone_name
    t.transform_type = transform_type
    t.transform_space = 'LOCAL_SPACE'
    d.expression = expr


def main():
    fr = find_facerig()
    if fr is None:
        raise Exception("No FaceRig armature (with '... Bone' controls) found.")

    # index every shape key by normalized name; prefer a *_face mesh
    meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.shape_keys]
    meshes.sort(key=lambda m: 0 if "_face" in m.name.lower() else 1)
    sk_index = {}
    for m in meshes:
        for sk in m.data.shape_keys.key_blocks:
            if sk.name == "Basis":
                continue
            sk_index.setdefault(norm(sk.name), sk)

    added = 0
    missed = []
    mouth_bone = None
    lo = -1.0 if BIDIRECTIONAL else 0.0

    for b in fr.data.bones:
        if not b.name.endswith(" Bone"):
            continue
        base = b.name[:-5]                 # strip " Bone"
        if base.strip().lower() == "mth":  # the 2D mouth joystick, handled below
            mouth_bone = b.name
            continue
        sk = sk_index.get(norm(base))
        if sk is None:
            missed.append(b.name)
            continue
        make_driver(sk, fr, b.name, 'LOC_X', "var / %s" % DRIVE_RANGE, lo)
        added += 1

    # 2D mouth joystick: X = left/right, Y = up/down
    if mouth_bone:
        for keyname, axis, expr in (
                ("mth_left", 'LOC_X', "var / %s" % DRIVE_RANGE),
                ("mth_right", 'LOC_X', "-var / %s" % DRIVE_RANGE),
                ("mth_up", 'LOC_Y', "var / %s" % DRIVE_RANGE),
                ("mth_down", 'LOC_Y', "-var / %s" % DRIVE_RANGE)):
            sk = sk_index.get(keyname)
            if sk is not None:
                make_driver(sk, fr, mouth_bone, axis, expr, 0.0)
                added += 1

    print("=" * 60)
    print(f"FaceRig: {fr.name}")
    print(f"Drivers added: {added}")
    if mouth_bone:
        print(f"Mouth joystick wired: {mouth_bone}")
    if missed:
        print(f"\nControl bones with NO matching shape key ({len(missed)}):")
        for n in missed:
            print("   " + n)
        print("(If these should be driven, the shape-key names differ from the "
              "bone names - paste this list to Claude.)")
    print("=" * 60)


main()