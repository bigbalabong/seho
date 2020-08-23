'''
Tier: Base
'''

from ..MVar import *


class NodeComment( object ):

    def __init__( self, node ):
        self.Node = node


    @property
    def Data( self ):
        return self.Node.comment()

    @Data.setter
    def Data( self, comment ):
        '''
        PARMS:
                comment (str)
        '''
        self.Node.setComment( comment )
    

    def show( self ):
        self.Node.setGenericFlag( hou.nodeFlag.DisplayComment, True )

    def hide( self ):
        self.Node.setGenericFlag( hou.nodeFlag.DisplayComment, False )



def _node_getComment( self ):
    return NodeComment( self )
setAttr( hou.Node, "Comment", property( _node_getComment ) )





