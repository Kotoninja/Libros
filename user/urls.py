from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("registration/", views.registration, name="registration"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_user, name="logout"),
    path("settings/", views.settings_user, name="settings"),
]
