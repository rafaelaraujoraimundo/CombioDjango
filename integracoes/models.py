import secrets
from django.db import models
from django.utils import timezone

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

class PinggyToken(models.Model):
    """Token de acesso do Pinggy (dashboard.pinggy.io). Pode ter 1..N redirecionamentos."""
    nome = models.CharField(max_length=80)
    token = models.CharField(max_length=120, help_text="Use o token exibido no dashboard do Pinggy")
    subdominio = models.CharField(max_length=120, blank=True, null=True, help_text="Subdomínio persistente (Pro)")
    ativo = models.BooleanField(default=True)
    auto_start = models.BooleanField(default=False, help_text="Subir túnel automaticamente (via Celery/management task)")
    observacoes = models.TextField(blank=True, default="")


    class Meta:
        verbose_name = "Token Pinggy"
        verbose_name_plural = "Tokens Pinggy"


    def __str__(self):
        return f"{self.nome}"




TIPO_CHOICES = (
    ("http", "HTTP/HTTPS"),
    ("tcp", "TCP"),
    ("udp", "UDP"),
    ("tls", "TLS"),
    )


class PinggyRedirect(models.Model):
    """Mapeia redirecionamentos (porta/host local) que um token pode expor."""
    token = models.ForeignKey(PinggyToken, on_delete=models.CASCADE, related_name="redirects")
    nome = models.CharField(max_length=80)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default="http")
    host_local = models.CharField(max_length=120, default="localhost")
    porta_local = models.PositiveIntegerField()
    sni_local = models.CharField(max_length=120, blank=True, null=True, help_text="Para HTTPS local opcionalmente informe SNI")
    habilitado = models.BooleanField(default=True)


    # Campos dinâmicos obtidos quando o túnel está ativo
    url_publica = models.URLField(blank=True, null=True)
    porta_publica = models.PositiveIntegerField(blank=True, null=True)


    # Runtime / monitoramento
    online = models.BooleanField(default=False)
    ultimo_check = models.DateTimeField(blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)


    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Redirecionamento"
        verbose_name_plural = "Redirecionamentos"


    def __str__(self):
        return f"{self.nome} ({self.tipo} -> {self.host_local}:{self.porta_local})"


    def registrar_check(self, ok: bool):
        self.online = ok
        self.ultimo_check = timezone.now()
        self.save(update_fields=["online", "ultimo_check"]) 