from pymel.all import *

from buildScripts import *


#Definitions -----------------------------------------------------------------------------------------#

def queryCharName(): 

    if radioButton(pxBuildUI.oldGoatRadioButton, q = True, sl = True) == 1:
        charName = "_OldGoat" 
        return charName 
    if radioButton(pxBuildUI.youngGoatRadioButton, q = True, sl = True) == 1:
        charName = "_YoungGoat"
        return charName 
    if radioButton(pxBuildUI.trollRadioButton, q = True, sl = True) == 1:
        charName = "_Troll"
        return charName 
    else:
        confirmDialog( title='Warning:', message='Define a character to work with!!',  defaultButton='Yes', cancelButton='No', dismissString='No' )



def loadSkeleton():
   
    charName = queryCharName()
    if charName == "_OldGoat":
        cmds.file(r"\\zod\ProjectX\Production\CG_Assets\Characters\OldGoat_Project\scenes\Rigs\TemplateBuild\OldGoat_skeleton_template_REF.ma", #example file location - this file is local to me youll need a new file location
    	typ="mayaAscii",options="v=0;",o=1,f=1)                                         #Note the cmds abbreviation here, leave it like this, we'disscuss it at our next meeting.

    if charName == "_YoungGoat":
        cmds.file(r"C:\Users\Derek\Downloads\GoatAutoRig\GoatAutoRig\YoungGoat_skeleton_template_REF.ma", 
    	typ="mayaAscii",options="v=0;",o=1,f=1)
    	
    if charName == "_Troll":
        cmds.file("Z:/_Projects/DT_Enhancing Rigs with Maya Muscle/scenes/07_begin.ma",#example file location 
    	typ="mayaAscii",options="v=0;",o=1,f=1)

    #if charName == "_Troll" .... *fill this out*       

def saveAsRef(): # try to finish this out yourselves
    ''' this function will save the current scene as the new animation scene REF'''
    charName = queryCharName()
    if charName == "_OldGoat":
        cmds.file("\\zod\ProjectX\Pre_Production\RnD\Cg_Assets\Characters\OldGoat_Project\scenes\Rigs\Previs", #example file location - this file is local to me youll need a new file location
    	typ="mayaAscii",options="v=0;",o=1,f=1)                                         #Note the cmds abbreviation here, leave it like this, we'disscuss it at our next meeting.

    if charName == "_YoungGoat":
        cmds.file("Z:/_Projects/DT_Enhancing Rigs with Maya Muscle/scenes/07_begin.ma",#example file location 
    	typ="mayaAscii",options="v=0;",o=1,f=1)
    	
    if charName == "_Troll":
        cmds.file("Z:/_Projects/DT_Enhancing Rigs with Maya Muscle/scenes/07_begin.ma",#example file location 
    	typ="mayaAscii",options="v=0;",o=1,f=1)
    
    pass



#-------------------connect----------------------------------------------------------------------------------------------------------#

def pxBuildAll():    
    '''builds all of the individual parts seperately - then uses the argument to 
        determine whether it should connect the parts or not'''
    
    charName = queryCharName() #print (charName + "backToken")
    if objExists(charName + "backToken") and objExists(charName + "backToken") and objExists(charName + "backToken") and objExists(charName + "backToken"):
        
        confirmDialog( title='Warning:', message='Some build parts are present, you must complete the setup manually', button=['Ok'], defaultButton='Yes', cancelButton='No', dismissString='No' )
     
    else:    
        pxBuildSpine.pxBuildSpine()
        pxBuildBackLegs.pxBuildBackLegs()
        pxBuildFrontLegs.pxBuildFrontLegs()
        pxBuildEars.pxBuildEars()
        pxBuildFace.pxBuildFace()
        pxBuildNeck.pxBuildNeck()
        pxBuildTail.pxBuildTail()
        pxBuildUdder.pxBuildUdder()
        pxConnect()


def pxConnect():
    
    charName = queryCharName()
    print charName
    '''This script will actually call the connection script indirectly- 
        this is so we can use some error checking here'''

    if charName == '_YoungGoat':
        tokenExistsTestList = ["back_token" + charName, "neck_token" + charName, "l_ear_token" + charName, "r_ear_token" + charName,
          "tail_token" + charName, "l_foreleg_token" + charName, "r_foreleg_token" + charName,
          "l_hindleg_token" + charName, "r_hindleg_token" + charName]

    if charName == '_OldGoat':
        tokenExistsTestList = ["back_token" + charName, "neck_token" + charName, "l_ear_token" + charName, "r_ear_token" + charName,
          "tail_token" + charName, "l_foreleg_token" + charName, "r_foreleg_token" + charName,
          "l_hindleg_token" + charName, "r_hindleg_token" + charName, "udder_token" + charName]

    trueFalse = []
    for each in tokenExistsTestList:
        #see if the obj exists
        if objExists(each) == True:
            trueFalse.append("TRUE")
        if objExists(each) == False:    
            trueFalse.append("FALSE")
            
    if "FALSE" in trueFalse:
    #warn the user that not all parts are present
        confirmDialog( title='Warning:', message='Not all build parts are present', button=['Ok'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    else:
        #check to see if all parts are exist
        print "all objects found!"
        pxConnect.pxBuildConnections.pxBuildConnections() 

        
#---------------------------------------------------------------------------------------------------------------------#
#This will be the autorig ****UI**** used to bulid rigs for any of our characters
def pxBuildUI():
    pxBuildUI.mainWindow = window( title="pxAutoRigUtil_v0.01", iconName='Short Name', widthHeight=(300, 400) )
    #showWindow( mainWindow ) # <---uncomment this to see the ui build one step at a time 

    #This first part sets up the char selection
    columnLayout()
    text(label = "  Choose a Character:")
    rowLayout(numberOfColumns = 3)
    charCollection = radioCollection()
    pxBuildUI.oldGoatRadioButton = radioButton (l = "Old Goat")
    pxBuildUI.youngGoatRadioButton = radioButton (l = "Young Goat")
    pxBuildUI.trollRadioButton = radioButton (l = "Troll")
    setParent('..')  

    #Here the tab format is established
    tabs = tabLayout(innerMarginWidth=5, innerMarginHeight=5 )

    child1 = columnLayout() #Goat tab created
    text( label = "  1. Open the charachters build skeleton:")
    rowColumnLayout(numberOfColumns=2)
    button(l="Load Startup Skeleton",command = "ui.loadSkeleton()") # when the button is pressed run the command 

    setParent( '..' ) # <--This means step back up one level and make that the previous ui item the parent, in this case we are moving from the row layout back to column


    text(label = "  2. Build an individual component and then connect ..")
    rowColumnLayout(numberOfColumns=4)
    #first row of 4
    button(l="Spine", command = "pxBuildSpine.pxBuildSpine()") 
    button(l="Neck", command = "pxBuildNeck.pxBuildNeck()")
    button(l="Ears", command = "pxBuildEars.pxBuildEars()")
    button(l="Tail", command = "pxBuildTail.pxBuildTail()")
    #second row of 4
    button(l="FrontLegs", command = "pxBuildFrontLegs.pxBuildFrontLegs()")
    button(l="BackLegs", command = "pxBuildBackLegs.pxBuildBackLegs()")
    button(l="Udder", command = "pxBuildUdder.pxBuildUdder()")
    button(l="Face", command = "pxBuildFace.pxBuildFace()")

    setParent( '..' )

    columnLayout()
        #############################
    button(l="Connect", w = 180, command = "pxBuildConnections.pxBuildConnections()")
    button(l="CleanUp!", w = 180, command = "pxCleanup.pxCleanup()")
    button(l="Add Blends", w = 180, command = "pxBlend.applyCorrectives()")    #pxBlend.cacheGeoBlends();
    #################################
    setParent("..")
    rowColumnLayout(numberOfColumns=1)
    text(label = "  ... Or Build All and Connect")
    button(label = 'Build All and Connect', w = 180, command = "ui.pxBuildAll()")
    setParent( '..' )
    text(label = "  3. Utilities ..")
    rowColumnLayout(numberOfColumns = 2)
    button(l="Select Bind Joints", command = "pass")
    button(l="Select All Controls", command = "pass")
    button(l="Save as REF", command = "pass")

    setParent(tabs) #here i set the parent back to the original tabs layout, istead of stepping up twice


    child2 = columnLayout() #troll tab created

        #..... Fill in this portion of the ui for the troll tab, it will be very similar. read up on the "setParent command if you get "cant find" errors"########################################

    text(label = "  1. Load the character default skeleton:")
    rowColumnLayout(numberOfColumns = 2)
    button(label = "Load Default Skeleton", command = "loadSkeleton()")

    setParent ( '..' )
    text(label = "  2. Build an individual component and then connect...")
    rowColumnLayout(numberOfColumns = 4)
    #row of buttons
    button(label = "Spine", width = 50, command = "pass")
    button(label = "Arms", width = 50, command = "pass")
    button(label = "Legs", width = 50, command = "pass")
    button(label = "Face", width = 50, command = "pass")

    setParent( ".." )

    columnLayout()
    button(label="Connect Components", width = 200, command = "pass")
    setParent( ".." )
    rowColumnLayout(numberOfColumns = 1)
    text(label = "  ...Or Build All and Connect")
    button(label = "Build All and Connect", w = 200, command = "pxBuildAll(True)")
    setParent( ".." )
    text(label = "  3. Utilities")
    rowColumnLayout(numberOfColumns = 2)
    button(label = "Select Bind Joints", command = "pass")
    button(label = "Select All Controls", command = "pass")
    button(label = "Save as REF", command = "pass")


    setParent( tabs ) #this is the last line of the troll tab build


    tabLayout( tabs, edit=True, tabLabel=((child1, 'Goat Builder'), (child2, 'Troll Builder')) ) ##This line edits the names of the tabs, cant d
    showWindow( pxBuildUI.mainWindow )#END   
    pxBuildUI.hello = 'test'  
    
    
    
    
