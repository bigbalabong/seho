'''
Tier: Base
'''

from ..MVar import *


Gallery_Path = normpath( __file__, '../../../../../gallery', check=False )






###########################################################################
################################# Gallery #################################
###########################################################################
'''
hou.galleries                                 http://www.sidefx.com/docs/houdini/hom/hou/galleries.html
hou.Gallery                                   https://www.sidefx.com/docs/houdini/hom/hou/Gallery.html
Edit Node Gallery Entry window                https://www.sidefx.com/docs/houdini/ref/windows/savetogallery.html
Tool Palette                                  https://www.sidefx.com/docs/houdini/ref/panes/toolpalette.html

oppresetls                                    https://www.sidefx.com/docs/houdini/commands/oppresetls.html
oppresetload                                  https://www.sidefx.com/docs/houdini/commands/oppresetload.html
oppresetsave                                  https://www.sidefx.com/docs/houdini/commands/oppresetsave.html
'''

def _node_getGalleries( self ):
    '''
    Returns:
            All galleries.

    Author: Sean
    '''
    galleries = hou.galleries.galleryEntries( node_type = self.Type )
    galleries = list( galleries )
    
    for i in galleries:
        setAttr( i, 'Node', self )

    return galleries
setAttr( hou.Node, "Galleries", property( _node_getGalleries ) )



def _node_getPresets( self ):
    '''
    Returns:
            All galleries and presets. (because gallery is not a good name, so use preset as function name here.)
    
    Author: Sean
    '''
    # get presets
    presets = [ i.split('\n') for i in hou.hscript( 'oppresetls {}'.format( self.Path ) ) if i ]
    presets = L_( presets ).sum()
    presets = [ i.strip() for i in presets ]
    presets = [ i for i in presets if i ]

    # get galleries
    galleries = self.Galleries

    return presets + galleries
setAttr( hou.Node, "Presets", property( _node_getPresets ) )


def _node_getPresetNames( self ):
    """
    Author: Sean
    """
    presets_n_galleries = self.Presets

    presets = [ i for i in presets_n_galleries if isinstance( i, str ) ]

    galleries = [ i.Name for i in presets_n_galleries if not isinstance( i, str ) ]

    presets_n_galleries = presets + galleries
    presets_n_galleries.sort( lambda x: x.lower() )

    return presets_n_galleries
setAttr( hou.Node, "PresetNames", property( _node_getPresetNames ) )


def _node_getPresetLabels( self ):
    """
    Author: Sean
    """
    presets_n_galleries = self.Presets

    presets = [ i for i in presets_n_galleries if isinstance( i, str ) ]

    galleries = [ i.Label for i in presets_n_galleries if not isinstance( i, str ) ]

    presets_n_galleries = presets + galleries
    presets_n_galleries.sort( lambda x: x.lower() )

    return presets_n_galleries
setAttr( hou.Node, "PresetLabels", property( _node_getPresetLabels ) )




def _node_usePreset( self, preset_name ):
    """
    Author: Sean
    """
    preset_name = preset_name.lower()

    presets_n_galleries = self.Presets
    presets = [ i for i in presets_n_galleries if isinstance( i, str ) ]
    galleries = [ i for i in presets_n_galleries if not isinstance( i, str ) ]


    # ~~~~~~~~~~~ build presets dict ~~~~~~~~~~ #
    presets_dictItems = [ (i.lower(), i) for i in presets ]
    galleries_dictItems = L_([ ( (i.Name.lower(), i), (i.Label.lower(), i) ) for i in galleries ]).sum()
    presets_dict = dict( presets_dictItems + galleries_dictItems )


    # ~~~~~~~~~~~~~~ apply preset ~~~~~~~~~~~~~ #
    preset = presets_dict.get( preset_name )
    if preset:

        # apply gallery
        if type( preset ) is hou.GalleryEntry:
            preset.apply()

            # record
            self.UserData.add( 'preset', preset.Name )

        # apply preset
        else:
            codes = 'oppresetload {} {}'.format( self.Path, preset )
            hou.hscript( codes )

            # record
            self.UserData.add( 'preset', preset )

    else:
        logging.error( "{} dosen't exist".format( preset_name ) )
setAttr( hou.Node, 'usePreset', _node_usePreset )


def _node_newGallery( self, name, label=None, categories=() ):
    """
    Author: Sean
    """
    name = name.lower().replace(' ', '_')


    # ~~~~~~~~~~~~~~ new gallery ~~~~~~~~~~~~~~ #
    filename = '{}__{}.gal'.format( self.Type.Cate.Name.lower(), self.Type.Fullame.lower().replace('::', '_') )
    filepath = os.path.join( Gallery_Path, filename )

    new_gal = hou.galleries.createGalleryEntry( filepath, name, self )


    if label:
        new_gal.Label = label

    if categories:
        new_gal.Cates = categories

    return new_gal
setAttr( hou.Node, 'newGallery', _node_newGallery )


def _node_updateGallery( self ):
    """
    Author: Sean
    """
    # find the current gallery name in user data
    gal_name = self.userData('preset')

    if gal_name:
        gallery = hou.galleries.galleryEntries( name_pattern = gal_name, node_type = self.Type )

        if not gallery:
            print 'No gallery found.'
            return
        else:
            gallery = gallery[0]


    # find the current gallery name in comment
    else:   
        comment = [ i for i in self.comment().split('\n') if 'Created from Gallery Entry:' in i ]
        
        if not comment:
            print 'No gallery found.'
            return

        else:
            gal_name = comment[0].split(':',1)[1].strip().lower()

            galleries_dictItems = L_([ ( (i.Name.lower(), i), (i.Label.lower(), i) ) for i in self.Galleries ]).sum()
            galleries_dict = dict( galleries_dictItems )

            gallery = galleries_dict.get( gal_name )
            if not gallery:
                print 'No gallery found.'
                return

    
    #  update gallery by overriding the existing one  #
    name = gallery.Name
    label = gallery.Label
    categories = gallery.Cates

    new_gal = self.newGallery( name, label, categories )

    return new_gal
setAttr( hou.Node, 'updateGallery', _node_updateGallery )










###########################################################################
############################# hou.GalleryEntry ############################
###########################################################################
'''
hou.GalleryEntry                              https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html
'''

setAttr( hou.GalleryEntry, "Name", property( hou.GalleryEntry.name, hou.GalleryEntry.setName ) )
setAttr( hou.GalleryEntry, "Label", property( hou.GalleryEntry.label, hou.GalleryEntry.setLabel ) )

setAttr( hou.GalleryEntry, "Keywords", property( hou.GalleryEntry.keywords, hou.GalleryEntry.setKeywords ) )
setAttr( hou.GalleryEntry, "Desc", property( hou.GalleryEntry.description, hou.GalleryEntry.setDescription ) )

setAttr( hou.GalleryEntry, "Icon", property( hou.GalleryEntry.icon, hou.GalleryEntry.setIcon ) )
setAttr( hou.GalleryEntry, "Help", property( hou.GalleryEntry.helpURL, hou.GalleryEntry.setHelpURL ) )

setAttr( hou.GalleryEntry, "Cates", property( hou.GalleryEntry.categories, hou.GalleryEntry.setCategories ) )


def _galEntry_apply( self ):
    """
    Author: Sean
    """
    self.applyToNode( self.Node )
setAttr( hou.GalleryEntry, 'apply', _galEntry_apply )







