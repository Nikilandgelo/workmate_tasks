from .data import Data
from utils import raise_error_if_not_instance
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from router import Router


class Server:
    server_ip: int = 1

    def __init__(self) -> None:
        self.ip: int = self.server_ip
        self.__class__.server_ip += 1
        self.attached_router: Router | None = None
        self.buffer: list[Data] = []

    def get_ip(self) -> int:
        return self.ip

    def send_data(self, data: Data) -> None:
        if self.attached_router is None:
            raise RuntimeError("Server is not connected to any router.")
        raise_error_if_not_instance([(data, Data)])
        if self.ip == data.ip or data.ip >= self.server_ip:
            raise ValueError(
                (
                    "Invalid receiver IP address. Messages can only be sent to "
                    "servers with lower IP addresses and not to itself."
                )
            )
        self.attached_router.buffer.append(data)

    def get_data(self) -> list:
        temp_buffer: list = self.buffer.copy()
        self.buffer.clear()
        return temp_buffer
