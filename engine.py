#Imports
import os
import pickle
import pygame
import gameObject as go
import copy
import sneUtils
pygame.init()

#Global Constants
GAMEWINDOW_WIDTH = 1280
GAMEWINDOW_HEIGHT = 720
GAMEWINDOW_SIZE = (GAMEWINDOW_WIDTH,GAMEWINDOW_HEIGHT)

GAMEWINDOW_FPS = 60

MAX_GAMEOBJECTS = 200
MAX_TEXTURES = 200
MAX_FONTS = 200
MAX_ANIMATIONS = 200
Z_LAYERS = 10

IMG_ID_PLACEHOLDER = 0
IMG_ID_SMALLBLOCKDEBUG = 1
IMG_ID_BIGBLOCKDEBUG = 2

FONT_ID_DEBUG = 0
FONT_ID_DEBUG_BOLD = 1

FONT_ID_DEBUG_SIZE = 24

ANIM_SMALLTOBIG_DEBUG = 0

KEY_MOVEMENT_UP = pygame.K_w
KEY_MOVEMENT_DOWN = pygame.K_s
KEY_MOVEMENT_LEFT = pygame.K_a
KEY_MOVEMENT_RIGHT = pygame.K_d

KEY_EDITOR = pygame.K_F12
KEY_RESCALE_LOWER_X = pygame.K_LEFT
KEY_RESCALE_HIGHER_X = pygame.K_RIGHT
KEY_RESCALE_LOWER_Y = pygame.K_DOWN
KEY_RESCALE_HIGHER_Y = pygame.K_UP
KEY_EXPORT_LEVEL = pygame.K_F11
KEY_SELECT_PRESET_EDITOR = pygame.K_1
KEY_SELECT_ATTRIBUTE_EDITOR = pygame.K_2
KEY_SCROLL_UP = pygame.K_UP
KEY_SCROLL_DOWN = pygame.K_DOWN

GROUPID_DEBUGMENU = 1

EDITOR_SELECTED_COLOR = (0,255,0)
EDITOR_SELECTED_WIDTH = 2
EDITOR_RESCALESPEED = 1
EDITOR_MOVESPEED = 2

#Global arrays
objectList = [go.GameObject()]*MAX_GAMEOBJECTS
textureList = [pygame.surface.Surface((0,0))]*MAX_TEXTURES
fontList = [pygame.font.Font("assets/debugfont.ttf", 0)]*MAX_FONTS
inputArray = []
animationSetList = [[0 for i in range(MAX_ANIMATIONS)]]
animationTimeList = [[0 for i in range(MAX_ANIMATIONS)]]

#Global arrays entries
textureList[IMG_ID_PLACEHOLDER] = pygame.image.load("assets/placeholder.png")
textureList[IMG_ID_SMALLBLOCKDEBUG] = pygame.image.load("assets/smallblock.png")
textureList[IMG_ID_BIGBLOCKDEBUG] = pygame.image.load("assets/bigblock.png")

fontList[FONT_ID_DEBUG] = pygame.font.Font("assets/debugfont.ttf", FONT_ID_DEBUG_SIZE)
fontList[FONT_ID_DEBUG_BOLD] = pygame.font.Font("assets/debugfont.ttf", FONT_ID_DEBUG_SIZE)
fontList[FONT_ID_DEBUG_BOLD].bold = True

animationSetList[ANIM_SMALLTOBIG_DEBUG] = [IMG_ID_SMALLBLOCKDEBUG,IMG_ID_BIGBLOCKDEBUG]
animationTimeList[ANIM_SMALLTOBIG_DEBUG] = [30,30]

#Init values of array
for i in range(MAX_GAMEOBJECTS):
    objectList[i].overwritable = True

#Game window
gameWindow = pygame.display.set_mode(GAMEWINDOW_SIZE)

#OBJ Attributes
GAMEOBJECT_DICT = go.GameObject.__dict__
GAMEOBJECT_ATTRIBUTES = go.GameObject().__dir__()

scrollCursor = 0
scrollUpFlag = False
scrollDownFlag = False

for i in range(len(GAMEOBJECT_ATTRIBUTES)):
    if GAMEOBJECT_ATTRIBUTES[i].startswith("_"): GAMEOBJECT_ATTRIBUTES[i] = None
    
try:
    while GAMEOBJECT_ATTRIBUTES.remove(None) == None:
        pass
except ValueError:
    pass

#Global event catcher
debugModeFlag = False
debugMode = False
def catchEvents():
    global debugMode
    global debugModeFlag
    global currentEditorMode

    for e in pygame.event.get():
        
        if e.type == pygame.QUIT:
            global gameWindowStatus
            gameWindowStatus = False

        if debugMode:
            if e.type == pygame.DROPFILE:
                importLevel(e)

    if inputArray[KEY_EDITOR] and not debugModeFlag:
        debugModeFlag = True
        debugMode = not debugMode
        currentEditorMode = 0

        if debugMode:
                
            objectList[freeGameObject()] = go.GameObject(
                x = 10, y = 10, z = 9, on = True,
                fontContent = "[F12] Edit mode", fontType = FONT_ID_DEBUG,
                groupID = GROUPID_DEBUGMENU
            )

            objectList[freeGameObject()] = go.GameObject(
                x = 10, y = GAMEWINDOW_HEIGHT - 70, z = 9, on = True,
                fontContent = "[1] New", fontType = FONT_ID_DEBUG,
                groupID = GROUPID_DEBUGMENU
            )

            objectList[freeGameObject()] = go.GameObject(
                x = 10, y = GAMEWINDOW_HEIGHT - 40, z = 9, on = True,
                fontContent = "[2] Edit", fontType = FONT_ID_DEBUG,
                groupID = GROUPID_DEBUGMENU
            )

        else:
            #DEBUG MENU CLEAR
            for o in objectList:
                if o.groupID == GROUPID_DEBUGMENU:
                    o.overwritable = True
                    o.on = False
                if o.levelEditorSelected:
                    o.levelEditorSelected = False

    elif not inputArray[KEY_EDITOR] and debugModeFlag:
        debugModeFlag = False


#Clock
Clock = pygame.time.Clock()

#GameObjects renderer
# - Returns False if the passed argument isn't a pygame.Surface
# - Returns True if everything goes well
def renderObjects(window):

    if type(window) != pygame.Surface:
        return False

    window.fill((0,0,0))

    for z in range(Z_LAYERS):
        for o in objectList:
            if o.z == z:
                if o.on:

                    if o.texture != None:
                        window.blit(o.texture,(o.x,o.y))
                    if o.fontContent != None:
                        temp = o.fontContent
                        if o.fontVariables != None:
                            for i in range(len(o.fontVariables)):
                                temp = temp.replace(o.fontVariables[i][0], str(o.fontVariables[i][1].get()))
                        text = fontList[o.fontType].render(temp, True, o.fontColor)
                        window.blit(text, (o.x,o.y))
                    if o.levelEditorSelected:
                        pygame.draw.rect(gameWindow, EDITOR_SELECTED_COLOR, (o.x,o.y,o.texture.get_width(),o.texture.get_height()), EDITOR_SELECTED_WIDTH)
                    
    pygame.display.update()
    
    return True

#Finds the first overwritable gameobject
def freeGameObject():
    for i in range(MAX_GAMEOBJECTS):
        if objectList[i].overwritable:
            return i

#Limit the cpu speed
def limitCpuSpeed():
    Clock.tick(GAMEWINDOW_FPS)

editorSelectFlag = False

#function which selects things
def selectInEditor():

    global editorSelectFlag
    mouseinput = pygame.mouse.get_pressed()

    #selection
    if mouseinput[0] and not editorSelectFlag:
        editorSelectFlag = True

        if getHighZObjUnderMouse() == None:
            return

        target = objectList[getHighZObjUnderMouse()]

        if target.levelEditorSelected:
            target.levelEditorSelected = False
        else:

            for obj in objectList:
                if obj.levelEditorSelected:
                    return

            target.levelEditorSelected = True
            currentAttributeNamePointer.set(GAMEOBJECT_ATTRIBUTES[scrollCursor])

    elif not mouseinput[0] and editorSelectFlag:
        editorSelectFlag = False

def quickEditSelected():
    for o in objectList:
        if o.levelEditorSelected:
            if o.on:

                if o.texture.get_width() <= 1:
                    o._setTextureSize(2, o.texture.get_height())
                if o.texture.get_height() <= 1:
                    o._setTextureSize(o.texture.get_width(), 2)

                if inputArray[KEY_RESCALE_HIGHER_X]:
                    o._setTextureSize(o.texture.get_width() + EDITOR_RESCALESPEED, o.texture.get_height())
                if inputArray[KEY_RESCALE_HIGHER_Y]:
                    o._setTextureSize(o.texture.get_width(), o.texture.get_height() + EDITOR_RESCALESPEED)
                if inputArray[KEY_RESCALE_LOWER_X]:
                    o._setTextureSize(o.texture.get_width() - EDITOR_RESCALESPEED, o.texture.get_height())
                if inputArray[KEY_RESCALE_LOWER_Y]:
                    o._setTextureSize(o.texture.get_width(), o.texture.get_height() - EDITOR_RESCALESPEED)

                if inputArray[KEY_MOVEMENT_RIGHT]:
                    o.x += EDITOR_MOVESPEED
                if inputArray[KEY_MOVEMENT_LEFT]:
                    o.x -= EDITOR_MOVESPEED
                if inputArray[KEY_MOVEMENT_UP]:
                    o.y -= EDITOR_MOVESPEED
                if inputArray[KEY_MOVEMENT_DOWN]:
                    o.y += EDITOR_MOVESPEED

exportFlag = False
nExport = 0
def exportLevel():
    global exportFlag
    global nExport
    if inputArray[KEY_EXPORT_LEVEL] and not exportFlag:

        exportFlag = True
        
        #Level export
        nExport=len(os.listdir("exported/"))
        export = open(f"exported/level{nExport}.sne","wb")
        exportList = []

        for obj in objectList:
            if obj.on:
                if not obj.groupID == GROUPID_DEBUGMENU:

                    backupTexture = obj.texture
                    obj.textureExportWidth = obj.texture.get_width()
                    obj.textureExportHeight = obj.texture.get_height()
                    obj.texture = pygame.image.tostring(obj.texture, 'RGBA')
                    toexport = copy.deepcopy(obj)
                    exportList.append(toexport)
                    obj.texture = backupTexture

        pickle.dump(exportList, export)

    elif not inputArray[KEY_EXPORT_LEVEL] and exportFlag:
        exportFlag = False

def importLevel(dropFileEvent):
    file = open(dropFileEvent.file, "rb")
    importList = pickle.load(file)

    for obj in objectList:
        if obj.groupID != GROUPID_DEBUGMENU:
            obj.overwritable = True
            obj.on = False

    for obj in importList:

        toimport = copy.deepcopy(obj)
        cleanid = freeGameObject()
        objectList[cleanid] = toimport
        objectList[cleanid].texture = obj.texture = pygame.image.fromstring(obj.texture, (obj.textureExportWidth, obj.textureExportHeight), 'RGBA')

def createAttributeMenu():

    global currentAttributeNamePointer
    global currentAttributeValuePointer
    global scrollCursor

    scrollCursor = 0

    currentAttributeNamePointer = sneUtils.Pointer("Select an Object")
    currentAttributeValuePointer = sneUtils.Pointer("Select an Object")

    objectList[freeGameObject()] = go.GameObject(
        x = 10, y = GAMEWINDOW_HEIGHT - 130, z = 9, on = True,
        fontContent = "[/] Value: ^value", fontType = FONT_ID_DEBUG, fontVariables = [["^value", currentAttributeValuePointer]],
        groupID = GROUPID_DEBUGMENU
    )

    objectList[freeGameObject()] = go.GameObject(
        x = 10, y = GAMEWINDOW_HEIGHT - 160, z = 9, on = True,
        fontContent = "[/] Attribute: ^attribute", fontType = FONT_ID_DEBUG, fontVariables = [["^attribute", currentAttributeNamePointer]],
        groupID = GROUPID_DEBUGMENU
    )

def destroyAttributeMenu():
    for obj in objectList:
        if obj.fontContent != None:
            if obj.fontContent.__contains__("[/]"):
                obj.on = False
                obj.overwritable = True

presetEditorFlag = False
attributeEditorFlag = False
def switchEditorMode():   
    global presetEditorFlag
    global attributeEditorFlag
    global currentEditorMode

    for obj in objectList:
        if obj.levelEditorSelected:
            return

    if inputArray[KEY_SELECT_PRESET_EDITOR] and not presetEditorFlag:
        presetEditorFlag = True

        #SELECT EDITOR MODE 1
        if currentEditorMode == 1:

            currentEditorMode = 0

        else:

            currentEditorMode = 1

            for obj in objectList:
                obj.levelEditorSelected = False
            
            destroyAttributeMenu()

    elif not inputArray[KEY_SELECT_PRESET_EDITOR] and presetEditorFlag:
        presetEditorFlag = False

    if inputArray[KEY_SELECT_ATTRIBUTE_EDITOR] and not attributeEditorFlag:
        attributeEditorFlag = True

        #SELECT EDITOR MODE 2
        if currentEditorMode == 2:

            currentEditorMode = 0

            for obj in objectList:
                obj.levelEditorSelected = False
                
            destroyAttributeMenu()

        else:

            currentEditorMode = 2

            createAttributeMenu()

    elif not inputArray[KEY_SELECT_ATTRIBUTE_EDITOR] and attributeEditorFlag:
        attributeEditorFlag = False

    for o in objectList:
        if o.groupID == GROUPID_DEBUGMENU:
            if o.fontContent != None:
                if o.fontContent.__contains__("[1]"):
                    if currentEditorMode == 1:
                        o.fontColor = (255,0,0)
                    else:
                        o.fontColor = (255,255,255)
                elif o.fontContent.__contains__("[2]"):
                    if currentEditorMode == 2:
                        o.fontColor = (255,0,0)
                    else:
                        o.fontColor = (255,255,255)

def scrollAttributes():
    global scrollCursor
    global scrollUpFlag
    global scrollDownFlag

    if inputArray[KEY_SCROLL_UP] and not scrollUpFlag:
        scrollUpFlag = True
        if scrollCursor + 1 < len(GAMEOBJECT_ATTRIBUTES):
            scrollCursor += 1
            currentAttributeNamePointer.set(GAMEOBJECT_ATTRIBUTES[scrollCursor])
            currentAttributeValuePointer.set(GAMEOBJECT_DICT.get(GAMEOBJECT_ATTRIBUTES[scrollCursor]))
        else:
            scrollCursor = 0
            currentAttributeNamePointer.set(GAMEOBJECT_ATTRIBUTES[scrollCursor])
            currentAttributeValuePointer.set(GAMEOBJECT_DICT.get(GAMEOBJECT_ATTRIBUTES[scrollCursor]))
    elif not inputArray[KEY_SCROLL_UP] and scrollUpFlag:
        scrollUpFlag = False

    if inputArray[KEY_SCROLL_DOWN] and not scrollDownFlag:
        scrollDownFlag = True
        if scrollCursor - 1 >= 0:
            scrollCursor -= 1
            currentAttributeNamePointer.set(GAMEOBJECT_ATTRIBUTES[scrollCursor])
            currentAttributeValuePointer.set(GAMEOBJECT_DICT.get(GAMEOBJECT_ATTRIBUTES[scrollCursor]))
        else:
            scrollCursor = len(GAMEOBJECT_ATTRIBUTES) - 1
            currentAttributeNamePointer.set(GAMEOBJECT_ATTRIBUTES[scrollCursor])
            currentAttributeValuePointer.set(GAMEOBJECT_DICT.get(GAMEOBJECT_ATTRIBUTES[scrollCursor]))
    elif not inputArray[KEY_SCROLL_DOWN] and scrollDownFlag:
        scrollDownFlag = False
    
#Level editor (debug menu)
def levelEditor():

    exportLevel()
    switchEditorMode()

    if currentEditorMode == 2:
        selectInEditor()
        scrollAttributes()
        updateValuesInAttributesMenu()

def updateValuesInAttributesMenu():
    global scrollCursor
    for obj in objectList:
        if obj.levelEditorSelected:
            tempDict = obj.__dict__
            currentAttributeValuePointer.set(tempDict.get(GAMEOBJECT_ATTRIBUTES[scrollCursor]))
            break

#Process animations
def animateAnimated():
    for obj in objectList:
        if obj.animationState != None:

            if obj.animationLastState != obj.animationState:
                obj.texture = textureList[animationSetList[obj.animationState][0]]
                obj.animationCounter = 0
                obj.animationFrame = 0

            obj.animationLastState = obj.animationState
            
            if obj.animationCounter == animationTimeList[obj.animationState][obj.animationFrame]:

                if obj.animationFrame + 1 == len(animationSetList[obj.animationState]):
                    obj.animationFrame = 0
                else:
                    obj.animationFrame += 1
                obj.texture = textureList[animationSetList[obj.animationState][obj.animationFrame]]
                
                obj.animationCounter = 0
            else:
                obj.animationCounter += 1

#Moves objects which are moved by keyboard and avoids collisions
def moveKeyboardMoveables():
    global tempFlag
    for obj in objectList:
        if obj.movedByKeyboard:

            if inputArray[KEY_MOVEMENT_RIGHT]:
                for i in range(obj.movementSpeedX):
                    
                    tempFlag = False
                    obj.x += 1
                    
                    for obj2 in objectList:
                        if obj2.causesCollision:

                            if obj == obj2:
                                continue

                            if detectCollision(
                                obj.x, obj.x + obj.texture.get_width(),
                                obj.y, obj.y + obj.texture.get_height(),
                                obj2.x, obj2.x + obj2.texture.get_width(),
                                obj2.y, obj2.y + obj2.texture.get_height(),
                            ): tempFlag = True

                    if tempFlag: obj.x -= 1

            if inputArray[KEY_MOVEMENT_LEFT]:
                for i in range(obj.movementSpeedX):
                    
                    tempFlag = False
                    obj.x -= 1
                    
                    for obj2 in objectList:
                        if obj2.causesCollision:

                            if obj == obj2:
                                continue

                            if detectCollision(
                                obj.x, obj.x + obj.texture.get_width(),
                                obj.y, obj.y + obj.texture.get_height(),
                                obj2.x, obj2.x + obj2.texture.get_width(),
                                obj2.y, obj2.y + obj2.texture.get_height(),
                            ): tempFlag = True

                    if tempFlag: obj.x += 1

            if inputArray[KEY_MOVEMENT_UP]:
                for i in range(obj.movementSpeedY):
                    
                    tempFlag = False
                    obj.y -= 1
                    
                    for obj2 in objectList:
                        if obj2.causesCollision:

                            if obj == obj2:
                                continue

                            if detectCollision(
                                obj.x, obj.x + obj.texture.get_width(),
                                obj.y, obj.y + obj.texture.get_height(),
                                obj2.x, obj2.x + obj2.texture.get_width(),
                                obj2.y, obj2.y + obj2.texture.get_height(),
                            ): tempFlag = True

                    if tempFlag: obj.y += 1

            if inputArray[KEY_MOVEMENT_DOWN]:
                for i in range(obj.movementSpeedY):
                    
                    tempFlag = False
                    obj.y += 1
                    
                    for obj2 in objectList:
                        if obj2.causesCollision:

                            if obj == obj2:
                                continue

                            if detectCollision(
                                obj.x, obj.x + obj.texture.get_width(),
                                obj.y, obj.y + obj.texture.get_height(),
                                obj2.x, obj2.x + obj2.texture.get_width(),
                                obj2.y, obj2.y + obj2.texture.get_height(),
                            ): tempFlag = True

                    if tempFlag: obj.y -= 1

#Updates the input array
def getInput():
    global inputArray
    inputArray = pygame.key.get_pressed()

#function that returns the object with the highest Z on the mouse position
def getHighZObjUnderMouse():

    pos = pygame.mouse.get_pos()
    for z in range(Z_LAYERS-1, -1, -1):
        for i in range(MAX_GAMEOBJECTS):

            if objectList[i].z != z:
                continue

            if not objectList[i].levelEditorSelectable:
                continue

            if not objectList[i].on:
                continue

            if (
            pos[0] > objectList[i].x and pos[0] < objectList[i].x + objectList[i].texture.get_width() and
            pos[1] > objectList[i].y and pos[1] < objectList[i].y + objectList[i].texture.get_height()
                ):
                    return i
    return None

#this function detects if there is a collision between 2 rects
def detectCollision(ax1, ax2, ay1, ay2, bx1, bx2, by1, by2):

    if(
        ((ax1>=bx1 and ax1<=bx2) and (ay1>=by1 and ay1<=by2)) or
        ((ax2>=bx1 and ax2<=bx2) and (ay1>=by1 and ay1<=by2)) or
        ((ax1>=bx1 and ax1<=bx2) and (ay2>=by1 and ay2<=by2)) or
        ((ax2>=bx1 and ax2<=bx2) and (ay2>=by1 and ay2<=by2)) or
        ((bx1>=ax1 and bx1<=ax2) and (by1>=ay1 and by1<=ay2)) or
        ((bx2>=ax1 and bx2<=ax2) and (by1>=ay1 and by1<=ay2)) or
        ((bx1>=ax1 and bx1<=ax2) and (by2>=ay1 and by2<=ay2)) or
        ((bx2>=ax1 and bx2<=ax2) and (by2>=ay1 and by2<=ay2))
        ): return True
    return False

objectList[freeGameObject()] = go.GameObject(
    x=100, y=100, z=3, on=True, texture=textureList[IMG_ID_SMALLBLOCKDEBUG],
    movedByKeyboard=True,
    movementSpeedX=4, movementSpeedY=4,
    causesCollision=True, receivesCollision=True,
    levelEditorSelectable=True
)

objectList[freeGameObject()] = go.GameObject(
    x=200, y=300, z=4, on=True, texture=textureList[IMG_ID_SMALLBLOCKDEBUG],
    causesCollision=True, receivesCollision=True,
    levelEditorSelectable=True
)

objectList[freeGameObject()] = go.GameObject(
    x=500, y=300, z=4, on=True, texture=textureList[IMG_ID_BIGBLOCKDEBUG],
    causesCollision=True, receivesCollision=True,
    levelEditorSelectable=True
)

#Main loop
gameWindowStatus = True
while gameWindowStatus:

    limitCpuSpeed()
    getInput()
    catchEvents()

    if not debugMode:
        moveKeyboardMoveables()
        animateAnimated()
    else:
        levelEditor()

    renderObjects(gameWindow)

#Unload pygame
pygame.quit()