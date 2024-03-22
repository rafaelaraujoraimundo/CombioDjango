from django import template
from datetime import datetime

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

@register.filter(name='timestamp_to_date')
def timestamp_to_date(value):
    try:
        # Converte o valor para inteiro antes da divisão
        timestamp = int(value)
        date_time = datetime.fromtimestamp(timestamp / 1000.0)
        return date_time.strftime('%d/%m/%Y - %H:%M:%S')
    except ValueError:
        return value 

@register.filter(name='milliseconds_to_duration')
def milliseconds_to_duration(value):
    try:
        # Converte o valor para inteiro antes da divisão
        milliseconds = int(value)
        seconds = int(milliseconds / 1000)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    except ValueError:
        return value