import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_validators_help_text_html
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Profile

class SignUpForm(UserCreationForm):
    """
    A form for creating new users. It extends the base UserCreationForm to add
    custom validation, consistent styling, and additional profile fields.
    """
    # Define um dicionário de atributos de widget comum para manter a consistência.
    default_widget_attrs = {
        'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
    }

    # Redefine os campos do UserCreationForm para aplicar estilos consistentes.
    # A ordem aqui definirá a ordem no template se usarmos {% for field in form %}.
    username = forms.CharField(
        label="Nome de usuário",
        widget=forms.TextInput(attrs=default_widget_attrs)
    )
    first_name = forms.CharField(
        label="Nome",
        widget=forms.TextInput(attrs=default_widget_attrs)
    )
    last_name = forms.CharField(
        label="Sobrenome",
        widget=forms.TextInput(attrs=default_widget_attrs)
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs=default_widget_attrs)
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs=default_widget_attrs),
        help_text=password_validators_help_text_html()
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs=default_widget_attrs),
        help_text="Digite a mesma senha que antes, para verificação."
    )

    # Campos adicionais para o perfil do usuário.
    affiliation = forms.CharField(
        label="Afiliação Institucional",
        required=False,
        widget=forms.TextInput(attrs=default_widget_attrs)
    )
    interests = forms.CharField(
        label="Interesses de Pesquisa",
        required=False,
        widget=forms.TextInput(attrs=default_widget_attrs),
        help_text="Separe os interesses por vírgula."
    )
    biography = forms.CharField(
        label="Biografia",
        required=False,
        widget=forms.Textarea(attrs={
            **default_widget_attrs,
            'rows': 4
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Agora que todos os campos estão definidos acima, listamos a ordem desejada.
        # O UserCreationForm ainda cuidará da lógica de validação da senha.
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'affiliation', 'interests', 'biography')

    @transaction.atomic
    def save(self, commit=True):
        """
        Salva o usuário e, em seguida, cria e salva o perfil associado.
        Usa uma transação para garantir que ambas as operações ocorram com sucesso.
        """
        user = super().save(commit=commit)
        if commit:
            Profile.objects.create(
                user=user,
                affiliation=self.cleaned_data.get('affiliation', ''),
                interests=self.cleaned_data.get('interests', ''),
                biography=self.cleaned_data.get('biography', '')
            )
        return user

    def clean_first_name(self):
        """
        Custom validation to ensure the first name contains only letters.
        """
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[\w\s]+$', first_name, re.UNICODE):
            raise ValidationError("O nome deve conter apenas letras e espaços.")
        return first_name

    def clean_last_name(self):
        """
        Custom validation to ensure the last name contains only letters and spaces.
        """
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[\w\s]+$', last_name, re.UNICODE):
            raise ValidationError("O sobrenome deve conter apenas letras e espaços.")
        return last_name

    def clean_email(self):
        """
        Custom validation to check if the email is already registered.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Este endereço de e-mail já está em uso.")
        return email

class EmailAuthenticationForm(AuthenticationForm):
    """
    Overrides the default AuthenticationForm to use email instead of username.
    """
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm'})
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm'}),
    )
