"""Define custom exceptions."""

from os import terminal_size


class EmptyLinkedListError(Exception):
    """Raise this exception when a method is called on an empty LinkedList.

    The exception message includes the name of the method that was called.
    """

    def __init__(self, method_name: str) -> None:
        """Initialize the EmptyLinkedListError with the name of the method.

        Args:
            method_name: The name of the LinkedList method that was called.

        """
        super().__init__(
            f'Called method "{method_name}" on an empty LinkedList. '
            "Returning early.",
        )


class TooManyMinesError(Exception):
    """Raise this exception when the number of mines is too high.

    The exception message includes the number of mines and the size of the
    board.
    """

    def __init__(self, num_mines: int, board_size: int) -> None:
        """Initialize the TooManyMinesError with the num of mines, board size.

        Args:
            num_mines: The number of mines that were requested.
            board_size: The size of the board.

        """
        super().__init__(
            f"The number of mines - {num_mines} is too high for the board with"
            f" size of {board_size}x{board_size}. Returning early.",
        )


class TerminalTooSmallError(Exception):
    """Raise this exception when the terminal is too small.

    The exception message includes the size of the terminal and the size of
    the board.
    """

    def __init__(self, terminal: terminal_size, needed_size: tuple) -> None:
        """Initialize the TerminalTooSmallError.

        Args:
            terminal: The size of the terminal.
            needed_size: The needed size.

        """
        super().__init__(
            f"Your terminal is too small to display the game. Minimum size is "
            f"{needed_size[0]}x{needed_size[1]}, but your terminal is "
            f"{terminal.columns}x{terminal.lines}.",
        )


class ServerDisconnectError(Exception):
    """Raise this exception when the server disconnected."""

    def __init__(self) -> None:
        """Initialize the ServerDisconnectError."""
        super().__init__("This server is not connected to a router.")


class WrongServerIPError(Exception):
    """Raise this exception when the server IP is wrong."""

    def __init__(self) -> None:
        """Initialize the WrongServerIPError."""
        super().__init__(
            "Invalid receiver IP address. You can only send messages to "
            "servers with lower IP addresses, and not to itself.",
        )


class WrongTypeError(Exception):
    """Raise this exception when the type is wrong."""

    def __init__(self, instance: tuple) -> None:
        """Initialize the WrongTypeError.

        Args:
            instance: The instance that was expected.

        """
        super().__init__(
            f"The object '{instance[0]}' is an instance of "
            f"'{instance[0].__class__.__name__}', but "
            f"'{instance[1].__name__}' was expected.",
        )
