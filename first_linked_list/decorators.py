"""Decorators for LinkedList methods."""

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable

from exceptions import EmptyLinkedListError

if TYPE_CHECKING:
    from linked_list import LinkedList


def non_empty(method: Callable[..., Any]) -> Callable[..., Any]:
    """Ensure that a LinkedList method is called only if the list is not empty.

    Args:
        method: The LinkedList method to be decorated.

    Raises:
        ValueError: If the LinkedList is empty.

    Returns:
        The decorated method.

    """

    @wraps(method)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrap the decorated method."""
        self: LinkedList = args[0]
        if self.tail is None:
            raise EmptyLinkedListError(method.__name__)
        return method(*args, **kwargs)

    return wrapper
