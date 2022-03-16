#Imports
import pygame
import gameObject
pygame.init()

#Constant values
GAMEWINDOW_WIDTH = 1920
GAMEWINDOW_HEIGHT = 1080
GAMEWINDOW_SIZE = (GAMEWINDOW_WIDTH,GAMEWINDOW_HEIGHT)

#Game window
gameWindow = pygame.display.set_mode(GAMEWINDOW_SIZE)

#Event catcher
def catchEvents():
    for e in pygame.event.get():
        
        if e.type == pygame.QUIT:
            global gameWindowStatus
            gameWindowStatus = False

        #Catch other events here

#Main loop
gameWindowStatus = True
while gameWindowStatus:
    
    catchEvents()

#Unload pygame
pygame.quit()