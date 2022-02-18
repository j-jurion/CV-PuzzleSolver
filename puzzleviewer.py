import cv2 as cv
import numpy as np


class PuzzleViewer:

  """
  Initialize puzzle viewer by creating white screen with given dimensions and fills in numbers given by optional 2D array.
  """
  def __init__(self, dim, init_matrix=0, solution_matrix=0):
    self.init_matrix = init_matrix
    self.solution_matrix = solution_matrix

    self.img = np.zeros((dim,dim, 3), dtype='uint8')
    cv.rectangle(self.img, (0,0), (self.img.shape[0],self.img.shape[1]), (255,255,255), thickness=cv.FILLED) ;#Fill blank screen white
    self.drawGrid()

    if init_matrix != 0:
      self.insertMatrix(self.init_matrix, True)
    if solution_matrix != 0:
      self.insertMatrix(self.solution_matrix, False)
     
    

  """
  Draws the sudoku grid on the image.
  """
  def drawGrid(self):
    for i in range(10):
      if i in {0, 3, 6, 9}:
        thickness = 2
      else:
        thickness = 1
      cv.line(self.img, (self.img.shape[0]//9*i,0), (self.img.shape[0]//9*i, self.img.shape[1]), (0,0,0), thickness=thickness) ;#Vertical lines
      cv.line(self.img, (0,self.img.shape[1]//9*i), (self.img.shape[0],self.img.shape[1]//9*i), (0,0,0), thickness=thickness) ;#Horizontal lines


  def insertMatrix(self, matrix, init=False):
    for i in range(len(matrix)):
      for j in range(len(matrix[i])):
        self._insertNumber(matrix[j][i], i, j, init)


  """
  Inserts a number with a specified value, x- and y coordinates. 
  If the viewer is initialized the numbers are printed in black, otherwise in red.
  """
  def _insertNumber(self, value, cellX, cellY, init=False):
    color = (0,0,0)
    if not init:
      assert self.init_matrix[cellY][cellX] == 0 or self.init_matrix[cellY][cellX] == value, f"The cell is not empty at coordinates ({cellX}, {cellY}) and its value is different from the inserted value {value}, it's value is already {self.init_matrix[cellY][cellX]}."
      color = (0,0,255)
    assert value in range(10), f"The value of inserted number should be [0-9], value is {value}."
    
    if value != 0 and ( init or value != self.init_matrix[cellY][cellX]):
      x = self.img.shape[0]//9*cellX + self.img.shape[0]//32 + self.img.shape[0]//160 ;#move to cell + move a quarter of a cell to right + move a fraction more to right
      y = self.img.shape[1]//9*cellY + self.img.shape[0]//18 + self.img.shape[0]//40  ;#move to cell + move half a cell downward + move a fraction more downwards
      cv.putText(self.img, str(value), (x,y), cv.FONT_HERSHEY_SCRIPT_SIMPLEX  , 1.0, color, 2)
    




"""
Test scripts
"""
if __name__ == "__main__":
  puzzle = [
    [0,0,0,3,0,0,0,0,0],
    [0,0,1,7,0,0,5,8,0],
    [0,6,0,0,0,2,0,0,1],
    [1,0,0,0,0,0,0,0,4],
    [7,0,0,0,0,8,0,0,0],
    [0,5,3,9,4,0,0,0,0],
    [0,0,0,0,9,0,1,0,0],
    [0,0,9,6,0,4,2,0,5],
    [6,4,7,2,0,0,0,0,0],
  ]

  solution = [
    [5, 7, 2, 3, 8, 1, 4, 6, 9], 
    [4, 3, 1, 7, 6, 9, 5, 8, 2], 
    [9, 6, 8, 4, 5, 2, 7, 3, 1], 
    [1, 8, 6, 5, 7, 3, 9, 2, 4], 
    [7, 9, 4, 1, 2, 8, 6, 5, 3], 
    [2, 5, 3, 9, 4, 6, 8, 1, 7], 
    [3, 2, 5, 8, 9, 7, 1, 4, 6], 
    [8, 1, 9, 6, 3, 4, 2, 7, 5], 
    [6, 4, 7, 2, 1, 5, 3, 9, 8]
  ]

  viewer = PuzzleViewer(495, puzzle)
  viewer.insertMatrix(solution)
  cv.imshow('bin1.JPG', viewer.img)

  cv.waitKey(0)