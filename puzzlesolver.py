import numpy as np
import cv2 as cv
import sys

from dev import DevMessage as devmsg
from dev import DevImage as devimg

from puzzleviewer import PuzzleViewer
from puzzlescanner import PuzzleScanner
from solver.binarypuzzle.src.binarypuzzle import BinaryPuzzle

# Take picture --> TODO
if len(sys.argv) < 2:
  image = 'images/bin12.jpg'
else:
  print(sys.argv)
  image = str(sys.argv[1])

print(image)
# Upload image in puzzlescanner.py
scanner = PuzzleScanner(image)
puzzle = scanner.puzzle
devmsg(f"Puzzle: \n {puzzle}")

# Solve puzzle
solution = np.array(BinaryPuzzle(puzzle).solve()._puzzle)
devmsg(f"Solution: \n {solution}")

# Show solved puzzle
viewer = PuzzleViewer(495, puzzle, solution)
cv.imshow('Solved puzzle', viewer.img)


cv.waitKey(0)
