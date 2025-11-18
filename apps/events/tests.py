import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Event, Edition

# Este marcador aplica o acesso ao banco de dados para todos os testes neste arquivo.
pytestmark = pytest.mark.django_db


@pytest.fixture
def test_event():
    """Cria um objeto Event de teste."""
    return Event.objects.create(name="Simpósio Brasileiro de Engenharia de Software", acronym="SBES")


@pytest.fixture
def test_edition(test_event):
    """Cria um objeto Edition de teste."""
    start_date = timezone.now().date()
    return Edition.objects.create(
        event=test_event,
        start_date=start_date,
        end_date=start_date + timedelta(days=4),
        location="Salvador, Bahia",
    )


# --- Testes de Modelo ---

def test_event_model_str(test_event):
    """Testa se o método __str__ do modelo Event retorna o nome do evento."""
    assert str(test_event) == "SBES"


def test_edition_model_str(test_edition):
    """Testa se o método __str__ do modelo Edition retorna a string formatada corretamente."""
    expected_str = f"SBES {test_edition.year} (Salvador, Bahia)"
    assert str(test_edition) == expected_str


# --- Testes de View ---

def test_event_list_view(client, test_event):
    """Testa se a event_list_view retorna o status 200 e contém o nome do evento."""
    url = reverse("events:event-list")
    response = client.get(url)
    assert response.status_code == 200
    assert test_event.name in response.content.decode("utf-8")


def test_event_detail_view(client, test_event, test_edition):
    """Testa se a event_detail_view retorna o status 200 e contém as informações da edição."""
    url = reverse("events:event-detail", kwargs={"event_id": test_event.pk})
    response = client.get(url)
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert test_event.name in content
    assert str(test_edition.year) in content
    assert test_edition.location in content
