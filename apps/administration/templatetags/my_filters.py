from django import template

register = template.Library()

@register.filter(name="format_gb")
def format_gb(value):
    """Formata o valor para duas casas decimais e adiciona a unidade GB."""
    return "{:.2f} GB".format(value / (1024 ** 3))


@register.filter(name="to_int")
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0