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

    def clean_authors(self):
        """
        Limpa e formata a string de autores.
        Garante que os nomes sejam separados por vírgula e sem espaços extras.
        """
        authors_string = self.cleaned_data.get('authors', '')
        authors_list = [author.strip() for author in authors_string.split(',') if author.strip()]
        return ", ".join(authors_list)

class BibtexUploadForm(forms.Form):
    bibtex_file = forms.FileField(
        label="Arquivo BibTeX (.bib)",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
        })
    )
    pdf_zip_file = forms.FileField(
        label="Arquivo ZIP com PDFs (Opcional)",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': (
                'block w-full text-sm text-gray-500 '
                'file:mr-4 file:py-2 file:px-4 '
                'file:rounded-md file:border-0 '
                'file:text-sm file:font-semibold '
                'file:bg-purple-50 file:text-purple-700 '
                'hover:file:bg-purple-100'
            )
        }),
        help_text="Envie um arquivo .zip contendo os PDFs. O nome de cada PDF deve ser igual ao ID da entrada BibTeX (ex: sbes-paper1.pdf)."
    )
    bibtex_text = forms.CharField(
        label="Ou cole o conteúdo BibTeX aqui",
        required=False,
        widget=forms.Textarea(attrs={'rows': 10, 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'})
    )

    def clean(self):
        cleaned_data = super().clean()
        bibtex_file = cleaned_data.get('bibtex_file')
        bibtex_text = cleaned_data.get('bibtex_text')
        if not bibtex_file and not bibtex_text:
            raise forms.ValidationError(
                "Você deve fornecer um arquivo BibTeX ou colar o conteúdo no campo de texto.",
                code='required'
            )
        return cleaned_data
