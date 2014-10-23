from ui import *
from buildScripts import pxUtilities


def pxBuildFace():
        
    charName = queryCharName()
    shortCharName = charName[1:]
    #charName = "_YoungGoat"
    
    # face parent constraints    
    if charName == "_YoungGoat":
        headChildren = ['nose_tip_jnt_grp' + charName, 'YoungGoat_Anim_Model_REF:YoungGoat_Anim_upr_Gums_GEO', 'YoungGoat_Anim_Model_REF:YoungGoat_Anim_UprTeeth_GEO', 'YoungGoat_Anim_Model_REF:YoungGoat_Anim_Tearduct_GEO', 'YoungGoat_Anim_Model_REF:YoungGoat_Anim_horns_GEO']
        jawChildren = ['tongue_Joints_grp' + charName, 'YoungGoat_Anim_Model_REF:YoungGoat_Anim_lwr_Gums_GEO', 'YoungGoat_Anim_Model_REF:YoungGoat_Anim_LwrTeeth_GEO']
    if charName == "_OldGoat":
        headChildren = ['nose_tip_jnt_grp' + charName, 'OldGoat_Anim_Model_REF:OldGoat_Anim_Upr_Gums_GEO', 'OldGoat_Anim_Model_REF:OldGoat_Anim_Upr_Teeth_GEO', 'OldGoat_Anim_Model_REF:OldGoat_Anim_Tearduct_GEO', 'OldGoat_Anim_Model_REF:OldGoat_Anim_Horns_GEO']
        jawChildren = ['tongue_Joints_grp' + charName, 'OldGoat_Anim_Model_REF:OldGoat_Anim_Lwr_Gums_GEO', 'OldGoat_Anim_Model_REF:OldGoat_Anim_Lwr_Teeth_GEO']
    
                  
    for each in headChildren:
        parentConstraint("head_jnt" + charName, each, mo = True)
        
    for each in jawChildren:
        parentConstraint("jaw_mid_jnt" + charName, each, mo = True)
    
    # eye control setup
    parentConstraint("vision_ctrl" + charName, "l_eye_ctrl_grp" + charName, mo = True)
    parentConstraint("vision_ctrl" + charName, "r_eye_ctrl_grp" + charName, mo = True)
        
    # primary head skinning
    
    faceJoints = [nt.Joint(u'head_jnt' + charName),
                 nt.Joint(u'jaw_rot_jnt' + charName),
                 nt.Joint(u'lip_jnt' + charName),
                 nt.Joint(u'l_eye_jnt' + charName),
                 nt.Joint(u'l_top_eyelid_jnt' + charName),
                 nt.Joint(u'l_btm_eyelid_jnt' + charName),
                 nt.Joint(u'r_eye_jnt' + charName),
                 nt.Joint(u'r_top_eyelid_jnt' + charName),
                 nt.Joint(u'r_btm_eyelid_jnt' + charName),
                 nt.Joint(u'jaw_mid_jnt' + charName),
                 nt.Joint(u'jaw_end_jnt' + charName),
                 nt.Joint(u'Main_Neck_jnt4' + charName),
                 nt.Joint(u'nose_tip_jnt' + charName),
                 nt.Joint(u'l_ear_Main_root' + charName),
                 nt.Joint(u'r_ear_Main_root' + charName),
                 nt.Joint(u'Main_Neck_jnt3' + charName)]
    select (faceJoints)
    
    pxUtilities.pxAddSkinCluster('head_jnt' + charName, "face_setup_primary_bind_mesh" + charName, faceJoints, charName,True)
    
    #add the weights
    select ('face_setup_primary_bind_mesh' + charName)
    pxDataManager.applyWeights(charName)
            
    #select('face_setup_primary_bind_mesh_YoungGoat')
    
    # controls
    parentConstraint("jaw_ctrl" + charName, "jaw_rot_jnt" + charName, mo = True)
    parentConstraint("Main_Neck_jnt5" + charName, "head_jnt" + charName, mo = True)
    parentConstraint("ikHeadCtrl" + charName, "head_jnt" + charName, mo = True)
    
    parentConstraint("FK_headCtrl" + charName, "jaw_ctrl_grp" + charName, mo = True)
    parentConstraint("ikHeadCtrl" + charName, "jaw_ctrl_grp" + charName, mo = True)
    
    parentConstraint("FK_headCtrl" + charName, "vision_ctrl_grp" + charName, mo = True)
    parentConstraint("ikHeadCtrl" + charName, "vision_ctrl_grp" + charName, mo = True)
    
    connectAttr("IKFK_Neck_conditionalNode.outColorR", "vision_ctrl_grp" + charName + "_parentConstraint1.FK_headCtrl" + charName + "W0")
    connectAttr("IKFK_Neck_conditionalNode.outColorG", "vision_ctrl_grp" + charName + "_parentConstraint1.ikHeadCtrl" + charName + "W1")
    
    connectAttr("IKFK_Neck_conditionalNode.outColorR", "jaw_ctrl_grp" + charName + "_parentConstraint1.FK_headCtrl" + charName + "W0")
    connectAttr("IKFK_Neck_conditionalNode.outColorG", "jaw_ctrl_grp" + charName + "_parentConstraint1.ikHeadCtrl" + charName + "W1")
    
    connectAttr("IKFK_Neck_conditionalNode.outColorR", "head_jnt" + charName + "_parentConstraint1.Main_Neck_jnt5" + charName + "W0")
    connectAttr("IKFK_Neck_conditionalNode.outColorG", "head_jnt" + charName + "_parentConstraint1.ikHeadCtrl" + charName + "W1")
    
    # blendshape 1 setup
    
    select("face_setup_secondary_bind_mesh" + charName, r = True)
    select("face_setup_primary_bind_mesh" + charName, tgl = True)
    select("face_setup_wrap_mesh" + charName, tgl = True)
    blendShape(n = "face_deform_shapes")
    setAttr("face_deform_shapes.face_setup_secondary_bind_mesh" + charName, 1)
    setAttr("face_deform_shapes.face_setup_primary_bind_mesh" + charName, 1)
    
    
    # wrap deformer setup
    
    select("faceVerts", r = True) #these verts are composed of a selection set pre-existing in the maya scene, they belong to the mesh - select("YoungGoat_Head_Shape_GEO")
    select("face_setup_wrap_mesh" + charName, tgl = True)
     
    mel.eval('CreateWrap')
    headWrap = listConnections("face_setup_wrap_mesh" + charName)[0]
    rename(headWrap,'headWrap')
    
    #create a blendshape from the wraped headbody, and from the normal skin cluster onto a new "TopGuy




