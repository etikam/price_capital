from django import template

register = template.Library()

@register.filter(name='times')
def times(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''


@register.filter(name='get_item')
def get_item(dictionary, key):
    """Filtre personnalisé pour accéder à un élément d'un dictionnaire."""
    return dictionary.get(key)