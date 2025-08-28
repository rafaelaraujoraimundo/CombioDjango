from django.urls import path
from .views import (MondayTokenCreateView, MondayTokenListView,
    MondayTokenUpdateView)
from . import views
app_name = "integracoes"

urlpatterns = [
    path("tokens/", MondayTokenListView.as_view(), name="tokens_list"),
    path("tokens/novo/", MondayTokenCreateView.as_view(), name="tokens_new"),
    path("tokens/<str:token>/editar/", MondayTokenUpdateView.as_view(), name="tokens_edit"),

    path("pinggy/", views.dashboard, name="pinggy_dashboard"),
    path("pinggy/token/novo/", views.token_novo, name="token_novo"),
    path("pinggy/redirect/novo/", views.redirect_novo, name="redirect_novo"),
    path("pinggy/<int:redirect_id>/start/", views.iniciar_tunel, name="iniciar_tunel"),
    path("pinggy/<int:redirect_id>/stop/", views.parar_tunel, name="parar_tunel"),

]

