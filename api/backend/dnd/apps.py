from django.apps import AppConfig


class DNDConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dnd'

    def ready(self):
        import dnd.signals
