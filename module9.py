# the convention is to number the coords from 1 to 4 as
# 1 TL
# 2 TR
# 3 BR
# 4 BR
# Of the 4 coordinates given, we need to sort them appropriately

# We use the logic:
# 1 has the lowest row * col
# 3 has the highest row * col
# 2 has the remaining lowest row of the remaining
# 4 is the remaining point
def getIdxs(pos):
    if not len(pos) == 4:
        print('pos must have exaclty 4 sets of coordinates')
        return([])
    prodPos = []
    allRows = []
    for i in range(0,4):
        prodPos.append(pos[i][0]*pos[i][1])
        allRows.append(pos[i][0])
    
    # 1
    idx_1 = prodPos.index(np.amin(prodPos))
    # 3
    idx_3 = prodPos.index(np.amax(prodPos))
    # 2
    allRows[idx_1] = 1e10 #insane high number (we will not have a picture with more than 1e10 rows)
    idx_2 = allRows.index(np.amin(allRows))
    # 4
    allRows[idx_1] = 0 #we will not have a picture with 0 rows
    allRows[idx_3] = 0 #we will not have a picture with 0 rows
    idx_4 = allRows.index(np.amax(allRows))

    return([idx_1, idx_2, idx_3, idx_4])

def getImageGrid(pos, img):
    if not len(pos) == 4:
        return(np.zeros(1,1)) #return a small array. We will then check that its shape in the main UI logic
    
    # sort the given pos
    posIdxs = getIdxs(pos)

    #get grid borders
    allRowsp12, allColsp12 = getCoords(pos[posIdxs[0]][0], pos[posIdxs[0]][1], pos[posIdxs[1]][0], pos[posIdxs[1]][1], 'row')    

    allRowsp23, allColsp23 = getCoords(pos[posIdxs[1]][0], pos[posIdxs[1]][1], pos[posIdxs[2]][0], pos[posIdxs[2]][1], 'col')

    allRowsp43, allColsp43 = getCoords(pos[posIdxs[3]][0], pos[posIdxs[3]][1], pos[posIdxs[2]][0], pos[posIdxs[2]][1], 'row')

    allRowsp14, allColsp14 = getCoords(pos[posIdxs[0]][0], pos[posIdxs[0]][1], pos[posIdxs[3]][0], pos[posIdxs[3]][1], 'col')    


    imgGrid = np.zeros((img.shape[0], img.shape[1]))
    for i in range(0,10):
        xs, ys = getLineFullImg(allRowsp12[i], allColsp12[i], allRowsp43[i], allColsp43[i], 'col')
        imgGrid[xs, ys] = imgGrid[xs, ys] + 1
        xs, ys = getLineFullImg(allRowsp23[i], allColsp23[i], allRowsp14[i], allColsp14[i], 'row')
        imgGrid[xs, ys] = imgGrid[xs, ys] + 1
    squares = np.argwhere(imgGrid==2)

    #assuming this difference is representative of the average size of a square
    squareSize = int(np.mean([allColsp12[1] - allColsp12[0], allRowsp14[1] - allRowsp14[0]])) 
    maxCol = np.amax(allColsp23)
    maxRow = np.amax(allRowsp43)
    tmpGrid = np.zeros((img.shape[0], img.shape[1]))
    k=0
    for ii in range(0, 100):
        rowStart = squares[ii][0]
        colStart = squares[ii][1]
        rowEnd = rowStart + squareSize
        colEnd = colStart + squareSize
        
        if colEnd <= maxCol+5 and rowEnd <= maxRow+5:
            tmpGrid[rowStart:rowEnd, colStart:colEnd] = 255
            thisSquare = img[rowStart:rowEnd, colStart:colEnd]
            desiredSize = 30 
            scaleFactor = desiredSize/thisSquare.shape[0]
            image_rescaled = rescale(thisSquare, scaleFactor, anti_aliasing=True, multichannel = False)
            if k == 0:
                allSquares = image_rescaled
            else:
                allSquares = np.dstack((allSquares, image_rescaled))
            k = k+1
            
    tmpGrid[imgGrid > 0] = 0
    
    allSquares = np.transpose(allSquares, (2, 0, 1))  
    # Reshaping the array to 4-dims so that it can work with the Keras API
    allSquares = allSquares.reshape(allSquares.shape[0], allSquares.shape[1],
                                            allSquares.shape[2], 1)
    
    return(tmpGrid, allSquares)

def getOverlay(img, background):
    background[:,:,0] = background[:,:,0]*img
    background[:,:,1] = background[:,:,1]*img
    background[:,:,2] = background[:,:,2]*img
    return(background)

