import django.views.generic
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

from chatbot.forms import ContatosForm
from .models import Contatos, WhatsAppMessage, Message, Interaction
from .utils import consulta_titulos_api_cnpj
from django.contrib.auth.decorators import login_required
from .whatsapp import process_incoming_message
from .chatcombio import send_message_chatbot
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib import messages

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



class ContatosList(ListView):
    model = Contatos
    queryset = Contatos.objects.all()
    template_name = 'chatbot/contatos/contatos_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContatosList, self).get_context_data(**kwargs)
        context['activegroup'] = 'Contatos'
        context['title'] = 'Lista de Contatos'
        return context


class ContatosCreate(CreateView):
    model = Contatos
    form_class = ContatosForm  # Certifique-se de que este formulário existe e está correto
    template_name = 'chatbot/contatos/contatos_form.html'
    success_url = reverse_lazy('contatos_list')

    def get_context_data(self, **kwargs):
        context = super(ContatosCreate, self).get_context_data(**kwargs)
        context['activegroup'] = 'Contatos'
        context['title'] = 'Inclusão de Contato'
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        

def contatos_edit(request, contato_id):
    activegroup = 'Contatos'
    title = 'Edição de Contato'
    contato = get_object_or_404(Contatos, pk=contato_id)
    if request.method == "POST":
        form = ContatosForm(request.POST, instance=contato)  # Certifique-se de que este formulário existe e está correto
        if form.is_valid():
            form.save()
            return redirect('contatos_list')
    else:
        form = ContatosForm(instance=contato)
    context = {'form': form, 'activegroup': activegroup, 'title': title}
    return render(request, 'chatbot/contatos/contatos_edit.html', context)


def contatos_delete(request, contato_id):
    contato = get_object_or_404(Contatos, pk=contato_id)
    if request.method == "POST":
        contato.delete()
        messages.success(request, f'"{contato.nome}" foi excluído com sucesso.')
        return redirect('contatos_list')
    return redirect('contatos_list')