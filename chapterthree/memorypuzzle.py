# Memory Puzzle

import random
import sys

import pygame
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
SCREENSIZE = (WINDOWWIDTH, WINDOWHEIGHT)
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 10
BOARDHEIGHT = 7
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even' \
                                            ' number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
BLUE     = (  0,   0, 255)
GREEN    = (  0, 255,   0)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
# not typing all that shit it

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is " \
                                                                        "too big for the number of shapes/colors defined"


def startGameAnimation(mainBoard):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(mainBoard, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(mainBoard, boxGroup)
        coverBoxesAnimation(mainBoard, boxGroup)

def getRandomizedBoard():
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape,color))
    random.shuffle(icons)
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons)

    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def generateRevealedBoxesData(param):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([param] * BOARDHEIGHT)
    return revealedBoxes

def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def drawBoard(mainBoard, revealedBoxes):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top,
                                                         BOXSIZE,
                                                         BOXSIZE))
                shape, color = getShapeAndColor(mainBoard, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def getBoxAtPixel(mousex, mousey):
    # Basically these 2 for loops will allow the code to
    # run over all instances of the size of the board and
    # return each one.  It first checks the columns then it
    # checks each row for that column
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(mousex, mousey):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)

    left, top = leftTopCoordsOfBox(boxx, boxy)

    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half),
                           half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half),
                           quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter,
                                              BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top),
                                                 (left + BOXSIZE - 1, top + half),
                                                 (left + half, top + BOXSIZE - 1),
                                                 (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left +
                                                                   i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1),
                             (left + BOXSIZE - 1, top - 1))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5,
                                                   BOXSIZE + 10, BOXSIZE + 10), 4)


def getShapeAndColor(mainBoard, boxx, boxy):
    #     This one is going to be tuff,  let me take a sip of my coffee
    return mainBoard[boxx][boxy][0], mainBoard[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(mainBoard, boxesToReveal):
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED):
        drawBoxCovers(mainBoard, boxesToReveal, coverage)


def coverBoxesAnimation(mainBoard, boxesToCover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(mainBoard, boxesToCover, coverage)


def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True

def gameWonAnimation(mainBoard):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawBoard(mainBoard, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def main():
    global FPSCLOCK, DISPLAYSURF

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)

    mousex = 0
    mousey = 0

    pygame.display.set_caption('Lineware Entertainment')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True:
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP
                                      and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex,mousey)
        boxLoc = (boxx, boxy)
        if boxx != None and boxy != None:
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx,boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [boxLoc])
                revealedBoxes[boxx][boxy] = True

                if firstSelection == None:
                    firstSelection = boxLoc
                else:
                    icon1shape, icon1color = getShapeAndColor(mainBoard,
                                                              firstSelection[0],
                                                              firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard,
                                                              boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard,
                                            [(firstSelection[0], firstSelection[1]),
                                             boxLoc])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        startGameAnimation(mainBoard)
                    firstSelection = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
