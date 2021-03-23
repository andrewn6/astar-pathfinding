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
  
  def is_barrier(self):
    return self.color == BLACK
  
  def is_start(self):
    return self.color == ORANGE 

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
    
    for neighbor in currentNode.neighbors:
      tempGScore = gScore[currentNode] + 1

      if tempGScore < gScore[neighbor]:
        refNodePath[neighbor] = currentNode
        gScore[neighbor] = tempGScore
        fScore[neighbor] = tempGScore + heu(neighbor.get_position(), end.get_position())

        if neighbor not in initQueue:
          count += 1
          pQueue.put((fScore[neighbor], count, neighbor))
          initQueue.add(neighbor)
          neighbor.make_start()

    if currentNode != end:
      currentNode.make_end()
    
    draw()
  return False

def main(win, width):
  ROWS = 50
  grid = make_grid(ROWS, width)

  start = None 
  end = None 
  
  run = True 
  started = False
  while run:
    
    ROWS = 40
    grid = make_grid(ROWS, width)

    start = None
    end = None
    running = True
    while running:
      draw(WIN, ROWS, width, grid)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return False or running == False
        
        if pygame.mouse.get_pressed()[0]:
          current_position = pygame.mouse.get_pos()
          row, col = get_clicked_pos(current_position, ROWS, width)
          currentNode = grid[row][col]

          if not start and currentNode != end:
            start = currentNode
            start.make_start()
          
          elif not end and currentNode != start:
            end = currentNode
            end.make_end()
          
          elif currentNode != start and currentNode != end:
            currentNode.make_barrier()
          

        elif pygame.mouse.get_pressed()[2]:
          current_position = pygame.mouse.get_pos()
          row, col = get_clicked_pos(current_position, ROWS, width)
          currentNode = grid[row][col]

          currentNode.reset()

          if currentNode == start:
            start = None
          
          if currentNode == end:
            end = None 
          
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE and start and end:
            for row in grid:
              for node in row:
                node.update_neighbors(grid)
            
            algorithim(lambda: (draw(WIN, ROWS, width, grid), grid, start, end)
        
        if event.pygame == pygame.K_c:
          start = None 
          end = None
          grid = make_grid(ROWS, width)
     

  pygame.quit()

main(WIN, WIDTH)
