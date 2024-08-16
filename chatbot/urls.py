# whatsapp_bot/urls.py

from django.urls import path
from .views import chatbot_view, send_message_chatbot, whatsapp_webhook, clear_session,  ContatosList, ContatosCreate, contatos_edit, contatos_delete

   


urlpatterns = [
    path('webhook/', whatsapp_webhook, name='whatsapp_webhook'),
     path('chatbot', chatbot_view, name='chatbot'),
    path('send_message/', send_message_chatbot, name='send_message_chatbot'),
    path('clear_session/', clear_session, name='clear_session'),

    path('contatos/', ContatosList.as_view(), name='contatos_list'),
    path('contatos/new/', ContatosCreate.as_view(), name='contato_create'),
    path('contatos/edit/<int:contato_id>/', contatos_edit, name='contato_edit'),
    path('contatos/delete/<int:contato_id>/', contatos_delete, name='contato_delete'),

]