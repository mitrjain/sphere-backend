from django.apps import AppConfig


class SphereBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sphere_backend'

    def ready(self):
        from .management.commands.process_transactions import Command
        Command().handle()
