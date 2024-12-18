from django import template

register = template.Library()

@register.filter(name='times')
def times(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''
