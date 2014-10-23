from ui import *
from buildScripts import pxUtilities

def pxBuildEarSide(earSideLong):
    ''' This script sets up a quadruped ear.
        It requires the ear joint chain and the requisite controls listed below:
            
            Joints:                               Controls: 
            - l_ear_fk_root                       - l_ear_ctrl
            - l_ear_01_jnt             
            - l_ear_02_jnt                    
            - l_ear_03_jnt                      
            - l_ear_04_jnt                    
            - l_ear_05_jnt
            - l_ear_end_jnt'''
    
    charName = queryCharName()
    
    if earSideLong == "left":
        earSide = "l"
    elif earSideLong == "right":
        earSide = "r"
    

    root = rename(earSide + '_ear_fk_root', earSide + '_ear_fk_root' + charName)
    jointRelatives = listRelatives(root, allDescendents = True)
    jointRelatives.reverse()
    
    dynamicChain = duplicate(root, n = earSide + '_ear_dyn_root' + charName)
    mainChain = duplicate(root, n = earSide + '_Main_Ear_root' + charName)
    
    # rename dynamic joint chain
    dynJointRelatives = listRelatives(dynamicChain, ad = True)
    dynJointRelatives.reverse()
    
    i = 1
    for each in dynJointRelatives:
        rename(each, earSide + '_ear_dyn_jnt' + str(i) + charName)
        i+=1
        
    # rename main joint chain
    mainJointRelatives = listRelatives(mainChain, ad = True)
    mainJointRelatives.reverse()
    
    j = 1
    for each in mainJointRelatives:
        rename(each, earSide + '_Main_Ear_jnt' + str(j) + charName)
        j+=1
    
    
    baseJoint = dynJointRelatives[0]
    endJoint = dynJointRelatives[5]
    
    
    ctrls = []
    nulls = []
    jointPositions = []
    
    for each in jointRelatives:
        # obtain the joint positions for curve creation
        position = xform(each, query = True, rotatePivot = True, worldSpace = True)
        jointPositions.append(position)
        
        # create control    
        if charName == '_YoungGoat':
            ctrl = circle(n = each + '_ctrl' + charName, nr = (1, 0, 0), c = (0, 0, 0), r = 0.1, ch = False)
        elif charName == '_OldGoat':
            ctrl = circle(n = each + '_ctrl' + charName, nr = (1, 0, 0), c = (0, 0, 0), r = 0.15, ch = False)
        ctrlShape = pickWalk(ctrl, d = 'down')  
        setAttr(ctrlShape[0] + '.overrideEnabled', 1)
        if earSideLong == 'left':
            setAttr(ctrlShape[0] + ".overrideColor", 18)
        elif earSideLong == 'right':
            setAttr(ctrlShape[0] + ".overrideColor", 13)
            
        ctrls.append(ctrl)
        select (cl = True)
        
        # position and parent constrain joints to controls
        null = group(n = each + '_offset' + charName, em = True)
        nulls.append(null)
        delete(parentConstraint(each, null, mo = False))
        delete(parentConstraint(each, ctrl, mo = False))
        parent(ctrl, null)
        parentConstraint(ctrl, each)
    
    # parent the nulls and controls
    parent(nulls[1], ctrls[0])
    parent(nulls[2], ctrls[1])
    parent(nulls[3], ctrls[2])
    parent(nulls[4], ctrls[3])
    
    delete(nulls[5])
       
    # create main curve
    mainCurve = curve(d = 1, n = earSide + "_main_curve" + charName, p = jointPositions)
    curveShape = mainCurve + 'Shape'
    numSpans = int(getAttr(curveShape + ".spans"))
    degree = int(getAttr(curveShape + ".degree"))
    numCV = numSpans + degree
    
    
    # create clusters on the curve's CVs
    k = 0
    l = 1
    for each in range(0, numCV):
        select(mainCurve + '.cv' + '[' + str(k) + ']')
        clstr = cluster(rel = False, n = 'main_curve_cluster' + str(l) + charName)
        setAttr(clstr[0] + 'Handle.visibility', 0, keyable = False)
        parent(clstr, jointRelatives[k])
        k+=1
        l+=1
    
    # create dynamic curve    
    select(mainCurve)
    mel.eval('makeCurvesDynamic 2 {"1","0","1","1","0"}')
    fkDynCurve = rename("curve1", earSide + "_fk_dynamic_curve" + charName)
    
    # rename dynamic nodes
    if earSideLong == "left":
        hairSystemNode = rename("hairSystem1", earSide + "_hair_system_node" + charName)
    elif earSideLong == "right":
        hairSystemNode = rename("hairSystem2", earSide + "_hair_system_node" + charName)  
    #this if statment can be removed once bugi updates the old goat templlate ref
    #if charName == '_YoungGoat':
    select(hairSystemNode)
    mel.eval('assignNSolver ""')
        
    select(mainCurve)
    follicleNode = rename(pickWalk (d = 'up'), earSide + "_follicle_node" + charName)
    pickWalk(follicleNode, d = 'up')
    nucleusNode = rename("nucleus1", earSide + "_nucleus" + charName)
    
    

    
    # add spline IK handle
    select(baseJoint)
    select(endJoint, add = True)
    select(fkDynCurve, add = True)
    dynIkHandle = ikHandle(solver = "ikSplineSolver", ccv = False, pcv = False)
    rename(dynIkHandle[0], earSide + "_ear_splineIKH" + charName)
    setAttr(dynIkHandle[0] + ".rootOnCurve", 0)
    
    # set follicle attribute values
    setAttr(follicleNode + ".pointLock", 1)
    setAttr(follicleNode + ".overrideDynamics", 1)
    
    # create control object to house dynamic attributes
    createNode("implicitSphere")
    dynamicControlObj = rename(pickWalk (d = "up"), earSide + "_dynamic_ctrl" + charName)
    
    pointConstraint(mainJointRelatives[5], dynamicControlObj, mo = False)
    
        # add dynamic attributes
    #addAttr(dynamicControlObj, ln = "enableDynamics", at = "bool", keyable = True)
    #setAttr(dynamicControlObj + ".enableDynamics", 0)
    addAttr(dynamicControlObj, ln = "spaceScale", at = "double", min = 0, max = 2, dv = 1, keyable = True)
    if charName == '_YoungGoat':
        setAttr(dynamicControlObj + '.spaceScale', 0.2)
    addAttr(dynamicControlObj, ln = "stiffness", at = "double", min = 0, max = 1, dv = 0.001, keyable = True)
    #if earSideLong == "left":
    addAttr(dynamicControlObj, ln = "drag", at = "double", min = 0, max = 1, dv = 0.1, keyable = True)
    addAttr(dynamicControlObj, ln = "damp", at = "double", min = 0, max = 10, dv = 0.05, keyable = True)
    addAttr(dynamicControlObj, ln = "gravity", at = "double", min = 0, max = 20, dv = 9.8, keyable = True)
    addAttr(dynamicControlObj, ln = "windCtrl", at = "bool", keyable = True)
    setAttr(dynamicControlObj + ".windCtrl", lock = True)
    addAttr(dynamicControlObj, ln = "windSpeed", at = "double", min = 0, max = 1000, dv = 0, keyable = True)
    addAttr(dynamicControlObj, ln = "windDirectionX", at = "double", min = -100, max = 100, dv = 1, keyable = True)
    addAttr(dynamicControlObj, ln = "windDirectionY", at = "double", min = -100, max = 100, dv = 0, keyable = True)
    addAttr(dynamicControlObj, ln = "windDirectionZ", at = "double", min = -100, max = 100, dv = 0, keyable = True)
    addAttr(dynamicControlObj, ln = "windNoise", at = "double", min = 0, max = 100, dv = 0, keyable = True)
    
    
    
        # extra attributes to be deleted with dynamics
    addAttr(dynamicControlObj, ln = "nameOfDynCurve", dt = "string", keyable = False)
    setAttr(dynamicControlObj + ".nameOfDynCurve", fkDynCurve,  type = "string", lock = True)
    addAttr(dynamicControlObj, ln = "nameOfFollicleNode", dt = "string", keyable = False)
    setAttr(dynamicControlObj + ".nameOfFollicleNode", follicleNode,  type = "string", lock = True)
    #if earSideLong == "left":
    addAttr(dynamicControlObj, ln = "nameOfHairSystemNode", dt = "string", keyable = False)
    setAttr(dynamicControlObj + ".nameOfHairSystemNode", hairSystemNode,  type = "string", lock = True)
    addAttr(dynamicControlObj, ln = "baseJoint", dt = "string", keyable = False)
    setAttr(dynamicControlObj + ".baseJoint", dynJointRelatives[0],  type = "string", lock = True)
    addAttr(dynamicControlObj, ln = "endJoint", dt = "string", keyable = False)
    setAttr(dynamicControlObj + ".endJoint", dynJointRelatives[5],  type = "string", lock = True)
    
    # connect dynamic attributes from controller object to follicle/hairSystem/Nucleus nodes
    #connectAttr(dynamicControlObj + ".enableDynamics", nucleusNode + ".enable", force = True)
    connectAttr(dynamicControlObj + ".spaceScale", nucleusNode + ".spaceScale", force = True)
    connectAttr(dynamicControlObj + ".stiffness", hairSystemNode + ".stiffness", force = True)
    #if earSideLong == "left":
    connectAttr(dynamicControlObj + ".drag", hairSystemNode + ".drag", force = True)
    connectAttr(dynamicControlObj + ".damp", hairSystemNode + ".damp", force = True)
    connectAttr(dynamicControlObj + ".gravity", nucleusNode + ".gravity", force = True)
    connectAttr(dynamicControlObj + ".windSpeed", nucleusNode + ".windSpeed", force = True)
    connectAttr(dynamicControlObj + ".windDirectionX", nucleusNode + ".windDirectionX", force = True)
    connectAttr(dynamicControlObj + ".windDirectionY", nucleusNode + ".windDirectionY", force = True)
    connectAttr(dynamicControlObj + ".windDirectionZ", nucleusNode + ".windDirectionZ", force = True)
    connectAttr(dynamicControlObj + ".windNoise", nucleusNode + ".windNoise", force = True)
    
    
    # cleanup unused nodes (replace with cleanup procedureH
    setAttr(dynamicControlObj + ".tx", lock = True, keyable = False)
    setAttr(dynamicControlObj + ".ty", lock = True, keyable = False)
    setAttr(dynamicControlObj + ".tz", lock = True, keyable = False)
    setAttr(dynamicControlObj + ".rx", lock = True, keyable = False)
    setAttr(dynamicControlObj + ".ry", lock = True, keyable = False)
    setAttr(dynamicControlObj + ".rz", lock = True, keyable = False)
    setAttr(dynamicControlObj + ".sx", lock = True, keyable = False)
    setAttr(dynamicControlObj + ".sy", lock = True, keyable = False)
    setAttr(dynamicControlObj + ".sz", lock = True, keyable = False)
    
    # ear control
    earControl = rename( earSide + "_ear_ctrl", earSide + "_ear_ctrl" + charName)
    delete(parentConstraint(mainChain, earControl, maintainOffset = False))
    earControlGrp = group(empty = True, name = earSide + "_ear_ctrl_grp" + charName)
    delete(parentConstraint(mainChain, earControlGrp, maintainOffset = False))
    parent(earControl, earControlGrp)
    makeIdentity(earControl, apply = True, t = True, r = True, s = True)
    parent(nulls[0], earControl)
    parentConstraint(earControl, root, mo = True)
    parentConstraint(earControl, dynamicChain, maintainOffset = True)
    #parentConstraint(earControl, fkDynCurve, maintainOffset = True)
    
    
    # create joint orient constraints to main joint chain
    #orientConstraint(root, dynamicChain, mainChain, mo = False)
    m = 0
    for each in jointRelatives:
        
    
        if m > len(jointRelatives):
            break    
        if m != 0 or -1:
            orientConstraint(jointRelatives[m], dynJointRelatives[m], mainJointRelatives[m], mo = False)
            m+=1
    parentConstraint(earControl, earSide + '_Main_Ear_root' + charName, mo = True)
    
    # setup FK/Dynamic switch
    addAttr(earControl, ln = "fkDynamicSwitch", at = "double", min = 0, max = 10, dv = 0, keyable = True)
    
    fkSrn = createNode("setRange", n = earSide + '_ear_fk_srn' + charName)
    connectAttr(earControl + '.fkDynamicSwitch', fkSrn + '.valueX')
    setAttr(fkSrn + '.minX', 1)
    setAttr(fkSrn + '.oldMaxX', 10)
    
    ikSrn = createNode("setRange", n = earSide + '_ear_ik_srn' + charName)
    
    connectAttr(earControl + '.fkDynamicSwitch', ikSrn + '.valueX')
    setAttr(ikSrn + '.maxX', 1)
    setAttr(ikSrn + '.oldMaxX', 10)
    
    n = 0
    for each in range(0, 5):
        connectAttr(fkSrn + '.outValueX', mainJointRelatives[n] + '_orientConstraint1.' + jointRelatives[n] + 'W0', force = True)
        connectAttr(ikSrn + '.outValueX', mainJointRelatives[n] + '_orientConstraint1.' + dynJointRelatives[n] + 'W1', force = True)
        n+=1
        
    # add a dynamic amount attribute
    addAttr(earControl, ln = "dynamicAmount", at = "double", min = 0, max = 10, dv = 0, keyable = True)
    dynSrn = createNode('setRange', n = earSide + '_dynamic_amt_srn' + charName)
    connectAttr(earControl + '.dynamicAmount', dynSrn + '.valueX')
    setAttr(dynSrn + '.minX', 1)
    setAttr(dynSrn + '.oldMaxX', 10)
    connectAttr(dynSrn + '.outValueX', hairSystemNode + ".startCurveAttract", force = True)
    setAttr(hairSystemNode + '.attractionDamp', 1)
    
    # add an attribute to control the dynamic start frame
    addAttr(earControl, ln = "startFrame", at = "long", dv = 1, keyable = True)
    connectAttr(earControl + '.startFrame', nucleusNode + '.startFrame')
    
    
        # token
    earTokens = group(empty = True, name = earSide + "_ear_token" + charName)      
    print "HEY THE %s HAS BEEN MADE!" % (earTokens)
    

        
def pxBuildEars():
    
    pxUtilities.mirrorJoints("l_ear_fk_root")   
    pxBuildEarSide("left")
    pxBuildEarSide("right")

