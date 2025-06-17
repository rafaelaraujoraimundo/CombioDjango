from django.urls import path
from django.contrib.auth.decorators import permission_required

from dashboard.views import dashboard_fluig, dashboard_chamados_ti


urlpatterns = [
    path('fluig', dashboard_fluig, name="dashboard_fluig"),
    path('chamadosti', dashboard_chamados_ti, name='dashboard_chamados_ti'),
]
