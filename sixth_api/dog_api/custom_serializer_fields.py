"""Define a custom serializer field for Breed instances.

This module provides the BreedField class, which allows serialization
and deserialization of Breed instances in Django REST Framework.

Attributes:
    BreedField: A serializer field for Breed instances.

Methods:
    to_representation(value: Breed) -> str:
        Return the name of the given Breed instance.

    to_internal_value(data: str) -> Breed:
        Convert input data to a Breed instance.

Raises:
    CustomSerializerFieldError: If the breed does not exist.

"""

import sys

from breed.models import Breed
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .settings import BASE_DIR

project_root = str(BASE_DIR.parent)
sys.path.append(project_root)

from exceptions import CustomSerializerFieldError  # noqa: E402


class BreedField(serializers.Field):
    """Define a custom serializer field for Breed instances."""

    def to_representation(self, value: Breed) -> str:
        """Return the name of the given Breed instance.

        Args:
            value (Breed): The Breed instance to serialize.

        Returns:
            str: The name of the breed.

        """
        return value.name

    def to_internal_value(self, data: str) -> Breed | None:
        """Convert input data to a Breed instance.

        Args:
            data (str): The name of the breed to retrieve.

        Returns:
            Breed: The corresponding Breed instance.

        Raises:
            CustomSerializerFieldError: If the breed does not exist.

        """
        try:
            return Breed.objects.get(name=data)
        except ObjectDoesNotExist as err:
            raise CustomSerializerFieldError(
                Breed.__name__,
                "name",
                data,
            ) from err
