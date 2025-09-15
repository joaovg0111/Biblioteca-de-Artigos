from django.contrib import admin
from django.urls import include, path
from apps.core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", core_views.index, name="index"),
    path("accounts/", include("apps.users.urls", namespace="users")),
    path("events/", include("apps.events.urls", namespace="events")),
]
