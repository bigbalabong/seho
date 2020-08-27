'''
Tier: Base
'''

from ..MVar import *


'''
hou.ParmTemplate                                  http://www.sidefx.com/docs/houdini/hom/hou/ParmTemplate.html#setConditional
hou.exprLanguage                                  http://www.sidefx.com/docs/houdini/hom/hou/exprLanguage.html
hou.parmCondType                                  http://www.sidefx.com/docs/houdini/hom/hou/parmCondType.html

Expression Functions                              https://www.sidefx.com/docs/houdini/expressions/index.html
'''


def _node_findMissingFiles( self, folderpath=None, all_files=None, recursive=False ):
    '''
    Find missing files.
    
    NOTE: Currently, only find missing file for the first parameter with IO error.
    
    Author: Sean
    '''
    # cook node to update error info
    # try:
    #     self.cook()
    # except:
    #     pass

    if not self.ErrorIO:
        return
    else:
        # collect info about missing files
        missing_filepath = self.ErrorIO[0].split('Unable to read file')[-1].strip()[:-1][1:-1]
        missing_file_basename = os.path.basename( missing_filepath )

        missing_file_parm = [ i for i in self.Parms if i.eval() == missing_filepath ]
        if not missing_file_parm:
            return
        else:
            missing_file_parm = missing_file_parm[0]


    if not folderpath:
        folderpath = hou.expandString('$HIP')
    
    if not all_files:
        all_files = File.allFiles( folderpath, as_dict=True )


    # find missing files
    if missing_file_basename in all_files.keys():
        missing_file_parm.set( all_files[missing_file_basename][0] )


    # re-cook node
    # try:
    #     self.cook()
    # except:
    #     pass


    if children:
        for node in self.Nodes:
            node.findMissingFiles( all_files=all_files )
setAttr( hou.Node, "findMissingFiles", _node_findMissingFiles )



def _node_getFrameRange( self ):
    """
    Author: Sean
    """
    parms = self.ParmsKey

    keyframe_start = keyframe_end = None
    if parms:
        # get frames
        keyframe_start = min([ i.keyframes()[0].frame() for i in parms ])
        keyframe_end = max([ i.keyframes()[-1].frame() for i in parms ])
        
    return keyframe_start, keyframe_end
setAttr( hou.Node, "FrameRange", property( _node_getFrameRange ) )


def _node_updateFrameRange( self ):
    """
    Author: Sean
    """
    keyframe_start, keyframe_end = self.FrameRange

    if keyframe_start is not None:
    # set playbar timeline range
        hou.playbar.setFrameRange( keyframe_start, keyframe_end )
        hou.playbar.setPlaybackRange( keyframe_start, keyframe_end )
setAttr( hou.Node, 'updateFrameRange', _node_updateFrameRange )







###########################################################################
################################ Parameter ################################
###########################################################################
'''
hou.Parm        http://www.sidefx.com/docs/houdini/hom/hou/Parm
'''

# ======================================================== #
# ====================== Basic Info ====================== #
# ======================================================== #
setAttr( hou.Parm, "Name", property( hou.Parm.name ) )
setAttr( hou.Parm, "Alias", property( hou.Parm.alias, hou.Parm.setAlias ) )


def _parm_setLabel( self, label ):
    """
    Author: Sean
    """
    tmp = self.ParmTemplate
    tmp.Label = label
    tmp.apply()
setAttr( hou.Parm, "Label", property( hou.Parm.description, _parm_setLabel ) )


setAttr( hou.Parm, "Path", property( hou.Parm.path ) )


def _parm_getIndex( self ):
    """
    Get parm index in parm tuple.

    Author: Sean
    """
    if self.ParmTemplate.numComponents() == 1:
        return 0
        
    else:
        suffix = self.Name[-1].lower()
        suffix_list = str(self.ParmTemplate.namingScheme()).rsplit('.', 1)[1].lower()
        index = suffix_list.index( suffix )
        return index
setAttr( hou.Parm, "Index", property( _parm_getIndex ), replace=False )



def _parm_getHelp( self ):
    """
    Author: Sean
    """
    return self.ParmTemplate.Help

def _parm_setHelp( self, info ):
    """
    Author: Sean
    """
    tmp = self.ParmTemplate
    tmp.Help = info
    tmp.apply()

setAttr( hou.Parm, "Help", property( _parm_getHelp, _parm_setHelp ) )




# ======================================================== #
# ========================= State ======================== #
# ======================================================== #
setAttr( hou.Parm, "Locked", property( hou.Parm.isLocked, hou.Parm.lock ) )

setAttr( hou.Parm, "Hidden", property( hou.Parm.isHidden, hou.Parm.hide ) )

def _parm_setVisible( self, bool_ ):
    """
    Author: Sean
    """
    self.hide( not bool_ )
setAttr( hou.Parm, "Visible", property( hou.Parm.isVisible, _parm_setVisible ) )


setAttr( hou.Parm, "Constrained", property( hou.Parm.isConstrained ) )

setAttr( hou.Parm, "TimeDependent", property( hou.Parm.isTimeDependent ) )


setAttr( hou.Parm, "Disabled", property( hou.Parm.isDisabled, hou.Parm.disable ) )


setAttr( hou.Parm, "Scoped", property( hou.Parm.isScoped, hou.Parm.setScope ) )
setAttr( hou.Parm, "AutoScoped", property( hou.Parm.isAutoscoped, hou.Parm.setAutoscope ) )


setAttr( hou.Parm, "Selected", property( hou.Parm.isSelected, hou.Parm.setSelect ) )
setAttr( hou.Parm, "AutoSelected", property( hou.Parm.isAutoSelected, hou.Parm.setAutoSelect ) )





# ======================================================== #
# ======================== String ======================== #
# ======================================================== #
def _parm_stringToList( self ):
    tmp = self.ParmTemplate
    
    if not isinstance( tmp, hou.StringParmTemplate ):
        return

    strings = [ i.strip() for i in self._.split( ' ' ) ]
    strings = [ i for i in strings if i ]
    return strings
setAttr( hou.Parm, "toList", _parm_stringToList, replace=True )


def _parm_stringToNode( self ):
    return self.Node.node( self._ )
setAttr( hou.Parm, "toNode", _parm_stringToNode, replace=False )




# ======================================================== #
# ========================= Menu ========================= #
# ======================================================== #
setAttr( hou.Parm, "MenuLabels", property( hou.Parm.menuLabels ) )
setAttr( hou.Parm, "MenuValues", property( hou.Parm.menuItems ) )

def _parm_getMenuItems( self ):
    """
    Examples:
        hou.parm('/obj/geo1/sphere1/type').Value
        # Returns: 0
        hou.parm('/obj/geo1/sphere1/type').Raw
        # Returns: 'prim'

    Author: Sean
    """
    return zip( self.MenuLabels, self.MenuValues )
setAttr( hou.Parm, "MenuItems", property( _parm_getMenuItems ) )






# ======================================================== #
# ====================== Multi-parm ====================== #
# ======================================================== #

# ~~~~~~~~~~~~~~~ Multi-parm ~~~~~~~~~~~~~~ #

def _parm_getMultiParmInstances( self ):
    return self.multiParmInstances()
setAttr( hou.Parm, "Instances", property( _parm_getMultiParmInstances ) )


def _parm_getMultiParmInstanceGroups( self ):
    instances = self.Instances

    if not instances:
        # return empty tuple
        return instances

    num = len( self.ParmTemplate.ParmTemplates )
    return L_( instances ).group( num )
setAttr( hou.Parm, "InstanceGrps", property( _parm_getMultiParmInstanceGroups ), replace=True )


def _parm_getMultiParmInstanceGroupJustBorn( self ):
    multiparm_tmps = self.ParmTemplate.ParmTemplates
    justBorn_tmp = [ i for i in multiparm_tmps if i.Name.endswith( '__justBorn#' ) ]
    
    if not justBorn_tmp:
        return

    index = multiparm_tmps.index( justBorn_tmp[0] )

    grps = [ i for i in self.InstanceGrps if i[index]._ == True ]
    return grps
setAttr( hou.Parm, "InstanceGrpsJustBorn", property( _parm_getMultiParmInstanceGroupJustBorn ), replace=True )




# ~~~~~~~~~~ Multi-parm Instance ~~~~~~~~~~ #

def _parm_getMultiParmInstanceIndexGlobal( self ):
    if not self.isMultiParmInstance():
        return

    return self.multiParmInstanceIndices()[0]
setAttr( hou.Parm, "InstanceIndexGlobal", property( _parm_getMultiParmInstanceIndexGlobal ), replace=True )


def _parm_getMultiParmInstanceIndexLocal( self ):
    if not self.isMultiParmInstance():
        return

    num = len( self.parentMultiParm().ParmTemplate.ParmTemplates )
    index = self.multiParmInstanceIndices()[0]
    return index % num
setAttr( hou.Parm, "InstanceIndexLocal", property( _parm_getMultiParmInstanceIndexLocal ), replace=True )


def _parm_getMultiParmInstanceGroupIndex( self ):
    if not self.isMultiParmInstance():
        return

    num = len( self.parentMultiParm().ParmTemplate.ParmTemplates )
    index = self.multiParmInstanceIndices()[0]
    return index / num
setAttr( hou.Parm, "InstanceGrpIndex", property( _parm_getMultiParmInstanceGroupIndex ), replace=True )









# ======================================================== #
# ========================= Value ======================== #
# ======================================================== #
def _parm_getValue( self ):
    """
    Author: Sean
    """
    value = self.eval()
    
    if type( value ) is hou.Ramp:
        setAttr( value, "Parm", self )

    return value

def _parm_setValue( self, value ):
    if isinstance( value, hou.Node ):
        node = value

        if isinstance( self.ParmTemplate, hou.StringParmTemplate ):
            nodepath = self.Node.relativePathTo( node )
            self.set( nodepath )

    else:
        self.set( value )

setAttr( hou.Parm, "Value", property( _parm_getValue, _parm_setValue ), replace=True )
setAttr( hou.Parm, "_", hou.Parm.Value, replace=True )



"""
Examples:
    hou.parm('/obj/geo1/sphere1/type').Value
    # Returns: 0
    hou.parm('/obj/geo1/sphere1/type').Raw
    # Returns: 'prim'
"""
setAttr( hou.Parm, "Raw", property( hou.Parm.rawValue ) )



def _parm_getValueType( self ):
    """
    hou.parmData        http://www.sidefx.com/docs/houdini/hom/hou/parmData.html

    Returns:
            (str) int / float / string / ramp
    
    Author: Sean
    """
    return self.ParmTemplate.DataType
setAttr( hou.Parm, "DataType", property( _parm_getValueType ) )
setAttr( hou.Parm, "ValueType", property( _parm_getValueType ) )



# ~~~~~~~~~~~~~~~~ Default ~~~~~~~~~~~~~~~~ #
'''
.hasTemporaryDefaults
.isAtDefault
.revertToAndRestorePermanentDefaults
.revertToDefaults
'''

def _parm_getDefault( self ):
    """
    Author: Sean
    """
    default = self.ParmTemplate.Default
    index = self.Index
    return default[ index ]
setAttr( hou.Parm, "Default", property( _parm_getDefault ), replace=False )



# ~~~~~~~~~~~~~~ Value Range ~~~~~~~~~~~~~~ #
def _parm_getMinimum( self ):
    tmp = self.ParmTemplate

    if type(tmp) not in ( hou.IntParmTemplate, hou.FloatParmTemplate ):
        return

    return tmp.Min

def _parm_setMinimum( self, value ):
    tmp = self.ParmTemplate

    if type(tmp) not in ( hou.IntParmTemplate, hou.FloatParmTemplate ):
        return

    tmp.Min = value
    tmp.apply()

setAttr( hou.Parm, "Min", property( _parm_getMinimum, _parm_setMinimum ), replace=True)




def _parm_getMaximum( self ):
    tmp = self.ParmTemplate

    if type(tmp) not in ( hou.IntParmTemplate, hou.FloatParmTemplate ):
        return

    return tmp.Max

def _parm_setMaximum( self, value ):
    tmp = self.ParmTemplate

    if type(tmp) not in ( hou.IntParmTemplate, hou.FloatParmTemplate ):
        return

    tmp.Max = value
    tmp.apply()

setAttr( hou.Parm, "Max", property( _parm_getMaximum, _parm_setMaximum ), replace=True )











# ======================================================== #
# ========================== UI ========================== #
# ======================================================== #
def _parm_getJoinNext( self ):
    """
    Author: Sean
    """
    return self.ParmTemplate.joinsWithNext()

def _parm_setJoinNext( self, state ):
    """
    Author: Sean
    """
    template = self.ParmTemplate
    template >> state
    template.apply()

setAttr( hou.Parm, "JoinNext", property( _parm_getJoinNext, _parm_setJoinNext ) )








# ======================================================== #
# ========================= .chan ======================== #
# ======================================================== #
'''
chwrite         https://www.sidefx.com/docs/houdini/commands/chwrite.html
chread          https://www.sidefx.com/docs/houdini/commands/chread.html
'''

















