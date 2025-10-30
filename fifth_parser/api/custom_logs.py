"""Provide custom Redis backend for FastAPI cache with logging capabilities.

Extends the standard RedisBackend to add logging functionality for cache
operations.

Logs all method calls with their arguments for debugging and monitoring
purposes.
"""

import logging
from functools import wraps
from typing import Any

from fastapi_cache.backends.redis import RedisBackend
from termcolor import colored


class LoggingRedisBackend(RedisBackend):
    """Extend RedisBackend with logging capabilities for cache operations.

    Wraps all callable methods to log their execution with arguments using
    colored output.
    Maintains all original RedisBackend functionality while adding logging
    layer.
    """

    def __getattribute__(self, attr_name: str) -> object:
        """Override attribute access to add logging for method calls.

        Args:
            attr_name: Name of the attribute being accessed

        Returns:
            Wrapped method with logging if attribute is callable, original
            attribute otherwise.

        """
        attr_or_method = super().__getattribute__(attr_name)
        if callable(attr_or_method):

            @wraps(attr_or_method)
            async def wrapper(*args: list, **kwargs: dict) -> Any:
                # if level below of WARNING, then it's not working even if with
                # root logger like right now, btw it's essentially to use the
                # root logger, cuz else wise will be some not good formatting
                logging.getLogger().warning(
                    colored("Calling method from cache ", "green")
                    + colored(f'"{attr_or_method.__name__}" ', "blue")
                    + colored("with args:\n", "green")
                    + colored(f"{args}\n", "blue")
                    + colored("and kwargs:\n", "green")
                    + colored(f"{kwargs}", "blue"),
                )
                return await attr_or_method(*args, **kwargs)

            return wrapper
        return attr_or_method
