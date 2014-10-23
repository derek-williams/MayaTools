from pymel.all import *

def pxAddAnnotation(theJoint, poleVec):
    
    worldSpaceOfJoint = xform(theJoint, q = True, worldSpace = True, rp = True)
    worldSpaceOfLoc = xform(poleVec, q = True, worldSpace = True, rp = True)
    locator = spaceLocator(p = (0, 0, 0), n = poleVec + "_loc")
    annotation = cmds.annotate(str(locator), tx = ' ', point = worldSpaceOfLoc)
    move(locator, worldSpaceOfJoint, a = True)
    parent(locator, theJoint)
    setAttr(locator + "Shape.visibility", 0)
    annotation = pickWalk(annotation, d = "up")
    select(poleVec, r = True)
    select(annotation, tgl = True)
    mel.eval('doCreateParentConstraintArgList 1 { "0","0","0","0","0","0","0","1","","1" };') 
    rename(annotation, poleVec + "_annot")
    annotation = poleVec + "_annot"
    setAttr(annotation + '.overrideEnabled', 1)
    setAttr(annotation + '.overrideDisplayType', 2)
    select(clear = True)
    
def mirrorJoints(root):
        mirrorJoint(root, mirrorYZ = True, mirrorBehavior = True, searchReplace = ('l_', 'r_'))

def pxCreateOrganizationGroup(charName, grpName):
        groupName = group(empty = True, name = grpName + charName)
        return groupName

def pXGroupControl(ctrlName):

	#duplicates the selected ctrl based on the char name and listed ctrl
	ctrlDuplicate=duplicate(ctrlName)
	#this next command will find the shape node of the duplicated ctrl - and - delete it
	    #this effectively creating a an emtpy transform/null 
	ctrlDuplicateShape = listRelatives(ctrlDuplicate[0], shapes = True)
	delete(ctrlDuplicateShape)
	rename(ctrlDuplicate[0],(ctrlName + "_grp"))
	#parents the control under the null
	parent((ctrlName),(ctrlName + "_grp"))
	#return the name of the newly created null grp
	return (ctrlName + "_grp")
	


def setColorAndRadius(jointToAffect,colorChoice, size):
        ''' Color Choices:
                colorPalette = {'red, blue, yellow, pink, white, purple}
                                                                        ''' 

        colorPalette = {
        'red' : 4, 
        'blue' : 5, 
        'yellow' : 17,
        'pink' : 9,
        'white' : 16,
        'purple' : 8
        }
        setAttr(jointToAffect + ".overrideEnabled", 1)
    
        setAttr(jointToAffect + ".overrideColor", colorPalette[colorChoice])
        setAttr(jointToAffect + ".radius", size) 

def setColor(object,colorChoice):
        ''' Color Choices:
                colorPalette = {'red, blue, yellow, pink, white, purple}
                                                                        ''' 

        colorPalette = {
        'red' : 13, 
        'blue' : 18, 
        'yellow' : 17,
        'pink' : 9,
        'white' : 16,
        'purple' : 8
        }
        setAttr(object + ".overrideEnabled", 1)
    
        setAttr(object + ".overrideColor", colorPalette[colorChoice])
    


def pxStretchySplineIk(prefix, spineIKCurve, joints, charName):
        
    #prefix = "spine" or "neck both work the same as well as any other string
    
    
    #create an arc length node and capture its curent cal
    arcLengthNode = arclen(spineIKCurve, ch = True, n = (prefix + "_cInfo" + charName) ) 
    restArcLength = getAttr(arcLengthNode + ".arcLength")
    
    #create a divide node to divide the dynamic arclenth and the rest length 
    
    divideNode = shadingNode('multiplyDivide', asUtility = True, n  = ( prefix + "_DivideNode" + charName))
    setAttr(divideNode + ".operation", 2)  
    setAttr(divideNode + ".input2X", restArcLength)
    connectAttr((arcLengthNode + ".arcLength"), (divideNode + ".input1X"))
    
    #create a "to the power of" node to adjust the output of the divide node
     
    powerNode = shadingNode('multiplyDivide', asUtility = True, n  = ( prefix + "_PowerOfNode_" + charName))
    setAttr(powerNode + ".operation", 3) 
    setAttr(powerNode + ".input2X", 0.300)  
    connectAttr(divideNode + ".outputX", powerNode+".input1X" ) 
    
    #here well use a for loop to give the stretchy behavior to all the joints
     
    for j in range(1,len(joints)):
    
        setDrivenKeyframe((str(joints[j]) + ".tx"),
    			dv=1,
    			itt="clamped",
    			cd=(str(divideNode) + ".outputX"),
    			ott="clamped",
    			v=(getAttr(str(joints[j]) + ".tx")))
    		#These two commands create 1 full set driven key
    		#driverValue -the value that the driver is set to - .............the first value is 1
    		#value that the driven item is set to
    		#inTangentType - sets tangent to..
    		#here the factor MultNode is driving each current joint // creates a sdk from last multdiv to each
    		#currentDriver - these are the actual attributes being keyed
        setDrivenKeyframe((str(joints[j]) + ".tx"),
    			dv=2,
    			itt="clamped",
    			cd=(str(divideNode) + ".outputX"),
    			ott="clamped",
    			v=((getAttr(str(joints[j]) + ".tx")) * 2))
    
        setAttr((str(joints[j]) + "_translateX.preInfinity"), 1)
        setAttr((str(joints[j]) + "_translateX.postInfinity"), 1)
    return divideNode





        
        
        
def orientJoints(root, primaryOrientation, secondaryOrientation):
    ''' User should specify the root of the joint chain they are orienting as well as
the primary and secondary orentation configurations. A typical example would be:
orientJoints(hip, "xyz", "yup")
xyz and yup being the default configuration.'''
    joint(root, edit = True, orientJoint = primaryOrientation, secondaryAxisOrient = secondaryOrientation, children = True, zeroScaleOrient = True)
 
        
        
def ikFkChainSwitch(ikJoints,fkJoints,mainJoints,theSwitch, nameOfSwitchAttr, translation):
    
    '''takes two joint chains as input, applies to the main joint chain, enter the name of the obj to 
        recieve the switch, what prefix ie. "fkIk", and whether you want translation set up as well  '''
    
    #create an attribute on the switch to act as an attr
            
    addAttr(theSwitch,ln=nameOfSwitchAttr + "_Switch", max=10, min = 0, dv= 0 ,at='double', k= True)    
    
    #create a set range node to make the range 0 - 10
    
    setRangeNode = shadingNode('setRange',asUtility = True, n = theSwitch + "_" + nameOfSwitchAttr +"_setRangeNode")
    setAttr (setRangeNode + ".oldMaxX", 10)
    setAttr (setRangeNode + ".maxX", 1)
    connectAttr(theSwitch + "." + nameOfSwitchAttr + "_Switch", setRangeNode + ".valueX")
        
    i = 0 
    for each in mainJoints:
        
        rotateBlendNode = shadingNode('blendColors',asUtility = True, n = (each + "_RotateBlendNode"))
        connectAttr( ikJoints[i] +".rotate", rotateBlendNode + ".color1")
        connectAttr( fkJoints[i] +".rotate", rotateBlendNode + ".color2")

        connectAttr(rotateBlendNode + ".output", each + ".rotate")
        connectAttr(setRangeNode + ".outValueX", rotateBlendNode + ".blender")

        
        if translation == True:
            
            translateBlendNode = shadingNode('blendColors',asUtility = True, n = (each + "_TranslateBlendNode"))
            connectAttr( ikJoints[i] +".translate",translateBlendNode + ".color1")
            connectAttr( fkJoints[i] +".translate", translateBlendNode + ".color2")            

            connectAttr(translateBlendNode  + ".output", each + ".translate")
            connectAttr(setRangeNode  + ".outValueX", translateBlendNode + ".blender")
        
        i += 1            
            
    return setRangeNode        

        

def unlock():        

    sel = selected()
    
    
    for each in sel:
        setAttr (each + ".translateX", l = False, k = True) 
        setAttr (each + ".translateY", l = False, k = True) 
        setAttr (each + ".translateZ", l = False, k = True) 
        setAttr (each + ".rotateX", l = False, k = True) 
        setAttr (each + ".rotateY", l = False, k = True) 
        setAttr (each + ".rotateZ", l = False, k = True)
        setAttr (each + ".scaleX", l = False, k = True) 
        setAttr (each + ".scaleY", l = False, k = True) 
        setAttr (each + ".scaleZ", l = False, k = True) 
        setAttr (each + ".visibility", l = False, k = True)
        setAttr(each + ".visibility",1)        
       
def vectorDistance(jointA, jointB): # thats a  pretty handy fomula youve got there!  
    Ax, Ay, Az = xform(jointA, query = True,  rotatePivot = True, worldSpace = True)
    Bx, By, Bz = xform(jointB, query = True,  rotatePivot = True, worldSpace = True)
    
    distance = (((Ax - Bx)**2) + ((Ay-By)**2) + ((Az - Bz)**2))**0.5
    return distance #single return variable - easier to read


def makeIkStretchy(theIKHandle):
    '''This function works on RP and SC IK solvers'''
    
    # list connections of the ik handle
    connections = listConnections(theIKHandle)
    
    # define the end effector and start joint of the affected chain
    for each in connections:
        if nodeType(each) == "ikEffector":
            endEffector = each
        if nodeType(each) == "joint":
            startJoint = each
            
    #this is assuming that this setup will always contain a hip, knee, and ankle,
     
    midJoint = pickWalk(endEffector, direction = "up")[0] #took the lib of defining this as well
    endJoint = pickWalk(midJoint, direction = "down")[0]
    #The condition you had for your while loop could never be satisfied, therfore maya will always get stuck in an infinite loop
    #Result.. Crash -  I general avoid while loops, favoring instead equivalent for loops 
    #for loops are usually simpler to understand syntactically and are much more difficult to crash out of..
    
    #took me awhile to figure out what was happening here, but looks like you can remove the loop enirely
    #I could be way off base here, but it looked like the while loop was working toward..  
    startToMid = vectorDistance(startJoint,midJoint)
    midToEnd = vectorDistance(midJoint,endJoint)

    totalDistance = startToMid + midToEnd
    print totalDistance
    # measure the distance between the IK handle and start joint using 2 nulls and 
    # a distanceBetween render node
    select(cl = True) 
    startPoint = group(empty = True, name = theIKHandle + "startPoint")
    
    select(cl = True)
    endPoint = group(empty = True, name = theIKHandle + "endPoint")
    
    # point costrain to the start joint and ik handle
    pointConstraint(startJoint, startPoint)
    pointConstraint(theIKHandle, endPoint)
    
    # create a distanceBetween render node
    distanceNode = shadingNode("distanceBetween", name = "stretchyDistance", asUtility = True)
    
    # connect the translates of the point constrained nulls to the point 1 & 2 inputs 
    # on the distance node
    connectAttr (startPoint + ".translate", distanceNode + ".point1")
    connectAttr (endPoint + ".translate", distanceNode + ".point2")
    
    # create a condition node
    conditionNode =  shadingNode("condition", name = "stretchyCondition", asUtility = True)
    
    connectAttr (distanceNode + ".distance", conditionNode + ".colorIfFalseR")
    connectAttr (distanceNode + ".distance", conditionNode + ".secondTerm")
    
    # set operation to 'greater or equal'
    setAttr(conditionNode + ".operation", 3)
    
    # set the condition node's colorIfTrueR to the totalDistance
    setAttr(conditionNode + ".colorIfTrueR", totalDistance)
    
    # set the condition node's first term to the totalDistance
    setAttr(conditionNode + ".firstTerm", totalDistance)
    
    # create a multiplyDivide node
    multiDivNode = shadingNode("multiplyDivide", name = "stretchyMultiDiv", asUtility = True)
    
    # set the node operation to 'divide'
    setAttr(multiDivNode + ".operation", 2)
    
    # set the dividend to the distance between the ik handle and start joint
    connectAttr(conditionNode + ".outColorR", multiDivNode + ".input1X")
    
    # set the divisor to the total distance along the chain
    setAttr(multiDivNode + ".input2X", totalDistance)
    
    # connect the output of the multiDivNode to the scale X of each joint in the affected chaiSn
    connectAttr(multiDivNode + ".outputX", startJoint + ".scaleX")
    connectAttr(multiDivNode + ".outputX", midJoint + ".scaleX")        
        

def hideOrShowSwitch(switchAttr, defaultControlList, alternateControlList):   #the attribute to be used as a switch(0-1), defaultControlList, alternateControlList

    #attr ="Switch.switch"
    splitAttr = switchAttr.split('.')
    
    #make sure the operation can work based on the data given
    
    #get some info from the attributeQuery command
    #find the middle point of the  floating point switch attr
    minMaxList = attributeQuery (splitAttr[1], node = splitAttr[0], range = True)
    min = minMaxList[0]
    max = minMaxList[1]
    middleValue = max/2
    
    
    #create all the associated Nodes
    conditionalNode = shadingNode('condition', asShader=True, name = splitAttr[0] + '_conditionalNode')
    

    
    #set the valuse to operate as a greater than switch 
    setAttr (conditionalNode + ".operation", 2)
    setAttr (conditionalNode + ".secondTerm", middleValue)
    
    setAttr (conditionalNode + ".colorIfTrueG" ,1)
    setAttr (conditionalNode + ".colorIfFalseG", 0)
    
    setAttr (conditionalNode + ".colorIfTrueR", 0)
    setAttr (conditionalNode + ".colorIfFalseR", 1)
    #make all the proper connections
    #switch to conditional first term
    connectAttr(switchAttr, conditionalNode + ".firstTerm")
    
    #condition to the first set of controls
    for each in defaultControlList:
    
        connectAttr(conditionalNode + ".outColor.outColorG", each + ".v")
      
    for each in alternateControlList:
    
        connectAttr(conditionalNode + ".outColor.outColorR", each + ".v")


#hideOrShowSwitch('Switch.switch', defaultControlList, alternateControlList)





def spaceSwitcher(constraintGrp,switch,localSpacePrefix, localItem, worldItem): #constraintGrp, switch, localSpacePrefix, localItem, s
        
    '''   
    This function wiil serve as a way to swap from local space to world space, it works based off a pair of set range nodes that control constraint target weights
    Future updates may add the functionality to add additional slots for space, this function was only designed with the intent of switching between world and 1 local spaces ie the neck local vs world 
    
    #exapmle variables
    constraintGrp = 'ConstraintGrp'
    switch = 'TheWorld'
    localSpacePrefix = 'R_Arm'
    localItem  = 'Local'    
    worldItem = 'TheWorld'
    '''
    
    #parent constraits will stack the local con is just a visual convention
    localCon = parentConstraint (localItem, constraintGrp, name = "%s_%s_Constraint" %(localSpacePrefix, localItem), mo = True)
    worldCon = parentConstraint (worldItem, constraintGrp, name = "%s_%s_Constraint" %(localSpacePrefix, worldItem) , mo = True)
    
    #add the an attribute to control the space switching
    attrName = constraintGrp + "Local_OR_World"
    addAttr(switch, ln = attrName, at='double', k = True, max = 10, min = 0, dv = 0)
    
    #create two set range nodes the first to convert the value of the worldLocal switch -> 0-1
    #the second set range node to remap 0 to 1 -> 1 to 0 -essentially reversing the 0 to 1 range
    
    
    
    
    setRangeNode = shadingNode('setRange',asUtility = True, n = constraintGrp + "worldLocal_setRangeNode")
    setAttr (setRangeNode + ".oldMaxX", 10)
    setAttr (setRangeNode + ".maxX", 1)
    connectAttr(switch +'.'+ attrName, setRangeNode + ".valueX")
    
    reverseSetRangeNode = shadingNode( 'setRange',asUtility = True, n = constraintGrp + "worldLocal_setRangeNode_Rev")
    setAttr (reverseSetRangeNode + ".oldMaxX", 1)
    setAttr (reverseSetRangeNode + ".oldMinX", 0)
    setAttr (reverseSetRangeNode + ".maxX", 0)
    setAttr (reverseSetRangeNode + ".minX", 1)
    connectAttr(setRangeNode + ".outValueX", reverseSetRangeNode + ".valueX")
    
    #capture the target list of the parent constraint
    weightsList = parentConstraint (worldCon, q = True, weightAliasList = True) 
    local = weightsList[0]
    world = weightsList[1]
    
    #connect the set range nodes to the proper constraint targets eestablished in tne weightsList
    connectAttr (setRangeNode + '.outValueX',world) 
    connectAttr (reverseSetRangeNode + '.outValueX',local)
    return attrName

def cleanup(obj, myAttr):
    index = 0
    for each in myAttr:
        setAttr(obj + myAttr[index], keyable = False, channelBox = False, lock = True)
        index += 1
        
        
def cleanupHandles(handles):
    i = 0
    for item in handles:
        setAttr(handles[i] + ".visibility", 0, keyable = False, channelBox = False, lock = True)
        i += 1
    
            
def pxAddSkinCluster(rootJoint, geo,bindJoints,charName,dualQuaternion ):
    
    select(bindJoints)
    nameOfCluster =  geo + '_SkinCluster' + charName
    skinClusterCatcher = skinCluster( rootJoint ,geo,  name = nameOfCluster, toSelectedBones = True )
    
    #now we can name the components that come along with the skincluster
        #use list connections to gater the data
    catcherClusterConnections = listConnections(skinClusterCatcher , shapes = 1, d = 1)# including shape node
        # creates a set - removes duplicate items from the list
    clusterConnections = list(set(catcherClusterConnections))  
    
    
    for current in clusterConnections:
    
        #take advantage of pymels node type option
        if nodeType(current) ==  "dagPose":
            rename(current, geo + "SkinCluster_DagPose" + charName)
            
        
        if nodeType(current) ==  "objectSet":
            rename(current , (geo + "Cluster_Set" + charName)) 
    
        #Also name the associated tweak node        
    shape = listRelatives(geo, s = 1)[0]
    tweak = listConnections(shape + ".tweakLocation")
    print tweak
    #rename (tweak, geo + "_Tweak" + charName)     

    for currentJoint in bindJoints:
        if currentJoint !=  rootJoint:
            skinCluster(skinClusterCatcher, addInfluence = currentJoint , dr=100 , wt=0 , edit = True , lw = False)
    if dualQuaternion == True:
        
        setAttr(skinClusterCatcher + ".skinningMethod",1)
             

def attachGeo(theJoint,theItems):
    for each in theItems:
        test = xform (theJoint, q  = True,ws =True ,rotatePivot= True)
        xform (each, rp = test, p = True, ws = True)
        
        mel.eval('parentConstraint -mo -weight 1 -name "%s" %s %s;' % (each + '_TO_'+ theJoint, str(theJoint),str(each) ))

            
def aGroupAbove(nameOfTheNewGrp, ctrl ):


    parentObj = pickWalk(ctrl,direction = 'up') #from the control to find the parent node

#create the null 
    grp = group(empty  =  True, name = nameOfTheNewGrp)
    
#temp parent constrain the grp to the parentObj

    tempConstraint = parentConstraint(parentObj,grp)
    delete (tempConstraint)
    
    parent (grp,parentObj)
    makeIdentity(grp, n=0,s=1,r=1,t=1,apply=True,pn=1)
    parent (ctrl,grp)
    return grp
