from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from administration.views import (itemMenu_delete, ItensMenu_edit, ItensMenuCreate, ItensMenuList,
    password_manager_create, PasswordManagerList, servidorfluig_create, servidorfluig_delete, password_manager_create,
    servidorfluig_edit, servidorfluig_list, user_edit, get_logged_in_user_profile, user_list,create_user,change_password,delete_user, change_logged_in_user_password, edit_logged_in_user_profile)

urlpatterns = [
    path('userList/', user_list, name="administration_users"),
    path('useredit/<int:user_id>/',user_edit , name='user_edit'),
    path('user/new', create_user, name='adminsitration_user_new'),
    path('change-password/', change_password, name='administration_change_password'),
    path('change-password-login/', change_logged_in_user_password, name='change_logged_in_user_password'),
    path('edit-profile/', edit_logged_in_user_profile, name='edit_logged_in_user_profile'),
    path('get-profile/', get_logged_in_user_profile, name='get_logged_in_user_profile'), 
    path('userdelete/<int:user_id>/', delete_user, name='user_delete'),

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
