from django.contrib.auth.models import Group
from .models import ItensMenu, GrupoMenu
from django.urls import resolve
from administration.models import User

class VerificarPermissoesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Executar ações antes que a solicitação seja processada
        resolver_match = resolve(request.path_info)
        request.activemenu = resolver_match.url_name
        
        if request.user.is_authenticated:
            # Obtém os grupos aos quais o usuário está associado
            #user_admin = User.objects.filter(id=1).first()
            #grupos_usuario = Group.objects.filter(user=user_admin)
            grupos_usuario = Group.objects.filter(user=request.user)
            # Set para armazenar os grupos únicos em que o usuário tem permissão
            grupos_com_permissao = set()
            itens_com_permissao = set()
            # Verifica se o usuário tem permissão para cada item de menu
            for grupo in grupos_usuario:
                # Retrieve the GrupoMenu instance
                grupo_menu = GrupoMenu.objects.get(grupo_id=grupo.id)
                itens_menu = ItensMenu.objects.filter(grupo_id_id=grupo_menu.id).order_by('order')

                for item in itens_menu:
                    if request.user.has_perm(f'{item.permission.content_type.app_label}.{item.permission.codename}'):
                        # O usuário tem permissão para este item de menu, então adiciona o grupo à lista
                        grupos_com_permissao.add(grupo_menu)
                        itens_com_permissao.add(item)
            # Converte o set em uma lista e ordena os grupos
            grupos_com_permissao = sorted(list(grupos_com_permissao), key=lambda x: x.order)
            itens_com_permissao = sorted(list(itens_com_permissao), key=lambda x: x.order)

            # Obtém todos os itens de menu relacionados aos grupos com permissão e os ordena
            #itens_com_permissao = ItensMenu.objects.filter(
            #    grupo_id__in=grupos_com_permissao
            #).order_by('grupo_id__order', 'order')

            # Adiciona os grupos e itens com permissão ao objeto de solicitação
            request.grupos_com_permissao = grupos_com_permissao
            request.itens_com_permissao = itens_com_permissao

        response = self.get_response(request)

        # Executar ações depois que a resposta foi enviada

        return response

class VerificarPermissoesMiddleware1:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Executar ações antes que a solicitação seja processada
        resolver_match = resolve(request.path_info)
        request.activemenu = resolver_match.url_name
        
        if request.user.is_authenticated:
            grupos_usuario = Group.objects.filter(user=request.user)
            grupos_com_permissao = set()
            itens_com_permissao = []

            # Verifica se o usuário tem permissão para cada grupo e seus itens de menu
            for grupo in grupos_usuario:
                grupo_menu = GrupoMenu.objects.get(grupo=grupo)
                itens_menu = ItensMenu.objects.filter(grupo_id_id=grupo_menu.id).order_by('order')

                for item in itens_menu:
                    # Verificar permissão para cada item de menu
                    if request.user.has_perm(f'{item.permission.content_type.app_label}.{item.permission.codename}'):
                        grupos_com_permissao.add(grupo_menu)
                        itens_com_permissao.append(item)

            # Ordena os grupos com permissão
            grupos_com_permissao = sorted(list(grupos_com_permissao), key=lambda x: x.order)

            # Ordena os itens de menu com permissão
            itens_com_permissao.sort(key=lambda x: (x.grupo.order, x.order))

            # Adiciona os grupos e itens com permissão ao objeto de solicitação
            request.grupos_com_permissao = grupos_com_permissao
            request.itens_com_permissao = itens_com_permissao

        # Processa a solicitação e gera a resposta
        response = self.get_response(request)

        # Executar ações depois que a resposta foi enviada
        return response
