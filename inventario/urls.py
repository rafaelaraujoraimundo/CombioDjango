from django.urls import path
from .views import (acoesprontuario_delete, acoesprontuario_edit, AcoesProntuarioCreate,
    AcoesProntuarioList, celular_delete, CelularCreate, CelularList, CelularUpdate,
    computador_delete, ComputadorCreate, ComputadorDetailView, ComputadorList, ComputadorUpdate,
    controlefones_delete, ControleFonesCreate, ControleFonesList, ControleFonesUpdate,
    controlekit_delete, ControlekitCreate, ControlekitList, ControlekitUpdate,
    estabelecimento_chart, estoque_delete, estoque_edit, EstoqueCreate, EstoqueList,
    monitor_delete, MonitorCreate, MonitorList, MonitorUpdate, ProntuarioCelularCreate,
    ProntuarioCelularDelete, ProntuarioCelularListView, ProntuarioCelularUpdate,
    ProntuarioComputadorCreate, ProntuarioComputadorDelete, ProntuarioComputadorListView,
    ProntuarioComputadorUpdate, ProntuarioMonitorCreate, ProntuarioMonitorDelete,
    ProntuarioMonitorListView, ProntuarioMonitorUpdate, status_delete, status_edit, StatusCreate,
    StatusList, tipoItem_delete, TipoItem_edit, TipoItemCreate, TipoItemList, export_computadores_excel, export_estoque_excel,
    export_controlekit_excel, export_controlefones_excel,
    export_monitor_excel,export_celular_excel,LinhaListView, LinhaCreateView, LinhaUpdateView, linha_delete, export_linha_excel,
    ProntuarioLinhaListView, ProntuarioLinhaCreateView, ProntuarioLinhaUpdateView, prontuario_linha_delete, EstoqueMovimentacaoList, 
    relatorio_movimentacoes, estoque_movimentacao_create, export_movimentacoes_excel, estoque_movimentacao_delete,
    disparar_populate_hardware)

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
    path('prontuario/computador/delete/<int:pk>/', ProntuarioComputadorDelete.as_view(), name='prontuario_computador_delete'),

    path('computador/details/<int:pk>/', ComputadorDetailView.as_view(), name='computador-detail'),
    path('dashboard/', estabelecimento_chart, name='estabelecimento_chart'),
    path('computador/export', export_computadores_excel, name='export_computadores_excel'),
      path('estoque/export', export_estoque_excel, name='export_estoque_excel'),
    path('controlekit/export', export_controlekit_excel, name='export_controlekit_excel'),
    path('controlefones/export', export_controlefones_excel, name='export_controlefones_excel'),
    path('monitor/export', export_monitor_excel, name='export_monitor_excel'),
    path('celular/export', export_celular_excel, name='export_celular_excel'),

        # URLs para Linhas
    path('linha/', LinhaListView.as_view(), name='linha_list'),
    path('linha/new/', LinhaCreateView.as_view(), name='linha_create'),
    path('linha/edit/<int:pk>/', LinhaUpdateView.as_view(), name='linha_edit'),
    path('linha/delete/<int:pk>/', linha_delete, name='linha_delete'),
    path('linha/export/', export_linha_excel, name='export_linha_excel'),

    # URLs para Prontuário da Linha
    path('linha/<int:linha_id>/prontuario/', ProntuarioLinhaListView.as_view(), name='prontuario_linha_list'),
    path('linha/<int:linha_id>/prontuario/novo/', ProntuarioLinhaCreateView.as_view(), name='prontuario_linha_create'),
    path('prontuario/linha/<int:pk>/editar/', ProntuarioLinhaUpdateView.as_view(), name='prontuario_linha_edit'),
    path('prontuario/linha/<int:pk>/excluir/', prontuario_linha_delete, name='prontuario_linha_delete'),
    
    #URLS para movimentação de Estoque
    path('estoque/movimentacao_list/<int:estoque_id>/', EstoqueMovimentacaoList.as_view(), name='estoque_movimentacao_list'),
    path('estoque/movimentacao/create/<int:estoque_id>/', estoque_movimentacao_create, name='estoque_movimentacao_create'),
    path('estoque/movimentacao/relatorio/', relatorio_movimentacoes, name='relatorio_movimentacoes'),
    path('estoque/movimentacao/export_excel/', export_movimentacoes_excel, name='export_movimentacoes_excel'),
    path('estoque/movimentacao/delete/<int:movimentacao_id>/', estoque_movimentacao_delete, name='estoque_movimentacao_delete'),

    path('computador/disparar-importacao/', disparar_populate_hardware, name='disparar_populate_hardware'),
    
]
