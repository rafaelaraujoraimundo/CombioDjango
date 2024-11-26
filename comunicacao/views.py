from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ConfiguracaoForm, SetorEmailForm
from .models import Configuracao, SetorEmail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from PIL import Image, ImageOps
from django.http import JsonResponse
from io import BytesIO
import base64
from django.conf import settings
import os

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


@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_comunicacao', login_url='erro_page'), name='dispatch')
class SetorEmailListView(ListView):
    model = SetorEmail
    template_name = 'comunicacao/setoremail/setor_email_list.html'
    context_object_name = 'setoremails'

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_comunicacao', login_url='erro_page'), name='dispatch')
class SetorEmailCreateView(CreateView):
    model = SetorEmail
    form_class = SetorEmailForm
    template_name = 'comunicacao/setoremail/setor_email_form.html'
    success_url = reverse_lazy('setoremail_list')

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_comunicacao', login_url='erro_page'), name='dispatch')
class SetorEmailUpdateView(UpdateView):
    model = SetorEmail
    form_class = SetorEmailForm
    template_name = 'comunicacao/setoremail/setor_email_form.html'
    success_url = reverse_lazy('setoremail_list')

@method_decorator(login_required(login_url='account_login'), name='dispatch')
@method_decorator(permission_required('global_permissions.combio_comunicacao', login_url='erro_page'), name='dispatch')
class SetorEmailDeleteView(DeleteView):
    model = SetorEmail
    template_name = 'comunicacao/setoremail/setor_email_confirm_delete.html'
    success_url = reverse_lazy('setoremail_list')


from django.shortcuts import render
from django.http import JsonResponse
from .forms import SignatureForm

def generate_signature(request):
    if request.method == 'POST':
        form = SignatureForm(request.POST)
        if form.is_valid():
            context = {
                'nome': form.cleaned_data['nome_completo'],
                'email': form.cleaned_data['email'],
                'telefone': form.cleaned_data['telefone'],
                'setor': form.cleaned_data['setor_email'].nome
            }
            return JsonResponse(context)
    else:
        form = SignatureForm()
    
    return render(request, 'comunicacao/generate_signature/generate_signature.html', {'form': form})


def combined_view(request):
    if request.method == 'POST':
        form = SignatureForm(request.POST, request.FILES)
        if form.is_valid():
            context = {
                'nome': form.cleaned_data['nome_completo'],
                'email': form.cleaned_data['email'],
                'telefone': form.cleaned_data['telefone'],
                'setor': form.cleaned_data['setor_email'].nome
            }

            # Processa a imagem, se disponível
            if 'uploadImage' in request.FILES:
                user_image = Image.open(request.FILES['uploadImage']).convert('RGBA')

                # Define o caminho para a imagem de fundo dentro dos arquivos estáticos
                background_image_path = os.path.join(settings.STATIC_ROOT, 'images', 'email_background.png')
                background_image = Image.open(background_image_path).convert('RGBA')

                # Centraliza a imagem do usuário na imagem de fundo
                # Assume que x, y são calculados ou fixos
                x = (background_image.width - user_image.width) // 2
                y = (background_image.height - user_image.height) // 2

                # Cria uma nova imagem em RGBA para compor o resultado final
                new_image = Image.new('RGBA', background_image.size)
                new_image.paste(background_image, (0, 0))
                new_image.paste(user_image, (x, y), user_image)

                buffer = BytesIO()
                new_image.save(buffer, format='PNG')
                image_png = buffer.getvalue()
                image_base64 = base64.b64encode(image_png)

                context['image'] = image_base64.decode('utf-8')
                return JsonResponse(context)

        return render(request, 'comunicacao/generate_signature/generate_signature.html', {'form': form})
    else:
        form = SignatureForm()
        return render(request, 'comunicacao/generate_signature/generate_signature.html', {'form': form})
    


def process_image(request):
    if request.method == 'POST':
        form = SignatureForm(request.POST, request.FILES)
        if form.is_valid():
            # Dados do formulário
            nome = form.cleaned_data['nome_completo']
            email = form.cleaned_data['email']
            telefone = form.cleaned_data['telefone']
            setor = form.cleaned_data['setor_email'].nome  # Ajuste conforme seu modelo

            context = {
                'nome': nome,
                'email': email,
                'telefone': telefone,
                'setor': setor
            }

            # Processa a imagem, se disponível
            if 'uploadImage' in request.FILES:
                user_image = Image.open(request.FILES['uploadImage']).convert('RGBA')
                background_image_path = os.path.join(settings.STATIC_ROOT, 'images', 'email_background.png')
                background_image = Image.open(background_image_path).convert('RGBA')

                # Centralizar a imagem do usuário na imagem de fundo
                x = (background_image.width - user_image.width) // 2
                y = (background_image.height - user_image.height) // 2

                background_image.paste(user_image, (x, y), user_image)

                # Converter para base64 para enviar como JSON
                buffer = BytesIO()
                background_image.save(buffer, format='PNG')
                image_png = buffer.getvalue()
                image_base64 = base64.b64encode(image_png).decode('utf-8')

                context['image'] = image_base64

            return JsonResponse(context)

        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)