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
from django.utils.html import format_html, escape
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
                    created_articles_titles = [] # --- MUDANÇA: Armazena os títulos dos artigos criados
                    skipped_articles = []  # (title, reason) 튜플을 저장

                    for entry in bib_database.entries:
                        # Normaliza os campos para minúsculas para facilitar o acesso
                        entry = {k.lower(): v for k, v in entry.items()}
                        entry_key = entry.get('id') # Ex: 'sbes-paper1'

                        # --- MUDANÇA: Lógica de validação com flag e coleta de todos os erros ---
                        is_valid = True
                        entry_errors = []

                        title = entry.get('title')
                        if not title:
                            is_valid = False
                            entry_errors.append("Título não encontrado.")
                        
                        # Identificador para o relatório de erros, mesmo se o título faltar
                        entry_identifier = title or f"ID: {entry_key or 'desconhecido'}"

                        event_name = entry.get('journal') or entry.get('booktitle')
                        if not event_name:
                            is_valid = False
                            entry_errors.append("Campo 'journal' ou 'booktitle' não encontrado.")

                        year_str = entry.get('year')
                        year = None
                        if not year_str:
                            is_valid = False
                            entry_errors.append("Campo 'year' não encontrado.")
                        else:
                            try:
                                year = int(year_str)
                            except ValueError:
                                is_valid = False
                                entry_errors.append(f"Ano inválido: '{year_str}'.")

                        # Se houver erros de validação, agrupa-os e pula para a próxima entrada
                        if not is_valid:
                            combined_errors = ", ".join(entry_errors)
                            skipped_articles.append((entry_identifier, combined_errors))
                            continue
                        # --- Fim da MUDANÇA na validação ---

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
                            # --- CORREÇÃO: Adiciona 'location' ao critério de busca ---
                            # Isso garante que a busca por uma edição existente seja precisa
                            # e evita erros de integridade ao criar duplicatas.
                            location='A definir',
                            defaults={
                                'end_date': date(year, 12, 31)
                            }
                        )
                        
                        # --- Lógica para Artigo ---
                        # Verifica se o artigo já existe para evitar duplicatas
                        if Article.objects.filter(title__iexact=title, edition=edition).exists():
                            skipped_articles.append((title, "Artigo já existe na base de dados."))
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
                        created_articles_titles.append(new_article.title) # --- MUDANÇA: Adiciona o título à lista

                    # --- Feedback para o Administrador ---
                    if created_count > 0:
                        # --- MUDANÇA: Mensagem de sucesso com títulos em negrito ---
                        success_details = [format_html("<strong>'{}'</strong>", escape(title)) for title in created_articles_titles]
                        message_html = format_html("{} artigo(s) importado(s) com sucesso: {}", created_count, format_html("; ".join(success_details)))
                        messages.add_message(request, messages.SUCCESS, message_html, extra_tags='safe')
                    
                    if skipped_articles:
                        # --- MUDANÇA: Formata a mensagem com HTML para destacar o motivo ---
                        # Usamos format_html para construir uma string HTML segura.
                        # escape() garante que o título do artigo não seja interpretado como HTML.
                        skipped_messages = [format_html("<strong>'{}'</strong> (Motivo: <strong style='color: red;'>{}</strong>)", escape(title), escape(reason)) for title, reason in skipped_articles]
                        message_html = format_html("{} artigo(s) foram ignorados. Detalhes: {}", len(skipped_articles), format_html("<br>".join(skipped_messages)))
                        messages.add_message(request, messages.WARNING, message_html, extra_tags='safe')

                    if created_count == 0 and not skipped_articles:
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