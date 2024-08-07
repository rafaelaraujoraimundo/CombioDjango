import re
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta
from django.utils import timezone
from decouple import config
from django.db.models import IntegerField
from django.db.models.functions import Cast
from .models import WhatsAppMessage, Message, Interaction
from .utils import consulta_titulos_api_cnpj
from django.contrib.auth.decorators import login_required
from .whatsapp import process_incoming_message
from .chatcombio import send_message_chatbot
import json

def clear_session(request):
    request.session.flush()
    return HttpResponse("Session cleared")

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'GET':
        challenge = request.GET.get('hub.challenge')
        if challenge:
            return HttpResponse(challenge)
    elif request.method == 'POST':
        incoming_message = json.loads(request.body.decode('utf-8'))
        process_incoming_message(incoming_message)
        return JsonResponse({'status': 'success', 'message': 'Message processed'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def chatbot_view(request):
    context = {
        'activegroup': 'chatbot',
        'title': 'Chatbot Combio',
    }
    return render(request, 'chatbot/chatbot.html', context)

@login_required
def send_message_chatbot_view(request):
    return send_message_chatbot(request)
