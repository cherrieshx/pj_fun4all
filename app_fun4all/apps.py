from django.apps import AppConfig


class AppFun4AllConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_fun4all'

    def ready(self):
        import app_fun4all.signals  # Registra i segnali all'avvio dell'applicazione
