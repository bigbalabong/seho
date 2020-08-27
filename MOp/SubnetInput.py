'''
Tier: Base
'''

from ..MVar import *





setAttr( hou.SubnetIndirectInput, 'Index', property( hou.SubnetIndirectInput.number ) )



def _subnetInput_createNull( self, extra_dot=True ):
    root = self.Parent

    # new null
    name = 'subnet_input_{}'.format( self.Index )
    null = root.createNode( 'null', name )
    null.P = self.P + nPy *1
    null.Shape = 'chevron_down'
    null.setInput( 0, self, 0 )

    # new dot
    # dot = root.createNetworkDot()
    # dot.P = null.P + nPy *1 + nPx *0.3
    # dot.Pinned = True
    # dot.setInput( 0, null, 0 )
setAttr( hou.SubnetIndirectInput, 'createNull', _subnetInput_createNull, replace=True )







