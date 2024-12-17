"""Define models related to dog attributes and behaviors.

This module contains the Dog class, which represents a dog with its
attributes such as name, age, breed, gender, color, favorite food,
and favorite toy. Utilize this module to manage dog-related data
within the application.
"""

from breed.models import Breed
from django.db import models


class Dog(models.Model):
    """Represent a dog with its attributes and behaviors.

    Attributes:
        name (str): The name of the dog.
        age (int): The age of the dog.
        breed (Breed): The breed of the dog.
        gender (str): The gender of the dog.
        color (str): The color of the dog.
        favorite_food (str): The favorite food of the dog.
        favorite_toy (str): The favorite toy of the dog.

    """

    class Gender(models.TextChoices):
        """Define the gender options for a dog."""

        MALE = "Male"
        FEMALE = "Female"

    name: str = models.CharField(max_length=255, db_comment="Name of the dog")
    age: int = models.PositiveSmallIntegerField(db_comment="Age of the dog")
    breed: Breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        related_name="dogs",
        db_comment="Breed of the dog",
    )
    gender: str = models.CharField(
        choices=Gender,
        max_length=6,
        db_comment="Gender of the dog",
    )
    color: str = models.CharField(
        max_length=100,
        db_comment="Color of the dog",
    )
    favorite_food: str = models.CharField(
        max_length=255,
        db_comment="Favorite food of the dog",
    )
    favorite_toy: str = models.CharField(
        max_length=255,
        db_comment="Favorite toy of the dog",
    )

    def __str__(self) -> str:
        """Return the string representation of the dog.

        Returns:
            str: The name of the dog.

        """
        return self.name
