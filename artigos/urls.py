
from django.urls import path
from .views import ListaArtigosView, upload_artigo, download_artigo
urlpatterns = [
    path('', ListaArtigosView.as_view(), name='lista_artigos'),
    path('upload/', upload_artigo, name='upload_artigo'),
    path('download/<int:pk>/', download_artigo, name='download_artigo'),
]
