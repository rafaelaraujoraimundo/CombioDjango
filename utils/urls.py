from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from utils.views import processar_arquivo

urlpatterns = [
    path('importproducts', processar_arquivo, name="utils_importproduct"),
]
