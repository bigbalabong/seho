'''
Tier: Base
'''

from ...MVar import *






# ~~~~~~~~~~~~~~~ Expression ~~~~~~~~~~~~~~ #

Expr_PDG_Ref = '''pdg_attr = '@test'
use_pdg = ch('/obj/CTRL/pdg_enable')
if use_pdg:
    return hou.hscriptExpression( pdg_attr )
else:
    return ch('{}')'''




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
                        method.startswith( 'key_' ),
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
    def MenuItems_Key( self ):
        parm = self.Parm

        if not parm:
            return ()

        tmp = type( parm.ParmTemplate )

        if tmp in ( hou.StringParmTemplate, ):
            return ()

        items = [ i for i in self.MenuItems_All if i[0].startswith( 'key_' ) ]

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
        parms = [ i for i in self.Node.Parms if i.Keys ]
        
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
    ################################### Key ###################################
    ###########################################################################

    def _key_setAllExprAs( self, expr ):
        """
        Set all expressions of keysframes as input.

        Args:
            expr (str): Keyframe expression.

        Author: Sean
        """
        for parm in self.Parms:
            keys = parm.Keys

            for key in keys:
                key.Expr = expr
            
            parm.Keys = keys

    def key_setAllExprAsBezier( self ):
        """
        Expr:  bezier()

        bezier      https://www.sidefx.com/docs/houdini/expressions/bezier.html

        Author: Sean
        """ 
        self._key_setAllExprAs( 'bezier()' )

    def key_setAllExprAsConstant( self ):
        """
        Expr:  constant()

        Author: Sean
        """
        self._key_setAllExprAs( 'constant()' )

    def key_setAllExprAsCubic( self ):
        """
        Expr:  cubic()

        Author: Sean
        """
        self._key_setAllExprAs( 'cubic()' )

    def key_setAllExprAsEase( self ):
        """
        Expr:  ease()

        Author: Sean
        """
        self._key_setAllExprAs( 'ease()' )

    def key_setAllExprAsEasein( self ):
        """
        Expr:  easein()

        Author: Sean
        """
        self._key_setAllExprAs( 'easein()' )

    def key_setAllExprAsEaseout( self ):
        """
        Expr:  easeout()

        Author: Sean
        """
        self._key_setAllExprAs( 'easeout()' )

    def key_setAllExprAsLinear( self ):
        """
        Expr:  linear()

        Author: Sean
        """
        self._key_setAllExprAs( 'linear()' )

    def key_setAllExprAsQlinear( self ):
        """
        Expr:  qlinear()

        Author: Sean
        """
        self._key_setAllExprAs( 'qlinear()' )

    def key_setAllExprAsSpline( self ):
        """
        Expr:  spline()

        spline      https://www.sidefx.com/docs/houdini/expressions/spline.html

        Author: Sean
        """
        self._key_setAllExprAs( 'spline()' )





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
setAttr( hou.Parm, 'ContextMenu', ContextMenuParm, replace=True )








