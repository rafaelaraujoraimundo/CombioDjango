# Create your models here.
from pathlib import Path
from django.db import models
from django.utils.timezone import now
import os
from django.conf import settings

class Consultoria(models.Model):
    nome = models.CharField(max_length=100, null=False)
    valor_hora = models.DecimalField(max_digits=5, decimal_places=2, default=100)

    def __str__(self):
        return self.nome
    


class Sistemas(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.nome
    

# Helper function to create the upload path
def upload_to(instance, filename):
    return f'projetos/{instance.id}/{filename}'

class Projeto(models.Model):
    nome_projeto = models.CharField(max_length=255)
    data_entrega = models.DateField(default=now)
    horas_utilizadas = models.DecimalField(max_digits=5, decimal_places=2)
    consultoria = models.ForeignKey('Consultoria', on_delete=models.PROTECT)
    sistemas = models.ForeignKey('Sistemas', on_delete=models.PROTECT)
    descricao_solucao = models.TextField()
    anexo_escopo = models.FileField(upload_to=upload_to, blank=True, null=True)
    anexo_documentacao = models.FileField(upload_to=upload_to, blank=True, null=True)
    anexo_fontes = models.FileField(upload_to=upload_to, blank=True, null=True)

    class Meta:
        db_table = 'projeto'

    def __str__(self):
        return self.nome_projeto

    def save(self, *args, **kwargs):
        # Salvar temporariamente os arquivos
        temp_escopo = self.anexo_escopo
        temp_documentacao = self.anexo_documentacao
        temp_fontes = self.anexo_fontes

        # Salvar sem arquivos para obter o ID
        self.anexo_escopo = None
        self.anexo_documentacao = None
        self.anexo_fontes = None
        super().save(*args, **kwargs)

        # Atualizar os caminhos dos arquivos após obter o ID
        if temp_escopo:
            temp_escopo.name = os.path.join(f'', 'escopo' + os.path.splitext(temp_escopo.name)[1])
        if temp_documentacao:
            temp_documentacao.name = os.path.join(f'', 'documents' + os.path.splitext(temp_documentacao.name)[1])
        if temp_fontes:
            temp_fontes.name = os.path.join(f'', 'fonts' + os.path.splitext(temp_fontes.name)[1])

        # Reatribuir os arquivos e salvar novamente
        self.anexo_escopo = temp_escopo
        self.anexo_documentacao = temp_documentacao
        self.anexo_fontes = temp_fontes
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
    # Lista de campos de arquivo
        files = [self.anexo_escopo, self.anexo_documentacao, self.anexo_fontes]
        for file_field in files:
            if file_field:
                file_path = Path(settings.MEDIA_ROOT) / file_field.path
                if file_path.exists():
                    file_path.unlink()  # Usar unlink para excluir o arquivo

    # Deletar a instância do modelo após a remoção dos arquivos
        super().delete(*args, **kwargs)