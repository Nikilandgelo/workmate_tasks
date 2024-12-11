"""Handle SQLAlchemy models with UUID support and automatic table naming.

This module provides a custom metaclass for automatic table naming and a mixin
for adding UUID primary keys to SQLAlchemy models.
"""

from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Uuid
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column


class AutoTableName(DeclarativeMeta):
    """Automatically set the __tablename__ attribute to the lowercase.

    Define a new class with automatic table naming based on the class name.
    """

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> type:
        """Set the __tablename__ attribute to the lowercase from class name.

        Args:
            name (str): The name of the class.
            bases (tuple): The base classes of the class.
            attrs (dict): The attributes of the class.

        Returns:
            type: The class with the __tablename__ attribute set.

        """
        if "__tablename__" not in attrs:
            attrs["__tablename__"] = name.lower()
        return super().__new__(cls, name, bases, attrs)


Base = declarative_base(metaclass=AutoTableName)


class UuidMixin(Base):
    """Mixin class to add a UUID primary key to SQLAlchemy models.

    This class serves as an abstract base class that adds a UUID column
    as the primary key for any SQLAlchemy model that inherits from it.

    Attributes:
        uuid (Mapped[UUID]): The UUID primary key for the model.

    """

    __abstract__ = True
    uuid: Mapped[UUID] = mapped_column(Uuid(), default=uuid4, primary_key=True)


def default_mapped_column(*args: Any, **kwargs: Any) -> MappedColumn:
    """Create a mapped column with nullable set to False by default.

    Set the 'nullable' attribute of the column to False unless specified
    otherwise.

    Args:
        *args: Positional arguments for the mapped_column.
        **kwargs: Keyword arguments for the mapped_column.

    Returns:
        MappedColumn: The configured mapped column.

    """
    kwargs.setdefault("nullable", False)
    return mapped_column(*args, **kwargs)
