from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ArticleForm
from .models import Article
from django.db.models import Q

@login_required
def article_upload_view(request):
    """
    Exibe o formulário de upload de artigos e processa os dados submetidos.
    """
    if request.method == 'POST':
        # Passa request.FILES para lidar com os dados do arquivo.
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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