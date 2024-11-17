from object_list import ObjList
from decorators import non_empty


class LinkedList:
    __slots__ = ("head", "tail")

    def __init__(self):
        self.__set_default_state()

    def __set_default_state(self):
        self.head = None
        self.tail = None

    def add_obj(self, obj: ObjList):
        """Adds an object to the end of the linked list.

        Args:
            obj: The object to add.  Must be an instance of ObjList.

        Raises:
            TypeError: If obj is not an instance of ObjList.
        """
        if not isinstance(obj, ObjList):
            raise TypeError("Passing object must be ObjList instance")
        if self.head is None:
            self.head: ObjList = obj
        else:
            obj.set_prev(self.tail)
            self.tail.set_next(obj)
        self.tail: ObjList = obj

    @non_empty
    def remove_obj(self):
        """Removes the last object from the linked list.

        If the linked list contain only one object, it sets linked list to the
        initial state - head and tail are None. Otherwise, it updates the
        tail to point to the previous object, and sets the next pointer of
        the previous object to None.
        """
        prev_obj: ObjList | None = self.tail.get_prev()
        if prev_obj is None:
            self.__set_default_state()
        else:
            prev_obj.set_next(None)
            self.tail = prev_obj

    @non_empty
    def get_data(self) -> list:
        """Retrieves all data from the linked list as a list.

        Traverses the linked list from head to tail, collecting the data
        from each ObjList object into a list which is then returned.

        Returns:
            A list containing the data from each ObjList object in the linked
            list.
        """
        all_data: list = []
        current_obj: ObjList = self.head
        while current_obj is not None:
            all_data.append(current_obj.get_data())
            current_obj = current_obj.get_next()
        return all_data
