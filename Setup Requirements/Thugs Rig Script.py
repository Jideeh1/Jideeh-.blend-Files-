### CREDITS:
### Rigging+Scripting: Enthralpy
### Shader: Just_ScaasI, BonnyAnimations, Aiko
### Supervised and made possible by Stormz67  

# INSTRUCTION
# Import using betterfbx
# Run this script
# Long chains of bones like tails usually have broken parenting. Select the tail bones and then run script #2

# NOTE: This is the RIG-ONLY build. The Shader, Geonode and Outline setup
# have been removed; running this script only generates the character rig.

import bpy
ver = bpy.app.version_string
if ver[:3] == '4.0':
    ver = 4
elif ver[0] == '4':
    ver = float(ver[:3])
elif ver[0] == '3':
    ver = 3
else:
    raise Exception("youre using blender 3 or blender 4 right??")

# Import the FBX with BetterFBX, then run this script.
#
# Leave charname as "" to auto-derive it from the armature name
# ("Avatar_Female_Size02_Brujas_UI" -> "Brujas"). Or hard-set it here.
charname = ""

# Set True only if you want the script to hide HairShadow / _FX helper objects.
# Left False so nothing in your file disappears (some outline/effect meshes are
# geometry-node driven and would otherwise vanish from view).
HIDE_HELPER_OBJECTS = False



bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.scale_clear(clear_delta=False)
bpy.ops.object.select_all(action='DESELECT')

# --- Avatar / Bip001 armature finder -----------------------------------------
# This character's armature is named like "Avatar_Female_Size02_Brujas_UI"
# (some rips instead call it "Bone_Root"). Grab the character armature, and if
# it hangs off an Empty, adopt that Empty's name and delete it.
faceobj = None
arm = None
for ob in bpy.data.objects:
    n = ob.name.lower()
    if "_face" in n and "weapon_" not in n and "gun_" not in n and ob.type == 'MESH':
        faceobj = ob
    if ob.type == 'ARMATURE' and 'lighting' not in n and 'eye' not in n and 'metarig' not in n:
        arm = ob
    if HIDE_HELPER_OBJECTS and ("hairshadow" in n or "_fx" in n):
        ob.hide_viewport = True
        ob.hide_render = True

# Prefer the obvious character armature names if several armatures exist.
for pref in ("Bone_Root",):
    _exact = bpy.data.objects.get(pref)
    if _exact is not None and _exact.type == 'ARMATURE':
        arm = _exact
if arm is None:
    arm = next((o for o in bpy.data.objects
                if o.type == 'ARMATURE' and 'avatar' in o.name.lower()), arm)

if arm is None:
    raise Exception("No character armature found (expected 'Avatar_...' or 'Bone_Root').")

# Auto-derive the character name from the armature, e.g.
# "Avatar_Female_Size02_Brujas_UI" -> "Brujas".
if charname.strip() == "":
    parts = arm.name.split("_")
    guess = parts[-1]
    if guess.lower() in ("ui", "model", "npc") and len(parts) >= 2:
        guess = parts[-2]
    charname = guess + " "

# If the armature is parented to an Empty, adopt its name and remove it.
if arm.parent is not None and arm.parent.type == 'EMPTY':
    parent_empty = arm.parent
    arm.parent = None
    try:
        bpy.data.objects.remove(parent_empty, do_unlink=True)
    except Exception as e:
        print("could not remove parent empty:", e)

# Rigify indexes some objects by <data-name>.001 after separate(); keep the
# object name and its armature-data name identical so that indexing is valid.
arm.data.name = arm.name
arm.show_in_front = True

### Zero the armature's object rotation so the model stands upright.
arm.rotation_euler = (0.0, 0.0, 0.0)
arm.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)


############### ARMATURE RIG SECTION #############
context = bpy.context

### RIG-ONLY: guarantee a valid active object before entering object mode
### (the deprecated shader pass used to leave one active here).
if bpy.context.view_layer.objects.active is None:
    bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
# Cerydra build: the character armature was already resolved above.
obj = arm

bpy.context.view_layer.objects.active = obj
obj.select_set(True)
    
if obj.name[-4:] == ".001":
     obj.name = obj.name[:-4]
print("Rig  Run\n\n")

## Rename all bones in selected armature to ORG
original_name = obj.name
abadidea = {
    ## --- Bone_Root (3ds Max Biped "Bip001" skeleton) -> Rigify metarig names ---
    ## Spine chain (Pelvis is the hip/root; note we skip spine.005 like the
    ## human metarig's neck offset)
    'Bip001 Pelvis': 'spine',
    'Bip001 Spine': 'spine.001',
    'Bip001 Spine1': 'spine.002',
    'Bip001 Spine2': 'spine.003',
    'Bip001 Neck': 'spine.004',
    'Bip001 Head': 'spine.006',
    ## Left leg
    'Bip001 L Thigh': 'thigh.L',
    'Bip001 L Calf': 'shin.L',
    'Bip001 L Foot': 'foot.L',
    'Bip001 L Toe0': 'toe.L',
    ## Right leg
    'Bip001 R Thigh': 'thigh.R',
    'Bip001 R Calf': 'shin.R',
    'Bip001 R Foot': 'foot.R',
    'Bip001 R Toe0': 'toe.R',
    ## Left arm  (Clavicle = shoulder, UpperArm = upper_arm)
    'Bip001 L Clavicle': 'shoulder.L',
    'Bip001 L UpperArm': 'upper_arm.L',
    'Bip001 L Forearm': 'forearm.L',
    'Bip001 L Hand': 'hand.L',
    ## Right arm
    'Bip001 R Clavicle': 'shoulder.R',
    'Bip001 R UpperArm': 'upper_arm.R',
    'Bip001 R Forearm': 'forearm.R',
    'Bip001 R Hand': 'hand.R',
    ## Left fingers  (Biped: Finger0=thumb, 1=index, 2=middle, 3=ring, 4=pinky)
    'Bip001 L Finger0': 'thumb.01.L',
    'Bip001 L Finger01': 'thumb.02.L',
    'Bip001 L Finger02': 'thumb.03.L',
    'Bip001 L Finger1': 'f_index.01.L',
    'Bip001 L Finger11': 'f_index.02.L',
    'Bip001 L Finger12': 'f_index.03.L',
    'Bip001 L Finger2': 'f_middle.01.L',
    'Bip001 L Finger21': 'f_middle.02.L',
    'Bip001 L Finger22': 'f_middle.03.L',
    'Bip001 L Finger3': 'f_ring.01.L',
    'Bip001 L Finger31': 'f_ring.02.L',
    'Bip001 L Finger32': 'f_ring.03.L',
    'Bip001 L Finger4': 'f_pinky.01.L',
    'Bip001 L Finger41': 'f_pinky.02.L',
    'Bip001 L Finger42': 'f_pinky.03.L',
    ## Right fingers
    'Bip001 R Finger0': 'thumb.01.R',
    'Bip001 R Finger01': 'thumb.02.R',
    'Bip001 R Finger02': 'thumb.03.R',
    'Bip001 R Finger1': 'f_index.01.R',
    'Bip001 R Finger11': 'f_index.02.R',
    'Bip001 R Finger12': 'f_index.03.R',
    'Bip001 R Finger2': 'f_middle.01.R',
    'Bip001 R Finger21': 'f_middle.02.R',
    'Bip001 R Finger22': 'f_middle.03.R',
    'Bip001 R Finger3': 'f_ring.01.R',
    'Bip001 R Finger31': 'f_ring.02.R',
    'Bip001 R Finger32': 'f_ring.03.R',
    'Bip001 R Finger4': 'f_pinky.01.R',
    'Bip001 R Finger41': 'f_pinky.02.R',
    'Bip001 R Finger42': 'f_pinky.03.R',
    ## Eyes + breasts (Skn_*_Chest = breast, Skn_*_Eye = eyeball)
    'Skn_L_Eye': 'eye.L',
    'Skn_R_Eye': 'eye.R',
    'Skn_L_Chest': 'breast.L',
    'Skn_R_Chest': 'breast.R',
    }

bpy.ops.object.mode_set(mode='EDIT')
armature = bpy.context.selected_objects[0].data

bpy.ops.armature.select_all(action='DESELECT')
def select_bone(bone):
    bone.select = True
    bone.select_head = True
    bone.select_tail = True

# Disconnect the spine bones so Expykit/Rigify can reposition them freely.
for _sp in ("Bip001 Spine", "Bip001 Spine1", "Bip001 Spine2"):
    _b = armature.edit_bones.get(_sp)
    if _b:
        select_bone(_b)
bpy.ops.armature.parent_clear(type='DISCONNECT')
bpy.ops.armature.select_all(action='DESELECT')

try:
    # Chest bones act as the breast bones on this skeleton.
    select_bone(armature.edit_bones["Skn_R_Chest"])
    select_bone(armature.edit_bones["Skn_L_Chest"])
    bpy.ops.armature.parent_clear(type='DISCONNECT')
    bpy.ops.armature.select_all(action='DESELECT')
except:
    pass

eb = armature.edit_bones
# Nudge the knees forward a hair so the IK solver bends the right way.
for _knee in ("Bip001 L Calf", "Bip001 R Calf"):
    _b = eb.get(_knee)
    if _b:
        _b.head[1] -= .005

bones_list = obj.pose.bones
for bone in bones_list:
    if bone.name in abadidea:
        bone.name = abadidea[bone.name]

# --- Ensure 3-segment fingers ----------------------------------------------
# Some characters have 2-bone fingers (e.g. only Finger1/Finger11), but Rigify
# and the finger roll/axis fixes below expect thumb/index/middle/ring/pinky to
# each have .01/.02/.03. Build short stub segments for any that are missing so
# nothing downstream KeyErrors and the generated finger rig is uniform.
eb = armature.edit_bones
for _side in ("L", "R"):
    for _fb in ("thumb", "f_index", "f_middle", "f_ring", "f_pinky"):
        _b1 = eb.get(_fb + ".01." + _side)
        if _b1 is None:
            continue
        _b2 = eb.get(_fb + ".02." + _side)
        if _b2 is None:
            _b2 = eb.new(_fb + ".02." + _side)
            _v = _b1.tail - _b1.head
            _b2.head = _b1.tail.copy()
            _b2.tail = _b1.tail + _v * 0.7
            _b2.parent = _b1
            _b2.use_connect = True
            _b2.use_deform = True
        _b3 = eb.get(_fb + ".03." + _side)
        if _b3 is None:
            _b3 = eb.new(_fb + ".03." + _side)
            _v = _b2.tail - _b2.head
            _b3.head = _b2.tail.copy()
            _b3.tail = _b2.tail + _v * 0.6
            _b3.parent = _b2
            _b3.use_connect = True
            _b3.use_deform = True


#put hand corection here
import mathutils
bpy.ops.armature.select_all(action='DESELECT')

bpy.context.object.data.use_mirror_x = True
try:
    eb["Skn_R_Mouth"].length = 0.04
    eb["Skn_L_Mouth"].length = 0.04
    eb["Skn_M_Mouth"].length = 0.04
except:
    pass
if eb["hand.L"].tail[0] <= eb["hand.L"].head[0]:
    eb["forearm.L"]
    eb["hand.L"].length = 0.2

    bone_1 = eb["forearm.L"]
    bone_2 = eb["hand.L"]

    direction = (bone_1.tail - bone_1.head).normalized()
    extended_tail_position = bone_1.tail + (direction * 2.0)
    bone_2.tail = extended_tail_position
    bone_2.length = bone_1.length

bpy.context.object.data.use_mirror_x = False

bpy.ops.armature.select_all(action='DESELECT')

        
# Fix finger rolls
how_not = ['f_index.01.L', 'f_index.02.L', 'f_index.03.L']
hahaha = ['f_middle.01.L', 'f_middle.02.L', 'f_middle.03.L']
to_name = ['f_ring.01.L', 'f_ring.02.L', 'f_ring.03.L']
things_efficiently = ['f_pinky.01.L', 'f_pinky.02.L', 'f_pinky.03.L']

for bone in how_not:
    armature.edit_bones[bone].roll -= .1197
    
for bone in hahaha:
    armature.edit_bones[bone].roll -= .04
    
for bone in to_name:
    armature.edit_bones[bone].roll += .1297
    
for bone in things_efficiently:
    armature.edit_bones[bone].roll += .338

if eb["shoulder.L"].roll > -50 and eb["shoulder.L"].roll < 80:
    armature.edit_bones["shoulder.R"].roll = -armature.edit_bones["shoulder.L"].roll 
elif eb["shoulder.R"].roll > -80 and eb["shoulder.R"].roll < 50:
    armature.edit_bones["shoulder.L"].roll = -armature.edit_bones["shoulder.R"].roll 
else:
    eb["shoulder.L"].roll = 0
    eb["shoulder.R"].roll = 0


#Aw shit here we go again.  This second loop is for making it possible to symmetrize pose bones properly.
for bone in bones_list:
    if ".L" in bone.name: 
        whee = bone.name[:-2] + ".R"
        if "f_" in bone.name or "thumb" in bone.name:
            armature.edit_bones[whee].roll = -armature.edit_bones[bone.name].roll
        else:
            lefteye = armature.edit_bones.get("eye.L") # for eyepatched characters
            righteye = armature.edit_bones.get("eye.R")
            if not righteye or not lefteye:
                pass
            else:
                try:
                    armature.edit_bones[bone.name].roll = -armature.edit_bones[whee].roll
                except:
                    pass

# Fixes the thumb scale rotating inward on x instead of z
armature.edit_bones["thumb.01.L"].roll += 3.14 / 4
armature.edit_bones["thumb.02.L"].roll += 3.14 / 4
armature.edit_bones["thumb.03.L"].roll += 3.14 / 4     
armature.edit_bones["thumb.01.R"].roll -= 3.14 / 4
armature.edit_bones["thumb.02.R"].roll -= 3.14 / 4
armature.edit_bones["thumb.03.R"].roll -= 3.14 / 4    

for bone in armature.edit_bones:
    if "thumb" in bone.name or "index" in bone.name or "middle" in bone.name or "ring" in bone.name or "pinky" in bone.name:
        if ".L" in bone.name:
            armature.edit_bones[bone.name].roll -= 1.571 
        else:
            armature.edit_bones[bone.name].roll += 1.571 
    ## The Biped master root ("Bip001") sits above the pelvis; reparent its
    ## non-spine children to spine and delete it.
    if bone.name == "Bip001":
        for childbone in bone.children:
            if childbone.name != "spine":
                armature.edit_bones[childbone.name].parent = armature.edit_bones['spine']
        armature.edit_bones.remove(bone)
    elif ".L" not in bone.name and ".R" not in bone.name:
        armature.edit_bones[bone.name].roll = 0

        
## Fixes the weirdass pelvis/spine bone.  Sets the spine's head and tail X to 0.  
def realign(bone):
    bone.head.x = 0
    bone.tail.x = 0
realign(armature.edit_bones['spine'])
realign(armature.edit_bones['spine.006'])


## Attaches the feet to the toes and the upperarms to lowerarms
def attachfeets(foot, toe):
    armature.edit_bones[foot].tail.x = armature.edit_bones[toe].head.x
    armature.edit_bones[foot].tail.y = armature.edit_bones[toe].head.y
    armature.edit_bones[foot].tail.z = armature.edit_bones[toe].head.z

attachfeets('foot.L', 'toe.L')
attachfeets('foot.R', 'toe.R')
attachfeets('upper_arm.L', 'forearm.L')
attachfeets('upper_arm.R', 'forearm.R')
attachfeets('thigh.L', 'shin.L')
attachfeets('thigh.R', 'shin.R') 
attachfeets('forearm.L', 'hand.L')
attachfeets('forearm.R', 'hand.R')
attachfeets('spine', 'spine.001')
attachfeets('spine.001', 'spine.002')
attachfeets('spine.002', 'spine.003')
attachfeets('spine.003', 'spine.004')
attachfeets('spine.004', 'spine.006')

## Points toe bones in correct direction
armature.edit_bones['toe.L'].tail.z = 0
armature.edit_bones['toe.R'].tail.z = 0
armature.edit_bones['toe.L'].tail.y -= 0.05
armature.edit_bones['toe.R'].tail.y -= 0.05
        
bpy.ops.armature.select_all(action='DESELECT')
try:
    select_bone(armature.edit_bones["breast.L"])
    bpy.ops.armature.symmetrize()
    bpy.ops.armature.select_all(action='DESELECT')

except Exception:
    pass

try:
    armature.edit_bones["eye.L"].name = "DEF-eye.L"
    armature.edit_bones["eye.R"].name = "DEF-eye.R"
except:
    pass
bpy.ops.object.mode_set(mode='POSE')

bpy.ops.object.expykit_convert_bone_names(src_preset='Rigify_Metarig.py', trg_preset='Rigify_Deform.py')
bpy.ops.object.expykit_extract_metarig(rig_preset='Rigify_Metarig.py', assign_metarig=True)



## Fixes the tiddy bones.  Expykit, why did you neglect them

metarm = bpy.data.objects["metarig"].data
bpy.ops.object.mode_set(mode='EDIT')
armature = bpy.data.objects[obj.name].data

## Left side first, right side's xyz is same as left, but x is negative
def getboob(bone, tip):
    if tip == "head":
        return armature.edit_bones[bone].head.x, armature.edit_bones[bone].head.y, armature.edit_bones[bone].head.z
    else:
        return armature.edit_bones[bone].tail.x, armature.edit_bones[bone].tail.y, armature.edit_bones[bone].tail.z
        
    
try:
    xh, yh, zh = getboob("breast.L", "head")
    xt, yt, zt = getboob("breast.L", "tail")

    ## Change the meta arm's boob positions

    def fixboob(bone, xh, yh, zh, xt, yt, zt):
        bone.head.x = xh
        bone.head.y = yh
        bone.head.z = zh
        bone.tail.x = xt
        bone.tail.y = yt
        bone.tail.z = zt

    boobL = metarm.edit_bones["breast.L"]
    fixboob(boobL, xh, yh, zh, xt, yt, zt)
    boobR = metarm.edit_bones["breast.R"]
    fixboob(boobR, -xh, yh, zh, -xt, yt, zt)

    boobL.roll = armature.edit_bones["breast.L"].roll
    boobR.roll = -boobL.roll
except Exception:
    # If breast bones dont exist in the orig rig, then delete from the meta rig
    metarm.edit_bones.remove(metarm.edit_bones["breast.L"])
    metarm.edit_bones.remove(metarm.edit_bones["breast.R"])
    
    
    
# Fixes the finger rolls
bpy.ops.object.mode_set(mode='OBJECT')
metapose = bpy.data.objects['metarig'].pose
for bone_name in ['f_index', 'f_middle', 'f_ring', 'f_pinky']:
    metapose.bones[f"{bone_name}.01.L"].rigify_parameters.primary_rotation_axis = 'Z'
    metapose.bones[f"{bone_name}.01.R"].rigify_parameters.primary_rotation_axis = '-Z'
                                                                           
metapose.bones["thumb.01.L"].rigify_parameters.primary_rotation_axis = 'Z'
metapose.bones["thumb.01.R"].rigify_parameters.primary_rotation_axis = '-Z'     

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

armature = obj.data
for o in bpy.data.objects:
    # Check for given object names
    if o.name in ("metarig", armature.name):
        o.select_set(True)

bpy.ops.object.mode_set(mode='EDIT')
for bone in metarm.edit_bones:
    if "f_" in bone.name or "thumb" in bone.name:
        bone.roll =  armature.edit_bones["DEF-"+bone.name].roll


##########  DETACH PHYSICS BONES,  

metanames = ['eye.L', 'eye.R', 'spine', 'thigh.L', 'shin.L', 'foot.L', 'toe.L', 'thigh.R', 'shin.R', 'foot.R', 'toe.R', 'spine.001', 'spine.002', 'spine.003', 'breast.L', 'breast.R', 'shoulder.L', 'upper_arm.L', 'forearm.L', 'hand.L', 'thumb.01.L', 'thumb.02.L', 'thumb.03.L', 'f_index.01.L', 'f_index.02.L', 'f_index.03.L', 'f_middle.01.L', 'f_middle.02.L', 'f_middle.03.L', 'f_ring.01.L', 'f_ring.02.L', 'f_ring.03.L', 'f_pinky.01.L', 'f_pinky.02.L', 'f_pinky.03.L', 'spine.004', 'spine.006', 'shoulder.R', 'upper_arm.R', 'forearm.R', 'hand.R', 'thumb.01.R', 'thumb.02.R', 'thumb.03.R', 'f_index.01.R', 'f_index.02.R', 'f_index.03.R', 'f_middle.01.R', 'f_middle.02.R', 'f_middle.03.R', 'f_ring.01.R', 'f_ring.02.R', 'f_ring.03.R', 'f_pinky.01.R', 'f_pinky.02.R', 'f_pinky.03.R']

pre_res = ["DEF-" + bonename for bonename in metanames]
armature = obj.data ## Original char rig


## Make a dictionary.  Key is a main body bone that exists in the Rigify (arm, leg, spine, etc), and the value is a list of all the children bones that aren't other main body bones (usually hair, clothes, deform, etc.)
savethechildren = {
    
}
bpy.ops.object.mode_set(mode='EDIT')
for bone in armature.edit_bones:
    if bone.name in pre_res:
        childlist = []
        for childbone in armature.edit_bones[bone.name].children:
            if childbone.name not in pre_res: # Adds only non-main body bones, avoids like forearm or knee etc
                childlist.append(childbone.name)
        if childlist: # If list isn't empty, add it to dict
            wtf = bone.name
            savethechildren[wtf] = childlist

    
## Duplicates the physics bones
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.armature.select_all(action='DESELECT')
bones = armature.edit_bones[:]
for bone in bones:
    if bone.name not in pre_res:
        #this is a physics bone, so duplicate it.
        bone.select = True
        bone.select_tail = True
        bone.select_head = True

bpy.ops.armature.separate()
# Generates rigify rig and renames it to 'rigify'
bpy.ops.pose.rigify_generate()
bpy.data.objects[obj.name].name = "rigify"
bpy.context.view_layer.objects.active = bpy.data.objects[armature.name + ".001"]


for o in bpy.data.objects:
    # Check for given object names
    if o.name in ("rigify", armature.name):
        o.select_set(True)
        
# THEN REATTACH PHYSICS

bpy.ops.object.mode_set(mode='OBJECT')
### BLENDER ARE U GOOD LMAO WTF IS THIS (this joins two objects together)
newrig = armature.name + ".001" ## New temporary armature with the physics bones. Hopefully you didnt touch any names lmao

## Why's the list for selected objects ordered alphabetically instead of by selection order
objList = bpy.context.selected_objects
unselected = [obj for obj in objList if obj != context.active_object]
rigifyr = unselected[0]  ## Rigified Rig

obs = [bpy.data.objects[rigifyr.name], bpy.data.objects[newrig]]
c={}
c["object"] = c["active_object"] = bpy.data.objects[rigifyr.name]
c["selected_objects"] = c["selected_editable_objects"] = obs
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

with bpy.context.temp_override(active_object=bpy.data.objects.get("rigify"), selected_editable_objects=obs):
    bpy.ops.object.join()


bpy.context.view_layer.objects.active = bpy.data.objects["rigify"]
bpy.ops.object.mode_set(mode='EDIT')

## Reattach the physics bones to their parents
#Go back into rigify, find the main body bones, and reattach every bone in the corresponding dict list
for mainbone in savethechildren:    
    for childbone in savethechildren[mainbone]:
        rigifyr.data.edit_bones[childbone].parent = rigifyr.data.edit_bones[mainbone]

print("donelol\n")
bpy.ops.object.mode_set(mode='OBJECT')
bpy.data.objects["rigify"].show_in_front = True

# Symmetrize clothes/hair bones
for bone in rigifyr.data.edit_bones:
    if " L " in bone.name:  # Finds clothes/hair bones with symmetrical bones
        y = bone.name.find(' L ')  # Finds index of "Hair L 1"
        orgname = bone.name
        try:
            oppbone = orgname[:y] + " R " + orgname[y+3:] # oppbone = "Hair R 1"
            bone.name = orgname[:y] + orgname[y+3:] + ".L"  #Rename bones to "Hair 1.L/R" so Blender 
            rigifyr.data.edit_bones[oppbone].name = orgname[:y] + orgname[y+3:] + ".R" # goes ":o symmetry"
        except:
            pass


bpy.ops.object.mode_set(mode='POSE')

rigifyr.pose.bones["upper_arm_parent.L"]["pole_parent"] = 2
rigifyr.pose.bones["upper_arm_parent.R"]["pole_parent"] = 2
rigifyr.pose.bones["thigh_parent.L"]["pole_parent"] = 2
rigifyr.pose.bones["thigh_parent.R"]["pole_parent"] = 2
rigifyr.pose.bones["upper_arm_parent.R"]["pole_vector"] = True
rigifyr.pose.bones["upper_arm_parent.L"]["pole_vector"] = True
rigifyr.pose.bones["thigh_parent.L"]["pole_vector"] = True
rigifyr.pose.bones["thigh_parent.R"]["pole_vector"] = True


bpy.ops.object.mode_set(mode='OBJECT')
#change active object to rigifyr

bpy.context.view_layer.objects.active = bpy.data.objects["rigify"]

bpy.ops.object.mode_set(mode='OBJECT')

# This part puts all the main bones I use into the secoond bone layer
listofbones = ["root", "eye.L", "eye.R", "foot_heel_ik.R", "foot_heel_ik.L", "toe_ik.R", "toe_ik.L", "foot_ik.R", "foot_ik.L", "thigh_ik_target.R", "thigh_ik_target.L", "hips", "torso", "chest", "neck", "head", "shoulder.L", "shoulder.R", "upper_arm_fk.L", "upper_arm_fk.R", "forearm_fk.L", "forearm_fk.R", "hand_fk.L", "hand_fk.R", "upper_arm_ik_target.L", "upper_arm_ik_target.R", "hand_ik.R", "hand_ik.L"]

clothes = ["ribbon", "sleeve", "strap", "skirt", "button", "belt", "cloth", "tail", "bag", "chain", "collar", "cloak", "hat",
           "yidai", "hubi", "jiankou", "hujia", "fadai", "routui", "shake", "cj",
           "weapon", "wpn", "guneye", "teles", "hood", "hoop", "brooch", "wristband",
           "shoelace", "footring", "hipcovering",
           "gun", "runner", "majia", "yaodai", "tielian", "prop",
           "crossbow", "thug", "grenade", "helmet", "ext_"]
hair = ["hair", "eardrop", "bangs", "liuhai", "maweibian", "fadai_"]
face = ["brow", "mouth", "eye", "ear_", "teeth"]

eb = obj.pose.bones
bpy.ops.object.mode_set(mode='POSE')
if ver == 3:
    for bone in listofbones:
        bpy.context.active_object.pose.bones[bone].bone.layers[1] = True
        
        # Separates physics-related bones into layers 22 and 23
    for bone in eb:
        for name in clothes:
            if name in bone.name.lower():
                obj.pose.bones[bone.name].bone.layers[22] = True
                obj.pose.bones[bone.name].bone.layers[0] = False
        for name in hair:
            if name in bone.name.lower():
                obj.pose.bones[bone.name].bone.layers[23] = True
                obj.pose.bones[bone.name].bone.layers[0] = False

else:
    bone_collection = rigifyr.data.collections.new(name="Main")
    for bone_name in listofbones:
        bone_collection.assign(rigifyr.pose.bones.get(bone_name))
        
    bpy.ops.pose.select_all(action='DESELECT')
    phys_collection = rigifyr.data.collections.new(name="Clothes")
    hair_collection = rigifyr.data.collections.new(name="Hair")
    misc_collection = rigifyr.data.collections.new(name="Misc")
    # Cerydra build: the metarig is extracted with no_face, so Rigify never
    # creates a "Face" collection. Make one ourselves so the face deform bones
    # (brows, lips, mouth, eyes, ears) have a home.
    if "Face" not in rigifyr.data.collections:
        rigifyr.data.collections.new(name="Face")
    for bone in eb:  # search every bone to see if it's a physisc bone by name
        for name in clothes:
            if name in bone.name.lower():
                phys_collection.assign(bone)
        for name in hair:
            if name in bone.name.lower():
                hair_collection.assign(bone)

        for name in face:
            if name in bone.name.lower() and "DEF-" not in bone.name and "ORG-" not in bone.name:
                rigifyr.data.collections["Face"].assign(bone)

        if not any(bone.name in coll.bones for coll in rigifyr.data.collections):
            misc_collection.assign(bone)
    # Move our custom collections to the front; index 26 assumes a full ZZZ
    # face rig, which we don't have, so guard it.
    try:
        for _ in range(4):
            rigifyr.data.collections.move(len(rigifyr.data.collections) - 1, 0)
    except Exception as e:
        print("collection reorder skipped:", e)
    if ver == 4: # version 4.0
        bpy.ops.armature.collection_solo_visibility(name="Main")
    elif ver != 3:
        for c in rigifyr.data.collections:
            c.is_visible = False
        rigifyr.data.collections_all["Main"].is_visible = True
        pass
#    rigifyr.data.collections["Physics"].is_visible = True
#    rigifyr.data.collections["Hair"].is_visible = True

        
bpy.ops.object.mode_set(mode='OBJECT')
bpy.data.objects["rigify"].name = charname.strip() + "Rig"


bpy.ops.object.mode_set(mode='EDIT')
bones = rigifyr.data.edit_bones[:]

# this bitch empty. YEET
#rigifyr.data.edit_bones.remove(rigifyr.data.edit_bones["palm.L"])
#rigifyr.data.edit_bones.remove(rigifyr.data.edit_bones["palm.R"])

# Change any physics bones attached to shoulder to be attached to spine instead bc it's a pain in the ass
# for bone in bones:
    # if bone.parent:
        # if bone.name not in pre_res and bone.parent.name in ["DEF-shoulder.L", "DEF-shoulder.R"]:
            # print(bone)
            # bone.parent = rigifyr.data.edit_bones["DEF-spine.003"]
        
# makes a root #2 bone
newroot = rigifyr.data.edit_bones.new("root_2")
root = rigifyr.data.edit_bones["root"]
newroot.head = root.head.copy()
newroot.tail = root.tail.copy()
newroot.roll = root.roll
newroot.matrix = root.matrix.copy()
newroot.tail.y += 0.5
root.parent = newroot

bpy.ops.object.mode_set(mode='POSE')   
bpy.ops.pose.select_all(action='DESELECT')
bones_list = obj.pose.bones
bpy.ops.object.mode_set(mode='POSE')
# Widget objects are named after the generated rig; the exact name varies, so
# find the root widget instead of assuming "WGT-<original>_root".
_root_wgt = bpy.data.objects.get("WGT-" + original_name + "_root")
if _root_wgt is None:
    _root_wgt = next((o for o in bpy.data.objects
                      if o.name.startswith("WGT-") and o.name.endswith("_root")), None)
if _root_wgt is not None:
    rigifyr.pose.bones["root_2"].custom_shape = _root_wgt

bpy.ops.pose.select_all(action='DESELECT')
bone = rigifyr.pose.bones["root_2"].bone
rigifyr.data.bones.active = bone
if ver == 3:
    bpy.ops.pose.group_assign(type=6)
    for x in range(0, 28):
        bone.layers[x] = False
    bone.layers[1] = True

else:
    rigifyr.data.collections["Main"].assign(rigifyr.pose.bones.get("root_2"))
    rigifyr.data.collections["Root"].assign(rigifyr.pose.bones.get("root_2"))

# Creates selection sets for FK arms + shoulders, hair bones, and clothes bones.  Selection Sets is an addon that comes with Blender.
try:
    bpy.ops.object.mode_set(mode='POSE')

    arms = ['upper_arm_fk', 'forearm_fk', 'hand_fk', 'shoulder']
    bpy.ops.pose.select_all(action='DESELECT')
    for side in ['.L', '.R']:
        for bone in arms:
            bonename = bone + side
            rigifyr.pose.bones[bonename].bone.select= True
    bpy.ops.pose.selection_set_add()
    bpy.ops.pose.selection_set_assign()
    bpy.ops.pose.select_all(action='DESELECT')

    ## Hair
    for bone in bones_list:
        if "Hair" in bone.name:
            rigifyr.pose.bones[bone.name].bone.select = True
    bpy.ops.pose.selection_set_add()
    bpy.ops.pose.selection_set_assign()
    bpy.ops.pose.select_all(action='DESELECT')

    ## Clothes
    for bone in bones_list:
        if "Amice" in bone.name or ("fk" not in bone.name and "tweak" not in bone.name and "Twist" not in bone.name and "Hair" not in bone.name and (bone.name[-1].isdigit() or bone.name[-3].isdigit())):
            rigifyr.pose.bones[bone.name].bone.select = True
    bpy.ops.pose.selection_set_add()
    bpy.ops.pose.selection_set_assign()
    bpy.ops.pose.select_all(action='DESELECT')
    bpy.context.object.selection_sets[0].name = "FK Arms"
    bpy.context.object.selection_sets[1].name = "Hair"
    bpy.context.object.selection_sets[2].name = "Clothes"
except:
    pass

bpy.ops.object.mode_set(mode='OBJECT')
    
rigifyr.pose.bones["upper_arm_parent.L"]["IK_Stretch"] = 0.000
rigifyr.pose.bones["upper_arm_parent.R"]["IK_Stretch"] = 0.000
rigifyr.pose.bones["thigh_parent.L"]["IK_Stretch"] = 0.000
rigifyr.pose.bones["thigh_parent.R"]["IK_Stretch"] = 0.000
rigifyr.pose.bones["torso"]["neck_follow"] = 1.000

rig = rigifyr

for oDrv in rig.animation_data.drivers:
    for variable in oDrv.driver.variables:
        for target in variable.targets:
            if ".03" in oDrv.data_path and target.data_path[-7:] == "scale.y":
                target.data_path = target.data_path[:-1] + "x"


fingerlist = ["thumb.01_master", "f_index.01_master", "f_middle.01_master", "f_ring.01_master", "f_pinky.01_master"]

for side in [".L", ".R"]:
    for bone in fingerlist:
        rig.pose.bones[bone + side].lock_scale[0] = False
        

armature = rig

fucks = ["upper_arm_ik_target.L", "upper_arm_ik_target.R", "VIS_upper_arm_ik_pole.L", "VIS_upper_arm_ik_pole.R", "thigh_ik_target.L", "thigh_ik_target.R", "VIS_thigh_ik_pole.L", "VIS_thigh_ik_pole.R"]
bpy.ops.object.mode_set(mode='POSE')
for fuck in fucks:
    armature.data.bones[fuck].driver_remove("hide")
    
bpy.ops.object.mode_set(mode='EDIT')
for bone in armature.data.edit_bones:
    if "_L_" in bone.name:  # Finds clothes/hair bones with symmetrical bones
        y = bone.name.find('_L_')  # Finds index of "Hair_L_1"
        orgname = bone.name
        try:
            oppbone = orgname[:y] + "_R_" + orgname[y+3:] # oppbone = "Hair_R_1"
            bone.name = orgname[:y] + orgname[y+3:] + ".L"  #Rename bones to "Hair 1.L/R" so Blender 
            armature.data.edit_bones[oppbone].name = orgname[:y] + orgname[y+3:] + ".R" # goes ":o symmetry"
#            print(orgname, oppbone)
        except:
            pass

bpy.ops.object.mode_set(mode='OBJECT')

### RIG-ONLY: the lighting panel, head-direction empties, and color wheels
### live only in the shader/setup .blend, so all of that setup is removed here
### (as is the face rig, which depended on the same file). Just name the rig.
bpy.context.view_layer.objects.active = rigifyr
rigifyr.name = charname + "Rig"
_rig_coll = rig.users_collection[0]
if _rig_coll != bpy.context.scene.collection:  # the master Scene Collection's name is read-only
    _rig_coll.name = charname[:-1]

bpy.ops.object.mode_set(mode='EDIT')
edit_bones = rigifyr.data.edit_bones
### EYE RIG PART
eyes = True
if "eye.R" not in rigifyr.pose.bones and "eye.L" not in rigifyr.pose.bones:
    eyes = False

if eyes:
    if "eye.L" in rigifyr.pose.bones:
        original_bone = edit_bones["eye.L"]
        new_bone = edit_bones.new("Eye Control")
        
    elif "eye.R" in rigifyr.pose.bones:
        original_bone = edit_bones["eye.R"]
        new_bone = edit_bones.new("Eye Control")
        
    new_bone.use_inherit_rotation = False
    new_bone.parent = edit_bones["DEF-spine.006"]
    new_bone.name = "Eye Control"
    new_bone.head = original_bone.head
    new_bone.tail = original_bone.tail
    new_bone.head.x = 0
    new_bone.tail.x = 0
    new_bone.head.z = new_bone.tail.z
    new_bone.head.y -= 0.1
    new_bone.tail.y -= 0.15
    new_bone.head[2] = original_bone.head[2]
    new_bone.tail[2] = original_bone.head[2]
    new_bone.length = .07

# Switch to pose mode to set custom shape
bpy.ops.object.mode_set(mode='POSE')
if eyes:
    if ver != 3:
        rigifyr.data.collections["Main"].assign(rigifyr.pose.bones.get("Eye Control"))
        rigifyr.data.collections["Face"].assign(rigifyr.pose.bones.get("Eye Control"))
    pose_bone = rigifyr.pose.bones["Eye Control"]
    pose_bone.custom_shape = rigifyr.pose.bones["thigh_ik_target.L"].custom_shape
    eye_bones = ["eye.L", "eye.R"]
    for bone_name in eye_bones:
        try:
            pose_bone = rigifyr.pose.bones[bone_name]
            constraint = pose_bone.constraints.new(type='CHILD_OF')
            constraint.target = rigifyr
            constraint.subtarget = "Eye Control"
            constraint.use_location_x = False
            constraint.use_location_y = False
            constraint.use_location_z = False
            constraint.use_scale_x = False
            constraint.use_scale_y = False
            constraint.use_scale_z = False
        except:
            pass
    pose_bone = rigifyr.pose.bones["Eye Control"] ### For eye shrink shapekeys later
    constraint = pose_bone.constraints.new(type='LIMIT_SCALE')
    constraint.use_min_x = True
    constraint.use_min_y = True
    constraint.use_min_z = True
    constraint.min_x = 0.100
    constraint.min_y = 0.100
    constraint.min_z = 0.100

if ver != 3:
    cols = rigifyr.data.collections

    def _row(colname, row, title=None):
        """Set a UI row / title only if the collection actually exists."""
        c = cols.get(colname)
        if c is None:
            return
        c.rigify_ui_row = row
        if title is not None:
            c.rigify_ui_title = title

    # These only exist if a Rigify face rig was generated; we extract with
    # no_face, so remove them defensively instead of assuming they're present.
    for dead in ("Face (Primary)", "Face (Secondary)"):
        c = cols.get(dead)
        if c is not None:
            cols.remove(c)

    for c in cols:
        if c.rigify_ui_row:
            c.rigify_ui_row -= 3

    _row("Main", 1)
    _row("Face", 2)
    _row("Torso", 4)
    _row("Torso (Tweak)", 4, "Torso (Tweak)")
    _row("Fingers", 5)
    _row("Fingers (Detail)", 5, "Fing (Detail)")
    _row("Root", 15)
    _row("Clothes", 16)
    _row("Hair", 16)
    _row("Misc", 17)



bpy.ops.object.mode_set(mode='OBJECT')  


### RIG-ONLY: face rig object-hiding drivers removed (no face rig / no "Facerig" collection).
armature = rigifyr

## This next part adds the eye shrink stuff
if eyes:
    bpy.context.view_layer.objects.active = faceobj
    faceobj.shape_key_add(name="ShrinkEye.R")
    faceobj.shape_key_add(name="ShrinkEye.L")

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'

    for side in ['R', 'L']:   # Shrink the eye vertices to make the shrink shapekeys
        notthisshitagain = ["DEF-eye." + side, "eye." + side + ".002", "eye." + side, "eye." + side + ".001", "SknHighlights." + side, "SknHighlights_New." + side]
        bpy.ops.mesh.select_all(action='DESELECT')
        for vg in notthisshitagain:
            if vg in faceobj.vertex_groups:
                if side == 'R':
                    faceobj.active_shape_key_index = len(faceobj.data.shape_keys.key_blocks)-2
                else:
                    faceobj.active_shape_key_index = len(faceobj.data.shape_keys.key_blocks)-1            
                group_index = faceobj.vertex_groups[vg].index
                bpy.ops.object.vertex_group_set_active(group=vg)
                bpy.ops.object.vertex_group_select()
        bpy.ops.transform.resize(value=(0.2, 0.2, 0.2))
            
    faceobj.active_shape_key_index = 0
    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.object.mode_set(mode='OBJECT')
    bone_name = "Eye Control"
    shape_keys = faceobj.data.shape_keys.key_blocks

    for shapekey in ["ShrinkEye.L", "ShrinkEye.R"]:
        sk = shape_keys[shapekey]
        
        driver = sk.driver_add("value").driver
        var = driver.variables.new()
        var.name = 'var'
        var.type = 'TRANSFORMS'
        var.targets[0].id = armature  # The object the bone belongs to
        var.targets[0].bone_target = bone_name
        var.targets[0].transform_type = 'SCALE_X'
        var.targets[0].transform_space = 'LOCAL_SPACE'
        driver.expression = '(-10*var)/9 + 10/9'

for obj in bpy.data.objects:
    if "metarig" in obj.name:
        obj.hide_viewport = True
        obj.hide_render = True

bpy.ops.object.select_all(action='DESELECT')
# NOTE: the original ZZZ script ended by deleting a throwaway
# "Shader Materials (delete later)" object and then running
# outliner.orphans_purge(do_recursive=True). That purge nukes any material or
# geometry-node group that isn't actively assigned at that instant, which
# destroys your file's shaders/geonodes. This is a rig-only build, so we do
# NOT purge anything. If you ever want to clean orphans, do it by hand from
# the Outliner so you can see what's being removed.