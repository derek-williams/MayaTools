from ui import *
from buildScripts import pxUtilities
#from pymel.all import *

def pxBuildTail():
    
    charName = queryCharName()

    root = "tail_root"
    pxUtilities.orientJoints(root, "xyz", "yup")   
    # List variable names 
    jointRelatives = listRelatives(root, allDescendents = True )
    #print jointRelatives
    # Reverse the order of the elements in the list
    jointRelatives.reverse()
    
    # Append the root to the beginning of the list
    jointList = [root] + jointRelatives
    #print jointList
    
    # Create curve controls
    jointNames = ["tail_root","tail_01_jnt","tail_02_jnt","tail_end_jnt"]
    ctrls = []
    nulls = []
    
    i = 0
    #double for loop to create the ctrls and null grps; then parenting the ctrls&nulls to the joints.
    for each in jointList:
        #create a control and name it 
        if charName == '_YoungGoat':
            ctrl = circle (n = jointNames[i] + "_ctrl" + charName, nr = (1, 0, 0), c = (0, 0, 0), r = 0.05, ch = False)
        elif charName == '_OldGoat':
            ctrl = circle (n = jointNames[i] + "_ctrl" + charName, nr = (1, 0, 0), c = (0, 0, 0), r = 0.12, ch = False)
        ctrlShape = pickWalk(ctrl, d = 'down') 
        setAttr(ctrlShape[0] + '.overrideEnabled', 1)
        setAttr(ctrlShape[0] + ".overrideColor", 17)
        ctrls.append(ctrl)    
        #clear selection
        select (cl = True)
        #create the nulls
        null = group (empty = True, n = jointNames[i] + "_Grp" + charName)
        nulls.append(null)   
        moveGrp = [null,ctrl]
        #parent constrain both to the joint
        for item in moveGrp:
            tempConstraint = parentConstraint(jointNames[i], item)
            delete(tempConstraint)
        #parent the ctrls under the nulls
        parent(ctrl, null)
        
        parentConstraint(ctrl, jointNames[i]) 
        i+=1 
        
    #parent the nulls underneath the previous ctrls    
    parent(nulls[1], ctrls[0])
    parent(nulls[2], ctrls[1])
    parent(nulls[3], ctrls[2])
     
    #delete the last null/ctrl grp
    delete(nulls[3])
    
    tailToken = group(empty = True, name = "tail_token" + charName )
    print "HEY THE %s HAS BEEN MADE!" % (tailToken) 
