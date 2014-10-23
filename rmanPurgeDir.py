import maya.standalone
maya.standalone.initialize(name='python')

from pymel.all import *
import maya.cmds as cmds
import os

"""List all .ma files in current directory and sub-directories"""
# The top argument for walk
topdir = 'zod\\ProjectX'
# The extension to search for
exten = '.ma'
# Append maya scene pathes in a variable "myFiles"
results = str()
myFiles = [] 
for dirpath, dirnames, files in os.walk(topdir):
for name in files:
if name.lower().endswith(exten):

results = '%s' % os.path.join(dirpath, name)
myFiles.append(results)

"""For all files run commands"""
for i in myFiles:
cmds.file(i, force=True, open=True)
# Maya Commands : delete rman nodes
mel.eval('''rmanPurgePlugin;''')
# Save the file	
cmds.file(save=True, force=True)
