from django import forms
from administration.models import GroupProcess
from .models import UsuarioDesligamento, UsuarioFluig, MS365Tenant


class UsuarioDesligamentoForm(forms.ModelForm):
    class Meta:
        model = UsuarioDesligamento
        fields = [
            'usuario', 'data_desligamento', 'data_limite',
            'bloqueio_email', 'usuario_email',
            'envio_email_gestor', 'gestor',
            'bloqueio_fluig', 'usuario_fluig',
            'bloqueio_datasul', 'usuario_datasul', 'usuario_goglobal',
            'bloqueio_monday', 'usuario_monday',
            # removido bloqueio_qualiteam e usuario_qualiteam
            'bloqueio_portal_chamados', 'usuario_portal_chamados',
            'bloqueio_usuario_impressora', 'usuario_impressora',
            'backup_email', 'observacao_email',
            'backup_onedrive', 'observacao_onedrive',
            'backup_desktop', 'observacao_desktop',

            # 🔹 novos campos
            'backup_keepit', 'data_backup_keepit', 'obsservao_datasul',
            'backup_desktop_C', 'backup_desktop_documentos', 'backup_desktop_download',
            'devolucao_periferico', 'observacao_periferico',

            'devolucao_computador', 'observacao_computador',
            'devolucao_celular', 'observacao_celular',
        ]
        labels = {
            'usuario': 'Usuário a ser desligado',
            'data_desligamento': 'Data de Desligamento',
            'data_limite': 'Data Limite',
            'bloqueio_email': 'Bloqueio Email',
            'usuario_email': 'Usuário de E-mail',
            'bloqueio_fluig': 'Bloqueio Fluig',
            'usuario_fluig': 'Usuário Fluig',
            'bloqueio_datasul': 'Bloqueio Datasul',
            'usuario_datasul': 'Usuário Datasul',
            'usuario_goglobal': 'Usuário Go-Global',
            'bloqueio_monday': 'Bloqueio Monday',
            'usuario_monday': 'Usuário Monday',
            'bloqueio_portal_chamados': 'Bloqueio Portal de Chamados',
            'usuario_portal_chamados': 'Usuário do Portal de Chamados',
            'bloqueio_usuario_impressora': 'Bloqueio Usuário da Impressora',
            'usuario_impressora': 'Usuário de Impressora',
            'backup_email': 'Backup do E-mail',
            'observacao_email': 'Observação sobre o Backup do E-mail',
            'backup_onedrive': 'Backup do OneDrive',
            'observacao_onedrive': 'Observação sobre o Backup do OneDrive',
            'backup_desktop': 'Backup da Área de Trabalho',
            'observacao_desktop': 'Observação sobre o Backup da Área de Trabalho',

            # 🔹 novos labels
            'backup_keepit': 'Backup Keepit',
            'data_backup_keepit': 'Data do Backup Keepit',
            'obsservao_datasul': 'Observação do Datasul',
            'backup_desktop_C': 'Backup do Disco C',
            'backup_desktop_documentos': 'Backup da pasta Documentos',
            'backup_desktop_download': 'Backup da pasta Downloads',
            'devolucao_periferico': 'Devolução de Periféricos',
            'observacao_periferico': 'Observação sobre Periféricos',

            'devolucao_computador': 'Devolução do Computador',
            'observacao_computador': 'Observação sobre a Devolução do Computador',
            'devolucao_celular': 'Devolução do Celular',
            'observacao_celular': 'Observação sobre a Devolução do Celular',
        }

class SubstituicaoForm(forms.Form):
    usuario_a_substituir = forms.ModelChoiceField(
        queryset=UsuarioFluig.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Usuário a ser Substituído"
    )
    usuario_substituto = forms.ModelChoiceField(
        queryset=UsuarioFluig.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Usuário Substituto"
    )
    data_inicial = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Data Inicial"
    )
    data_final = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Data Final"
    )
    grupos_switch = forms.ModelMultipleChoiceField(
        queryset=GroupProcess.objects.all(),  # Filtragem adicional pode ser feita aqui se necessário
        widget=forms.CheckboxSelectMultiple(),
        label="Grupos para Substituição"
    )
    code = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )



class MS365TenantForm(forms.ModelForm):
    """Formulário para configuração de Tenant Microsoft 365"""
    
    client_secret = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o Client Secret'
        }),
        label="Client Secret",
        help_text="Client secret do app registration no Azure AD",
        required=True
    )
    
    confirm_client_secret = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme o Client Secret'
        }),
        label="Confirmar Client Secret",
        help_text="Digite novamente o client secret para confirmação",
        required=True
    )

    class Meta:
        model = MS365Tenant
        fields = [
            'nome_empresa', 
            'tenant_id', 
            'client_id', 
            'ativo', 
            'observacoes'
        ]
        
        widgets = {
            'nome_empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Combio Energia Ltda'
            }),
            'tenant_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            }),
            'client_id': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'custom-control-input'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre este tenant...'
            })
        }

    def __init__(self, *args, **kwargs):
        # Para edição, não exigir confirmação de senha
        self.is_edit_mode = kwargs.pop('is_edit_mode', False)
        super().__init__(*args, **kwargs)
        
        if self.is_edit_mode:
            # Em modo de edição, tornar os campos de senha opcionais
            self.fields['client_secret'].required = False
            self.fields['confirm_client_secret'].required = False
            self.fields['client_secret'].help_text = "Deixe em branco para manter o secret atual"
            self.fields['confirm_client_secret'].help_text = "Deixe em branco para manter o secret atual"

    def clean(self):
        cleaned_data = super().clean()
        client_secret = cleaned_data.get('client_secret')
        confirm_client_secret = cleaned_data.get('confirm_client_secret')
        
        # Validar senhas apenas se foram preenchidas
        if client_secret or confirm_client_secret:
            if client_secret != confirm_client_secret:
                raise forms.ValidationError("Os Client Secrets não coincidem!")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Salvar client secret criptografado se foi fornecido
        client_secret = self.cleaned_data.get('client_secret')
        if client_secret:
            instance.set_client_secret(client_secret)
        
        if commit:
            instance.save()
        
        return instance


class MS365UserSearchForm(forms.Form):
    """Formulário para busca de usuários no M365"""
    
    tenant = forms.ModelChoiceField(
        queryset=MS365Tenant.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tenant",
        help_text="Selecione o tenant para buscar"
    )
    
    termo_busca = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o email ou ID do usuário'
        }),
        label="Usuário",
        help_text="Email ou ID do usuário para buscar",
        max_length=255
    )


class MS365UserUpdateForm(forms.Form):
    """Formulário para atualização de usuários no M365"""

    tenant = forms.ModelChoiceField(
        queryset=MS365Tenant.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tenant",
        help_text="Selecione o tenant"
    )

    usuario_alvo = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o email ou ID do usuário'
        }),
        label="Usuário Alvo",
        help_text="Email ou ID do usuário para atualizar",
        max_length=255
    )

    # Campos atualizáveis via Graph API
    given_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome'
        }),
        label="Nome",
        required=False
    )

    surname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sobrenome'
        }),
        label="Sobrenome",
        required=False
    )

    display_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de Exibição'
        }),
        label="Nome de Exibição",
        required=False
    )

    job_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cargo'
        }),
        label="Cargo",
        required=False
    )

    department = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Departamento'
        }),
        label="Departamento",
        required=False
    )

    office_location = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Localização'
        }),
        label="Localização",
        required=False
    )

    business_phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefone comercial'
        }),
        label="Telefone",
        required=False
    )

    mobile_phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Celular'
        }),
        label="Celular",
        required=False
    )

    manager_email = forms.CharField(
    required=False,
    label="E-mail do Gerente",
    widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'ex: gerente@empresa.com'
    })
)

    def clean(self):
        cleaned_data = super().clean()

        update_fields = [
            'given_name', 'surname', 'display_name',
            'job_title', 'department', 'office_location',
            'business_phone', 'mobile_phone'
        ]

        has_data = any(cleaned_data.get(field) for field in update_fields)

        if not has_data:
            raise forms.ValidationError("Preencha pelo menos um campo para atualizar!")

        return cleaned_data
class MS365ManagerForm(forms.Form):
    """Formulário para gerenciamento de managers no M365"""
    
    tenant = forms.ModelChoiceField(
        queryset=MS365Tenant.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tenant",
        help_text="Selecione o tenant"
    )
    
    usuario = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o email ou ID do usuário'
        }),
        label="Usuário",
        help_text="Email ou ID do usuário",
        max_length=255
    )
    
    novo_manager = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o email ou ID do manager (opcional para remoção)'
        }),
        label="Novo Manager",
        help_text="Email ou ID do novo manager (deixe em branco para remover)",
        max_length=255,
        required=False
    )


class MS365ListUsersForm(forms.Form):
    """Formulário para listagem de usuários no M365"""
    
    tenant = forms.ModelChoiceField(
        queryset=MS365Tenant.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tenant",
        help_text="Selecione o tenant para listar usuários"
    )
    
    filtro = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Digite o nome do usuario (deixe em branco para buscar todos)"
        }),
        label="Filtro OData (opcional)",
        help_text="Filtro OData para refinar a busca",
        max_length=500,
        required=False
    )