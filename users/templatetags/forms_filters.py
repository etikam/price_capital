from django.template import Library

register = Library()


# un filtre personnalisé pour vidé les champs invalides en maintenir les champs valide en cas de ValidationError
def default_if_none(value):
    return value if value else ''

register.filter('default_if_none', default_if_none)
