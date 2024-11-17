from os import get_terminal_size, terminal_size


def make_terminal_calc(grid_size: int):
    terminal: terminal_size = get_terminal_size()

    # 8 minimum width because "LINES | " equal 8 characters,
    # 8 minimum height because 3 lines above of main field and 5 below
    min_width: int = 8 + (grid_size * 2)
    min_height: int = 8 + grid_size
    if terminal.columns < min_width or terminal.lines < min_height:
        raise ValueError(
            f"Terminal size is too small. Minimum size is "
            f"{min_width}x{min_height}, your size is "
            f"{terminal.columns}x{terminal.lines}."
        )
    space_for_lines: int = max(terminal.columns // 10, 8)
    remaining_width: int = terminal.columns - space_for_lines
    cell_width: int = remaining_width // grid_size
    column_headers: str = "".join(str(i).ljust(cell_width) for i in range(grid_size))
    return space_for_lines, remaining_width, cell_width, column_headers
