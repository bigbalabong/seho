'''
Tier: Base
'''

from ..MVar import *





###########################################################################
############################### hou.NodeType ##############################
###########################################################################
setAttr( hou.NodeType, "ParmTemplateGrp", property( hou.NodeType.parmTemplateGroup ) )

def _nodetype_getParmTemplates( self ):
    """
    Author: Sean
    """
    templates = self.parmTemplates()
    for i in templates:
        setAttr( i, 'Nodetype', self )
        copyAttr( i, 'Node', self, 'Node' )
    return templates
setAttr( hou.NodeType, "ParmTemplates", property( _nodetype_getParmTemplates ) )
setAttr( hou.NodeType, 'Templates', hou.NodeType.ParmTemplates )




# ======================================================== #
# ========================== HDA ========================= #
# ======================================================== #
setAttr( hou.HDADefinition, "ParmTemplateGrp", 
            property( hou.HDADefinition.parmTemplateGroup, hou.HDADefinition.setParmTemplateGroup ) )







###########################################################################
################################# hou.Node ################################
###########################################################################
setAttr( hou.Node, "Parms", property( hou.Node.parms ) )

def _node_getParmNames( self ):
    '''
    RETURN:
            All names of parameters.
    
    Author: Sean
    '''
    return [ i.Name for i in self.Parms ]
setAttr( hou.Node, "ParmNames", property( _node_getParmNames ) )


setAttr( hou.Node, "ParmTuples", property( hou.Node.parmTuples ) )

def _node_getParmTupleNames( self ):
    '''
    RETURN:
            All names of parameter tuples.
    
    Author: Sean
    '''
    return [ i.Name for i in self.ParmTuples ]
setAttr( hou.Node, "ParmTupleNames", property( _node_getParmTupleNames ) )


def _node_getParmsKey( self ):
    '''
    RETURN:
            Parameters with keyframes.
    
    Author: Sean
    '''
    return [ i for i in self.Parms if i.Keys ]
setAttr( hou.Node, "ParmsKey", property( _node_getParmsKey ) )


def _node_getParmsExp( self ):
    '''
    RETURN:
            Parameters with expression.
    
    Author: Sean
    '''
    return [ i for i in self.Parms if i.Expr ]
setAttr( hou.Node, "ParmsExp", property( _node_getParmsExp ) )


setAttr( hou.Node, "SpareParms", property( hou.Node.spareParms ) )


def _node_getFolderParmTemplates( self ):
    """
    Author: Sean
    """
    return [ i for i in self.Parms if isinstance( i.ParmTemplate, hou.FolderParmTemplate ) ]
setAttr( hou.Node, "FolderParms", property( _node_getFolderParmTemplates ) )

def _node_getFolderSetParmTemplates( self ):
    """
    Author: Sean
    """
    return [ i for i in self.Parms if isinstance( i.ParmTemplate, hou.FolderSetParmTemplate ) ]
setAttr( hou.Node, "FolderSetParms", property( _node_getFolderSetParmTemplates ) )


setAttr( hou.Node, "ParmTemplateGrp", property( hou.Node.parmTemplateGroup ) )


def _node_getParmsIO( self ):
    """
    Author: Sean
    """
    pass
setAttr( hou.Node, "ParmsIO", property( _node_getParmsIO ) )







###########################################################################
################################# hou.Parm ################################
###########################################################################
setAttr( hou.Parm, "ParmTuple", property( hou.Parm.tuple ) )


def _parm_getParmTemplate( self ):
    """
    Author: Sean
    """
    template = self.parmTemplate()
    setAttr( template, 'Parm', self )
    copyAttr( template, 'Node', self, 'Node' )
    return template
setAttr( hou.Parm, "ParmTemplate", property( _parm_getParmTemplate ) )
setAttr( hou.Parm, "Tmp", hou.Parm.ParmTemplate )







###########################################################################
############################## hou.ParmTuple ##############################
###########################################################################
def _parmTuple_getParms( self ):
    """
    Author: Sean
    """
    num = self.__len__()
    parms = [ self[i] for i in range(num) ]
    return parms
setAttr( hou.ParmTuple, "Parms", property( _parmTuple_getParms ) )


setAttr( hou.ParmTuple, "ParmTemplate", property( hou.ParmTuple.parmTemplate ) )
setAttr( hou.ParmTuple, "Tmp", hou.ParmTuple.ParmTemplate )






###########################################################################
############################# hou.ParmTemplate ############################
###########################################################################
def _parmTemplate_getParmTemplateGrp( self ):
    """
    Author: Sean
    """
    return self.Node.ParmTemplateGrp
setAttr( hou.ParmTemplate, "ParmTemplateGrp", property( _parmTemplate_getParmTemplateGrp ) )







###########################################################################
########################## hou.ParmTemplateGroup ##########################
###########################################################################
def _parmTemplateGrp_getParmTemplates( self ):
    """
    Author: Sean
    """
    templates = self.parmTemplates()

    for i in templates:
        setAttr( i, 'ParmTemplateGroup', self )
        copyAttr( i, 'Node', self, 'Node' )
        copyAttr( i, 'Nodetype', self, 'Nodetype' )

    return templates
setAttr( hou.ParmTemplateGroup, "ParmTemplates", property( _parmTemplateGrp_getParmTemplates ) )


def _parmTemplateGrp_getParmTemplateNames( self ):
    """
    Author: Sean
    """
    return [ i.Name for i in self.ParmTemplates ]
setAttr( hou.ParmTemplateGroup, "ParmTemplateNames", property( _parmTemplateGrp_getParmTemplateNames ) )





def _parmTemplateGrp_getFolderParmTemplates( self ):
    """
    Author: Sean
    """
    return [ i for i in self.ParmTemplates if isinstance( i, hou.FolderParmTemplate ) ]
setAttr( hou.ParmTemplateGroup, "FolderParmTemplates", property( _parmTemplateGrp_getFolderParmTemplates ) )

def _parmTemplateGrp_getSpareFolderParmTemplate( self ):
    """
    Author: Sean
    """
    spare_folder = [ i for i in self.FolderParmTemplates if i.Label == 'Spare' and i.FolderType == hou.folderType.Tabs ]
    if spare_folder:
        return spare_folder[0]
setAttr( hou.ParmTemplateGroup, "SpareFolderParmTemplate", property( _parmTemplateGrp_getSpareFolderParmTemplate ) )


def _parmTemplateGrp_getFolderSetParmTemplates( self ):
    """
    Author: Sean
    """
    return [ i for i in self.ParmTemplates if isinstance( i, hou.FolderSetParmTemplate ) ]
setAttr( hou.ParmTemplateGroup, "FolderSetParmTemplates", property( _parmTemplateGrp_getFolderSetParmTemplates ) )












