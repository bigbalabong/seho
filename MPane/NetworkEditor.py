'''
Tier: Base
'''

from ..MVar import *





###########################################################################
############################## NetworkEditor ##############################
###########################################################################
'''
hou.NetworkEditor               https://www.sidefx.com/docs/houdini/hom/hou/NetworkEditor.html
'''

setAttr( hou.NetworkEditor, "Cursor", property( hou.NetworkEditor.cursorPosition ) )


# ~~~~~~~~~~ List Network Editors ~~~~~~~~~ #

def _netEditor_getAll():
    """
    Author: Sean
    """
    return [ i for i in hou.ui.paneTabs() if type(i) == hou.NetworkEditor ]
setAttr( hou.NetworkEditor, "getAll", staticmethod( _netEditor_getAll ) )




# ======================================================== #
# ======================= Navigate ======================= #
# ======================================================== #
def _netEditor_focus( self, nodes ):
    """
    Author: Sean
    """
    if not isSequence( nodes ):
        nodes = [nodes]

    # cd
    self.PWD = nodes[0].Parent


    # frame nodes
    nodegraphview.frameItems( self, nodes, True )


    # update selection
    hou.clearAllSelected()
    for i in nodes:
        i.Selected = True
setAttr( hou.NetworkEditor, "frameItems", _netEditor_focus, replace=False )
setAttr( hou.NetworkEditor, "focus", _netEditor_focus, replace=False )







# custom get network pane
def getNetworkPane( node=None, floating=False ):
    """
    Author: Sean
    """

    # all network panes
    editors = [ i for i in hou.ui.currentPaneTabs() if isinstance(i, hou.NetworkEditor) ]
    editors = editors if not floating else [ i for i in editors if i.isFloating() ]

    # filtering by specific node
    editors_filtered = [ i for i in editors if node in [i.pwd()] + list(i.pwd().children()) ] if node else []

    # if no one matched, return the first network editor
    if editors_filtered.__len__() == 0:
        editor = editors[0]
    
    # if only one matched, return the chosen one
    elif editors_filtered.__len__() == 1:
        editor = editors_filtered[0]

    # if multiple matched, return the one under cursor.
    # if the panetab under cursor is not network editor, return the first matched in the above filtered list
    elif editors_filtered.__len__() >= 2:
        editor_underCursor = hou.ui.paneTabUnderCursor()

        editors_filtered.reverse()
        editors_filtered.sort( key = lambda x: int(bool( x == editor_underCursor )) )

        editor = editors_filtered[-1]

    # this could never happen
    else:
        editor = None


    return editor


def _parmEditor_openParm( node, pos=() ):
    """
    Open a floating parameter pane for input node.

    Args:
        node (hou.Node): [description]
        pos ((int, int), optional): Window position. Defaults to (). 
                                    Create new floating panetab at defaut position.

    Returns:
        [hou.PaneTab]: [description]
    
    Author: Sean
    """

    if isinstance( pos, hou.Vector2 ):
        pos = ( int(pos.x()), int(pos.y()) )
    

    # create new floating panetab
    pane_tab = hou.ui.curDesktop().createFloatingPaneTab( hou.paneTabType.Parm, pos )
    pane_tab.setCurrentNode( node )
    pane_tab.setPin( True )

    return pane_tab
setAttr( hou.ParameterEditor, "open", staticmethod( _parmEditor_openParm ) )


def openParmPaneHotkey():
    """
    Author: Sean
    """
    pass


def boundOfNodes( nodes ):
    '''
    return:
            corner_min  --  lower left corner
            corner_max  --  upper right corner
    
    Author: Sean
    '''

    pos_list = [ i.position() for i in nodes ]
    for node in nodes:
        if node.__class__.__name__ in ['StickyNote', 'NetworkBox']:
            pos_list.append( node.position() + node.restoredSize() )

    pos_list = zip( *pos_list )
    corner_min = hou.Vector2( min(pos_list[0]), min(pos_list[1]) )
    corner_max = hou.Vector2( max(pos_list[0]), max(pos_list[1]) )
    return corner_min, corner_max





# ======================================================== #
# =================== Background Image =================== #
# ======================================================== #
'''
References:
    Set screenshot as network background (linux)
    https://berniebernie.fr/wiki/Houdini_Python_Temp

    NetworkImage
    https://forums.odforce.net/topic/32581-networkimage/
'''
'''
BUG:
    hou.NetworkEditor.setBackgroundImages
        This method will not chagne user data dict of the node,
        which means the updated background images will be restored to the old ones,
        when you open the scene next time.
        So, you need to modify the user data dict manually to chagne the background images actually.
'''

def _networkEditor_getBGImages( self ):
    """
    Returns:
        [tuple of hou.NetworkImage / empty tuple]: [description]
    
    Author: Sean
    """
    images = self.backgroundImages()
    pwd = self.PWD

    for i in images:
        i.PWD = pwd

    return images
setAttr( hou.NetworkEditor, "BGImages", property( _networkEditor_getBGImages, hou.NetworkEditor.setBackgroundImages ) )

def _networkEditor_getAllBGImages( self ):
    """
    Don't use this method to get all background images.
    Use hou.Node.getAllBGImages instead.
    
    Author: Sean
    """
    # store pwd
    pwd = self.PWD


    # get all background images
    opened_networks = ROOT.AllOpenedNetworks

    images = ()
    for i in opened_networks:
        # update pwd to get bg images
        self.PWD = i
        images += self.BGImages


    # restore pwd
    self.PWD = pwd

    return images
# hou.NetworkEditor.AllBGImages = property( _networkEditor_getAllBGImages )
'''
Here is something strange:
    If define "AllBGImages" as class instance property, 
    when you type 'pane.' in houdini python shell, 
    the context menu will pop up, which contains all the properties and funcs of hou.NetworkEditor.
    At this time, "AllBGImages" will be executed.
    This shouldn't be happened.
    So, just define "getAllBGImages" as class instance method here.
'''
# hou.NetworkEditor.getAllBGImages = _networkEditor_getAllBGImages



'''
hou.NetworkImage        https://www.sidefx.com/docs/houdini/hom/hou/NetworkImage.html
NOTE:
        If you want to update background image, just setting path of hou.NetworkImage will not be enough.
        Cause hou.NetworkImage is just description.
        You must execute hou.NetworkEditor.setBackgroundImages to apply them.
'''

def _bgImage_getFilepath( self ):
    """
    Author: Sean
    """
    return hou.expandString( self.path() )
setAttr( hou.NetworkImage, "Path", property( _bgImage_getFilepath, hou.NetworkImage.setPath ) )
setAttr( hou.NetworkImage, 'Image', hou.NetworkImage.Path )

def _bgImage_getBasename( self ):
    """
    Author: Sean
    """
    return os.path.basename( self.Path )
setAttr( hou.NetworkImage, "Basename", property( _bgImage_getBasename ) )


# hou.NetworkImage.



setAttr( hou.NetworkImage, "Rect", property( hou.NetworkImage.rect, hou.NetworkImage.setRect ) )

setAttr( hou.NetworkImage, "Brightness", property( hou.NetworkImage.brightness, hou.NetworkImage.setBrightness ) )


setAttr( hou.NetworkImage, "Tied", property( hou.NetworkImage.relativeToPath, hou.NetworkImage.setRelativeToPath ) )
setAttr( hou.NetworkImage, 'Node', hou.NetworkImage.Tied )













###########################################################################
######################## Screenshot of Nodes Graph ########################
###########################################################################

# complement for menubar of network editor, help context info on the upper right corner of network editor. value in pixels
screenshotOfNetworkEditor_topMargin = 90

# as max_scale argument for setVisibleBounds function of NetworkEditor class
screenshotOfNetworkEditor_zoom = 110


def panNetworkEditor( editor, init_bound, screen_width, screen_height, row, column ):
    """
    Author: Sean
    """

    # initialize visiable bound as same as init_bound argument. in this way to keep init_bound variable intact for referencing repeatly
    visible_bound = hou.BoundingRect( init_bound.min(), init_bound.max() )

    # offset visible bound for current snapshot
    visible_bound.translate( hou.Vector2( screen_width * column, screen_height * row ) )

    # top margin complement
    visible_bound.translate( hou.Vector2( 0, editor.lengthFromScreen( screenshotOfNetworkEditor_topMargin )*row*-1 ) )

    # pan network editor
    editor.setVisibleBounds( visible_bound, max_scale=screenshotOfNetworkEditor_zoom, set_center_when_scale_rejected=True )


def workAreaSizeOfPrimaryMonitor():
    """
    Author: Sean
    """
    user32 = ctypes.windll.user32
    rect = ctypes.wintypes.RECT()
    user32.SystemParametersInfoA(48,0,rect,0)

    return ( rect.left, rect.top, rect.right, rect.bottom )


def screenshot( editor, file_path_temp, file_name, row, column ):
    """
    Author: Sean
    """

    # screen resolution of primary monitor excluding windows taskbar
    workArea_size = workAreaSizeOfPrimaryMonitor()

    # node graph resolution including menubar of network editor, help context info on the upper right corner of network editor. value in pixels
    panelContent_size = editor.contentSize()

    # snapshot
    im = PIL.ImageGrab.grab()

    # cut out windows taskbar 
    im = im.crop( workArea_size )

    # cut out edge margin (1 pixel), window title (e.g. Houdini FX - panel1), tab menubar (e.g. /obj/dopnet1/smokesolver1)
    # bound is from upper left corner to lower right corner
    im = im.crop( ( 1, im.size[1] - panelContent_size[1] + screenshotOfNetworkEditor_topMargin, im.size[0]-1, im.size[1] ) )

    # save snapshot as png file
    im.save('{}/{}row{}_collumn{}.png'.format( file_path_temp, file_name, row, column ))

    # cause using hdefereval.execute_deferred, it seems like that return statement won't work right.
    # return im


def mergeScreenshot( rows, columns, file_path_temp, file_path_final, file_name ):
    """
    Author: Sean
    """

    # collect screenshot image files
    screenshot_files =  [ '{}/{}'.format( file_path_temp, i ) for i in os.listdir( file_path_temp ) ]
    screenshot_files = [ i for i in screenshot_files if os.path.isfile(i) ]
    screenshot_files.sort()

    # screenshot_files_filtered = []
    # for screenshot in screenshot_files:
    #     if screenshot[-3:] == 'png':
    #         screenshot_files_filtered.append( screenshot )
    screenshot_files = [ i for i in screenshot_files if i[-3:] == 'png' ]
    screenshot_files = [ i for i in screenshot_files if file_name in i and 'nodeGraph' not in i ]



    images = [ PIL.Image.open( i ) for i in screenshot_files ]



    if not images:
        logging.error( 'No Screenshots Image Files Found !!' )
        return


    # get final resolution
    res_x_unit, res_y_unit = images[0].size
    res_x = res_x_unit * columns
    res_y = res_y_unit * rows


    # new image
    new_im = PIL.Image.new('RGB', (res_x, res_y))


    # merge screenshots
    for i in images:

        row_index, column_index = [ int(j) for j in i.filename.rsplit('.',1)[0].rsplit('row',1)[1].rsplit('_collumn',1) ]
        x_offset = res_x_unit * column_index
        y_offset = res_y - res_y_unit * (row_index + 1)

        new_im.paste( i, (x_offset, y_offset) )


    

    # crop edge margin
    upper_left_x = int(res_x_unit * 0.3)
    upper_left_y = int(res_y_unit * 0.0)
    lower_right_x = new_im.size[0] - int(res_x_unit * 0.3)
    lower_right_y = new_im.size[1] - int(res_y_unit * 0.3)

    new_im = new_im.crop( ( upper_left_x, upper_left_y, lower_right_x, lower_right_y ) )




    # save merged image as png file
    new_im.save( '{}/{}nodeGraph.png'.format( file_path_final, file_name ) )




    # delete screenshots
    for i in screenshot_files:
        os.remove( i )


def screenshotOfNetworkEditor():
    '''
    How to use:
            1. Tear off Pane Tab Copy. Hotkey: Alt+Shift+C
            2. Maximize the above new teared off floating Network Editor.
            3. Execute "Nodegraph Screenshot" function via Tab Menu of Network Editor.
                    Screeenshot image will be saved to Desktop.
    
    Author: Sean
    '''

    print '\n'*4
    print 'Taking Snapshot....'

    # get floating network editor
    editor = get_networkPaneTab( floating=True )

    if not editor:
        logging.error( 'No floating network editor found !!' )
        return



    if not editor.pwd().allItems():
        logging.error( 'No nodes in this Network Editor !!' )
        return



    # sreenshot file path, base name
    file_name = '{}_{}__'.format( hou.hipFile.basename(), editor.pwd().name() )
    file_path_temp = os.environ['TMP']
    file_path_final = os.path.join(os.environ['USERPROFILE'], 'Desktop')


    # get bound of node graph
    corner_min, corner_max = boundOfNodes( editor.pwd().allItems() )
    width = corner_max[0] - corner_min[0]
    height = corner_max[1] - corner_min[1]
    init_bound = hou.BoundingRect( corner_min[0], corner_min[1], corner_min[0]+1, corner_min[1]+1 )


    # pan and zoom network editor to initial position
    editor.setVisibleBounds( init_bound, max_scale=screenshotOfNetworkEditor_zoom, set_center_when_scale_rejected=True )


    # get resolution of visible network editor in network view coordinates
    panelContent_size = editor.contentSize()
    screen_width = editor.lengthFromScreen( panelContent_size[0] )
    screen_height = editor.lengthFromScreen( panelContent_size[1] )


    # planning screenshot tasks
    columns = int(math.ceil( width / screen_width ) ) + 1
    rows = int(math.ceil( height / screen_height )) + 1

    # complement
    rowsComplement_topMargin = int( round( editor.lengthFromScreen( screenshotOfNetworkEditor_topMargin ) * (rows-1) / screen_height ) )
    rows += rowsComplement_topMargin

    print( 'columns: ', columns, '  rows: ', rows, '  rows complement: ', rowsComplement_topMargin )


    # take screenshots block by block
    for j in range( rows ):
        for i in range( columns ):

            # pan network editor
            hdefereval.execute_deferred( panNetworkEditor, *[editor, init_bound, screen_width, screen_height, j, i] )

            # take screenshot
            hdefereval.execute_deferred( screenshot, *[ editor, file_path_temp, file_name, j, i ] )




    # merge all screenshots
    hdefereval.execute_deferred( mergeScreenshot, *[ rows, columns, file_path_temp, file_path_final, file_name ] )


    # pop up info
    hdefereval.execute_deferred( hou.ui.displayMessage, 'Screenshot Finished.' )














