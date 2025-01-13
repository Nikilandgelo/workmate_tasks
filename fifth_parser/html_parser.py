"""Module for parsing HTML content and extracting Excel links from it."""

import logging

from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from termcolor import colored

from fifth_parser.config import get_settings


async def get_all_xls_links(response: ClientResponse) -> ResultSet[Tag]:
    """Parse HTML content and extract all excel links.

    Args:
        response (ClientResponse): aiohttp ClientResponse object
            containing HTML content.

    Returns:
        ResultSet[Tag]: A ResultSet of bs4 Tag objects
            representing the found Excel links.

    """
    full_document: BeautifulSoup = BeautifulSoup(
        await response.text(),
        "html.parser",
    )
    links_container: ResultSet[Tag] = full_document.css.select(
        get_settings().CSS_PATH_TO_EXCEL_LINKS,
    )
    logging.info(
        colored(f"Found new {len(links_container)} excel links", "green"),
    )
    return links_container
