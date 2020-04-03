import numpy as np
import sys
import math
import time

#loop through the cells to get all possible numbers in that cell
def getPossibilities(grid):
    possibleNs = []
    for ir in range (0,9):
        for ic in range(0,9):
            cellPoss = [0]
            for i in range(1,10):
                if grid[ir, ic] == i:
                    cellPoss[0] = i
                else:
                    if probabilityFunction(grid, ir, ic, i):
                        if cellPoss[0] == 0:
                            cellPoss = [i]
                        else:
                            cellPoss.append(i)
                
            possibleNs.append(cellPoss)
    return(possibleNs)

#mapping to get where a ns list idx is in a grid
def getMapping():
    mapping = np.asarray(list(range(0,81))).reshape(9,9)
    squaresIdx = ([[0, 1, 2], [0, 1, 2]],
                  [[0, 1, 2], [3, 4, 5]],
                  [[0, 1, 2], [6, 7, 8]],
                  [[3, 4, 5], [0, 1, 2]],
                  [[3, 4, 5], [3, 4, 5]],
                  [[3, 4, 5], [6, 7, 8]],
                  [[6, 7, 8], [0, 1, 2]],
                  [[6, 7, 8], [3, 4, 5]],
                  [[6, 7, 8], [6, 7, 8]]
                 )
    return(mapping, squaresIdx)

def intersection(lst1, lst2): 
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3 

# get idx for rows
def getIdxs(i, typeIs):
    mapping, squaresIdx = getMapping()
    if typeIs == 'row':
        idxs = list(mapping[i,:])
    if typeIs == 'col':
        idxs = list(mapping[:,i])
    if typeIs == 'square':
        idxs = []
        for ir in range(0,3):
            for ic in range(0,3):
                idxs.append(mapping[squaresIdx[i][0][ir], squaresIdx[i][1][ic]])
    return(idxs)

def checkForPairs(nsPair, idxs):
    for idx1 in range(0,8):
        lst1 = nsPair[idxs[idx1]]
        for idx2 in range(idx1+1, 9):
            lst2 = nsPair[idxs[idx2]]
            if len(lst1) == 2 and len(lst2) == 2:
                lstInt = intersection(lst1, lst2)
                if len(lstInt) == 2:
                    #we assume that there must be only 2 places where we have naked pairs
                    # having it in more would mean that the sudoku is not valid
                    return(lstInt, idxs[idx1], idxs[idx2])
    return([0], 0, 0)


def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

# what to do if I have pairs
# the below tells us where in the grid we have pairs, and what the vallues are
# we remove all those values for the same row, col and square of the pair
def replacePairs(nsPair, typeIs):
    replaceMade = False
    for i in range(0,9):
        idxs = getIdxs(i, typeIs)
        thisPair, idx1, idx2 = checkForPairs(nsPair, idxs)
        if len(thisPair) == 2:
            for ii in idxs:
                if not ii == idx1 and not ii == idx2:
                    orList = nsPair[ii].copy()
                    nsPair[ii] = remove_values_from_list(nsPair[ii], thisPair[0])
                    nsPair[ii] = remove_values_from_list(nsPair[ii], thisPair[1])
                    if not orList == nsPair[ii]:
                        replaceMade = True
    return(nsPair, replaceMade)
    
def fillGridFromPoss(grid, poss):
    line = np.ndarray.flatten(grid)
    for i in range(0, 81):
        if len(poss[i]) == 1:
            line[i] = poss[i][0]
    grid = line.reshape((9,9))
    return(grid)

# Finally, create a function to wrap everything
def solveNakedPairs(grid):
    nsPossibilities = getPossibilities(grid)
    keepLooping = True
    while keepLooping:
        nsPossibilities, replaceMadeR = replacePairs(nsPossibilities, 'row')
        nsPossibilities, replaceMadeC = replacePairs(nsPossibilities, 'col')
        nsPossibilities, replaceMadeS = replacePairs(nsPossibilities, 'square')
        if not replaceMadeR and not replaceMadeC and not replaceMadeS:
            keepLooping = False
    grid = fillGridFromPoss(grid, nsPossibilities)
    return(grid)

# lines and rows only have unique values
def lineCheck(line):
    line = [i for i in line if i > 0]
    res = len(line) == len(np.unique(line))
    return(res)

# a sub-grid (3X3) only has unique values
def checkSquare(grid):
    grid = np.ndarray.flatten(grid)
    res = lineCheck(grid)
    return(res)

# wrapper to call all the the check funcitons
def validateGrid(grid):
    if not grid.shape == (9,9):
        print('wrong shape')
        return(False)
    rows = all(np.apply_along_axis(lineCheck, 0, grid))
    cols = all(np.apply_along_axis(lineCheck, 1, grid))
    if( not rows or not cols):
        print('duplicates in rows or cols')
        return(False)
    gridCoord = [0,3,6]
    checkSquareRes = []
    for i in gridCoord:
        for ii in gridCoord:
            square = grid[i:i+3, ii:ii+3]
            checkSquareRes = np.append(checkSquareRes, checkSquare(square))
            
    
    checkSquareRes = all(checkSquareRes)
    if( not checkSquareRes):
        print('duplicates in square')
        return(False)
    
    return(True)

def getSquareID(idx):
    idx = idx + 1 #adding one to get around the fact the python starts to count from 0
    idx = math.ceil(idx/3)
    idx = (idx * 3) - 3
    return(idx)

######
# CORE SOLVER FUNCTION.
# DETERMINES IF I CAN ADD A NUMBER TO A CELL
# BASED ON ITS ROW, COL AND 3X3 SQUARE NUMBERS


def probabilityFunction(grid, rowN, colN, val):
    if not grid[rowN,colN] == 0:
        return(False)
    #val must not be already in row
    if val in grid[rowN,:]:
        return(False)
    #val must not be already in col
    if val in grid[:,colN]:
        return(False)
    squareIdRow = getSquareID(rowN)
    squareIdCol = getSquareID(colN)
    square = grid[squareIdRow: squareIdRow+3, squareIdCol:squareIdCol+3]
    line = np.ndarray.flatten(square)
    line = [i for i in line if i == val]
    if not len(line) == 0:
        return(False)
    
    return(True)

def fillSquares(grid):
    allowedValues = list(range(1,10))
    for rowN in [0,3,6]:
        for colN in [0,3,6]:
            square = grid[rowN:rowN + 3, colN:colN + 3]
            # get missing values
            line = np.ndarray.flatten(square)
            missingValues = [i for i in allowedValues if not i in line]
            if len(missingValues) == 1:
                #replace the 0 with the missing value
                line[line == 0] = missingValues
                resSquare = np.reshape(line,(-1,3))
                grid[rowN:rowN + 3, colN:colN + 3] = resSquare

    return(grid)

def countZeros(grid):
    line = np.ndarray.flatten(grid)
    line = [i for i in line if i == 0]
    n0 = len(line)
    return(n0)
    
def solveSudoku(grid, timeMax = 30):
    grid = grid.copy()
    #should also validate timeMax
    
    if not validateGrid(grid):
        return('Sudoku cannot be solved: duplicate values in rows, cols or squares')
    
    allowedValues = list(range(1,10))
    
    #set the execution timeout
    timeout = time.time() + timeMax
    while True:
        #count 0s we start with
        n0start = countZeros(grid)
        if n0start == 0:
            break
        grid = fillSquares(grid)
        n0s = countZeros(grid)
        if n0s == 0:
            break
        for rowN in list(range(0,9)):
            for colN in list(range(0,9)):
                nOK = 0
                for  val in list(range(1,10)):
                    isPossible = probabilityFunction(grid, rowN, colN, val)
                    if isPossible:   
                        nOK = nOK+1
                        okRow = rowN
                        okCol = colN
                        okVal = val
                if nOK == 1:
                    grid[okRow, okCol] = okVal
                    
        #did we solved it?
        n0end = countZeros(grid)
        if n0end == 0:
            break
        #check if we are making progress
        if n0start == n0end:
            # naked pairs
            grid = solveNakedPairs(grid)
            #did we solved it?
            n0end = countZeros(grid)
            if n0end == 0 or n0start == n0end:
                break
        
        # check if we passed the timout
        if time.time() > timeout:
            break
    
    
    #check if we solved
    n0end = countZeros(grid)
    if n0end == 0:
        return(grid, True)
    else:
        return(grid, False)
