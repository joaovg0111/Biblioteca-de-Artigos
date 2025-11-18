import pytest
from django.urls import reverse
import re
from playwright.sync_api import Page, expect
from datetime import date

from apps.events.models import Event, Edition

pytestmark = pytest.mark.django_db


@pytest.fixture
def test_event_and_edition(db):
    """Cria dados de evento e edição para testes E2E."""
    event = Event.objects.create(name="Conferência de Testes de Software", acronym="CTS")
    edition = Edition.objects.create(
        event=event,
        location="Online",
        start_date=date(2025, 10, 20),
        end_date=date(2025, 10, 24),
    )
    return event, edition


def test_events_navigation_flow(page: Page, live_server, test_event_and_edition):
    """
    Testa o fluxo de navegação completo do usuário, começando na página de lista de eventos
    até a página de detalhes de uma edição específica.
    """
    event, edition = test_event_and_edition

    # 1. Navega para a página de lista de eventos.
    page.goto(live_server.url + reverse("events:event-list"))
    # Torna o seletor mais específico para evitar ambiguidade.
    # Procuramos por um link que contenha o acrônimo do evento.
    # Usamos uma expressão regular para encontrar um link cujo nome contenha o acrônimo.
    event_link = page.get_by_role("link", name=re.compile(event.acronym, re.IGNORECASE))
    expect(event_link).to_be_visible()

    # 2. Clica em um evento específico para navegar para a página de detalhes do evento (lista de edições).
    event_link.click()
    # CORREÇÃO: A verificação foi simplificada para procurar apenas o nome do evento,
    # tornando o teste menos frágil a mudanças no texto do cabeçalho.
    expect(page.get_by_text(event.name)).to_be_visible()

    # 3. Clica em uma edição específica para navegar para a página de detalhes da edição.
    # CORREÇÃO: O seletor foi simplificado para corresponder ao texto real do link,
    # que, conforme observado, é "Edição de [ano]".
    edition_link_text = f"Edição de {edition.year}"
    edition_link = page.get_by_role("link", name=re.compile(edition_link_text))
    expect(edition_link).to_be_visible() # Verifica se o link da edição está visível
    edition_link.click()

    # CORREÇÃO: As asserções foram atualizadas para corresponder ao conteúdo exato da página de detalhes da edição.
    expect(page.get_by_text(f"Edição de {edition.year}")).to_be_visible()
    expect(page.get_by_text(f"Local: {edition.location}")).to_be_visible()
    
    start_date_str = edition.start_date.strftime('%d/%m/%Y')
    end_date_str = edition.end_date.strftime('%d/%m/%Y')
    expect(page.get_by_text(f"Período: de {start_date_str} até {end_date_str}")).to_be_visible()

    expect(page.get_by_text("Artigos Publicados Nesta Edição")).to_be_visible()
    expect(page.get_by_text("Nenhum artigo foi encontrado para esta edição.")).to_be_visible()