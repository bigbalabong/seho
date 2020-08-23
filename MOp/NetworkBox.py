'''
Tier: Base
'''

from ..MVar import *




def _node_inBox( self, 
                networkBox_name, networkBox_label=None, 
                moveable=False,
                force_new = False,
                top_margin = None
            ):

    networkBox_name += '__networkBox'


    if self.parentNetworkBox() and self.parentNetworkBox().Name == networkBox_name:
        return


    # get network box
    networkBox = self.Parent.findNetworkBox( networkBox_name )

    if not networkBox or force_new:
        networkBox = self.Parent.createNetworkBox( networkBox_name )


    # move node to the bottom position of network box
    if moveable:
        top_left_corner, right_bottom_corner = boundOfNodes( networkBox.nodes( recurse=True ) )
        dest_pos = hou.Vector2( top_left_corner.x() * 0.5 + right_bottom_corner.x() * 0.5, right_bottom_corner.y() + node_pos_offset.y() )

        self.setPosition( dest_pos )


    # set label
    if networkBox_label is not None:
        networkBox.Label = networkBox_label
    else:
        networkBox.Label = networkBox_name.rsplit('__',1)[0]


    # add this node to the network box
    networkBox.addNode( self )
    networkBox.fitAroundContents()


    if top_margin is not None:
        self.P += top_margin

    return networkBox
setAttr( hou.Node, 'inBox', _node_inBox, replace=False )








###########################################################################
############################## hou.NetworkBox #############################
###########################################################################
'''
hou.NetworkBox      http://www.sidefx.com/docs/houdini/hom/hou/NetworkBox.html
'''

setAttr( hou.NetworkBox, "Items", property( hou.NetworkBox.items ) )

def _networkBox_addItems( self, items ):
    if isSequence( items ):
        for i in items:
            self.addItem( i )

    else:
        item = items
        self.addItem( item )
setAttr( hou.NetworkBox, 'add', _networkBox_addItems )

setAttr( hou.NetworkBox, "AutoFit", property( hou.NetworkBox.autoFit, hou.NetworkBox.setAutoFit ) )

setAttr( hou.NetworkBox, "Comment", property( hou.NetworkBox.comment, hou.NetworkBox.setComment ) )
setAttr( hou.NetworkBox, 'Label', hou.NetworkBox.Comment )















