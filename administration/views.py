from django.shortcuts import render
from administration.models import PasswordManager, ServidorFluig, User
from administration.forms import CustomUserChangeForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.forms import CheckboxSelectMultiple
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import ServidorFluigForm
from menu.models import ItensMenu
from django.urls import reverse_lazy
from .forms import ItensMenuForm, PasswordManagerForm, UserCreationForm
from .models import PasswordManager, PasswordGroup
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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


@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class PasswordManagerList(ListView):
    model = PasswordManager
    template_name = 'administration/passwordManager/passwordManager_list.html'


    def get_context_data(self, **kwargs):
        # Primeiro, pegue o contexto existente da classe base
        context = super(PasswordManagerList, self).get_context_data(**kwargs)
        # Agora, adicione suas variáveis de contexto
        context['PasswordGroups'] = PasswordGroup.objects.all()
        context['activegroup'] = 'administration'
        context['title'] = 'Password Manager'
        # Retorne o contexto atualizado
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        for password in queryset:
            password.decrypted_password = password.get_password()  # Adiciona a senha descriptografada ao objeto
        return queryset

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
    return render(request, 'administration/passwordManager/password_manager_form.html', {'form': form})

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def create_user(request):
    activegroup = 'administration'
    title = 'Criação de Usuarios'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration_users')  # Redirecionar para a página de login após o registro bem-sucedido
    else:
        form = UserCreationForm()
    context = {'form': form,
               'activegroup': activegroup,
               'title': title}
    return render(request, 'administration/user/user_form.html', context)


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


@login_required
def get_logged_in_user_profile(request):
    user = request.user
    data = {
        'usuario_datasul': user.usuario_datasul,
        'usuario_fluig': user.usuario_fluig,
    }
    return JsonResponse(data)