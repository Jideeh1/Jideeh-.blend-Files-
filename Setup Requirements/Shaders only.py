### CREDITS:
### Rigging+Scripting: Enthralpy
### Shader: Just_ScaasI, BonnyAnimations, Aiko
### Supervised and made possible by Stormz67  

# INSTRUCTION
# Import using betterfbx
# Run this script
#
# NOTE: The rigging AND outline portions of this script have been removed.
# This version only imports/sets up the model and applies the ZZZ shaders
# (eye transparency, texture scan/load, shader-material assignment, light vectors).
# No Rigify rig, facerig, or outline geonodes are created.

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

# Use BetterFBX to load in the FBX of your ZZZ model.  Run this script and uh hopefully it works lmao. Also remember to change charname to the character's name.

charname = None

# If you want to manually rename the character (Some character names arent their actual ingame names), remove the hashtag in the next line and replace 'Burnice'
#charname = "Burnice "


def findpath():
    for img in bpy.data.images:
        if "_map" in img.name.lower() or "d.png" in img.name.lower():
            path = img.filepath.replace("\\","/")
            break
    splits = path.split("/")
#    if splits[-2] == "Textures":
#        newpath = "/".join(splits[0:-1])
#    else: # no Textures folder, imgs are in same folder as the fbx
#        newpath = "/".join(splits[0:-2])

    newpath = "/".join(splits[0:-1])  ## top 4 lines prove I'm a dumbass.
    return newpath.replace("\\", "/")

folder = findpath()
folder = bpy.path.abspath(folder)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.scale_clear(clear_delta=False)
bpy.ops.object.select_all(action='DESELECT')
 
# Thank you 2.3 for making this necessary, goddamn. 
for obj in bpy.data.objects:
    screwyou = bpy.data.objects.get("Bone_Root")
    if screwyou and screwyou.type == 'ARMATURE':
        for obj in bpy.data.objects:
            if obj.name.lower().endswith("yidhari_eyebrow"):
                obj.parent = screwyou
                obj.rotation_quaternion = (1,0,0,0)

for obj in bpy.data.objects:
    if obj.type == 'ARMATURE' and obj.name == "Bone_Root": # Usually the rig doesnt have an Empty as a parent. If it does, the rig name is fucked, need to fix.
            obj.parent.name += "A"
            obj.name = obj.parent.name[:-1]
            obj.data.name = obj.name # Armature data name and armature object name need to match            
            bpy.data.objects.remove(obj.parent, do_unlink=True) # Delete the parent
            obj.rotation_quaternion = (1,0,0,0) # Reset the rotation 

    #fuckyou orphie, this is to fix orphie weird bone swap
    A=bpy.context.object
    if A and A.type=='ARMATURE' and A.name=="Avatar_Female_Size02_Brujas_UI":
        b=[("Bip001 R Toe0","Skn_R_Shoelace_New_03"),
        ("Bip001 L Toe0","Skn_L_Shoelace_New_03"),
        ("Bip001 R Foot","Skn_R_Shoelace_New_01"),
        ("Bip001 L Foot","Skn_L_Shoelace_New_01")]
        bpy.ops.object.mode_set(mode='EDIT')
        for a,c in b:
            x,y=A.data.edit_bones.get(a),A.data.edit_bones.get(c)
            if x and y:x.name="TMP";y.name=a;A.data.edit_bones["TMP"].name=c 

for obj in bpy.data.objects:
    if "_face" in obj.name.lower() and "weapon_" not in obj.name.lower() and "gun_" not in obj.name.lower(): # gdi orphie
        faceobj = obj
    if obj.type == 'ARMATURE' and 'Lighting' not in obj.name and 'Eye' not in obj.name:
        arm = obj
        if charname is None: # If youre not manually renaming.
            charname = arm.name.split("_")[-1] + " "
            if charname == "UI ":
                charname = arm.name.split("_")[-2] + " "
            if charname == "Model ":
                charname = arm.name.split("_")[-2] + " "
                
    if "HairShadow" in obj.name:
#        bpy.data.objects.remove(obj, do_unlink=True)
        obj.hide_viewport = True
        obj.hide_render = True
    if "FX" in obj.name:
        obj.hide_viewport = True
        obj.hide_render = True
    if obj.type == 'EMPTY' and "Head " not in obj.name and "Light " not in obj.name and obj.users_collection[0].name != "LP wgt" and obj.parent != bpy.data.objects["Lighting Panel"]:
        bpy.data.objects.remove(obj, do_unlink=True) # this only works for empties; otherwise youd have to also delete object data, which empties dont have
arm.show_in_front = True



################################### SHADER SECTION ###############################

print("\n\ntEST")
###### FIX EYE SHADOW ###### 
def fixeyeshadow():
    bpy.context.view_layer.objects.active = faceobj
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = faceobj
    faceobj.select_set(True)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='DESELECT')
    
    matlen = len(faceobj.material_slots)
#    if matlen == 2:
    count = 0
    for obj in bpy.data.objects:
        if "NPC" in obj.name:
            return
    for mat in faceobj.material_slots:
        if "_eye" in mat.name.lower() and "brows" not in mat.name.lower():
            faceobj.active_material_index = count
        if "_Ben_" in mat.name or "PanYinhu" in mat.name: ### OR YINHU
            return
        count += 1
#    faceobj.active_material_index = 1
    bpy.ops.object.material_slot_select() # Select all verts in eye mat

    # deselect Eye_R and Eye_L verts.  why are there like 3 diff eye names.
    
    for vg in ['Eye_R','Skn_R_Eye','Skn_R_Pupil','Bdy_R_Eye', 'Skn_Bn_Eye_R', 'Bn_Eye_R', 'Skn_R_Highlights', 'EYE_R']:
        try:
            bpy.ops.object.vertex_group_set_active(group=vg)
            bpy.ops.object.vertex_group_deselect()  # Putting this here bc new models have Highhlights VG with eye VG
        except:
            pass

    for vg in ['Eye_L','Skn_L_Eye','Skn_L_Pupil','Bdy_L_Eye', 'Skn_Bn_Eye_L', 'Bn_Eye_L', 'Skn_L_Highlights', 'EYE_L']:
        try:
            bpy.ops.object.vertex_group_set_active(group=vg)
            bpy.ops.object.vertex_group_deselect()
        except:
            pass             
    
    
    bpy.ops.object.vertex_group_deselect()
    bpy.ops.mesh.hide(unselected=True)
    bpy.ops.object.material_slot_add()
    bpy.context.object.material_slots[-1].material = bpy.data.materials["Eye Transparent"]
    bpy.ops.object.material_slot_assign()
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all( action = 'DESELECT' )
    bpy.ops.object.mode_set(mode='OBJECT')
    
    
import os
### SCAN FOR IMAGES ###
def scan(folder):
    dick = {}
    bodyparts = ["Body_1", "Body_2", "Face", "Weapon", "Weapon_2", "Hair", "Leg", "Body_3", "Tail"]
    ### Note: Body_Map1, Body_Map2, Weapon_A, Weapon_2_A. annoying af.        
    for body in bodyparts:
        dick[body] = []
        
    for obj in bpy.data.objects: #to fix ye shunguang hair anomaly
        if obj.type == 'MESH':
            for slot in obj.material_slots:
                if slot.material and slot.material.name == "MAT_Zhenzhen_Hair_T_UI":
                    slot.material = bpy.data.materials.get("MAT_Zhenzhen_Hair_UI")
        
    for filename in os.listdir(folder): # goddamn wtf is up with these two characters
        if "Astra_Chandelier_Map1_D" in filename:
            bpy.data.images["Astra_Chandelier_Map1_D.png"].name = "Astra_Body_Map1_D.png"
            replacement = folder + "/" + filename.replace("Chandelier", "Body")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
        elif "Astra_Chandelier" in filename:
            replacement = folder + "/" + filename.replace("Chandelier", "Body")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
        if "Norano_WhiteHeart_Map1_D" in filename:
            bpy.data.images["Norano_WhiteHeart_Map1_D.png"].name = "Norano_Body_Map1_D.png"
            replacement = folder + "/" + filename.replace("Norano_WhiteHeart_Map1_D", "Norano_Body_Map1_D")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
        elif "Norano_WhiteHeart_Map2_D" in filename:
            bpy.data.images["Norano_WhiteHeart_Map2_D.png"].name = "Norano_Body_Map2_D.png"
            replacement = folder + "/" + filename.replace("Norano_WhiteHeart_Map2_D", "Norano_Body_Map2_D")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
        elif "Norano_WhiteHeart" in filename:
            replacement = folder + "/" + filename.replace("Norano_WhiteHeart_Map", "Norano_Body_Map")
            filename = folder + "/" + filename
            os.rename(filename, replacement)

        if "Clara_Map1_D" in filename:
            bpy.data.images["Clara_Map1_D.png"].name = "Clara_Body_Map1_D.png"
            replacement = folder + "/" + filename.replace("Clara_Map1_D", "Clara_Body_Map1_D")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
        elif "Clara_Map2_D" in filename:
            bpy.data.images["Clara_Map2_D.png"].name = "Clara_Body_Map2_D.png"
            replacement = folder + "/" + filename.replace("Clara_Map2_D", "Clara_Body_Map2_D")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
        elif "Clara_Map" in filename:
            replacement = folder + "/" + filename.replace("Clara_Map", "Clara_Body_Map")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
        if "Alice_Swimwear_Weanpon" in filename:
            bpy.data.images["Alice_Swimwear_Weanpon_Map1_D.png"].name = "Alice_Swimwear_Weapon_Map1_D.png"
            replacement = folder + "/" + filename.replace("Alice_Swimwear_Weanpon", "Alice_Swimwear_Weapon")
            filename = folder + "/" + filename
            os.rename(filename, replacement)
            
    for img in bpy.data.images: #to fix the setup for the 2nd time
        if "Chandelier" in img.name:
            new_name = img.name.replace("Chandelier", "Body")
            img.name = new_name
            img.filepath = folder + "/" + "Astra_Body_Map1_D.png"
            img.reload()
            replaced = True
        if "Clara_Map1_D.png" in img.name:
            bpy.data.images["Clara_Map1_D.png"].name = "Clara_Body_Map1_D.png"
            img.filepath = folder + "/" + "Clara_Body_Map1_D.png"
            img.reload()
            replaced = True
        if "Clara_Map2_D.png" in img.name:
            bpy.data.images["Clara_Map2_D.png"].name = "Clara_Body_Map2_D.png"
            img.filepath = folder + "/" + "Clara_Body_Map2_D.png"
            img.reload()
            replaced = True
        if "Norano_WhiteHeart_Map1_D.png" in img.name:
            bpy.data.images["Norano_WhiteHeart_Map1_D.png"].name = "Norano_Body_Map1_D.png"
            img.filepath = folder + "/" + "Norano_Body_Map1_D.png"
            img.reload()
            replaced = True
        if "Norano_WhiteHeart_Map2_D.png" in img.name:
            bpy.data.images["Norano_WhiteHeart_Map2_D.png"].name = "Norano_Body_Map2_D.png"
            img.filepath = folder + "/" + "Norano_Body_Map2_D.png"
            img.reload()
            replaced = True
        if "Alice_Swimwear_Weanpon_Map1_D.png" in img.name:
            new_name = img.name.replace("Alice_Swimwear_Weanpon_Map1_D.png", "Alice_Swimwear_Weapon_Map1_D.png")
            img.name = new_name
            img.filepath = folder + "/" + "Alice_Swimwear_Weapon_Map1_D.png"
            img.reload()
            replaced = True
                    
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if (filename[-15:-10] + filename[-7:-6]) == "Body_1" or (filename[-10:-5] + filename[-4:]) == "Body_.png" or (filename[-12:-5] + filename[-4:]) == "Body_1_.png": 
            dick["Body_1"].append(filename)
        elif (filename[-15:-10] + filename[-7:-6]) == "Body_2" or (filename[-12:-5] + filename[-4:]) == "Body_2_.png":
            dick["Body_2"].append(filename)
        elif "Weapon_2" in filename:
            dick["Weapon_2"].append(filename)
        elif "weapon" in filename.lower():
            dick["Weapon"].append(filename)
        elif "Face" in filename:
            dick["Face"].append(filename)
        elif "Hair" in filename:
            dick["Hair"].append(filename)
        elif "Leg" in filename:
            dick["Leg"].append(filename)  
        elif "Tail" in filename:
            dick["Tail"].append(filename)    
        elif (filename[-15:-10] + filename[-7:-6]) == "Body_3" or (filename[-12:-5] + filename[-4:]) == "Body_3_.png":
            dick["Body_3"].append(filename)    
            print("A\n\n")
    for k in dick:
        print(k, dick[k])
            
    return dick
        
def assignmats(mats, outs):
    for mat in bpy.data.materials:
        if "Outlines" in mat.name:
            outs.append(mat)
        elif "Shader" in mat.name:
            mats.append(mat)
            
def assignshader(arm):
    body2 = False
    for obj in arm.children:
        if "Body_2" in obj.name and "NuoCha" not in obj.name: # gfdi nicole
            body2 = True
        
            
    for obj in arm.children:
        mats = obj.data.materials
        for x in range(0, len(obj.data.materials)):
            mat = mats[x]
            if "Body_1" in mat.name or "Clara_Map1" in mat.name or (body2 == False and "Body" in mat.name and "_2" not in mat.name):
                mats[x] = bpy.data.materials["ZZZ Shader Body"]
                imgnode(mats[x], "Body_1")
    
            elif "Body_2" in mat.name or "Clara_Map2" in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Body 2"]
                imgnode(mats[x], "Body_2")
                
            elif "Hair_T_" in mat.name or mat.name.endswith("Hair_T"): # this bitch can be either body_1 or body_2 or smthng
                imgname = mat.node_tree.nodes["Image Texture"].image.name
                checks = ["body_map1", "body_d", "body_1_d"]
                body1 = False
                for check in checks:
                    if check in imgname.lower():
                        mats[x] = bpy.data.materials["ZZZ Shader Body"]
                        imgnode(mats[x], "Body_1")
                        body1 = True
                        break
                if not body1:
                    mats[x] = bpy.data.materials["ZZZ Shader Body 2"]
                    imgnode(mats[x], "Body_2")
            
            elif "Body_3" in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Body3/Leg"]
                imgnode(mats[x], "Body_3")
                
            elif "Face" in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Face"]
                imgnode(mats[x], "Face")
            elif "Eye" in mat.name and mat.name != "Eye Transparent":
#                mats[x] = bpy.data.materials["ZZZ Shader Eye"]
                mats[x] = bpy.data.materials["ZZZ Shader Face"]
                imgnode(mats[x], "Face")
                
            elif "Hair" in mat.name and "Shadow" not in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Hair"]
                imgnode(mats[x], "Hair")
                
            elif "Leg" in mat.name and "Shadow" not in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Body3/Leg"]
                imgnode(mats[x], "Leg")    
            elif "Tail" in mat.name: # I hope no character ever has tail, leg, and body3 all at once lmao.
                mats[x] = bpy.data.materials["ZZZ Shader Body3/Leg"] 
                imgnode(mats[x], "Tail")    
                
            elif "Weapon_" in mat.name or "_Weapon" in mat.name:
                mats[x] = bpy.data.materials["ZZZ Shader Weapon"]
                imgnode(mats[x], "Weapon")
            elif "Weapon_2" in mat.name: # Mat names are Weapon_ and Weapon_2
                try:
                    mats[x] = bpy.data.materials["ZZZ Shader Weapon 2"]
                except:
                    newmat = bpy.data.materials["ZZZ Shader Weapon"]
                    mats[x] = newmat.copy()
                    mats[x].name = "ZZZ Shader Weapon 2"
                imgnode(mats[x], "Weapon_2")
                
def imgnode(mat, name):
    nodes = mat.node_tree.nodes
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            type = node.name[-1] + ".png" # D.png, A.png, etc
            for f in files[name]:
                if f.endswith("D.png") and node.name.endswith("_D"): # dumbass u forgot this already gets imported
                    node.image = bpy.data.images[f]
                    node.image.alpha_mode = 'CHANNEL_PACKED'
#                    print(mat.name, name, node.image)

                elif f.endswith(type):
                    img = bpy.data.images.load(folder + "/" + f)
                    node.image = img
                    node.image.colorspace_settings.name = 'Non-Color'
                    node.image.alpha_mode = 'CHANNEL_PACKED'
                    
                elif "face" in f.lower() and "lightmap" in f.lower(): # face lightmap
                    lnode = bpy.data.node_groups["Face Lightmap"].nodes["Face_Lightmap"]
                    img = bpy.data.images.load(folder + "/" + f)
                    lnode.image = img
                    lnode.image.colorspace_settings.name = 'Non-Color'
                    lnode.image.alpha_mode = 'CHANNEL_PACKED'
#            print(node.name, node.image.name, sep=": ")
#                    pass
            
    
files = scan(folder)

def addlightvec():
    for obj in arm.children:
        mod = obj.modifiers.new(type="NODES",name="Light Vectors")
        mod.node_group = bpy.data.node_groups["Light Vectors"]
        mod["Input_3"] = bpy.data.objects["Light Direction"]
        mod["Input_4"] = bpy.data.objects["Head Direction"]
        mod["Input_5"] = bpy.data.objects["Head Forward"]
        mod["Input_6"] = bpy.data.objects["Head Up"]
        
        obs = bpy.data.objects
        mod["Socket_0"] = obs["ColorWheel-Ambient"]
        mod["Socket_1"] = obs["ColorPicker-Ambient"]
        mod["Socket_2"] = obs["ColorWheel-Lit"]
        mod["Socket_3"] = obs["ColorPicker-Lit"]
        mod["Socket_4"] = obs["ColorWheel-Shadow"]
        mod["Socket_5"] = obs["ColorPicker-Shadow"]
        mod["Socket_6"] = obs["ColorWheel-RimLit"]
        mod["Socket_7"] = obs["ColorPicker-RimLit"]
        mod["Socket_8"] = obs["ColorWheel-RimShadow"]
        mod["Socket_9"] = obs["ColorPicker-RimShadow"]
        mod["Socket_26"] = obs["Origin-RimX"]
        mod["Socket_27"] = obs["Slider-RimX"]
        mod["Socket_28"] = obs["Origin-RimY"]
        mod["Socket_29"] = obs["Slider-RimY"]

fixeyeshadow()
mats = []
outs = []
assignmats(mats, outs)
assignshader(arm)
addlightvec()


#################################### CLEANUP ###############################
# Shader-helper housekeeping: remove the shader source data once it's been assigned.

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
obj = bpy.data.objects.get("Shader Materials (delete later)")
if obj:
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.delete()
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)