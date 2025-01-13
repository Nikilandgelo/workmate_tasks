"""Define API routes for the FastAPI application."""

from fastapi import APIRouter

dates = APIRouter(
    prefix="/dates",
    tags=["Date"],
)

trades = APIRouter(
    prefix="/trades",
    tags=["Trade"],
)


ALL_ROUTERS = [
    obj for _, obj in locals().items() if isinstance(obj, APIRouter)
]
