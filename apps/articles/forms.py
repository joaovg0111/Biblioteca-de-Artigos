from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes CSS a todos os campos para estilização consistente
        for field_name, field in self.fields.items():
            # Arquivos e checkboxes têm uma estilização diferente, então aplicamos a classe apenas aos outros
            if not isinstance(field.widget, (forms.FileInput, forms.CheckboxInput)):
                field.widget.attrs.update({
                    'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
                })
        
    class Meta:
        model = Article
        fields = ['title', 'authors', 'abstract', 'pdf_file']

class BibtexUploadForm(forms.Form):
    bibtex_file = forms.FileField(
        label="Arquivo BibTeX (.bib)",
        widget=forms.ClearableFileInput(attrs={
            'class': (
                'block w-full text-sm text-gray-500 '
                'file:mr-4 file:py-2 file:px-4 '
                'file:rounded-md file:border-0 '
                'file:text-sm file:font-semibold '
                'file:bg-blue-50 file:text-blue-700 '
                'hover:file:bg-blue-100'
            )
        })
    )