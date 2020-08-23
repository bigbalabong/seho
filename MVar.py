'''
Tier: Base
'''

from .MBase import *




App_Path = S_( sys.executable ).normpath()
APP_Root = App_Path.rsplit('bin', 1)[0][:-1]




###########################################################################
#################################### Qt ###################################
###########################################################################

# C:\Program Files\Side Effects Software\Houdini 18.0.416\houdini\config\Styles\base.qss


# from PySide2.QtCore import __version__ as Qt_Ver


# def dropEvent( self, event ):
#     print event.mimeData().formats()
Houdini_DnD_Format_NodePath = 'application/sidefx-houdini-node.path'
Houdini_DnD_Format_ParmPath = 'application/sidefx-houdini-parm.path'









###########################################################################
############################# Global Variables ############################
###########################################################################

aboutGlobalVars = {
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Environment Variables
    # https://www.sidefx.com/docs/houdini/basics/project.html#tips-and-notes
    "$HSITE" : "For tools and resources common across all projects, the Houdini convention is to use an environment variable named $HSITE.",
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # HScript Global Variables          https://www.sidefx.com/docs/houdini/network/expressions.html#globals
    "$HFS" : "The directory where Houdini is installed.",
    "$HH" : "$HFS/houdini",
    "$HOME" : "Your home directory.     e.g. C:/Users/SEAN/Documents",
    "$HOUDINI_USER_PREF_DIR" : "e.g. C:/Users/SEAN/Documents/houdini17.5",
    "$JOB" : "The project directory.    e.g. $JOB/sim/cached/test.$SF.sim",
    "$HIP" : "This defaults to the directory where you started Houdini. (The directory containing the current scene file.)",
    "$HIPFILE" : "The full path of the loaded scene file, including the file extension.     e.g. C:/Users/SEAN/Desktop/untitled.hip",
    "$HIPFILE:r" : "without extension name.     e.g. C:/Users/SEAN/Desktop/untitled",
    "$HIPNAME" : "The name of the current .hip file without the extension. This can be useful for building other filenames based on the name of the scene where they originate from.",
    "$ACTIVETAKE" : "The name of the current take.",
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Timeline
    "$F" : "The current frame, (as set with the Playbar controls). Very useful variable, especially for rendered picture filename numbering. e.g. test.$F4.jpg. And $F4 means 0001, 0002... 0105...",
    "$FF" : "Floating point frame number. Same as @Frame.",
    "$T" : "Current time in seconds. Equals ($F-1)/$FPS. Same as @Time.",
    "$TIMESTEP" : "The size of a simulation timestep. Useful to scale values that are expressed in units per second, but are applied on each timestep.",
    "$FPS" : "Playback speed in frames per second (as set with the Playbar controls).",
    "$FSTART" : "Frame number of the 1st frame of animation (as set with the Playbar controls).",
    "$FEND" : "Frame number of the last frame of animation (as set with the Playbar controls).",
    "$RFSTART" : "Frame number of the 1st frame shown in the playbar.",
    "$RFEND" : "Frame number of the last frame shown in the playbar.",
    "$NFRAMES" : "Number of frames in the animation. $NFRAMES = $FEND - $FSTART + 1",
    "$TSTART" : "Start time of animation in seconds.",
    "$TEND" : "End time of animation in seconds.",
    "$TLENGTH" : "Total length of animation in seconds.",
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # DOPs
    "$SF" : "Simulation Frame (or more accurately, the simulation time step number) for which the node is being evaluated. This value may not be equal to the current Houdini frame number represented by the $F, depending on the settings of the DOP Network parameters. Instead, this value is equal to $ST divided by $TIMESTEP.",
    "$ST" : "Simulation Time for which the node is being evaluated. This value may not be equal to the current Houdini time represented by the $T, depending on the settings of the DOP Network Offset Time and Time Scale parameters. This value is guaranteed to have a value of 0 at the start of a simulation, so when testing for the first timestep of a simulation, it is best to use a test like $ST == 0 rather than $T == 0 or $FF == 1.",
    "$SFPS" : "The number of timesteps per second of simulation time. The inverse of the $TIMESTEP.",
    "$OBJ" : "The index of the specific object being processed by the node. This value will always run from 0 to $NOBJ-1 in a given timestep. This value does not identify the current object within the simulation like $OBJID or $OBJNAME, just the object's position in the current order of processing. Useful for generating a random number for each object, or simply splitting the objects into two or more groups to be processed in different ways. This value will be -1 if the node does not process objects sequentially (such as the Group DOP).",
    "$OBJID" : "The unique object identifier for the object being processed. Every object is assigned an integer value that is unique among all objects in the simulation for all time. Even if an object is deleted, its identifier is never reused. The object identifier can always be used to uniquely identify a given object. This makes this variable very useful in situations where each object needs to be treated differently. It can be used to produce a unique random number for each object, for example. This value is also the best way to look up information on an object using the dopfield expression function. This value will be -1 if the node does not process objects sequentially (such as the Group DOP).",
    "$ALLOBJIDS" : "This string contains a space separated list of the unique object identifiersfor every object being processed by the current node.",
    "$OBJNAME" : "A string value containing the name of the object being processed. Object names are not guaranteed to be unique within a simulation. However, if you name your objects carefully so that they are unique, the object name can be a much easier way to identify an objectthan the unique object identifier, $OBJID. The object name can also be used to treat a number of similar objects (with the same name) as a virtual group. If there are 20 objects named 'myobject', specifying strcmp($OBJNAME, 'myobject') == 0 in the activation field of a DOP will cause that DOP to operate only on those 20 objects. This value will be the empty string if the node does not process objects sequentially (such as the Group DOP).",
    "$ALLOBJNAMES" : "This string contains a space separated list of the names of every object being processed by the current node.",
    "$OBJCF" : "The simulation frame (see variable $SF) at which the current object was created. This value is equivalent to using the dopsttoframe expression on the $OBJCT variable. This value will be 0 if the node does not process objects sequentially (such as the Group DOP).",
    "$DATACF" : "The simulation frame (see $SF) at which the current data was created. This value may not be the same as the current simulation frame if this node is modifying existing data, rather than creating new data.",
    "$OBJCT" : "The simulation time (see $ST) at which the current object was created. Therefore, to check if an object was created on the current timestep, the expression $ST == $OBJCT should always be used. This value will be 0 if the node does not process objects sequentially (such as the Group DOP).",
    "$DATACT" : "The simulation time (see variable ST) at which the current data was created. This value may not be the same as the current simulation time if this node is modifying existing data, rather than creating new data.",
    "$NOBJ" : "The number of objects that will be evaluated by the current nodeduring this timestep. This value will often be different from $SNOBJ, as many nodes do not process all the objects in a simulation. This value may return 0 if the node does not process each object sequentially (such as the Group DOP).",
    "$SNOBJ" : "The number of objects in the simulation. For nodes that create objects such as the Empty Object DOP, this value will increase for each object that is evaluated. A good way to guarantee unique object names is to use an expression like object_$SNOBJ.",
    "$DOPNET" : "A string value containing the full path of the current DOP Network. This value is most useful in DOP subnet digital assets where you want to know the path to the DOP Network that contains the node.",
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Math
    "$E" : "The mathematical constant e(2.71828...).",
    "$PI" : "The mathematical constant pi(3.1415926...).",
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # CHOPs
    "$OS" : "Current Operator's name.",
    "$CH" : "Current channel's name",
    "$IV" : "In value (value at start of segment).",
    "$OV" : "Out value.",
    "$IM" : "In slope.",
    "$OM" : "Out slope.",
    "$IA" : "In acceleration.",
    "$OA" : "Out acceleration.",
    "$LT" : "Local time - not including stretch or offset.",
    "$IT" : "Start time of segment.",
    "$OT" : "End time of segment.",
    "$LIT" : "Local start time of segment.",
    "$LOT" : "Local end time of segment.",
    "$PREV_IT" : "Previous segment start time.",
    "$NEXT_OT" : "Next segment end time.",
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # COPs
    "$CSTART" : "Start frame of the current COP.",
    "$CEND" : "End frame of the current COP.",
    "$CFRAMES" : "Number of frames for the current COP.",
    "$CFRAMES_IN" : "Number of frames available from the 1st input COP.",
    "$CINC" : "Get the global frame increment value.",
    "$W" : "Current image width.",
    "$H" : "Current image height.",
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Render
    "$N" : "Current frame being rendered.",
    "$NRENDER" : "Number of frames being rendered.",
    }












###########################################################################
################################ Parameter ################################
###########################################################################

ParmName_Filepath = ( 'file', 'fileName' )

Grouptypes = {
    'point':                        'point',
    'edge' :                        'edge',
    'vertex':                       'vert',
    'primitive':                    'prim',
    'breakpoint':                   'break',
    'guess':                        'guess',
    hou.geometryType.Points:        'point',
    hou.geometryType.Edges:         'edge',
    hou.geometryType.Primitives:    'prim',
    hou.geometryType.Breakpoints:   'break',
    }






###########################################################################
################################### Node ##################################
###########################################################################

ROOT = hou.node('/')


# unit size 1 is equal to one node width
# gap between node and node name is 0.1
# node position offset vector
nPx = hou.Vector2( 3, 0 )
nPy = hou.Vector2( 0, -1.0075 )     # hou.Vector2( 0, -1.2 )

def autoNPx( names ):
    """
    Author: Sean
    """
    if isinstance( names[0], hou.Node ):
        names = [ i.Name for i in names ]

    unit_width = float(max([ len(i) for i in names ])) / 9 + 1.1        # 1 is one node with. 0.1 is the gap between node and node name.
    gap = 0.4

    return hou.Vector2( unit_width + gap, 0 )


HDA_Notes_Path = r'C:\Dropbox\houdini\sean\otls\notes'


Wrangle_NodeNames = [ 'attribwrangle' ]


Gallery_Path = r'C:\Dropbox\houdini\sean\gallery'


Builtin_HDR_Path =      hou.expandString('$HFS/houdini/pic/hdri/')
Builtin_Texture_Path =  hou.expandString('$HFS/houdini/pic/texture/')




Node_Errors = {
    'File Missing' : ( 'Error evaluating objects in file', 'Unable to read file' )
    }


# Nodetype_Cates = {
#     'vop':          ('Sop/attribvop', 'Sop/volumevop'),
#     
#     'draw':         ('Sop/stroke', 'Sop/drawcurve',
#                     'Sop/guidegroom'),
#     'noise':        ('Vop/aanoise', 'Vop/unifiednoise', 'Vop/unifiednoise_static'),
#     'collision':    ('Sop/detangle',),
#     'compile':      ('Sop/compile_end',),
#     'io':           ('Sop/file', 'Sop/filecache', 'Sop/filemerge', ),
#     }
# Nodetype_Cates_Reversed = dict( D_(Nodetype_Cates).itemsUnzippedReversed() )







###########################################################################
################################### Mesh ##################################
###########################################################################

BB_Corner = {
        0 :     ('D_XMIN', 'D_YMIN', 'D_ZMIN'),
        1 :     ('D_XMAX', 'D_YMIN', 'D_ZMIN'),
        2 :     ('D_XMAX', 'D_YMIN', 'D_ZMAX'),
        3 :     ('D_XMIN', 'D_YMIN', 'D_ZMIN'),
        4 :     ('D_XMIN', 'D_YMAX', 'D_ZMIN'),
        5 :     ('D_XMAX', 'D_YMAX', 'D_ZMIN'),
        6 :     ('D_XMAX', 'D_YMAX', 'D_ZMAX'),
        7 :     ('D_XMIN', 'D_YMAX', 'D_ZMAX'),
    }











###########################################################################
################################### VEX ###################################
###########################################################################

VEX_Libs = { 
        'SEAN': {
                'base' : ( 'seho_base.h', normpath( __file__, '../../../../vex/include/seho_base.h', check=False ) ),
            }
    }


vex_libs_dir = os.path.join( APP_Root, 'houdini/vex' )
vex_libs_paths = File.allFiles( vex_libs_dir, subfolder=True )
vex_libs_dict = dict( [ ( os.path.basename( i ), i ) for i in vex_libs_paths ] )


opencl_libs_dir = os.path.join( APP_Root, 'houdini/ocl' )
opencl_libs_paths = File.allFiles( opencl_libs_dir, subfolder=True )
opencl_libs_dict = dict( [ ( os.path.basename( i ), i ) for i in opencl_libs_paths ] )









###########################################################################
################################### HDA ###################################
###########################################################################

hda_naming_conventions = '''
ATTRIBUTE:
        _*      helpful attributes
        __*     temp attributes. only be used inside HDA. clean out these attributes at the end of HDA
'''














###########################################################################
################################### Pane ##################################
###########################################################################

# pane position offset vector
pPx = hou.Vector2( 100, 0 )
pPy = hou.Vector2( 0, -70 )













