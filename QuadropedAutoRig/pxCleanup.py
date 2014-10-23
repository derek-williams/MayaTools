
from ui import *
from buildScripts import pxUtilities


def pxCleanup():
    print "Cleanup!!!"
    
    #BEGIN GRP CLEANUP
    masterNames = ['Ctrls',"No_Touch",'Joints']
    charName = queryCharName()

    print charName
    allGrp = "All_Grp" + charName
    ctrlsGrp = "Ctrls_Grp" + charName
    jointsGrp = "Joints_Grp" + charName
    dontTouchGrp = "No_Touch_Grp" + charName
    #spine
    spineGroups = ['animationControls_grp' + charName]
    spineNoTouch = ['dontTouch_grp' + charName, 
                    'pelvis_helper_aim_loc'+ charName,
                    'sternum_helper_aim_loc'+ charName]
    spineJointChains = ['dontTouchJoints_grp' + charName,'Chest_HelperJnt' + charName, 'LowerPelvis_HelperJnt' + charName]
    prefix = 'spine'
    prefixTypes = [spineGroups, spineNoTouch, spineJointChains]
    i = 0
    for each in prefixTypes:
        typeGrp = group(n = prefix + "_" + masterNames[i] + "_Grp",empty = True)
        parent  (typeGrp , masterNames[i] + '_Grp'+ charName) 
        for j in each:
                parent (j, typeGrp)
        i+=1
    #neck 
    neckGroups = [nt.Transform(u'ikBtmNeckCtrl' + charName),
     nt.Transform(u'AllNeck_Pre_Grp'),
     nt.Transform(u'bindJointBtm_grp'),
     nt.Transform(u'bindJointMid_grp'),
     nt.Transform(u'bindJointTop_grp'),
     nt.Transform(u'ikMidCtrl' + charName + '_preGrp'),
     nt.Transform(u'ikHeadCtrl' + charName + '_preGrp'),
     #nt.Transform(u'allNeck_pivot_grp' + charName),
     'IKFK_Neck']
    neckNoTouch = [nt.IkHandle(u'neck_ikhandle' + charName),
     nt.Transform(u'neck_curve' + charName)]
    neckJointChains = [nt.Joint(u'neck_ik_rootjnt' + charName),
     nt.Joint(u'neck_fk_rootjnt' + charName),
     nt.Joint(u'Main_Neck_jnt1' + charName)]
    prefix = 'neck'
    prefixTypes = [neckGroups, neckNoTouch, neckJointChains]
    masterNames = ['Ctrls',"No_Touch",'Joints']
    i = 0
    for each in prefixTypes:
        typeGrp = group(n = prefix + "_" + masterNames[i] + "_Grp",empty = True)
        parent  (typeGrp , masterNames[i] + '_Grp'+ charName) 
        for j in each:
                parent (j, typeGrp)
        i+=1
    #tail
    tailGroups = ['tail_root_Grp' + charName]
    tailNoTouch = []
    tailJointChains = ['tail_root']
    prefix = 'tail'
    prefixTypes = [tailGroups, tailNoTouch, tailJointChains]
    i = 0
    for each in prefixTypes:
        typeGrp = group(n = prefix + "_" + masterNames[i] + "_Grp",empty = True)
        parent  (typeGrp , masterNames[i] + '_Grp'+ charName) 
        for j in each:
                parent (j, typeGrp)
        i+=1
    
    #udder
    udderGroups = ['udder_01_jnt_Grp' + charName]
    udderNoTouch = []
    udderJointChains = ['udder_root']
    prefix = 'tail'
    prefixTypes = [udderGroups, udderNoTouch, udderJointChains]
    i = 0
    for each in prefixTypes:
        typeGrp = group(n = prefix + "_" + masterNames[i] + "_Grp",empty = True)
        parent  (typeGrp , masterNames[i] + '_Grp'+ charName) 
        for j in each:
                parent (j, typeGrp)
        i+=1
        
    #annotates
    annoGroups = [nt.Transform(u'l_wrist_pv'+ charName +'_annot'),
     nt.Transform(u'r_wrist_pv'+ charName +'_annot'),
     nt.Transform(u'l_ankle_pv'+ charName +'_annot'),
     nt.Transform(u'r_ankle_pv'+ charName +'_annot'),
     nt.Transform(u'l_knee_pv'+ charName +'_annot'),
     nt.Transform(u'r_knee_pv'+ charName +'_annot')]
    annoNoTouch = []
    annoJointChains = []
    prefix = 'Annot'
    prefixTypes = [annoGroups, annoNoTouch, annoJointChains]
    i = 0
    for each in prefixTypes:
        typeGrp = group(n = prefix + "_" + masterNames[i] + "_Grp",empty = True)
        parent  (typeGrp , masterNames[i] + '_Grp'+ charName) 
        for j in each:
                parent (j, typeGrp)
        i+=1
    tailGroups = ['tail_root_Grp' + charName]
    tailNoTouch = []
    tailJointChains = ['tail_root']
    prefix = 'tail'
    prefixTypes = [tailGroups, tailNoTouch, tailJointChains]
    i = 0
    for each in prefixTypes:
        typeGrp = group(n = prefix + "_" + masterNames[i] + "_Grp",empty = True)
        parent  (typeGrp , masterNames[i] + '_Grp'+ charName) 
        for j in each:
                parent (j, typeGrp)
        i+=1
    
        
    #frontLegs
    frontLegsGroups = [nt.Transform(u'l_front_foot_ctrl_grp' + charName),
     nt.Transform(u'r_front_foot_ctrl_grp' + charName),
     nt.Transform(u'r_wrist_pv_grp' + charName),
     nt.Transform(u'l_wrist_pv_grp' + charName),
     nt.Transform(u'r_shoulder_pv' + charName),
     nt.Transform(u'l_shoulder_ctrl_grp' + charName),
     nt.Transform(u'r_shoulder_ctrl_grp' + charName),
     nt.Transform(u'l_shoulder_pv' + charName)] 
    frontLegsNoTouch = [nt.Transform(u'r_leg_ikHandle' + charName + 'startPoint'),
     nt.Transform(u'r_leg_ikHandle' + charName + 'endPoint'),
     nt.IkHandle(u'r_elbow_ikHandle' + charName),
     nt.IkHandle(u'r_shoulder_ikHandle' + charName),
     nt.IkHandle(u'l_elbow_ikHandle' + charName),
     nt.IkHandle(u'l_shoulder_ikHandle' + charName),
     nt.Transform(u'l_leg_ikHandle' + charName + 'endPoint'),
     nt.Transform(u'l_leg_ikHandle' + charName + 'startPoint')] 
    frontLegsJointChains = [nt.Transform(u'l_foreleg_grp' + charName),
     nt.Transform(u'r_foreleg_grp' + charName)] 
    prefix = 'frontLegs'
    prefixTypes = [frontLegsGroups, frontLegsNoTouch, frontLegsJointChains]
    i = 0
    for each in prefixTypes:
        typeGrp = group(n = prefix + "_" + masterNames[i] + "_Grp",empty = True)
        parent  (typeGrp , masterNames[i] + '_Grp'+ charName) 
        for j in each:
                parent (j, typeGrp)
        i+=1 
    #rearLegs
    rearLegsGroups = [nt.Transform(u'l_ankle_pv_grp' + charName),
     nt.Transform(u'r_ankle_pv_grp' + charName),
     nt.Transform(u'r_back_foot_ctrl_grp' + charName),
     nt.Transform(u'l_back_foot_ctrl_grp' + charName),
     nt.Transform(u'r_hip_ctrl_grp' + charName),
     nt.Transform(u'l_hip_ctrl_grp' + charName),
     nt.Transform(u'l_knee_pv_grp' + charName),
     nt.Transform(u'r_knee_pv_grp' + charName)]
    rearLegsNoTouch =[nt.Transform(u'r_legRP_ikHandle' + charName + 'endPoint'),
     nt.Transform(u'r_legRP_ikHandle' + charName + 'startPoint'),
     nt.Transform(u'l_legRP_ikHandle' + charName + 'endPoint'),
     nt.Transform(u'l_legRP_ikHandle' + charName + 'startPoint')]
    rearLegsJointChains =  [nt.Joint(u'r_hip_jnt_spring' + charName),
     nt.Transform(u'r_back_leg_grp' + charName),
     nt.Transform(u'l_back_leg_grp' + charName),
     nt.Joint(u'l_hip_jnt_spring' + charName)]
    prefix = 'rearLegs'
    prefixTypes = [rearLegsGroups, rearLegsNoTouch, rearLegsJointChains]
    i = 0
    for each in prefixTypes:
        typeGrp = group(n = prefix + "_" + masterNames[i] + "_Grp",empty = True)
        parent  (typeGrp , masterNames[i] + '_Grp'+ charName) 
        for j in each:
                parent (j, typeGrp)
        i+=1
    #ears
    group("l_fk_dynamic_curve" + charName, "r_fk_dynamic_curve" + charName, name = "ear_dynamic_curves_grp" + charName)
    group("l_main_curve" + charName, "l_main_curve" + charName, name = "ear_spline_curves_grp" + charName)
    #group("l_ear_ikh" + charName, "r_ear_ikh" + charName, "l_ear_splineIKH" + charName, "r_ear_splineIKH" + charName, name = "ear_ikh_grp" + charName)
    earsGroups = [nt.Transform(u'l_dynamic_ctrl' + charName),
     nt.Transform(u'l_ear_ctrl_grp' + charName),
     nt.Transform(u'r_ear_ctrl_grp' + charName),
     nt.Transform(u'r_dynamic_ctrl' + charName)]
    earsNoTouch = ['hairSystem2OutputCurves',
     'hairSystem2Follicles',
     'l_nucleus' + charName,
     'hairSystem2',
     'hairSystem1OutputCurves',
     'hairSystem1Follicles',
     'r_nucleus' + charName,
     'l_hair_system_node' + charName,
     "ear_dynamic_curves_grp" + charName, 
     "ear_spline_curves_grp" + charName, "ear_ikh_grp" + charName,
     'r_ear_ikSpline_root'+ charName,
     'l_ear_ikSpline_root'+ charName,
     'r_r_earSplineIk_curve' + charName + '_cv_Null_0',
     'l_l_earSplineIk_curve' + charName + '_cv_Null_0',
     'l_ear_splineIKH'+charName ,
     'r_ear_splineIKH'+charName ,
     'r_hair_system_node'+charName 
     ] 
    earsJointChains = ['r_ear_fk_root' + charName, 
                      ' l_ear_fk_root' + charName, 
                       'l_Main_Ear_root'+ charName,
                       'r_Main_Ear_root'+ charName,
                       'l_ear_dyn_root' + charName,
                       'r_ear_dyn_root' + charName]
    prefix = 'ears'
    prefixTypes = [earsGroups, earsNoTouch, earsJointChains]
    i = 0
    for each in prefixTypes:
        typeGrp = group(n = prefix + "_" + masterNames[i] + "_Grp",empty = True)
        parent  (typeGrp , masterNames[i] + '_Grp'+ charName) 
        for j in each:
                parent (j, typeGrp)
        i+=1
    parent ('worldLocator',"COG")
    #*************check this with bugi****************
    #parentConstraint("l_ear_ctrl" + charName, "l_l_earSplineIk_curve" + charName + "_cv_Null_0", mo = True)
    #parentConstraint("r_ear_ctrl" + charName, "r_r_earSplineIk_curve" + charName + "_cv_Null_0", mo = True)
    
    #BEGIN ATTRIBUTE CLEANUP
    #SPINE
    myAttr = [ ".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("body_ctrl" + charName, myAttr)
        #fk controls
    fkControls = ["FK_neckCtrl4" + charName, "FK_neckCtrl3" + charName, "FK_neckCtrl2" + charName,
    "FK_neckCtrl1" + charName, "fkBack3_ctrl" + charName, "fkBack2_ctrl" + charName, "fkBack1_ctrl" + charName,
    "l_ear_ctrl" + charName, "r_ear_ctrl" + charName, "udder_01_jnt_ctrl" + charName, "tail_root_ctrl" + charName, "tail_01_jnt_ctrl" + charName,
    "tail_02_jnt_ctrl" + charName,'AllNeck_Ctrl' + charName] 
    myAttr = myAttr = [".tx", ".ty", ".tz", ".sx", ".sy", ".sz", ".visibility"]
    for each in fkControls:
        pxUtilities.cleanup(each, myAttr)
        # ikCtrls
    ikControls = ["shoulder_ctrl" + charName, "torso_ctrl" + charName, "pelvis_ctrl" + charName]
    myAttr = myAttr = [".sx", ".sy", ".sz", ".visibility"]
    for each in ikControls:
        pxUtilities.cleanup(each, myAttr)
    #cleanup neck attrs
    myAttr = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("IKFK_Neck", myAttr)
    if objExists('character_grp' + charName): 
        delete ('character_grp' + charName)
    # HIND LEG
    # cleanup hip control groups
    myAttr = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("l_hip_ctrl_grp" + charName, myAttr)
    pxUtilities.cleanup("r_hip_ctrl_grp" + charName, myAttr)
    # cleanup hip control groups
    myAttr = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("l_shoulder_ctrl_grp" + charName, myAttr)
    pxUtilities.cleanup("r_shoulder_ctrl_grp" + charName, myAttr)
    pxUtilities.cleanup("l_foreleg_grp" + charName, myAttr)
    pxUtilities.cleanup("r_foreleg_grp" + charName, myAttr)
    # cleanup spring joint chain
    setAttr("l_hip_jnt_spring" + charName + ".visibility", 0)
    setAttr("r_hip_jnt_spring" + charName + ".visibility", 0)
    # cleanup pole vector groups
    myAttr = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("l_knee_pv_grp" + charName, myAttr)
    pxUtilities.cleanup("r_knee_pv_grp" + charName, myAttr)
    pxUtilities.cleanup("l_ankle_pv_grp" + charName, myAttr)
    pxUtilities.cleanup("r_ankle_pv_grp" + charName, myAttr)
    # cleanup pole vectors
    myAttr = [".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("l_knee_pv" + charName, myAttr)
    pxUtilities.cleanup("r_knee_pv" + charName, myAttr)
    pxUtilities.cleanup("l_ankle_pv" + charName, myAttr)
    pxUtilities.cleanup("r_ankle_pv" + charName, myAttr)
    # cleanup hip control
    myAttr = [".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("l_hip_ctrl" + charName, myAttr)
    pxUtilities.cleanup("r_hip_ctrl" + charName, myAttr)
    # cleanup foot control
    myAttr = [".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("l_back_foot_ctrl" + charName, myAttr)
    pxUtilities.cleanup("r_back_foot_ctrl" + charName, myAttr)
    # FORE LEG
    # cleanup shoulder pole vectors
    setAttr("l_shoulder_pv" + charName + ".visibility", 0)
    setAttr("r_shoulder_pv" + charName + ".visibility", 0)
    myAttr = [".visibility"]
    pxUtilities.cleanup("l_shoulder_pv" + charName, myAttr)
    pxUtilities.cleanup("r_shoulder_pv" + charName, myAttr)
    # cleanup pole vector group
    myAttr = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("l_wrist_pv_grp" + charName, myAttr)
    pxUtilities.cleanup("r_wrist_pv_grp" + charName, myAttr)
    # cleanup pole vector
    myAttr = [ ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("l_wrist_pv" + charName, myAttr)
    pxUtilities.cleanup("r_wrist_pv" + charName, myAttr) 
    # cleanup elbow control
    myAttr = [".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("l_elbow_ctrl" + charName, myAttr)
    pxUtilities.cleanup("r_elbow_ctrl" + charName, myAttr)
    # cleanup shoulder control
    myAttr = [".sx", ".sy", ".sz", ".visibility"]
    pxUtilities.cleanup("l_shoulder_ctrl" + charName, myAttr)
    pxUtilities.cleanup("r_shoulder_ctrl" + charName, myAttr)
    # cleanup foot control
    pxUtilities.cleanup("l_front_foot_ctrl" + charName, myAttr)
    pxUtilities.cleanup("r_front_foot_ctrl" + charName, myAttr)
    # IK HANDLES
    #"select ("r_shoulder_ikHandle" + charName)
    handles = [ "r_shoulder_ikHandle" + charName,"r_elbow_ikHandle" + charName, "r_distPhalanx_outer_ikHandle" + charName,"r_distPhalanx_inner_ikHandle" + charName,
               "r_midPhalanx_ikHandle" + charName, "r_leg_ikHandle" + charName, "l_spring_ikHandle" + charName,
               "l_legRP_ikHandle" + charName, "l_pastern_outer_ikHandle" + charName, "l_pastern_inner_ikHandle" + charName, "l_fetlock_ikHandle" + charName,
               "r_fetlock_ikHandle" + charName, "r_pastern_outer_ikHandle" + charName, "r_pastern_inner_ikHandle" + charName, "r_spring_ikHandle" + charName,
               "r_legRP_ikHandle" + charName, "l_leg_ikHandle" + charName, "l_midPhalanx_ikHandle" + charName,
               "l_distPhalanx_outer_ikHandle" + charName, "l_distPhalanx_inner_ikHandle" + charName, "l_elbow_ikHandle" + charName, "l_shoulder_ikHandle" + charName,
               "r_ear_splineIKH" + charName, "l_ear_splineIKH" + charName, "neck_ikhandle" + charName,
               "spine_IKhandle" + charName]
    pxUtilities.cleanupHandles(handles)
    #face
    hideNoTouch = [nt.Transform(u'Joints_Grp' +charName),
                   nt.Transform(u'No_Touch_Grp' +charName)]
                   #nt.Joint(u'head_jnt' +charName)
    ikBindJoints = [nt.Joint(u'spine_IK_jnt1' +charName),
                    nt.Joint(u'spine_IK_jnt2' +charName),
                    nt.Joint(u'spine_IK_jnt3' +charName),
                    nt.Joint(u'neck_ik_bind_jntBtm' +charName),
                    nt.Joint(u'neck_ik_bind_jntMid' +charName),
                    nt.Joint(u'neck_ik_bind_jntTop' +charName)]
    hide(hideNoTouch,ikBindJoints)
    select(cl = True)
    
    
    if charName == '_OldGoat':
        setAttr('head_jnt.visibility', 0)
        parentConstraint('FK_neckCtrl2_OldGoat', 'collar_offset_OldGoat', mo = True)
    
    # Parent constrain collar rig
    if charName == '_YoungGoat':
        parentConstraint('body_ctrl_YoungGoat', 'collar_offset_YoungGoat', mo = 1)
    
    #delete('joints_temp')
    setAttr("COG.meshResolution",1)
