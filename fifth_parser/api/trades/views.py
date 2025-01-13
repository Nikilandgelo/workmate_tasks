"""Implement API endpoints for trading results."""

from datetime import date
from typing import Annotated

from fastapi import Query
from fastapi_cache.decorator import cache
from sqlalchemy.sql.expression import ColumnOperators

from fifth_parser.api.trades.serializers import SpimexTradingResultsSerializer
from fifth_parser.api.urls import trades
from fifth_parser.api.utils import calculate_cache_time
from fifth_parser.config import get_settings
from fifth_parser.main import db_manager
from fifth_parser.models import SpimexTradingResults


@trades.get(
    "/",
    response_model=SpimexTradingResultsSerializer,
    summary="Trading results",
    description="This endpoint has pagination with 'page' query parameter and "
    "can be filtered by fields: 'oil_id', 'delivery_type_id' and "
    "'delivery_basis_id'.",
    name="get_trading_results",
)
@cache(expire=calculate_cache_time())
async def get_trading_results(
    oil_id: Annotated[
        str,
        Query(
            max_length=4,
            description="Filter by oil ID.",
        ),
    ] = "%",
    delivery_type_id: Annotated[
        str,
        Query(
            max_length=1,
            description="Filter by delivery type ID.",
        ),
    ] = "%",
    delivery_basis_id: Annotated[
        str,
        Query(
            max_length=3,
            description="Filter by delivery basis ID.",
        ),
    ] = "%",
    page: Annotated[
        int,
        Query(
            ge=1,
            description="Page number for pagination.",
        ),
    ] = 1,
) -> SpimexTradingResultsSerializer:
    """Get trading results with filtering and pagination.

    Args:
        oil_id(str): Filter by oil ID.
        delivery_type_id(str): Filter by delivery type ID.
        delivery_basis_id(str): Filter by delivery basis ID.
        page(int): Page number for pagination.

    Returns:
        Serialized trading results.

    """
    result = await db_manager.get_spimex_trading_results(
        conditions={
            SpimexTradingResults.oil_id: [
                (ColumnOperators.icontains, oil_id),
            ],
            SpimexTradingResults.delivery_type_id: [
                (ColumnOperators.ilike, delivery_type_id),
            ],
            SpimexTradingResults.delivery_basis_id: [
                (ColumnOperators.icontains, delivery_basis_id),
            ],
        },
        limit=get_settings().PAGE_SIZE,
        order_by=SpimexTradingResults.date,
        order_desc=True,
        offset=get_settings().PAGE_SIZE * (page - 1),
    )
    return SpimexTradingResultsSerializer(trades=result)


@trades.get(
    "/dynamics",
    response_model=SpimexTradingResultsSerializer,
    summary="Dynamics of trading results related to specific date range",
    description="Can be filtered by fields: 'oil_id', 'delivery_type_id' and "
    "'delivery_basis_id'.",
    name="get_dynamics",
)
@cache(expire=calculate_cache_time())
async def get_dynamics(
    start_date: date,
    end_date: date,
    oil_id: Annotated[
        str,
        Query(
            max_length=4,
            description="Filter by oil ID.",
        ),
    ] = "%",
    delivery_type_id: Annotated[
        str,
        Query(
            max_length=1,
            description="Filter by delivery type ID.",
        ),
    ] = "%",
    delivery_basis_id: Annotated[
        str,
        Query(
            max_length=3,
            description="Filter by delivery basis ID.",
        ),
    ] = "%",
) -> SpimexTradingResultsSerializer:
    """Get trading results dynamics for a date range.

    Args:
        start_date(date): Start date of the range.
        end_date(date): End date of the range.
        oil_id(str): Filter by oil ID.
        delivery_type_id(str): Filter by delivery type ID.
        delivery_basis_id(str): Filter by delivery basis ID.

    Returns:
        Serialized trading results.

    """
    result = await db_manager.get_spimex_trading_results(
        conditions={
            SpimexTradingResults.date: [
                (ColumnOperators.__ge__, start_date),
                (ColumnOperators.__le__, end_date),
            ],
            SpimexTradingResults.oil_id: [
                (ColumnOperators.icontains, oil_id),
            ],
            SpimexTradingResults.delivery_type_id: [
                (ColumnOperators.ilike, delivery_type_id),
            ],
            SpimexTradingResults.delivery_basis_id: [
                (ColumnOperators.icontains, delivery_basis_id),
            ],
        },
    )
    return SpimexTradingResultsSerializer(trades=result)
