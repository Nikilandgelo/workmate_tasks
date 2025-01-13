"""Test date-related API endpoints."""

import secrets
from typing import TYPE_CHECKING

import pytest
from fastapi import status

from fifth_parser.api.urls import dates
from fifth_parser.models import SpimexTradingResults

pytestmark = [pytest.mark.anyio]


if TYPE_CHECKING:
    from httpx import Response


async def test_get_default_dates(client, mixer, acceptable_dates):
    """Test get dates without number_of_days param.

    Args:
        client: The test client.
        mixer: The mixer fixture.
        acceptable_dates: Fixture that returns acceptable dates.

    """
    random_date = secrets.choice(tuple(acceptable_dates()))
    await mixer.async_blend(SpimexTradingResults, date=random_date)

    response: Response = await client.get(dates.url_path_for("get_dates"))

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("dates"), list)
    assert len(response.json().get("dates")) == 1
    assert response.json().get("dates")[0].get("date") == str(random_date)


async def test_get_dates(client, mixer, acceptable_dates) -> None:
    """Test get dates with number_of_days param.

    Args:
        client: The test client.
        mixer: The mixer fixture.
        acceptable_dates: Fixture that returns acceptable dates.

    """
    # if we will use parametrize, it will trigger TRUNCATE after each test, so
    for count, day in enumerate((1, 125, 365), start=1):
        random_date = secrets.choice(tuple(acceptable_dates(day)))
        await mixer.async_blend(SpimexTradingResults, date=random_date)

        response: Response = await client.get(
            dates.url_path_for("get_dates"),
            params={
                "number_of_days": day,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get("dates")) == count


@pytest.mark.parametrize(
    "day",
    [-1, 9999999999, "Mamamia"],
)
async def test_get_dates_invalid_days(client, day) -> None:
    """Test get dates with invalid number_of_days param.

    Args:
        client: The test client.
        day: Invalid number of days.

    """
    response: Response = await client.get(
        dates.url_path_for("get_dates"),
        params={
            "number_of_days": day,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
