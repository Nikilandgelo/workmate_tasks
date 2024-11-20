from __future__ import annotations


class Cell:
    __slots__ = ("around_mines", "mine", "fl_open")

    def __init__(self, around_mines: int = 0, mine: bool = False) -> None:
        self.around_mines: int = around_mines
        self.mine: bool = mine
        self.fl_open = False

    @staticmethod
    def reveal_all_cells(pole: list[list[Cell]]) -> None:
        for row in pole:
            for cell in row:
                cell.fl_open = True

    @staticmethod
    def increase_neighbors_counters(
        pole: list[list[Cell]],
        current_row: int,
        current_column: int,
        grid_size: int,
    ) -> None:
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
            row, column = current_row + row, current_column + column
            if 0 <= row < grid_size and 0 <= column < grid_size:
                pole[row][column].around_mines += 1

    def __str__(self) -> str:
        if not self.fl_open:
            return "#"
        if self.mine:
            return "*"
        return f"{self.around_mines}" if self.around_mines else " "
