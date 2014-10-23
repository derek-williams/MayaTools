import maya.cmds as cmds
import re

#select objects imported into your scene and run this script

selection = cmds.ls(sl=True)
for current in selection:
    obj_name = re.search("[^_]*$", current)
    cmds.select(current, r=True)
    cmds.rename(obj_name.group(0))
    