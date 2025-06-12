#week 6
#app.py file 
from django.apps import AppConfig

class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'  # replace with your app's name

    def ready(self):
        import messaging.signals  # replace with your app's name
