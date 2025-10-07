from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list_view, name="event-list"),
    path('<int:event_id>/', views.event_detail_view, name='event-detail'),
    
    # --- MUDANÇA: Nova URL para a página de detalhes da edição ---
    path('edition/<int:edition_id>/', views.edition_detail_view, name='edition-detail'),
]