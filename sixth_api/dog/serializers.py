"""Provide serializers for Dog model in the application.

This module contains the DogSerializer class, which is responsible for
serializing Dog model instances to and from JSON format.
"""

from typing import ClassVar

from dog.models import Dog
from dog_api.custom_serializer_fields import BreedField
from rest_framework import serializers


class DogSerializer(serializers.ModelSerializer):
    """Serialize Dog model instances.

    Attributes:
        breed (BreedField): Custom field for breed serialization.
        breed_avg_age (float): Average age of the breed, read-only.
        breed_count (int): Count of dogs of the breed, read-only.

    """

    breed = BreedField()
    breed_avg_age = serializers.FloatField(read_only=True)
    breed_count = serializers.IntegerField(read_only=True)

    class Meta:
        """Define metadata for DogSerializer.

        Fields:
            model (Dog): The model to serialize.
            fields (list[str]): List of fields to include in serialization.
        """

        model = Dog
        fields: ClassVar[list[str]] = [
            "name",
            "age",
            "breed",
            "breed_avg_age",
            "breed_count",
            "gender",
            "color",
            "favorite_food",
            "favorite_toy",
        ]
