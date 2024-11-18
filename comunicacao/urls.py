from django.urls import path
from .views import (ConfiguracaoListView, ConfiguracaoCreateView, ConfiguracaoUpdateView, ConfiguracaoDeleteView)

urlpatterns = [
    path('papeldeparede/', ConfiguracaoListView.as_view(), name='configuracao_list'),
    path('papeldeparede/new/', ConfiguracaoCreateView.as_view(), name='configuracao_create'),
    path('papeldeparede/<int:pk>/edit/', ConfiguracaoUpdateView.as_view(), name='configuracao_edit'),
    path('papeldeparede/<int:pk>/delete/', ConfiguracaoDeleteView.as_view(), name='configuracao_delete'),
]