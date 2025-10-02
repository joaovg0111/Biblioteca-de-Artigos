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
    list_display = ('acronym', 'name')
    search_fields = ('name', 'acronym')

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'event', 'year', 'location')
    list_filter = ('event',)
    search_fields = ('event__acronym', 'location')