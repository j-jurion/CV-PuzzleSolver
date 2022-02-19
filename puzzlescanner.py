import cv2 as cv
import numpy as np

from models.predictor import Predictor
from dev import DevMessage as devmsg
from dev import DevImage as devimg


"""
Constants
"""
puzzle_cells_width = 12 ;# equals the puzzle height

cellwidth = 55
border = 13 ;#Required! to get the right shape for predictor.py
widthImg = cellwidth*puzzle_cells_width
heightImg = cellwidth*puzzle_cells_width



class PuzzleScanner():
  def __init__(self, filename):
    img = cv.imread(filename)
    devimg('Original', img)
    imgContour = img.copy()
    biggest = self.getContours(img, imgContour)
    if biggest.size !=0:
      imgWarped=self.getWarp(img,biggest)
      devimg("ImageWarped", imgWarped)

    devimg('Contour on original', imgContour)

    self.puzzle = self.getPuzzle(imgWarped)




  """
  Select cells which have numbers in it, recognize the values and fill in corresponding element in puzzle array.
  """
  def getPuzzle(self, img):
    puzzle = np.full((puzzle_cells_width, puzzle_cells_width), -1, dtype=np.int8)

    for x in range (12):
      for y in range (12):
        cv.rectangle(img, (x*cellwidth,y*cellwidth), ((x+1)*cellwidth, (y+1)*cellwidth), (0,255,0), 2)
        cell = img[x*cellwidth+border+1:(x+1)*cellwidth-border, y*cellwidth+border+1:(y+1)*cellwidth-border]
        devmsg(f"cell shape: {cell.shape}. Should be (28,28,3)")
        cell_processed = cell.copy()
        cell_processed = self.preProcessing(cell_processed, False)
        contours, hierarchy = cv.findContours(cell_processed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        devimg('contour cells', img)

        #Select cells which have a value
        if contours: 
          cell = cv.bitwise_not(cell)
          assert cell.shape[:2] == (28,28), f"Cell shape should be (28,28), is {cell.shape[:2]}"
          prediction = Predictor(cell, 'models/model.h5').prediction
          puzzle[x][y] = prediction
    return puzzle



  """
  Processing image (blur is optional)
  """
  def preProcessing(self, img, blur=True):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    if blur:
      img = cv.GaussianBlur(img, (5,5), 1) 
    img = cv.Canny(img, 150, 255) 
    kernel = np.ones((1,1))
    img = cv.dilate(img, kernel, iterations=2)
    img = cv.erode(img, kernel, iterations=1)
  
    return img

  
  """
  Find largest contours to find puzzle area on image
  """
  def getContours(self, img, imgContour):
    img = self.preProcessing(img)
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
      area = cv.contourArea(cnt)
      if area > 5000:
        cv.drawContours(imgContour, cnt, -1, (255,0,0), 3)
        peri = cv.arcLength(cnt, True) ;#True: we expect all our shapes to be closed
        approx = cv.approxPolyDP(cnt, 0.02*peri, True)
        if area > maxArea and len(approx) == 4:
          biggest = approx
          maxArea = area
    cv.drawContours(imgContour, biggest, -1, (255,0,0), 20)
    return biggest



  """
  Re-order the corner points of the contour from smallest to largest
  """
  def reOrder(self, myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1]= myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew


  """
  Warp image in birds eye view
  """
  def getWarp(self, img, biggest):
    biggest = self.reOrder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv.warpPerspective(img, matrix, (widthImg, heightImg))
 
    imgCropped = imgOutput[0:imgOutput.shape[0],0:imgOutput.shape[1]]
    imgCropped = cv.resize(imgCropped,(widthImg,heightImg))
    return imgCropped


