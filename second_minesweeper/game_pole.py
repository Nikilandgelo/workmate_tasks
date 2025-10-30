"""Implements the main game logic for a Minesweeper game."""

import sys
from random import randint
from typing import NoReturn

from colorama import just_fix_windows_console
from termcolor import colored

from exceptions import TooManyMinesError

from .cell import Cell
from .terminal_checker import make_terminal_calc


class GamePole:
    """Represents the game board for Minesweeper."""

    def __init__(self, grid_size: int, num_mines: int) -> None:
        """Initialize the game with the specified size and number of mines.

        Args:
            grid_size: The size of the square grid (e.g., 9 for a 9x9 grid).
            num_mines: The number of mines to place on the grid.

        Raises:
            ValueError: If the number of mines exceeds the total number of\
                cells.

        """
        if num_mines >= grid_size**2:
            raise TooManyMinesError(num_mines, grid_size)
        self.grid_size: int = grid_size
        self.cell_counter: int = grid_size**2 - num_mines
        self.pole = [
            [Cell() for _ in range(grid_size)] for _ in range(grid_size)
        ]
        mine_locations = set()
        while len(mine_locations) < num_mines:
            row: int = randint(0, grid_size - 1)  # noqa: S311
            col: int = randint(0, grid_size - 1)  # noqa: S311
            mine_locations.add((row, col))
        for row, col in mine_locations:
            self.pole[row][col].mine = True
            Cell.increase_neighbors_counters(self.pole, row, col, grid_size)
        (
            self.space_for_lines,
            self.remaining_width,
            self.cell_width,
            self.column_headers,
        ) = make_terminal_calc(grid_size)

    def show(self) -> None:
        """Start the main game loop.

        Displaying the board and handling user input.
        """
        while True:
            self.__display_table()
            print(colored("\nWhat would you like?\n1. Open cell", "cyan"))
            print(colored("2. Exit", "red"))
            user_choice: str = input()
            if user_choice == "1":
                try:
                    row = int(input(colored("Enter row: ", "magenta")))
                    col = int(input(colored("Enter column: ", "magenta")))
                    if not (
                        0 <= row < self.grid_size and 0 <= col < self.grid_size
                    ):
                        print(
                            colored(
                                "Invalid cell coordinates. Try again.",
                                "red",
                            ),
                        )
                        continue
                    cell: Cell = self.pole[row][col]
                    if cell.mine:
                        self.__end_of_game(
                            ("BOOM! Sadly you hit a mine, see you next time."),
                            "red",
                        )
                    cell.fl_open = True
                    self.cell_counter -= 1
                    if self.cell_counter == 0:
                        self.__end_of_game(
                            ("Congratulations! You've won the game!"),
                            "green",
                        )
                except ValueError:
                    print(
                        colored(
                            "Please enter valid numbers for row and column.",
                            "red",
                        ),
                    )
            elif user_choice == "2":
                break
            else:
                print(colored("Invalid choice. Please try again.", "red"))

    def __display_table(self) -> None:
        """Display the game board in the terminal."""
        print()
        trail: str = colored("| ".rjust(self.space_for_lines), "cyan")
        print(trail + colored("COLUMNS".center(self.remaining_width), "cyan"))
        print(trail + colored(self.column_headers, "green"))
        print(
            colored("LINES | ".rjust(self.space_for_lines), "cyan")
            + colored("-" * self.remaining_width, "cyan"),
        )
        for number, row in enumerate(self.pole):
            cells: str = "".join(
                str(cell).ljust(self.cell_width) for cell in row
            )
            cells = colored(cells, "magenta")
            print(
                colored(f"{number} | ".rjust(self.space_for_lines), "green")
                + cells,
            )

    def __end_of_game(self, text: str, color: str) -> NoReturn:
        """Handle the end of the game.

        Revealing all cells and displaying the result.
        """
        print(colored(text, color))
        Cell.reveal_all_cells(self.pole)
        self.__display_table()
        sys.exit()


if __name__ == "__main__":
    just_fix_windows_console()
    pole_game = GamePole(10, 12)
    pole_game.show()
