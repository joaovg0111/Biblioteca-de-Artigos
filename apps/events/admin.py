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
    search_fields = ('name', 'acronym', 'promoting_entity') # 검색 필드 유지
    inlines = [EditionInline]

    # --- CORREÇÃO: Define explicitamente os campos para evitar duplicatas ---
    # 폼에 표시될 필드를 명시적으로 지정합니다.
    fields = ('name', 'acronym', 'promoting_entity', 'full_description', 'website')

    # 'promoting_entity' 필드에 검색 위젯을 적용하여 사용성을 개선합니다.
    # (이 필드가 ForeignKey로 변경될 경우 특히 유용합니다.)
    # raw_id_fields = ('promoting_entity',) # 현재는 CharField이므로 주석 처리

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'event', 'year', 'location')
    list_display_links = ('__str__',)
    list_filter = ('event',)
    search_fields = ('event__acronym', 'location')