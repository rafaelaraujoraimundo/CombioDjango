from django.shortcuts import render
from administration.models import (GroupProcessSelection, ServidorFluig, User)
from administration.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib import messages
from django.forms import CheckboxSelectMultiple
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from administration.tasks import update_processes
from .forms import ServidorFluigForm
from menu.models import ItensMenu
from django.urls import reverse_lazy
from .forms import ItensMenuForm, UserCreationForm, GroupProcessForm, ParametroForm
from .models import Parametro
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import GroupProcess
from django.views import View
from django.utils import timezone

from django.views.decorators.http import require_POST

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('administration_users')
    return redirect('administration_users')

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def change_password(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if new_password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('administration_users')
        
        user = get_object_or_404(User, id=user_id)
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Senha alterada com sucesso.')
        return redirect('administration_users')
    else:
        messages.error(request, 'Método não permitido.')
        return redirect('administration_users')

 # Redireciona para a página de login se não estiver logado
@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def user_list(request):
    # Permissões e Definições para o Menu
    activegroup = 'administration'
    title = 'Usuários'
    users = User.objects.all().order_by('id')
    context = {'users': users,
               'activegroup': activegroup,
               'title': title}
    return render(request, 'users/user_list.html', context)



@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def create_user(request):
    activegroup = 'administration'
    title = 'Criação de Usuários'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user, save_m2m = form.save(commit=False)  # Recebe a função save_m2m
            user.save()  # Salva o usuário
            save_m2m()  # Chama save_m2m para salvar as relações ManyToMany
            user.user_permissions.set(form.cleaned_data['custom_permissions'])  # Configura as permissões customizadas
            user.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('administration_users')
        else:
            messages.error(request, 'Erro ao criar o usuário. Verifique os dados.')
    else:
        form = CustomUserCreationForm()

    context = {'form': form, 'activegroup': activegroup, 'title': title}
    return render(request, 'administration/user/user_form.html', context)

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def user_edit(request, user_id):
    activegroup = 'administration'
    title = 'Edição de Usuário'
    context = {'activegroup': activegroup,
               'title' : title}
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.groups.clear()
            print('user_edit')
            print(form.cleaned_data.get('groups'))
            for group in form.cleaned_data.get('groups'):
                user.groups.add(group)
            user.user_permissions.clear()
            for perm in form.cleaned_data.get('user_permissions'):
                user.user_permissions.add(perm)
            update_session_auth_hash(request, user)
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('administration_users')
        else:
            return redirect('administration_users')
    else:
        form = CustomUserChangeForm(instance=user)
        form.fields['groups'].widget = CheckboxSelectMultiple()
        # form.fields['groups'].widget.attrs = {'custom-control-input'}
        form.fields['groups'].queryset = Group.objects.all()
        form.fields['user_permissions'].widget = CheckboxSelectMultiple()
        form.fields['user_permissions'].queryset = Permission.objects.filter(
            codename__icontains='combio_')
        context['form'] = form
        return render(request, 'users/user_edit.html', context=context)

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def servidorfluig_list(request):
    # Permissões e Definições para o Menu
    activegroup = 'administration'
    title = 'Servidores Fluig'


    servidoresfluig = ServidorFluig.objects.all()
    context = {'servidoresfluig': servidoresfluig,
               'activegroup': activegroup,
               'title' : title}
    return render(request, 'administration/servidorfluig/servidor_list.html', context)



@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def servidorfluig_edit(request, servidor_id):
    activegroup = 'administration'
    title = 'Edição de Servidores Fluig'
    context = {'activegroup': activegroup,
               'title' : title}
    servidorfluig = get_object_or_404(ServidorFluig, pk=servidor_id)
    if request.method == "POST":
        form = ServidorFluigForm(request.POST, instance=servidorfluig)
        if form.is_valid():
            form.save()
            return redirect('administration_servidorfluig_list')
        else:
            context['form'] = form
    else:
        form = ServidorFluigForm(instance=servidorfluig)
        context['form'] = form
    return render(request, 'administration/servidorfluig/servidor_edit.html', context)

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def servidorfluig_create(request):
    activegroup = 'administration'
    title = 'Criação de Servidor Fluig'
    context = {'activegroup': activegroup,
               'title' : title}
    if request.method == 'POST':
        form = ServidorFluigForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration_servidorfluig_list')
        else:
            context['form'] = form
    else:
        form = ServidorFluigForm()
        context['form'] = form
    return render(request, 'administration/servidorfluig/servidor_new.html', context)

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def servidorfluig_delete(request, servidor_id):
    activegroup = 'administration'
    title = 'Exclusão de Servidores Fluig'
    context = {'activegroup': activegroup,
               'title' : title}
    servidorfluig = get_object_or_404(ServidorFluig, pk=servidor_id)
    if request.method == "POST":
        servidorfluig.delete()
        messages.success(request, f'"{servidorfluig.servidor}" foi excluído com sucesso.')
        return redirect('administration_servidorfluig_list')
    else:
        form = ServidorFluigForm(instance=servidorfluig)
        context['form'] = form
    return render(request, 'administration/servidorfluig/servidor_delete.html', context)
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')   
class ItensMenuList(ListView):
    model = ItensMenu
    queryset = ItensMenu.objects.all()
    template_name = 'administration/itensmenu/itensmenu_list.html'


    def get_context_data(self, **kwargs):
        # Primeiro, pegue o contexto existente da classe base
        context = super(ItensMenuList, self).get_context_data(**kwargs)
        # Agora, adicione suas variáveis de contexto
        context['activegroup'] = 'administration'
        context['title'] = 'Itens de Menu Principal'
        # Retorne o contexto atualizado
        return context
    

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class ItensMenuCreate(CreateView):
    model = ItensMenu
    #fields = ['codigo', 'Item', 'grupo_id', 'icon_item', 'url', 'permission']
    form_class = ItensMenuForm
    template_name = 'administration/itensmenu/itensmenu_form.html'
    success_url = reverse_lazy('administration_itensmenu_list')

    def get_context_data(self, **kwargs):
        # Primeiro, pegue o contexto existente da classe base
        context = super(ItensMenuCreate, self).get_context_data(**kwargs)
        # Agora, adicione suas variáveis de contexto
        context['activegroup'] = 'administration'
        context['title'] = 'inclusão de Item de Menu'
        # Retorne o contexto atualizado
        return context
     
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Este é o lugar para adicionar qualquer lógica antes de salvar o formulário
            # Por exemplo, manipular os dados do formulário antes de salvar
            return self.form_valid(form)
        else:
            # Este é o lugar para adicionar qualquer lógica quando o formulário não é válido
            # Por exemplo, adicionar mensagens de erro personalizadas, logging, etc.
            return self.form_invalid(form)

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def ItensMenu_edit(request, itensMenu_id):
    activegroup = 'administration'
    title = 'Edição de Itens de Menu'
    context = {'activegroup': activegroup,
               'title' : title}
    itensMenu = get_object_or_404(ItensMenu, pk=itensMenu_id)
    if request.method == "POST":
        form = ItensMenuForm(request.POST, instance=itensMenu)
        if form.is_valid():
            form.save()
            return redirect('administration_itensmenu_list')
        else:
            context['form'] = form
    else:
        form = ItensMenuForm(instance=itensMenu)
        context['form'] = form
    return render(request, 'administration/itensmenu/itensmenu_edit.html', context)

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def itemMenu_delete(request, itensMenu_id):
   
    itensMenu = get_object_or_404(ItensMenu, pk=itensMenu_id)
    if request.method == "POST":
        itensMenu.delete()
        messages.success(request, f'"{itensMenu.item}" foi excluído com sucesso.')
        return redirect('administration_itensmenu_list')
   
    return redirect('administration_itensmenu_list')




User = get_user_model()

@login_required
@require_POST
def change_logged_in_user_password(request):
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    if new_password != confirm_password:
        return JsonResponse({'success': False, 'message': 'As senhas não coincidem.'}, status=400)

    user = request.user
    if not user.check_password(current_password):
        return JsonResponse({'success': False, 'message': 'Senha atual incorreta.'}, status=400)

    user.set_password(new_password)
    user.save()

    return JsonResponse({'success': True, 'message': 'Senha alterada com sucesso.'})

@login_required
@require_POST
def edit_logged_in_user_profile(request):
    usuario_datasul = request.POST.get('usuario_datasul')
    usuario_fluig = request.POST.get('usuario_fluig')
    user = request.user

    errors = {}

    # Validação básica dos campos (adicione validações adicionais conforme necessário)
    if not usuario_datasul:
        errors['usuario_datasul'] = ["Este campo é obrigatório."]
    if not usuario_fluig:
        errors['usuario_fluig'] = ["Este campo é obrigatório."]

    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    # Atualiza os dados do usuário logado
    user.usuario_datasul = usuario_datasul
    user.usuario_fluig = usuario_fluig
    user.save()

    return JsonResponse({'success': True, 'message': 'Perfil atualizado com sucesso.'})


@login_required(login_url='account_login') 
def get_logged_in_user_profile(request):
    user = request.user
    data = {
        'usuario_datasul': user.usuario_datasul,
        'usuario_fluig': user.usuario_fluig,
    }
    return JsonResponse(data)


@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def list_group_processes(request):
    #update_processes() # Atualiza os dados de processos antes de exibir a página
    groups = GroupProcess.objects.all()
    context = {
        'groups': groups,
        'activegroup': 'administration',
        'title': 'Lista de Grupos de Processos'
    }
    return render(request, 'administration/groupprocess/groupprocess_list.html', context)

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def delete_group_process(request, pk):
    group = get_object_or_404(GroupProcess, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('list_group_processes')
    context = {
        'group': group,
        'activegroup': 'administration',
        'title': 'Excluir Grupo de Processos'
    }
    return render(request, 'administration/groupprocess/delete_confirmation.html', context)

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def create_group_process(request):
    if request.method == 'POST':
        form = GroupProcessForm(request.POST)
        if form.is_valid():
            # Salva o grupo primeiro
            group = form.save(commit=False)
            group.save()
            
            # Salva as seleções de processos em GroupProcessSelection
            selected_processes = form.cleaned_data['selected_processes']
            for process in selected_processes:
                GroupProcessSelection.objects.create(group=group, process=process)
            
            return redirect('list_group_processes')
    else:
        form = GroupProcessForm()
    context = {
        'form': form,
        'activegroup': 'administration',
        'title': 'Adicionar Grupo de Processos',
        'button_label': 'Adicionar'
    }
    return render(request, 'administration/groupprocess/groupprocess_form.html', context)

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def edit_group_process(request, pk):
    group = get_object_or_404(GroupProcess, pk=pk)
    
    if request.method == 'POST':
        form = GroupProcessForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()

            # Limpa seleções de processos anteriores
            GroupProcessSelection.objects.filter(group=group).delete()

            # Salva as novas seleções de processos das checkboxes
            selected_processes = form.cleaned_data['selected_processes']
            for process in selected_processes:
                GroupProcessSelection.objects.create(group=group, process=process)

            # Salva as novas seleções de processos dos switches
            selected_processes_switch = form.cleaned_data['selected_processes_switch']
            for process in selected_processes_switch:
                GroupProcessSelection.objects.get_or_create(group=group, process=process)

            return redirect('list_group_processes')
    else:
        # Configura o formulário com processos já selecionados para checkboxes e switches
        form = GroupProcessForm(instance=group)
        selected_process_ids = group.process_selections.values_list('process_id', flat=True)
        form.fields['selected_processes'].initial = group.process_selections.values_list('process', flat=True)
        form.fields['selected_processes_switch'].initial = group.process_selections.values_list('process', flat=True)
    
    context = {
        'form': form,
        'activegroup': 'administration',
        'selected_process_ids': list(selected_process_ids),
        'title': 'Editar Grupo de Processos',
        'button_label': 'Salvar'
    }
    return render(request, 'administration/groupprocess/groupprocess_form.html', context)






@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class ParametroCreate(CreateView):
    model = Parametro
    form_class = ParametroForm
    template_name = 'administration/parametro/parametro_form.html'
    success_url = reverse_lazy('parametro_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'administration'
        context['title'] = 'Novo Parâmetro'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class ParametroList(ListView):
    model = Parametro
    template_name = 'administration/parametro/parametro_list.html'
    context_object_name = 'parametros'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'administration'
        context['title'] = 'Lista de Parâmetros'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class ParametroUpdate(UpdateView):
    model = Parametro
    form_class = ParametroForm
    template_name = 'administration/parametro/parametro_form.html'
    success_url = reverse_lazy('parametro_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'administration'
        context['title'] = 'Editar Parâmetro'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class ParametroDelete(DeleteView):
    model = Parametro
    template_name = 'administration/parametro/parametro_confirm_delete.html'
    success_url = reverse_lazy('parametro_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'administration'
        context['title'] = 'Confirmar Exclusão de Parâmetro'
        return context