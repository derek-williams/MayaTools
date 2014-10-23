from ui import *
from buildScripts import pxUtilities

  
# main setup function    
def pxBuildForeleg(legSideLong):
    ''' This script sets up a quadruped foreleg.
    It requires the leg joint chain and the requisite controls listed below:
        
        Joints:                               Controls: 
        - l_shoulder_anchor_jnt            - l_front_foot_ctrl
        - l_shoulder_hinge_jnt             - l_wrist_pv
        - l_scapula_jnt                    - l_elbow_ctrl
        - l_elbow_jnt                      - l_shoulder_ctrl
        - l_wrist_jnt                    
        - l_palm_jnt
        - l_middle_phalanx_rotate_jnt
        - l_middle_phalanx_left_jnt
        - l_middle_phalanx_right_jnt
        - l_distal_phalanx_left_jnt
        - l_distal_phalanx_right_jnt'''
   
    charName = queryCharName()
    
    if legSideLong == "left":
        legSide = "l"
    elif legSideLong == "right":
        legSide = "r"

    # rename joints
    rootJoint = rename(legSide + "_shoulder_anchor_jnt", legSide + "_shoulder_anchor_jnt" + charName)
    joints = listRelatives(rootJoint, c = 1, ad = 1)
    

    for each in joints:
        rename(each, each + charName)
        
        
    # orient joint chain
    pxUtilities.orientJoints(legSide + "_shoulder_anchor_jnt" + charName, "xyz", "yup")
    
    
    # setup ik handles
    shoulderIKH = ikHandle(solver = "ikRPsolver", sj = legSide + "_shoulder_anchor_jnt" + charName, ee = legSide + "_scapula_jnt" + charName, n = legSide + "_shoulder_ikHandle" + charName, p = 1)[0]
    elbowIKH = ikHandle(solver = "ikSCsolver",sj = legSide + "_scapula_jnt" + charName, ee = legSide + "_elbow_jnt" + charName, n = legSide + "_elbow_ikHandle" + charName, p = 1)[0]
    legIKH = ikHandle(solver = "ikRPsolver", sj = legSide + "_elbow_jnt" + charName, ee = legSide + "_palm_jnt" + charName, n = legSide + "_leg_ikHandle" + charName, p = 1)[0]
    ballIKH = ikHandle(solver = "ikSCsolver",sj = legSide + "_palm_jnt" + charName, ee = legSide + "_middlePhalanx_rotate_jnt" + charName, n = legSide + "_midPhalanx_ikHandle" + charName, p = 1)[0]
    toeOutIKH = ikHandle(solver = "ikSCsolver",sj = legSide + "_middlePhalanx_outer_jnt" + charName, ee = legSide + "_distalPhalanx_outer_jnt" + charName, n = legSide + "_distPhalanx_outer_ikHandle" + charName, p = 1)[0]
    toeInIKH = ikHandle(solver = "ikSCsolver",sj = legSide + "_middlePhalanx_inner_jnt" + charName, ee = legSide + "_distalPhalanx_inner_jnt" + charName, n = legSide + "_distPhalanx_inner_ikHandle" + charName, p = 1)[0]
    
    # setup controls
    tempPlacementConstraint = pointConstraint(legSide + "_palm_jnt" + charName, legSide + "_front_foot_ctrl" + charName)
    delete(tempPlacementConstraint)
    makeIdentity(legSide + "_front_foot_ctrl" + charName, apply =True, translate = True, rotate = True, scale = True)
    
    # parent IK handles under foot control
    parent(legIKH, ballIKH, toeOutIKH, toeInIKH, legSide + "_front_foot_ctrl" + charName)
    
    # place elbow control
    tempPlacementConstraint = pointConstraint(legSide + "_elbow_jnt" + charName, legSide + "_elbow_ctrl" + charName)
    delete(tempPlacementConstraint)
    worldSpaceOfJoint = xform(legSide + "_elbow_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    if legSide == "l":
        move(0.2, 0, 0, legSide + "_elbow_ctrl" + charName, relative = True)
    if legSide == "r":
        move(-0.2, 0, 0, legSide + "_elbow_ctrl" + charName, relative = True)
    move(legSide + "_elbow_ctrl" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    makeIdentity(legSide + "_elbow_ctrl" + charName, apply =True, translate = True, rotate = True, scale = True)
    
    # place shoulder control
    tempPlacementConstraint = pointConstraint(legSide + "_scapula_jnt" + charName, legSide + "_shoulder_ctrl" + charName)
    delete(tempPlacementConstraint)
    worldSpaceOfJoint = xform(legSide + "_scapula_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    if legSide == "l":
        move(0.1, 0, 0, legSide + "_shoulder_ctrl" + charName, relative = True)
    elif legSide == "r":
        move(-0.1, 0, 0, legSide + "_shoulder_ctrl" + charName, relative = True)
    move(legSide + "_shoulder_ctrl" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    makeIdentity(legSide + "_shoulder_ctrl" + charName, apply =True, translate = True, rotate = True, scale = True)
    
    # place pole vector control
    tempPlacementConstraint = pointConstraint(legSide + "_wrist_jnt" + charName, legSide + "_wrist_pv" + charName)
    delete(tempPlacementConstraint)
    worldSpaceOfJoint = xform(legSide + "_wrist_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(0, 0, 0.42, legSide + "_wrist_pv" + charName, relative = True)
    makeIdentity(legSide + "_wrist_pv" + charName, apply =True, translate = True, rotate = True, scale = True)
    
    tempPlacementConstraint = pointConstraint(legSide + "_shoulder_jnt" + charName, legSide + "_shoulder_pv" + charName)
    delete(tempPlacementConstraint)
    move(0.044, 0, 0.281, legSide + "_shoulder_pv" + charName, relative = True)
    makeIdentity(legSide + "_shoulder_pv" + charName, apply =True, translate = True, rotate = True, scale = False)
    
    # control-joint parent constraints
    parentConstraint(legSide + "_elbow_ctrl" + charName, elbowIKH, maintainOffset = True)
    parentConstraint(legSide + "_shoulder_ctrl" + charName, shoulderIKH, maintainOffset = True)
    poleVectorConstraint(legSide + "_wrist_pv" + charName, legIKH)
    poleVectorConstraint(legSide + "_shoulder_pv" + charName, shoulderIKH)
    
    parent(legSide + "_elbow_ctrl" + charName, legSide + "_shoulder_ctrl" + charName)
    
    
    # finish pole vector setup
    group(legSide + "_wrist_pv" + charName, name = legSide + "_wrist_pv_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_palm_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_wrist_pv_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    connectAttr(legSide + "_front_foot_ctrl" + charName + ".rz", legSide + "_wrist_pv_grp" + charName + ".rz")
    connectAttr(legSide + "_front_foot_ctrl" + charName + ".tz", legSide + "_wrist_pv_grp" + charName + ".tz")
    
    
    # add reverse foot attributes to foot control
    addAttr(legSide + "_front_foot_ctrl" + charName, longName = "heelLift", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_front_foot_ctrl" + charName, longName = "toeWiggle", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_front_foot_ctrl" + charName, longName = "outerHoofWiggle", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_front_foot_ctrl" + charName, longName = "innerHoofWiggle", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_front_foot_ctrl" + charName, longName = "outerHoofSpread", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_front_foot_ctrl" + charName, longName = "innerHoofSpread", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_front_foot_ctrl" + charName, longName = "tipToe", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_front_foot_ctrl" + charName, longName = "footTwist", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    addAttr(legSide + "_front_foot_ctrl" + charName, longName = "toeTwist", attributeType = "float", defaultValue = 0.0, hidden = False, keyable = True)
    
    
    # group-based reverse foot setup
        # toe wiggle
    group(ballIKH, toeOutIKH, toeInIKH, name = legSide + "_front_toeWiggle_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_middlePhalanx_rotate_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_front_toeWiggle_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
        # outer hoof wiggle
    group(toeOutIKH, name = legSide + "_front_outerHoofWiggle_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_middlePhalanx_outer_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_front_outerHoofWiggle_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
        # inner hoof wiggle
    group(toeInIKH, name = legSide + "_front_innerHoofWiggle_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_middlePhalanx_inner_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_front_innerHoofWiggle_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
        # heel lift
    group(legIKH, name = legSide + "_front_heelLift_grp" + charName)
    move(legSide + "_front_heelLift_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
        # toe pivot
    group(legSide + "_front_toeWiggle_grp" + charName, legSide + "_front_heelLift_grp" + charName, name = legSide + "_front_toePivot_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_temp_frontToePivot_pos" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_front_toePivot_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    delete(legSide + "_temp_frontToePivot_pos" + charName)
    
        # heel pivot
    group(legSide + "_front_toePivot_grp" + charName, name = legSide + "_front_heelPivot_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_middlePhalanx_rotate_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_front_heelPivot_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
    # group shoulder control
    group(legSide + "_shoulder_ctrl" + charName, name = legSide + "_shoulder_ctrl_grp" + charName)
    worldSpaceOfControl = xform(legSide + "_shoulder_ctrl" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_shoulder_ctrl_grp" + charName + ".rotatePivot", worldSpaceOfControl, absolute = True)
    makeIdentity(legSide + "_shoulder_ctrl_grp" + charName, apply =True, translate = True, rotate = True, scale = True)
    
    # group anchor joint
    group(legSide + "_shoulder_anchor_jnt" + charName, name = legSide + "_foreleg_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_shoulder_anchor_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_foreleg_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    makeIdentity(legSide + "_foreleg_grp" + charName, apply =True, translate = True, rotate = True, scale = True)
    
    # connect foot attributes
    connectAttr(legSide + "_front_foot_ctrl" + charName + ".toeWiggle", legSide + "_front_toeWiggle_grp" + charName + ".rx", force = True)
    connectAttr(legSide + "_front_foot_ctrl" + charName + ".outerHoofWiggle", legSide + "_front_outerHoofWiggle_grp" + charName + ".rx", force = True)
    connectAttr(legSide + "_front_foot_ctrl" + charName + ".innerHoofWiggle", legSide + "_front_innerHoofWiggle_grp" + charName + ".rx", force = True)
    connectAttr(legSide + "_front_foot_ctrl" + charName + ".outerHoofSpread", legSide + "_front_outerHoofWiggle_grp" + charName + ".ry", force = True)
    connectAttr(legSide + "_front_foot_ctrl" + charName + ".innerHoofSpread", legSide + "_front_innerHoofWiggle_grp" + charName + ".ry", force = True)
    connectAttr(legSide + "_front_foot_ctrl" + charName + ".heelLift",legSide + "_front_heelLift_grp" + charName + ".rx", force = True)
    connectAttr(legSide + "_front_foot_ctrl" + charName + ".tipToe",legSide + "_front_toePivot_grp" + charName + ".rx", force = True)
    connectAttr(legSide + "_front_foot_ctrl" + charName + ".toeTwist",legSide + "_front_toePivot_grp" + charName + ".ry", force = True)
    connectAttr(legSide + "_front_foot_ctrl" + charName + ".footTwist",legSide + "_front_heelPivot_grp" + charName + ".ry", force = True)
        
    # make leg IK stretchy
    pxUtilities.makeIkStretchy(legIKH)

    # final foot control group
    group(legSide + "_front_foot_ctrl" + charName, name = legSide + "_front_foot_ctrl_grp" + charName)
    worldSpaceOfJoint = xform(legSide + "_palm_jnt" + charName, query = True, rotatePivot = True, worldSpace = True)
    move(legSide + "_front_foot_ctrl_grp" + charName + ".rotatePivot", worldSpaceOfJoint, absolute = True)
    
    # token
    foreLegTokens = group(empty = True, name = legSide + "_foreleg_token" + charName)      
    print "HEY THE %s HAS BEEN MADE!" % (foreLegTokens)
    
    # finish setup
    select(clear = True)
    
def pxBuildFrontLegs():
    
    pxUtilities.mirrorJoints("l_shoulder_anchor_jnt")   
    pxBuildForeleg("left")
    pxBuildForeleg("right")




