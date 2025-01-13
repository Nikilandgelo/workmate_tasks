"""Provide async mixing capabilities for SQLAlchemy models in test environment.

Extends the standard Mixer class to support async operations with SQLAlchemy,
specifically designed for creating test data in async database sessions.
Manages model creation and tracks created models for testing purposes.

Requires an async SQLAlchemy session for operation.
"""

import logging
from typing import TYPE_CHECKING, Any

from mixer.backend.sqlalchemy import Mixer
from termcolor import colored

from fifth_parser.models import SpimexTradingResults

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class AsyncMixer(Mixer):
    """Extend Mixer class to provide async database operations for testing.

    Manages async model creation and tracking while maintaining compatibility
    with the base Mixer functionality. Automatically disables auto-commit.

    Attributes:
        created_models (list): Store names of models created during mixing.

    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize async mixer with auto-commit disabled.

        Args:
            **kwargs: Configuration parameters for mixer initialization.

        """
        super().__init__(**kwargs, commit=False)
        self.created_models: list = []

    async def async_blend(
        self,
        model: str | type[SpimexTradingResults],
        **values: Any,
    ) -> None:
        """Create and persist a new model instance asynchronously.

        Args:
            model: Model class to create
            **values: Attribute values to set on the created instance

        """
        session: AsyncSession = self.params.get("session")
        logging.info(
            colored(f"Blending {model.__tablename__} model", "light_cyan"),
        )
        obj = self.blend(model, **values)
        if obj.__tablename__ not in self.created_models:
            self.created_models.append(obj.__tablename__)
        session.add(obj)
        await session.commit()
