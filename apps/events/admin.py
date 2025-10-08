from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Event, Edition

class EditionInline(admin.TabularInline):
    """
    Mostra as edições de um evento como uma lista somente leitura,
    com links para editar ou remover cada uma.
    """
    model = Edition
    template = 'admin/events/edition/tabular_inline_with_delete_button.html'

    # 1. Definimos os campos que queremos exibir e torná-los 'readonly'.
    fields = ('edition_link', 'location', 'website', 'start_date', 'end_date')
    readonly_fields = ('edition_link', 'location', 'website', 'start_date', 'end_date')

    # --- A SOLUÇÃO DEFINITIVA ---
    # 2. Desativamos todas as permissões de modificação para este inline.
    #    Isso diz ao Django para não tentar validar este formulário no POST.
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    # ---------------------------

    def edition_link(self, instance):
        if instance.pk:
            url = reverse('admin:events_edition_change', args=[instance.pk])
            return format_html('<a href="{}">{}</a>', url, str(instance))
        return "N/A"
    edition_link.short_description = 'Edição'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'name', 'promoting_entity')
    search_fields = ('name', 'acronym', 'promoting_entity')
    inlines = [EditionInline] 

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'event', 'year', 'location')
    list_display_links = ('__str__',)
    list_filter = ('event',)
    search_fields = ('event__acronym', 'location')