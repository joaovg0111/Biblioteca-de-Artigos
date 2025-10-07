# CRIE ESTE NOVO ARQUIVO EM: apps/notifications/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from apps.articles.models import Article
from .models import UserInterest
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Article)
def notify_users_on_new_article(sender, instance, created, **kwargs):
    """
    Este sinal é acionado sempre que um novo artigo é salvo.
    Se o artigo for novo (created=True), ele notifica os usuários interessados.
    """
    if created and instance.keywords:
        # Pega as palavras-chave do novo artigo, converte para minúsculas e remove espaços
        article_keywords = {kw.strip().lower() for kw in instance.keywords.split(',') if kw.strip()}
        
        if not article_keywords:
            return

        # Encontra todos os interesses de usuários que correspondem às palavras-chave do artigo
        matching_interests = UserInterest.objects.filter(keyword__in=article_keywords).select_related('user')
        
        # Agrupa os interesses por usuário para enviar um único e-mail por pessoa
        users_to_notify = {}
        for interest in matching_interests:
            if interest.user.email: # Apenas se o usuário tiver um e-mail cadastrado
                if interest.user.id not in users_to_notify:
                    users_to_notify[interest.user.id] = {
                        'user': interest.user,
                        'keywords': set()
                    }
                users_to_notify[interest.user.id]['keywords'].add(interest.keyword)
        
        # Constrói a URL completa para o artigo
        domain = Site.objects.get_current().domain
        protocol = 'http' # Use http para desenvolvimento local
        article_url = f"{protocol}://{domain}/articles/{instance.id}/"

        # Envia um e-mail para cada usuário
        for user_id, data in users_to_notify.items():
            user = data['user']
            matching_keywords = list(data['keywords'])
            
            subject = f"[Biblioteca Digital] Novo Artigo de seu Interesse: '{instance.title[:50]}...'"
            
            email_context = {
                'user': user,
                'article': instance,
                'matching_keywords': matching_keywords,
                'article_url': article_url
            }
            
            message = render_to_string('notifications/new_article_notification_email.txt', email_context)
            
            send_mail(
                subject=subject,
                message=message,
                from_email='nao-responda@bibliotecadigital.com', # Remetente genérico
                recipient_list=[user.email],
                fail_silently=False,
            )