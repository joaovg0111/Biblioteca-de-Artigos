from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
# Import BOTH of your custom forms
from .forms import SignUpForm, EmailAuthenticationForm
from .models import Profile

def signup_view(request):
    """
    Handles user registration.
    On GET, it displays a blank registration form.
    On POST, it validates the submitted data. If valid, it creates a new
    user and their profile, logs them in, and redirects to the home page.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # A criação do perfil agora é tratada de forma segura dentro do método save() do SignUpForm.
            # Após a criação, o usuário já é considerado autenticado.
            # No entanto, com múltiplos backends de autenticação, o Django precisa saber
            # qual backend associar à sessão do usuário. Especificar o ModelBackend
            # padrão garante que a sessão seja criada de forma consistente.
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Cadastro realizado com sucesso! Bem-vindo(a), {user.first_name}!")
            return redirect('index')
    else:
        form = SignUpForm()
        
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    """
    Handles user login using email and password.
    """
    if request.method == 'POST':
        # Use our custom EmailAuthenticationForm instead of the default one.
        form = EmailAuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # The form is valid, so we can get the authenticated user.
            # The form's get_user() method handles the email/password check for us.
            user = form.get_user()
            
            # Log the user in.
            login(request, user)
            messages.success(request, f"Login realizado com sucesso. Bem-vindo(a) de volta, {user.first_name}!")
            return redirect('index')
        else:
            # If the form is invalid (bad email/password), show an error.
            messages.error(request, "Email ou senha inválidos. Por favor, tente novamente.")
    else:
        form = EmailAuthenticationForm()
        
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """
    Logs the current user out and redirects to the home page.
    """
    logout(request)
    messages.info(request, "Você foi desconectado com sucesso.")
    return redirect('index')
