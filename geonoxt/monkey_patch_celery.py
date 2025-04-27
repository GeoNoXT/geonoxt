from geonode.celery_app import app  # Ojo: importa bien tu instancia de Celery
from geonoxt.cloud_tasks import create_cloud_task

from celery import Task
original_apply_async = Task.apply_async


def cloud_tasks_apply_async(self, args=None, kwargs=None, **options):
    if should_use_cloud_tasks():
        enqueue_in_cloud_tasks(self.name, args=args, kwargs=kwargs)
    else:
        return original_apply_async(self, args=args, **options)


def patch_celery():
    Task.apply_async = cloud_tasks_apply_async


def should_use_cloud_tasks():
    # Aquí decides si usas Cloud Tasks, por ejemplo según settings
    from django.conf import settings
    return getattr(settings, 'USE_CLOUD_TASKS', False)


def monkey_patch_celery_tasks():
    def should_patch_task(taskname):
        # Solo parchear tareas propias, evitar las del sistema
        # Puedes ajustar los prefijos que aceptas
        VALID_PREFIXES = [
            'geonode.tasks.',
            'geonode.harvesting.',  # si quieres incluir harvesting
            'geonode.other_custom_module.',  # otro módulo propio que uses
        ]

        # Lista de tareas que nunca debes parchear
        EXCLUDED_TASKS = [
            'celery.backend_cleanup',
            'celery.chord_unlock',
        ]

        if taskname in EXCLUDED_TASKS:
            return False

        return any(taskname.startswith(prefix) for prefix in VALID_PREFIXES)

    for task_name, task in app.tasks.items():
        if should_patch_task(task_name):
            print(f"[geonoxt] Monkey-patcheando {task_name}")
            task.apply_async = create_cloud_task(task)

