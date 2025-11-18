import pytest
from playwright.sync_api import Page, expect
from django.contrib.auth import get_user_model
from django.urls import reverse

# Marca todos os testes para terem acesso ao banco de dados.
pytestmark = pytest.mark.django_db

def test_user_signup_flow(page: Page, live_server):
    """
    História de Usuário: "Como visitante, quero me cadastrar no site para poder
    submeter e gerenciar meus artigos."
    """
    # 1. Preparação (Arrange) - Define os dados para o novo usuário.
    new_user_data = {
        "username": "e2e_tester",
        "first_name": "EndToEnd",
        "last_name": "Tester",
        "email": "e2e.tester@example.com",
        "password": "a-secure-e2e-password-123"
    }

    # 2. Ação (Act) - Navega para a página de cadastro, preenche e submete o formulário.
    signup_url = live_server.url + reverse('users:signup')
    page.goto(signup_url)
    
    page.locator('input[name="username"]').fill(new_user_data["username"])
    page.locator('input[name="first_name"]').fill(new_user_data["first_name"])
    page.locator('input[name="last_name"]').fill(new_user_data["last_name"])
    page.locator('input[name="email"]').fill(new_user_data["email"])
    page.locator('input[name="password1"]').fill(new_user_data["password"])
    page.locator('input[name="password2"]').fill(new_user_data["password"])
    # Preenche os campos adicionais do perfil.
    page.locator('input[name="affiliation"]').fill("Universidade de Teste E2E")
    page.locator('input[name="interests"]').fill("Engenharia de Software, Testes Automatizados")
    page.locator('textarea[name="biography"]').fill("Esta é uma biografia de teste para o usuário E2E.")

    # Submete o formulário após preencher todos os campos.
    page.get_by_role("button", name="Cadastrar").click()

    # 3. Verificação (Assert) - Confirma o redirecionamento e o estado de login.
    # Espera que a URL mude para a página inicial, indicando sucesso.
    page.wait_for_url(live_server.url + reverse('index'))

    # Verifica se o usuário está logado procurando pelo botão que contém o nome do usuário.
    # Este botão abre o menu dropdown.
    user_menu_button = page.get_by_role("button", name=new_user_data["first_name"])
    expect(user_menu_button).to_be_visible()


def test_user_login_and_logout_flow(page: Page, live_server):
    """
    História de Usuário: "Como um usuário registrado, quero poder fazer login
    e logout da minha conta."
    """
    # 1. Preparação (Arrange) - Cria um usuário de teste no banco de dados.
    User = get_user_model()
    password = "a-very-secure-password-456"
    user = User.objects.create_user(
        username="login_user",
        email="login.user@example.com",
        password=password,
        first_name="LoginUser"
    )

    # 2. Ação e Verificação (Act & Assert) - Login
    login_url = live_server.url + reverse('users:login')
    page.goto(login_url)

    page.locator('input[name="username"]').fill("login.user@example.com")
    page.locator('input[name="password"]').fill(password)
    page.get_by_role("button", name="Entrar").click()

    # Verifica se o login foi bem-sucedido, redirecionou para a página inicial e mostra o link "Sair".
    # Em vez de procurar por "Sair", procuramos pelo botão do menu do usuário.
    page.wait_for_url(live_server.url + reverse('index'))
    user_menu_button = page.get_by_role("button", name=user.first_name)
    expect(user_menu_button).to_be_visible()

    # 3. Ação e Verificação (Act & Assert) - Logout
    # Clica no botão do menu do usuário para abrir o dropdown e, em seguida, clica em "Logout".
    user_menu_button.click()
    page.get_by_role("link", name="Logout").click()

    # Verifica se o logout foi bem-sucedido e redirecionou para a página inicial.
    page.wait_for_url(live_server.url + reverse('index'))
    # Confirma que o usuário foi deslogado procurando pelo link "Login".
    # Usamos get_by_role para uma correspondência exata e mais robusta,
    # evitando que o seletor encontre acidentalmente o link "Logout".
    expect(page.get_by_role("link", name="Login", exact=True)).to_be_visible()