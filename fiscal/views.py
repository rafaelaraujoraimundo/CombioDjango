import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import UploadSPEDForm
from .models import UnificacaoSPED
from fiscal.unificar_sped import unificar_arquivos_sped, escrever_arquivo_sped

@login_required
def unificar_sped(request):
    if request.method == 'POST':
        form = UploadSPEDForm(request.POST, request.FILES)
        if form.is_valid():
            principal = form.cleaned_data['arquivo_principal']
            secundarios = form.cleaned_data['arquivos_secundarios']  # lista de arquivos

            # Pasta temporária para salvar arquivos enviados
            pasta_temp = os.path.join(settings.MEDIA_ROOT, 'sped_unificador', 'temp')
            os.makedirs(pasta_temp, exist_ok=True)

            # Salvar arquivo principal
            caminho_principal = os.path.join(pasta_temp, principal.name)
            with open(caminho_principal, 'wb+') as f:
                for chunk in principal.chunks():
                    f.write(chunk)

            # Salvar arquivos secundários
            caminhos_secundarios = []
            nomes_secundarios = []

            for arquivo in secundarios:
                caminho = os.path.join(pasta_temp, arquivo.name)
                with open(caminho, 'wb+') as f:
                    for chunk in arquivo.chunks():
                        f.write(chunk)
                caminhos_secundarios.append(caminho)
                nomes_secundarios.append(arquivo.name)

            # Unificar usando a função existente
            todos_arquivos = [caminho_principal] + caminhos_secundarios
            linhas_unificadas = unificar_arquivos_sped(todos_arquivos)

            # Caminho para salvar o resultado
            resultado_path = os.path.join(settings.MEDIA_ROOT, 'sped_unificador', 'resultados', f'resultado_{principal.name}')
            os.makedirs(os.path.dirname(resultado_path), exist_ok=True)
            escrever_arquivo_sped(resultado_path, linhas_unificadas)

            # Salvar no banco apenas os nomes
            UnificacaoSPED.objects.create(
                usuario=request.user,
                nome_arquivo_principal=principal.name,
                nomes_arquivos_secundarios=", ".join(nomes_secundarios),
                arquivo_resultado=f'sped_unificador/resultados/resultado_{principal.name}'
            )

            # Redireciona para GET limpo após POST (PRG pattern)
            return redirect('sped_unificador')

    else:
        form = UploadSPEDForm()

    # Histórico das últimas unificações do usuário logado
    historico = UnificacaoSPED.objects.filter(usuario=request.user).order_by('-data_processo')[:10]
    
    return render(request, 'fiscal/sped_unificador/upload.html', {
        'form': form,
        'historico': historico,
        'title': 'Unificação SPED',
        'activegroup': 'comunicacao',
    })
