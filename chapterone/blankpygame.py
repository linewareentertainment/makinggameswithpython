
# this is the character length line ---------------------------------------------------

# if you read the pep 8 manual it says you should separate all you imports
# by python modules, 3rd party modules and local

# Python Modules
import sys

# 3rd Party Modules
import pygame
from pygame.locals import *

# Local Modules

# this first line is how we initialize pygame. You have to call this
pygame.init()

# The DISPLAYSURF is the surface for our game it is in caps because it is a Constant
DISPLAYSURF = pygame.display.set_mode((400, 300))

# Sets the caption on the top of the window
pygame.display.set_caption('Hello World!')

# This is our game loop
while True:
    for event in pygame.event.get(): # Checks the events

        # This is how we take inputs from the outside to process like up down
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Draws the surface objects from DISPLAYSURF
        pygame.display.update()

# The black screen is what shows up after you run the game