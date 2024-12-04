# profileapp/apps.py

from django.apps import AppConfig

class ProfileappConfig(AppConfig):
    name = 'profileapp'

    def ready(self):
        import profileapp.signals  # Ensure the signal is imported and connected
