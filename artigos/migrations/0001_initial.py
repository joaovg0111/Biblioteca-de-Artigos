
from django.db import migrations, models
import artigos.models
from django.core.validators import FileExtensionValidator
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Artigo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, verbose_name='Título')),
                ('autores', models.CharField(max_length=255, verbose_name='Autores')),
                ('resumo', models.TextField(blank=True, verbose_name='Resumo')),
                ('arquivo', models.FileField(help_text='Envie um arquivo PDF, DOC ou DOCX.', upload_to=artigos.models.caminho_upload, validators=[FileExtensionValidator(['pdf','doc','docx'])], verbose_name='Arquivo')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
            ],
            options={
                'verbose_name': 'Artigo',
                'verbose_name_plural': 'Artigos',
                'ordering': ['-criado_em'],
            },
        ),
    ]
