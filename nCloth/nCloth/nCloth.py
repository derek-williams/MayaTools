import pymel.all as pm

if pm.objExists('YoungGoat_Anim_Rig_REF:YoungGoat_Anim_Model_REF:rope'):
    pm.select('YoungGoat_Anim_Rig_REF:YoungGoat_Anim_Model_REF:rope')
    pm.nClothCreate
elif pm.objExists('OldGoat_Anim_Rig_REF:OldGoat_Anim_Model_REF:rope'):
    pm.select('OldGoat_Anim_Rig_REF:OldGoat_Anim_Model_REF:rope')
    pm.nClothCreate
else:
    print('Warning: no surface exists, you dick')