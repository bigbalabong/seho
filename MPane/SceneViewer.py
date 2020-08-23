'''
Tier: Base
'''

from ..MVar import *




###########################################################################
############################### Scene Viewer ##############################
###########################################################################
'''
hou.SceneViewer         https://www.sidefx.com/docs/houdini/hom/hou/SceneViewer.html
'''

setAttr( hou.SceneViewer, "SelectedGeo", 
            property( hou.SceneViewer.currentGeometrySelection, hou.SceneViewer.setCurrentGeometrySelection ) )

setAttr( hou.SceneViewer, "SelectedItems", 
            property( hou.SceneViewer.currentSceneGraphSelection, hou.SceneViewer.setCurrentSceneGraphSelection ) )


setAttr( hou.SceneViewer, "CurrentState", 
            property( hou.SceneViewer.currentState, hou.SceneViewer.setCurrentState ) )
setAttr( hou.SceneViewer, "ViewerState", hou.SceneViewer.CurrentState )



setAttr( hou.SceneViewer, "CurrentViewport", property( hou.SceneViewer.curViewport ) )
setAttr( hou.SceneViewer, "Viewport", hou.SceneViewer.CurrentViewport )


setAttr( hou.SceneViewer, "Viewports", property( hou.SceneViewer.viewports ) )

setAttr( hou.SceneViewer, 'viewport', hou.SceneViewer.findViewport )





# ======================================================== #
# ======================== Select ======================== #
# ======================================================== #
def _sceneViewer_selectBones( self ):
    """
    Author: Sean
    """
    sels = self.selectObjects(
                        prompt = 'Select "Bone". \n Press enter to confirm.',
                        allowed_types = ('bone',),
                        allow_multisel = True,
                    )
    return sels
setAttr( hou.SceneViewer, 'selectBones', _sceneViewer_selectBones, replace=False )




# ======================================================== #
# ======================= Selection ====================== #
# ======================================================== #
def _sceneViewer_lssNodes( self ):
    """
    Author: Sean
    """
    return self.GeoSelection.Nodes
setAttr( hou.SceneViewer, 'lssNodes', _sceneViewer_lssNodes, replace=False )


def _sceneViewer_lssGeoType():
    """
    Author: Sean
    """
    return self.GeoSelection.GeoType
setAttr( hou.SceneViewer, 'lssGeoType', _sceneViewer_lssGeoType, replace=False )


def _sceneViewer_lssAABB( self ):
    """
    Author: Sean
    """
    return self.GeoSelection.AABB
setAttr( hou.SceneViewer, 'lssAABB', _sceneViewer_lssAABB, replace=False )

def _sceneViewer_lssOBB( self ):
    """
    Author: Sean
    """
    return self.GeoSelection.AABB
setAttr( hou.SceneViewer, 'lssOBB', _sceneViewer_lssOBB, replace=False )


        





###########################################################################
################################# Viewport ################################
###########################################################################
def _sceneViewer_getViewport():
    """
    Author: Sean
    """
    return hou.getSceneViewer().Viewport
setAttr( hou, 'getViewport', _sceneViewer_getViewport )


'''
hou.GeometryViewport    https://www.sidefx.com/docs/houdini/hom/hou/GeometryViewport.html
'''









###########################################################################
########################### hou.GeometryViewport ##########################
###########################################################################
'''
hou.GeometryViewportSettings    https://www.sidefx.com/docs/houdini/hom/hou/GeometryViewportSettings.html
'''

setAttr( hou.GeometryViewport, "Pivot", property( hou.GeometryViewport.viewPivot ) )

setAttr( hou.GeometryViewport, "Xform", property( hou.GeometryViewport.viewTransform ) )






# ======================================================== #
# ======================= Settings ======================= #
# ======================================================== #
def _viewport_getAspectRatioEnabled( self ):
    """
    Author: Sean
    """
    return self.settings().usingAspectRatio()

def _viewport_setAspectRatioEnabled( self, state ):
    """
    Author: Sean
    """
    self.settings().useAspectRatio( state )

setAttr( hou.GeometryViewport, "AspectRatioEnabled", 
            property( _viewport_getAspectRatioEnabled, _viewport_setAspectRatioEnabled ) )


def _viewport_getAspectRatio( self ):
    """
    Author: Sean
    """
    return self.settings().aspectRatio()

def _viewport_setAspectRatio( self, value=1 ):
    """
    Author: Sean
    """
    self.settings().setAspectRatio( value )

setAttr( hou.GeometryViewport, "AspectRatio", property( _viewport_getAspectRatio, _viewport_setAspectRatio ) )




def _viewport_getGamma( self ):
    """
    Author: Sean
    """
    return self.settings().sceneGamma()

def _viewport_setGamma( self, value=2.2 ):
    """
    Author: Sean
    """
    self.settings().setSceneGamma( value )

setAttr( hou.GeometryViewport, "Gamma", property( _viewport_getGamma, _viewport_setGamma ) )



def _viewport_getLUTEnabled( self ):
    """
    Author: Sean
    """
    return self.settings().useSceneLUT()

def _viewport_setLUTEnabled( self, state ):
    """
    Author: Sean
    """
    self.settings().setUseSceneLUT( state )

setAttr( hou.GeometryViewport, "LUTEnabled", property( _viewport_getLUTEnabled, _viewport_setLUTEnabled ) )


def _viewport_getLUT( self ):
    """
    Author: Sean
    """
    return self.settings().sceneLUT()

def _viewport_setLUT( self, filepath ):
    """
    Author: Sean
    """
    self.settings().setSceneLUT( filepath )

setAttr( hou.GeometryViewport, "LUT", property( _viewport_getLUT, _viewport_setLUT ) )



def _viewport_getAntialias( self ):
    """
    Author: Sean
    """
    return self.settings().sceneAntialias()

def _viewport_setAntialias( self, level=4 ):
    """
    Author: Sean
    """
    self.settings().setSceneAntialias( level )

setAttr( hou.GeometryViewport, "Antialias", property( _viewport_getAntialias, _viewport_setAntialias ) )



def _viewport_getXray( self ):
    """
    Author: Sean
    """
    return self.settings().xrayDrawing()

def _viewport_setXray( self, state=False ):
    """
    Author: Sean
    """
    self.settings().setXrayDrawing( state )

setAttr( hou.GeometryViewport, "Xray", property( _viewport_getXray, _viewport_setXray ) )



def _viewport_getBackfaceCulling( self ):
    """
    Author: Sean
    """
    return self.settings().removeBackfaces()

def _viewport_setBackfaceCulling( self, state=False ):
    """
    Author: Sean
    """
    self.settings().setRemoveBackfaces( state )

setAttr( hou.GeometryViewport, "BackfaceCulling", 
            property( _viewport_getBackfaceCulling, _viewport_setBackfaceCulling ) )



def _viewport_getHullsOnly( self ):
    """
    Author: Sean
    """
    return self.settings().hullsOnly()

def _viewport_setHullsOnly( self, state=False ):
    """
    Author: Sean
    """
    self.settings().setHullsOnly( state )

setAttr( hou.GeometryViewport, "HullsOnly", property( _viewport_getHullsOnly, _viewport_setHullsOnly ) )



def _viewport_getOnionSkinning( self ):
    """
    Author: Sean
    """
    return self.settings().onionSkinning()

def _viewport_setOnionSkinning( self, state=False ):
    """
    Author: Sean
    """
    self.settings().setOnionSkinning( state )

setAttr( hou.GeometryViewport, "OnionSkinning", 
            property( _viewport_getOnionSkinning, _viewport_setOnionSkinning ) )



# ~~~~~~~~~~~~~~~~~ Camera ~~~~~~~~~~~~~~~~ #
def _viewport_getCamera( self ):
    """[summary]

    Returns:
        [hou.Node]: [description]

    Author: Sean
    """
    return self.settings().camera()

def _viewport_setCamera( self, camera ):
    """[summary]

    Args:
        camera (hou.Node): [description]

    Author: Sean
    """
    self.settings().setCamera( camera )

setAttr( hou.GeometryViewport, "Camera", property( _viewport_getCamera, _viewport_setCamera ) )



# ~~~~~~~~~~~~~~~~ Geometry ~~~~~~~~~~~~~~~ #
def _viewport_getPointSize( self ):
    """
    Author: Sean
    """
    return self.settings().pointMarkerSize()

def _viewport_setPointSize( self, value=3.0 ):
    """
    Author: Sean
    """
    self.settings().setPointMarkerSize( value )

setAttr( hou.GeometryViewport, "PointSize", property( _viewport_getPointSize, _viewport_setPointSize ) )



def _viewport_getParticleSize( self ):
    """
    Author: Sean
    """
    return self.settings().particlePointSize()

def _viewport_setParticleSize( self, value=3.0 ):
    """
    Author: Sean
    """
    self.settings().particlePointSize( value )

setAttr( hou.GeometryViewport, "ParticleSize", property( _viewport_getParticleSize, _viewport_setParticleSize ) )



def _viewport_getNormalScale( self ):
    """
    Author: Sean
    """
    return self.settings().normalScale()

def _viewport_setNormalScale( self, value=0.2 ):
    """
    Author: Sean
    """
    self.settings().setNormalScale( value )

setAttr( hou.GeometryViewport, "NormalScale", property( _viewport_getNormalScale, _viewport_setNormalScale ) )



def _viewport_getWireWidth( self ):
    """
    Author: Sean
    """
    return self.settings().wireWidth()

def _viewport_setWireWidth( self, width=1.0 ):
    """
    Author: Sean
    """
    self.settings().wireWidth( width )

setAttr( hou.GeometryViewport, "WireWidth", property( _viewport_getWireWidth, _viewport_setWireWidth ) )



# ~~~~~~~~~~~~~~~~~ Volume ~~~~~~~~~~~~~~~~ #
def _viewport_getVolumeQuality( self ):
    """
    Author: Sean
    """
    return self.settings().volumeQuality()

def _viewport_setVolumeQuality( self, quality='normal' ):
    """
    Author: Sean
    """
    quality = { 
                'verylow':  hou.viewportVolumeQuality.VeryLow,
                'low':      hou.viewportVolumeQuality.Low,
                'normal':   hou.viewportVolumeQuality.Normal,
                'high':     hou.viewportVolumeQuality.High,
            }.get( quality.lower() )
    
    if not quality:
        quality = hou.viewportVolumeQuality.Normal
    
    self.settings().volumeQuality( quality )

setAttr( hou.GeometryViewport, "VolumeQuality", 
            property( _viewport_getVolumeQuality, _viewport_setVolumeQuality ), replace=False )



# ~~~~~~~~~~~~~~~~ Lighting ~~~~~~~~~~~~~~~ #
def _viewport_getLighting( self ):
    """
    Author: Sean
    """
    return self.settings().lighting()

def _viewport_setLighting( self, mode='normal' ):
    """
    Author: Sean
    """
    mode = { 
                'off':          hou.viewportLighting.Off,
                'headlight':    hou.viewportLighting.Headlight,
                'normal':       hou.viewportLighting.Normal,
                'high':         hou.viewportLighting.HighQuality,
                'highshadow':   hou.viewportLighting.HighQualityWithShadows,
            }.get( mode.lower() )
    
    if not mode:
        mode = hou.viewportLighting.Headlight
    
    self.settings().setLighting( mode )

setAttr( hou.GeometryViewport, "Lighting", property( _viewport_getLighting, _viewport_setLighting ), replace=False )


def _viewport_getLightingSamples( self ):
    """
    Author: Sean
    """
    return self.settings().lightSampling()

def _viewport_setLightingSamples( self, samples=8 ):
    """
    Author: Sean
    """
    self.settings().setLightSampling( samples )

setAttr( hou.GeometryViewport, "LightingSamples", property( _viewport_getLightingSamples, _viewport_setLightingSamples ) )



def _viewport_getAO( self ):
    """
    Author: Sean
    """
    return self.settings().ambientOcclusion()

def _viewport_setAO( self, state=True ):
    """
    Author: Sean
    """
    self.settings().setAmbientOcclusion( state )

setAttr( hou.GeometryViewport, "AO", property( _viewport_getAO, _viewport_setAO ) )



def _viewport_getAmbient( self ):
    """
    Author: Sean
    """
    return self.settings().showingAmbient()

def _viewport_setAmbient( self, state=True ):
    """
    Author: Sean
    """
    self.settings().showAmbient( state )

setAttr( hou.GeometryViewport, "Ambient", property( _viewport_getAmbient, _viewport_setAmbient ) )


def _viewport_getDiffuse( self ):
    """
    Author: Sean
    """
    return self.settings().showingDiffuse()

def _viewport_setDiffuse( self, state=True ):
    """
    Author: Sean
    """
    self.settings().showDiffuse( state )

setAttr( hou.GeometryViewport, "Diffuse", property( _viewport_getDiffuse, _viewport_setDiffuse ) )


def _viewport_getSpecular( self ):
    """
    Author: Sean
    """
    return self.settings().showingSpecular()

def _viewport_setSpecular( self, state=True ):
    """
    Author: Sean
    """
    self.settings().showSpecular( state )

setAttr( hou.GeometryViewport, "Specular", property( _viewport_getSpecular, _viewport_setSpecular ) )


def _viewport_getEmission( self ):
    """
    Author: Sean
    """
    return self.settings().showingEmission()

def _viewport_setEmission( self, state=True ):
    """
    Author: Sean
    """
    self.settings().showEmission( state )

setAttr( hou.GeometryViewport, "Specular", property( _viewport_getEmission, _viewport_setEmission ) )



def _viewport_getCd( self ):
    """
    Author: Sean
    """
    return self.settings().showingGeometryColor()

def _viewport_setCd( self, state=True ):
    """
    Author: Sean
    """
    self.settings().showGeometryColor( state )

setAttr( hou.GeometryViewport, "Cd", property( _viewport_getCd, _viewport_setCd ) )



def _viewport_getTexture( self ):
    """
    Author: Sean
    """
    return self.settings().displayTextures()

def _viewport_setTexture( self, state=True ):
    """
    Author: Sean
    """
    self.settings().setDisplayTextures( state )

setAttr( hou.GeometryViewport, "Texture", property( _viewport_getTexture, _viewport_setTexture ) )


def _viewport_getTexture2DRes( self ):
    """
    Author: Sean
    """
    return self.settings().textureMaxRes2D()

def _viewport_setTexture2DRes( self, res=2048 ):
    """
    Author: Sean
    """
    if not isSequence( res ):
        res = ( res, res, res )

    self.settings().setTextureMaxRes2D( res )

setAttr( hou.GeometryViewport, "Texture2DRes", property( _viewport_getTexture2DRes, _viewport_setTexture2DRes ) )


def _viewport_getTexture3DRes( self ):
    """
    Author: Sean
    """
    return self.settings().textureMaxRes3D()

def _viewport_setTexture3DRes( self, res=256 ):
    """
    Author: Sean
    """
    if not isSequence( res ):
        res = ( res, res, res )

    self.settings().setTextureMaxRes3D( res )

setAttr( hou.GeometryViewport, "Texture3DRes", property( _viewport_getTexture3DRes, _viewport_setTexture3DRes ) )



def _viewport_getMaterial( self ):
    """
    Author: Sean
    """
    return self.settings().showingMaterials()

def _viewport_setMaterial( self, state=True ):
    """
    Author: Sean
    """
    self.settings().showMaterials( state )

setAttr( hou.GeometryViewport, "Material", property( _viewport_getMaterial, _viewport_setMaterial ) )


def _viewport_getMaterialStylesheet( self ):
    """
    Author: Sean
    """
    return self.settings().usingMaterialStylesheets()

def _viewport_setMaterialStylesheet( self, state=True ):
    """
    Author: Sean
    """
    self.settings().useMaterialStylesheets( state )

setAttr( hou.GeometryViewport, "MaterialStylesheet", 
            property( _viewport_getMaterialStylesheet, _viewport_setMaterialStylesheet ) )



def _viewport_getDisplacement( self ):
    """
    Author: Sean
    """
    return self.settings().usingDisplacement()

def _viewport_setDisplacement( self, state=True ):
    """
    Author: Sean
    """
    self.settings().useDisplacement( state )

setAttr( hou.GeometryViewport, "Displacement", property( _viewport_getDisplacement, _viewport_setDisplacement ) )


def _viewport_getDisplacementLevel( self ):
    """
    Author: Sean
    """
    return self.settings().displacementLevel()

def _viewport_setDisplacementLevel( self, level=1.0 ):
    """
    Author: Sean
    """
    self.settings().setDisplacementLevel( level )

setAttr( hou.GeometryViewport, "DisplacementLevel", 
            property( _viewport_getDisplacementLevel, _viewport_setDisplacementLevel ) )



def _viewport_getShadowMapSize( self ):
    """
    Author: Sean
    """
    return self.settings().shadowMapSize()

def _viewport_setShadowMapSize( self, size=2048 ):
    """
    Author: Sean
    """
    self.settings().setShadowMapSize( size )

setAttr( hou.GeometryViewport, "ShadowMapSize", property( _viewport_getShadowMapSize, _viewport_setShadowMapSize ) )











###########################################################################
########################## hou.GeometrySelection ##########################
###########################################################################
setAttr( hou.SceneViewer, "GeoSelection", property( hou.SceneViewer.currentGeometrySelection ) )


'''
hou.GeometrySelection       https://www.sidefx.com/docs/houdini/hom/hou/GeometrySelection.html
'''
setAttr( hou.GeometrySelection, "Nodes", property( hou.GeometrySelection.nodes ) )


setAttr( hou.GeometrySelection, "GeoType", 
            property( hou.GeometrySelection.geometryType, hou.GeometrySelection.setGeometryType ) )


setAttr( hou.GeometrySelection, "AABB", property( hou.GeometrySelection.boundingBox ) )
setAttr( hou.GeometrySelection, "OBB", property( hou.GeometrySelection.orientedBoundingBox ) )


def _geoSelection_getNum( self ):
    """
    Author: Sean
    """
    return sum([ i.Num for i in self.Selections ])
setAttr( hou.GeometrySelection, "Num", property( _geoSelection_getNum ) )








###########################################################################
############################## hou.Selection ##############################
###########################################################################
def _sceneViewer_getSelections( self ):
    return self.GeoSelection.Selections
setAttr( hou.SceneViewer, "Selections", property( _sceneViewer_getSelections ), replace=False )


def _geoSelection_getSelections( self ):
    nodes = self.Nodes
    geo = [ i.Geo for i in nodes ]
    sels = self.selections()

    for i, sel in enumerate( sels ):
        setAttr( sel, 'Node', nodes[i] )
        setAttr( sel, 'Geo', geo[i] )
        
    return sels
setAttr( hou.GeometrySelection, "Selections", property( _geoSelection_getSelections ), replace=False )


'''
hou.Selection           https://www.sidefx.com/docs/houdini/hom/hou/Selection.html
'''

setAttr( hou.Selection, "GeoType", property( hou.Selection.selectionType ) )

setAttr( hou.Selection, "Num", property( hou.Selection.numSelected ) )


def _selection_getPoints( self ):
    return self.points( self.Geo )
setAttr( hou.Selection, 'Points', property( _selection_getPoints ) )

def _selection_getVertices( self ):
    return self.vertices( self.Geo )
setAttr( hou.Selection, 'Vertices', property( _selection_getVertices ) )

def _selection_getEdges( self ):
    return self.edges( self.Geo )
setAttr( hou.Selection, 'Edges', property( _selection_getEdges ) )

def _selection_getPrims( self ):
    return self.prims( self.Geo )
setAttr( hou.Selection, 'Prims', property( _selection_getPrims ) )


setAttr( hou.Selection, 'Num', property( hou.Selection.numSelected ) )



def _selection_getSelectionString( self ):
    return self.selectionString( self.Geo )
setAttr( hou.Selection, 'SelectionString', property( _selection_getSelectionString ) )



# ~~~~~~~~~~~~~~ Bounding Box ~~~~~~~~~~~~~ #
def _selection_getPointAABB( self ):
    return self.Geo.pointBoundingBox( self.SelectionString )
setAttr( hou.Selection, 'getPointAABB', _selection_getPointAABB )

def _selection_getPrimAABB( self ):
    return self.Geo.primBoundingBox( self.SelectionString )
setAttr( hou.Selection, 'getPrimAABB', _selection_getPrimAABB )



def _selection_newAABB( self, obb=False ):
    """[summary]

    Args:
        obb (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]

    Author: Sean
    """
    node = self.Node

    bound = node.Out0 >> 'bound'
    bound.moveToGoodPosition()


    geotype = {
                'points':       'points',
                'edges':        'edges',
                'breakpoints':  'breakpoints',
                'primitives':   'prims',
            }.get( self.GeoType.name().lower() )

    if not geotype:
        return

    bound._['grouptype']._ = geotype
    bound._['group']._ = self.SelectionString

    bound.Template = True


    # switch to OBB
    if obb:
        bound._['orientedbbox']._ = True

    return bound
setAttr( hou.Selection, 'newAABB', _selection_newAABB, replace=True )

def _selection_newOBB( self ):
    return self.newAABB( True )
setAttr( hou.Selection, 'newOBB', _selection_newOBB )








###########################################################################
############################ Construction Plane ###########################
###########################################################################
setAttr( hou.SceneViewer, "ConstructionPlane", property( hou.SceneViewer.constructionPlane ) )


'''
hou.ConstructionPlane   https://www.sidefx.com/docs/houdini/hom/hou/ConstructionPlane.html
'''
setAttr( hou.ConstructionPlane, "SceneViewer", property( hou.ConstructionPlane.sceneViewer ) )


setAttr( hou.ConstructionPlane, "Visible", 
            property( hou.ConstructionPlane.isVisible, hou.ConstructionPlane.setIsVisible ) )


setAttr( hou.ConstructionPlane, "Transform", 
            property( hou.ConstructionPlane.transform, hou.ConstructionPlane.setTransform ) )
setAttr( hou.ConstructionPlane, "Xform", hou.ConstructionPlane.Transform )


setAttr( hou.ConstructionPlane, "CellSize", 
            property( hou.ConstructionPlane.cellSize, hou.ConstructionPlane.setCellSize ) )
setAttr( hou.ConstructionPlane, "NumCells", 
            property( hou.ConstructionPlane.numberOfCells, hou.ConstructionPlane.setNumberOfCells ) )
setAttr( hou.ConstructionPlane, "NumCellsPerRulerLine", 
            property( hou.ConstructionPlane.numberOfCellsPerRulerLine, hou.ConstructionPlane.setNumberOfCellsPerRulerLine ) )







###########################################################################
############################# Reference Plane #############################
###########################################################################
setAttr( hou.SceneViewer, "ReferencePlane", property( hou.SceneViewer.referencePlane ) )


'''
hou.ReferencePlane  https://www.sidefx.com/docs/houdini/hom/hou/ReferencePlane.html
'''
setAttr( hou.ReferencePlane, "SceneViewer", property( hou.ReferencePlane.sceneViewer ) )


setAttr( hou.ReferencePlane, "Visible", property( hou.ReferencePlane.isVisible, hou.ReferencePlane.setIsVisible ) )


setAttr( hou.ReferencePlane, "Transform", property( hou.ReferencePlane.transform, hou.ReferencePlane.setTransform ) )
setAttr( hou.ReferencePlane, "Xform", hou.ReferencePlane.Transform )


setAttr( hou.ReferencePlane, "CellSize", property( hou.ReferencePlane.cellSize, hou.ReferencePlane.setCellSize ) )
setAttr( hou.ReferencePlane, "NumCellsPerRulerLine", 
            property( hou.ReferencePlane.numberOfCellsPerRulerLine, hou.ReferencePlane.setNumberOfCellsPerRulerLine ) )









