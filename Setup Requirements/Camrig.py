import bpy
import math
from mathutils import Vector, Matrix

RIG_NAME = "CAM_RIG"
WGT_COLL = "WGT_CAM_RIG"
CON_AIM = "CamRig Aim"
CON_FACE = "CamRig Face"
CON_SNAP = "CamRig Snap"
P_TRACK = "Track To"
P_DOF = "Depth of Field"
AIM_DIST = 5.0
YELLOW = (1.0, 0.82, 0.06)
MCH_BONES = ("MCH_TRACK", "MCH_ROLL")

ROOT_VERTS = [
    (0.7071067690849304, 0.7071067690849304, 0.0), (0.7071067690849304, -0.7071067690849304, 0.0),
    (-0.7071067690849304, 0.7071067690849304, 0.0), (-0.7071067690849304, -0.7071067690849304, 0.0),
    (0.8314696550369263, 0.5555702447891235, 0.0), (0.8314696550369263, -0.5555702447891235, 0.0),
    (-0.8314696550369263, 0.5555702447891235, 0.0), (-0.8314696550369263, -0.5555702447891235, 0.0),
    (0.9238795042037964, 0.3826834261417389, 0.0), (0.9238795042037964, -0.3826834261417389, 0.0),
    (-0.9238795042037964, 0.3826834261417389, 0.0), (-0.9238795042037964, -0.3826834261417389, 0.0),
    (0.9807852506637573, 0.19509035348892212, 0.0), (0.9807852506637573, -0.19509035348892212, 0.0),
    (-0.9807852506637573, 0.19509035348892212, 0.0), (-0.9807852506637573, -0.19509035348892212, 0.0),
    (0.19509197771549225, 0.9807849526405334, 0.0), (0.19509197771549225, -0.9807849526405334, 0.0),
    (-0.19509197771549225, 0.9807849526405334, 0.0), (-0.19509197771549225, -0.9807849526405334, 0.0),
    (0.3826850652694702, 0.9238788485527039, 0.0), (0.3826850652694702, -0.9238788485527039, 0.0),
    (-0.3826850652694702, 0.9238788485527039, 0.0), (-0.3826850652694702, -0.9238788485527039, 0.0),
    (0.5555717945098877, 0.8314685821533203, 0.0), (0.5555717945098877, -0.8314685821533203, 0.0),
    (-0.5555717945098877, 0.8314685821533203, 0.0), (-0.5555717945098877, -0.8314685821533203, 0.0),
    (0.19509197771549225, 1.2807848453521729, 0.0), (0.19509197771549225, -1.2807848453521729, 0.0),
    (-0.19509197771549225, 1.2807848453521729, 0.0), (-0.19509197771549225, -1.2807848453521729, 0.0),
    (1.280785322189331, 0.19509035348892212, 0.0), (1.280785322189331, -0.19509035348892212, 0.0),
    (-1.280785322189331, 0.19509035348892212, 0.0), (-1.280785322189331, -0.19509035348892212, 0.0),
    (0.3901839852333069, 1.2807848453521729, 0.0), (0.3901839852333069, -1.2807848453521729, 0.0),
    (-0.3901839852333069, 1.2807848453521729, 0.0), (-0.3901839852333069, -1.2807848453521729, 0.0),
    (1.280785322189331, 0.39018189907073975, 0.0), (1.280785322189331, -0.39018189907073975, 0.0),
    (-1.280785322189331, 0.39018189907073975, 0.0), (-1.280785322189331, -0.39018189907073975, 0.0),
    (0.0, 1.5807849168777466, 0.0), (0.0, -1.5807849168777466, 0.0),
    (1.5807852745056152, 0.0, 0.0), (-1.5807852745056152, 0.0, 0.0),
]

ROOT_EDGES = [
    (0, 24), (2, 26), (1, 25), (3, 27), (16, 20), (18, 22), (17, 21), (19, 23),
    (4, 0), (6, 2), (5, 1), (7, 3), (8, 4), (10, 6), (9, 5), (11, 7),
    (12, 8), (14, 10), (13, 9), (15, 11), (24, 20), (26, 22), (25, 21), (27, 23),
    (16, 28), (18, 30), (17, 29), (19, 31), (12, 32), (14, 34), (13, 33), (15, 35),
    (28, 36), (30, 38), (29, 37), (31, 39), (32, 40), (34, 42), (33, 41), (35, 43),
    (36, 44), (38, 44), (37, 45), (39, 45), (40, 46), (42, 47), (41, 46), (43, 47),
]


def _purge_object(name):
    ob = bpy.data.objects.get(name)
    if ob is None:
        return
    data = ob.data
    bpy.data.objects.remove(ob, do_unlink=True)
    if data is None or data.users:
        return
    if isinstance(data, bpy.types.Mesh):
        bpy.data.meshes.remove(data)
    elif isinstance(data, bpy.types.Armature):
        bpy.data.armatures.remove(data)


def _widget_collection(scene):
    coll = bpy.data.collections.get(WGT_COLL)
    if coll is None:
        coll = bpy.data.collections.new(WGT_COLL)
    if coll.name not in scene.collection.children:
        try:
            scene.collection.children.link(coll)
        except RuntimeError:
            pass
    coll.hide_viewport = True
    coll.hide_render = True
    return coll


def _mesh_object(name, verts, edges, faces, coll):
    _purge_object(name)
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, edges, faces)
    me.validate()
    me.update()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def _thicken(verts, edges, faces, depth):
    if not faces:
        return verts, edges, faces
    n = len(verts)
    out = [(v[0], v[1] - depth, v[2]) for v in verts]
    out += [(v[0], v[1] + depth, v[2]) for v in verts]
    tally = {}
    for f in faces:
        count = len(f)
        for k in range(count):
            a = f[k]
            b = f[(k + 1) % count]
            key = (a, b) if a < b else (b, a)
            tally[key] = tally.get(key, 0) + 1
    out_faces = [list(f) for f in faces]
    out_faces += [[i + n for i in reversed(f)] for f in faces]
    for f in faces:
        count = len(f)
        for k in range(count):
            a = f[k]
            b = f[(k + 1) % count]
            key = (a, b) if a < b else (b, a)
            if tally[key] == 1:
                out_faces.append([b, a, a + n, b + n])
    return out, [tuple(e) for e in edges], out_faces


def _bracket_frame(hw, hh, arm, th):
    verts = []
    faces = []
    for sx, sz in ((1.0, 1.0), (-1.0, 1.0), (-1.0, -1.0), (1.0, -1.0)):
        ox = hw * sx
        oz = hh * sz
        pts = (
            (ox, oz),
            (ox - arm * sx, oz),
            (ox - arm * sx, oz - th * sz),
            (ox - th * sx, oz - th * sz),
            (ox - th * sx, oz - arm * sz),
            (ox, oz - arm * sz),
        )
        base = len(verts)
        for px, pz in pts:
            verts.append((px, 0.0, pz))
        idx = [base + k for k in range(6)]
        if sx * sz < 0.0:
            idx.reverse()
        faces.append(idx)
    return verts, [], faces


def _ring(radius, th, seg):
    verts = []
    for r in (radius + th, radius):
        for k in range(seg):
            a = 2.0 * math.pi * k / seg
            verts.append((r * math.cos(a), 0.0, r * math.sin(a)))
    faces = []
    for k in range(seg):
        n = (k + 1) % seg
        faces.append([k, n, seg + n, seg + k])
    return verts, [], faces


def _rect_ring(hw, hh, th):
    outer = ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))
    inner = (
        (-hw + th, -hh + th),
        (hw - th, -hh + th),
        (hw - th, hh - th),
        (-hw + th, hh - th),
    )
    verts = [(p[0], 0.0, p[1]) for p in outer] + [(p[0], 0.0, p[1]) for p in inner]
    faces = []
    for k in range(4):
        n = (k + 1) % 4
        faces.append([k, n, 4 + n, 4 + k])
    return verts, [], faces


def _rigify_root(scale):
    verts = [(v[0] * scale, v[1] * scale, v[2] * scale) for v in ROOT_VERTS]
    return verts, [tuple(e) for e in ROOT_EDGES], []


def _set_bone_color(pb, palette, rgb=None):
    if not hasattr(pb, "color"):
        return
    if rgb is None:
        pb.color.palette = palette
        return
    pb.color.palette = 'CUSTOM'
    pb.color.custom.normal = rgb
    pb.color.custom.select = tuple(min(c + 0.18, 1.0) for c in rgb)
    pb.color.custom.active = (1.0, 1.0, 1.0)


def _find_camera(context):
    scene = context.scene
    if scene.camera is not None and scene.camera.type == 'CAMERA':
        return scene.camera
    for ob in scene.objects:
        if ob.type == 'CAMERA':
            scene.camera = ob
            return ob
    cd = bpy.data.cameras.new("Camera")
    ob = bpy.data.objects.new("Camera", cd)
    scene.collection.objects.link(ob)
    ob.location = (0.0, -8.5, 2.4)
    ob.rotation_euler = (math.radians(78.0), 0.0, 0.0)
    scene.camera = ob
    return ob


def _frame_extents(cam, scene, dist):
    cd = cam.data
    lens = max(cd.lens, 1.0)
    rx = max(scene.render.resolution_x * scene.render.pixel_aspect_x, 1.0)
    ry = max(scene.render.resolution_y * scene.render.pixel_aspect_y, 1.0)
    if cd.sensor_fit == 'VERTICAL':
        hh = dist * (cd.sensor_height * 0.5) / lens
        hw = hh * (rx / ry)
    elif cd.sensor_fit == 'AUTO' and ry > rx:
        hh = dist * (cd.sensor_width * 0.5) / lens
        hw = hh * (rx / ry)
    else:
        hw = dist * (cd.sensor_width * 0.5) / lens
        hh = hw * (ry / rx)
    return max(hw * 0.55, 0.05), max(hh * 0.55, 0.05)


def _split_index(path):
    if path.endswith("]"):
        head, _, tail = path.rpartition("[")
        inner = tail[:-1]
        if inner.isdigit():
            return head, int(inner)
    return path, -1


def _clear_drivers(id_data, path, index=-1):
    ad = getattr(id_data, "animation_data", None)
    if ad is None:
        return
    for fc in list(ad.drivers):
        if fc.data_path == path and (index < 0 or fc.array_index == index):
            ad.drivers.remove(fc)


def _purge_constraint_drivers(ob):
    ad = getattr(ob, "animation_data", None)
    if ad is None:
        return
    for fc in list(ad.drivers):
        if fc.data_path.startswith("constraints["):
            ad.drivers.remove(fc)


def _make_driver(id_data, path, entries=(), dist_entries=(), coeffs=(0.0, 1.0)):
    path, index = _split_index(path)
    _clear_drivers(id_data, path, index)
    fc = id_data.driver_add(path, index) if index >= 0 else id_data.driver_add(path)
    drv = fc.driver
    drv.type = 'AVERAGE'
    for v in list(drv.variables):
        drv.variables.remove(v)
    for name, target, dpath in entries:
        var = drv.variables.new()
        var.name = name
        var.type = 'SINGLE_PROP'
        tgt = var.targets[0]
        tgt.id_type = 'OBJECT'
        tgt.id = target
        tgt.data_path = dpath
    for name, target, bone_a, bone_b in dist_entries:
        var = drv.variables.new()
        var.name = name
        var.type = 'LOC_DIFF'
        t0 = var.targets[0]
        t0.id = target
        t0.bone_target = bone_a
        t0.transform_space = 'WORLD_SPACE'
        t1 = var.targets[1]
        t1.id = target
        t1.bone_target = bone_b
        t1.transform_space = 'WORLD_SPACE'
    for m in list(fc.modifiers):
        fc.modifiers.remove(m)
    gen = fc.modifiers.new('GENERATOR')
    gen.mode = 'POLYNOMIAL'
    gen.poly_order = 1
    gen.use_restricted_range = False
    gen.coefficients[0] = coeffs[0]
    gen.coefficients[1] = coeffs[1]
    while len(fc.keyframe_points):
        fc.keyframe_points.remove(fc.keyframe_points[0], fast=True)
    return fc


def _rest_bone_matrix(rig, bone_name):
    bone = rig.data.bones[bone_name]
    return rig.matrix_world @ bone.matrix_local @ Matrix.Translation((0.0, bone.length, 0.0))


def _face_constraint(pb, rig, name):
    con = pb.constraints.new('DAMPED_TRACK')
    con.name = name
    con.target = rig
    con.subtarget = "CAM"
    con.head_tail = 0.0
    con.track_axis = 'TRACK_NEGATIVE_Y'
    return con


def _distance_scale(rig, bone_name, base):
    for axis in range(3):
        _make_driver(
            rig,
            'pose.bones["%s"].custom_shape_scale_xyz[%d]' % (bone_name, axis),
            dist_entries=(("d", rig, bone_name, "CAM"),),
            coeffs=(0.0, 1.0 / base),
        )


def build():
    context = bpy.context
    scene = context.scene

    if context.object is not None and context.object.mode != 'OBJECT':
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except RuntimeError:
            pass

    cam = _find_camera(context)
    cd = cam.data

    _purge_object(RIG_NAME)
    if cam.parent is not None and cam.parent.name == RIG_NAME:
        cam.parent = None

    coll = _widget_collection(scene)

    mw = cam.matrix_world.copy()
    loc = mw.translation.copy()
    basis = mw.to_3x3()
    fwd = (basis @ Vector((0.0, 0.0, -1.0))).normalized()
    up = (basis @ Vector((0.0, 1.0, 0.0))).normalized()
    aim_point = loc + fwd * AIM_DIST

    hw, hh = _frame_extents(cam, scene, AIM_DIST)
    span = min(hw, hh)
    seg = AIM_DIST * 0.14
    depth = span * 0.055

    wgt_frame = _mesh_object(
        "WGT_CamFrame",
        *_thicken(*_bracket_frame(hw, hh, span * 0.38, span * 0.10), depth),
        coll)
    wgt_focus = _mesh_object(
        "WGT_CamFocus",
        *_thicken(*_ring(span * 0.26, span * 0.055, 32), depth),
        coll)
    wgt_body = _mesh_object(
        "WGT_CamBody",
        *_thicken(*_rect_ring(span * 0.22, span * 0.16, span * 0.035), depth * 0.8),
        coll)
    wgt_root = _mesh_object("WGT_CamRoot", *_rigify_root(max(AIM_DIST * 0.22, 0.4)), coll)

    arm_data = bpy.data.armatures.new(RIG_NAME)
    rig = bpy.data.objects.new(RIG_NAME, arm_data)
    scene.collection.objects.link(rig)
    rig.matrix_world = Matrix.Identity(4)
    rig.show_in_front = True

    context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')

    ebs = arm_data.edit_bones
    ground = Vector((loc.x, loc.y, 0.0))

    root = ebs.new("ROOT")
    root.head = ground
    root.tail = ground + Vector((0.0, max(AIM_DIST * 0.2, 0.4), 0.0))
    root.align_roll(Vector((0.0, 0.0, 1.0)))

    body = ebs.new("CAM")
    body.head = loc
    body.tail = loc + fwd * seg
    body.align_roll(up)
    body.parent = root
    body.use_connect = False

    aim = ebs.new("AIM")
    aim.head = aim_point
    aim.tail = aim_point + fwd * seg
    aim.align_roll(up)
    aim.parent = root
    aim.use_connect = False

    focus = ebs.new("FOCUS")
    focus.head = aim_point
    focus.tail = aim_point + fwd * (seg * 0.8)
    focus.align_roll(up)
    focus.parent = aim
    focus.use_connect = False
    focus.inherit_scale = 'FULL'

    mch_track = ebs.new("MCH_TRACK")
    mch_track.head = loc
    mch_track.tail = loc + fwd * seg
    mch_track.align_roll(up)
    mch_track.parent = body
    mch_track.use_connect = False
    mch_track.inherit_scale = 'NONE'

    mch_roll = ebs.new("MCH_ROLL")
    mch_roll.head = loc
    mch_roll.tail = loc + fwd * seg
    mch_roll.align_roll(up)
    mch_roll.parent = mch_track
    mch_roll.use_connect = False
    mch_roll.inherit_scale = 'NONE'

    bpy.ops.object.mode_set(mode='OBJECT')

    shapes = (
        ("ROOT", wgt_root, 'THEME03', None),
        ("CAM", wgt_body, 'THEME09', None),
        ("AIM", wgt_frame, 'CUSTOM', YELLOW),
        ("FOCUS", wgt_focus, 'CUSTOM', YELLOW),
    )
    for bone_name, shape, palette, rgb in shapes:
        pb = rig.pose.bones[bone_name]
        pb.custom_shape = shape
        pb.use_custom_shape_bone_size = False
        _set_bone_color(pb, palette, rgb)

    for bone_name in MCH_BONES:
        arm_data.bones[bone_name].hide = True
        pb = rig.pose.bones[bone_name]
        pb.rotation_mode = 'XYZ'
        pb.lock_location = (True, True, True)
        pb.lock_scale = (True, True, True)

    for bone_name in ("ROOT", "CAM", "AIM", "FOCUS"):
        rig.pose.bones[bone_name].rotation_mode = 'XYZ'

    pb_focus = rig.pose.bones["FOCUS"]
    pb_focus.lock_rotation = (True, True, True)
    pb_focus.lock_scale = (True, True, True)

    pb_aim = rig.pose.bones["AIM"]
    pb_aim.lock_rotation = (True, False, True)

    _face_constraint(pb_aim, rig, CON_FACE)
    _face_constraint(pb_focus, rig, CON_FACE)

    pb_track = rig.pose.bones["MCH_TRACK"]
    con_aim = pb_track.constraints.new('DAMPED_TRACK')
    con_aim.name = CON_AIM
    con_aim.target = rig
    con_aim.subtarget = "AIM"
    con_aim.track_axis = 'TRACK_Y'

    _purge_constraint_drivers(cam)
    for c in list(cam.constraints):
        if c.type in ('TRACK_TO', 'DAMPED_TRACK', 'LOCKED_TRACK', 'COPY_LOCATION',
                      'COPY_ROTATION', 'TRANSFORM', 'LIMIT_DISTANCE'):
            cam.constraints.remove(c)

    parent_rest = _rest_bone_matrix(rig, "MCH_ROLL")
    cam.parent = rig
    cam.parent_type = 'BONE'
    cam.parent_bone = "MCH_ROLL"
    cam.matrix_parent_inverse = parent_rest.inverted()
    cam.rotation_mode = 'XYZ'
    cam.location = loc
    cam.rotation_euler = mw.to_euler('XYZ')
    cam.scale = (1.0, 1.0, 1.0)

    con_snap = cam.constraints.new('DAMPED_TRACK')
    con_snap.name = CON_SNAP
    con_snap.target = rig
    con_snap.subtarget = "AIM"
    con_snap.track_axis = 'TRACK_NEGATIVE_Z'

    cam[P_TRACK] = True
    cam[P_DOF] = True
    for key, desc in ((P_TRACK, "Aim the camera at the frame control"),
                      (P_DOF, "Depth of field focused on the focus control")):
        try:
            cam.id_properties_ui(key).update(description=desc)
        except (TypeError, AttributeError):
            pass

    base_lens = max(cd.lens, 1.0)
    cd.dof.use_dof = True
    cd.dof.focus_object = rig
    cd.dof.focus_subtarget = "FOCUS"

    _make_driver(
        cd,
        "lens",
        entries=(
            ("sx", rig, 'pose.bones["AIM"].scale[0]'),
            ("sz", rig, 'pose.bones["AIM"].scale[2]'),
        ),
        coeffs=(0.0, base_lens),
    )
    _make_driver(cd, "dof.use_dof", entries=(("dof", cam, '["%s"]' % P_DOF),))
    _make_driver(
        rig,
        'pose.bones["MCH_TRACK"].constraints["%s"].influence' % CON_AIM,
        entries=(("trk", cam, '["%s"]' % P_TRACK),),
    )
    _make_driver(
        cam,
        'constraints["%s"].influence' % CON_SNAP,
        entries=(("trk", cam, '["%s"]' % P_TRACK),),
    )
    _make_driver(
        rig,
        'pose.bones["MCH_ROLL"].rotation_euler[1]',
        entries=(("rl", rig, 'pose.bones["AIM"].rotation_euler[1]'),),
    )
    _distance_scale(rig, "AIM", AIM_DIST)
    _distance_scale(rig, "FOCUS", AIM_DIST)

    context.view_layer.update()

    for ob in context.selected_objects:
        ob.select_set(False)
    rig.select_set(True)
    context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='POSE')
    for b in arm_data.bones:
        b.select = b.name == "AIM"
    arm_data.bones.active = arm_data.bones["AIM"]

    return rig, cam


build()