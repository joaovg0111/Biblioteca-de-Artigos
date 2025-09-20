from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'authors', 'abstract')
    date_hierarchy = 'created_at'
