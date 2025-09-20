from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, BibtexUploadForm
from .models import Article
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404
from django.utils.text import slugify 
import bibtexparser
from bibtexparser.bparser import BibTexParser
import os

@staff_member_required
def article_upload_view(request):
    """
    Exibe o formulário de upload de artigos e processa os dados submetidos.
    Apenas para administradores (staff).
    """
    if request.method == 'POST':
        # Passa request.FILES para lidar com os dados do arquivo.
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.submitter = request.user
            # Se um arquivo foi enviado, armazena seu nome original
            if 'pdf_file' in request.FILES:
                article.original_filename = request.FILES['pdf_file'].name
            article.save()
            form.save_m2m() # Necessário para relações ManyToMany, boa prática manter.
            messages.success(request, "Artigo enviado com sucesso.")
            return redirect('index') # Redireciona para a página inicial após o upload
    else:
        form = ArticleForm()
    return render(request, 'articles/article_form.html', {'form': form})

def article_search_view(request):
    """
    Busca artigos com base em uma consulta do usuário.
    A busca é feita nos campos de título, autores e resumo.
    """
    query = request.GET.get('q')
    results = []
    if query:
        # Usando Q objects para criar uma consulta OR complexa
        results = Article.objects.filter(
            Q(title__icontains=query) |
            Q(authors__icontains=query) |
            Q(abstract__icontains=query)
        ).distinct()

    context = {'query': query, 'results': results}
    return render(request, 'articles/article_search_results.html', context)

@staff_member_required
def bulk_article_upload_view(request):
    """
    Processa o upload de um arquivo BibTeX para criar múltiplos artigos em massa.
    Apenas para administradores (staff).
    """
    if request.method == 'POST':
        form = BibtexUploadForm(request.POST, request.FILES)
        if form.is_valid():
            bibtex_file = form.cleaned_data['bibtex_file']

            try:
                # O arquivo precisa ser decodificado para string
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
                messages.success(request, f"{created_count} artigos foram importados com sucesso.")
                return redirect('index')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao processar o arquivo BibTeX: {e}")
    else:
        form = BibtexUploadForm()
    
    return render(request, 'articles/bulk_article_upload.html', {'form': form})

def download_pdf_view(request, article_id):
    """
    Força o download de um arquivo PDF com seu nome original ou um nome derivado do título.
    """
    article = get_object_or_404(Article, pk=article_id)
    if not article.pdf_file:
        raise Http404("Nenhum arquivo PDF associado a este artigo.")

    # Define o nome do arquivo para download
    if article.original_filename:
        download_filename = article.original_filename
    else:
        # Cria um nome de arquivo a partir do título se o original não existir
        download_filename = f"{slugify(article.title)}.pdf"

    # Abre o arquivo e o serve como uma resposta HTTP
    try:
        with open(article.pdf_file.path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            # Define o cabeçalho Content-Disposition para forçar o download com o nome correto
            response['Content-Disposition'] = f'attachment; filename="{download_filename}"'
            return response
    except FileNotFoundError:
        raise Http404("Arquivo PDF não encontrado no servidor.")

@login_required
def my_articles_view(request):
    """
    Exibe uma lista de artigos que o usuário logado enviou.
    """
    articles = Article.objects.filter(submitter=request.user).order_by('-created_at')
    return render(request, 'articles/my_articles.html', {'articles': articles})

@login_required
def article_edit_view(request, article_id):
    """
    Permite que o autor de um artigo o edite.
    """
    article = get_object_or_404(Article, pk=article_id, submitter=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            edited_article = form.save(commit=False)
            if 'pdf_file' in request.FILES:
                edited_article.original_filename = request.FILES['pdf_file'].name
            edited_article.save()
            form.save_m2m()
            messages.success(request, "Artigo atualizado com sucesso.")
            return redirect('articles:my-articles')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article_form.html', {'form': form, 'is_editing': True})

@login_required
def article_delete_view(request, article_id):
    """
    Permite que o autor de um artigo o exclua após a confirmação.
    """
    article = get_object_or_404(Article, pk=article_id, submitter=request.user)
    if request.method == 'POST':
        article.delete()
        messages.success(request, "Artigo excluído com sucesso.")
        return redirect('articles:my-articles')
    return render(request, 'articles/article_confirm_delete.html', {'article': article})