from django.urls import path
from .views import (MondayTokenCreateView, MondayTokenListView,
    MondayTokenUpdateView)
app_name = "integracoes"

urlpatterns = [
    path("tokens/", MondayTokenListView.as_view(), name="tokens_list"),
    path("tokens/novo/", MondayTokenCreateView.as_view(), name="tokens_new"),
    path("tokens/<str:token>/editar/", MondayTokenUpdateView.as_view(), name="tokens_edit"),

]
