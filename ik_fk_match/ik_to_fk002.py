import maya.cmds as cmds
import maya.mel as mel
import random

ctrl_name = cmds.ls(sl = True, sn = True)
ctrl_name_str = str(ctrl_name)
name_space_list = ctrl_name_str.split(":")
name_space_amount = len(name_space_list)
actual_name_space = name_space_list[0]
i = 1 
while i < name_space_amount - 1:
    actual_name_space = actual_name_space + ":" +  name_space_list[i]
    i = (i+ 1)

actual_name_space = actual_name_space + ":"

if "'" in actual_name_space: 
    param, name_space = actual_name_space.split("'",1) 
    
ctrl_name =  cmds.ls(sl= True, sn = True)
print ctrl_name    

if ctrl_name == [name_space + 'lf_wrist_CTRL']:
    name = "lf"
    tempwristPos= cmds.getAttr ((name_space + 'ik_' + name + '_wrist_info.translate'))
    wristPos = tempwristPos[0]
    
    wrist_X = wristPos[0] 
    wrist_Y = wristPos[1] 
    wrist_Z = wristPos[2]
    
    
    tempwristRot= cmds.getAttr ((name_space + 'ik_' +name + '_wrist_info.rotate'))
    wristRot = tempwristRot[0]
    
    wrist_roX = wristRot[0] 
    wrist_roY = wristRot[1] 
    wrist_roZ = wristRot[2] 
    
    cmds.select((name_space + 'ik_' + name + '_wrist_CTRL'), r = True)
    cmds.move (wrist_X, wrist_Y, wrist_Z)
    cmds.rotate (wrist_roX, wrist_roY, wrist_roZ) 
    
    tempelbowpvPos= cmds.getAttr ((name_space + name + '_elbowpv_info.translate'))
    elbowpvPos = tempelbowpvPos[0]
    
    pv_X = elbowpvPos[0] 
    pv_Y = elbowpvPos[1] 
    pv_Z = elbowpvPos[2]
    cmds.select((name_space + name + '_elbow_PV'),r = True)
    cmds.move(pv_X, pv_Y, pv_Z)
    cmds.setAttr(name_space +'lf_IKFKSwitch_CTRL.IK_FK_switch', 0 )
    print "left arm has been switched to ik"


elif ctrl_name == [name_space + 'ik_lf_wrist_CTRL'] : 
        
    name = "lf"
    tempshoulderRot= cmds.getAttr ((name_space + name + '_shoulder_info.rotate'))
    shoulderRot = tempshoulderRot[0]
    
    shoulder_roX = shoulderRot[0] 
    shoulder_roY = shoulderRot[1] 
    shoulder_roZ = shoulderRot[2] 
    
    cmds.select((name_space +name + '_shoulder_CTRL'), r = True)
    cmds.rotate (shoulder_roX, shoulder_roY, shoulder_roZ)
    
    tempelbowRot= cmds.getAttr ((name_space +name + '_elbow_info.rotate'))
    elbowRot = tempelbowRot[0]
    
    elbow_roX = elbowRot[0] 
    elbow_roY = elbowRot[1] 
    elbow_roZ = elbowRot[2] 
    
    cmds.select((name_space +name + '_elbow_CTRL'), r = True)
    cmds.rotate (elbow_roX, elbow_roY, elbow_roZ)
    
    tempwristRot= cmds.getAttr ((name_space +name + '_wrist_info.rotate'))
    wristRot = tempwristRot[0]
    
    wrist_roX = wristRot[0] 
    wrist_roY = wristRot[1] 
    wrist_roZ = wristRot[2] 
    
    cmds.select(name_space +(name + '_wrist_CTRL'), r = True)
    cmds.rotate (wrist_roX, wrist_roY, wrist_roZ)
    cmds.setAttr(name_space +'lf_IKFKSwitch_CTRL.IK_FK_switch', 1 )
    print "left arm has been switched to fk"
    
elif ctrl_name == [name_space + 'rt_wrist_CTRL']:
    name = "rt"
    tempwristPos= cmds.getAttr ((name_space + 'ik_' + name + '_wrist_info.translate'))
    wristPos = tempwristPos[0]
    
    wrist_X = wristPos[0] 
    wrist_Y = wristPos[1] 
    wrist_Z = wristPos[2]
    
    
    tempwristRot= cmds.getAttr ((name_space + 'ik_' +name + '_wrist_info.rotate'))
    wristRot = tempwristRot[0]
    
    wrist_roX = wristRot[0] 
    wrist_roY = wristRot[1] 
    wrist_roZ = wristRot[2] 
    
    cmds.select((name_space + 'ik_' + name + '_wrist_CTRL'), r = True)
    cmds.move (wrist_X, wrist_Y, wrist_Z)
    cmds.rotate (wrist_roX, wrist_roY, wrist_roZ) 
    
    tempelbowpvPos= cmds.getAttr ((name_space + name + '_elbowpv_info.translate'))
    elbowpvPos = tempelbowpvPos[0]
    
    pv_X = elbowpvPos[0] 
    pv_Y = elbowpvPos[1] 
    pv_Z = elbowpvPos[2]
    cmds.select((name_space + name + '_elbow_PV'),r = True)
    cmds.move(pv_X, pv_Y, pv_Z)
    cmds.setAttr(name_space + 'rt_IKFKSwitch_CTRL.IK_FK_switch', 0 )
    print "right arm has been switched to ik"


elif ctrl_name == [name_space + 'ik_rt_wrist_CTRL'] : 
        
    name = "rt"
    tempshoulderRot= cmds.getAttr ((name_space +name + '_shoulder_info.rotate'))
    shoulderRot = tempshoulderRot[0]
    
    shoulder_roX = shoulderRot[0] 
    shoulder_roY = shoulderRot[1] 
    shoulder_roZ = shoulderRot[2] 
    
    cmds.select((name_space +name + '_shoulder_CTRL'), r = True)
    cmds.rotate (shoulder_roX, shoulder_roY, shoulder_roZ)
    
    tempelbowRot= cmds.getAttr ((name_space + name + '_elbow_info.rotate'))
    elbowRot = tempelbowRot[0]
    
    elbow_roX = elbowRot[0] 
    elbow_roY = elbowRot[1] 
    elbow_roZ = elbowRot[2] 
    
    cmds.select((name_space + name + '_elbow_CTRL'), r = True)
    cmds.rotate (elbow_roX, elbow_roY, elbow_roZ)
    
    tempwristRot= cmds.getAttr ((name_space + name + '_wrist_info.rotate'))
    wristRot = tempwristRot[0]
    
    wrist_roX = wristRot[0] 
    wrist_roY = wristRot[1] 
    wrist_roZ = wristRot[2] 
    
    cmds.select((name_space + name + '_wrist_CTRL'), r = True)
    cmds.rotate (wrist_roX, wrist_roY, wrist_roZ)
    cmds.setAttr(name_space + 'rt_IKFKSwitch_CTRL.IK_FK_switch', 1 )
    print "right arm has been switched to fk"
else:
    print "Please select a wrist or ankle control"
