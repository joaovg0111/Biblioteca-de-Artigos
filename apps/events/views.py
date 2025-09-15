from django.shortcuts import render
from .models import Event

def event_list_view(request):
    """
    Esta vista obtém todos os eventos do banco de dados e renderiza uma página
    que os lista numa grelha.
    """
    # Obtém todos os objetos Event, ordenados pelo acrónimo
    events = Event.objects.all()
    
    # Passa a lista de eventos para o contexto do template
    context = {
        'events': events,
    }
    return render(request, "events/event_list.html", context)
