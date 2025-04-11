from django import forms

from multiupload.fields import MultiFileField

class UploadSPEDForm(forms.Form):
    arquivo_principal = forms.FileField(label="Arquivo Principal")
    arquivos_secundarios = MultiFileField(
        label="Arquivos Secundários",
        min_num=1,
        max_num=10,
        max_file_size=1024*1024*10  # 10 MB por arquivo
    )