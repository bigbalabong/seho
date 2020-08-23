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
# ========================= Menu ========================= #
# ======================================================== #
setAttr( hou.Parm, "MenuLabels", property( hou.Parm.menuLabels ) )
setAttr( hou.Parm, "MenuValues", property( hou.Parm.menuItems ) )

def _parm_getMenuItems( self ):
    """
    Author: Sean
    """
    return zip( self.MenuLabels, self.MenuValues )
setAttr( hou.Parm, "MenuItems", property( _parm_getMenuItems ) )






# ======================================================== #
# ========================= Value ======================== #
# ======================================================== #
def _parm_getValue( self ):
    """
    Author: Sean
    """
    value = self.eval()
    
    if type( value ) is hou.Ramp:
        value.Parm = self

    return value
setAttr( hou.Parm, "Value", property( _parm_getValue, hou.Parm.set ) )
setAttr( hou.Parm, "_", hou.Parm.Value )


setAttr( hou.Parm, "Raw", property( hou.Parm.rawValue ) )



def _parm_getValueType( self ):
    '''
    hou.parmData        http://www.sidefx.com/docs/houdini/hom/hou/parmData.html

    RETURN:
            (str) int / float / string / ramp
    
    Author: Sean
    '''
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

















