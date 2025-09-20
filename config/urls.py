from django.contrib import admin
from django.urls import include, path
from apps.articles import views as article_views  # Importa as views de articles
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", article_views.home_view, name="index"),  # Aponta a raiz para a home_view
    path("accounts/", include("apps.users.urls", namespace="users")),
    path("events/", include("apps.events.urls", namespace="events")),
    path("articles/", include("apps.articles.urls", namespace="articles")),
]

# Configuração para servir arquivos de mídia enviados pelo usuário em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
