from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from functools import wraps
from django.db import connections
import logging

logger = logging.getLogger("geonode")


def close_invalid_connections():
    for conn in connections.all():
        try:
            if not conn.in_atomic_block and (
                not conn.connection or (conn.connection.cursor() and not conn.is_usable())
            ):
                conn.close()
        except Exception:
            pass


def verify_google_token(request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return False

    token = auth_header.split(" ")[1]
    logger.info(f"token: {token}")
    try:
        id_info = id_token.verify_oauth2_token(
            token, grequests.Request(), audience=settings.SITEURL.rstrip("/")
        )
        logger.info(f"idinfo: {id_info}")
        if id_info["email"] != settings.GCP_TASKS_SERVICE_ACCOUNT_EMAIL:
            return False
        return True
    except Exception as e:
        logger.error(f"Error verifying token: {e}")
        return False


def require_google_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not verify_google_token(request):
            logger.warning(f"Token inválido o ausente. URL solicitada: {request.path}")
            return HttpResponseForbidden("No autorizado")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def require_post_method(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method != 'POST':
            logger.warning(f"{view_func.__name__}: Invalid method '{request.method}' for URL {request.path}")
            return HttpResponseNotAllowed(['POST'])
        return view_func(request, *args, **kwargs)

    return _wrapped_view
