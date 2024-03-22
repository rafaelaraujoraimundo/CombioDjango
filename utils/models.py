from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.base import ContentFile
from administration.models import User
import os


def pasta_upload(instance, filename):
    # Gera o caminho para a pasta de upload com base no ID do modelo e no nome do arquivo
    nome_arquivo = os.path.basename(filename)
    return f'uploads/finalizados/{instance.id}/{nome_arquivo}'


class Arquivo(models.Model):
    arquivo_original = models.FileField(upload_to='uploads/')
    data_processamento = models.DateTimeField(default=timezone.now)
    arquivo_final = models.FileField(upload_to=pasta_upload)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return os.path.basename(self.arquivo_original.name)

    def processar_arquivo(self):
        # Realize aqui o processamento necessário no arquivo original
        # Neste exemplo, vou apenas adicionar um prefixo ao nome do arquivo final
        nome_arquivo_final = 'processado_' + \
            os.path.basename(self.arquivo_original.name)

        # Crie o conteúdo do arquivo final (neste exemplo, será o mesmo do arquivo original)
        conteudo_arquivo_final = self.arquivo_original.read()

        # Salve o arquivo final
        self.arquivo_final.save(
            nome_arquivo_final, ContentFile(conteudo_arquivo_final))
