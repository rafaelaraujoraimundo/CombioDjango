from django import forms
from .models import Configuracao, SetorEmail

class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = Configuracao
        fields = ['arquivo_imagem', 'nome_arquivo', 'padrao_papel_parede', 'padrao_bloqueio_tela', 'observacao']
        widgets = {
            'usuario_inclusao': forms.HiddenInput(),
            'usuario_alteracao': forms.HiddenInput(),
        }


class SetorEmailForm(forms.ModelForm):
    class Meta:
        model = SetorEmail
        fields = ['nome']


class SignatureForm(forms.Form):
    nome_completo = forms.CharField(label='Nome Completo', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    telefone = forms.CharField(label='Telefone', max_length=20)
    setor_email = forms.ModelChoiceField(queryset=SetorEmail.objects.all(), label='Setor')