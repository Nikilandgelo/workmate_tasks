"""Configure application settings and database connection."""

from datetime import date
from enum import StrEnum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


# ruff: noqa: RUF001
class NeededColumns(StrEnum):
    """Define columns needed for the trade data.

    Attributes:
        EXCHANGE_PRODUCT_ID: Exchange product ID column name.
        EXCHANGE_PRODUCT_NAME: Exchange product name column name.
        DELIVERY_BASIS_NAME: Delivery basis name column name.
        VOLUME: Volume of contracts column name.
        TOTAL: Total volume of contracts column name.
        COUNT: Count of contracts column name.

    """

    EXCHANGE_PRODUCT_ID = "Код Инструмента"
    EXCHANGE_PRODUCT_NAME = "Наименование Инструмента"
    DELIVERY_BASIS_NAME = "Базис поставки"
    VOLUME = "Объем Договоров в единицах измерения"
    TOTAL = "Обьем Договоров, руб."
    COUNT = "Количество Договоров, шт."


class AdditionalColumns(StrEnum):
    """Define additional columns to be added to the trade data.

    Attributes:
        DATE: Date of trade column name.

    """

    DATE = "Дата Торгов"


class Settings(BaseSettings):
    """Define application settings.

    Attributes:
        POSTGRES_PASSWORD: Password for PostgreSQL database.
        POSTGRES_USER: Username for PostgreSQL database.
        POSTGRES_HOST: Host for PostgreSQL database.
        POSTGRES_PORT: Port for PostgreSQL database.
        PG_DB_NAME: Database name for PostgreSQL.
        SECRET_KEY: Secret key for application.
        DEBUG: Debug mode flag.
        LOG_LEVEL: Log level for application.
        REDIS_HOST: Host for Redis.
        REDIS_PORT: Port for Redis.
        REDIS_LOGICAL_DB: Logical database for Redis.
        START_DATE: Start date for data fetching.
        DOMAIN: Domain for SPIMEX website.
        START_URL: Start URL for data fetching.
        CSS_PATH_TO_EXCEL_LINKS: CSS path to excel links.
        ROWS_TO_SKIP: Number of rows to skip from the start of the file.
        PAGE_SIZE: Page size for API trades results.
        FASTAPI_TITLE: Title for FastAPI application.
        FASTAPI_SUMMARY: Summary for FastAPI application.
        FASTAPI_DESCRIPTION: Description for FastAPI application.
        FASTAPI_VERSION: Version for FastAPI application.
        FASTAPI_CONTACT_NAME: Developer's name of the application.
        FASTAPI_CONTACT_URL: Developer's GitHub profile of the application.
        FASTAPI_CONTACT_EMAIL: Developer's email of the application.

    """

    model_config = SettingsConfigDict(env_file=[".env", ".env.dev"])

    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    PG_DB_NAME: str

    SECRET_KEY: str
    DEBUG: bool
    LOG_LEVEL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_LOGICAL_DB: int

    START_DATE: date = date(2023, 1, 1)
    DOMAIN: str = "https://spimex.com"
    START_URL: str = f"{DOMAIN}/markets/oil_products/trades/results/"
    CSS_PATH_TO_EXCEL_LINKS: str = (
        "div.page-content__tabs__blocks > div[data-tabcontent]:nth-of-type(1) "
        "div.accordeon-inner__item"
    )
    ROWS_TO_SKIP: int = 6
    PAGE_SIZE: int = 10  # just like in source site

    FASTAPI_TITLE: str = "SPIMEX Trades Parser API"
    FASTAPI_SUMMARY: str = (
        "API for parsed SPIMEX trades data from their "
        "Excel files starting with 2023-01-01."
    )
    FASTAPI_DESCRIPTION: str = (
        "## This API provides access to parsed SPIMEX trades data with "
        "capabilities to:\n"
        "- **Get all last days of trades** _(Date tag)_;\n"
        "- **Get all trades with specific date range** _(Trade tag)_;\n"
        "- **Get all trades** _(Trade tag)_\n"
        "### With filtering by fields:\n"
        "- **exchange_product_id**;\n"
        "- **oil_id**;\n"
        "- **delivery_type_id**;\n"
        "- **delivery_basis_id**\n"
        "### And also with pagination by:\n"
        "- **page** query parameter for specific entry"
    )
    FASTAPI_VERSION: str = "0.0.1"
    FASTAPI_CONTACT_NAME: str = "Nikita"
    FASTAPI_CONTACT_URL: str = "https://github.com/Nikilandgelo"
    FASTAPI_CONTACT_EMAIL: str = "niki_landgelo@outlook.com"


@lru_cache
def get_settings() -> Settings:
    """Return settings object.

    Returns:
        Settings: Application settings object.

    """
    return Settings()


def get_db_url() -> str:
    """Return database URL.

    Returns:
        str: Database connection URL.

    """
    return (
        f"postgresql+asyncpg://{get_settings().POSTGRES_USER}:"
        f"{get_settings().POSTGRES_PASSWORD}@"
        f"{get_settings().POSTGRES_HOST}:"
        f"{get_settings().POSTGRES_PORT}/"
        f"{get_settings().PG_DB_NAME}"
    )


def get_redis_url() -> str:
    """Return Redis connection URL.

    Returns:
        str: Redis connection URL.

    """
    return (
        f"redis://{get_settings().REDIS_HOST}:"
        f"{get_settings().REDIS_PORT}/{get_settings().REDIS_LOGICAL_DB}"
    )


class HTMLTemplatesForTests(StrEnum):
    """Define various HTML templates for tests.

    Attributes:
        LINK_OF_FIRST_EXCEL_FILE: Link of the first test Excel file.
        LINK_OF_SECOND_EXCEL_FILE: Link of the second test Excel file.
        DATE_OF_FIRST_EXCEL_FILE: Date of the first test Excel file.
        DATE_OF_SECOND_EXCEL_FILE: Date of the second test Excel file.
        VALID_HTML_TEMPLATE: Valid HTML template.
        EMPTY_HTML_TEMPLATE: Empty HTML template.
        INVALID_HTML_TEMPLATE: Invalid HTML template.

    """

    LINK_OF_FIRST_EXCEL_FILE = "file1.xls"
    LINK_OF_SECOND_EXCEL_FILE = "file2.xls"
    DATE_OF_FIRST_EXCEL_FILE = "01.01.2024"
    DATE_OF_SECOND_EXCEL_FILE = "02.01.2024"

    VALID_HTML_TEMPLATE = f"""
    <html>
    <body>
        <div class="page-content__tabs__blocks">
            <div data-tabcontent>
                <div class="accordeon-inner__item">
                    <a href="{LINK_OF_FIRST_EXCEL_FILE}">Excel File 1</a>
                    <span>{DATE_OF_FIRST_EXCEL_FILE}</span>
                </div>
                <div class="accordeon-inner__item">
                    <a href="{LINK_OF_SECOND_EXCEL_FILE}">Excel File 2</a>
                    <span>{DATE_OF_SECOND_EXCEL_FILE}</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    EMPTY_HTML_TEMPLATE = """
    <html>
    <body>
        <div class="page-content__tabs__blocks">
            <div data-tabcontent>
                <!-- No accordeon-inner__item elements -->
            </div>
        </div>
    </body>
    </html>
    """
    INVALID_HTML_TEMPLATE = "Not a valid HTML"
