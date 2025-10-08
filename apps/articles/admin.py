# COPIE E COLE O CONTEÚDO COMPLETO PARA: apps/articles/admin.py

from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from django.db import transaction
from django.forms import formset_factory
from .forms import BibtexUploadForm, ArticlePreviewForm
from .models import Article
from apps.events.models import Event, Edition
import bibtexparser
from bibtexparser.bparser import BibTexParser
from datetime import date

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'keywords', 'edition', 'created_at')
    list_filter = ('edition', 'created_at',)
    search_fields = ('title', 'authors', 'abstract', 'keywords')
    date_hierarchy = 'created_at'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(self.bulk_upload_view), name='articles_article_bulk_upload'),
        ]
        return custom_urls + urls

    def bulk_upload_view(self, request):
        ArticleFormSet = formset_factory(ArticlePreviewForm, extra=0)
        
        if request.method == 'POST':
            # Etapa 2: Processando o formulário de revisão que o usuário submeteu
            if 'confirm_import' in request.POST:
                formset = ArticleFormSet(request.POST)
                if formset.is_valid():
                    created_count = 0
                    with transaction.atomic():
                        for form_data in formset.cleaned_data:
                            if form_data.get('import_this'):
                                title = form_data.get('title')
                                event_name = form_data.get('booktitle')
                                year_str = form_data.get('year')
                                edition = None
                                
                                if event_name and year_str:
                                    try:
                                        year = int(year_str)
                                        event, _ = Event.objects.get_or_create(name=event_name, defaults={'acronym': "".join(word[0] for word in event_name.split()[:4]).upper()})
                                        edition, _ = Edition.objects.get_or_create(event=event, start_date=date(year, 1, 1), defaults={'location': form_data.get('location', 'A definir'), 'end_date': date(year, 12, 31)})
                                    except (ValueError, TypeError):
                                        continue
                                
                                if not Article.objects.filter(title__iexact=title, edition=edition).exists():
                                    Article.objects.create(
                                        title=title,
                                        authors=form_data.get('authors'),
                                        keywords=form_data.get('keywords', ''),
                                        abstract=form_data.get('abstract', ''),
                                        pages=form_data.get('pages', ''),
                                        location=form_data.get('location', ''),
                                        publisher=form_data.get('publisher', ''),
                                        edition=edition,
                                        submitter=request.user
                                    )
                                    created_count += 1

                    self.message_user(request, f"{created_count} artigo(s) importado(s) com sucesso.")
                    return redirect('admin:articles_article_changelist')
                else:
                    # --- CORREÇÃO: Re-renderizar a página de preview com os erros ---
                    # Em vez de redirecionar, mostramos o formulário novamente para que o usuário possa corrigir.
                    reconstructed_data_for_template = []
                    for form in formset:
                        # Recria o dicionário 'initial' para o template a partir dos dados do POST
                        data_dict = {key.split('-')[-1]: value for key, value in form.data.items() if key.startswith(form.prefix)}
                        # Adiciona os erros de validação específicos deste formulário ao dicionário
                        data_dict['validation_errors'] = [msg for error_list in form.errors.values() for msg in error_list]
                        reconstructed_data_for_template.append(data_dict)

                    messages.error(request, "Por favor, corrija os erros nos artigos selecionados antes de continuar.")

                    context = self.admin_site.each_context(request)
                    context['opts'] = self.model._meta
                    context['title'] = "Revisar Artigos para Importação"
                    context['formset'] = formset # O formset com os erros
                    context['parsing_errors'] = []
                    # Combina o formset (com erros) e os dados reconstruídos para o template
                    context['initial_data_with_errors'] = zip(formset, reconstructed_data_for_template)
                    return render(request, "admin/articles/bulk_upload_preview.html", context)
            
            # Etapa 1: Processando o upload inicial do BibTeX
            else:
                form = BibtexUploadForm(request.POST, request.FILES)
                if form.is_valid():
                    bibtex_file = form.cleaned_data.get('bibtex_file')
                    bibtex_text = form.cleaned_data.get('bibtex_text')
                    bibtex_str = bibtex_file.read().decode('utf-8') if bibtex_file else bibtex_text
                    
                    initial_data = []
                    parsing_errors = []
                    try:
                        bib_database = bibtexparser.loads(bibtex_str, parser=BibTexParser(common_strings=True))
                        for entry in bib_database.entries:
                            entry_data = {k.lower(): v for k, v in entry.items()}
                            
                            data_for_form = {
                                'title': entry_data.get('title', ''),
                                'authors': ' and '.join(entry_data.get('author', '').replace('\n', ' ').split(' and ')),
                                'year': entry_data.get('year', ''),
                                'booktitle': entry_data.get('journal', '') or entry_data.get('booktitle', ''),
                                'keywords': entry_data.get('keywords', ''),
                                'abstract': entry_data.get('abstract', ''),
                                'pages': entry_data.get('pages', ''),
                                'location': entry_data.get('location', ''),
                                'publisher': entry_data.get('publisher', ''),
                                'validation_errors': []
                            }

                            if not data_for_form['title']: data_for_form['validation_errors'].append("Título é obrigatório.")
                            if not data_for_form['authors']: data_for_form['validation_errors'].append("Autores são obrigatórios.")
                            if not data_for_form['year']: data_for_form['validation_errors'].append("Ano é obrigatório.")
                            if not data_for_form['booktitle']: data_for_form['validation_errors'].append("Journal/Booktitle é obrigatório.")
                            
                            data_for_form['import_this'] = not data_for_form['validation_errors']
                            initial_data.append(data_for_form)

                    except Exception as e:
                        parsing_errors.append(f"Erro crítico ao processar o BibTeX: {e}")

                    formset = ArticleFormSet(initial=[d for d in initial_data])
                    context = self.admin_site.each_context(request)
                    context['opts'] = self.model._meta
                    context['title'] = "Revisar Artigos para Importação"
                    context['formset'] = formset
                    context['parsing_errors'] = parsing_errors
                    context['initial_data_with_errors'] = zip(formset, initial_data)
                    return render(request, "admin/articles/bulk_upload_preview.html", context)
                # Se o formulário inicial for inválido, a execução continua para baixo, onde o formulário com erros será renderizado.

        # Este bloco lida com requisições GET ou com POSTs inválidos da Etapa 1
        form = BibtexUploadForm() if request.method == 'GET' else form

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['title'] = "Importar Artigos em Massa (BibTeX)"
        context['form'] = form
        return render(request, 'admin/articles/bulk_upload.html', context)