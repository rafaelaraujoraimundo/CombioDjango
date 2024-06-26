from django import forms
from django.shortcuts import render
from .models import Arquivo, ArquivoAtivo, AtivoValores
from utils.forms import UploadArquivoAtivoForm, UploadArquivoForm, UploadAtivoPatrimonialForm
from menu.menu import GetGroup, GetMenu


def processar_arquivo(request):
    activegroup = 'utils'
    title = 'Upload de Arquivos para Processamento'
    arquivos = Arquivo.objects.all()
    if request.method == 'POST':
        form = UploadArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = form.save(commit=False)
            arquivo.usuario = request.user  # Associando o usuário logado ao arquivo
            arquivo.save()
            arquivo.processar_arquivo()  # Processa o arquivo original

            # Gera um link para o arquivo finalizado
            link_arquivo_finalizado = arquivo.arquivo_final.url

            # Retorne o link para o template ou faça o redirecionamento
            form = UploadArquivoForm()
            return render(request, 'utils/upload_arquivo.html', {'link_arquivo_finalizado': link_arquivo_finalizado, 'form': form, 'arquivos': arquivos, 'arquivo': arquivo})
    else:
        form = UploadArquivoForm()

    return render(request, 'utils/upload_arquivo.html', {'form': form, 'arquivos': arquivos, 'activegroup': activegroup, 'title': title})

def processar_arquivo_ativo(request):
    activegroup = 'utils'
    title = 'Upload de Arquivos para Processamento dos Ativos'
    arquivos = ArquivoAtivo.objects.all()
    if request.method == 'POST':
        form = UploadArquivoAtivoForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = form.save(commit=False)
            arquivo.usuario = request.user
            arquivo.save()
            arquivo.processar_arquivo()

            link_arquivo_finalizado = arquivo.arquivo_final.url
            form = UploadArquivoAtivoForm()  # Reset form
            return render(request, 'utils/upload_arquivo.html', {
                'link_arquivo_finalizado': link_arquivo_finalizado, 
                'form': form, 'arquivos': arquivos, 'arquivo': arquivo
            })
    else:
        form = UploadArquivoAtivoForm()

    return render(request, 'utils/upload_arquivo_ativo.html', {'form': form, 'arquivos': arquivos, 'activegroup': activegroup, 'title': title})

def processar_arquivo_ativo_valores(request):
    activegroup = 'utils'
    title = 'Upload de Arquivos para Processamento dos Ativos'
    arquivos = AtivoValores.objects.all()
    if request.method == 'POST':
        form = UploadAtivoPatrimonialForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = form.save(commit=False)
            arquivo.usuario = request.user
            arquivo.save()
            arquivo.processar_arquivo()

            link_arquivo_finalizado = arquivo.arquivo_final.url
            form = UploadAtivoPatrimonialForm()  # Reset form
            return render(request, 'utils/upload_arquivo_ativo_valores.html', {
                'link_arquivo_finalizado': link_arquivo_finalizado, 
                'form': form, 'arquivos': arquivos, 'arquivo': arquivo
            })
    else:
        form = UploadAtivoPatrimonialForm()

    return render(request, 'utils/upload_arquivo_ativo_valores.html', {'form': form, 'arquivos': arquivos, 'activegroup': activegroup, 'title': title})

