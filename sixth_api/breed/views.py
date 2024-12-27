"""Define API views for managing breeds.

This module contains the BreedViewSet for handling breed-related API
requests.
"""

from breed.models import Breed
from breed.serializers import BreedSerializer
from django.db.models import Count, OuterRef, QuerySet, Subquery
from dog.models import Dog
from rest_framework import viewsets


class BreedViewSet(viewsets.ModelViewSet):
    """Manage breeds in the API.

    Attributes:
        serializer_class: The serializer class for breed representation.

    """

    serializer_class = BreedSerializer

    def get_queryset(self) -> QuerySet:
        """Retrieve the queryset of breeds.

        Returns:
            QuerySet: A queryset of breeds, annotated with the count of
            associated dogs if the action is 'list'.

        """
        if self.action == "list":
            return Breed.objects.annotate(
                dog_count=Subquery(
                    Dog.objects.filter(breed_id=OuterRef("id"))
                    .values("breed_id")
                    .annotate(count=Count("*"))
                    .values("count"),
                ),
            )
        return Breed.objects.all()
