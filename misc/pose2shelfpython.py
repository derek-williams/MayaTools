import maya.cmds as cmds
import maya.mel as mel

def selection2shelf(s):
    selection = cmds.ls(sl = True)
    shelf_label = cmds.textFieldGrp('optional_label', q = True, text = True)
    selection_size = len(selection)
    if selection_size == 0:
        cmds.warning("nothing is selected please blame Maya (the person not the program)")
    else:
        name_space = cmds.referenceQuery( selection[0], filename=True, shortName=True )
        print name_space
        if "." in name_space: 
            name_space, param = name_space.split(".",1)
        shelf_command = r'selection = cmds.ls(sl = True)' + "\n" + r'name_space = cmds.referenceQuery(selection[0],  referenceNode=True)' + "\n" + r'if "RN" in name_space: ' + "\n\t" + r'name_space, param = name_space.split("RN",1)' + "\n" + r'name_space = name_space + ":"' + "\n" + r'cmds.select(clear = True)'
        
        for each in selection:
            ctrl_name_str = str(each)
            name_space_list = ctrl_name_str.split(":")
            name_space_amount = len(name_space_list)
            
            actual_name_space = name_space_list[0]
            each = name_space_list[(name_space_amount -1)]
            i = 1 
            if name_space_amount != 1:
                while i < name_space_amount - 1:
                    actual_name_space = actual_name_space + ":" +  name_space_list[i]
                    i = (i+ 1)
            
            name_space = actual_name_space + ":"
            
            if "'" in name_space: 
                param, name_space = actual_name_space.split("'",1) 
            shelf_step = r'cmds.select(name_space + "' + each + r'", add = True)'
            shelf_command = shelf_command + "\n" + shelf_step
        shelf_level = mel.eval('$tempMelVar = $gShelfTopLevel')
        tab_level = cmds.tabLayout ( shelf_level, q = True,st = True)
        cmds.shelfButton(enableCommandRepeat = 1, enable= 1,width= 34, height =34, annotation = 'selection', parent = (shelf_level + "|" + tab_level), command = shelf_command, iol = shelf_label, st = "textOnly",  label = shelf_label,  image1 = "cmdWndIcon.png")
   
            
    return
#selection working need to redeclare each so it does not include namespaces    
def pose2shelf(s):
    selection = cmds.ls(sl = True)
    shelf_label = cmds.textFieldGrp('optional_label', q = True, text = True)
    selection_size = len(selection)
    if selection_size == 0:
        cmds.warning ("nothing is selected. Derek obviously didn't code for this contingency. Maybe he should have thought about that before handing it off to people.")
    else:
        name_space = cmds.referenceQuery( selection[0], filename=True, shortName=True )
        print name_space
        if "." in name_space: 
            name_space, param = name_space.split(".",1)
        shelf_command = r'selection = cmds.ls(sl = True)' + "\n" + r'name_space = cmds.referenceQuery(selection[0],  referenceNode=True)' + "\n" + r'if "RN" in name_space: ' + "\n\t" + r'name_space, param = name_space.split("RN",1)' + "\n" + r'name_space = name_space + ":"' + "\n" + r'cmds.select(clear = True)'
    
        
        
        for each in selection:
            ctrl_name_str = str(each)
            name_space_list = ctrl_name_str.split(":")
            name_space_amount = len(name_space_list)
            
            actual_name_space = name_space_list[0]
            each = name_space_list[(name_space_amount -1)]
            i = 1 
            if name_space_amount != 1:
                while i < name_space_amount - 1:
                    actual_name_space = actual_name_space + ":" +  name_space_list[i]
                    i = (i+ 1)
            
            name_space = actual_name_space + ":"
            
            if "'" in name_space: 
                param, name_space = actual_name_space.split("'",1) 
            keyableAttrs = cmds.listAttr(name_space + each, r = True, w = True, k = True, u = True, v = True, m = True, s = True)
            attrlen = len(keyableAttrs)
            if attrlen != None:
                for attr in keyableAttrs:
                    value = cmds.getAttr(name_space + each + "." + attr)
                    shelf_step =r'cmds.setAttr(name_space + "' + each + "." + str(attr) + r'",' + " " + str(value) + r')'
                    shelf_command = str(shelf_command)  + "\n" + shelf_step
        
        shelf_level = mel.eval('$tempMelVar = $gShelfTopLevel')
        tab_level = cmds.tabLayout ( shelf_level, q = True,st = True)
        cmds.shelfButton(enableCommandRepeat = 1, enable= 1,width= 34, height =34, annotation = 'pose', parent = (shelf_level + "|" + tab_level), command = shelf_command, iol = shelf_label, st = "textOnly",  label = shelf_label,  image1 = "cmdWndIcon.png")
    return

window = cmds.window(title = "pose to shelf", iconName = 'short name', w = 2 ,s = False )
cmds.columnLayout()
cmds.text('Optional Label:')
cmds.textFieldGrp('optional_label', w = 110)
cmds.button(label ='pose2shelf', command = pose2shelf)
cmds.text('Or')
cmds.button(label = 'selection2shelf', command = selection2shelf)
cmds.showWindow (window)





