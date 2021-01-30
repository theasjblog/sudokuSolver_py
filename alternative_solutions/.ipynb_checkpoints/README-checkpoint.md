# Sudoku Solver

Semi-automatic solver. In its current state the solver:

* Get user to take a picture of the sudoku
* Analyze sudoku to get the number in each square. This is done using a pre-trained classifier model (`sudoku_clf.kb`)
* Alow user to manually fix any mis-calssification
* Solve using recursion and backtracking
* Print solution

# 

## To do and issues

* Build UI around it
* Better and more automatic way to detect grid corners
* The image taking will  not work with grids that are not squares. In that case twe need to do a manual warp to re-size the grid to a square
* Try CNN to  get better solution
* Allow upload of csv and/or spreadsheet

