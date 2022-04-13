#Imports
import pygame
import gameObject as go
pygame.init()

#Global Constants
GAMEWINDOW_WIDTH = 1280
GAMEWINDOW_HEIGHT = 720
GAMEWINDOW_SIZE = (GAMEWINDOW_WIDTH,GAMEWINDOW_HEIGHT)

MAX_GAMEOBJECTS = 200
MAX_TEXTURES = 50

Z_LAYERS = 10

IMG_ID_PLACEHOLDER = 0

KEY_MOVEMENT_UP = pygame.K_w
KEY_MOVEMENT_DOWN = pygame.K_s
KEY_MOVEMENT_LEFT = pygame.K_a
KEY_MOVEMENT_RIGHT = pygame.K_d

#Global arrays
textureList = [pygame.Surface((0,0))]*MAX_TEXTURES
objectList = [go.GameObject()]*MAX_GAMEOBJECTS
inputArray = []

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
    
loadTextures()

#Contains the main logic code which gets executed every tick
def mainLogic():
    getInput()
    moveKeyboardMoveables()

#Moves objects which are moved by keyboard
def moveKeyboardMoveables():
    for obj in objectList:
        if obj.movedByKeyboard:

            global flag

            if inputArray[KEY_MOVEMENT_UP]:

                if not obj.receivesCollision:
                    obj.y -= obj.movementSpeedY
                else:
                    tempy = obj.y - obj.movementSpeedY
                    flag = False

                    for obj2 in objectList:
                        if obj2.causesCollision:

                            if obj == obj2: continue

                            if detectCollision( obj.x, obj.x + obj.texture.get_width(),
                                                tempy, tempy + obj.texture.get_height(),
                                                obj2.x, obj2.x + obj2.texture.get_width(),
                                                obj2.y, obj2.y + obj2.texture.get_height()
                                              ): flag = True

                    if not flag:
                        obj.y -= obj.movementSpeedY

            if inputArray[KEY_MOVEMENT_DOWN]:

                if not obj.receivesCollision:
                    obj.y += obj.movementSpeedY
                else:
                    tempy = obj.y + obj.movementSpeedY
                    flag = False

                    for obj2 in objectList:
                        if obj2.causesCollision:

                            if obj == obj2: continue

                            if detectCollision( obj.x, obj.x + obj.texture.get_width(),
                                                tempy, tempy + obj.texture.get_height(),
                                                obj2.x, obj2.x + obj2.texture.get_width(),
                                                obj2.y, obj2.y + obj2.texture.get_height()
                                              ): flag = True

                    if not flag:
                        obj.y += obj.movementSpeedY

            if inputArray[KEY_MOVEMENT_LEFT]:

                if not obj.receivesCollision:
                    obj.x -= obj.movementSpeedX
                else:
                    tempx = obj.x - obj.movementSpeedX
                    flag = False

                    for obj2 in objectList:
                        if obj2.causesCollision:

                            if obj == obj2: continue

                            if detectCollision( tempx, tempx + obj.texture.get_width(),
                                                obj.y, obj.y + obj.texture.get_height(),
                                                obj2.x, obj2.x + obj2.texture.get_width(),
                                                obj2.y, obj2.y + obj2.texture.get_height()
                                              ): flag = True

                    if not flag:
                        obj.x -= obj.movementSpeedX

            if inputArray[KEY_MOVEMENT_RIGHT]:

                if not obj.receivesCollision:
                    obj.x += obj.movementSpeedX
                else:
                    tempx = obj.x + obj.movementSpeedX
                    flag = False

                    for obj2 in objectList:
                        if obj2.causesCollision:

                            if obj == obj2: continue

                            if detectCollision( tempx, tempx + obj.texture.get_width(),
                                                obj.y, obj.y + obj.texture.get_height(),
                                                obj2.x, obj2.x + obj2.texture.get_width(),
                                                obj2.y, obj2.y + obj2.texture.get_height()
                                              ): flag = True

                    if not flag:
                        obj.x += obj.movementSpeedX

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
    texture=textureList[IMG_ID_PLACEHOLDER],
    movedByKeyboard=True, movementSpeedX=1, movementSpeedY=1,
    receivesCollision=True, causesCollision=True
    )

objectList[freeGameObject()] = go.GameObject(
    x=100, y=300, on=True,
    texture=textureList[IMG_ID_PLACEHOLDER],
    movedByKeyboard=True, movementSpeedX=1, movementSpeedY=1,
    receivesCollision=True,causesCollision=True
    )

objectList[freeGameObject()] = go.GameObject(
    x=400, y=500, on=True,
    texture=textureList[IMG_ID_PLACEHOLDER],
    movedByKeyboard=True, movementSpeedX=1, movementSpeedY=1,
    receivesCollision=True, causesCollision=True
    )

objectList[freeGameObject()] = go.GameObject(
    x=200, y=200, on=True,
    texture=textureList[IMG_ID_PLACEHOLDER],
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