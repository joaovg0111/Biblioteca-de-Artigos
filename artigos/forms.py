
"""Formulários com validação de tamanho/ extensão em PT-BR."""
from django import forms
from .models import Artigo
TAMANHO_MAX_MB = 25
class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo','autores','resumo','arquivo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control','placeholder':'Ex.: Um Estudo Sobre X'}),
            'autores': forms.TextInput(attrs={'class':'form-control','placeholder':'Nome do Autor; Nome da Autora'}),
            'resumo': forms.Textarea(attrs={'class':'form-control','rows':4,'placeholder':'Resumo (opcional)'}),
        }
        labels = {'titulo':'Título','autores':'Autores','resumo':'Resumo','arquivo':'Arquivo'}
    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        if arquivo:
            tamanho_mb = arquivo.size / (1024*1024)
            if tamanho_mb > TAMANHO_MAX_MB:
                raise forms.ValidationError(f"O arquivo excede {TAMANHO_MAX_MB} MB. Tamanho enviado: {tamanho_mb:.2f} MB")
        return arquivo
