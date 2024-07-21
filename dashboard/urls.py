from django.urls import path
from django.contrib.auth.decorators import permission_required

from dashboard.views import dashboard_fluig


urlpatterns = [
    path('fluig', dashboard_fluig, name="dashboard_fluig"),
]
