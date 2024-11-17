from django import forms
from .models import PasswordManager, PasswordType, PasswordGroup


class PasswordManagerForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Senha',
        required=False  # O campo é opcional
    )

    class Meta:
        model = PasswordManager
        fields = ['site_name', 'url', 'username', 'password', 'tipo', 'grupo', 'observacoes', 'ativo']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')  # Instância para edição
        super().__init__(*args, **kwargs)
        if instance:
            # Preenche o campo password com a senha descriptografada
            self.fields['password'].initial = instance.get_password()

    def save(self, commit=True):
        password_manager = super().save(commit=False)
        # Atualiza a senha apenas se o campo estiver preenchido
        if self.cleaned_data['password']:
            password_manager.set_password(self.cleaned_data['password'])
        if commit:
            password_manager.save()
        return password_manager

class PasswordTypeForm(forms.ModelForm):
    class Meta:
        model = PasswordType
        fields = ['nome']
        labels = {
            'nome': 'Nome',
        }


class PasswordGroupForm(forms.ModelForm):
    class Meta:
        model = PasswordGroup
        fields = ['nome']
        labels = {
            'nome': 'Nome do Grupo',
        }