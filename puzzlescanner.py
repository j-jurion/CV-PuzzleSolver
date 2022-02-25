import cv2 as cv
import numpy as np
import random

from models.predictor import Predictor
from dev import DevMessage as devmsg
from dev import DevImage as devimg
import statistics as st
import math


"""
Constants
"""

#cellwidth = 55
widthImg = 500
heightImg = 500
default_var = 30

class PuzzleScanner():
  def __init__(self, filename):
    img = cv.imread(filename)
    devimg('Original', img)
    imgContour = img.copy()
    biggest = self.getContours(img, imgContour)
    assert biggest.size !=0, f"Puzzle contour not found."
    imgWarped=self.getWarp(img,biggest)
    imgWarpedGray=cv.cvtColor(imgWarped, cv.COLOR_BGR2GRAY)
    devimg("ImageWarped", imgWarped)

    edged = cv.Canny(imgWarpedGray, 10, 200)
    devimg("Edged", edged)
    contours, hierarchy = cv.findContours(edged, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    imgWarped2 = imgWarped.copy()
    self.puzzle_size = self.getPuzzleSize(contours, imgWarped2)

    self.puzzle = self.getPuzzle(imgWarped, self.puzzle_size)


  def getPuzzleSize(self, contours, img):
    x_coords = np.array([])
    y_coords = np.array([])
    for cnt in contours:
      peri = cv.arcLength(cnt, True) ;#True: we expect all our shapes to be closed
      approx = cv.approxPolyDP(cnt, 0.02*peri, True)

      if len(approx) == 4 and peri > 100:
        for i in range(3):
          if self.sameCoordinateGroup(x_coords,approx[i][0][0]) : x_coords = np.append(x_coords, approx[i][0][0])
          if self.sameCoordinateGroup(y_coords,approx[i][0][1]) : y_coords = np.append(y_coords, approx[i][0][1])
        cv.drawContours(img, cnt, -1, (0,0,255), 3)
        cv.drawContours(img, approx, -1, (255,0,0), 8)
    
    devmsg(f"X coordinates: {x_coords}")
    devmsg(f"Y coordinates: {y_coords}")
    puzzle_size = max(len(x_coords), len(y_coords))-1
    devimg('Cells', img)
    devmsg(f"Puzzle Size: {puzzle_size}")
    
    return puzzle_size

  def sameCoordinateGroup(self, coords, c):
    for i in coords:
      if abs(c-i) < default_var:
        return False
    return True



  """
  Select cells which have numbers in it, recognize the values and fill in corresponding element in puzzle array.
  """
  def getPuzzle(self, img, puzzle_size):
    puzzle = np.full((self.puzzle_size, self.puzzle_size), -1, dtype=np.int8)
    cellwidth = widthImg/puzzle_size
    border = 6
    img_draw = img.copy()

    for x in range (puzzle_size):
      for y in range (puzzle_size):
        cv.rectangle(img_draw, (round(x*cellwidth),round(y*cellwidth)), (round((x+1)*cellwidth), round((y+1)*cellwidth)), (0,255,0), 2)
        cell = img[round(x*cellwidth+border):round((x+1)*cellwidth-border), round(y*cellwidth+border):round((y+1)*cellwidth-border)]
        #devmsg(f"cell shape: {cell.shape}. Should be (28,28,3)")
        cell_processed = cell.copy()
        cell_processed = self.preProcessing(cell_processed, False)
        contours, hierarchy = cv.findContours(cell_processed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        devimg("ImageWarped_draw", img_draw)

        #Select cells which have a value
        if contours: 
          cell = cv.bitwise_not(cell)
          cell = cv.resize(cell, (28,28))
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

