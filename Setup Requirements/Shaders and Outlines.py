### CREDITS:
### Rigging+Scripting: Enthralpy
### Shader: Just_ScaasI, BonnyAnimations, Aiko
### Supervised and made possible by Stormz67  

# INSTRUCTION
# Import using betterfbx
# Run this script
#
# ### NO-RIG VARIANT ###
# The Rigify/Expykit armature generation has been removed. This does shader,
# geonodes and outlines only, and leaves the model on its original game armature.
# You do NOT need the Rigify or Expykit addons enabled to run this.
# Since there is no rig: no facerig, no eye control bone, no eye-shrink shapekeys,
# and no FaceShadow X-Y bone (adjust face shadow offset by hand in the
# "Face Shader" node group, nodes Math.004 / Math.008, if you need to).

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


#################################### GEONODE SECTION ###############################


def add_driver(source, target, path, dataPath):
    d = source.driver_add( path).driver
    v = d.variables.new()
    d.type = "AVERAGE"
    v.name                 = "Input_7"
    v.targets[0].id        = target
    v.targets[0].data_path = dataPath
    
def modassign(mod):
        mod['Input_3_use_attribute'] = 0
        mod["Input_12"] = True
        mod["Input_13"] = True
        mod["Input_10"] = bpy.data.materials["ZZZ Shader Hair"]
        mod["Input_5"] = bpy.data.materials["ZZZ Hair Outlines"]
        mod["Input_11"] = bpy.data.materials["ZZZ Shader Body"]
        mod["Input_9"] = bpy.data.materials["ZZZ Body Outlines"]
        mod["Input_14"] = bpy.data.materials["ZZZ Shader Body 2"]
        mod["Input_15"] = bpy.data.materials["ZZZ Body 2 Outlines"]
        mod["Input_18"] = bpy.data.materials["ZZZ Shader Body"]
        mod["Input_19"] = bpy.data.materials["ZZZ Body Outlines"]
        mod["Input_24"] = bpy.data.materials["ZZZ Shader Weapon"]
        mod["Input_25"] = bpy.data.materials["ZZZ Weapon Outlines"]
        mod["Input_26"] = bpy.data.materials["ZZZ Shader Weapon"]
        mod["Input_27"] = bpy.data.materials["ZZZ Weapon Outlines"]
        mod["Socket_0"] = bpy.data.materials["ZZZ Shader Body3/Leg"]
        mod["Socket_1"] = bpy.data.materials["ZZZ Body3/Leg Outlines"]

def syncdriver(source, name, target, path): # Make drivers for cast shadow values to sync them across bodyparts
    d = source.driver_add(path).driver
    v = d.variables.new()
    d.type = "AVERAGE"
    v.name                 = name
    v.targets[0].id        = target
    v.targets[0].data_path = path
    
        

def geonode(arm):
    inputs = ["Input_10" , "Input_5" , "Input_11" , "Input_9" , "Input_14" , "Input_15" , "Input_18" , "Input_19" , "Input_24" , "Input_25" , "Input_26" , "Input_27", "Socket_0", "Socket_1"]
    grp = bpy.data.node_groups["ZZZ Outlines"]
    for obj in arm.children: # This is for finding the main body object to do driver stuff
        if "body_1" in obj.name.lower() or obj.name[-5:].lower() == "_body" or obj.name.endswith("Body1"):
            mod = obj.modifiers.new("Extra FX", "NODES")
            mod.node_group = bpy.data.node_groups["Extra FX Geonode"] # Assign extra fx geonode
            mod["Socket_0_attribute_name"] = "cast shadow" # order matters; fx geonode needs to be above outline.
            mod["Socket_11_attribute_name"] = "shadowsharpness"   

            bod = obj
            mod = obj.modifiers.new("Outlines", "NODES")
            mod.node_group = grp
            modassign(mod)
            break
        
    for ob in arm.children: # Assign outlines modifier to other meshes
        if "body_1" in ob.name.lower() or ob.name[-5:].lower() == "_body":
            pass # already did this. 
        else:
            mod = ob.modifiers.new("Extra FX", "NODES")
            mod.node_group = bpy.data.node_groups["Extra FX Geonode"] # Assign extra fx geonode
            mod["Socket_0_attribute_name"] = "cast shadow"
            mod["Socket_11_attribute_name"] = "shadowsharpness"   
#            mod["Output_3_attribute_name"] = "depth"
#            mod["Output_2_attribute_name"] = "blend"         

            if ob == obj: # ignore this body obj, already assigned
                continue
            if "face" in ob.name.lower(): ### Only face needs these geonode attributes
                mod["Output_3_attribute_name"] = "depth"
                mod["Output_2_attribute_name"] = "blend"
                mod["Socket_5_attribute_name"] = "face shadow"
                mod["Socket_6_attribute_name"] = "faceshadX"
                mod["Socket_7_attribute_name"] = "faceshadY"
                mod["Socket_9_attribute_name"] = "faceshadadjust"

                continue # Skip adding outline geonode to face; do it with Solidify manually.
            mod = ob.modifiers.new("Outlines", "NODES")
            mod.node_group = grp
            modassign(mod)
            add_driver(ob, bod, 'modifiers["Outlines"]["Input_7"]', 'modifiers["Outlines"]["Input_7"]')
            
    for ob in arm.children: # Cast shadow driver
        if ob == faceobj:
            pass
        else:
            syncdriver(ob, "Socket_1", faceobj, 'modifiers["Extra FX"]["Socket_1"]') # cast shadow
            syncdriver(ob, "Socket_10", faceobj, 'modifiers["Extra FX"]["Socket_10"]') # shadow sharpness
        
        
def findimg(name):
    for img in bpy.data.images:
        if img.name.endswith(name):
            return img
        
def outlineshader():
    mat = bpy.data.materials["ZZZ Body Outlines"]
    for mat in bpy.data.materials:
        if "Outlines" in mat.name: 
            nodes = mat.node_tree.nodes
            if "Body 2 Outlines" in mat.name and bpy.data.materials["ZZZ Shader Body 2"].node_tree.nodes["Body_D"].image != None: # Make sure body2 actually exists since youre checking every material
                nodes["Outline_Diffuse"].image = findimg("Body_Map2_D.png")
                nodes["Outline_Lightmap"].image = findimg("Body_Map2_M.png")
                
                if nodes["Outline_Diffuse"].image == None:
                    nodes["Outline_Diffuse"].image = findimg("Body_2_D.png")
                    nodes["Outline_Lightmap"].image = findimg("Body_2_M.png")
                    
                nodes["Outline_Diffuse"].image.alpha_mode = 'CHANNEL_PACKED'
                nodes["Outline_Lightmap"].image.colorspace_settings.name = 'Non-Color'
                nodes["Outline_Lightmap"].image.alpha_mode = 'CHANNEL_PACKED'
                
            elif "Body3/Leg Outlines" in mat.name and bpy.data.materials["ZZZ Shader Body3/Leg"].node_tree.nodes["Body_D"].image != None:
                nodes["Outline_Diffuse"].image = findimg("Body_Map3_D.png")
                nodes["Outline_Lightmap"].image = findimg("Body_Map3_M.png")
                
                if nodes["Outline_Diffuse"].image == None: # schoolEllen and hugo dont have 'map' in the name wtf.
                    nodes["Outline_Diffuse"].image = findimg("Body_3_D.png")
                    nodes["Outline_Lightmap"].image = findimg("Body_3_M.png")
                
                if nodes["Outline_Diffuse"].image == None: # this means it's leg, not body3.
                    nodes["Outline_Diffuse"].image = findimg("Leg_D.png")
                    nodes["Outline_Lightmap"].image = findimg("Leg_M.png")
                    
                if nodes["Outline_Diffuse"].image == None: # fuck you yidhari
                    nodes["Outline_Diffuse"].image = findimg("Tail_Map1_D.png")
                    nodes["Outline_Lightmap"].image = findimg("Tail_Map1_M.png")
                    
                nodes["Outline_Diffuse"].image.alpha_mode = 'CHANNEL_PACKED'
                nodes["Outline_Lightmap"].image.colorspace_settings.name = 'Non-Color'
                nodes["Outline_Lightmap"].image.alpha_mode = 'CHANNEL_PACKED'
                
            elif "Body Outlines" in mat.name:
                thisisstupid = ["Body_Map1_D.png", "Body_D.png", "Body_1_D.png", "Weapon_Map2_D.png"]
                for ugh in thisisstupid:
                    nodes["Outline_Diffuse"].image = findimg(ugh)
                    if nodes["Outline_Diffuse"].image != None:
                        break
                nodes["Outline_Diffuse"].image.alpha_mode = 'CHANNEL_PACKED'
                
                thisisstupid = ["Body_Map1_M.png", "Body_M.png", "Body_1_M.png", "Weapon_Map2_M.png"]
                for ugh in thisisstupid:
                    nodes["Outline_Lightmap"].image = findimg(ugh)
                    if nodes["Outline_Lightmap"].image != None:
                        break
                    
                nodes["Outline_Lightmap"].image.colorspace_settings.name = 'Non-Color'
                nodes["Outline_Lightmap"].image.alpha_mode = 'CHANNEL_PACKED'
                
            elif "Hair Outlines" in mat.name:
                if findimg("Hair_D.png") != None:
                    nodes["Outline_Diffuse"].image = findimg("Hair_D.png")
                    nodes["Outline_Diffuse"].image.alpha_mode = 'CHANNEL_PACKED'

                    nodes["Outline_Lightmap"].image = findimg("Hair_M.png")
                    nodes["Outline_Lightmap"].image.colorspace_settings.name = 'Non-Color'
                    nodes["Outline_Lightmap"].image.alpha_mode = 'CHANNEL_PACKED'
                
            elif "Weapon Outlines" in mat.name:
                thisisstupid = ["Weapon_D.png", "Weapon_01_D.png", "Weapon_Map1_D.png", "Weapon_Map2_D.png", "weapon_Map_D.png"]
                for ugh in thisisstupid:
                    nodes["Outline_Diffuse"].image = findimg(ugh)
                    if nodes["Outline_Diffuse"].image != None:
                        break
                if nodes["Outline_Diffuse"].image != None:
                    nodes["Outline_Diffuse"].image.alpha_mode = 'CHANNEL_PACKED'
                    
                    thisisstupid = ["Weapon_M.png", "Weapon_01_M.png", "Weapon_Map1_M.png", "Weapon_Map2_M.png", "weapon_Map_M.png"]
                    for ugh in thisisstupid:
                        nodes["Outline_Lightmap"].image = findimg(ugh)
                        print(ugh, findimg(ugh))
                        if nodes["Outline_Lightmap"].image != None:
                            break
                        
                    nodes["Outline_Lightmap"].image.colorspace_settings.name = 'Non-Color'
                    nodes["Outline_Lightmap"].image.alpha_mode = 'CHANNEL_PACKED'
            elif "Face Outline" in mat.name:
                nodes["Face_D"].image = bpy.data.materials["ZZZ Shader Face"].node_tree.nodes["Face_D"].image
                
geonode(arm)
outlineshader()


############### NO-RIG FINISHING SECTION ###############
# The original script's ARMATURE RIG SECTION (Rigify/Expykit metarig generation,
# facerig, eye control bones, FaceShadow X-Y bone) has been removed.
# Everything below is the shader/outline work that originally ran *after* the rig,
# rewritten to use the model's original armature (`arm`) instead of the Rigify rig.

print("\n\nNO-RIG MODE: skipping rigify, running shader + outline finishing\n\n")

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

######## LIGHT PANEL HOOKUP ########
# Originally the Lighting Panel armature was joined into the rigify rig and the
# "Head Direction" empty was childed to DEF-spine.006. Without a rig we point it
# at the original head bone so face shading still follows the head.

lightpanel = bpy.data.objects.get("Lighting Panel")

for oname in ["Head Up", "Head Forward"]:
    o = bpy.data.objects.get(oname)
    if o:
        o.hide_viewport = True

headdir = bpy.data.objects.get("Head Direction")
if headdir and "Child Of" in [c.name for c in headdir.constraints]:
    headbone = None
    for cand in ("Bip001 Head", "Head", "head", "Bip001 Neck"):
        if cand in arm.data.bones:
            headbone = cand
            break
    if headbone is None:
        for b in arm.data.bones:
            if "head" in b.name.lower():
                headbone = b.name
                break
    con = headdir.constraints["Child Of"]
    con.target = arm
    if headbone:
        con.subtarget = headbone
        bpy.context.view_layer.objects.active = headdir
        bpy.ops.constraint.childof_set_inverse(constraint="Child Of", owner='OBJECT')
    else:
        print("!! No head bone found; 'Head Direction' left unconstrained.")

# Colour wheel visibility drivers used to point at the joined rig's armature data.
# Point them at the Lighting Panel armature instead, since nothing gets joined now.
if lightpanel:
    for o in [o for o in bpy.data.objects if "ColorWheel-" in o.name]:
        try:
            drv = o.animation_data.drivers[0]
            drv.driver.variables[0].targets[0].id = lightpanel.data
            hidedrv = o.animation_data.drivers.find("hide_viewport")
            if ver == 3:
                hidedrv.driver.variables[0].targets[0].data_path = 'layers[0]'
            else:
                hidedrv.driver.variables[0].targets[0].data_path = 'collections["Light Panel"].is_visible'
        except Exception as e:
            print("ColorWheel driver skipped for", o.name, ":", e)

    if ver != 3:
        try:
            lightpanel.data.collections["Light Panel"].is_visible = True
            lightpanel.data.collections["Light Panel Extras"].is_visible = False
        except Exception as e:
            print("Light panel bone collections skipped:", e)


######## FACE MATERIAL / MODIFIER TIDY ########
try:
    bpy.data.materials["ZZZ Shader Face"].blend_method = 'CLIP'
except Exception as e:
    print("blend_method 'CLIP' not available in this Blender version:", e)

if len(faceobj.modifiers) > 2:
    faceobj.modifiers[2].name = """Extra FX (ALL EXCEPT LAST 2 IS FACE ONLY"""
    faceobj.modifiers[2].show_in_editmode = False


def eyehighlight():
    bpy.ops.object.mode_set(mode='OBJECT')
    faceobj.active_material_index = len(faceobj.data.materials)-1
    bpy.context.view_layer.objects.active = faceobj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    vertex_groups = ['SknHighlights.R', 'SknHighlights.L']
    for group_name in vertex_groups:
        bpy.ops.object.vertex_group_set_active(group=group_name)
        bpy.ops.object.vertex_group_select()
    for x in range(5):
        bpy.ops.mesh.select_more()
    bpy.ops.object.material_slot_assign()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.materials["ZZZ Shader EyeHighlights"].node_tree.nodes["Face_D"].image = bpy.data.materials["ZZZ Shader Face"].node_tree.nodes["Face_D"].image


# Join the separate eyebrow mesh into the face mesh
eyebrowobj = None
for obj in arm.children:
    if obj.name.lower().endswith("_eyebrow"):
        eyebrowobj = obj

if eyebrowobj is not None:
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = faceobj
    eyebrowobj.select_set(True)
    faceobj.select_set(True)
    bpy.ops.object.join()

# NOTE: the original script renamed the eyebrow vertex groups to SknHighlights.L/.R
# during the rig section. Without the rig those groups keep their raw names, so
# check for both.
hlgroups = [g for g in ("SknHighlights.R", "SknHighlights.L",
                        "Skn_R_Highlights", "Skn_L_Highlights")
            if g in faceobj.vertex_groups]

if hlgroups:
    faceobj.data.materials.append(bpy.data.materials['ZZZ Shader EyeHighlights'])
    try:
        if "SknHighlights.R" in faceobj.vertex_groups:
            eyehighlight()
        else:
            # same routine, raw vertex group names
            bpy.ops.object.mode_set(mode='OBJECT')
            faceobj.active_material_index = len(faceobj.data.materials)-1
            bpy.context.view_layer.objects.active = faceobj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            for group_name in hlgroups:
                bpy.ops.object.vertex_group_set_active(group=group_name)
                bpy.ops.object.vertex_group_select()
            for x in range(5):
                bpy.ops.mesh.select_more()
            bpy.ops.object.material_slot_assign()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.data.materials["ZZZ Shader EyeHighlights"].node_tree.nodes["Face_D"].image = bpy.data.materials["ZZZ Shader Face"].node_tree.nodes["Face_D"].image
    except Exception as e:
        print("Eye highlight assign skipped:", e)


######## FACE OUTLINES (SOLIDIFY) ########
bpy.ops.object.mode_set(mode='OBJECT')
for a in bpy.data.objects:
    if a.type == 'MESH' and a.name.lower().endswith('_face') and "weapon_" not in a.name.lower() and "gun_" not in a.name.lower():
        obj = a

obj.vertex_groups.new(name="No OL")

mod = obj.modifiers.new("Outlines", "SOLIDIFY")
mod.offset = 1
mod.thickness = 0.001
mod.use_flip_normals = True
mod.material_offset = 1
mod.vertex_group = "No OL"
mod.invert_vertex_group = True
mod.use_rim = False

bod = None
for x in arm.children:  # Find the main body object to hang outline viewport drivers off
    if "body_1" in x.name.lower() or x.name[-5:].lower() == "_body" or x.name.endswith("Body1"):
        bod = x

if bod is not None:
    for x in arm.children:
        if x == bod:
            continue
        try:
            if x.modifiers[2].name == "Outlines":
                add_driver(x, bod, 'modifiers["Outlines"].show_viewport', 'modifiers["Outlines"].show_viewport')
            elif x.modifiers[3].name == "Outlines":  # The face
                add_driver(x, bod, 'modifiers["Outlines"].show_viewport', 'modifiers["Outlines"].show_viewport')
        except:
            pass

bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

mats = obj.data.materials
origlen = len(mats)
# Traverse each mat, decide what type of outline to use.

for i in range(origlen):
    bpy.ops.object.material_slot_add()

for i in range(origlen*2-2, 0, -2):
    for b in range(0, i):
        bpy.ops.object.material_slot_move(direction='UP')
    obj.active_material_index = len(obj.data.materials)-1

for i in range(0, len(obj.data.materials)-1, 2):
    mat = obj.data.materials[i]
    hohoho = None
    if mat.name == "ZZZ Shader Face":
        hohoho = bpy.data.materials["ZZZ Face Outlines"]
    elif mat.name == "ZZZ Shader EyeHighlights" or mat.name == "Eye Transparent":
        hohoho = bpy.data.materials["Transp OL"]
    obj.data.materials[i+1] = hohoho


######## RENAME + CLEANUP ########
for oname in ["Lighting Panel", "Head Direction", "Light Direction", "Head Up", "Head Forward"]:
    o = bpy.data.objects.get(oname)
    if o:
        o.name = charname + oname

try:
    arm.users_collection[0].name = charname[:-1]
except Exception as e:
    print("Collection rename skipped:", e)

for o in bpy.data.objects:
    if "metarig" in o.name:
        o.hide_viewport = True
        o.hide_render = True

bpy.ops.object.select_all(action='DESELECT')
obj = bpy.data.objects.get("Shader Materials (delete later)")
if obj:
    obj.select_set(True)
    bpy.ops.object.delete()
bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

print("\n\nDone: shader + outlines applied, no rig generated.\n\n")