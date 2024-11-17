from django.shortcuts import render
from .models import PasswordManager, PasswordGroup, PasswordType
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PasswordManagerForm, PasswordTypeForm, PasswordGroupForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Prefetch

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class PasswordManagerList(ListView):
    model = PasswordManager
    template_name = 'cofre/passwordManager/passwordManager_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Password Manager'
        context['form'] = PasswordManagerForm()  # Formulário vazio para modal de edição
        context['tipos'] = PasswordType.objects.all()  # Todos os tipos
        context['grupos'] = PasswordGroup.objects.all()  # Todos os grupos
        context['password_groups'] = PasswordGroup.objects.prefetch_related(
                Prefetch(
        'passwords',
        queryset=PasswordManager.objects.filter(ativo=True)
                        )
            ).all()
        return context

    def post(self, request, *args, **kwargs):
        if 'edit_password_id' in request.POST:
            password_manager = get_object_or_404(PasswordManager, id=request.POST.get('edit_password_id'))
            form = PasswordManagerForm(request.POST, instance=password_manager)

            if form.is_valid():
                password_manager = form.save(commit=False)
                password_manager.usuario_alteracao = request.user
                password_manager.data_alteracao = timezone.now()
                password_manager.save()
                return redirect(reverse_lazy('administration_passwordmanager_list'))

        return super().get(request, *args, **kwargs)


@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def password_manager_create(request):
    if request.method == 'POST':
        form = PasswordManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration_passwordmanager_list')
    else:
        form = PasswordManagerForm()
    return render(request, 'cofre/passwordManager/password_manager_form.html', {'form': form})



@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def get_decrypted_password(request, id):
    password_manager = PasswordManager.objects.get(pk=id)
    decrypted_password = password_manager.get_password()
    messages.success(request, 'Senha copiada com sucesso.')
    return JsonResponse({'decrypted_password': decrypted_password})


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class InactivatePasswordManager(View):
    def post(self, request, pk, *args, **kwargs):
        password_manager = get_object_or_404(PasswordManager, pk=pk)
        password_manager.ativo = False
        password_manager.usuario_alteracao = request.user
        password_manager.save()
        return redirect(reverse_lazy('administration_passwordmanager_list'))



@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
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
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
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
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
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
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
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
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
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
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
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
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
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
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class PasswordGroupDelete(DeleteView):
    model = PasswordGroup
    template_name = 'cofre/passwordgroup/passwordgroup_confirm_delete.html'
    success_url = reverse_lazy('passwordgroup_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'cofre'
        context['title'] = 'Confirmar Exclusão do Grupo de Senhas'
        return context