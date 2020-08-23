'''
Tier: Base
'''

from ..MVar import *



def _node_destroyAndBreakConnections( self ):
    # delete node connections
    connections = self.OutputConnections
    for i in connections:
        i.destroy()
    
    # delete node
    self.destroy()
setAttr( hou.Node, 'destroyAndBreakConnections', _node_destroyAndBreakConnections )




# ======================================================== #
# ========================= Input ======================== #
# ======================================================== #
setAttr( hou.Node, "InputNodes", property( hou.Node.inputs ) )
setAttr( hou.Node, "Inputs", hou.Node.InputNodes )

setAttr( hou.Node, "InputNames", property( hou.Node.inputNames ) )
setAttr( hou.Node, "InputLabels", property( hou.Node.inputLabels ) )

def _node_getNumInputs( self ):
    """[summary]

    Returns:
        [int]: [description]

    Author: Sean
    """
    return len( self.Inputs )
setAttr( hou.Node, "NumInputs", property( _node_getNumInputs ) )


setAttr( hou.Node, "InputConnections", property( hou.Node.inputConnections ) )

def _node_getInputIndexesWithConnections( self ):
    """
    Returns:
        [list of int]: input indexes which have connections.

    Author: Sean
    """
    return [ i.DownstreamIndex for i in self.inputConnections() ]
setAttr( hou.Node, "InputIndexes", property( _node_getInputIndexesWithConnections ) )



@undoGroup
def _node_sortInputIndexes( self ):
    """
    Say, there're 5 inputs connectors with connections, which are input0, input1, input2, input3, input4.
    Then, disconnect input1 and input3.
    The remains won't change.
    So, there are 'gaps' now because input1, input3 connectors have no connections.
    If you want to move the latter ones forward to fill the empty connectors, try this method.

    Author: Sean
    """
    input_connections = self.InputConnections

    old_input_indexes = self.InputIndexes                       # e.g. [0, 2, 4]
    new_input_indexes = range( len(input_connections) )         # e.g. [0, 1, 2]

    for i in new_input_indexes:
        connection = input_connections[i]
        old_input_index = old_input_indexes[i]
        new_input_index = new_input_indexes[i]

        if old_input_index == new_input_index:
            continue


        # change input index of connection
        connection.DownstreamIndex = new_input_index            # redirect the connection plugging into input2 to input1
setAttr( hou.Node, 'sortInputIndexes', _node_sortInputIndexes )





def _node_getInput0( self ):
    """
    Returns:
        [hou.Node]: [description]

    Author: Sean
    """
    nodes = self.Inputs
    if nodes:
        return nodes[0]

def _node_getInput1( self ):
    """[summary]

    Returns:
        [hou.Node]: [description]

    Author: Sean
    """
    nodes = self.Inputs
    if len( nodes ) >= 2 :
        return nodes[1]

def _node_getInput2( self ):
    """[summary]

    Returns:
        [hou.Node]: [description]

    Author: Sean
    """
    nodes = self.Inputs
    if len( nodes ) >= 3 :
        return nodes[2]

def _node_getInput3( self ):
    """[summary]

    Returns:
        [hou.Node]: [description]

    Author: Sean
    """
    nodes = self.Inputs
    if len( nodes ) >= 4 :
        return nodes[3]

setAttr( hou.Node, "Input0", property( _node_getInput0 ) )
setAttr( hou.Node, "Input1", property( _node_getInput1 ) )
setAttr( hou.Node, "Input2", property( _node_getInput2 ) )
setAttr( hou.Node, "Input3", property( _node_getInput3 ) )




# ======================================================== #
# ======================== Output ======================== #
# ======================================================== #
setAttr( hou.Node, "OutputNodes", property( hou.Node.outputs ) )
setAttr( hou.Node, "Outputs", hou.Node.OutputNodes )

setAttr( hou.Node, "OutputNames", property( hou.Node.outputNames ) )
setAttr( hou.Node, "OutputLabels", property( hou.Node.outputLabels ) )


def _node_getNumOutputs( self ):
    """[summary]

    Returns:
        [int]: [description]

    Author: Sean
    """
    return len( self.Outputs )
setAttr( hou.Node, "NumOutputs", property( _node_getNumOutputs ) )



setAttr( hou.Node, "OutputConnections", property( hou.Node.outputConnections ) )






# ======================================================== #
# =============== Input / Output Connector =============== #
# ======================================================== #

class NodePort( object ):

    """
    Author: Sean
    """

    def __init__( self, node, index ):
        """
        This class is aim for create connections between nodes more easily.

        Args:
            node (hou.Node): [description]
            index (int): Index of connector on node.
                        NOTE: This number should not be out of range.

        Example 1:
            a, b = seho.lss()
            a.Out1 >> b.In0

        Author: Sean
        """
        self.Node = node
        self.Index = index

    def __rshift__( self, target ):
        """
        Args:
            target (NodePort / str): Connect nodes, or create a new ouptut node.

        Author: Sean
        """
        # connect node
        if type( target ) is self.__class__:
            target.Node.setInput( target.Index, self.Node, self.Index )

        # create new output node
        elif type( target ) is str:
            new_node = self.Node.createOutputNode( target )
            self >> NodePort( new_node, 0 )
            return new_node

        # create new output node and rename
        elif type( target ) is tuple and type( target[0] ) is str:
            nodetype, name = target
            new_node = self.Node.createOutputNode( nodetype )
            self >> NodePort( new_node, 0 )
            new_node.Name = name
            return new_node

    def __lshift__( self, source ):
        """
        Args:
            source (NodePort): [description]

        Author: Sean
        """
        self.Node.setInput( self.Index, source.node, source.Index )

    def __floordiv__( self, target ):
        """
        Args:
            target (NodePort): [description]

        Author: Sean
        """
        target.Node.setInput( target.Index, None, 0 )


def _node_input0( self ):
    return NodePort( self, 0 )

def _node_input1( self ):
    return NodePort( self, 1 )

def _node_input2( self ):
    return NodePort( self, 2 )

def _node_input3( self ):
    return NodePort( self, 3 )

def _node_input4( self ):
    return NodePort( self, 4 )

def _node_input5( self ):
    return NodePort( self, 5 )

def _node_input6( self ):
    return NodePort( self, 6 )

def _node_input7( self ):
    return NodePort( self, 7 )

def _node_input8( self ):
    return NodePort( self, 8 )

def _node_input9( self ):
    return NodePort( self, 9 )

def _node_input10( self ):
    return NodePort( self, 10 )

def _node_input11( self ):
    return NodePort( self, 11 )

def _node_input12( self ):
    return NodePort( self, 12 )

def _node_input13( self ):
    return NodePort( self, 13 )

def _node_input14( self ):
    return NodePort( self, 14 )

def _node_input15( self ):
    return NodePort( self, 15 )

def _node_input16( self ):
    return NodePort( self, 16 )

def _node_input17( self ):
    return NodePort( self, 17 )

def _node_input18( self ):
    return NodePort( self, 18 )

def _node_input19( self ):
    return NodePort( self, 19 )

def _node_input20( self ):
    return NodePort( self, 20 )

def _node_input21( self ):
    return NodePort( self, 21 )

def _node_input22( self ):
    return NodePort( self, 22 )

def _node_input23( self ):
    return NodePort( self, 23 )

def _node_input24( self ):
    return NodePort( self, 24 )

setAttr( hou.Node, "In0", property( _node_input0 ) )
setAttr( hou.Node, "In1", property( _node_input1 ) )
setAttr( hou.Node, "In2", property( _node_input2 ) )
setAttr( hou.Node, "In3", property( _node_input3 ) )
setAttr( hou.Node, "In4", property( _node_input4 ) )
setAttr( hou.Node, "In5", property( _node_input5 ) )
setAttr( hou.Node, "In6", property( _node_input6 ) )
setAttr( hou.Node, "In7", property( _node_input7 ) )
setAttr( hou.Node, "In8", property( _node_input8 ) )
setAttr( hou.Node, "In9", property( _node_input9 ) )
setAttr( hou.Node, "In10", property( _node_input10 ) )
setAttr( hou.Node, "In11", property( _node_input11 ) )
setAttr( hou.Node, "In12", property( _node_input12 ) )
setAttr( hou.Node, "In13", property( _node_input13 ) )
setAttr( hou.Node, "In14", property( _node_input14 ) )
setAttr( hou.Node, "In15", property( _node_input15 ) )
setAttr( hou.Node, "In16", property( _node_input16 ) )
setAttr( hou.Node, "In17", property( _node_input17 ) )
setAttr( hou.Node, "In18", property( _node_input18 ) )
setAttr( hou.Node, "In19", property( _node_input19 ) )
setAttr( hou.Node, "In20", property( _node_input20 ) )
setAttr( hou.Node, "In21", property( _node_input21 ) )
setAttr( hou.Node, "In22", property( _node_input22 ) )
setAttr( hou.Node, "In23", property( _node_input23 ) )
setAttr( hou.Node, "In24", property( _node_input24 ) )



def _node_output0( self ):
    return NodePort( self, 0 )

def _node_output1( self ):
    return NodePort( self, 1 )

def _node_output2( self ):
    return NodePort( self, 2 )

def _node_output3( self ):
    return NodePort( self, 3 )

def _node_output4( self ):
    return NodePort( self, 4 )

def _node_output5( self ):
    return NodePort( self, 5 )

def _node_output6( self ):
    return NodePort( self, 6 )

def _node_output7( self ):
    return NodePort( self, 7 )

def _node_output8( self ):
    return NodePort( self, 8 )

def _node_output9( self ):
    return NodePort( self, 9 )

def _node_output10( self ):
    return NodePort( self, 10 )

def _node_output11( self ):
    return NodePort( self, 11 )

def _node_output12( self ):
    return NodePort( self, 12 )

def _node_output13( self ):
    return NodePort( self, 13 )

def _node_output14( self ):
    return NodePort( self, 14 )

def _node_output15( self ):
    return NodePort( self, 15 )

def _node_output16( self ):
    return NodePort( self, 16 )

def _node_output17( self ):
    return NodePort( self, 17 )

def _node_output18( self ):
    return NodePort( self, 18 )

def _node_output19( self ):
    return NodePort( self, 19 )

def _node_output20( self ):
    return NodePort( self, 20 )

def _node_output21( self ):
    return NodePort( self, 21 )

def _node_output22( self ):
    return NodePort( self, 22 )

def _node_output23( self ):
    return NodePort( self, 23 )

def _node_output24( self ):
    return NodePort( self, 24 )

setAttr( hou.Node, "Out0", property( _node_output0 ) )
setAttr( hou.Node, "Out1", property( _node_output1 ) )
setAttr( hou.Node, "Out2", property( _node_output2 ) )
setAttr( hou.Node, "Out3", property( _node_output3 ) )
setAttr( hou.Node, "Out4", property( _node_output4 ) )
setAttr( hou.Node, "Out5", property( _node_output5 ) )
setAttr( hou.Node, "Out6", property( _node_output6 ) )
setAttr( hou.Node, "Out7", property( _node_output7 ) )
setAttr( hou.Node, "Out8", property( _node_output8 ) )
setAttr( hou.Node, "Out9", property( _node_output9 ) )
setAttr( hou.Node, "Out10", property( _node_output10 ) )
setAttr( hou.Node, "Out11", property( _node_output11 ) )
setAttr( hou.Node, "Out12", property( _node_output12 ) )
setAttr( hou.Node, "Out13", property( _node_output13 ) )
setAttr( hou.Node, "Out14", property( _node_output14 ) )
setAttr( hou.Node, "Out15", property( _node_output15 ) )
setAttr( hou.Node, "Out16", property( _node_output16 ) )
setAttr( hou.Node, "Out17", property( _node_output17 ) )
setAttr( hou.Node, "Out18", property( _node_output18 ) )
setAttr( hou.Node, "Out19", property( _node_output19 ) )
setAttr( hou.Node, "Out20", property( _node_output20 ) )
setAttr( hou.Node, "Out21", property( _node_output21 ) )
setAttr( hou.Node, "Out22", property( _node_output22 ) )
setAttr( hou.Node, "Out23", property( _node_output23 ) )
setAttr( hou.Node, "Out24", property( _node_output24 ) )





###########################################################################
############################# Node Connection #############################
###########################################################################
'''
hou.NodeConnection      https://www.sidefx.com/docs/houdini/hom/hou/NodeConnection.html
'''

setAttr( hou.NodeConnection, "Upstream", property( hou.NodeConnection.inputNode ) )
setAttr( hou.NodeConnection, "Downstream", property( hou.NodeConnection.outputNode ) )



def _nodeConnection_setUpstreamIndex( self, index ):
    """[summary]

    Args:
        index (int): [description]

    Author: Sean
    """
    self.Downstream.setInput( self.DownstreamIndex, self.Upstream, index )
setAttr( hou.NodeConnection, "UpstreamIndex", 
            property( hou.NodeConnection.outputIndex, _nodeConnection_setUpstreamIndex ) )

def _nodeConnection_setDownstreamIndex( self, index ):
    """[summary]

    Args:
        index ([type]): [description]

    Author: Sean
    """
    # delete current connection
    self.Downstream.setInput( self.DownstreamIndex, None )

    # create new connection
    self.Downstream.setInput( index, self.Upstream, self.UpstreamIndex )
setAttr( hou.NodeConnection, "DownstreamIndex", 
            property( hou.NodeConnection.inputIndex, _nodeConnection_setDownstreamIndex ) )



def _nodeConnection_getUpstreamPort( self ):
    """[summary]

    Returns:
        [type]: [description]
    
    Author: Sean
    """
    index = self.UpstreamIndex
    port = 'In{}'.format( index )
    port = getattr( self.Upstream, port )
    return port
setAttr( hou.NodeConnection, "UpstreamPort", property( _nodeConnection_getUpstreamPort ), replace=False )

def _nodeConnection_getDownstreamPort( self ):
    """[summary]

    Returns:
        [type]: [description]
    
    Author: Sean
    """
    index = self.DownstreamIndex
    port = 'Out{}'.format( index )
    port = getattr( self.Downstream, port )
    return port
setAttr( hou.NodeConnection, "DownstreamPort", property( _nodeConnection_getDownstreamPort ), replace=False )



setAttr( hou.NodeConnection, "UpstreamName", property( hou.NodeConnection.inputName ) )
setAttr( hou.NodeConnection, "DownstreamName", property( hou.NodeConnection.outputName ) )


setAttr( hou.NodeConnection, "UpstreamLabel", property( hou.NodeConnection.inputLabel ) )
setAttr( hou.NodeConnection, "DownstreamLabel", property( hou.NodeConnection.outputLabel ) )



def _nodeConnection_destroy( self ):
    """
    Author: Sean
    """
    node = self.Downstream
    index = self.DownstreamIndex
    node.setInput( index, None )
setAttr( hou.NodeConnection, 'destroy', _nodeConnection_destroy )









