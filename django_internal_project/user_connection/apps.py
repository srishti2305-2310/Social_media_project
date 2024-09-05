from django.apps import AppConfig
# from utility.scheduler_helper import start_scheduler



class UserConnectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_connection'

class UserConnectionConfig(AppConfig):
    name = 'user_connection'

    def ready(self):
        from utility.scheduler_helper import start_scheduler
        start_scheduler()