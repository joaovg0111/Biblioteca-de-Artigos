# Em apps/articles/admin.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BibtexUploadForm
from .models import Article
# --- MUDANÇA 1: Importe os modelos que vamos precisar ---
from apps.events.models import Author, Edition
import bibtexparser
from bibtexparser.bparser import BibTexParser

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # --- MUDANÇA 2: Corrigido o list_display e melhorado os filtros e busca ---
    list_display = ('title', 'display_authors', 'edition', 'created_at')
    list_filter = ('edition__event', 'edition', 'authors')
    search_fields = ('title', 'authors__name', 'abstract')
    date_hierarchy = 'created_at'
    
    # --- MUDANÇA 3: A nova função para exibir os autores ---
    def display_authors(self, obj):
        """Cria uma string com os nomes dos autores para exibir no admin."""
        return ", ".join([author.name for author in obj.authors.all()])
    display_authors.short_description = 'Autores'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(self.bulk_upload_view), name='articles_article_bulk_upload'),
        ]
        return custom_urls + urls

    def bulk_upload_view(self, request):
        """
        Processa o upload de um arquivo BibTeX para criar múltiplos artigos em massa
        dentro da interface de administração.
        """
        # AVISO: Esta função de bulk upload precisará ser adaptada no futuro
        # para lidar com a criação ou busca de Autores e Edições.
        # Por enquanto, vamos deixá-la como está para não quebrar.
        if request.method == 'POST':
            form = BibtexUploadForm(request.POST, request.FILES)
            if form.is_valid():
                bibtex_file = form.cleaned_data['bibtex_file']
                try:
                    bibtex_str = bibtex_file.read().decode('utf-8')
                    parser = BibTexParser(common_strings=True)
                    bib_database = bibtexparser.loads(bibtex_str, parser=parser)

                    created_count = 0
                    # Esta parte vai dar erro porque 'authors' agora é um ManyToManyField
                    # e 'edition' é um campo obrigatório.
                    # É necessário adaptar esta lógica depois que as migrações funcionarem.
                    for entry in bib_database.entries:
                        # Artigo de exemplo para evitar que o sistema quebre AGORA
                        # self.message_user(request, "FUNCIONALIDADE DE BULK UPLOAD DESATIVADA TEMPORARIAMENTE.", messages.WARNING)
                        pass
                    
                    self.message_user(request, f"ATENÇÃO: A importação em massa precisa ser atualizada para o novo modelo de dados.", messages.WARNING)
                    return redirect('admin:articles_article_changelist')

                except Exception as e:
                    self.message_user(request, f"Ocorreu um erro ao processar o arquivo BibTeX: {e}", messages.ERROR)
        else:
            form = BibtexUploadForm()
        
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['title'] = "Importar Artigos em Massa (BibTeX)"
        context['form'] = form
        return render(request, 'admin/articles/bulk_upload.html', context)
