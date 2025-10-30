"""Module for managing database interactions."""

from collections.abc import Sequence
from typing import TYPE_CHECKING

from pandas import DataFrame
from sqlalchemy import Column, RowMapping, desc, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from .config import AdditionalColumns, NeededColumns, get_db_url
from .models import SpimexTradingResults

if TYPE_CHECKING:
    from sqlalchemy.engine import Result
    from sqlalchemy.sql.expression import ColumnOperators


class DBManager:
    """Manage database interactions."""

    def __init__(self, engine: AsyncEngine = None) -> None:
        """Initialize instance and create async session maker in attributes."""
        self.session_maker: async_sessionmaker = async_sessionmaker(
            engine if engine else create_async_engine(get_db_url(), echo=True),
        )

    async def check_if_data_exists(self) -> bool:
        """Check if any data exists in the database.

        Returns:
            bool: True if data exists, False otherwise.

        """
        async with self.session_maker() as session:
            result: Result = await session.execute(
                select(SpimexTradingResults.id).limit(1),
            )
            return result.first() is not None

    async def add_new_data(self, df: DataFrame) -> None:
        """Insert new trading results into the database.

        Process data from a DataFrame and insert it into the database.

        Args:
            df: DataFrame with SPIMEX trading results. Columns must
                match the SpimexTradingResults model fields.

        """
        trading_results: list = []
        async with self.session_maker() as session:
            for _, row in df.iterrows():
                result: SpimexTradingResults = SpimexTradingResults(
                    exchange_product_id=row[
                        NeededColumns.EXCHANGE_PRODUCT_ID.value
                    ],
                    exchange_product_name=row[
                        NeededColumns.EXCHANGE_PRODUCT_NAME.value
                    ],
                    oil_id=row[NeededColumns.EXCHANGE_PRODUCT_ID.value][:4],
                    delivery_basis_id=row[
                        NeededColumns.EXCHANGE_PRODUCT_ID.value
                    ][4:7],
                    delivery_basis_name=row[
                        NeededColumns.DELIVERY_BASIS_NAME.value
                    ],
                    delivery_type_id=row[
                        NeededColumns.EXCHANGE_PRODUCT_ID.value
                    ][-1],
                    volume=int(row[NeededColumns.VOLUME.value]),
                    total=round(float(row[NeededColumns.TOTAL.value])),
                    count=int(row[NeededColumns.COUNT.value]),
                    date=row[AdditionalColumns.DATE.value],
                )
                trading_results.append(result)
        session.add_all(trading_results)
        await session.commit()

    async def get_spimex_trading_results(
        self,
        *,
        columns: list[Column] | None = None,
        conditions: dict[Column, list[tuple]] | None = None,
        only_unique: bool = False,
        order_by: Column | None = None,
        order_desc: bool = False,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[RowMapping]:
        """Get SPIMEX trading results from the database.

        Args:
            columns: List of columns to select. Defaults to all columns.
            conditions: Dict of conditions to filter by. Keys are columns,
                values are lists of (operator, value) tuples.
            only_unique: If True, return only unique rows.
            order_by: Column to order by.
            order_desc: If True, order in descending order.
            limit: Maximum number of rows to return.
            offset: Number of rows to skip.

        Returns:
            Sequence[RowMapping]: Sequence of RowMapping objects
                representing the query results.

        """
        async with self.session_maker() as session:
            needed_columns: list[Column] = columns or [
                *SpimexTradingResults.__table__.columns,
            ]
            conditions: dict = conditions or {}

            all_column_conditions: list[ColumnOperators] = [
                getattr(column, sql_operator.__name__)(value)
                for column, list_conditions in conditions.items()
                for sql_operator, value in list_conditions
            ]

            sql_query = select(*needed_columns).where(*all_column_conditions)
            if only_unique:
                sql_query = sql_query.distinct()
            if order_by is not None:
                if order_desc:
                    sql_query = sql_query.order_by(desc(order_by))
                else:
                    sql_query = sql_query.order_by(order_by)
            if limit is not None:
                sql_query = sql_query.limit(limit)
            if offset is not None:
                sql_query = sql_query.offset(offset)

            result: Result = await session.execute(sql_query)
            return result.mappings().all()
