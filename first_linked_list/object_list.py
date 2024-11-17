from __future__ import annotations


class ObjList:
    __slots__ = ("__data", "__next", "__prev")

    def __init__(self, data: str):
        self.__data: str = data
        self.__next: ObjList | None = None
        self.__prev: ObjList | None = None

    def get_data(self) -> str:
        return self.__data

    def set_data(self, data: str) -> None:
        self.__data: str = data

    def get_next(self) -> ObjList | None:
        return self.__next

    def set_next(self, obj: ObjList | None) -> None:
        self.__next: ObjList | None = obj

    def get_prev(self) -> ObjList | None:
        return self.__prev

    def set_prev(self, obj: ObjList | None) -> None:
        self.__prev: ObjList | None = obj
