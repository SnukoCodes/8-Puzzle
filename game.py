import heapq
from typing import Callable, Dict, List, Tuple
from node import Node
from state import State, GOAL

# For each index of the blank (0..8), define which indices are adjacent.
# This is used to generate valid moves.
NEIGHBOR_INDEXES = {
    0: (1, 3),
    1: (0, 2, 4),
    2: (1, 5),
    3: (0, 4, 6),
    4: (1, 3, 5, 7),
    5: (2, 4, 8),
    6: (3, 7),
    7: (4, 6, 8),
    8: (5, 7),
}

# Precompute where each tile *should* be in the goal state for Manhattan distance
GOAL_POSITIONS = {}
for index, tile in enumerate(GOAL):
    GOAL_POSITIONS[tile] = index

def get_successor_states(state: State) -> List[Tuple[State, int]]:
    """
    Return a list of all valid next states from the current state.
    Each element is (next_state, moved_tile).
    """
    blank_index = state.index(0)  # find the blank (0)
    successors = []

    for neighbor_index in NEIGHBOR_INDEXES[blank_index]:
        new_state_list = list(state)
        moved_tile = new_state_list[neighbor_index]

        # swap the blank and the neighbor tile
        new_state_list[blank_index], new_state_list[neighbor_index] = (
            new_state_list[neighbor_index],
            new_state_list[blank_index],
        )
        successors.append((tuple(new_state_list), moved_tile))

    return successors

def hamming_distance(state: State) -> int:
    """Number of tiles out of place (ignoring the blank)."""
    return sum(
        1 for index, tile in enumerate(state)
        if tile != 0 and tile != GOAL[index]
    )

def manhattan_distance(state: State) -> int:
    """Sum of Manhattan distances for all tiles from their goal positions."""
    total_distance = 0
    for index, tile in enumerate(state):
        if tile == 0:
            continue
        goal_index = GOAL_POSITIONS[tile]
        row_distance = abs(index // 3 - goal_index // 3)
        col_distance = abs(index % 3 - goal_index % 3)
        total_distance += row_distance + col_distance
    return total_distance

def a_star_search(start_state: State, heuristic: Callable[[State], int]) -> Tuple[List[Node], int]:
    """
    Perform A* search starting from 'start_state' using the given heuristic.
    Returns:
      - solution_path: list of Nodes from start to goal
      - expanded_nodes_count: how many nodes were expanded
    """

    # Initial heuristic and node setup
    initial_heuristic = heuristic(start_state)
    open_list: List[Node] = []
    heapq.heappush(
        open_list,
        Node(
            f=initial_heuristic,   # f = g + h (here g=0 at start)
            state=start_state,
            g=0,
            h=initial_heuristic,
            parent=None,
            move=None
        )
    )

    # Tracks the lowest known cost to reach each visited state
    best_cost_so_far: Dict[State, int] = {start_state: 0}
    expanded_nodes_count = 0

    while open_list:
        # Get the most promising node (lowest f = g + h)
        current_node = heapq.heappop(open_list)
        expanded_nodes_count += 1

        # Goal check
        if current_node.state == GOAL:
            return current_node.path(), expanded_nodes_count

        # Expand neighbors
        for successor_state, moved_tile in get_successor_states(current_node.state):
            new_cost = current_node.g + 1  # each move costs 1

            # Skip if we've already found a cheaper way to reach this state
            if successor_state in best_cost_so_far and new_cost >= best_cost_so_far[successor_state]:
                continue

            # Compute heuristic and f-cost for this successor
            successor_heuristic = heuristic(successor_state)
            successor_f = new_cost + successor_heuristic

            # Create a new node and push it into the priority queue
            successor_node = Node(
                f=successor_f,
                state=successor_state,
                g=new_cost,
                h=successor_heuristic,
                parent=current_node,
                move=moved_tile
            )

            best_cost_so_far[successor_state] = new_cost
            heapq.heappush(open_list, successor_node)

    # If no solution is found (should never happen for solvable puzzles)
    return [], expanded_nodes_count
