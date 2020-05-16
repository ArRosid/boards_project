from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from accounts.views import signup


app_name = "accounts"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "login/", LoginView.as_view(template_name="accounts/login.html"), name="login"
    ),
]
