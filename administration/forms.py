from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission
from django.forms.widgets import CheckboxSelectMultiple
from .models import User, ServidorFluig, GroupProcess, Process, GroupProcessSelection, Parametro
from menu.models import ItensMenu
from requests_oauthlib import OAuth1Session
from django.apps import apps
from django.urls import get_resolver

def get_all_urls():
    url_patterns = []
    all_urls = get_resolver().url_patterns  # Recupera todas as rotas do URLConf raiz
    for url in all_urls:
        if hasattr(url, 'name') and url.name:  # Verifica se a URL tem um nome
            url_patterns.append(url.name)
    return url_patterns


class CustomUserCreationForm(UserCreationForm):


    custom_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(codename__startswith='combio'),  # Filtra permissões com um prefixo específico
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Custom Permissions"
    )
    #pagina_inicial = forms.ChoiceField(choices=[(url, url) for url in get_all_urls()])

    class Meta:
        model = User
        fields = ('email', 'usuario_datasul', 'usuario_fluig', 'groups', 'user_permissions', 'is_active','custom_permissions','enviar_email_desligados','nome_completo')
        widgets = {
            'usuario_datasul': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_fluig': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.CheckboxSelectMultiple(),
            'user_permissions': forms.CheckboxSelectMultiple(),
            'enviar_email_desligados': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.save_m2m()  # Garante que o save_m2m seja chamado para salvar relações ManyToMany
        else:
            return user, self.save_m2m  # Retornar a função save_m2m se não commitar imediatamente

        # Adicionando permissões customizadas
        user.user_permissions.set(self.cleaned_data['custom_permissions'])
        return user
class CustomUserChangeForm(UserChangeForm):

    usuario_datasul = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-control custom-switch custom-control-input'}),
        required=False,
        label="Groups"
    )
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(codename__icontains='combio'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-control custom-switch custom-control-input'}),
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
                  'groups', 'user_permissions', 'is_active', 'enviar_email_desligados','nome_completo')

        widgets = {
            'usuario_fluig': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'enviar_email_desligados': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
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




class GroupProcessForm(forms.ModelForm):
    selected_processes = forms.ModelMultipleChoiceField(
        queryset=Process.objects.filter(active=True),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    selected_processes_switch = forms.ModelMultipleChoiceField(
        queryset=Process.objects.filter(active=True),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = GroupProcess
        fields = ['name', 'selected_processes', 'selected_processes_switch']

    def __init__(self, *args, **kwargs):
        super(GroupProcessForm, self).__init__(*args, **kwargs)
        self.fields['selected_processes'].help_text = "Selecione os processos ativos."
        self.fields['selected_processes_switch'].help_text = "Selecione os processos ativos usando o switch."



class ParametroForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = ['codigo', 'modulo', 'tipo_dado', 'valor']
        labels = {
            'codigo': 'Código',
            'modulo': 'Módulo',
            'tipo_dado': 'Tipo de Dado',
            'valor': 'Valor',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carrega dinamicamente os nomes dos apps no campo 'modulo'
        self.fields['modulo'].widget = forms.Select()
        app_names = [(app.name, app.verbose_name) for app in apps.get_app_configs()]
        self.fields['modulo'].choices = app_names