import pytest
from datetime import timedelta
from playwright.sync_api import Page, expect

# Nossos imports do Django para criar dados
from apps.articles.models import Article
from apps.events.models import Event, Edition
from django.utils import timezone

@pytest.mark.django_db
def test_search_article_by_title(page: Page, live_server):
    """
    Testa a História de Usuário 5:
    "Como usuário, eu quero pesquisar por artigos por título"
    """
    # --- 1. Preparação (Arrange) ---
    # Cria os dados de teste no banco de dados
    start = timezone.now().date()
    event = Event.objects.create(name="E2E Event")
    edition = Edition.objects.create(
        event=event, 
        start_date=start,
        end_date=start + timedelta(days=3),
        location="Testland"
    )
    Article.objects.create(
        title="O Artigo Perfeito para Busca",
        authors="Autor E2E",
        edition=edition
    )
    Article.objects.create(
        title="Outro Artigo",
        authors="Autor E2E",
        edition=edition
    )

    # --- 2. Ação (Act) ---
    # O 'live_server' nos dá a URL do servidor de teste
    # (Assumindo que a barra de busca está na home page '/')
    page.goto(live_server.url + "/")

    # Encontra os elementos do formulário de busca (baseado no views.py)
    # O views.py espera 'q' (query) e 'search_field'
    page.locator('input[name="q"]').fill("Perfeito para Busca")
    page.select_option('select[name="search_field"]', 'title')

    # Clica no botão de submissão
    page.get_by_role("button", name="Buscar").click()

    # --- 3. Verificação (Assert) ---
    # Espera a página de resultados carregar (baseado no urls.py)
    page.wait_for_url(f"{live_server.url}/articles/search/**")

    # Verifica se o artigo correto apareceu
    expect(page.get_by_text("O Artigo Perfeito para Busca")).to_be_visible()

    # Verifica se o outro artigo NÃO apareceu
    expect(page.get_by_text("Outro Artigo")).not_to_be_visible()