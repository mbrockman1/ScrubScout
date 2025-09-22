from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Intentionally do NOT import accounts.signals here.
        # Review-related signals live in reviews.signals.
        pass