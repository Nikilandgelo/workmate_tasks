"""Provides utility functions for type checking."""

# needed because list type hint not < 3.9 compatible
from __future__ import annotations

from exceptions import WrongTypeError


def raise_error_if_not_instance(instances_with_classes: list[tuple]) -> None:
    """Raise a TypeError if any instance is not an instance of expected class.

    Args:
        instances_with_classes: A list of tuples, where each tuple contains an
                                instance and its expected class.

    Raises:
        TypeError: If any instance is not an instance of its expected class.

    """
    for instance in instances_with_classes:
        if not isinstance(instance[0], instance[1]):
            raise WrongTypeError(instance)
