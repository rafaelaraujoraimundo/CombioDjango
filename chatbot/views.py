from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import requests
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
from .models import WhatsAppMessage
import json
from django.utils import timezone
from decouple import config

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
                if 'contacts' in change.get('value', {}) and 'messages' in change.get('value', {}):
                    message_details = change.get('value', {}).get('messages', [])
                    for msg in message_details:
                        if 'text' in msg and 'body' in msg['text']:
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
                            
                            execute_stage_action(wa_id, new_stage, message_body)
                            
                            # Salvar a mensagem no banco de dados com o novo estágio
                            WhatsAppMessage.objects.create(
                                wa_id=wa_id,
                                message_id=message_id,
                                message_body=message_body,
                                timestamp_recebido=timestamp_recebido,
                                stage=new_stage
                            )
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
    return 'initial'  # Retorna ao inicial se algo der errado

def execute_stage_action(wa_id, stage, message_body):
    # Função para executar ações baseadas no estágio
    if stage == 'initial':
        send_template_message(wa_id, "modelo_inicio", language="pt_BR")
    elif stage == 'collect_cnpj':
        send_message(wa_id, f"Verificamos seu CPNJ... e segue as informações... Mensagem Original: {message_body}")
    elif stage == 'send_info':
        send_message(wa_id, f"Obrigado por utilizar nosso ChatBot... Mensagem Original: {message_body}")


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