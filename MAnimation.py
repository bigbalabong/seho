'''
Tier: Base
'''

from .MVar import *






###########################################################################
################################ Parameter ################################
###########################################################################
def _parm_getKeyframe( self ):
    """
    Get keyframe at current frame.

    Author: Sean
    """
    keys = [ i for i in self.Keys if (i.Frame - hou.frame()) < 0.02 ]
    if keys:
        return keys[0]
setAttr( hou.Parm, "Keyframe", property( _parm_getKeyframe, hou.Parm.setKeyframe ), replace=False )
setAttr( hou.Parm, "Key", hou.Parm.Keyframe, replace=False )


setAttr( hou.Parm, "Keyframes", property( hou.Parm.keyframes, hou.Parm.setKeyframes ) )
setAttr( hou.Parm, "Keys", hou.Parm.Keyframes )


def _parm_copyKeysFrom( self, parm ):
    """
    Copy all keyframes from input parameter.

    Args:
        parm (hou.Parm): [description]

    Author: Sean
    """
    self.deleteAllKeyframes()
    self.Keys = parm.Keys
setAttr( hou.Parm, "copyKeysFrom", _parm_copyKeysFrom )









###########################################################################
############################## Base Keyframe ##############################
###########################################################################
'''
HScript Global Variables - Channels  
                    https://www.sidefx.com/docs/houdini/network/expressions.html#channels
                    $OS         Operator String. Contains the current OP's name.
                    $CH         Current channel name.
                    $IV         In value (value at start of segment).
                    $OV         Out value.
                    $IM         In slope
                    $OM         Out slope
                    $IA         In acceleration
                    $OA         Out acceleration
                    $LT         Local time - not including stretch or offset
                    $IT         Start time of segment
                    $OT         End time of segment
                    $LIT        Local start time of segment
                    $LOT        Local end time of segment
                    $PREV_IT    Previous segment start time
                    $NEXT_OT    Next segment end time

Function field
                    https://www.sidefx.com/docs/houdini/ref/panes/changraph.html#function


hou.BaseKeyframe    http://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html


Channel Editor Weirdness
                    https://forums.odforce.net/topic/2945-channel-editor-weirdness/
                    fit01((($T-$IT)/($OT-$IT)),cubic(),bezier())
                    if((($T-$IT)/($OT-$IT)) < 0.5, cubic(),bezier())


keyframe interpolation programing
                    https://www.sidefx.com/forum/topic/13381/
                    fit($LT, $IT, $OT, $IV, $OV)


Control keyframe value by relative reference
                    https://www.sidefx.com/forum/topic/49265/
                    bezier() * ch("/obj/obj1/ty")


Channel graph keyframe expressions
                    https://www.sidefx.com/forum/topic/18355/


how to use linear() as expression
                    https://www.sidefx.com/forum/topic/20721/


fit($LT, $IT, $OT, spline()*ch('../transform5/tz'), bezier()*ch('../transform6/tz'))
'''




# ======================================================== #
# ========================= Time ========================= #
# ======================================================== #
setAttr( hou.BaseKeyframe, "Frame", property( hou.BaseKeyframe.frame, hou.BaseKeyframe.setFrame ) )
setAttr( hou.BaseKeyframe, "Time", property( hou.BaseKeyframe.time, hou.BaseKeyframe.setTime ) )




# ======================================================== #
# ====================== Expression ====================== #
# ======================================================== #
KeyExpr = (
            'bezier()', 'constant()', 'cubic()',

            'cycle()', 'cycleoffset()',

            'ease()', 'easein()', 'easeinp()', 'easeout()', 'easeoutp()', 'easep()',

            'linear()',

            'match()', 'matchin()', 'matchout()',

            'qlinear()', 'spline()',

            'vmatch()', 'vmatchin()', 'vmatchout()',
    )
setAttr( hou.BaseKeyframe, "Expressions", KeyExpr )



setAttr( hou.BaseKeyframe, "Expr", property( hou.BaseKeyframe.expression, hou.BaseKeyframe.setExpression ) )


def _baseKeyframe_getExprLanguage( self ):
    '''
    hou.exprLanguage        http://www.sidefx.com/docs/houdini/hom/hou/exprLanguage.html

    Returns:
            [str] hscript / python

    Author: Sean
    '''
    return str( self.expressionLanguage() ).rsplit('.', 1)[1].lower()
setAttr( hou.BaseKeyframe, "ExprLanguage", property( _baseKeyframe_getExprLanguage ) )



def _baseKeyframe_getHScript( self ):
    """
    Author: Sean
    """
    expr = self.Expr
    if expr and self.ExprLanguage == 'hscript':
        return expr

def _baseKeyframe_setHScript( self, codes ):
    """
    Args:
        codes (str): [description]

    Common Expression Functions:
        'linear()'
    
    Author: Sean
    """
    self.setExpression( codes, hou.exprLanguage.Hscript )

setAttr( hou.BaseKeyframe, "HScript", property( _baseKeyframe_getHScript, _baseKeyframe_setHScript ) )




def _baseKeyframe_getPython( self ):
    """
    Returns:
        [str]

    Author: Sean
    """
    expr = self.Expr
    if expr and self.ExprLanguage == 'python':
        return expr

def _baseKeyframe_setPython( self, codes ):
    """
    Args:
        codes (str): [description]

    Author: Sean
    """
    self.setExpression( codes, hou.exprLanguage.Python )

setAttr( hou.BaseKeyframe, "Python", property( _baseKeyframe_getPython, _baseKeyframe_setPython ) )








###########################################################################
################################# Keyframe ################################
###########################################################################
'''
hou.Keyframe            http://www.sidefx.com/docs/houdini/hom/hou/Keyframe.html
'''
setAttr( hou.Keyframe, "Value", property( hou.Keyframe.value, hou.Keyframe.setValue ) )
setAttr( hou.Keyframe, "_", property( hou.Keyframe.value, hou.Keyframe.setValue ) )

setAttr( hou.Keyframe, "Accel", property( hou.Keyframe.accel, hou.Keyframe.setAccel ) )

setAttr( hou.Keyframe, "Slope", property( hou.Keyframe.slope, hou.Keyframe.setSlope ) )








###########################################################################
############################# String Keyframe #############################
###########################################################################
'''
hou.StringKeyframe      http://www.sidefx.com/docs/houdini/hom/hou/StringKeyframe.html
'''









