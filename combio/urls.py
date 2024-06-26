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
from menu.views import index, erro_page
from django.conf.urls.static import static
from django.conf import settings
from .api import api



urlpatterns = [
    path('admin/', admin.site.urls, name="admin1"),
    #path("api/", api.urls),
    path("logout/",auth_views.LogoutView.as_view(template_name="login/logout.html"),name="logout"),
    path("",index,name="index"),
    path('accounts/', include('allauth.urls')),
    path('administration/', include('administration.urls')),
    path('dashboards/', include('dashboard.urls')),
    path('utils/', include('utils.urls')),
    path("error/",erro_page,name="erro_page"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
