"""Module for user models.

This module defines custom user models extending Django's AbstractUser.
"""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Extend the AbstractUser model to create a custom user model."""
