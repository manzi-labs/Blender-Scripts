import bpy
import mathutils

# Configuration
bones_to_remove = [ 
    "Hips", "Spine", "Chest", "Upper Chest", "Breast_L", "J_Sec_L_Bust2", "Breast_R", "J_Sec_R_Bust2", 
    "Left shoulder", "Left arm", "Left elbow", "Left wrist", 
    "IndexFinger1_L", "IndexFinger2_L", "IndexFinger3_L", "LittleFinger1_L", "LittleFinger2_L", "LittleFinger3_L", 
    "MiddleFinger1_L", "MiddleFinger2_L", "MiddleFinger3_L", "RingFinger1_L", "RingFinger2_L", "RingFinger3_L", 
    "Thumb0_L", "Thumb1_L", "Thumb2_L", "Right shoulder", "Right arm", "Right elbow", "Right wrist", "IndexFinger1_R", 
    "IndexFinger2_R", "IndexFinger3_R", "LittleFinger1_R", "LittleFinger2_R", "LittleFinger3_R", "MiddleFinger1_R", 
    "MiddleFinger2_R", "MiddleFinger3_R", "RingFinger1_R", "RingFinger2_R", "RingFinger3_R", "Thumb0_R", "Thumb1_R", 
    "Thumb2_R", "Left leg", "Left knee", "Left ankle", "Left toe", "Right leg", "Right knee", "Right ankle", 
    "Right toe" ]
    
bone_to_make_root = "Neck"
bone_for_origin = "Head"
target_meshes = ["Body", "Hair"]

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

        # Calculate the translation required to move the Head bone to (0, 0, 0)
        if bone_for_origin in armature.edit_bones:
            head_bone = armature.edit_bones[bone_for_origin]
            offset = -head_bone.head.copy()  # Get the translation vector to move to origin

            # Move the entire bone hierarchy under the Neck bone by the offset
            for bone in armature.edit_bones:
                if bone == root_bone or root_bone in bone.parent_recursive:
                    bone.translate(offset)

            # Switch to Object mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Also move the face mesh by the same offset
            for child in obj.children:
                if child.type == 'MESH' and child.name not in target_meshes:
                    # Move the face mesh by the same offset
                    child.location += offset
                    print(f"Moved {child.name} by {offset}")

            # Set the origin of the entire object (armature) to the new Head position (which is now at (0, 0, 0))
            bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

            print(f"Moved object and set origin at (0, 0, 0).")

            # Ensure all transforms are applied directly, not just as deltas
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

else:
    print("Please select an armature in object mode.")
