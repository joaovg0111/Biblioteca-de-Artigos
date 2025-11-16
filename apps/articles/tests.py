import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import os # Importe 'os' para o teste de download

# Marcar todos os testes neste arquivo como 'django_db' para dar acesso ao banco
pytestmark = pytest.mark.django_db

@pytest.fixture
def test_user():
    """Cria um usuário padrão para os testes."""
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='password123')

@pytest.fixture
def another_user():
    """Cria um segundo usuário para testes de permissão."""
    User = get_user_model()
    return User.objects.create_user(username='anotheruser', password='password456')

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
    from apps.events.models import Event, Edition
    
    event = Event.objects.create(name="Simpósio Brasileiro de Testes")
    start = timezone.now().date()
    edition = Edition.objects.create(
        event=event, 
        start_date=start,
        end_date=start + timedelta(days=3), # <-- Correção do erro anterior
        location="Belo Horizonte"
    )
    return edition

@pytest.fixture
def test_article(test_user, test_event_edition):
    """Cria um Artigo de teste."""
    from apps.articles.models import Article
    
    return Article.objects.create(
        title="Artigo de Teste",
        authors="Autor A, Autor B",
        abstract="Este é um resumo.",
        edition=test_event_edition,
        submitter=test_user
    )

@pytest.fixture
def test_article_with_pdf(test_user, test_event_edition, tmp_path):
    """Cria um artigo com um arquivo PDF real para o teste de download."""
    from apps.articles.models import Article

    # Cria um arquivo PDF falso
    pdf_content = b'%PDF-1.5...fake pdf content...'
    pdf_file = SimpleUploadedFile("test_file.pdf", pdf_content, content_type="application/pdf")

    article = Article.objects.create(
        title="Artigo com PDF",
        authors="Autor C",
        abstract="Resumo do PDF.",
        edition=test_event_edition,
        submitter=test_user,
        pdf_file=pdf_file,
        original_filename="test_file.pdf"
    )
    return article

def test_article_model_str(test_article):
    """Verifica se o __str__ do modelo Article retorna o título."""
    assert str(test_article) == "Artigo de Teste"

def test_article_form_clean_authors():
    """Testa a lógica de limpeza do campo 'authors' no ArticleForm."""
    from apps.articles.forms import ArticleForm
    
    form_data = {
        'title': 'Teste',
        'authors': 'Autor A ,  Autor B   ,Autor C'
    }
    form = ArticleForm(data=form_data)
    assert form.is_valid()
    assert form.cleaned_data['authors'] == "Autor A, Autor B, Autor C"

def test_author_list_view(client, test_article):
    """Testa a view 'author_list_view' (H.U. 7)."""
    url = reverse('articles:author-list')
    response = client.get(url)

    assert response.status_code == 200
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
    
    assert response.status_code == 302
    assert 'login' in response.url

def test_bulk_upload_bibtex(admin_client, test_admin_user):
    """Testa o upload em massa de BibTeX (H.U. 4)."""
    from apps.articles.models import Article
    from apps.events.models import Event, Edition
    
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
    }
    """
    
    bib_file = SimpleUploadedFile(
        "test.bib", 
        bibtex_content.encode('utf-8'), 
        content_type="text/plain"
    )

    url = reverse('admin:articles_article_bulk_upload')
    form_data = {'bibtex_file': bib_file}
    
    response = admin_client.post(url, data=form_data)
    
    assert response.status_code == 302 
    assert Article.objects.filter(title="Novo Artigo do BibTeX").exists()
    assert Event.objects.filter(name="SBES").exists()
    assert Edition.objects.filter(event__name="SBES", start_date__year=2025).exists()
    assert not Article.objects.filter(authors__icontains="Autor E").exists()

# --- NOVOS TESTES PARA COBRIR VIEWS.PY ---

def test_home_view(client, test_article):
    """Testa a home_view (não está no urls.py de articles, mas em config/urls.py)."""
    url = "/"
    response = client.get(url)
    assert response.status_code == 200
    assert "Artigo de Teste" in response.content.decode('utf-8')

def test_add_article_options_view(client):
    """Testa a view 'add_article_options_view'."""
    url = reverse('articles:add-article-options')
    response = client.get(url)
    assert response.status_code == 200

def test_article_list_view(client, test_article):
    """Testa a view 'article_list_view'."""
    url = reverse('articles:article-list')
    response = client.get(url)
    assert response.status_code == 200
    assert "Artigo de Teste" in response.content.decode('utf-8')

def test_article_search_view(client, test_article):
    """Testa a 'article_search_view' com vários filtros."""
    # 1. Busca por Título (Encontra)
    url = reverse('articles:article-search') + "?q=Teste&search_field=title"
    response = client.get(url)
    assert response.status_code == 200
    assert "Artigo de Teste" in response.content.decode('utf-8')

    # 2. Busca por Autor (Encontra)
    url = reverse('articles:article-search') + "?q=Autor A&search_field=author"
    response = client.get(url)
    assert response.status_code == 200
    assert "Artigo de Teste" in response.content.decode('utf-8')

    # 3. Busca por Evento (Encontra)
    url = reverse('articles:article-search') + "?q=Simpósio&search_field=event"
    response = client.get(url)
    assert response.status_code == 200
    assert "Artigo de Teste" in response.content.decode('utf-8')

    # 4. Busca (Não Encontra)
    url = reverse('articles:article-search') + "?q=NaoExiste&search_field=title"
    response = client.get(url)
    assert response.status_code == 200
    assert "Artigo de Teste" not in response.content.decode('utf-8')

def test_download_pdf_view_success(client, test_article_with_pdf):
    """Testa o download de um PDF que existe."""
    url = reverse('articles:download-pdf', kwargs={'article_id': test_article_with_pdf.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/pdf'
    assert response['Content-Disposition'] == 'attachment; filename="test_file.pdf"'
    # Limpa o arquivo após o teste
    os.remove(test_article_with_pdf.pdf_file.path)

def test_download_pdf_view_404(client, test_article):
    """Testa o download de um artigo sem PDF (deve retornar 404)."""
    url = reverse('articles:download-pdf', kwargs={'article_id': test_article.pk})
    response = client.get(url)
    assert response.status_code == 404

def test_article_edit_view_get(client, test_user, test_article):
    """Testa o GET na 'article_edit_view' (carregar o formulário)."""
    client.login(username='testuser', password='password123')
    url = reverse('articles:article-edit', kwargs={'article_id': test_article.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

def test_article_edit_view_post(client, test_user, test_article):
    """Testa o POST na 'article_edit_view' (salvar o formulário)."""
    client.login(username='testuser', password='password123')
    url = reverse('articles:article-edit', kwargs={'article_id': test_article.pk})
    form_data = {
        'title': 'Título Editado',
        'authors': test_article.authors, # Campos obrigatórios
        'abstract': test_article.abstract,
    }
    response = client.post(url, data=form_data)
    
    assert response.status_code == 302 # Deve redirecionar
    assert response.url == reverse('articles:my-articles')
    
    test_article.refresh_from_db()
    assert test_article.title == 'Título Editado'

def test_article_edit_view_wrong_user(client, another_user, test_article):
    """Testa se um usuário não pode editar o artigo de outro (deve dar 404)."""
    client.login(username='anotheruser', password='password456')
    url = reverse('articles:article-edit', kwargs={'article_id': test_article.pk})
    response = client.get(url)
    assert response.status_code == 404 # A view usa get_object_or_404

def test_article_delete_view_get(client, test_user, test_article):
    """Testa o GET na 'article_delete_view' (página de confirmação)."""
    client.login(username='testuser', password='password123')
    url = reverse('articles:article-delete', kwargs={'article_id': test_article.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'article' in response.context

def test_article_delete_view_post(client, test_user, test_article):
    """Testa o POST na 'article_delete_view' (deletar o artigo)."""
    from apps.articles.models import Article
    client.login(username='testuser', password='password123')
    
    article_pk = test_article.pk
    url = reverse('articles:article-delete', kwargs={'article_id': article_pk})
    response = client.post(url)
    
    assert response.status_code == 302
    assert response.url == reverse('articles:my-articles')
    assert not Article.objects.filter(pk=article_pk).exists() # Verifica se foi deletado

def test_article_detail_view(client, test_article):
    """Testa a 'article_detail_view'."""
    url = reverse('articles:article-detail', kwargs={'article_id': test_article.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert "Artigo de Teste" in response.content.decode('utf-8')

def test_author_detail_view(client, test_article):
    """Testa a 'author_detail_view'."""
    url = reverse('articles:author-detail', kwargs={'author_name': 'Autor A'})
    response = client.get(url)
    assert response.status_code == 200
    assert "Artigo de Teste" in response.content.decode('utf-8')

def test_bibtex_upload_form_validation_error():
    """Testa se BibtexUploadForm levanta erro quando nenhum campo é preenchido (linha 60 de forms.py)."""
    from apps.articles.forms import BibtexUploadForm
    
    # Submeter formulário vazio
    form = BibtexUploadForm(data={})
    
    assert not form.is_valid()
    assert 'Você deve fornecer um arquivo BibTeX' in str(form.errors)

def test_download_pdf_without_original_filename(client, test_article):
    """Testa download de PDF quando original_filename está vazio (linhas 75-76 de views.py)."""
    from apps.articles.models import Article
    from django.core.files.uploadedfile import SimpleUploadedFile
    
    # Criar artigo com PDF mas sem original_filename
    pdf_content = b'%PDF-1.4 fake pdf content'
    pdf_file = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")
    
    test_article.pdf_file = pdf_file
    test_article.original_filename = ""
    test_article.save()
    
    url = reverse('articles:download-pdf', args=[test_article.id])
    response = client.get(url)
    
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/pdf'
    # Verifica se o nome foi gerado a partir do título
    assert 'artigo-de-teste.pdf' in response['Content-Disposition']


def test_download_pdf_file_not_found(client, test_article):
    """Testa exceção FileNotFoundError em download_pdf_view (linha 101 de views.py)."""
    from apps.articles.models import Article
    from unittest.mock import patch
    
    # Simular que o arquivo não existe no sistema de arquivos
    test_article.pdf_file.name = 'non_existent_file.pdf'
    test_article.save()
    
    url = reverse('articles:download-pdf', args=[test_article.id])
    
    # Simular FileNotFoundError ao abrir o arquivo
    with patch('builtins.open', side_effect=FileNotFoundError):
        response = client.get(url)
        assert response.status_code == 404

def test_my_articles_multiple_years(client, test_user):
    """Testa agrupamento por ano em my_articles_view (linhas 110-111 de views.py)."""
    from apps.articles.models import Article
    from apps.events.models import Event, Edition
    from datetime import timedelta
    from django.utils.timezone import datetime
    from datetime import timezone as dt_timezone
    
    # Criar artigos de anos diferentes para testar o agrupamento
    event = Event.objects.create(name="Test Event")
    edition = Edition.objects.create(
        event=event,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timedelta(days=3)
    )
    
    # Artigo de 2024
    article_2024 = Article.objects.create(
        title="Artigo 2024",
        authors="Autor Teste",
        edition=edition,
        submitter=test_user
    )
    # Forçar data de criação para 2024
    article_2024.created_at = datetime(2024, 1, 1, tzinfo=dt_timezone.utc)
    article_2024.save()
    
    # Artigo de 2025
    article_2025 = Article.objects.create(
        title="Artigo 2025",
        authors="Autor Teste",
        edition=edition,
        submitter=test_user
    )
    article_2025.created_at = datetime(2025, 1, 1, tzinfo=dt_timezone.utc)
    article_2025.save()
    
    client.login(username='testuser', password='password123')
    url = reverse('articles:my-articles')
    response = client.get(url)
    
    assert response.status_code == 200
    assert "Artigo 2024" in response.content.decode('utf-8')
    assert "Artigo 2025" in response.content.decode('utf-8')

def test_article_edit_with_new_pdf(client, test_user, test_article):
    """Testa edição de artigo com upload de novo PDF (linha 147 de views.py)."""
    from django.core.files.uploadedfile import SimpleUploadedFile
    
    client.login(username='testuser', password='password123')
    
    # Criar novo arquivo PDF para upload
    new_pdf_content = b'%PDF-1.4 new fake pdf content'
    new_pdf = SimpleUploadedFile("new_article.pdf", new_pdf_content, content_type="application/pdf")
    
    url = reverse('articles:article-edit', args=[test_article.id])
    form_data = {
        'title': 'Título Editado',
        'authors': 'Autor Editado',
        'abstract': 'Resumo editado',
        'pdf_file': new_pdf
    }
    
    response = client.post(url, data=form_data)
    
    # Deve redirecionar após sucesso
    assert response.status_code == 302
    
    # Verificar que o artigo foi atualizado
    test_article.refresh_from_db()
    assert test_article.title == 'Título Editado'
    assert test_article.original_filename == 'new_article.pdf'
