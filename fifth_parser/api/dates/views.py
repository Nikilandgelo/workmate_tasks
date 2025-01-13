"""Define API endpoints for retrieving trading test_dates."""

from datetime import date, timedelta
from typing import TYPE_CHECKING, Annotated

from fastapi import Query
from fastapi_cache.decorator import cache
from sqlalchemy.sql.expression import ColumnOperators

from fifth_parser.api.urls import dates
from fifth_parser.api.utils import calculate_cache_time
from fifth_parser.config import get_settings
from fifth_parser.main import db_manager
from fifth_parser.models import SpimexTradingResults

from .serializers import DatesSerializer

if TYPE_CHECKING:
    from collections.abc import Sequence


@dates.get(
    "/",
    response_model=DatesSerializer,
    summary="Dates of the last trading results",
    description="By default returns last 30 days of trading results, but can "
    "be changed with the number_of_days query parameter.",
    name="get_dates",
)
@cache(expire=calculate_cache_time())
async def get_dates(
    number_of_days: Annotated[
        int,
        Query(
            ge=1,
            le=(date.today() - get_settings().START_DATE).days,
        ),
    ] = 30,
) -> DatesSerializer:
    """Get dates of the last trading results.

    Args:
        number_of_days (int): Number of days to retrieve
            trading results for.

    Returns:
        DatesSerializer: Serialized test_dates of trading results.

    """
    last_accepted_date: date = date.today() - timedelta(days=number_of_days)
    result: Sequence[
        SpimexTradingResults
    ] = await db_manager.get_spimex_trading_results(
        columns=[SpimexTradingResults.date],
        conditions={
            SpimexTradingResults.date: [
                (ColumnOperators.__ge__, last_accepted_date),
            ],
        },
        only_unique=True,
        order_by=SpimexTradingResults.date,
    )
    return DatesSerializer(dates=result)
