'''
Tier: Base
'''


from .Base import *






# ======================================================== #
# ============== Blend Parms v1 (key-based) ============== #
# ======================================================== #

BlendParmsV1_Parm = '''ratio = ch('blendParms_ratio')
num = ch('blendParms_targets')
frame = hou.hmath.fit( ratio, 1, num, 1, (num-1)*{}+1 )
return hou.parm("{}").evalAtFrame( frame )
'''


BlendParmsV1_Targets = '''node = kwargs['node']
parm = kwargs['parm']
maximum = max( parm._, 2 )
node._['blendParms_ratio'].Max = maximum
'''


BlendParmsV1_ScopeAll = '''node = kwargs['node']
parm_tuples = [ i for i in node.ParmTuples if i.Name.endswith( '__blendKeys' ) ]
for parm_tuple in parm_tuples:
    for parm in parm_tuple.Parms:
        if parm.Keys:
            parm.Scoped = True
'''


BlendParmsV1_UpdateKeys = '''node = kwargs['node']
parms = [ i for i in node.Parms if i.Python and i.Python.startswith( "ratio = ch('blendParms_ratio')" ) ]
parms = hou.text.filter( parms, filters=hou.ch('blendParms_updateKeys_parmsScope') )
for parm in parms:
    menu = hou.Parm.ContextMenu_BlendParms( kwargs={ 'parms': (parm, ) } )
    menu._blendParms_v1_updateKeys()
'''


BlendParmsV1_RebuildKeys = '''node = kwargs['node']
parms = [ i for i in node.Parms if i.Python and i.Python.startswith( "ratio = ch('blendParms_ratio')" ) ]
parms = hou.text.filter( parms, filters=hou.ch('blendParms_rebuildKeys_parmsScope') )
for parm in parms:
    menu = hou.Parm.ContextMenu_BlendParms( kwargs={ 'parms': (parm, ) } )
    menu._blendParms_v1_buildKeys()
'''







# ======================================================== #
# =============== Blend Parms v3 (vex-based) ============= #
# ======================================================== #

BlendParmsV2_Parm = '''node = pwd().node( ch('blendParms_ctrl') ).Output0
attr = 'parm_{}_value'.format( hou.evaluatingParm().Name )
return node.Geo[ attr ]
'''


BlendParmsV2_Targets = '''node = kwargs['node']
#parm = kwargs['parm']
#grp = parm.InstanceGrpsJustBorn
#justBorn_parm = grp[0]

# update maximum of ratio slider
ratio_tmp = node._['ratio'].ParmTemplate
ratio_tmp.Max = max( kwargs['parm']._, 2 )
ratio_tmp.apply()

#justBorn_parm._ = False
'''


BlendParmsV2_PosEnableAll = '''node = kwargs['node']
posEnable_parms = [ i[2] for i in node._['targets'].InstanceGrps ]
for i in posEnable_parms:
    i._ = True
'''

BlendParmsV2_PosDisableAll = '''node = kwargs['node']
posEnable_parms = [ i[2] for i in node._['targets'].InstanceGrps ]
for i in posEnable_parms:
    i._ = False
'''

BlendParmsV2_PosEvenlySpaced = '''node = kwargs['node']
pos_parms = [ i[3] for i in node._['targets'].InstanceGrps if i[2]._ ]

num = len( pos_parms )
start = pos_parms[0]._
end = pos_parms[-1]._
step = (end - start) / (num -1)

for i, pos_parm in enumerate( pos_parms[1:-1] ):
    pos_parm._ = start + step * (i +1)
'''

BlendParmsV2_PosAutoCorrect = '''node = kwargs['node']
pos_parms = [ i[3] for i in node._['targets'].InstanceGrps if i[2]._ ]

# the position of latter target should not be smaller than 
# the former one for this kind of sequentially blending.

threshold = 0.05
start = pos_parms[0]._

for i, pos_parm in enumerate( pos_parms[1:] ):
    val = pos_parm._
    pre_val = pos_parms[i]._
    if val - pre_val < threshold:
        pos_parm._ = pre_val + threshold
'''


BlendParmsV2_PosOffset = '''node = kwargs['node']

# get current parm
parm = kwargs['parm']
value = parm._

# get active position parms in instances of multi-parm targets
pos_parms = [ i[3] for i in node._['targets'].InstanceGrps if i[2]._ ]

# tweak value of position parms simultaneously
for pos_parm in pos_parms:
    pos_parm._ += value

# reset current parm value
parm._ = 0
'''


BlendParmsV2_VisEnable = '''node = kwargs['node']
parm = kwargs['parm']
if parm._:
    node.Output0.Template = True
'''


BlendParmsV2_PythonCtrl = '''# store related info in detal attrs 
node = hou.pwd()
geo = node.geometry()

# get instance groups of multi-parm targets
grps = hou.parm('targets').InstanceGrps

# get target nodes
targets = [ i[1].toNode() for i in grps ]
num = len(targets)

# get positions of keys
pos = [ i[3]._ for i in grps ]
geo.newDetailAttr( 'pos', pos )

# get parms values
parms = node._['parms'].toList()
for parm in parms:
    attr = 'parm_{}'.format( parm )
    values = [ i._[parm]._ for i in targets ]
    geo.newDetailAttr( attr, values )
    
# which detail attrs are storing parm values
parms = [ 'parm_{}'.format( i ) for i in parms ]
geo.newDetailAttr( 'parms', parms )

# get basis
geo.newDetailAttr( 'basis', hou.ch('basis') )

# get ratio
ratio = hou.ch('ratio')
ratio = (ratio -1) / (num -1)
geo.newDetailAttr( 'ratio', ratio )


# ~~~~~~~~~~~~~~ visulization ~~~~~~~~~~~~~ #
geo.newDetailAttr( 'vis_enable', hou.ch('vis_enable') )

# which detail attrs should be visualized
vis_parms = [ 'parm_{}'.format( i ) for i in node._['vis_parms'].toList() ]
geo.newDetailAttr( 'vis_parms', vis_parms )

geo.newDetailAttr( 'vis_steps', hou.ch('vis_steps') )
'''


BlendParmsV2_VEX = '''
int num;
float pos[], values[], ratio, value;
string parms[], basis, bases[];

int vis_enable, vis_index, vis_steps, vis_pnt, vis_pnts[];
float vis_ratio, vis_ratios[], vis_value, vis_values[], vis_valuesAbs[], vis_max;
vector vis_P, vis_Ps[];
string vis_parms[];


// get basic info
parms = detail(0, 'parms');

pos = detail(0, 'pos');
num = len(pos);

ratio = detail(0, 'ratio');

basis = detail(0, 'basis');
for( int i=0; i<num; i++ ) push( bases, basis );


// get visualization info
vis_enable = detail(0, 'vis_enable');

vis_parms = detail(0, 'vis_parms');

vis_steps = detail(0, 'vis_steps');


// calculate interpolation
foreach( string parm; parms ){
    values = detail(0, parm);
    value = spline( bases, ratio, values, pos );
    setdetailattrib( 0, parm + '_value', value, 'set' );
    
    
    // visulization
    if( vis_enable == 1 ){
        vis_index = find( vis_parms, parm );
        if( vis_index >= 0 ){
            vis_ratios = {};
            vis_values = {};
            vis_valuesAbs = {};
            vis_pnts = {};
            
            for( int i=0; i < vis_steps; i++ ){
                vis_ratio = float(i) / (vis_steps -1);
                push( vis_ratios, vis_ratio );
                
                vis_value = spline( bases, vis_ratio, values, pos );
                push( vis_values, vis_value );
                push( vis_valuesAbs, abs(vis_value) );
            }
            
            vis_max = max( vis_valuesAbs );

            // create points for interpolation
            foreach( int i; float val; vis_values ){
                // normalize ratio
                vis_ratio = vis_ratios[i] *2 + vis_index *3;
                // normalize value
                val = val / vis_max *-1;
                // get point position
                vis_P = set( vis_ratio, 0, val );
                // new point
                push( vis_pnts, addpoint( 0, vis_P ) );
            }
            
            // create points for key poisitions
            foreach( int i; float P; pos ){
                vis_P = set( P *2 + vis_index *3, 0, values[i] / vis_max *-1 );
                vis_pnt = addpoint( 0, vis_P );
                setpointattrib( 0, 'Cd', vis_pnt, {1,0,0}, 'set' );
                setpointgroup( 0, 'vis_keys', vis_pnt, 1, 'set' );
            }
        }
    }
}
'''




class ContextMenuParm_BlendParms( ContextMenuParm ):

    """
    Author: Sean
    """

    def __init__( self, kwargs ):
        super( ContextMenuParm_BlendParms, self ).__init__( kwargs )


    @property
    def MenuItems_BlendParms( self ):
        """
        Get menu items "Blend Parms".

        Author: Sean
        """
        items = [ i for i in self.MenuItems_All if i[0].startswith( 'blendParms_' ) ]
        items = L_(items).sum()
        return items


    BlendParms_Vars = {
            'keys_gap':     20,
            'label_width':  20,
        }




    ###########################################################################
    ################# Sequentially Blend Parms v1 (key-based) #################
    ###########################################################################
    def blendParms_v1_blend( self ):
        """
        v1 Blend (key-based)

        Author: Sean
        """
        node = self.Node

        # existence check
        if not node._['blendParms_folder']:
            targets = node.selectNodes( filter_same_nodetype=True )
            self._blendParms_v1_init( targets )
        

        # this duplicated parm template is used to store keyframes.
        self.Parm.duplicate( 
                            name_suffix = '__blendKeys',
                            label_suffix = ' (Blend Keys)',
                            hidden = True,
                            auto_rename = False,
                        )


        # build keys and set parm referencing
        self._blendParms_v1_buildKeys()


    def _blendParms_v1_init( self, nodes=None ):
        """
        Add spare parameters.

        Author: Sean
        """
        node = self.Node
        label_width = self.BlendParms_Vars['label_width']


        node.addSpareFolder()
        folder = node.addFolder( 'blendParms_folder', 'Blend Parameters', spare_folder=True )



        # ======================================================== #
        # ======================= new parms ====================== #
        # ======================================================== #

        # ~~~~~~~~~~~~~~~~ targets ~~~~~~~~~~~~~~~~ #
        target = node.addStr( 'blendParms_target#', 'Target #', add=False )

        targets = node.addMultiParm( 
                                    'blendParms_targets', 'Targets', 
                                    parm_templates = (target,), 
                                    callback = BlendParmsV1_Targets,
                                    folder = folder,
                                )
        targets = node._[ targets.Name ]

        if nodes:
            targets._ = len(nodes)
            for target_parm, target_node in zip( targets.Instances, nodes ):
                target_parm._ = target_node


        # ~~~~~~~~~~~~~~ blend ratio ~~~~~~~~~~~~~~ #
        maximum = len(nodes) if nodes else 2
        maximum = max( maximum, 2 )
        ratio = node.addFlt( 
                            'blendParms_ratio', 'Blending Ratio', 
                            initial = 1, value_range = (1, maximum), 
                            folder = folder  
                        )


        # ~~~~~~~~~~~~~~~~~~ sep ~~~~~~~~~~~~~~~~~~ #
        node.addSep( folder=folder )


        # ~~~~~~~~~~~~~~ scope button ~~~~~~~~~~~~~ #
        node.addBtn( 
                        'blendParms_scope', 'Scope Intermediate Parms', 
                        callback = BlendParmsV1_ScopeAll, 
                        folder = folder 
                    )


        # ~~~~~~~~~~~~ expression menu ~~~~~~~~~~~~ #
        node.addStr( 
                        'blendParms_keyExpr', 'Key Expression', 
                        default = ('linear()',),
                        menu_items = zip( hou.Keyframe.Expressions, hou.Keyframe.Expressions ),  
                        folder = folder,
                    )


        # ~~~~~~~~~~~~ update keyframes ~~~~~~~~~~~ #
        label = S_( 'Update Keys' ).mjust( label_width )
        node.addBtn( 
                        'blendParms_updateKeys', label, 
                        callback = BlendParmsV1_UpdateKeys, 
                        join_with_next = True, 
                        folder = folder 
                    )

        node.addStr( 'blendParms_updateKeys_parmsScope', 'Parms', label_hidden=True, default=('*',), folder=folder )


        # ~~~~~~~~~~~ rebuild keyframes ~~~~~~~~~~~ #
        label = S_( 'Rebuild Keys' ).mjust( label_width )
        node.addBtn( 
                        'blendParms_rebuildKeys', label, 
                        callback = BlendParmsV1_RebuildKeys, 
                        join_with_next = True, 
                        folder = folder 
                    )

        node.addStr( 'blendParms_rebuildKeys_parmsScope', 'Parms', label_hidden=True, default=('*',), folder=folder )


    def _blendParms_v1_buildKeys( self ):
        """
        Build keys on intermediate parms.

        Author: Sean
        """
        node = self.Node
        targets = self._blendParms_v1_getTargets()
        key_expr = node._['blendParms_keyExpr']._        
        keys_gap = self.BlendParms_Vars['keys_gap']


        for parm in self.Parms:
            double_parm = self._blendParms_v1_getDoubleParm( parm )
        
            # ~~~~~ build keys on intermediate parm ~~~~~ #
            keys = []
            for i, target in enumerate( targets ):
                # if multi-parm instance string parm is empty, target will be None
                if not target:
                    continue

                value = target._[parm.Name]._
            
                # new key
                key = hou.Keyframe()
                key.Frame = i * keys_gap + 1
                key.Value = value
                key.HScript = key_expr
                
                keys.append( key )

            double_parm.deleteAllKeyframes()
            double_parm.Keys = keys
            

            # set parm refercing
            parm.Python = BlendParmsV1_Parm.format( keys_gap, double_parm.Name )    


    def _blendParms_v1_updateKeys( self ):
        """
        Update keys on intermediate parms.
        Only values of keys will be matched to the values of parms on targets.
        The timing and expression will be left untouched.

        Author: Sean
        """
        node = self.Node
        targets = self._blendParms_v1_getTargets()
        targets = [ i for i in targets if i ]


        # ~~~~ update keys on intermediate parm ~~~ #
        update_failed = []
        for parm in self.Parms:
            double_parm = self._blendParms_v1_getDoubleParm( parm )
            keys = double_parm.Keys

            # if keys on the intermediate parm were not edited (add / delete) by user manually,
            # the num of keys and targets is always same.
            if len(keys) != len(targets):
                update_failed.append( parm )
                continue


            # update values of keys
            for key, target in zip( keys, targets ):

                key.Value = target._[parm.Name]._


            # update keys
            double_parm.Keys = keys


        # ~~~~~~~~~~~~ post-processing ~~~~~~~~~~~~ #
        if update_failed:
            print( 'Parms updated faield:  {}'.format( ', '.join( [ i.Name for i in update_failed ] ) ) )


    def blendParms_v1_clear( self ):
        """
        v1 Clear

        Author: Sean
        """
        parm = self.Parm

        # clear expression
        for parm in self.Parms:
            parm.deleteAllKeyframes()


        # destory parm template
        working_parms = [ i for i in parm.ParmTuple.Parms if i.Python and i.Python.startswith( "ratio = ch('blendParms_ratio')" ) ]
        if not working_parms:
            double_parm = self._blendParms_v1_getDoubleParm( parm )
            tmp = double_parm.ParmTemplate
            tmp.destroy()


    def blendParms_v1_scope( self ):
        """
        v1 Scope Intermediate Parameters.

        Author: Sean
        """
        for parm in self.Parms:
            double_parm = self._blendParms_v1_getDoubleParm( parm )
            double_parm.Scoped = True


    def _blendParms_v1_getTargets( self ):
        node = self.Node
        targets = [ i.toNode() for i in node._['blendParms_targets'].Instances ]
        return targets


    def _blendParms_v1_getDoubleParm( self, parm ):
        """
        Get intermediate parm storing keys.

        Args:
            parm (hou.Parm): [description]

        Returns:
            [hou.Parm]: [description]

        Author: Sean
        """
        double_parmTuple = parm.Node.parmTuple( parm.ParmTuple.Name + '__blendKeys' )
        double_parm = double_parmTuple[ parm.Index ]
        return double_parm







    ###########################################################################
    ################## Sequentially Blend Parms v3 (vex-based) ################
    ###########################################################################
    '''
    spline      https://www.sidefx.com/docs/houdini/vex/functions/spline.html
    '''

    def blendParms_v2_blend( self ):
        """
        v2 Blend (vex-based)

        Author: Sean
        """
        node = self.Node


        # ======================================================== #
        # ==================== existence check =================== #
        # ======================================================== #
        ctrl_parm = node._['blendParms_ctrl']
        # if parm dosn't exist or nodepath is invalid
        if not ctrl_parm or not node.node( ctrl_parm._ ):
            # select nodes with same type
            targets = node.selectNodes( filter_same_nodetype=True )

            # initialize parms
            self._blendParms_v2_init( targets )



        # ======================================================== #
        # ====================== setup parms ===================== #
        # ======================================================== #
        # add parms
        ctrl_node = node.node( node._['blendParms_ctrl']._ )
        parm_names = ctrl_node._['parms'].toList()

        for parm_name in [ i.Name for i in self.Parms ]:
            if parm_name not in parm_names:
                parm_names.append( parm_name )

        ctrl_node._['parms']._ = ' '.join( parm_names )


        # set expression
        for parm in self.Parms:
            # parm.Python = BlendParmsV2_Parm
            parm.HScript = "detail( '{}', '{}', 0 )".format( 
                                                        node._['blendParms_result']._,  
                                                        'parm_{}_value'.format( parm.Name ),
                                                    )


    def _blendParms_v2_init( self, nodes=None ):
        """
        Add spare parameters.

        Author: Sean
        """
        node = self.Node
        label_width = self.BlendParms_Vars['label_width']


        # ======================================================== #
        # ==================== existence check =================== #
        # ======================================================== #
        blendParms_ctrl = node._['blendParms_ctrl']
        blendParms_result = node._['blendParms_result']
        # if parm dosn't exist
        if not blendParms_ctrl:
            node.addSep()
            blendParms_ctrl = node.addStr( 
                                            'blendParms_ctrl', 'Blend Parms', 
                                            string_type = 'node', 
                                            as_parm = True,
                                        )
            blendParms_result = node.addStr( 
                                            'blendParms_result', 'Result', 
                                            string_type = 'node', 
                                            as_parm = True,
                                        ) 
        


        # ======================================================== #
        # ===================== create nodes ===================== #
        # ======================================================== #
        newbies = []

        # get root node based on context
        cate = node.Type.Cate.Name
        if cate == 'Sop':
            root = node.Parent

        elif cate == 'Object':
            root = node.Parent.createNode( 'geo', 'blend_parms' )
            newbies.append( root )
            root.P = node.P + nPx
        
        elif cate == 'Vop':
            root = hou.node('/obj').createNode( 'geo', 'blend_parms' )
            newbies.append( root )
        
        else:
            net = node.Parent.createNode( 'objnet', 'blend_parms' )
            newbies.append( net )
            net.P = node.P + nPx

            root = net.createNode( 'geo', 'blend_parms' )
            newbies.append( root )
        

        # new python sop
        python_sop = root.createNode( 'python', 'blendParms_ctrl' )
        newbies.append( python_sop )
        python_sop.P = node.P + nPx
        python_sop._['python']._ = BlendParmsV2_PythonCtrl
        

        # new wrangle sop
        wrangle_sop = python_sop.Out0 >> ( 'attribwrangle', 'blendParms_interpolation' )
        newbies.append( wrangle_sop )
        wrangle_sop.P = python_sop.P + nPy
        wrangle_sop._['class']._ = 'detail'
        wrangle_sop._['snippet']._ = BlendParmsV2_VEX
        wrangle_sop._['vex_selectiongroup']._ = 'vis_keys'


        # set node color
        hou.NodeColor.group( newbies )
        

        # record nodepath
        blendParms_ctrl._ = python_sop
        blendParms_result._ = wrangle_sop




        # ======================================================== #
        # ====================== setup nodes ===================== #
        # ======================================================== #

        # all the subsequent spare parms will be added before this seperator
        spare_sep = python_sop.addSep( 'spare_sep', insert_at_top=True )


        # record base node
        base_node_parm = python_sop.addStr( 
                                            'base_node', 'Base Node', 
                                            string_type = 'node', 
                                            as_parm = True, 
                                            insert_before = spare_sep, 
                                        )
        base_node_parm._ = node

        python_sop.addSep( insert_before=spare_sep  )


        # calculate interpolation for these parms
        python_sop.addStr( 'parms', 'Parameters', insert_before=spare_sep  )



        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # ~~~~~~~~~~~~~~~ Visualize ~~~~~~~~~~~~~~~ #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        visEnable_tmp = python_sop.addToggle( 
                                'vis_enable', 
                                label_hidden = True, 
                                default = False, 
                                callback = BlendParmsV2_VisEnable,
                                join_with_next = True,
                                add = False,
                            )

        visParms_tmp = python_sop.addStr( 
                                'vis_parms', 'Visualize', 
                                expr = ( "chs('parms')", ),
                                join_with_next = True,
                                add = False,
                            )
        
        visSteps_tmp = python_sop.addInt( 
                                'vis_steps', 'Steps', 
                                default=(50,), value_range = (4, 100),
                                add = False,
                            )

        # onnly if add these three parm templates together like below,
        # the argv "join_with_next" will work.
        grp = python_sop.ParmTemplateGrp
        for i in ( visEnable_tmp, visParms_tmp, visSteps_tmp ):
            grp.insertBefore( spare_sep, i )
        grp.apply()


        python_sop.addSep( insert_before=spare_sep )



        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # ~~~~~~~~~~~~~~~~ targets ~~~~~~~~~~~~~~~~ #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # target nodepath
        target_tmp = python_sop.addStr( 'target#', 'Target #', add=False )

        # if enabled, you could tweak position using the parms in the below folder called 'Position'
        targetP_offsetEnable_tmp = python_sop.addToggle( 
                                                        'targetP_offsetEnable#',
                                                        default = False,
                                                        label_hidden = True,
                                                        join_with_next = True, 
                                                        add = False,  
                                                    )

        # position of key
        targetP_tmp = python_sop.addFlt( 'targetP#', 'Positon', add=False, )

        # multi-parm including the above three parm templates
        targets_parm = python_sop.addMultiParm( 
                                            'targets', 'Targets', 
                                            parm_templates = ( 
                                                                target_tmp, 
                                                                targetP_offsetEnable_tmp, 
                                                                targetP_tmp, 
                                                            ), 
                                            extra_justBorn = True,
                                            callback = BlendParmsV2_Targets,
                                            insert_before = spare_sep,
                                            as_parm = True,
                                        )

        if nodes:
            num = len(nodes)
            targets_parm._ = num
            for i, grp in enumerate( targets_parm.InstanceGrps ):
                justBorn_parm, target_parm, pos_offsetEnable, pos_parm = grp
                target_node = nodes[i]
                
                # set nodepath
                target_parm._ = target_node

                # set position of key
                pos_parm._ = float(i) / (num -1)



        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # ~~~~~~~~~~~~ position offset ~~~~~~~~~~~~ #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # for convenience of tweaking positions of keys

        posOffset_tmp = python_sop.addFlt( 
                                    'pos_offset', 'Offset', 
                                    value_range = (-0.1, 0.1), 
                                    callback = BlendParmsV2_PosOffset, 
                                    add = False,
                                )

        width_1 = 10
        width_2 = 30

        btn_label = 'Enable All'
        btn_label = S_(btn_label).mjust( width_1 )
        posBtn1_tmp = python_sop.addBtn( 
                                    'pos_offsetEnableAll', btn_label, 
                                    callback = BlendParmsV2_PosEnableAll,
                                    join_with_next=True, 
                                    add=False 
                                )

        btn_label = 'Disable All'
        btn_label = S_(btn_label).mjust( width_1 )
        posBtn2_tmp = python_sop.addBtn( 
                                    'pos_offsetDisableAll', btn_label, 
                                    callback = BlendParmsV2_PosDisableAll,
                                    join_with_next=True, 
                                    add=False 
                                )

        btn_label = 'Evenly Spaced'
        btn_label = S_(btn_label).mjust( width_2 )
        posBtn3_tmp = python_sop.addBtn( 
                                    'pos_evenlySpaced', btn_label, 
                                    callback = BlendParmsV2_PosEvenlySpaced,
                                    join_with_next = True, 
                                    add = False,
                                )
        
        btn_label = 'Auto-correct'
        btn_label = S_(btn_label).mjust( width_2 )
        posBtn4_tmp = python_sop.addBtn( 
                                    'pos_correct', btn_label,
                                    callback = BlendParmsV2_PosAutoCorrect,
                                    add = False,
                                )

        # it's probably that you click on this position offset slider 
        # when you want to tweak the ratio slider.
        # so, this folder should be collapsed if you don't use them.
        python_sop.addFolder( 
                                'pos_folder', 'Position', 
                                folder_type = 'collapse', 
                                parm_templates = ( 
                                                    posOffset_tmp, 
                                                    posBtn1_tmp, posBtn2_tmp, 
                                                    posBtn3_tmp, posBtn4_tmp,
                                                ),
                                insert_before = spare_sep
                            )



        # ~~~~~~~~~~~~ ramp basis menu ~~~~~~~~~~~~ #
        basis_parm = python_sop.addStr( 
                            'basis', 'Basis', 
                            default = ('linear',),
                            menu_items = hou.Ramp.MenuItems,
                            insert_before = spare_sep,
                            as_parm = True,
                        )

        python_sop.addSep( insert_before = spare_sep )



        # ~~~~~~~~~~~~~~ blend ratio ~~~~~~~~~~~~~~ #
        maximum = len(nodes) if nodes else 2
        maximum = max( maximum, 2 )
        python_sop.addFlt( 
                            'ratio', 'Ratio', 
                            initial = 1, value_range = (1, maximum), 
                            insert_before = spare_sep,
                        )


    def blendParms_v2_clear( self ):
        """
        v2 Clear

        Author: Sean
        """
        node = self.Node
        parm = self.Parm

        # clear expression
        for parm in self.Parms:
            parm.deleteAllKeyframes()


        # update parms
        parms_parm = node._['blendParms_ctrl'].toNode()._['parms']
        parm_names = parms_parm.toList()

        for parm_name in [ i.Name for i in self.Parms ]:
            if parm_name in parm_names:
                parm_names.pop( parm_name )

        parms_parm._ = ' '.join( parm_names )
setAttr( hou.Parm, 'ContextMenu_BlendParms', ContextMenuParm_BlendParms, replace=True )
















