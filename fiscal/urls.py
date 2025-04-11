from django.urls import path
from .views import unificar_sped

urlpatterns = [
    path('sped-unificador/', unificar_sped, name='sped_unificador'),
]
