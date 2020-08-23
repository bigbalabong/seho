'''
Tier: Base
'''


from ..MVar import *






###########################################################################
############################## Channel Editor #############################
###########################################################################
'''
hou.ChannelEditorPane   https://www.sidefx.com/docs/houdini/hom/hou/ChannelEditorPane.html
'''
def _channelEditor_getChannelList( self ):
    channel_list = self.channelList()
    setAttr( channel_list, 'ChannelEditor', self )
    return channel_list
setAttr( hou.ChannelEditorPane, 'ChannelList', 
            property( _channelEditor_getChannelList, hou.ChannelEditorPane.setChannelList ), replace=False )


def _channelEditor_clear( self ):
    channel_list = self.ChannelList
    channel_list.clear()
    channel_list.apply()
setAttr( hou.ChannelEditorPane, 'clear', _channelEditor_clear )







'''
hou.ChannelList         https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html
'''
setAttr( hou.ChannelList, 'Parms', property( hou.ChannelList.parms ) )


setAttr( hou.ChannelList, 'SelectedParms', property( hou.ChannelList.selected ) )
setAttr( hou.ChannelList, 'PinnedParms', property( hou.ChannelList.pinned ) )


setAttr( hou.ChannelList, 'Filter', property( hou.ChannelList.filter, hou.ChannelList.setFilter ) )


def _channelList_apply( self ):
    self.ChannelEditor.ChannelList = self
setAttr( hou.ChannelList, 'apply', _channelList_apply )









