"""Represents a server in a local network."""

# needed because list type hint not < 3.9 compatible
from __future__ import annotations

from typing import TYPE_CHECKING

from exceptions import ServerDisconnectError, WrongServerIPError
from utils import raise_error_if_not_instance

from .data import Data

if TYPE_CHECKING:
    from .router import Router


class Server:
    """Represents a server in the local network."""

    server_ip: int = 1

    def __init__(self) -> None:
        """Initialize a Server object with a unique IP address."""
        self.ip: int = self.server_ip
        self.__class__.server_ip += 1
        self.attached_router: Router | None = None
        self.buffer: list[Data] = []

    def get_ip(self) -> int:
        """Return the IP address of the server."""
        return self.ip

    def send_data(self, data: Data) -> None:
        """Send data to another server via the attached router.

        Args:
            data: The Data object to send.

        Raises:
            RuntimeError: If the server is not connected to a router.
            TypeError: If data is not a Data object.
            ValueError: If the destination IP is invalid\
                (same as sender or higher).

        """
        if self.attached_router is None:
            raise ServerDisconnectError
        raise_error_if_not_instance([(data, Data)])
        if self.ip == data.ip or data.ip >= self.server_ip:
            raise WrongServerIPError
        self.attached_router.buffer.append(data)

    def get_data(self) -> list[Data]:
        """Retrieve and clears the server's data buffer.

        Returns:
            A list of Data objects from the buffer.
            The buffer is cleared after this call.

        """
        temp_buffer: list[Data] = self.buffer.copy()
        self.buffer.clear()
        return temp_buffer
