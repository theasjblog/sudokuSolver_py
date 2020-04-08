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

def negIntersection(lst1, lst2): 
    temp = set(lst2) 
    lst3 = [value for value in lst1 if not value in temp] 
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
    
def verifyNposs(ns):
    gr = np.zeros((9,9))
    gr = fillGridFromPoss(gr, ns)
    nsGr = getPossibilities(gr)
    m, s = getMapping()
    for iR in range(0,9):
        for iC  in range(0,9):
            thisNs = ns[m[iR, iC]]
            thisNsGr = nsGr[m[iR, iC]]
            if (len(thisNs) < len(thisNsGr)):
                ns[m[iR, iC]] = thisNs
            else:
                ns[m[iR, iC]] = thisNsGr
    return(ns)


# all intersections for a given 0-80 IDX
def getIntersections(idx):
    m, s = getMapping()
    rowCol = np.ndarray.tolist(np.argwhere(m == idx))
    ints = [np.ndarray.tolist(m[rowCol[0][0],:]) +  np.ndarray.tolist(m[:,rowCol[0][1]])][0]
    for i in range(0,9):
        idxS = getIdxs(i, 'square')
        if idx in idxS:
            ints = ints + idxS
    ints = np.ndarray.tolist(np.unique(np.asarray(ints)))
    return(ints)

def findIdx(lst, a):
    return [i for i, x in enumerate(lst) if x==a]

def negFindIdx(lst, a):
    return [i for i, x in enumerate(lst) if not x==a]

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
            ns = getPossibilities(grid)
            while hardSolve:
                nsOr = ns.copy()
                ns = solveNakedPairs(ns)
                #ns = verifyNposs(ns)

                ns = solveNaked3(ns)
                #ns = verifyNposs(ns)
                
                ns = solveNaked4(ns)
                #ns = verifyNposs(ns)
                
                ns = solveHiddenPairs(ns)
                #ns = verifyNposs(ns)
                
                ns = solveHidden3(ns)
                #ns = verifyNposs(ns)
                
                ns = solveHidden4(ns)
                #ns = verifyNposs(ns)
                
                ns = solveXwings(ns)
                #ns = verifyNposs(ns)
                
                ns = solevXYwing(ns)
                #ns = verifyNposs(ns)

                grid1 = fillGridFromPoss(grid, ns)
                if not np.array_equal(grid, grid1):
                    ns = getPossibilities(grid1)
                    grid = grid1.copy()
                    
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
# NAKED PAIRS
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
                return(lstInt, [thisComb[0], thisComb[1]])
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
                if not ii in idx:
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
## NAKED TRIPLETS
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
            for ii in idxs:
                if not ii in idx:
                    orList = ns.copy()
                    ns[ii] = remove_values_from_list(ns[ii], thisComb)
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
## NAKED QUADS
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
            for ii in idxs:
                if not ii in idx:
                    orList = ns.copy()
                    ns[ii] = remove_values_from_list(ns[ii], thisComb)
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

#####
# HIDDEN PAIRS
def checkForHiddenPairs(ns, idxs):
    # find all numbers that appear only twice
    numLst = []
    for i in range(1,10):
        appearCount = 0
        for thisIdx in idxs:
            if i in ns[thisIdx]:
                appearCount = appearCount + 1
        if appearCount == 2:
            numLst.append(i)
            
    if not len(numLst)>=2:
        return([0], [0, 0])
        
    combNum = list(combinations(numLst, 2))
    combIdx = list(combinations(idxs, 2))
    for thisComb in combNum:
        matches = 0
        for thisIdx in combIdx:
            lst1 = ns[thisIdx[0]]
            lst2 = ns[thisIdx[1]]
            if len(lst1)>=2 and len(lst2)>=1:
                lstInt = intersection(lst1, lst2)
                if len(lstInt)>=2:
                    lstInt = intersection(lstInt, thisComb)
                    if lstInt == [thisComb[0], thisComb[1]]:
                        matches = matches + 1
        if matches == 1:
            # get where the couple is
            # can just look for where the first num is
            resIdx = []
            for thisIdx in idxs:
                if thisComb[0] in ns[thisIdx]:
                    resIdx.append(thisIdx)
            return([thisComb[0], thisComb[1]], resIdx)
    return([0], [0, 0]) 
    
# what to do if I have pairs
# the below tells us where in the grid we have pairs, and what the vallues are
# we remove all those values for the same row, col and square of the pair
def replaceHiddenPairs(nsPair, typeIs):
    replaceMade = False
    for i in range(0,9):
        idxs = getIdxs(i, typeIs)
        thisPair, idx = checkForHiddenPairs(nsPair, idxs)
        if len(thisPair) == 2:
            orList = nsPair
            nsPair[idx[0]] =  thisPair
            nsPair[idx[1]] =  thisPair
            if not orList == nsPair:
                replaceMade = True
    return(nsPair, replaceMade)

# Finally, create a function to wrap everything
def solveHiddenPairs(nsPossibilities):
    keepLooping = True
    while keepLooping:
        nsPossibilities, replaceMadeR = replaceHiddenPairs(nsPossibilities, 'row')
        nsPossibilities, replaceMadeC = replaceHiddenPairs(nsPossibilities, 'col')
        nsPossibilities, replaceMadeS = replaceHiddenPairs(nsPossibilities, 'square')
        if not replaceMadeR and not replaceMadeC and not replaceMadeS:
            keepLooping = False
    return(nsPossibilities)

#####
# HIDDEN 3
def checkForHidden3(ns, idxs):
    # find all numbers that appear a max of 3 times
    numLst = []
    for i in range(1,10):
        appearCount = 0
        for thisIdx in idxs:
            if i in ns[thisIdx]:
                appearCount = appearCount + 1
        if appearCount > 1 and appearCount <= 3:
            numLst.append(i)
    if len(numLst)<3:
        return ([0], [0, 0, 0])
    
    combNum = list(combinations(numLst, 3))
    combIdx = list(combinations(idxs, 3))
    for thisComb in combNum:
        for thisIdx in combIdx:
            lst1 = ns[thisIdx[0]]
            lst2 = ns[thisIdx[1]]
            lst3 = ns[thisIdx[2]]
            lstTmp = lst1 +lst2 +lst3
            #we should make sure the numbers in
            # thisComb are not anywhere else in the grid
            lstTmp = list(
                np.unique(
                np.asarray(
                    intersection(lstTmp, list(thisComb))
                )
                )
            )
            negThisIdx = negIntersection(idxs, thisIdx)
            negLstTmp = ns[negThisIdx[0]] +             ns[negThisIdx[1]] +             ns[negThisIdx[2]] +             ns[negThisIdx[3]] +             ns[negThisIdx[4]] +             ns[negThisIdx[5]]
            negLstTmp = list(
                np.unique(
                np.asarray(
                    intersection(negLstTmp, list(thisComb))
                )
                )
            )
            if lstTmp == list(thisComb) and negLstTmp == []:
                return(list(thisComb), list(thisIdx))
    return([0], [0, 0, 0])

def replaceHidden3(ns, typeIs):
    replaceMade = False
    for i in range(0,9):
        idxs = getIdxs(i, typeIs)
        comb = list(combinations(idxs, 3))
        thisComb, idx = checkForHidden3(ns, idxs)
        if len(thisComb) == 3:
            orList = ns.copy()
            ns[idx[0]] = intersection(ns[idx[0]], list(thisComb))
            ns[idx[1]] = intersection(ns[idx[1]], list(thisComb))
            ns[idx[2]] = intersection(ns[idx[2]], list(thisComb))
            if not orList == ns:
                replaceMade = True
    return(ns, replaceMade)

# Finally, create a function to wrap everything
def solveHidden3(nsPossibilities):
    keepLooping = True
    while keepLooping:
        nsPossibilities, replaceMadeR = replaceHidden3(nsPossibilities, 'row')
        nsPossibilities, replaceMadeC = replaceHidden3(nsPossibilities, 'col')
        nsPossibilities, replaceMadeS = replaceHidden3(nsPossibilities, 'square')
        if not replaceMadeR and not replaceMadeC and not replaceMadeS:
            keepLooping = False
    return(nsPossibilities)

#####
# HIDDEN 4
def checkForHidden4(ns, idxs):
    # find all numbers that appear a max of 3 times
    numLst = []
    for i in range(1,10):
        appearCount = 0
        for thisIdx in idxs:
            if i in ns[thisIdx]:
                appearCount = appearCount + 1
        if appearCount > 1 and appearCount <= 4:
            numLst.append(i)
    if len(numLst)<4:
        return ([0], [0, 0, 0, 0])
    
    combNum = list(combinations(numLst, 4))
    combIdx = list(combinations(idxs, 4))
    for thisComb in combNum:
        for thisIdx in combIdx:
            lst1 = ns[thisIdx[0]]
            lst2 = ns[thisIdx[1]]
            lst3 = ns[thisIdx[2]]
            lst4 = ns[thisIdx[3]]
            lstTmp = lst1 +lst2 +lst3 + lst4
            #we should make sure the numbers in
            # thisComb are not anywhere else in the grid
            lstTmp = list(
                np.unique(
                np.asarray(
                    intersection(lstTmp, list(thisComb))
                )
                )
            )
            negThisIdx = negIntersection(idxs, thisIdx)
            negLstTmp = ns[negThisIdx[0]] +             ns[negThisIdx[1]] +             ns[negThisIdx[2]] +             ns[negThisIdx[3]] +             ns[negThisIdx[4]]
            negLstTmp = list(
                np.unique(
                np.asarray(
                    intersection(negLstTmp, list(thisComb))
                )
                )
            )
            if lstTmp == list(thisComb) and negLstTmp == []:
                return(list(thisComb), list(thisIdx))
    return([0], [0, 0, 0, 0])

def replaceHidden4(ns, typeIs):
    replaceMade = False
    for i in range(0,9):
        idxs = getIdxs(i, typeIs)
        comb = list(combinations(idxs, 4))
        thisComb, idx = checkForHidden4(ns, idxs)
        if len(thisComb) == 4:
            orList = ns.copy()
            ns[idx[0]] = intersection(ns[idx[0]], list(thisComb))
            ns[idx[1]] = intersection(ns[idx[1]], list(thisComb))
            ns[idx[2]] = intersection(ns[idx[2]], list(thisComb))
            ns[idx[3]] = intersection(ns[idx[3]], list(thisComb))
            if not orList == ns:
                replaceMade = True
    return(ns, replaceMade)

# Finally, create a function to wrap everything
def solveHidden4(nsPossibilities):
    keepLooping = True
    while keepLooping:
        nsPossibilities, replaceMadeR = replaceHidden4(nsPossibilities, 'row')
        nsPossibilities, replaceMadeC = replaceHidden4(nsPossibilities, 'col')
        nsPossibilities, replaceMadeS = replaceHidden4(nsPossibilities, 'square')
        if not replaceMadeR and not replaceMadeC and not replaceMadeS:
            keepLooping = False
    return(nsPossibilities)

################
# X-Wings
def checkXwingsRows(ns):
    m, s = getMapping()
    # loop through rows
    candidateRow = []            
    candidateNum = []
    candidateCol = []            
    for rowIdx in range(0,9):
        idxs = getIdxs(rowIdx, 'row')
        for thisNum in range(1,10):
            nCount = 0
            okRow = rowIdx
            okCol = []
            for colIdx in range(0,9):
                nsIdx = m[rowIdx, colIdx]
                p = ns[nsIdx]
                if thisNum in p:
                    nCount = nCount + 1
                    okCol.append(colIdx)
            if nCount == 2:
                candidateNum.append(thisNum)
                candidateRow.append(okRow)
                candidateCol.append(okCol)
            
    #verify x-wings
    xwings = []
    idxs = []
    for i in range(0, len(candidateNum)-1):
        num1 = candidateNum[i]
        cols1 = candidateCol[i]
        row1 = candidateRow[i]
        for ii in range(i+1, len(candidateNum)):
            num2 = candidateNum[ii]
            cols2 = candidateCol[ii]
            row2 = candidateRow[ii]
        #check that the num and the cols are he same
            if num1 == num2 and cols1 == cols2:
                xwings.append(num1)
                idxs.append([[row1, row2], cols1])
    return(xwings, idxs)


# now we remove all those numbers from the other rows in the columns where they appear
def replaceXwingsRows(ns, xwings, idxs):
    if len(xwings) == 0:
        return(ns)
    for i in range(0, len(xwings)):
        thisNum = xwings[i]
        #idxs of the first of the two cols
        idx1 = getIdxs(idxs[i][1][0], 'col')
        idx2 = getIdxs(idxs[i][1][1], 'col')
        idx3 = getIdxs(idxs[i][0][0], 'row')
        idx4 = getIdxs(idxs[i][0][1], 'row')
        allColsIdx = idx1 + idx2
        allRowsIdx = idx3 + idx4
        #remove row idx from col idx:
        allIdxs = remove_values_from_list(allColsIdx, allRowsIdx)
        for i in allIdxs:
            ns[i] = remove_values_from_list(ns[i], [thisNum])
    return(ns)

def solveXwingsRows(ns):
    xwings, idxs = checkXwingsRows(ns)
    ns = replaceXwingsRows(ns, xwings, idxs)
    return(ns)


def checkXwingsCols(ns):
    m, s = getMapping()
    # loop through rows
    candidateRow = []            
    candidateNum = []
    candidateCol = []            
    for colIdx in range(0,9):
        idxs = getIdxs(colIdx, 'col')
        for thisNum in range(1,10):
            nCount = 0
            okCol = colIdx
            okRow = []
            for rowIdx in range(0,9):
                nsIdx = m[rowIdx, colIdx]
                p = ns[nsIdx]
                if thisNum in p:
                    nCount = nCount + 1
                    okRow.append(rowIdx)
            if nCount == 2:
                candidateNum.append(thisNum)
                candidateRow.append(okRow)
                candidateCol.append(okCol)
            
    #verify x-wings
    xwings = []
    idxs = []
    for i in range(0, len(candidateNum)-1):
        num1 = candidateNum[i]
        col1 = candidateCol[i]
        rows1 = candidateRow[i]
        for ii in range(i+1, len(candidateNum)):
            num2 = candidateNum[ii]
            col2 = candidateCol[ii]
            rows2 = candidateRow[ii]
        #check that the num and the cols are he same
            if num1 == num2 and rows1 == rows2:
                xwings.append(num1)
                idxs.append([rows1, [col1, col2]])
    return(xwings, idxs)


# now we remove all those numbers from the other rows in the columns where they appear
def replaceXwingsCols(ns, xwings, idxs):
    if len(xwings) == 0:
        return(ns)
    for i in range(0, len(xwings)):
        thisNum = xwings[i]
        #idxs of the first of the two cols
        idx1 = getIdxs(idxs[i][1][0], 'col')
        idx2 = getIdxs(idxs[i][1][1], 'col')
        idx3 = getIdxs(idxs[i][0][0], 'row')
        idx4 = getIdxs(idxs[i][0][1], 'row')
        allColsIdx = idx1 + idx2
        allRowsIdx = idx3 + idx4
        #remove row idx from col idx:
        allIdxs = remove_values_from_list(allRowsIdx, allColsIdx)
        for i in allIdxs:
            ns[i] = remove_values_from_list(ns[i], [thisNum])
    return(ns)

def solveXWingsCols(ns):
    xwings, idxs = checkXwingsCols(ns)
    ns = replaceXwingsCols(ns, xwings, idxs)
    return(ns)

def solveXwings(ns):
    xwings, idxs = checkXwingsRows(ns)
    ns = replaceXwingsRows(ns, xwings, idxs)
    xwings, idxs = checkXwingsCols(ns)
    ns = replaceXwingsCols(ns, xwings, idxs)
    return(ns)

#################
## XY-Wing

def checkForXywing(ns):
    comb = list(combinations(list(range(0,81)), 3))
    posAre = []
    for thisComb in comb:
        num1 = ns[thisComb[0]]
        num2 = ns[thisComb[1]]
        num3 = ns[thisComb[2]]
        if len(num1) == 2 and len(num2) == 2 and len(num3) ==2:
            int1 = list(np.unique(np.asarray(num1 + num2)))
            int2 = list(np.unique(np.asarray(num2 + num3)))
            int3 = list(np.unique(np.asarray(num1 + num3)))
            allInt = list(np.unique(np.asarray(int1 + int2 + int3)))
            if len(int1) == 3 and len(int2) == 3 and len(int3) == 3 and len(allInt) == 3:
                posAre.append(thisComb)

    #now we validate positions
    #this is wrong
    okPos = []
    okVert = []
    okWings = []
    for thisCandidates in posAre:
        countApp = []
        for thisIdx in thisCandidates:
            allInts = getIntersections(thisIdx)
            countApp.append(len(intersection(allInts, list(thisCandidates))))
        if len(intersection(countApp, [3])) == 1:
            okPos.append(thisCandidates)
            okVert.append(findIdx(countApp, 3))
            okWings.append(negFindIdx(countApp, 3))
    return(okPos, okVert, okWings)

# do replacements
def replaceXywing(ns, pos, verts, wings):
    if len(pos) == 0:
        return(ns)
    for i in range(0, len(pos)):
        thisSet = list(pos[i])
        thisVert = verts[i]
        thisWings = wings[i]
        lst1 = getIntersections(pos[0][thisWings[0]])
        lst2 = getIntersections(pos[0][thisWings[1]])
        tmpLst = intersection(lst1, lst2)
        toRemove = intersection(ns[pos[0][thisWings[0]]], ns[pos[0][thisWings[1]]])[0]
        for ii in tmpLst:
            thisNs = ns[ii]
            if len(thisNs)>1 and toRemove in thisNs:
                thisNs.remove(toRemove)
            ns[ii] = thisNs
    return(ns)


def solevXYwing(ns):
    pos, vert, wings = checkForXywing(ns)
    ns = replaceXywing(ns, pos, vert, wings)
    return(ns)
