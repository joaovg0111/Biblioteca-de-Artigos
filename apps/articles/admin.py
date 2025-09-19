from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'edition', 'authors', 'created_at')
    list_filter = ('edition__event', 'edition__start_date')
    search_fields = ('title', 'authors', 'abstract')
    autocomplete_fields = ['edition']
    date_hierarchy = 'created_at'
