from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("registration/", views.registration, name="registration"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_user, name="logout"),
    path("reset_password/", views.reset_password_user, name="reset_password"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("activate_email/",views.resend_email,name="activate_email"),
    # Settings
    path("settings/profile", views.settings_profile_user, name="settings_profile"),
    path("settings/security", views.settings_security_user, name="settings_security"),
    path("settings/notifications", views.settings_notifications_user, name="settings_notifications"),
    path("settings/billing", views.settings_billing_user, name="settings_billing"),
]
