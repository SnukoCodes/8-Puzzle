from typing import Tuple

State = Tuple[int, ...]  # flat 9-tuple, row-major, 0 = blank

GOAL: State = (1, 2, 3,
               4, 5, 6,
               7, 8, 0)

def pretty_print_state(s: State) -> None:
    print(f"{s[0]} {s[1]} {s[2]}\n{s[3]} {s[4]} {s[5]}\n{s[6]} {s[7]} {s[8]}\n")
