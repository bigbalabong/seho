'''
Tier: Base
'''

from ..MVar import *



'''
Flag Hotkeys        http://www.sidefx.com/docs/houdini/network/flags#keys

Badges              http://www.sidefx.com/docs/houdini/network/badges.html
Badges              http://www.sidefx.com/docs/houdini/network/flags#badges

hou.nodeFlag        https://www.sidefx.com/docs/houdini/hom/hou/nodeFlag.html
        hou.nodeFlag.Audio
        hou.nodeFlag.Bypass
        hou.nodeFlag.ColorDefault
        hou.nodeFlag.Compress
        hou.nodeFlag.Current
        hou.nodeFlag.Debug
        hou.nodeFlag.Display
        hou.nodeFlag.DisplayComment
        hou.nodeFlag.DisplayDescriptiveName
        hou.nodeFlag.Export
        hou.nodeFlag.Expose
        hou.nodeFlag.Footprint
        hou.nodeFlag.Highlight
        hou.nodeFlag.InOutDetailLow
        hou.nodeFlag.InOutDetailMedium
        hou.nodeFlag.InOutDetailHigh
        hou.nodeFlag.Material
        hou.nodeFlag.Lock
        hou.nodeFlag.SoftLock
        hou.nodeFlag.Origin
        hou.nodeFlag.OutputForDisplay
        hou.nodeFlag.Pick
        hou.nodeFlag.Render
        hou.nodeFlag.Selectable
        hou.nodeFlag.Template
        hou.nodeFlag.Unload
        hou.nodeFlag.Visible
        hou.nodeFlag.XRay
'''

def _node_getFlagComment( self ):
    return self.isGenericFlagSet( hou.nodeFlag.DisplayComment )

def _node_setFlagComment( self, bool_ ):
    self.setGenericFlag( hou.nodeFlag.DisplayComment, bool_ )

setAttr( hou.Node, "DisplayComment", property( _node_getFlagComment, _node_setFlagComment ) )



def _node_getFlagLock( self ):
    return self.isGenericFlagSet( hou.nodeFlag.Lock )

def _node_setFlagLock( self, bool_ ):
    self.setGenericFlag( hou.nodeFlag.Lock, bool_ )

setAttr( hou.Node, "Lock", property( _node_getFlagLock, _node_setFlagLock ) )





# ======================================================== #
# ========================== OBJ ========================= #
# ======================================================== #
setAttr( hou.ObjNode, "Display", property( hou.ObjNode.isDisplayFlagSet, hou.ObjNode.setDisplayFlag ) )

setAttr( hou.ObjNode, "Selectable", property( hou.ObjNode.isSelectableInViewport, hou.ObjNode.setSelectableInViewport ) )

setAttr( hou.ObjNode, "Xray", property( hou.ObjNode.isUsingXray, hou.ObjNode.useXray ) )

setAttr( hou.ObjNode, "ShowingOrigin", property( hou.ObjNode.isShowingOrigin, hou.ObjNode.showOrigin ) )







# ======================================================== #
# ========================== SOP ========================= #
# ======================================================== #
setAttr( hou.SopNode, "Bypass", property( hou.SopNode.isBypassed, hou.SopNode.bypass ) )

setAttr( hou.SopNode, "Template", property( hou.SopNode.isTemplateFlagSet, hou.SopNode.setTemplateFlag ) )

setAttr( hou.SopNode, "Display", property( hou.SopNode.isDisplayFlagSet, hou.SopNode.setDisplayFlag ) )

setAttr( hou.SopNode, "Render", property( hou.SopNode.isRenderFlagSet, hou.SopNode.setRenderFlag ) )



def _node_isDisplay2( self ):
    return self.Render and self.Display

def _node_setDisplay2( self, state ):
    """
    Set render flag and display flag simultaneously.
    """
    self.Render = state
    self.Display = state

setAttr( hou.SopNode, "Display2", property( _node_isDisplay2, _node_setDisplay2 ) )






# ======================================================== #
# ========================== DOP ========================= #
# ======================================================== #
setAttr( hou.DopNode, "Bypass", property( hou.DopNode.isBypassed, hou.DopNode.bypass ) )

setAttr( hou.DopNode, "Template", property( hou.DopNode.isTemplateFlagSet, hou.DopNode.setTemplateFlag ) )

setAttr( hou.DopNode, "Display", property( hou.DopNode.isDisplayFlagSet, hou.DopNode.setDisplayFlag ) )










# ======================================================== #
# ========================= CHOP ========================= #
# ======================================================== #
setAttr( hou.ChopNode, "Output", property( hou.ChopNode.isCurrentFlagSet, hou.ChopNode.setCurrentFlag ) )







# ======================================================== #
# ========================== TOP ========================= #
# ======================================================== #
setAttr( hou.TopNode, "Bypass", property( hou.TopNode.isBypassed, hou.TopNode.bypass ) )

setAttr( hou.TopNode, "Display", property( hou.TopNode.isDisplayFlagSet, hou.TopNode.setDisplayFlag ) )

setAttr( hou.TopNode, "Render", property( hou.TopNode.isRenderFlagSet, hou.TopNode.setRenderFlag ) )







###########################################################################
################################# Isolate #################################
###########################################################################

def _node_isolateSelectedNodes():
    """
    Toggle nodes display under OBJ network.
    """
    if 'isolated_backup' not in sys.modules['__main__'].__dict__.keys() or sys.modules['__main__'].__dict__[ 'isolated_backup' ] is None:
        nodes = toolutils.networkEditor().PWD.Children
        sels = hou.selectedNodes()

        current_state = dict([ (i, i.Display) for i in nodes ])
        sys.modules['__main__'].__dict__[ 'isolated_backup' ] = current_state

        for i in nodes:
            i.Display = False

        for i in sels:
            i.Display = True

    else:
        # restore backup state
        current_state = sys.modules['__main__'].__dict__[ 'isolated_backup' ]
        for node, state in current_state.items():
            node.Display = state

        # reset backup state
        sys.modules['__main__'].__dict__[ 'isolated_backup' ] = None
setAttr( hou.Node, "isolate", staticmethod( _node_isolateSelectedNodes ), replace=False )

















###########################################################################
################################### Node ##################################
###########################################################################

def _node_getDisplayNode( self ):
    return self.displayNode()
setAttr( hou.ObjNode,       "DisplayNode",  property( _node_getDisplayNode ) )
setAttr( hou.SopNode,       "DisplayNode",  property( _node_getDisplayNode ) )
setAttr( hou.DopNode,       "DisplayNode",  property( _node_getDisplayNode ) )
setAttr( hou.PopNetNode,    "DisplayNode",  property( _node_getDisplayNode ) )
setAttr( hou.TopNode,       "DisplayNode",  property( _node_getDisplayNode ) )


def _node_getRenderNode( self ):
    return self.renderNode()
setAttr( hou.ObjNode,       "RenderNode",   property( _node_getRenderNode ) )
setAttr( hou.PopNetNode,    "RenderNode",   property( _node_getRenderNode ) )
setAttr( hou.TopNode,       "RenderNode",   property( _node_getRenderNode ) )














