from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from .encryptor import encrypt_password, decrypt_password
import hashlib

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
        )

        user.is_active = True
        user.is_staff = False
        user.is_superuser = False

        if password:
            user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="E-mail do usuário",
        max_length=254,
        unique=True,
    )
    nome_completo = models.CharField(
        verbose_name="Nome Completo",
        max_length=150,
        blank=True,
        null=True,
    )
    usuario_datasul = models.CharField(
        verbose_name="Usuário Datasul",
        max_length=50,
    )
    usuario_fluig = models.CharField(
        verbose_name="Usuário Fluig",
        max_length=100,
    )
    is_active = models.BooleanField(
        "Usuário ativo?",
        default=False
    )
    is_staff = models.BooleanField(
        "Usuário é da equipe de desenvolvimento?",
        default=False
    )
    is_superuser = models.BooleanField(
        "Usuário é um superusuário?",
        default=False
    )

    # Campo para controlar o envio de e-mail de desligamento
    enviar_email_desligados = models.BooleanField(
        "Enviar e-mail de desligamento?",
        default=False
    )

    hash_gravatar = models.CharField(max_length=32, blank=True, editable=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        db_table = "usuarios"
        app_label = 'administration'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.hash_gravatar or self._state.adding:
            self.hash_gravatar = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        super(User, self).save(*args, **kwargs)

class ServidorFluig(models.Model):
    servidor = models.CharField(max_length=255, null=False)  # Usando 255 como um valor comum para o comprimento máximo de uma string
    nome_servidor = models.CharField(max_length=255, null=False)
    client_key = models.CharField(max_length=255, null=False)
    consumer_secret = models.CharField(max_length=255, null=False)
    access_token = models.CharField(max_length=255, null=False)
    access_secret = models.CharField(max_length=255, null=False)
    url = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.nome_servidor

from django.db import models

class PasswordType(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class PasswordGroup(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class PasswordManager(models.Model):
    site_name = models.CharField(max_length=100)
    url = models.URLField()
    username = models.CharField(max_length=100)
    encrypted_password = models.CharField(max_length=255)  # Armazenar a senha criptografada
    tipo = models.ForeignKey(PasswordType, on_delete=models.PROTECT, related_name='passwords')
    grupo = models.ForeignKey(PasswordGroup, on_delete=models.PROTECT, related_name='passwords')

    def set_password(self, password):
        self.encrypted_password = encrypt_password(password)

    def get_password(self):
        return decrypt_password(self.encrypted_password)

    def __str__(self):
        return self.site_name