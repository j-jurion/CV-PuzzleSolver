import cv2 as cv
import numpy as np
from keras.models import model_from_json
import tensorflow as tf


from puzzleviewer import PuzzleViewer
from sudokusolver import SudokuSolver
from models.predictor import Predictor



"""
Constants
"""
cellwidth = 55
border = 5
widthImg = cellwidth*9
heightImg = cellwidth*9





"""
Processing image (blur is optional)
"""
def preProcessing(img, blur=True):
  imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  if blur:
    imgBlur = cv.GaussianBlur(imgGray, (5,5), 1) 
  else: 
    imgBlur = imgGray
  imgCanny = cv.Canny(imgBlur, 150, 255) 
  kernel = np.ones((1,1))
  imgDial = cv.dilate(imgCanny, kernel, iterations=2)
  imgThres = cv.erode(imgDial, kernel, iterations=1)
  
  return imgThres


"""
Find largest contours to find sudoku area on image
"""
def getContours(img):
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
Select cells which have numbers in it, recognize the values and fill in corresponding element in puzzle array.
"""
def initPuzzle(img):
  for x in range (9):
    for y in range (9):
      cv.rectangle(img, (x*cellwidth,y*cellwidth), ((x+1)*cellwidth, (y+1)*cellwidth), (0,255,0), 2)
      cell = img[x*cellwidth+border:(x+1)*cellwidth-border, y*cellwidth+border:(y+1)*cellwidth-border]
      cell_processed = preProcessing(cell, False)
      contours, hierarchy = cv.findContours(cell_processed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
      cv.imshow(f'contour cells', img)

      #Select cells which have a value
      if contours: 
        cell_processed = cell_processed
        cell_gray = cv.cvtColor(cell, cv.COLOR_BGR2GRAY)
        result_gray = 255 - cell_gray
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen = cv.filter2D(cell_gray, -1, sharpen_kernel)
        sharpen = 255 - sharpen
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (2,2)) ;#2,2
        dilate = cv.dilate(sharpen, kernel, iterations=2) ;2
        
        result = 255 - dilate 
        
        cv.imshow(f'cells {x,y}', cell_processed)
        cv.imwrite('images/test.jpg', cell_processed)

        value = Predictor('images/test.jpg', 'models/model.h5')
        print(value)

  # return -1


"""
Creates 2D array with values given by the coordinates
"""
def _createPuzzle(triplets):
  puzzle = [
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
  for v, x, y in triplets: 
    puzzle[y][x] = v
  return puzzle


"""
Re-order the corner points of the contour from smallest to largest
"""
def reOrder(myPoints):
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
def getWarp(img, biggest):
  biggest = reOrder(biggest)
  pts1 = np.float32(biggest)
  pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
  matrix = cv.getPerspectiveTransform(pts1, pts2)
  imgOutput = cv.warpPerspective(img, matrix, (widthImg, heightImg))
 
  imgCropped = imgOutput[0:imgOutput.shape[0],0:imgOutput.shape[1]]
  imgCropped = cv.resize(imgCropped,(widthImg,heightImg))
  return imgCropped




img = cv.imread('images/sudoku2.jpg')
# cv.imshow('Original', img)

imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.resize(img, (widthImg, heightImg))
imgContour = img.copy()
imgThres = preProcessing(img)

biggest = getContours(imgThres)
if biggest.size !=0:
  imgWarpedGray=getWarp(imgGray,biggest)
  imgWarped=getWarp(img,biggest)
  cv.imshow("ImageWarped", imgWarped)

cv.imshow('Contour on original', imgContour)

puzzle = initPuzzle(imgWarped)
# print(puzzle)
# #cv.imshow("ImageWarped with cells", imgWarped)

# viewer = PuzzleViewer(widthImg, puzzle)
# cv.imshow('Puzzle viewer', viewer.img)

# sudokusolver = SudokuSolver(puzzle)
# if not sudokusolver.isSolvable:
#   print("ERROR: Sudoku is not solvable!")
#   #TODO Manually edit value
# else:
#   viewer.insertMatrix(sudokusolver.solution)
#   cv.imshow('Solution', viewer.img)


cv.waitKey(0)