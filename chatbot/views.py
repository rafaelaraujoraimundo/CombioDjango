from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import requests
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
from dashboard.models import BiApbTitAp
from .models import WhatsAppMessage
import json
from django.utils import timezone
from decouple import config
from django.db.models import IntegerField
from django.db.models.functions import Cast

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'GET':
        challenge = request.GET.get('hub.challenge')
        if challenge:
            return HttpResponse(challenge)
    elif request.method == 'POST':
        incoming_message = json.loads(request.body.decode('utf-8'))
        #print(incoming_message)  # Opcional, para depuração
        process_incoming_message(incoming_message)
        return JsonResponse({'status': 'success', 'message': 'Message processed'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def process_incoming_message(message):
    try:
        entries = message.get('entry', [])
        for entry in entries:
            changes = entry.get('changes', [])
            for change in changes:
                value = change.get('value', {})
                if 'contacts' in value and 'messages' in value:
                    # Verificação do phone_number_id
                    phone_number_id = value.get('metadata', {}).get('phone_number_id')
                    if phone_number_id == config('WHATSAPP_ID_RECEIVER'):
                        message_details = value.get('messages', [])
                        for msg in message_details:
                            if 'text' in msg and 'body' in msg['text']:
                                print(message)
                                wa_id = msg.get('from')
                                message_id = msg.get('id')
                                message_body = msg['text']['body']
                                naive_timestamp_recebido = datetime.fromtimestamp(int(msg.get('timestamp')))
                                timestamp_recebido = timezone.make_aware(naive_timestamp_recebido, timezone.get_default_timezone())
                                
                                last_message = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('-id').first()
                                if last_message and last_message.stage == 'finalizado':
                                    new_stage = 'initial'  # Reiniciar o estágio para initial após finalizado
                                elif should_send_initial_message(wa_id):
                                    new_stage = 'initial'  # Tempo excedido, tratar como inicial
                                else:
                                    new_stage = determine_next_stage(last_message.stage, message_body) if last_message else 'initial'
                                
                                WhatsAppMessage.objects.create(
                                    wa_id=wa_id,
                                    message_id=message_id,
                                    message_body=message_body,
                                    timestamp_recebido=timestamp_recebido,
                                    stage=new_stage
                                )
                                execute_stage_action(wa_id, new_stage, message_body, message_id, timestamp_recebido )
                                
                                return  # Finaliza a função após processar a mensagem desejada
    except (KeyError, IndexError) as e:
        print(f"Error parsing message: {str(e)}")

    print("Message did not meet the structure criteria, ignoring.")

def send_initial_or_continue_message(wa_id, message_body):
    send_template_message(wa_id, "modelo_inicio", language="pt_BR")  # Por exemplo, sempre enviar o template inicial

def should_send_initial_message(wa_id):
    current_timestamp = timezone.now()
    last_message = WhatsAppMessage.objects.filter(wa_id=wa_id).order_by('-id').first()
    if last_message:
        time_diff = current_timestamp - last_message.timestamp_recebido
        return time_diff >= timedelta(minutes=2)  # Verifica se a última mensagem foi há mais de 10 minutos
    return True  # Se não houver última mensagem, envie a mensagem inicial

def determine_next_stage(last_stage, message_body):
    # Lógica para determinar o próximo estágio baseado no último estágio e corpo da mensagem
    if last_stage == 'initial':
        return 'collect_cnpj'
    elif last_stage == 'collect_cnpj':
        # Verificar se o corpo da mensagem é um CNPJ válido
        return 'send_info'
    elif last_stage == 'recollect_cnpj':
        if message_body.strip().lower() == 'sair':
            return 'send_info'
        else:
            return 'recollect_cnpj'
    return 'initial'  # Retorna ao inicial se algo der errado

def execute_stage_action(wa_id, stage, message_body, message_id, timestamp_recebido):
    # Função para executar ações baseadas no estágio
    if stage == 'initial':
        send_template_message(wa_id, "modelo_inicio", language="pt_BR")
    elif stage == 'collect_cnpj' or stage == 'recollect_cnpj':
        # Remover espaços em branco e converter o CNPJ para string
        cnpj = message_body.strip()
        
        # Verificar se o CNPJ fornecido é numérico
        if not cnpj.isdigit():
            send_message(wa_id, "O CNPJ fornecido não é válido. Por favor, forneça um CNPJ numérico ou digite SAIR para finalizar.")
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp_recebido,
                stage='recollect_cnpj'
            )
            return
        
        # Padronizar o CNPJ para 14 dígitos adicionando zeros à esquerda, se necessário
        cnpj = cnpj.zfill(14)
        contato_data = consulta_contato_datasul(cnpj)
        if contato_data:
            contatos_validos = [item for item in contato_data['items'] if item['telefone'] == wa_id]
            if not contatos_validos:
                send_message(wa_id, "Nenhum telefone correspondente encontrado para o CNPJ fornecido. Por favor, solicite o cadastro para a equipe de compras.")
                WhatsAppMessage.objects.create(
                    wa_id=wa_id,
                    message_id=message_id,
                    message_body=message_body,
                    timestamp_recebido=timezone.now(),
                    stage='send_info'
                )
                send_message(wa_id, f"Obrigado por utilizar nosso ChatBot...")
                return
            nome_contato = contatos_validos[0]['nome_contato']
            nome_emit = contatos_validos[0]['nome_emit']
            codigo_emit = contatos_validos[0]['codigo']
        # Filtrar os registros do modelo Titulo pelo CNPJ padronizado
        titulos = consulta_titulos_api(codigo_emit)
        
        if titulos:
            mensagem = f"Olá {nome_contato}, segue informações de NF abertas em nosso sistema:\n\n Empresa: *{nome_emit}* \n"
            for titulo in titulos:
                cod_tit_ap = str(titulo['cod_tit_ap'])
                cod_parcela = str(titulo['cod_parcela'])
                dat_emis_docto = datetime.strptime(titulo['dat_emis_docto'], '%Y-%m-%d').strftime('%d/%m/%Y') if titulo['dat_emis_docto'] else 'N/A'
                dat_vencto_tit_ap = datetime.strptime(titulo['dat_vencto_tit_ap'], '%Y-%m-%d').strftime('%d/%m/%Y') if titulo['dat_vencto_tit_ap'] else 'N/A'
                val_sdo_tit_ap = f"{titulo['val_sdo_tit_ap']:,.2f}" if titulo['val_sdo_tit_ap'] else '0.00'
                
                mensagem += (
                    f"\n"
                    f"*NF*: {cod_tit_ap}, "
                    f"*Emissão*: {dat_emis_docto}, "
                    f"*Vencimento*: {dat_vencto_tit_ap}, "
                    f"*Valor Saldo*: {val_sdo_tit_ap}\n"
                    
   )
            mensagem += (
                    f"\n\n*Politica interna de Pagamentos:* \n"
                    f"Os títulos com data de vencimento entre os dias 1 e 15 serão pagos no dia 15 do mês atual.\n"
                    f"Os títulos com data de vencimento entre os dias 16 e 31 serão pagos no último dia do mês atual.\n"
                    )    
            send_message(wa_id, mensagem)
            send_message(wa_id, f"Obrigado por utilizar nosso ChatBot...")
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp_recebido,
                stage='send_info'
                )
        else:
            mensagem = "Nenhuma informação encontrada para o CNPJ fornecido ou CNPJ incorreto. Por favor, forneça um CNPJ válido ou digite SAIR para finalizar."
            send_message(wa_id, mensagem)
            WhatsAppMessage.objects.create(
                wa_id=wa_id,
                message_id=message_id,
                message_body=message_body,
                timestamp_recebido=timestamp_recebido,
                stage='recollect_cnpj'
            )
            return

    elif stage == 'send_info':
        send_message(wa_id, f"Obrigado por utilizar nosso ChatBot... ")



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

def send_template_message(to, template_name, language="pt_BR"):
    token = config('TOKEN_WHATSAPP')
    
    url = f"https://graph.facebook.com/v20.0/{config('WHATSAPP_ID')}/messages"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    data = {
        'messaging_product': 'whatsapp',
        'to': to,
        'type': 'template',
        'template': {
            'name': template_name,
            'language': {
                'code': language
            },
        }
    }
    print(data)

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def consulta_contato_datasul(cnpj):
    url = f"{config('DATASUL_HOST')}/esp/combio/v1/api_chatbot/buscacontatos/"
    payload = json.dumps({"cnpj": cnpj})
    headers = {
        'Authorization': f'Basic {config('DATASUL_TOKEN')}',
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    return None


def consulta_titulos_api(codigo_emit):
    url = f"{config('DATASUL_HOST')}/esp/combio/v1/api_chatbot/buscatitulos/"
    payload = json.dumps({"codigo": codigo_emit})
    headers = {
        'Authorization': f'Basic {config('DATASUL_TOKEN')}',
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        print(response.json())
        return response.json().get('items', [])
    return []