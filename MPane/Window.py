'''
Tier: Base
'''

from ..MVar import *





###########################################################################
################################## Dialog #################################
###########################################################################

class Dialog( object ):

    """
    Author: Sean
    """

    @staticmethod
    def display( info='Hello world~', icon='message' ):
        """
        Author: Sean
        """
        icon = icon.lower()

        severity_types = {
                            'message':      hou.severityType.Message,
                            'important':    hou.severityType.ImportantMessage,
                            'warning':      hou.severityType.Warning,
                            'error':        hou.severityType.Error,
                            'fatal':        hou.severityType.Fatal,
                        }
        severity_type = severity_types.get( icon )

        if severity_type is None:
            severity_type = hou.severityType.Message

        hou.ui.displayMessage( info, severity=severity_type )


    @staticmethod
    def browseImage( dir=None ):
        """
        Author: Sean
        """
        filepath = hou.ui.selectFile( start_directory = dir,
                                    title = 'Select image.',
                                    file_type = hou.fileType.Image,
                                    image_chooser = True,
                                    )
        return filepath

    '''
    hou.ui.readInput
    hou.ui.readMultiInput
    '''
setAttr( hou.ui, "Dialog", Dialog )



###########################################################################
################################## Select #################################
###########################################################################

def _node_selectNode( self, 
                            initial_node = None,
                            return_node = True, exclude_self = True, 

                            filter_same_nodetype = False,

                            multi = False,
                            relative = True, 
                        ):
    """
    Select node(s).

    Args:
        initial_node (hou.Node, optional): If none, use self.
                                            Defaults to None.
        return_node (bool, optional): If true, return hou.Node.
                                        If false, return nodepath string.
                                        Defaults to True.
        exclude_self (bool, optional): If true, exclude self from selection results.

        filter_same_nodetype (bool, optional): If true, filter out the other nodetypes.
        
        multi (bool, optional): If true, select multi-nodes, and return list.
                                If false, select single node, and return hou.Node or string.
        relative (bool, optional): If return_node is false and relative is true, return relative nodepath string. 
                                    If return_node is false and relative is false, return absolute nodepath string.
                                    Defaults to 'relative'.

    Returns:
        [hou.Node / string]: [description]    

    References:
        https://www.sidefx.com/docs/houdini/hom/hou/ui.html#selectNode

    Author: Sean
    """
    if initial_node is None:
        initial_node = self

    custom_filter = None
    if filter_same_nodetype:
        custom_filter = lambda x: x.Type.CateName == self.Type.CateName


    # ~~~~~~~~~~~~~~ select nodes ~~~~~~~~~~~~~ #
    nodepaths = hou.ui.selectNode( 
                                    initial_node = initial_node, 
                                    relative_to_node = self if relative else None, 
                                    multiple_select = multi,
                                    custom_node_filter_callback = custom_filter,
                                )

    if not nodepaths:
        return


    if not multi:
        nodepaths = [nodepaths]


    # ~~~~~~~~~~~~~~ exclude self ~~~~~~~~~~~~~ #
    if exclude_self:
        nodepaths = [ i for i in nodepaths if i != '.' and i != self.Path ]

        if not nodepaths:
            return


    # ~~~~~~~~~~~~~~~~~ return ~~~~~~~~~~~~~~~~ #
    if return_node:
        nodes = [ self.node( i ) for i in nodepaths ]

        if multi:
            return nodes
        else:
            return nodes[0]

    else:
        if multi:
            return nodepaths
        else:
            return nodepaths[0]
setAttr( hou.Node, 'selectNode', _node_selectNode, replace=False )


def _node_selectNodes( self, **kwargs ):
    return self.selectNode( multi=True, **kwargs )
setAttr( hou.Node, 'selectNodes', _node_selectNodes, replace=False )


def _selectCamera( relative_to_node=None, multi=False ):
    nodepaths = hou.ui.selectNode( 
                                relative_to_node = relative_to_node, 
                                initial_node = hou.node('/obj'),
                                node_type_filter = hou.nodeTypeFilter.ObjCamera,
                                multiple_select = multi,
                            )

    # the returned nodepath could be None or '/' or '/obj'

    if not nodepaths:
        return

    if not multi:
        nodepaths = [nodepaths]


    if relative_to_node:
        nodes = [ relative_to_node.node( i ) for i in nodepaths ]
        
    else:
        nodes = [ hou.node( i ) for i in nodepaths ]

    cameras = [ i for i in nodes if i.Type.CateName == 'Object/cam' ]

    if not cameras:
        return
        
    if multi:
        return cameras
    else:
        return cameras[0]
setAttr( hou.ui, "selectCamera", _selectCamera, replace=False )







