from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BibtexUploadForm
from .models import Article
import bibtexparser
from bibtexparser.bparser import BibTexParser

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'authors', 'abstract')
    date_hierarchy = 'created_at'
    
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
        if request.method == 'POST':
            form = BibtexUploadForm(request.POST, request.FILES)
            if form.is_valid():
                bibtex_file = form.cleaned_data['bibtex_file']
                try:
                    bibtex_str = bibtex_file.read().decode('utf-8')
                    parser = BibTexParser(common_strings=True)
                    bib_database = bibtexparser.loads(bibtex_str, parser=parser)

                    created_count = 0
                    for entry in bib_database.entries:
                        Article.objects.create(
                            submitter=request.user,
                            title=entry.get('title', 'Título não especificado'),
                            authors=entry.get('author', 'Autores não especificados'),
                            abstract=entry.get('abstract', '')
                        )
                        created_count += 1
                    
                    self.message_user(request, f"{created_count} artigos foram importados com sucesso.", messages.SUCCESS)
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
