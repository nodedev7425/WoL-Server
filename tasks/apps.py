from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'tasks'

    def ready(self):
        if "runserver" not in sys.argv:
            return

        from .tasks import start_tasks
        start_tasks()



