'''
Tier: Base
'''

from .MVar import *



'''
hou.viewportVisualizers     http://www.sidefx.com/docs/houdini/hom/hou/viewportVisualizers.html
'''





###########################################################################
############################ ViewportVisualizer ###########################
###########################################################################
'''
hou.ViewportVisualizer      https://www.sidefx.com/docs/houdini/hom/hou/ViewportVisualizer.html
'''

# ======================================================== #
# ====================== Basic Info ====================== #
# ======================================================== #
setAttr( hou.ViewportVisualizer, "Name", property( hou.ViewportVisualizer.name, hou.ViewportVisualizer.setName ) )
setAttr( hou.ViewportVisualizer, "Label", property( hou.ViewportVisualizer.label, hou.ViewportVisualizer.setLabel ) )
setAttr( hou.ViewportVisualizer, "Icon", property( hou.ViewportVisualizer.icon, hou.ViewportVisualizer.setIcon ) )

setAttr( hou.ViewportVisualizer, "Type", property( hou.ViewportVisualizer.type, hou.ViewportVisualizer.setType ) )
setAttr( hou.ViewportVisualizer, "Cate", property( hou.ViewportVisualizer.category ) )

setAttr( hou.ViewportVisualizer, "Node", property( hou.ViewportVisualizer.categoryNode ) )

setAttr( hou.ViewportVisualizer, "Scope", property( hou.ViewportVisualizer.scope, hou.ViewportVisualizer.setScope ) )




# ======================================================== #
# ========================= State ======================== #
# ======================================================== #
setAttr( hou.ViewportVisualizer, "Active", 
            property( hou.ViewportVisualizer.isActive, hou.ViewportVisualizer.setIsActive ) )











