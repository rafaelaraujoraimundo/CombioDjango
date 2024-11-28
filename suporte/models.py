from django.db import models
from administration.models import GroupProcess, User
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

    envio_email_gestor = models.BooleanField(default=False, help_text="Indica se um email será enviado ao gestor")
    gestor = models.CharField(max_length=100, null=True, blank=True, help_text="Nome do gestor responsável")

    backup_email = models.BooleanField(default=False, help_text="Backup do e-mail realizado")
    observacao_email = models.TextField(null=True, blank=True, help_text="Observações sobre o backup do e-mail")

    backup_onedrive = models.BooleanField(default=False, help_text="Backup do OneDrive realizado")
    observacao_onedrive = models.TextField(null=True, blank=True, help_text="Observações sobre o backup do OneDrive")

    backup_desktop = models.BooleanField(default=False, help_text="Backup da Área de Trabalho/Documentos realizado")
    observacao_desktop = models.TextField(null=True, blank=True, help_text="Observações sobre o backup da Área de Trabalho/Documentos")

    devolucao_computador = models.BooleanField(default=False, help_text="Computador devolvido")
    observacao_computador = models.TextField(null=True, blank=True, help_text="Observações sobre a devolução do computador")

    devolucao_celular = models.BooleanField(default=False, help_text="Celular devolvido")
    observacao_celular = models.TextField(null=True, blank=True, help_text="Observações sobre a devolução do celular")    

    def __str__(self):
        return self.usuario


class UsuarioFluig(models.Model):
    login = models.CharField(max_length=100, unique=True, verbose_name="Login")
    email = models.EmailField(verbose_name="Email")
    code = models.CharField(max_length=100, verbose_name="Code")
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return f"{self.full_name} ({self.login})"
    


class Substituicao(models.Model):
    usuario_a_substituir = models.ForeignKey(
        UsuarioFluig,
        related_name="substituicoes_como_substituido",
        on_delete=models.CASCADE,
        verbose_name="Usuário a ser Substituído"
    )
    usuario_substituto = models.ForeignKey(
        UsuarioFluig,
        related_name="substituicoes_como_substituto",
        on_delete=models.CASCADE,
        verbose_name="Usuário Substituto"
    )
    data_inicial = models.DateField(verbose_name="Data Inicial")
    data_final = models.DateField(verbose_name="Data Final")
    grupos_switch = models.ManyToManyField(
        GroupProcess,
        verbose_name="Grupos para Substituição"
    )
    code = models.CharField(max_length=100, blank=True, null=True)
    usuario_inclusao = models.ForeignKey(  # Novo campo
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuário de Inclusão"
    )

    def __str__(self):
        return f"Substituição de {self.usuario_a_substituir} por {self.usuario_substituto} de {self.data_inicial} a {self.data_final}"