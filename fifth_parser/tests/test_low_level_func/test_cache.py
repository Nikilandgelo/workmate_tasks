"""Test caching functionality using a Redis engine."""

from fifth_parser.api.urls import dates, trades


async def test_cache(client, redis_engine):
    """Test the caching mechanism.

    Args:
        client: An HTTP client for making requests.
        redis_engine: A Redis engine for caching.

    """
    assert await redis_engine.keys("*") == []

    await client.get(
        trades.url_path_for("get_trading_results"),
    )
    all_redis_keys: list[str] = await redis_engine.keys("*")
    assert all_redis_keys != []
    assert len(all_redis_keys) == 1

    await client.get(
        dates.url_path_for("get_dates"),
    )
    all_redis_keys: list[str] = await redis_engine.keys("*")
    assert len(all_redis_keys) == 2  # noqa: PLR2004
