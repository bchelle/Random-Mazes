from PIL import Image

maze1 = Image.open('Maze5.png')
maze2 = Image.open('Maze6.png')

pix1 = maze1.load()
pix2 = maze2.load()

if maze1.size != maze2.size:
    print('Not Same Size')

same = 0
for x in range(3, maze1.size[0]-2,2):
    for y in range(3, maze2.size[0]-2,2):
        if pix1[x, y] == pix2[x, y]:
            same += 1

print(same/(999**2 - (249001) - 250000))

