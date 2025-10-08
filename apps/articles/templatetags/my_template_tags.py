from django import template

register = template.Library()

@register.filter(name='dict_get')
def dict_get(dictionary, key):
    """Permite acessar um valor de dicionário usando uma variável como chave no template."""
    return dictionary.get(key)