"""Define serializers for date objects.

Serializers are used to convert data to JSON.
"""

from datetime import date

from pydantic import BaseModel


class DateSerializer(BaseModel):
    """Represent a single date.

    Attributes:
        date: A date object.

    """

    date: date


class DatesSerializer(BaseModel):
    """Represent a list of dates.

    Attributes:
        dates: A list of DateSerializer objects.

    """

    dates: list[DateSerializer]
