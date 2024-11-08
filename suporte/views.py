from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from dashboard.models import BiCentroCusto, BiEstabelecimento, BiFuncionariosCombio
from .models import (UsuarioDesligamento)
from .forms import (UsuarioDesligamentoForm)
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.timezone import now



# Create your views here.
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_inventario', login_url='erro_page'), name='dispatch')
class UsuarioDesligamentoCreate(CreateView):
    model = UsuarioDesligamento
    form_class = UsuarioDesligamentoForm
    template_name = 'suporte/desligamento/desligamento_form.html'
    success_url = reverse_lazy('usuario_desligamento_list')

    def get_context_data(self, **kwargs):
        context = super(UsuarioDesligamentoCreate, self).get_context_data(**kwargs)
        context['activegroup'] = 'inventario'
        context['title'] = 'Novo Desligamento de Usuário'
        context['usuarios_list'] = BiFuncionariosCombio.objects.all().values('cdn_funcionario', 'nom_funcionario', 'cdn_estab')
        return context

    def form_valid(self, form):
        form.instance.usuario_cadastro = self.request.user  # Define o usuário de criação
        return super().form_valid(form)


@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_inventario', login_url='erro_page'), name='dispatch')
class UsuarioDesligamentoList(ListView):
    model = UsuarioDesligamento
    template_name = 'suporte/desligamento/usuario_desligamento_list.html'
    context_object_name = 'desligamentos'

    def get_context_data(self, **kwargs):
        context = super(UsuarioDesligamentoList, self).get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Desligamento de Usuários'


        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_inventario', login_url='erro_page'), name='dispatch')
class UsuarioDesligamentoUpdate(UpdateView):
    model = UsuarioDesligamento
    form_class = UsuarioDesligamentoForm
    template_name = 'suporte/desligamento/desligamento_form.html'
    success_url = reverse_lazy('usuario_desligamento_list')

    def get_context_data(self, **kwargs):
        context = super(UsuarioDesligamentoUpdate, self).get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Editar Desligamento de Usuário'
        context['usuarios_list'] = BiFuncionariosCombio.objects.all().values('cdn_funcionario', 'nom_funcionario', 'cdn_estab')
        return context

    def form_valid(self, form):
        form.instance.usuario_ultima_alteracao = self.request.user  # Define o usuário de alteração
        return super().form_valid(form)

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_inventario', login_url='erro_page'), name='dispatch')
class UsuarioDesligamentoDelete(DeleteView):
    model = UsuarioDesligamento
    template_name = 'suporte/desligamento/usuario_desligamento_confirm_delete.html'
    success_url = reverse_lazy('usuario_desligamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Confirmar Exclusão de Usuário'
        return context