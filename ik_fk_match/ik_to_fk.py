import maya.cmds as cmds
import maya.mel as mel
import random



name = "lf"
tempshoulderRot= cmds.getAttr ((name + '_shoulder_info.rotate'))
shoulderRot = tempshoulderRot[0]

shoulder_roX = shoulderRot[0] 
shoulder_roY = shoulderRot[1] 
shoulder_roZ = shoulderRot[2] 

cmds.select((name + '_shoulder_CTRL'), r = True)
cmds.rotate (shoulder_roX, shoulder_roY, shoulder_roZ)

tempelbowRot= cmds.getAttr ((name + '_elbow_info.rotate'))
elbowRot = tempelbowRot[0]

elbow_roX = elbowRot[0] 
elbow_roY = elbowRot[1] 
elbow_roZ = elbowRot[2] 

cmds.select((name + '_elbow_CTRL'), r = True)
cmds.rotate (elbow_roX, elbow_roY, elbow_roZ)

tempwristRot= cmds.getAttr ((name + '_wrist_info.rotate'))
wristRot = tempwristRot[0]

wrist_roX = wristRot[0] 
wrist_roY = wristRot[1] 
wrist_roZ = wristRot[2] 

cmds.select((name + '_wrist_CTRL'), r = True)
cmds.rotate (wrist_roX, wrist_roY, wrist_roZ)

    