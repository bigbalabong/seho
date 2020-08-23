'''
Tier: Base
'''

from ..MVar import *




###########################################################################
################################ StickyNote ###############################
###########################################################################
'''
hou.StickyNote      http://www.sidefx.com/docs/houdini/hom/hou/StickyNote.html
'''

setAttr( hou.StickyNote, "Text", property( hou.StickyNote.text, hou.StickyNote.setText ) )
setAttr( hou.StickyNote, "Size", property( hou.StickyNote.textSize, hou.StickyNote.setSize ) )
setAttr( hou.StickyNote, "Color", property( hou.StickyNote.textColor, hou.StickyNote.setTextColor ) )

setAttr( hou.StickyNote, "BG", property( hou.StickyNote.drawBackground, hou.StickyNote.setDrawBackground ) )

setAttr( hou.StickyNote, "Min", property( hou.StickyNote.isMinimized, hou.StickyNote.setMinimized ) )








