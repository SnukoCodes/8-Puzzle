# puzzle.py
import random
from typing import List, Tuple, Optional

class Puzzle8:
    """3x3 sliding puzzle (0 = blank)."""

    def __init__(self, board: Optional[List[int]] = None):
        """
        If board is None → generate a random solvable board.
        If board is provided → use it (and you can check solvability via is_solvable()).
        """
        if board is None:
            board = self._generate_random_flat()
        if len(board) != 9 or sorted(board) != list(range(9)):
            raise ValueError("Board must contain the numbers 0-8 exactly once.")

        self.board = [board[i:i + 3] for i in range(0, 9, 3)]
        self.legal_moves = self._compute_legal_moves()

    # ---------- public API ----------
    def moves(self) -> List[int]:
        """Return legal moves (tile values that can slide into the blank)."""
        return list(self.legal_moves)

    def move(self, tile: int) -> bool:
        """Slide 'tile' into the blank if legal; update legal moves. Return True if moved."""
        if tile not in self.legal_moves:
            return False
        br, bc = self._find_blank()
        for nr, nc in self._neighbors(br, bc):
            if self.board[nr][nc] == tile:
                self.board[br][bc], self.board[nr][nc] = self.board[nr][nc], self.board[br][bc]
                self.legal_moves = self._compute_legal_moves()
                return True
        return False

    def flatten(self) -> List[int]:
        """Return the board as a flat list (row-major)."""
        return [x for row in self.board for x in row]

    def is_solvable(self) -> bool:
        """Check if the current board is solvable."""
        return self._is_solvable_flat(self.flatten())

    def __str__(self) -> str:
        def cell(v: int) -> str:
            return "·" if v == 0 else f"{v}"
        rows = [" ".join(f"{cell(v):>2}" for v in row) for row in self.board]
        return "\n".join(rows)

    # ---------- internals ----------
    def _generate_random_flat(self) -> List[int]:
        nums = list(range(9))
        while True:
            random.shuffle(nums)
            if self._is_solvable_flat(nums):
                return nums

    def _is_solvable_flat(self, flat: List[int]) -> bool:
        """Solvable test for odd width (3x3): inversion count must be even (ignore 0)."""
        arr = [x for x in flat if x != 0]
        inversions = 0
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                inversions += arr[i] > arr[j]
        return inversions % 2 == 0

    def _find_blank(self) -> Tuple[int, int]:
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == 0:
                    return r, c
        raise RuntimeError("Blank not found")

    def _neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        neigh = []
        if r > 0: neigh.append((r - 1, c))
        if r < 2: neigh.append((r + 1, c))
        if c > 0: neigh.append((r, c - 1))
        if c < 2: neigh.append((r, c + 1))
        return neigh

    def _compute_legal_moves(self) -> List[int]:
        """Tiles adjacent to the blank (these can slide into it)."""
        br, bc = self._find_blank()
        return [self.board[nr][nc] for nr, nc in self._neighbors(br, bc)]
