from django.urls import path
from . import views

# This is important for namespacing URLs
app_name = "users"

urlpatterns = [
    # The URL for the signup page will be /accounts/signup/
    path("signup/", views.signup_view, name="signup"),
    
    # The URL for the login page will be /accounts/login/
    path("login/", views.login_view, name="login"),
    
    # THIS IS THE NEW LINE:
    # The URL for the logout action will be /accounts/logout/
    path("logout/", views.logout_view, name="logout"),
]