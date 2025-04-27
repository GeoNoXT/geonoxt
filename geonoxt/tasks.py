import json
from google.cloud import tasks_v2
from google.protobuf import duration_pb2
from django.conf import settings
from urllib.parse import urljoin
import logging

logger = logging.getLogger("geonode")


def create_cloud_task(task_name, payload, url_path, dispatch_deadline=None):
    project = settings.GCP_TASKS_PROJECT_ID
    region = settings.GCP_TASKS_REGION
    queue = settings.GCP_TASKS_QUEUE
    url = urljoin(settings.SITEURL, url_path)
    service_account_email = settings.GCP_TASKS_SERVICE_ACCOUNT_EMAIL

    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(project, region, queue)

    http_request = {
        "http_method": tasks_v2.HttpMethod.POST,
        "url": url,
        "headers": {"Content-type": "application/json"},
        "body": json.dumps(payload).encode(),
        "oidc_token": {
            "service_account_email": service_account_email,
            "audience": settings.SITEURL.rstrip("/")
        }
    }

    task = tasks_v2.Task(http_request=http_request)

    if dispatch_deadline:
        deadline = duration_pb2.Duration()
        deadline.FromSeconds(dispatch_deadline)
        task.dispatch_deadline.CopyFrom(deadline)

    response = client.create_task(parent=parent, task=task)
    logger.info(f"Tarea {task_name} creada: {response.name}")
    return response
