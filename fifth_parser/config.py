"""Define configuration settings for parsing trade results.

Specify constants for start date, domain, start URL, and column mappings.
Ensure correct handling of trade data from Excel files.
"""

from datetime import UTC, datetime

START_DATE: datetime = datetime(2023, 1, 1, tzinfo=UTC)
DOMAIN: str = "https://spimex.com"
START_URL: str = f"{DOMAIN}/markets/oil_products/trades/results/"
# ruff: noqa: RUF001
COLUMNS_FROM_EXCEL: list[str] = [
    "Код Инструмента",
    "Наименование Инструмента",
    "Базис поставки",
    "Объем Договоров в единицах измерения",
    "Обьем Договоров, руб.",
    "Количество Договоров, шт.",
]
NEEDED_COLUMNS: dict[str, str] = {
    "exchange_product_id": COLUMNS_FROM_EXCEL[0],
    "exchange_product_name": COLUMNS_FROM_EXCEL[1],
    "delivery_basis_name": COLUMNS_FROM_EXCEL[2],
    "volume": COLUMNS_FROM_EXCEL[3],
    "total": COLUMNS_FROM_EXCEL[4],
    "count": COLUMNS_FROM_EXCEL[5],
}
