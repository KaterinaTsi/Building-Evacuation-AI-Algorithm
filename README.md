# Building-Evacuation-AI-Algorithm
AI algorithm simulating building evacuation in emergencies. It models elevator trips to move occupants from floors to the rooftop. Supports DFS, BFS, and Best-First search, with a heuristic estimating steps. Useful for AI pathfinding and emergency planning simulations.

# Features----------------------------------------------------------------------

- **Simulates emergency evacuation:** Moves building occupants to the rooftop efficiently.
- **Search algorithms supported:** DFS, BFS, DFS-Q, BFS-Q, Best-First Search.
- **Heuristic evaluation:** Estimates number of elevator trips needed for faster solutions.
- **Flexible initial states:** Customize number of occupants per floor and elevator capacity.
- **Path tracking:** Provides the full sequence of states leading to the goal.

#Usage--------------------------------------------------------------------------

1.When prompted, enter the search method:
ENTER DFS OR BFS OR DFS-Q OR BFS-Q OR BESTFS:


2.The program will output:

>Current frontier or queue
>States explored
>Path to the goal state once found
>Goal state confirmation

#How it Works------------------------------------------------------------------

State Representation: [elevator floor, occupants 1st, 2nd, 3rd, 4th floor, people in elevator]

Operators: Functions that simulate moving occupants from floors to the elevator and then to the roof.

Search: Frontier (or queue) expansion using the chosen search method.

Heuristic: Assigns cost to states based on the number of trips needed to evacuate remaining occupants.

Example-------------------------------------------------------------------------

Initial state: [0, 9, 4, 12, 7, 0]
Goal state: [5, 0, 0, 0, 0, 0]

After running BFS, the program prints the path of states leading to the rooftop evacuation.
