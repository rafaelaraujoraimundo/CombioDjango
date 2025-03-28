from django.core.exceptions import ValidationError
from django.db import models
from .encryptor import encrypt_password, decrypt_password
from administration.models import User
import base64
import os


class PasswordType(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class PasswordGroup(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome



class Vault(models.Model):
    nome_cofre = models.CharField(max_length=255, verbose_name="Nome do Cofre")
    usuario_criacao = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário de Criação")
    valor = models.CharField(max_length=44, verbose_name="Chave de Criptografia")  # 44 caracteres base64

    def has_passwords(self):
        """Verifica se o Vault está associado a senhas."""
        return self.passwords.exists()

    def save(self, *args, **kwargs):
        """
        Garante que o campo `valor` esteja formatado corretamente como chave base64.
        """
        if not self.valor or len(self.valor) != 44:
            # Gera uma chave base64 compatível com Fernet se o campo estiver vazio ou inválido
            self.valor = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
        elif len(self.valor) != 44 or not self.is_base64(self.valor):
            raise ValidationError("A chave de criptografia deve ter 44 caracteres e estar no formato base64.")

        # Impede alterações em um Vault associado a senhas
        if self.pk and self.has_passwords():
            raise ValidationError("Não é possível alterar o cofre porque ele está associado a senhas.")

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Impede a exclusão de um Vault associado a senhas.
        """
        if self.has_passwords():
            raise ValidationError("Não é possível deletar o cofre porque ele está associado a senhas.")
        super().delete(*args, **kwargs)

    @staticmethod
    def is_base64(value):
        """Valida se uma string está no formato base64."""
        try:
            base64.urlsafe_b64decode(value.encode('utf-8'))
            return True
        except Exception:
            return False

    def __str__(self):
        return self.nome_cofre

class PasswordManager(models.Model):
    VISUALIZACAO_CHOICES = [
        ('TODOS', 'Todos'),
        ('PERSONAL', 'Pessoal'),
    ]

    site_name = models.CharField(max_length=100)
    url = models.URLField()
    username = models.CharField(max_length=100)
    encrypted_password = models.CharField(max_length=255)
    tipo = models.ForeignKey(PasswordType, on_delete=models.PROTECT, related_name='passwords')
    grupo = models.ForeignKey(PasswordGroup, on_delete=models.PROTECT, related_name='passwords')
    observacoes = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    usuario_alteracao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='password_alterations')
    data_alteracao = models.DateTimeField(auto_now=True)
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_creations', verbose_name='Usuário Criação')
    visualizacao = models.CharField(max_length=10, choices=VISUALIZACAO_CHOICES, default='TODOS', verbose_name='Visualização')
    vault = models.ForeignKey(Vault, on_delete=models.PROTECT, related_name='passwords', verbose_name='Cofre')

    def set_password(self, password):
            """Criptografa a senha usando o cofre associado."""
            if not self.vault:
                raise ValueError("O Vault associado não está definido.")
            self.encrypted_password = encrypt_password(password, self.vault)
    
    def get_password(self):
        """Descriptografa a senha usando o cofre associado."""
        if not self.vault:
            raise ValueError("O Vault associado não está definido.")
        return decrypt_password(self.encrypted_password, self.vault)

    def __str__(self):
        return self.site_name