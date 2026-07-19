### FACE PANEL — shape-key drivers (companion to the shaders+outlines script)
###
### Rigging+Scripting: Enthralpy   Shader: Just_ScaasI, BonnyAnimations, Aiko
### Supervised and made possible by Stormz67
###
### WHAT THIS DOES
### Builds the FaceRig control panel and adds drivers to the face mesh's shape
### keys so each expression is controlled by dragging the matching panel bone.
### This is the facerig portion pulled out of the main script and made runnable
### on its own.
###
### WHEN TO RUN
### After importing the model (and after running the shaders+outlines script, if
### you use it). The shaders+outlines script does not touch shape keys or create
### the face panel, so running this afterward is safe.
###
### REQUIREMENTS (same template objects the original script relied on)
###   - The face mesh (an object whose name ends in "_face")
###   - Face-panel template objects: "Facerig Border", "Extra 1".."Extra N",
###     "Extra 1 lim".."Extra N lim", and "Mth lim"
###
### NOTE: standalone, the panel is parented to "Facerig Border" and floats in
### place (it is not constrained to a head bone, since there's no rig here).

import bpy
import mathutils

ver = bpy.app.version_string
if ver[:3] == '4.0':
    ver = 4
elif ver[0] == '4':
    ver = float(ver[:3])
elif ver[0] == '3':
    ver = 3
else:
    raise Exception("youre using blender 3 or blender 4 right??")


# Find the face mesh (same detection the main script uses)
faceobj = None
for obj in bpy.data.objects:
    if "_face" in obj.name.lower() and "weapon_" not in obj.name.lower() and "gun_" not in obj.name.lower(): # gdi orphie
        faceobj = obj

if faceobj is None:
    raise Exception("Couldn't find a '*_face' mesh in the scene.")
if faceobj.data.shape_keys is None:
    raise Exception("The face mesh has no shape keys to drive.")


def shapekeyrename(keyblock):
    # rename inconsistent shapekeys, especially in older characters
    for sk in keyblock:
        if sk.name.endswith("_Unagi") or sk.name.endswith("_Anton") or sk.name.endswith("_Corin"): # miyabi, what the actual fuck
            sk.name = sk.name[:-6]
        if sk.name.endswith("_NuoCha"): # nicole, what the actual fuck
            sk.name = sk.name[:-7]
    dick = {
        "Mouth_↖_Ben" : "Fac_Mth_R_Up",
        "Mouth_↗_Ben" : "Fac_Mth_L_Up",
        "Mouth_↙_Ben": "Fac_Mth_R_Down", 
        "Mouth_↘_Ben": "Fac_Mth_L_Down", 
        "Mouth_上颌↑_Ben" : "Fac_Mth_Up", 
        "Mouth_下颌↓_Ben" : "Fac_Mth_Down", 
        "Mouth_呲_L_Ben" : "Fac_Mth_L_In", 
        "Mouth_呲_R_Ben" : "Fac_Mth_R_In", 
        "Eye_Open_↑_Ben": "Fac_Eye_R_Open",
        "Mouth_Oo_Ben": "Fac_Mth_UuOo",
        "Eye_Close2_Ben": "Fac_Eye_Sad",
        "Eye_Ball_↑_Ben": "Eye_Up",
        "Eye_Ball_↓_Ben": "Eye_Down",
        "Eye_Ball_→_Ben": "Eye_Left",
        "Eye_Ball_←_Ben": "Eye_Right",
        "Eye_Ball_No_Ben": "O_O",
        "Mouth_啧_R_Ben": "Fac_Mth_R_Out",
        "Mouth_啧_L_Ben": "Fac_Mth_L_Out" ,
        "Mouth_Ii1": "Fac_Mth_Ii",
        
        "Fac_Mth_Aa" : "Fac_Mth_Aa1", 
        "Fac_Mth_ooR" : "Fac_Mth_R_Out", 
        "Fac_Mth_Roo" : "Fac_Mth_R_In", 
        "Fac_Mth_Loo" : "Fac_Mth_L_Out", 
        "Fac_Mth_ooL" : "Fac_Mth_L_In", 
        "Fac_Mth_oo_RDown": "Fac_Mth_R_Down", 
        "Fac_Mth_LDown_oo": "Fac_Mth_L_Down", 
        "Fac_Mth_LUp_oo" : "Fac_Mth_L_Up",
        "Fac_Eye_Open_L" : "Fac_Eye_L_Open",
        "Fac_Eye_LowEyeUP" : "Fac_Eye_LowlidUp",
        "Fac_Eye_LowEyeUP" : "Fac_Eye_LowlidUp",
        "Fac_Mth_Laugh1" : "Fac_Mth_Laugh",
        
        ## NICOLE MIYABI WTF
        "EB_↑" : "Fac_Ebr_Up",
        "EB_↓" : "Fac_Ebr_Down", 
        "EB_Angry" : "Fac_Ebr_Angry", 
        "EB_Relax" : "Fac_Ebr_Relax", 
        "EB_困扰" : "Fac_Ebr_Sad", 
        "Eye_↙↘" : "Fac_Eye_BLBR",
        "Eye_Angry" : "Fac_Eye_Angry", 
        "Eye_Close" : "Fac_Eye_Close", 
        "Eye_Open_L" : "Fac_Eye_L_Open", 
        "Eye_Open_R" : "Fac_Eye_R_Open", 
        "Eye_Wink_L" : "Fac_Eye_L_Wink", 
        "Eye_Wink_R" : "Fac_Eye_R_Wink", 
        "EYE_Wink_L" : "Fac_Eye_L_Wink", 
        "EYE_Wink_R" : "Fac_Eye_R_Wink", 
        "Eye_半闭" : "Fac_Eye_HalfClose", 
        "Eye_困扰" : "Fac_Eye_Sad",
        "Eye_认真" : "Fac_Eye_MidDown",
        "Eye_下眼睑↑" : "Fac_Eye_LowlidUp", 
        "Mouth_△" : "Fac_Mth_Triangle", 
        "Mouth_↑" : "Fac_Mth_Up", 
        "Mouth_→" : "Fac_Mth_Left", 
        "Mouth_↓" : "Fac_Mth_Down", 
        "Mouth_←" : "Fac_Mth_Right", 
        "Mouth_Aa1" : "Fac_Mth_Aa1",
        "Mouth_Aa2" : "Fac_Mth_Aa2",
        "Mouth_Aa3Shout" : "Fac_Mth_Aa3Shout",
        "Mouth_AaTalk" : "Fac_Mth_AaTalk",
        "Mouth_Ee" : "Fac_Mth_Ee",
        "Mouth_Ii" : "Fac_Mth_Ii",
        "Mouth_Uu_Ben" : "Fac_Mth_Uu",
        "Mouth_Laugh" : "Fac_Mth_Laugh",
        "Mouth_Laugh2" : "Fac_Mth_Laugh2",
        "Mouth_oo←" : "Fac_Mth_L_In",
        "Mouth_↖oo" : "Fac_Mth_L_Up",
        "Mouth_←oo" : "Fac_Mth_R_Out",
        "Mouth_↙oo" : "Fac_Mth_R_Down",
        "Mouth_→oo" : "Fac_Mth_R_In",
        "Mouth_oo↗" : "Fac_Mth_R_Up",
        "Mouth_oo→" : "Fac_Mth_L_Out",
        "Mouth_oo↘" : "Fac_Mth_L_Down",
        "Mouth_Oo" : "Fac_Mth_Oo",
        "Mouth_Uu" : "Fac_Mth_Uu",
        "Mouth_UuOo" : "Fac_Mth_UuOo",
        
    }
    
    for key in dick.keys():
        try:
            keyblock[key].name = dick[key]  # change keyname to valuename
        except:
            for sk in keyblock:
                if key in sk.name:
                    sk.name = dick[key]
            pass

    for sk in keyblock:
        if sk.name.endswith("_Ben"): # put ben here bc this makes things easier.
            sk.name = sk.name[:-4]
            
def create_facerig_with_lim_bones(keyblock):
    shapekeys = [sk.name[4:] for sk in keyblock if "Fac_" in sk.name] # List of shapekey names without 'Fac_'
    for sk in keyblock:
        if "Fac_" not in sk.name and sk.name != "Basis":
            shapekeys.append(sk.name)
            sk.name = "Fac_" + sk.name  # starting to regret not just removing 'fac' from the shapekey names lol
        
    bpy.ops.object.armature_add()  # Create a new armature
    armature = bpy.context.object
    armature.name = "FaceRig"
    armature.data.name = "FaceRig"
    armature.parent = bpy.data.objects["Facerig Border"]    
    armature.matrix_parent_inverse = bpy.data.objects["Facerig Border"]   .matrix_world.inverted()
    
    
    bpy.ops.object.mode_set(mode='EDIT')  # Switch to edit mode
    armature.data.edit_bones.remove(armature.data.edit_bones["Bone"])
    faceroot = armature.data.edit_bones.new("Facerig Root")
    faceroot.head = (2, 0, 1.18)
    faceroot.tail = (2, 0, 1.48)
    
    for obj in bpy.data.objects:
        # Deal with extra shapekeys not in the base facerig
        if obj.name in shapekeys:
            shapekeys.remove(obj.name)
    print(shapekeys)

    for i in range(1, len(shapekeys)+1):
        text = bpy.data.objects["Extra " + str(i)]
        text.name = shapekeys[i-1]
        text.data.name = shapekeys[i-1]
        text.data.body = shapekeys[i-1]
        
        textlim = bpy.data.objects["Extra " + str(i) + " lim"]
        textlim.name = shapekeys[i-1] + " lim"
        textlim.data.name = shapekeys[i-1] + " lim"
        
    for obj in bpy.data.objects:
        if 'lim' in obj.name and ("Fac_" + obj.name[:-4]) in keyblock or (obj.name == "Mth lim"):  #  Makes a new bone if there's actually a shapekey for it
            bone = armature.data.edit_bones.new(obj.name[:-4] + " Bone")
            bone.head = obj.location  # Set bone head position
            bone.tail = obj.location + mathutils.Vector((0, 0, 0.1))  # Set bone tail position slightly above head
            bone.parent = armature.data.edit_bones["Facerig Root"]
        
    armature = bpy.data.objects["FaceRig"]
    
    bpy.ops.object.mode_set(mode='POSE')  
    
    for bone in armature.pose.bones:
        if ver != 3:
            armature.data.collections[0].assign(bone)
        if bone.name == "Facerig Root":
            continue
        bone.custom_shape = bpy.data.objects["Mth lim"]
        bone.custom_shape_scale_xyz[1] = 0.2
        bone.custom_shape_scale_xyz[2] = 0.2
        bone.custom_shape_scale_xyz[0] = 0.2
        
        # Lock transformations, rotation, and scale except X-axis
        if bone.name != "Mth Bone":
            bone.lock_location[1] = True
        bone.lock_location[2] = True
        bone.lock_rotation[0] = True
        bone.lock_rotation[1] = True
        bone.lock_rotation[2] = True
        bone.lock_scale[0] = True
        bone.lock_scale[1] = True
        bone.lock_scale[2] = True
        
        # Add limit location constraint
        if bone.name != "Mth Bone":
            constraint = bone.constraints.new(type='LIMIT_LOCATION')
            constraint.use_min_x = True
            constraint.use_max_x = True
            constraint.min_x = -0.1
            constraint.max_x = 0.1
            constraint.use_transform_limit = True
            constraint.owner_space = 'LOCAL'
        else:    
            constraint = bone.constraints.new(type='LIMIT_DISTANCE')
            constraint.distance = 0.1
            constraint.target = bpy.data.objects["Mth lim"]
    
    bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to object mode

def facestuff(mesh_obj):
    for shapekey in mesh_obj.data.shape_keys.key_blocks:
        if shapekey.name == "Basis":
            continue
        
        bone_name = shapekey.name
        shapekey.slider_min = -1.0
        
        if "Fac_" in bone_name:
            bone_name = bone_name[4:]
        if (bone_name + " Bone") in bpy.data.objects["FaceRig"].data.bones:

            driver = shapekey.driver_add("value").driver
            driver.type = 'SCRIPTED'
            var = driver.variables.new()
            var.name = "var"
            var.type = 'TRANSFORMS'
            target = var.targets[0]
            target.id = bpy.data.objects["FaceRig"]
            target.bone_target = bone_name + " Bone"
            target.transform_type = 'LOC_X' 
            target.transform_space = 'LOCAL_SPACE'
            
            driver.expression = "var / 0.1"

def mouthbone(keyblock):
    bone = bpy.data.objects["FaceRig"].data.bones["Mth Bone"]    

    sklist = ["Fac_Mth_Up","Fac_Mth_Left","Fac_Mth_Right","Fac_Mth_Down"]
    
    for shapekey in sklist: 
        if shapekey not in keyblock:
            continue
        keyblock[shapekey].slider_min = 0.0
        
        driver = keyblock[shapekey].driver_add("value").driver
        driver.type = 'SCRIPTED'
        var = driver.variables.new()
        var.name = "var"
        var.type = 'TRANSFORMS'
        target = var.targets[0]
        target.id = bpy.data.objects["FaceRig"]
        target.bone_target = bone.name
        target.transform_space = 'LOCAL_SPACE'
        if "_L" in shapekey or "_R" in shapekey:
            target.transform_type = 'LOC_X' 
        else:
            target.transform_type = 'LOC_Y' 
        if "_L" in shapekey or "_Up" in shapekey:
            driver.expression = "var / 0.1"
        else:
            driver.expression = "-var / 0.1"

keyblock = faceobj.data.shape_keys.key_blocks
            
shapekeyrename(keyblock)            
create_facerig_with_lim_bones(keyblock)
facestuff(faceobj)
mouthbone(keyblock)


def gdilycaon(): # Lycaon's mask has shapekeys. need to copy drivers.
    for shapekey in bpy.data.objects["Lycaon_Body_3"].data.shape_keys.key_blocks:
        if "_Body" in shapekey.name:
            shapekey.name = shapekey.name[:-5]
    facestuff(bpy.data.objects["Lycaon_Body_3"])    
    
try:
    gdilycaon()
except:
    pass

print("Face panel drivers done.\n")