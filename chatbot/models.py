from django.db import models

class WhatsAppMessage(models.Model):
    wa_id = models.CharField(max_length=50)
    message_id = models.CharField(max_length=100)
    message_body = models.TextField()
    timestamp_recebido = models.DateTimeField()
    stage = models.CharField(max_length=100, default='inicio')  # Adicionando o campo 'stage' com valor padrão 'inicio'

    def __str__(self):
        return f"{self.wa_id} - {self.stage}"
