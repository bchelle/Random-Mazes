from PIL import Image
from random import randint

"""Setup Functions"""

def SetupSM():
    global PIX, BLOCKSIZE, BLOCKDIMS
    maze = OpenMaze()
    width, height = maze.size
    PIX = maze.load()

    # Finds the size of each 'block', as well as the the maze dimensions in block, not pixels
    BLOCKSIZE = FindBlockSize(width, height)
    BLOCKDIMS = [int (width/ BLOCKSIZE), int (height/ BLOCKSIZE)]

    # Finds Location of start and finish, as well as nodes
    nodes = FindNodes()
    start = FindStart()
    finish = FindFinish()

    # Travels maze as a 'smart mouse'
    TravelMazeSM(nodes, start, finish)

    # Draws the start and finish back in
    DrawColor(start[0]*BLOCKSIZE, start[1]*BLOCKSIZE, (255, 0, 0))
    DrawColor(finish[0]*BLOCKSIZE, finish[1]*BLOCKSIZE, (0, 255, 0))

    maze.save('SolvedSM.png')

"""Opens the image file containing the maze"""
def OpenMaze():
    maze = Image.open('Maze.png')
    return maze

"""Finds all the nodes in the maze"""
def FindNodes():
    # Nodes is a dicitonary storing coordinates as the key and
    # directions from that node as the value
    nodes = {}
    for x in range(2, BLOCKDIMS[0] - 2, 2):
        for y in range(2, BLOCKDIMS[1] - 2, 2):
            allDirections = FindDirections(x, y)

            # Conditions for a block to be a 'node'
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
            # If the pixel read is red that marks the start
            if ColorCheck(x*BLOCKSIZE, y*BLOCKSIZE, (255, 0, 0)):
                return (x, y)

"""Finds the finish coordinates of the maze"""
def FindFinish():
    for x in range(2, BLOCKDIMS[0] - 2, 2):
        for y in range(2, BLOCKDIMS[1] - 2, 2):
            # If the pixel read is green that marks the finish
            if ColorCheck(x*BLOCKSIZE, y*BLOCKSIZE, (0, 255, 0)):
                return (x, y)

"""Navigation Functions"""

"""Applies the 'smart mouse' algorithm"""
def TravelMazeSM(nodes, start, finish):
    # Note: DOT is short for Direction of Travel

    # Assigns point to start and appends it to our path
    point = start
    DOT = nodes[point]
    path = [start]

    # End process when we have reached the end
    while point != finish:
        # Find the next node according to travel to
        nextNode = FindNextNode(point[0], point[1], DOT, nodes)
        # Delete the direction we departed the point from
        nodes[point] = nodes[point].replace(DOT, '')
        # Reassign point to the next node
        point = nextNode
        # Delete the direction we came from
        nodes[point] = nodes[point].replace(OppositeDirection(DOT), '')
        allDirections = nodes[point]
        if len(allDirections) > 0:
            DOT = allDirections[randint(0, len(allDirections)- 1)]
        path.append(point)

        # If we've reached a dead end, backtrack until we're not at one
        while len(allDirections) == 0 and point != finish:
            deadEnd = point
            if len(path) > 0:
                del path[len(path)-1]
                point = path[len(path)-1]
            allDirections = nodes[point]
        if len(allDirections) > 0:
            DOT = allDirections[randint(0, len(allDirections)- 1)] 
    DrawPath(path)

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

"""Finds the next node we fill the dead end into"""
def FindNextNode(x, y, DOT, nodes):
    # Jumps by 2 blocks in the direction of travel
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

    # Keep jumping until we have reached a recognized node
    while True:
        if (x, y) in nodes:
            return (x, y)
        else:
            x += xJump
            y += yJump

"""Draws the path according to the given direcitons"""
def DrawPath(path):
    for i in range(1, len(path)):
        if path[i][0] < path[i-1][0]:
            for x in range(path[i][0] + 1, path[i-1][0] + 1):
                if ColorCheck(x*BLOCKSIZE, path[i][1]*BLOCKSIZE, (255, 0, 0)):
                    continue
                DrawColor(x*BLOCKSIZE, path[i][1]*BLOCKSIZE, (0, 0, 255))

        elif path[i][0] > path[i-1][0]:
            for x in range(path[i-1][0], path[i][0]):
                if ColorCheck(x*BLOCKSIZE, path[i][1]*BLOCKSIZE, (255, 0, 0)):
                    continue
                DrawColor(x*BLOCKSIZE, path[i][1]*BLOCKSIZE, (0, 0, 255))


        if path[i][1] < path[i-1][1]:
            for y in range(path[i][1] + 1, path[i-1][1] + 1):
                DrawColor(path[i][0]*BLOCKSIZE, y*BLOCKSIZE, (0, 0, 255))

        elif path[i][1] > path[i-1][1]:
            for y in range(path[i-1][1], path[i][1]):
                DrawColor(path[i][0]*BLOCKSIZE, y*BLOCKSIZE, (0, 0, 255))

"""Finds all the directions you can go from any coordinate"""
def FindDirections(x, y):
    # It should be noted that 'U' is up, 'D' is down, 'R' is right...
    directions = ''

    # Checks all adjacent blocks, if theyre white... Add the direction
    if ColorCheck((x + 1)*BLOCKSIZE, y*BLOCKSIZE, (255, 255, 255)):
        directions += 'R'
    if ColorCheck((x - 1)*BLOCKSIZE, y*BLOCKSIZE, (255, 255, 255)):
        directions += 'L'
    if ColorCheck(x*BLOCKSIZE, (y + 1)*BLOCKSIZE, (255, 255, 255)):
        directions += 'D'
    if ColorCheck(x*BLOCKSIZE, (y - 1)*BLOCKSIZE, (255, 255, 255)):
        directions += 'U'
    return directions


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
