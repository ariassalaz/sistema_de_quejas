from django import template
from quejas.constantes import COLOR_ESTADO

register = template.Library()


@register.filter
def color_estado(estado):
    """Devuelve la clase Bootstrap correspondiente al estado de una queja."""
    return COLOR_ESTADO.get(estado, 'secondary')
