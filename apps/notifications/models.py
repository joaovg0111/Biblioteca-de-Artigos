# COPIE E COLE O CONTEÚDO COMPLETO PARA: apps/notifications/models.py

from django.db import models
from django.conf import settings

class UserInterest(models.Model):
    """
    Armazena uma única palavra-chave de interesse para um usuário.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interests")
    keyword = models.CharField("Palavra-chave de Interesse", max_length=100)

    class Meta:
        # Garante que um usuário não possa se inscrever na mesma palavra-chave duas vezes
        unique_together = ('user', 'keyword')
        verbose_name = "Interesse de Usuário"
        verbose_name_plural = "Interesses de Usuários"

    def __str__(self):
        return f"{self.user.username} -> {self.keyword}"