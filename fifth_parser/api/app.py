"""Define FastAPI application, with Redis for caching on app's startup.

This module contains the FastAPI application definition with including of all
routes and the Redis client for caching endpoints on startup.
"""

from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from redis.asyncio.client import Redis

# import all view modules from the api subpackages, not via * cuz it cause a
# weird error with wrong path, I tried to fix it, but it didn't work so __all__
from fifth_parser.api import __all__ as all_views  # noqa: F401
from fifth_parser.api.custom_logs import LoggingRedisBackend
from fifth_parser.config import get_redis_url, get_settings

from .urls import ALL_ROUTERS


@asynccontextmanager
async def startup(_: FastAPI) -> AbstractAsyncContextManager:
    """Initialize all FastAPI components and close them on exit.

    Returns:
        AsyncContextManager: Async context manager.

    """
    redis: Redis = Redis.from_url(get_redis_url())
    FastAPICache.init(LoggingRedisBackend(redis), prefix="cache")
    try:
        yield
    finally:
        await redis.close()


app = FastAPI(
    lifespan=startup,
    title=get_settings().FASTAPI_TITLE,
    description=get_settings().FASTAPI_DESCRIPTION,
    version=get_settings().FASTAPI_VERSION,
    contact={
        "name": get_settings().FASTAPI_CONTACT_NAME,
        "url": get_settings().FASTAPI_CONTACT_URL,
        "email": get_settings().FASTAPI_CONTACT_EMAIL,
    },
)

for router in ALL_ROUTERS:
    app.include_router(router)
