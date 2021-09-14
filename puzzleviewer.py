import cv2 as cv
import numpy as np


class PuzzleViewer:

  """
  Initialize puzzle viewer by creating white screen with given dimensions and fills in numbers given by optional 2D array.
  """
  def __init__(self, dim, matrix=0):
    if matrix == 0:
      self.matrix =   [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
      ]
    else:
      self.matrix = matrix
    self.img = np.zeros((dim,dim, 3), dtype='uint8')
    cv.rectangle(self.img, (0,0), (self.img.shape[0],self.img.shape[1]), (255,255,255), thickness=cv.FILLED) ;#Fill blank screen white
    self.drawGrid()
    for i in range(len(matrix)):
      for j in range(len(matrix[i])):
        self.insertNumber(matrix[j][i], i, j, True)
    self.insertNumber(9, 1, 4)


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


  """
  Inserts a number with a specified value, x- and y coordinates. 
  If the viewer is initialized the numbers are printed in black, otherwise in red.
  """
  def insertNumber(self, value, cellX, cellY, init=False):
    color = (0,0,0)
    if not init:
      assert self.matrix[cellY][cellX] == 0, f"The cell is not empty at coordinates ({cellX}, {cellY}), it's value is already {self.matrix[cellY][cellX]}."
      color = (0,0,255)
    assert value in range(10), f"The value of inserted number should be [0-9], value is {value}."
    
    if value != 0:
      x = self.img.shape[0]//9*cellX + self.img.shape[0]//32 + self.img.shape[0]//160 ;#move to cell + move a quarter of a cell to right + move a fraction more to right
      y = self.img.shape[1]//9*cellY + self.img.shape[0]//18 + self.img.shape[0]//40  ;#move to cell + move half a cell downward + move a fraction more downwards
      cv.putText(self.img, str(value), (x,y), cv.FONT_HERSHEY_SCRIPT_SIMPLEX  , 1.0, color, 2)
    




"""
Test scripts
"""
if __name__ == "__main__":
  matrix = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,9,0,0],
    [0,0,0,2,0,0,0,8,0],
    [0,0,0,0,3,0,0,0,7],
    [0,0,0,0,0,4,0,6,0],
    [0,0,0,0,0,0,5,0,0],
  ]

  viewer = PuzzleViewer(495, matrix)
  cv.imshow('puzzle', viewer.img)

  cv.waitKey(0)