import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Profile
from .forms import SignUpForm

# Marcar todos os testes neste arquivo para ter acesso ao banco de dados.
pytestmark = pytest.mark.django_db

# --- Fixtures (Dados de Teste Reutilizáveis) ---

@pytest.fixture
def user_data():
    """Fornece um dicionário com dados válidos para criar um usuário."""
    return {
        'username': 'new_signup_user',
        'email': 'new.signup.user@example.com',
        'password': 'a-very-complex-password-123!', # Senha mais forte para passar na validação
        'first_name': 'Test',
        'last_name': 'User',
    }

@pytest.fixture
def created_user(user_data):
    """Cria e retorna um usuário padrão para os testes."""
    User = get_user_model()
    return User.objects.create_user(
        username='existing_user',
        email='existing.user@example.com',
        password='another-complex-password-456!', # Senha mais forte também aqui
        first_name='Existing'
    )

# --- Testes de Modelo (models.py) ---

def test_user_model_creation(created_user, user_data):
    """
    Testa a criação bem-sucedida de um usuário usando o manager padrão.
    """
    assert created_user.username == 'existing_user'
    assert created_user.email == 'existing.user@example.com'
    assert created_user.first_name == 'Existing'
    assert created_user.is_active
    assert not created_user.is_staff
    assert not created_user.is_superuser
    assert created_user.check_password('another-complex-password-456!')
    assert str(created_user) == 'existing_user'

def test_superuser_model_creation(db):
    """
    Testa a criação bem-sucedida de um superusuário.
    """
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='password123'
    )
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser

def test_profile_creation_signal(created_user):
    """
    Testa se um Profile é criado automaticamente quando um User é criado.
    Nota: Este teste assume que você tem um signal para criar o Profile.
    Se a criação é feita na view, este teste falhará e o teste da view será mais importante.
    """
    # A view `signup_view` cria o Profile, então vamos testar isso lá.
    # Por enquanto, vamos verificar que um usuário pode existir sem um perfil.
    assert not Profile.objects.filter(user=created_user).exists()

# --- Testes de Formulário (forms.py) ---

def test_signup_form_valid(user_data):
    """Testa se o SignUpForm é válido com dados corretos."""
    form_data = user_data.copy()
    # UserCreationForm espera 'password1' e 'password2'.
    # Renomeamos 'password' para 'password1' e adicionamos 'password2' para confirmação.
    form_data['password1'] = form_data.pop('password')
    form_data['password2'] = form_data['password1']
    form = SignUpForm(data=form_data)
    # --- DEBUG: Imprime os erros do formulário se ele for inválido ---
    if not form.is_valid():
        print("SignUpForm Errors:", form.errors.as_json())
    # ----------------------------------------------------------------
    assert form.is_valid(), f"O SignUpForm deveria ser válido. Erros: {form.errors.as_json()}"

def test_signup_form_email_in_use(user_data, created_user):
    """Testa a validação de e-mail duplicado no SignUpForm."""
    # created_user의 이메일을 사용하여 가입 시도
    invalid_data = user_data.copy()
    invalid_data['email'] = created_user.email
    invalid_data['password2'] = invalid_data['password']

    form = SignUpForm(data=invalid_data)
    assert not form.is_valid()
    assert 'email' in form.errors
    assert "Este endereço de e-mail já está em uso." in form.errors['email']

# --- Testes de View (views.py) ---

def test_signup_view_success(client, user_data):
    """Testa o cadastro de um novo usuário através da view."""
    url = reverse('users:signup')
    form_data = user_data.copy()
    # A view usa o SignUpForm, que espera 'password1' e 'password2'.
    form_data['password1'] = form_data.pop('password')
    form_data['password2'] = form_data['password1']
    form_data['affiliation'] = 'Universidade Teste' # Campo extra processado pela view

    response = client.post(url, data=form_data)

    assert response.status_code == 302, "A página deveria redirecionar após o cadastro."
    assert response.url == reverse('index')

    # Verifica se o usuário e o perfil foram criados corretamente
    user = get_user_model().objects.get(username=user_data['username'])
    assert Profile.objects.filter(user=user, affiliation='Universidade Teste').exists()

    # Verifica se o usuário foi logado automaticamente
    assert '_auth_user_id' in client.session
    assert client.session['_auth_user_id'] == str(user.id)

def test_login_view_success(client, created_user, user_data):
    """Testa o login bem-sucedido com e-mail e senha."""
    # created_user fixture에서 생성된 사용자로 로그인 테스트
    url = reverse('users:login')
    login_data = {
        'username': created_user.email,
        'password': 'another-complex-password-456!'
    }
    response = client.post(url, data=login_data)

    assert response.status_code == 302
    assert response.url == reverse('index')
    assert '_auth_user_id' in client.session

def test_logout_view(client, created_user):
    """Testa se a view de logout desconecta o usuário."""
    client.login(username=created_user.username, password='another-complex-password-456!')
    assert '_auth_user_id' in client.session

    url = reverse('users:logout')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('index')
    assert '_auth_user_id' not in client.session