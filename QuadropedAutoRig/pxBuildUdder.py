from ui import *
from buildScripts import pxUtilities


def pxBuildUdder():
    
    charName = queryCharName()
    root = "udder_root"
    pxUtilities.orientJoints(root, "xyz", "yup")   
    #List variable names
    jointRelatives = listRelatives(root, allDescendents = True )
    #print jointRelatives
    # Reverse the order of the elements in the list
    jointRelatives.reverse()
    
    # Append the root to the beginning of the list
    jointList = [root] + jointRelatives
    #print jointList
    
    # Create curve controls
    jointNames = ["udder_root","udder_01_jnt", "udder_end_jnt"]
    ctrls = []
    nulls = []
    #create a control and name it
    ctrl = circle (n = jointNames[1] + "_ctrl" + charName, nr = (1, 0, 0), c = (0, 0, 0), r = 0.5, ch = False)
    ctrlShape = pickWalk(ctrl, d = 'down') 
    setAttr(ctrlShape[0] + '.overrideEnabled', 1)
    setAttr(ctrlShape[0] + ".overrideColor", 17)
    ctrls.append(ctrl)
    #clear selection
    select (cl = True)
    #create the nulls
    null = group (empty = True, n = jointNames[1] + "_Grp" + charName)
    nulls.append(null)   
    moveGrp = [null,ctrl]
    #parent constrain both to the joint
    for item in moveGrp:
        tempConstraint = parentConstraint(jointNames[1], item)
        delete(tempConstraint)
    #parent the ctrls under the nulls
    parent(ctrl, null)
        
    parentConstraint(ctrl, jointNames[1]) 
    
    
    udderToken = group(empty = True, name = "udder_token" + charName )          
    print "HEY THE %s HAS BEEN MADE!" % (udderToken)
