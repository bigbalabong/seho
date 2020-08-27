'''
Tier: Base
'''

from .MBase import *




###########################################################################
################################## String #################################
###########################################################################
'''
hou.text        http://www.sidefx.com/docs/houdini/hom/hou/text.html
'''

def _filter( objects, attr='Name', filters='*' ):
    """
    Filtering list of objects by filters.

    Args:
        objects (list of objects): Any type of object as long as the upconming returned attribute of object is string.
        attr (str, optional): The attribute of object. The type of returned value must be string.
                                Defaults to 'Name'.
        
        filters (str, optional): A single string containing filters which seperated by whitespace.
                                    If filter is equal to '*' or '', nothing will be filtered out.
                                    Defaults to '*'.
                                    E.g. '* ^group*'. 

    Returns:
        [list of objects]: [description]
    """
    filters = filters.strip()

    # nothing is filtered out
    if filters in ['*', '']:
        return objects


    # ~~~~~~~~~~~~~~ get filters ~~~~~~~~~~~~~~ #
    filters = [ i.strip() for i in filters.split( ' ' ) ]
    filters = [ i.replace( '*', '[\w]*' ) for i in filters if i ]

    include_filters = [ i for i in filters if not i.startswith( '^' ) ]
    exclude_filters = [ i[1:] for i in filters if i.startswith( '^' ) ]


    # ~~~~~~~~~~~~~ filter objects ~~~~~~~~~~~~ #
    filtered = []
    for obj in objects:
        if isinstance( obj, str ):
            string = obj
        else:
            string = getattr( obj, attr )

        include = [ re.search( i, string ) for i in include_filters ]
        include = [ i.group() == string for i in include if i ]
        include = sum( include )

        exclude = [ re.search( i, string ) for i in exclude_filters ]
        exclude = [ i.group() == string for i in exclude if i ]      
        exclude = sum( exclude ) 

        if include and not exclude:
            filtered.append( obj )

    return filtered
setAttr( hou.text, "filter", _filter, replace=False )







###########################################################################
################################## Vector #################################
###########################################################################
'''
hou.Vector2     https://www.sidefx.com/docs/houdini/hom/hou/Vector2.html
'''
setAttr( hou.Vector2, "X", property( hou.Vector2.x ) )
setAttr( hou.Vector2, "Y", property( hou.Vector2.y ) )

setAttr( hou.Vector2, "Length", property( hou.Vector2.length ) )
setAttr( hou.Vector2, "Length2", property( hou.Vector2.lengthSquared ) )





'''
hou.Vector3     https://www.sidefx.com/docs/houdini/hom/hou/Vector3.html
'''
def _vec3_setX( self, value ):
    self[0] = value
setAttr( hou.Vector3, "X", property( hou.Vector3.x, _vec3_setX ), replace=True )

def _vec3_setY( self, value ):
    self[1] = value
setAttr( hou.Vector3, "Y", property( hou.Vector3.y, _vec3_setY ), replace=True )

def _vec3_setZ( self, value ):
    self[2] = value
setAttr( hou.Vector3, "Z", property( hou.Vector3.z, _vec3_setZ ), replace=True )

setAttr( hou.Vector3, "Length", property( hou.Vector3.length ) )
setAttr( hou.Vector3, "Length2", property( hou.Vector3.lengthSquared ) )





'''
hou.Vector4     https://www.sidefx.com/docs/houdini/hom/hou/Vector4.html
'''
setAttr( hou.Vector4, "X", property( hou.Vector4.x ) )
setAttr( hou.Vector4, "Y", property( hou.Vector4.y ) )
setAttr( hou.Vector4, "Z", property( hou.Vector4.z ) )
setAttr( hou.Vector4, "W", property( hou.Vector4.w ) )

setAttr( hou.Vector4, "Length", property( hou.Vector4.length ) )
setAttr( hou.Vector4, "Length2", property( hou.Vector4.lengthSquared ) )









###########################################################################
################################ Quaternion ###############################
###########################################################################
'''
hou.Quaternion  https://www.sidefx.com/docs/houdini/hom/hou/Quaternion.html
'''

setAttr( hou.Quaternion, "AngleAxis", property( hou.Quaternion.extractAngleAxis ) )

def _quaternion_getAxis( self ):
    """
    Author: Sean
    """
    angle, axis = self.extractAngleAxis()
    return axis
setAttr( hou.Quaternion, "Axis", property( _quaternion_getAxis ), replace=False )

setAttr( hou.Quaternion, "Length", property( hou.Quaternion.length ) )


setAttr( hou.Quaternion, "Rotation", 
            property( hou.Quaternion.extractRotationMatrix3, hou.Quaternion.setToRotationMatrix ) )










###########################################################################
################################## Matrix #################################
###########################################################################

def _matrix_ident( cls ):
    """
    Author: Sean
    """
    m = cls()
    m.setToIdentity()
    return m
setAttr( hou.Matrix2, "ident", classmethod( _matrix_ident ) )
setAttr( hou.Matrix3, "ident", classmethod( _matrix_ident ) )
setAttr( hou.Matrix4, "ident", classmethod( _matrix_ident ) )


def _matrix_getQuaternion( self ):
    """
    Author: Sean
    """
    return hou.Quaternion( self )
setAttr( hou.Matrix3, "Quaternion", property( _matrix_getQuaternion ) )
setAttr( hou.Matrix4, "Quaternion", property( _matrix_getQuaternion ) )


def _matrix_getAxes( self ):
    """
    Author: Sean
    """
    x, y, z = self.asTupleOfTuples()[:3]
    x = x[:3]
    y = y[:3]
    z = z[:3]
    return hou.Vector3(x), hou.Vector3(y), hou.Vector3(z)
setAttr( hou.Matrix3, "Axes", property( _matrix_getAxes ), replace=False )
setAttr( hou.Matrix4, "Axes", property( _matrix_getAxes ), replace=False )






'''
hou.Matrix2     https://www.sidefx.com/docs/houdini/hom/hou/Matrix2.html
'''
def _matrix2_getitem( self, index ):
    """
    Get element by index.

    Args:
        index ([type]): [description]

    Returns:
        [float]: [description]

    As long as the class has __getitem__ method, you can use list() to flatten its instance.
        e.g. list( hou.Matrix2.ident() )
                Returns: [1.0, 0.0, 0.0, 1.0]

    Author: Sean
    """
    row = index / 2
    column = index % 2
    return self.at( row, column )
setAttr( hou.Matrix2, '__getitem__', _matrix2_getitem )


setAttr( hou.Matrix2, "Determinant", property( hou.Matrix2.determinant ) )
setAttr( hou.Matrix2, "Inverted", property( hou.Matrix2.inverted ) )
setAttr( hou.Matrix2, "Transposed", property( hou.Matrix2.transposed ) )






'''
hou.Matrix3     https://www.sidefx.com/docs/houdini/hom/hou/Matrix3.html
'''
def _matrix3_getitem( self, index ):
    """
    Get element by index.

    Args:
        index ([type]): [description]

    Returns:
        [float]: [description]

    As long as the class has __getitem__ method, you can use list() to flatten its instance.
        e.g. list( hou.Matrix3.ident() )
                Returns: [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

    Author: Sean
    """
    row = index / 3
    column = index % 3
    return self.at( row, column )
setAttr( hou.Matrix3, '__getitem__', _matrix3_getitem )


setAttr( hou.Matrix3, "Determinant", property( hou.Matrix3.determinant ) )
setAttr( hou.Matrix3, "Inverted", property( hou.Matrix3.inverted ) )
setAttr( hou.Matrix3, "Transposed", property( hou.Matrix3.transposed ) )






'''
hou.Matrix4     https://www.sidefx.com/docs/houdini/hom/hou/Matrix4.html

        hou.Matrix4()
                Returns: <hou.Matrix4 [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]>

        hou.Matrix4(1)
                Returns: <hou.Matrix4 [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]>

        hou.Matrix4( (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15) )
                Returns: <hou.Matrix4 [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]>

        hou.Matrix4( ((0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15)) )
                Returns: <hou.Matrix4 [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]>

        matrix3 = hou.Matrix3((0, 1, 2, 3, 4, 5, 6, 7, 8))
                Returns: <hou.Matrix3 [[0, 1, 2], [3, 4, 5], [6, 7, 8]]>
        hou.Matrix4( matrix3 )
                Returns: <hou.Matrix4 [[0, 1, 2, 0], [3, 4, 5, 0], [6, 7, 8, 0], [0, 0, 0, 1]]>
'''
def _matrix4_getitem( self, index ):
    """
    Get element by index.

    Args:
        index ([type]): [description]

    Returns:
        [float]: [description]

    As long as the class has __getitem__ method, you can use list() to flatten its instance.
        e.g. list( hou.Matrix4.ident() )
                Returns: [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]

    Author: Sean
    """
    row = index / 4
    column = index % 4
    return self.at( row, column )
setAttr( hou.Matrix4, '__getitem__', _matrix4_getitem )


setAttr( hou.Matrix4, "Determinant", property( hou.Matrix4.determinant ) )
setAttr( hou.Matrix4, "Inverted", property( hou.Matrix4.inverted ) )
setAttr( hou.Matrix4, "Transposed", property( hou.Matrix4.transposed ) )


def _matrix4_getTransformTo( self, transform ):
    """
    getTransformToNode(obj_node)        http://www.sidefx.com/docs/houdini/hom/hou/ObjNode.html

    Author: Sean
    """
    return self.inverted() * transform
setAttr( hou.Matrix4, '__div__', _matrix4_getTransformTo )


def _matrix4_setTranslate( self, value ):
    """
    Author: Sean
    """
    x, y, z = value
    self.setAt( 3, 0, x )
    self.setAt( 3, 1, y )
    self.setAt( 3, 2, z )
setAttr( hou.Matrix4, "Translate", property( hou.Matrix4.extractTranslates, _matrix4_setTranslate ) )

setAttr( hou.Matrix4, "Rotate", property( hou.Matrix4.extractRotates ) )
setAttr( hou.Matrix4, "Scale", property( hou.Matrix4.extractScales ) )
setAttr( hou.Matrix4, "Shear", property( hou.Matrix4.extractShears ) )


setAttr( hou.Matrix4, "Rotation", property( hou.Matrix4.extractRotationMatrix3 ) )













###########################################################################
################################## Color ##################################
###########################################################################
'''
hou.Color           https://www.sidefx.com/docs/houdini/hom/hou/Color.html
'''

setAttr( hou.Color, "RGB", property( hou.Color.rgb, hou.Color.setRGB ) )
setAttr( hou.Color, "HSV", property( hou.Color.hsv, hou.Color.setHSV ) )
setAttr( hou.Color, "HSL", property( hou.Color.hsl, hou.Color.setHSL ) )
setAttr( hou.Color, "LAB", property( hou.Color.lab, hou.Color.setLAB ) )


def _color_getRed( self ):
    """
    Author: Sean
    """
    return self.RGB[0]

def _color_setRed( self, val ):
    """
    Author: Sean
    """
    r, g, b = self.RGB
    r = val
    self.RGB = ( r, g, b )

setAttr( hou.Color, "Red", property( _color_getRed, _color_setRed ) )



def _color_getGreen( self ):
    """
    Author: Sean
    """
    return self.RGB[1]

def _color_setGreen( self, val ):
    """
    Author: Sean
    """
    r, g, b = self.RGB
    g = val
    self.RGB = ( r, g, b )

setAttr( hou.Color, "Green", property( _color_getGreen, _color_setGreen ) )



def _color_getBlue( self ):
    """
    Author: Sean
    """
    return self.RGB[2]

def _color_setBlue( self, val ):
    """
    Author: Sean
    """
    r, g, b = self.RGB
    b = val
    self.RGB = ( r, g, b )

setAttr( hou.Color, "Blue", property( _color_getBlue, _color_setBlue ) )



def _color_getHue( self ):
    """
    Author: Sean
    """
    return self.HSV[0]

def _color_setHue( self, val ):
    """
    Author: Sean
    """
    h, s, v = self.HSV
    h = val
    self.HSV = ( h, s, v )

setAttr( hou.Color, "Hue", property( _color_getHue, _color_setHue ) )



def _color_getSaturation( self ):
    """
    Author: Sean
    """
    return self.HSV[1]

def _color_setSaturation( self, val ):
    """
    Author: Sean
    """
    h, s, v = self.HSV
    s = val
    self.HSV = ( h, s, v )

setAttr( hou.Color, "Saturation", property( _color_getSaturation, _color_setSaturation ) )



def _color_getValue( self ):
    """
    Author: Sean
    """
    return self.HSV[2]

def _color_setValue( self, val ):
    """
    Author: Sean
    """
    h, s, v = self.HSV
    v = val
    self.HSV = ( h, s, v )

setAttr( hou.Color, "Value", property( _color_getValue, _color_setValue ) )



def _color_random( cls ):
    """
    Author: Sean
    """
    return cls( FLT.rand3() )
setAttr( hou.Color, "rand", classmethod( _color_random ) )



def _color_apply( self ):
    """
    Author: Sean
    """
    self.Item.Color = self
setAttr( hou.Color, 'apply', _color_apply )




# ======================================================== #
# ======================= Variable ======================= #
# ======================================================== #
class ColorPreset( object ):

    """
    Author: Sean
    """

    # pure solid color
    White =     hou.Color( 1, 1, 1 )
    Black =     hou.Color( 0, 0, 0 )
    Red =       hou.Color( 1, 0, 0 )
    Yellow =    hou.Color( 1, 1, 0 )
    Green =     hou.Color( 1, 1, 0 )
    Cyan =      hou.Color( 0, 1, 1 )
    Blue =      hou.Color( 0, 0, 1 )
    Magenta =   hou.Color( 1, 0, 1 )


    # harmony color
    Gray2 =     hou.Color( 0.478, 0.478, 0.478 )
    Red2 =      hou.Color( 0.98, 0.275, 0.275 )
    Orange2 =   hou.Color( 1.0, 0.45, 0.1 )
    Yellow2 =   hou.Color( 1, 0.725, 0 )
    Yellow3 =   hou.Color( 0.976, 0.78, 0.263 )
    Green2 =    hou.Color( 0.475, 0.812, 0.204 )
    Cyan2 =     hou.Color( 0.1, 0.65, 0.55 )
    Blue2 =     hou.Color( 0.29, 0.565, 0.886 )
    Purple2 =   hou.Color( 0.451, 0.369, 0.796 )
    Magenta2 =  hou.Color( 0.89, 0.412, 0.761 )


    # nodetpe
    Output =    hou.Color( 0.976, 0.78, 0.263 )


    # occupation
    Core =      Red2
    Key =       Yellow2
    Optimize =  Cyan2
    Temp =      Orange2
    Cal =       Purple2         # Calculation
    Vis  =      Magenta2
setAttr( hou.Color, 'Preset', ColorPreset )








###########################################################################
############################### Bounding Box ##############################
###########################################################################
'''
hou.BoundingBox     https://www.sidefx.com/docs/houdini/hom/hou/BoundingBox.html
'''

setAttr( hou.BoundingBox, "Min", property( hou.BoundingBox.minvec ) )
setAttr( hou.BoundingBox, "Max", property( hou.BoundingBox.maxvec ) )

setAttr( hou.BoundingBox, "Size", property( hou.BoundingBox.sizevec ) )

setAttr( hou.BoundingBox, "Center", property( hou.BoundingBox.center ) )
setAttr( hou.BoundingBox, "Mid", hou.BoundingBox.Center )


def _bb_newNode( self, parent, **kwargs ):
    """
    Create new Box node based on bounding box info.

    Author: Sean
    """
    node = parent.newNode( node_type_name='box', **kwargs )
    
    center_x, center_y, center_z = self.Center
    node.parm('tx').set( center_x )
    node.parm('ty').set( center_y )
    node.parm('tz').set( center_z )

    size_x, size_y, size_z = self.Size
    node.parm('sizex').set( size_x )
    node.parm('sizey').set( size_y )
    node.parm('sizez').set( size_z )

    return node
setAttr( hou.BoundingBox, 'newNode', _bb_newNode )









