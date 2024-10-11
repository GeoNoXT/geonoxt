from django.urls import path


from .views import UserInfoView, LogoutView

urlpatterns = [
    path("geonoxt/userinfo", UserInfoView.as_view(), name="userinfo"),
    path("geonoxt/logout", LogoutView.as_view(), name="logout"),
]