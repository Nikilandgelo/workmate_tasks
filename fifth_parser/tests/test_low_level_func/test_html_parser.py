"""Test get_all_xls_links function in fifth_parser.html_parser."""

from typing import TYPE_CHECKING

from fifth_parser.config import HTMLTemplatesForTests
from fifth_parser.html_parser import get_all_xls_links

if TYPE_CHECKING:
    from unittest.mock import (
        MagicMock,
    )

    from bs4 import ResultSet, Tag


async def test_get_all_xls_links_with_valid_html(mocker):
    """Test get_all_xls_links with valid HTML.

    Args:
        mocker: pytest mocker fixture.

    Returns:
        None.

    """
    mocked_response: MagicMock = mocker.patch(
        "fifth_parser.html_parser.ClientResponse",
    )
    mocked_response.text = mocker.AsyncMock(
        return_value=HTMLTemplatesForTests.VALID_HTML_TEMPLATE,
    )
    links: ResultSet[Tag] = await get_all_xls_links(mocked_response)

    assert len(links) == 2  # noqa: PLR2004
    assert (
        links[0].find("a").get("href")
        == HTMLTemplatesForTests.LINK_OF_FIRST_EXCEL_FILE.value
    )
    assert (
        links[0].find("span").get_text()
        == HTMLTemplatesForTests.DATE_OF_FIRST_EXCEL_FILE.value
    )

    assert (
        links[1].find("a").get("href")
        == HTMLTemplatesForTests.LINK_OF_SECOND_EXCEL_FILE.value
    )
    assert (
        links[1].find("span").get_text()
        == HTMLTemplatesForTests.DATE_OF_SECOND_EXCEL_FILE.value
    )


async def test_get_all_xls_links_with_no_links(mocker):
    """Test get_all_xls_links with no links.

    Args:
        mocker: pytest mocker fixture.

    Returns:
        None.

    """
    mocked_response: MagicMock = mocker.patch(
        "fifth_parser.html_parser.ClientResponse",
    )
    mocked_response.text = mocker.AsyncMock(
        return_value=HTMLTemplatesForTests.EMPTY_HTML_TEMPLATE,
    )
    links = await get_all_xls_links(mocked_response)
    assert len(links) == 0


async def test_get_all_xls_links_with_invalid_html(mocker):
    """Test get_all_xls_links with invalid HTML.

    Args:
        mocker: pytest mocker fixture.

    Returns:
        None.

    """
    mocked_response: MagicMock = mocker.patch(
        "fifth_parser.html_parser.ClientResponse",
    )
    mocked_response.text = mocker.AsyncMock(
        return_value=HTMLTemplatesForTests.INVALID_HTML_TEMPLATE,
    )
    links = await get_all_xls_links(mocked_response)
    assert len(links) == 0
