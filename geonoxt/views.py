from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from geonode.celery_app import app as celery_app
import google.auth.transport.requests
import google.oauth2.id_token
import json

AUTHORIZED_AUDIENCE = "https://TU_DOMINIO/geonoxt/ejecutar_task/"
AUTHORIZED_SERVICE_ACCOUNT = "TU_SERVICE_ACCOUNT@TU_PROJECT_ID.iam.gserviceaccount.com"

@csrf_exempt
def ejecutar_task(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Solo POST permitido.')

    # Validar token
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return HttpResponseForbidden('Falta Authorization.')

    token = auth_header.split(' ')[1]
    try:
        request_adapter = google.auth.transport.requests.Request()
        id_info = google.oauth2.id_token.verify_oauth2_token(token, request_adapter, AUTHORIZED_AUDIENCE)

        if id_info['email'] != AUTHORIZED_SERVICE_ACCOUNT:
            return HttpResponseForbidden('Cuenta de servicio no autorizada.')

    except Exception as e:
        return HttpResponseForbidden(f'Error validando token: {str(e)}')

    # Ejecutar task
    try:
        payload = json.loads(request.body)
        task_name = payload['task_name']
        args = payload.get('args', [])
        kwargs = payload.get('kwargs', {})

        task = celery_app.tasks.get(task_name)
        if not task:
            return HttpResponseBadRequest(f'Task {task_name} no encontrada.')

        result = task.run(*args, **kwargs)
        return JsonResponse({"status": "ok", "result": str(result)})

    except Exception as e:
        return HttpResponseBadRequest(f'Error ejecutando task: {str(e)}')
