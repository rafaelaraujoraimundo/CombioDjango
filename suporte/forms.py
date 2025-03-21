from django import forms
from administration.models import GroupProcess
from .models import UsuarioDesligamento, UsuarioFluig

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
            'bloqueio_qualiteam', 'usuario_qualiteam',
            'bloqueio_portal_chamados', 'usuario_portal_chamados',
            'bloqueio_usuario_impressora', 'usuario_impressora',
            'backup_email', 'observacao_email',
            'backup_onedrive', 'observacao_onedrive',
            'backup_desktop', 'observacao_desktop',
            'devolucao_computador', 'observacao_computador',
            'devolucao_celular', 'observacao_celular',
        ]
        labels = {
            'usuario': 'Usuário a ser desligado',
            'data_desligamento': 'Data de Desligamento',
             'envio_email_gestor': 'Envio de E-mail ao Gestor/Substituto',  # Novo rótulo
            'gestor': 'Gestor Responsável/Substituto',
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
            'bloqueio_qualiteam': 'Bloqueio Qualiteam',
            'usuario_qualiteam': 'Usuário Qualiteam',
            'bloqueio_portal_chamados': 'Bloqueio Portal de Chamados',
            'usuario_portal_chamados': 'Usuário do Portal de Chamados',
            'bloqueio_usuario_impressora': 'Bloqueio Usuário da Impressora (Matriz)',
            'usuario_impressora': 'Usuário de Impressora (Matriz)',
            'backup_email': 'Backup do E-mail',
            'observacao_email': 'Observação sobre o Backup do E-mail',
            'backup_onedrive': 'Backup do OneDrive',
            'observacao_onedrive': 'Observação sobre o Backup do OneDrive',
            'backup_desktop': 'Backup da Área de Trabalho/Documentos',
            'observacao_desktop': 'Observação sobre o Backup da Área de Trabalho/Documentos',
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