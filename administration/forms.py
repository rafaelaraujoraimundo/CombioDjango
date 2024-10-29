from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission
from django.forms.widgets import CheckboxSelectMultiple
from .models import User, ServidorFluig, PasswordManager
from menu.models import ItensMenu
from django import forms

class CustomUserCreationForm(UserCreationForm):
    usuario_datasul = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'teste'})
    )

    class Meta:
        model = User
        fields = ('email', 'usuario_datasul', 'usuario_fluig', )
        widget = {
            'usuario_datasul':
            forms.TextInput(attrs={'class': 'teste'})

        }


class CustomUserChangeForm(UserChangeForm):

    usuario_datasul = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-control-input'}),
        required=False,
        label="Groups"
    )
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(codename__icontains='combio'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-control-input'}),
        required=False,
        label="Permissions"
    )
    is_active = forms.BooleanField(
        required=False,  # Não é obrigatório
        label="Usuario Ativo?",  # Rótulo do campo
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})  # Estilo do checkbox
    )

    class Meta:
        model = User
        fields = ('email', 'usuario_datasul', 'usuario_fluig',
                  'groups', 'user_permissions', 'is_active')

        widgets = {
            'usuario_fluig': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }



class ServidorFluigForm(forms.ModelForm):
    class Meta:
        model = ServidorFluig
        fields = ['servidor', 'nome_servidor', 'client_key', 'consumer_secret', 'access_token', 'access_secret', 'url']



class ItensMenuForm(forms.ModelForm):

    permission = forms.ModelChoiceField(
        queryset=Permission.objects.filter(codename__icontains='combio'),
        required=False,
        label="Permission",
        empty_label="Select Permission"  # Opção para valor vazio, caso não seja obrigatório
    )
    class Meta:
        model = ItensMenu
        fields = ['codigo', 'item', 'grupo_id', 'icon_item', 'url', 'permission', 'order']




class PasswordManagerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    class Meta:
        model = PasswordManager
        fields = ['site_name', 'url', 'username', 'password', 'tipo', 'grupo']

    def save(self, commit=True):
        password_manager = super().save(commit=False)
        password_manager.set_password(self.cleaned_data['password'])
        if commit:
            password_manager.save()
        return password_manager
    


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(codename__istartswith='combio'),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    

    class Meta:
        model = User
        fields = ('email', 'usuario_datasul', 'usuario_fluig', 'groups', 'permissions', 'is_active')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()  # Save the many-to-many data for the form
        return user


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'widgets/custom_checkbox_select.html'
    option_template_name = 'widgets/custom_checkbox_option.html'