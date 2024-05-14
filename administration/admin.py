from django.contrib import admin
from administration.models import PasswordGroup, PasswordManager, PasswordType, ServidorFluig, User
# Register your models here.
admin.site.register(User)
admin.site.register(ServidorFluig)
admin.site.register(PasswordGroup)
admin.site.register(PasswordType)