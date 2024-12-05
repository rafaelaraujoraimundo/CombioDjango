from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventario.models import Celular, Computador, ControleFones, Controlekit, Monitor
from cofre.models import PasswordManager
# Create your views here.

@login_required(login_url='account_login')
def index(request):

    totals = {
        "Teclado/Mouse": Controlekit.objects.count(),
        "Fones": ControleFones.objects.count(),
        "Monitores": Monitor.objects.count(),
        "Computadores": Computador.objects.count(),
        "Celulares": Celular.objects.count(),
        "Passwords": PasswordManager.objects.count(),
    }

    colors = [
        "--iq-color1", "--iq-color2", "--iq-color3",
        "--iq-color4", "--iq-color5", "--iq-color6",
    ]

    
    totals_with_colors = [
        {"model": model, "count": count, "color": color}
        for (model, count), color in zip(totals.items(), colors)
    ]


    title = 'Sistemas Combio'
    context = {
        "title": title, 
       "totals_with_colors": totals_with_colors,
    }

    return render(request, "menu/principal.html", context)


def erro_page(request):
    return render(request, "menu/utils/pages-error.html")

def error_404_view(request, exception=None):
    return render(request, 'menu/utils/pages-error404.html', {})

def error_500_view(request, exception=None):
    return render(request, 'menu/utils/pages-error500.html', {})