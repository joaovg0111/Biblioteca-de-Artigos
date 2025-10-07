# COPIE E COLE O CONTEÚDO COMPLETO PARA: apps/notifications/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserInterest

@login_required
def manage_interests_view(request):
    """
    Permite que o usuário visualize, adicione e remova
    suas palavras-chave de interesse para notificações por e-mail.
    """
    # Lógica para adicionar um novo interesse
    if request.method == 'POST' and 'add_keyword' in request.POST:
        keyword = request.POST.get('keyword', '').strip().lower()
        if keyword:
            # O método get_or_create previne a criação de duplicatas
            interest, created = UserInterest.objects.get_or_create(user=request.user, keyword=keyword)
            if created:
                messages.success(request, f"Você será notificado sobre artigos com a palavra-chave: '{keyword}'.")
            else:
                messages.info(request, f"A palavra-chave '{keyword}' já estava na sua lista de interesses.")
        else:
            messages.error(request, "Por favor, insira uma palavra-chave válida.")
        return redirect('notifications:manage-interests')

    # Lógica para remover um interesse
    if request.method == 'POST' and 'remove_keyword' in request.POST:
        interest_id = request.POST.get('interest_id')
        interest = UserInterest.objects.filter(id=interest_id, user=request.user).first()
        if interest:
            keyword = interest.keyword
            interest.delete()
            messages.success(request, f"Você não será mais notificado sobre a palavra-chave: '{keyword}'.")
        return redirect('notifications:manage-interests')

    # Busca os interesses atuais do usuário para exibir na página
    user_interests = UserInterest.objects.filter(user=request.user).order_by('keyword')
    
    context = {
        'interests': user_interests
    }
    return render(request, 'notifications/manage_interests.html', context)