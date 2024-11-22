from ninja import Router
from django.shortcuts import get_object_or_404
from administration.models import Parametro
from .schema import PapelDeParedeSchema
import logging

routerParametro = Router()



logger = logging.getLogger(__name__)

def get_or_default(param_code, default_value=None):
    try:
        return Parametro.objects.get(codigo=param_code).valor
    except Parametro.DoesNotExist:
        return default_value

@routerParametro.get("/papeldeparede", response=PapelDeParedeSchema)
def get_papeldeparede(request):
    url_papeldeparede = get_or_default('url_papeldeparede','http://179.191.91.6:810/media/papeldeparede/papelparede.jpg')
    url_bloqueio = get_or_default('url_bloqueio', 'http://179.191.91.6:810/media/papeldeparede/bloqueio.jpg')
    pasta_papeldeparede = get_or_default('pasta_papelparede','C:/combio/wallpaper-combio/')

    return PapelDeParedeSchema(
        url_papeldeparede=url_papeldeparede,
        url_bloqueio=url_bloqueio,
        pasta_papeldeparede=pasta_papeldeparede
    )