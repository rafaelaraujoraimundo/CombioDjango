from django import forms
from .models import UsuarioDesligamento

class UsuarioDesligamentoForm(forms.ModelForm):
    class Meta:
        model = UsuarioDesligamento
        fields = [
            'usuario', 'data_desligamento', 'data_limite',
            'bloqueio_email', 'usuario_email', 
            'bloqueio_fluig', 'usuario_fluig',
            'bloqueio_datasul', 'usuario_datasul', 'usuario_goglobal',
            'bloqueio_monday', 'usuario_monday',
            'bloqueio_qualiteam', 'usuario_qualiteam',
            'bloqueio_portal_chamados', 'usuario_portal_chamados',
            'bloqueio_usuario_impressora', 'usuario_impressora'
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
            'bloqueio_qualiteam': 'Bloqueio Qualiteam',
            'usuario_qualiteam': 'Usuário Qualiteam',
            'bloqueio_portal_chamados': 'Bloqueio Portal de Chamados',
            'usuario_portal_chamados': 'Usuário do Portal de Chamados',
            'bloqueio_usuario_impressora': 'Bloqueio Usuário da Impressora (Matriz)',
            'usuario_impressora': 'Usuário de Impressora (Matriz)'
        }