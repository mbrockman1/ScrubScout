# reviews/apps.py
from django.apps import AppConfig

class ReviewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reviews"

    def ready(self):
        # Ensure this is the single source of truth for review signals
        from . import signals  # noqa: F401