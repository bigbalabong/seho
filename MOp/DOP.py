'''
Tier: Base
'''

from ..MVar import *




###########################################################################
################################### DOP ###################################
###########################################################################
'''
hou.DopNode         http://www.sidefx.com/docs/houdini/hom/hou/DopNode.html
'''








###########################################################################
############################## DOP Simulation #############################
###########################################################################
'''
hou.DopSimulation   http://www.sidefx.com/docs/houdini/hom/hou/DopSimulation.html
'''

# ======================================================== #
# ========================= Time ========================= #
# ======================================================== #
setAttr( hou.DopSimulation, "Time", property( hou.DopSimulation.time, hou.DopSimulation.setTime ) )

setAttr( hou.DopSimulation, "TimeStep", property( hou.DopSimulation.timestep, hou.DopSimulation.setTimestep ) )




# ======================================================== #
# ========================= State ======================== #
# ======================================================== #
setAttr( hou.DopSimulation, "Memory", property( hou.DopSimulation.memoryUsage ) )






###########################################################################
################################# DOP Data ################################
###########################################################################
'''
hou.DopData         http://www.sidefx.com/docs/houdini/hom/hou/DopData.html
'''


# ======================================================== #
# ========================= Basic ======================== #
# ======================================================== #
setAttr( hou.DopData, "Id", property( hou.DopData.id ) )

setAttr( hou.DopData, "Path", property( hou.DopData.path ) )

setAttr( hou.DopData, "DataType", property( hou.DopData.dataType ) )





# ======================================================== #
# ======================= Sub-data ======================= #
# ======================================================== #
def _dopData_getAllSubdata( self ):
    all_subdata = self.subData()

    for name, subdata in all_subdata.items():
        subdata.Name = name
    
    all_subdata = all_subdata.values()
    return all_subdata
setAttr( hou.DopData, "Subdata", property( _dopData_getAllSubdata ), replace=False )

setAttr( hou.DopData, "subdata", hou.DopData.findSubData )





setAttr( hou.DopData, "Geometry", property( hou.DopData.geometry ) )
setAttr( hou.DopData, "Geo", hou.DopData.Geometry )


def _dopData_getSubdataForces( self ):
    return self.AllSubdata.get( 'Forces' )
setAttr( hou.DopData, "Forces", property( _dopData_getSubdataForces ) )

def _dopData_getSubdataColliders( self ):
    return self.AllSubdata.get( 'Colliders' )
setAttr( hou.DopData, "Colliders", property( _dopData_getSubdataColliders ) )

def _dopData_getSubdataPhysicalParms( self ):
    return self.AllSubdata.get( 'PhysicalParms' )
setAttr( hou.DopData, "PhysicalParms", property( _dopData_getSubdataPhysicalParms ) )

def _dopData_getSubdataSolver( self ):
    return self.AllSubdata.get( 'Solver' )
setAttr( hou.DopData, "Solver", property( _dopData_getSubdataSolver ) )







# ======================================================== #
# ========================= State ======================== #
# ======================================================== #
setAttr( hou.DopData, "Frozen", property( hou.DopData.isFrozen ) )







# ======================================================== #
# ======================== Record ======================== #
# ======================================================== #
'''
hou.DopRecord       http://www.sidefx.com/docs/houdini/hom/hou/DopRecord.html
'''
class FakeRecord( object ):

    def __init__( self, record ):
        self.Record = record

    def __getitem__( self, field_name ):
        return self.Record.field2( field_name )

def _record_getFakeRecord( self ):
    return FakeRecord( self )
setAttr( hou.DopRecord, "_", property( _record_getFakeRecord ) )


setAttr( hou.DopRecord, "Index", property( hou.DopRecord.recordIndex ) )

setAttr( hou.DopRecord, "Type", property( hou.DopRecord.recordType ) )







# ======================================================== #
# ========================= Field ======================== #
# ======================================================== #
class RecordField( object ):

    def __init__( self, record, 
                        field_name, field_type, field_value ):
        self.Record = record
        
        self.Name =     field_name
        self.Type =     field_type
        self.Value =    field_value
        self._ =        field_value







'''
hou.DopObject       http://www.sidefx.com/docs/houdini/hom/hou/DopObject.html
'''
setAttr( hou.DopObject, "Name", property( hou.DopObject.name ) )

setAttr( hou.DopObject, "ObjId", property( hou.DopObject.objid ) )



setAttr( hou.DopObject, "Xform", property( hou.DopObject.transform ) )







'''
hou.DopRelationship     http://www.sidefx.com/docs/houdini/hom/hou/DopRelationship.html
'''
setAttr( hou.DopRelationship, "Name", property( hou.DopRelationship.name ) )








###########################################################################
################################# Shortcut ################################
###########################################################################

# ======================================================== #
# ========================= Node ========================= #
# ======================================================== #
setAttr( hou.DopNode, "DopNet", property( hou.DopNode.dopNetNode ) )

setAttr( hou.DopNode, "Sim", property( hou.DopNode.simulation ) )
setAttr( hou.Node, "Sim", property( hou.Node.simulation ) )


setAttr( hou.DopNode, "Created", property( hou.DopNode.createdObjects ) )

setAttr( hou.DopNode, "Processed", property( hou.DopNode.processedObjects ) )
setAttr( hou.DopNode, "GonnaProcess", property( hou.DopNode.objectsToProcess ) )




def _dop_getDopObject( self ):
    '''
    RETURN:
            Dop object.
    '''
    dop_object = [ i.eval() for i in self.Parms if i.Name in ('objname', 'object_name') ]
    
    if not dop_object:
        return
    else:
        dop_object = dop_object[0]

    dop_object = [ i for i in self.processedObjects() if i.name() == dop_object ]

    if not dop_object:
        return
    else:
        return dop_object[0]
setAttr( hou.DopNode, "DopObject", property( _dop_getDopObject ) )



setAttr( hou.DopNode, "PythonSolverData", property( hou.DopNode.pythonSolverData ) )





# ======================================================== #
# ========================== Sim ========================= #
# ======================================================== #
setAttr( hou.DopSimulation, "DopNet", property( hou.DopSimulation.dopNetNode ) )



setAttr( hou.DopSimulation, "AllData", property( hou.DopSimulation.findAllData ) )

setAttr( hou.DopSimulation, "data", hou.DopSimulation.findData )



setAttr( hou.DopSimulation, "Objects", property( hou.DopSimulation.objects ) )

setAttr( hou.DopSimulation, "object", hou.DopSimulation.findObject )



setAttr( hou.DopSimulation, "Relationships", property( hou.DopSimulation.relationships ) )

setAttr( hou.DopSimulation, "relationship", hou.DopSimulation.findRelationship )






# ======================================================== #
# ========================= Data ========================= #
# ======================================================== #
setAttr( hou.DopData, "Creator", property( hou.DopData.creator ) )

def _dopData_getNode( self ):
    node = self.Creator.Parent

    parent_is_locked_hda = node.isLockedHDA()
    parent_cate = node.Parent.Type.Cate.Name

    while parent_is_locked_hda and parent_cate == 'Dop':
        node = node.Parent

    return node
setAttr( hou.DopData, "Node", property( _dopData_getNode ), replace=False )



setAttr( hou.DopData, "DopNet", property( hou.DopData.dopNetNode ) )

setAttr( hou.DopData, "Sim", property( hou.DopData.simulation ) )



# ~~~~~~~~~~~~~~~~~ Record ~~~~~~~~~~~~~~~~ #
setAttr( hou.DopData, "RecordTypes", property( hou.DopData.recordTypes ) )


def _dopData_getRecords( self ):
    records = []
    for record_type in self.RecordTypes:
        records += self.records( record_type )
    return records
setAttr( hou.DopData, "Records", property( _dopData_getRecords ) )


def _dopData_getRecordTypeBasic( self ):
    return self.record( 'Basic' )
setAttr( hou.DopData, "Basic", property( _dopData_getRecordTypeBasic ) )

setAttr( hou.DopData, "Options", property( hou.DopData.options ) )



# ~~~~~~~~~~~~~~~~~ Field ~~~~~~~~~~~~~~~~~ #
def _dopData_getFields( self ):
    """
    Returns:
        [list of RecordField]: all the fields of records in this dop data.
    """
    fields = []

    for record_type in self.RecordTypes:

        records = self.records( record_type )

        for record in records:
            fields += record.Fields
    
    return fields
setAttr( hou.DopData, "Fields", property( _dopData_getFields ) )


def _dopData_getFieldNames( self ):
    return [ i.Name for i in self.Fields ]
setAttr( hou.DopData, "FieldNames", property( _dopData_getFieldNames ), replace=False )

def _dopData_getFieldNames( self ):
    return [ i.Value for i in self.Fields ]
setAttr( hou.DopData, "FieldValues", property( _dopData_getFieldNames ), replace=False )









# ======================================================== #
# ======================== Record ======================== #
# ======================================================== #
def _record_getField( self, field_name ):
    field_type = self.fieldType( field_name )
    field_value = self.field( field_name )

    return RecordField( record = self, 
                        field_name = field_name,
                        field_type = field_type,
                        field_value = field_value )
setAttr( hou.DopRecord, "field2", _record_getField )


def _record_getFields( self ):
    field_names = self.FieldNames
    return [ self.field2( i ) for i in field_names ]
setAttr( hou.DopRecord, "Fields", property( _record_getFields ) )

setAttr( hou.DopRecord, "FieldNames", property( hou.DopRecord.fieldNames ) )








