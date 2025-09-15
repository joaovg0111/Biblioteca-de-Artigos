import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    """
    A form for creating new users. It extends the base UserCreationForm to add
    custom validation and additional fields like first name, last name, and email.
    """
    first_name = forms.CharField(max_length=150, required=True, label="Nome")
    last_name = forms.CharField(max_length=150, required=True, label="Sobrenome")
    email = forms.EmailField(max_length=254, required=True, help_text='Obrigatório.', label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        # Define the fields that will be handled by this form.
        # UserCreationForm already provides 'username', 'password2', and 'password2'.
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def clean_first_name(self):
        """
        Custom validation to ensure the first name contains only letters.
        """
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[a-zA-Z\s]+$', first_name):
            raise ValidationError("O nome deve conter apenas letras e espaços.")
        return first_name

    def clean_last_name(self):
        """
        Custom validation to ensure the last name contains only letters.
        """
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[a-zA-Z\s]+$', last_name):
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

