from django.db import models
from administration.models import User
from django.utils import timezone

# Create your models here.
class UsuarioDesligamento(models.Model):
    usuario = models.CharField(max_length=100)  # Nome do usuário a ser desligado
    data_desligamento = models.DateField()
    data_limite = models.DateField()
    usuario_cadastro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="cadastro_usuario")
    data_cadastro = models.DateTimeField(default=timezone.now, editable=False)
    usuario_ultima_alteracao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="alteracao_usuario")
    data_ultima_alteracao = models.DateTimeField(auto_now=True)
    
    # Campos de bloqueio com o nome do usuário específico para cada sistema
    bloqueio_email = models.BooleanField(default=False)
    usuario_email = models.CharField(max_length=100, null=True, blank=True, help_text="Usuário de e-mail a ser bloqueado")

    bloqueio_fluig = models.BooleanField(default=False)
    usuario_fluig = models.CharField(max_length=100, null=True, blank=True, help_text="Usuário Fluig a ser bloqueado")

    bloqueio_datasul = models.BooleanField(default=False)
    usuario_datasul = models.CharField(max_length=100, null=True, blank=True, help_text="Usuário Datasul a ser bloqueado")
    usuario_goglobal = models.CharField(max_length=100, null=True, blank=True, help_text="Usuário Go-Global a ser bloqueado")

    bloqueio_monday = models.BooleanField(default=False)
    usuario_monday = models.CharField(max_length=100, null=True, blank=True, help_text="Usuário Monday a ser bloqueado")

    bloqueio_qualiteam = models.BooleanField(default=False)
    usuario_qualiteam = models.CharField(max_length=100, null=True, blank=True, help_text="Usuário Qualiteam a ser bloqueado")

    bloqueio_portal_chamados = models.BooleanField(default=False)
    usuario_portal_chamados = models.CharField(max_length=100, null=True, blank=True, help_text="Usuário do Portal de Chamados a ser bloqueado")

    bloqueio_usuario_impressora = models.BooleanField(default=False)
    usuario_impressora = models.CharField(max_length=100, null=True, blank=True, help_text="Usuário de Impressora (Matriz) a ser bloqueado")

    def __str__(self):
        return self.usuario