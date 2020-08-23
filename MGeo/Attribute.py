'''
Tier: Base
'''

from ..MVar import *





###########################################################################
############################### hou.Geometry ##############################
###########################################################################

# ~~~~~~~~~~~~~ Get Attribute ~~~~~~~~~~~~~ #
setAttr( hou.Geometry, 'PointAttrs', property( hou.Geometry.pointAttribs ) )
setAttr( hou.Geometry, 'VertexAttrs', property( hou.Geometry.vertexAttribs ) )
setAttr( hou.Geometry, 'PrimAttrs', property( hou.Geometry.primAttribs ) )
setAttr( hou.Geometry, 'DetailAttrs', property( hou.Geometry.globalAttribs ) )

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




# ~~~~~~~~~~ Get Detail Attribute ~~~~~~~~~ #
def _geo_getDetailAttr( self, name ):
    if self.findGlobalAttrib( name ):
        attr = Attribute( self, name )
        return attr
setAttr( hou.Geometry, '__getitem__', _geo_getDetailAttr, replace=False )




# ~~~~~~~~~~~~~ New Attribute ~~~~~~~~~~~~~ #
def _geo_newAttr( geo, attr_type, attr_name, attr_default, 
                        transform_as_normal=False, create_local_variable=True ):

    if not isSequence( attr_default ):
        new_attr = geo.addAttrib( attr_type, attr_name, attr_default, 
                                    transform_as_normal, create_local_variable)
        return new_attr

    else: # list / tuple
        tuple_size = attr_default.__len__()

        if isinstance(attr_default[0], int):
            data_type = hou.attribData.Int

        elif isinstance(attr_default[0], float):
            data_type = hou.attribData.Float

        else: # isinstance(attr_default[0], string):
            data_type = hou.attribData.String

        new_attr = geo.addArrayAttrib( attr_type, attr_name, data_type, tuple_size )
        return new_attr

def _geo_newPointAttr( self, attr_name, attr_default, transform_as_normal=False, create_local_variable=True ):
    return _geo_newAttr( self, hou.attribType.Point, attr_name, attr_default, transform_as_normal, create_local_variable )
setAttr( hou.Geometry, 'newPointAttr', _geo_newPointAttr )

def _geo_newVertexAttr( self, attr_name, attr_default, transform_as_normal=False, create_local_variable=True ):
    return _geo_newAttr( self, hou.attribType.Vertex, attr_name, attr_default, transform_as_normal, create_local_variable )
setAttr( hou.Geometry, 'newVertexAttr', _geo_newVertexAttr )

def _geo_newPrimAttr( self, attr_name, attr_default, transform_as_normal=False, create_local_variable=True ):
    return _geo_newAttr( self, hou.attribType.Prim, attr_name, attr_default, transform_as_normal, create_local_variable )
setAttr( hou.Geometry, 'newPrimAttr', _geo_newPrimAttr )

def _geo_newDetailAttr( self, attr_name, attr_default, transform_as_normal=False, create_local_variable=True ):
    return _geo_newAttr( self, hou.attribType.Global, attr_name, attr_default, transform_as_normal, create_local_variable )
setAttr( hou.Geometry, 'newDetailAttr', _geo_newDetailAttr )



# ~~~~~~~~~~~~~~~~ Variable ~~~~~~~~~~~~~~~ #
setAttr( hou.Node, 'Locals', hou.Node.localVariables )








###########################################################################
################################ hou.Point ################################
###########################################################################
def _point_getAttr( self, name ):
    if self.Geo.findPointAttrib( name ):
        attr = Attribute( self, name )
        return attr
setAttr( hou.Point, '__getitem__', _point_getAttr )




###########################################################################
################################ hou.Vertex ###############################
###########################################################################
def _vtx_getAttr( self, name ):
    if self.Geo.findVertexAttrib( name ):
        attr = Attribute( self, name )
        return attr
setAttr( hou.Vertex, '__getitem__', _vtx_getAttr )





###########################################################################
################################# hou.Prim ################################
###########################################################################
def _prim_getAttr( self, name ):
    if self.Geo.findPrimAttrib( name ):
        attr = Attribute( self, name )
        return attr
setAttr( hou.Prim, '__getitem__', _prim_getAttr )











###########################################################################
################################ Attribute ################################
###########################################################################
class Attribute( object ):

    def __init__( self, entity, name ):
        self.Entity = entity
        self.Name = name

    @property
    def Value( self ):
        value = self.Entity.attribValue( self.Name )
        return value

    @Value.setter
    def Value( self, value ):
        """
        Args:
            value ([type]): [description]


        Watch the type of input value.    
            # correct
            geo.point(0)['Cd'].Value = (0.0, 1.0, 0.0)

            # wrong
            geo.point(0)['Cd'].Value = (0, 1, 0)
        """
        # set value of detail attr
        if type( self.Entity ) is hou.Geometry:
            self.Entity.setGlobalAttribValue( self.Name, value )

        # set value of point / prim attr
        else:
            self.Entity.setAttribValue( self.Name, value )


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

setAttr( hou.Attrib, "Size", property( hou.Attrib.size, hou.Attrib.setSize ) )

setAttr( hou.Attrib, "Default", property( hou.Attrib.defaultValue ) )

setAttr( hou.Attrib, 'Geo', property( hou.Attrib.geometry ) )



def _attr_Val( self, mode='get', val=None, asString=False, fromString=False ):
    attr_name = self.name()
    attr_type = self.type().name()
    attr_size = self.size()
    data_type = self.dataType().name()

    geo = self.geometry()

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

        # if data_type == 'Int':
        #     if mode == 'get':
        #         return geo.intAttribValue( attr_name ) if attr_size == 1 else geo.intListAttribValue( attr_name )
        #     else: # mode == 'set'
        #         pass

        # elif data_type == 'Float':
        #     if mode == 'get':
        #         return geo.floatAttribValue( attr_name ) if attr_size == 1 else geo.floatListAttribValue( attr_name )
        #     else: # mode == 'set'
        #         pass
        
        # else: # data_type == 'String':
        #     if mode == 'get':
        #         return geo.stringAttribValue( attr_name ) if attr_size == 1 else geo.stringListAttribValue( attr_name )
        #     else: # mode == 'set'
        #         pass

        if mode == 'get':
            return geo.attribValue( attr_name )
        else: # mode == 'set':
            geo.setGlobalAttribValue( attr_name, val )
setAttr( hou.Attrib, '_Val', _attr_Val )

def _attr_getVal( self, asString=False ):
    return self._Val( mode='get', asString=asString )
setAttr( hou.Attrib, 'getVal', _attr_getVal )

def _attr_setVal( self, val, fromString=False ):
    self._Val( mode='set', val=val, fromString=fromString )
setAttr( hou.Attrib, 'setVal', _attr_setVal )



setAttr( hou.Attrib, "Strings", property( hou.Attrib.strings ) )









