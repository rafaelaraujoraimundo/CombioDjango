import json
from datetime import datetime, timedelta
from django.utils import timezone
from decouple import config
from .models import WhatsAppMessage
import requests
from django.core.mail import send_mail
from django.conf import settings
from .utils import formatar_titulos_em_blocos, formatar_titulos_pagos_em_blocos

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
                "Previsão de Pagamento:\nPor favor, informe o CNPJ/CPF para consultar todas as notas em aberto:"
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
        if not cnpj_valido(cnpj):
            send_message(wa_id, "❌ CNPJ/CPF inválido. Por favor, informe um CNPJ/CPF com 11 ou 14 dígitos numéricos.")
            return
        WhatsAppMessage.objects.create(
            wa_id=wa_id,
            message_id=message_id,
            message_body=cnpj,
            timestamp_recebido=timestamp,
            stage='final'
        )
        # Aqui, integre a consulta real para retornar todas as notas em aberto para o CNPJ
        send_message(wa_id, "Consultando informações no sistema, aguarde....")
        titulos = consulta_titulos_api(cnpj)

        if titulos:
            nome_emitente = titulos[0]['nome_fornecedor']
            mensagem = f"Prezado fornecedor, segue a relação dos títulos que temos em aberto até o momento:\n\nConsulta realizada para o CNPJ/CPF {cnpj}\nFornecedor: *{nome_emitente}*\n\n"
            send_message(wa_id, mensagem)
            blocos = formatar_titulos_em_blocos(titulos)

            for bloco in blocos:
                send_message(wa_id, bloco)

            
            mensagem = f"*Lembre-se: nossos pagamentos são realizados nos dias 15 e 30, conforme nossa política interna:*\n"
            mensagem += f"Títulos com vencimento entre os dias 1 e 15 serão pagos no dia 15 do mesmo mês.\n"   
            mensagem += f"Títulos com vencimento entre os dias 16 e 31 serão pagos no dia 30 do mesmo mês.\n" 
            mensagem += f"Caso a data de pagamento caia em um dia não útil, o pagamento será efetuado no próximo dia útil.\n" 
            mensagem += f"*Sentiu falta de alguma NF?*\n Fique ligado nesta Dica: Se a nota foi emitida há menos de 15 dias, ela pode estar em processo de lançamento interno e, em breve, entrará em nossa programação de pagamento. Caso tenha sido emitida há mais de 15 dias, recomendamos que entre em contato com o comprador para mais informações."
            send_message(wa_id, mensagem)
        else:
            mensagem = "Não foram encontrados títulos em aberto no momento, mas fique tranquilo!\n Se a nota foi emitida há menos de 15 dias, ela pode estar em processo de lançamento interno e, em breve, entrará em nossa programação de pagamento. \nCaso tenha sido emitida há mais de 15 dias, recomendamos que entre em contato com o comprador para mais informações."
            send_message(wa_id, mensagem)
            
        
        
        send_message(wa_id, "Posso ajudar com mais alguma coisa? Digite 'menu' para voltar ao menu principal ou 'sair' para encerrar.")
        return

    # ----------------------------------------------------
    # 1.2) Composição de Notas de Pagamento (Títulos Pagos)
    # Passo 1: Coleta de CNPJ
    # ----------------------------------------------------
    elif current_stage == 'consulta_composicao_cnpj':
        cnpj = message_body
        if not cnpj_valido(cnpj):
            send_message(wa_id, "❌ CNPJ/CPF inválido. Por favor, informe um CNPJ/CPF com 11 ou 14 dígitos numéricos.")
            return
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
        if not data_valida(data_inicial):
            send_message(wa_id, "❌ Data inicial inválida. Use o formato dd/mm/yyyy, como 01/05/2025.")
            return
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
        if not data_valida(data_final):
            send_message(wa_id, "❌ Data inicial inválida. Use o formato dd/mm/yyyy, como 01/05/2025.")
            return
        mensagens = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('-id')

        cnpj = next((m.message_body for m in mensagens if m.stage == 'consulta_composicao_data_inicial'), 'N/A')
        data_inicial = next((m.message_body for m in mensagens if m.stage == 'consulta_composicao_data_final'), 'N/A')
        data_final = message_body

        
        data_inicial_fmt = datetime.strptime(data_inicial, '%d/%m/%Y').strftime('%Y-%m-%d')
        data_final_fmt = datetime.strptime(data_final, '%d/%m/%Y').strftime('%Y-%m-%d')

        send_message(wa_id, "Consultando títulos pagos, aguarde...")

        titulos = consulta_titulos_pagos_api(cnpj, data_inicial_fmt, data_final_fmt)
        if titulos:
            nome_emitente = titulos[0]['nome_fornecedor']
            cabecalho = (
                    f"Composição de Notas de Pagamento (Títulos Pagos)\n\n"
                    f"Fornecedor: *{nome_emitente}*\n"
                    f"CNPJ: {cnpj}\n"
                    f"Período: {data_inicial} a {data_final}\n"
                )
            send_message(wa_id, cabecalho)

            blocos = formatar_titulos_pagos_em_blocos(titulos)
            for bloco in blocos:
                send_message(wa_id, bloco)



            mensagem = f"\n*Lembre-se: nossos pagamentos são realizados nos dias 15 e 30, conforme nossa política interna:*\n"
            mensagem += f"Títulos com vencimento entre os dias 1 e 15 serão pagos no dia 15 do mesmo mês.\n"   
            mensagem += f"Títulos com vencimento entre os dias 16 e 31 serão pagos no dia 30 do mesmo mês.\n" 
            mensagem += f"Caso a data de pagamento caia em um dia não útil, o pagamento será efetuado no próximo dia útil.\n" 
            send_message(wa_id, mensagem)
        else:
            mensagem = "Nenhum título pago encontrado no período informado.\n   "
            mensagem += "Em caso de dúvida, entrar em contato através do email: *contasapagar@combio.com.br* em breve um de nossos analistas irá atender sua solicitação."
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

    # -------------------------
    # 2) Dúvidas sobre Contas a Pagar
    # -------------------------
    elif current_stage == 'duvidas_menu':
        if message_body_lower in ['1', '2.1']:
            mensagem = f"\n*Nossos pagamentos são realizados nos dias 15 e 30, conforme nossa política interna:*\n"
            mensagem += f"Títulos com vencimento entre os dias 1 e 15 serão pagos no dia 15 do mesmo mês.\n"   
            mensagem += f"Títulos com vencimento entre os dias 16 e 31 serão pagos no dia 30 do mesmo mês.\n" 
            mensagem += f"Caso a data de pagamento caia em um dia não útil, o pagamento será efetuado no próximo dia útil.\n" 
            send_message(
                wa_id, mensagem
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
                "Para ajustes ou correções, por favor, informe o CNPJ, NF, contato para retorno e conte-nos brevemente a inconsistência encontrada"
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
            recipient_list=["chatbot@combio.com.br"],
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

    if response.status_code != 200:
        print("❌ Erro ao enviar mensagem para o WhatsApp:")
        print("Status:", response.status_code)
        print("Resposta:", response.text)
        print("Payload enviado:", json.dumps(data, indent=2))

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
        return time_diff >= timedelta(minutes=5)
    return True

def consulta_titulos_api(cnpj):
    url = f"{config('DATASUL_HOST')}/esp/combio/v1/api_chatbot/piBuscatitulosCNPJ/"
    payload = json.dumps({"cnpj": cnpj})
    headers = {
        'Authorization': f'Basic {config('DATASUL_TOKEN')}',
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        print(response)
        return response.json().get('items', [])
    return []

def cnpj_valido(cnpj):
    return cnpj.isdigit() and len(cnpj) in [11, 14]

def data_valida(data_str):
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False
    

def consulta_titulos_pagos_api(cnpj, data_inicial, data_final):
    url = f"{config('DATASUL_HOST')}/esp/combio/v1/api_chatbot/piBuscatitulosPagosCNPJ/"
    payload = json.dumps({
        "cnpj": cnpj,
        "dataInicial": data_inicial,
        "dataFinal": data_final
    })
    headers = {
        'Authorization': f'Basic {config("DATASUL_TOKEN")}',
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        print("❌ Erro ao consultar títulos pagos:")
        print("Status:", response.status_code)
        print("Resposta:", response.text)
        print("Payload enviado:", payload)

    if response.status_code == 200:
        return response.json().get('items', [])

    return []
