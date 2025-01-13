"""Test utility functions for the fifth_parser."""

from datetime import UTC, datetime, timedelta

from fifth_parser.api.utils import calculate_cache_time


def test_calculate_cache_time():
    """Test the calculate_cache_time function."""
    now: datetime = datetime.now(UTC)
    target: datetime = now.replace(hour=11, minute=11)
    if target < now:
        target += timedelta(days=1)
    assert calculate_cache_time() == int((target - now).total_seconds())
