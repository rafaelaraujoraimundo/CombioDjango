import json
from datetime import datetime, timedelta
from django.utils import timezone
from decouple import config
from .models import WhatsAppMessage
import requests
from django.core.mail import send_mail
from django.conf import settings

def process_combio_message(wa_id, msg):
    message_id = msg.get('id')
    message_body = msg['text']['body'].strip()
    message_body_lower = message_body.lower()  # Para facilitar comparações
    naive_timestamp = datetime.fromtimestamp(int(msg.get('timestamp')))
    timestamp = timezone.make_aware(naive_timestamp, timezone.get_default_timezone())

    # Consulta a última mensagem do usuário
    last_message = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('-id').first()
    last_stage = last_message.stage if last_message else None

    # 1) Se o usuário digitar "sair", finaliza a conversa imediatamente
    if message_body_lower == 'sair':
        send_message(wa_id, "Obrigado por utilizar nosso ChatBot. Até logo!")
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=message_body,
            timestamp_recebido=timestamp,
            stage='final'
        )
        return

    # 2) Se não houver histórico, ou se já estiver no estágio 'final',
    #    ou se o último registro foi há mais de 2 minutos,
    #    ou se o usuário digitou 'menu'/'inicial',
    #    então recomeça a conversa mostrando o menu inicial.
    if (
        not last_message or
        last_stage == 'final' or
        should_send_initial_message(wa_id) or
        message_body_lower in ['menu', 'inicial']
    ):
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
        return

    # Se chegou aqui, significa que o usuário tem histórico e não digitou "sair"
    # e não foi atingida a condição de reiniciar o menu.
    current_stage = last_stage

    if current_stage == 'initial':
        if message_body_lower == '1':
            # Menu de Consulta de Pagamento
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
            # Menu de Dúvidas sobre Contas a Pagar
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
            # 1.1) Previsão de Pagamento
            send_message(
                wa_id,
                "Previsão de Pagamento:\nPor favor, informe o CNPJ para consultar todas as notas em aberto:"
            )
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp,
                stage='consulta_previsao'
            )
        elif message_body_lower in ['2', '1.2']:
            # 1.2) Composição de Notas de Pagamento (Títulos Pagos)
            send_message(
                wa_id,
                "Composição de Notas de Pagamento (Títulos Pagos) - Passo 1/3:\n"
                "Por favor, informe o CNPJ do fornecedor:"
            )
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp,
                stage='consulta_composicao_cnpj'
            )
        else:
            send_message(wa_id, "Opção inválida. Por favor, escolha uma opção válida da consulta de pagamento.")
        return

    # ---------------------------
    # 1.1) Previsão de Pagamento - Apenas CNPJ
    # ---------------------------
    elif current_stage == 'consulta_previsao':
        cnpj = message_body
        # Aqui, integre a consulta real para retornar todas as notas em aberto para o CNPJ
        send_message(
            wa_id, 
            f"Previsão de Pagamento:\nConsulta realizada para o CNPJ {cnpj}.\n\n"
            "Exemplo de notas em aberto:\n"
            "- NF 001, Emissão: 01/09/2025, Vencimento: 15/09/2025, Valor: R$ 1.000,00\n"
            "- NF 002, Emissão: 05/09/2025, Vencimento: 30/09/2025, Valor: R$ 500,00"
        )
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=cnpj,
            timestamp_recebido=timestamp,
            stage='final'
        )
        send_message(wa_id, "Posso ajudar com mais alguma coisa? Digite 'menu' para voltar ao menu principal ou 'sair' para encerrar.")
        return

    # ----------------------------------------------------
    # 1.2) Composição de Notas de Pagamento (Títulos Pagos)
    # Passo 1: Coleta de CNPJ
    # ----------------------------------------------------
    elif current_stage == 'consulta_composicao_cnpj':
        cnpj = message_body
        send_message(wa_id, "Passo 2/3:\nPor favor, informe a *data inicial* no formato dd/mm/yyyy:")
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=cnpj,
            timestamp_recebido=timestamp,
            stage='consulta_composicao_data_inicial'
        )
        return

    # Passo 2: Coleta da data inicial
    elif current_stage == 'consulta_composicao_data_inicial':
        data_inicial = message_body
        send_message(wa_id, "Passo 3/3:\nPor favor, informe a *data final* no formato dd/mm/yyyy:")
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=data_inicial,
            timestamp_recebido=timestamp,
            stage='consulta_composicao_data_final'
        )
        return

    # Passo 3: Coleta da data final
    elif current_stage == 'consulta_composicao_data_final':
        data_final = message_body
        all_msgs = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('-id')
        data_inicial_msg = all_msgs[1] if len(all_msgs) > 1 else None
        data_inicial = data_inicial_msg.message_body if data_inicial_msg else 'N/A'
        cnpj_msg = all_msgs[2] if len(all_msgs) > 2 else None
        cnpj = cnpj_msg.message_body if cnpj_msg else 'N/A'

        send_message(
            wa_id,
            f"Composição de Notas de Pagamento (Títulos Pagos)\n\n"
            f"CNPJ: {cnpj}\n"
            f"Período: {data_inicial} a {data_final}\n\n"
            f"Exemplo de resultado:\n"
            f"- Nota 001, Valor: R$ 1.000,00 (Pago em 10/08/2025)\n"
            f"- Nota 002, Valor: R$ 500,00 (Pago em 15/08/2025)"
        )
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=data_final,
            timestamp_recebido=timestamp,
            stage='final'
        )
        send_message(wa_id, "Posso ajudar com mais alguma coisa? Digite 'menu' para voltar ou 'sair' para encerrar.")
        return

    # -------------------------
    # 2) Dúvidas sobre Contas a Pagar
    # -------------------------
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
    # 'message_body' contém a descrição do erro/correção fornecida pelo usuário
        user_details = message_body
        phone_number = wa_id  # Número de telefone do usuário

        subject = "Ajustes ou Correções em Pagamento"
    # Montamos o corpo do e-mail com as informações necessárias
        message_text = (
            f"Solicitação de Ajuste/Correção de Pagamento\n\n"
            f"Detalhes fornecidos pelo usuário:\n{user_details}\n\n"
            f"Telefone (WhatsApp) de contato: {phone_number}\n"
        )

    # Envia o e-mail para o responsável
        send_mail(
            subject=subject,
            message=message_text,  # Texto do e-mail (simples)
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["rafael.araujo@combio.com.br"],
        # Caso queira enviar em HTML, inclua 'html_message=html_conteudo' e um texto HTML
        )

    # Confirma ao usuário que a solicitação foi recebida
        send_message(wa_id, "Recebemos sua solicitação de ajuste/correção. Em breve entraremos em contato.")

    # Salva o registro no banco e encerra (stage='final')
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=message_body,
            timestamp_recebido=timestamp,
            stage='final'
        )

        send_message(wa_id, "Posso ajudar com mais alguma coisa? Digite 'menu' para voltar ou 'sair' para encerrar.")
        return

    # ---------------------
    # Estágio final
    # ---------------------
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

def should_send_initial_message(wa_id):
    """
    Verifica se a última mensagem do usuário foi há mais de 2 minutos.
    Se sim, retornamos True para que o chatbot mostre o menu inicial novamente.
    """
    current_timestamp = timezone.now()
    last_message = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('-id').first()
    if last_message:
        time_diff = current_timestamp - last_message.timestamp_recebido
        return time_diff >= timedelta(minutes=2)
    return True
