from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-$s7!d&snj^)h2sz-m1jvt$_ht_y&@*=(not^s_u=&54zcpox)5'
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # --- MUDANÇA: Adicione esta linha ---

    "apps.users",
    "apps.events",
    "apps.articles",
    "apps.notifications",  # --- MUDANÇA: Adicione esta linha ---
]

# --- MUDANÇA: Adicione esta linha ---
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'apps.users.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CONFIGURAÇÃO DE E-MAIL ---
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    # Se as credenciais SMTP estiverem definidas, usa o backend SMTP para enviar e-mails reais.
    # Exemplo para Gmail (requer "Senha de App" se a verificação em 2 etapas estiver ativa).
    print("\n✅ Credenciais de e-mail encontradas! Configurando para envio via SMTP (Gmail)...")
    # --- MUDANÇA: Alterando de TLS para SSL ---
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 465)) # Porta para SSL
    EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'True') == 'True' # Usar SSL em vez de TLS
    EMAIL_USE_TLS = False # Garantir que TLS não seja usado
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

    # --- DEBUGGING: Imprime as configurações que estão sendo usadas (exceto a senha) ---
    print(f"   - EMAIL_HOST: {EMAIL_HOST}")
    print(f"   - EMAIL_PORT: {EMAIL_PORT}")
    print(f"   - EMAIL_USE_SSL: {EMAIL_USE_SSL}")
    print(f"   - EMAIL_HOST_USER: {EMAIL_HOST_USER}\n")
else:
    # Se as credenciais não estiverem definidas, imprime os e-mails no console.
    # Isso evita que o servidor quebre durante o desenvolvimento.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    print("\nAVISO: Credenciais de e-mail não configuradas. E-mails serão impressos no console.\n")