from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    # Adiciona o padrão de URL para /articles/upload/
    path("upload/", views.article_upload_view, name="article-upload"),
    path("search/", views.article_search_view, name="article-search"),
]