from django.db import models
from administration.models import GroupProcess, User
from django.utils import timezone
from administration.encryptor import encrypt_password, decrypt_password


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

    #bloqueio_qualiteam = models.BooleanField(default=False)
    #usuario_qualiteam = models.CharField(max_length=100, null=True, blank=True, help_text="Usuário Qualiteam a ser bloqueado")

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

    backup_keepit = models.BooleanField(default=False, help_text="Backup do Keepit realizado")
    data_backup_keepit = models.DateField(null=True, blank=True, help_text="Data em que o backup do Keepit foi feito")
    obsservao_datasul = models.TextField(null=True, blank=True, help_text="Observações sobre o Datasul")

    backup_desktop_C = models.BooleanField(default=False, help_text="Backup do Disco C realizado")
    backup_desktop_documentos = models.BooleanField(default=False, help_text="Backup da pasta Documentos realizado")
    backup_desktop_download = models.BooleanField(default=False, help_text="Backup da pasta Downloads realizado")

    devolucao_periferico = models.BooleanField(default=False, help_text="Periféricos devolvidos")
    observacao_periferico = models.TextField(null=True, blank=True, help_text="Observações sobre a devolução de periféricos")

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




class MS365Tenant(models.Model):
    """Modelo para armazenar configurações de tenant Microsoft 365"""
    
    nome_empresa = models.CharField(
        max_length=200, 
        verbose_name="Nome da Empresa",
        help_text="Nome identificador da empresa/tenant"
    )
    
    tenant_id = models.CharField(
        max_length=100, 
        verbose_name="Tenant ID",
        help_text="ID do tenant no Azure AD"
    )
    
    client_id = models.CharField(
        max_length=100, 
        verbose_name="Client ID", 
        help_text="Application (client) ID do app registration"
    )
    
    encrypted_client_secret = models.TextField(
        verbose_name="Client Secret",
        help_text="Client secret criptografado"
    )
    
    ativo = models.BooleanField(
        default=True, 
        verbose_name="Ativo",
        help_text="Se este tenant está ativo para uso"
    )
    
    data_criacao = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Data de Criação"
    )
    
    usuario_criacao = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="m365_tenants_criados",
        verbose_name="Usuário de Criação"
    )
    
    data_ultima_alteracao = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última Alteração"
    )
    
    usuario_ultima_alteracao = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="m365_tenants_alterados",
        verbose_name="Último Usuário que Alterou"
    )
    
    observacoes = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Observações",
        help_text="Observações sobre este tenant"
    )

    class Meta:
        verbose_name = "Tenant Microsoft 365"
        verbose_name_plural = "Tenants Microsoft 365"
        ordering = ['nome_empresa']

    def __str__(self):
        return f"{self.nome_empresa} ({self.tenant_id})"

    def set_client_secret(self, plain_secret):
        """Criptografa e salva o client secret"""
        self.encrypted_client_secret = encrypt_password(plain_secret)

    def get_client_secret(self):
        """Descriptografa e retorna o client secret"""
        if self.encrypted_client_secret:
            return decrypt_password(self.encrypted_client_secret)
        return None


class MS365UserSearchLog(models.Model):
    """Log de buscas de usuários realizadas"""
    
    tenant = models.ForeignKey(
        MS365Tenant, 
        on_delete=models.CASCADE,
        verbose_name="Tenant"
    )
    
    usuario_pesquisador = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Usuário que Pesquisou"
    )
    
    termo_busca = models.CharField(
        max_length=255, 
        verbose_name="Termo de Busca",
        help_text="Email ou ID do usuário pesquisado"
    )
    
    encontrado = models.BooleanField(
        default=False, 
        verbose_name="Usuário Encontrado"
    )
    
    dados_encontrados = models.JSONField(
        blank=True, 
        null=True, 
        verbose_name="Dados Encontrados",
        help_text="Dados do usuário encontrado (sem informações sensíveis)"
    )
    
    data_pesquisa = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Data da Pesquisa"
    )
    
    ip_origem = models.GenericIPAddressField(
        blank=True, 
        null=True, 
        verbose_name="IP de Origem"
    )

    class Meta:
        verbose_name = "Log de Busca M365"
        verbose_name_plural = "Logs de Busca M365"
        ordering = ['-data_pesquisa']

    def __str__(self):
        status = "Encontrado" if self.encontrado else "Não encontrado"
        return f"{self.termo_busca} - {status} ({self.data_pesquisa.strftime('%d/%m/%Y %H:%M')})"


class MS365UserUpdateLog(models.Model):
    """Log de atualizações de usuários realizadas"""
    
    tenant = models.ForeignKey(
        MS365Tenant, 
        on_delete=models.CASCADE,
        verbose_name="Tenant"
    )
    
    usuario_atualizador = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Usuário que Atualizou"
    )
    
    usuario_alvo = models.CharField(
        max_length=255, 
        verbose_name="Usuário Alvo",
        help_text="Email ou ID do usuário que foi atualizado"
    )
    
    campos_atualizados = models.JSONField(
        verbose_name="Campos Atualizados",
        help_text="Campos que foram alterados e seus novos valores"
    )
    
    sucesso = models.BooleanField(
        default=False, 
        verbose_name="Atualização Bem-sucedida"
    )
    
    erro_detalhes = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Detalhes do Erro",
        help_text="Detalhes do erro caso a atualização tenha falhado"
    )
    
    data_atualizacao = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Data da Atualização"
    )
    
    ip_origem = models.GenericIPAddressField(
        blank=True, 
        null=True, 
        verbose_name="IP de Origem"
    )

    class Meta:
        verbose_name = "Log de Atualização M365"
        verbose_name_plural = "Logs de Atualização M365" 
        ordering = ['-data_atualizacao']

    def __str__(self):
        status = "Sucesso" if self.sucesso else "Falha"
        return f"{self.usuario_alvo} - {status} ({self.data_atualizacao.strftime('%d/%m/%Y %H:%M')})"
    

class UsuarioM365(models.Model):
    email = models.EmailField(primary_key=True, verbose_name="E-mail do Usuário")
    display_name = models.CharField(max_length=255, blank=True, null=True)
    given_name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    office_location = models.CharField(max_length=255, blank=True, null=True)
    mobile_phone = models.CharField(max_length=64, blank=True, null=True)
    business_phones = models.TextField(blank=True, null=True)
    user_type = models.CharField(max_length=50, blank=True, null=True)
    account_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True)

    manager_name = models.CharField(max_length=255, blank=True, null=True)
    manager_email = models.EmailField(blank=True, null=True)
    manager_title = models.CharField(max_length=255, blank=True, null=True)

    tenant = models.ForeignKey(MS365Tenant, on_delete=models.PROTECT, related_name="tenant")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Usuário M365"
        verbose_name_plural = "Usuários M365"
        ordering = ['display_name']

    def __str__(self):
        return f"{self.display_name} ({self.email})"