'''
Tier: Base
'''

from ..MVar import *







###########################################################################
################################### Tag ###################################
###########################################################################

GroupScriptAction = """import soputils
kwargs['geometrytype'] = ({}, )
kwargs['inputindex'] = 0
soputils.selectGroupParm(kwargs)"""


class ParmTags( object ):
    
    """
    Author: Sean
    """

    def __init__( self, parm_template ):
        self.ParmTemplate = parm_template


    @property
    def Tags( self ):
        """
        Author: Sean
        """
        return self.ParmTemplate.tags()

    @Tags.setter
    def Tags( self, tags ):
        """
        Author: Sean
        """
        self.ParmTemplate.setTags( tags )



    # ======================================================== #
    # ========================= Group ======================== #
    # ======================================================== #
    def _updateGroupScriptActionCodes( self, codes, geotype, state ):
        """
        Author: Sean
        """
        if state and codes is None:
            codes = GroupScriptAction.format( geotype )

        elif state and geotype not in codes:
            codes = codes.split( '\n', 2 )
            codes[1] = '{}{}, )'.format( codes[1][:-1], geotype )
            codes = '\n'.join( codes )

        elif not state and geotype in codes:
            codes = codes.split( '\n', 2 )
            codes[1] = ' '.join( codes[1].split( geotype + ',' ) )
            codes = '\n'.join( codes )

        return codes



    @property
    def GroupPoints( self ):
        """
        Author: Sean
        """
        codes = self.Tags.get( 'script_action' )

        if codes is None:
            return False
        else:
            return 'hou.geometryType.Points' in codes
    
    @GroupPoints.setter
    def GroupPoints( self, state ):
        """
        Author: Sean
        """
        tags = self.Tags

        codes = tags.get( 'script_action' )

        codes = self._updateGroupScriptActionCodes( codes, 'hou.geometryType.Points', state )
        if codes is not None:
            tags['script_action'] = codes

            if 'script_action_icon' not in tags.keys():
                tags['script_action_icon'] = 'BUTTONS_reselect'

        self.Tags = tags



    @property
    def GroupVertices( self ):
        """
        Author: Sean
        """
        codes = self.Tags.get( 'script_action' )

        if codes is None:
            return False
        else:
            return 'hou.geometryType.Vertices' in codes
    
    @GroupVertices.setter
    def GroupVertices( self, state ):
        """
        Author: Sean
        """
        tags = self.Tags

        codes = tags.get( 'script_action' )

        codes = self._updateGroupScriptActionCodes( codes, 'hou.geometryType.Vertices', state )
        if codes is not None:
            tags['script_action'] = codes

            if 'script_action_icon' not in tags.keys():
                tags['script_action_icon'] = 'BUTTONS_reselect'

        self.Tags = tags



    @property
    def GroupEdges( self ):
        """
        Author: Sean
        """
        codes = self.Tags.get( 'script_action' )

        if codes is None:
            return False
        else:
            return 'hou.geometryType.Edges' in codes
    
    @GroupEdges.setter
    def GroupEdges( self, state ):
        """
        Author: Sean
        """
        tags = self.Tags

        codes = tags.get( 'script_action' )

        codes = self._updateGroupScriptActionCodes( codes, 'hou.geometryType.Edges', state )
        if codes is not None:
            tags['script_action'] = codes

            if 'script_action_icon' not in tags.keys():
                tags['script_action_icon'] = 'BUTTONS_reselect'

        self.Tags = tags



    @property
    def GroupBreakpoints( self ):
        """
        Author: Sean
        """
        codes = self.Tags.get( 'script_action' )

        if codes is None:
            return False
        else:
            return 'hou.geometryType.Breakpoints' in codes
    
    @GroupBreakpoints.setter
    def GroupBreakpoints( self, state ):
        """
        Author: Sean
        """
        tags = self.Tags

        codes = tags.get( 'script_action' )

        codes = self._updateGroupScriptActionCodes( codes, 'hou.geometryType.Breakpoints', state )
        if codes is not None:
            tags['script_action'] = codes

            if 'script_action_icon' not in tags.keys():
                tags['script_action_icon'] = 'BUTTONS_reselect'

        self.Tags = tags



    @property
    def GroupPrims( self ):
        """
        Author: Sean
        """
        codes = self.Tags.get( 'script_action' )

        if codes is None:
            return False
        else:
            return 'hou.geometryType.Primitives' in codes
    
    @GroupPrims.setter
    def GroupPrims( self, state ):
        """
        Author: Sean
        """
        tags = self.Tags

        codes = tags.get( 'script_action' )

        codes = self._updateGroupScriptActionCodes( codes, 'hou.geometryType.Primitives', state )
        if codes is not None:
            tags['script_action'] = codes

            if 'script_action_icon' not in tags.keys():
                tags['script_action_icon'] = 'BUTTONS_reselect'

        self.Tags = tags




    # ======================================================== #
    # ========================= Maya ========================= #
    # ======================================================== #
    '''
    Group       http://www.sidefx.com/docs/maya/_maya__group.html
    '''

    @property
    def MayaSelectVertex( self ):
        """
        Author: Sean
        """
        tags = self.Tags
        return 'sidefx::maya_component_selection_type' in tags and tags['sidefx::maya_component_selection_type'] == 'vertex'

    @MayaSelectVertex.setter
    def MayaSelectVertex( self, state=True ):
        """
        Author: Sean
        """
        tags = self.Tags

        if state:
            tags['sidefx::maya_component_selection_type'] = 'vertex'
        else:
            if 'sidefx::maya_component_selection_type' in tags.keys():
                tags.pop( 'sidefx::maya_component_selection_type' )
        
        # update tags
        self.Tags = tags


    @property
    def MayaSelectEdge( self ):
        """
        Author: Sean
        """
        tags = self.Tags
        return 'sidefx::maya_component_selection_type' in tags and tags['sidefx::maya_component_selection_type'] == 'edge'

    @MayaSelectEdge.setter
    def MayaSelectEdge( self, state=True ):
        """
        Author: Sean
        """
        tags = self.Tags

        if state:
            tags['sidefx::maya_component_selection_type'] = 'edge'
        else:
            if 'sidefx::maya_component_selection_type' in tags.keys():
                tags.pop( 'sidefx::maya_component_selection_type' )
        
        # update tags
        self.Tags = tags


    @property
    def MayaSelectFace( self ):
        """
        Author: Sean
        """
        tags = self.Tags
        return 'sidefx::maya_component_selection_type' in tags and tags['sidefx::maya_component_selection_type'] == 'edge'

    @MayaSelectFace.setter
    def MayaSelectFace( self, state=True ):
        """
        Author: Sean
        """
        tags = self.Tags

        if state:
            tags['sidefx::maya_component_selection_type'] = 'face'
        else:
            if 'sidefx::maya_component_selection_type' in tags.keys():
                tags.pop( 'sidefx::maya_component_selection_type' )
        
        # update tags
        self.Tags = tags


    @property
    def MayaSelectUV( self ):
        """
        Author: Sean
        """
        tags = self.Tags
        return 'sidefx::maya_component_selection_type' in tags and tags['sidefx::maya_component_selection_type'] == 'edge'

    @MayaSelectUV.setter
    def MayaSelectUV( self, state=True ):
        """
        Author: Sean
        """
        tags = self.Tags

        if state:
            tags['sidefx::maya_component_selection_type'] = 'uv'
        else:
            if 'sidefx::maya_component_selection_type' in tags.keys():
                tags.pop( 'sidefx::maya_component_selection_type' )
        
        # update tags
        self.Tags = tags


def _parmTemplate_getTagsObject( self ):
    """
    Author: Sean
    """
    return ParmTags( self )
setAttr( hou.ParmTemplate, "Tags", property( _parmTemplate_getTagsObject ), replace=False )

    







###########################################################################
################################## Group ##################################
###########################################################################
def _parm_getTagGroupPoints( self ):
    """
    Author: Sean
    """
    return self.ParmTemplate.Tags.GroupPoints

def _parm_setTagGroupPoints( self, state ):
    """
    Author: Sean
    """
    tmp = self.ParmTemplate
    tmp.Tags.GroupPoints = state
    tmp.apply()

setAttr( hou.Parm, 'TagGroupPoints', property( _parm_getTagGroupPoints, _parm_setTagGroupPoints ) )



def _parm_getTagGroupVertices( self ):
    """
    Author: Sean
    """
    return self.ParmTemplate.Tags.GroupVertices

def _parm_setTagGroupVertices( self, state ):
    """
    Author: Sean
    """
    tmp = self.ParmTemplate
    tmp.Tags.GroupVertices = state
    tmp.apply()

setAttr( hou.Parm, 'TagGroupVertices', property( _parm_getTagGroupVertices, _parm_setTagGroupVertices ) )



def _parm_getTagGroupEdges( self ):
    """
    Author: Sean
    """
    return self.ParmTemplate.Tags.GroupEdges

def _parm_setTagGroupEdges( self, state ):
    """
    Author: Sean
    """
    tmp = self.ParmTemplate
    tmp.Tags.GroupEdges = state
    tmp.apply()

setAttr( hou.Parm, 'TagGroupEdges', property( _parm_getTagGroupEdges, _parm_setTagGroupEdges ) )



def _parm_getTagGroupBreakpoints( self ):
    """
    Author: Sean
    """
    return self.ParmTemplate.Tags.GroupBreakpoints

def _parm_setTagGroupBreakpoints( self, state ):
    """
    Author: Sean
    """
    tmp = self.ParmTemplate
    tmp.Tags.GroupBreakpoints = state
    tmp.apply()

setAttr( hou.Parm, 'TagGroupBreakpoints', property( _parm_getTagGroupBreakpoints, _parm_setTagGroupBreakpoints ) )



def _parm_getTagGroupPrims( self ):
    """
    Author: Sean
    """
    return self.ParmTemplate.Tags.GroupPrims

def _parm_setTagGroupPrims( self, state ):
    """
    Author: Sean
    """
    tmp = self.ParmTemplate
    tmp.Tags.GroupPrims = state
    tmp.apply()

setAttr( hou.Parm, 'TagGroupPrims', property( _parm_getTagGroupPrims, _parm_setTagGroupPrims ) )












