'''
Tier: Base
'''

from ..MVar import *




###########################################################################
################################## Basics #################################
###########################################################################
setAttr( hou.NetworkMovableItem, "Parent", property( hou.NetworkMovableItem.parent ) )

def _node_getParents( self ):
    """
    Returns:
        [list of hou.Node]: all parents of this node.

    Examples:
        hou.node('/obj/geo1/testgeometry_rubbertoy1/xform1').Parents
        # Returns: [<hou.Node at />, 
        #           <hou.Node at /obj>, 
        #           <hou.ObjNode of type geo at /obj/geo1>, 
        #           <hou.SopNode of type testgeometry_rubbertoy at /obj/geo1/testgeometry_rubbertoy1>]
    """
    parent = self.Parent
    parents = [ parent ]

    while parent:
        parent = parent.Parent
        if parent:
            parents.append( parent )

    # reverse order
    parents = parents[::-1]

    return parents    
setAttr( hou.NetworkMovableItem, "Parents", property( _node_getParents ) )



def _node_getChildren( self ):
    """
    Why this function:
        If this node is not a network, directly calling allItems() will lead to OperationFailed.
        ( OperationFailed: The attempted operation failed.
        This node is not a network. )

    Returns:
        [tuple of hou.NetworkMovableItem]
    """
    if self.isNetwork():
        return self.allItems()
    else:
        return ()
setAttr( hou.Node, "Children", property( _node_getChildren ) )

def _node_getAllChildren( self ):
    children = self.Children
    nodes = self.Nodes

    if nodes:
        for node in nodes:
            children += node.AllChildren

    return children
setAttr( hou.Node, "AllChildren", property( _node_getAllChildren ) )



setAttr( hou.Node, "Nodes", property( hou.Node.children ) )
setAttr( hou.Node, "AllNodes", property( hou.Node.allSubChildren ) )

def _node_allNodes():
    """
    Returns:
        [list of hou.Node]: all nodes in a Houdini HIP file.
    """
    return hou.node('/').allSubChildren()
setAttr( hou.Node, "allNodes", staticmethod( _node_allNodes ) )



def _node_getOpenedNetworks( self ):
    """
    Returns all opened networks, including subnet, unlocked HDA.
    """
    networks = [ i for i in self.Nodes if i.isNetwork() ]
    networks = [ i for i in networks if not i.isLockedHDA() ]
    return networks
setAttr( hou.Node, "OpenedNetworks", property( _node_getOpenedNetworks ) )

def _node_getAllOpenedNetworks( self ):
    networks = [ i for i in self.AllNodes if i.isNetwork() ]
    networks = [ i for i in networks if not i.isLockedHDA() ]
    return networks
setAttr( hou.Node, "AllOpenedNetworks", property( _node_getAllOpenedNetworks ) )




# ======================================================== #
# ========================== VOP ========================= #
# ======================================================== #
def _node_getParmVOPs( self ):
    if self.childTypeCategory().Name == 'Vop':
        return [ i for i in self.Nodes if i.Type.CateName == 'Vop/parameter' ]
setAttr( hou.Node, "VOPs_parameter", property( _node_getParmVOPs ) )


def _node_getSubinputVOPs( self ):
    if self.childTypeCategory().Name == 'Vop':
        return [ i for i in self.Nodes if i.Type.CateName == 'Vop/subinput' ]
setAttr( hou.Node, "VOPs_subinput", property( _node_getParmVOPs ) )






# ======================================================== #
# ========================== HDA ========================= #
# ======================================================== #
def _node_getHDAs( self, author=None ):
    nodes = [ i for i in self.Nodes if i.isHDA() ]
    return nodes
setAttr( hou.Node, "HDAs", property( _node_getHDAs ) )
setAttr( hou.Node, 'getHDAs', _node_getHDAs )

def _node_getAllHDAs( self, author=None ):
    nodes = [ i for i in self.AllNodes if i.isHDA() ]
    return nodes
setAttr( hou.Node, "AllHDAs", property( _node_getAllHDAs ) )
setAttr( hou.Node, 'getAllHDAs', _node_getAllHDAs )

def _node_getLockedHDAs( self ):
    nodes = [ i for i in self.HDAs if i.isLockedHDA() ]
    return nodes
setAttr( hou.Node, "LockedHDAs", property( _node_getLockedHDAs ) )

def _node_getAllLockedHDAs( self ):
    nodes = [ i for i in self.AllHDAs if i.isLockedHDA() ]
    return nodes
setAttr( hou.Node, "AllLockedHDAs", property( _node_getAllLockedHDAs ) )

def _node_getUnlockedHDAs( self ):
    nodes = [ i for i in self.HDAs if not i.isLockedHDA() ]
    return nodes
setAttr( hou.Node, "UnlockedHDAs", property( _node_getUnlockedHDAs ) )

def _node_getAllUnlockedHDAs( self ):
    nodes = [ i for i in self.AllHDAs if not i.isLockedHDA() ]
    return nodes
setAttr( hou.Node, "AllUnlockedHDAs", property( _node_getAllUnlockedHDAs ) )





# ======================================================== #
# ====================== Sticky Note ===================== #
# ======================================================== #
def _node_getNotes( self ):
    return [ i for i in self.Children if isinstance(i, hou.StickyNote) ]
setAttr( hou.Node, "Notes", property( _node_getNotes ) )

def _node_getAllNotes( self ):
    return [ i for i in self.AllChildren if isinstance(i, hou.StickyNote) ]
setAttr( hou.Node, "AllNotes", property( _node_getAllNotes ) )





# ======================================================== #
# ====================== Network Box ===================== #
# ======================================================== #
def _node_getNetworkBoxs( self ):
    return [ i for i in self.Children if isinstance(i, hou.NetworkBox) ]
setAttr( hou.Node, "NetworkBoxs", property( _node_getNetworkBoxs ) )

def _node_getAllNetworkBoxs( self ):
    return [ i for i in self.AllChildren if isinstance(i, hou.NetworkBox) ]
setAttr( hou.Node, "AllNetworkBoxs", property( _node_getAllNetworkBoxs ) )


def _networkBox_getNodes( self ):
    return self.nodes()
setAttr( hou.NetworkBox, "Nodes", property( _networkBox_getNodes ) )

def _networkBox_getAllNodes( self ):
    return self.nodes( recurse=True )
setAttr( hou.NetworkBox, "AllNodes", property( _networkBox_getAllNodes ) )


def _networkBox_getOutputNodes( self ):
    output_nodes = [ i for i in self.Nodes if i.Type.Name == 'output' ]
    return output_nodes
setAttr( hou.NetworkBox, "OutputNodes", property( _networkBox_getOutputNodes ) )









###########################################################################
########################### Collection by Types ###########################
###########################################################################

# ~~~~~~~~~~~~~~~~~ Basics ~~~~~~~~~~~~~~~~ #
def _node_getNodesByType( self, nodetypes ):
    """
    Args:
        nodetype (list of hou.NodeType / list of str): [description]

    Returns:
        [list of hou.Node]: [description]
    """
    if isinstance( nodetypes[0], str ):
        nodetypes = [ hou.NodeType.nodetype(i) for i in nodetypes ]
    
    nodes = [ i for i in self.Nodes if i.Type in nodetypes ]

    return nodes
setAttr( hou.Node, 'getNodesByType', _node_getNodesByType )

def _node_getAllNodesByType( self, nodetypes ):
    """
    Args:
        nodetype (list of hou.NodeType / list of str): [description]

    Returns:
        [list of hou.Node]: [description]
    """
    # convert str to hou.NodeType
    if isinstance( nodetypes[0], str ):
        nodetypes = [ hou.NodeType.nodetype(i) for i in nodetypes ]


    # get nodes
    nodes = [ i for i in self.AllNodes if i.Type in nodetypes ]

    if not nodes:
        return nodes        # empty list


    # get hierarchy
    for node in nodes:
        node._Parent = self
    getHierarchyofNodes( nodes )

    return nodes
setAttr( hou.Node, 'getAllNodesByType', _node_getAllNodesByType, replace=False )

def getHierarchyofNodes( nodes ):
    # initialize attriubte "_Parent" if necessary
    if '_Parent' not in dir( nodes[0] ):
        for i in nodes:
            i._Parent = ROOT


    # get hierarchy
    for node in nodes:
        _parents = node.Parents

        for i in nodes:
            if i == node:
                continue

            if i in _parents:

                # if i is closer to current context in hierachies
                if node._Parent in i.Parents:
                    node._Parent = i    



# ~~~~~~~~~~~~~~~~~ Types ~~~~~~~~~~~~~~~~~ #
def _node_getAllWrangleOps( self ):
    nodetypes = hou.NodeType.getAll( keywords=('wrangle',) )
    nodes = self.getAllNodesByType( nodetypes )
    return nodes
setAttr( hou.Node, "AllWrangleOps", property( _node_getAllWrangleOps ) )

def _node_getAllOpenCLOps( self ):
    nodetypes = hou.NodeType.getAll( keywords=('opencl',) )
    nodes = self.getAllNodesByType( nodetypes )
    return nodes
setAttr( hou.Node, "AllOpenCLOps", property( _node_getAllOpenCLOps ) )

def _node_getAllScriptOps( self ):
    nodetypes = hou.NodeType.getAll( keywords=('python', 'unix') )
    nodes = self.getAllNodesByType( nodetypes )
    return nodes
setAttr( hou.Node, "AllScriptOps", property( _node_getAllScriptOps ) )




def _node_getAllTimeOps( self ):
    nodetypes = hou.NodeType.getAll( keywords=('time',) )
    nodes = self.getAllNodesByType( nodetypes )
    return nodes
setAttr( hou.Node, "AllTimeOps", property( _node_getAllTimeOps ) )


def _node_getAllNoiseOps( self ):
    nodetypes = hou.NodeType.getAll( keywords=('noise',) )
    nodes = self.getAllNodesByType( nodetypes )
    return nodes
setAttr( hou.Node, "AllNoiseOps", property( _node_getAllNoiseOps ) )


def _node_getAllSolverOps( self ):
    # nodetypes = hou.NodeType.getAll( keywords=('solver',) )
    # nodes = self.getAllNodesByType( nodetypes )
    nodes = self.getAllNodesByType( hou.NodeType.Occupation.Solver )
    return nodes
setAttr( hou.Node, "AllSolverOps", property( _node_getAllSolverOps ) )


def _node_getAllContexts( self ):
    nodetypes = L_( hou.NodeType.Occupation.Context.values() ).sum()
    nodetypes = hou.NodeType.getAll( keywords=nodetypes )
    nodes = self.getAllNodesByType( nodetypes )
    return nodes
setAttr( hou.Node, "AllContextOps", property( _node_getAllContexts ) )


def _node_getAllCacheOps( self ):
    nodetypes = hou.NodeType.getAll( keywords=('file', 'cache', 'alembic', 'fbx', 'gltf') )
    nodes = self.getAllNodesByType( nodetypes )
    return nodes
setAttr( hou.Node, "AllCacheOps", property( _node_getAllCacheOps ) )


def _node_getAllRendererOps( self ):
    nodetypes = hou.NodeType.getAll( keywords=('mantra', 'arnold', 'renderman', 'redshift') )
    nodes = self.getAllNodesByType( nodetypes )
    return nodes
setAttr( hou.Node, "AllRendererOps", property( _node_getAllRendererOps ) )




def _node_getAllKeyOps( self ):
    nodes = self.getAllNodesByType( hou.NodeType.Occupation.Key )
    return nodes
setAttr( hou.Node, "AllKeyOps", property( _node_getAllKeyOps ) )

def _node_getAllDeprecatedNodes( self ):
    nodes = self.getAllNodesByType( hou.NodeType.Occupation.Deprecated )
    return nodes
setAttr( hou.Node, "AllDeprecatedOps", property( _node_getAllDeprecatedNodes ) )







