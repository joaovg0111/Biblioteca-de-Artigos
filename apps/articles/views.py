from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from apps.events.models import Event
from .forms import ArticleForm, BibtexUploadForm
from .models import Article
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404
from django.utils.text import slugify 
import bibtexparser
from bibtexparser.bparser import BibTexParser
import os


def home_view(request):
    """
    Exibe a página inicial, incluindo uma lista dos 5 artigos mais recentes.
    """
    recent_articles = Article.objects.order_by('-created_at')[:3]
    recent_events = Event.objects.order_by('-id')[:4]  # Pega os 4 eventos mais recentes
    context = {
        'recent_articles': recent_articles,
        'recent_events': recent_events,
    }
    return render(request, 'home/index.html', context)

def add_article_options_view(request):
    """
    Exibe uma página para administradores escolherem como adicionar artigos:
    individualmente ou em massa via BibTeX.
    """
    return render(request, 'articles/add_article_options.html')

def article_list_view(request):
    """
    Exibe uma lista paginada de todos os artigos.
    """
    article_list = Article.objects.order_by('-created_at')
    paginator = Paginator(article_list, 10)  # Mostra 10 artigos por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'articles/article_list.html', context)

def article_search_view(request):
    query = request.GET.get('q')
    articles = Article.objects.none()

    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(authors__icontains=query) |  # <-- Buscando em um campo de texto
            Q(edition__event__name__icontains=query) |
            Q(edition__event__acronym__iexact=query)
        ).distinct()

    context = {
        'query': query,
        'articles': articles
    }
    return render(request, 'articles/article_search_results.html', context)

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
@login_required
def my_articles_view(request):
    """
    Exibe uma lista de artigos que o usuário logado enviou,
    agrupados por ano de criação.
    """
    # Filtra os artigos do usuário logado e ordena do mais recente para o mais antigo
    articles_list = Article.objects.filter(submitter=request.user).order_by('-created_at')
    
    # Cria um dicionário para agrupar os artigos por ano
    articles_by_year = {}
    for article in articles_list:
        year = article.created_at.year
        if year not in articles_by_year:
            articles_by_year[year] = []
        articles_by_year[year].append(article)
        
    context = {
        'articles_by_year': articles_by_year,
    }
    return render(request, 'articles/my_articles.html', context)

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

def article_detail_view(request, article_id):
    """
    Esta view busca um único artigo pelo seu ID e o exibe em uma página de detalhes.
    """
    # Busca o artigo pelo ID ou retorna um erro 404 (Página não encontrada)
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article
    }
    return render(request, 'articles/article_detail.html', context)

def author_list_view(request):
    """
    Cria uma lista de todos os autores únicos a partir do campo de texto 'authors'
    de todos os artigos.
    """
    # Usamos values_list para pegar apenas o campo 'authors' e flat=True para obter uma lista de strings
    all_authors_strings = Article.objects.values_list('authors', flat=True)
    
    unique_authors = set()
    for author_string in all_authors_strings:
        # Divide a string de autores por vírgula e remove espaços em branco
        authors = [name.strip() for name in author_string.split(',') if name.strip()]
        unique_authors.update(authors)
    
    # Converte o conjunto para uma lista e ordena em ordem alfabética
    sorted_authors = sorted(list(unique_authors))
    
    context = {
        'authors': sorted_authors
    }
    return render(request, 'articles/author_list.html', context)


def author_detail_view(request, author_name):
    """
    Exibe uma lista de todos os artigos que contêm o nome do autor especificado
    em seu campo 'authors'.
    """
    # Filtra artigos onde o campo 'authors' contém o nome do autor
    # A busca é case-insensitive (não diferencia maiúsculas de minúsculas)
    articles_by_author = Article.objects.filter(authors__icontains=author_name).order_by('-created_at')
    
    context = {
        'author_name': author_name,
        'articles': articles_by_author
    }
    return render(request, 'articles/author_detail.html', context)
