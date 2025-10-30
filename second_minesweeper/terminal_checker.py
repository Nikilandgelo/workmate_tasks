"""Checks terminal size and calculates layout parameters for the game."""

# needed because tuple type hint not < 3.9 compatible
from __future__ import annotations

from os import get_terminal_size, terminal_size

from exceptions import TerminalTooSmallError


def make_terminal_calc(grid_size: int) -> tuple[int, int, int, str]:
    """Calculate the terminal layout parameters for the Minesweeper game.

    Args:
        grid_size: The size of the game grid.

    Returns:
        A tuple containing: space_for_lines, remaining_width, cell_width,
        column_headers.

    Raises:
        ValueError: If the terminal size is too small to display the game.

    """
    terminal: terminal_size = get_terminal_size()

    # 8 minimum width because "LINES | " equal 8 characters,
    # 8 minimum height because 3 lines above of main field and 5 below
    min_width: int = 8 + (grid_size * 2)
    min_height: int = 8 + grid_size
    if terminal.columns < min_width or terminal.lines < min_height:
        raise TerminalTooSmallError(terminal, (min_width, min_height))
    space_for_lines: int = max(terminal.columns // 10, 8)
    remaining_width: int = terminal.columns - space_for_lines
    cell_width: int = remaining_width // grid_size
    column_headers: str = "".join(
        str(i).ljust(cell_width) for i in range(grid_size)
    )
    return space_for_lines, remaining_width, cell_width, column_headers
