'''
Tier: Base
'''

from ..MVar import *




def _netItem_getColor( self ):
    color = self.color()
    color.Item = self
    return color

def _netItem_setColor( self, color ):
    if type(color) is not hou.Color:
        color = hou.Color(color)

    self.setColor( color )

setAttr( hou.NetworkMovableItem, 'Color', property( _netItem_getColor, _netItem_setColor ) )




def _netItem_lightenColor( self ):
    color = hou.Vector3( self.color().rgb() )
    color *= 1.35
    color = hou.Color( color )
    self.setColor( color )
setAttr( hou.NetworkMovableItem, 'lightenColor', _netItem_lightenColor )


def _netItem_darkenColor( self ):
    color = hou.Vector3( self.color().rgb() )
    color *= 0.75
    color = hou.Color( color )
    self.setColor( color )
setAttr( hou.NetworkMovableItem, 'darkenColor', _netItem_darkenColor )




def _node_resetColor( self ):
    default_color = self.type().defaultColor()
    self.setColor( default_color )
    return default_color
setAttr( hou.Node, 'resetColor', _node_resetColor )




def colorByOccupation( nodes ):
    """
    WIP

    Args:
        nodes ([type]): [description]
    """

    top_nodestypes = {
        'data': ['csvinput', 'csvconcat', 'csvmodify', 'texttocsv', 'csvoutput', 'xmlinput', 'jsoninput', 'jsonoutput',
                 'sqlinput', 'sqloutput', ],
        'attrs': ['attributecopy', 'attributecreate', 'attributedelete', 'attributefromstring'],
        'wedge': [color_lib['yellow'], 'wedge'],
        'processor': ['hdaprocessor', 'invoke', ],
        'partition': [color_lib['gray'], 'partitionbyattribute', 'partitionbybounds', 'partitionbycombination',
                      'partitionbycomparison', 'partitionbyexpression', 'partitionbyframe', 'partitionbyindex',
                      'partitionbynode', 'partitionbyrange', 'partitionbytile', 'pythonpartitioner', 'waitforall'],
        'rop': [color_lib['green'], 'ropgeometry', 'ropalembic'],
        'render': [color_lib['cyan'], 'ropmantra', 'ropfetch'],
        'render_post': [color_lib['blue'], 'imagemagick', 'ropcomposite', 'ffmpegencodevideo', 'ffmpegextractimages'],
        'external': ['perforce', 'sendemail', 'shotguncreate', 'shotgundownload', 'shotgunfind', 'shotgunnewversion',
                     'shotgunsession', 'shotgunupdate', 'shotgunupload', 'commandserver', 'commandserverend',
                     'pythonscript', 'downloadfile', 'mayaserver'],
        'os': ['geometryimport', 'filepattern', 'filerename', 'filecopy', 'fileremove', 'filecompress',
               'filedecompress', 'makedir', ],
        'scheduler': ['localscheduler', 'hqueuescheduler', 'tractorscheduler', 'deadlinescheduler', 'pythonscheduler',
                      'houdiniserver', ],
        'net': ['objnet', 'sopnet', 'dopnet', 'chopnet', 'cop2net', 'vopnet', 'matnet', 'shopnet', 'ropnet',
                'subnet', ],
        'flow_control': ['switch', 'merge', 'split', 'workitemexpand', 'errorhandler', 'feedbackbegin', 'feedbackend',
                         'output', ],
        'others': ['environmentedit', 'filterbyexpression', 'genericgenerator', 'mapall', 'mapbyexpression',
                   'mapbyindex', 'mapbyrange', 'null', 'opnotify', 'pythonmapper', 'pythonprocessor', 'renderifd',
                   'sendcommand', 'topfetch', 'topfetchinput']}

    if not nodes:
        nodes = hou.selectedNodes()

    for each in nodes:
        for key in top_nodestypes.keys():
            if each.type().name() in top_nodestypes[key] and top_nodestypes[key][0].__class__.__name__ == 'Color':
                each.setColor(top_nodestypes[key][0])


class NodeColor( object ):

    @staticmethod
    def group( nodes=None, select=False ):
        """
        Slightly bias node color.

        Args:
            nodes (list of nodes): [description]
            select (bool): If true, select input nodes.
                            Default is False.
                            Easy-to-use. Colorring nodes and setting selected are 
                            two common operations in post-processing phase of many methods. 
        """
        if not nodes:
            nodes = hou.lss()

            if not nodes:
                return

        base_color = nodes[0].Color
        hue, saturation, value = base_color.HSV


        # get random num
        bias_ratio = 0.25
        rand_num = (random.random() *2 -1) * bias_ratio


        # update color
        hue += rand_num * 1.2 * 360
        hue = hue if hue <= 360 else hue - 360

        saturation += rand_num
        saturation = max( saturation, 0.15 )

        value += rand_num
        value = max( value, 0 )

        base_color.HSV = ( hue, saturation, value )

        # update node color
        for i  in nodes:
            i.Color = base_color


        # ~~~~~~~~~~~~~~~~~ Select ~~~~~~~~~~~~~~~~ #
        if select:
            hou.clearAllSelected()
            for i in nodes:
                i.Selected = True
setAttr( hou, 'NodeColor', NodeColor, replace=False )







