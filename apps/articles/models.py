from django.db import models
from apps.events.models import Edition

def article_upload_path(instance, filename):
    """
    Gera dinamicamente o caminho onde o arquivo enviado será salvo.
    ex: media/articles/2024/meu_artigo.pdf
    """
    return f'articles/{instance.edition.year}/{filename}'

class Article(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name='articles', verbose_name="Edição")
    title = models.CharField("Título", max_length=255)
    authors = models.CharField("Autores", max_length=500)
    abstract = models.TextField("Resumo", blank=True)
    pdf_file = models.FileField("Arquivo PDF", upload_to=article_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
