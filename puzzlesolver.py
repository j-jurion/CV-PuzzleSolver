import numpy as np
import cv2 as cv

from dev import DevMessage as devmsg
from dev import DevImage as devimg

from puzzleviewer import PuzzleViewer
from puzzlescanner import PuzzleScanner
from solver.binarypuzzle.src.binarypuzzle import BinaryPuzzle

# Take picture --> TODO
image = 'images/bin10-2-clean.jpg'

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
