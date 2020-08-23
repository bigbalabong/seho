'''
Tier: Base
'''

from ..MVar import *





###########################################################################
################################## State ##################################
###########################################################################
setAttr( hou.Node, "Errors", property( hou.Node.errors ) )


def _node_ErrorCompile( self ):
    errors = self.Errors
    if 'Unable to compile input.' in errors:
        return True
setAttr( hou.Node, 'ErrorCompile', property( _node_ErrorCompile ) )


def _node_getErrorIO( self ):
    '''
    "IOError" is built-in <type 'exceptions.IOError'>.
    '''
    return [ i for i in self.Errors if i.startswith( 'Unable to read file' ) ]
setAttr( hou.Node, "ErrorIO", property( _node_getErrorIO ) )












###########################################################################
################################ User Data ################################
###########################################################################
class NodeUserData( object ):

    def __init__( self, node ):
        self.Node = node

    @property
    def Data( self ):
        return self.Node.userDataDict()


    @property
    def Keys( self ):
        '''
        Easy-to-use
        '''
        return self.Data.keys()

    @property
    def Values( self ):
        '''
        Easy-to-use
        '''
        return self.Data.values()


    def key( self, key ):
        """
        Args:
            key (str): [description]

        Returns:
            [type]: [description]
        """
        return self.Node.userData( key )


    def add( self, key, value ):
        """
        Add new key-value pair, or set new value for existing key.

        Args:
            key (str): [description]
            value (str): User data only supports string.
        """
        self.Node.setUserData( key, value )


    def delete( self, key ):
        self.Node.destroyUserData( key )


    def clear( self ):
        self.Node.clearUserDataDict()



    # ======================================================== #
    # ======================== Preset ======================== #
    # ======================================================== #
    def storeInitialColor( self ):
        key = 'initial_color'
        value = str(self.Node.Color.RGB)[1:-1]
        self.Node.setUserData( key, value )

    def storeInitialShape( self ):
        key = 'initial_shape'
        value = self.Node.Shape
        self.Node.setUserData( key, value )



    # ======================================================== #
    # =================== Background Image =================== #
    # ======================================================== #
    @property
    def BGImages( self ):
        return

    @BGImages.setter
    def BGImages( self, filepaths ):
        return

    def storeBGImagesInHDA( self, hda=None, 
                            only_external_links=False,
                            remove_original_extras=True ):
        """
        Store background images with external links into the input HDA as extras.

        Args:
            hda (hou.HDADefinition, optional): Where the background images will be stored. 
                            Defaults to None.
                            If None, auto create a new embedded HDA.
            only_external_links (bool, optional): 
                            If true, only store images with external links into target HDA.
                            If false, store all images into target HDA,
                            which are with external links or have been already stored into other HDA.
                            Defaults to False.
            remove_original_extras (bool, optional):
                            If true, the original extras will be removed 
                            when images are extracted from some HDA to be stored into a new one.
                            If false, keep the original extras intact.
                            Defaults to True.

        Returns:
            [hou.HDADefinition / None]:
                            When creating a new embedded HDA, return it.
                            When storing images into the input HDA, return None.
        """
        return
    



def _node_getUserData( self ):
    return NodeUserData( self )
setAttr( hou.Node, "UserData", property( _node_getUserData ) )




# ~~~~~~~~~~~~~~~~~ Shape ~~~~~~~~~~~~~~~~~ #
# get all node shapes
# hou.getNetworkEditor().nodeShapes()

def _node_getShape( self ):
    if 'nodeshape' in self.UserData.Data.keys():
        return self.UserData.Data['nodeshape']

    else:
        shape = self.Type.defaultShape()
        if not shape:
            return 'null'
        else:
            return shape

def _node_setShape( self, shape ):
    '''
    PARMS:
            shape (str)
    '''
    self.UserData.add( 'nodeshape', shape )

setAttr( hou.Node, "Shape", property( _node_getShape, _node_setShape ) )




# ~~~~~~~~~~~~~~~~ Pointer ~~~~~~~~~~~~~~~~ #
def _node_getPointer( self ):
    return self.userData( 'pointer' )

def _node_setPointer( self, node ):
    self.setUserData('pointer', node.path())
    node.setUserData('pointer', self.path())

setAttr( hou.Node, "Pointer", property( _node_getPointer, _node_setPointer ) )


def _node_framePointer( self ):
    pointer = hou.node( self.userData( 'pointer' ) )

    if not pointer:
        p( 'No pointer found.' )
        return
    else:
        editor = getNetworkPane()
        editor.setPwd( pointer.parent() )        
        nodegraphview.frameItems( editor, [ pointer ], True ) 
        pointer.setSelected( True, True )
        return pointer
setAttr( hou.Node, 'framePointer', _node_framePointer )




# ~~~~~~~~~~~ Background Images ~~~~~~~~~~~ #
def _node_getBGImages( self ):
    """
    Returns:
        [list of str / empty list]: filepaths of images.
    """
    if 'backgroundimages' not in self.userDataDict().keys():
        return []

    info = self.userDataDict()['backgroundimages']
    info = info.split( '"path": "' )[1:]
    info = [ i.split( '", "rect"' ) for i in info ]
    info = L_(info).sum()
    info = [ i for i in info if not i.startswith(':') ]
    
    return info
setAttr( hou.Node, "BGImages", property( _node_getBGImages ) )


def _node_getAllBGImages():
    """
    Returns:
        [list of str / None]: filepaths of images.
    """
    nodes = ROOT.AllOpenedNetworks
    nodes = [ i for i in nodes if 'backgroundimages' in i.userDataDict().keys() ]

    if not nodes:
        return
    

    # get all background images
    images = [ i.BGImages for i in nodes ]
    images = L_( images ).sum()
    images = list(set( images ))

    return images
setAttr( hou.Node, "getAllBGImages", staticmethod( _node_getAllBGImages ) )









###########################################################################
################################ Node Info ################################
###########################################################################
setAttr( hou.Node, 'Info', property( hou.Node.infoTree ) )


'''
hou.NodeInfoTree        http://www.sidefx.com/docs/houdini/hom/hou/NodeInfoTree.html
'''
setAttr( hou.NodeInfoTree, 'Name', property( hou.NodeInfoTree.name ) )

setAttr( hou.NodeInfoTree, 'Type', property( hou.NodeInfoTree.infoType ) )

setAttr( hou.NodeInfoTree, 'Order', property( hou.NodeInfoTree.branchOrder ) )



setAttr( hou.NodeInfoTree, 'Branches', property( hou.NodeInfoTree.branches ) )

setAttr( hou.NodeInfoTree, 'Headings', property( hou.NodeInfoTree.headings ) )

setAttr( hou.NodeInfoTree, 'Rows', property( hou.NodeInfoTree.rows ) )


def _infoTree_getValue( self, property_name ):
    '''
    Args:
        property_name (str): name pf property.

    Returns:
        [str]: value of property.
    '''    
    info_dict = dict( self.Rows )
    value = info_dict.get( property_name )

    if value is not None:
        return value
    
    
    branches = dict( self.Branches )
    info_tree = branches.get( property_name )
    return info_tree
setAttr( hou.NodeInfoTree, '__getitem__', _infoTree_getValue, replace=False )







