from ui import *
from buildScripts import pxUtilities



def pxBuildConnections():
    print "test"

    charName = queryCharName()

    # token creation condition
    group("back_token" + charName, "neck_token" + charName, "l_ear_token" + charName, "r_ear_token" + charName,
          "tail_token" + charName, "l_foreleg_token" + charName, "r_foreleg_token" + charName,
          "l_hindleg_token" + charName, "r_hindleg_token" + charName, name = charName + "_characterTOKEN")

    # connect hind legs
    parentConstraint("pelvis_ctrl" + charName, "l_hip_ctrl_grp" + charName, maintainOffset = True)
    parentConstraint("pelvis_ctrl" + charName, "l_back_leg_grp" + charName, maintainOffset = True)
    parentConstraint("pelvis_ctrl" + charName, "r_hip_ctrl_grp" + charName, maintainOffset = True)
    parentConstraint("pelvis_ctrl" + charName, "r_back_leg_grp" + charName, maintainOffset = True)

    # connect front legs
    parentConstraint("shoulder_ctrl" + charName, "l_shoulder_ctrl_grp" + charName, maintainOffset = True)
    parentConstraint("shoulder_ctrl" + charName, "r_shoulder_ctrl_grp" + charName, maintainOffset = True)
    parentConstraint("shoulder_ctrl" + charName, "l_foreleg_grp" + charName, maintainOffset = True)
    parentConstraint("shoulder_ctrl" + charName, "r_foreleg_grp" + charName, maintainOffset = True)

    # connect shoulder pole vectors
    group(empty = True, name = "l_shoulder_pv_grp" + charName)
    delete(pointConstraint("shoulder_ctrl" + charName, "l_shoulder_pv_grp" + charName, maintainOffset = False))
    parent("l_shoulder_pv" + charName, "l_shoulder_pv_grp" + charName)
    parent("l_shoulder_pv_grp" + charName, "shoulder_ctrl" + charName)
        
    group(empty = True, name = "r_shoulder_pv_grp" + charName)
    delete(pointConstraint("shoulder_ctrl" + charName, "r_shoulder_pv_grp" + charName, maintainOffset = False))
    parent("r_shoulder_pv" + charName, "r_shoulder_pv_grp" + charName)
    parent("r_shoulder_pv_grp" + charName, "shoulder_ctrl" + charName)

    # connect tail 
    parentConstraint("pelvis_ctrl" + charName, "tail_root_Grp" + charName, maintainOffset = True)
    
    # connect head
    parentConstraint("FK_headCtrl" + charName, "head_jnt", maintainOffset = True)

    # connect neck
    parentConstraint("shoulder_ctrl" + charName, "AllNeck_Constraint_Grp", maintainOffset = True)

    select(cl = True)

    #build helper joints
    chestHelper = joint(name = 'Chest_HelperJnt' + charName)

    chestConstraint = pointConstraint([('l_shoulder_jnt'+ charName),('r_shoulder_jnt'+ charName)], chestHelper, name = 'Chest_HelperConst' + charName)

    select(cl = True)
    lowerPelvisHelper = joint(name ='LowerPelvis_HelperJnt' + charName)

    lowerPelvisConstriant = pointConstraint([('r_hip_jnt'+ charName),('l_hip_jnt'+ charName)], lowerPelvisHelper, name = 'pelvis_HelperConst' + charName)

    # connect helper joint aim locators
    parentConstraint("shoulder_ctrl" + charName, "sternum_helper_aim_loc" + charName, mo = True)
    aimConstraint("sternum_helper_aim_loc" + charName, "Chest_HelperJnt" + charName, maintainOffset = True, wut = "objectrotation", wuo = "sternum_helper_aim_loc" + charName)
    parentConstraint("pelvis_ctrl" + charName, "pelvis_helper_aim_loc" + charName, mo = True)
    aimConstraint("pelvis_helper_aim_loc" + charName, "LowerPelvis_HelperJnt" + charName, maintainOffset = True, wut = "objectrotation", wuo = "pelvis_helper_aim_loc" + charName)
    
    #connect the ears
    print "earStart!"
    parentConstraint('head_jnt','l_ear_ctrl_grp'+ charName, mo = True)
    parentConstraint('head_jnt','r_ear_ctrl_grp'+ charName, mo = True)
    print "earEnd!"
    #setup the leg stuff
    localWsLegControls = ['r_front_foot_ctrl'+ charName,
     'l_front_foot_ctrl'+ charName,
     'r_back_foot_ctrl'+ charName,
     'l_back_foot_ctrl'+ charName
     ] 
    
    
    attrs = []
    for each in localWsLegControls:
        grpName = str(each).replace("ctrl", "localWorld_LegGrp") 
        grp = pxUtilities.aGroupAbove(grpName, each)

        attr = pxUtilities.spaceSwitcher(grp,'body_ctrl'+ charName, 'legs', 'body_ctrl'+ charName,'worldLocator')
        attrs.append(attr)
    

    localWsPvControls = ["r_wrist_pv" + charName,
    "l_wrist_pv" + charName,
    "r_ankle_pv" + charName,
    "l_ankle_pv" + charName]    

    
    i = 0
    for each in localWsPvControls:
        grpName = str(each).replace("pv", "localWorld_pvGrp")    
        grp = pxUtilities.aGroupAbove(grpName, each)
        
        attr = pxUtilities.spaceSwitcher(grp,'body_ctrl'+ charName, 'legs', 'body_ctrl'+ charName,localWsLegControls[i])
        attrs.append(attr)
        i +=1
        
    grpName = str('l_knee_pv'+ charName).replace("pv", "localWorld_pvGrp")  
    grp = pxUtilities.aGroupAbove(grpName, 'l_knee_pv'+ charName) 
    attr = pxUtilities.spaceSwitcher(grp,'body_ctrl'+ charName, 'legs', 'body_ctrl'+ charName,'l_back_foot_ctrl' + charName)
    attrs.append(attr)
    
    
    grpName = str('r_knee_pv'+ charName).replace("pv", "localWorld_pvGrp")  
    grp = pxUtilities.aGroupAbove(grpName, 'r_knee_pv'+ charName) 
    attr = pxUtilities.spaceSwitcher(grp,'body_ctrl'+ charName, 'legs', 'body_ctrl'+ charName,'r_back_foot_ctrl' + charName)
    attrs.append(attr)

    
    addAttr('body_ctrl'+ charName, ln = "feetLocalVsWorld",dv = 10, at = 'double', min = 0, max = 10, k = True)    
    
    for each in attrs:
        connectAttr('body_ctrl'+ charName + ".feetLocalVsWorld", 'body_ctrl'+ charName + "." + each)
        #set the individual controls back to not keyable, since they are directly connected to the single localvWorld switch
        print each

        setAttr('body_ctrl'+ charName + "." + each, channelBox=False,keyable=False)  
      







    
    ######-------------------------charachter specific -due to model with different naming conventions------------------------------------------------#####
    
    # ADD ANNOTATION ARROWS TO POLE VECTORS
    pxUtilities.pxAddAnnotation("l_wrist_jnt"+ charName, "l_wrist_pv"+ charName)
    pxUtilities.pxAddAnnotation("r_wrist_jnt"+ charName, "r_wrist_pv"+ charName)
    pxUtilities.pxAddAnnotation("l_ankle_jnt"+ charName, "l_ankle_pv"+ charName)
    pxUtilities.pxAddAnnotation("r_ankle_jnt"+ charName, "r_ankle_pv"+ charName)
    pxUtilities.pxAddAnnotation("l_knee_jnt"+ charName, "l_knee_pv"+ charName)
    pxUtilities.pxAddAnnotation("r_knee_jnt"+ charName, "r_knee_pv"+ charName)
        

    
    
    
    
    
    
    if charName == "_YoungGoat":
        shortCharName = charName[1:len(charName)]

        #this is the visibility attribute for the mesh resolution
        addAttr('COG',ln="meshResolution",en="Low:High:",at="enum", k = True )
        
        lowHighConditionNode = shadingNode('condition', asUtility = True, name = 'LowHighCondition_Node')
        
        setAttr(lowHighConditionNode + ".colorIfTrueG", 1)
        setAttr(lowHighConditionNode + ".colorIfFalseG", 0)
        
        connectAttr('COG.meshResolution',lowHighConditionNode + '.firstTerm')
        connectAttr(lowHighConditionNode +  '.outColorR', 'HiRez_Geo_Grp.v')
        connectAttr(lowHighConditionNode +  '.outColorG', 'LowRez_Geo_Grp.v')
        
        #HIGH POLY Hooves

        pxUtilities.pxAddSkinCluster('l_palm_jnt_YoungGoat', nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_FL_Hoof_GEO'), [nt.Joint(u'l_middlePhalanx_inner_jnt_YoungGoat'),
                                                                                                                                    nt.Joint(u'l_middlePhalanx_outer_jnt_YoungGoat'),
                                                                                                                                    nt.Joint(u'l_palm_jnt_YoungGoat')] ,charName,True) 

        pxUtilities.pxAddSkinCluster('r_palm_jnt_YoungGoat', nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_FR_Hoof_GEO'), [nt.Joint(u'r_palm_jnt_YoungGoat'),
                                                                                                                                    nt.Joint(u'r_middlePhalanx_inner_jnt_YoungGoat'),
                                                                                                                                    nt.Joint(u'r_middlePhalanx_outer_jnt_YoungGoat')],charName,True) 

        pxUtilities.pxAddSkinCluster('r_fetlock_jnt_YoungGoat', nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_BR_Hoof_GEO'), [nt.Joint(u'r_fetlock_jnt_YoungGoat'),
                                                                                                                                       nt.Joint(u'r_pastern_inner_jnt_YoungGoat'),
                                                                                                                                       nt.Joint(u'r_pastern_outer_jnt_YoungGoat')] ,charName,True) 

        pxUtilities.pxAddSkinCluster('l_fetlock_jnt_YoungGoat', nt.Transform(u'YoungGoat_Anim_Model_REF:YoungGoat_Anim_BL_Hoof_GEO'), [nt.Joint(u'l_fetlock_jnt_YoungGoat'),
                                                                                                                                    nt.Joint(u'l_pastern_inner_jnt_YoungGoat'),
                                                                                                                                    nt.Joint(u'l_pastern_outer_jnt_YoungGoat')] ,charName,True) 
        
        deformerWeights("YoungGoat_Anim_FR_Hoof_GEO.xml",path="//zod/ProjectX/Production/Tools/Depot/PipelineTools/Character_Data/_YoungGoat/VertexWeights/",im=1,method="index",deformer="YoungGoat_Anim_Model_REF:YoungGoat_Anim_FR_Hoof_GEO_SkinCluster_YoungGoat")
        print 'FRComplete'
        deformerWeights("YoungGoat_Anim_FL_Hoof_GEO.xml",path="//zod/ProjectX/Production/Tools/Depot/PipelineTools/Character_Data/_YoungGoat/VertexWeights/",im=1,method="index",deformer="YoungGoat_Anim_Model_REF:YoungGoat_Anim_FL_Hoof_GEO_SkinCluster_YoungGoat")
        print 'FLComplete'
        deformerWeights("YoungGoat_Anim_BR_Hoof_GEO.xml",path="//zod/ProjectX/Production/Tools/Depot/PipelineTools/Character_Data/_YoungGoat/VertexWeights/",im=1,method="index",deformer="YoungGoat_Anim_Model_REF:YoungGoat_Anim_BR_Hoof_GEO_SkinCluster_YoungGoat")
        print 'BRComplete'
        deformerWeights("YoungGoat_Anim_BL_Hoof_GEO.xml",path="//zod/ProjectX/Production/Tools/Depot/PipelineTools/Character_Data/_YoungGoat/VertexWeights/",im=1,method="index",deformer="YoungGoat_Anim_Model_REF:YoungGoat_Anim_BL_Hoof_GEO_SkinCluster_YoungGoat")
        print 'BLComplete'        

        #select ('YoungGoat_Anim_Model_REF:YoungGoat_Body_GEO')
        #pxDataManager.applyWeights(charName) 
        
 
        
        
        #LOW POLY
        
        #rFrontFoot
        pxUtilities.attachGeo(("r_palm_jnt" + charName),['Low_R_FrontFootPad'])
        pxUtilities.attachGeo(("r_middlePhalanx_rotate_jnt" + charName),['Low_R_FrontHoof'])
        
        #lFrontFoot
        pxUtilities.attachGeo(("l_palm_jnt" + charName),['Low_L_FrontFootPad'])
        pxUtilities.attachGeo(("l_middlePhalanx_rotate_jnt" + charName),['Low_L_FrontHoof'])
        
        #rRearFoot
        pxUtilities.attachGeo(("r_fetlock_jnt" + charName),['Low_R_ReartFootPad'])
        pxUtilities.attachGeo(("r_pastern_rotate_jnt" + charName),['Low_R_RearHoof'])
        #lRearFoot
        pxUtilities.attachGeo(("l_fetlock_jnt" + charName),['Low_L_RearFootPad'])
        pxUtilities.attachGeo(("l_pastern_rotate_jnt" + charName),['Low_L_RearHoof'])
        
    
        #pxBuildWeights

        rootJoint =  ('root_jnt' + charName) 
        bindJoints = pxDataManager.listBindJoints(charName)

        print bindJoints
        pxUtilities.pxAddSkinCluster(rootJoint, 'Low_Body', bindJoints,charName,True) 
        select ('Low_Body')
        pxDataManager.applyWeights(charName)
        
        
        bindJoints = pxDataManager.listBindJoints(charName)
        currentJoints = skinCluster('YoungGoat_Anim_Model_REF:YoungGoat_Body_GEO_SkinCluster_YoungGoat', q = True, inf = True)
        for each in bindJoints:
            if each not in currentJoints:

                skinCluster('YoungGoat_Anim_Model_REF:YoungGoat_Body_GEO_SkinCluster_YoungGoat',  addInfluence = each, dr=100 , wt=0 , edit = True , lw = False)

        deformerWeights("YoungGoat_Body_GEO.xml",path="//zod/ProjectX/Production/Tools/Depot/PipelineTools/Character_Data/_YoungGoat/VertexWeights/",im=1,method="index",deformer="YoungGoat_Anim_Model_REF:YoungGoat_Body_GEO_SkinCluster_YoungGoat")

        
        # mouth shape setup
        #setAttr('upperLipBlend.upper_lip_default', 0) 
        #connectAttr('mouth_open_srn.outValueZ', 'upperLipBlend.upper_lip_open', f = True)
        #connectAttr ('mouth_open_srn.outValueZ', 'lowerLipBlend.lower_lip_open', f = True)
        
        
        parentConstraint ('FK_headCtrl' + charName, 'head_jnt' ,mo = True)

    
        parentConstraint ('FK_headCtrl' + charName, 'CONTROLS', mo = True)
        
        parentConstraint('FK_headCtrl' + charName,'facialLocatorJointGrp',mo= True)

        
    if charName == "_OldGoat":
        
        
        #this is the visibility attribute for the mesh resolution
        addAttr('COG',ln="meshResolution",en="Low:High:",at="enum", k = True )
        
        lowHighConditionNode = shadingNode('condition', asUtility = True, name = 'LowHighCondition_Node')
        
        setAttr(lowHighConditionNode + ".colorIfTrueG", 1)
        setAttr(lowHighConditionNode + ".colorIfFalseG", 0)
        
        connectAttr('COG.meshResolution',lowHighConditionNode + '.firstTerm')
        connectAttr(lowHighConditionNode +  '.outColorR', 'HiRez_Geo_Grp.v')
        connectAttr(lowHighConditionNode +  '.outColorG', 'LowRez_Geo_Grp.v')
        
        #ParentConstraint on all the geo that isnt deforming -This will be changing
        #need to lop off the "_" from the name 
        shortCharName = charName[1:len(charName)]
        #HighPoly
        #rFrontFoot
        

        #LowPoly
        
        #rFrontFoot

        pxUtilities.attachGeo(("r_middlePhalanx_rotate_jnt" + charName),['LOW_R_FrontHoof'])
        
        #lFrontFoot

        pxUtilities.attachGeo(("l_middlePhalanx_rotate_jnt" + charName),['LOW_L_FrontHoof'])
        
        #rRearFoot
 
        pxUtilities.attachGeo(("r_pastern_rotate_jnt" + charName),['LOW_R_RearHoof'])
        #lRearFoot
   
        pxUtilities.attachGeo(("l_pastern_rotate_jnt" + charName),['LOW_L_RearHoof'])

                                                        
        #pxBuildWeights

        rootJoint = 'root_jnt' + charName
        bindJoints = pxDataManager.listBindJoints(charName)
        print bindJoints
        pxUtilities.pxAddSkinCluster(rootJoint, 'LOW_LowPoly_Body', bindJoints,charName, True) 
        select ('LOW_LowPoly_Body')
        pxDataManager.applyWeights(charName)
        
        currentJoints = skinCluster('OldGoat_Anim_Model_REF:OldGoat_Anim_body_GEO', q = True, inf = True)
        for each in bindJoints:
            if each not in currentJoints:

                skinCluster('OldGoat_Anim_Model_REF:OldGoat_Anim_body_skinCluster',  addInfluence = each, dr=100 , wt=0 , edit = True , lw = False)
        select ('OldGoat_Anim_Model_REF:OldGoat_Anim_body_GEO')
        
        removeDummyJoints = [nt.Joint(u'body_dummy_jnt'),nt.Joint(u'r_ear_dummy_jnt'),nt.Joint(u'r_ear_root'),nt.Joint(u'l_ear_dummy_jnt'),nt.Joint(u'l_ear_root')]
        for each in removeDummyJoints:
            
            skinCluster('OldGoat_Anim_Model_REF:OldGoat_Anim_body_skinCluster',e=1,ri=each)        
        
        deformerWeights("OldGoat_Anim_body_Geo.xml",path="//zod/ProjectX/Production/Tools/Depot/PipelineTools/Character_Data/_OldGoat/VertexWeights/",im=1,method="index",deformer="OldGoat_Anim_Model_REF:OldGoat_Anim_body_skinCluster")
        
        
        skinCluster("OldGoat_Anim_Model_REF:OldGoat_Anim_body_skinCluster",forceNormalizeWeights=1,e=1)
        pxUtilities.pxAddSkinCluster('l_palm_jnt_OldGoat', nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_FL_Hoof_GEO'), [nt.Joint(u'l_middlePhalanx_outer_jnt_OldGoat'),nt.Joint(u'l_middlePhalanx_inner_jnt_OldGoat'),nt.Joint(u'l_palm_jnt_OldGoat')],charName,True) 
        deformerWeights("OldGoat_FL_Hoof.xml",path="//zod/ProjectX/Production/Tools/Depot/PipelineTools/Character_Data/_OldGoat/VertexWeights/",im=1,method="index",deformer="OldGoat_Anim_Model_REF:OldGoat_Anim_FL_Hoof_GEO_SkinCluster_OldGoat")
        
        pxUtilities.pxAddSkinCluster('r_palm_jnt_OldGoat', nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_FR_Hoof_GEO'), [nt.Joint(u'r_middlePhalanx_outer_jnt_OldGoat'),nt.Joint(u'r_middlePhalanx_inner_jnt_OldGoat'),nt.Joint(u'r_palm_jnt_OldGoat')],charName,True) 
        deformerWeights("OldGoat_FR_Hoof.xml",path="//zod/ProjectX/Production/Tools/Depot/PipelineTools/Character_Data/_OldGoat/VertexWeights/",im=1,method="index",deformer="OldGoat_Anim_Model_REF:OldGoat_Anim_FR_Hoof_GEO_SkinCluster_OldGoat")
        
        pxUtilities.pxAddSkinCluster('l_fetlock_jnt_OldGoat', nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_BL_Hoof_GEO'), [nt.Joint(u'l_fetlock_jnt_OldGoat'), nt.Joint(u'l_pastern_inner_jnt_OldGoat'), nt.Joint(u'l_pastern_outer_jnt_OldGoat')],charName,True) 
        deformerWeights("OldGoat_BL_Hoof.xml",path="//zod/ProjectX/Production/Tools/Depot/PipelineTools/Character_Data/_OldGoat/VertexWeights/",im=1,method="index",deformer="OldGoat_Anim_Model_REF:OldGoat_Anim_BL_Hoof_GEO_SkinCluster_OldGoat")
        
        pxUtilities.pxAddSkinCluster('r_fetlock_jnt_OldGoat', nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_BR_Hoof_GEO'), [nt.Joint(u'r_fetlock_jnt_OldGoat'),  nt.Joint(u'r_pastern_inner_jnt_OldGoat'), nt.Joint(u'r_pastern_outer_jnt_OldGoat')],charName,True)       
        deformerWeights("OldGoat_BR_Hoof.xml",path="//zod/ProjectX/Production/Tools/Depot/PipelineTools/Character_Data/_OldGoat/VertexWeights/",im=1,method="index",deformer="OldGoat_Anim_Model_REF:OldGoat_Anim_BR_Hoof_GEO_SkinCluster_OldGoat")
        
        
        pxUtilities.pxAddSkinCluster('head_jnt', nt.Transform(u'OldGoat_Anim_Model_REF:OldGoat_Anim_Horns_GEO'), ['head_jnt'],charName,True)       
                
                
        
        
        #print "run datamanager"
        #pxDataManager.applyWeights(charName)


        #pxUtilities.pxAddSkinCluster(rootJoint, 'OldGoat_Anim_Model_REF:OldGoat_Anim_body_GEO', bindJoints,charName) 
        #select ('OldGoat_Anim_Model_REF:OldGoat_Anim_body_GEO')
        #pxDataManager.applyWeights(charName)     
        

        delete(nt.Joint(u'l_ear_root'),nt.Joint(u'r_ear_root'),nt.Joint(u'body_dummy_jnt'),nt.Joint(u'r_ear_dummy_jnt'),nt.Joint(u'l_ear_dummy_jnt')) 
        print "connections worked properly!"
        
        
        
        
        
