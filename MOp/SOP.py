'''
Tier: Base
'''

from ..MVar import *




###########################################################################
################################### SOP ###################################
###########################################################################
'''
hou.SopNode         http://www.sidefx.com/docs/houdini/hom/hou/SopNode.html
'''

def _node_newObjectMerge( self ):
    '''
    Create new "Object Merge" node and point to this node.
    '''
    new_objMerge = self.Parent.newNode( 'object_merge' )
    new_objMerge.P = self.P + nPy * 2

    new_objMerge.parm('objpath1').set( new_objMerge.relativePathTo( self ) )

    return new_objMerge
setAttr( hou.SopNode, 'newObjectMerge', _node_newObjectMerge )
setAttr( hou.SopNode, 'toObjectMerge', _node_newObjectMerge )











