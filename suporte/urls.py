from django.urls import path
from .views import (CreateSubstitutoFluig, UsuarioDesligamentoCreate, UsuarioDesligamentoDelete,
  UsuarioDesligamentoList, UsuarioDesligamentoUpdate, SubstituicaoListView, SubstituicaoDetailView)
    
urlpatterns = [
     path('desligamento/novo/', UsuarioDesligamentoCreate.as_view(), name='usuario_desligamento_create'),
     path('desligamento/', UsuarioDesligamentoList.as_view(), name='usuario_desligamento_list'),
      path('desligamento/edit/<int:pk>/', UsuarioDesligamentoUpdate.as_view(), name='usuario_desligamento_edit'),
      path('desligamento/delete/<int:pk>/', UsuarioDesligamentoDelete.as_view(), name='usuario_desligamento_delete'),

       path('substitutofluig/new/', CreateSubstitutoFluig.as_view(), name='create_substituto_fluig'),
       path('substitutofluig/', SubstituicaoListView.as_view(), name='substituicao_list'),
        path('substituicoes/<int:pk>/', SubstituicaoDetailView.as_view(), name='substituicao_detail'),
    ]