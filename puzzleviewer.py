import cv2 as cv
import numpy as np

puzzle_cells_width = 12

class PuzzleViewer:

  """
  Initialize puzzle viewer by creating white screen with given dimensions and fills in numbers given by optional 2D array.
  """
  def __init__(self, dim, init_matrix, solution_matrix):
    self.init_matrix = init_matrix
    self.solution_matrix = solution_matrix
 
    self.img = np.zeros(shape=(dim,dim))
    cv.rectangle(self.img, (0,0), (self.img.shape[0],self.img.shape[1]), (255,255,255), thickness=cv.FILLED) ;#Fill blank screen white
    self.drawGrid()

    self.insertMatrix(self.init_matrix, True)
    self.insertMatrix(self.solution_matrix, False)
     
    

  """
  Draws the puzzle grid on the image.
  """
  def drawGrid(self):
    for i in range(puzzle_cells_width+1):
      cv.line(self.img, (self.img.shape[0]//puzzle_cells_width*i+1,0), (self.img.shape[0]//puzzle_cells_width*i+1, self.img.shape[1]), (0,0,0), thickness=2) ;#Vertical lines
      cv.line(self.img, (0,self.img.shape[1]//puzzle_cells_width*i+1), (self.img.shape[0],self.img.shape[1]//puzzle_cells_width*i+1), (0,0,0), thickness=2) ;#Horizontal lines


  def insertMatrix(self, matrix, init=False):
    for i in range(len(matrix)):
      for j in range(len(matrix[i])):
        self._insertNumber(matrix[j][i], i, j, init)


  """
  Inserts a number with a specified value, x- and y coordinates. 
  If the viewer is initialized the numbers are printed in black, otherwise in red.
  """
  def _insertNumber(self, value, cellX, cellY, init=False):
    color = (0,255,0)
    if not init:
      #assert self.init_matrix[cellY][cellX] == None or self.init_matrix[cellY][cellX] == value, f"The cell is not empty at coordinates ({cellX}, {cellY}) and its value is different from the inserted value {value}, it's value is already {self.init_matrix[cellY][cellX]}."
      color = (0,0,255)
    #assert value in range(2) or value is None, f"The value of inserted number should be [0-1], value is {value}."
    print(f"({cellX},{cellY}) | value={value} | color is {color}, init is {init}")
    if value != None and ( init or value != self.init_matrix[cellY][cellX]):
      x = self.img.shape[0]//puzzle_cells_width*cellX + self.img.shape[0]//40  ;#move to cell + move a quarter of a cell to right + move a fraction more to right
      y = self.img.shape[1]//puzzle_cells_width*cellY + self.img.shape[0]//18 + self.img.shape[0]//80  ;#move to cell + move half a cell downward + move a fraction more downwards
      cv.putText(self.img, str(value), (x,y), cv.FONT_HERSHEY_SCRIPT_SIMPLEX  , 1, (0,0,255), 2)
    




"""
Test scripts
"""
if __name__ == "__main__":
  puzzle = np.array([
      [None, None, None, None, None, None,  1, None, None,  1, None, None],  
      [None, None, None, None, None, None,  1, None, None,  1, None, None],  
      [None, None, None, None, None, None,  1, None, None,  1, None, None],  
      [None, None, None, None, None, None,  1, None, None,  1, None, None],  
      [None, None, None, None, None, None,  1, None, None,  1, None, None],  
      [None, None, None, None, None, None,  1, None, None,  1, None, None],  
      [None, None, None, None, None, None,  1, None, None,  1, None, None],  
      [None, None, None, None, None, None,  1, None, None,  1, None, None],  
      [None, None, None, None, None, None,  1, None, None,  1, None, None],  
      [None, None, None, None, None, None,  1, None, None,  1, None, None],  
      [None, None, None, None, None, None,  1, None, None,  1, None, None],  
      [None, None, None, None, None, None,  1, None, None,  1, None, None]  
    ])

  solution = np.array([
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   
    [0, 1, 0, 1, 1, 0,  1, 0, 1,  1, 0, 1],   

  ])

  viewer = PuzzleViewer(495, puzzle, solution)
  cv.imshow('binsolved', viewer.img)

  cv.waitKey(0)