"""Database initialization and data management module for trading results.

This module provides functionality to initialize database connections and
manage trading results data in a PostgreSQL database using SQLAlchemy. It
handles async database operations and data insertion from pandas DataFrames.
"""

from os import getenv

from dotenv import load_dotenv
from pandas import DataFrame
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .config import NEEDED_COLUMNS
from .models import Base, SpimexTradingResults


async def init_db_engine() -> async_sessionmaker[AsyncSession]:
    """Initialize the database engine and create all required database tables.

    Loads environment variables for database connection and establishes an
    async connection to PostgreSQL. Creates all defined tables if they
    don't exist.

    Returns:
        async_sessionmaker[AsyncSession]: Session maker for creating new
            database sessions.

    """
    load_dotenv(override=True)
    engine: AsyncEngine = create_async_engine(
        f'postgresql+asyncpg://{getenv("POSTGRES_USER")}:'
        f'{getenv("POSTGRES_PASSWORD")}@{getenv("POSTGRES_HOST")}:'
        f'{getenv("POSTGRES_PORT")}/{getenv("POSTGRES_DB")}',
        echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_sessionmaker(engine)


async def add_new_data(
    session_maker: async_sessionmaker[AsyncSession],
    df: DataFrame,
) -> None:
    """Insert new trading results data from DataFrame into the database.

    Process trading results data from a pandas DataFrame and insert it into
    the database using the provided session maker.

    Args:
        session_maker: Async session maker for database operations
        df: DataFrame containing SPIMEX trading results with columns matching
            the SpimexTradingResults model fields

    Returns:
        None

    """
    trading_results: list = []
    async with session_maker() as session:
        for _, row in df.iterrows():
            result: SpimexTradingResults = SpimexTradingResults(
                exchange_product_id=row[
                    NEEDED_COLUMNS.get("exchange_product_id")
                ],
                exchange_product_name=row[
                    NEEDED_COLUMNS.get("exchange_product_name")
                ],
                oil_id=row[NEEDED_COLUMNS.get("exchange_product_id")][:4],
                delivery_basis_id=row[
                    NEEDED_COLUMNS.get("exchange_product_id")
                ][4:7],
                delivery_basis_name=row[
                    NEEDED_COLUMNS.get("delivery_basis_name")
                ],
                delivery_type_id=row[
                    NEEDED_COLUMNS.get("exchange_product_id")
                ][-1],
                volume=int(row[NEEDED_COLUMNS.get("volume")]),
                total=round(float(row[NEEDED_COLUMNS.get("total")])),
                count=int(row[NEEDED_COLUMNS.get("count")]),
            )
            trading_results.append(result)
    session.add_all(trading_results)
    await session.commit()
