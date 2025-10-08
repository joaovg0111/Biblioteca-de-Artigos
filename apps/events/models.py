from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome Completo do Evento")
    acronym = models.CharField(max_length=20, verbose_name="Acrónimo")

    # --- CORREÇÃO: Campo duplicado 'entidade_promotora' removido. ---
    promoting_entity = models.CharField("Entidade Promotora", max_length=255, blank=True)
    
    website = models.URLField(max_length=255, blank=True, verbose_name="Website do Evento")
    full_description = models.TextField(verbose_name="Descrição Completa")

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['acronym']

    def __str__(self):
        return self.acronym

class Edition(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='editions', verbose_name="Evento")
    location = models.CharField(max_length=100, verbose_name="Localização")
    website = models.URLField(max_length=255, blank=True, verbose_name="Website da Edição")
    start_date = models.DateField(verbose_name="Data de Início")
    end_date = models.DateField(verbose_name="Data de Fim")

    class Meta:
        verbose_name = "Edição"
        verbose_name_plural = "Edições"
        unique_together = ('event', 'location', 'start_date', 'end_date')
        ordering = ['-start_date']

    @property
    def year(self):
        if self.start_date:
            return self.start_date.year
        return "N/A"

    def __str__(self):
        return f"{self.event.acronym} {self.year} ({self.location})"