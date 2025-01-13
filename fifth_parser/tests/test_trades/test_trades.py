"""Test trade related endpoints."""

import secrets
from datetime import date, timedelta
from typing import TYPE_CHECKING

import pytest
from fastapi import status

from fifth_parser.api.urls import trades
from fifth_parser.models import SpimexTradingResults

pytestmark = [pytest.mark.anyio]


if TYPE_CHECKING:
    from httpx import Response


async def test_get_trading_results(client, mixer, acceptable_dates):
    """Test get trading results without filters.

    :param client: pytest fixture
    :param mixer: pytest fixture
    :param acceptable_dates: pytest fixture
    :returns: None
    """
    await mixer.async_blend(
        SpimexTradingResults,
        date=secrets.choice(tuple(acceptable_dates())),
    )

    response: Response = await client.get(
        trades.url_path_for("get_trading_results"),
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("trades"), list)


async def test_get_trading_results_oil_id(client, mixer, acceptable_dates):
    """Test get trading results filtered by oil_id.

    :param client: pytest fixture
    :param mixer: pytest fixture
    :param acceptable_dates: pytest fixture
    :returns: None
    """
    all_tested_oils_ids = ("ABCD", "EFGH", "IJKL")
    for oil_id in all_tested_oils_ids:
        random_date: date = secrets.choice(tuple(acceptable_dates()))
        await mixer.async_blend(
            SpimexTradingResults,
            date=random_date,
            oil_id=oil_id,
        )
        response: Response = await client.get(
            trades.url_path_for("get_trading_results"),
            params={
                "oil_id": oil_id,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get("trades")) == 1
        assert response.json().get("trades")[0].get("oil_id") == oil_id
        assert response.json().get("trades")[0].get("date") == str(random_date)

    all_response: Response = await client.get(
        trades.url_path_for("get_trading_results"),
    )
    assert all_response.status_code == status.HTTP_200_OK
    assert len(all_response.json().get("trades")) == len(all_tested_oils_ids)
    for trade in all_response.json().get("trades"):
        assert trade.get("oil_id") in all_tested_oils_ids


async def test_get_trading_results_delivery_type_id(
    client,
    mixer,
    acceptable_dates,
):
    """Test get trading results filtered by delivery_type_id.

    :param client: pytest fixture
    :param mixer: pytest fixture
    :param acceptable_dates: pytest fixture
    :returns: None
    """
    all_tested_types = ("A", "B", "C", "D", "E")
    for delivery_type_id in all_tested_types:
        await mixer.async_blend(
            SpimexTradingResults,
            date=secrets.choice(tuple(acceptable_dates())),
            delivery_type_id=delivery_type_id,
        )
        response: Response = await client.get(
            trades.url_path_for("get_trading_results"),
            params={
                "delivery_type_id": delivery_type_id,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get("trades")) == 1
        assert (
            response.json().get("trades")[0].get("delivery_type_id")
            == delivery_type_id
        )

    all_response: Response = await client.get(
        trades.url_path_for("get_trading_results"),
    )
    assert len(all_response.json().get("trades")) == len(all_tested_types)
    for trade in all_response.json().get("trades"):
        assert trade.get("delivery_type_id") in all_tested_types


async def test_get_trading_results_delivery_basis_id(
    client,
    mixer,
    acceptable_dates,
):
    """Test get trading results filtered by delivery_basis_id.

    :param client: pytest fixture
    :param mixer: pytest fixture
    :param acceptable_dates: pytest fixture
    :returns: None
    """
    all_tested_delivery_basis_ids = ("ABC", "DEF", "GHI", "JKL")
    for delivery_basis_id in all_tested_delivery_basis_ids:
        await mixer.async_blend(
            SpimexTradingResults,
            date=secrets.choice(tuple(acceptable_dates())),
            delivery_basis_id=delivery_basis_id,
        )
        response: Response = await client.get(
            trades.url_path_for("get_trading_results"),
            params={
                "delivery_basis_id": delivery_basis_id,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get("trades")) == 1
        assert (
            response.json().get("trades")[0].get("delivery_basis_id")
            == delivery_basis_id
        )

    all_response: Response = await client.get(
        trades.url_path_for("get_trading_results"),
    )
    assert len(all_response.json().get("trades")) == len(
        all_tested_delivery_basis_ids,
    )
    for trade in all_response.json().get("trades"):
        assert trade.get("delivery_basis_id") in all_tested_delivery_basis_ids


async def test_get_trading_results_pagination(
    client,
    mixer,
    acceptable_dates,
):
    """Test get trading results with pagination.

    :param client: pytest fixture
    :param mixer: pytest fixture
    :param acceptable_dates: pytest fixture
    :returns: None
    """
    for _ in range(11):
        await mixer.async_blend(
            SpimexTradingResults,
            date=secrets.choice(tuple(acceptable_dates())),
        )

    first_page_response: Response = await client.get(
        trades.url_path_for("get_trading_results"),
    )
    assert first_page_response.status_code == status.HTTP_200_OK
    assert len(first_page_response.json().get("trades")) == 10  # noqa: PLR2004

    second_page_response: Response = await client.get(
        trades.url_path_for("get_trading_results"),
        params={
            "page": 2,
        },
    )
    assert second_page_response.status_code == status.HTTP_200_OK
    assert len(second_page_response.json().get("trades")) == 1


@pytest.mark.parametrize(
    "param, value",
    [
        ("oil_id", "ABCDE"),
        ("delivery_type_id", "FG"),
        ("delivery_basis_id", "HIJKL"),
        ("page", 0),
    ],
)
async def test_get_trading_results_invalid_params(client, param, value):
    """Test get trading results with invalid params.

    :param client: pytest fixture
    :param param: parameter name
    :param value: parameter value
    :returns: None
    """
    response = await client.get(
        trades.url_path_for("get_trading_results"),
        params={
            f"{param}": value,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_dynamics_start_date(client, mixer):
    """Test get dynamics with start_date filter.

    :param client: pytest fixture
    :param mixer: pytest fixture
    :returns: None
    """
    today: date = date.today()
    start_date: date = today - timedelta(days=30)

    date_out: date = start_date - timedelta(days=1)
    for index in range(3):
        await mixer.async_blend(
            SpimexTradingResults,
            date=date_out + timedelta(days=index),
        )
    response: Response = await client.get(
        trades.url_path_for("get_dynamics"),
        params={
            "start_date": str(start_date),
            "end_date": str(today),
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("trades"), list)
    assert len(response.json().get("trades")) == 2  # noqa: PLR2004

    full_response: Response = await client.get(
        trades.url_path_for("get_dynamics"),
        params={
            "start_date": str(date_out),
            "end_date": str(today),
        },
    )
    assert len(full_response.json().get("trades")) == 3  # noqa: PLR2004


async def test_get_dynamics_end_date(client, mixer):
    """Test get dynamics with end_date filter.

    :param client: pytest fixture
    :param mixer: pytest fixture
    :returns: None
    """
    today: date = date.today()
    start_date: date = today - timedelta(days=90)
    end_date: date = today - timedelta(days=30)

    date_out: date = end_date + timedelta(days=1)
    for index in range(3):
        await mixer.async_blend(
            SpimexTradingResults,
            date=date_out - timedelta(days=index),
        )
    response: Response = await client.get(
        trades.url_path_for("get_dynamics"),
        params={
            "start_date": str(start_date),
            "end_date": str(end_date),
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("trades"), list)
    assert len(response.json().get("trades")) == 2  # noqa: PLR2004

    full_response: Response = await client.get(
        trades.url_path_for("get_dynamics"),
        params={
            "start_date": str(start_date),
            "end_date": str(date_out),
        },
    )
    assert len(full_response.json().get("trades")) == 3  # noqa: PLR2004


@pytest.mark.parametrize(
    "start_date, end_date, oil_id, delivery_type_id, delivery_basis_id",
    [
        (None, "2023-01-02", "ABCD", "F", "HIJ"),
        ("2023-01-01", None, "ABCD", "F", "HIJ"),
        (None, None, "ABCD", "F", "HIJ"),
        ("2024-01-01", "2024-01-02", "ABCDE", "F", "HIJ"),
        ("2024-01-01", "2024-01-02", "ABCD", "FG", "HIJ"),
        ("2024-01-01", "2024-01-02", "ABCD", "F", "HIJK"),
    ],
)
async def test_get_dynamics_invalid_params(
    client,
    start_date,
    end_date,
    oil_id,
    delivery_type_id,
    delivery_basis_id,
):
    """Test get dynamics with invalid params.

    :param client: pytest fixture
    :param start_date: start date
    :param end_date: end date
    :param oil_id: oil id
    :param delivery_type_id: delivery type id
    :param delivery_basis_id: delivery basis id
    :returns: None
    """
    response = await client.get(
        trades.url_path_for("get_dynamics"),
        params={
            "start_date": start_date,
            "end_date": end_date,
            "oil_id": oil_id,
            "delivery_type_id": delivery_type_id,
            "delivery_basis_id": delivery_basis_id,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
