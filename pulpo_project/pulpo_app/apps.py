from django.apps import AppConfig

class PulpoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pulpo_app'

    def ready(self):
        import pulpo_app.signals
