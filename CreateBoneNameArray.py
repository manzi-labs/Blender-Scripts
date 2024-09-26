import bpy

# Ensure the armature is selected and in object mode
if bpy.context.object and bpy.context.object.type == 'ARMATURE':
    armature = bpy.context.object.data
    bones = armature.bones

    bone_names = [f'"{bone.name}"' for bone in bones]

    print("Bone names in array format: \n")
    print("[", ", ".join(bone_names), "]")
else:
    print("Please select an armature.")
