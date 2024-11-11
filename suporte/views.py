import django.contrib.auth
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.shortcuts import get_object_or_404, redirect, render
from dashboard.models import BiCentroCusto, BiEstabelecimento, BiFuncionariosCombio
from .models import Substituicao, UsuarioDesligamento, UsuarioFluig
from .forms import SubstituicaoForm, UsuarioDesligamentoForm
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.timezone import now
from .tasks import substituir_usuario_fluig, update_usuario_fluig
from django.views import View
from administration .models import GroupProcess, GroupProcessSelection
from django.db.models import Count




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
    


from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views import View
from django.shortcuts import render, redirect
from .forms import SubstituicaoForm
from .models import Substituicao, GroupProcess
from .tasks import substituir_usuario_fluig

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_inventario', login_url='erro_page'), name='dispatch')
class CreateSubstitutoFluig(View):
    template_name = 'suporte/substitutofluig/substituto_fluig_form.html'
    result_template_name = 'suporte/substitutofluig/substituicao_list.html'

    def get(self, request):
        form = SubstituicaoForm()
        context = {
            'form': form,
            'activegroup': 'suporte',
            'title': 'Criação Substituto Fluig'
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SubstituicaoForm(request.POST)
        if form.is_valid():
            # Dados do formulário
            usuario_a_substituir = form.cleaned_data['usuario_a_substituir']
            usuario_substituto = form.cleaned_data['usuario_substituto']
            data_inicial = form.cleaned_data['data_inicial']
            data_final = form.cleaned_data['data_final']
            selected_groups = form.cleaned_data['grupos_switch']
            processes = [{'process': process.process.process_id} for group in selected_groups for process in group.process_selections.all()]

            # JSON para a task
            json_result = {
                "companyId": 1,
                "userId": usuario_a_substituir.code,
                "substituteId": usuario_substituto.code,
                "validationStartDate": data_inicial.strftime('%d/%m/%Y'),
                "validationFinalDate": data_final.strftime('%d/%m/%Y'),
                "processes": processes
            }
            print("JSON de substituição gerado:", json_result)

            # Executa a task de substituição de usuário
            result = substituir_usuario_fluig(json_result)

            if result["status"] == "success":
                # Salva a substituição no banco de dados com o usuário que a criou
                substituicao = Substituicao.objects.create(
                    usuario_a_substituir=usuario_a_substituir,
                    usuario_substituto=usuario_substituto,
                    data_inicial=data_inicial,
                    data_final=data_final,
                    usuario_inclusao=request.user  # Atribui o usuário atual
                )
                substituicao.grupos_switch.set(selected_groups)  # Atribui os grupos selecionados
                messages.success(request, result["message"])
                return redirect('substituicao_list')  # Redireciona para a lista em caso de sucesso

            # Caso de erro ao chamar a API
            messages.error(request, result["message"])

        # Renderiza o formulário novamente com o erro da API ou validação do formulário
        context = {
            'form': form,
            'activegroup': 'suporte',
            'title': 'Criação Substituto Fluig'
        }
        return render(request, self.template_name, context)


class SubstituicaoListView(ListView):
    model = Substituicao
    template_name = 'suporte/substitutofluig/substituicao_list.html'
    context_object_name = 'substituicoes'

    def get_queryset(self):
        # Prefetch the related processes to optimize counting
        queryset = super().get_queryset().select_related(
            'usuario_a_substituir', 'usuario_substituto', 'usuario_inclusao'
        ).prefetch_related('grupos_switch__process_selections__process')
        
        # Annotate each substituicao with the total count of processes
        queryset = queryset.annotate(
            total_process_count=Count('grupos_switch__process_selections__process', distinct=True)
        )
        
        return queryset

    def get_context_data(self, **kwargs):
        # Add additional context for template
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Lista de Substituto Fluig'
        return context
    

class SubstituicaoDetailView(DetailView):
    model = Substituicao
    template_name = 'suporte/substitutofluig/substituicao_detail.html'
    context_object_name = 'substituicao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Detalhes da Substituição'
        # Calcula o número total de processos nos grupos selecionados
        context['total_processes'] = sum(group.process_selections.count() for group in self.object.grupos_switch.all())
        return context