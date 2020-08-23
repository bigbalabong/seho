'''
Tier: Base
'''

from .MVar import *




hou.hmath.Vars = {
        'sqrt2':    pow(2, 0.5),
        'sqrt2_r':  1 / pow(2, 0.5),

        'sqrt0_5':  pow(0.5, 0.5),          # hypotenuse if both cathetus is 1

        'norm110':  hou.Vector3(1,1,0).normalized(),
        'norm111':  hou.Vector3(1,1,1).normalized(),
    }










###########################################################################
################################## Ratio ##################################
###########################################################################
def _ratioByDotWith11( a, b ):
    """
    Author: Sean
    """
    sqrt2 =     hou.hmath.Vars['sqrt2']
    sqrt2_r =   hou.hmath.Vars['sqrt2_r']

    vec1 = hou.hmath.Vars['norm110']
    vec2 = hou.Vector3( a, b, 0 )
    angle = vec1.dot( vec2.normalized() )
    mag = vec2.Length / sqrt2

    val = mag * hou.hmath.fit( angle, sqrt2_r, 1, 0, 1 )
    return val
setAttr( hou.hmath, "ratioByDotWith11", _ratioByDotWith11 )








