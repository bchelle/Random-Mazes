# Random Maze Generator & Solvers 🧩

Contributors: Brock Chelle, Benjamin Wagg

## Included Files 📁

1. CreateMaze.py: Pseudo Randomly generates a maze of the user input size, the algorithm used here is called the 'Growing Tree'
2. SolveRM.py: Solves the randomly generated maze using the 'Random Mouse Method'
3. SolveLHR.py: Solves the randomly generated maze using the 'Left Hand Rule'
4. SolveDEE.py: Solves the randomly generated maze using the 'Dead End Elimination'
5. SolveSM.py: Solves the randomly generated maze using the 'Smart Mouse Method', which is a depth first search

All the below files won't appear until the code is executed
1. Maze.png: A PNG file containing the randomly generated maze
    * The Red and Green blocks on the maze are randomly placed (with some bias), and represent the start & finish respectively
2. SolvedRM.png: PNG file containing the 'Random Mouse' solution to the maze
    * The Blue Path is everywhere the mouse went on his path to the finish
    * The white areas are everywhere the mouse didn't go on his path to the finish
3. SolvedLHR.png: PNG file containing the 'Left Hand Rule' solution to the maze
    * The Blue Path is the path from start to finish while sticking to the left wall (Relative to direction of travel)
4. SolvedDEE.png: PNG file containing the 'Dead End Elimination' solution to the maze
    * The White Path is the shortest path from start to finish
    * The Blue Areas represent all the dead ends that were filled in
5. SolvedSM.png: PNG file containing the 'Smart Mouse' solution to the maze
    * The Blue Path is the shortest path from start to finish

### Notes 📝

1. A self-created simulation of all these algorithms is availble at https://www.youtube.com/watch?v=gktYREKxwkw
2. CreateMaze.py Has 3 Adjustable modes within the code.
    * Mode 1, SOLVERS: When on (1) will ask if you want them to be solved using the algorithms
    * Mode 2, INSTRUCTIONS: Gives in depth instuctions on allowable user inputs
    * Mode 3, RUNTIMER: Will return the runtime of CreateMaze.py along with any of the solving algorithms used
    * Default Mode is: SOLVERS (ON), INSTRUCTIONS (ON), RUNTIMER(OFF)

## Running Instructions 🏃‍♀️

1. Clone the repository onto your machine
2. Install the PILLOW module
3. In the terminal, Navigate to the directory with all the files
4. Execute `python3 CreateMaze.py`
5. Follow the given input intructions when the program is run
6. If Solvers is ON, select which algorithms you would like to solve the maze with
7. When you have finished executing the program there will be a series of '.png' files in the same directiory, see the 'Other Included Files' if clarification is needed

## Assumptions

* Inputs for  maze size will be be positive odd integers, where at least one is greater than 1
* Inputs for zoom are positive integers

* To solve with the Left Hand Rule the Zoom must be divisible by 3
* To solve with the Random Mouse the maze has to be of a relatively small size due to the inefficiency of the algorithm
