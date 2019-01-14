# I love cats but I am not using any cat animation pics.  I will find
# my own

import sys
import time

import pygame
from pygame.locals import *

pygame.init()

FPS = 30 # Frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption("Lineware Entertainment")

WHITE = (250,250,250)
adventurerImg = pygame.image.load('sprites/adventurer-idle-00.png')
advX = 10
advY = 10
direction = 'right'

# Sound effects
soundObj = pygame.mixer.Sound('Sounds/LandSoft.wav')

while True: # game loop
    DISPLAYSURF.fill(WHITE)

    if direction == 'right':
        advX += 5
        if advX == 280:
            direction = 'down'
            soundObj.play()
            time.sleep(1)
            soundObj.stop()
    elif direction == 'down':
        advY += 5
        if advY == 220:
            direction = 'left'
            soundObj.play()
            time.sleep(1)
            soundObj.stop()
    elif direction == 'left':
        advX -= 5
        if advX == 10:
            direction = 'up'
            soundObj.play()
            time.sleep(1)
            soundObj.stop()
    elif direction == 'up':
        advY -= 5
        if advY == 10:
            direction = 'right'
            soundObj.play()
            time.sleep(1)
            soundObj.stop()

    DISPLAYSURF.blit(adventurerImg, (advX,advY))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)