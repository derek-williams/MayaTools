#face sdk setup
import maya.cmds as cmds
import maya.mel as mel
import random

cmds.curve(name = 'rt_palm_CTRL', d = 1, p = [(.05,0,0), (.95,0,0), (.98, .02, 0), (1,.05,0), (1,.95,0),(.98,.98,0),(.95,1,0), (.05,1,0),(.02,.98,0),(0,.95,0), (0,.05,0),(.02,.02,0),(.05,0,0)])
cmds.curve(name = 'rt_thumb_CTRL', d = 1, p = [(1,.1,0), (1.4,.4,0), (1.4, 1.38,0), (1.38,1.4,0), (1.18, 1.4,0),(1.16,1.38,0),(1.16,.75,0),(1.08,.65,0),(1,.6,0)])
cmds.curve(name = 'rt_pinky_CTRL', d = 1, p = [(0,0,0),(0,.7,0),(.02,.73,0),(.05, .75,0),(.15,.75,0),(.18,.73,0),(.2,.7,0),(.2,0,0)])
cmds.curve(name = 'rt_ring_CTRL', d = 1, p = [(0,0,0),(0,.8,0),(.02,.83,0),(.05, .85,0),(.15,.85,0),(.18,.83,0),(.2,.8,0),(.2,0,0)])
cmds.curve(name = 'rt_mid_CTRL', d = 1, p = [(0,0,0),(0,.9,0),(.02,.93,0),(.05, .95,0),(.15,.95,0),(.18,.93,0),(.2,.9,0),(.2,0,0)])
cmds.curve(name = 'rt_index_CTRL', d = 1, p = [(0,0,0),(0,.75,0),(.02,.78,0),(.05, .8,0),(.15,.8,0),(.18,.78,0),(.2,.75,0),(.2,0,0)])
cmds.select('rt_index_CTRL', 'rt_pinky_CTRL', 'rt_ring_CTRL', 'rt_mid_CTRL', r = True)
cmds.move (0,1,0)
cmds.select('rt_ring_CTRL', r = True)
cmds.move(.25,0,0,r = True)
cmds.select('rt_mid_CTRL', r = True)
cmds.move(.5,0,0,r = True)
cmds.select('rt_index_CTRL', r = True)
cmds.move(.75,0,0,r = True)

cmds.select('rt_index_CTRL', 'rt_pinky_CTRL', 'rt_ring_CTRL', 'rt_mid_CTRL', 'rt_palm_CTRL', 'rt_thumb_CTRL', r = True)
selection = cmds.ls(sl = True, sn = True)
i = 1
for each in selection:
    cmds.setAttr((each + '.tx'), lock= True, keyable= False, channelBox =False )
    cmds.setAttr((each + '.ty'), lock= True, keyable= False, channelBox =False) 
    cmds.setAttr((each + '.tz'), lock= True, keyable= False, channelBox =False )
    cmds.setAttr((each + '.rx'), lock= True, keyable= False, channelBox =False )
    cmds.setAttr((each + '.ry'), lock= True, keyable= False, channelBox =False )
    cmds.setAttr((each + '.rz'), lock= True, keyable= False, channelBox =False )
    cmds.setAttr((each + '.sx'), lock= True, keyable= False, channelBox =False )
    cmds.setAttr((each + '.sy'), lock= True, keyable= False, channelBox =False )
    cmds.setAttr((each + '.sz'), lock= True, keyable= False, channelBox =False )
    cmds.setAttr((each + '.visibility'), lock= True, keyable= False, channelBox =False )

cmds.select('rt_index_CTRL', 'rt_pinky_CTRL', 'rt_ring_CTRL', 'rt_mid_CTRL','rt_thumb_CTRL',r = True)
cmds.addAttr(shortName = 'base', defaultValue=0, minValue=-10, maxValue=10, keyable = True )
cmds.addAttr(shortName = 'mid', defaultValue=0, minValue=-10, maxValue=10, keyable = True  )
cmds.addAttr(shortName = 'tip', defaultValue=0, minValue=-10, maxValue=10, keyable = True  )
cmds.addAttr(shortName = 'spread', defaultValue=0, minValue=-10, maxValue=10, keyable = True  )
cmds.addAttr(shortName = 'twist', defaultValue=0, minValue=-10, maxValue=10, keyable = True  )

cmds.select('rt_palm_CTRL', r = True)
cmds.addAttr(shortName = 'palm_bend', defaultValue=0, minValue=-10, maxValue=10, keyable = True )
cmds.addAttr(shortName = 'palm_cup', defaultValue=0, minValue=-10, maxValue=10, keyable = True  )

cmds.select('rt_index_CTRL', 'rt_pinky_CTRL', 'rt_ring_CTRL', 'rt_mid_CTRL', 'rt_palm_CTRL', 'rt_thumb_CTRL', r = True)
    
cmds.group(name = 'rt_hand_null_CTRL')
