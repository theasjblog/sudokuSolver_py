# Sudoku Solver

Semi-automatic solver. In its current state the solver:

* Get user to take a picture of the sudoku (needs to be optimized for different screen sizes and resolutions)
* Analyze sudoku to get the number in each square. This is done using a pre-trained classifier model (`sudoku_clf.kb`)
* Alow user to manually fix any mis-calssification
* Solve using recursion and backtracking
* Print solution

# Repos file

* `00-solver`: the core solver
* `01-image analysis`: an attempt to automatically detect the grid. The genaral approach is not used in the final solution, but some functions are recycled
* `02-image capture`: use the laptop camera to capture an image of a sudoku
* `03-get training data`: process the training dataset to get the individual grid's squares and labels
* `04-image processing for training`: ML training
* `05-from image to solution`: putting everything (interactive parts) together in one notebook using the model trained in notebook 04
* `rawImg`: The dataset (details in the notebook)
* `alternative_solutions`: a folder containing previous approach to the solution

## To do and issues

* Build UI around it
* Generalize image aquisition (currently working for Microsoft Surface Go Gen1)
* Complete testing
* Better and more automatic way to detect grid corners
* The image taking will  not work with grids that are not squares. In that case twe need to do a manual warp to re-size the grid to a square
* Try CNN to  get better solution
* Allow upload of csv and/or spreadsheet

