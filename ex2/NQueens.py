""" =======================================================
File: NQueens.py

This file implements a simple N-Queens board ADT (not using classes, so the 
code is more accessible).  It can create a board, print a board, check for 
the presence of a queen, compute a heuristic cost based on how many pairs
of queens can attack each other, etc."""


import random


class NQueens:
    
    def __init__(self, n=8, queens=None, full=True):
        """Takes in a size and an optional list of queen locations, and makes
        an nxn board with one queen per column. If the queens are given, it
        must be a list n long, specifying the row for each queen, in order by
        column. If no queens are given, then the queen locations are
        generated randomly. The board is represented as a dictionary whose
        key values are the columns, and whose data values are the row the
        queen is in."""
        self.n = n
        self.fullPrint = full
        self.board = {}
        if queens != None:
            # queens are specified in queens list
            if len(queens) != n:
                # if not right number of columns
                raise NQueensException("Expected " + str(n) + " queens and given " + str(len(queens)))
            elif not all([0 <= x < n for x in queens]):
                # if some value is not valid row designation
                raise NQueensException("Queen given invalid row index")
            else:
                for col in range(n):
                    self.board[col] = queens[col]
        else:   # randomly place queens
            for col in range(n):
                row = random.randint(0, n-1)
                self.board[col] = row
        
        self.value = self.heuristic()


    def getSize(self):
        """Returns the size of the problem"""
        return self.n
    
    
    def getValue(self):
        """Returns the heuristic value of this state"""
        return self.value


    def setPrintMode(self, full):
        """Changes the print mode: full = True means print multiline representation.
        full = False means print one-line representation."""
        self.fullPrint = full


    def getQueenLoc(self, col):
        """Given a column, return the row of the queen in that column."""
        if 0 <= col < self.n:
            return self.board[col]
        else:
            raise NQueensException("Column index out of range: " + str(col))


    def isQueen(self, col, row):
        """Given a row and column value, this returns true if there is a
        queen at that position, and false otherwise"""
        return self.board[col] == row
    
    
    def moveQueenUp(self, col):
        """Given a column, change the queen for that column to one row
        higher. Raise an exception if the queen is in the first row already."""
        oldRow = self.board[col]
        if 0 <= col < self.n and 0 < oldRow:
            self.board[col] = oldRow - 1
            self.value = self.heuristic()
        elif (col < 0) or (col >= self.n):
            raise NQueensException("Column index out of range: " + str(col))
        else:
            raise NQueensException("Can't move queen up from first row: " + str(oldRow))
        

    def moveQueenDown(self, col):
        """Given a column, change the queen for that column to one row
        lowerer. Raise an exception if the queen is in the lasst row already."""
        oldRow = self.board[col]
        if 0 <= col < self.n and oldRow < self.n - 1:
            self.board[col] = oldRow + 1
            self.value = self.heuristic()
        elif (col < 0) or (col >= self.n):
            raise NQueensException("Column index out of range: " + str(col))
        else:
            raise NQueensException("Can't move queen down from last row: " + str(oldRow))


    def copyState(self):
        """Builds and returns a new board identical to this one."""
        queenLocs = []
        for col in range(self.n):
            queenLocs.append(self.board[col])
        return NQueens(self.n, queenLocs, self.fullPrint)
    
    
    def __eq__(self, otherState):
        """Takes in a board and checks if it equals this board (same
        locations for every queen."""
        if type(otherState) != type(self) or self.n != otherState.getSize():
            return False    
        else:
            for col in range(self.n):
                r1 = self.board[col]
                r2 = otherState.getQueenLoc(col)
                if r1 != r2:
                    return False
            return True
    
    
    def __str__(self):
        """Takes a board and produces a string representation suitable for printing.
        The self.fullPrint variable determines whether to print a compact version
        or the full grid."""
        finalStr = ""
        if self.fullPrint:
            for row in range(self.n):
                finalStr += ("----" * self.n) + "-\n"
                for col in range(self.n):
                    if self.board[col] == row:
                        finalStr += "| Q "
                    else:   
                        finalStr += "|   "
                finalStr += "|\n"
            finalStr += ("----" * self.n) + "-\n"
        else:
            for col in range(self.n):
                finalStr += str(self.board[col]) + ' '
            finalStr += "    "
            
        finalStr += "Value = " + str(self.value) + " out of " + str(self.getMaxValue())
        return finalStr
            
    
    def allNeighbors(self):
        """Generate a list containing all neighbors of this state"""
        neighbors = []
        for col in range(self.n):
            opts = self._moveOpts(col)
            for move in opts:
                newS = self.makeMove(col, move)
                neighbors.append(newS)
        return neighbors
          
    
    def randomNeighbors(self, num):
        """Generate num random neighbors of this state. Note that the 
        same neighbor could be generated more than once."""
        neighbors = []
        for i in range(num):
            newS = self.makeRandomMove()
            neighbors.append(newS)
        return neighbors
    
        
    def makeRandomMove(self):
        """Takes a board and returns a new board identical to the original,
        but with one random move, moving one queen to a new row in her
        column."""
        randCol = random.randrange(0, self.n)
        opts = self._moveOpts(randCol)
        randDir = random.choice(opts)   
        return self.makeMove(randCol, randDir)
    
     
    def _moveOpts(self, col):
        """Given a column, it generates a list of the legal movements"""
        opts = []
        oldRow = self.board[col]
        if oldRow > 0:
            opts.append('up')
        if oldRow < self.n - 1:
            opts.append('down')
        return opts
    
        
    def makeMove(self, col, moveDir):
        """Takes as board, a column value, and a direction of movement ('up'
        or 'down'), and it builds a copy of the board with the input column
        queen moved to the input row"""
        newBoard = self.copyState()
        if moveDir == 'up':
            newBoard.moveQueenUp(col)
        else:
            newBoard.moveQueenDown(col)
        return newBoard

        
    def getMaxValue(self):
        """Determines the maximum possible value for the current heuristic, given
        the size of the board."""
        return (self.n * (self.n - 1)) / 2

    def crossover(self, otherState):
        """Given another NQueens state, this computes a crossover point and creates
        two new states that have been crossed over."""
        crossPoint = random.randint(0, self.n)
        if crossPoint == 0 or crossPoint == self.n:
            new1 = self.copyState()
            new2 = otherState.copyState()
            return new1, new2
        else:
            new1List = []
            new2List = []
            for col in range(crossPoint):  # Up to crossover point, copy locs from originals
                new1List.append(self.getQueenLoc(col))
                new2List.append(otherState.getQueenLoc(col))
            for col in range(crossPoint, self.n):  # After crossover point, swap which one goes to which
                new1List.append(otherState.getQueenLoc(col))
                new2List.append(self.getQueenLoc(col))
            new1 = NQueens(self.n, new1List, self.fullPrint)
            new2 = NQueens(self.n, new2List, self.fullPrint)
            return new1, new2


    def heuristic(self):
        """With the help of the three helper functions below, this checks to see
        how many attacking pairs there are on the board. It then subtracts this
        value from the total possible to generate a value that increases as there
        are fewer attacking pairs."""
        total = 0
        size = self.n
        for col in range(size):
            row = self.board[col]
            sum1 = self._checkRow(col, row)        # check row to right of col
            sum2 = self._checkDiag(col, row, -1)   # check diagonal up and to right
            sum3 = self._checkDiag(col, row, +1)   # check diagonal down and to right
            total += sum1 + sum2 + sum3
        totalPoss = self.getMaxValue()
        return totalPoss - total

    
    def _checkRow(self, col, row):
        """Takes a column and row and checks all slots to the right of that
        position to see if there are any queens. It adds one for each queen
        it finds, and returns the total."""
        sum = 0
        for c in range(col+1, self.n):
            if self.board[c] == row:
                sum += 1
        return sum
    
    
    def _checkDiag(self, col, row, deltaR):
        """Takes in a column and row, and also either +1 or -1 and it checks
        the diagonal values. if +1 is given for deltaR then this will check
        the diagonal going down and to the right for other queens. If -1 is
        given for deltaR then this will check the diagonal going up and to
        the right for other queens. The total number found is returned."""
        sum = 0
        c = col + 1
        r = row + deltaR
        while (0 <= c < self.n) and (0 <= r < self.n):
            if self.board[c] == r:
                sum += 1
            c += 1
            r += deltaR
        return sum


class NQueensException(Exception):
    def __init__(self, explanation):
        self.explan = explanation
    def __str__(self):
        return str(self.explan)
