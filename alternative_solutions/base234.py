import numpy as np
import sys
import math
import time
from itertools import combinations

############
## BASE UTILITIES
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


def remove_values_from_list(the_list, val):
    for i in val:
        the_list = [value for value in the_list if value != i]
    return(the_list)

def fillGridFromPoss(grid, poss):
    line = np.ndarray.flatten(grid)
    for i in range(0, 81):
        if len(poss[i]) == 1:
            line[i] = poss[i][0]
    grid = line.reshape((9,9))
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
    
####
# MAIN SOLVER
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
            hardSolve = True
            while hardSolve:
                nsOr = getPossibilities(grid)
                ns = getPossibilities(grid)
                ns = solveNakedPairs(ns)
                ns = solveNaked3(ns)
                ns = solveNaked4(ns)
                grid = fillGridFromPoss(grid, ns)
                ns = getPossibilities(grid)
                hardSolve = (not ns == nsOr)
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
    
#####
# PAIRS
def checkForPairs(ns, idxs):
    comb = list(combinations(idxs, 2))
    for thisComb in comb:
        lst1 = ns[thisComb[0]]
        lst2 = ns[thisComb[1]]
        if len(lst1)==2 and len(lst2)==2:
            lstInt = intersection(lst1, lst2)
            if len(lstInt) == 2:
                #we assume that there must be only 2 places where we have naked pairs
                # having it in more would mean that the sudoku is not valid
                return(lstInt, thisComb)
    return([0], [0, 0])

# what to do if I have pairs
# the below tells us where in the grid we have pairs, and what the vallues are
# we remove all those values for the same row, col and square of the pair
def replacePairs(nsPair, typeIs):
    replaceMade = False
    for i in range(0,9):
        idxs = getIdxs(i, typeIs)
        thisPair, idx = checkForPairs(nsPair, idxs)
        if len(thisPair) == 2:
            for ii in idxs:
                if not ii == idx[0] and not ii == idx[1]:
                    orList = nsPair[ii].copy()
                    nsPair[ii] = remove_values_from_list(nsPair[ii], [thisPair[0], thisPair[1]])
                    if not orList == nsPair[ii]:
                        replaceMade = True
    return(nsPair, replaceMade)

# Finally, create a function to wrap everything
def solveNakedPairs(nsPossibilities):
    keepLooping = True
    while keepLooping:
        nsPossibilities, replaceMadeR = replacePairs(nsPossibilities, 'row')
        nsPossibilities, replaceMadeC = replacePairs(nsPossibilities, 'col')
        nsPossibilities, replaceMadeS = replacePairs(nsPossibilities, 'square')
        if not replaceMadeR and not replaceMadeC and not replaceMadeS:
            keepLooping = False
    return(nsPossibilities)

##############
## TRIPLETS
def checkFor3(ns, idxs):
    comb = list(combinations(idxs, 3))
    for thisComb in comb:
        lst1 = ns[thisComb[0]]
        lst2 = ns[thisComb[1]]
        lst3 = ns[thisComb[2]]
        if len(lst1)>1 and len(lst2)>1 and len(lst3)>1:
            lstTmp = lst1 + lst2 + lst3
            lstTmp = np.array(lstTmp) 
            lstTmp = list(np.unique(lstTmp))
            if len(lstTmp) == 3:
                return(lstTmp, thisComb)
    return([0], [0, 0, 0])


def replace3(ns, typeIs):
    replaceMade = False
    for i in range(0,9):
        idxs = getIdxs(i, typeIs)
        comb = list(combinations(idxs, 3))
        thisComb, idx = checkFor3(ns, idxs)
        if len(thisComb) == 3:
            for ii in comb:
                if not ii == thisComb:
                    orList = ns.copy()
                    ns[ii[0]] = remove_values_from_list(ns[ii[0]], thisComb)
                    ns[ii[1]] = remove_values_from_list(ns[ii[1]], thisComb)
                    ns[ii[2]] = remove_values_from_list(ns[ii[2]], thisComb)
                    if not orList == ns:
                        replaceMade = True
    return(ns, replaceMade)

# Finally, create a function to wrap everything
def solveNaked3(nsPossibilities):
    keepLooping = True
    while keepLooping:
        nsPossibilities, replaceMadeR = replace3(nsPossibilities, 'row')
        nsPossibilities, replaceMadeC = replace3(nsPossibilities, 'col')
        nsPossibilities, replaceMadeS = replace3(nsPossibilities, 'square')
        if not replaceMadeR and not replaceMadeC and not replaceMadeS:
            keepLooping = False
    return(nsPossibilities)

################
## QUADS
def checkFor4(ns, idxs):
    comb = list(combinations(idxs, 4))
    for thisComb in comb:
        lst1 = ns[thisComb[0]]
        lst2 = ns[thisComb[1]]
        lst3 = ns[thisComb[2]]
        lst4 = ns[thisComb[3]]
        if len(lst1)>1 and len(lst2)>1 and len(lst3)>1 and len(lst4)>1:
            lstTmp = lst1 + lst2 + lst3 +lst4
            lstTmp = np.array(lstTmp) 
            lstTmp = list(np.unique(lstTmp))
            if len(lstTmp) == 4:
                return(lstTmp, thisComb)
    return([0], [0, 0, 0, 0])


def replace4(ns, typeIs):
    replaceMade = False
    for i in range(0,9):
        idxs = getIdxs(i, typeIs)
        comb = list(combinations(idxs, 4))
        thisComb, idx = checkFor4(ns, idxs)
        if len(thisComb) == 4:
            for ii in comb:
                if not ii == thisComb:
                    orList = ns.copy()
                    ns[ii[0]] = remove_values_from_list(ns[ii[0]], thisComb)
                    ns[ii[1]] = remove_values_from_list(ns[ii[1]], thisComb)
                    ns[ii[2]] = remove_values_from_list(ns[ii[2]], thisComb)
                    ns[ii[3]] = remove_values_from_list(ns[ii[3]], thisComb)
                    if not orList == ns:
                        replaceMade = True
    return(ns, replaceMade)

# Finally, create a function to wrap everything
def solveNaked4(nsPossibilities):
    keepLooping = True
    while keepLooping:
        nsPossibilities, replaceMadeR = replace4(nsPossibilities, 'row')
        nsPossibilities, replaceMadeC = replace4(nsPossibilities, 'col')
        nsPossibilities, replaceMadeS = replace4(nsPossibilities, 'square')
        if not replaceMadeR and not replaceMadeC and not replaceMadeS:
            keepLooping = False
    return(nsPossibilities)