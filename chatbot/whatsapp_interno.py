import json
from datetime import datetime, timedelta
from django.utils import timezone
from decouple import config
from chatbot.utils import consulta_titulos_api_cnpj
from .models import WhatsAppMessage, Contatos
import requests

def process_internal_message(wa_id, msg):
    message_id = msg.get('id')
    message_body = msg['text']['body'].strip().lower()
    naive_timestamp_recebido = datetime.fromtimestamp(int(msg.get('timestamp')))
    timestamp_recebido = timezone.make_aware(naive_timestamp_recebido, timezone.get_default_timezone())

    last_message = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('-id').first()

    if last_message and should_send_initial_message(wa_id):
        last_message = None  # Resetting to start from the menu

    if last_message and last_message.stage == 'internal_menu':
        if message_body == '1':
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp_recebido,
                stage='collect_cnpj'
            )
            send_message(wa_id, "Por favor, digite o número do CNPJ:")
        elif message_body == '2':
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp_recebido,
                stage='status_menu'
            )
            send_message(wa_id, "Selecione o tipo de Status:\n*1*- Pedidos de Compra\n*2*- Solicitações\n*3*- Ordem de Compra\nOu digite *SAIR* para voltar ao menu inicial\n")
        else:
            send_message(wa_id, "Opção inválida. Por favor escolha uma opção válida:\n*1-* Financeiro\n*2-* Status de Solicitações, Pedidos e ou Ordem de Compra")
            return
    elif last_message and last_message.stage == 'collect_cnpj':
        if message_body.isdigit() and len(message_body) == 14:
            cnpj = message_body.zfill(14)
            titulos = consulta_titulos_api_cnpj(cnpj)
            if titulos:
                nome_emit = titulos[0]['nome_fornecedor']
                mensagem = f"Empresa: *{nome_emit}*\n\n"
                for titulo in titulos:
                    cod_tit_ap = str(titulo['cod_tit_ap'])
                    cod_parcela = str(titulo['cod_parcela'])
                    dat_emis_docto = datetime.strptime(titulo['dat_emis_docto'], '%Y-%m-%d').strftime('%d/%m/%Y') if titulo['dat_emis_docto'] else 'N/A'
                    dat_vencto_tit_ap = datetime.strptime(titulo['dat_vencto_tit_ap'], '%Y-%m-%d').strftime('%d/%m/%Y') if titulo['dat_vencto_tit_ap'] else 'N/A'
                    val_sdo_tit_ap = f"{titulo['val_sdo_tit_ap']:,.2f}" if titulo['val_sdo_tit_ap'] else '0.00'
                    
                    mensagem += (
                        f"*NF*: {cod_tit_ap}, "
                        f"*Emissão*: {dat_emis_docto}, "
                        f"*Vencimento*: {dat_vencto_tit_ap}, "
                        f"*Valor Saldo*: R$ {val_sdo_tit_ap}\n"
                    )
                mensagem += (
                    f"\n\n*Politica interna de Pagamentos:* \n"
                    f"Os títulos com data de vencimento entre os dias 1 e 15 serão pagos no dia 15 do mês atual.\n"
                    f"Os títulos com data de vencimento entre os dias 16 e 31 serão pagos no último dia do mês atual.\n"
                    )
                send_message(wa_id, mensagem)
            else:
                send_message(wa_id, "Nenhum título encontrado para o CNPJ fornecido.")
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp_recebido,
                stage='internal_menu'  # Finalizando a interação e retornando ao menu inicial
            )
            send_message(wa_id, "Obrigado por utilizar nosso ChatBot.")
        else:
            send_message(wa_id, "CNPJ inválido. Favor digitar um CNPJ válido ou digite SAIR para finalizar.")
    elif last_message and last_message.stage == 'status_menu':
        if message_body == '1':
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp_recebido,
                stage='consulta_pedido'
            )
            send_message(wa_id, "Por favor, digite o número do pedido de compra:")
        elif message_body == '2':
            send_message(wa_id, "Você selecionou 'Solicitações'. Em breve implementaremos essa funcionalidade.")
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp_recebido,
                stage='internal_menu'  # Finalizando a interação e retornando ao menu inicial
            )
        elif message_body == '3':
            send_message(wa_id, "Você selecionou 'Ordem de Compra'. Em breve implementaremos essa funcionalidade.")
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp_recebido,
                stage='internal_menu'  # Finalizando a interação e retornando ao menu inicial
            )
        elif message_body.lower() == 'sair':
            send_message(wa_id, "Obrigado por utilizar o ChatCombio. Você será redirecionado ao menu inicial.")
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp_recebido,
                stage='internal_menu'  # Redireciona para o menu inicial
            )
            send_message(wa_id, "Bem vindos ao ChatBot da Combio.\nPor favor escolha uma opção:\n*1-* Financeiro\n*2-* Status de Solicitações, Pedidos e ou Ordem de Compra\n")
        else:
            send_message(wa_id, "Opção inválida. Por favor, escolha uma opção válida ou digite SAIR para voltar ao menu inicial.")
            return
    elif last_message and last_message.stage == 'consulta_pedido':
        numero_pedido = message_body
        pedido_data = consulta_pedido_api(numero_pedido)
       
        if pedido_data and 'data' in pedido_data:
            send_message(wa_id,"Processando pedidos....")
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
            codigo_emitente = pedido.get('cod-emitente', 'N/A')

            mensagem = (
                f"\n *Filial:* {end_entrega} - "
                f"*Pedido:* {numero_pedido}\n"
                f"Nome Emitente: {nome_emit}\n"
                f"MLA Aprovação: {responsavel}\n"
                f"Valor Total: R$ {float(valor_total):,.2f}\n"
                f"Aprovado: {'SIM' if aprovado else 'NÃO'} - "
                f"Emergencial: {'SIM' if emergencial else 'NÃO'}\n"
            )
            send_message(wa_id,"Processando Recebimentos....")
            mensagem +=  f"\n*Recebimentos:*\n"
            for receb in ttRecebimento:
                data_movto = datetime.fromtimestamp(receb.get('data-movto', 0) / 1000).strftime('%d/%m/%Y')
                cSitErp = consulta_cSitErp(receb.get('numero-nota'), pedido.get('cod-emitente'))
                mensagem += (
                    f"- Data Movimento: {data_movto}, "
                    f"Nota: {receb.get('numero-nota', 'N/A')}, "
                    f"Qtd Rec.: {receb.get('quant-receb', 'N/A')}, "
                    f"Preço Unitário: R$ {float(receb.get('pre-unit-for', 0)):,.2f}\n"
                    f"     Situação ERP: {cSitErp}"
                )
                titulo_info = consulta_titulo_recebimento(codigo_emitente, receb.get('numero-nota', 'N/A'))
                if titulo_info:
                    
                    send_message(wa_id,"Processando títulos....")
                    mensagem += (
                     f"     Título: {titulo_info['cod_tit_ap']}, "
                     f"Emissão: {titulo_info['dat_emis_docto']}, "
                     f"Status: {titulo_info['status_pagamento']}"
                     )
                    if titulo_info['data_pagamento']:
                        mensagem += f" Data Pago: {titulo_info['data_pagamento']}"
                    mensagem += ("\n")
            mensagem += "\n*Ordens de Compra:*\n"
            send_message(wa_id,"Processando Ordens de Compras....")
            for i, ordem in enumerate(ttOrdemCompra):
                if i < 5:
                    mensagem += (
                        f"- OC: {ordem.get('numero-ordem', 'N/A')}, "
                        f"Item: {ordem.get('it-codigo', 'N/A')}, "
                        f"Descrição: {ordem.get('it-codigo-desc', 'N/A')}, "
                        f"Qtd Solicitada: {ordem.get('qt-solic', 'N/A')}, "
                        f"Preço Unitário: R$ {float(ordem.get('preco-unit', 0)):,.2f}\n"
                    )
                else:
                    mensagem += "...\n"
                    break
            
            if not aprovado:
                send_message(wa_id,"Processando Aprovações....")
                aprovacao_data = consulta_aprovacao_pedido(numero_pedido)
                if aprovacao_data and 'items' in aprovacao_data:
                    mensagem += "\nAprovações:"
                    for aprov in aprovacao_data['items']:
                        dt_geracao = aprov.get('dt_geracao', 'N/A')
                        cod_usuar = aprov.get('cod_usuar', 'N/A')
                        nome_usuar = aprov.get('nome_usuar', 'N/A')
                        ind_situacao = aprov.get('ind_situacao', 0)
                        dt_aprova = aprov.get('dt_aprova', 'N/A')

                        situacao = "Pendente" if ind_situacao == 1 else "Aprovado"
                        mensagem += (
                            f"\n- Situação: *{situacao.upper()}*, "
                            f"Data Geração: {dt_geracao}, "
                            f"Usuário: {cod_usuar}, "
                            f"Nome: {nome_usuar}, "
                        )
                        if dt_aprova:
                            data_formatada = datetime.strptime(dt_aprova, '%Y-%m-%d').strftime('%d/%m/%Y')
                            mensagem += f"Data Aprovação: {data_formatada}"
                        
            send_message(wa_id, mensagem + "\n\nObrigado por utilizar nosso ChatBot.\n")
        else:
            send_message(wa_id, "Pedido não encontrado ou número de pedido inválido.\n")
        
        # Finaliza a interação, voltando ao menu inicial
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=message_body,
            timestamp_recebido=timestamp_recebido,
            stage='internal_menu'  # Finalizando a interação e retornando ao menu inicial
        )
    else:
        # Apresenta o menu inicial para contatos internos
        response_message = (
            "Bem vindos ao ChatBot da Combio.\n"
            "Por favor escolha uma opção:\n"
            "*1-* Financeiro\n"
            "*2-* Status de Solicitações, Pedidos e ou Ordem de Compra\n"
        )
        send_message(wa_id, response_message)
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=message_body,
            timestamp_recebido=timestamp_recebido,
            stage='internal_menu'
        )

def should_send_initial_message(wa_id):
    current_timestamp = timezone.now()
    last_message = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('-id').first()
    if last_message:
        time_diff = current_timestamp - last_message.timestamp_recebido
        return time_diff >= timedelta(minutes=2)
    return True

def send_message(to, text):
    token = config('TOKEN_WHATSAPP')
    url = f"https://graph.facebook.com/v20.0/{config('WHATSAPP_ID')}/messages"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    data = {
        'messaging_product': 'whatsapp',
        'to': to,
        'type': 'text',
        'text': {'preview_url': False, 'body': text}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

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

def consulta_cSitErp(numero_nota, cod_emitente):
    url = f"https://combio-dts-prod-prime.totvscloud.com.br/dts/datasul-rest/resources/prg/gs/v1/esrfapi001?lastRecord=0&ide_nNF_ini={numero_nota}&ide_nNF_fim={numero_nota}&erp_cod_emitente_ini={cod_emitente}&erp_cod_emitente_fim={cod_emitente}&tp_data=1&dt_ini=2000-07-01&dt_fim=2099-07-20&page_size=100"
    headers = {
        'Authorization': 'Basic ' + config('DATASUL_TOKEN'),
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            return data['items'][0].get('cSitErp', 'Situação não encontrada')
    return 'Situação não encontrada'


def consulta_titulo_recebimento(codigo_emitente, numero_nota):
    url = "https://combio-dts-prod-prime.totvscloud.com.br/dts/datasul-rest/resources/prg/esp/combio/v1/api_chatbot/piBuscatitulosnfcnpj/"
    
    payload = json.dumps({
        "codigo": codigo_emitente,
        "nota": numero_nota
    })
    
    headers = {
        'Authorization': 'Basic ' + config('DATASUL_TOKEN'),
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        if data['total'] > 0:
            item = data['items'][0]
            return {
                "cod_tit_ap": item.get('cod_tit_ap', 'N/A'),
                "dat_emis_docto": item.get('dat_emis_docto', 'N/A'),
                "status_pagamento": item.get('status_pagamento', 'N/A'),
                "data_pagamento": item.get('data_pagamento', 'N/A') if item.get('status_pagamento') == 'PAGO' else None
            }
    return None