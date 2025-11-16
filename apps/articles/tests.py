import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.utils import timezone  # Importe timezone

# Marcar todos os testes neste arquivo como 'django_db' para dar acesso ao banco
pytestmark = pytest.mark.django_db

# Nossos imports locais
from .models import Article
from .forms import ArticleForm, BibtexUploadForm
from apps.events.models import Event, Edition

# Criamos um usuário de teste que podemos reusar
@pytest.fixture
def test_user():
    """Cria um usuário padrão para os testes."""
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='password123')

@pytest.fixture
def test_admin_user(test_user):
    """Cria um usuário admin para os testes de admin."""
    test_user.is_staff = True
    test_user.is_superuser = True
    test_user.save()
    return test_user

@pytest.fixture
def test_event_edition():
    """Cria um Evento e uma Edição de teste."""
    event = Event.objects.create(name="Simpósio Brasileiro de Testes")
    edition = Edition.objects.create(
        event=event, 
        start_date=timezone.now().date(),
        location="Belo Horizonte"
    )
    return edition

@pytest.fixture
def test_article(test_user, test_event_edition):
    """Cria um Artigo de teste."""
    return Article.objects.create(
        title="Artigo de Teste",
        authors="Autor A, Autor B",
        abstract="Este é um resumo.",
        edition=test_event_edition,
        submitter=test_user
    )

# --- 1. Teste de Model (models.py) ---
def test_article_model_str(test_article):
    """Verifica se o __str__ do modelo Article retorna o título."""
    assert str(test_article) == "Artigo de Teste"

# --- 2. Teste de Form (forms.py) ---
def test_article_form_clean_authors():
    """Testa a lógica de limpeza do campo 'authors' no ArticleForm."""
    # O form deve adicionar vírgulas e remover espaços extras
    form_data = {
        'title': 'Teste',
        'authors': 'Autor A ,  Autor B   ,Autor C'
    }
    form = ArticleForm(data=form_data)
    assert form.is_valid()
    # Verifica se a limpeza funcionou
    assert form.cleaned_data['authors'] == "Autor A, Autor B, Autor C"

# --- 3. Teste de View (views.py) ---
def test_author_list_view(client, test_article):
    """Testa a view 'author_list_view' (H.U. 7)."""
    # Acessa a URL
    url = reverse('articles:author-list')
    response = client.get(url)

    assert response.status_code == 200
    # Verifica se os autores do 'test_article' estão na página
    assert "Autor A" in response.content.decode('utf-8')
    assert "Autor B" in response.content.decode('utf-8')

def test_my_articles_view_authenticated(client, test_user, test_article):
    """Testa a view 'my_articles_view' (H.U. 7) quando o usuário está logado."""
    client.login(username='testuser', password='password123')
    url = reverse('articles:my-articles')
    response = client.get(url)

    assert response.status_code == 200
    assert "Artigo de Teste" in response.content.decode('utf-8')

def test_my_articles_view_unauthenticated(client):
    """Testa se 'my_articles_view' redireciona se o usuário não estiver logado."""
    url = reverse('articles:my-articles')
    response = client.get(url)
    
    # Deve redirecionar para a página de login
    assert response.status_code == 302
    assert 'login' in response.url

# --- 4. Teste de Admin (admin.py - H.U. 4) ---
def test_bulk_upload_bibtex(admin_client, test_admin_user):
    """Testa o upload em massa de BibTeX (H.U. 4)."""
    
    # Conteúdo do arquivo .bib de teste
    bibtex_content = """
    @inproceedings{sbes2025paper1,
      author = {Autor C and Autor D},
      title = {Novo Artigo do BibTeX},
      booktitle = {SBES},
      year = {2025},
      keywords = {teste, bibtex}
    }
    @inproceedings{sbes2025paper2-invalid,
      author = {Autor E},
      booktitle = {SBES},
      year = {2025}
      % Título faltando!
    }
    """
    
    # Simula um arquivo enviado
    bib_file = SimpleUploadedFile(
        "test.bib", 
        bibtex_content.encode('utf-8'), 
        content_type="text/plain"
    )

    url = reverse('admin:articles_article_bulk_upload')
    form_data = {'bibtex_file': bib_file}
    
    # 'admin_client' já está logado como o 'test_admin_user'
    response = admin_client.post(url, data=form_data)
    
    # 302 significa que o POST foi bem-sucedido e redirecionou (para a lista de artigos)
    assert response.status_code == 302 
    
    # Verifica se o artigo válido foi criado
    assert Article.objects.filter(title="Novo Artigo do BibTeX").exists()
    
    # Verifica se o evento e a edição foram criados automaticamente
    assert Event.objects.filter(name="SBES").exists()
    assert Edition.objects.filter(event__name="SBES", start_date__year=2025).exists()

    # Verifica se o artigo inválido (sem título) NÃO foi criado
    assert not Article.objects.filter(authors__icontains="Autor E").exists()
