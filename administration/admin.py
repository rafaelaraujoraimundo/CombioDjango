from django.contrib import admin
from administration.models import PasswordGroup, PasswordManager, PasswordType, ServidorFluig, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': (
                'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions'
            )
        }),
        ('Personal Info', {'fields': ('usuario_datasul', 'usuario_fluig')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )
    search_fields = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(ServidorFluig)
admin.site.register(PasswordGroup)
admin.site.register(PasswordType)