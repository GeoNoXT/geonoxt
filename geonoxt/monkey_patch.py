from geonode.celery_app import app
from .google_cloud_tasks import create_cloud_task
import logging
import sys

logger = logging.getLogger('geonode')


def patched_apply_async_celery2googlecloud(self, args=None, kwargs=None, **options):
    """
    Patch global para interceptar todas las llamadas a Celery Tasks.
    """
    task_name = self.name

    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
        if options:
            kwargs.update(options)

    # Detecta si estamos en modo "directo" (por ejemplo un management command)
    if 'manage.py' in sys.argv[0]:
        logger.info(f"Ejecutando {task_name} directamente sin pasar por Celery.")
        return self.run(*args, **kwargs)

    logger.info(f"Encolando tarea {task_name} en Cloud Tasks.")
    return create_cloud_task(task_name, args, kwargs, "/api/v2/management-tasks/run-task-job/")


def celery2googlecloud():
    """
    Aplica el monkey patch global de apply_async de todas las tareas Celery registradas.
    """
    # Obtener todas las tareas registradas en Celery
    registered_tasks = app.tasks

    # Aplicar el patch a todas las tareas registradas
for task_name, task in registered_tasks.items():
    # Parchear la tarea
    task.apply_async = patched_apply_async_celery2googlecloud
    logger.info(f"Tarea {task_name} parcheada para usar Cloud Tasks.")
