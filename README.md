This file will describe how to run the code for project 2

1) The packages used for this project are cv2, numpy, and sys. Please make sure these are installed 
and numpy is imported as np before running this code.
2) The first two variables in the code are Final_scale and Illistration_scale. These are used to scale the 
outputs of the code. Final_scale is set to 5 by default and will scale the final image of the search by 5 times.
Illistration_scale is set to 1 by default and will scale the activae visualization of the search by 1 by default. 
Change these values to your preference before running the code
3) The map has been pre-made and requires no user input
4) Once the code is run, the user will be prompted to input both the starting coordinates and the ending coordiantes.
If the user selects coordinates for either that are inside of an object, they will be prompted for new coordinates.
5) Once the start and end coordinates has been input the user will be shown a visualization for the search for the goal.
6) Once the goal has been found, a final image of the solution will be displayed to the user
7) In the console, the user with see the "track" dictionary displayed. This shows every parent child relationship generated
by The breadth first search (bfs)
8) The optimal path will then be displayed to the user. This path was found by tacking the goal child and parent combination
and backtracking through the "track" using the parent child relationship until the origianl parent is found
9) The corrisponding coordinates for each node will then be displayed in the same order that the optimal path is displayed. 
This shows the coordinate path from the end position to the start position as entered by the user
10) The program will then close and can be restarted with new starting and ending coordinates
11) Return to step 4
