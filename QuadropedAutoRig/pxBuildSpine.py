from ui import *
from buildScripts import pxUtilities

def pxBuildSpine():
    charName = queryCharName()
    #charName = "_OldGoat"
    rootJoint = "root_jnt" + charName
    pxUtilities.orientJoints(rootJoint, "xyz", "yup")        
    #the listrelatives command stores the joint hierarchy - not the root though
            
    joints = listRelatives(rootJoint, c = 1, ad = 1)

    #this for loop is used to rename the joints

    counter = len(joints)

    for each in joints:

        rename( each, "spine" + str(counter) + "_jnt" + charName)
        counter -= 1
            
    #create an empty array to temporarily hold world space positions		
    pos = []

    #-----------------------------this part of the script creates the fk jnts -----------------------------#


    # the gen. idea here is to find the worldSpace position - create a joint - 
        #then move it into position with the absolute move command



    select(cl = 1)  # these clear selections are very important!!! without them the joint tool will parent to the currently selected joint

    #Flag short hand key:
        #q = query, rp = rotatepivot, ws = worldspace


    pos =  xform(rootJoint, q = True, rp = True, ws = True)

    #creating the fk joints - im color coding them - yellow
    FKspineBack2Joint = cmds.joint(n = "FK_spine_back2_jnt" + charName) 
    pxUtilities.setColorAndRadius(FKspineBack2Joint, "yellow", 1) #custom def for activating drawing overrides, adding colors, and setting the radius of the joints
    cmds.move(pos[0], pos[1], pos[2], FKspineBack2Joint, a = 1)
    select(cl = 1)
    #cmds.xform(  FKspineBack2Joint, r=True, ws = True, t=(pos[0], pos[1], pos[2] )

    #find and place a joint at the shoulder
    pos = xform(joints[0], q = 1, rp = 1, ws = 1) 
    select( joints[0] )
    #cmds.spaceLocator( p=(pos[0], pos[1], pos[1]),r = 0, a = True )

    FKspineFront3Joint =  cmds.joint(n = "FK_spine_front3_jnt" + charName)
    pxUtilities.setColorAndRadius(FKspineFront3Joint, "yellow", 1)
    cmds.move(pos[0], pos[1], pos[2], FKspineFront3Joint, a = 1)
    select(cl = 1)



    FKspineBack1Joint = cmds.joint(n = "FK_spine_back1_jnt" + charName)
    pxUtilities.setColorAndRadius(FKspineBack1Joint,"yellow", 1) 
    #here we create a constraint to find the center point between the front and end of the joints
    tempConstraint = pointConstraint(FKspineBack2Joint, FKspineFront3Joint, FKspineBack1Joint)
    # setting the parent constraint to 3 .5 positions it correctly //yellow flag here for the pymel translation
    setAttr((tempConstraint + ".w0"), 3.5)
    #delete the parent constraint - contsraints are created in an array - THEY ARE NOT ITEM 0 in pymel
    delete(tempConstraint)


    #same technique used here with parent constraint - also duplicting and renaming in one swoop...fancy

    FKspineFront1Joint = duplicate(FKspineBack1Joint, rr = 1, rc = 1, n = "FK_spine_front1_jnt" + charName)[0]

    
    pxUtilities.setColorAndRadius(FKspineFront1Joint, "yellow", 2.2)
    select(cl = 1)	

    FKspineFront2Joint = joint(n = "FK_spine_front2_jnt" + charName)
    pxUtilities.setColorAndRadius(FKspineFront2Joint, "yellow", 1)
    tempConstraint = pointConstraint(FKspineBack2Joint, FKspineFront3Joint, FKspineFront2Joint)
    setAttr((tempConstraint + ".w1"), 1.1)
    delete(tempConstraint)
    select(cl = 1)

    #parents the newly created fk joints - see joint diagram < 0 < 0 < 00 > 0  
    parent(FKspineBack2Joint, FKspineBack1Joint)
    parent(FKspineFront3Joint, FKspineFront2Joint)
    parent(FKspineFront2Joint, FKspineFront1Joint)

    #-----------------------this part of the script creates the ik joints-------------------------#

    select(cl = 1)	

    #create ik joints - im color coding them  - red

    ikJoint1 = joint(n = "spine_IK_jnt1" + charName)
    pxUtilities.setColorAndRadius(ikJoint1, "red", 2.4)
    tempConstraint = pointConstraint(rootJoint, ikJoint1)
    delete (tempConstraint)	
    select(cl = 1)

    ikJoint3 = joint(n = "spine_IK_jnt3" + charName)
    pxUtilities.setColorAndRadius(ikJoint3, "red", 2.4)
    tempConstraint = pointConstraint(joints[0], ikJoint3)
    delete (tempConstraint)
    select(cl = 1)

    #we wont place this last joint until we have more information on where the ikspline curve(cvs) will be located
        #for now we'll just create it and set its drawing overides
    ikJoint2 = "spine_IK_jnt2" + charName
    ikJoint2 = joint(n = ikJoint2)
    pxUtilities.setColorAndRadius(ikJoint2, "red", 2.4)

    # here are some very important ikHandle settings iknow very little about :)

    ikHandleName = ("spine_IKhandle" + charName)

    ikHandle(createCurve = 1, 
        startJoint = rootJoint, 
        endEffector = joints[0], 
        rootOnCurve = 1, 
        parentCurve = 0, 
        solver = "ikSplineSolver", 
        simplifyCurve = 1, 
        name = ikHandleName,
        twistType = "linear", 
        numSpans = 1
        )


    #Fetching and renaming the -effector & curve- created by the spline ik:

        #effector
    catcherSpineIKEffector = listConnections (ikHandleName)[1]
    rename(catcherSpineIKEffector, ("spine_IKeffector" + charName))
        #curve
    catcherSpineIKCurve = listConnections (ikHandleName)[3]
    rename(catcherSpineIKCurve, ("spine_curve" + charName))

    #----------------------this part of the script creates the animation controls--------------------------------




    #create the actual nurbs curves - note we are using the user scale variable
    hipCtrl = "pelvis_ctrl" + charName 
    torsoCtrl = "torso_ctrl" + charName
    shoulderCtrl = "shoulder_ctrl" + charName
    fkBackCtrl1 = "fkBack1_ctrl" + charName
    fkBackCtrl2 = "fkBack2_ctrl" + charName
    fkBackCtrl3 = "fkBack3_ctrl" + charName
    #nodeType(fkBackCtrl3)
    #here we are setting all the rotations on the controls to zxy- I dont know exactly why we dothis. Might be a gimbal thing or have to do with the advanced twist???
    setAttr((hipCtrl + ".rotateOrder"), 2)
    setAttr((torsoCtrl + ".rotateOrder"), 2)
    setAttr((shoulderCtrl + ".rotateOrder"), 2) 
    setAttr((fkBackCtrl1 + ".rotateOrder"), 2)
    setAttr((fkBackCtrl2 + ".rotateOrder"), 2)
    setAttr((fkBackCtrl3 + ".rotateOrder"), 2)

    # Using a parent constraints to position controls onto the joints

        #hip
    tempConstraint = pointConstraint(rootJoint, hipCtrl)
    delete(tempConstraint)
        #shoulder
    tempConstraint = pointConstraint(joints[0], shoulderCtrl)
    delete(tempConstraint)

    #Here we'll get the average position of the middle CVs of the spine curve to find the torso controls position
    select(catcherSpineIKCurve)
    mel.selectCurveCV("all") #taking advantage of a mel only script
    sel = ls(sl = 1, fl = 1)  #-flatten(-fl) = "Flattens the returned list of objects so that each component is identified individually." No "cv[0:3]" results


    #finding the average position of the two middle cvs of the curve - coords in worldspace. Find the average of the two points by adding them and /2  
    cv1Pos = xform(sel[1], q = 1, ws = 1, t = 1)
    cv2Pos = xform(sel[2], q = 1, ws = 1, t = 1)


    avgPos0 = ((cv1Pos[0] + cv2Pos[0]) / 2)
    avgPos1 = ((cv1Pos[1] + cv2Pos[1]) / 2)
    avgPos2 = ((cv1Pos[2] + cv2Pos[2]) / 2)
    placementOfTorsoCtrl = spaceLocator( p=(avgPos0, avgPos1, avgPos2) )
    xform(placementOfTorsoCtrl,cp = True)
    tempConstraint = parentConstraint(placementOfTorsoCtrl , torsoCtrl)
    delete (tempConstraint, placementOfTorsoCtrl)
    #cmds.move(((cv1Pos[0] + cv2Pos[0]) / 2), ((cv1Pos[1] + cv2Pos[1]) / 2), ((cv1Pos[2] + cv2Pos[2]) / 2), torsoCtrl , a = 1 , ws = 1)



    select(cl = 1)

    #position the middle ik joint from earlier at the same place as the torso ctrl
    tempConstraint = pointConstraint(torsoCtrl, ikJoint2)
    delete(tempConstraint)


    #this part deals with positioning the "shadow fk ctrls" -little confused what these are for
    tempConstraint = pointConstraint(torsoCtrl, shoulderCtrl, fkBackCtrl3)
    setAttr((tempConstraint + ".w0"), 3)
    delete(tempConstraint)

    #same - I think they may be used as a pivot point of some sort for the main fk joints 
    tempConstraint = pointConstraint(hipCtrl, torsoCtrl, fkBackCtrl1)
    setAttr((tempConstraint + ".w0"), 2)
    delete(tempConstraint)

    tempConstraint = pointConstraint(hipCtrl, torsoCtrl, fkBackCtrl2)
    setAttr((tempConstraint + ".w1"), 1.5)
    delete(tempConstraint)

            #name the control  - this need to be scripted - need a better control making system
    bodyCtrl = "body_ctrl" + charName


    tempConstraint = pointConstraint(FKspineBack1Joint, bodyCtrl)
    delete (tempConstraint)
    makeIdentity(bodyCtrl, a = 1, s = 1, r = 1, t = 1)

    addAttr(bodyCtrl, ln = "controls", k = 1, en = "-:", at = "enum")
    setAttr((bodyCtrl + ".controls"))
    addAttr(bodyCtrl, ln = "show_FK", k = 1, en = "off:on:", at = "enum")
    addAttr(bodyCtrl, ln = "show_IK", k = 1, en = "off:on:", at = "enum")
    #orient the fk controls to the fk joints - I think were using orients constriants to match the controls 
    #to the correct orrientation of the joints 



    tempConstraint = orientConstraint(FKspineBack1Joint, fkBackCtrl1)
    delete (tempConstraint)
    tempConstraint = orientConstraint(FKspineBack1Joint, fkBackCtrl2)
    delete (tempConstraint)
    tempConstraint = orientConstraint(FKspineBack1Joint, fkBackCtrl3)
    delete (tempConstraint) 


    #applying the pxUtilities.pXGroupControl script to create null grps above the controls
    hipCtrlGrp = pxUtilities.pXGroupControl(hipCtrl)
    torsoCtrlGrp = pxUtilities.pXGroupControl(torsoCtrl)

    #duplicate the torso ctrl twice.
    #we dont use the pxUtilities.pXGroupControl here because there are two groups that need to be made from the same ctrl
    #screws up naming otherwise

    dupTorso1 = duplicate(torsoCtrl)
    rename (dupTorso1, ("torso_constGrp1" + charName))
    dupTorso1Shape = listRelatives(dupTorso1, s = 1)
    delete(dupTorso1Shape)

    dupTorso2 = duplicate(torsoCtrl)
    rename (dupTorso2, ("torso_constGrp2" + charName))
    dupTorso2Shape = listRelatives(dupTorso2, s = 1)
    delete(dupTorso2Shape)	


    #continue with the control grouping
    shoulderCtrlGrp = pxUtilities.pXGroupControl(shoulderCtrl )
    FKbackCtrlGrp1 = pxUtilities.pXGroupControl(fkBackCtrl1) # the shadow controls
    FKbackCtrlGrp2 = pxUtilities.pXGroupControl(fkBackCtrl2)
    FKbackCtrlGrp3 = pxUtilities.pXGroupControl(fkBackCtrl3)


    #parent the torso const groups to the hip and shoulder control - this is important !!!! 
    # not sure 100% whats happening here
        #its setting up pivot points at the torso
            
    parent(dupTorso1, hipCtrl)
    parent(dupTorso2, shoulderCtrl)

    #this command creates a point constraint that makes the grp above torso follow the torso constraint grps(tcg's). 
        #The tcg's are parented under the shoulder and hip ctrls ... hmmm .. see above note
    pointConstraint(dupTorso1, dupTorso2, torsoCtrlGrp, mo = 1)
        #the pivot are definetly playing a role in the smooth movement


    #next - bind the ik joints to the spline curve -we can adjust the weights her as well
    select(ikJoint1, ikJoint2, ikJoint3, r = 1)


    #creates a new skin cluster based on the selected joints
    spineSkinCluster = skinCluster( ikJoint1, ikJoint2, ikJoint3, catcherSpineIKCurve, 
        toSelectedBones = 1, 
        rui = 1, #remove Unused Influence
        omi = 1, #obey max influence
        mi = 1, # max influence
        dr = 4, #dropoffrate
        n = ("skinCluster_spine" + charName))

    #now we can name the components that come along with the skincluster
        #use list connections to gater the data
    catcherClusterConnections = listConnections(spineSkinCluster, shapes = 1, d = 1)# including shape node
        # creates a set - removes duplicate items from the list
    clusterConnections = list(set(catcherClusterConnections))  

        #name the associated bind pose
    for current in clusterConnections:

        #take advantage of pymels node type option
        if nodeType(current) ==  "dagPose":
            rename(current, "bindPose_spine" + charName)
        
        if nodeType(current) ==  "objectSet":
            rename(current , ("spine_skinClusterSet" + charName)) 

        #Also name the associated tweak node		
    shape = listRelatives(catcherSpineIKCurve, s = 1)
    tweak = listConnections(shape[0] + ".tweakLocation"	)
    rename (tweak, "tweak_spine" + charName) 	


        
    #using a for loop to arrange joints into the correct format for the stretchy spine proc

    jointString = rootJoint

    #jointString should = "A:B:C:D:E:ect" string format # or root_jnt_OldGoat:spine1_jnt_OldGoat:spine12_jnt_OldGoat:ect...
    counter = len(joints)-1
    for each in joints:
        
        jointString = jointString + ":" + joints[counter] 
        counter -=  1

        
    joints.reverse()
    joints =  ['rootJoint'] + joints



    #$charName = "_OldGoat";
    #string $type = "spine";
    #string $curve = "spine_curve_OldGoat";
    #string $jString = "root_jnt_OldGoat:spine1_jnt_OldGoat:spine2_jnt_OldGoat:spine3_jnt_OldGoat:spine4_jnt_OldGoat:spine5_jnt_OldGoat:spine6_jnt_OldGoat:spine7_jnt_OldGoat:spine8_jnt_OldGoat";

    prefix = "spine"


    divideNode = pxUtilities.pxStretchySplineIk(prefix, catcherSpineIKCurve, joints, charName)



    #back to reality here
    parent(ikJoint1, hipCtrl)
    parent(ikJoint3, shoulderCtrl)
    parent(ikJoint2, torsoCtrl)
    #move the FK control pivots to the FK joints
    pos = xform(FKspineBack1Joint, q = 1, rp = 1, ws = 1)
    cmds.move(pos[0], pos[1], pos[2], (fkBackCtrl1 + ".scalePivot"), (fkBackCtrl1 + ".rotatePivot"))

    pos = xform(FKspineFront1Joint, q = 1, rp = 1, ws = 1)
    cmds.move(pos[0], pos[1], pos[2], (fkBackCtrl2 + ".scalePivot"), (fkBackCtrl2 + ".rotatePivot"))

    pos = xform(FKspineFront2Joint, q = 1, rp = 1, ws = 1)
    cmds.move(pos[0], pos[1], pos[2], (fkBackCtrl3 + ".scalePivot"), (fkBackCtrl3 + ".rotatePivot"))

    #parent constrain the hip and shoulder control to the corresponding FK joints
    parentConstraint(FKspineFront3Joint, shoulderCtrlGrp, mo = 1)
    #parent constrain the hip and shoulder control to the corresponding FK joints
    parentConstraint(FKspineBack2Joint, hipCtrlGrp, mo = 1)
    #connect the FK controls with the FK joints  - these are not cisible 
    connectAttr((fkBackCtrl1 + ".r"), (FKspineBack1Joint + ".r"), f = 1)   #type(FKspineBack1Joint)
    connectAttr((fkBackCtrl2 + ".r"), (FKspineFront1Joint + ".r"), f = 1)   #type(FKspineFront1Joint)
    connectAttr((fkBackCtrl3 + ".r"), (FKspineFront2Joint + ".r"), f = 1)
    #enable the advanced twist and make the connections to the controls - yikes


    #Here are some very important advanced twist options

    connectAttr((hipCtrl + "Shape.worldMatrix[0]"), (ikHandleName + ".dWorldUpMatrix")) 
    connectAttr((shoulderCtrl + "Shape.worldMatrix[0]"), (ikHandleName + ".dWorldUpMatrixEnd"))
    setAttr((ikHandleName + ".dTwistControlEnable"), 1)
    setAttr((ikHandleName + ".dWorldUpType"), 4)
    #create a group for the FK joints

    FKspineJointsGrp = str(createNode('transform', n = ("FK_spine_joints_grp" + charName)))


    tempConstraint = pointConstraint(FKspineBack1Joint, FKspineJointsGrp)
    delete(tempConstraint)


    parent(FKspineBack1Joint, FKspineFront1Joint, FKspineJointsGrp)
    parentConstraint(bodyCtrl, FKspineJointsGrp, mo = 1)


    
    spineControlsGrp = pxUtilities.pxCreateOrganizationGroup(charName, "spine_controls_grp")
    animationControlsGrp = pxUtilities.pxCreateOrganizationGroup(charName, "animationControls_grp")


    parent(bodyCtrl, spineControlsGrp)
    parent(hipCtrlGrp, bodyCtrl)
    parent(torsoCtrlGrp, bodyCtrl)
    parent(shoulderCtrlGrp, bodyCtrl)
    parent(FKbackCtrlGrp1, bodyCtrl)
    parent(FKbackCtrlGrp2, bodyCtrl)
    parent(FKbackCtrlGrp3, bodyCtrl)

    dontTouchJointsGrp = pxUtilities.pxCreateOrganizationGroup(charName, "dontTouchJoints_grp")
    spineJointsGrp = pxUtilities.pxCreateOrganizationGroup(charName, "spineJoints_grp")

    print spineJointsGrp
    print dontTouchJointsGrp
    parent(spineJointsGrp, dontTouchJointsGrp)
    parent(rootJoint, spineJointsGrp)
    parent(FKspineJointsGrp, spineJointsGrp)

    dontTouchGrp = pxUtilities.pxCreateOrganizationGroup(charName, "dontTouch_grp")
    characterGrp = pxUtilities.pxCreateOrganizationGroup(charName, "character_grp")  
  
    parent(catcherSpineIKCurve, dontTouchGrp)
    parent(ikHandleName, dontTouchGrp)
    
    parent(("characterScale_grp" + charName), characterGrp)
    parent(animationControlsGrp, ("characterScale_grp" + charName))
    parent(spineControlsGrp, animationControlsGrp)
    parent(dontTouchJointsGrp, ("characterScale_grp" + charName))
    parent(dontTouchGrp, ("characterScale_grp" + charName))

            #add the neck attributes
    addAttr(shoulderCtrl, ln = "neck_status", k = 1, en = "IK:FK:", at = "enum")
    setAttr((shoulderCtrl + ".neck_status"), 1)
    addAttr(shoulderCtrl, min = 0, ln = "neckFollow", max = 1, k = 1, at = "float", dv = 0)
    addAttr(hipCtrl, min = 0, ln = "tailFollow", max = 1, k = 1, at = "float", dv = 0)

   
   

    #Warning Symbol for overStretch

    warningMark = "StretchWarning_Spine"
    tempConstraint = parentConstraint (bodyCtrl, warningMark )
    delete(tempConstraint)


    overStretchConditionNode = shadingNode("condition", asUtility = True, n = "%s_OverStretch%s" %(prefix, charName))
    setAttr(overStretchConditionNode + ".operation", 2) # greater then
    setAttr(overStretchConditionNode + ".secondTerm", 1.2) #a vale of 1.5 will activate stretch warning
    setAttr(overStretchConditionNode + ".colorIfTrueR", 1)
    setAttr(overStretchConditionNode + ".colorIfFalseR", 0)

    addStretchAttr = [shoulderCtrl, torsoCtrl, hipCtrl, bodyCtrl] 

    for each in addStretchAttr:
        print each
        cmds.addAttr( each, ln="spineStretch",dv=1,at='double', k = True)	
        cmds.connectAttr ((divideNode + ".outputX"),(each + ".spineStretch"))


    connectAttr((divideNode + ".outputX"),(overStretchConditionNode + ".firstTerm"))
    connectAttr((overStretchConditionNode + ".outColorR" ),(warningMark + ".visibility"))

    parent ( warningMark, bodyCtrl)

    #heres the back token the spine uses for
    
    backToken = group(empty = True, name = "back_token" + charName )
    print "HEY THE %s HAS BEEN MADE!" % (backToken)






    #tested up until here
            
    ##------------------------------------------------------------------------------------------------	
            
            
            
    print "Spine script finished execution!!!"        
            
            
   
