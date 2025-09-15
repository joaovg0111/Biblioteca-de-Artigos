from django.contrib import admin
from .models import Event, Edition

class EditionInline(admin.TabularInline):
    """
    Permite a edição de Edições diretamente na página de detalhe do Evento.
    """
    model = Edition
    extra = 1
    ordering = ('-start_date',)
    fields = ('location', 'website', 'start_date', 'end_date')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'name', 'website')
    search_fields = ('acronym', 'name')
    inlines = [EditionInline]

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('event', 'year', 'location', 'website', 'start_date')
    list_filter = ('event',)
    search_fields = ('event__acronym', 'event__name', 'location', 'website')
    autocomplete_fields = ['event']