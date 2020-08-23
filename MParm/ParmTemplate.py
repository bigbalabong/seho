'''
Tier: Base
'''

from ..MVar import *




###########################################################################
############################## Parm Template ##############################
###########################################################################
'''
hou.ParmTemplate        http://www.sidefx.com/docs/houdini/hom/hou/ParmTemplate.html
'''

setAttr( hou.ParmTemplate, "Name", property( hou.ParmTemplate.name, hou.ParmTemplate.setName ) )

setAttr( hou.ParmTemplate, "Label", property( hou.ParmTemplate.label, hou.ParmTemplate.setLabel ) )

setAttr( hou.ParmTemplate, "LabelHidden", property( hou.ParmTemplate.isLabelHidden, hou.ParmTemplate.hideLabel ) )



def _parmTemplate_getType( self ):
    '''
    hou.parmTemplateType        http://www.sidefx.com/docs/houdini/hom/hou/parmTemplateType.html
    
    RETURN:
            (str) int / float / string / toggle / menu / button / folderset / separator / label / ramp
    
    Author: Sean
    '''
    return str(self.type()).rsplit('.',1)[1].lower()
setAttr( hou.ParmTemplate, "Type", property( _parmTemplate_getType ), replace=False )
# setAttr( hou.ParmTemplate, "Type", property( hou.ParmTemplate.type ), replace=False )


def _parmTemplate_getDataType( self ):
    '''
    hou.parmData        http://www.sidefx.com/docs/houdini/hom/hou/parmData.html

    RETURN:
            (str) int / float / string / ramp
    
    Author: Sean
    '''
    return str( self.dataType() ).rsplit('.',1)[1].lower()
setAttr( hou.ParmTemplate, "DataType", property( _parmTemplate_getDataType ) )
setAttr( hou.ParmTemplate, "ValueType", property( _parmTemplate_getDataType ) )



setAttr( hou.ParmTemplate, "Help", property( hou.ParmTemplate.help, hou.ParmTemplate.setHelp ) )



# ======================================================== #
# ======================== Folder ======================== #
# ======================================================== #
def _parmTemplate_getContainingFolder( self ):
    """
    Author: Sean
    """
    try:
        folder = self.ParmTemplateGrp.containingFolder( self )
        return folder
    except:
        return None
setAttr( hou.ParmTemplate, "Folder", property( hou.ParmTemplate.help, hou.ParmTemplate.setHelp ) )


# def _parmTemplate_getContainingFolder( self ):
#     try:
#         folder = self.ParmTemplateGrp.containingFolder( self )
#         return folder
#     except:
#         return None
# setAttr( hou.ParmTemplate, "FolderSet", property( hou.ParmTemplate.help, hou.ParmTemplate.setHelp ) )




setAttr( hou.ParmTemplate, "Hidden", property( hou.ParmTemplate.isHidden, hou.ParmTemplate.hide ) )



def _parmTemplate_joinWithNext( self, parm=None ):
    """
    Author: Sean
    """
    if parm:
        self.setJoinWithNext( True )
    else:
        self.setJoinWithNext( False )
setAttr( hou.ParmTemplate, '__rshift__', _parmTemplate_joinWithNext )







def _parmTemplate_apply( self ):
    """
    Author: Sean
    """
    grp = self.ParmTemplateGrp
    grp.replace( self.Name, self )
    grp.apply()
setAttr( hou.ParmTemplate, 'apply', _parmTemplate_apply )


def _parmTemplate_applyToHDA( self ):
    """
    Author: Sean
    """
    grp = self.ParmTemplateGrp
    grp.replace( self.Name, self )
    grp.applyToHDA()
setAttr( hou.ParmTemplate, 'applyToHDA', _parmTemplate_applyToHDA )


def _parmTemplate_destroy( self ):
    """
    Author: Sean
    """
    grp = self.ParmTemplateGrp
    grp.remove( self )
    grp.apply()
setAttr( hou.ParmTemplate, 'destroy', _parmTemplate_destroy )








# ======================================================== #
# ======================= Condition ====================== #
# ======================================================== #
'''
Disable when/Hide when syntax   https://www.sidefx.com/docs/houdini/ref/windows/optype.html#conditions
    ninputs()           
            The highest wired input number. 
            This may be more than the number of wires if inputs in the middle are not connected. 
            It also counts subnet inputs that may not be wired in the parent node.

    hasinput(n)         
            Returns 1 if the given input number is connected, or 0 if not. 
            This does not count an input wired into a subnet input if that input is not also wired in the parent node.

            Examples:
                { hasinput(2) == 0 }      

    isparm(parmname)    
            Returns 1 if this parameter's name is parmname. 
            This is meant for use with multiparm items.
            For example, this rule would apply to the first item in a multiparm named blend, but not the second (blend1), third (blend2), and so on:
            { isparm(blend0) == 1 }
'''

setAttr( hou.ParmTemplate, "Conditions", property( hou.ParmTemplate.conditionals ) )



def _parmTemplate_getHideWhen( self ):
    """
    Author: Sean
    """
    return self.Conditions[ hou.parmCondType.HideWhen ]

def _parmTemplate_setHideWhen( self, codes ):
    """
    Author: Sean
    """
    self.setConditional( hou.parmCondType.HideWhen, codes )

setAttr( hou.ParmTemplate, "HideWhen", property( _parmTemplate_getHideWhen, _parmTemplate_setHideWhen ) )



def _parmTemplate_getDisableWhen( self ):
    """
    Author: Sean
    """
    return self.Conditions[ hou.parmCondType.DisableWhen ]

def _parmTemplate_setDisableWhen( self, codes ):
    """
    Author: Sean
    """
    self.setConditional( hou.parmCondType.DisableWhen, codes )

setAttr( hou.ParmTemplate, "DisableWhen", property( _parmTemplate_getDisableWhen, _parmTemplate_setDisableWhen ) )



def _parmTemplate_isDisabled( self ):
    """
    Author: Sean
    """
    return self.DisableWhen

def _parmTemplate_setDisabled( self, state ):
    """
    Disable permanently.

    Args:
        state (bool): [description]
    
    Author: Sean
    """
    if state:
        hou.ParmTemplate.DisableWhen = '{ isparm( never_exist ) == 0 }'
    # else:
    #     hou.ParmTemplate.DisableWhen = 

setAttr( hou.ParmTemplate, "Disabled", property( _parmTemplate_isDisabled, _parmTemplate_setDisabled ) )



def _parmTemplate_getNoCookWhen( self ):
    """
    Author: Sean
    """
    return self.Conditions[ hou.parmCondType.NoCookWhen ]

def _parmTemplate_setNoCookWhen( self, codes ):
    """
    Author: Sean
    """
    self.setConditional( hou.parmCondType.NoCookWhen, codes )

setAttr( hou.ParmTemplate, "NoCookWhen", property( _parmTemplate_getNoCookWhen, _parmTemplate_setNoCookWhen ) )







# ======================================================== #
# =================== Int Parm Template ================== #
# ======================================================== #
'''
hou.IntParmTemplate     http://www.sidefx.com/docs/houdini/hom/hou/IntParmTemplate.html
'''

# ~~~~~~~~~~~~~~~~ Default ~~~~~~~~~~~~~~~~ #
setAttr( hou.IntParmTemplate, "Default", property( hou.IntParmTemplate.defaultValue, hou.IntParmTemplate.setDefaultValue ) )

setAttr( hou.IntParmTemplate, "DefaultExpr", property( hou.IntParmTemplate.defaultExpression, hou.IntParmTemplate.setDefaultExpression ) )

setAttr( hou.IntParmTemplate, "DefaultExprLanguage", 
            property( hou.IntParmTemplate.defaultExpressionLanguage, hou.IntParmTemplate.setDefaultExpressionLanguage ) )

setAttr( hou.IntParmTemplate, "Min", property( hou.IntParmTemplate.minValue, hou.IntParmTemplate.setMinValue ) )
setAttr( hou.IntParmTemplate, "Max", property( hou.IntParmTemplate.maxValue, hou.IntParmTemplate.setMaxValue ) )

setAttr( hou.IntParmTemplate, "LockMin", property( hou.IntParmTemplate.minIsStrict, hou.IntParmTemplate.setMinIsStrict ) )
setAttr( hou.IntParmTemplate, "LockMax", property( hou.IntParmTemplate.maxIsStrict, hou.IntParmTemplate.setMaxIsStrict ) )



# ~~~~~~~~~~~~~~~~~~ Menu ~~~~~~~~~~~~~~~~~ #
setAttr( hou.IntParmTemplate, "MenuType", property( hou.IntParmTemplate.menuType, hou.IntParmTemplate.setMenuType ) )

setAttr( hou.IntParmTemplate, "MenuLabels", property( hou.IntParmTemplate.menuLabels ) )

def _intParmTemplate_getMenuValues( self ):
    """
    Author: Sean
    """
    return [ int(i) for i in self.menuItems() ]
setAttr( hou.IntParmTemplate, "MenuValues", property( _intParmTemplate_getMenuValues, hou.IntParmTemplate.setMenuItems ) )

def _intParmTemplate_getMenuItems( self ):
    """
    Author: Sean
    """
    return zip( self.MenuLabels, self.MenuValues )
setAttr( hou.IntParmTemplate, "MenuItems", property( _intParmTemplate_getMenuItems ) )

setAttr( hou.IntParmTemplate, "MenuIcons", property( hou.IntParmTemplate.iconNames, hou.IntParmTemplate.setIconNames ) )







# ======================================================== #
# ================== Float Parm Template ================= #
# ======================================================== #
'''
hou.FloatParmTemplate   http://www.sidefx.com/docs/houdini/hom/hou/FloatParmTemplate.html
'''

setAttr( hou.FloatParmTemplate, "Default", property( hou.FloatParmTemplate.defaultValue, hou.FloatParmTemplate.setDefaultValue ) )

setAttr( hou.FloatParmTemplate, "DefaultExpr", 
            property( hou.FloatParmTemplate.defaultExpression, hou.FloatParmTemplate.setDefaultExpression ) )

setAttr( hou.FloatParmTemplate, "DefaultExprLanguage", 
            property( hou.FloatParmTemplate.defaultExpressionLanguage, hou.FloatParmTemplate.setDefaultExpressionLanguage ) )

setAttr( hou.FloatParmTemplate, "Min", property( hou.FloatParmTemplate.minValue, hou.FloatParmTemplate.setMinValue ) )
setAttr( hou.FloatParmTemplate, "Max", property( hou.FloatParmTemplate.maxValue, hou.FloatParmTemplate.setMaxValue ) )

setAttr( hou.FloatParmTemplate, "LockMin", property( hou.FloatParmTemplate.minIsStrict, hou.FloatParmTemplate.setMinIsStrict ) )
setAttr( hou.FloatParmTemplate, "LockMax", property( hou.FloatParmTemplate.maxIsStrict, hou.FloatParmTemplate.setMaxIsStrict ) )








# ======================================================== #
# ================= String Parm Template ================= #
# ======================================================== #
'''
hou.StringParmTemplate  http://www.sidefx.com/docs/houdini/hom/hou/StringParmTemplate.html
'''

# ~~~~~~~~~~~~~~~~ Default ~~~~~~~~~~~~~~~~ #
setAttr( hou.StringParmTemplate, "Default", property( hou.StringParmTemplate.defaultValue, hou.StringParmTemplate.setDefaultValue ) )

setAttr( hou.StringParmTemplate, "DefaultExpr", property( hou.StringParmTemplate.defaultExpression, hou.StringParmTemplate.setDefaultExpression ) )

setAttr( hou.StringParmTemplate, "DefaultExprLanguage", 
            property( hou.StringParmTemplate.defaultExpressionLanguage, hou.StringParmTemplate.setDefaultExpressionLanguage ) )



# ~~~~~~~~~~~~~~~~~~ Type ~~~~~~~~~~~~~~~~~ #
def _strParmTmp_setStringType( self, string_type='regular' ):
    """
    Args:
        string_type (str, optional): regular / file / node / node_list. 
                                    Defaults to 'regular'.
    
    Author: Sean
    """
    string_type = string_type.lower()

    if string_type == 'regular':
        self.setStringType( hou.stringParmType.Regular )
    elif string_type == 'file':
        self.setStringType( hou.stringParmType.FileReference )
    elif string_type == 'node':
        self.setStringType( hou.stringParmType.NodeReference )
    elif string_type == 'node_list':
        self.setStringType( hou.stringParmType.NodeReferenceList )
setAttr( hou.StringParmTemplate, "StringType", property( hou.StringParmTemplate.stringType, _strParmTmp_setStringType ), replace=False )

setAttr( hou.StringParmTemplate, "FileType", property( hou.StringParmTemplate.fileType, hou.StringParmTemplate.setFileType ), replace=False )


setAttr( hou.StringParmTemplate, "Icons", property( hou.StringParmTemplate.iconNames, hou.StringParmTemplate.setIconNames ), replace=False )



# ~~~~~~~~~~~~~~~~~~ Menu ~~~~~~~~~~~~~~~~~ #
setAttr( hou.StringParmTemplate, "MenuType", property( hou.StringParmTemplate.menuType, hou.StringParmTemplate.setMenuType ) )


setAttr( hou.StringParmTemplate, "MenuLabels", property( hou.StringParmTemplate.menuLabels, hou.StringParmTemplate.setMenuLabels ) )
setAttr( hou.StringParmTemplate, "MenuValues", property( hou.StringParmTemplate.menuItems, hou.StringParmTemplate.setMenuItems ) )


def _stringParmTemplate_getMenuItems( self ):
    """
    Author: Sean
    """
    return zip( self.MenuValues, self.MenuLabels )

def _stringParmTemplate_setMenuItems( self, items ):
    """
    Author: Sean
    """
    values, labels = zip( *items )
    self.MenuValues = values
    self.MenuLabels = labels
    
setAttr( hou.StringParmTemplate, "MenuItems", 
            property( _stringParmTemplate_getMenuItems, _stringParmTemplate_setMenuItems ), replace=False )





setAttr( hou.StringParmTemplate, "GeneratorScript", 
            property( hou.StringParmTemplate.itemGeneratorScript, hou.StringParmTemplate.setItemGeneratorScript ), replace=False )

setAttr( hou.StringParmTemplate, "GeneratorScriptLanguage", 
            property( hou.StringParmTemplate.itemGeneratorScriptLanguage, hou.StringParmTemplate.setItemGeneratorScriptLanguage ), replace=False )







# ======================================================== #
# ================== Menu Parm Template ================== #
# ======================================================== #
'''
hou.MenuParmTemplate    http://www.sidefx.com/docs/houdini/hom/hou/MenuParmTemplate.html
'''

setAttr( hou.MenuParmTemplate, "DefaultExpr", 
            property( hou.MenuParmTemplate.defaultExpression, hou.MenuParmTemplate.setDefaultExpression ) )
setAttr( hou.MenuParmTemplate, "DefaultExprLanguage", 
            property( hou.MenuParmTemplate.defaultExpressionLanguage, hou.MenuParmTemplate.setDefaultExpressionLanguage ) )








# ======================================================== #
# ================= Folder Parm Template ================= #
# ======================================================== #
'''
hou.FolderParmTemplate      http://www.sidefx.com/docs/houdini/hom/hou/FolderParmTemplate.html
'''

setAttr( hou.FolderParmTemplate, "ParmTemplates", property( hou.FolderParmTemplate.parmTemplates ) )


setAttr( hou.FolderParmTemplate, "FolderType", 
            property( hou.FolderParmTemplate.folderType, hou.FolderParmTemplate.setFolderType ) )


setAttr( hou.FolderParmTemplate, "DefaultValue", 
            property( hou.FolderParmTemplate.defaultValue, hou.FolderParmTemplate.setDefaultValue ) )




'''
hou.FolderSetParmTemplate   http://www.sidefx.com/docs/houdini/hom/hou/FolderSetParmTemplate.html
'''

setAttr( hou.FolderSetParmTemplate, "FolderNames", 
            property( hou.FolderSetParmTemplate.folderNames, hou.FolderSetParmTemplate.setFolderNames ) )

setAttr( hou.FolderSetParmTemplate, "FolderType", 
            property( hou.FolderSetParmTemplate.folderType, hou.FolderSetParmTemplate.setFolderType ) )








###########################################################################
########################### Parm Template Group ###########################
###########################################################################
'''
hou.ParmTemplateGroup       http://www.sidefx.com/docs/houdini/hom/hou/ParmTemplateGroup.html
'''

def _parmTemplateGrp_insertAtTop( self, parm_template ):
    """
    Author: Sean
    """
    first_tmp = self.ParmTemplates[0]
    self.insertBefore( first_tmp, parm_template )
setAttr( hou.ParmTemplateGroup, 'insertAtTop', _parmTemplateGrp_insertAtTop )


def _parmTemplateGrp_apply( self ):
    """
    Change the spare parameters for this node.
    
    Author: Sean
    """
    self.Node.setParmTemplateGroup( self )
setAttr( hou.ParmTemplateGroup, "apply", _parmTemplateGrp_apply )


def _parmTemplateGrp_applyToHDA( self ):
    """
    Change the parameters for this digital asset.
    The HDA dosn't need to be unlocked.
    
    Author: Sean
    """
    self.Node.HDA.setParmTemplateGroup( self )
setAttr( hou.ParmTemplateGroup, "applyToHDA", _parmTemplateGrp_applyToHDA )









