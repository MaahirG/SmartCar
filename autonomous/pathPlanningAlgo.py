
"""
MODULE HANDLES PATH PLANNING ALGORITHM

"""

from autonomous import draw, make_path
STARTSTATE = 99

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
	current_set.put((0, count, start)) 	# fscore, count for tiebreaking, node
	current_set_tracker = {start}

	came_from = {} 	# dictionary, each key is a node, value is the previous node that it came from (since all the keys prior have a camefrom value, just follow the chain downwards for the whole path)
	g_score = {} 	# dictionary, each key is a node, value is score
	f_score = {} 	# dictionary, each key is a node, value is score

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

		current_node = current_set.get()[2] 	# get the node from tuple
		current_set_tracker.remove(current_node)

		if current_node == end:
			xList, yList = reconstruct_path(came_from, end, draw, xList, yList)
			end.make_end()
			return xList, yList

		for neighbor in current_node.neighbors:
			temp_g_score = g_score[current_node] + 1 	# 1 is g_score[neighbor]

			if temp_g_score < g_score[neighbor]:  		# LESS THAN INFINITY usually or if you just visited one of the neighbours that you are looking back on, it could 
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

def h(p1, p2): # p1 and p2 are return values of get_pos()
	x1, y1 = p1
	x2, y2 = p2
	diffX = abs(x1 - x2)
	diffY = abs(y1 - y2)
	# return diffX + diffY # Manhattan
	return math.sqrt(diffX**2 + diffY**2)	# Euclidean
