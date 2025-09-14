from django.urls import path
from . import views

# This is important for namespacing URLs
app_name = "users"

urlpatterns = [
    # The URL for the signup page will be /accounts/signup/
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
]
