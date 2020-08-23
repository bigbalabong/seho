'''
Tier: Base
'''

from ..MVar import *



###########################################################################
################################### CHOP ##################################
###########################################################################
'''
hou.ChopNode        http://www.sidefx.com/docs/houdini/hom/hou/ChopNode.html
'''

setAttr( hou.ChopNode, 'SampleRate', property( hou.ChopNode.sampleRate ) )
setAttr( hou.ChopNode, 'SampleRange', property( hou.ChopNode.sampleRange ) )







###########################################################################
############################# Track / Channel #############################
###########################################################################
'''
hou.Track       http://www.sidefx.com/docs/houdini/hom/hou/Track.html
'''
setAttr( hou.Track, 'Name', property( hou.Track.name ), replace=False )


setAttr( hou.Track, 'Value', property( hou.Track.eval ), replace=False )
setAttr( hou.Track, '_', hou.Track.Value, replace=False )


setAttr( hou.Track, 'Samples', property( hou.Track.allSamples ), replace=False )

setAttr( hou.Track, 'NumSamples', property( hou.Track.numSamples ), replace=False )


def _chan_getMinSample( self ):
    return min( self.Samples )
setAttr( hou.Track, 'Min', property( _chan_getMinSample ), replace=False )

def _chan_getMaxSample( self ):
    return max( self.Samples )
setAttr( hou.Track, 'Max', property( _chan_getMaxSample ), replace=False )









###########################################################################
################################# Shortcut ################################
###########################################################################

# ======================================================== #
# ========================= Node ========================= #
# ======================================================== #
setAttr( hou.ChopNode, 'Tracks', property( hou.ChopNode.tracks ) )
setAttr( hou.ChopNode, 'Channels', hou.ChopNode.Tracks )

def _chop_getChannelNames( self ):
    return [ i.Name for i in self.Channels ]
setAttr( hou.ChopNode, 'ChannelNames', property( _chop_getChannelNames ) )


def _chop_getNumChannels( self ):
    return len( self.Channels )
setAttr( hou.ChopNode, 'NumChannels', property( _chop_getNumChannels ) )


def _chop_getChannel( self, name_or_index=0 ):
    if type(name_or_index) is int:
        index = name_or_index
        return self.Channels[ index ]

    elif type(name_or_index) is str:
        name = name_or_index
        return self.track( name )
setAttr( hou.ChopNode, 'channel', _chop_getChannel )





# ======================================================== #
# ========================= Track ======================== #
# ======================================================== #
setAttr( hou.Track, 'Node', property( hou.Track.chopNode ), replace=False )








