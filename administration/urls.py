from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from administration.views import (itemMenu_delete, ItensMenu_edit, ItensMenuCreate, ItensMenuList,
    password_manager_create, PasswordManagerList, servidorfluig_create, servidorfluig_delete, password_manager_create,
    servidorfluig_edit, servidorfluig_list, user_edit, user_list)

urlpatterns = [
    path('userList/', user_list, name="administration_users"),
    path('useredit/<int:user_id>/',user_edit , name='user_edit'),

    path('servidorfluig/', servidorfluig_list, name="administration_servidorfluig_list"),
    path('servidorfluig/<int:servidor_id>/',servidorfluig_edit , name='administration_servidorfluig_edit'),
    path('servidorDelete/<int:servidor_id>/',servidorfluig_delete , name='administration_servidorfluig_delete'),
    path('servidorfluig/new/', servidorfluig_create, name='administration_servidorfluig_create'),

    path('itensmenu/', ItensMenuList.as_view(), name='administration_itensmenu_list'),
    path('itensmenu/new/', ItensMenuCreate.as_view(), name='administration_itensmenu_new'),
    path('itensmenu/<int:itensMenu_id>/',ItensMenu_edit , name='administration_itensmenu_edit'),
    path('itensmenuDelete/<int:itensMenu_id>/',itemMenu_delete , name='administration_itensmenu_delete'),

     path('passwordmanager/', PasswordManagerList.as_view(), name='administration_passwordmanager_list'),
     path('passwordmanager/new', password_manager_create, name='administration_passwordmanager_new'),
]
