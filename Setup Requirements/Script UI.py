import bpy
import os

SCRIPT_1_TEXT_NAME = "#1 Setup shader, rig, and outline"
SCRIPT_2_TEXT_NAME = "Jideeh's Setup"
SCRIPT_3_TEXT_NAME = "Facerig"
SCRIPT_4_TEXT_NAME = "Thugs Rig Script"
SCRIPT_5_TEXT_NAME = "Face Panel Controllers"
SCRIPT_6_TEXT_NAME = "Bangboo Rig"
SCRIPT_7_TEXT_NAME = "Purge Empties"
SCRIPT_8_TEXT_NAME = "Shaders & Outlines"
SCRIPT_9_TEXT_NAME = "Shaders & Outlines No Face"

BETTER_FBX_OPERATOR_IDS = [
    "better_import.fbx",
    "better_fbx.import_fbx",
    "import_scene.better_fbx",
    "import_scene.betterfbx",
    "betterfbx.import_scene",
    "betterfbx.import_fbx",
]

FACE_MESH_SUFFIX = "_Face"
FACE_MATERIAL_NAME = "ZZZ Shader Face"

FACE_FX_COLLECTION_NAME = "Face FX"
FACE_FX_COLOR_TAG = "COLOR_05"
FACE_FX_WIDGET_NAME = "Face FX Widget"
FACERIG_BONE_COLLECTION = "Facerig"
ZZZ_FACE_MATERIAL_NAME = "ZZZ Shader Face"
FACE_EFFECT_MATERIAL_NAME = "Face Effect"
FACE_LIGHTMAP_GROUP_NAME = "Face Lightmap"
BURAT_GROUP_LABEL = "Burat"
ARMATURE_COLLECTION_NAME = "Armature"
FACE_EXPRESSIONS_BONE = "Face Expressions"
DEF_SPINE_VERTEX_GROUP = "DEF-spine.006"
WGTS_COLLECTION_NAME = "WGTS"

OLD_FACE_FX_PROPERTIES = ["Aozameru", "Blush", "Switch FX"]

LIGHTMAP_GROUPS = [
    (
        "Female",
        [
            ("1", "Female_Face_Lightmap.png"),
            ("2", "Female_Face_Lightmap_02.png"),
            ("FX", "Female_Face_lightmap_FX.png"),
        ],
    ),
    (
        "Male",
        [
            ("1", "Male_Face_01_Lightmap.png"),
            ("2", "Male_Face_02_Lightmap.png"),
        ],
    ),
    (
        "Monster",
        [
            ("1", "Monster_Face_01_Lightmap.png"),
        ],
    ),
    (
        "NPC Face",
        [
            ("Child", "NPC_Face_Child_Lightmap.png"),
            ("Older", "NPC_Face_Older_Lightmap.png"),
        ],
    ),
    (
        "NPC Furry",
        [
            ("1", "NPC_Furry_Face01_Lightmap.png"),
            ("2", "NPC_Furry_Face02_Lightmap.png"),
            ("3", "NPC_Furry_Face03_Lightmap.png"),
        ],
    ),
]

def disable_auto_keying():
    bpy.context.scene.tool_settings.use_keyframe_insert_auto = False

def strip_py_extension(name):
    lowered = name.lower()

    if lowered.endswith(".py"):
        return lowered[:-3]

    return lowered

def find_text_block(text_name):
    text_block = bpy.data.texts.get(text_name)

    if text_block is not None:
        return text_block

    target = strip_py_extension(text_name)

    for text in bpy.data.texts:
        if strip_py_extension(text.name) == target:
            return text

    return None

def run_text_block(text_name):
    text_block = find_text_block(text_name)

    if text_block is None:
        available_texts = [text.name for text in bpy.data.texts]
        raise RuntimeError(f'Could not find a text block named "{text_name}" (with or without a .py extension). Available text blocks: {available_texts}')

    namespace = {
        "__name__": "__main__",
        "__file__": text_block.name,
        "bpy": bpy,
    }

    exec(text_block.as_string(), namespace)

def operator_exists(operator_id):
    parts = operator_id.split(".")

    if len(parts) != 2:
        return False

    category_name, operator_name = parts
    category = getattr(bpy.ops, category_name, None)

    if category is None:
        return False

    operator = getattr(category, operator_name, None)

    return operator is not None

def call_operator(operator_id):
    category_name, operator_name = operator_id.split(".")
    category = getattr(bpy.ops, category_name)
    operator = getattr(category, operator_name)
    return operator("INVOKE_DEFAULT")

def run_better_fbx_importer():
    for operator_id in BETTER_FBX_OPERATOR_IDS:
        if operator_exists(operator_id):
            return call_operator(operator_id)

    raise RuntimeError(
        "Could not find the Better FBX Importer operator. "
        "Open Blender's Python console, run the Better FBX importer once, "
        "then check the operator name in the Info log and add it to BETTER_FBX_OPERATOR_IDS."
    )

def normalize_name(name):
    return name.lower().replace(" ", "").replace("_", "").replace(".", "").replace("-", "")

def clean_image_name(name):
    return os.path.basename(name).lower()

def find_image_by_name(image_name):
    target = clean_image_name(image_name)

    for image in bpy.data.images:
        if clean_image_name(image.name) == target:
            return image

    for image in bpy.data.images:
        if image.filepath and clean_image_name(image.filepath) == target:
            return image

    for image in bpy.data.images:
        if image.filepath and clean_image_name(bpy.path.abspath(image.filepath)) == target:
            return image

    return None

def find_face_mesh():
    obj = bpy.context.object

    if obj and obj.type == "MESH" and obj.name.endswith(FACE_MESH_SUFFIX):
        return obj

    for obj in bpy.context.selected_objects:
        if obj.type == "MESH" and obj.name.endswith(FACE_MESH_SUFFIX):
            return obj

    for obj in bpy.context.scene.objects:
        if obj.type == "MESH" and obj.name.endswith(FACE_MESH_SUFFIX):
            return obj

    for obj in bpy.data.objects:
        if obj.type == "MESH" and obj.name.endswith(FACE_MESH_SUFFIX):
            return obj

    return None

def get_face_material(face_obj):
    if len(face_obj.material_slots) < 1:
        raise RuntimeError(f'{face_obj.name} does not have material slot 1.')

    material = face_obj.material_slots[0].material

    if material is None:
        raise RuntimeError(f'Material slot 1 on {face_obj.name} is empty.')

    if normalize_name(material.name) != normalize_name(FACE_MATERIAL_NAME):
        raise RuntimeError(f'Material slot 1 is "{material.name}", not "{FACE_MATERIAL_NAME}".')

    if material.node_tree is None:
        raise RuntimeError(f'{material.name} does not use nodes.')

    return material

def node_matches_face_lightmap(node):
    names = [
        node.name,
        getattr(node, "label", ""),
    ]

    if node.type == "GROUP" and node.node_tree is not None:
        names.append(node.node_tree.name)

    for name in names:
        normalized = normalize_name(name)

        if "facelightmap" in normalized:
            return True

    return False

def image_node_matches_lightmap(node):
    names = [
        node.name,
        getattr(node, "label", ""),
    ]

    if node.image is not None:
        names.append(node.image.name)
        names.append(node.image.filepath)

    for name in names:
        normalized = normalize_name(name)

        if "face" in normalized and "lightmap" in normalized:
            return True

        if "facelightmap" in normalized:
            return True

    return False

def find_upstream_image_nodes(node, found, visited_nodes):
    if node in visited_nodes:
        return

    visited_nodes.add(node)

    if node.type == "TEX_IMAGE":
        found.append(node)
        return

    for input_socket in node.inputs:
        for link in input_socket.links:
            find_upstream_image_nodes(link.from_node, found, visited_nodes)

def find_image_nodes_connected_to_group_output(node_tree):
    found = []

    for node in node_tree.nodes:
        if node.type == "GROUP_OUTPUT":
            for input_socket in node.inputs:
                for link in input_socket.links:
                    find_upstream_image_nodes(link.from_node, found, set())

    return found

def collect_lightmap_image_nodes_from_tree(node_tree, found, visited_trees):
    if node_tree in visited_trees:
        return

    visited_trees.add(node_tree)

    for node in node_tree.nodes:
        if node.type == "TEX_IMAGE" and image_node_matches_lightmap(node):
            found.append(node)

        if node.type == "GROUP" and node.node_tree is not None:
            if node_matches_face_lightmap(node):
                output_image_nodes = find_image_nodes_connected_to_group_output(node.node_tree)

                if output_image_nodes:
                    for image_node in output_image_nodes:
                        if image_node not in found:
                            found.append(image_node)

                for inner_node in node.node_tree.nodes:
                    if inner_node.type == "TEX_IMAGE":
                        if inner_node not in found:
                            found.append(inner_node)

            collect_lightmap_image_nodes_from_tree(node.node_tree, found, visited_trees)

def find_face_lightmap_image_nodes(material):
    found = []
    collect_lightmap_image_nodes_from_tree(material.node_tree, found, set())

    unique_found = []

    for node in found:
        if node not in unique_found:
            unique_found.append(node)

    if unique_found:
        return unique_found

    all_image_nodes = []

    def collect_all_image_nodes(node_tree, visited_trees):
        if node_tree in visited_trees:
            return

        visited_trees.add(node_tree)

        for node in node_tree.nodes:
            if node.type == "TEX_IMAGE":
                all_image_nodes.append(node)

            if node.type == "GROUP" and node.node_tree is not None:
                collect_all_image_nodes(node.node_tree, visited_trees)

    collect_all_image_nodes(material.node_tree, set())

    image_node_names = []

    for node in all_image_nodes:
        current_image = node.image.name if node.image else "No image"
        image_node_names.append(f'{node.name} / {current_image}')

    raise RuntimeError(f'Could not find a face lightmap image texture node. Found image nodes: {image_node_names}')

def set_face_lightmap_image(image_name):
    image = find_image_by_name(image_name)

    if image is None:
        raise RuntimeError(f'Image "{image_name}" was not found in bpy.data.images. Make sure it is loaded in the blend file.')

    face_obj = find_face_mesh()

    if face_obj is None:
        raise RuntimeError(f'No mesh ending with "{FACE_MESH_SUFFIX}" was found.')

    material = get_face_material(face_obj)
    image_nodes = find_face_lightmap_image_nodes(material)

    for image_node in image_nodes:
        image_node.image = image

    node_names = [node.name for node in image_nodes]

    return face_obj.name, node_names, image.name

def lightmap_prop_name(group_name):
    return "jideeh_lightmap_" + normalize_name(group_name)

LIGHTMAP_SLIDERS = []
MONSTER_IMAGE = None
for _group_name, _items in LIGHTMAP_GROUPS:
    _images = [_image for _label, _image in _items]
    if _group_name == "Monster":
        MONSTER_IMAGE = _images[0]
        continue
    LIGHTMAP_SLIDERS.append((_group_name, lightmap_prop_name(_group_name), _images))

def make_lightmap_update(prop_name, images):
    def update(self, context):
        value = getattr(self, prop_name)

        if value < 1 or value > len(images):
            return

        try:
            set_face_lightmap_image(images[value - 1])
        except Exception as error:
            print("Face lightmap switch failed:", error)

    return update

def exclude_collection_from_view_layer(collection_name):
    def recurse(layer_collection):
        if layer_collection.collection.name == collection_name:
            layer_collection.exclude = True
            return True

        for child in layer_collection.children:
            if recurse(child):
                return True

        return False

    recurse(bpy.context.view_layer.layer_collection)

def transplant_face_effect(face_effect):
    if face_effect is None:
        print(f'Material "{FACE_EFFECT_MATERIAL_NAME}" was not appended; nothing to transplant.')
        return

    zzz = bpy.data.materials.get(ZZZ_FACE_MATERIAL_NAME)

    if zzz is not None and zzz is not face_effect:
        zzz.user_remap(face_effect)
        bpy.data.materials.remove(zzz)

    face_effect.name = ZZZ_FACE_MATERIAL_NAME

def append_face_fx_collection(filepath):
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        if FACE_FX_COLLECTION_NAME not in data_from.collections:
            raise RuntimeError(f'No collection named "{FACE_FX_COLLECTION_NAME}" was found in {filepath}.')

        data_to.collections = [FACE_FX_COLLECTION_NAME]

        if FACE_EFFECT_MATERIAL_NAME in data_from.materials:
            data_to.materials = [FACE_EFFECT_MATERIAL_NAME]

    linked = None

    for collection in data_to.collections:
        if collection is None:
            continue

        if collection.name not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(collection)

        collection.color_tag = FACE_FX_COLOR_TAG
        linked = collection

    if linked is None:
        raise RuntimeError(f'Failed to append "{FACE_FX_COLLECTION_NAME}" from {filepath}.')

    appended_material = None

    for material in data_to.materials:
        if material is not None:
            appended_material = material
            break

    transplant_face_effect(appended_material)

    exclude_collection_from_view_layer(WGTS_COLLECTION_NAME)
    insert_face_lightmap_node()
    fill_face_texture()

    return linked.name

def find_node_by_name(node_tree, name):
    target = normalize_name(name)

    for node in node_tree.nodes:
        if normalize_name(node.name) == target:
            return node

    for node in node_tree.nodes:
        if normalize_name(getattr(node, "label", "")) == target:
            return node

    for node in node_tree.nodes:
        if node.type == "GROUP" and node.node_tree is not None and normalize_name(node.node_tree.name) == target:
            return node

    return None

def find_input_socket(node, label):
    target = normalize_name(label)

    for socket in node.inputs:
        if normalize_name(socket.name) == target:
            return socket

    return None

def _set_driver_var(fcurve, face_obj, data_path):
    driver = fcurve.driver
    driver.type = "AVERAGE"

    for variable in list(driver.variables):
        driver.variables.remove(variable)

    variable = driver.variables.new()
    variable.name = "var"
    variable.type = "SINGLE_PROP"

    target = variable.targets[0]
    target.id_type = "OBJECT"
    target.id = face_obj
    target.data_path = data_path

def drive_socket_default(socket, face_obj, data_path, index=-1):
    if index < 0:
        socket.driver_remove("default_value")
        fcurve = socket.driver_add("default_value")
    else:
        socket.driver_remove("default_value", index)
        fcurve = socket.driver_add("default_value", index)

    _set_driver_var(fcurve, face_obj, data_path)

def setup_number_property(obj, name, default, minimum, maximum, description=""):
    obj[name] = default

    try:
        ui = obj.id_properties_ui(name)
        if description:
            ui.update(default=default, min=minimum, max=maximum, description=description)
        else:
            ui.update(default=default, min=minimum, max=maximum)
    except Exception as error:
        print(f'UI update failed for "{name}":', error)

    try:
        obj.property_overridable_library_set(f'["{name}"]', True)
    except Exception as error:
        print(f'Library override flag failed for "{name}":', error)

def setup_color_property(obj, name, default):
    obj[name] = list(default)

    try:
        ui = obj.id_properties_ui(name)
        ui.update(default=list(default), min=0.0, max=1.0, subtype="COLOR")
    except Exception as error:
        print(f'UI update failed for "{name}":', error)

def find_face_diffuse_image():
    for image in bpy.data.images:
        if clean_image_name(image.name).endswith("_face_d.png"):
            return image

    for image in bpy.data.images:
        if image.filepath and clean_image_name(image.filepath).endswith("_face_d.png"):
            return image

    return None

def fill_face_texture():
    material = bpy.data.materials.get(ZZZ_FACE_MATERIAL_NAME)

    if material is None or material.node_tree is None:
        return

    burat = find_node_by_name(material.node_tree, BURAT_GROUP_LABEL)

    if burat is None or getattr(burat, "node_tree", None) is None:
        print(f'Group node "{BURAT_GROUP_LABEL}" was not found in "{ZZZ_FACE_MATERIAL_NAME}".')
        return

    image = find_face_diffuse_image()

    if image is None:
        print('No image ending with "_Face_D.png" was found to fill the face texture.')
        return

    target = None

    for node in burat.node_tree.nodes:
        if node.type == "TEX_IMAGE" and (normalize_name(node.name) == "faced" or normalize_name(getattr(node, "label", "")) == "faced"):
            target = node
            break

    if target is None:
        for node in burat.node_tree.nodes:
            if node.type == "TEX_IMAGE" and node.image is None:
                target = node
                break

    if target is None:
        print(f'No Face_D image node was found inside "{BURAT_GROUP_LABEL}".')
        return

    target.image = image

def insert_face_lightmap_node():
    material = bpy.data.materials.get(ZZZ_FACE_MATERIAL_NAME)

    if material is None or material.node_tree is None:
        return

    node_tree = material.node_tree
    group = bpy.data.node_groups.get(FACE_LIGHTMAP_GROUP_NAME)

    if group is None:
        print(f'Node group "{FACE_LIGHTMAP_GROUP_NAME}" was not found.')
        return

    separate = None

    for node in node_tree.nodes:
        if node.type == "SEPARATE_COLOR" or normalize_name(node.name) == "separatecolor":
            separate = node
            break

    if separate is None:
        print(f'No Separate Color node was found in "{ZZZ_FACE_MATERIAL_NAME}".')
        return

    lightmap = None

    for node in node_tree.nodes:
        if node.type == "GROUP" and node.node_tree is group:
            lightmap = node
            break

    if lightmap is None:
        lightmap = node_tree.nodes.new("ShaderNodeGroup")
        lightmap.node_tree = group
        lightmap.label = FACE_LIGHTMAP_GROUP_NAME
        lightmap.location = (separate.location.x - 300, separate.location.y)

    out_socket = None

    for socket in lightmap.outputs:
        if normalize_name(socket.name) == "color":
            out_socket = socket
            break

    if out_socket is None and len(lightmap.outputs) > 0:
        out_socket = lightmap.outputs[0]

    in_socket = None

    for socket in separate.inputs:
        if normalize_name(socket.name) == "color":
            in_socket = socket
            break

    if in_socket is None and len(separate.inputs) > 0:
        in_socket = separate.inputs[0]

    if out_socket is None or in_socket is None:
        return

    for link in node_tree.links:
        if link.from_socket == out_socket and link.to_socket == in_socket:
            return

    node_tree.links.new(out_socket, in_socket)

def drive_aozameru_colorramp(aozameru_node, face_obj):
    warnings = []
    tree = getattr(aozameru_node, "node_tree", None)

    if tree is None:
        warnings.append("Aozameru group has no internal node tree")
        return warnings

    ramp = None

    for node in tree.nodes:
        if node.type == "VALTORGB":
            ramp = node
            break

    if ramp is None:
        warnings.append("no ColorRamp inside Aozameru")
        return warnings

    data_path = 'nodes["' + ramp.name + '"].color_ramp.elements[0].position'

    try:
        tree.driver_remove(data_path)
    except Exception:
        pass

    try:
        fcurve = tree.driver_add(data_path)
        _set_driver_var(fcurve, face_obj, '["Aozameru Top to Down"]')
    except Exception as error:
        warnings.append(f"Aozameru color stop driver failed: {error}")

    return warnings

def drive_blush_mix_color(blush_node, face_obj):
    warnings = []
    tree = getattr(blush_node, "node_tree", None)

    if tree is None:
        warnings.append("Blush group has no internal node tree")
        return warnings

    mix = None

    for node in tree.nodes:
        if normalize_name(node.name) == "mixcolor" or normalize_name(getattr(node, "label", "")) == "mixcolor":
            mix = node
            break

    if mix is None:
        for node in tree.nodes:
            if node.type in ("MIX", "MIX_RGB"):
                mix = node
                break

    if mix is None:
        warnings.append("no Mix Color inside Blush")
        return warnings

    b_socket = None

    for socket in mix.inputs:
        if normalize_name(socket.name) == "b" and socket.type == "RGBA":
            b_socket = socket
            break

    if b_socket is None:
        for socket in mix.inputs:
            if socket.type == "RGBA" and normalize_name(socket.name) in ("b", "color2"):
                b_socket = socket
                break

    if b_socket is None:
        warnings.append('no "B" color input on Mix Color inside Blush')
        return warnings

    for i in range(3):
        try:
            drive_socket_default(b_socket, face_obj, '["Blush Color"][' + str(i) + ']', index=i)
        except Exception as error:
            warnings.append(f"Blush Color driver [{i}] failed: {error}")

    return warnings

def assign_widget_to_facerig_collection():
    target = normalize_name(FACE_FX_WIDGET_NAME)
    widget = None

    for obj in bpy.data.objects:
        if obj.type == "ARMATURE" and normalize_name(obj.name) == target:
            widget = obj
            break

    if widget is None:
        print(f'Armature "{FACE_FX_WIDGET_NAME}" was not found.')
        return

    armature = widget.data
    bone_collection = armature.collections.get(FACERIG_BONE_COLLECTION)

    if bone_collection is None:
        bone_collection = armature.collections.new(FACERIG_BONE_COLLECTION)

    for bone in armature.bones:
        bone_collection.assign(bone)

def find_bone_owner(bone_name):
    for obj in bpy.data.objects:
        if obj.type == "ARMATURE" and bone_name in obj.pose.bones:
            return obj

    return None

def find_rig_in_armature_collection():
    for obj in bpy.data.objects:
        if obj.type == "ARMATURE" and obj.name.endswith("Rig"):
            return obj

    return None

def find_face_fx_mesh():
    target = normalize_name(FACE_FX_COLLECTION_NAME)

    for obj in bpy.data.objects:
        if obj.type == "MESH" and normalize_name(obj.name) == target:
            return obj

    return None

def parent_face_mesh():
    face_fx_obj = find_face_fx_mesh()

    if face_fx_obj is None:
        raise RuntimeError(f'Mesh "{FACE_FX_COLLECTION_NAME}" was not found.')

    rig = find_rig_in_armature_collection()

    if rig is None:
        raise RuntimeError('No armature ending with "Rig" was found in the blend file.')

    if face_fx_obj.data.shape_keys is not None:
        for key_block in face_fx_obj.data.shape_keys.key_blocks:
            key_block.value = 0.0

    if bpy.context.object is not None and bpy.context.object.mode != "OBJECT":
        try:
            bpy.ops.object.mode_set(mode="OBJECT")
        except Exception:
            pass

    bpy.ops.object.select_all(action="DESELECT")
    face_fx_obj.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.parent_set(type="ARMATURE")

    group = face_fx_obj.vertex_groups.get(DEF_SPINE_VERTEX_GROUP)

    if group is None:
        group = face_fx_obj.vertex_groups.new(name=DEF_SPINE_VERTEX_GROUP)

    group.add([vertex.index for vertex in face_fx_obj.data.vertices], 1.0, "REPLACE")

    result_name = face_fx_obj.name
    face_obj = find_face_mesh()

    if face_obj is not None and face_obj is not face_fx_obj:
        bpy.ops.object.select_all(action="DESELECT")
        try:
            face_fx_obj.select_set(True)
            face_obj.select_set(True)
            bpy.context.view_layer.objects.active = face_obj
            bpy.ops.object.join()
            result_name = face_obj.name
        except Exception as error:
            print("Face FX join failed:", error)
    else:
        print(f'No mesh ending with "{FACE_MESH_SUFFIX}" was found to join into.')

    owner = find_bone_owner(FACE_EXPRESSIONS_BONE)

    if owner is not None:
        bone = owner.data.bones.get(FACE_EXPRESSIONS_BONE)
        if bone is not None:
            bone.hide = True

    return result_name

def refresh_face_fx():
    material = bpy.data.materials.get(ZZZ_FACE_MATERIAL_NAME)

    if material is not None and material.node_tree is not None:
        material.node_tree.update_tag()
        material.update_tag()

    scene = bpy.context.scene

    if scene is not None:
        scene.frame_set(scene.frame_current)

def wire_face_fx_drivers(face_obj):
    material = bpy.data.materials.get(ZZZ_FACE_MATERIAL_NAME)
    warnings = []

    if material is None or material.node_tree is None:
        warnings.append(f'material "{ZZZ_FACE_MATERIAL_NAME}" not found, drivers skipped')
        return warnings

    node_tree = material.node_tree

    aozameru = find_node_by_name(node_tree, "Aozameru")

    if aozameru is None:
        warnings.append('"Aozameru" group node not found')
    else:
        socket = find_input_socket(aozameru, "Type")

        if socket is None:
            warnings.append('"Type" input not found on Aozameru')
        else:
            drive_socket_default(socket, face_obj, '["Aozameru"]')

        warnings.extend(drive_aozameru_colorramp(aozameru, face_obj))

    blush = find_node_by_name(node_tree, "Blush")

    if blush is None:
        warnings.append('"Blush" group node not found')
    else:
        warnings.extend(drive_blush_mix_color(blush, face_obj))

        socket = find_input_socket(blush, "Cycle")

        if socket is None:
            warnings.append('"Cycle" input not found on Blush')
        else:
            drive_socket_default(socket, face_obj, '["Blush Type"]')

    og_aozameru = find_node_by_name(node_tree, "Original Aozameru")

    if og_aozameru is None:
        warnings.append('"Original Aozameru" group node not found')
    else:
        socket = find_input_socket(og_aozameru, "Intensity")

        if socket is None:
            warnings.append('"Intensity" input not found on Original Aozameru')
        else:
            drive_socket_default(socket, face_obj, '["OG Aozameru Intensity"]')

    og_blush = find_node_by_name(node_tree, "Original Blush")

    if og_blush is None:
        warnings.append('"Original Blush" group node not found')
    else:
        socket = find_input_socket(og_blush, "Value")

        if socket is None:
            warnings.append('"Value" input not found on Original Blush')
        else:
            drive_socket_default(socket, face_obj, '["OG Blush Intensity"]')

    switch_node = None
    named_switch = find_node_by_name(node_tree, "Switch FX")

    if named_switch is not None and named_switch.type == "VALUE":
        switch_node = named_switch
    else:
        for node in node_tree.nodes:
            if node.type == "VALUE":
                switch_node = node
                break

    if switch_node is None:
        warnings.append("no Value node found for Switch FX")
    else:
        drive_socket_default(switch_node.outputs[0], face_obj, '["Switch FX"]')

    return warnings

def create_face_fx_properties(face_obj):
    for name in OLD_FACE_FX_PROPERTIES:
        if name in face_obj.keys():
            del face_obj[name]

    setup_number_property(face_obj, "Aozameru", 1, 1, 3)
    setup_number_property(face_obj, "Aozameru Top to Down", 0.96, 0.0, 1.0)
    setup_color_property(face_obj, "Blush Color", (1.0, 1.0, 1.0))
    setup_number_property(face_obj, "Blush Type", 1, 1, 6)
    setup_number_property(face_obj, "OG Aozameru Intensity", 0.0, 0.0, 20.0)
    setup_number_property(face_obj, "OG Blush Intensity", 0.0, 0.0, 1.5)
    setup_number_property(face_obj, "Switch FX", 1, 1, 4, "1 = Aozameru, 2 = Blush, 3 = Original Aozameru, 4 = Original Blush")

def apply_face_fx_drivers():
    face_obj = find_face_mesh()

    if face_obj is None:
        raise RuntimeError(f'No mesh ending with "{FACE_MESH_SUFFIX}" was found.')

    create_face_fx_properties(face_obj)

    warnings = wire_face_fx_drivers(face_obj)

    assign_widget_to_facerig_collection()

    fill_face_texture()

    refresh_face_fx()

    return face_obj.name, warnings

def rebuild_face_fx_drivers():
    face_obj = find_face_mesh()

    if face_obj is None:
        raise RuntimeError(f'No mesh ending with "{FACE_MESH_SUFFIX}" was found.')

    warnings = wire_face_fx_drivers(face_obj)

    refresh_face_fx()

    return face_obj.name, warnings


def draw_subpanel(layout, data, prop_name, label, icon):
    box = layout.box()
    row = box.row()
    row.alignment = "LEFT"
    row.prop(
        data,
        prop_name,
        icon="TRIA_DOWN" if getattr(data, prop_name) else "TRIA_RIGHT",
        icon_only=True,
        emboss=False,
    )
    row.label(text=label, icon=icon)

    return box, getattr(data, prop_name)

def indented_row(layout, align=False):
    split = layout.split(factor=0.05)
    split.label(text="")
    return split.row(align=align)

class JIDEEH_OT_append_face_fx(bpy.types.Operator):
    bl_idname = "jideeh.append_face_fx"
    bl_label = "Get Face FX Mesh"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH", default="")
    filter_glob: bpy.props.StringProperty(default="*.blend", options={"HIDDEN"})

    def invoke(self, context, event):
        scene = context.scene

        if scene.jideeh_face_fx_cache_enabled and scene.jideeh_face_fx_cache_path:
            self.filepath = scene.jideeh_face_fx_cache_path
            return self.execute(context)

        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        try:
            context.scene.jideeh_face_fx_cache_path = self.filepath
            collection_name = append_face_fx_collection(self.filepath)
            self.report({"INFO"}, f'Appended "{collection_name}" and transplanted the Face Effect setup into "{ZZZ_FACE_MATERIAL_NAME}".')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_refresh_face_fx(bpy.types.Operator):
    bl_idname = "jideeh.refresh_face_fx"
    bl_label = "Refresh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            refresh_face_fx()
            self.report({"INFO"}, "Face FX drivers refreshed.")
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_rebuild_face_fx(bpy.types.Operator):
    bl_idname = "jideeh.rebuild_face_fx"
    bl_label = "Rebuild"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            face_obj_name, warnings = rebuild_face_fx_drivers()

            if warnings:
                self.report({"WARNING"}, f'Drivers re-set for "{face_obj_name}", but some were skipped: ' + "; ".join(warnings))
            else:
                self.report({"INFO"}, f'Drivers re-set for "{face_obj_name}".')

            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_parent_face_mesh(bpy.types.Operator):
    bl_idname = "jideeh.parent_face_mesh"
    bl_label = "Parent Face Mesh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            owner_name = parent_face_mesh()
            self.report({"INFO"}, f'Child Of constraint set on "{FACE_EXPRESSIONS_BONE}" ({owner_name}).')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_clear_face_fx_cache(bpy.types.Operator):
    bl_idname = "jideeh.clear_face_fx_cache"
    bl_label = "Clear"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.scene.jideeh_face_fx_cache_path = ""
        self.report({"INFO"}, "Face FX cache cleared.")
        return {"FINISHED"}

class JIDEEH_OT_apply_face_fx_drivers(bpy.types.Operator):
    bl_idname = "jideeh.apply_face_fx_drivers"
    bl_label = "Apply Drivers"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            face_obj_name, warnings = apply_face_fx_drivers()

            if warnings:
                self.report({"WARNING"}, f'Custom properties added to "{face_obj_name}", but some drivers were skipped: ' + "; ".join(warnings))
            else:
                self.report({"INFO"}, f'Custom properties and drivers applied for "{face_obj_name}".')

            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_set_face_lightmap(bpy.types.Operator):
    bl_idname = "jideeh.set_face_lightmap"
    bl_label = "Set Face Lightmap"
    bl_options = {"REGISTER", "UNDO"}

    image_name: bpy.props.StringProperty(default="")

    def execute(self, context):
        try:
            face_obj_name, node_names, image_name = set_face_lightmap_image(self.image_name)
            self.report({"INFO"}, f'Set {face_obj_name} face lightmap to {image_name}.')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_run_better_fbx_importer(bpy.types.Operator):
    bl_idname = "jideeh.run_better_fbx_importer"
    bl_label = "Better FBX Importer"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            disable_auto_keying()
            result = run_better_fbx_importer()
            self.report({"INFO"}, "Better FBX Importer opened.")
            return result
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_run_setup_shader_rig_outline(bpy.types.Operator):
    bl_idname = "jideeh.run_setup_shader_rig_outline"
    bl_label = "Rig, Outline, Shaders"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            disable_auto_keying()
            run_text_block(SCRIPT_1_TEXT_NAME)
            disable_auto_keying()
            self.report({"INFO"}, f'Ran "{SCRIPT_1_TEXT_NAME}".')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_run_jideeh_setup(bpy.types.Operator):
    bl_idname = "jideeh.run_jideeh_setup"
    bl_label = "Jideeh's Setup"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            disable_auto_keying()
            run_text_block(SCRIPT_2_TEXT_NAME)
            disable_auto_keying()
            self.report({"INFO"}, f'Ran "{SCRIPT_2_TEXT_NAME}".')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_run_facerig(bpy.types.Operator):
    bl_idname = "jideeh.run_facerig"
    bl_label = "Facerig"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            disable_auto_keying()
            run_text_block(SCRIPT_3_TEXT_NAME)
            disable_auto_keying()
            self.report({"INFO"}, f'Ran "{SCRIPT_3_TEXT_NAME}".')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_run_face_panel_controllers(bpy.types.Operator):
    bl_idname = "jideeh.run_face_panel_controllers"
    bl_label = "Face Panel Controllers"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            disable_auto_keying()
            run_text_block(SCRIPT_5_TEXT_NAME)
            disable_auto_keying()
            self.report({"INFO"}, f'Ran "{SCRIPT_5_TEXT_NAME}".')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_run_thugs_rig_script(bpy.types.Operator):
    bl_idname = "jideeh.run_thugs_rig_script"
    bl_label = "Thugs Rig"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            disable_auto_keying()
            run_text_block(SCRIPT_4_TEXT_NAME)
            disable_auto_keying()
            self.report({"INFO"}, f'Ran "{SCRIPT_4_TEXT_NAME}".')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_run_bangboo_rig(bpy.types.Operator):
    bl_idname = "jideeh.run_bangboo_rig"
    bl_label = "Bangboo Rig"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            disable_auto_keying()
            run_text_block(SCRIPT_6_TEXT_NAME)
            disable_auto_keying()
            self.report({"INFO"}, f'Ran "{SCRIPT_6_TEXT_NAME}".')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_run_remove_empties(bpy.types.Operator):
    bl_idname = "jideeh.run_remove_empties"
    bl_label = "Remove Empties"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            disable_auto_keying()
            run_text_block(SCRIPT_7_TEXT_NAME)
            disable_auto_keying()
            self.report({"INFO"}, f'Ran "{SCRIPT_7_TEXT_NAME}".')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_run_shaders_outlines(bpy.types.Operator):
    bl_idname = "jideeh.run_shaders_outlines"
    bl_label = "Shaders & Outlines"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            disable_auto_keying()
            run_text_block(SCRIPT_8_TEXT_NAME)
            disable_auto_keying()
            self.report({"INFO"}, f'Ran "{SCRIPT_8_TEXT_NAME}".')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_OT_run_shaders_outlines_no_face(bpy.types.Operator):
    bl_idname = "jideeh.run_shaders_outlines_no_face"
    bl_label = "Shaders & Outlines No Face"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            disable_auto_keying()
            run_text_block(SCRIPT_9_TEXT_NAME)
            disable_auto_keying()
            self.report({"INFO"}, f'Ran "{SCRIPT_9_TEXT_NAME}".')
            return {"FINISHED"}
        except Exception as error:
            self.report({"ERROR"}, str(error))
            raise

class JIDEEH_PT_script_runner_panel(bpy.types.Panel):
    bl_label = "Jideeh Script Runner"
    bl_idname = "JIDEEH_PT_script_runner_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.scale_y = 2
        row.operator("jideeh.run_better_fbx_importer", text="BetterFBX")

        row = layout.row()
        row.scale_y = 1.5
        row.operator("jideeh.run_setup_shader_rig_outline", text="Rig, Outline, Shaders")

        row = layout.row()
        row.scale_y = 1.5
        row.operator("jideeh.run_jideeh_setup", text="Jideeh's Setup")

        menus = layout.box()

        box, expanded = draw_subpanel(menus, scene, "jideeh_show_extra_utilities", "Extra Utilities", "TOOL_SETTINGS")
        if expanded:
            indented_row(box).label(text="Rigs")
            row = box.row(align=True)
            row.operator("jideeh.run_bangboo_rig", text="Bangboo")
            row.operator("jideeh.run_thugs_rig_script", text="Thugs")
            row.operator("jideeh.run_facerig", text="Facerig")

            indented_row(box).label(text="Shaders & Outlines")
            row = box.row(align=True)
            row.operator("jideeh.run_shaders_outlines", text="With Face")
            row.operator("jideeh.run_shaders_outlines_no_face", text="No Face")

            indented_row(box).label(text="Fixes")
            row = box.row(align=True)
            row.operator("jideeh.run_face_panel_controllers", text="Face Panel")
            row.operator("jideeh.run_remove_empties", text="Remove Empties")

        box, expanded = draw_subpanel(menus, scene, "jideeh_show_lightmap", "Face Lightmap toggle", "TEXTURE")
        if expanded:
            for group_name, prop_name, images in LIGHTMAP_SLIDERS:
                box.prop(scene, prop_name, text=group_name, slider=True)

            row = box.row()
            row.scale_y = 1.5
            row.operator("jideeh.set_face_lightmap", text="Monster").image_name = MONSTER_IMAGE

        box, expanded = draw_subpanel(menus, scene, "jideeh_show_face_fx", "Face FX", "SHADERFX")
        if expanded:
            col = box.column(align=True)
            row = col.row()
            row.scale_y = 2
            row.operator("jideeh.append_face_fx", text="Get Face FX Mesh")
            row = col.row()
            row.scale_y = 1.25
            row.operator("jideeh.apply_face_fx_drivers", text="Apply Drivers")
            row = col.row(align=True)
            row.scale_y = 1
            row.operator("jideeh.refresh_face_fx", text="Refresh", icon="FILE_REFRESH")
            row.operator("jideeh.rebuild_face_fx", text="Rebuild")
            row = col.row()
            row.scale_y = 1
            row.operator("jideeh.parent_face_mesh", text="Parent Face Mesh")

            row = box.row(align=True)
            row.prop(scene, "jideeh_face_fx_cache_enabled", text="Cache")
            row.operator("jideeh.clear_face_fx_cache", text="Clear", icon="TRASH")

classes = (
    JIDEEH_OT_append_face_fx,
    JIDEEH_OT_refresh_face_fx,
    JIDEEH_OT_rebuild_face_fx,
    JIDEEH_OT_parent_face_mesh,
    JIDEEH_OT_clear_face_fx_cache,
    JIDEEH_OT_apply_face_fx_drivers,
    JIDEEH_OT_set_face_lightmap,
    JIDEEH_OT_run_better_fbx_importer,
    JIDEEH_OT_run_setup_shader_rig_outline,
    JIDEEH_OT_run_jideeh_setup,
    JIDEEH_OT_run_facerig,
    JIDEEH_OT_run_face_panel_controllers,
    JIDEEH_OT_run_thugs_rig_script,
    JIDEEH_OT_run_bangboo_rig,
    JIDEEH_OT_run_remove_empties,
    JIDEEH_OT_run_shaders_outlines,
    JIDEEH_OT_run_shaders_outlines_no_face,
    JIDEEH_PT_script_runner_panel,
)

def register_scene_props():
    bpy.types.Scene.jideeh_show_extra_utilities = bpy.props.BoolProperty(name="Extra Utilities", default=False)
    bpy.types.Scene.jideeh_show_lightmap = bpy.props.BoolProperty(name="Face Lightmap toggle", default=False)
    bpy.types.Scene.jideeh_show_face_fx = bpy.props.BoolProperty(name="Face FX", default=False)
    bpy.types.Scene.jideeh_face_fx_cache_enabled = bpy.props.BoolProperty(name="Cache", default=False)
    bpy.types.Scene.jideeh_face_fx_cache_path = bpy.props.StringProperty(name="Face FX Cache Path", default="", subtype="FILE_PATH")

    for group_name, prop_name, images in LIGHTMAP_SLIDERS:
        setattr(
            bpy.types.Scene,
            prop_name,
            bpy.props.IntProperty(
                name=group_name,
                default=1,
                min=1,
                max=len(images),
                update=make_lightmap_update(prop_name, images),
            ),
        )

def unregister_scene_props():
    for prop_name in ["jideeh_show_extra_utilities", "jideeh_show_lightmap", "jideeh_show_face_fx", "jideeh_face_fx_cache_enabled", "jideeh_face_fx_cache_path"] + [entry[1] for entry in LIGHTMAP_SLIDERS]:
        if hasattr(bpy.types.Scene, prop_name):
            delattr(bpy.types.Scene, prop_name)

def enable_register_on_this_text():
    markers = [
        "JIDEEH_PT_script_runner_panel",
        "jideeh.run_setup_shader_rig_outline",
        "jideeh.run_jideeh_setup",
        "jideeh.run_facerig",
        "jideeh.run_face_panel_controllers",
        "jideeh.run_thugs_rig_script",
        "jideeh.run_bangboo_rig",
        "jideeh.run_remove_empties",
        "jideeh.run_shaders_outlines",
        "jideeh.run_shaders_outlines_no_face",
        "jideeh.run_better_fbx_importer",
        "jideeh.set_face_lightmap",
        "jideeh.append_face_fx",
        "jideeh.apply_face_fx_drivers",
        "jideeh.refresh_face_fx",
        "jideeh.rebuild_face_fx",
        "jideeh.parent_face_mesh",
        "jideeh.clear_face_fx_cache",
        "Face Lightmap toggle",
    ]

    for text in bpy.data.texts:
        body = text.as_string()

        if all(marker in body for marker in markers):
            text.use_module = True
            return text.name

    return None

def register():
    disable_auto_keying()

    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass

    for cls in classes:
        bpy.utils.register_class(cls)

    register_scene_props()

    enabled_text_name = enable_register_on_this_text()

    if enabled_text_name:
        print(f'Auto-register enabled for text block: {enabled_text_name}')
    else:
        print("Could not automatically find this text block to enable Register.")

    print("Auto-keying disabled.")

def unregister():
    unregister_scene_props()

    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass

if __name__ == "__main__":
    register()