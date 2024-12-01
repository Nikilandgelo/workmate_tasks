"""Module containing tests for adding and retrieving data from the database.

Test module for database operations related to genres, authors, cities,
steps, and books. Utilize pytest and pytest-asyncio for asynchronous
testing.
"""

from os import getenv
from typing import TYPE_CHECKING, TypeVar

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import selectinload

from fourth_db_scheme.enums import StepStatuses
from fourth_db_scheme.models import (
    Author,
    Book,
    Buy,
    BuyBook,
    BuyStep,
    City,
    Client,
    Genre,
    Step,
)
from fourth_db_scheme.sqlalchemy_fix import Base

if TYPE_CHECKING:
    from collections.abc import Sequence

pytestmark = pytest.mark.asyncio
engine: AsyncEngine | None = None

Model = TypeVar(
    "Model",
    Genre,
    Author,
    City,
    Step,
    Book,
    Client,
    Buy,
    BuyBook,
    BuyStep,
)


async def init_db_engine() -> AsyncEngine:
    """Initialize the database engine and create all tables."""
    load_dotenv(override=True)
    global engine  # noqa: PLW0603
    engine = create_async_engine(
        f'postgresql+asyncpg://{getenv("POSTGRES_USER")}:'
        f'{getenv("POSTGRES_PASSWORD")}@{getenv("POSTGRES_HOST")}:'
        f'{getenv("POSTGRES_PORT")}/{getenv("POSTGRES_DB")}',
        echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


async def add_data_in_db(
    session: AsyncSession,
    models: tuple[Model, Model],
) -> tuple[Model, Model]:
    """Add data to the database and return the added records."""
    session.add_all(models)
    await session.flush()
    result: Result = await session.execute(
        select(models[0].__class__),
    )
    got_data: Sequence[Model] = result.scalars().all()
    return got_data[0], got_data[1]


async def refresh_data_from_db(
    session: AsyncSession,
    models_with_related_fields: dict[Model, list[str]],
) -> list[Model]:
    """Refresh data from the database for given models and their fields."""
    models: list[Model] = []
    for model, related_fields in models_with_related_fields.items():
        sql_query = select(model)
        for field in related_fields:
            sql_query = sql_query.options(
                selectinload(getattr(model, field)),
            )
        result: Result = await session.execute(sql_query)
        models.extend(result.scalars().all())
    return models


@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    """Provide a database session for testing."""
    if engine is None:
        await init_db_engine()
    session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    async with session_factory() as session, session.begin():
        yield session
        await session.rollback()
    await engine.dispose()


@pytest.fixture
def genres() -> tuple[Genre, Genre]:
    """Provide sample genres for testing."""
    return Genre(name="Genre 1"), Genre(name="Genre 2")


@pytest.fixture
def authors() -> tuple[Author, Author]:
    """Provide sample authors for testing."""
    return Author(name="Author 1"), Author(name="Author 2")


@pytest.fixture
def cities() -> tuple[City, City]:
    """Provide sample cities for testing."""
    return City(name="City 1", days_delivery=5), City(
        name="City 2",
        days_delivery=10,
    )


@pytest.fixture
def steps() -> tuple[Step, Step]:
    """Provide sample steps for testing."""
    return Step(name=StepStatuses.RECEIVED), Step(
        name=StepStatuses.IN_PROGRESS,
    )


async def test_added_genres(
    db_session: AsyncSession,
    genres: tuple[Genre, Genre],
) -> None:
    """Test adding genres to the database."""
    result: tuple[Genre, Genre] = await add_data_in_db(db_session, genres)
    assert result[0].name == genres[0].name
    assert result[1].name == genres[1].name


async def test_added_authors(
    db_session: AsyncSession,
    authors: tuple[Author, Author],
) -> None:
    """Test adding authors to the database."""
    result: tuple[Author, Author] = await add_data_in_db(db_session, authors)
    assert result[0].name == authors[0].name
    assert result[1].name == authors[1].name


async def test_added_cities(
    db_session: AsyncSession,
    cities: tuple[City, City],
) -> None:
    """Test adding cities to the database."""
    result: tuple[City, City] = await add_data_in_db(db_session, cities)
    assert result[0].name == cities[0].name
    assert result[0].days_delivery == cities[0].days_delivery
    assert result[1].name == cities[1].name
    assert result[1].days_delivery == cities[1].days_delivery


async def test_added_steps(
    db_session: AsyncSession,
    steps: tuple[Genre, Genre],
) -> None:
    """Test adding steps to the database."""
    result: tuple[Step, Step] = await add_data_in_db(db_session, steps)
    assert result[0].name == steps[0].name
    assert result[1].name == steps[1].name


async def test_added_books(
    db_session: AsyncSession,
    authors: tuple[Author, Author],
    genres: tuple[Genre, Genre],
) -> None:
    """Test adding books to the database."""
    all_authors: tuple[Author, Author] = await add_data_in_db(
        db_session,
        authors,
    )
    all_genres: tuple[Genre, Genre] = await add_data_in_db(db_session, genres)
    books: tuple[Book, Book] = (
        Book(
            title="Book 1",
            author_id=all_authors[0].uuid,
            genre_id=all_genres[0].uuid,
            price=10,
            amount=5,
        ),
        Book(
            title="Book 2",
            author_id=all_authors[1].uuid,
            genre_id=all_genres[1].uuid,
            price=20,
            amount=10,
        ),
    )
    result: tuple[Book, Book] = await add_data_in_db(db_session, books)
    updated_related_models: list = await refresh_data_from_db(
        db_session,
        {Author: ["books"], Genre: ["books"]},
    )
    assert result[0].title == books[0].title
    assert result[0].author.name == authors[0].name
    assert updated_related_models[0].books[0].uuid == result[0].uuid
    assert result[0].genre.name == genres[0].name
    assert updated_related_models[2].books[0].uuid == result[0].uuid
    assert result[0].price == books[0].price
    assert result[0].amount == books[0].amount

    assert result[1].title == books[1].title
    assert result[1].author.name == authors[1].name
    assert updated_related_models[1].books[0].uuid == result[1].uuid
    assert result[1].genre.name == genres[1].name
    assert updated_related_models[3].books[0].uuid == result[1].uuid
    assert result[1].price == books[1].price
    assert result[1].amount == books[1].amount


async def test_added_clients(
    db_session: AsyncSession,
    cities: tuple[City, City],
) -> None:
    """Test adding clients to the database."""
    all_cities: tuple[City, City] = await add_data_in_db(db_session, cities)
    clients = (
        Client(
            name="Client 1",
            city_id=all_cities[0].uuid,
            email="client1@email.com",
        ),
        Client(
            name="Client 2",
            city_id=all_cities[1].uuid,
            email="client2@email.com",
        ),
    )
    result: tuple[Client, Client] = await add_data_in_db(db_session, clients)
    updated_related_models: list = await refresh_data_from_db(
        db_session,
        {City: ["clients"]},
    )
    assert result[0].name == clients[0].name
    assert result[0].city.name == cities[0].name
    assert updated_related_models[0].clients[0].uuid == result[0].uuid
    assert result[0].email == clients[0].email

    assert result[1].name == clients[1].name
    assert result[1].city.name == cities[1].name
    assert updated_related_models[1].clients[0].uuid == result[1].uuid
    assert result[1].email == clients[1].email


async def test_added_buys(
    db_session: AsyncSession,
    cities: tuple[City, City],
) -> None:
    """Test adding buys to the database."""
    all_cities: tuple[City, City] = await add_data_in_db(db_session, cities)
    clients: tuple[Client, Client] = (
        Client(
            name="Client 1",
            city_id=all_cities[0].uuid,
            email="client1@email.com",
        ),
        Client(
            name="Client 2",
            city_id=all_cities[1].uuid,
            email="client2@email.com",
        ),
    )
    all_clients: tuple[Client, Client] = await add_data_in_db(
        db_session,
        clients,
    )
    buys: tuple[Buy, Buy] = (
        Buy(buy_description="Buy 1", client_id=all_clients[0].uuid),
        Buy(buy_description="Buy 2", client_id=all_clients[1].uuid),
    )
    result: tuple[Buy, Buy] = await add_data_in_db(db_session, buys)
    updated_related_models: list = await refresh_data_from_db(
        db_session,
        {Client: ["buys"]},
    )
    assert result[0].buy_description == buys[0].buy_description
    assert result[0].client.name == clients[0].name
    assert updated_related_models[0].buys[0].uuid == result[0].uuid

    assert result[1].buy_description == buys[1].buy_description
    assert result[1].client.name == clients[1].name
    assert updated_related_models[1].buys[0].uuid == result[1].uuid


async def test_added_buy_books(
    db_session: AsyncSession,
    cities: tuple[City, City],
    authors: tuple[Author, Author],
    genres: tuple[Genre, Genre],
) -> None:
    """Test adding buy-books relationships to the database."""
    all_cities: tuple[City, City] = await add_data_in_db(db_session, cities)
    clients: tuple[Client, Client] = (
        Client(
            name="Client 1",
            city_id=all_cities[0].uuid,
            email="client1@email.com",
        ),
        Client(
            name="Client 2",
            city_id=all_cities[1].uuid,
            email="client2@email.com",
        ),
    )
    all_clients: tuple[Client, Client] = await add_data_in_db(
        db_session,
        clients,
    )
    buys: tuple[Buy, Buy] = (
        Buy(buy_description="Buy 1", client_id=all_clients[0].uuid),
        Buy(buy_description="Buy 2", client_id=all_clients[1].uuid),
    )
    all_buys: tuple[Buy, Buy] = await add_data_in_db(db_session, buys)

    all_authors: tuple[Author, Author] = await add_data_in_db(
        db_session,
        authors,
    )
    all_genres: tuple[Genre, Genre] = await add_data_in_db(db_session, genres)
    books = (
        Book(
            title="Book 1",
            author_id=all_authors[0].uuid,
            genre_id=all_genres[0].uuid,
            price=10,
            amount=5,
        ),
        Book(
            title="Book 2",
            author_id=all_authors[1].uuid,
            genre_id=all_genres[1].uuid,
            price=20,
            amount=10,
        ),
    )
    all_books: tuple[Book, Book] = await add_data_in_db(db_session, books)

    buy_books: tuple[BuyBook, BuyBook] = (
        BuyBook(buy_id=all_buys[0].uuid, book_id=all_books[0].uuid),
        BuyBook(buy_id=all_buys[1].uuid, book_id=all_books[1].uuid),
    )
    result: tuple[BuyBook, BuyBook] = await add_data_in_db(
        db_session,
        buy_books,
    )
    updated_related_models: list = await refresh_data_from_db(
        db_session,
        {Buy: ["orders"], Book: ["orders"]},
    )
    assert result[0].buy.buy_description == buys[0].buy_description
    assert result[0].book.title == books[0].title
    assert updated_related_models[0].orders[0].uuid == result[0].uuid
    assert updated_related_models[1].orders[0].uuid == result[1].uuid

    assert result[1].buy.buy_description == buys[1].buy_description
    assert result[1].book.title == books[1].title
    assert updated_related_models[2].orders[0].uuid == result[0].uuid
    assert updated_related_models[3].orders[0].uuid == result[1].uuid


async def test_added_buy_steps(
    db_session: AsyncSession,
    cities: tuple[City, City],
    steps: tuple[Step, Step],
) -> None:
    """Test adding buy-steps relationships to the database."""
    all_cities: tuple[City, City] = await add_data_in_db(db_session, cities)
    clients: tuple[Client, Client] = (
        Client(
            name="Client 1",
            city_id=all_cities[0].uuid,
            email="client1@email.com",
        ),
        Client(
            name="Client 2",
            city_id=all_cities[1].uuid,
            email="client2@email.com",
        ),
    )
    all_clients: tuple[Client, Client] = await add_data_in_db(
        db_session,
        clients,
    )
    buys: tuple[Buy, Buy] = (
        Buy(buy_description="Buy 1", client_id=all_clients[0].uuid),
        Buy(buy_description="Buy 2", client_id=all_clients[1].uuid),
    )
    all_buys: tuple[Buy, Buy] = await add_data_in_db(db_session, buys)

    all_steps: tuple[Step, Step] = await add_data_in_db(db_session, steps)
    buy_steps: tuple[BuyStep, BuyStep] = (
        BuyStep(buy_id=all_buys[0].uuid, step_id=all_steps[0].uuid),
        BuyStep(buy_id=all_buys[1].uuid, step_id=all_steps[1].uuid),
    )
    result: tuple[BuyStep, BuyStep] = await add_data_in_db(
        db_session,
        buy_steps,
    )
    updated_related_models: list = await refresh_data_from_db(
        db_session,
        {Buy: ["steps"], Step: ["orders"]},
    )
    assert result[0].buy.buy_description == buys[0].buy_description
    assert result[0].step.name == steps[0].name
    assert updated_related_models[0].steps[0].uuid == result[0].uuid
    assert updated_related_models[2].orders[0].uuid == result[0].uuid

    assert result[1].buy.buy_description == buys[1].buy_description
    assert result[1].step.name == steps[1].name
    assert updated_related_models[1].steps[0].uuid == result[1].uuid
    assert updated_related_models[3].orders[0].uuid == result[1].uuid
