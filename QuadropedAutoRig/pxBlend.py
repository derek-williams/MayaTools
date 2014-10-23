'''
Created on Jun 26, 2014

@author: rgarcia
'''
from ui import *
from buildScripts import pxUtilities
'''
def cacheGeoBlends():

    charName = queryCharName()
    
    if charName == '_YoungGoat':
    
        geo =[nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_R_OtrEye_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_R_MidEye_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_R_InrEye_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_L_OtrEye_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_L_MidEye_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_L_InrEye_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_upr_Gums_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_lwr_Gums_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_Tongue_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_LwrTeeth_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_UprTeeth_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:rope'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:wrapA'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:string1A'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:string2A'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:string3A'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:loopA'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:wrapB'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:string1B'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:string2B'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:string3B'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:loopB'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:Bell'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:latch'),
     nt.Transform(u'YoungGoat_Body_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_horns_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_Tearduct_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_FR_Hoof_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_FL_Hoof_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_BR_Hoof_GEO'),
     nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_BL_Hoof_GEO')] 
     
        hide ('YoungGoat_Anim_Model_REF:YoungGoat_Anim_GEO_GRP')
     
        
    if charName == '_OldGoat':
       
        geo = [nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_R_OtrEye_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_R_MidEye_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_R_InrEye_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_L_OtrEye_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_L_MidEye_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_L_InrEye_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_Tongue_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_Lwr_Gums_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_Upr_Gums_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_Lwr_Teeth_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_Upr_Teeth_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_Horns_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_udder_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_body_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_BL_Hoof_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_BR_Hoof_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_FL_Hoof_GEO'),
     nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_FR_Hoof_GEO')]

        hide('OldGoat_Anim_Model_REF:OldGoat_Anim_GEO_GRP')
    
    for each in geo:
    
        dupMesh = duplicate(each)[0]
        cacheMesh = dupMesh.replace('GEO','CACHE')
        rename (dupMesh, cacheMesh)

        #crappy exception to handle a hiccup 
        if each == 'YoungGoat_Body_GEO' :
            hide ('YoungGoat_Anim_Model_REF:YoungGoat_Anim_GEO_GRP')
            cacheMesh = rename('YoungGoat_Body_CACHE1','YoungGoat_Body_CACHE')


    
            
        #create a blendshape from the original to the new mesh 
        
        blendNode = blendShape(each, cacheMesh, name = cacheMesh + '_BlendNode')[0] 
        #if it has a namespace 
        if each.find(':') != -1:
            each = each.split(':')[1]
        setAttr(blendNode +'.'+ each, 1 )
        parent(cacheMesh,'CacheGeo_Grp')
        '''     
def getDistance():
    sel = selected()
    a = sel[0]
    b = sel[1]
    
    #create two locators and move them to the selected points
    locA = spaceLocator (name = "A")
    locB = spaceLocator (name = "B")    
    temp = parentConstraint(a, locA)
    delete (temp)
    temp = parentConstraint(b, locB)
    delete (temp)
    #find the distance between points a and b
    
    
    distNode = shadingNode('distanceBetween',asUtility=1)
    connectAttr(locA+ '.translate',distNode + '.point1')
    connectAttr(locB+ '.translate',distNode + '.point2')
    dist = getAttr (distNode + ".distance")
    delete(locA,locB,distNode)
    print  "distanceSetup('%s', '%s', %s, fullActivationDistance)"%(a,b,str(dist))
    
def distanceSetup(itemA, itemB, destinationAttrs, defaultDistance, fullActivationDistance):
    #('joint1', 'joint3', 15.0, 4)
        #itemA = 'joint1'
        #itemB = 'joint3'
        #defaultDistance = 15.0
        #fullActivationDistance = 4
        
    #check to see if distance node already exists
    if objExists("dist_%s_%s" %(itemA, itemB)) == False:
        
        locA =  spaceLocator (name = itemA + '_pointA')
        locB =  spaceLocator (name = itemB + '_pointB')
        
        
        parentConstraint(itemA, locA)
        parentConstraint(itemB, locB)
        hide(locA,locB)
        
        distNode = shadingNode('distanceBetween',asUtility=1, name = "dist_%s_%s" %(itemA, itemB))
        connectAttr(locA+ '.translate',distNode + '.point1')
        connectAttr(locB+ '.translate',distNode + '.point2')
        
        
    if objExists("dist_%s_%s" %(itemA, itemB)) == True:   
        distNode=  "dist_%s_%s" %(itemA, itemB)
    
    
    setRangeNode = shadingNode('setRange',asUtility=1,name = 'setRange_%s_%s' %(itemA, itemB))


    if defaultDistance < fullActivationDistance:
        #default is smaller - stretching
        
        connectAttr(distNode+ '.distance',  setRangeNode + '.valueX')
        setAttr(setRangeNode + ".oldMinX", defaultDistance)
        setAttr(setRangeNode + ".oldMaxX", fullActivationDistance )   
        setAttr(setRangeNode + ".minX", 0 )
        setAttr(setRangeNode + ".maxX", 1)          
        
        outputAttr = setRangeNode + ".outValueX"
    
    
    
    if defaultDistance > fullActivationDistance:
        #default is bigger - compressing
        
        
        connectAttr(distNode+ '.distance',  setRangeNode + '.valueX')
        setAttr(setRangeNode + ".oldMinX", fullActivationDistance  )
        setAttr(setRangeNode + ".oldMaxX", defaultDistance )   
        setAttr(setRangeNode + ".minX", 0 )
        setAttr(setRangeNode + ".maxX", 1)        
        
        reverseNode = shadingNode('reverse',asUtility=1,name = 'reverse_%s_%s' %(itemA, itemB))
        connectAttr (setRangeNode + ".outValueX", reverseNode + ".inputX" )   
        
        outputAttr = reverseNode+ '.outputX'
     
    for each in destinationAttrs:
        connectAttr(outputAttr , each)   


def createActivator(item):
    #item = "l_hip_jnt_YoungGoat"  
    name = item.split('_')
    name = name[0] + '_' + name[1]
    null = group(em = True,n = name + "_Null_Activator")
    activator = spaceLocator(n = name + "_Activator")
    for each in [null,activator]:
        temp = parentConstraint(item,each)
        delete (temp)
    parent (activator,null)
    parentConstraint(item,activator) 
    hide(activator)   
    return activator    
    
    




    
def attributeSetup(sourceAttr,destinationAttrs, default, fullActivation ):  
    
    itemA = sourceAttr.split('.')[0]
    itemB = destinationAttrs[0].split('.')[0]
    
    setRangeNode = shadingNode('setRange',asUtility=1,name = 'setRange_%s_%s' %(itemA, itemB))
    
    
    
    if fullActivation >0:
        setAttr(setRangeNode + ".oldMinX", default)
        setAttr(setRangeNode + ".oldMaxX", fullActivation)   
        setAttr(setRangeNode + ".minX", 1 )
        setAttr(setRangeNode + ".maxX", 0)

    if fullActivation <0:
        setAttr(setRangeNode + ".oldMinX", fullActivation)
        setAttr(setRangeNode + ".oldMaxX",default )   
        setAttr(setRangeNode + ".minX", 0 )
        setAttr(setRangeNode + ".maxX", 1)
        
    

    connectAttr(sourceAttr,  setRangeNode + '.valueX')
    
    
    reverseNode = shadingNode('reverse',asUtility=1,name = 'reverse_%s_%s' %(itemA, itemB))
    connectAttr (setRangeNode + ".outValueX", reverseNode + ".inputX" )   
    for each in destinationAttrs:
        connectAttr(reverseNode+ '.outputX', each)     

def applyCorrectives():

    #add all the corrective blends in the CorrectiveBlend_Grp
    charName = queryCharName()
    
    if charName == '_OldGoat':
        print 'still working on momma goats correctives!'
        
    if charName == '_YoungGoat': 
        blends = listRelatives("CorrectiveBlend_Grp",c = True)
        
        
        
        
        #select(blends, 'YoungGoat_Body_GEO')
        #blendShape(n = 'CorrectiveBlends_Node',frontOfChain = True)
        
        #setup blend networks and their associated blendshapes
        attributeSetup("shoulder_ctrl_YoungGoat.rotateX",['CorrectiveBlends_Node.stomach_rot50'], 0, 50 )
        #distanceSetup(itemA, itemB, destinationAttrs, defaultDistance, fullActivationDistance)
        
        
        #attributeSetup(sourceAttr,destinationAttrs, default, fullActivation )
        
        
        
        attributeSetup("l_ankle_jnt_YoungGoat.rotateZ",["CorrectiveBlends_Node.l_rear_front_of_Leg"], 0, 90 )
        attributeSetup("r_ankle_jnt_YoungGoat.rotateZ",["CorrectiveBlends_Node.r_rear_front_of_Leg"], 0, 90 )
        
        activator = createActivator("l_hip_jnt_YoungGoat")
        attributeSetup( activator + ".rotateZ",["CorrectiveBlends_Node.l_rear_shortLeg"], 0, 30 )
        attributeSetup(activator +".rotateZ",["CorrectiveBlends_Node.l_rear_longLeg"], 0, -60 )
        
        activator = createActivator("r_hip_jnt_YoungGoat")
        attributeSetup( activator + ".rotateZ",["CorrectiveBlends_Node.r_rear_shortLeg"], 0, 30 )
        attributeSetup(activator +".rotateZ",["CorrectiveBlends_Node.r_rear_longLeg"], 0, -60)
        

        parent('l_hip_Null_Activator','r_hip_Null_Activator','pelvis_ctrl_YoungGoat')
        
        distanceSetup('l_shoulder_jnt_YoungGoat', 'l_ShoulderUp_Activator',["CorrectiveBlends_Node.l_UpperShoulder"], 12.126067868, 0)
        distanceSetup('r_shoulder_jnt_YoungGoat', 'r_ShoulderUp_Activator',["CorrectiveBlends_Node.r_UpperShoulder"], 12.126067868, 0)
        
        parent('r_ShoulderUp_Activator','l_ShoulderUp_Activator', 'shoulder_ctrl_YoungGoat' )
        #blendShape('CorrectiveBlends_Node',e=1,t=[('YoungGoat_Body_GEO', 9, 'Breathing_Body_Manual', 1), ('YoungGoat_Body_GEO', 10, 'Breathing_Body_Auto', 1)])
        #clean up  the remaining activators
        activatorGrp  = group(em = True, name = "WSMeasureActivators" )
        parent([nt.Transform(u'l_shoulder_jnt_YoungGoat_pointA'),nt.Transform(u'l_ShoulderUp_Activator_pointB'),nt.Transform(u'r_shoulder_jnt_YoungGoat_pointA'),nt.Transform(u'r_ShoulderUp_Activator_pointB')],activatorGrp  )
        
        
        parent(activatorGrp, 'All_Grp_YoungGoat')
        
        
        setAttr("CorrectiveBlends_Node.Breathing_Body_Auto",1)
        setAttr("CorrectiveBlends_Node.Breathing_Body_Manual",1)

