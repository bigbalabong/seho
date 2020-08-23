'''
Tier: Base
'''

from ..MVar import *





# ======================================================== #
# ================== Ramp Parm Template ================== #
# ======================================================== #
'''
hou.RampParmTemplate    http://www.sidefx.com/docs/houdini/hom/hou/RampParmTemplate.html

hou.rampParmType        http://www.sidefx.com/docs/houdini/hom/hou/rampParmType.html
        hou.rampParmType.Color
        hou.rampParmType.Float

hou.rampBasis           http://www.sidefx.com/docs/houdini/hom/hou/rampBasis.html
        hou.rampBasis.Linear
            Does a linear (straight line) interpolation between keys.
        hou.rampBasis.Constant
            Holds the value constant until the next key.
        hou.rampBasis.CatmullRom
            Interpolates smoothly between the keys. See Catmull-Rom_spline .
        hou.rampBasis.MonotoneCubic
            Another smooth interpolation that ensures that there is no overshoot. For example, if a key's value is smaller than the values in the adjacent keys, this type ensures that the interpolated value is never less than the key's value.
        hou.rampBasis.Bezier
            Cubic Bezier curve that interpolates every third control point and uses the other points to shape the curve. See Bezier curve .
        hou.rampBasis.BSpline
            Cubic curve where the control points influence the shape of the curve locally (that is, they influence only a section of the curve). See B-Spline .
        hou.rampBasis.Hermite
            Cubic Hermite curve that interpolates the odd control points, while even control points control the tangent at the previous interpolation point. See Hermite spline .

hou.colorType           http://www.sidefx.com/docs/houdini/hom/hou/colorType.html
        hou.colorType.RGB
            The red green blue color model.
        hou.colorType.HSV
            The hue saturation value color model.
        hou.colorType.HSL
            The hue saturation lightness color model.
        hou.colorType.LAB
            The CIE L* a* b* color space model.
        hou.colorType.XYZ
            The CIE XYZ color space model.


References:
    Dealing with ramp using python
    https://forums.odforce.net/topic/33443-dealing-with-ramp-using-python/
'''

setAttr( hou.RampParmTemplate, "DefaultBasis", 
            property( hou.RampParmTemplate.defaultBasis, hou.RampParmTemplate.setDefaultBasis ) )




'''
hou.Ramp            http://www.sidefx.com/docs/houdini/hom/hou/Ramp.html
'''
def _ramp_setColorType( self, color_type='RGB' ):
    """
    Author: Sean
    """
    color_type = color_type.lower()

    if color_type == 'rgb':
        self.setColorType( hou.colorType.RGB )

    elif color_type == 'hsv':
        self.setColorType( hou.colorType.HSV )

    elif color_type == 'hsl':
        self.setColorType( hou.colorType.HSL )

    elif color_type == 'lab':
        self.setColorType( hou.colorType.LAB )

    elif color_type == 'xyz':
        self.setColorType( hou.colorType.XYZ )
setAttr( hou.Ramp, "ColorType", property( hou.Ramp.colorType, hou.Ramp.setColorType ) )


def _ramp_getNumKeys( self ):
    """
    Author: Sean
    """
    return len( self.keys() )
setAttr( hou.Ramp, "NumKeys", property( _ramp_getNumKeys ) )


def _ramp_getKey( self, index ):
    """
    Author: Sean
    """
    if index >= len( self.keys() ):
        return

    parm = self.Parm.Name
    node = self.Parm.Node
    parms = [   node['{}{}pos'.format( parm, index +1 )], 
                node['{}{}value'.format( parm, index +1 )], 
                node['{}{}interp'.format( parm, index +1 )] ]

    return RampKey( self, index, *parms )
setAttr( hou.Ramp, 'key', _ramp_getKey )
setAttr( hou.Ramp, '__getitem__', _ramp_getKey )


def _ramp_getKeys( self ):
    """
    Author: Sean
    """
    num = len( self.keys() )
    
    parm = self.Parm.Name
    node = self.Parm.Node
    parms = []
    for i in range(num):
        parms.append([  node['{}{}pos'.format( parm, i +1 )], 
                        node['{}{}value'.format( parm, i +1 )], 
                        node['{}{}interp'.format( parm, i +1 )] ])

    keys = []
    for index, related_parms in enumerate( parms ):
        keys.append( RampKey( self, index, *related_parms ) )

    return keys
setAttr( hou.Ramp, "Keys", property( _ramp_getKeys ) )

setAttr( hou.Ramp, "Values", property( hou.Ramp.values ) )

setAttr( hou.Ramp, "Basis", property( hou.Ramp.basis ) )


# hou.Ramp.insertBefore

# hou.Ramp.insertAfter


def _ramp_update( self ):
    """
    Author: Sean
    """
    self.Parm.Value = self
hou.Ramp.update = _ramp_update




class RampKey( object ):
    
    """
    Author: Sean
    """

    def __init__( self, ramp, index, 
                        parm_pos, parm_value, parm_basis ):
        self.Ramp = ramp

        self.Index = index

        self.ParmPos = parm_pos
        self.ParmValue = parm_value
        self.ParmBasis = parm_basis


    @property
    def P( self ):
        """
        Author: Sean
        """
        # return self.Ramp.keys()[ self.Index ]
        return self.ParmPos.Value

    @P.setter
    def P( self, value ):
        """
        Author: Sean
        """
        self.ParmPos.Value = value


    def lerpP( self, ratio ):
        """
        Author: Sean
        """
        index = self.Index

        if index == 0:
            a = 0
            b = self.Ramp.keys()[ index +1 ]

        elif index == self.Ramp.NumKeys - 1:
            a = self.Ramp.keys()[ index -1 ]
            b = 1

        else:
            a = self.Ramp.keys()[ index -1 ]
            b = self.Ramp.keys()[ index +1 ]

        self.P = a * (1 - ratio) + b * ratio














