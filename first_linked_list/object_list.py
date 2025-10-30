"""Implementation of an object within the linked list."""

from typing import Self, Union


class ObjList:
    """Represents a single object within the linked list."""

    __slots__ = "__data", "__next", "__prev"

    def __init__(self, data: str) -> None:
        """Initialize an ObjList object with the given data.

        Args:
            data: The data to store in this object.

        """
        self.__data: str = data
        self.__next: Self | None = None
        self.__prev: Self | None = None

    def get_data(self) -> str:
        """Retrieve the data stored in this object."""
        return self.__data

    def set_data(self, data: str) -> None:
        """Update the data stored in this object."""
        self.__data = data

    def get_next(self) -> Union["Self", None]:
        """Retrieve the next object in the list."""
        return self.__next

    def set_next(self, obj: Union["Self", None]) -> None:
        """Set the next object in the list."""
        self.__next = obj

    def get_prev(self) -> Union["Self", None]:
        """Retrieve the previous object in the list."""
        return self.__prev

    def set_prev(self, obj: Union["Self", None]) -> None:
        """Set the previous object in the list."""
        self.__prev = obj
