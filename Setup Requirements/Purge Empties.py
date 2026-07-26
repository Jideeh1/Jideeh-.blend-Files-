import bpy

head_direction_suffix = "head direction"
light_direction_suffix = "light direction"

def strip_blender_numeric_suffix(name):
    parts = name.rsplit(".", 1)

    if len(parts) == 2 and parts[1].isdigit():
        return parts[0]

    return name

def normalized_object_name(name):
    return strip_blender_numeric_suffix(name).lower()

def is_head_direction_object(obj):
    name = normalized_object_name(obj.name)
    return name == head_direction_suffix or name.endswith(" " + head_direction_suffix)

def is_light_direction_object(obj):
    name = normalized_object_name(obj.name)
    return name == light_direction_suffix or name.endswith(" " + light_direction_suffix)

def is_protected_root(obj):
    return is_head_direction_object(obj) or is_light_direction_object(obj)

def is_descendant_of_protected(obj):
    parent = obj.parent

    while parent is not None:
        if is_protected_root(parent):
            return True

        parent = parent.parent

    return False

def should_preserve_empty(obj):
    return is_protected_root(obj) or is_descendant_of_protected(obj)

try:
    bpy.ops.object.mode_set(mode="OBJECT")
except Exception:
    pass

empties_to_remove = []
empties_preserved = []

# Decide everything up front, against the original hierarchy,
# so that deletions cannot change any parent chain mid-pass.
for obj in list(bpy.data.objects):
    if obj.type == "EMPTY":
        if should_preserve_empty(obj):
            empties_preserved.append(obj.name)
        else:
            empties_to_remove.append(obj)

empties_removed = []
empties_failed = []

def unparent_children_keep_transform(obj):
    for child in list(obj.children):
        matrix_world = child.matrix_world.copy()
        child.parent = None
        child.matrix_world = matrix_world

for obj in empties_to_remove:
    obj_name = obj.name

    try:
        unparent_children_keep_transform(obj)
        bpy.data.objects.remove(obj, do_unlink=True)
        empties_removed.append(obj_name)
    except Exception as error:
        empties_failed.append(f"{obj_name}: {error}")

try:
    bpy.context.view_layer.update()
except Exception:
    pass

if empties_removed:
    print("Empties removed:")
    for object_name in empties_removed:
        print(object_name)
else:
    print("No empties were removed.")

if empties_preserved:
    print("Empties preserved (Head Direction / Light Direction and their contents):")
    for object_name in empties_preserved:
        print(object_name)
else:
    print("No Head Direction or Light Direction empties were found to preserve.")

if empties_failed:
    print("These empties could not be removed:")
    for entry in empties_failed:
        print(entry)

print(f"Removed {len(empties_removed)} empties, preserved {len(empties_preserved)}.")