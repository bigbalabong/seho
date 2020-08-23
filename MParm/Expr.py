'''
Tier: Base
'''

from ..MVar import *





###########################################################################
################################ Expression ###############################
###########################################################################
'''
hou.exprLanguage        http://www.sidefx.com/docs/houdini/hom/hou/exprLanguage.html
'''
def _parm_getExprLanguage( self ):
    '''
    RETURN:
            (str) hscript / python
    
    Author: Sean
    '''
    return str(self.expressionLanguage()).rsplit('.',1)[1].lower()
setAttr( hou.Parm, "ExprLanguage", property( _parm_getExprLanguage ) )


def _parm_getExpr( self ):
    """
    Author: Sean
    """
    try:
        expr = self.expression()
        return expr
    except:
        return

def _parm_setExpr( self, expr ):
    """
    Author: Sean
    """
    if self.Expr:
        language = self.expressionLanguage()
    else:
        language = self.Node.expressionLanguage()

    self.setExpression( expr, language )
setAttr( hou.Parm, "Expr", property( _parm_getExpr, _parm_setExpr ), replace=False )



def _parm_getHScript( self ):
    """
    Author: Sean
    """
    expr = self.Expr
    if expr and self.Lang == 'hscript':
        return expr

def _parm_setHScript( self, code ):
    """
    Author: Sean
    """
    self.setExpression( code, language=hou.exprLanguage.Hscript )

setAttr( hou.Parm, "HScript", property( _parm_getHScript, _parm_setHScript ) )



def _parm_getPython( self ):
    """
    Author: Sean
    """
    expr = self.Expr
    if expr and self.ExprLanguage == 'python':
        return expr

def _parm_setPython( self, code ):
    """
    Author: Sean
    """
    self.setExpression( code, language=hou.exprLanguage.Python )

setAttr( hou.Parm, "Python", property( _parm_getPython, _parm_setPython ) )









###########################################################################
################################# Callback ################################
###########################################################################
setAttr( hou.ParmTemplate, "Callback", property( hou.ParmTemplate.scriptCallback, hou.ParmTemplate.setScriptCallback ) )

setAttr( hou.ParmTemplate, "CallbackLanguage", 
            property( hou.ParmTemplate.scriptCallbackLanguage, hou.ParmTemplate.setScriptCallbackLanguage ) )



def _parm_getCallback( self ):
    """
    Author: Sean
    """
    return self.ParmTemplate.Callback

def _parm_setCallback( self, code ):
    """
    Author: Sean
    """
    parm_template = self.ParmTemplate
    parm_template.Callback = code
    parm_template.apply()

setAttr( hou.Parm, "Callback", property( _parm_getCallback, _parm_setCallback ) )











###########################################################################
################################ Reference ################################
###########################################################################
setAttr( hou.Node, 'References', property( hou.Node.references ), replace=False )
setAttr( hou.Node, 'Dependents', property( hou.Node.dependents ), replace=False )


setAttr( hou.Parm, 'Reference', property( hou.Parm.getReferencedParm ), replace=False )



def _parm_getDependents( self, mode='all' ):
    """
    4 Kinds of References:
            1. ch() HScript Function
                    the most common scenerio.
                    just using the builtin python function called parmsReferencingThis() of hou.Parm class
            
            2. Parameter VOP
                    e.g. Principle Shader VOP
                    retrieve all the Parameter VOPs in children one by one, to see if its name is equal to the name of parm.
            
            3. Subnet Inputs VOP
                    e.g. Classic Shader Core VOP
                    retrive all the Subnet Inputs VOPs in children one by one, to see if its output name is equal to the name of parm.
            
            4. ch() VEX Function of VEX codes in Wrangle SOP  --  referencing outside target might not be the standard way to use ch() funtion. but it's possible and worked.
                    e.g. GameDev Color Adjustment SOP
                    parse the VEX code and collect all the sentences containing ch() function. then check if the targets in ch() function is equal to the name of parm.
    
    Author: Sean
    """
    mode = mode.lower()

    # get node
    node = self.Node
    children = node.allSubChildren()

    # get node network pane
    # editor = toolutils.networkEditor()



    # get 1st kind of inspectors
    all_inspectors = self.parmsReferencingThis()
    
    inspectors = []

    if mode in ('inside', 'all'):
        # filter inspectors by inside / outside
        inspectors += [ i for i in all_inspectors if i.Node in children ]                                                          
        inspectors.sort( key = lambda x: children.index( x.Node ) )


        # check children nodes
        if node.isSubNetwork():
            if node.childTypeCategory().Name == 'Vop':

                # get 2nd kind of inspectors (Parameter VOP)
                inspectors += [ i for i in node.VOPs_parameter if i._['parmname']._ == self.Name ]

                # get 3rd kind of inspectors (Subnet Inputs VOP)
                for subinput in node.VOPs_subinput:
                    if self.Name in [ i[1:] for i in subinput.OutputNames ]:
                        inspectors.append( subinput )


            # get 4th kind of inspectors
            inspectors += [ i for i in node.AllWrangleOps if self in i.References ]


    if mode in ('outside', 'all'):
        # filter inspectors by inside / outside
        inspectors += [ i for i in all_inspectors if i.Node not in children ]                                                      


    return inspectors
setAttr( hou.Parm, 'getDependents', _parm_getDependents, replace=False )














