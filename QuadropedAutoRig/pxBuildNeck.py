from ui import *
from buildScripts import pxUtilities


#def's
def pxBuildNeck():    
        
    #variables 
    rootJoint = "neck_root"
    charName = queryCharName()
    #charName = '_YoungGoat'
    #prepare the original chain
    #orient the strat Joints and delete the head joint it is not needed after orient'
        
    pxUtilities.orientJoints(rootJoint, "xyz", "yup")
    delete("neck_05_jnt")

    #fk
        
    #create the fk joint chain
       
    fkRootJoint = duplicate(rootJoint, n = "neck_fk_rootjnt" + charName, rc = True)[0] 
    fkJointCatcher = listRelatives(fkRootJoint, c = 1, ad = 1)
    fkJointCatcher.reverse() #listConnection works backwards -reverse
    fkJoints = []

    #rename the fk joints

    counter = 1
    for each in fkJointCatcher:

        renamedItem = rename(each, "neck_fk" + str(counter) + "_jnt" + charName)
        fkJoints.append(renamedItem)

        counter +=1   
        
    fkJoints = [fkRootJoint]  + fkJoints

    for each in fkJoints:

        pxUtilities.setColorAndRadius(each,'yellow',1.5)
        
        
    #KSANA******************************* setup all the fk null grps and their controls
    fkAllNeckCtrl = 'AllNeck_Ctrl' + charName
    fkNeckCtrl1 = 'FK_neckCtrl1' + charName
    fkNeckCtrl2 = 'FK_neckCtrl2' + charName
    fkNeckCtrl3 = 'FK_neckCtrl3' + charName
    fkNeckCtrl4 = 'FK_neckCtrl4' + charName
    fkHeadCtrl = 'FK_headCtrl' + charName

    fkCtrls = [fkNeckCtrl1,fkNeckCtrl2,fkNeckCtrl3,fkNeckCtrl4,fkHeadCtrl]



    #KSANA************** add the Ik controls similar to way we did fk control

    dupList = [fkAllNeckCtrl,fkNeckCtrl2,fkHeadCtrl]
    ikCtrls = ['ikBtmNeckCtrl' + charName,'ikMidCtrl' + charName,'ikHeadCtrl' + charName]
    print ikCtrls
    select (dupList)
    i = 0
    for each in dupList:
        dup =  duplicate(each,rc = True, name = ikCtrls[i])[0]
        
        i += 1


          

    #set up the allNeckControl

    allNeckPivotGrp = 'allNeck_pivot_grp' + charName
    tempConstraint = orientConstraint (fkJoints[0],allNeckPivotGrp)
    delete (tempConstraint)
    delete (allNeckPivotGrp + "Shape")
    tempConstraint = pointConstraint(allNeckPivotGrp, fkAllNeckCtrl)
    delete (tempConstraint)


    allNeckPreGrp = duplicate (allNeckPivotGrp, name = 'AllNeck_Pre_Grp')
    allNeckConstraintGrp = duplicate (allNeckPivotGrp, name = 'AllNeck_Constraint_Grp')
    parent (allNeckConstraintGrp,allNeckPreGrp)
    parent (allNeckPivotGrp, allNeckConstraintGrp)
    parent (fkAllNeckCtrl,allNeckPivotGrp)
    makeIdentity(fkAllNeckCtrl,n=0,s=1,r=1,t=1,apply=True,pn=1)

    
    #pxUtilities.pXGroupControl(fkAllNeckCtrl)


    grps = []

    i = 0



    for each in fkCtrls:
            
        
        tempConstraint = parentConstraint(fkJoints[i], each)
        
        delete(tempConstraint)
        parentConstraint(each,fkJoints[i])
        grp = pxUtilities.pXGroupControl(each)
        grps.append(grp)
        i += 1

    #KSANA******************************* parent the controls accordingly      

    i = 0

    for each in range(0,len(grps)):
            parent (grps[i+1],fkCtrls[i])
            i += 1
            if i == (len(grps))-1:
                break
    parent(grps[0],fkAllNeckCtrl)

    #ik stuff

    #create the ik Chain (for use as spline ik joints)
    ikRootJoint = duplicate(rootJoint, n = "neck_ik_rootjnt" + charName, rc = True)[0] 
    ikJointCatcher = listRelatives(ikRootJoint, c = 1, ad = 1)
    ikJointCatcher.reverse()
    ikJoints = []

    #rename the other ik joints
    counter = 1
    for each in ikJointCatcher:

        renamedItem = rename(each, "neck_ik" + str(counter) + "_jnt" + charName)
        ikJoints.append(renamedItem)

        counter +=1   

    #add ikRoot to the list    
    ikJoints = [ikRootJoint]  + ikJoints
    print ikJoints
    for each in ikJoints:

        pxUtilities.setColorAndRadius(each,'blue', 1.5)
        
        
        
    #Creating Spline ik bind Joints (add pre groups to eliminate transforms)


    select(cl = 1)
    bindJointBtm = joint(n = "neck_ik_bind_jntBtm" + charName)
    pxUtilities.setColorAndRadius(bindJointBtm,'red', 2)
    #KSANA*********************#create a new group for the ik bind joint *****************************
    bindJointBtmGrp = group(bindJointBtm, n = 'bindJointBtm_grp')
    tempConstraint = parentConstraint(fkJoints[0], bindJointBtmGrp)
    delete(tempConstraint)



    select(cl = 1)
    bindJointMid = joint(n = "neck_ik_bind_jntMid" + charName)#For loop for next time!
    pxUtilities.setColorAndRadius(bindJointMid,'red', 2)
    #create a new pregroup for the ik bind joint ****************************
    bindJointMidGrp = group(bindJointMid, n = 'bindJointMid_grp')
    #orient the middle joint the same way the base is
    tempConstriant = orientConstraint (fkJoints[0],bindJointMidGrp)
    delete (tempConstriant)
    #move it to the right spot
    tempConstraint = pointConstraint(fkJoints[-1],fkJoints[0],bindJointMidGrp)
    delete(tempConstraint)


    select (cl = 1)
    bindJointTop = joint(n = "neck_ik_bind_jntTop" + charName)
    pxUtilities.setColorAndRadius(bindJointTop,'red', 2)
    #KSANA*********************#create a new pre group for the ik bind joint *****************************
    bindJointTopGrp = group(bindJointTop, n = 'bindJointTop_grp')
    tempConstraint = parentConstraint(fkJoints[-1],bindJointTopGrp)
    delete(tempConstraint)
    select(cl = 1)
    bindJoints  = [bindJointBtm, bindJointMid, bindJointTop]


      
    #Position IK controls to bind joints
    xform(ikCtrls[0],cp = True)
    select (ikCtrls[0])
    tempConstraint = parentConstraint(bindJointBtm,ikCtrls[0])
    delete(tempConstraint)
    delete(ikCtrls[0] + "Shape")

    #move the controls to the ikBind joints

    tempConstraint = parentConstraint(bindJointMid,ikCtrls[1])
    delete(tempConstraint)
    preGrp = group (empty = True, name = ikCtrls[1] + "_preGrp")
    tempConstraint = parentConstraint(bindJointMid,preGrp)
    delete(tempConstraint)
    ikMidConstraintGrp = group (empty = True, name = ikCtrls[1] + "_constraintGrp")
    tempConstraint = parentConstraint(bindJointMid,ikMidConstraintGrp)
    delete(tempConstraint)
    parent (ikMidConstraintGrp, preGrp)
    parent (ikCtrls[1],ikMidConstraintGrp)

    tempConstraint = parentConstraint(bindJointTop,ikCtrls[-1])
    select (bindJointTop)
    delete(tempConstraint)


    #Constraining IK controls to bind Joints
    parentConstraint(ikCtrls[0],bindJointBtm)
    parentConstraint(ikCtrls[1],bindJointMid)
    parentConstraint(ikCtrls[-1],bindJointTop)

    #pxUtilities.pXGroupControl(ikCtrls[1])
    #make sure the mid joint knows where to be in space

    pointConstraint(ikCtrls[0],ikCtrls[-1],ikMidConstraintGrp , name = ikCtrls[-1] + "_pointConstraint"  )
    aimConstraint(ikCtrls[-1],ikMidConstraintGrp, name = ikCtrls[-1] + "_aimConstraint" )
    parentConstraint (fkAllNeckCtrl, ikCtrls[0], mo = True)




    preGrp = group (empty = True, name = ikCtrls[-1] + "_preGrp")
    tempConstraint = parentConstraint(bindJointTop,preGrp)
    delete(tempConstraint)
    ikHeadConstraintGrp = group (empty = True, name = ikCtrls[-1] + "_constraintGrp")
    tempConstraint = parentConstraint(bindJointTop,ikHeadConstraintGrp)
    delete(tempConstraint)
    parent (ikHeadConstraintGrp, preGrp)
    parent (ikCtrls[-1],ikHeadConstraintGrp)




    #create the Ik spline handle 
        
    ikHandleName = ("neck_ikhandle" + charName)
    ikHandleCatcher = ikHandle(createCurve = 1, 
        startJoint = ikJoints[0],                     
        endEffector = ikJoints[-1], 
        rootOnCurve = 1, 
        parentCurve = 0, 
        solver = "ikSplineSolver", 
        simplifyCurve = 1, 
        name = ikHandleName,
        twistType = "linear", 
        numSpans = 1
        )

    #Fetching and renaming effector and curve created by spline ik#
            
    #rename effector
    catcherNeckikEffector = listConnections (ikHandleName)[1]
    rename(catcherNeckikEffector, ("neck_ikeffector" + charName))

    #rename curve
    catcherNeckikCurve = listConnections (ikHandleName)[3]#this prints out a the third item in the list, in this case the curve
    rename(catcherNeckikCurve, ("neck_curve" + charName))

    #attach stretchy to ik spline
    prefix = "neck"
    divideNode = pxUtilities.pxStretchySplineIk(prefix, catcherNeckikCurve, ikJoints, charName)            

    #bind the bindJoints to the spline Curve

    select(bindJointBtm,bindJointMid, bindJointTop, catcherNeckikCurve)
    neckSkinCluster = skinCluster(
        toSelectedBones = 1, 
        rui = 1, #remove Unused Influence
        omi = 1, #obey max influence
        mi = 1, # max influence
        dr = 4, #dropoffrate
        n = ("skinCluster_neck" + charName))

    #create the main joints that will get their influence from the ik spline joints 
    mainJointRoot = duplicate(ikJoints[0], name = "Main_Neck_jnt1" + charName ,rc = True)[0]
    mainJoints = listRelatives(mainJointRoot, ad = True,c = True)

    for each in mainJoints:
        if nodeType(each) == "ikEffector":
            delete(each)
            mainJoints.remove(each)

    mainJoints.reverse()

    counter  = 2
    for each in mainJoints:
        
        if each != ikJoints[0]:
            rename (each, "Main_Neck_jnt" + str(counter) + charName)
        counter += 1

    #add the root joint to the mainJointList
    mainJoints = [mainJointRoot] + mainJoints


    #assign the switch control 
    theSwitch =  "IKFK_Neck"
    translation = True 
    workHorseSetRangeNode = pxUtilities.ikFkChainSwitch(ikJoints,fkJoints,mainJoints,theSwitch,'FkIk',translation)
    #move the pivot point to the world origin
    cmds.move(0,0,0,theSwitch +'.scalePivot',theSwitch +'.rotatePivot')






    #spaceSwitcher(constraintGrp, switch, localSpacePrefix, localItem, worldItem)
    pxUtilities.spaceSwitcher(ikHeadConstraintGrp, theSwitch, prefix, fkAllNeckCtrl, theSwitch)


    #hideOrShowSwitch(switchAttr, defaultControlList, alternateControlList)
    pxUtilities.hideOrShowSwitch(theSwitch + ".FkIk_Switch",  ikCtrls,fkCtrls)
    #warningMark
    warningMark = "StretchWarning_Neck"
    tempConstraint = parentConstraint (theSwitch, warningMark )
    delete(tempConstraint)


    overStretchConditionNode = shadingNode("condition", asUtility = True, n = "%s_OverStretch%s" %(prefix, charName))
    setAttr(overStretchConditionNode + ".operation", 2) # greater then
    setAttr(overStretchConditionNode + ".secondTerm", 1.2) #a vale of 1.5 will activate stretch warning
    setAttr(overStretchConditionNode + ".colorIfTrueR", 1)
    setAttr(overStretchConditionNode + ".colorIfFalseR", 0)

    addStretchAttr = [ikCtrls[2]] 

    for each in addStretchAttr:
        print each
        cmds.addAttr( each, ln="neckStretch",dv=1,at='double', k = True)	
        cmds.connectAttr ((divideNode + ".outputX"),(each + ".neckStretch"))


    connectAttr((divideNode + ".outputX"),(overStretchConditionNode + ".firstTerm"))
    connectAttr((overStretchConditionNode + ".outColorR" ),(warningMark + ".visibility"))

    parent ( warningMark, theSwitch)


    #kill the original joint chain it is no longer needed
    delete (rootJoint)



    neckToken = group(empty = True, name = "neck_token" + charName )
    print "HEY THE %s HAS BEEN MADE!" % (neckToken)




















      
    






