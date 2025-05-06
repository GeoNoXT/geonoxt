import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import require_google_token, require_post_method
from django.core.serializers.json import DjangoJSONEncoder
import google.auth
from google.auth.transport.requests import AuthorizedSession
from django.conf import settings
from google.cloud import run_v2
import json

logger = logging.getLogger('geonode')


@csrf_exempt
@require_post_method
@require_google_token
def cloud_task_run_job(request):
    try:
        data = json.loads(request.body)

        task_name = data.get('task_name')
        args = data.get('args', [])
        kwargs = data.get('kwargs', {})

        logger.info(f"Ejecutando tarea {task_name} desde Cloud Task")
        logger.info(f"args {args} desde Cloud Task")
        logger.info(f"kwargs {kwargs} desde Cloud Task")

        if not task_name:
            return JsonResponse({'error': 'task_name es requerido'}, status=400)

        if not isinstance(args, list) or not isinstance(kwargs, dict):
            return JsonResponse({'error': 'args debe ser una lista y kwargs un diccionario'}, status=400)

        logger.info(f"Ejecutando tarea {task_name} desde Cloud Task")

        # Construir el comando a pasar al job
        command = [
            "python",
            "manage.py",
            "run_celery_task",
            task_name,
            *map(str, args),  # convertir todos los args a string
            "--task-kwargs", json.dumps(kwargs)
        ]

        # Lanzar el job
        run_cloud_run_job("geonoxt-django-1", command)

        return JsonResponse({'status': 'job triggered'}, encoder=DjangoJSONEncoder)

    except Exception as e:
        logger.error("Error ejecutando tarea", e)
        return JsonResponse({'error': str(e)}, status=500)


def run_cloud_run_job(job_name, command_override):
    project_id = settings.GCP_TASKS_PROJECT_ID
    region = settings.GCP_REGION

    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    authed_session = AuthorizedSession(credentials)

    client = run_v2.JobsClient()
    parent = f"projects/{project_id}/locations/{region}"
    name = f"{parent}/jobs/{job_name}"

    job_full_name = f"projects/{project_id}/locations/{region}/jobs/{job_name}"
    url = f"https://run.googleapis.com/v2/{job_full_name}:run"

    payload = {
        "overrides": {
            "containerOverrides": [{
                "command": command_override
            }]
        }
    }

    response = authed_session.post(url, json=payload)

    if response.status_code >= 400:
        logger.error(f"Fallo al ejecutar Cloud Run Job: {response.text}")
        raise Exception(f"Error ejecutando job: {response.text}")

    """
    # Lanzar ejecución del Job
    response = client.run_job(
        name=name,
        overrides=run_v2.RunJobRequest.Overrides(
            container_overrides=[
                run_v2.ContainerOverride(
                    command=command_override
                )
            ]
        )
    )
    logger.info(f"Cloud Run Job lanzado: {response.name}")
    """

    logger.info(f"Cloud Run Job lanzado correctamente: {response.json()}")
    return response.json()
