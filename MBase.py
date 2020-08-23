'''
Tier: Base


Conflicts:
        (solved) Crash on using Blend Pose Shelf Tool.
'''

from __future__ import print_function

import sys, os
import ctypes
import re
import logging
import math, random
import time

import PIL.ImageGrab

import sepy
reload(sepy)
p =                 sepy.p
type_ =             sepy.type_
I_ =                sepy.I_
F_ =                sepy.F_
S_ =                sepy.S_
L_ =                sepy.L_
D_ =                sepy.D_
Vec3 =              sepy.Vec3
isSequence =        sepy.isSequence
isClass =           sepy.isClass
setAttr =           sepy.setAttr
copyAttr =          sepy.copyAttr
hasAttr =           sepy.hasAttr
clear =             sepy.clear
Time =              sepy.Time
File =              sepy.File
Color =             sepy.Color
normpath =          sepy.normpath
declareMainVar =    sepy.declareMainVar
whatsTheTime =      sepy.whatsTheTime


import hou




import hdefereval

def executeDeferred(func):

    def wrapper(*args):
        result = hdefereval.execute_deferred(func, *args)
        return result

    return wrapper



import toolutils
setAttr( hou, 'getSceneViewer', toolutils.sceneViewer )
setAttr( hou, 'getNetworkEditor', toolutils.networkEditor )
setAttr( hou, 'layoutNodes', toolutils.moveNodesToGoodPosition )



import stateutils
# setAttr( hou, 'getSceneViewer', stateutils.findSceneViewer )


import nodegraphview 


# import loptoolutils           # C:\Program Files\Side Effects Software\Houdini 18.0.287\houdini\python2.7libs\loptoolutils.py
# import loputils               # C:\Program Files\Side Effects Software\Houdini 18.0.287\houdini\python2.7libs\loputils.py


'''
Houdini Third-party Libraries and Tools     http://www.sidefx.com/docs/houdini/licenses/index

Houdini Python Modules                      https://ikrima.github.io/houdini_additional_python_docs/index.html
'''






# ======================================================== #
# ========================= Undo ========================= #
# ======================================================== #
'''
hou.undos        http://www.sidefx.com/docs/houdini/hom/hou/undos.html
'''

def undoGroup( func ):

    def wrapper( *args, **kwargs ):

        with hou.undos.group( "Python Scripts." ):
            result = func( *args, **kwargs )

        return result

    return wrapper





# ======================================================== #
# ===================== Progress Bar ===================== #
# ======================================================== #
'''
hou.InterruptableOperation      http://www.sidefx.com/docs/houdini/hom/hou/InterruptableOperation.html
'''

# with hou.InterruptableOperation( "Performing", "Performing Tasks", open_interrupt_dialog=True ) as operation:
#     for i in range(5):
#         time.sleep(1)
#         operation.updateProgress(float(i)/5)






# ======================================================== #
# ========================= Cook ========================= #
# ======================================================== #
def updateModeToggle():
    '''
    Toggle cook mode between 'auto update' and 'manual'.

    Author: Sean
    '''
    mode = hou.updateModeSetting().name()

    if mode == 'AutoUpdate':
        hou.setUpdateMode( hou.updateMode.Manual )

    if mode == 'Manual':
        hou.setUpdateMode( hou.updateMode.AutoUpdate )




 

# ======================================================== #
# ======================== Select ======================== #
# ======================================================== #
def _ls():
    """
    Return the first selected.

    Author: Sean
    """
    sels = hou.selectedItems()
    if sels:
        return sels[0]
setAttr( hou, 'ls', _ls )

setAttr( hou, 'lss', hou.selectedItems )


def _select( items=None ):
    """
    Author: Sean
    """
    if items is None:
        return

    hou.clearAllSelected()

    for i in items:
        i.Selected = True
setAttr( hou, 'select', _select )








# ======================================================== #
# ========================= Node ========================= #
# ======================================================== #
class Node( object ):

    '''
    This custom class have some decorators for common manipulations about node or nodetype.

    Author: Sean
    '''

    @staticmethod
    def nodetype( nodetypes ):
        """
        If the nodetype of node instance is not one of the specified, stop execution.

        Args:
            nodetypes (list of hou.NodeType / list of str): 
                                The list of str is used to specify nodetypes manually.
                                The list of nodetypes is more suited to the results returned by hou.NodeType.getAll.
        """

        def decorator( func ):

            def wrapper( *args, **kwargs ):

                if args[0].Type not in nodetypes and args[0].Type.CateName not in nodetypes:
                    logging.error( 'Nodetype Error.' )
                    return

                result = func( *args, **kwargs )

                return result

            return wrapper

        return decorator


    @staticmethod
    def nodecate( categories ):
        '''
        If the category of this node instance is not one of the specified categories, stop execution.

        Args:
            categories (list of str)
        '''

        def decorator( func ):

            def wrapper( *args, **kwargs ):

                if args[0].Type.Cate.Name.upper() not in categories:
                    logging.error( 'Node Category Error.' )
                    return

                result = func( *args, **kwargs )

                return result

            return wrapper

        return decorator







# ======================================================== #
# ===================== Context Menu ===================== #
# ======================================================== #
def getMenuItemsOfCls( cls ):
    """
    Get list of menu items used to build context menu.

    Author: Sean
    """
    # get methods
    methods = [ i for i in dir(cls) if not i.startswith('_') and callable( getattr(cls, i) ) ]
    
    
    # get labels based on doc string
    labels = []
    for method in methods:
        func = getattr( cls, method )
        doc = func.__doc__
        
        if not doc:
            labels.append( method )
            continue

        label = [ i.strip() for i in doc.split('\n') if i ][0]
        labels.append(label)


    # methods = [ i.__name__ for i in methods ]


    # get menu items
    menu_items = zip( methods, labels )
    menu_items.sort( key=lambda x: x[1].lower() )
    # menu_items = L_(menu_items).sum()

    return menu_items









