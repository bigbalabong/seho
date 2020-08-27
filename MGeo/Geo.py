'''
Tier: Base
'''

from ..MVar import *





###########################################################################
################################# Geometry ################################
###########################################################################
'''
hou.Geometry        https://www.sidefx.com/docs/houdini/hom/hou/Geometry.html
'''

setAttr( hou.Geometry, 'Node', property( hou.Geometry.sopNode ) )




# ======================================================== #
# ====================== Basic Info ====================== #
# ======================================================== #
def _geo_getMemory( self ):
    return self.intrinsicValue( 'memoryusage' )
setAttr( hou.Geometry, 'Memory', property( _geo_getMemory ) )





# ======================================================== #
# ========================= Count ======================== #
# ======================================================== #
def _geo_getNumPoints( self ):
    return self.intrinsicValue( 'pointcount' )
setAttr( hou.Geometry, 'NumPoints', property( _geo_getNumPoints ) )

def _geo_getNumVertices( self ):
    return self.intrinsicValue( 'vertexcount' )
setAttr( hou.Geometry, 'NumVertices', property( _geo_getNumVertices ) )

def _geo_getNumPrims( self ):
    return self.intrinsicValue( 'primitivecount' )
setAttr( hou.Geometry, 'NumPrims', property( _geo_getNumPrims ) )





# ======================================================== #
# ========================= Group ======================== #
# ======================================================== #
def _geo_getPointGroupNames( self ):
    return self.intrinsicValue( 'pointgroups' )
setAttr( hou.Geometry, 'PointGroupNames', property( _geo_getPointGroupNames ) )

def _geo_getVertexGroupNames( self ):
    return self.intrinsicValue( 'vertexgroups' )
setAttr( hou.Geometry, 'VertexGroupNames', property( _geo_getVertexGroupNames ) )

def _geo_getEdgeGroupNames( self ):
    return self.intrinsicValue( 'edgegroups' )
setAttr( hou.Geometry, 'EdgeGroupNames', property( _geo_getEdgeGroupNames ) )

def _geo_getPrimGroupNames( self ):
    return self.intrinsicValue( 'primitivegroups' )
setAttr( hou.Geometry, 'PrimGroupNames', property( _geo_getPrimGroupNames ) )








# ======================================================== #
# ===================== Bounding Box ===================== #
# ======================================================== #
setAttr( hou.Geometry, 'Bound', property( hou.Geometry.boundingBox ) )
setAttr( hou.Geometry, 'BB', hou.Geometry.Bound )







# ======================================================== #
# ======================= Material ======================= #
# ======================================================== #
def _geo_getMaterialPaths( self ):
    mat_attr = self.primAttr('shop_materialpath')
    if not mat_attr:
        return None
    else:
        return mat_attr.Strings
setAttr( hou.Geometry, 'MaterialPaths', property( _geo_getMaterialPaths ) )
setAttr( hou.Geometry, 'MatPaths', hou.Geometry.MaterialPaths )


def _geo_getMaterials( self ):
    mat_paths = self.MaterialPaths
    if not mat_paths:
        return
    else:
        return [ hou.node(i) for i in mat_paths ]
setAttr( hou.Geometry, 'Materials', property( _geo_getMaterials ) )
setAttr( hou.Geometry, 'Mats', hou.Geometry.Materials )








###########################################################################
################################## Point ##################################
###########################################################################
setAttr( hou.Geometry, 'Points', property( hou.Geometry.points ) )


'''
hou.Point       https://www.sidefx.com/docs/houdini/hom/hou/Point.html
'''

setAttr( hou.Point, 'Geo', property( hou.Point.geometry ) )

setAttr( hou.Point, 'Index', property( hou.Point.number ) )

setAttr( hou.Point, 'P', property( hou.Point.position, hou.Point.setPosition ) )
setAttr( hou.Point, 'Weight', property( hou.Point.weight, hou.Point.setWeight ) )

setAttr( hou.Point, 'Vertices', property( hou.Point.vertices ) )
setAttr( hou.Point, 'Prims', property( hou.Point.prims ) )







###########################################################################
################################## Vertex #################################
###########################################################################
'''
hou.Vertex      https://www.sidefx.com/docs/houdini/hom/hou/Vertex.html
'''

setAttr( hou.Vertex, 'Geo', property( hou.Vertex.geometry ) )

setAttr( hou.Vertex, 'Index', property( hou.Vertex.number ) )
setAttr( hou.Vertex, 'LinearIndex', property( hou.Vertex.linearNumber ) )

setAttr( hou.Vertex, 'Point', property( hou.Vertex.point ) )
setAttr( hou.Vertex, 'Prim', property( hou.Vertex.prim ) )







###########################################################################
################################### Edge ##################################
###########################################################################
'''
hou.Edge        https://www.sidefx.com/docs/houdini/hom/hou/Edge.html
'''

setAttr( hou.Edge, 'Geo', property( hou.Edge.geometry ) )

setAttr( hou.Edge, 'Index', property( hou.Edge.edgeId ) )

setAttr( hou.Edge, 'Length', property( hou.Edge.length ) )

setAttr( hou.Edge, 'Points', property( hou.Edge.points ) )
setAttr( hou.Edge, 'Prims', property( hou.Edge.prims ) )








###########################################################################
################################ Primitive ################################
###########################################################################
setAttr( hou.Geometry, 'Prims', property( hou.Geometry.prims ) )


'''
hou.Prim        https://www.sidefx.com/docs/houdini/hom/hou/Prim.html
'''

setAttr( hou.Prim, 'Geo', property( hou.Prim.geometry ) )

setAttr( hou.Prim, 'BB', property( hou.Prim.boundingBox ) )

setAttr( hou.Prim, 'Groups', property( hou.Prim.groups ) )

setAttr( hou.Prim, 'Index', property( hou.Prim.number ) )

setAttr( hou.Prim, 'Type', property( hou.Prim.type ) )

setAttr( hou.Prim, 'Points', property( hou.Prim.points ) )
setAttr( hou.Prim, 'Vertices', property( hou.Prim.vertices ) )
setAttr( hou.Prim, 'NumVertices', property( hou.Prim.numVertices ) )










###########################################################################
#################################### UV ###################################
###########################################################################
'''
How do you get UV density and UV distortion as attributes?      https://forums.odforce.net/topic/25511-how-do-you-get-uv-density-and-uv-distortion-as-attributes/
'''










