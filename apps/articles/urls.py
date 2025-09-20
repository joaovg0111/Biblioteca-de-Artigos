from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    # Adiciona o padrão de URL para /articles/upload/
    path("upload/", views.article_upload_view, name="article-upload"),
    path("search/", views.article_search_view, name="article-search"),
    path("bulk-upload/", views.bulk_article_upload_view, name="bulk-article-upload"),
    path("download/<int:article_id>/", views.download_pdf_view, name="download-pdf"),
    path("my-articles/", views.my_articles_view, name="my-articles"),
    path("edit/<int:article_id>/", views.article_edit_view, name="article-edit"),
    path("delete/<int:article_id>/", views.article_delete_view, name="article-delete"),
]