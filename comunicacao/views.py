from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ConfiguracaoForm
from .models import Configuracao
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_comunicacao', login_url='erro_page'), name='dispatch')
class ConfiguracaoListView(ListView):
    model = Configuracao
    template_name = 'comunicacao/papeldeparede/configuracao_list.html'
    context_object_name = 'configuracoes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Papel de Parede'  # Título específico para a listagem
        context['activegroup'] = 'comunicacao'  # Grupo ativo no menu
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_comunicacao', login_url='erro_page'), name='dispatch')
class ConfiguracaoCreateView(LoginRequiredMixin, CreateView):
    model = Configuracao
    form_class = ConfiguracaoForm
    template_name = 'comunicacao/papeldeparede/configuracao_form.html'
    success_url = reverse_lazy('configuracao_list')

    def form_valid(self, form):
        form.instance.usuario_inclusao = self.request.user  # Define o usuário de inclusão
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Adicionar Papel de Parede'  # Título para criação
        context['activegroup'] = 'comunicacao'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_comunicacao', login_url='erro_page'), name='dispatch')
class ConfiguracaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Configuracao
    form_class = ConfiguracaoForm
    template_name = 'comunicacao/papeldeparede/configuracao_form.html'
    success_url = reverse_lazy('configuracao_list')

    def form_valid(self, form):
        form.instance.usuario_alteracao = self.request.user  # Atualiza o usuário de alteração
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Papel de Parede'  # Título para edição
        context['activegroup'] = 'comunicacao'
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_comunicacao', login_url='erro_page'), name='dispatch')
class ConfiguracaoDeleteView(DeleteView):
    model = Configuracao
    template_name = 'comunicacao/papeldeparede/configuracao_confirm_delete.html'
    success_url = reverse_lazy('configuracao_list')

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'status': 'success'}, status=200)
        else:
            response = super(ConfiguracaoDeleteView, self).delete(request, *args, **kwargs)
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Papel de Parede'
        context['activegroup'] = 'comunicacao'
        return context