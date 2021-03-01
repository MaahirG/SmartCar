# MINI TESLA CODE
# BSPLINE: https://github.com/kawache/Python-B-spline-examples, https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.BSpline.html
import pygame
import math
from queue import PriorityQueue
import time
import numpy as np
import scipy.interpolate as interpolate
import matplotlib.pyplot as plt
import Jetson.GPIO as GPIO
import jetson.inference as ji
import jetson.utils
import numpy as np
import cv2
import time
import multiprocessing

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

COLORDICT = {
	0 : BLACK,
	1 : RED,
	2 : WHITE,
	3 : PURPLE,
	4 : YELLOW,
	5 : ORANGE,
	6 : TURQUOISE 	
}

OBSTACLESTATE = 0
EMPTYSTATE = 1 # white
UNEXPLOREDSTATE = 2
EGOPATH = 3
EGOPOSE = 4
STARTSTATE = 99
ENDSTATE = 66

SCREENWIDTH = 800
NUMROWS = 40
MIDCOORDS = math.ceil(NUMROWS/2) - 1

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
		
	def set_state(self, state, row, col):
		# if out of bounds (especially probable for extra radius of boundaries when moving, do nothing)
		if row > self.total_rows-1 or row < 0 or col > self.total_rows-1 or col < 0:
			return 

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

def reconstruct_path(came_from, current, draw, xList, yList):
	while current in came_from:
		p1,p2 = current.get_pos()
		xList.append(p1)
		yList.append(p2)
		current = came_from[current]
		if current.get_state() == STARTSTATE:
			continue
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

		current_node = current_set.get()[2] 		# get the node from tuple
		current_set_tracker.remove(current_node)

		if current_node == end:
			xList, yList = reconstruct_path(came_from, end, draw, xList, yList)
			end.make_end()
			return xList, yList

		for neighbor in current_node.neighbors:
			temp_g_score = g_score[current_node] + 1 # 1 is g_score[neighbor]

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

def movement(direction, endNode, win, grid, rows, width, tiles): # moving the car vertically so it's always 41x41, left = 0, right = 1
	if direction == None:
		print("NO DIRECTION in movement()")
		return endNode

	boundaryKeyList = []
	for node in BOUNDARYCENTRES.keys():
		boundaryKeyList.append(node)
	
	egoPathUpdates = []
	for row in range(rows):
		for col in range(rows):
			cur = grid[row][col]
			tempState = cur.get_state()
			if tempState == EGOPATH or tempState == EMPTYSTATE or tempState == ENDSTATE:
				if tempState == ENDSTATE:
					endRow, endCol = endNode.get_pos()
				if tempState == EGOPATH:
					egoPathUpdates.append(cur)
				grid[row][col].set_state(UNEXPLOREDSTATE, row, col)

	mid = MIDCOORDS
	
	# not iterating through dictionary because dict values change in boundaryCreator
	for node in boundaryKeyList: # list of boundary nodes with non updated coordinates
		row, col = node.get_pos()
		size = node.get_boundary_size()
		boundaryCreator(size, row, col, 1, win, grid, rows, width) # clears the boundary and resets the states of cleared nodes
		BOUNDARYCENTRES.pop(node)
		if direction == 'right': 		# if ego moves right (upscreen) boundaries go left (downscreen)
			row += tiles
		elif direction == 'straight':
			col += tiles
		elif direction == 'left': 
			row -= tiles
		elif direction == 'back':
			col -= tiles
		boundaryCreator(size, row, col, 0, win, grid, rows, width) # recreates the boundary - and adds to BoundaryCentreTracking dictionary
	
	for node in egoPathUpdates:
		row, col = node.get_pos()

		# delete the original path that would go past the start
		if abs(row - mid) <= 1 and abs(col - mid) <= 1:
			continue

		if direction == 'right': # if ego moves right (upscreen) boundaries go left (downscreen)
			row += tiles
		elif direction == 'straight':
			col += tiles
		elif direction == 'left': 
			row -= tiles
		elif direction == 'back':
			col -= tiles
		grid[row][col].make_path()
	
	if direction == 'right':
		endRow += tiles		# if the car is going right, rows need to increase (end point comes downwards visually on the map)
	elif direction == 'straight':
		endCol += tiles
	elif direction == 'left': 
		endRow -= tiles
	elif direction == 'back':
		endCol -= tiles
	endNodeUpdated = grid[endRow][endCol]
	endNodeUpdated.make_end()

	draw(win, grid, rows, width)	
	return endNodeUpdated

def boundaryCreator(diameter, x, y, cleanup, win, grid, rows, width):
	# if the middle goes out of range, don't worry about the boundary anymore ~ assumption that no boundary just from the bottom and so near the end will have an effect on the path.
	if x > rows-1 or x < 0 or y > rows-1 or y < 0:
		return
	elif cleanup:
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
		grid[x+i][y].set_state(state, x+i, y)
		if i<0:
			start2 = 0-index # index = 1: -1 start, +1 end
			end = 0+index
			indexStoringList.append(index)
			for j in range(start2,end+1): # if index is 0, none, index = 1, go up 1 down 1, index 
				grid[x+i][y+j].set_state(state, x+i, y+j)
		elif i > 0:
			startDescent = 0-indexStoringList[len(indexStoringList)-1]
			endDescent = 0 + indexStoringList[len(indexStoringList)-1]
			indexStoringList.pop()
			for k in range(startDescent,endDescent+1):
				grid[x+i][y+k].set_state(state, x+i, y+k)
		else: 
			# print("You are at the middle!")
			pass
		
		# don't need loops twice for the vertical line of the star, above covers it 
		grid[x][y+i].set_state(state, x, y+i)

	return

def h(p1, p2): # p1 and p2 are return values of get_pos()
	x1, y1 = p1
	x2, y2 = p2
	diffX = abs(x1 - x2)
	diffY = abs(y1 - y2)
	# return diffX + diffY # Manhattan
	return math.sqrt(diffX**2 + diffY**2)	# Euclidean

def map(x, in_min, in_max, out_min, out_max):
  return ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

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

def getCarAngleTov2(curAngle, desiredAngle, experimentalZeroTurnTime, pins):
	angDiff = abs(curAngle - desiredAngle)
	turnTime = map(angDiff, 0, 360, 0, experimentalZeroTurnTime)
	if (desiredAngle > curAngle):
		print("ZEROTURN LEFT FOR TIME:", turnTime)
		GPIO.output(pins["IN1"],GPIO.LOW)		# in1 is right side of car
		GPIO.output(pins["IN2"],GPIO.LOW)
		GPIO.output(pins["IN3"],GPIO.HIGH)
		GPIO.output(pins["IN4"],GPIO.LOW)
	else:
		print("ZEROTURN RIGHT FOR TIME:", turnTime)
		GPIO.output(pins["IN1"],GPIO.LOW)
		GPIO.output(pins["IN2"],GPIO.HIGH)
		GPIO.output(pins["IN3"],GPIO.LOW)
		GPIO.output(pins["IN4"],GPIO.LOW)

	time.sleep(turnTime)
	stopCar(pins)	

def moveCar(pins):
	print("Motors Forward")
	
	GPIO.output(pins["IN1"],GPIO.LOW)
	GPIO.output(pins["IN2"],GPIO.HIGH)
	GPIO.output(pins["IN3"],GPIO.HIGH)
	GPIO.output(pins["IN4"],GPIO.LOW)

def getCarAngleTo(curAngle, desiredAngle, experimentalZeroTurnTime, pins):
	angDiff = abs(curAngle - desiredAngle)
	turnTime = map(angDiff, 0, 360, 0, experimentalZeroTurnTime)
	if (desiredAngle > curAngle):
		print("ZEROTURN LEFT FOR TIME:", turnTime)
		GPIO.output(pins["IN1"],GPIO.HIGH)		# in1 is right side of car
		GPIO.output(pins["IN2"],GPIO.LOW)
		GPIO.output(pins["IN3"],GPIO.LOW)
		GPIO.output(pins["IN4"],GPIO.LOW)
	else:
		print("ZEROTURN RIGHT FOR TIME:", turnTime)
		GPIO.output(pins["IN1"],GPIO.LOW)
		GPIO.output(pins["IN2"],GPIO.LOW)
		GPIO.output(pins["IN3"],GPIO.LOW)
		GPIO.output(pins["IN4"],GPIO.HIGH)

	time.sleep(turnTime)
	stopCar(pins)	

def moveCar(pins):
	print("Motors Forward")
	
	GPIO.output(pins["IN1"],GPIO.HIGH)
	GPIO.output(pins["IN2"],GPIO.LOW)
	GPIO.output(pins["IN3"],GPIO.LOW)
	GPIO.output(pins["IN4"],GPIO.HIGH)

def stopCar(pins):
	GPIO.output(pins["IN1"],GPIO.LOW)
	GPIO.output(pins["IN2"],GPIO.LOW)
	GPIO.output(pins["IN3"],GPIO.LOW)
	GPIO.output(pins["IN4"],GPIO.LOW)

def main(width, ROWS, mpQueue):
	time.sleep(2)
	win = pygame.display.set_mode((SCREENWIDTH, SCREENWIDTH))
	pygame.display.set_caption("Path Planning")

	midCoords = MIDCOORDS # the middle block: ceil(NUMROWS/2) - 1 because 0th index
	grid = populate_grid(ROWS, width)
	
	endRow = 1
	endCol = 26

	pins = {
		"ENA" : 32, #PWM
		"IN1" : 35,
		"IN2" : 37,
		"ENB" : 33,
		"IN3" : 31,
		"IN4" : 29 #PWM
	}

	pinList = []
	GPIO.setmode(GPIO.BOARD)

	for key in pins.keys():
		pinList.append(pins[key])

	GPIO.setup(pinList, GPIO.OUT, initial=GPIO.LOW) #INIT WITH MOTORS STOPPED
	APWM = GPIO.PWM(pins["ENA"],50) # Frequency 100 cycles per second
	BPWM = GPIO.PWM(pins["ENB"],50) 
	# APWM.start(100) # Duty Cycle
	# BPWM.start(100)

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


	# v = d/t --> get a set velocity and now you can always get the time to travel any distance (t = d/v)
	# map the actual ruler distance to the first reference obstacle to the mapsize
	# 60 inches obstacle, IRL maxsize = 100 --> 
	# distance to the reference car that we'll put at some specified (20,36) boundary coordinate

	# EXAMPLE: Beginning reference car is x45, y5 inches away, we will compute x,y distance from start point 19,19 
	# to boundary hardcoded - selected by the user and will relate that to either x OR y. say 45x Inches = 

	# irlX, irlY, irlRadius, Size = input("ENTER HERE").split() # take as input, boundaries location, +-(x) +-(y) in meters, also the entire SQUARE that you are trying to fill 2meter by 2meter?
	# irlX = float(irlX)
	# irlY = float(irlY)
	# irlRadius = float(irlRadius)
	# Size = float(Size)
	
	# TEST CASES: 
	# boundaryCreator(9, 11, 22, 0, win, grid, ROWS, width) #(diameter, row, col, cleanup, win, grid, rows, width)
	# boundaryCreator(7, 3, 30, 0, win, grid, ROWS, width)


	# Keep in mind: 'RADIUS' and MEASURED FROM THE MIDCOORDS --> 0.63 up (in the 180 degree direction) from the midcoords.
	# Test case for 9,11,22
	# irlX = 0.15
	# irlY = 0.4 
	# irlRadius = 1
	# Size = 9
	# OG: zeroturntime = 7, speed = 0.6
	experimentalZeroTurnTime = 10 # experimental
	speed = 0.6 # 100% motor speed/duty cycle in meters/second
	curAngle = 180 # default for the car pointing in the forward (left, -x) direction


	# realObstacles = [(0.15, 0.4, 1, 9),(-0.45, 0.63, 1, 5), (0.55, 0.8,1,7)] # irlX, irlY, irlRadius, Size 

	realObstacles = [(0.3, 0.8, 2, 9),(-0.9, 1.26, 2, 5), (1.1, 1.6,2,7)] # irlX, irlY, irlRadius, Size, use this 

	for obstacle in realObstacles:
		realRatioX = obstacle[0]/obstacle[2] # irlX/irlRadius
		realRatioY = obstacle[1]/obstacle[2] # irlY/irlRadius --> Approximate row length of the longest sides of the actual human sized car grid.

		gridXEquivalent = abs((ROWS/2)*realRatioX) # how many tiles would equate to the location of other cars/boundaries
		gridYEquivalent = abs((ROWS/2)*realRatioY)

		# gridXEquivalent = abs((ROWS)*realRatioX) # how many tiles would equate to the location of other cars/boundaries
		# gridYEquivalent = abs((ROWS)*realRatioY)

		if obstacle[0] < 0:
			boundCol = midCoords - gridXEquivalent # columns would decrease
		elif obstacle[0] > 0: # columns increase
			boundCol = midCoords + gridXEquivalent
		
		if obstacle[1] < 0:
			boundRow = midCoords + gridYEquivalent # rows would increase
		elif obstacle[1] > 0: # rows decrease
			boundRow = midCoords - gridYEquivalent
		
		# boundaryCreator(obstacle[3], int(boundRow), int(boundCol), 0, win, grid, ROWS, width) #(diameter, x, y, cleanup, win, grid, rows, width)

	metersPerTile = abs(realObstacles[len(realObstacles)-1][0])/gridXEquivalent  # abs(irlX)/gridXEquivalent, irlX of last boundary because gridXEquivalent will be of the last boundary
	timePerMeter = 1/speed
	timePerTile = timePerMeter*metersPerTile
	print("TIME PER TILE", timePerTile)
	print("METERS PER TILE", metersPerTile)
	print("TIME PER METER", timePerMeter)

	numDetections = 0
	run = True
	loopIter = 0
	mainIter = 0
	buttonClickedToStart = False
	firstPassStartFindPath = True

	while run:
		# print("WHILE RUN ITERATION")

		if grid[midCoords][midCoords].get_state() == OBSTACLESTATE:
			print("YOU CRASHED.")

		grid[midCoords][midCoords].make_start()
		draw(win, grid, ROWS, width)
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				buttonClickedToStart = True
			if event.type == pygame.QUIT:
				run = False	

		# Get detections from perception
		if buttonClickedToStart:
			if not mpQueue.empty() or firstPassStartFindPath:
				detectionCollection = []
				while not mpQueue.empty():
					detectionCollection = mpQueue.get() # only new detections (filtered in camera process)
					print("IN MULTIPROCESSING QUEUE MEANING NOT EMPTY!")
					for detection in detectionCollection:
						boundaryCreator(detection[0], detection[1], detection[2], 0, win, grid, ROWS, width) #(diameter, x, y, cleanup, win, grid, rows, width)
					print("LOOPED DETECTIONS IN mpQueue.get()")
				

			# for event in pygame.event.get():
			# 	if event.type == pygame.QUIT:
			# 		run = False				
			# 	if event.type == pygame.KEYDOWN:	# https://www.programcreek.com/python/example/5891/pygame.K_LEFT
			# 		if event.key == pygame.K_UP:
			# 			boundaryCreator(3, 11, 15, 0, win, grid, ROWS, width) #(diameter, x, y, cleanup, win, grid, rows, width)
			# 			print("TRYING TO CREATE BOUNDARY")
			# 		if event.key == pygame.K_LEFT:
			# 			end = movement('straight', end, win, grid, ROWS, width, 1)
			# 		if event.key == pygame.K_DOWN:
			# 			end = movement('left', end, win, grid, ROWS, width, 1)				
			# 		if event.key == pygame.K_RIGHT:
			# 			end = movement('back', end, win, grid, ROWS, width, 1)

				for row in grid:
					for node in row:
						node.update_neighbors(grid)
				
				draw(win, grid, ROWS, width)

				xList = []
				yList = []
				# row, col of each node in came_from
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
					thresh = (int)(ROWS*0.15) # too many points to try and map to the path with not much movement means choppy turns - so restrict it.
				else:
					thresh = (int)(ROWS*0.25)

				tck,u = interpolate.splprep([x,y],k=3,s=0) # returns tuple and array
				u=np.linspace(0,1,num=thresh,endpoint=True) # num is the number of entries the spline will try and map onto the graph, if you have more rows, you want more points when interpolating to make the model better fit
				out = interpolate.splev(u,tck) # 'out' is the interpolated array of new row,col positions out[0] = rows, out[1] = cols
				print("INTERPOLATED ORIGINAL ARRAY SIZE: ", len(out[0]))

				localChangeList = []	# list of tuples, [0][0] is local X changes, [0][1] is local Y changes
				for i in range(len(out[0])-1):
					# out[0][0] is the last interpolated value (farthest from ego position)
					# if out x val(rows) is decreasing: car is going right, call: movement(right) --> boundary moves left though
					rowDiff = out[0][i]-out[0][i+1]	# Note, this order will allow O(N) pop() later on for the first ego position.
					colDiff = out[1][i]-out[1][i+1]	
					localChangeList.append((rowDiff, colDiff))
				
				# visualize and clear lists containing path for next iteration
				plt.figure()
				plt.plot(y, x, 'ro', out[1], out[0], 'b')
				plt.legend(['Points', 'Interpolated B-spline', 'True'],loc='best')
				plt.axis([min(y)-1, max(y)+1, max(x)+1, min(x)-1])
				plt.title('Interpolated Planned Path')
				plt.show(block=False)
				plt.pause(1)
			
				mainIter = len(out[0])-1
				loopIter+=1
				firstPassStartFindPath = False
		else:
			print("Press any button to start autonomous driving")
			continue

		# AFTER RUNNING ALGORITHM, YOU HAVE THE MOST UP TO DATE DATA ABOUT BOUNDARIES, PATH (SMOOTHED), ALL NODE STATUS		
		# IF NO NEW DETECTION OCCURS, THE WHILE RUN LOOP WILL JUMP TO HERE!
		
		# NOTE THE INCREMENTAL MOVEMENTS OF THE CAR HAPPEN IN SEPARATE WHILE LOOP ITERATIONS, THE WHILE RUN HAPPENS AFTER EVERY INCREMENTAL MOVEMENT
		# THIS MEANS IF WE HAVE A NEW DETECTION WE CAN CHANGE THE PATH ON THE FLY!
		
		iteration = len(xList)-1 # xList[iteration] would give: the closest to egopose from came_from[]


		if loopIter == 0: # algorithm hasn't run yet.
			continue
		elif len(localChangeList) == 0: # deplete localChangeList which is the spline point to point updates - may still be left overs in xList because of the shotcaller - nextAddition, so just go through the remaining 
			while iteration > 0:
				# this part is just for the visual - filling in the remaining movement() for the end points and boundaries
				nodeX, nodeY = xList[iteration], yList[iteration]
				nextNodeX, nextNodeY = xList[iteration-1], yList[iteration-1]
				
				if nextNodeX-nodeX > 0:
					dir = 'left'
				elif nextNodeX-nodeX < 0:
					dir = 'right'
				elif nextNodeY-nodeY > 0:
					dir = 'back'
				elif nextNodeY-nodeY < 0:
					dir = 'straight'
				else:
					dir = '' 
				
				end = movement(dir, end, win, grid, ROWS, width, 1)
				print("end pos:" , end.get_pos())
				xList.pop()
				yList.pop()			
				iteration -= 1

			
			xList.pop()
			yList.pop()

			print("You made it!")
			break

		# need to see how much is overlapped from xList and yList to the movement happening in spline.
		# max of rowDiff and colDiff takes precedence - shot caller
		# see how far max of ^ would take us in the xList,yList (camefrom subset) and just pop() until you get there.
		# ex. max()--> 2.392, if max was col --> look in yList, else look in xList, pop() and subtract till max is almost reached
		# if you subtract and pop one more time, will it be a greater distance from 0 than if you left it? --> if yes, leave it--> that's where end is.

		# xList[0] has the row position of start tile
		# difference between consecutive xList vals
		# goal: does shotcaller benefit from adding another xList val or does it get further awawy from 0?

		# infoTuple indexing: X,Y,MAG,ANGLE
		infoTuple = localChangeList[len(localChangeList)-1] # gives closest one to the ego vehicle
		# for efficiency, do the computations here because you might not need the whole list if algorithm runs again
		rowDiffClosestToEgo = infoTuple[0]
		colDiffClosestToEgo = infoTuple[1]

		# computed for each subset of spline that is a subpath
		distance = math.sqrt(rowDiffClosestToEgo**2 + colDiffClosestToEgo**2)
		desiredAngle = (int)((math.atan2(colDiffClosestToEgo,rowDiffClosestToEgo) * 180 / math.pi)+360) % 360 	# get angle between 0-360 instead of (-pi to pi)
		
		nextAddition = abs(xList[iteration]-xList[iteration-1]) + abs(yList[iteration]-yList[iteration-1]) # difference between the two next came_from points
		dir = ''
		shotCaller = abs(rowDiffClosestToEgo) + abs(rowDiffClosestToEgo)

		if abs(curAngle - desiredAngle) > 10:
			# only then stop motors and readjust
			print("STOP AND GET CAR TO ANGLE - BIG ANGLE CHANGE", curAngle, desiredAngle)
			stopCar(pins)
			time.sleep(0.1)

			getCarAngleTo(curAngle, desiredAngle, experimentalZeroTurnTime, pins) # map difference to a time: (curCarAngle - desiredAngle) # have experimental time for full turn
	
		# Else don't stop the motors, the trajectory is fine - this is here because one straighht line might be split into multiple splines
		curAngle = desiredAngle # update anyways to protect for incremental error

		travelTime = distance*timePerTile # tiles*time/tile
		print("TRAVELTIME", travelTime)

		moveCar(pins)
		timer = time.clock()		
		
		# shotCaller is a larger number than nextAddition, nextAdditions are smaller movements that make up shotCaller
		while shotCaller - nextAddition > 0 and iteration > 0:	# distance away from 0			

			# incase car goes over 'travelTime' inside loop.
			if (time.clock() - timer) > travelTime:
				stopCar(pins)
				print("STOPPED CAUGHT IN WHILE LOOP", (time.clock()-timer))

			# don't count this part as taking much time - just set teh motors going in desired direction and time.sleep(calcTime) after.
			shotCaller -= nextAddition
			
			nodeX, nodeY = xList[iteration], yList[iteration]
			nextNodeX, nextNodeY = xList[iteration-1], yList[iteration-1]
			
			if nextNodeX-nodeX > 0:
				dir = 'left'
			elif nextNodeX-nodeX < 0:
				dir = 'right'
			elif nextNodeY-nodeY > 0:
				dir = 'back'
			elif nextNodeY-nodeY < 0:
				dir = 'straight'
			else:
				dir = '' 
			
			# the way the algorithm is written, the came_from list will contain the immediately adjacent tile (meaning 1 tile move in 1 direction only)
			end = movement(dir, end, win, grid, ROWS, width, 1)
			print("End pos:", end.get_pos())
			xList.pop()
			yList.pop()
			
			iteration = iteration-1
			if iteration > 0:
				nextAddition = abs(xList[iteration]-xList[iteration-1]) + abs(yList[iteration]-yList[iteration-1]) #always going to be 1
			# time.sleep(0.5) # MAP TO VELOCITY OF CAR 
		
		print("Visualization Mapping Time:", time.clock()-timer)
		while (time.clock() - timer) < travelTime:
			# print("Still Moving", time.clock()-timer)
			continue
		

		print("DIST JUST TRAVELLED:", distance, "@DESIRED ANGLE", desiredAngle, "\n")
		# Do this only everytime car moves one full distance - distance is between n number of spline points and so is out[0] gets done
		mainIter -= 1
		localChangeList.pop()
		
		# finally:
			# print("CLEANUP GPIO")
			# GPIO.cleanup()

	pygame.quit()

def cameraProcess(n, mpQueue):
	net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.8)
	camera = jetson.utils.gstCamera(1280, 720, "0")
	cv2.destroyAllWindows()

	truck = [5,13,28] # size, dx, dy 
	car = [7,11,15]
	pedestrian = []
	seenDetections = { -1:[0,pedestrian], 8:[0,truck], 3:[0,car] } # person is ID 6

	while True:
		img, width, height = camera.CaptureRGBA(zeroCopy=True)
		detections = net.Detect(img, width, height)

		detectionCollection = []
		
		if len(detections) > 0:
			for detection in detections:
				id = detection.ClassID
				if id in seenDetections.keys():
					print("DETECTED A VEHICLE - RELEVANT")
					if seenDetections[id][0] == 0:
						detect = seenDetections[id][1]
						detectionCollection.append((detect[0],detect[1],detect[2])) #tuple of diamater, x, y
						seenDetections[id][0] = 1
						print("ClassID:", id , "Left:", detection.Left, "Right:", detection.Right, "Width:", detection.Width, "Height:", detection.Height)
						mpQueue.put(detectionCollection) # need to put diameter, x, y.
					else:
						print("Already tracking this detection.", id)					

		fps = net.GetNetworkFPS()

		jetson.utils.cudaDeviceSynchronize()
		# create a numpy ndarray that references the CUDA memory it won't be copied, but uses the same memory underneath
		aimg = jetson.utils.cudaToNumpy(img, width, height, 4)
		# print ("img shape {}".format (aimg.shape))
		aimg = cv2.cvtColor (aimg.astype (np.uint8), cv2.COLOR_RGBA2BGR)
		cv2.putText(aimg, "FPS: {}".format(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
		cv2.imshow("image", aimg)
		if cv2.waitKey(1)==ord('q'):
			break

mpQueue = multiprocessing.Queue() # communicate between 2 processes
camProc = multiprocessing.Process(target=cameraProcess, args=([], mpQueue))
mainProc = multiprocessing.Process(target=main, args=(SCREENWIDTH, NUMROWS, mpQueue))
mainProc.start()
time.sleep(3)
camProc.start()

"""
NEED TO FIX THE BOUNDARIES GOING OUT OF RANGE!!!! FIXED

Goal: movement() needs to align with spline path. (DONE)
(int)spline[0][x] - spline[1][x] = how much movement() should occur, 
same time: (int)spline[0][y] - spline[1][y] = how much movement() should occur, 

only way you get a new xList or yList is if a new boundary is detected.

How the car follow the path:
first decide on direction of travel, then map the differential turn
map a differential turn, to the angle between two consecutive points, p1 = x1,y1 and p2 = x2,y2 of the spline path list
map the magnitude of the pytahgorean val of two consecutive spline points to the time the motors are moving at said differential


each tile is 10cm. 
emulates other stuff moving around but really ego car is just moving around
assumption: no reving up controls - we maintain slow speed in autonomous mode so 1 tile @startup is the same as 1 tile from full speed
in a real autonomous car, the updates come from the radar and lidar, which is how the pose of obstacles or cars is updated, here were updating their pose
based on the ego cars movement closer to them.

Using MNIST data to get sign
can cover the cars with a blanket and then take it off quickly to test and show realtime mapping and trajectory planning
Replacement for ranging and tracking techniques with sensors
first detect the object, then get object dx dy w.r.t another object that is probably already on the map with a predetermined label
written on a sign: 26  23  1  2 3
dx dy referencing object 1, being object 2, size of object (changes mapped diameter)
object 1 would already be on the map and now we have object 2 to be put on the roadmap as an obstacle



### EXTRA STUFF: MOVING WINDOW ALGOS

def shiftPosition(grid,row_new,col_new,midCoords):
	grid[midCoords][midCoords].set_state(EGOPATH) # 19x19
	grid[row_new][col_new].set_state(EGOPOSE) #18x19
	# grid[row_new][col_new].make_start()
	return grid

def vertical(draw, win, grid, boolDirection, midCoords, rows, screenWidth, tileWidth): # Shfiting the grid vertically so it's always 41x41, left = 0, right = 1
	if(boolDirection): # move right(up on screen): pop the bottom row, insert 0 row
		grid = shiftPosition(grid, midCoords-1,midCoords,midCoords)
		# for i in range(rows):
		# 	grid[rows-1][i].set_state(OBSTACLESTATE)
		# 	grid[0][i].set_state(OBSTACLESTATE)
		nodeList = []
		for i in range(rows):
			for j in range(rows):
				# add one to every y.
		nodeList.append(Node(0, i, tileWidth, rows, OBSTACLESTATE))
		grid.insert(0, nodeList)
		print("Last Row Pre Pop:", grid[rows-1][0].get_color())
		grid.pop(rows-1) # pop bottom row. // # pop last column
		# print(grid[rows-1][0].get_color)
		print("Last Row Post Pop:" ,grid[rows-1][0].get_color())
		print("First Row Color:", grid[0][1].get_color())
		print("Second Row Color:", grid[1][1].get_color())

	else:
		shiftPosition(grid, midCoords+1,midCoords,midCoords)  # rows increase downwards, basically setting one row down to be the new mid position
		grid.pop(0)
		grid.append([Node(i, rows-1, tileWidth, rows, OBSTACLESTATE) for i in range(NUMROWS)])
	draw()
	return grid

def horizontal(win, grid, boolDirection, midCoords, rows, screenWidth, tileWidth): # Shfiting the grid horizontally so it's always 41x41, straight = 1, backward = 0
	if(boolDirection):
		shiftPosition(grid, midCoords, midCoords-1,midCoords) # this line should be first or the grid will be shifted
		for index,row in enumerate(grid):
			row.pop(NUMROWS-1)           # popping the last column value for each row, this is 41
			row.insert(0, Node(0, index, tileWidth, rows, UNEXPLOREDSTATE)) # x location always 0, y location is index as it moves down the rows
	else:
		shiftPosition(grid, midCoords,midCoords+1,midCoords)
		for index2,row in enumerate(grid):
			row.pop(0) # pop the 1st columns for every row
			row.append(Node(rows-1, index2, tileWidth, rows, UNEXPLOREDSTATE)) # numrows = numcols
		draw(win,grid,rows,screenWidth)
		return

everytime the car goes any direction, the boundary center moves the opposite direection and re-expands size.
this way the car stays in the middle, the map row/col is always the same and the boundaries just move into different row/cols setting state.

new start point at newPose each iteration (then run A* each time new start position)
end position moves just as barriers move, COULD JUST PERFORM A -1 OR +1 TRANSFORMATION ON THE ROW/COL OF THE WHOLE MAP/ALL NODES BUT FOR EFFICIENCY find boundary centres and end pos.
move boundary centre down or any direction and then blow it up again for size.
 boundaries are coming at you every movement, thus A* runs again
need some catch if obstacles go out of bounds
just set_state of a new node to obstacle if that's what needs to be done
A* runs each time moved a tile or two tiles.	

""" 