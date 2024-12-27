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

    class Meta:
        """Define the Meta class for the Dog model.

        Attributes:
            verbose_name (str): The verbose name of the model.
            verbose_name_plural (str): The verbose name of the model in plural.

        """

        verbose_name = "Dog"
        verbose_name_plural = "Dogs"

    class Gender(models.TextChoices):
        """Define the gender options for a dog."""

        MALE = "Male"
        FEMALE = "Female"

    name: str = models.CharField(
        max_length=255,
        db_comment="Name of the dog with length of 255",
        verbose_name="Name",
        help_text="Dog name can be up to 255 characters long.",
    )
    age: int = models.PositiveSmallIntegerField(
        db_comment="Age of the dog more or equal to 0",
        verbose_name="Age",
        help_text="Dog age must be a positive integer.",
    )
    breed: Breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        related_name="dogs",
        db_comment="ID of the dog's breed",
        verbose_name="Breed",
        help_text="Dog breed must be a valid breed ID.",
    )
    gender: str = models.CharField(
        choices=Gender,
        max_length=6,
        db_comment="Gender which can be one of: Male or Female",
        verbose_name="Gender",
        help_text="Dog gender must be one of: Male, Female.",
    )
    color: str = models.CharField(
        max_length=100,
        db_comment="Color of the dog with length of 100",
        verbose_name="Color",
        help_text="Dog color must be a string with length of 100.",
    )
    favorite_food: str = models.CharField(
        max_length=255,
        db_comment="Favorite food with length of 255",
        verbose_name="Favorite Food",
        help_text="Dog favorite food must be a string with length of 255.",
    )
    favorite_toy: str = models.CharField(
        max_length=255,
        db_comment="Favorite toy with length of 255",
        verbose_name="Favorite Toy",
        help_text="Dog favorite toy must be a string with length of 255.",
    )

    def __str__(self) -> str:
        """Return the string representation of the dog.

        Returns:
            str: The name of the dog.

        """
        return self.name
