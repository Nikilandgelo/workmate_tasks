"""Define enumerations for various statuses."""

from enum import Enum


class StepStatuses(Enum):
    """Represent the status of a step."""

    RECEIVED = "received"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
