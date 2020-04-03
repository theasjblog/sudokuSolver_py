import numpy as np

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