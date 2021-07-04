import pygame
import math
from queue import PriorityQueue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
	def __init__(self,row,col,width,total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbours = []
		self.width = width
		self.total_rows = total_rows
		self.parent = None
	def get_pos(self):
		return(self.row,self.col)

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def is_not_visited(self):
		return self.color == WHITE or self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self,win):
		pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

	def update_neighbours(self,grid):
		#down
		if self.row + 1 < self.total_rows and not grid[self.row + 1][self.col].is_barrier():
			self.neighbours.append(grid[self.row + 1][self.col])

		#up
		if self.row - 1 >= 0 and not grid[self.row - 1][self.col].is_barrier():
			self.neighbours.append(grid[self.row - 1][self.col])

		#left
		if self.col + 1 < self.total_rows and not grid[self.row][self.col + 1].is_barrier():
			self.neighbours.append(grid[self.row][self.col + 1])

		#right
		if self.col - 1 >= 0 and not grid[self.row][self.col - 1].is_barrier():
			self.neighbours.append(grid[self.row][self.col - 1])
	def other_node_for_reset(self):
		return not(self.color == ORANGE or self.color == TURQUOISE or self.color == BLACK)
	def assign_parent(self,node):
		self.parent = node
	def ret_parent(self):
		return(self.parent)
	#def __lt__(self,other):#less than
		#return False


def h(p1,p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path_astar(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def algorithm_astar(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}

	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = h(start.get_pos(),end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path_astar(came_from, end, draw)
			end.make_end()
			return True

		for neighbour in current.neighbours:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbour]:
				came_from[neighbour] = current
				g_score[neighbour] = temp_g_score
				f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())	
				if neighbour not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbour], count, neighbour))
					open_set_hash.add(neighbour)
					neighbour.make_open()


		draw()

		if current != start:
			current.make_closed()

	return(False)

def reconstruct_path(current, start, draw):
	while current != start:
		current = current.ret_parent()
		current.make_path()
		draw()


def algorithm_bfs(draw, grid, start, end):
	q = [start]

	while q != []:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = q.pop(0)

		if current == end:
			reconstruct_path(current, start, draw)
			end.make_end()
			return True

		for neighbour in current.neighbours:
			if neighbour.is_not_visited():
				neighbour.make_open()
				neighbour.assign_parent(current)
				q.append(neighbour)

		draw()

		if current != start:
			current.make_closed()

		
	return False

def algorithm_dfs(draw, grid, start, end):
	stack = [start]

	while stack != []:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = stack.pop()

		if current == end:
			reconstruct_path(current, start, draw)
			end.make_end()
			return True

		for neighbour in current.neighbours:
			if neighbour.is_not_visited():
				neighbour.make_open()
				neighbour.assign_parent(current)
				stack.append(neighbour)

		draw()

		if current != start:
			current.make_closed()

		
	return False

def make_grid(rows,width):
	grid = []
	gap = width // rows 
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
	for j in range(rows):
		pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width, text = "Pathfinding Visualiser"):
	win.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win,rows,width)
	pygame.display.set_caption(text)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col
 

def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	

	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			

			if pygame.mouse.get_pressed()[0]: #left
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]

				if not start and node != end:
					start = node
					start.make_start()

				elif not end and node != start:
					end = node
					end.make_end()

				elif node != end and node != start:
					node.make_barrier()


			elif pygame.mouse.get_pressed()[2]: #right
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]

				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None


			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a and start and end:
					for row in grid:
						for node in row:
							node.update_neighbours(grid)

					algorithm_astar(lambda: draw(win, grid, ROWS, width, text = "A-Star Algorithm"), grid, start, end)

				if event.key == pygame.K_b and start and end:
					for row in grid:
						for node in row:
							node.update_neighbours(grid)

					algorithm_bfs(lambda: draw(win, grid, ROWS, width, text = "Breadth First Search Algorithm"), grid, start, end)

				if event.key == pygame.K_d and start and end:
					for row in grid:
						for node in row:
							node.update_neighbours(grid)

					algorithm_dfs(lambda: draw(win, grid, ROWS, width, text = "Depth First Search Algorithm"), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS,width)

				if event.key == pygame.K_r:
					for row in grid:
						for node in row:
							if node.other_node_for_reset():
								node.reset()
					start.make_start()

					


	pygame.quit()


main(WIN, WIDTH)
