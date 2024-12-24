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

    class Meta:
        verbose_name = "Breed"
        verbose_name_plural = "Breeds"

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
        db_comment="Unique name of the breed with length of 255",
        verbose_name="Name",
        help_text="Breed name must be unique.",
        unique=True,
    )
    size: str = models.CharField(
        choices=Size,
        max_length=6,
        db_comment="Size of the breed which can be one of: Tiny, Small, "
                   "Medium, or Large",
        verbose_name="Size",
        help_text="Breed size must be one of: Tiny, Small, Medium, or Large.",
    )
    friendliness: int = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        db_comment="Friendliness from 1 to 5",
        verbose_name="Friendliness",
        help_text="Breed friendliness must be between 1 and 5.",
    )
    trainability: int = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        db_comment="Trainability from 1 to 5",
        verbose_name="Trainability",
        help_text="Breed trainability must be between 1 and 5.",
    )
    shedding_amount: int = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        db_comment="Shedding amount from 1 to 5",
        verbose_name="Shedding Amount",
        help_text="Breed shedding amount must be between 1 and 5.",
    )
    exercise_needs: int = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        db_comment="Exercise needs from 1 to 5",
        verbose_name="Exercise Needs",
        help_text="Breed exercise needs must be between 1 and 5.",
    )

    def __str__(self) -> str:
        """Return the string representation of the breed."""
        return self.name
