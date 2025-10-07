# CRIE ESTE NOVO ARQUIVO EM: apps/notifications/urls.py

from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path('my-interests/', views.manage_interests_view, name='manage-interests'),
]