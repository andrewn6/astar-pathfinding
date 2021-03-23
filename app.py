import pygame
import math
import sys
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding")

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
  def __init__(self, row, col, width, total_rows):
    self.row = row 
    self.col = col 
    self.x = row * width
    self.y = col * width
    self.color = WHITE 
    self.neighbors = []
    self.width = width 
    self.total_rows = total_rows
  
  # Get position of "spot" or "node" via row/col
  def get_position(self):
    return self.row, self.col 
  
  # Check if its closed by checking if the color is red
  def is_closed(self):
    return self.color == RED
  
  def is_open(self):
    return self.color == GREEN
  
  # Check if its a barrier if the color is black
  def is_barrier(self):
    return self.color == BLACK
  
  # Check if its the start via Orange
  def is_start(self):
    return self.color == ORANGE 

  # Check if its the end via Purple color
  def is_end(self):
    return self.color == TURQUOISE
  
  def reset(self):
    self.color = WHITE 
  
  def make_start(self):
    self.color = ORANGE

  def make_closed(self):
    self.color = RED 

  def make_open(self):
    self.color = GREEN 
  
  def make_barrier(self):
    self.color ==BLACK 
  
  def make_end(self):
    self.color = TURQUOISE
  
  def make_path(self):
    self.color = PURPLE
  
  def draw(self, win):
    pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

  def update_neighbors(self, grid):
    self.neighbors = []

    if self.row < self.total_rows -1 and not grid[self.row - 1][self.col].is_barrier():
      self.neighbors.append(grid[self.row - 1][self.col])
    
    if self.row > 0 and not grid[self.row - 1][self.cols].is_barrier():
      self.neighbors.append(grid[self.row - 1][self.cols])
    
    if self.cols < self.total_rows -1 and not grid[self.row][self.cols + 1].is_barrier():
      self.neighbors.append(grid[self.row][self.cols + 1])

    if self.cols > 0 and not grid[self.row][self.cols - 1].is_barrier():
      self.neighbors.append(grid[self.row][self.cols - 1])



  def __lt__(self, other):
    return False

def heu(p1, p2):
  x1, y1 = p1 
  x2, y2 = p2
  return abs(x1 - x2 + abs(y1 - y2))

def make_grid(rows, width):
  grid = []
  gap = width // rows
  for i in range(rows):
    grid.append([])
    for j in range(rows):
      # Add new spot
      node = Node(i, j, gap, rows)
      grid[i].append(node)
  return grid

def draw_grid(win, rows, width):
  gap = width // rows
  for i in range(rows):
    pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
       pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Make it 60 frames per second so its cleannn
def draw(win, grid, rows, width):
  win.fill(WHITE)
  
  for row in grid:
    for spot in row:
      spot.draw(win)
  
  draw_grid(win, rows, width)
  pygame.display.update()

def get_clicked_pos(pos, rows, width):
  gap = width // rows 
  y, x = pos

  row = y // gap 
  col = x // gap
  return row, col

def definePath(draw, refNodePath, curNode):
  while curNode in refNodePath:
    curNode = refNodePath[curNode]
    curNode.make_path()
    draw()

# Algorithim goes on top of the queue, It is the first to get dequeued.
def algorithim(draw, grid, start, end):
  pQueue = PriorityQueue()
  count = 0

  pQueue.put((0, count, start))
  initQueue = {start}
  refNodePath = {}

  gScore = {node: float("inf") for row in grid for node in row}
  fScore = {node: float("inf") for row in grid for node in row}

  gScore[start] = 0
  fScore[start] =  heu(start.get_position(), end.get_position())

  while not pQueue.empty():
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return False
    
    currentNode = pQueue.get()[2]
    initQueue.remove(currentNode)

    if currentNode == end:
      start.make_start()
      end.make_end()
      definePath(draw, refNodePath, currentNode)
      return True
    
    # Check for current node neighbors, with manatthen distance than dequeue the algorithim
def main(win, width):
  ROWS = 50
  grid = make_grid(ROWS, width)

  start = None 
  end = None 
  
  run = True 
  started = False
  while run:
    draw(win, grid, ROWS, width)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      
      if started:
        continue
      if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        row, col = get_clicked_pos(pos, ROWS, width)
        spot = grid[row][col]
        if not start and spot != end:
          start = spot 
          start.make_start()

        elif not end and spot != start:
          end = spot 
          end.make_end()

        elif spot != end and spot != start:
          spot.make_barrier()

      elif pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        row, col = get_clicked_pos(pos, ROWS, width)
        spot = grid[row][col]
        spot.reset()
        if spot == start:
          start = None

        elif spot == end:
          end == None
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and not started:
          pass

      
  pygame.quit()

main(WIN, WIDTH)