from utils import raise_error_if_not_instance


class Data:
    __slots__ = ("data", "ip")

    def __init__(self, data: str, ip: int):
        raise_error_if_not_instance([(data, str), (ip, int)])
        self.data: str = data
        self.ip: int = ip
