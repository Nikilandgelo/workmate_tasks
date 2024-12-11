"""Define configuration settings for parsing trade results.

Specify constants for start date, domain, start URL, and column mappings.
Ensure correct handling of trade data from Excel files.
"""

from datetime import UTC, datetime
from enum import StrEnum

START_DATE: datetime = datetime(2023, 1, 1, tzinfo=UTC)
DOMAIN: str = "https://spimex.com"
START_URL: str = f"{DOMAIN}/markets/oil_products/trades/results/"


# ruff: noqa: RUF001
class NeededColumns(StrEnum):
    """Columns needed for the trade data."""

    EXCHANGE_PRODUCT_ID = "Код Инструмента"
    EXCHANGE_PRODUCT_NAME = "Наименование Инструмента"
    DELIVERY_BASIS_NAME = "Базис поставки"
    VOLUME = "Объем Договоров в единицах измерения"
    TOTAL = "Обьем Договоров, руб."
    COUNT = "Количество Договоров, шт."
