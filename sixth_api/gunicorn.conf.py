"""Configure Gunicorn server settings for the application.

Attributes:
    wsgi_app (str): The WSGI application to run.
    accesslog (str): Access log file; '-' means stdout.
    loglevel (str): Logging level; 'debug' for detailed logs.
    bind (str): Address to bind the server; '0.0.0.0:8000' for all interfaces.
    workers (int): Number of worker processes; calculated based on CPU count.

"""

from os import cpu_count

wsgi_app = "dog_api.wsgi:application"
accesslog = "-"
loglevel = "debug"
bind = "0.0.0.0:8000"
workers = 2 * cpu_count()
