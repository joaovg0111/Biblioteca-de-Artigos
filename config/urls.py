from django.contrib import admin
from django.urls import include, path
from apps.core import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", core_views.index, name="index"),
    path("accounts/", include("apps.users.urls", namespace="users")),
    path("events/", include("apps.events.urls", namespace="events")),
    path("articles/", include("apps.articles.urls", namespace="articles")),
]

# Configuração para servir arquivos de mídia enviados pelo usuário em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
