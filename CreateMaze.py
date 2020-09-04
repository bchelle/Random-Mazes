from PIL import Image
from random import randint
from math import floor, ceil
import time
import SolveDEE, SolveLHR, SolveSM, SolveRM
import os

RUNTIMER = 1
INSTRUCTIONS = 1
SOLVERS = 1

"""Setup Phase Functions"""

def DeleteOldMazes():
    for filename in os.listdir():
        if filename.endswith(".png"):
            os.remove(filename)

# Makes a 'blank' maze, will be all red pixels, but color doesnt actually matter as long as it's not
# white or black
def MakeBlankMaze():
    maze = Image.new('RGB', (SIZE[0] * BLOCKSIZE, SIZE[1] * BLOCKSIZE), color = (255, 0, 0))
    return maze


# Gets size dimensions for the maze, as well as the size of the 'pixel blocks'
def GetMazeSize():
    """
    A valid input includes:
    1. 2 numbers are entered, space separated
    2. Both inputs must be odd positive integers
    If either of these conditions are not met then the user will be prompted again
    """
    if INSTRUCTIONS == 1:
        print("\nRules For Valid Input Size:")
        print("1.Must have exactly 2 space separated input")
        print("2.Both inputs must be ODD POSITIVE INTEGERS")
    while True:
        SIZE = input("Input Maze Size: ").split()
        if len(SIZE) == 2 and SIZE[0].isdigit() and SIZE[1].isdigit() \
        and int(SIZE[0]) % 2 == 1 and int(SIZE[1]) % 2 == 1 and int(SIZE[0])*int(SIZE[1]) > 1\
        and (int(SIZE[0]) + 4) * (int(SIZE[1]) + 4) <= 70000000:
            break

    # Increases the users input dimensions by 4 to account for the border walls that will be added
    for i in range(len(SIZE)):
            SIZE[i] = int(SIZE[i]) + 4

    """
    A valid BlockSize input includes:
    1. A single positive integer is entered
    2. If you want to use the left hand rule as a solver, the blocksize must be divisible by 3

    Note: The purpose of blocksize is to add the ability to make a smaller maze appear larger, 
    a small maze with a large blocksize will be easier to see. It does this by increasig the amount
    of pixels each block contains
    """
    if INSTRUCTIONS == 1:
        print("\nRules For Valid Input BlockSize:")
        print("1.Must Have exactly 1 input")
        print("2.The input must a POSITIVE INTEGER")
        print("Note: If the input is not divisible by 3 then the left hand solver will not work")
    while True:
        BLOCKSIZE = input("Zoom (1 or Larger): ")

        if BLOCKSIZE.isdigit() and (int(BLOCKSIZE)**2)*(SIZE[0])*(SIZE[1]) < 70000000:
            BLOCKSIZE = int(BLOCKSIZE)
            break

    # Returns the users input maze size and blocksize
    return SIZE, BLOCKSIZE


# Draws 2 black walls on all edges of the image to frame the maze
def DrawBorders():
    # Draws the top and bottom wall
    for x in range(0, SIZE[0]):
        for y in range(0, 2):
            DrawColor(x*BLOCKSIZE, y*BLOCKSIZE, (0,0,0))
        for y in range(SIZE[1]-2, SIZE[1]):
            DrawColor(x*BLOCKSIZE, y*BLOCKSIZE, (0,0,0))

    # Draws the left and right wall
    for y in range(2, SIZE[1] - 2):
        for x in range(0, 2):
            DrawColor(x*BLOCKSIZE, y*BLOCKSIZE, (0,0,0))
        for x in range(SIZE[0] - 2, SIZE[0]):
            DrawColor(x*BLOCKSIZE, y*BLOCKSIZE, (0,0,0))


# Draws the grid that will frame all the individual cells
def DrawGrid():
    for x in range(2, SIZE[0] - 1):
        for y in range(2, SIZE[1] - 1):
            if x % 2 == 1 or y % 2 == 1:
                DrawColor(x*BLOCKSIZE, y*BLOCKSIZE, (0,0,0))


"""Growing Tree Phase"""

# Applies the growing tree algorithm
def GrowTree():
    Cells = []
    # Picks a random cell to start at and appends it to the list of cells
    x, y = PickRandCell()
    Cells.append([x, y])
    DrawColor(x*BLOCKSIZE, y*BLOCKSIZE, (255,255,255))

    #Once our cell list becomes empty, that implies that the maze has been generated
    while len(Cells) > 0:
        # Finds all the possible cells that the current cell can grow into
        neighbours = FindNeighbours(Cells[len(Cells) - 1][0], Cells[len(Cells) - 1][1])

        # If we can't carve into any cells, this means that we've hit a dead end
        # and must backtrack
        if neighbours == '':
            # Delete the the most recently visited cell
            del Cells[len(Cells) - 1]

            # Check to make sure that the cell list isn't empty
            if len(Cells) > 0:
                # Assign x and y to the last cell in the list
                x = Cells[len(Cells) - 1][0]
                y = Cells[len(Cells) - 1][1]
            continue

        #Randomly chooses a 'neighbour cell' to grow into
        DOT = neighbours[randint(0, len(neighbours) - 1)]
        Cells, x, y = CarvePath(DOT, Cells, x, y)


# Randomly Selects a cell to start at
def PickRandCell():
    numCells = int((SIZE[0] - 3) / 2) * int((SIZE[1] - 3) / 2)
    randCell = randint(0, numCells - 1)
    col = randCell % int((SIZE[0] - 3) / 2)
    row = int(floor(randCell / ((SIZE[0] - 3) / 2)))

    x = col * 2 + 2
    y = row * 2 + 2

    return x, y


# Finds all the possible directions which a cell can carve into
def FindNeighbours(x, y):
    neighbours = ""
    if ColorCheck(x*BLOCKSIZE, y*BLOCKSIZE - 2*BLOCKSIZE, (255, 0, 0)):
        neighbours += 'U'
    if ColorCheck(x*BLOCKSIZE + 2*BLOCKSIZE, y*BLOCKSIZE, (255, 0, 0)):
        neighbours += 'R'
    if ColorCheck(x*BLOCKSIZE, y*BLOCKSIZE + 2*BLOCKSIZE, (255, 0, 0)):
        neighbours += 'D'
    if ColorCheck(x*BLOCKSIZE - 2*BLOCKSIZE, y*BLOCKSIZE, (255, 0, 0)):
        neighbours += 'L'
    return neighbours


# Will carve a path through the maze depending on the diection of travel
def CarvePath(DOT, Cells, x, y):
    # If up, carves to the cell above
    if DOT == 'U':
        y -= 2
        Cells.append([x, y]) # Adds the new cell coordinates to the list
        DrawColor(x*BLOCKSIZE, y*BLOCKSIZE, (255, 255, 255))
        DrawColor(x*BLOCKSIZE, (y + 1)*BLOCKSIZE, (255, 255, 255))

    # If right, carves to the cell to the right
    elif DOT == 'R':
        x += 2
        Cells.append([x, y]) # Adds the new cell coordinates to the list
        DrawColor(x*BLOCKSIZE, y*BLOCKSIZE, (255, 255, 255))
        DrawColor((x-1)*BLOCKSIZE, y*BLOCKSIZE, (255, 255, 255))

    # If Down, carves to the cell below
    elif DOT == 'D':
        y += 2
        Cells.append([x, y]) # Adds the new cell coordinates to the list
        DrawColor(x*BLOCKSIZE, y*BLOCKSIZE, (255, 255, 255))
        DrawColor(x*BLOCKSIZE, (y - 1)*BLOCKSIZE, (255, 255, 255))

    # If Left, carves to the cell to the left
    elif DOT == 'L':
        x -= 2
        Cells.append([x, y]) # Adds the new cell coordinates to the list
        DrawColor(x*BLOCKSIZE, y*BLOCKSIZE, (255, 255, 255))
        DrawColor((x+1)*BLOCKSIZE, y*BLOCKSIZE, (255, 255, 255))

    # Returns the coordinates of the new cell
    return Cells, x, y



"""Placing Start and Finish Phase Functions"""

# Finds all the dead ends in each of the 4 quadrants
def FindDeadEnds():
    deadEnds = {0:[], 1:[], 2:[], 3:[]}
    deadEnds[0] = (QuadrantDeadEnds(2, int(ceil(SIZE[0]/2)), 2, int(ceil(SIZE[1]/2))))
    deadEnds[1] = (QuadrantDeadEnds(int(ceil(SIZE[0]/2)), SIZE[0] - 2, 2, int(ceil(SIZE[1]/2))))
    deadEnds[2] = (QuadrantDeadEnds(2, int(ceil(SIZE[0]/2)), int(ceil(SIZE[1]/2)), SIZE[1] - 2))
    deadEnds[3] = (QuadrantDeadEnds(int(ceil(SIZE[0]/2)), SIZE[0] - 2 , int(ceil(SIZE[1]/2)), SIZE[1] - 2))
    DrawStartFinish(deadEnds)

# Finds all the dead ends in any of the 4 quadrants
def QuadrantDeadEnds(lowX, highX, lowY, highY):
    deadEnds = []
    for x in range(lowX,highX):
        for y in range(lowY,highY):
            if not ColorCheck(x*BLOCKSIZE, y*BLOCKSIZE, (255, 255, 255)):
                continue
            adjacent = NumAdjacent(x*BLOCKSIZE, y*BLOCKSIZE)
            if adjacent == 1:
                deadEnds.append([x, y])
    return deadEnds

# Counts the amount of adjacent cells there are from any given cell
def NumAdjacent(x, y):
    count = 0
    if ColorCheck(x, y - BLOCKSIZE, (255, 255, 255)):
        count += 1
    if ColorCheck(x, y + BLOCKSIZE, (255, 255, 255)):
        count += 1
    if ColorCheck(x + BLOCKSIZE, y, (255, 255, 255)):
        count += 1
    if ColorCheck(x - BLOCKSIZE, y, (255, 255, 255)):
        count += 1
    return count


# Places the start and  in opposite quadrants of the maze,
# with the exception that not all quadrants contain a dead end
def DrawStartFinish(deadEnds):
    eligibleQuadrants = ''
    for i in range(0,4):
        # If the quadrant has at least 1 dead end, it is considered eligible
        if len(deadEnds[i]) > 0:
            eligibleQuadrants += '{}'.format(i)

    # Randomly selects a quadrant from the list of eligible quadrants
    quadrantUsed = int(eligibleQuadrants[randint(0,len(eligibleQuadrants) - 1)])

    # Places the start in the random dead end in the randomly selected quadrant
    start = deadEnds[quadrantUsed][randint(0, len(deadEnds[quadrantUsed]) - 1)]
    DrawColor(start[0]*BLOCKSIZE, start[1]*BLOCKSIZE, (255,0,0)) # The start is a red block

    # Checks to see if the opposite quadrant is eligible, if it is thats where the finish will be place
    if len(deadEnds[3-quadrantUsed]) > 0:
        eligibleQuadrants = str(3 - quadrantUsed)
    # If the opposite quadrant has no dead ends it will randomly choose an adjacent quadrant
    elif len(eligibleQuadrants) > 1:
        eligibleQuadrants = eligibleQuadrants.replace(str(quadrantUsed), '')
    #  If there are no other eligible quadrants, the dead end will be placed in the same quadrant
    else:
        # Ensures that the finish is not placed on top of the start
        deadEnds[quadrantUsed].remove(start)

    quadrantUsed = int(eligibleQuadrants[randint(0,len(eligibleQuadrants) - 1)])

    # Randomly places the finish in the chosen quadrant
    finish = deadEnds[quadrantUsed][randint(0, len(deadEnds[quadrantUsed]) - 1)]
    DrawColor(finish[0]*BLOCKSIZE, finish[1]*BLOCKSIZE, (0, 255, 0)) #The finish will be green



"""Utility Functions"""

# Draws a square 'pixel block' of an input color
def DrawColor(startX, startY, color):
    #Example, if BLOCKSIZE = 3, will draw a block made of 3x3 pixels
    for x in range(startX, startX + BLOCKSIZE):
        for y in range(startY, startY + BLOCKSIZE):
            PIX[x,y] = color

# Checks to see if a pixel is of a certain color
def ColorCheck(x, y, color):
    if PIX[x, y] == color:
        return True
    return False



"""Main, Weaves in and out out all the phases"""
def Main():
    global SIZE, BLOCKSIZE, PIX
    DeleteOldMazes()

    # Gets user input for the maze dimensions and blocksize
    SIZE, BLOCKSIZE = GetMazeSize()

    # If you wish to time the maze generation, turn the timer on
    startTime = time.time()

    # The next four lines are setup for the maze.
    maze = MakeBlankMaze()
    PIX = maze.load()
    DrawBorders()
    DrawGrid()

    # Applies the growing tree algorithm to the setup
    GrowTree()

    # Finds all the dead ends in the maze, and randomly places the start and finish
    FindDeadEnds()

    if RUNTIMER == 1:
        print("{} Seconds To Generate Maze\n".format(time.time() - startTime))

    '''Saves the maze to 'Maze.png', which is the file that the solving algorithms
    read from'''
    maze.save("Maze.png")

    if SOLVERS == 1:
        Solvers()

"""Calls the various solving algorithms"""
def Solvers():
    # If the maze is too large, random mouse isn't practical and therefore will not solve
    if (SIZE[0]*SIZE[1] < 249001):
        # Asks if it would like to be solved with the random mouse
        if input("Solve Using Random Mouse (Y/N): ").upper() == 'Y':
            startTimeRM = time.time()
            SolveRM.SetupRM()

            if RUNTIMER == 1:
                print("{} Seconds To Solve Maze Using Random Mouse\n".format(time.time() - startTimeRM))
    # BLOCKSIZE must be divisible by 3 to apply LHR
    if BLOCKSIZE % 3 == 0:
        #Asks If it would like to be solved with the left hand rule
        if input("Solve Using Left Hand Rule (Y/N): ").upper() == 'Y':
            startTimeLHR = time.time()
            SolveLHR.SetupLHR()

            if RUNTIMER == 1:
                print("{} Seconds To Solve Maze Using Left Hand Rule\n".format(time.time() - startTimeLHR))

    # Asks if it would like to be solved with the dead end filler
    if input("Solve Using Dead End Filler (Y/N): ").upper() == 'Y':
            startTimeDEE = time.time()
            SolveDEE.SetupDEE()

            if RUNTIMER == 1:
                print("{} Seconds To Solve Maze Using Dead End Filler\n".format(time.time() - startTimeDEE))

    # Asks if it would like to be solved with the smart mouse
    if input("Solve Using Smart Mouse (Y/N): ").upper() == 'Y':
        startTimeSM = time.time()
        SolveSM.SetupSM()

        if RUNTIMER == 1:
            print("{} Seconds To Solve Maze Using Smart Mouse\n".format(time.time() - startTimeSM))


if __name__ == "__main__":
    Main()
