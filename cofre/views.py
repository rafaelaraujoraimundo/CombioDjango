from django.shortcuts import render
from .models import PasswordManager, PasswordGroup, PasswordType, Vault
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PasswordManagerForm, PasswordTypeForm, PasswordGroupForm, VaultForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Prefetch
from django.db import models
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.db.models import Q, Prefetch

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class PasswordManagerList(ListView):
    model = PasswordManager
    template_name = 'cofre/passwordManager/passwordManager_list.html'
    context_object_name = 'passwords'

    def get_queryset(self):
        """
        Aplica filtros para exibir apenas os registros permitidos e realiza a pesquisa.
        """
        user = self.request.user

        # Termo de pesquisa
        search_query = self.request.GET.get('search', '').strip()

        # Filtro inicial com base na visualização
        queryset = PasswordManager.objects.filter(
            ativo=True
        ).filter(
            Q(visualizacao='TODOS') | Q(visualizacao='PERSONAL', usuario_criacao=user)
        )

        if search_query:
            # Adiciona o filtro de pesquisa
            queryset = queryset.filter(
                Q(site_name__icontains=search_query) |
                Q(username__icontains=search_query) |
                Q(url__icontains=search_query) |
                Q(observacoes__icontains=search_query) |
                Q(tipo__nome__icontains=search_query) |
                Q(grupo__nome__icontains=search_query) |
                Q(vault__nome_cofre__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Define os dados adicionais que serão passados ao template.
        """
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Password Manager'
        context['form'] = PasswordManagerForm()  # Formulário vazio para modal de edição
        context['tipos'] = PasswordType.objects.all()  # Todos os tipos
        context['grupos'] = PasswordGroup.objects.all()  # Todos os grupos
        context['vaults'] = Vault.objects.all()  # Todos os cofres
        context['password_groups'] = PasswordGroup.objects.prefetch_related(
            Prefetch(
                'passwords',
                queryset=self.get_queryset()
            )
        ).all()
        return context

    def post(self, request, *args, **kwargs):
        """
        Processa a edição de registros enviada via modal.
        """
        password_manager_id = request.POST.get('password_manager_id')
        if password_manager_id:
            password_manager = PasswordManager.objects.get(id=password_manager_id)
            form = PasswordManagerForm(request.POST, instance=password_manager)
            if form.is_valid():
                password_manager = form.save(commit=False)
                password_manager.usuario_alteracao = request.user
                password_manager.save()
        return self.get(request, *args, **kwargs)


@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_cofre', login_url='erro_page')
def password_manager_create(request):
    if request.method == 'POST':
        form = PasswordManagerForm(request.POST)
        if form.is_valid():
            password_manager = form.save(commit=False)  # Não salva ainda
            password_manager.usuario_criacao = request.user  # Atribui o usuário autenticado
            password_manager.save()  # Salva o registro com o usuário
            return redirect('administration_passwordmanager_list')
    else:
        form = PasswordManagerForm()
    return render(request, 'cofre/passwordManager/password_manager_form.html', {'form': form,
                                                                               'activegroup': 'cofre',
                                                                                'title': 'Incluir Senha Segura' })



@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_cofre', login_url='erro_page')
def get_decrypted_password(request, id):
    password_manager = PasswordManager.objects.get(pk=id)
    decrypted_password = password_manager.get_password()
    messages.success(request, 'Senha copiada com sucesso.')
    return JsonResponse({'decrypted_password': decrypted_password})


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class InactivatePasswordManager(View):
    def post(self, request, pk, *args, **kwargs):
        password_manager = get_object_or_404(PasswordManager, pk=pk)
        password_manager.ativo = False
        password_manager.usuario_alteracao = request.user
        password_manager.save()
        return redirect(reverse_lazy('administration_passwordmanager_list'))



@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class PasswordTypeCreate(CreateView):
    model = PasswordType
    form_class = PasswordTypeForm
    template_name = 'cofre/passwordtype/passwordtype_form.html'
    success_url = reverse_lazy('passwordtype_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Novo Tipo de Senha'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class PasswordTypeList(ListView):
    model = PasswordType
    template_name = 'cofre/passwordtype/passwordtype_list.html'
    context_object_name = 'password_types'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Lista de Tipos de Senha'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class PasswordTypeUpdate(UpdateView):
    model = PasswordType
    form_class = PasswordTypeForm
    template_name = 'cofre/passwordtype/passwordtype_form.html'
    success_url = reverse_lazy('passwordtype_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Editar Tipo de Senha'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class PasswordTypeDelete(DeleteView):
    model = PasswordType
    template_name = 'cofre/passwordtype/passwordtype_confirm_delete.html'
    success_url = reverse_lazy('passwordtype_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Confirmar Exclusão do Tipo de Senha'
        return context



@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class PasswordGroupCreate(CreateView):
    model = PasswordGroup
    form_class = PasswordGroupForm
    template_name = 'cofre/passwordgroup/passwordgroup_form.html'
    success_url = reverse_lazy('passwordgroup_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Novo Grupo de Senhas'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class PasswordGroupList(ListView):
    model = PasswordGroup
    template_name = 'cofre/passwordgroup/passwordgroup_list.html'
    context_object_name = 'password_groups'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Lista de Grupos de Senhas'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class PasswordGroupUpdate(UpdateView):
    model = PasswordGroup
    form_class = PasswordGroupForm
    template_name = 'cofre/passwordgroup/passwordgroup_form.html'
    success_url = reverse_lazy('passwordgroup_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Editar Grupo de Senhas'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class PasswordGroupDelete(DeleteView):
    model = PasswordGroup
    template_name = 'cofre/passwordgroup/passwordgroup_confirm_delete.html'
    success_url = reverse_lazy('passwordgroup_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Confirmar Exclusão do Grupo de Senhas'
        return context
    

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class VaultCreate(CreateView):
    model = Vault
    form_class = VaultForm
    template_name = 'cofre/vault/vault_form.html'
    success_url = reverse_lazy('vault_list')

    def form_valid(self, form):
        # Atribui o usuário autenticado ao campo `usuario_criacao`
        form.instance.usuario_criacao = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Novo Cofre'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class VaultList(ListView):
    model = Vault
    template_name = 'cofre/vault/vault_list.html'
    context_object_name = 'vaults'

    def get_queryset(self):
        # Filtra os objetos criados pelo usuário autenticado
        return Vault.objects.filter(usuario_criacao=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Lista de Cofres'
        return context


@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class VaultUpdate(UpdateView):
    model = Vault
    form_class = VaultForm
    template_name = 'cofre/vault/vault_form.html'
    success_url = reverse_lazy('vault_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.usuario_criacao != self.request.user:
            raise PermissionDenied("Você não tem permissão para editar este cofre.")
        return obj

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Editar Cofre'
        return context


@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class VaultDelete(DeleteView):
    model = Vault
    template_name = 'cofre/vault/vault_confirm_delete.html'
    success_url = reverse_lazy('vault_list')

    def get_object(self, queryset=None):
        # Garante que o objeto pertence ao usuário autenticado
        obj = super().get_object(queryset)
        if obj.usuario_criacao != self.request.user:
            raise PermissionDenied("Você não tem permissão para excluir este cofre.")
        return obj

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            messages.success(request, "Cofre deletado com sucesso.")
        except ValidationError as e:
            # Captura as mensagens da exceção ValidationError e as exibe ao usuário
            for message in e.messages:
                messages.error(request, message)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Confirmar Exclusão do Cofre'
        return context
    
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class InactivePasswordManagerList(View):
    def get(self, request, *args, **kwargs):
        # Lista todos os registros onde ativo=False
        inactive_passwords = PasswordManager.objects.filter(ativo=False)
        return render(request, 'cofre/passwordManager/inactive_password_list.html', {
            'inactive_passwords': inactive_passwords,
            'title': 'Senhas Inativas',
            'activegroup': 'cofre'
        })

    def post(self, request, *args, **kwargs):
        # Ativa a senha pelo ID fornecido
        password_manager_id = request.POST.get('password_manager_id')
        password_manager = get_object_or_404(PasswordManager, pk=password_manager_id)
        password_manager.ativo = True
        password_manager.usuario_alteracao = request.user
        password_manager.save()
        return redirect(reverse_lazy('inactive_password_manager_list'))
    


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('global_permissions.combio_cofre', login_url='erro_page'), name='dispatch')
class ActivatePasswordManager(View):
    def post(self, request, pk, *args, **kwargs):
        # Encontra o registro e ativa
        password_manager = get_object_or_404(PasswordManager, pk=pk)
        password_manager.ativo = True
        password_manager.usuario_alteracao = request.user
        password_manager.save()
        return redirect(reverse_lazy('inactive_password_manager_list'))