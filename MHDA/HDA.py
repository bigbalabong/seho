'''
Tier: Base
'''

from ..MVar import *




'''
Documenting your Assets             https://www.sidefx.com/docs/houdini/help/nodes.html
'''


HDA_Dir_SEAN = normpath( __file__, '../../../../../otls', check=False )









###########################################################################
############################ hou.HDADefinition ############################
###########################################################################
'''
hou.HDADefinition                   http://www.sidefx.com/docs/houdini/hom/hou/HDADefinition.html
'''

setAttr( hou.HDADefinition, "Filepath", property( hou.HDADefinition.libraryFilePath ) )



# ======================================================== #
# ======================= Metadata ======================= #
# ======================================================== #
setAttr( hou.HDADefinition, "Ver", property( hou.HDADefinition.version, hou.HDADefinition.setVersion ) )

setAttr( hou.HDADefinition, "Label", property( hou.HDADefinition.description, hou.HDADefinition.setDescription ) )

setAttr( hou.HDADefinition, "Comment", property( hou.HDADefinition.comment, hou.HDADefinition.setComment ) )

setAttr( hou.HDADefinition, "Icon", property( hou.HDADefinition.icon, hou.HDADefinition.setIcon ) )




# ======================================================== #
# ==================== Input / Output ==================== #
# ======================================================== #
'''
In this method, you can have zero subnet input:
    1. Set maximum inputs as 0.
    2. Set maximum inputs as what you need using python func "hou.HDADefinition.setMaxNumInputs".
        In this way, subnet input won't be created.
'''
setAttr( hou.HDADefinition, "InputsMin", property( hou.HDADefinition.minNumInputs, hou.HDADefinition.setMinNumInputs ) )
setAttr( hou.HDADefinition, "InputsMax", property( hou.HDADefinition.maxNumInputs, hou.HDADefinition.setMaxNumInputs ) )



def _hda_getInputsRange( self ):
    """
    Author: Sean
    """
    return ( self.InputsMin, self.InputsMax )

def _hda_setInputsRange( self, num_range ):
    """
    Args:
        range (list of int): [description]

    Author: Sean
    """
    self.InputsMin, self.InputsMax = num_range

setAttr( hou.HDADefinition, "InputsRange", property( _hda_getInputsRange, _hda_setInputsRange ) )







# ======================================================== #
# ======================== Subnet ======================== #
# ======================================================== #
def _hda_updateNodeBlocks( kwargs, 
                            subnet = 'subnet', start_node = 'IN', end_node = 'output0',
                            codes = None,
                            gap = 15,
                            mode = 'sequential',
                            ):
    """
    Framework for creating node blocks in editable subnet of HDA.

    Args:
        kwargs ([type]): [description]

        subnet (str): name of subnet node.
        start_node (str): name of start node.
        end_node (str): name of end node.

        codes (str): additonal codes.
        gap (int): node position offset.

        mode (str): sequential / parallel.

    Example 1:
        # Sop/sean::group_create_multi
        hou.HDADefinition.updateNodeBlocks( kwargs )

    Example 2:
        # 'Sop/sean::test_subnet_node_block_parallel'
        hou.HDADefinition.updateNodeBlocks( kwargs, end_node='merge', mode='parallel' )

    Author: Sean
    """
    # get subnet node
    subnet = kwargs['node'].node( subnet )

    # get start node and end node
    if start_node:
        start_node = subnet.node( start_node )
    end_node = subnet.node( end_node )

    # get total num of node blocks
    total_num = kwargs['parm'].Value



    # ~~~~~~ Get codes from python module ~~~~~ #
    if codes is None:
        if hasattr( kwargs['node'].hm(), 'Node_Block_Codes' ):
            codes = getattr( kwargs['node'].hm(), 'Node_Block_Codes' )
        else:
            codes = ''



    # ~~~~~~~~~~~~ Get Node Blocks ~~~~~~~~~~~~ #
    prefix = 'node_block_'
    
    blocks = [ i for i in subnet.NetworkBoxs if i.Name.startswith( prefix ) ]

    for block in blocks:
        block.Index = int( block.Name.split(prefix, 1)[1] )

    blocks.sort( key=lambda x: x.Index )

    curr_num = len( blocks )
    


    # ======================================================== #
    # ================== Update Node Blocks ================== #
    # ======================================================== #

    # delete redundant node block
    if curr_num > total_num:
        useless_blocks = blocks[ total_num: ]

        if mode == 'sequential':
            for i in useless_blocks:
                # delete network boxes with node contents
                i.destroy( True )

        else: # mode == 'parallel'
            for i in useless_blocks:
                # delete output nodes with connections
                block_output = [ j for j in i.Nodes if j.Name.startswith( 'null_output_' ) ][0]
                block_output.destroyAndBreakConnections()

                # delete network boxes with node contents
                i.destroy( True )
    

    # create new node block
    elif curr_num < total_num:
        # set position of end node temporarily to avoid 
        # potential position conflicts with new created nodes.
        end_node.P = start_node.P - nPx * 2
        end_node.layoutOutputs()


        if mode == 'sequential':
            # get last node
            if blocks:
                last_node = [ i for i in blocks[-1].Nodes if i.Name.startswith( 'null_output_' ) ][0]
            else:
                last_node = start_node


            # create new node blocks
            for index in range( curr_num, total_num ):
                # ~~~~~~~~~~~~ new network box ~~~~~~~~~~~~ #
                new_networkbox = subnet.createNetworkBox()
                new_networkbox.Name = new_networkbox.Label = '{}{}'.format( prefix, index )


                # ~~~~~~~~~~~~ Create new nodes ~~~~~~~~~~~ #
                new_nodes = []

                # start node of block
                last_node = last_node.Out0 >> 'null'
                new_nodes.append( last_node )
                last_node.P += nPy * 1
                last_node.HM2.asInput()

                # actual functional nodes.
                # record these nodes in python module of HDA
                exec( codes )
                
                # last node of block
                last_node = last_node.Out0 >> 'null'
                new_nodes.append( last_node )
                last_node.HM2.asOutput()
                

                # ~~~~ fill network box with new nodes ~~~~ #
                new_networkbox.add( new_nodes )
                new_networkbox.fitAroundContents()
                
            last_node.Out0 >> end_node.In0

        
        else: # mode == 'parallel'
            # create new node blocks
            for index in range( curr_num, total_num ):
                # ~~~~~~~~~~~~ new network box ~~~~~~~~~~~~ #
                new_networkbox = subnet.createNetworkBox()
                new_networkbox.Name = new_networkbox.Label = '{}{}'.format( prefix, index )


                # ~~~~~~~~~~~~ Create new nodes ~~~~~~~~~~~ #
                new_nodes = []

                # start node of block
                last_node = start_node.Out0 >> 'null'
                new_nodes.append( last_node )
                last_node.P = start_node.P + nPx * 2 * (index + 1) + nPy * 1
                last_node.HM2.asInput()
        
                # actual functional nodes.
                # record these nodes in python module of HDA
                exec( codes )

                # last node of block
                last_node = last_node.Out0 >> 'null'
                new_nodes.append( last_node )
                last_node.HM2.asOutput()

                print( last_node, end_node )
                end_node.setNextInput( last_node )
                

                # ~~~~ fill network box with new nodes ~~~~ #
                new_networkbox.add( new_nodes )
                new_networkbox.fitAroundContents()


    # ~~~~~~~~~~ auto-layout end node ~~~~~~~~~ #
    # subnet.layoutChildren()
    end_node.moveToGoodPosition()
    end_node.P += nPy * 2
    end_node.layoutOutputs()
setAttr( hou.HDADefinition, "updateNodeBlocks", staticmethod( _hda_updateNodeBlocks ) )
    








# ======================================================== #
# ==================== Embedded Files ==================== #
# ======================================================== #
setAttr( hou.HDADefinition, "Sections", property( hou.HDADefinition.sections ) )
setAttr( hou.HDADefinition, 'Extras', hou.HDADefinition.Sections )

def _hda_addExtra( self, name, filepath ):
    """
    Add input file as new section of HDA.

    Args:
        name (str): New extra name.
        filepath (str): [description]

    Returns:
        (hou.HDASection)
    
    Author: Sean
    """
    with open( filepath, 'rb' ) as f:
        content = f.read()
        new_extra = self.addSection( name, content )
    
    return new_extra
setAttr( hou.HDADefinition, 'addExtra', _hda_addExtra )




# ~~~~~~~~~~~~~~~~ Example ~~~~~~~~~~~~~~~~ #
class HDAExample( object ):

    """
    Author: Sean
    """

    def __init__( self, HDA, example ):
        self.HDA = HDA
        self.Type = HDA.Type
        self.Example = example

    def __repr__( self ):
        return '<HDAExample  {}>'.format( self.Example )


    def open( self, temp=True ):
        """
        Open example hip file.

        Args:
            temp (bool, optional): If true, save opened scene as a new file in temp folder.
                                    Defaults to True.

        Author: Sean
        """
        filepath = 'opdef:/{}?{}'.format( self.Type.CateFullName, self.Example )
        hou.hipFile.load( filepath )  

        if temp:
            new_filename = '{}/temp__{}'.format( hou.expandString('$TEMP'), self.Example )
            hou.hipFile.save( new_filename )      


def _hda_getExamples( self ):
    """
    Get example hip files.

    Author: Sean
    """
    examples = [ i for i in self.Extras.keys() if i.startswith( 'example_' ) and i.endswith( '.hip' ) ]

    if examples:
        return [ HDAExample( self, i ) for i in examples ]
setAttr( hou.HDADefinition, 'Examples', property( _hda_getExamples ), replace=False )









###########################################################################
############################### HDA Section ###############################
###########################################################################
'''
hou.HDASection      http://www.sidefx.com/docs/houdini/hom/hou/HDASection.html
'''

setAttr( hou.HDASection, "Name", property( hou.HDASection.name ) )

setAttr( hou.HDASection, "Definition", property( hou.HDASection.definition ) )
setAttr( hou.HDASection, 'HDA', hou.HDASection.Definition )

setAttr( hou.HDASection, "Size", property( hou.HDASection.size ) )

setAttr( hou.HDASection, "LastModification", property( hou.HDASection.modificationTime ) )









###########################################################################
################################# hou.hda #################################
###########################################################################
'''
Operator Type Properties window     https://www.sidefx.com/docs/houdini/ref/windows/optype.html
Disable when/Hide when syntax       https://www.sidefx.com/docs/houdini/ref/windows/optype.html#conditions

Disable permanently                 { isparm(invalid) == 0 }
'''

def _hda_getFolderpathsOfInstalledHDAs():
    """
    Author: Sean
    """
    hda_filepaths = hou.hda.loadedFiles()

    hda_dirs = list(set( [ os.path.dirname(i) for i in hda_filepaths ] ))
    hda_dirs.sort( lambda x: x.lower() )

    return hda_dirs
setAttr( hou.hda, 'getFolderpathsOfInstalledHDAs', _hda_getFolderpathsOfInstalledHDAs )



# ======================================================== #
# ======================== New HDA ======================= #
# ======================================================== #
def _newHDA( node, **kwargs ):
    '''
    Returns:
            New HDA definition.

    Author: Sean
    '''
    # pre-processing arguments
    if 'icon' in kwargs.keys():
        icon = kwargs['icon']
        del kwargs['icon']
    else:
        icon = None


    if node.canCreateDigitalAsset():
        # return new node which nodetype is new HDA
        new_HDA = node.createDigitalAsset( **kwargs )
        new_HDA = new_HDA.Type.HDA

    else:
        kwargs_v2 = {}
        kwargs_v2['file_name'] = kwargs['hda_file_name']
        kwargs_v2['new_name'] = kwargs['name']
        kwargs_v2['new_menu_name'] = kwargs['description']

        node.Type.HDA.copyToHDAFile( *kwargs_v2 )

        new_HDA = [ i for i in hou.hda.definitionsInFile( hda_file_name ) if i.Type.FullName == name ][0]
        # new_HDA.Icon = icon

        if not new_HDA.isInstalled():
            hou.hda.installFile( hda_filepath )

        # change nodetype to new HDA
        self.changeNodeType( new_HDA.nodeType().name() )


    if icon:
        new_HDA.Icon = icon
    
    return new_HDA


def _node_newHDA( self,
                    name = None, label = None,
                    icon = None,
                    inputs = None,
                    author = 'SEAN',
                    hda_dir = HDA_Dir_SEAN,
                ):
    """
    Create new HDA from this node.

    Args:
        name (str, optional): [description]. 
                                For example, 'group_by_connectivity'.
                                Defaults to None.
        label (str, optional): [description]. 
                                For example, 'Group by Connectivity'.
                                Defaults to None.
        inputs ((int, int), optional): Min inputs num, max inputs num. Defaults to None.
        icon (str, optional): [description]. 
                                For example, 'SOP_connectivity'.
                                Defaults to None.

    Returns:
        [type]: [description]

    Author: Sean
    """
    # ======================================================== #
    # ======================= get info ======================= #
    # ======================================================== #
    if name:
        type_name = '{}::{}'.format( author.lower(), name )

        if not label:
            label = ' '.join( [ i.capitalize() for i in name.split('_') ] )
        label = '{} {}'.format( author, label )   


        # retrieve versions from installed hda
        all_versions = [ i for i in self.Type.Cate.Nodetypes if i.Name == type_name ]
        if not all_versions:
            version_latest = 0.0
        else:
            all_versions.sort( key = lambda x: x.Ver )
            version_latest = all_versions[-1].Ver


        if inputs:
            inputsNum_min, inputsNum_max = inputs
        else:
            inputsNum_min, inputsNum_max = (1,1)


        hda_basename = '{}__{}.hda'.format( self.Type.Cate.Name.lower(), name )
        hda_filepath = os.path.join( hda_dir, hda_basename )  

        new_version = str( version_latest + 0.1 ) 
        type_fullname = '{}::{}'.format( type_name, new_version )    


    else:
        type_latest = self.Type.VerLatest
        
        type_name = self.Type.Name

        if label:
            label = '{} {}'.format( author, label )
        else:
            label = self.Type.Label


        version_latest = type_latest.Ver


        if inputs:
            inputsNum_min, inputsNum_max = inputs
        else:
            inputsNum_min = type_latest.HDA.InputsNumMin
            inputsNum_max = type_latest.HDA.InputsNumMax


        if not icon:
            icon = self.Type.Icon


        hda_filepath = self.Type.HDA.Path

        new_version = str(version_latest + 0.1) 
        type_fullname = '{}::{}'.format( type_name, new_version )    



    # ======================================================== #
    # ======================== new HDA ======================= #
    # ======================================================== #
    # if the hda filepath has already exist, the new hda definition will be appended to the existing hda file.
    new_HDA = _newHDA( self, 
                        hda_file_name = hda_filepath,
                        name = type_fullname, description = label,
                        min_num_inputs = inputsNum_min, max_num_inputs = inputsNum_max,
                        version = new_version,
                        icon = icon,
                    )        

    print( 'New HDA has been created successfully.' )

    return new_HDA
setAttr( hou.Node, 'newHDA', _node_newHDA  )




# ~~~~~~~~~~~~ Background Image ~~~~~~~~~~~ #
def _node_createEmbeddedTempBGImagesHDA():
    """
    Author: Sean
    """
    # get all opened nodes (network, subnet, unlocked HDA) with background images
    nodes = ROOT.AllOpenedNetworks
    nodes = [ i for i in nodes if 'backgroundimages' in i.userDataDict().keys() ]

    if not nodes:
        return
    

    # get all background images
    images = [ i.BGImages for i in nodes ]
    images = L_( images ).sum( setized=True )
    # get images with external link
    images = [ i for i in images if not i.startswith( 'opdef:' ) ]

    print( '\n\n Background Images:' )
    for i in images: print( i )



    # ======================================================== #
    # ========================== HDA ========================= #
    # ======================================================== #

    # check existence of temp HDA
    if not hou.node( '/obj/Temp_BG_Images' ):

        # new node
        temp_node = hou.node('/obj').createNode('subnet', 'Temp_BG_Images')
        temp_node.Color = hou.Color.Black
        temp_node.Shape = 'circle'

        # new note
        note = temp_node.createStickyNote()
        note.Text = 'This embeded HDA contains background images.'
        note.setSize( (6, 1) )

        # new embedded HDA
        hda_name = 'temp_bg_images'
        temp_hda = temp_node.createDigitalAsset( name = hda_name, description = 'Temp BG Images',
                                                min_num_inputs = 0, max_num_inputs = 0,
                                                save_as_embedded = True ).Type.HDA

    else:
        temp_hda = hou.node( '/obj/Temp_BG_Images' ).HDA

    
    # ~~~~~~~~~~ add new extra files ~~~~~~~~~~ #
    existing_extras = temp_hda.Extras.keys()
    prefix = 'BGImage/'
    for i in images:
        i = hou.expandString( i )                   # convert "$HIP/a.jpg" to absolute filepath.

        # add extra files
        extra_name = '{}{}'.format( prefix, os.path.basename( i ) )

        if extra_name not in existing_extras:
            temp_hda.addExtra( extra_name, i )



    # ======================================================== #
    # =============== Update Background Images =============== #
    # ======================================================== #
    for node in nodes:
        # get new description
        description = node.userDataDict()['backgroundimages']

        old_images = node.BGImages
        old_images = [ i for i in old_images if not i.startswith( 'opdef:' ) ]
        old_images = list(set( old_images ))
        new_images = [ 'opdef:/Object/{}?{}{}'.format( hda_name, prefix, os.path.basename(i) ) for i in old_images ]
        
        for old, new in zip( old_images, new_images ):
            description = description.replace( old, new )

        # update user data dict
        node.setUserData( 'backgroundimages', description )


    print( 'Embedded Temp BG Images HDA has been created.' )

    return temp_hda
setAttr( hou.hda, "createEmbeddedTempBGImagesHDA", _node_createEmbeddedTempBGImagesHDA )
    








def _nodetypeNotes_bak( nodetype, notes_filepath ):
    """
    Author: Sean
    """
    if isinstance( nodetype, hou.Node ):
        nodetype = nodetype.type()


    # nodetype_name = nodetype.name()
    # nodetype_cate = nodetype.category().name()


    # file_name = '[{}]{}'.format( nodetype_cate, '__'.join(nodetype.nameComponents()[1:]) )

    # file_path = '{}/{}.hda'.format( hda_notes_path, file_name )


    new_name = list( nodetype.nameComponents() )
    new_name[2] += '_notes'
    new_name = [ i for i in new_name if i ]
    new_name = '::'.join( new_name )

    new_menu_name = '{} (notes)'.format( nodetype.description() )
    

    new_hda_file = nodetype.definition().copyToHDAFile( notes_filepath, new_name, new_menu_name )


def updateEditableSubnet( func ):

    def wrapper( *args, **kwargs ):

        # print 'args', args.__len__(), args
        # print 'kwargs', kwargs.keys(), kwargs

        # initialize variables
        hda_node = args[0]['node']
        subnet_node = hda_node.node( kwargs['subnet_node'] )
        subnet_in = subnet_node.node( 'INPUT' )
        subnet_out = subnet_node.node( 'OUTPUT' )

        nodetype_name = kwargs['nodetype_name']
        num = args[0]['parm'].eval()
        observer_parms = kwargs['observer_parms']
        observed_parms = kwargs['observed_parms']
        layout = kwargs['layout']

        # print hda_node, type(hda_node)
        # print subnet_node, type(subnet_node)
        # print num


        # get existing nodes
        existing_nodes = [ i for i in subnet_node.children() if i.type().name() == nodetype_name ]
        existing_num = existing_nodes.__len__()
        

        # get last node
        if existing_nodes:
            last_node = existing_nodes[-1]
        else:
            last_node = subnet_in
        
            


        # update subnet
        if existing_nodes.__len__() > num:
            for i in existing_nodes[num:]:
                i.destroy()
                
        
        elif existing_nodes.__len__() < num:
        
            for i in range( existing_nodes.__len__(), num ):
            
                # create node
                new_node = last_node.createOutputNode( 'groupcreate', 'group{}'.format( str(i+1) ) )
                    

                # build parm references
                if observer_parms:

                    # auto find the observed parm
                    if not observed_parms:
                        observer_list = [ new_node.parm(j) for j in observer_parms ]
                        observed_list = [ hda_node.parm(j+str(i+1)) for j in observer_parms ]
                        
                        reference_pair_list = zip( observer_list,  observed_list )
                        for observer, observed in reference_pair_list:
                            observer.set( observed, language=hou.exprLanguage.Hscript, follow_parm_reference=True )




                # custom funciton
                kwargs['loop_index'] = i
                func( *args, **kwargs )




                # update last group node
                last_node = new_node
                

            # update input connection of output
            subnet_out.setInput( 0, last_node, 0 )
                            
                
        else:
            return


        # auto-layout
        subnet_node.layoutChildren( subnet_node.allItems() )


    return wrapper








