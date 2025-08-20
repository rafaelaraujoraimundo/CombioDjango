import secrets
from django.db import models

class MondayToken(models.Model):
    token = models.CharField(primary_key=True, max_length=64)
    monday_key = models.CharField(max_length=400)
    monday_board = models.BigIntegerField()  # numeric(10,0)

    class Meta:
        db_table = "monday_tokens"
    

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        # gera um token seguro se vier vazio
        if not self.token:
            self.token = secrets.token_urlsafe(48)[:64]
        return super().save(*args, **kwargs)