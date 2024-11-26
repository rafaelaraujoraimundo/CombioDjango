from django.urls import path
from .views import (ConfiguracaoListView, ConfiguracaoCreateView, ConfiguracaoUpdateView, ConfiguracaoDeleteView,
                    SetorEmailListView, SetorEmailCreateView,SetorEmailUpdateView, SetorEmailDeleteView, 
                    generate_signature, combined_view, process_image)

urlpatterns = [
    path('papeldeparede/', ConfiguracaoListView.as_view(), name='configuracao_list'),
    path('papeldeparede/new/', ConfiguracaoCreateView.as_view(), name='configuracao_create'),
    path('papeldeparede/<int:pk>/edit/', ConfiguracaoUpdateView.as_view(), name='configuracao_edit'),
    path('papeldeparede/<int:pk>/delete/', ConfiguracaoDeleteView.as_view(), name='configuracao_delete'),

    path('setoremail/', SetorEmailListView.as_view(), name='setoremail_list'),
    path('setoremail/new/', SetorEmailCreateView.as_view(), name='setoremail_create'),
    path('setoremail/<int:pk>/edit/', SetorEmailUpdateView.as_view(), name='setoremail_edit'),
    path('setoremail/<int:pk>/delete/', SetorEmailDeleteView.as_view(), name='setoremail_delete'),

    path('generate_signature/', generate_signature, name='generate_signature'),
    path('generate/', combined_view, name='generate_signature1'),  # Caminho para acessar a view combinada
    path('generate/processimagem', process_image, name='process_image'),  # Caminho para acessar a view combinada

]