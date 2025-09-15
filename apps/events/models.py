from django.db import models

class Event(models.Model):
    """
    Representa um evento científico, como uma conferência ou simpósio.
    """
    name = models.CharField(max_length=255, verbose_name="Nome Completo do Evento")
    acronym = models.CharField(max_length=20, verbose_name="Acrónimo")
    full_description = models.TextField(verbose_name="Descrição Completa")

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['acronym']

    def __str__(self):
        return self.acronym

class Edition(models.Model):
    """
    Representa uma edição específica de um Evento.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='editions', verbose_name="Evento")
    year = models.PositiveIntegerField(verbose_name="Ano")
    location = models.CharField(max_length=100, verbose_name="Localização")
    start_date = models.DateField(verbose_name="Data de Início")
    end_date = models.DateField(verbose_name="Data de Fim")

    class Meta:
        verbose_name = "Edição"
        verbose_name_plural = "Edições"
        # ESTA É A ALTERAÇÃO CRÍTICA:
        # Agora, a combinação de TODOS estes campos deve ser única.
        unique_together = ('event', 'year', 'location', 'start_date', 'end_date')
        ordering = ['-year', '-start_date']

    def __str__(self):
        return f"{self.event.acronym} {self.year} ({self.location})"