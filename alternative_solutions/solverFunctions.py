
# coding: utf-8

# # Sudoku Solver core functions
# 
# 
# This notebook contains the core functions to solve a sudoku:
# 
# * The solver
# * Validator
# * Some test cases

# In[1]:


# imports
import numpy as np
import sys
import math
import time


# In[2]:


# test grids
emptySudoku = np.zeros((9,9))

sampleSudoku = np.array([[5, 3, 0, 0, 7, 0, 0, 0, 0],
                         [6, 0, 0, 1, 9, 5, 0, 0, 0],
                         [0, 9, 8, 0, 0, 0, 0, 6, 0],
                         [8, 0, 0, 0, 6, 0, 0, 0, 3],
                         [4, 0, 0, 8, 0, 3, 0, 0, 1],
                         [7, 0, 0, 0, 2, 0, 0, 0, 6],
                         [0, 6, 0, 0, 0, 0, 2, 8, 0],
                         [0, 0, 0, 4, 1, 9, 0, 0, 5],
                         [0, 0, 0, 0, 8, 0, 0, 7, 9]])

invalidRow = np.array([[5, 5, 0, 0, 7, 0, 0, 0, 0],
                         [6, 0, 0, 1, 9, 5, 0, 0, 0],
                         [0, 9, 8, 0, 0, 0, 0, 6, 0],
                         [8, 0, 0, 0, 6, 0, 0, 0, 3],
                         [4, 0, 0, 8, 0, 3, 0, 0, 1],
                         [7, 0, 0, 0, 2, 0, 0, 0, 6],
                         [0, 6, 0, 0, 0, 0, 2, 8, 0],
                         [0, 0, 0, 4, 1, 9, 0, 0, 5],
                         [0, 0, 0, 0, 8, 0, 0, 7, 9]])

invalidCol = np.array([[5, 3, 0, 0, 7, 0, 0, 0, 0],
                         [6, 0, 0, 1, 9, 5, 0, 0, 0],
                         [5, 9, 8, 0, 0, 0, 0, 6, 0],
                         [8, 0, 0, 0, 6, 0, 0, 0, 3],
                         [4, 0, 0, 8, 0, 3, 0, 0, 1],
                         [7, 0, 0, 0, 2, 0, 0, 0, 6],
                         [0, 6, 0, 0, 0, 0, 2, 8, 0],
                         [0, 0, 0, 4, 1, 9, 0, 0, 5],
                         [0, 0, 0, 0, 8, 0, 0, 7, 9]])

invalidSquare = np.array([[5, 3, 0, 0, 7, 0, 0, 0, 0],
                         [6, 0, 3, 1, 9, 5, 0, 0, 0],
                         [0, 9, 8, 0, 0, 0, 0, 6, 0],
                         [8, 0, 0, 0, 6, 0, 0, 0, 3],
                         [4, 0, 0, 8, 0, 3, 0, 0, 1],
                         [7, 0, 0, 0, 2, 0, 0, 0, 6],
                         [0, 6, 0, 0, 0, 0, 2, 8, 0],
                         [0, 0, 0, 4, 1, 9, 0, 0, 5],
                         [0, 0, 0, 0, 8, 0, 0, 7, 9]])

solvedSudoku = np.array([[5, 3, 4, 6, 7, 8, 9, 1, 2],
                         [6, 7, 2, 1, 9, 5, 3, 4, 8],
                         [1, 9, 8, 3, 4, 2, 5, 6, 7],
                         [8, 5, 9, 7, 6, 1, 4, 2, 3],
                         [4, 2, 6, 8, 5, 3, 7, 9, 1],
                         [7, 1, 3, 9, 2, 4, 8, 5, 6],
                         [9, 6, 1, 5, 3, 7, 2, 8, 4],
                         [2, 8, 7, 4, 1, 9, 6, 3, 5],
                         [3, 4, 5, 2, 8, 6, 1, 7, 9]])


# # Validation 
# 
# Functions to see if a grid is solvable.
# 
# To be solvable, a grid must:
# 
# * be of shape (9,9)
# * every row and column must contain only unique values (excluded 0s)
# * each 3X3 sub-grid must contain only unique values

# In[3]:


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
        #print('wrong shape')
        return(False)
    rows = all(np.apply_along_axis(lineCheck, 0, grid))
    cols = all(np.apply_along_axis(lineCheck, 1, grid))
    if( not rows or not cols):
        #print('duplicates in rows or cols')
        return(False)
    gridCoord = [0,3,6]
    checkSquareRes = []
    for i in gridCoord:
        for ii in gridCoord:
            square = grid[i:i+3, ii:ii+3]
            checkSquareRes = np.append(checkSquareRes, checkSquare(square))
            
    
    checkSquareRes = all(checkSquareRes)
    if( not checkSquareRes):
        #print('duplicates in square')
        return(False)
    
    return(True)


# # Main solver function
# 
# Iteratively loop over cols, rows and sub-grids to see what can be filled up. Keep repeting the loops until a solution is found or until we hit the imposed time limit.

# In[4]:


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
        line = np.ndarray.flatten(grid)
        line = [i for i in line if i == 0]
        n0start = len(line)
        if n0start == 0:
            break
        grid = fillSquares(grid)
        line = np.ndarray.flatten(grid)
        line = [i for i in line if i == 0]
        n0s = len(line)
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
        line = np.ndarray.flatten(grid)
        line = [i for i in line if i == 0]
        n0end = len(line)
        if n0end == 0:
            break
        #check if we are making progress
        if n0start == n0end:
            break
        # check if we passed the timout
        if time.time() > timeout:
            break
    
    
    #check if we solved
    line = np.ndarray.flatten(grid)
    line = [i for i in line if i == 0]
    n0end = len(line)
    if n0end == 0:
        return(grid)
    else:
        return('Sudoku was not solved')


# In[5]:


solveSudoku(sampleSudoku)

