from django.urls import path
from .views import (acoesprontuario_delete, acoesprontuario_edit, AcoesProntuarioCreate,
    AcoesProntuarioList, celular_delete, CelularCreate, CelularList, CelularUpdate,
    computador_delete, ComputadorCreate, ComputadorList, ComputadorUpdate, controlefones_delete,
    ControleFonesCreate, ControleFonesList, ControleFonesUpdate, controlekit_delete,
    ControlekitCreate, ControlekitList, ControlekitUpdate, estoque_delete, estoque_edit,
    EstoqueCreate, EstoqueList, monitor_delete, MonitorCreate, MonitorList, MonitorUpdate,
    prontuario_computador_delete, ProntuarioCelularCreate, ProntuarioCelularDelete,
    ProntuarioCelularListView, ProntuarioCelularUpdate, ProntuarioComputadorCreate,
    ProntuarioComputadorListView, ProntuarioComputadorUpdate, ProntuarioMonitorCreate,
    ProntuarioMonitorDelete, ProntuarioMonitorListView, ProntuarioMonitorUpdate, status_delete,
    status_edit, StatusCreate, StatusList, tipoItem_delete, TipoItem_edit, TipoItemCreate,
    TipoItemList)

urlpatterns = [
    path('tipoitem/', TipoItemList.as_view(), name='tipoitem_list'),
    path('tipoitem/new/', TipoItemCreate.as_view(), name='tipoitem_new'),
    path('tipoitem/edit/<int:tipoitem_id>/', TipoItem_edit, name='tipoitem_edit'),
    path('tipoitem/delete/<int:tipoitem_id>/', tipoItem_delete, name='tipoitem_delete'),

    path('status/', StatusList.as_view(), name='status_list'),
    path('status/new/', StatusCreate.as_view(), name='status_new'),
    path('status/edit/<int:status_id>/', status_edit, name='status_edit'),
    path('status/delete/<int:status_id>/', status_delete, name='status_delete'),

    path('estoque/', EstoqueList.as_view(), name='estoque_list'),
    path('estoque/new/', EstoqueCreate.as_view(), name='estoque_new'),
    path('estoque/edit/<int:estoque_id>/', estoque_edit, name='estoque_edit'),
    path('estoque/delete/<int:estoque_id>/', estoque_delete, name='estoque_delete'),

    path('controlekit/', ControlekitList.as_view(), name='controlekit_list'),
    path('controlekit/new/', ControlekitCreate.as_view(), name='controlekit_new'),
    path('controlekit/edit/<int:pk>/', ControlekitUpdate.as_view(), name='controlekit_edit'),
    path('controlekit/delete/<int:controlekit_id>/', controlekit_delete, name='controlekit_delete'),

    path('controlefones/', ControleFonesList.as_view(), name='controlefones_list'),
    path('controlefones/new/', ControleFonesCreate.as_view(), name='controlefones_new'),
    path('controlefones/edit/<int:pk>/', ControleFonesUpdate.as_view(), name='controlefones_edit'),
    path('controlefones/delete/<int:controlefones_id>/', controlefones_delete, name='controlefones_delete'),


    path('celular/', CelularList.as_view(), name='celular_list'),
    path('celular/new/', CelularCreate.as_view(), name='celular_create'),
    path('celular/edit/<int:pk>/', CelularUpdate.as_view(), name='celular_edit'),
    path('celular/delete/<int:celular_id>/', celular_delete, name='celular_delete'),

    path('acoesprontuario/', AcoesProntuarioList.as_view(), name='acoesprontuario_list'),
    path('acoesprontuario/new/', AcoesProntuarioCreate.as_view(), name='acoesprontuario_new'),
    path('acoesprontuario/edit/<int:acoesprontuario_id>/', acoesprontuario_edit, name='acoesprontuario_edit'),
    path('acoesprontuario/delete/<int:acoesprontuario_id>/', acoesprontuario_delete, name='acoesprontuario_delete'),

    path('celular/<int:celular_id>/prontuario/', ProntuarioCelularListView.as_view(), name='prontuario_celular_list'),
    path('celular/<int:celular_id>/prontuario/novo/', ProntuarioCelularCreate.as_view(), name='prontuario_celular_create'),
    path('prontuario/<int:pk>/editar/', ProntuarioCelularUpdate.as_view(), name='prontuario_celular_edit'),
    path('prontuario/<int:pk>/excluir/', ProntuarioCelularDelete.as_view(), name='prontuario_celular_delete'),

    path('monitores/', MonitorList.as_view(), name='monitor_list'),
    path('monitores/novo/', MonitorCreate.as_view(), name='monitor_create'),
    path('monitores/<int:pk>/editar/', MonitorUpdate.as_view(), name='monitor_edit'),
    path('monitores/delete/<int:monitor_id>/', monitor_delete, name='monitor_delete'),
    
    path('monitores/<int:monitor_id>/prontuario/',ProntuarioMonitorListView.as_view(), name='prontuario_monitor_list'),
    path('monitores/<int:monitor_id>/prontuario/novo/', ProntuarioMonitorCreate.as_view(), name='prontuario_monitor_create'),
    path('monitores/prontuario/<int:pk>/editar/', ProntuarioMonitorUpdate.as_view(), name='prontuario_monitor_edit'),
    path('monitores/prontuario/<int:pk>/delete/', ProntuarioMonitorDelete.as_view(), name='prontuario_monitor_delete'),

    path('computador/', ComputadorList.as_view(), name='computador_list'),
    path('computador/new/', ComputadorCreate.as_view(), name='computador_create'),
    path('computador/edit/<int:pk>/', ComputadorUpdate.as_view(), name='computador_edit'),
    path('computador/delete/<int:pk>/', computador_delete, name='computador_delete'),

        path('computador/<int:computador_id>/prontuario/', ProntuarioComputadorListView.as_view(), name='prontuario_computador_list'),
    path('computador/<int:computador_id>/prontuario/new/', ProntuarioComputadorCreate.as_view(), name='prontuario_computador_create'),
    path('prontuario/computador/edit/<int:pk>/', ProntuarioComputadorUpdate.as_view(), name='prontuario_computador_edit'),
    path('prontuario/computador/delete/<int:pk>/', prontuario_computador_delete, name='prontuario_computador_delete'),
]
