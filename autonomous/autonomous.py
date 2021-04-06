import pygame
import math
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
from queue import PriorityQueue
from occupancyNode import Node

"""
SmartCar Code
python autonomous.py

Relevant System Functions List:
	reconstruct_path(came_from, current, draw, xList, yList)
	algorithm(draw, grid, start, end, xList, yList)
	movement(direction, endNode, win, grid, rows, width, tiles)
	boundaryCreator(diameter, x, y, cleanup, win, grid, rows, width)
	populate_grid(numRows, gridWidth)
	draw_grid(win, rows, screenWidth)
	draw(win, grid, rows, screenWidth)
	moveCar(pins)
	stopCar(pins)
	getCarAngleTo(curAngle, desiredAngle, experimentalZeroTurnTime, pins)

"""

pins = {
	"ENA" : 32, #PWM
	"IN1" : 35,
	"IN2" : 37,
	"ENB" : 33,
	"IN3" : 31,
	"IN4" : 29 #PWM
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

experimentalZeroTurnTime = 12	# experimental
speed = 0.27 					# 100% motor speed/duty cycle in meters/second
curAngle = 180 					# default for the car pointing in the forward (left, -x) direction


# Moves the car and its' surroundings within the occupancy grid
def movement(direction, endNode, win, grid, rows, width, tiles):
	if direction == None:
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
	for node in boundaryKeyList: 									# list of boundary nodes with non updated coordinates
		row, col = node.get_pos()
		size = node.get_boundary_size()
		boundaryCreator(size, row, col, 1, win, grid, rows, width) 	# clears the boundary and resets the states of cleared nodes
		BOUNDARYCENTRES.pop(node)
		if direction == 'right': row += tiles  						# if ego moves right (upscreen) boundaries go left (downscreen)
		elif direction == 'straight': col += tiles
		elif direction == 'left': row -= tiles
		elif direction == 'back': col -= tiles
		boundaryCreator(size, row, col, 0, win, grid, rows, width) 	# recreates the boundary + update BoundaryCenters
	
	for node in egoPathUpdates:
		row, col = node.get_pos()

		if abs(row - mid) <= 1 and abs(col - mid) <= 1: continue	# delete the original path that would go past the start
		
		if direction == 'right': row += tiles						# if ego moves right (upscreen) boundaries go left (downscreen)
		elif direction == 'straight': col += tiles
		elif direction == 'left': row -= tiles
		elif direction == 'back':col -= tiles
		grid[row][col].make_path()
	
	if direction == 'right': endRow += tiles						# car goes right, rows increase (end point comes downwards visually)
	elif direction == 'straight': endCol += tiles
	elif direction == 'left': endRow -= tiles
	elif direction == 'back': endCol -= tiles
	endNodeUpdated = grid[endRow][endCol]
	endNodeUpdated.make_end()

	draw(win, grid, rows, width)	
	return endNodeUpdated


# Build and tear down the obstacle visualizations
def boundaryCreator(diameter, x, y, cleanup, win, grid, rows, width):
	
	if x > rows-1 or x < 0 or y > rows-1 or y < 0:	# assume if the middle goes out of range, don't worry about the boundary anymore
		return
	elif cleanup:
		state = UNEXPLOREDSTATE
	else: 
		state = OBSTACLESTATE
		grid[x][y].set_boundary_size(diameter)
		if grid[x][y] not in BOUNDARYCENTRES:
			BOUNDARYCENTRES[grid[x][y]] = 1 		# boundary centre node

	half = math.floor(diameter/2)  					# 5/2 = 2 --> -2,-1,0,1,2
	start = 0 - half
	if diameter%2==0:
		print("Use an odd number for diameter for uniformity.")
		return

	indexStoringList = []
	for index,i in enumerate(range(start,half+1)):
		grid[x+i][y].set_state(state, x+i, y)
		if i<0:
			start2 = 0-index 						# index = 1: -1 start, +1 end
			end = 0+index
			indexStoringList.append(index)
			for j in range(start2,end+1):			# if index is 0, none, index = 1, go up 1 down 1, index 
				grid[x+i][y+j].set_state(state, x+i, y+j)
		elif i>0:
			startDescent = 0-indexStoringList[len(indexStoringList)-1]
			endDescent = 0 + indexStoringList[len(indexStoringList)-1]
			indexStoringList.pop()
			for k in range(startDescent,endDescent+1):
				grid[x+i][y+k].set_state(state, x+i, y+k)
		else: pass

		grid[x][y+i].set_state(state, x, y+i)
	return


# Fill up occupancy grid with node states
def populate_grid(numRows, gridWidth):
	grid = []
	rows = []
	tileWidth = gridWidth // numRows 	# integer division, gap is for visualization
	
	for i in range(numRows): 			# size is actually gridSize x gridSize, stops 1 before gridSize, but starts at index 0
		for j in range(numRows):
			rows.append(Node(i, j, tileWidth, numRows, UNEXPLOREDSTATE))
		grid.append(rows)
		rows = []     
	return grid


# Draw lines of the grid
def draw_grid(win, rows, screenWidth):
	tileWidth = screenWidth // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * tileWidth), (screenWidth, i * tileWidth)) 		# draw horizontal lines skip the tileWidth for the y axis and then draw lines across the screenWidth
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * tileWidth, 0), (j * tileWidth, screenWidth)) 	# draw vertical lines skip the tileWidth for the y axis and then draw lines up down of screenWidth


# Draw entire grid, lines and nodes
def draw(win, grid, rows, screenWidth):
	win.fill(WHITE)	
	for row in grid:
		for node in row:
			node.draw(win)
	draw_grid(win, rows, screenWidth)
	pygame.display.update()


# Bulk of the functionality of the AV
def autonomousDriving(width, ROWS, mpQueue):
	win = pygame.display.set_mode((SCREENWIDTH, SCREENWIDTH))
	pygame.display.set_caption("Path Planning")

	midCoords = MIDCOORDS
	grid = populate_grid(ROWS, width)
	

	# GPIO Setup
	pinList = []
	GPIO.setmode(GPIO.BOARD)
	for key in pins.keys():
		pinList.append(pins[key])
	GPIO.setup(pinList, GPIO.OUT, initial=GPIO.LOW) # Init with motors stopped
	APWM = GPIO.PWM(pins["ENA"], 50) 				# Frequency 50 cycles per second
	BPWM = GPIO.PWM(pins["ENB"], 50) 
	APWM.start(100) 								# Duty Cycle
	BPWM.start(100)
	

	# Initial declarations
	xList, yList = [], []
	numDetections, loopIter, mainIter = 0, 0, 0
	run, buttonClickedToStart, firstPassStartFindPath = True, False, True
	experimentalZeroTurnTime = 12 	# experimental
	speed = 0.27 					# 100% motor speed/duty cycle in meters/second
	curAngle = 180 					# default for the car pointing in the forward (left, -x) direction
	timePerTile = 0.2

	# Navigation goal
	endRow, endCol = 1, 26
	grid[midCoords][midCoords].make_start()
	grid[endRow][endCol].make_end()

	start = grid[midCoords][midCoords]
	end = grid[endRow][endCol]


	# Main functionality loop - car is now driving
	while run:
		if grid[midCoords][midCoords].get_state() == OBSTACLESTATE:
			print("You crashed.")

		grid[midCoords][midCoords].make_start()
		draw(win, grid, ROWS, width)
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN: buttonClickedToStart = True
			if event.type == pygame.QUIT: run = False	

		# Get detections from perception // interprocess communication 
		if buttonClickedToStart:
			if not mpQueue.empty() or firstPassStartFindPath:
				stopCar(pins)
				while not mpQueue.empty():
					detection = mpQueue.get() # new detections only (filtered in camera process)
					print("In multiprocessing queue --> not empty!")
					timePerTile = detection[3]
					boundaryCreator(detection[0], detection[1], detection[2], 0, win, grid, ROWS, width) # diameter, x, y, cleanup, win, grid, rows, width
					
				for row in grid:
					for node in row:
						node.update_neighbors(grid)
				
				draw(win, grid, ROWS, width)

				xList, yList = [], []
				xList, yList = algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, xList, yList)  # row, col of each node in came_from		


				# Spline generation
				x, y = np.array(xList), np.array(yList)
				xe, ye = end.get_pos()
				xs, ys = start.get_pos()
				dist = math.sqrt(abs(xs-xe)**2 + abs(ys-ye)**2)

				if dist < 15: thresh = (int)(ROWS*0.15) 	# too many points to try and map to the path with not much movement means choppy turns - so restrict it.
				else: thresh = (int)(ROWS*0.25)

				tck,u = interpolate.splprep([x,y],k=2,s=0) 	# returns tuple and array
				u=np.linspace(0,1,num=thresh,endpoint=True) # num is the number of entries the spline will try and map onto the graph, if you have more rows, you want more points when interpolating to make the model better fit
				out = interpolate.splev(u,tck) 				# 'out' is the interpolated array of new row,col positions out[0] = rows, out[1] = cols
				print("Interpolated original array size: ", len(out[0]))

				localChangeList = []						# list of tuples, [0][0] is local X changes, [0][1] is local Y changes
				for i in range(len(out[0])-1):
					# out[0][0] is the last interpolated value (farthest from ego position)
					# if out x val(rows) is decreasing: car is going right, call: movement(right) --> boundary moves left though
					# Note, the order below will allow O(N) pop() later on for the first ego position.
					rowDiff, colDiff = out[0][i]-out[0][i+1], out[1][i]-out[1][i+1]	
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
		else: continue
		
		"""
			After running algorithm, you have the most up to date data about boundaries, path (smoothed), 
			all node status. If no new detection occurs, the while run loop will jump to here!
			
			The incremental movements of the car happen in separate while loop iterations, the while run
			happens after every incremental movement this means if we have a new detection we can change the path on the fly!
		
		"""
		
		iteration = len(xList)-1 		# xList[iteration] would give: the closest to egopose from came_from[]

		if loopIter == 0: 				# algorithm hasn't run yet.
			continue
		elif len(localChangeList) == 0: # deplete localChangeList which is the spline point to point updates - may still be left overs in xList because of the shotcaller - nextAddition, so just go through the remaining 
			while iteration > 0:
				# this part is just for the visual - filling in the remaining movement() for the end points and boundaries
				nodeX, nodeY = xList[iteration], yList[iteration]
				nextNodeX, nextNodeY = xList[iteration-1], yList[iteration-1]
				
				if nextNodeX-nodeX > 0:   dir = 'left'
				elif nextNodeX-nodeX < 0: dir = 'right'
				elif nextNodeY-nodeY > 0: dir = 'back'
				elif nextNodeY-nodeY < 0: dir = 'straight'
				else: dir = '' 
				
				end = movement(dir, end, win, grid, ROWS, width, 1)
				print("end pos:" , end.get_pos())
				xList.pop()
				yList.pop()			
				iteration -= 1

			xList.pop()
			yList.pop()

			print("You made it!")
			break
		
		infoTuple = localChangeList[len(localChangeList)-1] # gives closest one to the ego vehicle

		rowDiffClosestToEgo = infoTuple[0]
		colDiffClosestToEgo = infoTuple[1]

		# computed for each subset of spline that is a subpath
		distance = math.sqrt(rowDiffClosestToEgo**2 + colDiffClosestToEgo**2)
		desiredAngle = (int)((math.atan2(colDiffClosestToEgo,rowDiffClosestToEgo) * 180 / math.pi)+360) % 360 	# get angle between 0-360 instead of (-pi to pi)
		
		nextAddition = abs(xList[iteration]-xList[iteration-1]) + abs(yList[iteration]-yList[iteration-1]) 		# difference between the two next came_from points
		shotCaller = abs(rowDiffClosestToEgo) + abs(rowDiffClosestToEgo)
		dir = ''

		if abs(curAngle - desiredAngle) > 10:
			# only then stop motors and readjust
			print("Stop and get car to angle - big angle change", curAngle, desiredAngle)
			stopCar(pins)
			time.sleep(0.2)
			getCarAngleTo(curAngle, desiredAngle, experimentalZeroTurnTime, pins) # map difference to a time: (curCarAngle - desiredAngle) # have experimental time for full turn
	
		# Else don't stop the motors, the trajectory is fine
		# this is here because one straight line might be split into multiple splines
		# update anyways to protect for incremental error
		curAngle = desiredAngle

		travelTime = distance*timePerTile # tiles*time/tile
		print("TRAVELTIME", travelTime)

		moveCar(pins)
		timer = time.clock()		
		
		# shotCaller is a larger number than nextAddition, nextAdditions are smaller movements that make up shotCaller
		while shotCaller - nextAddition > 0 and iteration > 0:	# distance away from 0			

			# incase car goes over 'travelTime' inside loop.
			if (time.clock() - timer) > travelTime:
				stopCar(pins)
				print("Stopped, caught in while loop", (time.clock()-timer))

			shotCaller -= nextAddition
			
			nodeX, nodeY = xList[iteration], yList[iteration]
			nextNodeX, nextNodeY = xList[iteration-1], yList[iteration-1]
			
			if nextNodeX-nodeX > 0: dir = 'left'
			elif nextNodeX-nodeX < 0: dir = 'right'
			elif nextNodeY-nodeY > 0: dir = 'back'
			elif nextNodeY-nodeY < 0: dir = 'straight'
			else: dir = '' 
			
			# algorithm is written such that came_from list will contain the immediately adjacent tile (meaning 1 tile move in 1 direction only)
			end = movement(dir, end, win, grid, ROWS, width, 1)
			print("End pos:", end.get_pos())
			xList.pop()
			yList.pop()
			
			iteration = iteration-1
			if iteration > 0:
				nextAddition = abs(xList[iteration]-xList[iteration-1]) + abs(yList[iteration]-yList[iteration-1]) # always going to be 1
			# time.sleep(0.5) # MAP TO VELOCITY OF CAR 
		
		print("Visualization Mapping Time:", time.clock()-timer)
		while (time.clock() - timer) < travelTime:
			print("Still Moving", time.clock()-timer)
			continue

		print("DIST JUST TRAVELLED:", distance, "@DESIRED ANGLE", desiredAngle, "\n")
		# Do this only everytime car moves one full distance - distance is between n number of spline points and so is out[0] gets done
		mainIter -= 1
		localChangeList.pop()

	pygame.quit()


# Handles obstacle detection and realtime camera feed
def cameraProcess(n, ROWS, mpQueue):
	experimentalZeroTurnTime = 12 	# experimental
	speed = 0.27 					# 100% motor speed/duty cycle in meters/second
	curAngle = 180 					# default for the car pointing in the forward (left, -x) direction

	net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.8)
	camera = jetson.utils.gstCamera(1280, 720, "0")
	cv2.destroyAllWindows()

	truck = [0.4, 0.6, 1, 1.5, 5] 	# irlX, irlY, irlRadiusX, irlRadiusY, Size, use this 
	car = [0.7, 1.2, 1, 1.5, 7]
	pedestrian = []
	
	# Compressed version of finding timePerTile for new dimensions. # 
	xEquivalent = abs((ROWS/2)*(truck[1]/truck[3]))	# how many tiles would equate to the location of other cars/boundaries
	metersPerTile = abs(truck[0]/xEquivalent)  		# abs(irlX)/gridXEquivalent, irlX of last boundary because gridXEquivalent will be of the last boundary
	timePerMeter = 1/speed
	timePerTile = timePerMeter*metersPerTile
	print("TIME PER TILE", timePerTile)
	
	seenDetections = { -1:[0,pedestrian], 8:[0,truck], 3:[0,car] } # person is ID 6

	while True:
		img, width, height = camera.CaptureRGBA(zeroCopy=True)
		detections = net.Detect(img, width, height)

		detectionCollection = []
		
		if len(detections) > 0:
			for detection in detections:
				id = detection.ClassID
				if id in seenDetections.keys():
					if seenDetections[id][0] == 0:
						print("Detected a relevated vehicle ")

						obstacle = seenDetections[id][1]

						realRatioX = obstacle[0]/obstacle[2] 		# irlX/irlRadiusX
						realRatioY = obstacle[1]/obstacle[3] 		# irlY/irlRadiusY --> Approximate row length of the longest sides of the actual human sized car grid.

						gridXEquivalent = abs((ROWS/2)*realRatioX) 	# how many tiles would equate to the location of other cars/boundaries
						gridYEquivalent = abs((ROWS/2)*realRatioY)

						midCoords = ROWS//2
						print(midCoords)

						if obstacle[0] < 0:
							boundCol = midCoords - gridXEquivalent 	# columns would decrease
						elif obstacle[0] > 0: 						# columns increase
							boundCol = midCoords + gridXEquivalent
						
						if obstacle[1] < 0:
							boundRow = midCoords + gridYEquivalent 	# rows would increase
						elif obstacle[1] > 0: 						# rows decrease
							boundRow = midCoords - gridYEquivalent
						
						detectionCollection = (obstacle[4], int(boundRow), int(boundCol), timePerTile)
						mpQueue.put(detectionCollection) 			# need to put diameter, x, y.

						seenDetections[id][0] = 1
						print("ClassID:", id , "Left:", detection.Left, "Right:", detection.Right, "Width:", detection.Width, "Height:", detection.Height)
					else:
						pass

		fps = net.GetNetworkFPS()

		jetson.utils.cudaDeviceSynchronize()
		aimg = jetson.utils.cudaToNumpy(img, width, height, 4) # np.ndarray that references the CUDA memory it won't be copied, but uses same memory underneath
		aimg = cv2.cvtColor (aimg.astype (np.uint8), cv2.COLOR_RGBA2BGR)
		cv2.putText(aimg, "FPS: {}".format(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
		cv2.imshow("image", aimg)
		if cv2.waitKey(1)==ord('q'):
			break


### MAIN ###
mpQueue = multiprocessing.Queue() 	# communicate between 2 processes via Queue data structure
camProc = multiprocessing.Process(target=cameraProcess, args=([], NUMROWS, mpQueue))
mainProc = multiprocessing.Process(target=autonomousDriving, args=(SCREENWIDTH, NUMROWS, mpQueue))
mainProc.start()
time.sleep(3)
camProc.start()