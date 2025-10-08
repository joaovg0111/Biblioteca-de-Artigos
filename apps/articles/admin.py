# COPIE E COLE O CONTEÚDO COMPLETO PARA: apps/articles/admin.py

from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from django.db import transaction
from django.forms import formset_factory
from .forms import BibtexUploadForm, ArticlePreviewForm
from .models import Article
<<<<<<< HEAD
from apps.events.models import Event, Edition  # --- MUDANÇA: Importamos os modelos de Eventos
import zipfile
from django.core.files.base import ContentFile
=======
from apps.events.models import Event, Edition
>>>>>>> 5042e0d (entrega final)
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

    def bulk_upload_view(self, request):
<<<<<<< HEAD
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
=======
        ArticleFormSet = formset_factory(ArticlePreviewForm, extra=0)
>>>>>>> 5042e0d (entrega final)
        
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