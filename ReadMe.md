8-Puzzle Task Documentation
1. Short Task Description

This project implements a solution for the classic 8-Puzzle problem using the A* search algorithm with two heuristic functions: Hamming distance and Manhattan distance.

The application offers two main features:

Generate and solve 100 random solvable puzzles, comparing heuristic performance.

Input a custom puzzle and solve it if it’s solvable (or inform the user if it’s not).

The main purpose is to study the behavior of A* search with different heuristics and to gain experience with search algorithms, state-space exploration, and Python project structuring.

2. Software Architecture Diagram
```mermaid
flowchart TB
    main[main.py<br/>Entry point] --> app[app.py<br/>CLI, input, printing, flow control]

    app --> puzzle[puzzle.py<br/>Puzzle8, moves, solvability]
    app --> game[game.py<br/>A* search, heuristics, successor states]
    app --> state[state.py<br/>State alias, GOAL, utils]

    game --> node[node.py<br/>Node (f, g, h, parent)]
    game --> state
    puzzle --> state
    node --> state
```



3. Module Overview

main.py: Entry point of the application. Starts the program and calls into the main menu logic.

app.py: Handles the command-line interface: menu, user input, validation, and printing results. It also runs the batch test for 100 puzzles.

puzzle.py:	Defines the Puzzle8 class. Generates random solvable puzzles, represents the puzzle state, and includes move logic and solvability checks.

node.py:	Defines the Node class used by A*. Stores state, parent reference, cost (g), heuristic (h), and total cost (f = g + h).

game.py: Contains the A* search algorithm, successor generation, and both heuristics (Hamming and Manhattan).

state.py: Holds the State type alias, the GOAL state, and utility functions related to puzzle state representation.

4. Design Decisions


State Representation:
Puzzle states are stored as immutable 9-element tuples. Tuples are hashable and efficient for dictionary and set lookups when tracking visited states.

Node Class:
Each Node stores its state, cost (g), heuristic (h), total cost (f = g + h), and a reference to its parent to reconstruct the solution path.

Heuristics:

Hamming Distance: Counts how many tiles are not in their correct position.

Manhattan Distance: Calculates the total distance each tile is from its correct position.
Manhattan is more informed and leads to significantly fewer node expansions.

Architecture and Responsibilities:
The program is structured into separate modules for clarity, but some modules (e.g. app.py and game.py) still handle multiple responsibilities. For example, app.py both handles the user interface and benchmarking, and game.py contains the search algorithm, successor generation, and heuristics. These decisions were made to keep the code compact and easier to navigate for a project of this size, even if they slightly compromise strict single-responsibility principles.

Input Validation:
User-provided puzzles are validated for correct format and checked for solvability before solving.

5. Discussion and Conclusions
Experience

This project provided valuable hands-on experience with heuristic search algorithms, puzzle solvability, and Python project organization. While the architecture works well for a small project, some modules could be split further if the project were to grow. Balancing clarity, simplicity, and clean design was an important part of the process.

Heuristic Comparison after 100 runs:

Hamming: 
- avg steps=21.74 
- avg expanded=14166.9 
- avg time=96.5 ms

Manhattan: 
- avg steps=21.74 
- avg expanded=1334.2 
- avg time=9.3 ms

Conclusion:
Both heuristics are admissible and lead to optimal solutions, but Manhattan distance consistently expands fewer nodes and runs faster because it provides a more accurate estimate of the remaining cost.

Possible Improvements

- Implement additional heuristics for deeper comparisons.

- Add a graphical user interface (GUI) using PySide6.

- Visualize the search process or solution path.
