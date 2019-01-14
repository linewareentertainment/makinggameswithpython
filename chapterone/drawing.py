# Python Modules
import sys

# 3rd party mods
import pygame
from pygame.locals import *

# local mods

pygame.init()

# Set up the window
DISPLAYSURF = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption("Lineware Entertainment")

# set up the colors
BLACK = ( 10, 10, 10)
WHITE = (250,250,250)
RED = (250, 10, 10)
GREEN = (10, 250, 10)
BLUE = (10, 10, 250)

# draw on the surace object
DISPLAYSURF.fill(WHITE)
pygame.draw.polygon(DISPLAYSURF, # surface
                    GREEN, # Color
                    ((146, 0), (291, 106), (236, 277), (156, 277), (0, 106))) # pointlist

pygame.draw.line(DISPLAYSURF, # surface
                    BLUE, # Color
                    (60, 60), (291, 106), 4) # pointlist
pygame.draw.line(DISPLAYSURF, # surface
                    BLUE, # Color
                    (16, 0), (129, 106)) # pointlist
pygame.draw.circle(DISPLAYSURF,
                   BLUE,
                   (100, 50), # pos
                   20,  # Radius
                   0) # width
pygame.draw.ellipse(DISPLAYSURF,
                    RED,
                    (100, 250, 40, 80), # rect
                    1)
pygame.draw.rect(DISPLAYSURF,
                 RED,
                 (20,150,100,50))

# you can see the 6 little dots in the bottom right corner
pixObj = pygame.PixelArray(DISPLAYSURF)
pixObj[480][380] = BLACK
pixObj[182][382] = BLACK
pixObj[484][384] = BLACK
pixObj[486][386] = BLACK
pixObj[488][388] = BLACK
del pixObj

while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()