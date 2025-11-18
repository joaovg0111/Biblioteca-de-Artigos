import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import UserInterest

# Marca todos os testes para terem acesso ao banco de dados.
pytestmark = pytest.mark.django_db

@pytest.fixture
def test_user():
    """
    Fixture que cria um usuário de teste simples.
    """
    User = get_user_model()
    return User.objects.create_user(
        username='notify_user',
        password='a-secure-password',
        first_name='Notify',
        email='notify@example.com'
    )

@pytest.fixture
def user_with_interests(test_user):
    """
    Fixture que cria um usuário e adiciona alguns interesses iniciais
    usando o modelo UserInterest.
    """
    UserInterest.objects.create(user=test_user, keyword='engenharia de software')
    UserInterest.objects.create(user=test_user, keyword='testes')
    return test_user

def test_manage_interests_view_redirects_unauthenticated_user(client):
    """
    Testa se um usuário não autenticado é redirecionado para a página de login.
    """
    url = reverse('notifications:manage-interests')
    response = client.get(url)
    
    # Verifica o redirecionamento para a página de login.
    assert response.status_code == 302
    assert 'login' in response.url

def test_manage_interests_view_get_authenticated_user(client, user_with_interests):
    """
    Testa se um usuário autenticado consegue visualizar seus interesses existentes.
    """
    client.login(username=user_with_interests.username, password='a-secure-password')
    url = reverse('notifications:manage-interests')
    response = client.get(url)
    
    assert response.status_code == 200
    content = response.content.decode('utf-8')
    # Verifica se as palavras-chave individuais estão na página.
    assert 'engenharia de software' in content
    assert 'testes' in content

def test_add_interest_view(client, test_user):
    """
    Testa se um usuário pode adicionar uma nova palavra-chave de interesse.
    """
    client.login(username=test_user.username, password='a-secure-password')
    url = reverse('notifications:manage-interests')
    new_keyword = 'inteligência artificial'
    
    # Simula o envio do formulário para adicionar uma palavra-chave.
    response = client.post(url, {'keyword': new_keyword, 'add_keyword': ''})
    
    # Verifica se redireciona após a adição bem-sucedida.
    assert response.status_code == 302
    # Verifica se o novo interesse foi salvo no banco de dados.
    assert UserInterest.objects.filter(user=test_user, keyword=new_keyword).exists()

def test_remove_interest_view(client, user_with_interests):
    """
    Testa se um usuário pode remover uma palavra-chave de interesse existente.
    """
    client.login(username=user_with_interests.username, password='a-secure-password')
    url = reverse('notifications:manage-interests')
    interest_to_remove = UserInterest.objects.get(user=user_with_interests, keyword='testes')
    
    # Simula o envio do formulário para remover a palavra-chave.
    response = client.post(url, {'interest_id': interest_to_remove.id, 'remove_keyword': ''})
    
    assert response.status_code == 302
    # Verifica se o interesse foi removido do banco de dados.
    assert not UserInterest.objects.filter(id=interest_to_remove.id).exists()