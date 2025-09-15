from django.contrib import admin
from .models import Event, Edition

class EditionInline(admin.TabularInline):
    """
    Permite a edição de Edições diretamente na página de detalhe do Evento.
    """
    model = Edition
    extra = 1  # Mostra um campo de edição extra por defeito
    ordering = ('-year',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'name')
    search_fields = ('acronym', 'name')
    # Adiciona a gestão de edições inline à página do Evento
    inlines = [EditionInline]

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('event', 'year', 'location', 'start_date')
    list_filter = ('event', 'year')
    search_fields = ('event__acronym', 'event__name', 'year', 'location')
    autocomplete_fields = ['event']
