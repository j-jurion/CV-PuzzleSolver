import cv2 as cv
import numpy as np
import pytesseract ;#Install tesseract.exe file (v4.1.1)

from puzzleviewer import PuzzleViewer
from sudokusolver import SudokuSolver

pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"

cellwidth = 55
border = 5
widthImg = cellwidth*9
heightImg = cellwidth*9





img = cv.imread('images/sudoku2.jpg')
cv.imshow('Sudoku', img)

imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#cv.imshow('Gray', gray)

#TODO crop to size of puzzle
#cropped = img[50:200, 200:400]


def preProcessing(img, blur):
  imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  if blur:
    imgBlur = cv.GaussianBlur(imgGray, (5,5), 1) ;#5,5
  else: 
    #imgBlur = cv.GaussianBlur(imgGray, (5,5), 1) ;#5,5
    imgBlur = imgGray
  imgCanny = cv.Canny(imgBlur, 150, 255) ;#150, 255
  kernel = np.ones((1,1)) ;#1,1
  imgDial = cv.dilate(imgCanny, kernel, iterations=2)
  imgThres = cv.erode(imgDial, kernel, iterations=1)
  
  return imgThres


"""
Find largest contours
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
Select cells which have numbers in it and fill in corresponding element in puzzle array.
"""
def initPuzzle(img):
  img_concat = np.zeros((cellwidth-2*border,cellwidth-2*border), dtype='uint8')
  coordinates = []
  for x in range (9):
    for y in range (9):
      cv.rectangle(img, (x*cellwidth,y*cellwidth), ((x+1)*cellwidth, (y+1)*cellwidth), (0,255,0), 2)
      cell = img[x*cellwidth+border:(x+1)*cellwidth-border, y*cellwidth+border:(y+1)*cellwidth-border]
      cell_processed = preProcessing(cell, False)
      contours, hierarchy = cv.findContours(cell_processed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
      #Select cells which have a value
      if contours: 
        coordinates.append([y,x])
        cell_gray = cv.cvtColor(cell, cv.COLOR_BGR2GRAY)
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen = cv.filter2D(cell_gray, -1, sharpen_kernel)
        sharpen = 255 - sharpen
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (1,1))
        dilate = cv.dilate(sharpen, kernel, iterations=1)
        result = 255 - dilate 
        img_concat = cv.hconcat([img_concat, result])   
  cv.imshow(f'result{x,y}', img_concat)
  # print(coordinates)
  values = getValues(img_concat)
  return createPuzzle(coordinates, values)

"""
Return the value of the number on the image, using trained a model.
"""
def getValues(img):
  text = pytesseract.image_to_string(img)
  # print(text)
  values = []
  for i in text:
    if is_integer(i):
      values.append(i)
  print(values)
  return values

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def createPuzzle(coordinates, values):
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
  for x, y in coordinates: 
    puzzle[y][x] = int(values.pop(0))
  return puzzle

"""
Re-order the corner points of the contour from smallest to largest
"""
def reOrder(myPoints):
  myPoints = myPoints.reshape((4,2))
  myPointsNew = np.zeros((4,1,2),np.int32)
  add = myPoints.sum(1)
  #print("add", add)
  myPointsNew[0] = myPoints[np.argmin(add)]
  myPointsNew[3] = myPoints[np.argmax(add)]
  diff = np.diff(myPoints,axis=1)
  myPointsNew[1]= myPoints[np.argmin(diff)]
  myPointsNew[2] = myPoints[np.argmax(diff)]
  #print("NewPoints",myPointsNew)
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


cv.resize(img, (widthImg, heightImg))
imgContour = img.copy()
  
imgThres = preProcessing(img, True)
#cv.imshow('SudokuThres', imgThres)

biggest = getContours(imgThres)
if biggest.size !=0:
  imgWarpedGray=getWarp(imgGray,biggest)
  imgWarped=getWarp(img,biggest)
  cv.imshow("ImageWarped", imgWarped)


#cv.imshow('Contour', imgContour)

puzzle = initPuzzle(imgWarped)
print(puzzle)
cv.imshow("ImageWarped with cells", imgWarped)
"""
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
"""
viewer = PuzzleViewer(widthImg, puzzle)
cv.imshow('Puzzle', viewer.img)

sudokusolver = SudokuSolver(puzzle)
viewer.insertMatrix(sudokusolver.solution)

cv.imshow('Solution', viewer.img)


cv.waitKey(0)