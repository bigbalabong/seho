'''
Tier: Base
'''

from ..MVar import *






###########################################################################
########################## hou.NetworkMovableItem #########################
###########################################################################
'''
hou.NetworkMovableItem      http://www.sidefx.com/docs/houdini/hom/hou/NetworkMovableItem.html
'''

# ======================================================== #
# ====================== Basic Info ====================== #
# ======================================================== #
setAttr( hou.NetworkMovableItem, 'Path', property( hou.NetworkMovableItem.path ) )

setAttr( hou.NetworkMovableItem, 'Id', property( hou.NetworkMovableItem.sessionId ) )

setAttr( hou.NetworkMovableItem, 'P', property( hou.NetworkMovableItem.position, hou.NetworkMovableItem.setPosition ) )


def _netItem_setName( self, new_name ):
    """
    Rename node and auto-avoid naming conflicts.

    Args:
        new_name ([type]): [description]

    Author: Sean
    """
    self.setName( new_name, unique_name=True )
setAttr( hou.NetworkMovableItem, 'Name', property( hou.NetworkMovableItem.name, _netItem_setName ) )



# ======================================================== #
# ========================= State ======================== #
# ======================================================== #
setAttr( hou.NetworkMovableItem, 'Selected', 
            property( hou.NetworkMovableItem.isSelected, hou.NetworkMovableItem.setSelected ) )









###########################################################################
################################### Node ##################################
###########################################################################
'''
hou.Node                http://www.sidefx.com/docs/houdini/hom/hou/Node.html
hou.SopNode             https://www.sidefx.com/docs/houdini/hom/hou/SopNode.html
hou.NodeTypeCategory    https://www.sidefx.com/docs/houdini/hom/hou/NodeTypeCategory.html
'''


# ======================================================== #
# ====================== Basic Info ====================== #
# ======================================================== #
def _node_getNameWithCate( self ):
    """
    Examples:
        'tube1 (Sop)'
        'voronoifracture1 (Sop)'
        'geo1 (Object)'

    Author: Sean
    """
    return '{} ({})'.format( self.Name, self.Type.Cate.Name )
setAttr( hou.Node, 'NameCate', property( _node_getNameWithCate ) )

def _node_rename( nodes=None, new_name=None ):
    """
    Rename multi-nodes.

    Args:
        nodes ([type], optional): [description]. Defaults to None.
        new_name ([type], optional): [description]. Defaults to None.

    Author: Sean
    """
    if not not nodes:
        nodes = hou.lss()


    # rename temporarily to avoid naming conflicts
    for i in range( nodes.__len__() ):
        temp_name = 'temp_{}_{}'.format( int(time.clock()), i )
        nodes[i].setName( temp_name, unique_name=True )


    # rename
    for i in range( nodes.__len__() ):
        this_new_name = '{}_{}'.format( new_name, str(i+1).rjust( str(nodes.__len__()).__len__(), '0') )
        nodes[i].setName( this_new_name, unique_name=True )
setAttr( hou.Node, 'rename', staticmethod( _node_rename ) )


def _node_getLabel( self ):
    """
    Author: Sean
    """
    return self.Type.Label
setAttr( hou.Node, 'Label', property( _node_getLabel ) )



def _node_getIcon( self ):
    """
    Author: Sean
    """
    return self.Type.Icon
setAttr( hou.Node, 'Icon', property( _node_getIcon ) )


def _node_root( self ):
    '''
    RETURN:
            The root node under root context.

    EXAMPLES:
            ls().PATH
                RETURN: '/obj/geo1/subnet1/mountain1'
            ls().ROOT
                RETURN: <hou.ObjNode of type geo at /obj/geo1>
    
    Author: Sean
    '''
    return hou.node( '/'.join( self.path().split('/',3)[:3] ) )
setAttr( hou.Node, 'Root', property( _node_root ) )


def _node_setCurrent2( self ):
    '''
    Make this node as current node of network editor.

    Author: Sean
    '''
    network_editors = [ i for i in hou.NetworkEditor.getAll() if i.PWD == self.Parent ]
    for network in network_editors:
        network.Node = self
setAttr( hou.Node, 'setCurrent2', _node_setCurrent2 )









# ======================================================== #
# ======================= New Node ======================= #
# ======================================================== #
def _node_newNode( self, *args, **kwargs ):
    '''
    PARMS:
            position
            last_node (hou.Node)
            as_network_current (bool)

    Author: Sean
    '''
    # pre-processing arguments
    if 'position' in kwargs.keys():    
        position = kwargs['position']
        del kwargs['position']
    else:
        position = hou.Vector2()

    if 'last_node' in kwargs.keys():
        last_node = kwargs['last_node']
        del kwargs['last_node']
    else:
        last_node = None

    if 'as_network_current' in kwargs.keys():
        as_network_current = kwargs['as_network_current']
        del kwargs['as_network_current']
    else:
        as_network_current = False

    if 'selection_group' in kwargs.keys():
        selection = lssGeo()
        if not selection:
            selection_group = False
        else:
            selection = selection.NodesDict

            if not selection:
                selection_group = False
            else:
                selection_group = True
                selection_info = selection[last_node]
                grouptype = Grouptypes[selection_info['geotype']]
                group = selection_info['selection']
        del kwargs['selection_group']
    else:
        selection_group = False


    # create new node
    if last_node:
        new_node = last_node.createOutputNode( *args, **kwargs )
    else:    
        new_node = self.createNode( *args, **kwargs )
        new_node.P = position

    
    # post-processing
    new_node.Display = True
    new_node.Render = True

    if as_network_current:
        new_node.setCurrent2()

    if selection_group:
        new_node.Grouptype = grouptype
        new_node.Group = group


    return new_node
setAttr( hou.Node, 'newNode', _node_newNode )


def _node_newContexts( self, contexts=None, P=None ):
    '''
    PARMS:
            contexts (list/tuple)  -  ('mat', 'shop', 'rop', 'cop', 'chop', 'top')

    Author: Sean
    '''
    # get contexts
    if contexts:
        contexts = [ hou.NodeType.Occupation.Context[i] for i in contexts ] 
    else:
        contexts = hou.NodeType.Occupation.Context.values()
        contexts.sort()

    contexts = L_(contexts).sum()


    # get node position
    if P is None:
        left_top_corner, right_bottom_corner = hou.Node.bound( self.children() )
        P = hou.Vector2( right_bottom_corner.X + nPx.X, left_top_corner.Y * 0.3 + right_bottom_corner.Y * 0.6 )
    


    # ======================================================== #
    # ===================== new contexts ===================== #
    # ======================================================== #
    new_contexts = []
    for i in contexts:
        try:
            new_context = self.createNode(i, i)
            new_contexts.append( new_context )

        except:
            continue




    # create new netbox
    netbox = self.createNetworkBox( 'contexts__networkBox' )
    netbox.Label = 'Contexts'

    for i, node in enumerate(new_contexts):
        node.P = P + nPy * i
        netbox.addNode( node )

    netbox.fitAroundContents()

    return new_contexts
setAttr( hou.Node, 'newContexts', _node_newContexts, replace=False )


def _node_merge( nodes ):
    '''
    Merge Nodes.

    Author: Sean
    '''

    if not nodes:
        nodes = lss()
setAttr( hou.Node, 'merge', staticmethod( _node_merge ) )


def _node_toOBJ( self, jump=False ):
    """
    Author: Sean
    """
    if self.type().category().name() != 'Sop':
        return


    # get parent node
    parent = self.root
    parent_name = parent.name()
    parent_pos = parent.position()

    root = parent.parent()


    # create new node
    new_name = '{}_{}'.format( parent_name, self.name() )

    if not root.node( new_name ):
        new_node = root.createNode( 'geo', new_name )
        new_node.setPosition( parent_pos + hou.Vector2(random.random(), -2) )
        new_node.setColor( hou.Color(0.451, 0.369, 0.796) )
        new_node.setUserData( 'nodeshape', "null" )

        new_merge = new_node.createNode( 'object_merge', self.name() )
        new_merge.parm('objpath1').set( new_merge.relativePathTo( self ) )

        print( 'Extracted to: {}'.format( new_merge.path() ) )

    else:
        new_merge = root.node( new_name ).node( self.name() )

        print( 'Already extracted to: {}'.format( new_merge.path() ) )


    # jump to new network position
    if jump:
        jumpTo( new_merge )


    return new_merge
setAttr( hou.Node, 'toOBJ', _node_toOBJ )



# ~~~~~~~~~~~~~~~~~~ Copy ~~~~~~~~~~~~~~~~~ #
def _node_duplicate( self, reference=True, parms_without_ref=None ):
    """
    Duplicate node.

    Args:
        reference (bool, optional): [description]. Defaults to True.
        parms_without_ref (list of str, optional): These parms will have no referencing. 
                                                    Defaults to None.

    Returns:
        [type]: [description]

    Author: Sean
    """
    temp_subnet = self.Parent.createNode( 'subnet' )
    temp_subnet.copyItems( 
                            items =                         (self,),
                            channel_reference_originals =   reference,
                            relative_references =           True,
                        )
    new_node = temp_subnet.extractAndDelete()[0]


    # ~~~~~~~~~~~~ parm references ~~~~~~~~~~~~ #
    if parms_without_ref:
        parms = [ i for i in new_node.Parms if i.Name not in parms_without_ref ]
    else:
        parms = new_node.Parms

    for parm in parms:
        if parm.Expr:
            new_expr = parm.Expr.replace( './', '../{}/'.format( self.Name ) )
            parm.Expr = new_expr

    if parms_without_ref:
        for name in parms_without_ref:
            new_node._[name].deleteAllKeyframes()

    return new_node
setAttr( hou.Node, "duplicate", _node_duplicate, replace=False )





# ======================================================== #
# =================== Bound / Position =================== #
# ======================================================== #
def _node_bound( nodes ):
    '''
    RETURN:
            left_top_corner
            right_bottom_corner

    Author: Sean
    '''
    if not nodes:
        return  hou.Vector2(0,0), hou.Vector2(0,0)


    pos_list = [ i.P for i in nodes ]
    for node in nodes:
        if type(node) in ( hou.StickyNote, hou.NetworkBox ):
            pos_list.append( node.P + node.restoredSize() )

    pos_list = zip( *pos_list )
    x_min = min(pos_list[0])
    x_max = max(pos_list[0])
    y_min = min(pos_list[1])
    y_max = max(pos_list[1])

    left_top_corner = hou.Vector2( x_min, y_max )
    right_bottom_corner = hou.Vector2( x_max, y_min )

    return left_top_corner, right_bottom_corner
setAttr( hou.Node, "bound", staticmethod( _node_bound ) )


@undoGroup
def _node_scalePositions( items, scale=2, attachDist=4.5 ):

    '''
    PARMS:
            items  --  nodes, sticky notes, network boxs....
            scale  --  how far to move selected items
            attachDist  --  if the distance between sticky note and node is less than this threshold, the sticky note is seen as being attached to the specific node.

    Author: Sean
    '''

    nodes = [ i for i in items if isinstance(i, hou.Node) ]
    notes = dict( [ (i, {}) for i in items if isinstance(i, hou.StickyNote) ] )
    boxs = [ i for i in items if isinstance(i, hou.NetworkBox) ]



    # collect state info of stiky notes
    for i in notes.keys():
        notes[i]['folded'] = i.isMinimized()
        i.setMinimized( True )

        distance = min( [ ( j, i.position() - j.position() ) for j in nodes ], key=lambda x: x[1].length() )

        notes[i]['attached'] = distance[1].length() < attachDist
        notes[i]['attachTo'] = distance[0]
        notes[i]['offsetPos'] = distance[1]


        
    # get center pivot
    top_left_corner, right_bottom_corner = boundOfNodes( nodes )
    center = ( top_left_corner + right_bottom_corner ) / 2



    # move nodes
    for i in nodes:
        current_pos = i.position()
        offset_pos = current_pos - center
        new_pos = current_pos + offset_pos * (scale - 1)
        i.setPosition( new_pos )



    # move sticky notes
    for i in notes.keys():

        if notes[i]['attached']:    # keep attach to nodes
            new_pos = notes[i]['attachTo'].position() + notes[i]['offsetPos']
            i.setPosition( new_pos )

        else:                       # move like nodes
            current_pos = i.position()
            offset_pos = current_pos - center
            new_pos = current_pos + offset_pos * (scale - 1)
            i.setPosition( new_pos )


        # restore fold state
        i.setMinimized( notes[i]['folded'] )
setAttr( hou.Node, "scalePositions", staticmethod( _node_scalePositions ) )


def _node_layoutOutputNodes( self ):
    """
    Author: Sean
    """
    nodes = self.Outputs
    
    if not nodes:
        return

    if len( nodes ) == 1:
        node = nodes[0]
        node.moveToGoodPosition()
    else:
        self.Parent.layoutChildren( nodes )
setAttr( hou.Node, 'layoutOutputs', _node_layoutOutputNodes )







# ======================================================== #
# ========================= Group ======================== #
# ======================================================== #
def _node_getGroup( self ):
    """
    Author: Sean
    """
    if not self.parm('group'):
        return
        
    return self.parm('group').eval()

def _node_setGroup( self, components ):
    '''
    PARMS:
            components (str)

    Author: Sean
    '''
    if not self.parm('group'):
        return

    self.parm('group').set( components )

setAttr( hou.Node, "Group", property( _node_getGroup, _node_setGroup ) )



def _node_getGrouptype( self ):
    """
    Author: Sean
    """
    if not self.parm('grouptype'):
        return
    
    return self.parm('grouptype').rawValue()

def _node_setGrouptype( self, grouptype ):
    """
    Author: Sean
    """
    if not self.parm('grouptype'):
        return
    
    tokens = self.parm('grouptype').menuItems()
    grouptype = [ i for i in tokens if i.startswith(grouptype) ][0]
    self.parm('grouptype').set( grouptype )

setAttr( hou.Node, "Grouptype", property( _node_getGrouptype, _node_setGrouptype ) )










# ======================================================== #
# ====================== Expression ====================== #
# ======================================================== #
def _node_getExprLanguage( self ):
    '''
    hou.exprLanguage        http://www.sidefx.com/docs/houdini/hom/hou/exprLanguage.html

    RETURN:
            (str) hscript / python

    Author: Sean
    '''
    return str(self.expressionLanguage()).rsplit('.',1)[1].lower()

def _node_setExprLanguage( self, language ):
    """
    Author: Sean
    """
    language = language.lower()

    if language == 'hscript':
        self.setExpressionLanguage( hou.exprLanguage.Hscript )
    elif language == 'python':
        self.setExpressionLanguage( hou.exprLanguage.Python )

setAttr( hou.Node, 'Language', property( _node_getExprLanguage, _node_setExprLanguage ) )








# ======================================================== #
# ======================= Callback ======================= #
# ======================================================== #
def _node_getEventCallbacks( self ):
    """
    Author: Sean
    """
    callbacks = self.eventCallbacks()

    callbacks_dict = {}
    for index, i in enumerate( callbacks ):
        event, func = i

        class_instance = None
        creation_time = None
        
        try:
            class_instance =  func.im_self
            creation_time = class_instance.CreationTime
        except:
            pass

        callbacks_dict[index] = {
            'Index':        index,
            'Event':        event,
            'Func':         func,
            'Class_Inst':   class_instance,
            'CreationTime': creation_time,
        }

    return callbacks_dict
setAttr( hou.Node, "Callbacks", property( _node_getEventCallbacks ) )


def _node_getNumCallbacks( self ):
    """
    Author: Sean
    """
    return len( self.eventCallbacks() )
setAttr( hou.Node, "NumCallbacks", property( _node_getNumCallbacks ) )










