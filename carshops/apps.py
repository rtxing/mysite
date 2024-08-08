from django.apps import AppConfig


class CarshopsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carshops'

    def ready(self):
        import carshops.signals

