#Imports
import pygame
import gameObject as go
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

fontList[FONT_ID_DEBUG] = pygame.font.Font("assets/debugfont.ttf", 24)

animationSetList[ANIM_SMALLTOBIG_DEBUG] = [IMG_ID_SMALLBLOCKDEBUG,IMG_ID_BIGBLOCKDEBUG]
animationTimeList[ANIM_SMALLTOBIG_DEBUG] = [30,30]

#Init values of array
for i in range(MAX_GAMEOBJECTS):
    objectList[i].overwritable = True

#Game window
gameWindow = pygame.display.set_mode(GAMEWINDOW_SIZE)

#Global event catcher
debugModeFlag = False
debugMode = False
def catchEvents():
    global debugMode
    global debugModeFlag
    
    for e in pygame.event.get():
        
        if e.type == pygame.QUIT:
            global gameWindowStatus
            gameWindowStatus = False

    if inputArray[KEY_EDITOR] and not debugModeFlag:
        debugModeFlag = True
        debugMode = not debugMode

        if debugMode:
            #DEBUG MENU CREATION
            objectList[freeGameObject()] = go.GameObject(
                z = 9, on = True,
                fontContent = " - Edit mode", fontType = FONT_ID_DEBUG,
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
                        text = fontList[o.fontType].render(o.fontContent, True, o.fontColor)
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
            target.levelEditorSelected = True

    elif not mouseinput[0] and editorSelectFlag:
        editorSelectFlag = False

def rescaleSelected():

    for o in objectList:
        if o.levelEditorSelected:
            if o.on:

                if o.texture.get_width() <= 1:
                    o.setTextureSize(2, o.texture.get_height())
                if o.texture.get_height() <= 1:
                    o.setTextureSize(o.texture.get_width(), 2)

                if inputArray[KEY_RESCALE_HIGHER_X]:
                    o.setTextureSize(o.texture.get_width() + EDITOR_RESCALESPEED, o.texture.get_height())
                if inputArray[KEY_RESCALE_HIGHER_Y]:
                    o.setTextureSize(o.texture.get_width(), o.texture.get_height() + EDITOR_RESCALESPEED)
                if inputArray[KEY_RESCALE_LOWER_X]:
                    o.setTextureSize(o.texture.get_width() - EDITOR_RESCALESPEED, o.texture.get_height())
                if inputArray[KEY_RESCALE_LOWER_Y]:
                    o.setTextureSize(o.texture.get_width(), o.texture.get_height() - EDITOR_RESCALESPEED)

                if inputArray[KEY_MOVEMENT_RIGHT]:
                    o.x += EDITOR_MOVESPEED
                if inputArray[KEY_MOVEMENT_LEFT]:
                    o.x -= EDITOR_MOVESPEED
                if inputArray[KEY_MOVEMENT_UP]:
                    o.y -= EDITOR_MOVESPEED
                if inputArray[KEY_MOVEMENT_DOWN]:
                    o.y += EDITOR_MOVESPEED

#Level editor (debug menu)
def levelEditor():
    selectInEditor()
    rescaleSelected()

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