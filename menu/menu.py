from menu.models import GrupoMenu, ItensMenu
from django.core import serializers


def GetGroup():
    groupMenu = GrupoMenu.objects.all()
    return groupMenu


def GetMenu():
    itensmenu = ItensMenu.objects.all()
    return itensmenu


def backup_dados():
    registros = GrupoMenu.objects.all()
    serialized_data = serializers.serialize('json', registros)
    backup_file = 'GrupoMenu.json'
    with open(backup_file, 'w') as file:
        file.write(serialized_data)

    registrosItens = ItensMenu.objects.all()
    serialized_data = serializers.serialize('json', registrosItens)
    backup_file = 'Menu.json'
    with open(backup_file, 'w') as file:
        file.write(serialized_data)
    print('Dados salvos com sucesso!')

    # Função para retornar os dados se nescessário
    # python manage.py loaddata caminho_do_backup/backup.json
    return True
