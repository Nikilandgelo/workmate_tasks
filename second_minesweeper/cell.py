"""Represents a single cell in a Minesweeper game."""

# without it linters would complain on Self in classmethod`s
from __future__ import annotations

from typing import Self


class Cell:
    """Represents a cell in the Minesweeper grid."""

    __slots__ = "around_mines", "mine", "fl_open"

    def __init__(self, *, around_mines: int = 0, mine: bool = False) -> None:
        """Initialize a Cell object.

        Args:
            around_mines: The number of mines adjacent to this cell.\
            Defaults to 0.
            mine: True if this cell contains a mine, False otherwise.\
            Defaults to False.

        """
        self.around_mines: int = around_mines
        self.mine: bool = mine
        self.fl_open: bool = False

    @classmethod
    def reveal_all_cells(cls, pole: list[list[Self]]) -> None:
        """Reveals all cells in the given grid.

        Args:
            pole: The Minesweeper grid represented as a list of lists of Cell\
                objects.

        """
        for row in pole:
            for cell in row:
                cell.fl_open = True

    @classmethod
    def increase_neighbors_counters(
        cls,
        pole: list[list[Self]],
        current_row: int,
        current_column: int,
        grid_size: int,
    ) -> None:
        """Increment the around_mines counter for cells adjacent to a mine.

        Args:
            pole: The Minesweeper grid.
            current_row: The row index of the mine.
            current_column: The column index of the mine.
            grid_size: The size of the grid.

        """
        adjacent_coords = (
            (-1, 0),
            (-1, -1),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, 0),
            (1, -1),
            (1, 1),
        )
        for row, column in adjacent_coords:
            adj_row, adj_column = current_row + row, current_column + column
            if 0 <= adj_row < grid_size and 0 <= adj_column < grid_size:
                pole[adj_row][adj_column].around_mines += 1

    def __str__(self) -> str:
        """Return a string representation of the cell."""
        if not self.fl_open:
            return "#"
        if self.mine:
            return "*"
        return f"{self.around_mines}" if self.around_mines else " "
