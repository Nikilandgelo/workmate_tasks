"""Handle API views for Dog objects.

This module provides the DogViewSet class to manage dog-related
operations, including listing and retrieving dog instances.
"""

from django.db.models import Avg, Count, OuterRef, QuerySet, Subquery
from dog.models import Dog
from dog.serializers import DogSerializer
from rest_framework import viewsets


class DogViewSet(viewsets.ModelViewSet):
    """Manage CRUD operations for Dog instances.

    Attributes:
        serializer_class: The serializer used for Dog instances.

    """

    serializer_class = DogSerializer

    def get_queryset(self) -> QuerySet:
        """Retrieve the queryset of Dog instances based on the action.

        Returns:
            QuerySet: A queryset of Dog instances, annotated with
            breed average age or breed count based on the action.

        """
        if self.action == "list":
            queryset = Dog.objects.annotate(
                breed_avg_age=Subquery(
                    Dog.objects.filter(breed_id=OuterRef("breed_id"))
                    .values("breed_id")
                    .annotate(avg_age=Avg("age"))
                    .values("avg_age"),
                ),
            )
        elif self.action == "retrieve":
            queryset = Dog.objects.annotate(
                breed_count=Subquery(
                    Dog.objects.filter(breed_id=OuterRef("breed_id"))
                    .values("breed_id")
                    .annotate(count=Count("*"))
                    .values("count"),
                ),
            )
        else:
            queryset = Dog.objects.all()

        # because of the breed name in the serializer, we don`t want to make
        # another query in the breed table there just for a name
        return queryset.select_related("breed")
