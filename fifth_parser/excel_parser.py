"""Excel file parser module for processing trade data from remote Excel files.

This module provides functionality to download, parse and filter Excel files
containing trade data. It handles data cleaning, column filtering, and numeric
validation.
"""

from datetime import date
from io import BytesIO
from re import fullmatch

from aiohttp import ClientSession
from pandas import DataFrame, read_excel

from .config import AdditionalColumns, NeededColumns, get_settings


async def parse_excel_file(link: str, trade_date: date) -> DataFrame:
    """Download and parse Excel file from given URL, and filter trade data.

    Args:
        link: URL string pointing to the Excel file location.
        trade_date: Date object representing the date of the Excel file.

    Returns:
        DataFrame containing filtered and cleaned trade data with required
        columns. Only rows with positive number of contracts are included.

    Notes:
        - Skips first 6 rows of the Excel file
        - Cleans column names by removing newlines and extra spaces
        - Filters out rows with missing values in required columns
        - Converts contract quantities to integers, invalid values become 0
        - Keeps only rows where contract quantity is greater than 0

    """
    async with ClientSession() as session, session.get(link) as response:
        file_object: BytesIO = BytesIO(await response.read())
        all_values: list[str] = [
            xls_column_name
            for _, xls_column_name in NeededColumns.__members__.items()
        ]

        df: DataFrame = read_excel(
            file_object,
            skiprows=get_settings().ROWS_TO_SKIP,
        )
        df.columns = [col.replace("\n", " ").strip() for col in df.columns]
        df: DataFrame = df[all_values]
        df: DataFrame = df.dropna(subset=all_values, how="any")
        df[NeededColumns.COUNT.value] = df[NeededColumns.COUNT.value].apply(
            lambda x: int(x) if fullmatch(r"[0-9]+", str(x)) else 0,
        )
        filtered_df: DataFrame = df[df[NeededColumns.COUNT.value] > 0].copy()
        filtered_df.loc[:, AdditionalColumns.DATE.value] = trade_date
        return filtered_df
