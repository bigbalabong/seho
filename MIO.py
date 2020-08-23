'''
Tier: Base
'''

from .MVar import *




'''
hou.NodeTypeCategory        https://www.sidefx.com/docs/houdini/hom/hou/NodeTypeCategory.html
'''




###########################################################################
################################## Import #################################
###########################################################################

class Import( object ):

    """
    Author: Sean
    """

    @staticmethod
    def importFile( kwargs ):
        """
        Author: Sean
        """
        pane = kwargs['pane']
        cursor = kwargs['cursor']
        root = kwargs['root']
        filepath = kwargs['filepath']


        ext = os.path.splitext( filepath )[1]
        ext = ext.lower()
        

        if ext in ('.bgeo', '.fbx'):
            if root.childTypeCategory().Name == 'Sop':
                new_node = root.createNode( 'file' )
                new_node.P = cursor
                new_node._['file']._ = filepath
        

        elif ext == '.abc':
            if root.childTypeCategory().Name == 'Sop':
                new_node = root.createNode( 'alembic' )
                new_node.P = cursor
                new_node._['fileName']._ = filepath
                new_node.Out0 >> ( 'convert' )


        # elif ext == '.fbx':
        #     if root.childTypeCategory().Name == 'Sop':
        #         new_node = root.createNode( 'labs::fbx_archive_import' )
        #         new_node.P = cursor
        #         new_node['sFBXFile'].Value = filepath


        elif ext in ('.exr', '.jpg', '.png'):
            pass



        elif ext in ('.mp3', ):
            if root.childTypeCategory().Name == 'Chop':
                new_node = root.createNode( 'file' )
                new_node.P = cursor
                new_node._['file']._ = filepath
        


        elif ext == '.hip':
            hou.hipFile.load( hou.expandString( filepath ) )








###########################################################################
################################## Export #################################
###########################################################################

# def _exportROP( func ):

#     def wrapper( *args, **kwargs ):

#         result = func( *args, **kwargs )

#         return result

#     return wrapper


def exportABC( self, fitFrameRange=False ):
    """
    Author: Sean
    """
    # root = self.root
    parent = self.parent()


    if self.type().category().name() == 'Sop':

        # get existing rop / create a new one
        abc_rop = [ i for i in self.outputs() if i.type().name() == 'rop_alembic' ]
        if abc_rop:
            abc_rop = abc_rop[0]
        else:
            abc_rop = self.createOutputNode( 'rop_alembic', self.name() + '__abc' )
            abc_rop.setPosition( self.position() + n_posX + n_posY )


        # set parms
        abc_rop.parm('use_sop_path').set( True )
        abc_rop.parm('sop_path').set( self.path() )        


    else:

        # get rop / create a new one
        rop_context = parent.node( 'ropnet' )
        if not rop_context:
            rop_context = newContexts( parent, ('rop',) )[0]

        abc_rop = rop_context.node( self.name() + '__abc' )
        if not abc_rop:
            abc_rop = rop_context.createNode( 'alembic', self.name() + '__abc' )


        # set parms
        abc_rop.parm('root').set( self.path() )
        abc_rop.inBox( 'abc', moveable = True )



    # set parms
    abc_rop.setUserData( 'source', self.path() )
    abc_rop.parm('filename').set( '$HIP/{}.abc'.format( self.name() ) )

    if fitFrameRange:
        frameRange_start, frameRange_end = self.getFrameRange()

        if frameRange_start != frameRange_end:

            abc_rop.parm('trange').set( 1 )

            abc_rop.parm('f1').deleteAllKeyframes()
            abc_rop.parm('f1').set( frameRange_start )

            abc_rop.parm('f2').deleteAllKeyframes()
            abc_rop.parm('f2').set( frameRange_end )



    # export
    abc_rop.render()


    return abc_rop
setAttr( hou.SopNode, 'exportABC', exportABC )


# @_exportROP
# def exportFBX( self ):
#     return




