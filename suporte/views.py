import django.contrib.auth
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.shortcuts import get_object_or_404, redirect, render
from dashboard.models import BiCentroCusto, BiEstabelecimento, BiFuncionariosCombio
from .models import Substituicao, UsuarioDesligamento, UsuarioFluig, MS365Tenant, MS365UserSearchLog, MS365UserUpdateLog
from .forms import SubstituicaoForm, UsuarioDesligamentoForm, MS365TenantForm, MS365UserSearchForm, MS365UserUpdateForm, MS365ManagerForm, MS365ListUsersForm
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.timezone import now
from .tasks import substituir_usuario_fluig, update_usuario_fluig, atualizar_usuarios_m365
from django.views import View
from administration .models import GroupProcess, GroupProcessSelection
from django.db.models import Count
from django.http import HttpResponse
import csv
import logging
from django.utils.encoding import smart_str
import codecs
from collections import defaultdict
from .models import UsuarioM365



logger = logging.getLogger(__name__)

# suporte/views.py - Adicionar ao arquivo existente

import json
from django.http import JsonResponse

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .m365_service import MS365ApiService


def get_client_ip(request):
    """Utilitário para obter IP do cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# ==================== VIEWS PARA GERENCIAMENTO DE TENANTS ====================

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
class MS365TenantListView(ListView):
    model = MS365Tenant
    template_name = 'suporte/m365/tenant_list.html'
    context_object_name = 'tenants'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Tenants Microsoft 365'
        return context


@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
class MS365TenantCreateView(CreateView):
    model = MS365Tenant
    form_class = MS365TenantForm
    template_name = 'suporte/m365/tenant_form.html'
    success_url = reverse_lazy('m365_tenant_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Novo Tenant Microsoft 365'
        context['action'] = 'Criar'
        return context
    
    def form_valid(self, form):
        form.instance.usuario_criacao = self.request.user
        form.instance.usuario_ultima_alteracao = self.request.user
        messages.success(self.request, 'Tenant criado com sucesso!')
        return super().form_valid(form)


@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
class MS365TenantUpdateView(UpdateView):
    model = MS365Tenant
    form_class = MS365TenantForm
    template_name = 'suporte/m365/tenant_form.html'
    success_url = reverse_lazy('m365_tenant_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_edit_mode'] = True
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Editar Tenant Microsoft 365'
        context['action'] = 'Atualizar'
        return context
    
    def form_valid(self, form):
        form.instance.usuario_ultima_alteracao = self.request.user
        messages.success(self.request, 'Tenant atualizado com sucesso!')
        return super().form_valid(form)


@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
class MS365TenantDeleteView(DeleteView):
    model = MS365Tenant
    template_name = 'suporte/m365/tenant_confirm_delete.html'
    success_url = reverse_lazy('m365_tenant_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Excluir Tenant Microsoft 365'
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tenant excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
@require_http_methods(["POST"])
def test_m365_connection(request, pk):
    """Testa conexão com tenant M365"""
    tenant = get_object_or_404(MS365Tenant, pk=pk)
    
    try:
        service = MS365ApiService(tenant)
        success, message = service.test_connection()
        
        return JsonResponse({
            'success': success,
            'message': message
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        })


# ==================== VIEWS PARA OPERAÇÕES COM USUÁRIOS ====================

@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
def m365_dashboard(request):
    """Dashboard principal do M365"""
    
    context = {
        'activegroup': 'suporte',
        'title': 'Microsoft 365 - Dashboard',
        'tenants_count': MS365Tenant.objects.filter(ativo=True).count(),
        'recent_searches': MS365UserSearchLog.objects.select_related('tenant', 'usuario_pesquisador').order_by('-data_pesquisa')[:10],
        'recent_updates': MS365UserUpdateLog.objects.select_related('tenant', 'usuario_atualizador').order_by('-data_atualizacao')[:10],
    }
    return render(request, 'suporte/m365/dashboard.html', context)


@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
def m365_search_user(request):
    """Buscar usuário no M365"""
    context = {
        'activegroup': 'suporte',
        'title': 'Microsoft 365 - Buscar Usuário',
    }
    
    if request.method == 'POST':
        form = MS365UserSearchForm(request.POST)
        if form.is_valid():
            tenant = form.cleaned_data['tenant']
            termo_busca = form.cleaned_data['termo_busca']
            
            try:
                service = MS365ApiService(tenant)
                user_data, error_msg = service.get_user(
                    termo_busca, 
                    requesting_user=request.user,
                    ip_address=get_client_ip(request)
                )
            
                if user_data:
                    context['user_data'] = user_data
                    context['success'] = True
                    messages.success(request, 'Usuário encontrado com sucesso!')

                    # Buscar manager
                    try:
                        manager_data, _ = service.get_user_manager(user_data['id'])
                        if manager_data:
                            context['manager_data'] = manager_data
                    except Exception as e:
                        logger.warning(f"Não foi possível obter o manager: {e}")
            except Exception as e:
                error_msg = f'Erro interno: {str(e)}'
                context['error_message'] = error_msg
                messages.error(request, error_msg)
    else:
        form = MS365UserSearchForm()
    
    context['form'] = form
    return render(request, 'suporte/m365/search_user.html', context)


@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
def m365_list_users(request):
    context = {
        'activegroup': 'suporte',
        'title': 'Microsoft 365 - Listar Usuários',
    }

    if request.method == 'POST':
        form = MS365ListUsersForm(request.POST)
        acao = request.POST.get('acao', 'listar')

        if form.is_valid():
            tenant = form.cleaned_data['tenant']
            filtro = form.cleaned_data['filtro']
            service = MS365ApiService(tenant)
            users_list, error_msg = service.list_users(filtro)

            if acao == 'exportar' and users_list:
                # Exportar para CSV com delimitador ; e UTF-8 BOM
                from io import StringIO

                response = HttpResponse(content_type='text/csv; charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="usuarios_m365.csv"'

                csv_buffer = StringIO()
                writer = csv.writer(csv_buffer, delimiter=';')

                # Cabeçalho
                writer.writerow([
                    'Nome Completo', 'Email', 'UPN', 'ID', 'Nome', 'Sobrenome',
                    'Cargo', 'Departamento', 'Localização', 'Telefone(s)',
                    'Celular', 'Tipo', 'Ativo', 'Criado em', 'Último Login', 'Idioma',
                    'Gerente', 'Email do Gerente', 'Cargo do Gerente'
                ])

                # Linhas de dados
                for user in users_list:
                    writer.writerow([
                        user.get('displayName', ''),
                        user.get('mail') or user.get('userPrincipalName'),
                        user.get('userPrincipalName', ''),
                        user.get('id', ''),
                        user.get('givenName', ''),
                        user.get('surname', ''),
                        user.get('jobTitle', ''),
                        user.get('department', ''),
                        user.get('officeLocation', ''),
                        ', '.join(user.get('businessPhones', [])),
                        user.get('mobilePhone', ''),
                        user.get('userType', ''),
                        'Sim' if user.get('accountEnabled') else 'Não',
                        user.get('createdDateTime', ''),
                        user.get('signInActivity', {}).get('lastSignInDateTime', ''),
                        user.get('preferredLanguage', ''),
                        user.get('managerDisplayName', ''),
                        user.get('managerMail', ''),
                        user.get('managerJobTitle', '')
                    ])

                # Escreve BOM + CSV no response
                response.write('\ufeff')  # UTF-8 BOM
                response.write(csv_buffer.getvalue())
                csv_buffer.close()

                return response


            elif users_list:
                context['users_list'] = users_list
                context['users_count'] = len(users_list)
                context['success'] = True
                messages.success(request, f'Encontrados {len(users_list)} usuários')
            else:
                context['error_message'] = error_msg or 'Nenhum usuário encontrado'
                messages.warning(request, 'Nenhum usuário encontrado')

        else:
            messages.error(request, 'Formulário inválido.')

    else:
        form = MS365ListUsersForm()

    context['form'] = form
    return render(request, 'suporte/m365/list_users.html', context)


@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
def m365_update_user(request):
    context = {
        'activegroup': 'suporte',
        'title': 'Microsoft 365 - Atualizar Usuário',
    }

    if request.method == 'GET' and 'tenant' in request.GET and 'usuario_alvo' in request.GET:
        tenant_id = request.GET.get('tenant')
        usuario_id = request.GET.get('usuario_alvo')

        try:
            tenant = MS365Tenant.objects.get(id=tenant_id)
            service = MS365ApiService(tenant)
            user_data, error_msg = service.get_user(
                usuario_id,
                requesting_user=request.user,
                ip_address=get_client_ip(request)
            )

            if user_data:
                initial_data = {
                    'tenant': tenant.id,
                    'usuario_alvo': user_data.get('userPrincipalName'),
                    'given_name': user_data.get('givenName'),
                    'surname': user_data.get('surname'),
                    'display_name': user_data.get('displayName'),
                    'job_title': user_data.get('jobTitle'),
                    'department': user_data.get('department'),
                    'office_location': user_data.get('officeLocation'),
                    'business_phone': ', '.join(user_data.get('businessPhones', [])),
                    'mobile_phone': user_data.get('mobilePhone'),
                }
                manager_data, _ = service.get_user_manager(usuario_id)
                if manager_data:
                    initial_data['manager_email'] = manager_data.get('mail') or manager_data.get('userPrincipalName')

                form = MS365UserUpdateForm(initial=initial_data)
                form.fields['usuario_alvo'].widget.attrs['readonly'] = True

            else:
                messages.error(request, error_msg or 'Usuário não encontrado')
                form = MS365UserUpdateForm()

        except Exception as e:
            messages.error(request, f'Erro ao buscar dados do usuário: {e}')
            form = MS365UserUpdateForm()

    elif request.method == 'POST':
        form = MS365UserUpdateForm(request.POST)
        if form.is_valid():
            tenant = form.cleaned_data['tenant']
            usuario_alvo = form.cleaned_data['usuario_alvo']

            # Mapeamento para PATCH
            updates = {}
            field_mapping = {
                'given_name': 'givenName',
                'surname': 'surname',
                'display_name': 'displayName',
                'job_title': 'jobTitle',
                'department': 'department',
                'office_location': 'officeLocation',
                'business_phone': 'businessPhones',
                'mobile_phone': 'mobilePhone'
            }

            for form_field, api_field in field_mapping.items():
                value = form.cleaned_data.get(form_field)
                if value:
                    updates[api_field] = [value] if form_field == 'business_phone' else value

            try:
                service = MS365ApiService(tenant)
                success, error_msg = service.update_user_profile(
                    usuario_alvo,
                    updates,
                    requesting_user=request.user,
                    ip_address=get_client_ip(request)
                )
                manager_email = form.cleaned_data.get('manager_email')
                if manager_email:
                    try:
                        success_mgr, error_mgr = service.set_user_manager(
                            usuario_alvo,
                            manager_email,
                            requesting_user=request.user,
                            ip_address=get_client_ip(request)
                        )
                        if not success_mgr:
                            messages.warning(request, f"Usuário atualizado, mas não foi possível alterar o gerente: {error_mgr}")
                    except Exception as e:
                        messages.warning(request, f"Erro ao atualizar gerente: {e}")

                if success:
                    display_name = updates.get('displayName') or usuario_alvo
                    messages.success(
                    request,
                    f"✅ Usuário {display_name} atualizado com sucesso!"
                    )
                    return redirect('m365_dashboard')
                else:
                    context['error_message'] = error_msg
                    messages.error(request, f'Erro: {error_msg}')

            except Exception as e:
                error_msg = f'Erro interno: {str(e)}'
                context['error_message'] = error_msg
                messages.error(request, error_msg)
        else:
            messages.error(request, 'Formulário inválido.')

    else:
        form = MS365UserUpdateForm()

    context['form'] = form
    return render(request, 'suporte/m365/update_user.html', context)

@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
def m365_manage_manager(request):
    """Gerenciar manager de usuário no M365"""
    context = {
        'activegroup': 'suporte',
        'title': 'Microsoft 365 - Gerenciar Manager',
    }
    
    if request.method == 'POST':
        form = MS365ManagerForm(request.POST)
        if form.is_valid():
            tenant = form.cleaned_data['tenant']
            usuario = form.cleaned_data['usuario']
            novo_manager = form.cleaned_data['novo_manager']
            
            try:
                service = MS365ApiService(tenant)
                
                # Primeiro, buscar manager atual
                current_manager, _ = service.get_user_manager(usuario)
                context['current_manager'] = current_manager
                
                # Se novo_manager foi fornecido, definir/alterar
                if novo_manager:
                    success, error_msg = service.set_user_manager(usuario, novo_manager)
                    if success:
                        context['success'] = True
                        context['action'] = 'set'
                        messages.success(request, f'Manager {novo_manager} definido para {usuario}')
                    else:
                        context['error_message'] = error_msg
                        messages.error(request, f'Erro ao definir manager: {error_msg}')
                
                # Se novo_manager está vazio, remover manager atual
                elif current_manager:
                    success, error_msg = service.remove_user_manager(usuario)
                    if success:
                        context['success'] = True
                        context['action'] = 'remove'
                        messages.success(request, f'Manager removido de {usuario}')
                    else:
                        context['error_message'] = error_msg
                        messages.error(request, f'Erro ao remover manager: {error_msg}')
                else:
                    messages.info(request, 'Usuário não possui manager para remover')
                    
            except Exception as e:
                error_msg = f'Erro interno: {str(e)}'
                context['error_message'] = error_msg
                messages.error(request, error_msg)
    else:
        form = MS365ManagerForm()
    
    context['form'] = form
    return render(request, 'suporte/m365/manage_manager.html', context)


# ==================== VIEWS PARA LOGS E RELATÓRIOS ====================

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
class MS365SearchLogListView(ListView):
    model = MS365UserSearchLog
    template_name = 'suporte/m365/search_logs.html'
    context_object_name = 'logs'
    paginate_by = 50
    
    def get_queryset(self):
        return MS365UserSearchLog.objects.select_related(
            'tenant', 'usuario_pesquisador'
        ).order_by('-data_pesquisa')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Microsoft 365 - Logs de Busca'
        return context


@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
class MS365UpdateLogListView(ListView):
    model = MS365UserUpdateLog
    template_name = 'suporte/m365/update_logs.html'
    context_object_name = 'logs'
    paginate_by = 50
    
    def get_queryset(self):
        return MS365UserUpdateLog.objects.select_related(
            'tenant', 'usuario_atualizador'
        ).order_by('-data_atualizacao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Microsoft 365 - Logs de Atualização'
        return context


# ==================== AJAX ENDPOINTS ====================

@login_required
@permission_required('global_permissions.combio_suporte')
def ajax_get_user_data(request):
    """Endpoint AJAX para buscar dados de usuário"""
    if request.method == 'POST':
        tenant_id = request.POST.get('tenant_id')
        user_id = request.POST.get('user_id')
        
        if not tenant_id or not user_id:
            return JsonResponse({'success': False, 'error': 'Parâmetros obrigatórios'})
        
        try:
            tenant = MS365Tenant.objects.get(pk=tenant_id, ativo=True)
            service = MS365ApiService(tenant)
            
            user_data, error_msg = service.get_user(
                user_id,
                requesting_user=request.user,
                ip_address=get_client_ip(request)
            )
            
            if user_data:
                return JsonResponse({
                    'success': True,
                    'user_data': {
                        'givenName': user_data.get('givenName', ''),
                        'surname': user_data.get('surname', ''),
                        'displayName': user_data.get('displayName', ''),
                        'jobTitle': user_data.get('jobTitle', ''),
                        'department': user_data.get('department', ''),
                        'officeLocation': user_data.get('officeLocation', ''),
                        'businessPhones': user_data.get('businessPhones', [])
                    }
                })
            else:
                return JsonResponse({'success': False, 'error': error_msg})
                
        except MS365Tenant.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tenant não encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


# Create your views here.
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
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
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
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
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
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
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
class UsuarioDesligamentoDelete(DeleteView):
    model = UsuarioDesligamento
    template_name = 'suporte/desligamento/usuario_desligamento_confirm_delete.html'
    success_url = reverse_lazy('usuario_desligamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activegroup'] = 'suporte'
        context['title'] = 'Confirmar Exclusão de Usuário'
        return context
    




@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
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

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
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
    
@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_suporte', login_url='erro_page'), name='dispatch')
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


@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
def m365_export_users_csv(request):
    """Exporta usuários do M365 para CSV com acentos e separador ;"""
    if request.method == 'POST':
        form = MS365ListUsersForm(request.POST)
        if form.is_valid():
            tenant = form.cleaned_data['tenant']
            filtro = form.cleaned_data['filtro']
            service = MS365ApiService(tenant)
            users_list, error_msg = service.list_users(filtro)

            if users_list:
                # Resposta e cabeçalhos
                response = HttpResponse(content_type='text/csv; charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="usuarios_m365.csv"'

                # Buffer intermediário para escrita CSV
                csv_buffer = StringIO()
                writer = csv.writer(csv_buffer, delimiter=';')  # <- ponto e vírgula

                # Cabeçalho
                writer.writerow([
                    'Nome Completo', 'Email', 'UPN', 'ID', 'Nome', 'Sobrenome',
                    'Cargo', 'Departamento', 'Localização', 'Telefone(s)',
                    'Celular', 'Tipo', 'Ativo', 'Criado em', 'Último Login', 'Idioma',
                    'Gerente', 'Email do Gerente', 'Cargo do Gerente'
                ])

                # Dados
                for user in users_list:
                    writer.writerow([
                        user.get('displayName', ''),
                        user.get('mail') or user.get('userPrincipalName'),
                        user.get('userPrincipalName', ''),
                        user.get('id', ''),
                        user.get('givenName', ''),
                        user.get('surname', ''),
                        user.get('jobTitle', ''),
                        user.get('department', ''),
                        user.get('officeLocation', ''),
                        ', '.join(user.get('businessPhones', [])),
                        user.get('mobilePhone', ''),
                        user.get('userType', ''),
                        'Sim' if user.get('accountEnabled') else 'Não',
                        user.get('createdDateTime', ''),
                        user.get('signInActivity', {}).get('lastSignInDateTime', ''),
                        user.get('preferredLanguage', ''),
                        user.get('managerDisplayName', ''),
                        user.get('managerMail', ''),
                        user.get('managerJobTitle', '')
                    ])

                # Escreve o BOM + conteúdo CSV no response
                response.write('\ufeff')  # UTF-8 BOM
                response.write(csv_buffer.getvalue())
                csv_buffer.close()
                return response
            else:
                messages.error(request, error_msg or 'Nenhum dado para exportar.')

    messages.error(request, 'Formulário inválido.')
    return redirect('m365_list_users')


@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
def m365_update_massivo(request):
    context = {
        'title': 'Atualização em Massa de Usuários M365',
        'activegroup': 'suporte',
    }

    if request.method == 'POST' and request.FILES.get('arquivo_csv'):
        arquivo = request.FILES['arquivo_csv']
        tenant_id = request.POST.get('tenant')
        tenant = get_object_or_404(MS365Tenant, id=tenant_id)
        service = MS365ApiService(tenant)

        decoded_file = arquivo.read().decode('utf-8-sig').splitlines()
        reader = csv.DictReader(decoded_file, delimiter=';')

        resultados = []
        for linha in reader:
            usuario = linha.get('Email') or linha.get('UPN')
            updates = {
                'displayName': linha.get('Nome Completo'),
                'givenName': linha.get('Nome'),
                'surname': linha.get('Sobrenome'),
                'jobTitle': linha.get('Cargo'),
                'department': linha.get('Departamento'),
                'officeLocation': linha.get('Localização'),
                'mobilePhone': linha.get('Celular'),
                'businessPhones': [linha.get('Telefone(s)')] if linha.get('Telefone(s)') else []
            }

            updates = {k: v for k, v in updates.items() if v}  # Remove vazios

            success, error = service.update_user_profile(
                usuario, updates,
                requesting_user=request.user,
                ip_address=get_client_ip(request)
            )

            # Atualizar gerente se fornecido
            gerente = linha.get('Email do Gerente')
            if gerente:
                service.set_user_manager(usuario, gerente)

            resultados.append({
                'usuario': usuario,
                'status': 'OK' if success else 'Erro',
                'mensagem': error if error else 'Atualizado com sucesso'
            })

        context['resultados'] = resultados

    context['form'] = MS365ListUsersForm()
    return render(request, 'suporte/m365/update_massivo.html', context)


@csrf_exempt
@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
def m365_update_usuario_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tenant_id = data.get('tenant')
            usuario = data.get('usuario')

            tenant = get_object_or_404(MS365Tenant, id=tenant_id)
            service = MS365ApiService(tenant)

            updates = data.get('updates', {})
            gerente = data.get('gerente')

            success, error = service.update_user_profile(usuario, updates)

            if gerente:
                service.set_user_manager(usuario, gerente)

            return JsonResponse({
                'usuario': usuario,
                'status': 'OK' if success else 'Erro',
                'mensagem': error if error else 'Atualizado com sucesso'
            })

        except Exception as e:
            return JsonResponse({'status': 'Erro', 'mensagem': str(e)}, status=400)



@csrf_exempt
@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
def m365_export_csv_api(request):
    tenant_id = request.GET.get('tenant')
    filtro = request.GET.get('filtro', '')

    if not tenant_id:
        return JsonResponse({'erro': 'Tenant não informado'}, status=400)

    try:
        tenant = MS365Tenant.objects.get(id=tenant_id)
    except MS365Tenant.DoesNotExist:
        return JsonResponse({'erro': 'Tenant inválido'}, status=400)

    service = MS365ApiService(tenant)
    users_list, error_msg = service.list_users(filtro)

    if not users_list:
        return JsonResponse({'erro': error_msg or 'Nenhum usuário encontrado'}, status=404)

    # Gerar CSV em memória
    from io import StringIO
    import csv

    buffer = StringIO()
    writer = csv.writer(buffer, delimiter=';')
    writer.writerow([
        'Nome Completo', 'Email', 'UPN', 'ID', 'Nome', 'Sobrenome',
        'Cargo', 'Departamento', 'Localização', 'Telefone(s)',
        'Celular', 'Tipo', 'Ativo', 'Criado em', 'Último Login', 'Idioma',
        'Gerente', 'Email do Gerente', 'Cargo do Gerente'
    ])

    for user in users_list:
        writer.writerow([
            user.get('displayName', ''),
            user.get('mail') or user.get('userPrincipalName'),
            user.get('userPrincipalName', ''),
            user.get('id', ''),
            user.get('givenName', ''),
            user.get('surname', ''),
            user.get('jobTitle', ''),
            user.get('department', ''),
            user.get('officeLocation', ''),
            ', '.join(user.get('businessPhones', [])),
            user.get('mobilePhone', ''),
            user.get('userType', ''),
            'Sim' if user.get('accountEnabled') else 'Não',
            user.get('createdDateTime', ''),
            user.get('signInActivity', {}).get('lastSignInDateTime', ''),
            user.get('preferredLanguage', ''),
            user.get('managerDisplayName', ''),
            user.get('managerMail', ''),
            user.get('managerJobTitle', '')
        ])

    csv_data = buffer.getvalue()
    buffer.close()

    return HttpResponse('\ufeff' + csv_data, content_type='text/csv; charset=utf-8')


def montar_arvore(usuario, todos):
    filhos = todos.filter(manager_email=usuario.email)
    return {
        'nome': usuario.display_name,
        'email': usuario.email,
        'cargo': usuario.job_title,
        'filhos': [montar_arvore(sub, todos) for sub in filhos]
    }

@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
def m365_organograma(request):
    todos = UsuarioM365.objects.all()
    raiz = todos.filter(email__iexact="paulo.skaf@combio.com.br").first()
    estrutura = montar_arvore(raiz, todos) if raiz else {}
    return JsonResponse(estrutura, safe=False)

@login_required(login_url='account_login')
@permission_required('global_permissions.combio_suporte', login_url='erro_page')
def organograma_interativo_view(request):
    context = {
        'title': 'Organograma Combio',
        'activegroup': 'Dashboard',
    }

    return render(request, 'suporte/m365/organograma_interativo.html', context)