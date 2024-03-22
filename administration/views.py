from django.shortcuts import render
from administration.models import User, ServidorFluig
from administration.forms import CustomUserChangeForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.forms import CheckboxSelectMultiple
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import ServidorFluigForm
from menu.models import ItensMenu
from django.urls import reverse_lazy
from .forms import ItensMenuForm


def user_list(request):
    # Permissões e Definições para o Menu
    activegroup = 'administration'
    title = 'Usuários'
    users = User.objects.all()
    context = {'users': users,
               'activegroup': activegroup,
               'title': title}
    return render(request, 'users/user_list.html', context)


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


def servidorfluig_list(request):
    # Permissões e Definições para o Menu
    activegroup = 'administration'
    title = 'Servidores Fluig'


    servidoresfluig = ServidorFluig.objects.all()
    context = {'servidoresfluig': servidoresfluig,
               'activegroup': activegroup,
               'title' : title}
    return render(request, 'administration/servidorfluig/servidor_list.html', context)




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