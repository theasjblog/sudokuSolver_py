from imageAnalysisGrid import *
import csv
import os
import re
from skimage.transform import rescale

def getCoords(row1, col1, row2, col2, direction):
    if direction == 'row':
        row1 = int(np.mean([row1, row2]))
        row2 = row1
    if direction == 'col':
        col1 = int(np.mean([col1, col2]))
        col2 = col1
    allRows = list(map(int, np.linspace(row1, row2, 10)))
    allCols = list(map(int, np.linspace(col1, col2, 10)))
    return(allRows, allCols)

def getLineFullImg(row1, col1, row2, col2, direction):
    if direction == 'row':
        rowStart = int(np.mean([row1, row2]))
        rowEnd = rowStart
        colStart = col1
        colEnd = col2
        
    if direction == 'col':
        colStart = int(np.mean([col1, col2]))
        colEnd = colStart
        rowStart = row1
        rowEnd = row2
    
    nPoints = np.amax([np.absolute(rowStart-rowEnd), np.absolute(colStart-colEnd)])
        
    xs = list(map(int, np.linspace(rowStart, rowEnd, nPoints)))
    ys = list(map(int, np.linspace(colStart, colEnd, nPoints)))
    return(xs, ys)

def getBorders(cornersDict, idx):
    allRowsp12, allColsp12 = getCoords(cornersDict['p1_y'][idx], cornersDict['p1_x'][idx],
                                cornersDict['p2_y'][idx], cornersDict['p2_x'][idx], 'row')    

    allRowsp23, allColsp23 = getCoords(cornersDict['p2_y'][idx], cornersDict['p2_x'][idx],
                                cornersDict['p3_y'][idx], cornersDict['p3_x'][idx], 'col')    

    allRowsp43, allColsp43 = getCoords(cornersDict['p4_y'][idx], cornersDict['p4_x'][idx],
                                cornersDict['p3_y'][idx], cornersDict['p3_x'][idx], 'row')    

    allRowsp14, allColsp14 = getCoords(cornersDict['p1_y'][idx], cornersDict['p1_x'][idx],
                                cornersDict['p4_y'][idx], cornersDict['p4_x'][idx], 'col')
    
    return(allRowsp12, allColsp12, allRowsp23, allColsp23, allRowsp43, allColsp43, allRowsp14, allColsp14)


