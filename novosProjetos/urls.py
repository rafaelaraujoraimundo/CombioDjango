from django.urls import path
from django.contrib.auth.decorators import permission_required

from .views import (consultoria_delete, consultoria_edit,  ConsultoriaList,
    novosprojetos_dashboard, novosprojetos_list, projetos_delete, ProjetosList,
    sistema_create, sistemas_delete, sistemas_edit, SistemasList, consultoria_create, projeto_create, edit_projeto)

urlpatterns = [
    path('dashboard', novosprojetos_dashboard, name="novosprojetos_dashboard"),
    path('list', novosprojetos_list, name="novosprojetos_list"),
    
    #Consultoria
    path('consultoria/', ConsultoriaList.as_view(), name='projetos_consultoria_list'),
    path('consultoria/new/', consultoria_create, name='projetos_consultoria_new'),
    path('consultoria/<int:consultoria_id>/',consultoria_edit , name='projetos_consultoria_edit'),
    path('consultoriaDelete/<int:consultoria_id>/',consultoria_delete , name='projetos_consultoria_delete'),
    #Sistemas
    path('sistemas/', SistemasList.as_view(), name='projetos_sistemas_list'),
    path('sistemas/new/', sistema_create, name='projetos_sistemas_new'),
    path('sistemas/<int:sistemas_id>/',sistemas_edit , name='projetos_sistemas_edit'),
    path('sistemas/delete/<int:sistemas_id>/',sistemas_delete , name='projetos_sistemas_delete'),
    #Projeto
    path('projetos/', ProjetosList.as_view(), name='projetos_projetos_list'),
    path('projetos/new/', projeto_create, name='projetos_projetos_new'),
    path('projetos/delete/<int:projetos_id>/',projetos_delete , name='projetos_projetos_delete'),
    path('projetos/edit/<int:projeto_id>/', edit_projeto, name='projetos_projeto_edit'),

    #path('servidorfluig/', servidorfluig_list, name="administration_servidorfluig_list"),
    #path('servidorfluig/<int:servidor_id>/',servidorfluig_edit , name='administration_servidorfluig_edit'),
    #path('servidorDelete/<int:servidor_id>/',servidorfluig_delete , name='administration_servidorfluig_delete'),
    #path('servidorfluig/new/', servidorfluig_create, name='administration_servidorfluig_create'),
]
