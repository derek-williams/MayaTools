import pymel.core as pm
import sys

class neckRope:
    
    def checkNeck(ogoat, ygoat, troll):
        ogoat = 'Main_Neck_jnt1_OldGoat'
        ygoat = 'Main_Neck_jnt1_YoungGoat'
        troll = 'Troll_neck_jnt'
        if pm.objExists(ogoat):
            return True
        elif pm.objExists(troll):
            return True
        elif pm.objExists(ygoat):
            return True
        else:
            return False
        
    def duplicateJoint(self, checkTrue):
    
        