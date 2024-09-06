from django.urls import path


from .views import UserInfoView

urlpatterns = [
    path("geonuxt/userinfo", UserInfoView.as_view(), name="userinfo"),
    path("geonuxt/logout", UserInfoView.as_view(), name="userinfo"),
]