"""Define the Dog application configuration.

This module contains the configuration for the Dog application within
Django. It sets up the application name and any other necessary
configuration.
"""

from django.apps import AppConfig


class DogConfig(AppConfig):
    """Configure the Dog application.

    Attributes:
        name (str): The name of the application, set to "dog".

    """

    name = "dog"
