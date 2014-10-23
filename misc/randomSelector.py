import maya
import maya.cmds as mc
import random
from random import random, randint

rockList = mc.ls( sl=True )
numRocks = len(rockList)

randRock = randint(0,(numRocks-1))
mc.select(cl=True)
for i in range(randRock):
    mc.select(rockList[randint(0,(numRocks-1))], toggle=True)