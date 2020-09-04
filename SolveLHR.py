from PIL import Image
from math import floor

"""Setup Functions"""

# Gets nessecary information about the maze in order to trave it
def SetupLHR():
    global PIX, BLOCKSIZE, PATHSIZE
    # Opens the maze file
    maze = OpenMaze()
    # Gets pixel width and height of the maze
    width, height = maze.size
    PIX = maze.load()

    # Finds the blocksize of the maze
    BLOCKSIZE = FindBlockSize(width, height)
    if BLOCKSIZE % 3 != 0:
        print("Maze Cannot be solved with LHR to to blocksize")
        return False

    # Finds the 'Pathsize' which is 1/3 the blocksize
    PATHSIZE = int(BLOCKSIZE / 3)

    # Finds the start block and the direction of stave out of it
    start = FindStartBlock(width, height)
    DOT = FindDOT(start)
    x, y = FindStartPoint(DOT, start)

    # Travels the maze
    TravelMazeLHR(x, y, DOT)
    maze.save('SolvedLHR.png')
    pass

# Opens the randomly generated maze
def OpenMaze():
    maze = Image.open('Maze.png')
    return maze

# Determines the pixel dimensions of each square 'pixel block'
def FindBlockSize(width, height):
    for x in range(0, width):
        for y in range(0, height):
            if ColorCheck(x, y, (255, 255, 255)):
                BLOCKSIZE = int(x / 2)
                return BLOCKSIZE

# Determines the initial direction of travel
def FindDOT(start):
    # DOT is the direction where there is a white pixel
    if ColorCheck(start[0]*BLOCKSIZE, (start[1]-1)*BLOCKSIZE, (255, 255, 255)):
        return 'U'
    elif ColorCheck((start[0]+1)*BLOCKSIZE, start[1]*BLOCKSIZE, (255, 255, 255)):
        return 'R'
    elif ColorCheck(start[0]*BLOCKSIZE, (start[1]+1)*BLOCKSIZE, (255, 255, 255)):
        return 'D'
    elif ColorCheck((start[0]-1)*BLOCKSIZE, start[1]*BLOCKSIZE, (255, 255, 255)):
        return 'L'

# Finds the start of the maze
def FindStartBlock(width, height):
    # Looks for a red pixel because that denotes the start
    for x in range(2, int(width / BLOCKSIZE)):
        for y in range(2, int(height / BLOCKSIZE)):
            if ColorCheck(x*BLOCKSIZE, y*BLOCKSIZE, (255, 0, 0)):
                return [x, y]

# Finds the starting pixel, must be on the left wall relative to the direction of travel
def FindStartPoint(DOT, start):
    if DOT == 'U':
        return start[0]*3, start[1]*3-3
    elif DOT == 'R':
        return start[0]*3+3, start[1]*3
    elif DOT == 'D':
        return start[0]*3+2, start[1]*3+3
    elif DOT == 'L':
        return start[0]*3-3, start[1]*3+2


"""Navigate Maze Functions"""

# Travels the maze from start to finish
def TravelMazeLHR(x, y, DOT):
    while (True):
        # Calls a travel funcction based on the current DOT
        if DOT == 'U':
            DrawPath(x*PATHSIZE, PATHSIZE, y*PATHSIZE, BLOCKSIZE, (0,0,255))
            x, y, DOT = Up(x, y)
        elif DOT == 'R':
            DrawPath(x*PATHSIZE, BLOCKSIZE, y*PATHSIZE, PATHSIZE, (0,0,255))
            x, y, DOT = Right(x, y)
        elif DOT == 'D':
            DrawPath(x*PATHSIZE, PATHSIZE, y*PATHSIZE, BLOCKSIZE, (0,0,255))
            x, y, DOT = Down(x, y)
        elif DOT == 'L':
            DrawPath(x*PATHSIZE, BLOCKSIZE, y*PATHSIZE, PATHSIZE, (0,0,255))
            x, y, DOT = Left(x, y)

        # Checks to see if the maze has been solved
        if Solved(x, y):
            if DOT == 'U' or DOT == 'D':
                DrawPath(x*PATHSIZE, PATHSIZE, y*PATHSIZE, BLOCKSIZE, (0,0,255))
            if DOT == 'L' or DOT == 'R':
                DrawPath(x*PATHSIZE, BLOCKSIZE, y*PATHSIZE, PATHSIZE, (0,0,255))
            return True

# Actions to be taken if the current direction of travel is Up
def Up(x, y):
    # Checks if there is a path to the navigators left relative to the direction of travel
    if ColorCheck(x*PATHSIZE - BLOCKSIZE, y*PATHSIZE - PATHSIZE, (255, 255, 255)):
        DrawPath(x*PATHSIZE, PATHSIZE, (y-1) * PATHSIZE, PATHSIZE, (0,0,255))
        return x-3 , y - 1, 'L'
    # Checks to see if there is wall immediately in front of the navigator
    elif not ColorCheck(x*PATHSIZE, y*PATHSIZE-BLOCKSIZE, (255, 255, 255)):
        DrawPath(x*PATHSIZE, BLOCKSIZE, y*PATHSIZE, PATHSIZE, (0,0,255))
        return x, y, 'R'
    else:
        return x, y-3, 'U'

# Actions to be taken if the current direction of travel is Right
def Right(x, y):
    # Checks if there is a path to the navigators left relative to the direction of travel
    if ColorCheck(x*PATHSIZE + BLOCKSIZE, y * PATHSIZE - BLOCKSIZE, (255, 255, 255)):
        DrawPath((x+3)*PATHSIZE, PATHSIZE, y*PATHSIZE, PATHSIZE, (0,0,255))
        return x+3 , y-3, 'U'
    # Checks to see if there is wall immediately in front of the navigator
    elif not ColorCheck(x*PATHSIZE+BLOCKSIZE, y*PATHSIZE, (255, 255, 255)):
        return x+2, y, 'D'
    else:
        return x+3, y, 'R'

# Actions to be taken if the current direction of travel is Down
def Down(x, y):
    # Checks if there is a path to the navigators left relative to the direction of travel
    if ColorCheck(x*PATHSIZE+PATHSIZE, y*PATHSIZE+BLOCKSIZE, (255, 255, 255)):
        DrawPath(x*PATHSIZE, PATHSIZE, (y+3)*PATHSIZE, PATHSIZE, (0,0,255))
        return x+1 , y+3, 'R'
    # Checks to see if there is wall immediately in front of the navigator
    elif not ColorCheck(x*PATHSIZE, y*PATHSIZE+BLOCKSIZE, (255, 255, 255)):
        return x-2, y+2, 'L'
    else:
        return x, y+3, 'D'

# Actions to be taken if the current direction of travel is Left
def Left(x, y):
    # Checks if there is a path to the navigators left relative to the direction of travel
    if ColorCheck(x*PATHSIZE-PATHSIZE, y*PATHSIZE+PATHSIZE, (255, 255, 255)):
        DrawPath((x-1)*PATHSIZE, PATHSIZE, y*PATHSIZE, PATHSIZE, (0, 0, 255))
        return x-1 , y+1, 'D'
    # Checks to see if there is wall immediately in front of the navigator
    elif not ColorCheck(x*PATHSIZE-PATHSIZE, y*PATHSIZE, (255, 255, 255)):
        return x, y-2, 'U'
    else:
        return x-3, y, 'L'

# Checks to see if the maze has been solved
def Solved(x, y):
    # Checks all directions looking for the green finish block
    if ColorCheck(x*PATHSIZE, (y-1)*PATHSIZE, (0, 255, 0))\
    or ColorCheck((x+3)*PATHSIZE, y*PATHSIZE, (0, 255, 0))\
    or ColorCheck(x*PATHSIZE, (y+3)*PATHSIZE, (0, 255, 0))\
    or ColorCheck((x-1)*PATHSIZE, y*PATHSIZE, (0, 255, 0)):
        return True
    else:
        return False


"""Versatile Functions"""

# Check if a pixel is of a certain color
def ColorCheck(x, y, color):
    if PIX[x, y] == color:
        return True
    return False

# Draws the path from start to finish
def DrawPath(startX, pathWidth, startY, pathHeight, color):
    for x in range(startX, startX + pathWidth):
        for y in range(startY, startY + pathHeight):
            PIX[x,y] = color
