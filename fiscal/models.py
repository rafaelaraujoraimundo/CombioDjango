from django.db import models
from administration.models import User

class UnificacaoSPED(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Apenas os nomes dos arquivos:
    nome_arquivo_principal = models.CharField(max_length=255)
    nomes_arquivos_secundarios = models.TextField(help_text="Separados por vírgula")

    # Caminho do resultado continua sendo um arquivo real
    arquivo_resultado = models.FileField(upload_to='sped_unificador/resultados/', null=True, blank=True)
    
    data_processo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.data_processo.strftime('%d/%m/%Y %H:%M')}"