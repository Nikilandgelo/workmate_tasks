"""Implementation of a singly linked list."""

from utils import raise_error_if_not_instance

from .decorators import non_empty
from .object_list import ObjList


class LinkedList:
    """Represents a singly linked list."""

    __slots__ = "head", "tail"

    def __init__(self) -> None:
        """Initialize an empty LinkedList."""
        self.__set_default_state()

    def __set_default_state(self) -> None:
        """Reset the LinkedList to an empty state."""
        self.head = None
        self.tail = None

    def add_obj(self, obj: ObjList) -> None:
        """Add an object to the end of the linked list.

        Args:
            obj: The object to add. Must be an instance of ObjList.

        Raises:
            TypeError: If obj is not an instance of ObjList.

        """
        raise_error_if_not_instance([(obj, ObjList)])
        if self.head is None:
            self.head: ObjList = obj
        else:
            obj.set_prev(self.tail)
            self.tail.set_next(obj)
        self.tail: ObjList = obj

    @non_empty
    def remove_obj(self) -> None:
        """Remove the last object from the linked list.

        If the list has only one object, reset it to the empty state.
        Otherwise, update the tail and adjust the previous object's next
        pointer.
        """
        prev_obj: ObjList | None = self.tail.get_prev()
        if prev_obj is None:
            self.__set_default_state()
        else:
            prev_obj.set_next(None)
            self.tail = prev_obj

    @non_empty
    def get_data(self) -> list:
        """Retrieve all data from the linked list as a list.

        Traverse the list, collecting data from each ObjList object.

        Returns:
            A list containing the data from all ObjList objects.

        """
        all_data: list = []
        current_obj: ObjList = self.head
        while current_obj is not None:
            all_data.append(current_obj.get_data())
            current_obj = current_obj.get_next()
        return all_data
