from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserInterest

@login_required
def manage_interests_view(request):
    """
    Permite que o usuário gerencie suas palavras-chave de interesse.
    Processa a adição (POST com 'add_keyword') e remoção (POST com 'remove_keyword')
    de interesses. Em requisições GET, exibe os interesses atuais.
    """
    if request.method == 'POST':
        if 'add_keyword' in request.POST:
            keyword = request.POST.get('keyword', '').strip().lower()
            if keyword:
                _, created = UserInterest.objects.get_or_create(user=request.user, keyword=keyword)
                messages.success(request, f"Interesse '{keyword}' adicionado.")
        elif 'remove_keyword' in request.POST:
            interest_id = request.POST.get('interest_id')
            UserInterest.objects.filter(id=interest_id, user=request.user).delete()
            messages.success(request, "Interesse removido.")
        return redirect('notifications:manage-interests') # Redireciona após a ação POST

    # Para requisições GET (ou após o redirecionamento), busca e exibe os interesses.
    user_interests = UserInterest.objects.filter(user=request.user).order_by('keyword')
    return render(request, 'notifications/manage_interests.html', {'interests': user_interests})