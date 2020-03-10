# imports

import os
import imageio
import numpy as np
from skimage import io
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import math
from PIL import Image
from skimage.filters import threshold_niblack, threshold_sauvola
from skimage.transform import hough_line, hough_line_peaks
get_ipython().run_line_magic('matplotlib', 'inline')



# get grayscale image
def readImg(filePath):
    imgOr = imageio.imread(filePath)
    img = rgb2gray(imgOr)
    return(img)


# get adaptive threshold
def doThresholding(method, window_size, k, img):
    if method == 'niblack':
        th_mask = threshold_niblack(img, window_size=window_size, k=k)
    if method == 'sauvola':
        th_mask = threshold_sauvola(img, window_size=window_size)

    binary_mask = img < th_mask
    return(binary_mask)

def applyHough(nAngles, img):
    # hough
    # Classic straight-line Hough transform
    # Set a precision of 0.5 degree.
    tested_angles = np.linspace(-np.pi / 2, np.pi / 2, nAngles)

    h, theta, d = hough_line(img, theta=tested_angles)
    return(h, theta, d)

def getYs(sizeRef, h, theta, d):
    origin = np.array((0, sizeRef))
    allY0s = []
    allY1s = []
    for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
        y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)
        allY0s.append(y0)
        allY1s.append(y1)
    return(allY0s, allY1s)

def getLines(allY0s, allY1s, shapeIm):
    allRowsReturn = []
    allColsReturn = []
    nPoints = int(round(math.sqrt(shapeIm[0]**2+shapeIm[1]**2)))
    
    for i in range(0, len(allY0s)):
        y0 = allY0s[i]
        y1 = allY1s[i]
        x0, x1, y0, y1 = getCoords(y0, y1, shapeIm)
        
        allRows, allCols = getIdxsArray(x0, x1, y0, y1) 
        allColsReturn.append(allCols)
        allRowsReturn.append(allRows)
    return(allRowsReturn, allColsReturn)

def getIdxsArray(x0, x1, y0, y1):
    #this converts plot coordinates to array coordinates
        #linespace to get all values between the plot ([x0, y0], [x1, y1]) coordinates
        allRows = list(map(int, np.ndarray.tolist(np.round(np.linspace(y0, y1, nPoints),0))))
        allCols = list(map(int, np.ndarray.tolist(np.round(np.linspace(x0, x1, nPoints),0))))
        return(allRows, allCols)
    
def getCoords(y0, y1, shapeIm):
    origin = np.array((0, shapeIm[1]))
    if y0 < 0 or y1 > shapeIm[0]:
        # this deals with vertical lines, using the equation of a line to
        # get the corresponding points fitting inside the figure coordinates space
        mLine = (y0-y1)/(origin[0]-origin[1])
        qLine = y0
        #when y=0 and y = (img height)-1
        y0 = 0
        y1 = shapeIm[0]-2
        x0 = int(round((y0-qLine)/mLine))
        x1 = int(round((y1-qLine)/mLine))
    else :
        x0 = 0
        x1 = shapeIm[1]-1
        y1 = y1-2
        # ugly piece of code to deal with going out of array index
        if y0 > shapeIm[0]-1:
            y0 = shapeIm[0]-1
        if y1 > shapeIm[0]-1:
            y1 = shapeIm[0]-1
                
    return(x0, x1, y0, y1)

def checkLines(filename, window_size, k, nAngles):
    img = readImg(filename)

    thImg = doThresholding('niblack', window_size, k, img)

    h, theta, d = applyHough(nAngles, thImg)

    allY0s, allY1s = getYs(thImg.shape[1], h, theta, d)

    return(allY0s, allY1s)


