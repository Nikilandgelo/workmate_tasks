"""Represents a data packet in the network."""

from utils import raise_error_if_not_instance


class Data:
    """Represents a data packet with its content and destination IP."""

    __slots__ = "data", "ip"

    def __init__(self, data: str, ip: int) -> None:
        """Initialize a Data object.

        Args:
            data: The data payload as a string.
            ip: The destination IP address as an integer.

        Raises:
            TypeError: if data is not a string or ip is not an integer.

        """
        raise_error_if_not_instance([(data, str), (ip, int)])
        self.data: str = data
        self.ip: int = ip
