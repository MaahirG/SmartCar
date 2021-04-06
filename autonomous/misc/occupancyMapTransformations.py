import math


def shiftPosition(grid,row_new,col_new):
    grid[midCoords][midCoords] = 3
    grid[row_new][col_new] = 4



def horizontal(grid,boolDirection): # Shfiting the grid horizontally so it's always 41x41, straight = 1, backward = 0
    if(boolDirection):
        shiftPosition(grid, midCoords, midCoords-1) # this line should be first or the grid will be shifted
        for row in grid:
            row.pop(gridSize-1)           # this is 41
            row.insert(0,5)
    else:
        shiftPosition(grid, midCoords,midCoords+1)
        for row in grid:
            row.pop(0)
            row.append(5)
    return



def vertical(grid,boolDirection): # Shfiting the grid vertically so it's always 41x41, left = 0, right = 1
    if(boolDirection):
        shiftPosition(grid, midCoords-1,midCoords)
        grid.pop(gridSize-1)           # this is 41
        grid.insert(0,[5 for i in range(gridSize)])
    else:
        shiftPosition(grid, midCoords+1,midCoords)  #rows increase downwards
        grid.pop(0)
        grid.append([5 for i in range(gridSize)])
    return



def thresholdDetection(grid, diameter, x, y, objectNumber):
    half = math.floor(diameter/2)  # 5/2 = 2 --> -2,-1,0,1,2
    start = 0 - half
    if diameter%2==0:
        print("Use an odd number for diameter for uniformity.")
        return

    indexStoringList = []
    for index,i in enumerate(range(start,half+1)):
        grid[x+i][y] = objectNumber
        if i<0:
            start2 = 0-index # index = 1: -1 start, +1 end
            end = 0+index
            indexStoringList.append(index)
            for j in range(start2,end+1): # if index is 0, none, index = 1, go up 1 down 1, index 
                grid[x+i][y+j] = objectNumber
        elif i > 0:
            startDescent = 0-indexStoringList[len(indexStoringList)-1]
            endDescent = 0 + indexStoringList[len(indexStoringList)-1]
            indexStoringList.pop()
            for j in range(startDescent,endDescent+1):
                grid[x+i][y+j] = objectNumber
        else: 
            print("You are at the middle!")
        
        # don't need it twice, above covers it 
        grid[x][y+i] = objectNumber
        
    return




grid = []
rows = []
gridSize = 41 # global
for i in range(gridSize): # size is actually gridSize x gridSize, stops 1 before gridSize, but starts at index 0
    for j in range(gridSize):
        rows.append(2) # '2' is the unknown value
    grid.append(rows)
    rows = []        

midCoords = math.ceil(gridSize/2) - 1 # the middle block ceil(gridSize/2) - 1 because 0th index
print(midCoords)

grid[midCoords][midCoords] = 4 # Current Position

'''
Occupancy Map Legend:
0-Obstacle
1-Empty Space
2-Unexplored
3-Ego Car Path
4-Ego Car Position
5-Added layers testing
'''

# Testing Grid
objectNumber = 8
thresholdDetection(grid, 7, 13, 21, objectNumber)

# horizontal(grid,1) # mutable objects like lists are pass by reference
vertical(grid,1)
vertical(grid,1)
# horizontal(grid,1)

for row in grid:
    print(row)

# each tile is 10cm. 
# emulates other stuff moving around but really ego car is just moving around
# assumption: no reving up controls - we maintain slow speed in autonomous mode so 1 tile @startup is the same as 1 tile from full speed
# in a real autonomous car, the updates come from the radar and lidar, which is how the pose of obstacles or cars is updated, here were updating their pose
# based on the ego cars movement closer to them.

# Using MNIST data to get sign
# can cover the cars with a blanket and then take it off quickly to test and show realtime mapping and trajectory planning
# Replacement for ranging and tracking techniques with sensors
# first detect the object, then get object dx dy w.r.t another object that is probably already on the map with a predetermined label
# written on a sign: 26  23  1  2 3
# dx dy referencing object 1, being object 2, size of object (changes mapped diameter)
# object 1 would already be on the map and now we have object 2 to be put on the roadmap as an obstacle