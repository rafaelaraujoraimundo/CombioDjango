from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='account_login')
def index(request):
    title = 'Sistema Combio'
    context = {
        "title": title, 
    }

    return render(request, "menu/principal.html", context)


def erro_page(request):
    return render(request, "menu/utils/pages-error.html")

def error_404_view(request, exception=None):
    return render(request, 'menu/utils/pages-error404.html', {})

def error_500_view(request, exception=None):
    return render(request, 'menu/utils/pages-error500.html', {})