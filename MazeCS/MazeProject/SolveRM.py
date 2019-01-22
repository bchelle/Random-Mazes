from PIL import Image
from math import floor
from random import randint

"""Setup Phase Functions""" 

"""Gets nessecary information to solve the maze"""
def SetupRM():
    global PIX, BLOCKSIZE, BLOCKDIMS
    #Opens maze and gets nessecary setup information
    maze = OpenMaze()
    width, height = maze.size
    PIX = maze.load()

    #Finds the Blocksize of the maze
    BLOCKSIZE = FindBlockSize(width, height)
    BLOCKDIMS = [int (width/ BLOCKSIZE), int (height/ BLOCKSIZE)]

    #Finds the start and the finish as well as all the nodes
    start = FindStart()
    finish = FindFinish()
    nodes = FindNodes()

    #Travels the maze
    TravelMazeRM(nodes, start, finish)
    maze.save('SolvedRM.png')

"""Opens the image file containing the maze"""
def OpenMaze():
    maze = Image.open('Maze.png')
    return maze

"""Finds all the nodes in the maze"""
def FindNodes():
    """Nodes is a dicitonary storing coordinates as the key and 
    directions from that node as the value"""
    nodes = {}
    for x in range(2, BLOCKDIMS[0] - 2, 2):
        for y in range(2, BLOCKDIMS[1] - 2, 2):
            allDirections = FindDirections(x, y)

            #Conditions for a block to be a 'node'
            if len(allDirections) >= 3 or allDirections == 'LU'\
            or allDirections == 'LD'\
            or allDirections == 'RU' or allDirections == 'RD'\
            or len(allDirections) == 1:
                nodes[x, y] = allDirections
    return nodes

"""Obtains the 'blocksize' of the maze"""
def FindBlockSize(width, height):
    for x in range(0, width):
        for y in range(0, height):
            if ColorCheck(x, y, (255, 255, 255)):
                BLOCKSIZE = int(x / 2)
                return BLOCKSIZE

"""Finds the start coordinates of the maze"""
def FindStart():
    for x in range(2, BLOCKDIMS[0] - 2, 2):
        for y in range(2, BLOCKDIMS[1] - 2, 2):
            #If the pixel read is red that marks the start
            if ColorCheck(x*BLOCKSIZE, y*BLOCKSIZE, (255, 0, 0)):
                return (x, y)

"""Finds the finish coordinates of the maze"""
def FindFinish():
    for x in range(2, BLOCKDIMS[0] - 2, 2):
        for y in range(2, BLOCKDIMS[1] - 2, 2):
            #If the pixel read is green that marks the finish
            if ColorCheck(x*BLOCKSIZE, y*BLOCKSIZE, (0, 255, 0)):
                return (x, y)

"""Finds all the directions you can go from any coordinate"""
def FindDirections(x, y):
    #It should be noted that 'U' is up, 'D' is down, 'R' is right...
    directions = ''

    #Checks all adjacent blocks, if theyre white... Add the direction
    if ColorCheck((x + 1)*BLOCKSIZE, y*BLOCKSIZE, (255, 255, 255)):
        directions += 'R'
    if ColorCheck((x - 1)*BLOCKSIZE, y*BLOCKSIZE, (255, 255, 255)):
        directions += 'L'
    if ColorCheck(x*BLOCKSIZE, (y + 1)*BLOCKSIZE, (255, 255, 255)):
        directions += 'D'
    if ColorCheck(x*BLOCKSIZE, (y - 1)*BLOCKSIZE, (255, 255, 255)):
        directions += 'U'
    return directions


"""Navigate Maze Functions"""

"""Navigates the maze using the Random Mouse Algorithm"""
def TravelMazeRM(nodes,  start, finish):
    #Assigns point to be the start and assigns the direction of travel
    point = start
    DOT = nodes[point]

    #Keeps navigating until the end is reached
    while point != finish:
        #Finds the next node according to current location and direction of travel
        nextNode = FindNextNode(point[0], point[1], DOT, nodes)

        #Draws the path that the mouse just travelled
        if point[0] < nextNode[0]:
            for x in range(point[0], nextNode[0]):
                DrawColor(x*BLOCKSIZE, point[1]*BLOCKSIZE, (0, 0, 255))

        elif point[0] > nextNode[0]:
            for x in range(nextNode[0] + 1, point[0] + 1):
                DrawColor(x*BLOCKSIZE, point[1]*BLOCKSIZE, (0, 0, 255))


        if point[1] < nextNode[1]:
            for y in range(point[1], nextNode[1]):
                DrawColor(point[0]*BLOCKSIZE, y*BLOCKSIZE, (0, 0, 255))

        elif point[1] > nextNode[1]:
            for y in range(nextNode[1] + 1, point[1] + 1):
                DrawColor(point[0]*BLOCKSIZE, y*BLOCKSIZE, (0, 0, 255))

        #Assign point to become the next node, and finds all the directions it can go from there
        point = nextNode
        allDirections = nodes[point]

        #Delete the direction that the mouse just came from cause we dont want him to be too dumb
        if len(allDirections) > 1:
            allDirections = allDirections.replace(OppositeDirection(DOT), '')

        #Randomly choose a direction to travel
        DOT = allDirections[randint(0, len(allDirections)- 1)]
    
    #Redraw the start as it can get colored over while the mouse is navigating   
    DrawColor(start[0]*BLOCKSIZE, start[1]*BLOCKSIZE, (255, 0, 0))

"""Finds the next node we fill the dead end into"""
def FindNextNode(x, y, DOT, nodes):
    #Jumps by 2 blocks in the direction of travel
    if DOT == 'L':
        xJump = -2
        yJump = 0
    elif DOT == 'R':
        xJump = 2
        yJump = 0
    if DOT == 'U':
        xJump = 0
        yJump = -2
    if DOT == 'D':
        xJump = 0
        yJump = 2

    x += xJump
    y += yJump
    
    #Keep jumping until we have reached a recognized node 
    while True:
        if (x, y) in nodes:
            return (x, y)
        else:
            x += xJump
            y += yJump 

"""Returns the opposite direction of the input"""
def OppositeDirection(DOT):
    if DOT == 'U':
        return 'D'
    elif DOT == 'D':
        return 'U'
    elif DOT == 'L':
        return 'R'
    elif DOT == 'R':
        return 'L'


"""Versatile Functions"""

"""Check to see if a pixel is of a certain color"""
def ColorCheck(x, y, color):
    if PIX[x, y] == color:
        return True
    return False

"""Draw a 'block' a specified color at any coordinate"""
def DrawColor(startX, startY, color):
    for x in range(startX, startX + BLOCKSIZE):
        for y in range(startY, startY + BLOCKSIZE):
            PIX[x,y] = color
    
