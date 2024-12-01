"""SQLAlchemy models for the SPIMEX trading results parser.

This module defines the SQLAlchemy ORM models used to store and manage SPIMEX
trading results data. It includes the base declarative class, a UUID mixin for
primary keys, and the main trading results model.

Classes:
    Base: The SQLAlchemy declarative base class.
    UuidMixin: Mixin class providing UUID primary key functionality.
    SpimexTradingResults: Model for storing SPIMEX trading data.
"""

from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, Integer, String, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from fourth_db_scheme.sqlalchemy_fix import default_mapped_column


class Base(DeclarativeBase):
    """Declare the base class for SQLAlchemy declarative models.

    This class serves as the foundation for all SQLAlchemy models in the
    application, providing core functionality for ORM operations.
    """


class UuidMixin(Base):
    """Mixin class to add a UUID primary key to SQLAlchemy models.

    This class serves as an abstract base class that adds a UUID column
    as the primary key for any SQLAlchemy model that inherits from it.

    Attributes:
        uuid (Mapped[UUID]): The UUID primary key for the model.

    """

    __abstract__ = True
    uuid: Mapped[UUID] = mapped_column(Uuid(), default=uuid4, primary_key=True)


class SpimexTradingResults(UuidMixin):
    """Store SPIMEX trading results data.

    This model represents daily trading results from the SPIMEX exchange,
    including product details, delivery information, and trading statistics.

    Attributes:
        uuid (UUID): Primary key, automatically generated UUID.
        exchange_product_id (str): Unique identifier for the exchange product.
        exchange_product_name (str): Full name of the exchange product.
        oil_id (str): 4-character identifier for the oil type.
        delivery_basis_id (str): 3-character code for delivery basis.
        delivery_basis_name (str): Full name of the delivery basis location.
        delivery_type_id (str): Single character identifying delivery type.
        volume (int): Total trading volume for the product.
        total (int): Total monetary value of trades.
        count (int): Number of trades executed.
        date (Date): Trading date, defaults to current date.
        created_on (DateTime): Record creation timestamp, auto-set to now.
        updated_on (DateTime): Last update timestamp, auto-set to now.

    Table:
        spimex_trading_results: Stores daily SPIMEX trading data.

    Note:
        All string fields use a maximum length of 255 characters except for
        oil_id (4 chars), delivery_basis_id (3 chars), and delivery_type_id
        (1 char).

    """

    __tablename__ = "spimex_trading_results"

    exchange_product_id: Mapped[str] = default_mapped_column(String(255))
    exchange_product_name: Mapped[str] = default_mapped_column(String(255))
    oil_id: Mapped[str] = default_mapped_column(String(4))
    delivery_basis_id: Mapped[str] = default_mapped_column(String(3))
    delivery_basis_name: Mapped[str] = default_mapped_column(String(255))
    delivery_type_id: Mapped[str] = default_mapped_column(String(1))
    volume: Mapped[int] = default_mapped_column(Integer())
    total: Mapped[int] = default_mapped_column(Integer())
    count: Mapped[int] = default_mapped_column(Integer())
    date: Mapped[Date] = default_mapped_column(
        Date(),
        default=func.current_date(),
    )
    created_on: Mapped[DateTime] = default_mapped_column(
        DateTime(),
        default=func.now(),
    )
    updated_on: Mapped[DateTime] = default_mapped_column(
        DateTime(),
        default=func.now(),
    )
