from django.urls import path


from .views import UserInfoView, LogoutView

urlpatterns = [
    path("geonuxt/userinfo", UserInfoView.as_view(), name="userinfo"),
    path("geonuxt/logout", LogoutView.as_view(), name="logout"),
]