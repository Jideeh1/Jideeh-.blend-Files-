import bpy

bpy.ops.object.mode_set(mode='EDIT')

eb = bpy.context.object.data.edit_bones

selected = sorted([b.name for b in bpy.context.selected_bones])

groups = {}

for name in selected:
    key = name[:-2]
    groups.setdefault(key, []).append(name)

for key, chain in groups.items():

    chain.sort()

    for i in range(len(chain)):

        bone = eb[chain[i]]

        bone.length *= 0.5

        if i > 0:
            bone.parent = eb[chain[i - 1]]

print("Done")