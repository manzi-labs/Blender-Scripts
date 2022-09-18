import bpy


i = 0
j=1
x=0

objects = bpy.context.scene.objects

while i < len(objects):
    bpy.ops.object.select_all(action='DESELECT')
    
    if(j==2):
        i+=1
        j=0
    
    print(objects[i].name+" - Deleted")
    bpy.data.objects[i].select_set(True)
    bpy.ops.object.delete()
    x+=1
    i+=1
    j+=1

print("Complete - "+str(x)+" Items Deleted")
