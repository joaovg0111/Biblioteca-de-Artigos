from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    # Adiciona o padrão de URL para /articles/upload/
    path("", views.article_list_view, name="article-list"),
    path("add-options/", views.add_article_options_view, name="add-article-options"),
    path("search/", views.article_search_view, name="article-search"),
    path('<int:article_id>/', views.article_detail_view, name='article-detail'),
    path("download/<int:article_id>/", views.download_pdf_view, name="download-pdf"),
    path("my-articles/", views.my_articles_view, name="my-articles"),
    path("edit/<int:article_id>/", views.article_edit_view, name="article-edit"),
    path("delete/<int:article_id>/", views.article_delete_view, name="article-delete"),
]