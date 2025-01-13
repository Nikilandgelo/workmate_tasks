"""Configure pytest fixtures for Fifth Parser application testing environment.

Provides fixtures for:
    - Database connection and session management
    - Redis cache initialization and cleanup
    - HTTP client setup
    - Test data generation through mixer
    - Date utilities for testing
"""

import logging
from collections.abc import Generator
from datetime import date, timedelta
from functools import lru_cache
from typing import Callable

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.sql import text
from starlette.types import ASGIApp
from termcolor import colored

from fifth_parser.api.app import app
from fifth_parser.config import get_db_url, get_redis_url
from fifth_parser.models import Base
from fifth_parser.tests.async_mixer import AsyncMixer


@pytest.fixture(scope="session")
def async_engine() -> AsyncEngine:
    """Create SQLAlchemy async engine instance for test database.

    Returns:
        AsyncEngine: Configured SQLAlchemy async engine instance.

    """
    logging.info(
        colored(
            f"Creating async engine from this test db url: {get_db_url()}",
            "blue",
        ),
    )
    return create_async_engine(get_db_url())


@pytest.fixture(scope="session")
def redis_engine() -> Redis:
    """Create Redis engine instance for test cache.

    Returns:
        Redis: Configured Redis client instance.

    """
    logging.info(
        colored(
            f"Creating redis engine from this redis url: {get_redis_url()}",
            "blue",
        ),
    )
    return Redis.from_url(get_redis_url())


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Set up AnyIO backend for async testing.

    Returns:
        str: Name of the async backend to use ('asyncio').

    """
    logging.info(
        colored("Creating custom anyio backend with session scope", "magenta"),
    )
    return "asyncio"


@pytest.fixture(scope="session")
async def async_app(anyio_backend: str) -> ASGIApp:
    """Create ASGI application instance with lifespan support.

    Returns:
        ASGIApp: Application instance wrapped in lifespan manager.

    """
    logging.info(
        colored("Creating async app with support for lifespan", "light_cyan"),
    )
    async with LifespanManager(app) as manager:
        yield manager.app


@pytest.fixture
async def client(
    anyio_backend: str,
    async_app: ASGIApp,
    redis_engine: Redis,
) -> AsyncClient:
    """Create HTTP test client for making requests to the application.

    Args:
        anyio_backend: AnyIO backend configuration.
        async_app: ASGI application instance.
        redis_engine: Redis client for cache management.

    Returns:
        AsyncClient: Configured HTTP test client.

    """
    logging.info(colored("Getting test client", "light_cyan"))
    async with AsyncClient(
        transport=ASGITransport(app=async_app),
        base_url="http://localhost:8000",
    ) as test_client:
        yield test_client
    logging.info(
        colored("Clearing redis cache after reaching endpoints", "yellow"),
    )
    await redis_engine.flushdb()


@pytest.fixture
async def session(
    anyio_backend: str,
    async_engine: AsyncEngine,
) -> AsyncSession:
    """Create database session for test operations.

    Args:
        anyio_backend: AnyIO backend configuration.
        async_engine: SQLAlchemy async engine instance.

    Returns:
        Generator[AsyncSession]: Active database session.

    """
    logging.info(colored("Getting async session", "light_cyan"))
    session_maker = async_sessionmaker(async_engine)
    async with session_maker() as session:
        yield session


@pytest.fixture
async def mixer(
    anyio_backend: str,
    session: AsyncSession,
) -> AsyncMixer:
    """Create async mixer instance for generating test data.

    Args:
        anyio_backend: AnyIO backend configuration.
        session: Active database session.

    Returns:
        AsyncMixer: Configured mixer instance for data generation.

    """
    logging.info(colored("Getting async mixer", "light_cyan"))
    async_mixer = AsyncMixer(session=session)
    yield async_mixer
    for model_name in async_mixer.created_models:
        logging.info(
            colored(f"Truncating table {model_name}", "yellow"),
        )
        await session.execute(
            text(f"TRUNCATE {model_name}"),
        )
        await session.commit()


@pytest.fixture
@lru_cache
def acceptable_dates() -> Callable[[int], Generator[date]]:
    """Create and return function for generation testing dates from some range.

    Returns:
        Callable[[int], Generator[date]]: Function that yields dates from today
            backwards.

    """

    def return_acceptable_dates(days: int = 30) -> Generator[date]:
        """Generate sequence of dates for testing purposes.

        Args:
            days: Number of days to generate dates for (default: 30).

        """
        end_date = date.today() - timedelta(days=days)
        current_date = date.today()
        while current_date > end_date:
            yield current_date
            current_date -= timedelta(days=1)

    return return_acceptable_dates


@pytest.fixture(scope="session", autouse=True)
async def init_db(anyio_backend: str, async_engine: AsyncEngine) -> Generator:
    """Initialize test database schema and clean up after tests.

    Args:
        anyio_backend: AnyIO backend configuration.
        async_engine: SQLAlchemy async engine instance.

    """
    connection: AsyncConnection
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        logging.info(colored("Database models initialized", "blue"))
    yield
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        logging.info(colored("Database models dropped", "blue"))


@pytest.fixture(scope="session", autouse=True)
async def clear_cache(anyio_backend: str, redis_engine: Redis) -> None:
    """Clear Redis cache before test session starts.

    Args:
        anyio_backend: AnyIO backend configuration.
        redis_engine: Redis client instance.

    """
    result: bool = await redis_engine.flushdb()
    logging.info(
        colored(
            "Clear cache on startup in case if something was there and "
            "check that it's successful",
            "light_cyan",
        ),
    )
    assert result
