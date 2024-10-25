from django.urls import path
from .views import (celular_delete, CelularCreate, CelularList, CelularUpdate,
    controlefones_delete, ControleFonesCreate, ControleFonesList, ControleFonesUpdate,
    controlekit_delete, ControlekitCreate, ControlekitList, ControlekitUpdate, estoque_delete,
    estoque_edit, EstoqueCreate, EstoqueList, status_delete, status_edit, StatusCreate, StatusList,
    tipoItem_delete, TipoItem_edit, TipoItemCreate, TipoItemList, AcoesProntuarioList, AcoesProntuarioCreate, acoesprontuario_edit,acoesprontuario_delete )

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
]
