from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from utils.views import processar_arquivo, processar_arquivo_ativo, processar_arquivo_ativo_valores

urlpatterns = [
    path('importproducts', processar_arquivo, name="utils_importproduct"),
    path('importproductsativo', processar_arquivo_ativo, name="utils_importproduct_ativo"),
    path('importproductsvalores', processar_arquivo_ativo_valores, name="utils_importproduct_valores"),
]
