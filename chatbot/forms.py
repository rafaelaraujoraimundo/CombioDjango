from django import forms
from .models import Contatos

class ContatosForm(forms.ModelForm):
    class Meta:
        model = Contatos
        fields = ['nome', 'unidade', 'telefone']
