import os
import shutil
from django.db import models
from administration.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class Configuracao(models.Model):
    arquivo_imagem = models.ImageField(upload_to='papeldeparede/', blank=True, null=True)
    nome_arquivo = models.CharField(max_length=100, blank=True)
    usuario_inclusao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario_inclusao')
    data_inclusao = models.DateTimeField(auto_now_add=True)
    usuario_alteracao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario_alteracao', null=True, blank=True)
    data_alteracao = models.DateTimeField(auto_now=True)
    padrao_papel_parede = models.BooleanField(default=False)
    padrao_bloqueio_tela = models.BooleanField(default=False)
    observacao = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Save the instance first to get an id
        super(Configuracao, self).save(*args, **kwargs)

        if self.arquivo_imagem:
            # Define the new filename and path
            new_filename = f'{self.id}.jpg'
            new_path = os.path.join('media', 'papeldeparede', new_filename)

            # Check if the file needs to be moved
            current_path = self.arquivo_imagem.path
            if not current_path == new_path:
                if os.path.exists(current_path):
                    # Move and rename the file
                    os.rename(current_path, new_path)
                    self.arquivo_imagem.name = os.path.join('papeldeparede', new_filename)
                    super(Configuracao, self).save(update_fields=['arquivo_imagem'])

                # Handle copies for special features
                if self.padrao_papel_parede:
                    shutil.copy(new_path, os.path.join('media', 'papeldeparede', 'papelparede.jpg'))
                if self.padrao_bloqueio_tela:
                    shutil.copy(new_path, os.path.join('media', 'papeldeparede', 'bloqueio.jpg'))

    def __str__(self):
        return self.nome_arquivo if self.nome_arquivo else str(self.id)