import sys
import time
from typing import Iterable, Set
from puzzle import Puzzle8
from state import State, GOAL, pretty_print_state
from game import a_star_search, hamming_distance, manhattan_distance

def to_state(iterable: Iterable[int]) -> State:
    vals = tuple(int(x) for x in iterable)
    if len(vals) != 9:
        raise ValueError("State must have exactly 9 integers.")
    return vals  # flat 9-tuple

def _print_solution(path) -> None:
    for i, node in enumerate(path):
        if i == 0:
            print("Start:")
        else:
            print(f"Move {i}: slide {node.move}")
        pretty_print_state(node.state)


def _is_valid_multiset(state: State) -> bool:
    return sorted(state) == list(range(9))

def _generate_unique_start_states(n: int) -> list[State]:
    """Build N unique, solvable (non-goal) start states using Puzzle8()."""
    seen: Set[State] = set()
    out: list[State] = []
    while len(out) < n:
        p = Puzzle8()
        s = to_state(p.flatten())
        if s == GOAL or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def _run_batch(states: list[State]) -> None:
    print(f"Solving {len(states)} random instances...\n")

    total_h_len = total_h_exp = 0
    total_m_len = total_m_exp = 0
    total_h_t = total_m_t = 0.0

    for idx, state in enumerate(states, 1):
        # Hamming
        t0 = time.perf_counter()
        path_h, exp_h = a_star_search(state, hamming_distance)
        t1 = time.perf_counter()

        # Manhattan
        t2 = time.perf_counter()
        path_m, exp_m = a_star_search(state, manhattan_distance)
        t3 = time.perf_counter()

        total_h_len += len(path_h) - 1
        total_h_exp += exp_h
        total_h_t += (t1 - t0)

        total_m_len += len(path_m) - 1
        total_m_exp += exp_m
        total_m_t += (t3 - t2)

        print(f"#{idx:03}: Hamming steps={len(path_h)-1}, expanded={exp_h};  "
              f"Manhattan steps={len(path_m)-1}, expanded={exp_m}")

    n = len(states)
    print("\n=== Averages over", n, "instances ===")
    print(f"Hamming   : avg steps={total_h_len / n:.2f}, "
          f"avg expanded={total_h_exp / n:.1f}, "
          f"avg time={(total_h_t / n) * 1000:.1f} ms")
    print(f"Manhattan : avg steps={total_m_len / n:.2f}, "
          f"avg expanded={total_m_exp / n:.1f}, "
          f"avg time={(total_m_t / n) * 1000:.1f} ms")


def _prompt_custom_state() -> State:
    """Ask the user for a single-line 8-puzzle until it's valid and solvable."""
    print("Enter your 8-puzzle (use 0 for the blank).")
    print("Examples:")
    print("  123456780")
    print("  1 2 3 4 5 6 7 8 0")

    while True:
        line = input("> ").strip()

        # Case 1: contiguous 9 digits
        if len(line) == 9 and line.isdigit():
            raw = [int(ch) for ch in line]

        # Case 2: space or comma separated
        else:
            parts = [p for p in line.replace(",", " ").split() if p]
            if len(parts) != 9 or not all(p.isdigit() for p in parts):
                print("Invalid input. Please enter exactly 9 numbers (0 to 8) either as one block or separated by spaces.")
                continue
            raw = [int(p) for p in parts]

        # Validate that all numbers 0–8 are present
        if sorted(raw) != list(range(9)):
            print("Invalid puzzle. The input must contain each of the numbers 0 to 8 exactly once.")
            continue

        state = tuple(raw)

        # Use Puzzle8 class to check solvability
        from puzzle import Puzzle8
        puzzle = Puzzle8(list(state))
        if not puzzle.is_solvable():
            print("This puzzle is not solvable. Please try again.")
            continue

        return state

def _solve_and_report(state: State) -> None:
    """Solve the given state with both heuristics and print results (or report unsolvable)."""
    print("\nYour puzzle:")
    pretty_print_state(state)

    puzzle = Puzzle8(list(state))
    if not puzzle.is_solvable():
        print("This puzzle is not solvable. Please try again.")
        return

    print("Solvable ✓  Running A* with both heuristics...\n")

    # Hamming
    t0 = time.perf_counter()
    path_h, exp_h = a_star_search(state, hamming_distance)
    t1 = time.perf_counter()

    # Manhattan
    t2 = time.perf_counter()
    path_m, exp_m = a_star_search(state, manhattan_distance)
    t3 = time.perf_counter()

    print("--- Hamming solution ---")
    print(f"Length: {len(path_h)-1} moves, Expanded: {exp_h}, Time: {(t1 - t0)*1000:.1f} ms\n")
    _print_solution(path_h)

    print("--- Manhattan solution ---")
    print(f"Length: {len(path_m)-1} moves, Expanded: {exp_m}, Time: {(t3 - t2)*1000:.1f} ms\n")
    _print_solution(path_m)

#actual orchestration
def run_app() -> None:
    print("8-Puzzle A*")
    print("-----------")
    print("1) Create 100 random puzzles and solve them")
    print("2) Input your own 8-puzzle and solve it (If solvable)")
    while True:
        choice = input("Choose 1 or 2: ").strip()

        if choice == "1":
            starts = _generate_unique_start_states(100)
            # Optional demo of the first (kept for debugging):
            #demo_path, _ = astar(starts[0], manhattan)
            #print("\n--- Demo solve for the first start (Manhattan) ---\n")
            #_print_solution(demo_path)
            _run_batch(starts)
            sys.exit(1)
        elif choice == "2":
            try:
                state = _prompt_custom_state()
                _solve_and_report(state)
                sys.exit(1)
            except Exception as ex:
                print(f"Input error: {ex}")
        else:
            print("Invalid choice. Please choose 1 or 2.")
