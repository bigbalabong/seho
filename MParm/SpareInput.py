'''
Tier: Base
'''

from ..MVar import *






###########################################################################
############################### Spare Input ###############################
###########################################################################

def _parm_getSpareInputs( self ):
    """
    Returns:
        [hou.Parm]: spare input parameters (hou.StringParmTemplate).
    
    Author: Sean
    """
    spare_input_parms = [ i for i in self.Parms if i.Name.startswith( 'spare_input' ) ]
    spare_input_parms = [ i for i in spare_input_parms if i.Name.split( 'spare_input', 1 )[1].isdigit() ]
    return spare_input_parms
setAttr( hou.Node, 'SpareInputs', property( _parm_getSpareInputs ), replace=False )


def _node_addSpareInputsAuto( self ):
    """
    Author: Sean
    """
    # get references
    ref_nodes = self.References

    # get spare inpputs
    spare_inputs = self.SpareInputs
    spare_inputs_nodes = [ self.node( i ) for i in spare_inputs ]

    # get nodes need to be added
    new_nodes = list(set(ref_nodes) - set(spare_inputs_nodes))
    new_nodepaths = [ self.relativePathTo( i ) for i in new_nodes ]

    # create new spare input parm
    new_tmps = []
    for i in new_nodepaths:
        new_template = self.addSpareInput( node_path = i )
        new_tmps.append( new_template )

    return new_tmps
setAttr( hou.Node, 'addSpareInputsAuto', _node_addSpareInputsAuto, replace=False )




SpareInput_MultiParm_Callback = '''node = kwargs['node']
for i in range(0, kwargs['parm']._):
    spare_input = 'spare_input{{}}'.format(i)
    if not node._[ spare_input ]:
        codes = "chs('fake_spare_input{{}}')".format( i+1 )
        spare_input = node.addStr( 
                    spare_input, spare_input, expr=(codes,), 
                    hidden = {},
                    insert_before=kwargs['parm'].ParmTemplate.Name )
'''

def _node_addSpareInputMultiParm( self, hide_spare_input=True, folder=None ):
    """
    Add multi-parm for spare inputs.

    Args:
        hide_spare_input (bool, optional): If true, hide real spare input parameters. 
                                            Defaults to True.
    """
    # ~~~~~~~~~~~~~ add seperator ~~~~~~~~~~~~~ #
    # put the incoming multi-parm at the top
    if folder is None:
        sep = self._['sep_spare_inputs']

        if sep:
            sep = sep.ParmTemplate
        else:
            sep = self.addSep( 'sep_spare_inputs', insert_at_top = True )
    
    # put the incoming multi-parm in the folder
    else:
        sep = None


    # ~~~~~~~~~~~~~ add multi-parm ~~~~~~~~~~~~ #
    tmp = self.addStr( 'fake_spare_input#', 'Spare Input -#', add=False )
    
    codes = SpareInput_MultiParm_Callback.format( hide_spare_input )

    multi_parm = self.addMultiParm( 
                                    'fake_spare_inputs', 'Spare Inputs', 
                                    parm_templates = (tmp,), 
                                    callback = codes,
                                    insert_before = sep,
                                    folder = folder,
                                )
setAttr( hou.Node, 'addSpareInputMultiParm', _node_addSpareInputMultiParm, replace=False )



def _node_addSpareInput( self, 
                            node=None, label=None, 
                            folder=None,
                        ):
    """
    Add spare input parameter.

    Args:
        node (hou.Node): [description]
        node_path (str, optional): Node path to reference. Defaults to ''.

    Returns:
        [hou.StringParmTemplate]: [description]
    
    Author: Sean
    """
    # get node path
    if node is not None:
        if isinstance( node, str ):
            node_path = node
        else:
            node_path = self.relativePathTo( node )


    # get existing spare inputs
    spare_input_parms = self.SpareInputs
    num = len( spare_input_parms )


    # ======================================================== #
    # ================= new spare input parm ================= #
    # ======================================================== #
    parm_name = 'spare_input{}'.format( num )
    parm_label = 'Spare Input {}'.format( num ) if label is None else label

    if folder:
        new_tmp = self.addStr( name = parm_name,
                                label = parm_label,
                                folder = folder,
                                )

    # new parm and seperator
    else:
        if num == 0:
            new_tmp = self.addStr( name = parm_name,
                                    label = parm_label,
                                    insert_at_top = True,
                                    folder = folder,
                                    )
            self.addSep( 'sep_spare_inputs', insert_after = new_tmp )

        # new parm
        else:
            sep = self._['sep_spare_inputs']
            if sep:
                sep = sep.ParmTemplate

            new_tmp = self.addStr( name = parm_name,
                                    label = parm_label,
                                    insert_before = sep,
                                    folder = folder,
                                    )


    # ======================================================== #
    # ==================== post-processing =================== #
    # ======================================================== #
    if node_path:
        self._[parm_name]._ = node_path


    return new_tmp
setAttr( hou.Node, 'addSpareInput', _node_addSpareInput, replace=False )







