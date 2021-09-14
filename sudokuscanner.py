import cv2 as cv
import numpy as np
import pytesseract ;#Install tesseract.exe file (v4.1.1)

from puzzleviewer import PuzzleViewer

pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"

cellwidth = 55
widthImg = cellwidth*9
heightImg = cellwidth*9

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



img = cv.imread('Images/sudoku2.jpg')
#cv.imshow('Sudoku', img)

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
  for x in range (9):
    for y in range (9):
      cv.rectangle(img, (x*cellwidth,y*cellwidth), ((x+1)*cellwidth, (y+1)*cellwidth), (0,255,0), 2)
      cell = img[x*cellwidth+5:(x+1)*cellwidth-5, y*cellwidth+5:(y+1)*cellwidth-5]
      cell = preProcessing(cell, False)
      contours, hierarchy = cv.findContours(cell, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
      file = open("recognized.txt", "w+")
      file.write("")
      file.close()
      #Select cells which have a value
      if contours:                         
        file = open("recognized.txt", "a")
        cv.imshow(f'Cell ({x,y})', cell)
        puzzle[x][y] = getValue(cell, file)


"""
Return the value of the number on the image, using trained a model.
"""
def getValue(img, file):
  text = pytesseract.image_to_string(img)
  print(text)
  file.write(text)
  file.write("\n")
  return 1


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

initPuzzle(imgWarped)
cv.imshow("ImageWarped with cells", imgWarped)


print(puzzle)

puzzleViewer = PuzzleViewer(widthImg, puzzle)
cv.imshow('Solution', puzzleViewer.img)

cv.waitKey(0)