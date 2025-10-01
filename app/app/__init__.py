from .celery import app as celery_app
from . import celerybeat_schedule  # noqa: F401

__all__ = ('celery_app',)
