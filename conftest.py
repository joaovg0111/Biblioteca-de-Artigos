import os
import django
from django.conf import settings

def pytest_configure(config):
    """Configure Django before running tests."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    if not settings.configured:
        django.setup()
