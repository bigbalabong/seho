'''
Tier: Base
'''

from ..MVar import *

'''
Houdini Engine 3.3              https://www.sidefx.com/docs/hengine/
Houdini Engine for Maya         http://www.sidefx.com/docs/maya/


Callback Script         https://www.sidefx.com/docs/maya/_maya__parameters.html#Maya_Parameters_CallbackScript


Houdini 18.0.509
        Added the sidefx::maya_parm_affects_others parm tag. 
        This tag notifies Maya that a full attribute sync should be performed when the parm is modified.
        Thu. June 25, 2020
'''



'''
Custom Python Module won't be imported.
But custom VEX lib can be.
'''



def _hda_addInfoParmForMaya( self ):
    """
    Add a hiden string parm storing info about this HDA.

    Author: Sean
    """
    # collect info
    icon = self.Icon
    info = [ ( 'icon', icon ) ]
    info = [ ': '.join(i) for i in info ]
    info = '; '.join( info )
    info += ';'


    # new string parm to store info
    info_parm = hou.StringParmTemplate( name = '__hda_info', label = '__hda_info', 
                                        num_components = 1,
                                        help = info 
                                        )
    info_parm.Hidden = True


    # update parm template group
    grp = self.ParmTemplateGrp
    first_parm = grp.ParmTemplates[0]
    grp.insertBefore( first_parm, info_parm )
    
    # apply parm template group
    self.setParmTemplateGroup( grp, rename_conflicting_parms=True )
setAttr( hou.HDADefinition, 'addInfoParmForMaya', _hda_addInfoParmForMaya )








