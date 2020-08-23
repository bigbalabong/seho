'''
Tier: Base
'''

from ..MVar import *




###########################################################################
############################### Parm Tuple ################################
###########################################################################
'''
hou.ParmTuple       http://www.sidefx.com/docs/houdini/hom/hou/ParmTuple.html
'''


# ======================================================== #
# ====================== Basic Info ====================== #
# ======================================================== #
setAttr( hou.ParmTuple, "Name", property( hou.ParmTuple.name ) )
setAttr( hou.ParmTuple, "Label", property( hou.ParmTuple.description ) )




# ======================================================== #
# ========================= State ======================== #
# ======================================================== #
setAttr( hou.ParmTuple, "Disabled", property( hou.ParmTuple.isDisabled, hou.ParmTuple.disable ) )

setAttr( hou.ParmTuple, "Hidden", property( hou.ParmTuple.isHidden, hou.ParmTuple.hide ) )


def _parmTuple_getLocked( self ):
    """
    Author: Sean
    """
    return [ i.Locked for i in self.Parms ]
setAttr( hou.ParmTuple, "Locked", property( _parmTuple_getLocked, hou.ParmTuple.lock ) )




# ======================================================== #
# ========================= Value ======================== #
# ======================================================== #
setAttr( hou.ParmTuple, "Value", property( hou.ParmTuple.eval, hou.ParmTuple.set ) )
setAttr( hou.ParmTuple, "_", hou.ParmTuple.Value )






