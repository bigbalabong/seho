'''
Tier: Base
'''

from ..MVar import *



Datatypes_with_Multi_Elements = ( 
            hou.Vector2, hou.Vector3, hou.Vector4, 
            hou.Quaternion, 
            hou.Matrix2, hou.Matrix3, hou.Matrix4 
        )





###########################################################################
############################### hou.Geometry ##############################
###########################################################################

# ======================================================== #
# ===================== Get Attribute ==================== #
# ======================================================== #
setAttr( hou.Geometry, 'PointAttrs', property( hou.Geometry.pointAttribs ) )
setAttr( hou.Geometry, 'VertexAttrs', property( hou.Geometry.vertexAttribs ) )
setAttr( hou.Geometry, 'PrimAttrs', property( hou.Geometry.primAttribs ) )
setAttr( hou.Geometry, 'DetailAttrs', property( hou.Geometry.globalAttribs ) )


def _geo_getPointAttrNames( self ):
    return self.intrinsicValue( 'pointattributes' )
setAttr( hou.Geometry, 'PointAttrNames', property( _geo_getPointAttrNames ) )

def _geo_getVertexAttrNames( self ):
    return self.intrinsicValue( 'vertexattributes' )
setAttr( hou.Geometry, 'VertexAttrNames', property( _geo_getVertexAttrNames ) )

def _geo_getPrimAttrNames( self ):
    return self.intrinsicValue( 'primitiveattributes' )
setAttr( hou.Geometry, 'PrimAttrNames', property( _geo_getPrimAttrNames ) )

def _geo_getDetailAttrNames( self ):
    return self.intrinsicValue( 'detailattributes' )
setAttr( hou.Geometry, 'DetailAttrNames', property( _geo_getDetailAttrNames ) )



def _geo_pointAttribute( self, name ):
    if '*' not in name:
        return self.findPointAttrib( name )

    else:
        name = name.replace('*', r'\w*')    
        attrs = [ i for i in self.PointAttrs if re.search( name, i.Name ) ]
        return attrs
setAttr( hou.Geometry, 'pointAttr', _geo_pointAttribute )

def _geo_vertexAttribute( self, name ):
    if '*' not in name:
        return self.findVertexAttrib( name )

    else:
        name = name.replace('*', r'\w*')    
        attrs = [ i for i in self.VertexAttrs if re.search( name, i.Name ) ]
        return attrs
setAttr( hou.Geometry, 'vertexAttr', _geo_vertexAttribute )

def _geo_primitiveAttribute( self, name ):
    if '*' not in name:
        return self.findPrimAttrib( name )

    else:
        name = name.replace('*', r'\w*')    
        attrs = [ i for i in self.PrimAttrs if re.search( name, i.Name ) ]
        return attrs
setAttr( hou.Geometry, 'primAttr', _geo_primitiveAttribute )

def _geo_detailAttribute( self, name ):
    if '*' not in name:
        return self.findGlobalAttrib( name )

    else:
        name = name.replace('*', r'\w*')    
        attrs = [ i for i in self.DetailAttrs if re.search( name, i.Name ) ]
        return attrs
setAttr( hou.Geometry, 'detailAttr', _geo_detailAttribute )



def _point_getAttr( self, name ):
    return self.Geo.pointAttr( name )
setAttr( hou.Point, 'attr', _point_getAttr )

def _vertex_getAttr( self, name ):
    return self.Geo.vertexAttr( name )
setAttr( hou.Vertex, 'attr', _vertex_getAttr )

def _prim_getAttr( self, name ):
    return self.Geo.primAttr( name )
setAttr( hou.Prim, 'attr', _prim_getAttr )

def _geo_getAttr( self, name ):
    return self.detailAttr( name )
setAttr( hou.Geometry, 'attr', _geo_getAttr, replace=True )




# ======================================================== #
# ===================== New Attribute ==================== #
# ======================================================== #
def _geo_newAttr( 
                    geo, 
                    attr_type, attr_name, 

                    attr_default, use_default_as_init = True,

                    transform_as_normal = False, 
                    create_local_variable = False,
                ):
    """
    Create new Attribute.

    Args:
        geo (hou.Geometry): [description]

        attr_type (enum): hou.attribType.Point / hou.attribType.Vertex / hou.attribType.Prim / hou.attribType.Global
        attr_name (str): [description]
        attr_default ([type]): [description]

        transform_as_normal (bool, optional): [description]. 
                                                Defaults to False.
        create_local_variable (bool, optional): [description]. 
                                                Defaults to True.

    Returns:
        [type]: [description]

    Examples:
        # new string attr
        geo.newPointAttr( 'name', 'box' )

        # new vec attr
        geo.newPointAttr( 'old_P', hou.Vector3(0,0,0) )
        
        # new array attr
        geo.newPointAttr( 'array_of_flt', (0.0,) )
    """
    # ======================================================== #
    # ================= new attr (non-array) ================= #
    # ======================================================== #
    if not isSequence( attr_default ):
        # get attr default
        if type( attr_default ) in Datatypes_with_Multi_Elements:
            attr_default = list( attr_default ) 

        # new attr
        new_attr = geo.addAttrib( 
                                    attr_type, attr_name, attr_default, 
                                    transform_as_normal = transform_as_normal, 
                                    create_local_variable = create_local_variable,
                                )

        # set init value
        if use_default_as_init:
            if attr_type == hou.attribType.Point and isinstance( attr_default, str ):
                geo.setPointStringAttribValues( attr_name, [attr_default] * geo.NumPoints )

            if attr_type == hou.attribType.Global and isinstance( attr_default, str ):
                geo.setGlobalAttribValue( attr_name, attr_default )


    # ======================================================== #
    # ==================== new array attr ==================== #
    # ======================================================== #
    else: 
        # get tuple size & data type
        if isSequence( attr_default[0] ):
            tuple_size = len( attr_default[0] )

            if isinstance( attr_default[0][0], int ):
                data_type = hou.attribData.Int

            elif isinstance( attr_default[0][0], float ):
                data_type = hou.attribData.Float

            else: # isinstance( attr_default[0][0], string ):
                data_type = hou.attribData.String
        
        elif type( attr_default[0] ) in Datatypes_with_Multi_Elements:
            tuple_size = len( list( attr_default[0] ) )

            data_type = hou.attribData.Float

        else:
            tuple_size = 1

            if isinstance(attr_default[0], int):
                data_type = hou.attribData.Int

            elif isinstance(attr_default[0], float):
                data_type = hou.attribData.Float

            else: # isinstance(attr_default[0], string):
                data_type = hou.attribData.String


        # new attr
        new_attr = geo.addArrayAttrib( attr_type, attr_name, data_type, tuple_size )


        # set init value
        # NOTE: only detail array attribute can be set
        if attr_type == hou.attribType.Global:
            geo.setGlobalAttribValue( attr_name, attr_default )
    return new_attr


def _geo_newPointAttr( self, attr_name, attr_default, **kwargs ):
    print( hou )
    return _geo_newAttr( self, hou.attribType.Point, attr_name, attr_default, **kwargs )
setAttr( hou.Geometry, 'newPointAttr', _geo_newPointAttr, replace=True )


def _geo_newVertexAttr( self, attr_name, attr_default, **kwargs ):
    return _geo_newAttr( self, hou.attribType.Vertex, attr_name, attr_default, **kwargs )
setAttr( hou.Geometry, 'newVertexAttr', _geo_newVertexAttr, replace=True )


def _geo_newPrimAttr( self, attr_name, attr_default, **kwargs ):
    return _geo_newAttr( self, hou.attribType.Prim, attr_name, attr_default, **kwargs )
setAttr( hou.Geometry, 'newPrimAttr', _geo_newPrimAttr, replace=True )


def _geo_newDetailAttr( self, attr_name, attr_default, **kwargs ):
    return _geo_newAttr( self, hou.attribType.Global, attr_name, attr_default, **kwargs )
setAttr( hou.Geometry, 'newDetailAttr', _geo_newDetailAttr, replace=True )




# ~~~~~~~~~~~~~~~~ Variable ~~~~~~~~~~~~~~~ #
setAttr( hou.Node, 'Locals', hou.Node.localVariables )





# ======================================================== #
# =============== Get / Set Attribute Value ============== #
# ======================================================== #
def _entity_getAttrValue( self, name ):
    """
    Get specific attribute value of current entity.

    Args:
        name (str): attribute name

    Returns:
        [type]: attribute value

    Examples:
        # point attr
        geo.point(0)['P']
        # vertex attr
        geo.prim(0).vertex(0)['uv']
        # primitive attr
        geo.prim(0)['shop_materialpath']
        # detail attr
        geo['test']
    """
    attr = self.attr( name )

    if not attr:
        return

    if attr.isArray():
        if attr.Datatype == hou.attribData.Int:
            value = self.intListAttribValue( name )

        elif attr.Datatype == hou.attribData.Float:
            value = self.floatListAttribValue( name )
            
        else: # attr.Datatype == hou.attribData.String:
            value = self.stringListAttribValue( name )
    
    else:
        value = self.attribValue( name )
    
    return value
setAttr( hou.Point, '__getitem__', _entity_getAttrValue, replace=True )
setAttr( hou.Vertex, '__getitem__', _entity_getAttrValue, replace=True )
setAttr( hou.Prim, '__getitem__', _entity_getAttrValue, replace=True )
setAttr( hou.Geometry, '__getitem__', _entity_getAttrValue, replace=True )


def _entity_setAttrValue( self, name, value ):
    """
    Set specific attribute value of current entity.

    Args:
        name (str): attribute name
        value ([type]): attribute value

    Examples:
        # WARNING: if new value is (2, 0, 0), the below codes would result in error.
        geo.point(0)['P'] = (2.0, 0, 0)
    """
    return self.setAttribValue( name, value )
setAttr( hou.Point, '__setitem__', _entity_setAttrValue, replace=True )
setAttr( hou.Vertex, '__setitem__', _entity_setAttrValue, replace=True )
setAttr( hou.Prim, '__setitem__', _entity_setAttrValue, replace=True )

def _geo_setAttrValue( self, name, value ):
    return self.setGlobalAttribValue( name, value )
setAttr( hou.Geometry, '__setitem__', _geo_setAttrValue, replace=True )











###########################################################################
################################ Attribute ################################
###########################################################################
'''
hou.Attrib      https://www.sidefx.com/docs/houdini/hom/hou/Attrib.html
'''

def _attr_setName( self, new_name ):
    attr_name = self.name()
    attr_type = self.type()

    geo = self.geometry()

    if attr_type == hou.attribType.Point:
        geo.renamePointAttrib( attr_name, new_name )

    elif attr_type == hou.attribType.Vertex:
        geo.renameVertexAttrib( attr_name, new_name )
    
    elif attr_type == hou.attribType.Prim:
        geo.renamePrimAttrib( attr_name, new_name )
    
    else: # attr_type == hou.attribType.Global:
        geo.renameGlobalAttrib( attr_name, new_name )
setAttr( hou.Attrib, 'Name', property( hou.Attrib.name, _attr_setName ) )

def _attr_getClass( self ):
    '''
    hou.attribType        https://www.sidefx.com/docs/houdini/hom/hou/attribType.html
    '''
    attr_class = str(self.type()).rsplit('.',1)[1].lower()
    return { 'point': 'point', 'vertex': 'vertex', 'prim': 'primitive', 'global': 'detail' }[attr_class]
setAttr( hou.Attrib, 'Class', property( _attr_getClass ) )


setAttr( hou.Attrib, "Type", property( hou.Attrib.type ) )


def _attr_getDatatype( self ):
    '''
    hou.attribData      https://www.sidefx.com/docs/houdini/hom/hou/attribData.html
    '''
    datatype = str(self.dataType()).rsplit('.',1)[1].lower()
    datasize = self.Size
    datatype = '{}{}'.format( datatype, datasize )
    return { 'int1': 'integer', 
            'float1': 'float', 
            'float3': 'vector3',
            'float4': 'vector4',
            'float9': 'matrix3',
            'float16': 'matrix4',
            'string1': 'string' }[datatype]
setAttr( hou.Attrib, "Datatype", property( _attr_getDatatype ) )

setAttr( hou.Attrib, "isArray", hou.Attrib.isArrayType )



setAttr( hou.Attrib, "Size", property( hou.Attrib.size, hou.Attrib.setSize ) )


setAttr( hou.Attrib, 'Geo', property( hou.Attrib.geometry ) )


setAttr( hou.Attrib, "Strings", property( hou.Attrib.strings ) )




# ======================================================== #
# ========================= Value ======================== #
# ======================================================== #
setAttr( hou.Attrib, "Default", property( hou.Attrib.defaultValue ) )



def _attr_Val( attr, mode='get', val=None, asString=False, fromString=False ):
    """
    Get / set values of all entities.

    Args:
        attr (hou.Attrib): [description]
        mode (str, optional): 'get' / 'set'. 
                                Defaults to 'get'.
        val ([type], optional): [description]. Defaults to None.
        
        asString (bool, optional): [description]. Defaults to False.
        fromString (bool, optional): [description]. Defaults to False.

    Returns:
        [value / None]: [description]

    Author: Sean
    """
    attr_name = attr.Name
    attr_type = attr.type().name()
    attr_size = attr.Size
    data_type = attr.dataType().name()

    geo = attr.Geo

    if attr_type == 'Point':

        if data_type == 'Int':
            if mode == 'get':
                return geo.pointIntAttribValues( attr_name ) if not asString else geo.pointIntAttribValuesAsString( attr_name, int_type=hou.numericData.Int32 )
            else: # mode == 'set'
                geo.setPointIntAttribValues( attr_name, val ) if not fromString else geo.setPointIntAttribValuesFromString( attr_name, val, int_type=hou.numericData.Int32)

        elif data_type == 'Float':
            if mode == 'get':
                return geo.pointFloatAttribValues( attr_name ) if not asString else geo.pointFloatAttribValuesAsString( attr_name, float_type=hou.numericData.Float32 )
            else: # mode == 'set'
                geo.setPointFloatAttribValues( attr_name, val ) if not fromString else geo.setPointFloatAttribValuesFromString( attr_name, val, float_type=hou.numericType.Float32)
        
        else: # data_type == 'String':
            if mode == 'get':
                return geo.pointStringAttribValues( attr_name )
            else: # mode == 'set'
                geo.setPointStringAttribValues( attr_name, val )


    elif attr_type == 'Vertex':

        if data_type == 'Int':
            if mode == 'get':
                return geo.vertexIntAttribValues( attr_name ) if not asString else geo.vertexIntAttribValuesAsString( attr_name, int_type=hou.numericData.Int32 )
            else: # mode == 'set'
                geo.setVertexIntAttribValues( attr_name, val ) if not fromString else geo.setVertexIntAttribValuesFromString( attr_name, val, int_type=hou.numericData.Int32)

        elif data_type == 'Float':
            if mode == 'get':
                return geo.vertexFloatAttribValues( attr_name ) if not asString else geo.vertexFloatAttribValuesAsString( attr_name, float_type=hou.numericData.Float32 )
            else: # mode == 'set'
                geo.setVertexFloatAttribValues( attr_name, val ) if not fromString else geo.setVertexFloatAttribValuesFromString( attr_name, val, int_type=hou.numericData.Int32)
        
        else: # data_type == 'String':
            if mode == 'get':
                return geo.vertexStringAttribValues( attr_name )
            else: # mode == 'set'
                geo.setVertexStringAttribValues( attr_name, val )


    elif attr_type == 'Prim':

        if data_type == 'Int':
            if mode == 'get':
                return geo.primIntAttribValues( attr_name ) if not asString else geo.primIntAttribValuesAsString( attr_name, int_type=hou.numericData.Int32 )
            else: # mode == 'set'
                geo.setPrimIntAttribValues( attr_name, val ) if not fromString else geo.setPrimIntAttribValuesFromString( attr_name, val, int_type=hou.numericType.Int32 )

        elif data_type == 'Float':
            if mode == 'get':
                return geo.primFloatAttribValues( attr_name ) if not asString else geo.primFloatAttribValuesAsString( attr_name, float_type=hou.numericData.Float32 )
            else: # mode == 'set'
                geo.setPrimFloatAttribValues( attr_name, val ) if not fromString else geo.setPrimFloatAttribValuesFromString( attr_name, val, float_type=hou.numericType.Float32 )
        
        else: # data_type == 'String':
            if mode == 'get':
                return geo.primStringAttribValues( attr_name )
            else: # mode == 'set'
                geo.setPrimStringAttribValues( attr_name, val )


    else: # attr_type == 'Global':

        if mode == 'get':
            return geo.attribValue( attr_name )
        else: # mode == 'set':
            geo.setGlobalAttribValue( attr_name, val )

def _attr_getValue( self ):
    return _attr_Val( self, mode='get' )

def _attr_setValue( self, val ):
    _attr_Val( self, mode='set' )

setAttr( hou.Attrib, 'Value', property( _attr_getValue, _attr_setValue ) )
setAttr( hou.Attrib, '_', hou.Attrib.Value )











