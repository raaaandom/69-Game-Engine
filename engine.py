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

#Main loop
gameWindowStatus = True
while gameWindowStatus:
    pass

#Unload pygame
pygame.quit()