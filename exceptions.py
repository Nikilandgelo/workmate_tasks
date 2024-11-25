"""Define custom exceptions for LinkedList operations."""


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
