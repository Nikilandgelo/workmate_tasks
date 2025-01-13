"""Test low-level database functions."""

import secrets

import pytest

from fifth_parser.config import AdditionalColumns
from fifth_parser.db import DBManager
from fifth_parser.models import (
    SpimexTradingResults,
)

pytestmark = [pytest.mark.anyio]


async def test_check_if_data_exists(async_engine, mixer, acceptable_dates):
    """Check if data exists in the database.

    Args:
        async_engine: Async SQLAlchemy engine.
        mixer: pytest-mixer fixture.
        acceptable_dates: Fixture for acceptable dates.

    """
    assert await DBManager(async_engine).check_if_data_exists() is False

    await mixer.async_blend(
        SpimexTradingResults,
        date=secrets.choice(tuple(acceptable_dates())),
    )

    assert await DBManager(async_engine).check_if_data_exists()


async def test_add_new_data_and_get(
    async_engine,
    acceptable_dates,
    dataframe_setup,
):
    """Add new data to the database and retrieve it.

    Args:
        async_engine: Async SQLAlchemy engine.
        acceptable_dates: Fixture for acceptable dates.
        dataframe_setup: Fixture for dataframe setup.

    """
    assert await DBManager(async_engine).check_if_data_exists() is False

    test_rows = [
        "1457843",
        "8894849",
        "2683303",
        "8394849",
        "2679004",
    ]
    df, _ = dataframe_setup(test_rows)
    df.loc[:, AdditionalColumns.DATE.value] = secrets.choice(
        tuple(acceptable_dates()),
    )
    await DBManager(async_engine).add_new_data(df)
    assert await DBManager(async_engine).check_if_data_exists()
    assert len(
        await DBManager(async_engine).get_spimex_trading_results(),
    ) == len(test_rows)
