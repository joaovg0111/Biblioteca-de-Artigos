from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
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
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
        })
    )
    bibtex_text = forms.CharField(
        label="Ou cole o conteúdo BibTeX aqui",
        required=False,
        widget=forms.Textarea(attrs={'rows': 10, 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'})
    )
    ignore_missing_fields = forms.BooleanField(
        label="Tentar importar artigos mesmo com campos obrigatórios faltando (ex: ano, autor).",
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        bibtex_file = cleaned_data.get('bibtex_file')
        bibtex_text = cleaned_data.get('bibtex_text')
        if not bibtex_file and not bibtex_text:
            raise forms.ValidationError("Você deve fornecer um arquivo BibTeX ou colar o conteúdo no campo de texto.", code='required')
        return cleaned_data

class ArticlePreviewForm(forms.Form):
    import_this = forms.BooleanField(required=False, initial=True)
    
    # --- MUDANÇA: Campos agora são required=False; a validação é feita no método clean() ---
    title = forms.CharField(label="Título", required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    authors = forms.CharField(label="Autores", required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    year = forms.CharField(label="Ano", required=False, widget=forms.TextInput(attrs={'class': 'vTextField', 'size': '4'}))
    booktitle = forms.CharField(label="Journal/Booktitle", required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    
    keywords = forms.CharField(label="Palavras-chave", required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    abstract = forms.CharField(label="Resumo", required=False, widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 3}))
    pages = forms.CharField(label="Páginas", required=False, widget=forms.TextInput(attrs={'class': 'vTextField', 'size': '10'}))
    location = forms.CharField(label="Localização", required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))
    publisher = forms.CharField(label="Publicador", required=False, widget=forms.TextInput(attrs={'class': 'vTextField'}))

    def clean(self):
        cleaned_data = super().clean()
        
        # A validação só é acionada se o usuário explicitamente marcou este item para importação.
        if cleaned_data.get('import_this'):
            if not cleaned_data.get('title'):
                self.add_error('title', 'Título é obrigatório para importação.')
            if not cleaned_data.get('authors'):
                self.add_error('authors', 'Autores são obrigatórios para importação.')
            if not cleaned_data.get('year'):
                self.add_error('year', 'Ano é obrigatório para importação.')
            if not cleaned_data.get('booktitle'):
                self.add_error('booktitle', 'Journal/Booktitle é obrigatório para importação.')
        
        return cleaned_data