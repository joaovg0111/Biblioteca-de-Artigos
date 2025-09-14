from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    Extends Django's built-in User model to store extra information.
    There is a one-to-one link between a User and a Profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliation = models.CharField(max_length=255, blank=True, verbose_name="Afiliação Institucional")
    interests = models.CharField(max_length=255, blank=True, verbose_name="Interesses de Pesquisa")
    biography = models.TextField(blank=True, verbose_name="Biografia do Perfil")

    def __str__(self):
        return f"Profile for {self.user.username}"
