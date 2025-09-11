
"""Views (PT-BR) para listar, enviar e baixar artigos."""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponse
from django.views.generic import ListView
from .models import Artigo
from .forms import ArtigoForm
import mimetypes, os

class ListaArtigosView(ListView):
    template_name = 'artigos/lista.html'
    context_object_name = 'artigos'
    model = Artigo

def upload_artigo(request):
    """
    Estratégia: salvar primeiro a instância sem arquivo para obter pk,
    depois salvar o arquivo usando upload_to que depende do pk.
    Isso evita o erro "no file associated" e caminhos temporários.
    """
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)
        if form.is_valid():
            artigo = Artigo(
                titulo=form.cleaned_data['titulo'],
                autores=form.cleaned_data['autores'],
                resumo=form.cleaned_data.get('resumo', ''),
            )
            artigo.save()  # agora tem pk
            arquivo = form.cleaned_data['arquivo']
            artigo.arquivo.save(arquivo.name, arquivo, save=True)
            return redirect('lista_artigos')
    else:
        form = ArtigoForm()
    return render(request, 'artigos/upload.html', {'form': form})

def download_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if not artigo.arquivo:
        return HttpResponse('Arquivo não encontrado.', status=404)
    caminho = artigo.arquivo.path
    nome = os.path.basename(caminho)
    tipo, _ = mimetypes.guess_type(nome)
    tipo = tipo or 'application/octet-stream'
    resposta = FileResponse(open(caminho, 'rb'), content_type=tipo)
    resposta['Content-Disposition'] = f'attachment; filename="{nome}"'
    return resposta
