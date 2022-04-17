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
MAX_TEXTURES = 50

Z_LAYERS = 10

IMG_ID_PLACEHOLDER = 0
IMG_ID_SMALLBLOCKDEBUG = 1
IMG_ID_BIGBLOCKDEBUG = 2

ANIM_SMALLTOBIG_DEBUG = 0

KEY_MOVEMENT_UP = pygame.K_w
KEY_MOVEMENT_DOWN = pygame.K_s
KEY_MOVEMENT_LEFT = pygame.K_a
KEY_MOVEMENT_RIGHT = pygame.K_d

#Global arrays
textureList = [pygame.Surface((0,0))]*MAX_TEXTURES
objectList = [go.GameObject()]*MAX_GAMEOBJECTS
inputArray = []

animationSetList = [
    [IMG_ID_SMALLBLOCKDEBUG,IMG_ID_BIGBLOCKDEBUG] #DEBUG SMALL TO BIG // ANIM_SMALLTOBIG_DEBUG
]
animationTimeList = [
    [30,30] #DEBUG SMALL TO BIG // ANIM_SMALLTOBIG_DEBUG
]

#Init values of array
for i in range(MAX_GAMEOBJECTS):
    objectList[i].overwritable = True

#Game window
gameWindow = pygame.display.set_mode(GAMEWINDOW_SIZE)

#Global event catcher
def catchEvents():
    for e in pygame.event.get():
        
        if e.type == pygame.QUIT:
            global gameWindowStatus
            gameWindowStatus = False

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
                    if o.texture == None:
                        continue
                    else:
                        window.blit(o.texture,(o.x,o.y))

    pygame.display.update()
    
    return True

#Finds the first overwritable gameobject
def freeGameObject():
    for i in range(MAX_GAMEOBJECTS):
        if objectList[i].overwritable:
            return i

#Load textures in memory
def loadTextures():
    textureList[IMG_ID_PLACEHOLDER] = pygame.image.load("assets/placeholder.png")
    textureList[IMG_ID_SMALLBLOCKDEBUG] = pygame.image.load("assets/smallblock.png")
    textureList[IMG_ID_BIGBLOCKDEBUG] = pygame.image.load("assets/bigblock.png")
    
loadTextures()

#Limit the cpu speed
def limitCpuSpeed():
    Clock.tick(GAMEWINDOW_FPS)

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

#Contains the main logic code which gets executed every tick
def mainLogic():
    limitCpuSpeed()
    getInput()
    moveKeyboardMoveables()
    animateAnimated()

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

#Init phase end
#Custom code here

objectList[freeGameObject()] = go.GameObject(
    x=200, y=500, on=True,
    texture=textureList[IMG_ID_SMALLBLOCKDEBUG],
    movedByKeyboard=True, movementSpeedX=1, movementSpeedY=1,
    receivesCollision=True, causesCollision=True,
    animationState = ANIM_SMALLTOBIG_DEBUG
    )

objectList[freeGameObject()] = go.GameObject(
    x=200, y=200, on=True,
    texture=textureList[IMG_ID_SMALLBLOCKDEBUG],
    causesCollision=True
    )

objectList[freeGameObject()] = go.GameObject(
    x=900, y=200, on=True,
    texture=textureList[IMG_ID_BIGBLOCKDEBUG],
    causesCollision=True
    )

#Main loop
gameWindowStatus = True
while gameWindowStatus:
    
    catchEvents()
    mainLogic()
    renderObjects(gameWindow)

#Unload pygame
pygame.quit()