'''
Tier: Base
'''

from ..MVar import *


'''
hou.playbar         https://www.sidefx.com/docs/houdini/hom/hou/playbar.html
hou.playMode        https://www.sidefx.com/docs/houdini/hom/hou/playMode.html
'''



class _Playbar( object ):

    """
    Author: Sean
    """

    @property
    def StartFrame( self ):
        """
        Author: Sean
        """
        start_frame, end_frame = hou.playbar.frameRange()
        return start_frame

    @StartFrame.setter
    def StartFrame( self, value ):
        """
        Author: Sean
        """
        start_frame, end_frame = hou.playbar.frameRange()
        start_frame = value

        hou.playbar.setFrameRange( start_frame, end_frame )
        hou.playbar.setPlaybackRange( start_frame, end_frame )


    @property
    def EndFrame( self ):
        """
        Author: Sean
        """
        start_frame, end_frame = hou.playbar.frameRange()
        return end_frame

    @EndFrame.setter
    def EndFrame( self, value ):
        """
        Author: Sean
        """
        start_frame, end_frame = hou.playbar.frameRange()
        end_frame = value

        hou.playbar.setFrameRange( start_frame, end_frame )
        hou.playbar.setPlaybackRange( start_frame, end_frame )


    @property
    def FPS( self ):
        """
        https://www.sidefx.com/docs/houdini/hom/hou/fps.html
        """
        return hou.fps()

    @FPS.setter
    def FPS( self, value ):
        """
        https://www.sidefx.com/docs/houdini/hom/hou/setFps.html
        """
        hou.setFps( value )


    @property
    def Frame( self ):
        """
        https://www.sidefx.com/docs/houdini/hom/hou/frame.html
        """
        return hou.frame()

    @Frame.setter
    def Frame( self, value ):
        """
        https://www.sidefx.com/docs/houdini/hom/hou/setFrame.html
        """
        hou.setFrame( value )


    @property
    def Time( self ):
        """
        https://www.sidefx.com/docs/houdini/hom/hou/time.html
        """
        return hou.time()

    @Time.setter
    def Time( self, value ):
        """
        https://www.sidefx.com/docs/houdini/hom/hou/setTime.html
        """
        hou.setTime( value )



    PlayModes = {
            'loop':     hou.playMode.Loop,
            'once':     hou.playMode.Once,
            'zigzag':   hou.playMode.Zigzag,
        }

    @property
    def PlayMode( self ):
        return hou.playbar.playMode()

    @PlayMode.setter
    def PlayMode( self, mode ):
        """
        Args:
            mode (str): 'loop' / 'once' / 'zigzag'
        """
        mode = mode.lower()
        mode = self.PlayModes.get( mode )
        print( mode )

        if mode is None:
            print( "The mode dosn't exist." )
            return

        hou.playbar.setPlayMode( mode )




    # ======================================================== #
    # ========================= Audio ======================== #
    # ======================================================== #
    def setAudioSource( self, chop=None, filepath=None ):
        """
        Author: Sean
        """
        if chop is not None:
            hou.audio.useChops()
            hou.audio.setChopPath( chop )

        elif filepath is not None:
            hou.audio.useAudioFile()
            hou.audio.setAudioFileName( filepath )

        hou.audio.useTimeLineMode()
        hou.playbar.showAudio( True )


    def setAudioOffset( self, frame=None, time=None ):
        """
        Author: Sean
        """
        if frame is not None:
            hou.audio.setAudioFrame( frame )
        
        elif time is not None:
            hou.audio.setAudioOffset( time )
Playbar = _Playbar()
setAttr( hou.ui, "Playbar", Playbar )








