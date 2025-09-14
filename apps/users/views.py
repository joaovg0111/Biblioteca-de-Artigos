from django.shortcuts import render

def signup_view(request):
    """
    This view renders the user registration page.
    """
    return render(request, "registration/signup.html")

def login_view(request):
    """
    This view renders the user login page.
    """
    return render(request, "registration/login.html")

