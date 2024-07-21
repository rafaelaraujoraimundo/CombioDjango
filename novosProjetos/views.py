from  django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import CreateView
from api_v1.models import Dataset, FluigDatabaseInfo, FluigDatabaseSize, FluigOperationSystem, FluigRuntime
from novosProjetos.forms import ConsultoriaForm, ProjetoForm, SistemasForm
from novosProjetos.models import Sistemas, Consultoria, Projeto
from administration.models import ServidorFluig
from django.db.models import F, Sum
from django.utils.decorators import method_decorator

# Create your views here.
@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
def novosprojetos_dashboard(request):
    title = 'Projetos Combio'
    activegroup = 'Projetos'
    consultoria_id = request.GET.get('consultoria_id')
    consultorias = Consultoria.objects.all()
    sistemas = Sistemas.objects.all()

    if consultoria_id:
        projetos_filtrados = Projeto.objects.filter(consultoria__id=consultoria_id)
        consultoria_selecionada = Consultoria.objects.get(id=consultoria_id)
    else:
        projetos_filtrados = Projeto.objects.all()
        consultoria_selecionada = None

    
    #Grafico de Rosca
    grafico_por_sistemas = []
    for sistema in sistemas:
        count_projetos = projetos_filtrados.filter(sistemas=sistema).count()
        if count_projetos > 0:  # Incluir apenas sistemas com projetos
            grafico_por_sistemas.append({'label': sistema.nome, 'value': count_projetos})

    # GRafico de Consultoria Empilhado
    categorias = [consultoria.nome for consultoria in consultorias]
    dados_temp = {sistema.nome: [0] * len(categorias) for sistema in sistemas}
    active_categories = [False] * len(categorias)  # Rastreador de categorias ativas

    # Coletar dados
    for idx, consultoria in enumerate(consultorias):
        for sistema in sistemas:
            count = projetos_filtrados.filter(consultoria=consultoria, sistemas=sistema).count()
            dados_temp[sistema.nome][idx] = count
            if count > 0:
                active_categories[idx] = True  # Marca a categoria como ativa

    # Filtrar categorias e dados baseados na atividade
    categorias_ativas = [cat for idx, cat in enumerate(categorias) if active_categories[idx]]
    series = [{'name': sistema, 'data': [data[idx] for idx, active in enumerate(active_categories) if active]} for sistema, data in dados_temp.items()]
    valor_total_projetos = projetos_filtrados.annotate(
        custo_projeto=F('horas_utilizadas') * F('consultoria__valor_hora')
    ).aggregate(total=Sum('custo_projeto'))['total'] or 0  # Usar 'or 0' para lidar com None


    context = {
        'activegroup': activegroup,
        'projetos': projetos_filtrados,
        'consultorias': consultorias,
        'consultoria_selecionada': consultoria_selecionada,
        'title': title,
        'categorias': categorias_ativas,
        'series': series,
        'valor_total_projetos': valor_total_projetos,
        'grafico_por_sistemas': grafico_por_sistemas
    }

    return render(request, 'projetos/dashboard.html', context)

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_project_user', login_url='erro_page') 
def novosprojetos_list(request):
    title = 'Relação dos Projetos de Customização'
    activegroup = 'Projetos'
    context = {'activegroup': activegroup,'title': title }
    return render(request, 'projetos/projetos/novosprojetos_list.html', context)

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_project_admin', login_url='erro_page'), name='dispatch')
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


@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_project_admin', login_url='erro_page'), name='dispatch')
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

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_project_admin', login_url='erro_page')
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

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_project_admin', login_url='erro_page')
def consultoria_delete(request, consultoria_id):
   
    consultoria = get_object_or_404(Consultoria, pk=consultoria_id)
    if request.method == "POST":
        consultoria.delete()
        messages.success(request, f'"{consultoria.nome}" foi excluído com sucesso.')
        return redirect('projetos_consultoria_list')
   
    return redirect('projetos_consultoria_list')

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_project_admin', login_url='erro_page'), name='dispatch')
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


@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_project_admin', login_url='erro_page')
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

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_project_admin', login_url='erro_page')
def sistemas_delete(request, sistemas_id):
   
    sistemas = get_object_or_404(Sistemas, pk=sistemas_id)
    if request.method == "POST":
        sistemas.delete()
        messages.success(request, f'"{sistemas.nome}" foi excluído com sucesso.')
        return redirect('projetos_sistemas_list')
   
    return redirect('projetos_sistemas_list')

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_project_user', login_url='erro_page'), name='dispatch')
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
    

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_project_user', login_url='erro_page')
def projetos_delete(request, projetos_id):
   
    projeto = get_object_or_404(Projeto, pk=projetos_id)
    if request.method == "POST":
        projeto.delete()
        messages.success(request, f'"{projeto.nome_projeto}" foi excluído com sucesso.')
        return redirect('projetos_projetos_list')
   
    return redirect('projetos_projetos_list')


@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_project_admin', login_url='erro_page')
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

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_project_admin', login_url='erro_page')
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

@login_required(login_url='account_login')  # Redireciona para a página de login se não estiver logado
@permission_required('global_permissions.combio_project_user', login_url='erro_page')
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