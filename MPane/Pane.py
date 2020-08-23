'''
Tier: Base
'''

from ..MVar import *







###########################################################################
################################### Open ##################################
###########################################################################

def _openChannelEditor( pos=(), empty=True ):
    pane = hou.ui.curDesktop().createFloatingPaneTab( 
                                                        hou.paneTabType.ChannelEditor,
                                                        position = pos,
                                                    )
    
    if empty:
        pane.clear()
    
    return pane
setAttr( hou.ui, 'openChannelEditor', _openChannelEditor, replace=False )


def _openChannelViewer( pos=() ):
    pane = hou.ui.curDesktop().createFloatingPaneTab( 
                                                        hou.paneTabType.ChannelViewer,
                                                        position = pos,
                                                    )
    return pane
setAttr( hou.ui, 'openChannelViewer', _openChannelViewer, replace=False )


def _openCompositeViewer( pos=() ):
    pane = hou.ui.curDesktop().createFloatingPaneTab( 
                                                        hou.paneTabType.CompositorViewer,
                                                        position = pos,
                                                    )
    return pane
setAttr( hou.ui, 'openCompositeViewer', _openCompositeViewer, replace=False )








###########################################################################
################################## Active #################################
###########################################################################

def _activePythonShell():
    """
    Author: Sean
    """
    from pynput.mouse import Controller as mouseCtrl
    from pynput.mouse import Button as mouseBtn
    from pynput.keyboard import Controller as keyCtrl
    from pynput.keyboard import Key as keyBtn

    mouse = mouseCtrl()
    keyboard = keyCtrl()

    initial_pos = mouse.position


    mouse.position = (1675, 1271)
    underCursor = hou.ui.paneTabUnderCursor()
    if underCursor and underCursor.type() == hou.paneTabType.PythonShell:
        mouse.click( mouseBtn.left, 1 )
        mouse.position = initial_pos


    else:
        mouse.position = initial_pos

        # avoid key conflicts
        time.sleep( 0.1 )

        # press hotkey ctrl P
        keyboard.press(keyBtn.shift)
        keyboard.press(keyBtn.alt)
        keyboard.press('p')
        keyboard.release(keyBtn.shift)
        keyboard.release(keyBtn.alt)
        keyboard.release('p')



    # define variables under __main__
    nodes = hou.selectedItems()
    if nodes:
        node = nodes[0]
        a =  nodes[0]
        b = nodes[1] if nodes.__len__()>=2 else None

        import __main__
        __main__.nodes = nodes
        __main__.node = node
        __main__.a = a
        __main__.b = b


        # type in: node.
        time.sleep( 0.2 )
        for i in 'node.':
            keyboard.press(i)
            keyboard.release(i)
setAttr( hou.ui, "activePythonShell", _activePythonShell )









###########################################################################
########################### hou.PathBasedPaneTab ##########################
###########################################################################
'''
hou.PathBasedPaneTab    https://www.sidefx.com/docs/houdini/hom/hou/PathBasedPaneTab.html
'''

setAttr( hou.PathBasedPaneTab, "PWD", property( hou.PathBasedPaneTab.pwd, hou.PathBasedPaneTab.setPwd ) )


def _pathPane_getCurrentNode( self ):
    """
    Author: Sean
    """
    node = self.currentNode()

    if node == self.PWD:
        return None
    else:
        return node
setAttr( hou.PathBasedPaneTab, "Node", property( _pathPane_getCurrentNode, hou.PathBasedPaneTab.setCurrentNode ) )








