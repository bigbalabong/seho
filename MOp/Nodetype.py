'''
Tier: Base
'''

from ..MVar import *




class NodetypeOccupation( object ):

    """
    Author: Sean
    """

    Context = {
            # The value is the name of nodetype.
            # You can create new context using hou.Node.createNode( 'objnet', 'objnet' )
            # The 1st arg is name of nodetype. The 2nd arg is name of new node.
            'obj':  ('objnet',),
            'mat':  ('matnet',),
            'shop': ('shopnet',),
            'lop':  ('lopnet',),
            'rop':  ('ropnet',),
            'cop':  ('cop2net',),
            'top':  ('topnet', 'topnetmgr'),
            'chop': ('chopnet',),
        }

    Deprecated = [
            'Sop/copy',     # Copy Stamp
            'Sop/delete',   # Delete
        ]


    Key = [
            'Sop/detangle',
            'Sop/windingnumber',
        ]

    Solver = [ 
            # ~~~~~~~~~~~~~~~ SOP Solver ~~~~~~~~~~~~~~ #
            'Sop/solver', 'Dop/sopsolver',

            # ~~~~~~~~~~~~~~~~~~ RBD ~~~~~~~~~~~~~~~~~~ #
            'Sop/rbdbulletsolver',

            # ~~~~~~~~~~~~~~~~~~ Pyro ~~~~~~~~~~~~~~~~~ #
            'Sop/pyrosolver',

            # ~~~~~~~~~~~~~~~~~~ FLIP ~~~~~~~~~~~~~~~~~ #


            # ~~~~~~~~~~~~~~~~~ Vellum ~~~~~~~~~~~~~~~~ #
            'Sop/vellumsolver',
        ]

    Stroke = [
            'Sop/stroke', 'Sop/drawcurve', 'Sop/guidegroom'
        ]

'rop_volume_texture', 'sop_terrain_segment_rop', 'sop_terrain_texture_rop',
'niagara_rop', 'rop_marmoset_export', 'rop_sketchfab', 
'rop_games_baker', 'rop_impostor_texture', 'rop_pyro_preview', 
'rop_csv_exporter', 'rop_motion_vectors', 'rop_texture_sheets',
'ropnet', 'rop_geometry', 'rop_vector_field',
'Geometry', 
'Wedge', 'HQueue Render'

setAttr( hou.NodeType, 'Occupation', NodetypeOccupation )





def _node_isContext( self ):
    """
    Shortcut to hou.NodeType.isContext()

    Author: Sean
    """
    return self.Type.isContext()
setAttr( hou.Node, 'isContext', _node_isContext )


def _node_openNotes( self ):
    """
    Author: Sean
    """
    nodetype = self.type()
    nodetype_name = nodetype.name()
    nodetype_cate = nodetype.category().name()


    if not nodetype.definition():
        logging.error( 'This node is note a HDA.' )
        return

    
    notes_filename = '[{}]{}'.format( nodetype_cate, '__'.join( nodetype.nameComponents()[1:]) )
    notes_filepath = '{}/{}.hda'.format( hda_notes_path, notes_filename )


    # if there's no notes file, create new one.
    if not os.path.exists( notes_filepath ):
        nodetypeNotes_bak( nodetype, notes_filepath )

    
    # install hda
    hou.hda.installFile( notes_filepath )

    # get nodetype inside specified hda file
    hda_definition = hou.hda.definitionsInFile( notes_filepath )[0]
    hda_nodetype = hda_definition.nodeType()


    # open notes
    notes_position = self.position() + hou.Vector2( node_pos_offset.x(), 0 )
    new_notes = self.parent().createNode( hda_nodetype.name() )
    new_notes.setPosition( notes_position )
    new_notes.setColor( nodeColor_dict['purple'] )
    new_notes.setUserData( 'nodeshape', "null" )
    new_notes.allowEditingOfContents()
    

    return new_notes
setAttr( hou.Node, 'openNotes', _node_openNotes )





###########################################################################
############################ Nodetype Category ############################
###########################################################################
'''
hou.NodeTypeCategory        http://www.sidefx.com/docs/houdini/hom/hou/NodeTypeCategory.html

Examples:
    hou.nodeTypeCategories()['Sop']
        <hou.NodeTypeCategory for Sop>
'''

# ======================================================== #
# ====================== Basic Info ====================== #
# ======================================================== #
setAttr( hou.NodeTypeCategory, "Name", property( hou.NodeTypeCategory.name ) )
setAttr( hou.NodeTypeCategory, "Label", property( hou.NodeTypeCategory.label ) )

def _nodetypeCate_nodetypes( self ):
    """
    Author: Sean
    """
    return self.nodeTypes().values()
setAttr( hou.NodeTypeCategory, "Nodetypes", property( _nodetypeCate_nodetypes ) )




# ======================================================== #
# ===================== All Nodetypes ==================== #
# ======================================================== #
def _nodetype_getNodetype( nodetype ):
    """
    Args:
        nodetype (str): [description]

    Returns:
        (hou.NodeType): The latest version.

    Author: Sean
    """
    nodetypes = [ i for i in hou.NodeType.getAll() if i.Name == nodetype or i.CateName == nodetype ]

    if nodetypes:
        nodetypes.sort( key=lambda x: x.Ver )
        return nodetypes[-1]
setAttr( hou.NodeType, "nodetype", staticmethod( _nodetype_getNodetype ) )


def _nodetype_getAllNodetypes( keywords=None, parms=None ):
    """
    Args:
        keywords (list of str): [description]

        parms (list of str): Names of parameters.

    Returns:
        [list of hou.NodeType]: all nodetypes which name contain the keyword.

    Examples:
        hou.NodeType.getAll()
        # Return all nodetypes.

        hou.NodeType.getAll( keywords=['python'] )
        # Return all nodetypes which name contain 'python'.

        hou.NodeType.getAll( keywords=['wrangle'], parms=['snippet'] )
        # Return all nodetypes which name contains 'wrangle', and has parm named as 'snippet'.
    
    Author: Sean
    """
    # get all nodetypes
    all_nodetypes = []

    for cate in hou.nodeTypeCategories().values():
        nodetypes = cate.Nodetypes
        nodetypes.sort( key=lambda x: x.Name.lower() )

        all_nodetypes += nodetypes


    if keywords is None:
        return all_nodetypes


    # get nodetypes by keywords of name
    nodetypes = []
    for keyword in keywords:
        nodetypes += [ i for i in all_nodetypes if keyword in i.Name.lower() ]


    # filter nodetypes by names of parms
    if parms:
        parms = set(parms)

        nodetypes = [ i for i in nodetypes if set([ j.Name for j in i.ParmTemplates ]) & parms ]


    # sort list by category
    nodetypes.sort( key = lambda x: x.CateName.lower() )

    return nodetypes
setAttr( hou.NodeType, "getAll", staticmethod( _nodetype_getAllNodetypes ) )

def _nodetype_getAllDeperacated():
    """
    Returns:
        [list of hou.NodeType]: all deprecated nodetypes.
    
    Author: Sean
    """
    nodetypes = hou.NodeType.getAll()
    deprecated = [ i for i in nodetypes if i.Deprecated ]
    return deprecated
setAttr( hou.NodeType, "getAllDeperacated", staticmethod( _nodetype_getAllDeperacated ) )


def _nodetype_getAllObjNodetypes():
    """
    Author: Sean
    """
    nodetypes = hou.nodeTypeCategories()['Object'].nodeTypes().values()
    nodetypes.sort( key=lambda x: x.Name.lower() )
    return nodetypes
setAttr( hou.NodeType, "AllObjNodetypes", property( _nodetype_getAllObjNodetypes ) )

def _nodetype_getAllSopNodetypes():
    """
    Author: Sean
    """
    nodetypes = hou.nodeTypeCategories()['Sop'].nodeTypes().values()
    nodetypes.sort( key=lambda x: x.Name.lower() )
    return nodetypes
setAttr( hou.NodeType, "AllSopNodetypes", property( _nodetype_getAllSopNodetypes ) )

def _nodetype_getAllShopNodetypes():
    """
    Author: Sean
    """
    nodetypes = hou.nodeTypeCategories()['Shop'].nodeTypes().values()
    nodetypes.sort( key=lambda x: x.Name.lower() )
    return nodetypes
setAttr( hou.NodeType, "AllShopNodetypes", property( _nodetype_getAllShopNodetypes ) )

def _nodetype_getAllCopNodetypes():
    """
    Author: Sean
    """
    nodetypes = hou.nodeTypeCategories()['Cop2'].nodeTypes().values()
    nodetypes.sort( key=lambda x: x.Name.lower() )
    return nodetypes
setAttr( hou.NodeType, "AllCopNodetypes", property( _nodetype_getAllCopNodetypes ) )

def _nodetype_getAllChopNodetypes():
    """
    Author: Sean
    """
    nodetypes = hou.nodeTypeCategories()['Chop'].nodeTypes().values()
    nodetypes.sort( key=lambda x: x.Name.lower() )
    return nodetypes
setAttr( hou.NodeType, "AllChopNodetypes", property( _nodetype_getAllChopNodetypes ) )

def _nodetype_getAllVopNodetypes():
    """
    Author: Sean
    """
    nodetypes = hou.nodeTypeCategories()['Vop'].nodeTypes().values()
    nodetypes.sort( key=lambda x: x.Name.lower() )
    return nodetypes
setAttr( hou.NodeType, "AllVopNodetypes", property( _nodetype_getAllVopNodetypes ) )

def _nodetype_getAllDopNodetypes():
    """
    Author: Sean
    """
    nodetypes = hou.nodeTypeCategories()['Dop'].nodeTypes().values()
    nodetypes.sort( key=lambda x: x.Name.lower() )
    return nodetypes
setAttr( hou.NodeType, "AllDopNodetypes", property( _nodetype_getAllDopNodetypes ) )

def _nodetype_getAllTopNodetypes():
    """
    Author: Sean
    """
    nodetypes = hou.nodeTypeCategories()['Top'].nodeTypes().values()
    nodetypes.sort( key=lambda x: x.Name.lower() )
    return nodetypes
setAttr( hou.NodeType, "AllTopNodetypes", property( _nodetype_getAllTopNodetypes ) )

def _nodetype_getAllLopNodetypes():
    """
    Author: Sean
    """
    nodetypes = hou.nodeTypeCategories()['Lop'].nodeTypes().values()
    nodetypes.sort( key=lambda x: x.Name.lower() )
    return nodetypes
setAttr( hou.NodeType, "AllLopNodetypes", property( _nodetype_getAllLopNodetypes ) )

def _nodetype_getAllRopNodetypes():
    """
    Author: Sean
    """
    nodetypes = hou.nodeTypeCategories()['Driver'].nodeTypes().values()
    nodetypes.sort( key=lambda x: x.Name.lower() )
    return nodetypes
setAttr( hou.NodeType, "AllRopNodetypes", property( _nodetype_getAllRopNodetypes ) )









###########################################################################
################################# Nodetype ################################
###########################################################################
'''
hou.NodeType            http://www.sidefx.com/docs/houdini/hom/hou/NodeType.html
'''

'''
All kinds of names.

Examples:

Labs Maps Baker (HDA)
    FullName        'labs::maps_baker::3.0'
    Name            'labs::maps_baker'
    LiteName        'maps_baker'

    CateFullName    'labs::Sop/maps_baker::3.0'
    CateName        'Sop/labs::maps_baker'
    CateName2       'Nodetype2_Sop_labs::maps_baker'
    CateLiteName    'Sop/maps_baker'

    Label           'Labs Maps Baker'

    Cate            <hou.NodeTypeCategory for Sop>

    Ver             3.0
    Vers            [<hou.SopNodeType for Sop labs::maps_baker>, 
                    <hou.SopNodeType for Sop labs::maps_baker::2.0>, 
                    <hou.SopNodeType for Sop labs::maps_baker::3.0>]
    VerLatest       <hou.SopNodeType for Sop labs::maps_baker::3.0>

    Namespace       'labs'
'''


# ======================================================== #
# ====================== Basic Info ====================== #
# ======================================================== #
setAttr( hou.NodeType, "FullName", property( hou.NodeType.name ) )

def _nodetype_name( self ):
    """
    Author: Sean
    """
    return '::'.join([ i for i in self.nameComponents()[:-1] if i ])
setAttr( hou.NodeType, "Name", property( _nodetype_name ) )

def _nodetype_litename( self ):
    """
    Author: Sean
    """
    return self.nameComponents()[2]
setAttr( hou.NodeType, "LiteName", property( _nodetype_litename ) )


def _nodetype_fullnameWithCategory( self ):
    '''
    EXAMPLES:
            # used to get nodetype
            hou.nodeType( ls().Type.CateFullName )
                RETURNS: <hou.SopNodeType for Sop tube>
    
    Author: Sean
    '''
    return self.nameWithCategory()
setAttr( hou.NodeType, "CateFullName", property( _nodetype_fullnameWithCategory ) )

def _nodetype_nameWithCategory( self ):
    """
    Author: Sean
    """
    return '{}/{}'.format( self.Cate.Name, self.Name )
setAttr( hou.NodeType, "CateName", property( _nodetype_nameWithCategory ) )

def _nodetype_nameWithCategory2( self ):
    """
    Author: Sean
    """
    return 'Nodetype2_' + self.CateName.replace('/', '_')
setAttr( hou.NodeType, "CateName2", property( _nodetype_nameWithCategory2 ) )

def _nodetype_litenameWithCategory( self ):
    """
    Author: Sean
    """
    return '{}/{}'.format( self.Cate.Name, self.LiteName )
setAttr( hou.NodeType, "CateLiteName", property( _nodetype_litenameWithCategory ) )


setAttr( hou.NodeType, "Label", property( hou.NodeType.description ) )


setAttr( hou.NodeType, "Cate", property( hou.NodeType.category ) )


def _nodetype_namespace( self ):
    """
    Author: Sean
    """
    return self.nameComponents()[1]
setAttr( hou.NodeType, "Namespace", property( _nodetype_namespace ) )


setAttr( hou.NodeType, "Icon", property( hou.NodeType.icon ) )



# ~~~~~~~~~~~~~~~~ Version ~~~~~~~~~~~~~~~~ #
def _nodetype_version( self ):
    """
    Author: Sean
    """
    version = self.nameComponents()[-1]

    if not version:
        version = 0.0
    else:
        version = float(version)

    return version
setAttr( hou.NodeType, "Ver", property( _nodetype_version ) )

def _nodetype_versions( self ):
    """
    Author: Sean
    """
    nodetype_name = self.Name

    all_nodetypes = self.Cate.Nodetypes
    all_versions = [ i for i in all_nodetypes if i.Name == nodetype_name ]
    all_versions.sort( key = lambda x: x.Ver )

    return all_versions

    # all_nodetypes_dict = {}
    # for i in all_nodetypes:
    #     nodetype_info = i.nameComponents()

    #     nodetype_name = '::'.join( nodetype_info[:-1] )

    #     ver = nodetype_info[-1]
    #     ver = float(ver) if ver else 0.0

    #     if nodetype_name not in all_nodetypes_dict.keys():
    #         all_nodetypes_dict[ nodetype_name ] = [ (i, ver) ]
    #     else:
    #         all_nodetypes_dict[ nodetype_name ].append( (i, ver) )



    # this_nodetype_vers = all_nodetypes_dict[ this_nodetype_name ]
    # this_nodetype_vers.sort( key = lambda x: x[1] )

    # last_version = this_nodetype_vers[-1]

    # if asDigits:
    #     return last_version[1]
    # else:
    #     return last_version[0]
setAttr( hou.NodeType, "Vers", property( _nodetype_versions ) )

def _nodetype_versionLatest( self ):
    """
    Author: Sean
    """
    return self.Vers[-1]
setAttr( hou.NodeType, "VerLatest", property( _nodetype_versionLatest ) )



# ~~~~~~~~~~~~~~~~~ State ~~~~~~~~~~~~~~~~~ #
setAttr( hou.NodeType, "Deprecated", property( hou.NodeType.deprecated ) )




# ~~~~~~~~~~~~~~~ Occupation ~~~~~~~~~~~~~~ #
# hou.NodeType.isGenerator

# hou.NodeType.isManager

def _nodetype_isContext( self ):
    """
    Author: Sean
    """
    nodetypes = L_( hou.NodeType.Occupation.Context.values() ).sum()
    return self.Name in nodetypes
setAttr( hou.NodeType, 'isContext', _nodetype_isContext )








