from django import template
from quejas.constantes import COLOR_ESTADO

register = template.Library()


@register.filter
def color_estado(estado):
    """Devuelve la clase Bootstrap correspondiente al estado de una queja."""
    return COLOR_ESTADO.get(estado, 'secondary')


@register.simple_tag(takes_context=True)
def url_pagina(context, numero_pagina):
    """Construye la URL de paginación preservando los filtros activos."""
    params = context['request'].GET.copy()
    params['page'] = numero_pagina
    return f'?{params.urlencode()}'
