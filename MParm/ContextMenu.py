'''
Tier: Base
'''

from ..MVar import *






# ~~~~~~~~~~~~~~~ Expression ~~~~~~~~~~~~~~ #

Expr_PDG_Ref = '''pdg_attr = '@test'
use_pdg = ch('/obj/CTRL/pdg_enable')
if use_pdg:
    return hou.hscriptExpression( pdg_attr )
else:
    return ch('{}')'''


# ~~~~~~~~~~~~~~~ Blend Parms ~~~~~~~~~~~~~ #

BlendParms_Targets_Callback = '''tmp = kwargs['node']._['blendParms_ratio'].ParmTemplate
tmp.Max = max( kwargs['parm']._, 2 )
tmp.apply()'''


BlendParms_ScopeAll_Callbak = '''parm_tuples = [ i for i in kwargs['node'].ParmTuples if i.Name.endswith( '__blendKeys' ) ]
for parm_tuple in parm_tuples:
    for parm in parm_tuple.Parms:
        if parm.Keys:
            parm.Scoped = True'''


BlendParms_UpdateKeys_Callback = '''parms = [ i for i in kwargs['node'].Parms if i.Python and i.Python.startswith( "ratio = ch('blendParms_ratio')" ) ]
parms = hou.text.filter( parms, filters=hou.ch('blendParms_updateKeys_parmsScope') )
for parm in parms:
    menu = hou.Parm.ContextMenu( kwargs={ 'parms': (parm, ) } )
    menu._blendParms_updateKeys()'''


BlendParms_RebuildKeys_Callback = '''parms = [ i for i in kwargs['node'].Parms if i.Python and i.Python.startswith( "ratio = ch('blendParms_ratio')" ) ]
parms = hou.text.filter( parms, filters=hou.ch('blendParms_rebuildKeys_parmsScope') )
for parm in parms:
    menu = hou.Parm.ContextMenu( kwargs={ 'parms': (parm, ) } )
    menu._blendParms_buildKeys()'''


BlendParms_Key_Expr = '''ratio = ch('blendParms_ratio')
num = ch('blendParms_targets')
frame = hou.hmath.fit( ratio, 1, num, 1, (num-1)*{}+1 )
return hou.parm("{}").evalAtFrame( frame )'''

        

class ContextMenuParm( object ):

    """
    Author: Sean
    """

    def __init__( self, kwargs ):
        self.kwargs = kwargs



    ###########################################################################
    ############################### Context Menu ##############################
    ###########################################################################
    @property
    def Parms( self ):
        """
        Author: Sean
        """
        return self.kwargs.get('parms')

    @property
    def Parm( self ):
        """
        Author: Sean
        """
        parms = self.Parms

        if parms:
            return parms[0]

    @property
    def ParmsLocked( self ):
        """
        Author: Sean
        """
        return self.kwargs.get('locked_parms')


    @property
    def Node( self ):
        """
        Author: Sean
        """
        parm = self.Parm

        if parm:
            return parm.Node

    @property
    def Func( self ):
        """
        Author: Sean
        """
        return self.kwargs.get('selectedtoken')

    @property
    def KeyCtrl( self ):
        """
        Author: Sean
        """
        return self.kwargs.get('ctrlclick')

    @property
    def KeyAlt( self ):
        """
        Author: Sean
        """
        return self.kwargs.get('altclick')

    @property
    def KeyShift( self ):
        """
        Author: Sean
        """
        return self.kwargs.get('shiftclick')

    @property
    def KeyCmd( self ):
        """
        Author: Sean
        """
        return self.kwargs.get('cmdclick')




    # ======================================================== #
    # ====================== Build Menu ====================== #
    # ======================================================== #
    @property
    def MenuItems_All( self ):
        """
        Author: Sean
        """
        items = getMenuItemsOfCls( self.__class__ )
        # items = L_(items).group(2)
        return items


    @property
    def MenuItems_General( self ):
        """
        Author: Sean
        """
        items = []
        for i in self.MenuItems_All:
            method = i[0]
            exclude_criteria = [
                        method.startswith( 'expr_' ),
                        method.startswith( 'blendParms_' ),
                    ]

            if sum( exclude_criteria ) == 0:
                items.append( i )

        items = L_(items).sum()
        return items



    @property
    def MenuItems_Expr( self ):
        """
        Get menu items "Expression".

        Author: Sean
        """
        parm = self.Parm

        if not parm:
            return ()

        tmp = type( parm.ParmTemplate )

        items = []

        items += [ i for i in self.MenuItems_All if i[0].startswith( 'expr_pdg_' ) ]


        if tmp in ( hou.StringParmTemplate, ):
            items += [ i for i in self.MenuItems_All if i[0].startswith( 'expr_str_' ) ]


        items = L_(items).sum()
        return items


    @property
    def MenuItems_BlendParms( self ):
        """
        Get menu items "Blend Parms".

        Author: Sean
        """
        items = [ i for i in self.MenuItems_All if i[0].startswith( 'blendParms_' ) ]
        items = L_(items).sum()
        return items


    def _exec( self ):
        """
        Author: Sean
        """
        func = getattr( self.__class__, self.Func )
        func( self )





    ###########################################################################
    ################################## Common #################################
    ###########################################################################
    def scopeAllAnimatedParms( self ):
        """
        Scope all keyframed parameters.
        
        Author: Sean
        """
        parms = [ i for i in hou.node('/obj/geo1/transform9').Parms if i.Keys ]
        
        for i in parms:
            i.Scoped = True






    ###########################################################################
    ################################ Expression ###############################
    ###########################################################################
    def _opinputpath( self, index=0, parent=False ):
        """
        Author: Sean
        """
        node = '..' if parent else '.'

        for parm in self.Parms:
            parm.HScript = "opinputpath('{}', {})".format( node, index )

    def expr_str_opinputpath_0( self ):
        """
        opinputpath('.', 0)
        
        Author: Sean
        """
        self._opinputpath( 0 )

    def expr_str_opinputpath_self_1( self ):
        """
        opinputpath('.', 1)
        
        Author: Sean
        """
        self._opinputpath( 1 )

    def expr_str_opinputpath_self_2( self ):
        """
        opinputpath('.', 2)
        
        Author: Sean
        """
        self._opinputpath( 2 )

    def expr_str_opinputpath_self_3( self ):
        """
        opinputpath('.', 3)
        
        Author: Sean
        """
        self._opinputpath( 3 )


    def expr_pdg_reference( self ):
        """
        Referencing PDG attribute.
        
        Author: Sean
        """
        pdg_attr = hou.ui.readInput('PDG Attribute Name:')[1]

        if not pdg_attr:
            return


        # ======================================================== #
        # ====================== copy parms ====================== #
        # ======================================================== #
        self.Node.addSpareFolder()
        double_parms = self.Parm.copyToSpareFolder()

        if len( self.Parms ) == 1:
            double_parms = [double_parms]


        # ======================================================== #
        # ======== set python expression for original parm ======= #
        # ======================================================== #
        for original, double in zip( self.Parms, double_parms ):
            codes = Expr_PDG_Ref.format( double.Name )

            original.Python = codes
        




    ###########################################################################
    ################################ Reference ################################
    ###########################################################################
    def getDependents( self ):
        """
        Get dependent parms.
        
        Author: Sean
        """     
        import seho.utils.parm_manager.parm_references as parm_references
        reload(parm_references)
        parm_references.show( parm = self.Parm )


    # def getRefInside( self ):
    #     """
    #     Get parm references inside.
    #     """
    #     pass


    # def getRefOutside( self ):
    #     """
    #     Get parm references outside.
    #     """
    #     pass
        




    ###########################################################################
    ################################## Blend ##################################
    ###########################################################################
    BlendParms_Vars = {
            'keys_gap':     20,
            'label_width':  20,
        }


    def blendParms_blend( self ):
        """
        Blend

        Author: Sean
        """
        node = self.Node

        # existence check
        if not node._['blendParms_folder']:
            targets = node.selectNodes( filter_same_nodetype=True )
            self._blendParms_init( targets )
        

        # this duplicated parm template is used to store keyframes.
        self.Parm.duplicate( 
                            name_suffix = '__blendKeys',
                            label_suffix = ' (Blend Keys)',
                            hidden = True,
                            auto_rename = False,
                        )


        # build keys and set parm referencing
        self._blendParms_buildKeys()


    def _blendParms_init( self, nodes=None ):
        """
        Add spare parameters.

        Author: Sean
        """
        label_width = self.BlendParms_Vars['label_width']

        node = self.Node

        node.addSpareFolder()
        folder = node.addFolder( 'blendParms_folder', 'Blend Parameters', spare_folder=True )



        # ======================================================== #
        # ======================= new parms ====================== #
        # ======================================================== #

        # ~~~~~~~~~~~~~~~~ targets ~~~~~~~~~~~~~~~~ #
        target = node.addStr( 'blendParms_target#', 'Target #', add=False )

        codes = BlendParms_Targets_Callback
        targets = node.addMultiParm( 
                                    'blendParms_targets', 'Targets', 
                                    parm_templates = (target,), 
                                    callback = codes,
                                    folder = folder,
                                )
        targets = node._[ targets.Name ]

        if nodes:
            targets._ = len(nodes)
            for target_parm, target_node in zip( targets.multiParmInstances(), nodes ):
                target_parm._ = node.relativePathTo( target_node )


        # ~~~~~~~~~~~~~~ blend ratio ~~~~~~~~~~~~~~ #
        maximum = len(nodes) if nodes else 2
        maximum = max( maximum, 2 )
        ratio = node.addFlt( 
                            'blendParms_ratio', 'Blending Ratio', 
                            initial = 1, value_range = (1, maximum), 
                            folder = folder  
                        )


        # ~~~~~~~~~~~~~~~~~~ sep ~~~~~~~~~~~~~~~~~~ #
        node.addSep( folder=folder )


        # ~~~~~~~~~~~~~~ scope button ~~~~~~~~~~~~~ #
        codes = BlendParms_ScopeAll_Callbak
        node.addBtn( 'blendParms_scope', 'Scope Intermediate Parms', callback=codes, folder=folder )


        # ~~~~~~~~~~~~ expression menu ~~~~~~~~~~~~ #
        node.addStr( 
                    'blendParms_keyExpr', 'Key Expression', 
                    default = ('linear()',),
                    menu_items = zip( hou.Keyframe.Expressions, hou.Keyframe.Expressions ),  
                    folder = folder,
                )


        # ~~~~~~~~~~~~ update keyframes ~~~~~~~~~~~ #
        label = S_( 'Update Keys' ).mjust( label_width )
        codes = BlendParms_UpdateKeys_Callback
        node.addBtn( 'blendParms_updateKeys', label, callback=codes, join_with_next=True, folder=folder )

        node.addStr( 'blendParms_updateKeys_parmsScope', 'Parms', label_hidden=True, default=('*',), folder=folder )


        # ~~~~~~~~~~~ rebuild keyframes ~~~~~~~~~~~ #
        label = S_( 'Rebuild Keys' ).mjust( label_width )
        codes = BlendParms_RebuildKeys_Callback
        node.addBtn( 'blendParms_rebuildKeys', label, callback=codes, join_with_next=True, folder=folder )

        node.addStr( 'blendParms_rebuildKeys_parmsScope', 'Parms', label_hidden=True, default=('*',), folder=folder )


    def _blendParms_getDoubleParm( self, parm ):
        """
        Get intermediate parm storing keys.

        Args:
            parm (hou.Parm): [description]

        Returns:
            [hou.Parm]: [description]

        Author: Sean
        """
        double_parmTuple = parm.Node.parmTuple( parm.ParmTuple.Name + '__blendKeys' )
        double_parm = double_parmTuple[ parm.Index ]
        return double_parm


    def _blendParms_buildKeys( self ):
        """
        Build keys on intermediate parms.

        Author: Sean
        """
        node = self.Node
        targets = [ node.node(i._) for i in node._['blendParms_targets'].multiParmInstances() ]
        key_expr = node._['blendParms_keyExpr']._        
        keys_gap = self.BlendParms_Vars['keys_gap']


        for parm in self.Parms:
            double_parm = self._blendParms_getDoubleParm( parm )
        
            # ~~~~~ build keys on intermediate parm ~~~~~ #
            keys = []
            for i, target in enumerate( targets ):
                # if multi-parm instance string parm is empty, target will be None
                if not target:
                    continue

                value = target._[parm.Name]._
            
                # new key
                key = hou.Keyframe()
                key.Frame = i * keys_gap + 1
                key.Value = value
                key.HScript = key_expr
                
                keys.append( key )

            double_parm.deleteAllKeyframes()
            double_parm.Keys = keys
            

            # set parm refercing
            parm.Python = BlendParms_Key_Expr.format( keys_gap, double_parm.Name )    


    def _blendParms_updateKeys( self ):
        """
        Update keys on intermediate parms.
        Only values of keys will be matched to the values of parms on targets.
        The timing and expression will be left untouched.

        Author: Sean
        """
        node = self.Node
        targets = [ node.node(i._) for i in node._['blendParms_targets'].multiParmInstances() ]
        targets = [ i for i in targets if i ]


        # ~~~~ update keys on intermediate parm ~~~ #
        update_failed = []
        for parm in self.Parms:
            double_parm = self._blendParms_getDoubleParm( parm )
            keys = double_parm.Keys

            # if keys on the intermediate parm were not edited (add / delete) by user manually,
            # the num of keys and targets is always same.
            if len(keys) != len(targets):
                update_failed.append( parm )
                continue


            # update values of keys
            for key, target in zip( keys, targets ):

                key.Value = target._[parm.Name]._


            # update keys
            double_parm.Keys = keys


        # ~~~~~~~~~~~~ post-processing ~~~~~~~~~~~~ #
        if update_failed:
            print( 'Parms updated faield:  {}'.format( ', '.join( [ i.Name for i in update_failed ] ) ) )


    def blendParms_scopeIntermediaParm( self ):
        """
        Scope Intermediate Parameters.

        Author: Sean
        """
        for parm in self.Parms:
            double_parm = self._blendParms_getDoubleParm( parm )
            double_parm.Scoped = True


    def blendParms_clear( self ):
        """
        Clear

        Author: Sean
        """
        parm = self.Parm

        # clear expression
        for parm in self.Parms:
            parm.deleteAllKeyframes()


        # destory parm template
        working_parms = [ i for i in parm.ParmTuple.Parms if i.Python and i.Python.startswith( "ratio = ch('blendParms_ratio')" ) ]
        if not working_parms:
            double_parm = self._blendParms_getDoubleParm( parm )
            tmp = double_parm.ParmTemplate
            tmp.destroy()
setAttr( hou.Parm, 'ContextMenu', ContextMenuParm )








