from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from administration.views import user_list, user_edit, servidorfluig_list, servidorfluig_edit, servidorfluig_create, servidorfluig_delete

urlpatterns = [
    path('userList/', user_list, name="administration_users"),
    path('useredit/<int:user_id>/',user_edit , name='user_edit'),

    path('servidorlist/', servidorfluig_list, name="administration_servidorfluig_list"),
    path('servidorlist/<int:servidor_id>/',servidorfluig_edit , name='administration_servidorfluig_edit'),
    path('servidorDelete/<int:servidor_id>/',servidorfluig_delete , name='administration_servidorfluig_delete'),
    path('servidorfluig/new/', servidorfluig_create, name='administration_servidorfluig_create'),
]
