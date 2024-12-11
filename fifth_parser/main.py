"""Parse SPIMEX market data from their official website and store it in db.

This module handles web scraping of oil products trading results from SPIMEX,
downloads Excel files containing market data, and stores parsed information in
a database. It implements asynchronous operations for improved performance.

Note:
    The parser starts from January 1st, 2023 and works backwards in time.

"""

from asyncio import Task, TaskGroup, run
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from .config import DOMAIN, START_DATE, START_URL
from .db import add_new_data, init_db_engine
from .excel_parser import parse_excel_file

if TYPE_CHECKING:
    from bs4.element import ResultSet, Tag
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def get_page_links() -> None:
    """Fetch and process SPIMEX trading results pages asynchronously.

    Iterates through paginated trading results, downloads Excel files
    containing market data, and stores parsed information in the database.
    Processing starts from the most recent data and continues until reaching
    January 1st, 2023.

    The function performs the following steps:
    1. Initialize database connection
    2. Fetch HTML content from each page
    3. Extract Excel file links and corresponding dates
    4. Download and parse Excel files
    5. Store parsed data in the database

    Returns:
        None

    Raises:
        aiohttp.ClientError: If network requests fail

    """
    session_maker: async_sessionmaker[AsyncSession] = await init_db_engine()
    counter: int = 1
    correct_date: bool = True
    db_tasks: list[Task] = []
    async with TaskGroup() as db_tg:
        while correct_date:
            async with (
                ClientSession() as session,
                session.get(f"{START_URL}?page=page-{counter}") as response,
            ):
                full_document: BeautifulSoup = BeautifulSoup(
                    await response.text(),
                    "html.parser",
                )
                links_container: ResultSet[Tag] = full_document.css.select(
                    "div.page-content__tabs__blocks > "
                    "div[data-tabcontent]:nth-of-type(1) "
                    "div.accordeon-inner__item",
                )
                async with TaskGroup() as html_tg:
                    for container in links_container:
                        date: datetime = datetime.strptime(
                            container.find("span").get_text(),
                            "%d.%m.%Y",
                        ).replace(tzinfo=UTC)
                        print(f"Took new file from date: {date}")
                        if date < START_DATE:
                            correct_date = False
                            print("\nDate is exceed... Exiting\n")
                            break
                        link: str = (
                            f'{DOMAIN}/{container.find("a").get("href")}'
                        )
                        task: Task = html_tg.create_task(
                            parse_excel_file(link),
                        )
                        db_tasks.append(task)
                for task in db_tasks:
                    db_tg.create_task(
                        add_new_data(session_maker, task.result()),
                    )
                db_tasks.clear()
                counter += 1


if __name__ == "__main__":
    run(get_page_links())
