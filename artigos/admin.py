
from django.contrib import admin
from .models import Artigo
@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo','autores','criado_em')
    search_fields = ('titulo','autores')
    list_filter = ('criado_em',)
