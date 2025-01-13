"""Pytest conf file providing fixtures for mocking data and sessions.

Contains mock data generators and session setup utilities
for testing the fifth parser functionality.

Fixtures:
    - dataframe_setup: Creates mock Excel files and DataFrames
    - excel_mock_date: Provides a fixed test date
    - mock_aiohttp_session: Sets up mock HTTP client sessions
"""

import logging
from datetime import date
from io import BytesIO
from typing import Callable
from unittest.mock import AsyncMock, MagicMock

import pytest
from pandas import DataFrame
from termcolor import colored

from fifth_parser.config import NeededColumns, get_settings


@pytest.fixture
def dataframe_setup() -> Callable[[list], tuple[DataFrame, BytesIO]]:
    """Create a function that generates mock DataFrame and Excel file.

    Returns:
        Callable: Function that takes a list of values and returns DataFrame
        and BytesIO tuple containing mock data structured according to
        NeededColumns.

    """
    logging.info(
        colored("Setting up dataframe", "magenta"),
    )

    def wrapper(list_of_values: list) -> tuple[DataFrame, BytesIO]:
        """Generate mock DataFrame and Excel file from provided values.

        Args:
            list_of_values (list): Values to populate each column with

        Returns:
            tuple[DataFrame, BytesIO]: Generated DataFrame and Excel file in
            memory

        """
        mock_data = {
            value: list_of_values
            for _, value in NeededColumns.__members__.items()
        }
        mock_excel_file = BytesIO()

        dataframe = DataFrame(mock_data)
        dataframe.to_excel(
            mock_excel_file,
            index=False,
            startrow=get_settings().ROWS_TO_SKIP,
        )
        mock_excel_file.seek(0)
        return dataframe, mock_excel_file

    return wrapper


@pytest.fixture
def excel_mock_date() -> date:
    """Provide a fixed date for testing Excel-related functionality.

    Returns:
        date: Fixed date object set to January 1st, 2024

    """
    return date(2024, 1, 1)


@pytest.fixture
def mock_aiohttp_session(mocker) -> Callable[[BytesIO, str], NotImplemented]:
    """Create a function that sets up mock aiohttp client session for testing.

    Args:
        mocker: Pytest mocker fixture

    Returns:
        Callable: Function to configure mock session with provided file data

    """
    logging.info(
        colored("Setting up mock aiohttp session", "blue"),
    )

    def wrapper(
        bytes_of_file: BytesIO,
        path_to_session: str = "fifth_parser.excel_parser.ClientSession",
    ) -> None:
        """Configure mock aiohttp session with specified file data.

        Args:
            bytes_of_file (BytesIO): File data to be returned by mock session
            path_to_session (str): Import path to mock, defaults to
            ClientSession path

        Returns:
            None

        """
        mock_session: MagicMock = mocker.patch(path_to_session).return_value

        # it's important to keep this order, cuz for example this won't work:
        # mock_session = mock_session.__aenter__.return_value  # noqa: ERA001
        mock_session.__aenter__.return_value = mock_session

        mock_response = mock_session.get.return_value.__aenter__.return_value
        mock_response.read = AsyncMock(return_value=bytes_of_file.getvalue())

    return wrapper
