import json
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from decouple import config
from django.core.mail import send_mail
from django.conf import settings
from .models import WhatsAppMessage
from .utils import (
    consulta_titulos_api,
    consulta_titulos_pagos_api,
    cnpj_valido,
    data_valida,
    send_message
)

def consulta_contato_por_telefone_api(telefone):
    url = f"{config('DATASUL_HOST')}/esp/combio/v1/api_chatbot/piBuscaContatosPorTel/"
    payload = json.dumps({"tel": telefone})
    headers = {
        'Authorization': f'Basic {config("DATASUL_TOKEN")}',
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        return None
    data = response.json()
    if not data.get("items"):
        return None
    return data["items"][0]

def should_send_initial_message(wa_id):
    current_timestamp = timezone.now()
    last_message = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('-id').first()
    if last_message:
        time_diff = current_timestamp - last_message.timestamp_recebido
        return time_diff >= timedelta(minutes=2)
    return True

def get_cnpj_from_history(wa_id):
    mensagens = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('id')
    return next((m.message_body for m in mensagens if m.stage == 'consulta_externa_cnpj'), None)

def process_externo_message(wa_id, msg):
    message_id = msg.get('id')
    message_body = msg['text']['body'].strip()
    message_body_lower = message_body.lower()
    naive_timestamp = datetime.fromtimestamp(int(msg.get('timestamp')))
    timestamp = timezone.make_aware(naive_timestamp, timezone.get_default_timezone())

    last_message = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('-id').first()
    last_stage = last_message.stage if last_message else None

    if not last_stage or should_send_initial_message(wa_id) or message_body_lower in ['menu', 'inicial']:
        contato = consulta_contato_por_telefone_api(wa_id)
        if not contato:
            send_message(wa_id, "Telefone não encontrado. Entre em contato com o setor de Contas a Pagar para cadastro.")
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp,
                stage='final'
            )
            return

        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=contato['cnpj'],
            timestamp_recebido=timestamp,
            stage='consulta_externa_cnpj'
        )
        send_message(
            wa_id,
             f"Olá {contato['nome_contato']}!\n\nFORNECEDOR: *{contato['nome_emit']}*\nCNPJ: *{contato['cnpj']}*\n\nComo posso te ajudar hoje?\n\n"
            "1. Consulta de Pagamento\n"
            "2. Dúvidas sobre Contas a Pagar"
        )
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=message_body,
            timestamp_recebido=timestamp,
            stage='initial'
        )
        return

    current_stage = last_stage

    if current_stage == 'initial':
        if message_body_lower == '1':
            send_message(
                wa_id,
                "Você deseja consultar informações sobre um pagamento específico?\n"
                "Escolha uma opção:\n"
                "1.1) Previsão de Pagamento (Títulos em aberto)\n"
                "1.2) Composição de Notas de Pagamento (Títulos Pagos)"
            )
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp,
                stage='consulta_menu'
            )
        elif message_body_lower == '2':
            send_message(
                wa_id,
                "Como posso ajudar com suas dúvidas sobre contas a pagar?\n"
                "Escolha uma opção:\n"
                "2.1) Explicar as regras do Processo de Pagamento\n"
                "2.2) Ajustes ou Correções em Pagamento"
            )
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp,
                stage='duvidas_menu'
            )
        else:
            send_message(wa_id, "Opção inválida. Por favor, escolha uma opção válida.")
        return

    elif current_stage == 'consulta_menu':
        if message_body_lower in ['1', '1.1']:
            send_message(wa_id, "Consultando informações no sistema, aguarde....")
            cnpj = get_cnpj_from_history(wa_id)
            titulos = consulta_titulos_api(cnpj)

            if titulos:
                nome_emitente = titulos[0]['nome_fornecedor']
                mensagem = f"Previsão de Pagamento:\nConsulta realizada para o CNPJ/CPF {cnpj}\nFornecedor: *{nome_emitente}*\n\n"
                for titulo in titulos:
                    cod = titulo['cod_tit_ap']
                    parcela = titulo['cod_parcela']
                    emissao = datetime.strptime(titulo['dat_emis_docto'], '%Y-%m-%d').strftime('%d/%m/%Y')
                    vencimento = datetime.strptime(titulo['dat_vencto_tit_ap'], '%Y-%m-%d').strftime('%d/%m/%Y')
                    valor = f"R$ {titulo['val_sdo_tit_ap']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    mensagem += f"- NF {cod}-{parcela}, Emissão: {emissao}, Vencimento: {vencimento}, Valor: {valor}\n"
            else:
                mensagem = "Nenhuma nota em aberto encontrada para o CNPJ/CPF informado."
            send_message(wa_id, mensagem)
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=cnpj,
                timestamp_recebido=timestamp,
                stage='final'
            )
            send_message(wa_id, "Posso ajudar com mais alguma coisa? Digite 'menu' para voltar ao menu principal ou 'sair' para encerrar.")
            return

        elif message_body_lower in ['2', '1.2']:
            send_message(wa_id, "Passo 1/2:\nPor favor, informe a *data inicial* no formato dd/mm/yyyy:")
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp,
                stage='consulta_data_inicial'
            )
            return

    elif current_stage == 'consulta_data_inicial':
        if not data_valida(message_body):
            send_message(wa_id, "❌ Data inicial inválida. Use o formato dd/mm/yyyy, como 01/05/2025.")
            return
        send_message(wa_id, "Passo 2/2:\nPor favor, informe a *data final* no formato dd/mm/yyyy:")
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=message_body,
            timestamp_recebido=timestamp,
            stage='consulta_data_final'
        )
        return

    elif current_stage == 'consulta_data_final':
        if not data_valida(message_body):
            send_message(wa_id, "❌ Data final inválida. Use o formato dd/mm/yyyy, como 01/05/2025.")
            return

        mensagens = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('-id')
        cnpj = get_cnpj_from_history(wa_id)
        data_inicial = next((m.message_body for m in mensagens if m.stage == 'consulta_data_final'), 'N/A')
        data_final = message_body

        data_inicial_fmt = datetime.strptime(data_inicial, '%d/%m/%Y').strftime('%Y-%m-%d')
        data_final_fmt = datetime.strptime(data_final, '%d/%m/%Y').strftime('%Y-%m-%d')

        send_message(wa_id, "Consultando títulos pagos, aguarde...")

        titulos = consulta_titulos_pagos_api(cnpj, data_inicial_fmt, data_final_fmt)

        if titulos:
            nome_emitente = titulos[0]['nome_fornecedor']
            mensagem = (
                f"Composição de Notas de Pagamento (Títulos Pagos)\n\n"
                f"Fornecedor: *{nome_emitente}*\n"
                f"CNPJ: {cnpj}\n"
                f"Período: {data_inicial} a {data_final}\n\n"
                f"*{'NF':<10} {'Parcela':<8} {'Emissão':<12} {'Vencimento':<12} {'Pagamento':<12} {'Valor':<10}*\n"
            )
            for titulo in titulos:
                cod = titulo['cod_tit_ap']
                parcela = titulo['cod_parcela']
                emissao = datetime.strptime(titulo['dat_emis_docto'], '%Y-%m-%d').strftime('%d/%m/%Y')
                vencimento = datetime.strptime(titulo['dat_vencto_tit_ap'], '%Y-%m-%d').strftime('%d/%m/%Y')
                pagamento = datetime.strptime(titulo['data_pagamento'], '%Y-%m-%d').strftime('%d/%m/%Y')
                valor = f"R$ {titulo['val_sdo_tit_ap']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                linha = f"{cod:<10} {parcela:<8} {emissao:<12} {vencimento:<12} {pagamento:<12} {valor:<10}"
                mensagem += linha + '\n'
        else:
            mensagem = "Nenhum título pago encontrado no período informado."

        send_message(wa_id, mensagem)
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=data_final,
            timestamp_recebido=timestamp,
            stage='final'
        )
        send_message(wa_id, "Posso ajudar com mais alguma coisa? Digite 'menu' para voltar ou 'sair' para encerrar.")
        return

    elif current_stage == 'duvidas_menu':
        if message_body_lower in ['1', '2.1']:
            send_message(
                wa_id,
                "Regras do Processo de Pagamento:\n"
                "- Pagamentos programados após aprovação de Pedido e Recebimento físico e fiscal da NF\n"
                "- Pagamentos realizados nos dias 15 e 30 de cada mês\n"
                "- Pagamento via transferência bancária\n"
                "Para mais informações, entre em contato: contasapagar@combio.com.br"
            )
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp,
                stage='final'
            )
            send_message(wa_id, "Posso ajudar com mais alguma coisa? Digite 'menu' para voltar ou 'sair' para encerrar.")
        elif message_body_lower in ['2', '2.2']:
            send_message(
                wa_id,
                "Para ajustes ou correções, por favor, informe os detalhes do erro, incluindo CNPJ, NF e um contato para retorno."
            )
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp,
                stage='duvidas_ajustes'
            )
        else:
            send_message(wa_id, "Opção inválida. Por favor, escolha uma opção válida para dúvidas sobre contas a pagar.")
        return

    elif current_stage == 'duvidas_ajustes':
        user_details = message_body
        phone_number = wa_id
        subject = "Ajustes ou Correções em Pagamento"
        message_text = (
            f"Solicitação de Ajuste/Correção de Pagamento\n\n"
            f"Detalhes fornecidos pelo usuário:\n{user_details}\n\n"
            f"Telefone (WhatsApp) de contato: {phone_number}\n"
        )
        send_mail(
            subject=subject,
            message=message_text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["chatbot@combio.com.br"],
        )
        send_message(wa_id, "Recebemos sua solicitação de ajuste/correção. Em breve entraremos em contato.")
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=message_body,
            timestamp_recebido=timestamp,
            stage='final'
        )
        send_message(wa_id, "Posso ajudar com mais alguma coisa? Digite 'menu' para voltar ou 'sair' para encerrar.")
        return

    elif current_stage == 'final':
        if message_body_lower in ['menu', 'sim']:
            send_message(
                wa_id,
                "Olá! Como posso te ajudar hoje?\n"
                "1. Consulta de Pagamento\n"
                "2. Dúvidas sobre Contas a Pagar"
            )
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp,
                stage='initial'
            )
        else:
            send_message(
                wa_id,
                "Conversa finalizada. Iniciando novamente...\n"
                "1. Consulta de Pagamento\n"
                "2. Dúvidas sobre Contas a Pagar"
            )
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp,
                stage='initial'
            )
        return
