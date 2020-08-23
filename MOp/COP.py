'''
Tier: Base
'''

from ..MVar import *




###########################################################################
################################### COP ###################################
###########################################################################
'''
hou.CopNode         http://www.sidefx.com/docs/houdini/hom/hou/CopNode.html
'''

setAttr( hou.CopNode, "Planes", property( hou.CopNode.planes ) )


def _cop_getChannels( self, plane ):
    """[summary]

    Args:
        plane (str): [description]

    Returns:
        [type]: [description]
    """
    return self.components( plane )
setAttr( hou.CopNode, "Channels", property( _cop_getChannels ) )


setAttr( hou.CopNode, "ResX", property( hou.CopNode.xRes ) )
setAttr( hou.CopNode, 'Width', hou.CopNode.ResX )

setAttr( hou.CopNode, "ResY", property( hou.CopNode.yRes ) )
setAttr( hou.CopNode, 'Height', hou.CopNode.ResY )








