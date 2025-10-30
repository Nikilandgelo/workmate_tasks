"""Provide utility functions for the API."""

from datetime import UTC, datetime, timedelta


def calculate_cache_time() -> int:
    """Calculate the cache time in seconds until 11:11 UTC/14:11 MSK.

    Returns:
        int: The number of seconds until 11:11 UTC/14:11 MSK.

    """
    now: datetime = datetime.now(UTC)

    # 14:11 Europe/Moscow == 11:11 UTC
    target = now.replace(hour=11, minute=11)
    if target < now:
        target += timedelta(days=1)
    return int((target - now).total_seconds())
