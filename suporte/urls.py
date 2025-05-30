from django.urls import path
from .views import (CreateSubstitutoFluig, UsuarioDesligamentoCreate, UsuarioDesligamentoDelete,
  UsuarioDesligamentoList, UsuarioDesligamentoUpdate, SubstituicaoListView, SubstituicaoDetailView, MS365TenantListView, MS365TenantCreateView, MS365TenantUpdateView, MS365TenantDeleteView,
    test_m365_connection, m365_dashboard, m365_search_user, m365_list_users, 
    m365_update_user, m365_manage_manager, MS365SearchLogListView, MS365UpdateLogListView,m365_export_users_csv,
    ajax_get_user_data)
    
urlpatterns = [
     path('desligamento/novo/', UsuarioDesligamentoCreate.as_view(), name='usuario_desligamento_create'),
     path('desligamento/', UsuarioDesligamentoList.as_view(), name='usuario_desligamento_list'),
      path('desligamento/edit/<int:pk>/', UsuarioDesligamentoUpdate.as_view(), name='usuario_desligamento_edit'),
      path('desligamento/delete/<int:pk>/', UsuarioDesligamentoDelete.as_view(), name='usuario_desligamento_delete'),

       path('substitutofluig/new/', CreateSubstitutoFluig.as_view(), name='create_substituto_fluig'),
       path('substitutofluig/', SubstituicaoListView.as_view(), name='substituicao_list'),
        path('substituicoes/<int:pk>/', SubstituicaoDetailView.as_view(), name='substituicao_detail'),
        path('m365/tenants/', MS365TenantListView.as_view(), name='m365_tenant_list'),
    path('m365/tenants/new/', MS365TenantCreateView.as_view(), name='m365_tenant_create'),
    path('m365/tenants/<int:pk>/edit/', MS365TenantUpdateView.as_view(), name='m365_tenant_edit'),
    path('m365/tenants/<int:pk>/delete/', MS365TenantDeleteView.as_view(), name='m365_tenant_delete'),
    path('m365/tenants/<int:pk>/test/', test_m365_connection, name='m365_tenant_test'),
    
    # M365 User Operations
    path('m365/', m365_dashboard, name='m365_dashboard'),
    path('m365/search/', m365_search_user, name='m365_search_user'),
    path('m365/list/', m365_list_users, name='m365_list_users'),
    path('m365/update/', m365_update_user, name='m365_update_user'),
    path('m365/manager/', m365_manage_manager, name='m365_manage_manager'),
    
    # M365 Logs
    path('m365/logs/search/', MS365SearchLogListView.as_view(), name='m365_search_logs'),
    path('m365/logs/update/', MS365UpdateLogListView.as_view(), name='m365_update_logs'),
    
    # AJAX Endpoints
    path('m365/ajax/get-user-data/', ajax_get_user_data, name='m365_ajax_get_user_data'),

    #Export todos os usuarios em CSV
    path('m365/export/csv/', m365_export_users_csv, name='m365_export_users_csv'),
    ]