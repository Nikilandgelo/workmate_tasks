"""Define database models for the application."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, relationship

from .enums import StepStatuses
from .sqlalchemy_fix import UuidMixin, default_mapped_column


class Genre(UuidMixin):
    """Represent a genre of books."""

    name: Mapped[str] = default_mapped_column(String(255), unique=True)


class Author(UuidMixin):
    """Represent an author of books."""

    name: Mapped[str] = default_mapped_column(String(255))


class City(UuidMixin):
    """Represent a city where clients reside."""

    name: Mapped[str] = default_mapped_column(String(255), unique=True)
    days_delivery: Mapped[int] = default_mapped_column(Integer())


class Book(UuidMixin):
    """Represent a book with title, author, genre, price, and amount."""

    title: Mapped[str] = default_mapped_column(String(255))
    author_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("author.uuid", ondelete="CASCADE"),
    )
    genre_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("genre.uuid", ondelete="CASCADE"),
    )
    price: Mapped[int] = default_mapped_column(
        Integer(),
        CheckConstraint("price > 0"),
    )
    amount: Mapped[int] = default_mapped_column(
        Integer(),
        CheckConstraint("amount > 0"),
    )

    author: Mapped[Author] = relationship("Author", backref="books")
    genre: Mapped[Genre] = relationship("Genre", backref="books")


class Client(UuidMixin):
    """Represent a client who can buy books."""

    name: Mapped[str] = default_mapped_column(String(255))
    city_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("city.uuid", ondelete="CASCADE"),
    )
    email: Mapped[str] = default_mapped_column(
        String(255),
        CheckConstraint(r"email ~ '^.+@.+\..+$'"),
        unique=True,
    )

    city: Mapped[City] = relationship("City", backref="clients")


class Buy(UuidMixin):
    """Represent a purchase made by a client."""

    buy_description: Mapped[str] = default_mapped_column(Text())
    client_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("client.uuid", ondelete="CASCADE"),
    )

    client: Mapped[Client] = relationship("Client", backref="buys")


class BuyBook(UuidMixin):
    """Represent a book included in a purchase."""

    buy_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("buy.uuid", ondelete="CASCADE"),
    )
    book_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("book.uuid", ondelete="CASCADE"),
    )

    buy: Mapped[Buy] = relationship("Buy", backref="orders")
    book: Mapped[Book] = relationship("Book", backref="orders")


class Step(UuidMixin):
    """Represent a step in the buying process."""

    name: Mapped[StepStatuses] = default_mapped_column(
        Enum(StepStatuses),
        default=StepStatuses.RECEIVED,
    )


class BuyStep(UuidMixin):
    """Represent a step associated with a specific purchase."""

    buy_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("buy.uuid", ondelete="CASCADE"),
    )
    step_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("step.uuid", ondelete="CASCADE"),
    )
    date_step_begin: Mapped[datetime] = default_mapped_column(
        DateTime(),
        default=func.now(),
    )
    date_step_end: Mapped[datetime] = default_mapped_column(
        DateTime(),
        nullable=True,
    )

    buy = relationship("Buy", backref="steps")
    step = relationship("Step", backref="orders")
