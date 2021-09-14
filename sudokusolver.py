
class SudokuSolver:

  def __init__(self, puzzle):
    self.puzzle = puzzle
    self.solution = self.puzzle
    self.solve()
    print(self.solution)

  def findNextCellToFill(self, i, j):
    for x in range(i,9):
      for y in range(j,9):
        if self.solution[x][y] == 0:
          return x,y
    for x in range(0,9):
      for y in range(0,9):
        if self.solution[x][y] == 0:
          return x,y
    return -1,-1

  def isValid(self, i, j, e):
    rowOk = all([e != self.solution[i][x] for x in range(9)])
    if rowOk:
      columnOk = all([e != self.solution[x][j] for x in range(9)])
      if columnOk:
        # finding the top left x,y co-ordinates of the section containing the i,j cell
        secTopX, secTopY = 3 *(i//3), 3 *(j//3) #floored quotient should be used here. 
        for x in range(secTopX, secTopX+3):
          for y in range(secTopY, secTopY+3):
            if self.solution[x][y] == e:
              return False
        return True
    return False

  def solve(self, i=0, j=0):
    i,j = self.findNextCellToFill(i, j)
    if i == -1:
      return True
    for e in range(1,10):
      if self.isValid(i,j,e):
        self.solution[i][j] = e
        if self.solve(i, j):
          return True
        # Undo the current cell for backtracking
        self.solution[i][j] = 0
    return False


"""
Test scripts
"""
if __name__ == "__main__":
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

  solver = SudokuSolver(puzzle)
  

