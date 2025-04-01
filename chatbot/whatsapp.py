import json
from datetime import datetime
from django.utils import timezone
from decouple import config
import requests
from .models import Contatos
from .whatsapp_combio import process_combio_message
from .whatsapp_externo import process_externo_message

def process_incoming_message(message):
    try:
        entries = message.get('entry', [])
        for entry in entries:
            changes = entry.get('changes', [])
            for change in changes:
                value = change.get('value', {})
                if 'contacts' in value and 'messages' in value:
                    phone_number_id = value.get('metadata', {}).get('phone_number_id')
                    if phone_number_id == config('WHATSAPP_ID_RECEIVER'):
                        message_details = value.get('messages', [])
                        for msg in message_details:
                            if 'text' in msg and 'body' in msg['text']:
                                wa_id = msg.get('from')
                                print(f'wa_id {wa_id}')
                                
                                contato_model = Contatos.objects.filter(telefone=wa_id).first()
                                if contato_model:
                                    process_combio_message(wa_id, msg)
                                else:
                                    process_externo_message(wa_id, msg)
                                return
    except (KeyError, IndexError) as e:
        print(f"❌ Erro ao processar mensagem recebida: {str(e)}")

    print("❗ Mensagem ignorada: estrutura inválida.")

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
