from django.apps import AppConfig


class AdminPConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_p'

    def ready(self):
        from . import signals
