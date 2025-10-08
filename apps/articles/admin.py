# COPIE E COLE O CONTEÚDO COMPLETO PARA: apps/articles/admin.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .forms import BibtexUploadForm
from .models import Article
from apps.events.models import Event, Edition  # --- MUDANÇA: Importamos os modelos de Eventos
import zipfile
from django.core.files.base import ContentFile
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

    @transaction.atomic
    def bulk_upload_view(self, request):
        """
        Processa o upload de um arquivo BibTeX para criar múltiplos artigos em massa,
        encontrando ou criando Eventos e Edições de forma inteligente.
        """
        if request.method == 'POST':
            form = BibtexUploadForm(request.POST, request.FILES)
            if form.is_valid():
                # --- MUDANÇA: Processa os dois arquivos do formulário ---
                bibtex_file = form.cleaned_data['bibtex_file']
                pdf_zip_file = form.cleaned_data.get('pdf_zip_file') # Opcional
                
                pdf_files = {}
                if pdf_zip_file:
                    try:
                        with zipfile.ZipFile(pdf_zip_file, 'r') as zf:
                            for filename in zf.namelist():
                                if filename.lower().endswith('.pdf'):
                                    pdf_files[filename] = zf.read(filename)
                    except zipfile.BadZipFile:
                        self.message_user(request, "O arquivo ZIP com os PDFs é inválido.", messages.ERROR)
                        return redirect('.')

                try:
                    bibtex_str = bibtex_file.read().decode('utf-8')
                    parser = BibTexParser(common_strings=True)
                    bib_database = bibtexparser.loads(bibtex_str, parser=parser)

                    created_count = 0
                    skipped_count = 0
                    failed_entries = []
                    skipped_entries = []

                    for entry in bib_database.entries:
                        # Normaliza os campos para minúsculas para facilitar o acesso
                        entry = {k.lower(): v for k, v in entry.items()}
                        entry_key = entry.get('id') # Ex: 'sbes-paper1'

                        title = entry.get('title')
                        if not title:
                            failed_entries.append(f"Entrada sem título: {entry.get('id', 'ID desconhecido')}")
                            continue

                        # --- Lógica para Evento e Edição ---
                        event_name = entry.get('journal') or entry.get('booktitle')
                        year_str = entry.get('year')

                        if not event_name or not year_str:
                            failed_entries.append(f"Artigo '{title}' (ID: {entry_key}) sem 'journal'/'booktitle' ou 'year'.")
                            continue
                        
                        try:
                            year = int(year_str)
                        except ValueError:
                            failed_entries.append(f"Artigo '{title}' (ID: {entry_key}) com ano inválido: '{year_str}'.")
                            continue

                        # Encontra ou cria o Evento
                        event, _ = Event.objects.get_or_create(
                            name=event_name,
                            defaults={
                                'acronym': "".join(word[0] for word in event_name.split()[:4]).upper(),
                                'full_description': f"Evento '{event_name}' criado automaticamente via importação BibTeX."
                            }
                        )

                        # Encontra ou cria a Edição
                        edition, _ = Edition.objects.get_or_create(
                            event=event,
                            start_date=date(year, 1, 1), # Data padrão para o ano
                            defaults={
                                'location': 'A definir',
                                'end_date': date(year, 12, 31)
                            }
                        )
                        
                        # --- Lógica para Artigo ---
                        # Verifica se o artigo já existe para evitar duplicatas
                        if Article.objects.filter(title__iexact=title, edition=edition).exists():
                            skipped_entries.append(f"'{title}' (ID: {entry_key})")
                            continue

                        # Formata os autores
                        authors_list = [author.strip() for author in entry.get('author', '').replace('\n', ' ').split(' and ')]
                        authors_str = ", ".join(filter(None, authors_list))
                        
                        # Formata as palavras-chave
                        keywords_str = entry.get('keywords', '')

                        # Cria o objeto Artigo
                        new_article = Article(
                            title=title,
                            authors=authors_str,
                            keywords=keywords_str,
                            abstract=entry.get('abstract', ''),
                            edition=edition,
                            submitter=request.user # Associa o artigo ao admin que fez o upload
                        )

                        # --- MUDANÇA: Lógica para anexar o PDF (se existir) ---
                        if entry_key and pdf_files:
                            pdf_filename_to_find = f"{entry_key}.pdf"
                            if pdf_filename_to_find in pdf_files:
                                pdf_content = pdf_files[pdf_filename_to_find]
                                new_article.pdf_file.save(pdf_filename_to_find, ContentFile(pdf_content), save=False)
                                new_article.original_filename = pdf_filename_to_find

                        new_article.save()
                        created_count += 1

                    # --- Feedback para o Administrador ---
                    if created_count > 0:
                        self.message_user(request, f"{created_count} artigo(s) importado(s) com sucesso.", messages.SUCCESS)
                    if skipped_entries:
                        self.message_user(request, f"{len(skipped_entries)} artigo(s) já existiam e foram ignorados: {'; '.join(skipped_entries)}", messages.INFO)
                    if failed_entries:
                        self.message_user(request, f"Falha ao importar {len(failed_entries)} entrada(s). Detalhes: {'; '.join(failed_entries)}", messages.WARNING)
                    if created_count == 0 and not skipped_entries and not failed_entries:
                         self.message_user(request, "Nenhum novo artigo encontrado no arquivo.", messages.WARNING)

                    return redirect('admin:articles_article_changelist')

                except Exception as e:
                    self.message_user(request, f"Ocorreu um erro crítico ao processar o arquivo BibTeX: {e}", messages.ERROR)
        else:
            form = BibtexUploadForm()
        
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['title'] = "Importar Artigos em Massa (BibTeX)"
        context['form'] = form
        return render(request, 'admin/articles/bulk_upload.html', context)