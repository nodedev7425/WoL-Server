import sys

from django.apps import AppConfig
from django.core.cache import cache

class TasksConfig(AppConfig):
    name = 'tasks'

    def ready(self):
        if "runserver" not in sys.argv:
            return

        cache.clear()

        from .tasks import start_tasks

        start_tasks()



