'''
Tier: Base
'''

from ..MVar import *






###########################################################################
############################# Spare Parameter #############################
###########################################################################

def _node_hideAllParms( self ):
    """
    Hide all parameters (including built-in parms and spare parms).

    Author: Sean
    """
    grp = self.ParmTemplateGrp
    all_tmps = grp.ParmTemplates

    for i in all_tmps:
        i.Hidden = True

    new_grp = hou.ParmTemplateGroup( all_tmps )
    self.setParmTemplateGroup( new_grp )
setAttr( hou.Node, "hideAllParms", _node_hideAllParms, replace=False )


setAttr( hou.Node, 'clearParms', hou.Node.removeSpareParms )





# ======================================================== #
# ===================== New Parameter ==================== #
# ======================================================== #

def _parm_addParm( self, 
                        new_parmTmp, 

                        add = True,

                        spare_folder = False,
                        folder = None,

                        insert_at_top = False,
                        insert_before = None, 
                        insert_after = None, 

                        as_parm = False
                    ):
    """
    Add new parameter.

    Author: Sean
    """       
    setAttr( new_parmTmp, 'Node', self )

    if not add:
        return new_parmTmp

    grp = self.parmTemplateGroup()


    # put the new parm at the end of spare folder
    if spare_folder:
        # get spare folder
        spare_folder = grp.SpareFolderParmTemplate
        if not spare_folder:
            raise Exception( "There's no spare folder." )
        
        spare_folder.addParmTemplate( new_parmTmp )
        grp.replace( spare_folder.Name, spare_folder )


    # put the new parm in the folder
    elif folder:
        folder.addParmTemplate( new_parmTmp )
        grp.replace( folder.Name, folder )


    else:
        # put the new parm at the top of parm interface.
        if insert_at_top:
            grp.insertAtTop( new_parmTmp )

        # if the anchor parm is in some folder,
        # the new parm will also be added into the same one.

        elif insert_before:
            grp.insertBefore( insert_before, new_parmTmp )
        
        # if the anchor parm is in some folder,
        # the new parm will also be added into the same one.
        elif insert_after:
            grp.insertAfter( insert_after, new_parmTmp )
        
        # put the new parm at the end.
        else:
            grp.addParmTemplate( new_parmTmp )


    self.setParmTemplateGroup( grp, rename_conflicting_parms=True )

    if as_parm:
        return self._[ new_parmTmp.Name ]
    else:
        return new_parmTmp
setAttr( hou.Node, 'addParm', _parm_addParm, replace=True )




def _parm_addSep( self, 
                        name='sep', 
                        count=1,

                        **kwargs
                    ):
    """
    Add new seperator.

    Author: Sean
    """
    new_tmp = hou.SeparatorParmTemplate( name )
    return self.addParm( new_tmp, **kwargs )
setAttr( hou.Node, 'addSep', _parm_addSep )



def _parm_addBtn( self, 
                        name = 'button', label = 'Button', 

                        hidden = False,

                        tags = {},
                        help_info = None, 
                        callback = None, callback_language = hou.scriptLanguage.Python, 

                        join_with_next = False,

                        **kwargs
                    ):
    """
    Add new button.

    hou.ButtonParmTemplate      http://www.sidefx.com/docs/houdini/hom/hou/ButtonParmTemplate.html

    Author: Sean
    """
    new_tmp = hou.ButtonParmTemplate( 
                        name = name, label = label, 

                        is_hidden = hidden,

                        tags = tags,
                        help = help_info, 
                        script_callback = callback, script_callback_language = callback_language,

                        join_with_next = join_with_next,
                    )

    # if join_with_next:
    #     new_tmp.setJoinWithNext( True )

    return self.addParm( new_tmp, **kwargs )
setAttr( hou.Node, 'addBtn', _parm_addBtn, replace=True )



def _parm_addMenu( self,
                        name = 'menu', label = 'Menu',
                        menu_items = None,

                        default = 0,

                        hidden = False,

                        tags = {},
                        help_info = None, 
                        callback = None, callback_language = hou.scriptLanguage.Python,

                        join_with_next = False,

                        **kwargs
                    ):
    """
    Add new menu.

    hou.MenuParmTemplate        http://www.sidefx.com/docs/houdini/hom/hou/MenuParmTemplate.html

    Author: Sean
    """
    # get menu items
    if menu_items is not None:
        menu_values, menu_labels = zip(*menu_items)
    else:
        menu_values = menu_labels = ()


    # get default
    if isinstance( default, str ):
        default = menu_values.index( default )


    # new parm template
    new_tmp = hou.MenuParmTemplate( 
                        name = name, label = label,
                        menu_items = menu_values, menu_labels = menu_labels,

                        default_value = default,

                        is_hidden = hidden,

                        tags = tags,
                        help = help_info, 
                        script_callback = callback, script_callback_language = callback_language,

                        join_with_next = join_with_next,
                    )
setAttr( hou.Node, 'addMenu', _parm_addMenu, replace=True )



def _parm_addBtnStrip( self,
                        name = 'button_strip', label = 'Buttons', label_width = 30,
                        menu_items = None,
                        menu_type = 'replace',

                        hidden = False,

                        tags = {},
                        help_info = None, 
                        callback = None, callback_language = hou.scriptLanguage.Python,

                        join_with_next = False,

                        **kwargs
                    ):
    """
    Add new button strip.

    hou.MenuParmTemplate        http://www.sidefx.com/docs/houdini/hom/hou/MenuParmTemplate.html

    Author: Sean
    """
    # get menu items
    if menu_items is not None:
        menu_values, menu_labels_raw = zip(*menu_items)

        menu_labels = []
        for i in menu_labels_raw:
            pad = max( label_width - len(i), 0 ) /2
            i = ' ' * pad + i
            i = i.ljust( label_width, ' ' )
            i += '|'
            menu_labels.append( i )

        menu_labels[-1] = menu_labels[-1][:-1]
    else:
        menu_values = menu_labels = ()


    # get menu type
    menu_type = menu_type.lower()
    if menu_type == 'replace':
        menu_type = hou.menuType.StringReplace
    elif menu_type == 'toggle':
        menu_type = hou.menuType.StringToggle


    # new parm template
    new_tmp = hou.MenuParmTemplate( 
                        name = name, label = label,
                        menu_items = menu_values, menu_labels = menu_labels,
                        is_button_strip = True,

                        is_hidden = hidden,

                        tags = tags,
                        help = help_info, 
                        script_callback = callback, script_callback_language = callback_language,

                        join_with_next = join_with_next,
                    )

    return self.addParm( new_tmp, **kwargs )
setAttr( hou.Node, 'addBtnStrip', _parm_addBtnStrip, replace=False )



def _parm_addInt( self, 
                        name='integer', label='integer', 
                        default = (0,), initial = None,
                        size=1, 
                        value_range = (0, 10),

                        hidden = False,

                        tags = {},
                        help_info=None, 
                        script=None, language=hou.scriptLanguage.Python,

                        join_with_next = False,

                        **kwargs
                    ):
    """
    Add new integer.
    
    hou.IntParmTemplate     http://www.sidefx.com/docs/houdini/hom/hou/IntParmTemplate.html

    Author: Sean
    """
    # get default
    if not isSequence( default ):
        default = ( default, )

    # new parm template
    new_tmp = hou.IntParmTemplate( 
                        name=name, label=label,
                        default_value = default,
                        num_components = size,
                        min = value_range[0], max = value_range[1],

                        is_hidden = hidden,

                        tags = tags,
                        help = help_info, 
                        script_callback = script, script_callback_language = language,

                        join_with_next = join_with_next,
                    )

    # add parm
    new_tmp = self.addParm( new_tmp, **kwargs )

    # set initial value
    if initial is not None:
        self._[ new_tmp.Name ]._ = initial

    return new_tmp
setAttr( hou.Node, 'addInt', _parm_addInt, replace=False )



def _parm_addFlt( self, 
                        name = 'float', label = 'Float', 
                        default = (0,), initial = None,
                        size = 1, 
                        value_range = (0.0, 1.0),

                        hidden = False,

                        tags = {},
                        help_info = None, 
                        callback = None, callback_language = hou.scriptLanguage.Python,

                        join_with_next = False,

                        **kwargs
                ):
    """
    Add new float.

    hou.FloatParmTemplate   http://www.sidefx.com/docs/houdini/hom/hou/FloatParmTemplate.html

    Author: Sean
    """
    # get default
    if not isSequence( default ):
        default = ( default, )

    # new parm template
    new_tmp = hou.FloatParmTemplate( 
                        name = name, label = label,
                        default_value = default,
                        num_components = size,
                        min = value_range[0], max = value_range[1],

                        is_hidden = hidden,

                        tags = tags,
                        help = help_info, 
                        script_callback = callback, script_callback_language = callback_language,

                        join_with_next = join_with_next,
                    )
    
    # add parm
    new_tmp = self.addParm( new_tmp, **kwargs )

    # set initial value
    if initial is not None:
        self._[ new_tmp.Name ]._ = initial

    return new_tmp
setAttr( hou.Node, 'addFlt', _parm_addFlt, replace=False )



def _parm_addStr( self, 
                        name = 'string', 
                        label = 'String', label_hidden = False,
                        default = (), initial = None,
                        size = 1, 
                        string_type = 'regular',

                        expr=(), expr_language = (hou.scriptLanguage.Hscript,),

                        menu_items = None,

                        hidden = False,

                        tags = {},
                        help_info = None, 
                        callback = None, callback_language = hou.scriptLanguage.Python,

                        join_with_next = False,

                        **kwargs
                    ):
    """
    Add new string.

    hou.StringParmTemplate      http://www.sidefx.com/docs/houdini/hom/hou/StringParmTemplate.html

    Author: Sean
    """
    # get default
    if not isSequence( default ):
        default = (default, )


    # get menu items
    if menu_items is not None:
        menu_values, menu_labels = zip(*menu_items)
    else:
        menu_values = menu_labels = ()


    # new parm template
    new_tmp = hou.StringParmTemplate( 
                        name = name, 
                        label = label, is_label_hidden = label_hidden,
                        num_components = size,
                        default_value = default,

                        default_expression=expr, default_expression_language=expr_language,

                        menu_items = menu_values, menu_labels = menu_labels,

                        is_hidden = hidden,

                        tags = tags,
                        help = help_info, 
                        script_callback = callback, script_callback_language = callback_language,
                        
                        join_with_next = join_with_next,
                    )
    new_tmp.StringType = string_type


    # add parm
    new_tmp = self.addParm( new_tmp, **kwargs )


    # set initial value
    if initial is not None:
        self._[ new_tmp.Name ]._ = initial

    return new_tmp
setAttr( hou.Node, 'addStr', _parm_addStr, replace=False )



def _parm_addLabel( self, 
                        name = 'label', 
                        label = 'Label', label_hidden = False,
                        labels = (),

                        tags = {},
                        help_info = None, 

                        join_with_next = False,

                        **kwargs
                    ):
    """
    Add new label.

    hou.LabelParmTemplate       http://www.sidefx.com/docs/houdini/hom/hou/LabelParmTemplate.html

    Author: Sean
    """
    new_tmp = hou.LabelParmTemplate(
                        name = name, 

                        label = label,
                        is_label_hidden = label_hidden,

                        column_labels = labels,

                        tags = tags,
                        help = help_info, 

                        join_with_next = join_with_next,
                    )
    return self.addParm( new_tmp, **kwargs )
setAttr( hou.Node, 'addLabel', _parm_addLabel, replace=False )



def _parm_addToggle( self,
                        name = 'toggle', label = 'toggle', label_hidden = False,
                        default = True,

                        hidden = False,

                        tags = {},
                        help_info = None,
                        callback = None, callback_language = hou.scriptLanguage.Python,

                        join_with_next = False,

                        **kwargs
                    ):
    """
    Add new toggle.

    hou.ToggleParmTemplate      http://www.sidefx.com/docs/houdini/hom/hou/ToggleParmTemplate.html

    Author: Sean
    """
    new_tmp = hou.ToggleParmTemplate( 
                        name = name, label = label, is_label_hidden = label_hidden,
                        default_value = default,

                        is_hidden = hidden,

                        tags = tags,
                        help = help_info,
                        script_callback = callback, script_callback_language = callback_language,

                        join_with_next = join_with_next,
                    )
    return self.addParm( new_tmp, **kwargs )
setAttr( hou.Node, 'addToggle', _parm_addToggle, replace=True )



def _parm_addRamp( self, 
                        name = 'ramp', label = 'ramp',

                        hidden = False,

                        tags = {},
                        help_info = None,

                        **kwargs
                    ):
    """         
    hou.RampParmTemplate        http://www.sidefx.com/docs/houdini/hom/hou/RampParmTemplate.html
    """
    new_tmp = hou.RampParmTemplate(
                        name = name, label = label,
                        ramp_parm_type = hou.rampParmType.Float,

                        is_hidden = hidden,

                        tags = tags,
                        help = help_info,
                    )
    return self.addParm( new_tmp, **kwargs )
setAttr( hou.Node, 'addRamp', _parm_addRamp, replace=True )



def _parm_addColorRamp( self, 
                        name = 'ramp', label = 'ramp',

                        hidden = False,

                        tags = {},
                        help_info = None,

                        **kwargs
                    ):
    """         
    hou.RampParmTemplate        http://www.sidefx.com/docs/houdini/hom/hou/RampParmTemplate.html
    """
    new_tmp = hou.RampParmTemplate(
                        name = name, label = label,
                        ramp_parm_type = hou.rampParmType.Color,

                        is_hidden = hidden,

                        tags = tags,
                        help = help_info,
                    )
    return self.addParm( new_tmp, **kwargs )
setAttr( hou.Node, 'addColorRamp', _parm_addColorRamp, replace=True )



def _parm_addMultiParm( self,
                        name = 'folder', label = 'Folder',
                        parm_templates = (),

                        tags = {},
                        callback = None, callback_language = hou.scriptLanguage.Python, 

                        extra_justBorn = False,

                        **kwargs
                    ):
    # ~~~~~~ create extra parm templates ~~~~~~ #
    if extra_justBorn:
        parm_justBorn = hou.ToggleParmTemplate( 
                        name = name + '__justBorn#', label = 'Just Born',
                        default_value = True,
                        is_hidden = True
                    )
    
        parm_templates = [ parm_justBorn ] + list(parm_templates)


    # new parm template
    new_tmp = hou.FolderParmTemplate( 
                        name = name, label = label, 
                        parm_templates = parm_templates,
                        folder_type = hou.folderType.MultiparmBlock,

                        tags = tags,
                    )

    if callback:
        new_tmp.Callback = callback
        new_tmp.CallbackLanguage = callback_language

    return self.addParm( new_tmp, **kwargs )
setAttr( hou.Node, 'addMultiParm', _parm_addMultiParm, replace=True )



def _parm_addFolder( self,
                        name = 'folder', label = 'Folder',
                        parm_templates = (),
                        folder_type = 'simple',
                        ends_tab_group = False,

                        tags = {},

                        **kwargs
                    ):
    """
    Author: Sean
    """
    # get folder type
    folder_type = folder_type.lower()
    if folder_type == 'simple':
        folder_type = hou.folderType.Simple
    elif folder_type == 'tab':
        folder_type = hou.folderType.Tabs
    elif folder_type == 'multiparm':
        folder_type = hou.folderType.MultiparmBlock
    elif folder_type == 'collapse':
        folder_type = hou.folderType.Collapsible
    

    # new parm template
    new_tmp = hou.FolderParmTemplate( 
                        name = name, label = label, 
                        parm_templates = parm_templates,
                        folder_type = folder_type,
                        ends_tab_group = ends_tab_group,

                        tags = tags,
                    )

    return self.addParm( new_tmp, **kwargs )
setAttr( hou.Node, 'addFolder', _parm_addFolder, replace=True )



def _parm_addSpareFolder( self, ):
    """
    Put all existing parms in a new folder labeled with "Parms", and create another new folder labeled with "Spare".

    Author: Sean
    """
    # get parm template group
    grp = self.ParmTemplateGrp

    # existence check
    spare_folder = grp.SpareFolderParmTemplate
    if spare_folder:
        print( "Spare parm folder already exists." )
        return spare_folder


    # ======================================================== #
    # ====================== new folder ====================== #
    # ======================================================== #

    # storing all existing parms in new folder labeled with "Parms".
    parms_folder = self.addFolder( 
                        name = 'folder_parms', label = 'Parms',
                        parm_templates = grp.ParmTemplates,
                        folder_type = 'tab', 
                        ends_tab_group = False,
                        add = False 
                    )  

    # storing future spare parms in new folder labled with "Spare".
    spare_folder = self.addFolder( 
                        name = 'folder_spare', label = 'Spare',
                        folder_type = 'tab', 
                        ends_tab_group = True,
                        add = False 
                    )    

    # new parm template group
    new_grp = hou.ParmTemplateGroup( ( parms_folder, spare_folder ) )
    self.setParmTemplateGroup( new_grp )

    return spare_folder
setAttr( hou.Node, 'addSpareFolder', _parm_addSpareFolder, replace=False )







###########################################################################
################################### Copy ##################################
###########################################################################

def _parm_duplicate( self, 
                            name_suffix = None, label_suffix = None, 
                            new_name = None, new_label = None,
                            hidden = False,
                            auto_rename = False, raising = False,
                        ):
    """
    Duplicate current parm.

    Args:
        name_suffix ([type], optional): [description]. Defaults to None.
        label_suffix ([type], optional): [description]. Defaults to None.
        new_name ([type], optional): [description]. Defaults to None.
        new_label ([type], optional): [description]. Defaults to None.

        hidden (bool, optional): If true, hide the duplicated parm. 
                                    Defaults to False.

        auto_rename (bool, optional): If false, return the existing duplicated parm . 
                                        Defaults to False.
        raising (bool, optional): [description]. Defaults to False.

    Raises:
        Exception: [description]

    Returns:
        [hou.Parm]: [description]
    """
    node = self.Node
    grp = node.ParmTemplateGrp
    parm = self
    index = parm.Index
    tmp = parm.ParmTemplate

    if name_suffix:
        tmp.Name += name_suffix
    if label_suffix:
        tmp.Label += label_suffix
    if new_name:
        tmp.Name = new_name
    if new_label:
        tmp.Label = new_label

    tmp.Hidden = hidden


    # ~~~~~~~~~~~~ existence check ~~~~~~~~~~~~ #
    if not auto_rename:
        duplicated_parmTuple = node.parmTuple( tmp.Name )
        if duplicated_parmTuple:

            if raising:
                raise Exception( 'The duplicated parm already exists.' )

            return duplicated_parmTuple[ index ]


    # ~~~~~~~~~~~~~ duplicate parm ~~~~~~~~~~~~ #
    grp.insertAfter( parm.ParmTemplate.Name, tmp )
    grp.apply()

    duplicated_parmTuple = node.parmTuple( tmp.Name )
    return duplicated_parmTuple[ index ]
setAttr( hou.Parm, 'duplicate', _parm_duplicate )


def _parmTuple_duplicate( self, **kwargs ):
    return self[0].duplicate( **kwargs )
setAttr( hou.ParmTuple, 'duplicate', _parmTuple_duplicate )




# ======================================================== #
# ===================== to Clipboard ===================== #
# ======================================================== #
setAttr( hou.Parm, 'copyToClipboard', hou.Parm.copyToParmClipboard, replace=False )

'''
hou.parmClipboardContents       http://www.sidefx.com/docs/houdini/hom/hou/parmClipboardContents.html
'''



# ======================================================== #
# ================= to Spare Parm Folder ================= #
# ======================================================== #
def _parm_copyParmToSpareFolder( self ):
    """
    Author: Sean
    """
    grp = self.Node.ParmTemplateGrp

    spare_folderTmp = grp.SpareFolderParmTemplate

    if not spare_folderTmp:
        print( "There's no spare parm folder." )
        return


    # ======================================================== #
    # ======================= Copy parm ====================== #
    # ======================================================== #
    double_tmp = self.Tmp

    double_tmp.Name += '__RAW'

    if self.Node._[double_tmp.Name]:
        print( "The double parm exists. Copy execution has been terminated." )
        return


    spare_folderTmp.addParmTemplate( double_tmp )
    grp.replace( spare_folderTmp.Name, spare_folderTmp )

    self.Node.setParmTemplateGroup( grp, rename_conflicting_parms=True )



    # ======================================================== #
    # ================= Set value of new Parm ================ #
    # ======================================================== #
    old_parm = self.Node._[self.Tmp.Name]
    new_parm = self.Node._[double_tmp.Name]

    if isinstance( old_parm, hou.ParmTuple ):
        old_parm = old_parm.Parms
        new_parm = new_parm.Parms
    else:
        old_parm = [old_parm]
        new_parm = [new_parm]


    old_new_pair = zip( old_parm, new_parm )

    for old, new in old_new_pair:
        # value
        new._ = old._
        
        # expression
        expr = old.Expr
        if expr:
            new.setExpression( expr, old.expressionLanguage() )


    if isinstance( self, hou.ParmTuple ):
        return self.Node._[double_tmp.Name]
    else: # isinstance( self, hou.Parm )
        index = self.componentIndex()
        return self.Node.parmTuple( double_tmp.Name ).Parms[ index ]
setAttr( hou.Parm, 'copyToSpareFolder', _parm_copyParmToSpareFolder, replace=False )
setAttr( hou.ParmTuple, 'copyToSpareFolder', _parm_copyParmToSpareFolder, replace=False )











