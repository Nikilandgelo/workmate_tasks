from .server import Server
from .data import Data
from utils import raise_error_if_not_instance


class Router:
    __slots__ = ("buffer", "linked_servers")

    def __init__(self) -> None:
        self.buffer: list[Data] = []
        self.linked_servers: dict = {}

    def link(self, server: Server):
        raise_error_if_not_instance([(server, Server)])
        server.attached_router = self
        self.linked_servers[server.get_ip()] = server

    def unlink(self, server: Server):
        raise_error_if_not_instance([(server, Server)])
        server.attached_router = None
        self.linked_servers.pop(server.get_ip())

    def send_data(self):
        for data in self.buffer:
            server_receiver: Server = self.linked_servers.get(data.ip)
            server_receiver.buffer.append(data)
        self.buffer.clear()
