'''
Tier: Base
'''

from ..MVar import *





###########################################################################
################################### OBJ ###################################
###########################################################################
'''
hou.ObjNode     http://www.sidefx.com/docs/houdini/hom/hou/ObjNode.html
'''

def _obj_getOrigin( self ):
    """
    Return the object's origin position, in world space.
    """
    return self.origin()
setAttr( hou.ObjNode, "Origin", property( _obj_getOrigin ) )





# ======================================================== #
# =================== Transform Matrix =================== #
# ======================================================== #
def _obj_getLocalTransform( self ):
    return self.localTransform()
setAttr( hou.ObjNode, "LOCAL", property( _obj_getLocalTransform ) )


def _obj_getWorldTransform( self ):
    return self.worldTransform()

def _obj_setWorldTransform( self, transform ):
    self.setWorldTransform( transform, fail_on_locked_parms=False )

setAttr( hou.ObjNode, "WORLD", property( _obj_getWorldTransform, _obj_setWorldTransform ) )



def _obj_getParmTransform( self ):
    return self.parmTransform()

def _obj_setParmTransform( self, transform ):
    self.setParmTransform( transform, fail_on_locked_parms=False )

setAttr( hou.ObjNode, "PARM", property( _obj_getParmTransform, _obj_setParmTransform ) )



def _obj_getPivotTransform( self ):
    return self.parmPivotTransform()

def _obj_setPivotTransform( self, transform ):
    self.setParmTransform( transform, fail_on_locked_parms=False )

setAttr( hou.ObjNode, "PIVOT", property( _obj_getPivotTransform, _obj_setPivotTransform ) )


def _obj_getParentTransform( self ):
    """
    Return the input node's world space transform (if there is an input connected), 
    combined with the world space transform of the containing subnet object (if there is one). 
    """
    return self.parentAndSubnetTransform()
setAttr( hou.ObjNode, "PARENT", property( _obj_getParentTransform ) )


def _obj_getPreTransform( self ):
    """
    Return this object's pretransform.
    The pre-transform allows you to apply a transform after the parameter transform 
    but before input and containing object transforms.
    """
    return self.preTransform()

def _obj_setPreTransform( self, transform ):
    self.setPreTransform( transform )

setAttr( hou.ObjNode, "PRE", property( _obj_getPreTransform, _obj_setPreTransform ) )


setAttr( hou.ObjNode, 'parmToPre', hou.ObjNode.moveParmTransformIntoPreTransform )
setAttr( hou.ObjNode, 'parmTranslateToPre', hou.ObjNode.moveParmTranslateIntoPreTransform )
setAttr( hou.ObjNode, 'parmRotateToPre', hou.ObjNode.moveParmRotateIntoPreTransform )
setAttr( hou.ObjNode, 'parmScaleToPre', hou.ObjNode.moveParmScaleIntoPreTransform )


setAttr( hou.ObjNode, 'preToParm', hou.ObjNode.movePreTransformIntoParmTransform )


setAttr( hou.ObjNode, 'lookAt', hou.ObjNode.buildLookatRotation )



def _obj_getTransformOrder( self ):
    parm = self._['xOrd']
    order = parm.MenuValues[ parm._ ]
    return order

def _obj_setTransformOrder( self, order ):
    self._['xOrd']._ = order

setAttr( hou.ObjNode, 'TransformOrder', property( _obj_getTransformOrder, _obj_setTransformOrder ) )



def _obj_getRotateOrder( self ):
    parm = self._['rOrd']
    order = parm.MenuValues[ parm._ ]
    return order

def _obj_setRotateOrder( self, order ):
    self._['rOrd']._ = order

setAttr( hou.ObjNode, 'RotateOrder', property( _obj_getRotateOrder, _obj_setRotateOrder ) )








def _obj_getKeepPositionState( self ):
    """
    Keep position when parenting.
    """
    return self.parm('keeppos').eval()

def _obj_setKeepPositionState( self, bool ):
    self.parm('keeppos').set( bool )

setAttr( hou.ObjNode, "KeepPos", property( _obj_getKeepPositionState, _obj_setKeepPositionState ) )




def _obj_getConstraintState( self ):
    return self.parm('constraints_on').eval()

def _obj_setConstraintState( self, bool ):
    self.parm('constraints_on').set( bool )

setAttr( hou.ObjNode, "EnabledConstraint", property( _obj_getConstraintState, _obj_setConstraintState ) )







