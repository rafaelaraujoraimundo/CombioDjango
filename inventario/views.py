from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from dashboard.models import BiCentroCusto, BiEstabelecimento, BiFuncionariosCombio
from .models import Controlekit, Estoque, Status, TipoItem, ControleFones, Celular, AcoesProntuario
from .forms import ControleFonesForm, ControlekitForm, EstoqueForm, StatusForm, TipoItemForm, CelularForm, AcoesProntuarioForm
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.timezone import now
# View para listagem dos tipos de itens
class TipoItemList(ListView):
    model = TipoItem
    queryset = TipoItem.objects.all()
    template_name = 'inventario/tipoitem/tipoitem_list.html'

    def get_context_data(self, **kwargs):
        context = super(TipoItemList, self).get_context_data(**kwargs)
        context['activegroup'] = 'administration'
        context['title'] = 'Tipos de Itens'
        return context

# View para criação de novos tipos de itens
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class TipoItemCreate(CreateView):
    model = TipoItem
    form_class = TipoItemForm
    template_name = 'inventario/tipoitem/tipoitem_form.html'
    success_url = reverse_lazy('tipoitem_list')

    def get_context_data(self, **kwargs):
        context = super(TipoItemCreate, self).get_context_data(**kwargs)
        context['activegroup'] = 'administration'
        context['title'] = 'Inclusão de Tipo de Item'
        return context

# View para editar tipos de itens existentes
@login_required(login_url='account_login')
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def TipoItem_edit(request, tipoitem_id):
    activegroup = 'administration'
    title = 'Edição de Tipo de Item'
    context = {'activegroup': activegroup, 'title': title}
    tipoitem = get_object_or_404(TipoItem, pk=tipoitem_id)
    if request.method == "POST":
        form = TipoItemForm(request.POST, instance=tipoitem)
        if form.is_valid():
            form.save()
            return redirect('tipoitem_list')
        else:
            context['form'] = form
    else:
        form = TipoItemForm(instance=tipoitem)
        context['form'] = form
    return render(request, 'inventario/tipoitem/tipoitem_edit.html', context)


@login_required(login_url='account_login')
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def tipoItem_delete(request, tipoitem_id):
    tipoitem = get_object_or_404(TipoItem, pk=tipoitem_id)
    if request.method == "POST":
        tipoitem.delete()
        messages.success(request, f'"{tipoitem.nome}" foi excluído com sucesso.')
        return redirect('tipoitem_list')

    return redirect('tipoitem_list')



class StatusList(ListView):
    model = Status
    queryset = Status.objects.all()
    template_name = 'inventario/status/status_list.html'

    def get_context_data(self, **kwargs):
        context = super(StatusList, self).get_context_data(**kwargs)
        context['activegroup'] = 'administration'
        context['title'] = 'Lista de Status'
        return context

# View para criação de novos Status
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class StatusCreate(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'inventario/status/status_form.html'
    success_url = reverse_lazy('status_list')

    def get_context_data(self, **kwargs):
        context = super(StatusCreate, self).get_context_data(**kwargs)
        context['activegroup'] = 'administration'
        context['title'] = 'Inclusão de Status'
        return context

# View para edição de Status
@login_required(login_url='account_login')
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def status_edit(request, status_id):
    activegroup = 'administration'
    title = 'Edição de Status'
    context = {'activegroup': activegroup, 'title': title}
    status = get_object_or_404(Status, pk=status_id)
    if request.method == "POST":
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('status_list')
        else:
            context['form'] = form
    else:
        form = StatusForm(instance=status)
        context['form'] = form
    return render(request, 'inventario/status/status_edit.html', context)

# View para exclusão de Status
@login_required(login_url='account_login')
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def status_delete(request, status_id):
    status = get_object_or_404(Status, pk=status_id)
    if request.method == "POST":
        status.delete()
        messages.success(request, f'"{status.nome_status}" foi excluído com sucesso.')
        return redirect('status_list')

    return redirect('status_list')



# View para listagem dos itens de estoque
class EstoqueList(ListView):
    model = Estoque
    queryset = Estoque.objects.all()
    template_name = 'inventario/estoque/estoque_list.html'

    def get_context_data(self, **kwargs):
        context = super(EstoqueList, self).get_context_data(**kwargs)
        context['activegroup'] = 'inventario'
        context['title'] = 'Lista de Itens de Estoque'
        return context

# View para criação de novos itens de estoque
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class EstoqueCreate(CreateView):
    model = Estoque
    form_class = EstoqueForm
    template_name = 'inventario/estoque/estoque_form.html'
    success_url = reverse_lazy('estoque_list')

    def get_context_data(self, **kwargs):
        context = super(EstoqueCreate, self).get_context_data(**kwargs)
        context['activegroup'] = 'inventario'
        context['title'] = 'Inclusão de Item no Estoque'
        return context

# View para editar itens de estoque existentes
@login_required(login_url='account_login')
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def estoque_edit(request, estoque_id):
    activegroup = 'inventario'
    title = 'Edição de Item no Estoque'
    context = {'activegroup': activegroup, 'title': title}
    estoque = get_object_or_404(Estoque, pk=estoque_id)
    if request.method == "POST":
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            return redirect('estoque_list')
        else:
            context['form'] = form
    else:
        form = EstoqueForm(instance=estoque)
        context['form'] = form
    return render(request, 'inventario/estoque/estoque_edit.html', context)

# View para exclusão de itens de estoque
@login_required(login_url='account_login')
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def estoque_delete(request, estoque_id):
    estoque = get_object_or_404(Estoque, pk=estoque_id)
    if request.method == "POST":
        estoque.delete()
        messages.success(request, f'O item "{estoque.modelo}" foi excluído com sucesso.')
        return redirect('estoque_list')

    return redirect('estoque_list')

@method_decorator(login_required(login_url='account_login'), name='dispatch')
class ControlekitList(ListView):
    model = Controlekit
    template_name = 'inventario/controlekit/controlekit_list.html'

    def get_context_data(self, **kwargs):
        context = super(ControlekitList, self).get_context_data(**kwargs)
        context['title'] = 'Lista de Kits'
        context['activegroup'] = 'inventario'
        return context

# View para criar novo kit
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class ControlekitCreate(CreateView):
    model = Controlekit
    form_class = ControlekitForm
    template_name = 'inventario/controlekit/controlekit_form.html'
    success_url = reverse_lazy('controlekit_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios_list'] = BiFuncionariosCombio.objects.filter(mes=now().month, ano=now().year).values('cdn_funcionario', 'nom_funcionario', 'cdn_estab')
        context['estabelecimentos_list'] = BiEstabelecimento.objects.all().values('estabelecimento', 'sigla_unidade')
        context['centros_custo_list'] = BiCentroCusto.objects.all().values('centrocusto', 'descricaocusto')
        context['activegroup'] = 'inventario'
        context['title'] = 'Criação de Kit'
        return context
    
    def form_valid(self, form):
        # Verifique os dados recebidos e certifique-se de que estão corretos
        print(form.cleaned_data)  # Para debug
        return super().form_valid(form)


# View para editar kit
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class ControlekitUpdate(UpdateView):
    model = Controlekit
    form_class = ControlekitForm
    template_name = 'inventario/controlekit/controlekit_edit.html'
    success_url = reverse_lazy('controlekit_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passar os dados necessários para preencher os datalists
        context['usuarios_list'] = BiFuncionariosCombio.objects.filter(mes=now().month, ano=now().year).values('cdn_funcionario', 'nom_funcionario', 'cdn_estab')
        context['estabelecimentos_list'] = BiEstabelecimento.objects.all().values('estabelecimento', 'sigla_unidade')
        context['centros_custo_list'] = BiCentroCusto.objects.all().values('centrocusto', 'descricaocusto')
        context['activegroup'] = 'inventario'
        context['title'] = 'Alteração de Kit'
        return context

# View para excluir kit
@login_required(login_url='account_login')
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def controlekit_delete(request, controlekit_id):
    controlekit = get_object_or_404(Controlekit, pk=controlekit_id)
    if request.method == "POST":
        controlekit.delete()
        messages.success(request, 'Kit excluído com sucesso.')
        return redirect('controlekit_list')
    return redirect('controlekit_list')


@method_decorator(login_required(login_url='account_login'), name='dispatch')
class ControleFonesList(ListView):
    model = ControleFones
    template_name = 'inventario/controlefones/controlefones_list.html'

    def get_context_data(self, **kwargs):
        context = super(ControleFonesList, self).get_context_data(**kwargs)
        context['title'] = 'Lista de Fones'
        context['activegroup'] = 'inventario'
        return context

# View para criar novo fone
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class ControleFonesCreate(CreateView):
    model = ControleFones
    form_class = ControleFonesForm
    template_name = 'inventario/controlefones/controlefones_form.html'
    success_url = reverse_lazy('controlefones_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios_list'] = BiFuncionariosCombio.objects.filter(mes=now().month, ano=now().year).values('cdn_funcionario', 'nom_funcionario', 'cdn_estab')
        context['estabelecimentos_list'] = BiEstabelecimento.objects.all().values('estabelecimento', 'sigla_unidade')
        context['centros_custo_list'] = BiCentroCusto.objects.all().values('centrocusto', 'descricaocusto')
        context['activegroup'] = 'inventario'
        context['title'] = 'Criação de Controle de Fones'
        return context

# View para editar fone
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class ControleFonesUpdate(UpdateView):
    model = ControleFones
    form_class = ControleFonesForm
    template_name = 'inventario/controlefones/controlefones_edit.html'
    success_url = reverse_lazy('controlefones_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios_list'] = BiFuncionariosCombio.objects.filter(mes=now().month, ano=now().year).values('cdn_funcionario', 'nom_funcionario', 'cdn_estab')
        context['estabelecimentos_list'] = BiEstabelecimento.objects.all().values('estabelecimento', 'sigla_unidade')
        context['centros_custo_list'] = BiCentroCusto.objects.all().values('centrocusto', 'descricaocusto')
        context['activegroup'] = 'inventario'
        context['title'] = 'Edição de Controle de Fones'
        return context

# View para excluir fone
@login_required(login_url='account_login')
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def controlefones_delete(request, controlefones_id):
    controlefones = get_object_or_404(ControleFones, pk=controlefones_id)
    if request.method == "POST":
        controlefones.delete()
        messages.success(request, 'Fone excluído com sucesso.')
        return redirect('controlefones_list')
    return redirect('controlefones_list')



@method_decorator(login_required(login_url='account_login'), name='dispatch')
class CelularList(ListView):
    model = Celular
    template_name = 'inventario/celular/celular_list.html'

    def get_context_data(self, **kwargs):
        context = super(CelularList, self).get_context_data(**kwargs)
        context['title'] = 'Lista de Celulares'
        context['activegroup'] = 'inventario'
        return context


@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class CelularCreate(CreateView):
    model = Celular
    form_class = CelularForm
    template_name = 'inventario/celular/celular_form.html'
    success_url = reverse_lazy('celular_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inclusão de Celulares'
        context['activegroup'] = 'inventario'
        
        # Listas para autocomplete
        context['status_list'] = Status.objects.all()
        context['usuarios_list'] = BiFuncionariosCombio.objects.filter(
            mes=now().month, ano=now().year
        ).values('cdn_funcionario', 'nom_funcionario', 'cdn_estab')
        
        context['estabelecimentos_list'] = BiEstabelecimento.objects.all().values(
            'estabelecimento', 'sigla_unidade'
        )
        
        context['centros_custo_list'] = BiCentroCusto.objects.all().values(
            'centrocusto', 'descricaocusto'
        )
        
        return context

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class CelularUpdate(UpdateView):
    model = Celular
    form_class = CelularForm
    template_name = 'inventario/celular/celular_edit.html'
    success_url = reverse_lazy('celular_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lista de usuários, estabelecimentos, centros de custo e status para preencher os campos de datalist
        context['usuarios_list'] = BiFuncionariosCombio.objects.filter(mes=now().month, ano=now().year).values('cdn_funcionario', 'nom_funcionario', 'cdn_estab')
        context['estabelecimentos_list'] = BiEstabelecimento.objects.all().values('estabelecimento', 'sigla_unidade')
        context['centros_custo_list'] = BiCentroCusto.objects.all().values('centrocusto', 'descricaocusto')
        context['status_list'] = Status.objects.all()  # Para o campo de status
        context['title'] = 'Edição de Celular'
        context['activegroup'] = 'inventario'
        return context


@login_required(login_url='account_login')
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def celular_delete(request, celular_id):
    celular = get_object_or_404(Celular, pk=celular_id)
    if request.method == "POST":
        celular.delete()
        messages.success(request, 'Celular excluído com sucesso.')
        return redirect('celular_list')
    return redirect('celular_list')

class AcoesProntuarioList(ListView):
    model = AcoesProntuario
    queryset = AcoesProntuario.objects.all()
    template_name = 'inventario/acoesprontuario/acoesprontuario_list.html'

    def get_context_data(self, **kwargs):
        context = super(AcoesProntuarioList, self).get_context_data(**kwargs)
        context['activegroup'] = 'administration'
        context['title'] = 'Lista de Ações de Prontuário'
        return context

# Criação de nova Ação de Prontuário
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_admin_admin', login_url='erro_page'), name='dispatch')
class AcoesProntuarioCreate(CreateView):
    model = AcoesProntuario
    form_class = AcoesProntuarioForm
    template_name = 'inventario/acoesprontuario/acoesprontuario_form.html'
    success_url = reverse_lazy('acoesprontuario_list')

    def get_context_data(self, **kwargs):
        context = super(AcoesProntuarioCreate, self).get_context_data(**kwargs)
        context['activegroup'] = 'administration'
        context['title'] = 'Inclusão de Ação de Prontuário'
        return context

# Edição de Ações de Prontuário
@login_required(login_url='account_login')
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def acoesprontuario_edit(request, acoesprontuario_id):
    activegroup = 'administration'
    title = 'Edição de Ação de Prontuário'
    context = {'activegroup': activegroup, 'title': title}
    acoesprontuario = get_object_or_404(AcoesProntuario, pk=acoesprontuario_id)
    if request.method == "POST":
        form = AcoesProntuarioForm(request.POST, instance=acoesprontuario)
        if form.is_valid():
            form.save()
            return redirect('acoesprontuario_list')
        else:
            context['form'] = form
    else:
        form = AcoesProntuarioForm(instance=acoesprontuario)
        context['form'] = form
    return render(request, 'inventario/acoesprontuario/acoesprontuario_edit.html', context)

# Exclusão de Ações de Prontuário
@login_required(login_url='account_login')
@permission_required('global_permissions.combio_admin_admin', login_url='erro_page')
def acoesprontuario_delete(request, acoesprontuario_id):
    acoesprontuario = get_object_or_404(AcoesProntuario, pk=acoesprontuario_id)
    if request.method == "POST":
        acoesprontuario.delete()
        messages.success(request, f'"{acoesprontuario.acao}" foi excluído com sucesso.')
        return redirect('acoesprontuario_list')

    return redirect('acoesprontuario_list')