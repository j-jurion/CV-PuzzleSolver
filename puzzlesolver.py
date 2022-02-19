import numpy as np
import cv2 as cv

from dev import DevMessage as devmsg
from dev import DevImage as devimg

from puzzleviewer import PuzzleViewer
from puzzlescanner import PuzzleScanner
from solver.binarypuzzle.src.binarypuzzle import BinaryPuzzle

# Take picture --> TODO
image = 'images/bin1.jpg'

# Upload image in puzzlescanner.py
scanner = PuzzleScanner(image)
puzzle = scanner.puzzle
devmsg(puzzle)

# Solve puzzle
solution = np.array(BinaryPuzzle(puzzle).solve()._puzzle)
devmsg(solution)

# Show solved puzzle
viewer = PuzzleViewer(495, puzzle, solution)
cv.imshow('Solved puzzle', viewer.img)


cv.waitKey(0)
