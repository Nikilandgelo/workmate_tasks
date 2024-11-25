"""Implements a network router that manages data transfer between servers."""

from typing import TYPE_CHECKING

from utils import raise_error_if_not_instance

from .server import Server

if TYPE_CHECKING:
    from .data import Data


class Router:
    """Represents a router that manages data transmission between servers."""

    __slots__ = "buffer", "linked_servers"

    def __init__(self) -> None:
        """Initialize a router with an empty buffer and no linked servers."""
        self.buffer: list[Data] = []
        self.linked_servers: dict[str, Server] = {}

    def link(self, server: Server) -> None:
        """Link a server to the router.

        Args:
            server: The server to link.

        Raises:
            TypeError: if server is not an instance of Server.

        """
        raise_error_if_not_instance([(server, Server)])
        server.attached_router = self
        self.linked_servers[server.get_ip()] = server

    def unlink(self, server: Server) -> None:
        """Unlink a server from the router.

        Args:
            server: The server to unlink.

        Raises:
            TypeError: if server is not an instance of Server.

        """
        raise_error_if_not_instance([(server, Server)])
        server.attached_router = None
        self.linked_servers.pop(server.get_ip())

    def send_data(self) -> None:
        """Send all data in the buffer to the appropriate servers."""
        for data in self.buffer:
            server_receiver: Server | None = self.linked_servers.get(data.ip)
            server_receiver.buffer.append(data)
        self.buffer.clear()
