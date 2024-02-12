from django import forms
from django.shortcuts import render
from .models import Arquivo
from utils.forms import UploadArquivoForm
from menu.menu import GetGroup, GetMenu


def processar_arquivo(request):
    activegroup = 'utils'
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

    return render(request, 'utils/upload_arquivo.html', {'form': form, 'arquivos': arquivos, 'activegroup': activegroup})
