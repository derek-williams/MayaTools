from ui import *
from buildScripts import pxUtilities

  
# main setup function
def pxBuildHindleg(legSideLong):
    ''' This script sets up a quadruped hindleg.
    It requires the leg joint chain and the requisite controls listed below:
        
        Joints:                               Controls: 
        - l_hip_jnt                        - pelvis_ctrl
        - l_knee_jnt                       - l_back_foot_ctrl
        - l_ankle_jnt                      - l_hip_ctrl
        - l_heel_jnt                       - l_knee_pv
        - l_fetlock_jnt                    - l_ankle_pv
        - l_pastern_rotate_jnt
        - l_pastern_left_jnt
        - l_pastern_right_jnt
        - l_coffin_left_jnt 
        - l_coffin_right_jnt'''
    
    charName = queryCharName()

    if legSideLong == "left":
        legSide = "l"
    elif legSideLong == "right":
        legSide = "r" 

        
    
    # orient joint chain
    pxUtilities.orientJoints(legSide + "_hip_jnt", "xyz", "yup")
    
      
    duplicate(legSide + "_hip_jnt")
    
    
    # rename joint chains
    rootJoint = rename(legSide + "_hip_jnt", legSide + "_hip_jnt" + charName)
    joints = listRelatives(rootJoint, c = 1, ad = 1)

    for each in joints:
        rename(each, each + charName)

    
    hipJoint = rename(legSide + "_hip_jnt1", legSide + "_hip_jnt_spring" + charName)  
    springChain = listRelatives(hipJoint, allDescendents = True)
    
    for each in springChain:
        rename(each, each + "_spring" + charName)
        
    delete(legSide + "_pastern_rotate_jnt_spring" + charName)
    
    
    # ik setup
    mel.eval('ikSpringSolver')
    
    springIKH = ikHandle(solver = "ikSpringSolver", sj = legSide + "_hip_jnt_spring" + charName, ee = legSide + "_fetlock_jnt_spring" + charName, n = legSide + "_spring_ikHandle" + charName, p = 1)[0]
    rpIKH = ikHandle(solver = "ikRPsolver", sj = legSide + "_knee_jnt" + charName, ee = legSide + "_fetlock_jnt" + charName, n = legSide + "_legRP_ikHandle" + charName, p = 1)[0]
    fetlockIKH = ikHandle(solver = "ikSCsolver", sj = legSide + "_fetlock_jnt" + charName, ee = legSide + "_pastern_rotate_jnt" + charName, n = legSide + "_fetlock_ikHandle" + charName, p = 1)[0]
    pasternOutIKH = ikHandle(solver = "ikSCsolver", sj = legSide + "_pastern_outer_jnt" + charName, ee = legSide + "_coffin_outer_jnt" + charName, n = legSide + "_pastern_outer_ikHandle" + charName, p = 1)[0]
    pasternInIKH = ikHandle(solver = "ikSCsolver", sj = legSide + "_pastern_inner_jnt" + charName, ee = legSide + "_coffin_inner_jnt" + charName, n = legSide + "_pastern_inner_ikHandle" + charName, p = 1)[0]
    
    
    # setup controls
        # foot control
    tempPlacementConstraint = pointConstraint(legSide + "_pastern_rotate_jnt" + charName, legSide + "_back_foot_ctrl" + charName, maintainOffset = False)
    delete(tempPlacementConstraint)
    makeIdentity(legSide + "_back_foot_ctrl" + charName, apply =True, translate = True, rotate = True, scale = True)
    
        # pole vector controls
    tempPlacementConstraint = pointConstraint(legSide + "_knee_jnt_spring" + charName, legSide + "_knee_pv" + charName, maintainOffset = False)
    delete(tempPlacementConstraint)
    if legSide == "l":
        move(0.041, 0, 0.659, legSide + "_knee_pv" + charName, relative = True)
    elif legSide == "r":
        move(-0.041, 0, 0.659, legSide + "_knee_pv" + charName, relative = True)
    makeIdentity(legSide + "_knee_pv" + charName, apply =True, translate = True, rotate = True, scale = True)
    
    tempPlacementConstraint = pointConstraint(legSide + "_ankle_jnt_spring" + charName, legSide + "_ankle_pv" + charName)
    delete(tempPlacementConstraint)
    if legSide == "l":
        move(-0.1, 0, -0.736, legSide + "_ankle_pv" + charName, relative = True)
    elif legSide == "r":
        move(0.1, 0, -0.736, legSide + "_ankle_pv" + charName, relative = True)  
    makeIdentity(legSide + "_ankle_pv" + charName, apply =True, translate = True, rotate = True, scale = True)
    
        # hip control
    tempPlacementConstraint = pointConstraint(legSide + "_hip_jnt_spring" + charName, legSide + "_hip_ctrl" + charName, maintainOffset = False)
    delete(tempPlacementConstraint)
    worldSpaceOfJoint = xform(legSide + "_hip_jnt_spring" + charName, query = True, rotatePivot = True, worldSpace = True)
    if legSide == "l":
        move(0.2, 0, 0, legSide + "_hip_ctrl" + charName, relative = True)
    elif legSide == "r":
        move(-0.2, 0, 0, legSide + "_hip_ctrl" + charName, relative = True)
    move(legSide + "_hip_ctrl" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    makeIdentity(legSide + "_hip_ctrl" + charName, apply = True, translate = True, rotate = True, scale = True)
    
        # pole vector constraints
    poleVectorConstraint(legSide + "_knee_pv" + charName, springIKH)
    poleVectorConstraint(legSide + "_ankle_pv" + charName, rpIKH)
    
            # constrain to foot control to follow translate Z and rotate Y
    group(legSide + "_knee_pv" + charName, n = legSide + "_knee_pv_grp" + charName) 
    group(legSide + "_ankle_pv" + charName, n = legSide + "_ankle_pv_grp" + charName)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".tz", legSide + "_knee_pv_grp" + charName + ".tz", force = True)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".tz", legSide + "_ankle_pv_grp" + charName + ".tz", force = True)
    worldSpaceOfJoint = xform(legSide + "_pastern_rotate_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_ankle_pv_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".ry", legSide + "_ankle_pv_grp" + charName + ".ry", force = True)
    
    
    # group rotate plane leg
    worldSpaceOfJoint = xform(legSide + "_hip_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    group(empty = True, n = legSide + "_rp_jnt_grp" + charName)
    move(legSide + "_rp_jnt_grp" + charName, worldSpaceOfJoint, absolute = True)
    makeIdentity(legSide + "_rp_jnt_grp" + charName, apply = True, translate = True, rotate = True, scale = True)
    
    group(empty = True, n = legSide + "_back_leg_grp" + charName)
    move(legSide + "_back_leg_grp" + charName, worldSpaceOfJoint, absolute = True)
    makeIdentity(legSide + "_back_leg_grp" + charName, apply = True, translate = True, rotate = True, scale = True)
    
    parent(legSide + "_hip_jnt" + charName, legSide + "_rp_jnt_grp" + charName)
    parent(legSide + "_rp_jnt_grp" + charName, legSide + "_back_leg_grp" + charName)
    
    # constraining the joint chains
    parentConstraint(legSide + "_hip_jnt_spring" + charName, legSide + "_rp_jnt_grp" + charName, maintainOffset = True)
    pointConstraint(legSide + "_hip_ctrl" + charName, legSide + "_hip_jnt_spring" + charName, maintainOffset = True)
    group(legSide + "_hip_ctrl" + charName, n = legSide + "_hip_ctrl_grp" + charName)
    
    # add attributes to foot control
    addAttr(legSide + "_back_foot_ctrl" + charName, longName = "heelLift", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_back_foot_ctrl" + charName, longName = "toeWiggle", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_back_foot_ctrl" + charName, longName = "outerHoofWiggle", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_back_foot_ctrl" + charName, longName = "innerHoofWiggle", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_back_foot_ctrl" + charName, longName = "outerHoofSpread", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_back_foot_ctrl" + charName, longName = "innerHoofSpread", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_back_foot_ctrl" + charName, longName = "tipToe", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_back_foot_ctrl" + charName, longName = "footTwist", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_back_foot_ctrl" + charName, longName = "toeTwist", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_back_foot_ctrl" + charName, longName = "pitch", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    
    # group-based reverse foot setup
    
    parent(rpIKH, springIKH)
    parent(springIKH, fetlockIKH, pasternOutIKH, pasternInIKH, legSide + "_back_foot_ctrl" + charName)
    
        # toe wiggle
    group(fetlockIKH, pasternOutIKH, pasternInIKH, name = legSide + "_back_toeWiggle_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_pastern_rotate_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_back_toeWiggle_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
        # outer hoof wiggle
    group(pasternOutIKH, name = legSide + "_back_outerHoofWiggle_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_pastern_outer_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_back_outerHoofWiggle_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
     # inner hoof wiggle
    group(pasternInIKH, name = legSide + "_back_innerHoofWiggle_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_pastern_inner_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_back_innerHoofWiggle_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
        # heel lift
    group(springIKH, name = legSide + "_back_heelLift_grp" + charName)
    move(legSide + "_back_heelLift_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
        # toe pivot
    group(legSide + "_back_toeWiggle_grp" + charName, legSide + "_back_heelLift_grp" + charName, name = legSide + "_back_toePivot_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_temp_backToePivot_pos" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_back_toePivot_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    delete(legSide + "_temp_backToePivot_pos" + charName)
    
        # heel pivot
    group(legSide + "_back_toePivot_grp" + charName, name = legSide + "_back_heelPivot_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_pastern_rotate_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_back_heelPivot_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
    # connect foot attributes
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".toeWiggle", legSide + "_back_toeWiggle_grp" + charName + ".rx", force = True)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".outerHoofWiggle", legSide + "_back_outerHoofWiggle_grp" + charName + ".rx", force = True)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".innerHoofWiggle", legSide + "_back_innerHoofWiggle_grp" + charName + ".rx", force = True)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".outerHoofSpread", legSide + "_back_outerHoofWiggle_grp" + charName + ".ry", force = True)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".innerHoofSpread", legSide + "_back_innerHoofWiggle_grp" + charName + ".ry", force = True)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".heelLift", legSide + "_back_heelLift_grp" + charName + ".rx", force = True)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".tipToe", legSide + "_back_toePivot_grp" + charName + ".rx", force = True)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".toeTwist", legSide + "_back_toePivot_grp" + charName + ".ry", force = True)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".footTwist", legSide + "_back_heelPivot_grp" + charName + ".ry", force = True)
    connectAttr(legSide + "_back_foot_ctrl" + charName + ".pitch", legSide + "_hip_jnt" + charName + ".rz", force = True)
    
    # make leg IK stretchy
    pxUtilities.makeIkStretchy(rpIKH)

    # final foot control group
    group(legSide + "_back_foot_ctrl" + charName, name = legSide + "_back_foot_ctrl_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_pastern_rotate_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_back_foot_ctrl_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
    # token
    hindLegTokens = group(empty = True, name = legSide + "_hindleg_token" + charName)
    print "HEY THE %s HAS BEEN MADE!" % (hindLegTokens)
    
    # finish setup
    select(clear = True)
    
   
def pxBuildBackLegs():
    
    pxUtilities.mirrorJoints("l_hip_jnt")   
    pxBuildHindleg("left")
    pxBuildHindleg("right")
    
    
