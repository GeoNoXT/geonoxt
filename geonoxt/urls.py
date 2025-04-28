from django.urls import path, include
from geonoxt.views import run_cloud_task

urlpatterns = [
    # path("", include("geonoxt.xt_br.urls")),
    # path("", include("geonoxt.xt_geoserver.urls")),
    path('/api/v2/management-tasks/run-task-job/', run_cloud_task, name='run_cloud_task'),
]