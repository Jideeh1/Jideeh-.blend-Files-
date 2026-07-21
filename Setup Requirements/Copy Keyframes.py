import bpy
import re

OLD_DIVISOR = 0.1

MOUTH2D = {
    "Fac_Mth_Up": ("Mth Bone", 1, +1.0),
    "Fac_Mth_Down": ("Mth Bone", 1, -1.0),
    "Fac_Mth_Left": ("Mth Bone", 0, +1.0),
    "Fac_Mth_Right": ("Mth Bone", 0, -1.0),
}


def get_face_mesh():
    for obj in bpy.data.objects:
        n = obj.name.lower()
        if "_face" in n and "weapon_" not in n and "gun_" not in n:
            return obj
    return None


def gather_fcurves(arm):
    out = []
    adata = arm.animation_data
    if adata:
        if adata.action:
            out.extend(adata.action.fcurves)
        for tr in adata.nla_tracks:
            for st in tr.strips:
                if st.action:
                    out.extend(st.action.fcurves)
    return out


def is_control_bone(name):
    return name.startswith("CTRL-") or name.startswith("Face-Root")


faceobj = get_face_mesh()
if faceobj is None or faceobj.data.shape_keys is None:
    raise Exception("No '*_face' mesh with shape keys found.")
print("Face mesh:", faceobj.name)

armatures = [o for o in bpy.data.objects if o.type == 'ARMATURE']
print("Armatures in scene:", [a.name for a in armatures])

new_arm = None
for a in armatures:
    if any(b.name.startswith("CTRL-") for b in a.data.bones):
        new_arm = a
        break
if new_arm is None:
    raise Exception("Couldn't find the new control armature (no 'CTRL-' bones). Build the rig first.")
print("New control armature:", new_arm.name,
      "(%d CTRL bones)" % sum(1 for b in new_arm.data.bones if b.name.startswith("CTRL-")))

old_loc_fcurves = []
sources = {}
for a in armatures:
    for fc in gather_fcurves(a):
        if 'pose.bones' not in fc.data_path or not fc.data_path.endswith('.location'):
            continue
        m = re.search(r'pose\.bones\["(.+?)"\]', fc.data_path)
        if not m:
            continue
        bn = m.group(1)
        if is_control_bone(bn):
            continue
        old_loc_fcurves.append(fc)
        sources.setdefault(a.name, set()).add(bn)

if not old_loc_fcurves:
    raise Exception("Found no animated non-control bones anywhere. Nothing to copy from.")

for an, bs in sources.items():
    print("Animated panel bones on '%s': %s" % (an, sorted(bs)))

fc_map = {}
for fc in old_loc_fcurves:
    m = re.search(r'pose\.bones\["(.+?)"\]\.location', fc.data_path)
    if m:
        fc_map[(m.group(1), fc.array_index)] = fc

ad = faceobj.data.shape_keys.animation_data
if ad is None or not ad.drivers:
    raise Exception("Shape keys have no drivers. Build the new rig before transferring.")

inv = {}
for d in ad.drivers:
    m = re.search(r'key_blocks\["(.+?)"\]\.value', d.data_path)
    if not m:
        continue
    skname = m.group(1)
    expr = d.driver.expression
    for v in d.driver.variables:
        t = v.targets[0]
        if not t.bone_target:
            continue
        mm = re.search(re.escape(v.name) + r'\s*/\s*([0-9.eE+-]+)', expr)
        lim = float(mm.group(1)) if mm else 1.0
        sign = -1.0 if re.search(r'-\s*' + re.escape(v.name), expr) else 1.0
        inv.setdefault(skname, []).append(
            {'bone': t.bone_target, 'ttype': t.transform_type, 'sign': sign, 'lim': lim})
print("Shape keys driven by the new rig:", len(inv))


def old_bone_axis(skname):
    if skname in MOUTH2D:
        return MOUTH2D[skname]
    base = skname[4:] if skname.startswith("Fac_") else skname
    return (base + " Bone", 0, 1.0)


matched, unmatched = [], []
for skname in inv:
    bone, idx, sgn = old_bone_axis(skname)
    if (bone, idx) in fc_map:
        matched.append(skname)
    else:
        unmatched.append((skname, bone))
print("Matched %d/%d shape keys to panel bones." % (len(matched), len(inv)))
if unmatched:
    print("UNMATCHED (no panel fcurve found):")
    for sk, bn in unmatched:
        print("   shapekey '%s' expected panel bone '%s'" % (sk, bn))
if not matched:
    raise Exception("No shape keys matched panel bones. Compare the printed panel bone "
                    "names with the expected names in the UNMATCHED list and tell me.")


def old_value(skname, frame):
    bone, idx, sgn = old_bone_axis(skname)
    fc = fc_map.get((bone, idx))
    if fc is None:
        return 0.0
    return sgn * (fc.evaluate(frame) / OLD_DIVISOR)


allframes = []
for fc in old_loc_fcurves:
    for kp in fc.keyframe_points:
        allframes.append(kp.co.x)
f0, f1 = int(round(min(allframes))), int(round(max(allframes)))
print("Frame range:", f0, "-", f1)

ttype_idx = {'LOC_X': 0, 'LOC_Y': 1, 'LOC_Z': 2}
written = 0
for f in range(f0, f1 + 1):
    acc = {}
    for skname, entries in inv.items():
        val = old_value(skname, f)
        for e in entries:
            k = (e['bone'], e['ttype'])
            acc[k] = acc.get(k, 0.0) + e['sign'] * val * e['lim']
    for (bone, ttype), loc in acc.items():
        pb = new_arm.pose.bones.get(bone)
        if pb is None:
            continue
        i = ttype_idx.get(ttype, 0)
        pb.location[i] = loc
        pb.keyframe_insert(data_path="location", index=i, frame=f)
        written += 1

print("Done. Wrote %d keyframes onto '%s'." % (written, new_arm.name))
print("Old panel bones are left intact; hide/delete them once the result looks right.")