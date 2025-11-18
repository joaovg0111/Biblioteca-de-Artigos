import pytest
from playwright.sync_api import Page, expect
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.notifications.models import UserInterest

# Marca todos os testes para terem acesso ao banco de dados.
pytestmark = pytest.mark.django_db

@pytest.fixture
def user_with_initial_interest():
    """
    Fixture que cria um usuário de teste com uma palavra-chave de interesse inicial.
    """
    User = get_user_model()
    user = User.objects.create_user(
        username="interest_user",
        password="a-secure-password",
        first_name="Interest",
        email="interest.user@example.com"
    )
    UserInterest.objects.create(user=user, keyword="engenharia de software")
    return user

def test_manage_interests_e2e_flow(page: Page, live_server, user_with_initial_interest):
    """
    Testa o fluxo completo de gerenciamento de interesses de um usuário:
    1. Faz login e navega para a página de interesses.
    2. Verifica se o interesse inicial está visível.
    3. Adiciona um novo interesse e verifica se ele aparece.
    4. Remove o interesse inicial e verifica se ele desaparece.
    """
    # --- 1. Login e Navegação ---
    login_url = live_server.url + reverse('users:login')
    page.goto(login_url)
    page.locator('input[name="username"]').fill(user_with_initial_interest.email)
    page.locator('input[name="password"]').fill("a-secure-password")
    page.get_by_role("button", name="Entrar").click()

    # Navega para a página de gerenciamento de interesses através do menu do usuário
    page.get_by_role("button", name=user_with_initial_interest.first_name).click()
    page.get_by_role("link", name="Gerenciar Notificações").click()
    
    # --- 2. Verifica o Estado Inicial ---
    page.wait_for_url(live_server.url + reverse('notifications:manage-interests'))
    # Verifica se o interesse inicial está na página
    # Usamos exact=True para garantir que estamos selecionando o texto exato do interesse
    # e não uma parte do texto do rodapé.
    expect(page.get_by_text("engenharia de software", exact=True)).to_be_visible()

    # --- 3. Adiciona um Novo Interesse ---
    new_keyword = "testes automatizados"
    page.locator('input[name="keyword"]').fill(new_keyword)
    page.get_by_role("button", name="Adicionar").click()

    # Verifica se a página recarregou e o novo interesse está visível
    expect(page.get_by_text(new_keyword, exact=True)).to_be_visible()
    
    # --- 4. Remove um Interesse Existente ---
    # Prepara o Playwright para aceitar a próxima caixa de diálogo de confirmação.
    page.on("dialog", lambda dialog: dialog.accept())

    # Encontra o elemento <div> específico que contém o span com o texto exato do interesse
    # e, em seguida, encontra o botão "Remover" dentro desse contêiner.
    # Isso evita a ambiguidade do seletor anterior, garantindo que estamos no contêiner correto.
    interest_to_remove_locator = page.locator("div.flex:has(span:text-is('engenharia de software'))")
    interest_to_remove_locator.get_by_role("button", name="Remover").click()

    # Verifica se a página recarregou e o interesse foi removido
    expect(page.get_by_text("engenharia de software", exact=True)).not_to_be_visible()