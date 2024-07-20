from django.utils import timezone
from datetime import datetime, timedelta
import json
from  django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
import django.utils
from django.views.generic import ListView
from django.views.generic import CreateView
from api_v1.models import Dataset, FluigDatabaseInfo, FluigDatabaseSize, FluigOperationSystem, FluigRuntime
from novosProjetos.forms import ConsultoriaForm, ProjetoForm, SistemasForm
from novosProjetos.models import Sistemas, Consultoria, Projeto
from administration.models import ServidorFluig

# Create your views here.
@permission_required('global_permissions.combio_dashboard_ti', login_url='erro_page')
def novosprojetos_dashboard(request):
    title = 'Projetos Combio'
    activegroup = 'Projetos'
    servidores = ServidorFluig.objects.all().order_by('id')
    servidor_id = request.GET.get('servidor_id')
    status = request.GET.get('status', 'todos') 

    servidor_selecionado = get_object_or_404(ServidorFluig, id=servidor_id) if servidor_id else servidores.first()

    datasets = Dataset.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at')
    if status != 'todos':
        if status == 'sucesso':
            datasets = datasets.filter(syncstatussuccess=True)
        elif status == 'warning':
            datasets = datasets.filter(syncstatuswarning=True)
        elif status == 'erro':
            datasets = datasets.filter(syncstatuserror=True)

    # Inicializa um dicionário para o servidor selecionado
    dados_servidor = {
        'servidor': servidor_selecionado,
        'ultimo_database_info': FluigDatabaseInfo.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at').first(),
        'ultimo_database_size': FluigDatabaseSize.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at').first(),
        'ultimo_runtime': FluigRuntime.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at').first(),
        'ultimo_operation_system': FluigOperationSystem.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at').first(),
        'dados_memoria': FluigOperationSystem.objects.filter(servidor_fluig=servidor_selecionado).order_by('-created_at'),
        'datasets': datasets,
        'lasted_update_dataset': Dataset.objects.latest('created_at').created_at,
        'lasted_update_operation_system': FluigOperationSystem.objects.latest('created_at').created_at,
    }

    if dados_servidor['ultimo_operation_system']:
        try:
            server_hd_space = float(dados_servidor['ultimo_operation_system'].server_hd_space.replace(',', '.'))
            server_hd_space_free = float(dados_servidor['ultimo_operation_system'].server_hd_space_free.replace(',', '.'))
            server_hd_space_used = server_hd_space - server_hd_space_free
        except ValueError:
            server_hd_space_used = None

    dados_servidor['server_hd_space_used'] = server_hd_space_used

    agora = timezone.now()

# Filtra objetos criados no início do dia até o momento atual
    inicio_do_dia = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    fim_do_dia = inicio_do_dia + timedelta(days=1)
    dados_memoria = FluigOperationSystem.objects.filter(
                                                        servidor_fluig=servidor_selecionado,
                                                        created_at__range=(inicio_do_dia, fim_do_dia)
                                                ).order_by('-created_at'
                                                                        ).values('created_at', 'server_memory_size', 'server_memory_free')

    # Preparar os dados para o gráfico
    datas = [dado['created_at'].strftime("%Y-%m-%dT%H:%M:%S") for dado in dados_memoria]
    memoria_usada_mb = [int((dado['server_memory_size'] - dado['server_memory_free']) / (1024 * 1024)) for dado in dados_memoria]
    memoria_total_mb = [int(dado['server_memory_size'] / (1024 * 1024)) for dado in dados_memoria]


    # Convertendo os dados para JSON para serem utilizados pelo JavaScript
    dados_grafico = {
        'datas': datas,
        'memoria_usada_mb': memoria_usada_mb,
        'memoria_total_mb': memoria_total_mb,
     }
    dados_grafico_json = json.dumps(dados_grafico)
    context = {
        'servidor_selecionado': dados_servidor,  # Passa os dados do servidor selecionado
        'servidores': servidores,  # Passa a lista de todos os servidores para o template
        'activegroup': activegroup,
        'dados_grafico_json': dados_grafico_json, 
        'title': title,
    }
    return render(request, 'projetos/dashboard.html', context)

def novosprojetos_list(request):
    title = 'Relação dos Projetos de Customização'
    activegroup = 'Projetos'
    context = {'activegroup': activegroup,'title': title }
    return render(request, 'projetos/projetos/novosprojetos_list.html', context)


class ConsultoriaList(ListView):
    model = Consultoria
    queryset = Consultoria.objects.all()
    template_name = 'projetos/consultoria/consultoria_list.html'


    def get_context_data(self, **kwargs):
        # Primeiro, pegue o contexto existente da classe base
        context = super(ConsultoriaList, self).get_context_data(**kwargs)
        # Agora, adicione suas variáveis de contexto
        context['activegroup'] = 'Projetos'
        context['title'] = 'Consultorias'
        # Retorne o contexto atualizado
        return context

class ConsultoriaCreate(CreateView):
    model = Consultoria
    #fields = ['codigo', 'Item', 'grupo_id', 'icon_item', 'url', 'permission']
    form_class = ConsultoriaForm
    template_name = 'projetos/consultoria/consultoria_form.html'
    success_url = reverse_lazy('projetos_consultoria_list')

    def get_context_data(self, **kwargs):
        # Primeiro, pegue o contexto existente da classe base
        context = super(ConsultoriaCreate, self).get_context_data(**kwargs)
        # Agora, adicione suas variáveis de contexto
        context['activegroup'] = 'Projetos'
        context['title'] = 'Inclusão de Consultoria'
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

def consultoria_edit(request, consultoria_id):
    activegroup = 'Projetos'
    title = 'Edição de Projetos'
    context = {'activegroup': activegroup,
               'title' : title}
    consultoria = get_object_or_404(Consultoria, pk=consultoria_id)
    if request.method == "POST":
        form = ConsultoriaForm(request.POST, instance=consultoria)
        if form.is_valid():
            form.save()
            return redirect('projetos_consultoria_list')
        else:
            context['form'] = form
    else:
        form = ConsultoriaForm(instance=consultoria)
        context['form'] = form
    return render(request, 'projetos/consultoria/consultoria_edit.html', context)


def consultoria_delete(request, consultoria_id):
   
    consultoria = get_object_or_404(Consultoria, pk=consultoria_id)
    if request.method == "POST":
        consultoria.delete()
        messages.success(request, f'"{consultoria.nome}" foi excluído com sucesso.')
        return redirect('projetos_consultoria_list')
   
    return redirect('projetos_consultoria_list')



class SistemasList(ListView):
    model = Sistemas
    queryset = Sistemas.objects.all()
    template_name = 'projetos/sistemas/sistemas_list.html'


    def get_context_data(self, **kwargs):
        # Primeiro, pegue o contexto existente da classe base
        context = super(SistemasList, self).get_context_data(**kwargs)
        # Agora, adicione suas variáveis de contexto
        context['activegroup'] = 'Projetos'
        context['title'] = 'Sistemas'
        # Retorne o contexto atualizado
        return context



def sistemas_edit(request, sistemas_id):
    activegroup = 'Projetos'
    title = 'Edição de Projetos'
    context = {'activegroup': activegroup,
               'title' : title}
    sistemas = get_object_or_404(Sistemas, pk=sistemas_id)
    if request.method == "POST":
        form = SistemasForm(request.POST, instance=sistemas)
        if form.is_valid():
            form.save()
            return redirect('projetos_sistemas_list')
        else:
            context['form'] = form
    else:
        form = SistemasForm(instance=sistemas)
        context['form'] = form
    return render(request, 'projetos/sistemas/sistemas_edit.html', context)


def sistemas_delete(request, sistemas_id):
   
    sistemas = get_object_or_404(Sistemas, pk=sistemas_id)
    if request.method == "POST":
        sistemas.delete()
        messages.success(request, f'"{sistemas.nome}" foi excluído com sucesso.')
        return redirect('projetos_sistemas_list')
   
    return redirect('projetos_sistemas_list')


class ProjetosList(ListView):
    model = Projeto
    queryset = Projeto.objects.all()
    template_name = 'projetos/projetos/projetos_list.html'


    def get_context_data(self, **kwargs):
        # Primeiro, pegue o contexto existente da classe base
        context = super(ProjetosList, self).get_context_data(**kwargs)
        # Agora, adicione suas variáveis de contexto
        context['activegroup'] = 'Projetos'
        context['title'] = 'Projetos de Customização'
        # Retorne o contexto atualizado
        return context
    


def projetos_delete(request, projetos_id):
   
    projeto = get_object_or_404(Projeto, pk=projetos_id)
    if request.method == "POST":
        projeto.delete()
        messages.success(request, f'"{projeto.nome_projeto}" foi excluído com sucesso.')
        return redirect('projetos_projetos_list')
   
    return redirect('projetos_projetos_list')



def sistema_create(request):
    activegroup = 'Projetos'
    title = 'Criação de Sistemas'
    context = {'activegroup': activegroup,
               'title' : title}
    if request.method == 'POST':
        form = SistemasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projetos_sistemas_list')
        else:
            context['form'] = form
    else:
        form = SistemasForm()
        context['form'] = form
    return render(request, 'projetos/sistemas/sistemas_form.html', context)


def consultoria_create(request):
    activegroup = 'Projetos'
    title = 'Criação de Consultoria'
    context = {'activegroup': activegroup,
               'title' : title}
    if request.method == 'POST':
        form = ConsultoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projetos_consultoria_list')
        else:
            context['form'] = form
    else:
        form = ConsultoriaForm()
        context['form'] = form
    return render(request, 'projetos/consultoria/consultoria_form.html', context)


def projeto_create(request):
    activegroup = 'Projetos'
    title = 'Criação de Projetos'
    context = {'activegroup': activegroup,
               'title' : title}
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projetos_projetos_list')
        else:
            context['form'] = form
    else:
        form = ProjetoForm()
        context['form'] = form
    return render(request, 'projetos/projetos/projetos_form.html', context)