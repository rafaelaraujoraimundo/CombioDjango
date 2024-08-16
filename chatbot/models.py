from django.db import models
from django.conf import settings

class WhatsAppMessage(models.Model):
    wa_id = models.CharField(max_length=50)
    message_id = models.CharField(max_length=100)
    message_body = models.TextField()
    timestamp_recebido = models.DateTimeField()
    stage = models.CharField(max_length=100, default='inicio')  # Adicionando o campo 'stage' com valor padrão 'inicio'

    def __str__(self):
        return f"{self.wa_id} - {self.stage}"



class Message(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Interaction(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    session_key = models.CharField(max_length=40)
    stage = models.CharField(max_length=50, default='inicio')
    cnpj = models.CharField(max_length=14, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'session_key')



class Contatos(models.Model):
    nome = models.CharField(max_length=100)
    unidade = models.CharField(max_length=50)
    setor =  models.CharField(max_length=50, default='TI')
    cargo = models.CharField(max_length=50, default='Cargo')
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome