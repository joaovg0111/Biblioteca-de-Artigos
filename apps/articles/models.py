from django.db import models
from datetime import datetime
from django.conf import settings
import os
import uuid

def article_upload_path(instance, filename):
    """
    Usa um UUID para garantir um nome de arquivo único e evitar colisões.
    ex: media/articles/2024/f47ac10b-58cc-4372-a567-0e02b2c3d479.pdf
    """
    # Pega a extensão do arquivo original
    ext = os.path.splitext(filename)[1]
    # Gera um nome de arquivo único usando UUID4
    new_filename = f"{uuid.uuid4()}{ext}"
    # Organiza em pastas baseadas no ano atual
    return f'articles/{datetime.now().year}/{new_filename}'

class Article(models.Model):
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Enviado por")
    title = models.CharField("Título", max_length=255)
    authors = models.CharField("Autores", max_length=500)
    abstract = models.TextField("Resumo", blank=True)
    pdf_file = models.FileField("Arquivo PDF", upload_to=article_upload_path, blank=True, null=True)
    original_filename = models.CharField("Nome Original do Arquivo", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Se o objeto já existe no banco de dados, verifica se o arquivo foi alterado.
        if self.pk:
            try:
                old_instance = Article.objects.get(pk=self.pk)
                # Se o arquivo antigo existe e é diferente do novo, apaga o antigo.
                if old_instance.pdf_file and old_instance.pdf_file != self.pdf_file:
                    old_instance.pdf_file.delete(save=False)
            except Article.DoesNotExist:
                pass  # O objeto é novo, não faz nada.
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Antes de deletar o objeto do banco de dados, apaga o arquivo associado.
        if self.pdf_file:
            self.pdf_file.delete(save=False)
        super().delete(*args, **kwargs)
