"""Configure the user application for the Django project.

This module contains the configuration for the user app, defining
the app name and any related settings.
"""

from django.apps import AppConfig


class UserConfig(AppConfig):
    """Configure the user application.

    Attributes:
        name (str): The name of the application.

    """

    name = "user"
