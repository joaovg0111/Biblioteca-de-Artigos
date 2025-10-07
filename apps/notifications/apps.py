# CRIE ESTE NOVO ARQUIVO EM: apps/notifications/apps.py

from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.notifications'

    def ready(self):
        # Importa os sinais para que eles sejam registrados quando o aplicativo iniciar
        import apps.notifications.signals