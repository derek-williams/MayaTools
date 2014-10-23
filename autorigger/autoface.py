#    autoface.py
#    Suite of functions to quickly connect facial blendshape rig for Project X

from maya import cmds

def bakeLowerLipIntoShapes():
   controls = cmds.ls(selection=True, l=True)[:-1]
   geometry = cmds.ls(selection=True, l=True)[-1] 

   newBlendshapes = list()   
   for ctl in controls:
      shortname = ctl.rpartition('|')[2]
      cmds.setAttr(ctl + '.ty', 0.1)       
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'Up'))
      cmds.setAttr(ctl + '.ty', 0.0)
           
      cmds.setAttr(ctl + '.ty', -0.1)
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'Dn'))
      cmds.setAttr(ctl + '.ty', 0.0)

      cmds.setAttr(ctl + '.tz', -0.1)
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'Bak'))
      cmds.setAttr(ctl + '.tz', 0.0)

      cmds.setAttr(ctl + '.tz', 0.1)
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'Fwd'))
      cmds.setAttr(ctl + '.tz', 0.0)

      cmds.setAttr(ctl + '.tx', -0.1)
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'Right'))
      cmds.setAttr(ctl + '.tx', 0.0)

      cmds.setAttr(ctl + '.tx', 0.1)
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'Left'))
      cmds.setAttr(ctl + '.tx', 0.0)

      cmds.setAttr(ctl + '.rx', 90.0)
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'RotXPos'))
      cmds.setAttr(ctl + '.rx', 0.0)

      cmds.setAttr(ctl + '.rx', -90.0)
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'RotXNeg'))
      cmds.setAttr(ctl + '.rx', 0.0)

      cmds.setAttr(ctl + '.ry', 90.0)
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'RotYPos'))
      cmds.setAttr(ctl + '.ry', 0.0)

      cmds.setAttr(ctl + '.ry', -90.0)
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'RotYNeg'))
      cmds.setAttr(ctl + '.ry', 0.0)

      cmds.setAttr(ctl + '.rz', 90.0)
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'RotZPos'))
      cmds.setAttr(ctl + '.rz', 0.0)

      cmds.setAttr(ctl + '.rz', -90.0)
      newBlendshapes.extend(cmds.duplicate(geometry, name=shortname+'RotZNeg'))
      cmds.setAttr(ctl + '.rz', 0.0)
      
def setupTeeth():
   control = cmds.ls(selection=True)[0]
   
   cmds.addAttr(control, longName='TEETH', attributeType='short', min=0, max=0, hidden=False, keyable=False)
   cmds.setAttr(control+'.TEETH', channelBox=True)
   
   for side in ['Top', 'Bot']:
      teethMoveMul = cmds.shadingNode('multiplyDivide', asUtility=True, name=side.lower() + '_teeth_MUL')
      for axis in ['X', 'Y', 'Z']:
        attrName = '{0}Move{1}'.format(side, axis) 
        cmds.addAttr(control, longName=attrName, min=-10.0, max=10.0, keyable=True)  
        cmds.connectAttr(control + '.' + attrName, '{0}.input1{1}'.format(teethMoveMul, axis), force=True)
        cmds.setAttr('{0}.input2{1}'.format(teethMoveMul, axis), 0.1)
        
      cmds.connectAttr(teethMoveMul + '.output', side.lower() + '_teeth_SDKGRP.translate')
      
   cmds.select(control, replace=True)

def setupTongue():
    selection = cmds.ls(selection=True)
    control = selection[0]
    joints = selection[1:]
   
    for i in range(1,4):
        teethRotMul = cmds.shadingNode('multiplyDivide', asUtility=True, name='tongue{0}_MUL'.format(i))
        cmds.connectAttr('{0}.RotX{1}'.format(control, i), teethRotMul + '.input1X', force=True)
        cmds.connectAttr('{0}.RotY{1}'.format(control, i), teethRotMul + '.input1Y', force=True)
        cmds.connectAttr('{0}.RotZ{1}'.format(control, i), teethRotMul + '.input1Z', force=True)
        
        cmds.setAttr(teethRotMul + '.input2X', 9.0)
        cmds.setAttr(teethRotMul + '.input2Y', 9.0)
        cmds.setAttr(teethRotMul + '.input2Z', 9.0)
        
        cmds.connectAttr(teethRotMul + '.output', selection[i] + '.rotate', force=True)
        
    teethScaleMul = cmds.shadingNode('setRange', asUtility=True, name='scale_tongue_RNG')
    
    cmds.connectAttr(control + '.ScaleX', teethScaleMul + '.valueX')
    cmds.connectAttr(control + '.ScaleY', teethScaleMul + '.valueY')
    cmds.connectAttr(control + '.ScaleZ', teethScaleMul + '.valueZ')
    
    cmds.setAttr(teethScaleMul + '.minX', 0.5)
    cmds.setAttr(teethScaleMul + '.minX', 0.5)
    cmds.setAttr(teethScaleMul + '.minX', 0.5)
    cmds.setAttr(teethScaleMul + '.maxX', 1.5)
    cmds.setAttr(teethScaleMul + '.maxY', 1.5)
    cmds.setAttr(teethScaleMul + '.maxZ', 1.5)
    cmds.setAttr(teethScaleMul + '.oldMinX', -10)
    cmds.setAttr(teethScaleMul + '.oldMinY', -10)
    cmds.setAttr(teethScaleMul + '.oldMinZ', -10)
    cmds.setAttr(teethScaleMul + '.oldMaxX', 10)
    cmds.setAttr(teethScaleMul + '.oldMaxY', 10)
    cmds.setAttr(teethScaleMul + '.oldMaxZ', 10)
    
    for jnt in joints:
        cmds.connectAttr(teethScaleMul + '.outValue', jnt + '.scale')   
        
def setupLowerLip(characterPrefix):
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_jaw_open'.format(characterPrefix), currentDriver='jaw_CTRL.translateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_jaw_open'.format(characterPrefix), currentDriver='jaw_CTRL.translateY', 
                            value=1, driverValue=-1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_jaw_lf_shift'.format(characterPrefix), currentDriver='jaw_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_jaw_lf_shift'.format(characterPrefix), currentDriver='jaw_CTRL.translateX', 
                            value=1, driverValue=1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_jaw_rt_shift'.format(characterPrefix), currentDriver='jaw_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_jaw_rt_shift'.format(characterPrefix), currentDriver='jaw_CTRL.translateX', 
                            value=1, driverValue=-1, inTangentType='linear', outTangentType='linear')
    
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_slide'.format(characterPrefix), currentDriver='mouth_CTRL.Sideways', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_slide'.format(characterPrefix), currentDriver='mouth_CTRL.Sideways', 
                            value=1, driverValue=1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_slide'.format(characterPrefix), currentDriver='mouth_CTRL.Sideways', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_slide'.format(characterPrefix), currentDriver='mouth_CTRL.Sideways', 
                            value=1, driverValue=-1, inTangentType='linear', outTangentType='linear')
    
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipUp'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipUp'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateY', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipDn'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipDn'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateY', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipUp1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipUp1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateY', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipDn1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipDn1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateY', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipUp1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipUp1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateY', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipDn1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipDn1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateY', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipUp2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipUp2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateY', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipDn2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipDn2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateY', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipUp2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipUp2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateY', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipDn2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipDn2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateY', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    ## Bot Lip Middle
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipLeft'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipLeft'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateX', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRight'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRight'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateX', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipFwd'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipFwd'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateZ', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipBak'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipBak'.format(characterPrefix), currentDriver='bot_lip_CTRL.translateZ', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotXPos'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotXPos'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateX', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotXNeg'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotXNeg'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateX', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotYPos'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotYPos'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateY', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotYNeg'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotYNeg'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateY', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotZPos'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotZPos'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateZ', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotZNeg'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_botLipRotZNeg'.format(characterPrefix), currentDriver='bot_lip_CTRL.rotateZ', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    ## Left Bot Lip1
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipLeft1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipLeft1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateX', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRight1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRight1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateX', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipFwd1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipFwd1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateZ', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipBak1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipBak1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.translateZ', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotXPos1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotXPos1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateX', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotXNeg1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotXNeg1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateX', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotYPos1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotYPos1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateY', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotYNeg1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotYNeg1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateY', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotZPos1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotZPos1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateZ', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotZNeg1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotZNeg1'.format(characterPrefix), currentDriver='lf_bot_lip_01_CTRL.rotateZ', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    ## Left Bot Lip2
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipLeft2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipLeft2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateX', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRight2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRight2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateX', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipFwd2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipFwd2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateZ', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipBak2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipBak2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.translateZ', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotXPos2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotXPos2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateX', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotXNeg2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotXNeg2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateX', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotYPos2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotYPos2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateY', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotYNeg2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotYNeg2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateY', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotZPos2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotZPos2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateZ', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotZNeg2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_lf_botLipRotZNeg2'.format(characterPrefix), currentDriver='lf_bot_lip_02_CTRL.rotateZ', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    ## Right Bot Lip1
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipLeft1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipLeft1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateX', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRight1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRight1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateX', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipFwd1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipFwd1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateZ', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipBak1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipBak1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.translateZ', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotXPos1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotXPos1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateX', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotXNeg1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotXNeg1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateX', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotYPos1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotYPos1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateY', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotYNeg1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotYNeg1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateY', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotZPos1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotZPos1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateZ', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotZNeg1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotZNeg1'.format(characterPrefix), currentDriver='rt_bot_lip_01_CTRL.rotateZ', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    ## Right Bot Lip2
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipLeft2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipLeft2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateX', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRight2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRight2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateX', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipFwd2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipFwd2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateZ', 
                            value=1, driverValue=0.1, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipBak2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipBak2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.translateZ', 
                            value=1, driverValue=-0.1, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotXPos2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotXPos2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateX', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotXNeg2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateX', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotXNeg2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateX', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotYPos2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotYPos2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateY', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotYNeg2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateY', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotYNeg2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateY', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')

    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotZPos2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotZPos2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateZ', 
                            value=1, driverValue=90.0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotZNeg2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateZ', 
                            value=0, driverValue=0, inTangentType='linear', outTangentType='linear')
    cmds.setDrivenKeyframe('FacialBlendshapes.{0}_mouth_rt_botLipRotZNeg2'.format(characterPrefix), currentDriver='rt_bot_lip_02_CTRL.rotateZ', 
                            value=1, driverValue=-90.0, inTangentType='linear', outTangentType='linear')
    