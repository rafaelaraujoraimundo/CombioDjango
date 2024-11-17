from django.urls import path
from .views import (PasswordManagerList, password_manager_create, get_decrypted_password, InactivatePasswordManager,
                    PasswordTypeList, PasswordTypeCreate, PasswordTypeUpdate, PasswordTypeDelete, 
                    PasswordGroupList, PasswordGroupCreate, PasswordGroupUpdate, PasswordGroupDelete)
 
urlpatterns = [
        path('passwordmanager/', PasswordManagerList.as_view(), name='administration_passwordmanager_list'),
     path('passwordmanager/new', password_manager_create, name='administration_passwordmanager_new'),
    path('passwordmanager/get-password/<int:id>/', get_decrypted_password, name='get_decrypted_password'),
     path('passwordmanager/inactivate/<int:pk>/', InactivatePasswordManager.as_view(), name='administration_passwordmanager_inactivate'),

       path('passwordtype/', PasswordTypeList.as_view(), name='passwordtype_list'),
    path('passwordtype/create/', PasswordTypeCreate.as_view(), name='passwordtype_create'),
    path('passwordtype/edit/<int:pk>/', PasswordTypeUpdate.as_view(), name='passwordtype_edit'),
    path('passwordtype/delete/<int:pk>/', PasswordTypeDelete.as_view(), name='passwordtype_delete'),


     path('passwordgroup/', PasswordGroupList.as_view(), name='passwordgroup_list'),
    path('passwordgroup/create/', PasswordGroupCreate.as_view(), name='passwordgroup_create'),
    path('passwordgroup/edit/<int:pk>/', PasswordGroupUpdate.as_view(), name='passwordgroup_edit'),
    path('passwordgroup/delete/<int:pk>/', PasswordGroupDelete.as_view(), name='passwordgroup_delete'),

    
 ]