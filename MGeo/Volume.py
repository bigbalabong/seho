'''
Tier: Base
'''

from ..MVar import *






###########################################################################
################################## Volume #################################
###########################################################################
def _geo_getVolumes( self ):
    node = self.Node

    prims = [ i for i in self.Prims if type(i) is hou.Volume ]

    for i in prims:
        i.Node = node

    return prims
setAttr( hou.Geometry, 'Volumes', property( _geo_getVolumes ) )


'''
hou.Volume      http://www.sidefx.com/docs/houdini/hom/hou/Volume.html
'''

setAttr( hou.Volume, 'Res', property( hou.Volume.resolution ) )


setAttr( hou.Volume, 'Transform', property( hou.Volume.transform, hou.Volume.setTransform ) )


def _volume_newCOP( self ):
    node = self.Node
    name = self['name'].Value

    copnet = node.Parent.createNode( 'cop2net' )
    copnet.P = node.P + nPx

    sop_import = copnet.createNode( 'sopimport', 'sopimport_{}'.format( name ) )
    sop_import['size'].Value = self.Res
setAttr( hou.Volume, 'newCOP', _volume_newCOP )







###########################################################################
################################### VDB ###################################
###########################################################################
def _geo_getVDBs( self ):
    node = self.Node

    prims = [ i for i in self.Prims if type(i) is hou.VDB ]

    for i in prims:
        i.Node = node

    return prims
setAttr( hou.Geometry, 'Volumes', property( _geo_getVDBs ) )


'''
hou.VDB         http://www.sidefx.com/docs/houdini/hom/hou/VDB.html
'''

setAttr( hou.VDB, 'Res', property( hou.VDB.resolution ) )


setAttr( hou.VDB, 'Transform', property( hou.VDB.transform ) )






