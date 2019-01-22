from PIL import Image

"""Setup Phase Functions"""

"""Gathers all nessecary information for the solver"""
def SetupDEE():
    global PIX, BLOCKSIZE, BLOCKDIMS
    maze = OpenMaze()
    width, height = maze.size
    PIX = maze.load()
 
    #Finds the size of each 'block', as well as the the maze dimensions in block, not pixels
    BLOCKSIZE = FindBlockSize(width, height)
    BLOCKDIMS = [int (width/ BLOCKSIZE), int (height/ BLOCKSIZE)]
    
    #Finds Location of start and finish
    start = FindStart()
    finish = FindFinish()

    #Applies the DEE algorithm
    DeadEndElimination(start, finish)
    maze.save('SolvedDEE.png')

"""Opens the image file containing the maze"""
def OpenMaze():
    maze = Image.open('Maze.png')
    return maze

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
            #If the pixel read is green that marks the start
            if ColorCheck(x*BLOCKSIZE, y*BLOCKSIZE, (0, 255, 0)):
                return (x, y)


"""Elimination Phase Functions"""
def DeadEndElimination(start, finish):
    #Finds all nodes and dead ends of the initial maze
    nodes, deadEnds = FindNodesAndDeadEnds()

    #Loop will end when 2 dead ends remain (the start and the finish)
    while len(deadEnds) > 2:
        for i in deadEnds:
            point = i
            DOT = deadEnds[i]

            #If at dead end...
            while len(DOT) == 1 and point != start and point != finish:
                #Find the next node that we should will the dead end into
                nextNode = FindNextNode(point[0], point[1], DOT, nodes)

                #Fill the dead ends dependent on direction (which is what the 4 cases are)
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

                #Reassign point to the nextNode that we found and find directions 
                point = nextNode
                DOT = FindDirections(point[0], point[1])

        #Rescan the image for any dead ends
        nodes, deadEnds = FindNodesAndDeadEnds()

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

"""Does a 'scan' of the maze for all nodes and dead ends"""
def FindNodesAndDeadEnds():
    """Dictionaries will contain coordinates and all 
    the directions you can travel from that coordinate""" 
    nodes = {}
    deadEnds = {}
    for x in range(2, BLOCKDIMS[0] - 2, 2):
        for y in range(2, BLOCKDIMS[1] - 2, 2):
            #Finds all the directions we can travel
            allDirections = FindDirections(x, y)
            
            #If only 1 direction that implies dead end
            if len(allDirections) == 1:
                deadEnds[x, y] = allDirections

            #Conditions for a 'node'
            elif len(allDirections) >= 3 or allDirections == 'LU'\
            or allDirections == 'LD'\
            or allDirections == 'RU' or allDirections == 'RD':
                nodes[x, y] = allDirections
    return nodes, deadEnds

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
