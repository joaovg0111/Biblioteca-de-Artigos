
"""Modelos de dados para artigos científicos (comentários em PT-BR)."""
from django.db import models
from django.core.validators import FileExtensionValidator

def caminho_upload(instance, filename):
    """Salva em artigos/<id>/<arquivo>; requer que a instância já tenha pk."""
    return f"artigos/{instance.pk}/{filename}"

class Artigo(models.Model):
    titulo = models.CharField('Título', max_length=255)
    autores = models.CharField('Autores', max_length=255)
    resumo = models.TextField('Resumo', blank=True)
    arquivo = models.FileField('Arquivo', upload_to=caminho_upload,
        validators=[FileExtensionValidator(['pdf','doc','docx'])],
        help_text='Envie um arquivo PDF, DOC ou DOCX.')
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'
    def __str__(self):
        return self.titulo
