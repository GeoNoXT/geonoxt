import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from celery import current_app as celery_app
from utils import require_google_token, require_post_method
import json

logger = logging.getLogger(__name__)

@csrf_exempt
@require_post_method
@require_google_token
def run_cloud_task(request):
    try:
        data = json.loads(request.body)

        task_name = data.get('task_name')
        args = data.get('args', [])
        kwargs = data.get('kwargs', {})

        if not task_name:
            return JsonResponse({'error': 'task_name es requerido'}, status=400)

        logger.info(f"Ejecutando tarea {task_name} desde Cloud Task")

        # Buscar la tarea en el registro de Celery
        task = celery_app.tasks.get(task_name)

        if not task:
            logger.error(f"Tarea {task_name} no encontrada en Celery")
            return JsonResponse({'error': f"Tarea {task_name} no encontrada"}, status=404)

        # Ejecutar la tarea como función normal (sin async)
        result = task.run(*args, **kwargs)

        return JsonResponse({'status': 'ok', 'result': str(result)})

    except Exception as e:
        logger.exception(f"Error ejecutando tarea {e}")
        return JsonResponse({'error': str(e)}, status=500)
