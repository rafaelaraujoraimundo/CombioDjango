from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from menu.menu import GetGroup, GetMenu, backup_dados
# Create your views here.


def index(request):
    activegroup = 'index'
    activemenu = 'index'
    groups = GetGroup()
    menus = GetMenu()
    #a = backup_dados()
    user_groups = request.user.groups.all()
    context = {
        "nome_pagina": "Página inicial", 'groups': groups,
        'menus': menus, 'activegroup': activegroup,
        'activemenu': activemenu, 'user_groups': user_groups
    }

    return render(request, "menu/index.html", context)


def erro_page(request):
    return render(request, "menu/utils/pages-error.html")

def error_404_view(request, exception=None):
    return render(request, 'menu/utils/pages-error404.html', {})

def error_500_view(request, exception=None):
    return render(request, 'menu/utils/pages-error500.html', {})