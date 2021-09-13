import cv2 as cv
import numpy as np

widthImg = 500
heightImg = 500


img = cv.imread('Images/sudoku1.jpg')
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

def getCells(img):
  cells = np.array([])
  nbCells = 81 ;#9x9 = 81
  contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
  #contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
  for cnt in contours:
    area = cv.contourArea(cnt)
    if area < 250:
      print(area)
      #print(cnt)
      cv.drawContours(imgWarpedCells, cnt, -1, (255,0,0), 1)
      #print(hierarchy)
    #TODO
    #If contour is found in another contour, a number is present in the cell. 
    # For this cell store the cell index and find the value of the number in the cell.

    #cv.imshow('cnt',imgWarpedCells)
    # area = cv.contourArea(cnt)
    # if area > 50:
    #   cv.drawContours(imgWarpedCells, cnt, -1, (255,0,0), 3)
    #   peri = cv.arcLength(cnt, True) ;#True: we expect all our shapes to be closed
    #   approx = cv.approxPolyDP(cnt, 0.02*peri, True)
    #   print(peri)
    #   print(approx)
  return cells

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

imgWarpedCells = imgWarped.copy()
imgWarpedCellsProcessed = preProcessing(imgWarpedCells, False)


cells = getCells(imgWarpedCellsProcessed)
cv.imshow('PreProcessed', imgWarpedCellsProcessed)

cv.imshow('Cells', imgWarpedCells)



cv.waitKey(0)