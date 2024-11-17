from django.db import models
from .encryptor import encrypt_password, decrypt_password
from administration.models import User


class PasswordType(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class PasswordGroup(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# Create your models here.
class PasswordManager(models.Model):
    site_name = models.CharField(max_length=100)
    url = models.URLField()
    username = models.CharField(max_length=100)
    encrypted_password = models.CharField(max_length=255)  # Armazenar a senha criptografada
    tipo = models.ForeignKey(PasswordType, on_delete=models.PROTECT, related_name='passwords')
    grupo = models.ForeignKey(PasswordGroup, on_delete=models.PROTECT, related_name='passwords')
    observacoes = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    usuario_alteracao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='password_alterations')
    data_alteracao = models.DateTimeField(auto_now=True)

    def set_password(self, password):
        self.encrypted_password = encrypt_password(password)

    def get_password(self):
        return decrypt_password(self.encrypted_password)

    def __str__(self):
        return self.site_name