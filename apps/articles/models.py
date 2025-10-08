# COPIE E COLE O CONTEÚDO COMPLETO PARA: apps/articles/models.py

from django.db import models
from django.conf import settings
from datetime import datetime
import os
import uuid

# --- IMPORTAMOS APENAS O 'Edition' AGORA ---
from apps.events.models import Edition

def article_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid.uuid4()}{ext}"
    return f'articles/{datetime.now().year}/{new_filename}'

class Article(models.Model):
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Enviado por")
    title = models.CharField("Título", max_length=255)
    
    authors = models.CharField("Autores", max_length=500, help_text="Separe os nomes dos autores por vírgula")
    
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, verbose_name="Edição", related_name="articles", null=True, blank=True)

    abstract = models.TextField("Resumo", blank=True)
    
    keywords = models.CharField("Palavras-chave", max_length=255, blank=True, help_text="Separe as palavras-chave por vírgula")

    # --- MUDANÇA: Novos campos para dados do BibTeX ---
    pages = models.CharField("Páginas", max_length=50, blank=True)
    location = models.CharField("Localização (BibTeX)", max_length=100, blank=True)
    publisher = models.CharField("Publicador (BibTeX)", max_length=100, blank=True)

    pdf_file = models.FileField("Arquivo PDF", upload_to=article_upload_path, blank=True, null=True)
    original_filename = models.CharField("Nome Original do Arquivo", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"

    def __str__(self):
        return self.title