#Imports
import pygame
import gameObject as go
pygame.init()

#Global Constants
GAMEWINDOW_WIDTH = 1920
GAMEWINDOW_HEIGHT = 1080
GAMEWINDOW_SIZE = (GAMEWINDOW_WIDTH,GAMEWINDOW_HEIGHT)

MAX_GAMEOBJECTS = 200
MAX_TEXTURES = 50

Z_LAYERS = 10

IMG_ID_PLACEHOLDER = 0

#Global arrays
textureList = [pygame.Surface((0,0))]*MAX_TEXTURES
objectList = [go.GameObject()]*MAX_GAMEOBJECTS

#Init values of array
for i in range(MAX_GAMEOBJECTS):
    objectList[i].overwritable = True

#Game window
gameWindow = pygame.display.set_mode(GAMEWINDOW_SIZE)

#Event catcher
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

#Main loop
gameWindowStatus = True
while gameWindowStatus:
    
    catchEvents()
    renderObjects(gameWindow)

#Unload pygame
pygame.quit()