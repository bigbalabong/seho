'''
Tier: Base
'''

from ..MVar import *





###########################################################################
################################## Group ##################################
###########################################################################
'''
Vertex-edge Group       https://www.sidefx.com/docs/houdini/nodes/sop/uvflatten.html#vedges
'''
setAttr( hou.Geometry, "PointGroups", property( hou.Geometry.pointGroups ) )
setAttr( hou.Geometry, "EdgeGroups", property( hou.Geometry.edgeGroups ) )
setAttr( hou.Geometry, "PrimGroups", property( hou.Geometry.primGroups ) )


def _geo_pointGroupNames( self ):
    return [ i.name() for i in self.pointGroups() ]
setAttr( hou.Geometry, "PointGroupNames", property( _geo_pointGroupNames ) )

def _geo_edgeGroupNames( self ):
    return [ i.name() for i in self.edgeGroups() ]
setAttr( hou.Geometry, "EdgeGroupNames", property( _geo_edgeGroupNames ) )

def _geo_primGroupNames( self ):
    return [ i.name() for i in self.primGroups() ]
setAttr( hou.Geometry, "PrimGroupNames", property( _geo_primGroupNames ) )



def _geo_pointGroup( self, name ):
    return self.findPointGroup( name )
setAttr( hou.Geometry, 'pointGroup', _geo_pointGroup )

def _geo_vertexGroup( self, name ):
    return self.findVertexGroup( name )
setAttr( hou.Geometry, 'vertexGroup', _geo_vertexGroup )

def _geo_edgeGroup( self, name ):
    return self.findEdgeGroup( name )
setAttr( hou.Geometry, 'edgeGroup', _geo_edgeGroup )

def _geo_primGroup( self, name ):
    return self.findPrimGroup( name )
setAttr( hou.Geometry, 'primGroup', _geo_primGroup )



def _geo_newPointGrp( self, name, is_ordered=False ):
    self.createPointGroup( name, is_ordered )
setAttr( hou.Geometry, 'newPointGrp', _geo_newPointGrp )

def _geo_newEdgeGrp( self, name ):
    self.createEdgeGroup( name )
setAttr( hou.Geometry, 'newEdgeGrp', _geo_newEdgeGrp )

def _geo_newPrimGrp( self, name, is_ordered=False ):
    self.createPrimGroup( name, is_ordered )
setAttr( hou.Geometry, 'newPrimGrp', _geo_newPrimGrp )



def _geo_splitByGroups( self, names=None, type_='prim' ):
    '''
    PARMS:
            groups (str)
            type (str)  -  'point' / 'edge' / 'prim'
    '''
    # pre-processing arguments
    names = L_(names).list_


    # get all group names
    if type_ == 'point':
        all_groups = self.PointGroupNames
    elif type_ == 'edge':
        all_groups = self.EdgeGroupNames
    else: # type_ == 'prim':
        all_groups = self.PrimGroupNames


    if not names:
        groups = all_groups
    else:
        # get specific groups
        groups = []
        for name in names:
            groups += [ i for i in all_groups if re.match( name, i ) ]


    # create blast sop
    root = self.Node.Parent
    last_node = self.Node
    nPx = autoNPx( all_groups )
    total_width = nPx * len(all_groups)
    for i, group in enumerate( all_groups ):
        position = last_node.P + nPx + nPy*(i==0) - total_width/2*(i==0)
        new_blast = root.newNode( node_type_name='blast', node_name=group, position=position )

        new_blast.setNextInput( self.Node )
        new_blast.parm('group').set( group )
        new_blast.parm('grouptype').set( Grouptypes[type_] )
        new_blast.parm('negate').set(True)
        
        last_node = new_blast
setAttr( hou.Geometry, 'splitByGroups', _geo_splitByGroups )







###########################################################################
############################### Point Group ###############################
###########################################################################
'''
hou.PointGroup      http://www.sidefx.com/docs/houdini/hom/hou/PointGroup.html
'''

# ~~~~~~~~~~~~~~~~~ Basic ~~~~~~~~~~~~~~~~~ #
setAttr( hou.PointGroup, "Name", property( hou.PointGroup.name ) )


setAttr( hou.PointGroup, "Geo", property( hou.PointGroup.geometry ) )

setAttr( hou.PointGroup, "Points", property( hou.PointGroup.points ) )
setAttr( hou.PointGroup, 'Items', hou.PointGroup.Points )





###########################################################################
############################### Vertex Group ##############################
###########################################################################
'''
hou.VertexGroup     http://www.sidefx.com/docs/houdini/hom/hou/VertexGroup.html
'''

# ~~~~~~~~~~~~~~~~~ Basic ~~~~~~~~~~~~~~~~~ #
setAttr( hou.VertexGroup, "Name", property( hou.VertexGroup.name ) )



setAttr( hou.VertexGroup, "Geo", property( hou.VertexGroup.geometry ) )

setAttr( hou.VertexGroup, "Vertices", property( hou.VertexGroup.vertices ) )
setAttr( hou.VertexGroup, 'Items', hou.VertexGroup.Vertices )







###########################################################################
################################ Edge Group ###############################
###########################################################################
'''
hou.EdgeGroup       http://www.sidefx.com/docs/houdini/hom/hou/EdgeGroup.html
'''

# ~~~~~~~~~~~~~~~~~ Basic ~~~~~~~~~~~~~~~~~ #
setAttr( hou.EdgeGroup, "Name", property( hou.EdgeGroup.name ) )


setAttr( hou.EdgeGroup, "Geo", property( hou.EdgeGroup.geometry ) )

setAttr( hou.EdgeGroup, "Edges", property( hou.EdgeGroup.edges ) )
setAttr( hou.EdgeGroup, 'Items',hou.EdgeGroup.Edges  )






###########################################################################
############################# Primitive Group #############################
###########################################################################
'''
hou.PrimGroup       http://www.sidefx.com/docs/houdini/hom/hou/PrimGroup.html
'''

# ~~~~~~~~~~~~~~~~~ Basic ~~~~~~~~~~~~~~~~~ #
setAttr( hou.PrimGroup, "Name", property( hou.PrimGroup.name ) )


setAttr( hou.PrimGroup, "Geo", property( hou.PrimGroup.geometry ) )

setAttr( hou.PrimGroup, "Prims", property( hou.PrimGroup.prims ) )
setAttr( hou.PrimGroup, 'Items', hou.PrimGroup.Prims )






