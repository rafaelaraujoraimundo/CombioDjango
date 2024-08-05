# whatsapp_bot/urls.py

from django.urls import path
from .views import chatbot_view, send_message_chatbot, whatsapp_webhook, clear_session

urlpatterns = [
    path('webhook/', whatsapp_webhook, name='whatsapp_webhook'),
     path('chatbot', chatbot_view, name='chatbot'),
    path('send_message/', send_message_chatbot, name='send_message_chatbot'),
    path('clear_session/', clear_session, name='clear_session'),
]