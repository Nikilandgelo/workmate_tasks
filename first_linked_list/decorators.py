from functools import wraps
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from linked_list import LinkedList


def non_empty(method):
    """
    Decorator to ensure that a LinkedList method is called only if the list is
    not empty.

    Args:
        method: The LinkedList method to be decorated.
    """

    @wraps(method)
    def wrapper(*args, **kwargs):
        self: LinkedList = args[0]
        if self.tail is None:
            raise ValueError(
                (
                    f'Was called method "{method.__name__}" but '
                    "LinkedList is empty, so we are returning..."
                )
            )
        return method(*args, **kwargs)

    return wrapper
