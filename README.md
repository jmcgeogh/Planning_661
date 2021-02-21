# Planning_661
# Project 1
This file will describe how to run the code for project 1
1) Make sure all packages used at the top of the file have been installed on your machine. 
For this project that includes the "time" package
2) This project will output a .txt file with the full list of configurations created. 
This file will be created in the same directory where the code is run.
3) The five testable initial states have already been loaded in, which one you decide to run
is dpendent on which you set as equal to "initial_state"
4) Once the initial state you want to run has been selected, run the code. The code will run 
until one of the end conditions are met.
5) The while loop will run, moving the blank tile through the four direction when applicable and 
storing the viable configurations until the end state is found, it has run for two hours, or
the storage list reaches 1,000,000 values.
6) The end state is found using breadth first search, the total number of configurations tested,
as well as those still untested will be displayed in the consol
7) The .txt file for your selected state will then be created
8) You will be prompted to decide whether you would like to select a specific configuration to view
9) Selecting "n" will cause the program to close
10) Selecting "y" will display the tree dictioanry with all of the parent child relationships created
11) Select the parent number you would like to see
12) Select the child number you would like to see
13) The output configuration is the result of the parent child combination, the program will close
14) Return to step 3
