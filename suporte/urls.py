from django.urls import path
from .views import ( UsuarioDesligamentoCreate, 
UsuarioDesligamentoList, 
UsuarioDesligamentoUpdate,
UsuarioDesligamentoDelete)
    
urlpatterns = [
     path('desligamento/novo/', UsuarioDesligamentoCreate.as_view(), name='usuario_desligamento_create'),
     path('desligamento/', UsuarioDesligamentoList.as_view(), name='usuario_desligamento_list'),
      path('desligamento/edit/<int:pk>/', UsuarioDesligamentoUpdate.as_view(), name='usuario_desligamento_edit'),
      path('desligamento/delete/<int:pk>/', UsuarioDesligamentoDelete.as_view(), name='usuario_desligamento_delete'),
    ]