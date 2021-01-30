import numpy as np

# sample simple sudokusampleSudoku
sampleSudoku = np.array([[5, 3, 0, 0, 7, 0, 0, 0, 0],
                         [6, 0, 0, 1, 9, 5, 0, 0, 0],
                         [0, 9, 8, 0, 0, 0, 0, 6, 0],
                         [8, 0, 0, 0, 6, 0, 0, 0, 3],
                         [4, 0, 0, 8, 0, 3, 0, 0, 1],
                         [7, 0, 0, 0, 2, 0, 0, 0, 6],
                         [0, 6, 0, 0, 0, 0, 2, 8, 0],
                         [0, 0, 0, 4, 1, 9, 0, 0, 5],
                         [0, 0, 0, 0, 8, 0, 0, 7, 9]])

# hard sudoku
hardSudoku = np.zeros((9,9))
hardSudoku[0,1] = 4
hardSudoku[0,7] = 1
hardSudoku[1,0] = 2
hardSudoku[1,8] = 6
hardSudoku[7,0] = 9
hardSudoku[7,8] = 2
hardSudoku[8,1] = 1
hardSudoku[8,7] = 9

# pairs in
# not solvable but can test pairs			
pairSudoku = np.zeros((9,9))
pairSudoku[0,3] = 4
pairSudoku[0,4] = 5
pairSudoku[0,5] = 6
pairSudoku[0,6] = 7
pairSudoku[0,7] = 8
pairSudoku[0,8] = 9
pairSudoku[3,0] = 2
pairSudoku[3,1] = 1 
pairSudoku[6,2] = 1

	
# row 0, col 0, 1 and 6 are triplets
#not solvable but can test triplets
tripSudoku = np.zeros((9,9))
tripSudoku[0,2] = 7
tripSudoku[0,3] = 2
tripSudoku[0,4] = 3
tripSudoku[0,5] = 4
tripSudoku[1,0] = 6
tripSudoku[1,1] = 8
tripSudoku[3,6] = 6
tripSudoku[4,6] = 8
tripSudoku[3,7] = 5
tripSudoku[3,8] = 1

# another triplet, but this time not obvious
# in row 0, col 0, 4, 8
#not solvable but can test triplets
nakedTripSudoku = np.zeros((9,9))
nakedTripSudoku[0,1] = 2
nakedTripSudoku[1,1] = 3
nakedTripSudoku[2,1] = 7
nakedTripSudoku[6,0] = 4
nakedTripSudoku[3,0] = 1
nakedTripSudoku[4,0] = 8
nakedTripSudoku[5,0] = 9
nakedTripSudoku[3,2] = 5
nakedTripSudoku[2,4] = 3
nakedTripSudoku[1,4] = 5
nakedTripSudoku[4,3] = 9
nakedTripSudoku[4,4] = 1
nakedTripSudoku[3,4] = 4
nakedTripSudoku[5,4] = 7
nakedTripSudoku[7,4] = 9
nakedTripSudoku[7,5] = 4
nakedTripSudoku[3,5] = 8
nakedTripSudoku[4,2] = 6
nakedTripSudoku[6,3] = 1
nakedTripSudoku[7,3] = 8
nakedTripSudoku[3,3] = 6
nakedTripSudoku[1,5] = 9
nakedTripSudoku[1,6] = 1
nakedTripSudoku[2,6] = 6
nakedTripSudoku[4,6] = 5
nakedTripSudoku[5,6] = 8
nakedTripSudoku[6,7] = 8
nakedTripSudoku[3,8] = 3
nakedTripSudoku[4,8] = 4
nakedTripSudoku[6,8] = 7
nakedTripSudoku[8,8] = 9

#quad are in [0,0], [1,0], [1,1], [1,2]
#not solvable but can test quads
quadSudoku = np.zeros((9,9))
quadSudoku[0,1] = 5
quadSudoku[2,2] = 2
quadSudoku[0,6] = 4
quadSudoku[0,4] = 7
quadSudoku[3,0] = 3
quadSudoku[4,0] = 6
quadSudoku[5,0] = 8
quadSudoku[3,2] = 9
quadSudoku[1,3] = 4
quadSudoku[1,4] = 6
quadSudoku[1,5] = 8
quadSudoku[4,2] = 7
quadSudoku[2,6] = 7
quadSudoku[2,3] = 3
quadSudoku[6,1] = 8

# hidden pair in [2,0], [2,2]
hidden2Sudoku = np.zeros((9,9))
hidden2Sudoku[0,0] = 3
hidden2Sudoku[0,2] = 1
hidden2Sudoku[1,1] = 2
hidden2Sudoku[0,3] = 6
hidden2Sudoku[0,4] = 7
hidden2Sudoku[0,5] = 9
hidden2Sudoku[1,6] = 6
hidden2Sudoku[1,3] = 8
hidden2Sudoku[1,7] = 9
hidden2Sudoku[3,2] = 7
hidden2Sudoku[2,3] = 4
hidden2Sudoku[2,4] = 5
hidden2Sudoku[3,1] = 6
hidden2Sudoku[4,1] = 9

# hidden 3 in [1,0], [1,1], [2,0] = 2,6,8	
hidden3Sudoku = np.zeros((9,9))
hidden3Sudoku[2,1] = 5
hidden3Sudoku[0,3] = 1
hidden3Sudoku[0,4] = 2
hidden3Sudoku[0,5] = 6
hidden3Sudoku[0,6] = 8
hidden3Sudoku[1,3] = 3
hidden3Sudoku[2,3] = 8
hidden3Sudoku[3,0] = 3
hidden3Sudoku[4,0] = 9
hidden3Sudoku[6,1] = 3
hidden3Sudoku[3,2] = 7
hidden3Sudoku[3,1] = 1
hidden3Sudoku[4,2] = 2
hidden3Sudoku[5,2] = 6
hidden3Sudoku[6,2] = 8

# hidden 4 in [6,1], [6,2], [7,1], [7,2] = 2,4,5,8
hidden4Sudoku = np.zeros((9,9))
hidden4Sudoku[0,3] = 5
hidden4Sudoku[2,3] = 2
hidden4Sudoku[4,3] = 4
hidden4Sudoku[5,3] = 8
hidden4Sudoku[0,4] = 7
hidden4Sudoku[4,4] = 9
hidden4Sudoku[0,5] = 3
hidden4Sudoku[2,5] = 9
hidden4Sudoku[4,5] = 6
hidden4Sudoku[6,0] = 2
hidden4Sudoku[6,1] = 7
hidden4Sudoku[6,2] = 9
hidden4Sudoku[7,0] = 1
hidden4Sudoku[7,1] = 3
hidden4Sudoku[7,2] = 8
hidden4Sudoku[8,0] = 5
hidden4Sudoku[8,1] = 6
hidden4Sudoku[8,2] = 4
hidden4Sudoku[6,8] = 1
hidden4Sudoku[7,7] = 7
hidden4Sudoku[8,7] = 8
hidden4Sudoku[8,8] = 2


# cells [2,1], [2,3], [4,1], [4,3] = 4
xwingSudoku = np.zeros((9,9))
xwingSudoku[0,2] = 3
xwingSudoku[0,3] = 8
xwingSudoku[0,6] = 5
xwingSudoku[0,7] = 1
xwingSudoku[1,2] = 8
xwingSudoku[1,3] = 7
xwingSudoku[1,6] = 9
xwingSudoku[1,7] = 3
xwingSudoku[2,0] = 1
xwingSudoku[2,3] = 3
xwingSudoku[2,5] = 5
xwingSudoku[2,6] = 7
xwingSudoku[2,7] = 2
xwingSudoku[2,8] = 8
xwingSudoku[3,3] = 2
xwingSudoku[3,6] = 8
xwingSudoku[3,7] = 4
xwingSudoku[3,8] = 9
xwingSudoku[4,0] = 8
xwingSudoku[4,2] = 1
xwingSudoku[4,3] = 9
xwingSudoku[4,5] = 6
xwingSudoku[4,6] = 2
xwingSudoku[4,7] = 5
xwingSudoku[4,8] = 7
xwingSudoku[5,3] = 5
xwingSudoku[5,6] = 1
xwingSudoku[5,7] = 6
xwingSudoku[5,8] = 3
xwingSudoku[6,0] = 9
xwingSudoku[6,1] = 6
xwingSudoku[6,2] = 4
xwingSudoku[6,3] = 1
xwingSudoku[6,4] = 2
xwingSudoku[6,5] = 7
xwingSudoku[6,6] = 3
xwingSudoku[6,7] = 8
xwingSudoku[6,8] = 5
xwingSudoku[7,0] = 3
xwingSudoku[7,1] = 8
xwingSudoku[7,2] = 2
xwingSudoku[7,3] = 6
xwingSudoku[7,4] = 5
xwingSudoku[7,5] = 9
xwingSudoku[7,6] = 4
xwingSudoku[7,7] = 7
xwingSudoku[7,8] = 1
xwingSudoku[8,1] = 1
xwingSudoku[8,3] = 4
xwingSudoku[8,6] = 6
xwingSudoku[8,7] = 9
xwingSudoku[8,8] = 2



# xy wing in [2,0], [2,3], [0,5] = 1, 7, 2
xywingSudoku = np.zeros((9,9))
xywingSudoku[0,1] = 4
xywingSudoku[0,3] = 5
xywingSudoku[0,4] = 9
xywingSudoku[1,0] = 5
xywingSudoku[1,1] = 9
xywingSudoku[1,2] = 7
xywingSudoku[1,4] = 8
xywingSudoku[2,1] = 6
xywingSudoku[2,2] = 8
xywingSudoku[2,4] = 3
xywingSudoku[2,5] = 4
xywingSudoku[3,2] = 2
xywingSudoku[4,5] = 2
xywingSudoku[0,6] = 6
xywingSudoku[3,3] = 1