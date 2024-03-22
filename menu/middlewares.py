from django.contrib.auth.models import Group
from .models import ItensMenu, GrupoMenu
from django.urls import resolve


class VerificarPermissoesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Executar ações antes que a solicitação seja processada
        resolver_match = resolve(request.path_info)
        request.activemenu = resolver_match.url_name
        if request.user.is_authenticated:
            # Obtém os grupos aos quais o usuário está associado
            grupos_usuario = Group.objects.filter(user=request.user)

            # Set para armazenar os grupos únicos em que o usuário tem permissão
            grupos_com_permissao = set()

            # Verifica se o usuário tem permissão para cada item de menu
            for grupo in grupos_usuario:
                # Retrieve the GrupoMenu instance
                grupo_menu = GrupoMenu.objects.get(grupo_id=grupo.id)
                itens_menu = ItensMenu.objects.filter(grupo_id=grupo_menu)

                for item in itens_menu:
                    if request.user.has_perm(item.permission.codename):
                        # O usuário tem permissão para este item de menu, então adiciona o grupo à lista
                        grupos_com_permissao.add(grupo_menu)

            # Converte o set em uma lista
            grupos_com_permissao = list(grupos_com_permissao)

            # Obtém todos os itens de menu relacionados aos grupos com permissão
            itens_com_permissao = ItensMenu.objects.filter(
                grupo_id__in=grupos_com_permissao)

            # Adiciona os grupos e itens com permissão ao objeto de solicitação
            request.grupos_com_permissao = grupos_com_permissao
            request.itens_com_permissao = itens_com_permissao

        response = self.get_response(request)

        # Executar ações depois que a resposta foi enviada

        return response
