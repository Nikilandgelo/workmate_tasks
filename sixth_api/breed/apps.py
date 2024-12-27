"""Configure the breed application for Django.

This module defines the configuration for the breed application,
inheriting from Django's AppConfig. It specifies the name of the
application and any other configuration options as needed.
"""

from django.apps import AppConfig


class BreedConfig(AppConfig):
    """Configure the Breed application.

    Attributes:
        name (str): The name of the application, set to 'breed'.

    """

    name = "breed"
