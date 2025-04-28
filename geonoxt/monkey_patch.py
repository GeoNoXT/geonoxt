from celery import Celery
from .google_cloud_tasks import create_cloud_task
import os
import json
import logging
from functools import wraps
import sys


logger = logging.getLogger(__name__)
app = Celery("geonode")

_original_apply_async = app.Task.apply_async


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
    # if os.environ.get("EXECUTE_TASKS_INLINE") == "1":
    if 'manage.py' in sys.argv[0]:
        logger.info(f"Ejecutando {task_name} directamente sin pasar por Celery.")
        # Este return está incompleto, debería llamar una ejecución de run job
        # lo que no se es si comprobar primero el estado de la ejecución
        return self.run(*args, **kwargs)

    logger.info(f"Encolando tarea {task_name} en Cloud Tasks.")
    return create_cloud_task(task_name, args, kwargs, "/api/v2/management-tasks/run-task-job/")


def celery2googlecloud():
    """
    Aplica el monkey patch global de apply_async de todas las tareas Celery.
    """
    app.Task.apply_async = patched_apply_async_celery2googlecloud
    logger.info("Celery Tasks parcheadas para usar Cloud Tasks.")

