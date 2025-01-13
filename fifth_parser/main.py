"""Main module for the application.

This module contains the main logic for the application, including
asynchronous parsing trade data from the website, saving it to the database
and starting the FastAPI server.
"""

import logging
from asyncio import Task, as_completed, create_task, run
from datetime import date
from time import time

import uvicorn
from aiohttp import ClientSession
from termcolor import colored

from .config import get_settings
from .db import DBManager
from .excel_parser import parse_excel_file
from .html_parser import get_all_xls_links

db_manager = DBManager()


async def get_page_links() -> None:
    """Fetch and parse trade data from website pages.

    Iterates through pages, extracts excel links, and saves data to DB.
    """
    if await db_manager.check_if_data_exists():
        logging.warning(
            colored(
                "Data in DB already exists, exiting without parsing...",
                "yellow",
            ),
        )
        return
    counter: int = 1
    correct_date: bool = True
    db_tasks: list[Task] = []
    while correct_date:
        url: str = f"{get_settings().START_URL}?page=page-{counter}"
        async with ClientSession() as session, session.get(url) as response:
            logging.info(
                colored(f"Fetching data from this url: {url}", "magenta"),
            )
            for container in await get_all_xls_links(response):
                date_: list[str] = (
                    container.find("span").get_text().split(".")[::-1]
                )
                date_: list[int] = [int(x) for x in date_]
                trade_date: date = date(*date_)
                logging.info(
                    colored(f"Took new file from date: {trade_date}", "cyan"),
                )
                if trade_date < get_settings().START_DATE:
                    correct_date = False
                    logging.warning(
                        colored("Date is exceed. Exiting...\n", "yellow"),
                    )
                    break
                link: str = (
                    f"{get_settings().DOMAIN}/"
                    f"{container.find('a').get('href')}"
                )
                task: Task = create_task(
                    parse_excel_file(link, trade_date),
                )
                db_tasks.append(task)
            async for task in as_completed(db_tasks):
                await db_manager.add_new_data(task.result())
            db_tasks.clear()
            counter += 1


if __name__ == "__main__":
    logging.basicConfig(
        format=colored("{levelname} - ", "magenta")
        + colored("{asctime}: ", "blue")
        + "{message}",
        style="{",
        level=get_settings().LOG_LEVEL,
    )
    logging.info(colored("Starting SPIMEX trade data parser", "cyan"))
    start_time: float = time()
    run(get_page_links())
    logging.info(
        colored(
            text=f"Data successfully collected for "
            f"{round(time() - start_time, 2)} seconds, "
            f"starting uvicorn server now...",
            color="green",
            attrs=["bold"],
        ),
    )
    uvicorn.run("fifth_parser.api.app:app", host="0.0.0.0", reload=True)
