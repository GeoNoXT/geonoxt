from django.urls import path


from .views import UserInfoView, DirectLogoutView

urlpatterns = [
    path("geonuxt/userinfo", UserInfoView.as_view(), name="userinfo"),
    path("geonuxt/logout", DirectLogoutView.as_view(), name="logout"),
]