from django.apps import AppConfig

class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'

    def ready(self):
        # Connect signals here - imports happen AFTER apps are loaded
        import reviews.signals  # This will import and connect signals.py