from django import forms
from .models import Configuracao

class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = Configuracao
        fields = ['arquivo_imagem', 'nome_arquivo', 'padrao_papel_parede', 'padrao_bloqueio_tela', 'observacao']
        widgets = {
            'usuario_inclusao': forms.HiddenInput(),
            'usuario_alteracao': forms.HiddenInput(),
        }