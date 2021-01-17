bl_info = {
    "name": "Squeak Bake",
    "author": "Cristian Moga",
    "version": (2, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Speaker Data > SqeakBake",
    "description": "Tool to bake SFX in Speaker Object relative to the deformation of an object",
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
#______________clear the bake with the same name

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
            
            sqspeaker.animation_data.nla_tracks.remove(t)
    #deselect the SoundTrack
    gogu.select = False

#______________Bake the sound tracks
def sqeak_track (context):
        
       
    sqspeaker = context.object
    Squeaktool = context.scene.Squeak_tool
    SQ_label =  Squeaktool.Squeak_name
    
    
    
    
    tott = sqspeaker.animation_data.nla_tracks.new()
    tott.name = SQ_label
    bpy.ops.nla.soundclip_add(context.copy())
    tott.select=False        




class SQUEAKBAKE_OT_BakeSpeaker(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "squeakbake.squeak_bake"
    bl_label = "Bake Squeak"
    bl_info = "start the bake"
    bl_options = {'REGISTER' , 'UNDO'}
   

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'SPEAKER' and context.scene.prop  is not None
        
    
    
        

    def execute(self, context):
        
        
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
        
        if Squeaktool.def_enum == 'OP1':
            deformation = objectToCheck.rotation_euler
        if Squeaktool.def_enum == 'OP2':
            deformation = objectToCheck.location
        if Squeaktool.def_enum == 'OP3':
             deformation = objectToCheck.scale


        
        rotations = []
        sta= False
        scade= False
        creste= False
        bleep = False
#        Change the UI
        uitypesqueak = context.area.ui_type 
        context.area.ui_type = 'NLA_EDITOR'
        
        
        context.scene.frame_set(st-1)
        rotations.append(deformation[rolaxis])
        

        #____________________the loop______________
        
        if sqspeaker :
            sq_clear_bake (context)
            for i,x in enumerate(range(st,en)):
                context.scene.frame_set(x)
                rotations.append(deformation[rolaxis])
                                
                def_dif = rotations[i+1]-rotations[i]
                
                
                if def_dif == 0 :
                    if Squeaktool.zero_bool and sta: sqeak_track(context) 
                    sta = False
                else: sta = True
                  
                    
                if def_dif < 0 :
                    if Squeaktool.minus_bool and scade: sqeak_track(context)
                    scade = False
                else:scade = True
                
                     
                if def_dif > 0 :
                    if Squeaktool.plus_bool and creste: sqeak_track(context)
                    creste = False    
                else: creste = True
                  
                    
                      
            
                
                

            
           
        #______________________________________________________________________   
            
          
        bpy.context.area.ui_type = uitypesqueak 
        print("done")
        print("SqueakBake has Finished: %.4f sec" % (time.time() - time_start))
       
        self.report({'INFO'}, "It Squeaks now!")
        return {'FINISHED'}


class SQUEAKBAKE_PT_SPEAKER(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Squeak Bake"
    bl_idname = "SQUEAKBAKE_PT_SPEAKER"
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
        
        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")
        layout.label(text="")
        #NLA Track name
        
        layout.prop(Squeaktool, "Squeak_name", icon='NLA')
 

        
        #Object to be monitored 
        
        layout.prop(scene, "prop")
        #Axis to be monitored 
        layout.prop(Squeaktool, "axis_enum", icon='EMPTY_DATA')
        
        
        row = layout.row()
        row.scale_y = 0.1
        row.label(text="")
        
        
        #V2 update
       
       
        box=layout.box()
        row = box.row()
        row.scale_y = 1.5
        row.prop(Squeaktool, "def_enum",  expand=True)
        row = box.row()
        row.scale_y = 0.5
        row.label(text="From:")
        row = box.row()
        row.scale_y = 1.0
        row.prop(Squeaktool, "minus_bool", icon='PLAY_REVERSE')
        row.prop(Squeaktool, "zero_bool", icon='PAUSE')
        row.prop(Squeaktool, "plus_bool", icon='PLAY')
        
         # Bake button
        row = layout.row()
        row.scale_y = 0.1
        row.label(text="")
        
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.squeak_bake")
        
#________________registration____________________       









 
        
        
def sqeak_sequence (context):
        
       
    
    

    bpy.ops.sequencer.paste()
    












class SQUEAKBAKE_OT_Sequencer(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "squeakbake.squeak_seqbake"
    bl_label = "Squeak Sequences"
    bl_info = "multiply the sequence in reference to Squeaks"
    bl_options = {'REGISTER' , 'UNDO'}
   

    @classmethod
    def poll(cls, context):
        return  context.sequences is not None 
    
        

    def execute(self, context):
        
        time_start = time.time()
        context = bpy.context
        if context.scene.sequence_editor.sequences.data.active_strip.select == True :
            if context.scene.sequence_editor.sequences.data.active_strip.type == 'SOUND' :
                
            
                
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
                
                if Squeaktool.def_enum == 'OP1':
                    deformation = objectToCheck.rotation_euler
                if Squeaktool.def_enum == 'OP2':
                    deformation = objectToCheck.location
                if Squeaktool.def_enum == 'OP3':
                     deformation = objectToCheck.scale


                
                rotations = []
                sta= False
                scade= False
                creste= False
                bleep = False
        #        Change the UI
                bpy.context.area.ui_type = 'SEQUENCE_EDITOR'

                
                
                
                context.scene.frame_set(st-1)
                rotations.append(deformation[rolaxis])
                
                
                context.scene.frame_set(st)
                SequenceSq = context.scene.sequence_editor.sequences.data.active_strip
                SequenceSq.frame_start = st
                bpy.ops.sequencer.copy()
                SequenceSq.frame_start = en
                #bpy.ops.sequencer.delete()

            
                #____________________the loop______________
                
                for i,x in enumerate(range(st,en)):
                    context.scene.frame_set(x)
                    rotations.append(deformation[rolaxis])
                                        
                    def_dif = rotations[i+1]-rotations[i]
                        
                        
                    if def_dif == 0 :
                        if Squeaktool.zero_bool and sta: 
                            bpy.ops.sequencer.paste()
                            bleep = True
                        sta = False
                    else: sta = True
                          
                            
                    if def_dif < 0 :
                        if Squeaktool.minus_bool and scade: 
                            bpy.ops.sequencer.paste()
                            bleep = True
                        scade = False
                    else:scade = True
                        
                             
                    if def_dif > 0 :
                        if Squeaktool.plus_bool and creste: 
                            bpy.ops.sequencer.paste()
                            bleep = True
                        creste = False     
                    else: creste = True
                          
                context.scene.frame_set(st)           
                if bleep == False :
                                  
                    
                    bpy.ops.sequencer.paste()
                    
                    
                self.report({'INFO'}, "It Squeaks now!")
                print("done")
                print("SqueakBake has Finished: %.4f sec" % (time.time() - time_start))
           
            
                return {'FINISHED'}
            else : 
                self.report({'WARNING'}, "Must be a SOUND Track")
                return {'CANCELLED'}
        else : 
            self.report({'WARNING'}, "Select your track")
            return {'CANCELLED'}
        #______________________________________________________________________   
            
          
       
        

#_____________Properties input____________________


class SqueakProperties(bpy.types.PropertyGroup):
    
    Squeak_name : bpy.props.StringProperty(name= "NLA track", default="Squeak", description="the name of the NLA tracks")
    #axis 
    axis_enum : bpy.props.EnumProperty(
        name= "Axis",
        description= "The axis that will be monitored",
        items= [('OP1', "X", ""),
                ('OP2', "Y", ""),
                ('OP3', "Z", "")
        ]
    )
    
    #deformation typ  
    def_enum : bpy.props.EnumProperty(
        name= "Deformation",
        description= "The deformation that will be monitored",
        items= [('OP1', "Rotation", "search for Rotation Changes"),
                ('OP2', "Movement", "search for Position Changes"),
                ('OP3', "Scale", "search for Scale Changes")
        ]
    )

    #booleans of type of squeak    
    plus_bool : bpy.props.BoolProperty(
        name=" Higher Values",
        description="A simple bool property",
        default = True
    ) 
    zero_bool : bpy.props.BoolProperty(
        name=" Rest Position ",
        description="A simple bool property",
        default = True
    )
    minus_bool : bpy.props.BoolProperty(
        name=" Lower Values ",
        description="A simple bool property",
        default = True
    ) 

#_______________LAYOUT__________________


class SQUEAKBAKE_PT_SEQUENCER(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Squeak Bake"
    bl_idname = "SQUEAKBAKE_PT_SEQUENCER"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    #bl_context = 'sequences'
    #bl_options = {'HEADER_LAYOUT_EXPAND'}
    bl_category = "Squeak Bake"
    
    @classmethod
    def poll(cls, context):
        return  context.sequences is not None
        
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        Squeaktool = scene.Squeak_tool
        
       
 

        
        #Object to be monitored 
        
        layout.prop(scene, "prop")
        #Axis to be monitored 
        layout.prop(Squeaktool, "axis_enum", icon='EMPTY_DATA')
        
        
        row = layout.row()
        row.scale_y = 0.1
        row.label(text="")
        
        
        #V2 update
       
       
        box=layout.box()
        row = box.row()
        row.scale_y = 1.5
        row.prop(Squeaktool, "def_enum",  expand=True)
        row = box.row()
        row.scale_y = 0.5
        row.label(text="From:")
        row = box.row()
        row.scale_y = 1.0
        row.prop(Squeaktool, "minus_bool", icon='PLAY_REVERSE')
        row.prop(Squeaktool, "zero_bool", icon='PAUSE')
        row.prop(Squeaktool, "plus_bool", icon='PLAY')
        
         # Bake button
        row = layout.row()
        row.scale_y = 0.1
        row.label(text="")
        
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.squeak_seqbake")
        
#________________registration____________________       



classes = (
    SqueakProperties,
    SQUEAKBAKE_PT_SPEAKER,
    SQUEAKBAKE_PT_SEQUENCER,
    SQUEAKBAKE_OT_BakeSpeaker,
    SQUEAKBAKE_OT_Sequencer,
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
    
