
"""
MODULE REPRESENTS EACH NODE IN THE OCCUPANCY GRID

"""

RED = (255, 0, 0) # Explored state
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