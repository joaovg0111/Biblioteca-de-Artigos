from django.shortcuts import render, get_object_or_404
from .models import Event, Edition
from apps.articles.models import Article  # --- MUDANÇA: Importamos o modelo Article

def event_list_view(request):
    """
    Esta vista obtém todos os eventos do banco de dados e renderiza uma página
    que os lista numa grelha.
    """
    events = Event.objects.all()
    context = {
        'events': events,
    }
    return render(request, "events/event_list.html", context)

def event_detail_view(request, event_id):
    """
    Exibe os detalhes de um único evento, incluindo suas edições.
    """
    event = get_object_or_404(Event, pk=event_id)
    
    # Ordenamos por um campo que existe no banco de dados.
    editions = event.editions.all().order_by('-start_date') 
    
    context = {
        'event': event,
        'editions': editions
    }
    return render(request, 'events/event_detail.html', context)

# --- MUDANÇA: Nova view para a página de detalhes da edição ---
def edition_detail_view(request, edition_id):
    """
    Exibe os detalhes de uma única edição, incluindo uma lista de
    todos os artigos publicados nela.
    """
    edition = get_object_or_404(Edition, pk=edition_id)
    
    # Busca todos os artigos que estão associados a esta edição
    articles = Article.objects.filter(edition=edition).order_by('title')
    
    context = {
        'edition': edition,
        'articles': articles
    }
    return render(request, 'events/edition_detail.html', context)