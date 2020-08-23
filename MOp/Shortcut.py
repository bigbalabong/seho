'''
Tier: Base
'''

from ..MVar import *





###########################################################################
############################### hou.NodeType ##############################
###########################################################################
setAttr( hou.NodeType, "Instances", property( hou.NodeType.instances ) )


def _nodetype_isHDA( self ):
    """
    Author: Sean
    """
    if self.definition():
        return True
    else:
        return False
setAttr( hou.NodeType, 'isHDA', _nodetype_isHDA )

setAttr( hou.NodeType, "HDA", property( hou.NodeType.definition ) )



# ======================================================== #
# ========================== HDA ========================= #
# ======================================================== #
setAttr( hou.HDADefinition, "Nodetype", property( hou.HDADefinition.nodeType ) )
setAttr( hou.HDADefinition, 'Type', hou.HDADefinition.Nodetype )








###########################################################################
################################# hou.Node ################################
###########################################################################
class FakeNode( object ):

    """
    Author: Sean
    """

    def __init__( self, node ):
        self.Node = node

    def __getitem__( self, name ):
        '''
        Args:
            name (str): name pf parameter.

        Returns:
            [hou.Parm / hou.ParmTuple]: [description]    

        Examples:
            hou.node('/obj/geo1/box1')['sizex'].Value = 2
            hou.node('/obj/geo1/box1')['sizey'].Value = 0.1
        
        Author: Sean
        '''
        node = self.Node

        # try to get parm
        parm = node.parm( name )

        # try to get parm tuple
        if parm is None:
            parm = node.parmTuple( name )

        return parm

def _node_getFakeNode( self ):
    """
    Author: Sean
    """
    return FakeNode( self )
setAttr( hou.Node, '_', property( _node_getFakeNode ), replace=False )




def _node_getNodetype( self ):
    """
    Author: Sean
    """
    nodetype = self.type()
    setAttr( nodetype, 'Node', self )
    return nodetype
setAttr( hou.Node, "Nodetype", property( _node_getNodetype ) )
setAttr( hou.Node, 'Type', hou.Node.Nodetype )



def _node_isHDA( self ):
    """
    Shortcut to hou.NodeType.isHDA()

    Author: Sean
    """
    return self.Type.isHDA()
setAttr( hou.Node, 'isHDA', _node_isHDA )

def _node_isBlackbox( self ):
    """
    Author: Sean
    """
    if not self.isSubNetwork():
        return False

    try:
        children = self.Children
        return False
        
    except:
        return True
setAttr( hou.Node, 'isBlackbox', _node_isBlackbox )



def _node_getHDADefinition( self ):
    """
    Shortcut to get HDA definition.

    Author: Sean
    """
    hda = self.Type.HDA
    setAttr( hda, 'Node', self )
    return hda
setAttr( hou.Node, "HDA", property( _node_getHDADefinition ) )


setAttr( hou.Node, "HM", property( hou.Node.hm ) )





# ======================================================== #
# ====================== hou.SopNode ===================== #
# ======================================================== #
setAttr( hou.SopNode, 'Geo', property( hou.SopNode.geometry ) )

def _node_getInputGeo0( self ):
    '''
    RETURN:
            The Geometry of the input node index 0.

    Author: Sean
    '''
    return self.inputGeometry( 0 )
setAttr( hou.SopNode, 'Geo0', property( _node_getInputGeo0 ) )

def _node_getInputGeo1( self ):
    '''
    RETURN:
            The Geometry of the input node index 1.
    
    Author: Sean
    '''
    return self.inputGeometry( 1 )
setAttr( hou.SopNode, 'Geo1', property( _node_getInputGeo1 ) )

def _node_getInputGeo2( self ):
    '''
    RETURN:
            The Geometry of the input node index 2.
    
    Author: Sean
    '''
    return self.inputGeometry( 2 )
setAttr( hou.SopNode, 'Geo2', property( _node_getInputGeo2 ) )

def _node_getInputGeo3( self ):
    '''
    RETURN:
            The Geometry of the input node index 3.
    
    Author: Sean
    '''
    return self.inputGeometry( 3 )
setAttr( hou.SopNode, 'Geo3', property( _node_getInputGeo3 ) )



# ~~~~~~~~~~~~~~~ Visualizer ~~~~~~~~~~~~~~ #
def _node_getVisualizers( self ):
    """
    Author: Sean
    """
    hou.viewportVisualizers.visualizers( category=hou.viewportVisualizerCategory.Node, node=self )
setAttr( hou.Node, 'Visualizer', property( _node_getVisualizers ) )






###########################################################################
################################# hou.Parm ################################
###########################################################################
setAttr( hou.Parm, "Node", property( hou.Parm.node ) )






###########################################################################
############################## hou.ParmTuple ##############################
###########################################################################
setAttr( hou.ParmTuple, "Node", property( hou.ParmTuple.node ) )






###########################################################################
########################## hou.ParmTemplateGroup ##########################
###########################################################################
setAttr( hou.ParmTemplateGroup, "Node", property( hou.ParmTemplateGroup.sourceNode ) )

setAttr( hou.ParmTemplateGroup, "Nodetype", property( hou.ParmTemplateGroup.sourceNodeType ) )








