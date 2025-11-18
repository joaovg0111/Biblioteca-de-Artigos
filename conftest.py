import os
import sys
import pytest

# 🚨 FORÇAR CONFIGURAÇÃO DO DJANGO ANTES DE TUDO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

# Importar e configurar Django imediatamente
import django
from django.conf import settings

if not settings.configured:
    django.setup()

print("✅ Django configurado com sucesso no conftest.py")
print(f"📦 INSTALLED_APPS: {len(settings.INSTALLED_APPS)} apps carregados")


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(early_config, parser, args):
    """
    Hook que é executado ANTES de qualquer coleta de testes.
    Garante que Django esteja configurado antes de importar modelos.
    """
    print("🔧 pytest_load_initial_conftests: Configurando Django ANTES da coleta")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    if not settings.configured:
        django.setup()
        print("✅ Django configurado via pytest_load_initial_conftests")
# Este arquivo é usado para definir fixtures globais para o pytest.
# Deixe este arquivo vazio por enquanto.
# O pytest-django cuidará da configuração do Django usando as
# informações do arquivo pytest.ini.
#
# Adicionar chamadas manuais como `django.setup()` aqui causa
# conflitos e erros como "Conflicting models".
