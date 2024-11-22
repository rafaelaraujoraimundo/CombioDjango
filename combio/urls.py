"""
URL configuration for combio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from menu.views import index, erro_page, error_404_view
from django.conf.urls.static import static
from django.conf import settings
from .api import api
from novosProjetos.views import novosprojetos_dashboard
from django.views.generic.base import RedirectView

handler404 = 'menu.views.error_404_view'
handler500 = 'menu.views.error_500_view'

urlpatterns = [
    path('admin/', admin.site.urls, name="admin1"),
    #path("api/", api.urls),
    path("logout/",auth_views.LogoutView.as_view(template_name="login/logout.html"),name="logout"),
    path('', RedirectView.as_view(url='/inventario/dashboard/', permanent=True),name="index"),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('administration/', include('administration.urls')),
    path('dashboards/', include('dashboard.urls')),
    path('projetos/', include('novosProjetos.urls')),
    path('utils/', include('utils.urls')),
    path("error/",erro_page,name="erro_page"),
    path("error404",error_404_view, name="error_404"),
    path('chatbot/', include('chatbot.urls')),
     path('inventario/', include('inventario.urls')),
     path('suporte/', include('suporte.urls')),
     path('cofre/', include('cofre.urls')),
     path('comunicacao/', include('comunicacao.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
