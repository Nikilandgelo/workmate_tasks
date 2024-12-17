"""Provide serializers for the Breed model.

This module contains the BreedSerializer class, which is used to serialize
the Breed model instances for API responses.
"""

from breed.models import Breed
from rest_framework import serializers


class BreedSerializer(serializers.ModelSerializer):
    """Serialize the Breed model.

    Attributes:
        dog_count (int): Read-only field representing the number of dogs.

    """

    dog_count = serializers.IntegerField(read_only=True)

    class Meta:
        """Define model and fields for serialization using 'Breed' model."""

        model = Breed
        fields = "__all__"
