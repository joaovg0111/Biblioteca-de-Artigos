
        #!/bin/sh
        set -e
        echo "==> Aplicando migrações"
        python manage.py migrate --noinput
        echo "==> Coletando arquivos estáticos"
        python manage.py collectstatic --noinput || true
        if [ "$DJANGO_CREATE_SUPERUSER" = "1" ]; then
          echo "==> Criando superusuário (se ainda não existir)"
          python - <<'PY'
import os
import django
from django.core.exceptions import ObjectDoesNotExist
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_artigos.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')
try:
    User.objects.get(username=username)
    print("Superusuário já existe. Pulando.")
except ObjectDoesNotExist:
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superusuário criado: ", username)
PY
        fi
        echo "==> Iniciando servidor"
        if [ "$DEBUG" = "1" ]; then
          exec python manage.py runserver 0.0.0.0:8000
        else
          exec gunicorn site_artigos.wsgi:application --bind 0.0.0.0:8000 --workers 3
        fi
