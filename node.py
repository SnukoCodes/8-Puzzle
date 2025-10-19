from dataclasses import dataclass, field
from typing import Optional
from state import State

@dataclass(order=True)
class Node:
    # order=True so heapq can order by 'f' first
    # f = g+h
    f: int
    state: State = field(compare=False)
    #cost so far
    g: int = field(compare=False, default=0)
    #estimated heuristic cost
    h: int = field(compare=False, default=0)
    parent: Optional["Node"] = field(compare=False, default=None)
    move: Optional[int] = field(compare=False, default=None)  # the tile moved to reach this node

    def path(self) -> list["Node"]:
        """Return nodes from root to self."""
        n, out = self, []
        while n:
            out.append(n)
            n = n.parent
        return list(reversed(out))
