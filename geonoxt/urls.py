from django.urls import path, include
from geonoxt.views import cloud_task_run_job

urlpatterns = [
    # path("", include("geonoxt.xt_br.urls")),
    # path("", include("geonoxt.xt_geoserver.urls")),
    path('/api/v2/management-tasks/cloud-task-run-job/', cloud_task_run_job, name='cloud-task-run-job'),
]