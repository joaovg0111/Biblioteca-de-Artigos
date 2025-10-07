from django.contrib import admin
from django.urls import include, path
from apps.articles import views as article_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", article_views.home_view, name="index"),
    path("accounts/", include("apps.users.urls", namespace="users")),
    path("events/", include("apps.events.urls", namespace="events")),
    path("articles/", include("apps.articles.urls", namespace="articles")),
    
    # --- MUDANÇA: Adicione a URL para o aplicativo de notificações ---
    path("notifications/", include("apps.notifications.urls", namespace="notifications")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)