from django import forms
from .models import PasswordManager, PasswordType, PasswordGroup, Vault


class PasswordManagerForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a senha',
        }),
        label='Senha',
        required=False  # Campo opcional
    )

    class Meta:
        model = PasswordManager
        fields = ['site_name', 'url', 'username', 'password', 'tipo', 'grupo', 'visualizacao', 'vault', 'observacoes', 'ativo']
        widgets = {
            'site_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do site ou programa',
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL do site',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário',
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
            }),
            'grupo': forms.Select(attrs={
                'class': 'form-control',
            }),
            'visualizacao': forms.Select(attrs={
                'class': 'form-control',
            }),
            'vault': forms.Select(attrs={
                'class': 'form-control',
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observações (opcional)',
                'rows': 3,
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'site_name': 'Nome do Site/Programa',
            'url': 'URL',
            'username': 'Usuário',
            'tipo': 'Tipo',
            'grupo': 'Grupo',
            'visualizacao': 'Visualização',
            'vault': 'Cofre',
            'observacoes': 'Observações',
            'ativo': 'Ativo',
        }

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
            if not self.cleaned_data['vault']:
                raise ValueError("O Vault deve ser selecionado para criptografar a senha.")
            # Chama diretamente a função encrypt_password com os dois argumentos
            from cofre.encryptor import encrypt_password
            password_manager.encrypted_password = encrypt_password(
                self.cleaned_data['password'],
                self.cleaned_data['vault']
            )
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


class VaultForm(forms.ModelForm):
    class Meta:
        model = Vault
        fields = ['nome_cofre', 'valor']
        widgets = {
            'nome_cofre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do cofre'
            }),
            'valor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o valor (ou deixe vazio para gerar automaticamente)'
            }),
        }
        labels = {
            'nome_cofre': 'Nome do Cofre',
            'valor': 'Valor',
        }

    def clean_valor(self):
        """
        Método para garantir que o valor seja transformado automaticamente se estiver vazio.
        """
        valor = self.cleaned_data.get('valor')
        if not valor:
            import base64
            import os
            valor = f"sjddu{base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')}"
        return valor