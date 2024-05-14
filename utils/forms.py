from django import forms
from .models import Arquivo, ArquivoAtivo, AtivoValores


class UploadArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ['arquivo_original']

class UploadArquivoAtivoForm(forms.ModelForm):
    class Meta:
        model = ArquivoAtivo
        fields = ['arquivo_original']

class UploadAtivoPatrimonialForm(forms.ModelForm):
    class Meta:
        model = AtivoValores
        fields = ['arquivo_original']