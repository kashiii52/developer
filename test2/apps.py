from django.apps import AppConfig


class test2Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "test2"
    
    def ready(self):
        import test2.signals
