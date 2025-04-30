import json
from google.cloud import tasks_v2
from google.protobuf import duration_pb2
from django.conf import settings
from urllib.parse import urljoin
import django.core.serializers.json
import logging

logger = logging.getLogger("geonode")


def create_cloud_task(task_name, args, kwargs, url_path="/api/v2/management-tasks/cloud-task-run-job/"):
    project = settings.GCP_TASKS_PROJECT_ID
    region = settings.GCP_TASKS_REGION
    queue = settings.GCP_TASKS_QUEUE
    url = urljoin(settings.SITEURL, url_path)
    service_account_email = settings.GCP_TASKS_SERVICE_ACCOUNT_EMAIL

    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(project, region, queue)

    payload = {
        "task_name": task_name,
        "args": args,
        "kwargs": kwargs,
    }

    http_request = {
        "http_method": tasks_v2.HttpMethod.POST,
        "url": url,
        "headers": {"Content-type": "application/json"},
        "body": json.dumps(payload, cls=django.core.serializers.json.DjangoJSONEncoder).encode(),
        "oidc_token": {
            "service_account_email": service_account_email,
            "audience": settings.SITEURL.rstrip("/")
        }
    }

    task = {"http_request": http_request}

    try:
        response = client.create_task(request={"parent": parent, "task": task})
        logger.info(f"Task {task_name} encolada correctamente en {response.name}")
        return response
    except Exception as e:
        logger.error(f"Error al crear task {task_name}: {e}")
        raise
