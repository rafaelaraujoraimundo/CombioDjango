from django import forms
from .models import Arquivo


class UploadArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ['arquivo_original']
