bl_info = {
    "name": "Squeak Bake",
    "author": "Cristian Moga",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Speaker Data > SqeakBake",
    "description": "Tool to bake SFX in Speaker Object relative to the rotation of an object",
    "warning": "on heavy scenes it is slow",
    "doc_url": "https://www.youtube.com/c/CristianMoga",
    "category": "Animation",
}

# __________hope you enjoy this ADON


import bpy
from bpy.props import PointerProperty
import time

# do something...



#_________________the operations

def sq_clear_bake (context):
    sqspeaker = context.object
    
    Squeaktool = context.scene.Squeak_tool
    SQ_label =  Squeaktool.Squeak_name   
    en = context.scene.frame_end

    #deselect other objects NLA tracks
    for ob in context.scene.objects:
        numele = ob
        jj = ob.animation_data
        if jj :
            for ggg in jj.nla_tracks: 
                ggg.select = False
   
    
    #change the position of the original SoundTrack
    gogu = sqspeaker.animation_data.nla_tracks["SoundTrack"].strips["NLA Strip"]
    gogu.select = True
    frdiff= gogu.frame_end - gogu.frame_start
    gogu.frame_end = en + frdiff
    gogu.frame_start = en
    gogu.select = False
    #remove the other traks with the same name
    for t in sqspeaker.animation_data.nla_tracks:
        if t.name == SQ_label:
            t.select=True
            bpy.ops.nla.apply_scale()
            sqspeaker.animation_data.nla_tracks.remove(t)
    #deselect the SoundTrack
    gogu.select = False


def sqeak_track (context):
        
       
    sqspeaker = context.object
    Squeaktool = context.scene.Squeak_tool
    SQ_label =  Squeaktool.Squeak_name
    
    
    
    #for tott in sqspeaker.animation_data.nla_tracks:
    #    tott.select=False
        # add a track the usual way
    tott = sqspeaker.animation_data.nla_tracks.new()
    tott.name = SQ_label
    bpy.ops.nla.soundclip_add(context.copy())
    tott.select=False        
        


#__________Operator define_________________

class SqueakBake(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.squeak_bake"
    bl_label = "Bake Squeak"
    bl_info = "start the bake"
    bl_options = {'REGISTER' , 'UNDO'}
   

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'SPEAKER' and context.scene.prop  is not None
        
    
    
        

    def execute(self, context):
        #self.report({'INFO'}, "Its Baking!")
        
        sqspeaker = context.object
        
        time_start = time.time()
        context = bpy.context
        st = context.scene.frame_start
        en = context.scene.frame_end
        Squeaktool = context.scene.Squeak_tool
        
        
        
    
        #____________________properties Set______________
        
        objectToCheck = context.scene.prop

        if Squeaktool.axis_enum == 'OP1':
            rolaxis = int(0) 
        if Squeaktool.axis_enum == 'OP2':
            rolaxis = int(1)
        if Squeaktool.axis_enum == 'OP3':
            rolaxis = int(2)


        
        rotations = []
        sta=True
        scade=True
        creste=True
        uitypesqueak = context.area.ui_type 
        context.area.ui_type = 'NLA_EDITOR'
        
        context.scene.frame_set(st-2)
        rotations.append(objectToCheck.rotation_euler[rolaxis])
        context.scene.frame_set(st-1)
        rotations.append(objectToCheck.rotation_euler[rolaxis])
        
        if sqspeaker :
            sq_clear_bake (context)
            for i,x in enumerate(range(st,en)):
                context.scene.frame_set(x)
                rotations.append(objectToCheck.rotation_euler[rolaxis])
                
                ante= rotations[i-1] 
                post= rotations[i]
              
                

                  
                if ante == post:
                    #print ("Charging")  
                    sta = True
                else:
                    if sta == True :
                        sqeak_track(context)
                    sta = False
                    
                if ante > post:
                    #print ("Charging")  
                    scade = True
                else:
                    if scade == True  and sta == False:
                        sqeak_track(context)
                    scade = False
                    
                if ante < post:
                    #print ("Charging")  
                    creste = True
                else:
                    if creste == True and sta==False:
                        sqeak_track(context)
                    creste = False
            
                           
            
                
                
            #print ("deformation on frame")
            #print (i)
            
           
        #______________________________________________________________________   
            
          
        bpy.context.area.ui_type = uitypesqueak 
        print("done")
        print("SqueakBake has Finished: %.4f sec" % (time.time() - time_start))
       
        self.report({'INFO'}, "It Squeaks now!")
        return {'FINISHED'}



#_____________Properties input____________________


class SqueakProperties(bpy.types.PropertyGroup):
    
    Squeak_name : bpy.props.StringProperty(name= "NLA track", default="Squeak", description="the name of the NLA tracks")
    
    axis_enum : bpy.props.EnumProperty(
        name= "Axis",
        description= "The axis that will be monitored",
        items= [('OP1', "X", ""),
                ('OP2', "Y", ""),
                ('OP3', "Z", "")
        ]
    )


#_______________LAYOUT__________________


class SQ_PT_BK(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Squeak Bake"
    bl_idname = "SQ_PT_BK"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    bl_category = "Squeak Bake"
    
    @classmethod 
    def poll(cls, context):
        return context.speaker is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        Squeaktool = scene.Squeak_tool
        
        # Frames
        #layout.label(text="Change the scene start/end frame")
        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")
        #layout.label(text="")
        #NLA Track name
        #layout.label(text="    Set the name for the NLA Tracks", icon='PLAY_SOUND')
        layout.prop(Squeaktool, "Squeak_name", icon='NLA')
 

        #layout.label(text="")
        #Object to be monitored 
        #layout.label(text="    The monitored Object", icon='ZOOM_SELECTED')
        layout.prop(scene, "prop")
        layout.prop(Squeaktool, "axis_enum", icon='EMPTY_DATA')
       

        
        
        # Bake button
        #layout.label(text="")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.squeak_bake")
        #layout.label(text="")

#________________registration____________________       



classes = (
    SqueakProperties,
    SQ_PT_BK,
    SqueakBake,
    
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.Squeak_tool = bpy.props.PointerProperty(type= SqueakProperties)
    bpy.types.Scene.prop = PointerProperty(type=bpy.types.Object,name= "ObservObject ")
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.Squeak_tool
    del bpy.types.Scene.prop


if __name__ == "__main__":
    register()
    