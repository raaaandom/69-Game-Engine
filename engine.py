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
            
            if inputArray[KEY_MOVEMENT_UP]:
                obj.y -= obj.movementSpeedY
            if inputArray[KEY_MOVEMENT_DOWN]:
                obj.y += obj.movementSpeedY
            if inputArray[KEY_MOVEMENT_LEFT]:
                obj.x -= obj.movementSpeedX
            if inputArray[KEY_MOVEMENT_RIGHT]:
                obj.x += obj.movementSpeedX

#Updates the input array
def getInput():
    global inputArray
    inputArray = pygame.key.get_pressed()


#Init phase end
#Custom code here

objectList[freeGameObject()] = go.GameObject(
    x=10, y=10, on=True,
    texture=textureList[IMG_ID_PLACEHOLDER],
    movedByKeyboard=True, movementSpeedX=1, movementSpeedY=1
    )

#Main loop
gameWindowStatus = True
while gameWindowStatus:
    
    catchEvents()
    mainLogic()
    renderObjects(gameWindow)

#Unload pygame
pygame.quit()