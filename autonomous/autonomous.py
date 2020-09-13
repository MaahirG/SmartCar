# MINI TESLA CODE
# BSPLINE: https://github.com/kawache/Python-B-spline-examples, https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.BSpline.html
import pygame
import math
from queue import PriorityQueue
import time
import numpy as np
import scipy.interpolate as interpolate
import matplotlib.pyplot as plt
# import jetson.inference as ji
# import jetson.utils
# import numpy as np
# import cv2

RED = (255, 0, 0) # Explored
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

COLORDICT = {0 : BLACK,
			 1 : RED,
			 2 : WHITE,
			 3 : PURPLE,
			 4 : YELLOW,
			 5 : ORANGE,
			 6 : TURQUOISE 
			 }

BOUNDARYCENTRES = {}

class Node:
	def __init__(self, row, col, tileWidth, total_rows, state):
		self.row = row
		self.col = col
		self.x = row * tileWidth
		self.y = col * tileWidth
		self.state = state
		self.color = COLORDICT[state]
		self.neighbors = []
		self.tileWidth = tileWidth
		self.total_rows = total_rows
		self.boundarySize = 0

	def get_pos(self):
		return self.row, self.col

	def is_barrier(self):
		return self.state == OBSTACLESTATE

	def is_start(self):
		return self.state == STARTSTATE

	def is_end(self):
		return self.state == ENDSTATE

	def reset(self):
		self.color = WHITE
		self.state = UNEXPLOREDSTATE
	
	def get_state(self):
		return self.state
		
	def set_state(self, state):
		if state == OBSTACLESTATE:
			color = BLACK
		elif state == EMPTYSTATE:
			color = RED
		elif state == UNEXPLOREDSTATE:
			color = WHITE
		elif state == EGOPATH:
			color = PURPLE
		elif state == EGOPOSE:
			color = YELLOW
		elif state == STARTSTATE:
			color = ORANGE
		elif state == ENDSTATE:
			color = TURQUOISE

		self.state = state
		self.color = color

	def get_color(self):
		return self.color

	def make_start(self):
		self.color = ORANGE
		self.state = STARTSTATE
	
	def make_end(self):
		self.color = TURQUOISE
		self.state = ENDSTATE

	def make_TraversedNode(self):
		self.color = RED
		self.state = EMPTYSTATE

	def make_TraversableNode(self):
		self.color = GREEN
		self.state = EMPTYSTATE

	def make_barrier(self):
		self.color = BLACK
		self.state = OBSTACLESTATE
		
	def make_path(self):
		self.color = PURPLE
		self.state = EGOPATH

	def set_boundary_size(self, size):
		self.boundarySize = size

	def get_boundary_size(self):
		return self.boundarySize

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.y, self.x, self.tileWidth, self.tileWidth)) # rectangle defined by (left (face), top (face), width height)

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

SMOOTHX = []
SMOOTHY = []

def reconstruct_path(came_from, current, draw, xList, yList):
	while current in came_from:
		p1,p2 = current.get_pos()
		xList.append(p1)
		yList.append(p2)
		current = came_from[current]
		current.make_path()
		draw()
	return xList, yList


def algorithm(draw, grid, start, end, xList, yList):
	count = 0
	current_set = PriorityQueue()		# reliant on heap sort (min sort), insert at the end of tree and propagate up, can only access the root. Delete by swapping root with end and then heapify
	current_set.put((0, count, start)) # fscore, count for tiebreaking, node
	current_set_tracker = {start}

	came_from = {} 	# dictionary, each key is a node, value is the previous node that it came from (since all the keys prior have a camefrom value, just follow the chain downwards for the whole path)
	g_score = {} # dictionary, each key is a node, value is score
	f_score = {} # dictionary, each key is a node, value is score

	# init grid unexplored scores
	for row in grid:
		for spot in row:
			g_score[spot] = float("inf")
			f_score[spot] = float("inf")

	g_score[start] = 0
	f_score[start] = h(start.get_pos(), end.get_pos())

	while not current_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current_node = current_set.get()[2] 		# get the node
		current_set_tracker.remove(current_node)

		if current_node == end:
			xList, yList = reconstruct_path(came_from, end, draw, xList, yList)
			end.make_end()
			return xList, yList

		for neighbor in current_node.neighbors:
			temp_g_score = g_score[current_node] + 1

			if temp_g_score < g_score[neighbor]:  # LESS THAN INFINITY usually or if you just visited one of the neighbours that you are looking back on, it could 
				came_from[neighbor] = current_node
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in current_set_tracker:
					count += 1
					current_set.put((f_score[neighbor], count, neighbor)) # priority queue will heapify and get the minimum fscore on the top to be taken next
					current_set_tracker.add(neighbor)
					neighbor.make_TraversableNode()

		draw()

		if current_node != start:
			current_node.make_TraversedNode()

	return xList, yList

def movement(direction, endNode, win, grid, rows, width): # moving the car vertically so it's always 41x41, left = 0, right = 1
	boundaryKeyList = []
	for node in BOUNDARYCENTRES.keys():
		boundaryKeyList.append(node)
	
	for row in range(rows):
		for col in range(rows):
			tempState = grid[row][col].get_state()
			if tempState == EGOPATH or tempState == EMPTYSTATE or tempState == ENDSTATE:
				if tempState == ENDSTATE:
					endRow, endCol = endNode.get_pos()
				grid[row][col].set_state(UNEXPLOREDSTATE)

	# not iterating through dictionary because dict values change in boundaryCreator
	for node in boundaryKeyList: # list of boundary nodes with non updated coordinates
		row, col = node.get_pos()
		size = node.get_boundary_size()
		boundaryCreator(size, row, col, 1, win, grid, rows, width) # clears the boundary and resets the states of cleared nodes
		BOUNDARYCENTRES.pop(node)
		if direction == 'right': 		# if ego moves right (upscreen) boundaries go left (downscreen)
			row += 1
		if direction == 'straight':
			col += 1
		if direction == 'left': 
			row -= 1
		if direction == 'back':
			col -= 1
		boundaryCreator(size, row, col, 0, win, grid, rows, width) # recreates the boundary - and adds to BoundaryCentreTracking dictionary
	
	if direction == 'right':
		endRow += 1
	if direction == 'straight':
		endCol += 1
	if direction == 'left': 
		endRow -= 1
	if direction == 'back':
		endCol -= 1

	# updated coords reset end point
	endNodeUpdated = grid[endRow][endCol]
	endNodeUpdated.make_end()

	draw(win, grid, rows, width)	
	return endNodeUpdated

# doesn't check edge cases, out of bounds etc
def boundaryCreator(diameter, x, y, cleanup, win, grid, rows, width):
	if cleanup:
		state = UNEXPLOREDSTATE
	else: 
		state = OBSTACLESTATE
		grid[x][y].set_boundary_size(diameter)
		if grid[x][y] not in BOUNDARYCENTRES:
			BOUNDARYCENTRES[grid[x][y]] = 1 	# boundary centre node

	half = math.floor(diameter/2)  # 5/2 = 2 --> -2,-1,0,1,2
	start = 0 - half
	if diameter%2==0:
		print("Use an odd number for diameter for uniformity.")
		return

	indexStoringList = []
	for index,i in enumerate(range(start,half+1)):
		grid[x+i][y].set_state(state)
		if i<0:
			start2 = 0-index # index = 1: -1 start, +1 end
			end = 0+index
			indexStoringList.append(index)
			for j in range(start2,end+1): # if index is 0, none, index = 1, go up 1 down 1, index 
				grid[x+i][y+j].set_state(state)
		elif i > 0:
			startDescent = 0-indexStoringList[len(indexStoringList)-1]
			endDescent = 0 + indexStoringList[len(indexStoringList)-1]
			indexStoringList.pop()
			for k in range(startDescent,endDescent+1):
				grid[x+i][y+k].set_state(state)
		else: 
			print("You are at the middle!")
		
		# don't need loops twice for the vertical line of the star, above covers it 
		grid[x][y+i].set_state(state)
		
	draw(win, grid, rows, width)	
	return

def h(p1, p2): # p1 and p2 are return values of get_pos()
	x1, y1 = p1
	x2, y2 = p2
	diffX = abs(x1 - x2)
	diffY = abs(y1 - y2)
	# return diffX + diffY # Manhattan
	return math.sqrt(diffX**2 + diffY**2)	# Euclidean

# Fill up grid with nodes
def populate_grid(numRows, gridWidth):
	grid = []
	rows = []
	tileWidth = gridWidth // numRows # integer division, gap is for visualization
	
	for i in range(numRows): # size is actually gridSize x gridSize, stops 1 before gridSize, but starts at index 0
		for j in range(numRows):
			rows.append(Node(i, j, tileWidth, numRows, UNEXPLOREDSTATE)) # '2' is the unknown value
		grid.append(rows)
		rows = []     
	return grid

# Draw lines of the grid
def draw_grid(win, rows, screenWidth):
	tileWidth = screenWidth // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * tileWidth), (screenWidth, i * tileWidth)) # draw horizontal lines skip the tileWidth for the y axis and then draw lines across the screenWidth
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * tileWidth, 0), (j * tileWidth, screenWidth)) # draw vertical lines skip the tileWidth for the y axis and then draw lines up down of screenWidth

# Draw entire grid, lines and nodes
def draw(win, grid, rows, screenWidth):
	win.fill(WHITE)
	
	for row in grid:
		for node in row:
			node.draw(win) # draws individual tiles
	draw_grid(win, rows, screenWidth)
	pygame.display.update()


'''
Occupancy Map States::
0-Obstacle
1-Empty Space
2-Unexplored
3-Ego Car Path
4-Ego Car Position
5-Start
'''

OBSTACLESTATE = 0
EMPTYSTATE = 1 # white
UNEXPLOREDSTATE = 2
EGOPATH = 3
EGOPOSE = 4
STARTSTATE = 99
ENDSTATE = 66

NUMROWS = 40 # global
SCREENWIDTH = 800

WIN = pygame.display.set_mode((SCREENWIDTH, SCREENWIDTH))
pygame.display.set_caption("Path Planning")


def main(win, width, ROWS):
	print("hello")
	midCoords = math.ceil(ROWS/2) - 1 # the middle block: ceil(NUMROWS/2) - 1 because 0th index
	grid = populate_grid(ROWS, width)
	
	endRow = 1
	endCol = 36
	grid[midCoords][midCoords].make_start()
	grid[endRow][endCol].make_end()

	start = grid[midCoords][midCoords]
	end = grid[endRow][endCol]

	xList = []
	yList = []

	temp = []
	for row in grid:
		for node in row:
			temp.append(node.state)
		temp = []

	truck = [13,28,5] # dx, dy, size, detection num 
	car = [11,15,7]
	# each detection is relative to the previous detection

	# OPENCV DISPLAY
	# net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.8)
	# camera = jetson.utils.gstCamera(1280, 720, "0")
	# cv2.destroyAllWindows()

	boundaryCreator(9, 11, 22, 0, win, grid, ROWS, width) #(diameter, x, y, cleanup, win, grid, rows, width)
	boundaryCreator(7, 3, 30, 0, win, grid, ROWS, width)
	
	numDetections = 0
	run = True
	while run:
		
		if grid[midCoords][midCoords].get_state() == OBSTACLESTATE:
			print("YOU CRASHED.")

		grid[midCoords][midCoords].make_start()
		draw(win, grid, ROWS, width)
		
        # img, width, height = camera.CaptureRGBA(zeroCopy=True)
		# detections = net.Detect(img, width, height)
		# if len(detections) > 0:
		# 	for detection in detections:
		# 		id = detection.ClassID
		# 		print("ClassID:", id, "Left:", detection.Left, "Right:", detection.Right, "Width:", detection.Width, "Height:", detection.Height)
        #         if id == 8 or id == 6 or id ==3:
        #             print("DETECTED A VEHICLE")
        #             if numDetections = 0:
        #                 boundaryCreator(truck[2], truck[0], truck[1], 0, win, grid, ROWS, width) #(diameter, x, y, cleanup, win, grid, rows, width)
        #                 numDetections += 1
        #             elif numDetections = 1:
        #                 boundaryCreator(car[2], car[0], car[1], 0, win, grid, ROWS, width) #(diameter, x, y, cleanup, win, grid, rows, width)
        #                 numDetections += 1
        #             else
        #                 print("Already detected!")
        #                 break
                    
        #             for row in grid:
		# 			    for node in row:
		# 				    node.update_neighbors(grid)
					
		# 			xList, yList = algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, xList, yList)

		 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			# if some detection - run algorithm
			if event.type == pygame.KEYDOWN:	# https://www.programcreek.com/python/example/5891/pygame.K_LEFT
				if event.key == pygame.K_UP:
					end = movement('right', end, win, grid, ROWS, width)

				if event.key == pygame.K_LEFT:
					end = movement('straight', end, win, grid, ROWS, width)

				if event.key == pygame.K_DOWN:
					end = movement('left', end, win, grid, ROWS, width)				
					
				if event.key == pygame.K_RIGHT:
					end = movement('back', end, win, grid, ROWS, width)

				for row in grid:
					for node in row:
						node.update_neighbors(grid)
				
				xList, yList = algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, xList, yList)

				# if event.key == pygame.K_c:
				# 	grid = populate_grid(ROWS, width)


				# ONLY IF ALGORITHM RUNS --> MEANING THERE WAS A NEW BOUNDARY DETECTION: RUN SPLINE SMOOTHED INTERPOLATED PATH
				x = np.array(xList)
				y = np.array(yList)

				xe, ye = end.get_pos()
				xs, ys = start.get_pos()
				dist = math.sqrt(abs(xs-xe)**2 + abs(ys-ye)**2)

				if dist < 15:
					thresh = (int)(ROWS*0.2) # too many points to try and map to the path with not much movement means choppy turns - so restrict it.
				else:
					thresh = (int)(ROWS*0.3)

				tck,u = interpolate.splprep([x,y],k=3,s=0) # returns tuple and array
				u=np.linspace(0,1,num=thresh,endpoint=True) # num is the number of entries the spline will try and map onto the graph, if you have more rows, you want more points when interpolating to make the model better fit
				out = interpolate.splev(u,tck) # 'out' is the interpolated array of new x,y positions

				localChangeList = []	# list of tuples, [0][0] is local X changes, [0][1] is local Y changes

				for i in range(len(out[0])-1):	# if out x val(rows) is decreasing: car is going right, call: movement(right) --> boundary moves left though
					xDiff = out[0][i]-out[0][i+1]
					yDiff = out[1][i]-out[1][i+1]
					mag = math.sqrt(xDiff**2 + yDiff**2)
					angle = (int)((math.atan2(yDiff,xDiff) * 180 / math.pi)+360) % 360 	# get angle between 0-360 instead of (-pi to pi)
					tempx = round(xDiff)	# if negative, rows would be increasing --> car is going left --> call movement(left)
					tempy = round(yDiff)	# if negative, cols would be increasing --> car is going back --> call movement(back)
					localChangeList.append((tempx,tempy,mag,angle))

				for i in range(len(out[0])):
					print("X:ROW:", out[0][i], "Y:COL:", out[1][i])
					if i < len(out[0])-1:
						print("X", localChangeList[i][0], "Y", localChangeList[i][1], "MAG", localChangeList[i][2], "ANGLE", localChangeList[i][3])

				# visualize and clear lists containing path for next iteration
				plt.figure()
				plt.plot(x, y, 'ro', out[0], out[1], 'b')
				plt.legend(['Points', 'Interpolated B-spline', 'True'],loc='best')
				plt.axis([min(x)-1, max(x)+1, min(y)-1, max(y)+1])
				plt.title('B-Spline Interpolation')
				xList = []
				yList = []
				plt.show(block=False)
				plt.pause(15)
				plt.close()

				

				# Goal: movement() needs to align with spline path. (DONE)
				# (int)spline[0][x] - spline[1][x] = how much movement() should occur, 
				# same time: (int)spline[0][y] - spline[1][y] = how much movement() should occur, 
				
				# only way you get a new xList or yList is if a new boundary is detected.

				# How the car follow the path:
				# first decide on direction of travel, then map the differential turn
				# map a differential turn, to the angle between two consecutive points, p1 = x1,y1 and p2 = x2,y2 of the spline path list
				# map the magnitude of the pytahgorean val of two consecutive spline points to the time the motors are moving at said differential

	# REMEMBER TO CLEAR LISTX AND LISTY AFTER ALGORITHM RUNS
	pygame.quit()

main(WIN, SCREENWIDTH, NUMROWS)

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



#### EXTRA STUFF: MOVING WINDOW ALGOS

# def shiftPosition(grid,row_new,col_new,midCoords):
# 	grid[midCoords][midCoords].set_state(EGOPATH) # 19x19
# 	grid[row_new][col_new].set_state(EGOPOSE) #18x19
# 	# grid[row_new][col_new].make_start()
# 	return grid

# def vertical(draw, win, grid, boolDirection, midCoords, rows, screenWidth, tileWidth): # Shfiting the grid vertically so it's always 41x41, left = 0, right = 1
# 	if(boolDirection): # move right(up on screen): pop the bottom row, insert 0 row
# 		grid = shiftPosition(grid, midCoords-1,midCoords,midCoords)
# 		# for i in range(rows):
# 		# 	grid[rows-1][i].set_state(OBSTACLESTATE)
# 		# 	grid[0][i].set_state(OBSTACLESTATE)
# 		nodeList = []
# 		for i in range(rows):
# 			for j in range(rows):
# 				# add one to every y.
# 		nodeList.append(Node(0, i, tileWidth, rows, OBSTACLESTATE))
# 		grid.insert(0, nodeList)
# 		print("Last Row Pre Pop:", grid[rows-1][0].get_color())
# 		grid.pop(rows-1) # pop bottom row. // # pop last column
# 		# print(grid[rows-1][0].get_color)
# 		print("Last Row Post Pop:" ,grid[rows-1][0].get_color())
# 		print("First Row Color:", grid[0][1].get_color())
# 		print("Second Row Color:", grid[1][1].get_color())

# 	else:
# 		shiftPosition(grid, midCoords+1,midCoords,midCoords)  # rows increase downwards, basically setting one row down to be the new mid position
# 		grid.pop(0)
# 		grid.append([Node(i, rows-1, tileWidth, rows, OBSTACLESTATE) for i in range(NUMROWS)])
# 	draw()
# 	return grid

# def horizontal(win, grid, boolDirection, midCoords, rows, screenWidth, tileWidth): # Shfiting the grid horizontally so it's always 41x41, straight = 1, backward = 0
# 	if(boolDirection):
# 		shiftPosition(grid, midCoords, midCoords-1,midCoords) # this line should be first or the grid will be shifted
# 		for index,row in enumerate(grid):
# 			row.pop(NUMROWS-1)           # popping the last column value for each row, this is 41
# 			row.insert(0, Node(0, index, tileWidth, rows, UNEXPLOREDSTATE)) # x location always 0, y location is index as it moves down the rows
# 	else:
# 		shiftPosition(grid, midCoords,midCoords+1,midCoords)
# 		for index2,row in enumerate(grid):
# 			row.pop(0) # pop the 1st columns for every row
# 			row.append(Node(rows-1, index2, tileWidth, rows, UNEXPLOREDSTATE)) # numrows = numcols
# 		draw(win,grid,rows,screenWidth)
# 		return

# everytime the car goes any direction, the boundary center moves the opposite direection and re-expands size.
# this way the car stays in the middle, the map row/col is always the same and the boundaries just move into different row/cols setting state.

# new start point at newPose each iteration (then run A* each time new start position)
# end position moves just as barriers move, COULD JUST PERFORM A -1 OR +1 TRANSFORMATION ON THE ROW/COL OF THE WHOLE MAP/ALL NODES BUT FOR EFFICIENCY find boundary centres and end pos.
# move boundary centre down or any direction and then blow it up again for size.
#  boundaries are coming at you every movement, thus A* runs again
# need some catch if obstacles go out of bounds
# just set_state of a new node to obstacle if that's what needs to be done
# A* runs each time moved a tile or two tiles.	