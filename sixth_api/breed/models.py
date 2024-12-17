"""Define models related to breed attributes and behaviors.

This module contains the Breed model, which represents different dog breeds
with attributes such as name, size, friendliness, trainability, shedding
amount, and exercise needs.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Breed(models.Model):
    """Represent a dog breed with various characteristics.

    Attributes:
        name (str): The name of the breed, must be unique.
        size (str): The size of the breed, chosen from predefined sizes.
        friendliness (int): A rating from 1 to 5 indicating friendliness.
        trainability (int): A rating from 1 to 5 indicating trainability.
        shedding_amount (int): A rating from 1 to 5 indicating shedding amount.
        exercise_needs (int): A rating from 1 to 5 indicating exercise needs.

    """

    class Size(models.TextChoices):
        """Define the sizes available for breeds.

        Attributes:
            TINY (str): Represents a tiny breed.
            SMALL (str): Represents a small breed.
            MEDIUM (str): Represents a medium breed.
            LARGE (str): Represents a large breed.

        """

        TINY = "Tiny"
        SMALL = "Small"
        MEDIUM = "Medium"
        LARGE = "Large"

    name: str = models.CharField(
        max_length=255,
        db_comment="Name of the breed",
        unique=True,
    )
    size: str = models.CharField(
        choices=Size,
        max_length=6,
        db_comment="Size of the breed",
    )
    friendliness: int = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        db_comment="Friendliness of the breed",
    )
    trainability: int = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        db_comment="Trainability of the breed",
    )
    shedding_amount: int = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        db_comment="Shedding amount of the breed",
    )
    exercise_needs: int = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        db_comment="Exercise needs of the breed",
    )

    def __str__(self) -> str:
        """Return the string representation of the breed."""
        return self.name
