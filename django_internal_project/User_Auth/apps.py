from django.apps import AppConfig
# from utility.scheduler_helper import start_scheduler


class UserAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'User_Auth'

class UserAuthConfig(AppConfig):
    name = 'User_Auth'

    def ready(self):
        from utility.scheduler_helper import start_scheduler
        start_scheduler()

