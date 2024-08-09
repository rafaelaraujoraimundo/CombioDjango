import re
import requests
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Interaction
from .utils import consulta_titulos_api_cnpj
from datetime import datetime
from decouple import config

def consulta_pedido_api(numero_pedido):
    url = f"{config('DATASUL_HOST_PADRAO')}/api/ccp/ccapi351/purchaseOrderDetails?pCurrency=0&pNrPedido={numero_pedido}"
    headers = {
        'Authorization': 'Basic ' + config('DATASUL_TOKEN'),
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def consulta_aprovacao_pedido(numero_pedido):
    url = f"{config('DATASUL_HOST_PADRAO')}/api_mla/aprovacaopedidos/"
    payload = json.dumps({"pedido": numero_pedido})
    headers = {
        'Authorization': 'Basic ' + config('DATASUL_TOKEN'),
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    return None

@login_required
def send_message_chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        user = request.user

        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key
        response = "Comando não reconhecido. Por favor, tente novamente.<br>"

        interaction, created = Interaction.objects.get_or_create(
            user=user,
            session_key=session_key,
            defaults={'stage': 'inicio'}
        )

        if interaction.stage == 'inicio':
            if user_message == '1':
                interaction.stage = 'solicitar_cnpj'
                interaction.save()
                response = "Por favor, digite o número do CNPJ:<br>"
            elif user_message == '2':
                interaction.stage = 'status'
                interaction.save()
                response = ("Selecione o tipo de Status:<br>"
                            "1- Pedidos de Compra<br>"
                            "2- Solicitações<br>"
                            "3- Ordem de Compra<br>"
                            "Ou digite SAIR para voltar ao menu inicial<br>")
            else:
                response = ("Bem vindos ao ChatBot da Combio.<br>"
                            "Por favor escolha uma opção<br>"
                            "1- Financeiro<br>"
                            "2- Status de Solicitações, Pedidos e ou Ordem de Compra<br>")

        elif interaction.stage == 'solicitar_cnpj':
            if user_message.lower() == 'sair':
                interaction.stage = 'inicio'
                interaction.save()
                response = ("Bem vindos ao ChatBot da Combio.<br>"
                            "Por favor escolha uma opção<br>"
                            "1- Financeiro<br>"
                            "2- Status de Solicitações, Pedidos e ou Ordem de Compra<br>")
            elif re.match(r'^\d{14}$', user_message):
                interaction.cnpj = user_message

                titulos = consulta_titulos_api_cnpj(user_message)
                if titulos:
                    nome_emit = titulos[0]["nome_fornecedor"]
                    mensagem = f"Empresa: <strong>{nome_emit}</strong><br><br>"
                    for titulo in titulos:
                        cod_tit_ap = str(titulo['cod_tit_ap'])
                        cod_parcela = str(titulo['cod_parcela'])
                        dat_emis_docto = datetime.strptime(titulo['dat_emis_docto'], '%Y-%m-%d').strftime('%d/%m/%Y') if titulo['dat_emis_docto'] else 'N/A'
                        dat_vencto_tit_ap = datetime.strptime(titulo['dat_vencto_tit_ap'], '%Y-%m-%d').strftime('%d/%m/%Y') if titulo['dat_vencto_tit_ap'] else 'N/A'
                        val_sdo_tit_ap = f"{titulo['val_sdo_tit_ap']:,.2f}" if titulo['val_sdo_tit_ap'] else '0.00'

                        mensagem += (
                            f"\n"
                            f"<strong>NF</strong>: {cod_tit_ap}, "
                            f"<strong>Emissão</strong>: {dat_emis_docto}, "
                            f"<strong>Vencimento</strong>: {dat_vencto_tit_ap}, "
                            f"<strong>Valor Saldo</strong>: {val_sdo_tit_ap}<br>"
                        )
                    mensagem += (
                        f"<br><strong>Política interna de Pagamentos:</strong><br>"
                        f"Os títulos com data de vencimento entre os dias 1 e 15 serão pagos no dia 15 do mês atual.<br>"
                        f"Os títulos com data de vencimento entre os dias 16 e 31 serão pagos no último dia do mês atual.<br>"
                    )
                else:
                    mensagem = "Nenhum título encontrado para o CNPJ fornecido.<br>"

                response = mensagem + "<br><br>Obrigado por utilizar nosso ChatBot. Você será redirecionado ao início.<br>"
                interaction.stage = 'inicio'
                interaction.save()
            else:
                response = "CNPJ inválido. Favor digitar apenas números ou digite SAIR para voltar ao menu principal"

        elif interaction.stage == 'status':
            if user_message.lower() == 'sair':
                interaction.stage = 'inicio'
                interaction.save()
                response = ("Bem vindos ao ChatBot da Combio.<br>"
                            "Por favor escolha uma opção<br>"
                            "1- Financeiro<br>"
                            "2- Status de Solicitações, Pedidos e ou Ordem de Compra<br>")
            elif user_message in ['1', '2', '3']:
                if user_message == '1':
                    interaction.stage = 'consulta_pedido'
                    interaction.save()
                    response = "Por favor, digite o número do pedido de compra:<br>"
                elif user_message in ['2', '3']:  # Opções 2 e 3 para "Solicitações" e "Ordem de Compra"
                    response = "Modulo não implantado<br><br>Obrigado por utilizar nosso ChatBot.<br>"
                    interaction.stage = 'inicio'
                    interaction.save()
                else:
                    interaction.stage = 'inicio'
                    interaction.save()
                    response = "Processando sua solicitação..."

        elif interaction.stage == 'consulta_pedido':
            if user_message.lower() == 'sair':
                interaction.stage = 'inicio'
                interaction.save()
                response = ("Bem vindos ao ChatBot da Combio.<br>"
                            "Por favor escolha uma opção<br>"
                            "1- Financeiro<br>"
                            "2- Status de Solicitações, Pedidos e ou Ordem de Compra<br>")
            else:
                numero_pedido = user_message
                pedido_data = consulta_pedido_api(numero_pedido)
                if pedido_data and 'data' in pedido_data:
                    pedido = pedido_data['data'][0]
                    nome_emit = pedido.get('nome-emit', 'N/A')
                    ttRecebimento = pedido.get('ttRecebimento', [])
                    responsavel = pedido.get('responsavel', 'N/A')
                    valor_total = pedido.get('valor-total', 'N/A')
                    aprov_total = pedido.get('aprov-total', 'N/A')
                    emergencial = pedido.get('emergencial', 'N/A')
                    aprovado = pedido.get('aprovado', 'N/A')
                    ttOrdemCompra = pedido.get('ttOrdemCompra', [])
                    end_entrega = pedido.get('end-entrega', 'N/A')

                    mensagem = (
                        f"<br> Filial: {end_entrega} - "
                        f"Pedido: {numero_pedido}<br>"
                        f"Nome Emitente: {nome_emit}<br>"
                        f"MLA Aprovação: {responsavel}<br>"
                        f"Valor Total: R$ {float(valor_total):,.2f}<br>"
                        f"Aprovado: {'SIM' if aprovado else 'NÃO'} - "
                        f"Emergencial: {'SIM' if emergencial else 'NÃO'}<br>"
                        
                        f"<br>Recebimentos:<br>"
                    )

                    for receb in ttRecebimento:
                        data_movto = datetime.fromtimestamp(receb.get('data-movto', 0) / 1000).strftime('%d/%m/%Y')
                        mensagem += (
                            f"- Data Movimento: {data_movto}, "
                            f"Nota: {receb.get('numero-nota', 'N/A')}, "
                            f"Quantidade Recebida: {receb.get('quant-receb', 'N/A')}, "
                            f"Preço Unitário: R$ {float(receb.get('pre-unit-for', 0)):,.2f}<br>"
                        )

                    mensagem += "<br>Ordens de Compra:<br>"

                    for i, ordem in enumerate(ttOrdemCompra):
                        if i < 5:
                            mensagem += (
                                f"- Ordem Número: {ordem.get('numero-ordem', 'N/A')}, "
                                f"Cod. Item: {ordem.get('it-codigo', 'N/A')}, "
                                f"Descrição: {ordem.get('it-codigo-desc', 'N/A')}, "
                                f"Quantidade Solicitada: {ordem.get('qt-solic', 'N/A')}, "
                                f"Preço Unitário: R$ {float(ordem.get('preco-unit', 0)):,.2f}<br>"
                                                       )
                        else:
                            mensagem += "...<br>"
                            break
                    
                    if not aprovado:
                        
                        aprovacao_data = consulta_aprovacao_pedido(numero_pedido)
                        if aprovacao_data and 'items' in aprovacao_data:
                            mensagem += "<br>Aprovações:"
                            for aprov in aprovacao_data['items']:
                                dt_geracao = aprov.get('dt_geracao', 'N/A')
                                cod_usuar = aprov.get('cod_usuar', 'N/A')
                                nome_usuar = aprov.get('nome_usuar', 'N/A')
                                ind_situacao = aprov.get('ind_situacao', 0)
                                dt_aprova = aprov.get('dt_aprova', 'N/A')

                                situacao = "Pendente" if ind_situacao == 1 else "Aprovado"
                                mensagem += (
                                    f"<br>- Situação: {situacao.upper()}, "
                                    f"Data Geração: {dt_geracao}, "
                                    f"Usuário: {cod_usuar}, "
                                    f"Nome: {nome_usuar}, "
                                    )
                                if dt_aprova:
                                    data_formatada = datetime.strptime(dt_aprova, '%Y-%m-%d').strftime('%d/%m/%Y')
                                    mensagem += f"Data Aprovação: {data_formatada}"
                                

                    response = mensagem + "<br><br>Obrigado por utilizar nosso ChatBot.<br>"
                else:
                    response = "Pedido não encontrado ou número de pedido inválido.<br>"

                interaction.stage = 'inicio'
                interaction.save()

        else:
            # Qualquer tecla pressionada após a interação
            response = ("Bem vindos ao ChatBot da Combio.<br>"
                        "Por favor escolha uma opção<br>"
                        "1- Financeiro<br>"
                        "2- Status de Solicitações, Pedidos e ou Ordem de Compra<br>")
            interaction.stage = 'inicio'
            interaction.save()

        return JsonResponse({'response': response})


def consulta_aprovacao_pedido(numero_pedido):
    url = f"{config('DATASUL_HOST')}/esp/combio/v1/api_mla/aprovacaopedidos/"
    payload = json.dumps({"pedido": numero_pedido})
    headers = {
        'Authorization': 'Basic ' + config('DATASUL_TOKEN'),
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    return None
