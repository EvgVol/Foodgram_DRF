from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Конфигурация приложения API."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'API'
