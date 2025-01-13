"""Test excel parser functionality."""

from typing import TYPE_CHECKING

import pytest

from fifth_parser.config import AdditionalColumns
from fifth_parser.excel_parser import parse_excel_file

# Mark all tests in this module as async
pytestmark = [pytest.mark.anyio]


if TYPE_CHECKING:
    from pandas import DataFrame


async def test_parse_excel_file(
    dataframe_setup,
    mock_aiohttp_session,
    excel_mock_date,
):
    """Test parse_excel_file function.

    :param dataframe_setup: Fixture to setup dataframe.
    :param mock_aiohttp_session: Fixture to mock aiohttp session.
    :param excel_mock_date: Mock date for excel file.
    """
    test_rows = [1, 2, 3]
    df, mock_excel_file = dataframe_setup(test_rows)
    mock_aiohttp_session(mock_excel_file)

    result_df: DataFrame = await parse_excel_file(
        "dummy_url",
        excel_mock_date,
    )
    assert len(result_df) == len(test_rows)

    df.loc[:, AdditionalColumns.DATE.value] = excel_mock_date
    assert df.equals(result_df)
    assert all(result_df[AdditionalColumns.DATE.value] == excel_mock_date)


async def test_parse_excel_file_count(
    dataframe_setup,
    mock_aiohttp_session,
    excel_mock_date,
):
    """Test parse_excel_file function with filtering.

    :param dataframe_setup: Fixture to setup dataframe.
    :param mock_aiohttp_session: Fixture to mock aiohttp session.
    :param excel_mock_date: Mock date for excel file.
    """
    test_rows = [0, 0, 1]
    df, mock_excel_file = dataframe_setup(test_rows)
    mock_aiohttp_session(mock_excel_file)

    result_df: DataFrame = await parse_excel_file(
        "dummy_url",
        excel_mock_date,
    )
    filtered_test_rows = list(filter(lambda element: element > 0, test_rows))
    assert len(result_df) == len(filtered_test_rows)
