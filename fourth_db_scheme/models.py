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

    name: Mapped[str] = default_mapped_column(
        String(255),
        unique=True,
        comment="The name of the genre.",
    )


class Author(UuidMixin):
    """Represent an author of books."""

    name: Mapped[str] = default_mapped_column(
        String(255),
        comment="The name of the author.",
    )


class City(UuidMixin):
    """Represent a city where clients reside."""

    name: Mapped[str] = default_mapped_column(
        String(255),
        unique=True,
        comment="The name of the city.",
    )
    days_delivery: Mapped[int] = default_mapped_column(
        Integer(),
        comment="The number of days to deliver books to a city.",
    )


class Book(UuidMixin):
    """Represent a book with title, author, genre, price, and amount."""

    title: Mapped[str] = default_mapped_column(
        String(255),
        comment="The title of the book.",
    )
    author_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("author.uuid", ondelete="CASCADE"),
        comment="The author of the book.",
    )
    genre_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("genre.uuid", ondelete="CASCADE"),
        comment="The genre of the book.",
    )
    price: Mapped[int] = default_mapped_column(
        Integer(),
        CheckConstraint("price > 0"),
        comment="The price of the book.",
    )
    amount: Mapped[int] = default_mapped_column(
        Integer(),
        CheckConstraint("amount > 0"),
        comment="The amount of books in the order.",
    )
    author: Mapped[Author] = relationship("Author", backref="books")
    genre: Mapped[Genre] = relationship("Genre", backref="books")


class Client(UuidMixin):
    """Represent a client who can buy books."""

    name: Mapped[str] = default_mapped_column(
        String(255),
        comment="The name of the client.",
    )
    city_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("city.uuid", ondelete="CASCADE"),
        comment="The city of the client.",
    )
    email: Mapped[str] = default_mapped_column(
        String(255),
        CheckConstraint(r"email ~ '^.+@.+\..+$'"),
        unique=True,
        comment="The email of the client.",
    )
    city: Mapped[City] = relationship("City", backref="clients")


class Buy(UuidMixin):
    """Represent a purchase made by a client."""

    buy_description: Mapped[str] = default_mapped_column(
        Text(),
        comment="The description of the purchase.",
    )
    client_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("client.uuid", ondelete="CASCADE"),
        comment="The client who made the purchase.",
    )
    client: Mapped[Client] = relationship("Client", backref="buys")


class BuyBook(UuidMixin):
    """Represent a book included in a purchase."""

    buy_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("buy.uuid", ondelete="CASCADE"),
        comment="The purchase that includes the book.",
    )
    book_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("book.uuid", ondelete="CASCADE"),
        comment="The book included in the purchase.",
    )
    buy: Mapped[Buy] = relationship("Buy", backref="orders")
    book: Mapped[Book] = relationship("Book", backref="orders")


class Step(UuidMixin):
    """Represent a step in the buying process."""

    name: Mapped[StepStatuses] = default_mapped_column(
        Enum(StepStatuses),
        default=StepStatuses.RECEIVED,
        comment="The status of the step.",
    )


class BuyStep(UuidMixin):
    """Represent a step associated with a specific purchase."""

    buy_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("buy.uuid", ondelete="CASCADE"),
        comment="The purchase associated with the step.",
    )
    step_id: Mapped[UUID] = default_mapped_column(
        ForeignKey("step.uuid", ondelete="CASCADE"),
        comment="The step associated with the purchase.",
    )
    date_step_begin: Mapped[datetime] = default_mapped_column(
        DateTime(),
        default=func.now(),
        comment="The date the step began.",
    )
    date_step_end: Mapped[datetime] = default_mapped_column(
        DateTime(),
        nullable=True,
        comment="The date the step ended.",
    )
    buy = relationship("Buy", backref="steps")
    step = relationship("Step", backref="orders")
