import bpy

# Configuration
bones_to_remove = [
    "Root", "J_Bip_C_Hips", "J_Bip_C_Spine", "J_Bip_C_Chest", "J_Bip_C_UpperChest", 
    "J_Sec_L_Bust1", "J_Sec_L_Bust2", "J_Sec_R_Bust1", "J_Sec_R_Bust2", "J_Bip_C_Neck", 
    "J_Adj_L_FaceEye", "J_Adj_R_FaceEye", "J_Bip_L_Shoulder", "J_Bip_L_UpperArm", 
    "J_Bip_L_LowerArm", "J_Bip_L_Hand", "J_Bip_L_Index1", "J_Bip_L_Index2", "J_Bip_L_Index3", 
    "J_Bip_L_Little1", "J_Bip_L_Little2", "J_Bip_L_Little3", "J_Bip_L_Middle1", "J_Bip_L_Middle2", 
    "J_Bip_L_Middle3", "J_Bip_L_Ring1", "J_Bip_L_Ring2", "J_Bip_L_Ring3", "J_Bip_L_Thumb1", 
    "J_Bip_L_Thumb2", "J_Bip_L_Thumb3", "J_Bip_R_Shoulder", "J_Bip_R_UpperArm", "J_Bip_R_LowerArm", 
    "J_Bip_R_Hand", "J_Bip_R_Index1", "J_Bip_R_Index2", "J_Bip_R_Index3", "J_Bip_R_Little1", 
    "J_Bip_R_Little2", "J_Bip_R_Little3", "J_Bip_R_Middle1", "J_Bip_R_Middle2", "J_Bip_R_Middle3", 
    "J_Bip_R_Ring1", "J_Bip_R_Ring2", "J_Bip_R_Ring3", "J_Bip_R_Thumb1", "J_Bip_R_Thumb2", 
    "J_Bip_R_Thumb3", "J_Bip_L_UpperLeg", "J_Bip_L_LowerLeg", "J_Bip_L_Foot", "J_Bip_L_ToeBase", 
    "J_Bip_R_UpperLeg", "J_Bip_R_LowerLeg", "J_Bip_R_Foot", "J_Bip_R_ToeBase"
]
bone_to_make_root = "J_Bip_C_Head"
target_meshes = ["Body", "Face"]

# Get the active object
obj = bpy.context.object

# Check if object is selected
if obj is None:
    print("No object selected.")
else:
    # Remove meshes related to 'Body' and 'Face'
    for mesh in obj.children:
        if mesh.name == 'secondary':
            bpy.data.objects.remove(mesh, do_unlink=True)
            
        elif mesh.type == 'MESH' and any(target in mesh.name for target in target_meshes):
            print(f"Removing mesh: {mesh.name}")
            bpy.data.objects.remove(mesh, do_unlink=True)

# Ensure an armature is selected and is in object mode
if obj and obj.type == 'ARMATURE':
    armature = obj.data
    
    # Switch to Edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Remove bones listed in bones_to_remove
    for bone_name in bones_to_remove:
        if bone_name in armature.edit_bones:
            bone = armature.edit_bones[bone_name]
            armature.edit_bones.remove(bone)
            print(f"Removed bone: {bone_name}")

    # Set the new root bone by clearing its parent
    if bone_to_make_root in armature.edit_bones:
        root_bone = armature.edit_bones[bone_to_make_root]
        root_bone.parent = None
        print(f"Made '{bone_to_make_root}' the root bone.")

    # Switch back to Object mode
    bpy.ops.object.mode_set(mode='OBJECT')
else:
    print("Please select an armature in object mode.")
