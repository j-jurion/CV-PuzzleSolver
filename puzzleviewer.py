import cv2 as cv
import numpy as np


class PuzzleViewer:
  def __init__(self, dim):
    self.img = np.zeros((dim,dim, 3), dtype='uint8')
    cv.rectangle(self.img, (0,0), (self.img.shape[0],self.img.shape[1]), (255,255,255), thickness=cv.FILLED) ;#Fill blank screen white
    self.drawGrid()
    self.addNumber(0, 1, 1)
    self.addNumber(1, 5, 1)
    self.addNumber(2, 2, 1)
    self.addNumber(3, 3, 1)
    self.addNumber(4, 4, 1)
    self.addNumber(5, 1, 3)
    self.addNumber(6, 1, 5)
    self.addNumber(7, 1, 4)


  def drawGrid(self):
    for i in range(10):
      if i in {0, 3, 6, 9}:
        thickness = 2
      else:
        thickness = 1
      cv.line(self.img, (self.img.shape[0]//9*i,0), (self.img.shape[0]//9*i, self.img.shape[1]), (0,0,0), thickness=thickness) ;#Vertical lines
      cv.line(self.img, (0,self.img.shape[1]//9*i), (self.img.shape[0],self.img.shape[1]//9*i), (0,0,0), thickness=thickness) ;#Horizontal lines

  def addNumber(self, value, cellX, cellY):
    x = self.img.shape[0]//9*cellX + self.img.shape[0]//32
    y = self.img.shape[1]//9*cellY + self.img.shape[0]//18 + self.img.shape[0]//32
    cv.putText(self.img, str(value), (x,y), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0,0,0), 2)
    


viewer = PuzzleViewer(495)
cv.imshow('puzzle', viewer.img)

cv.waitKey(0)