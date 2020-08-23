'''
Tier: Base
'''

from ..MVar import *




setAttr( hou.Node, "NodeGroups", property( hou.Node.nodeGroups ) )




'''
hou.NodeGroup       https://www.sidefx.com/docs/houdini/hom/hou/NodeGroup.html
'''

setAttr( hou.NodeGroup, "Name", property( hou.NodeGroup.name ) )

setAttr( hou.NodeGroup, "Parrent", property( hou.NodeGroup.parent ) )


setAttr( hou.NodeGroup, "Nodes", property( hou.NodeGroup.nodes ) )


setAttr( hou.NodeGroup, "add", hou.NodeGroup.addNode )
setAttr( hou.NodeGroup, "remove", hou.NodeGroup.removeNode )







