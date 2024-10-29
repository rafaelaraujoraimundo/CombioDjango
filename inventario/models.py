import datetime
from django.db import models
from dashboard.models import BiCentroCusto, BiEstabelecimento, BiFuncionariosCombio
from datetime import timedelta

import os
from pathlib import Path
from django.conf import settings
from django.core.validators import MinLengthValidator, RegexValidator




# -----------------------------
# Tabelas relacionadas a Computadores
# -----------------------------


class TipoItem(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    

class Status(models.Model):
    nome_status = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome_status
    

class AcoesProntuario(models.Model):
    TIPO_CHOICES = [
        (1, 'Manutenção'),
        (2, 'Transferência'),
        (3, 'Apontamento'),
    ]

    acao = models.CharField(max_length=100, unique=True)
    tipo = models.IntegerField(choices=TIPO_CHOICES)

    def __str__(self):
        return self.acao



# -----------------------------
# Tabelas relacionadas a Estoque
# -----------------------------
class Estoque(models.Model):
    tipo_item = models.ForeignKey(TipoItem, on_delete=models.PROTECT)  # Usando o modelo de TipoItem
    modelo = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)  # Usando o modelo Status como chave estrangeira
    observacao = models.TextField(blank=True, null=True)
    local = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.tipo_item.nome} - {self.modelo}'



# -----------------------------
# Tabelas relacionadas a Celulares
# -----------------------------

def upload_to(instance, filename):
    return f'{filename}'

class Celular(models.Model):
    modelo = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100)
    imei = models.CharField(
        max_length=15,
        validators=[MinLengthValidator(15), RegexValidator(r'^\d{15}$', 'O IMEI deve conter 15 dígitos numéricos')]
    )
    numero_linha = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(11), RegexValidator(r'^\d{11}$', 'O número da linha deve conter 11 dígitos numéricos')]
    )
    usuario = models.CharField(max_length=100)
    status = models.ForeignKey('Status', on_delete=models.PROTECT)
    estabelecimento = models.CharField(max_length=100)
    centro_custo = models.CharField(max_length=100)
    arquivo_celular = models.FileField(upload_to=upload_to, blank=True, null=True)

    def save(self, *args, **kwargs):
        temp_arquivo = self.arquivo_celular
        if self.pk:
            previous = Celular.objects.get(pk=self.pk)
            if not self.arquivo_celular:
                # Mantém o arquivo existente se nenhum novo for carregado
                self.arquivo_celular = previous.arquivo_celular

        # Atualizar o caminho do arquivo após obter o ID
        if temp_arquivo:
            temp_arquivo.name = os.path.join(f'celular/{self.pk}', f'arquivo{os.path.splitext(temp_arquivo.name)[1]}')
            self.arquivo_celular = temp_arquivo
            super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        if self.arquivo_celular:
            file_path = Path(self.arquivo_celular.path)
            if file_path.exists():
                file_path.unlink()  # Deletar o arquivo ao excluir a instância
        super().delete(*args, **kwargs)

class ProntuarioCelular(models.Model):
    celular = models.ForeignKey(Celular, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    data = models.DateField()
    motivo_ocorrencia = models.TextField()
    acao = models.ForeignKey(AcoesProntuario, on_delete=models.PROTECT)  
    unidade_destino = models.CharField(max_length=100)
    local = models.CharField(max_length=100)

    def __str__(self):
        return f'Prontuário de {self.celular.modelo} - {self.data}'


# -----------------------------
# Tabelas relacionadas à Resposta da API
# -----------------------------

# Modelo principal: Hardware
class Hardware(models.Model):
    arch = models.CharField(max_length=100, blank=True, null=True)
    archive = models.CharField(max_length=255, blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    checksum = models.IntegerField(blank=True, null=True)
    default_gateway = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    dns = models.CharField(max_length=100, blank=True, null=True)
    etime = models.CharField(max_length=100, blank=True, null=True)
    fidelity = models.IntegerField(blank=True, null=True)
    ipaddr = models.CharField(max_length=100, blank=True, null=True)
    ipsrc = models.CharField(max_length=100, blank=True, null=True)
    last_come = models.DateTimeField(blank=True, null=True)
    last_date = models.DateTimeField(blank=True, null=True)
    memory = models.IntegerField(blank=True, null=True)  # Memória em MB
    name = models.CharField(max_length=255, blank=True, null=True)
    os_comments = models.CharField(max_length=255, blank=True, null=True)
    os_name = models.CharField(max_length=255, blank=True, null=True)
    os_version = models.CharField(max_length=100, blank=True, null=True)
    processor_n = models.IntegerField(blank=True, null=True)  # Número de processadores
    processors = models.IntegerField(blank=True, null=True)  # Clock speed
    processor_t = models.CharField(max_length=255, blank=True, null=True)  # Tipo de processador
    quality = models.CharField(max_length=100, blank=True, null=True)
    sstate = models.IntegerField(blank=True, null=True)
    swap = models.IntegerField(blank=True, null=True)  # Swap em MB
    type = models.IntegerField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    user_domain = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.CharField(max_length=255, blank=True, null=True)
    win_company = models.CharField(max_length=255, blank=True, null=True)
    win_owner = models.CharField(max_length=255, blank=True, null=True)
    win_prod_id = models.CharField(max_length=255, blank=True, null=True)
    win_prod_key = models.CharField(max_length=255, blank=True, null=True)
    workgroup = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Hardware {self.name} - {self.device_id}'

# Modelo para BIOS
class BIOS(models.Model):
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, related_name="bios")
    asset_tag = models.CharField(max_length=100, blank=True, null=True)
    bdate = models.CharField(max_length=100, blank=True, null=True)
    bmanufacturer = models.CharField(max_length=100, blank=True, null=True)
    bversion = models.CharField(max_length=100, blank=True, null=True)
    mmanufacturer = models.CharField(max_length=100, blank=True, null=True)
    mmodel = models.CharField(max_length=100, blank=True, null=True)
    msn = models.CharField(max_length=100, blank=True, null=True)
    smanufacturer = models.CharField(max_length=100, blank=True, null=True)
    smodel = models.CharField(max_length=100, blank=True, null=True)
    ssn = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'BIOS {self.bmanufacturer} - {self.bversion}'

# Modelo para CPUs
class CPU(models.Model):
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, related_name="cpus")
    cores = models.IntegerField(blank=True, null=True)
    cpu_arch = models.CharField(max_length=100, blank=True, null=True)
    current_address_width = models.IntegerField(blank=True, null=True)
    current_speed = models.CharField(max_length=100, blank=True, null=True)
    data_width = models.IntegerField(blank=True, null=True)
    l2_cache_size = models.CharField(max_length=100, blank=True, null=True)
    logical_cpus = models.IntegerField(blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    socket = models.CharField(max_length=100, blank=True, null=True)
    speed = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    voltage = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'CPU {self.manufacturer} - {self.type}'

# Modelo para Memórias
class Memory(models.Model):
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, related_name="memories")
    capacity = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    num_slots = models.IntegerField(blank=True, null=True)
    purpose = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    speed = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Memory {self.capacity} MB - {self.serial_number}'

# Modelo para Software
class Software(models.Model):
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, related_name="software")
    architecture = models.CharField(max_length=100, blank=True, null=True)
    bitswidth = models.IntegerField(blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    filesize = models.IntegerField(blank=True, null=True)
    folder = models.CharField(max_length=255, blank=True, null=True)
    guid = models.CharField(max_length=255, blank=True, null=True)
    install_date = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    name_id = models.IntegerField(blank=True, null=True)
    publisher_id = models.IntegerField(blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)
    version_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'Software {self.guid} - {self.install_date}'

# Modelo para Armazenamento (Storage)
class Storage(models.Model):
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, related_name="storages")
    description = models.CharField(max_length=255, blank=True, null=True)
    disk_size = models.IntegerField(blank=True, null=True)  # Tamanho do disco em MB
    firmware = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Storage {self.name} - {self.serial_number}'

class AccountInfo(models.Model):
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, related_name="accountinfo")
    tag = models.CharField(max_length=100, blank=True, null=True)
    fields_14 = models.CharField(max_length=255, blank=True, null=True)
    fields_3 = models.CharField(max_length=255, blank=True, null=True)
    fields_4 = models.CharField(max_length=255, blank=True, null=True)
    fields_5 = models.CharField(max_length=255, blank=True, null=True)
    fields_7 = models.CharField(max_length=255, blank=True, null=True)
    fields_8 = models.CharField(max_length=255, blank=True, null=True)
    fields_9 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'AccountInfo {self.tag}'


class Controlekit(models.Model):
    matricula = models.CharField(max_length=100)  # Novo campo 'matricula' para armazenar o código do usuário
    usuario = models.CharField(max_length=100)  # O nome do usuário será salvo aqui
    data_entrega = models.DateField()
    modelo = models.CharField(max_length=100)
    estabelecimento = models.CharField(max_length=100)
    centro_custo = models.CharField(max_length=100)
    serie = models.CharField(max_length=50, blank=True, null=True)
    data_final = models.DateField()

    def save(self, *args, **kwargs):
        # Calcular data final automaticamente (data_entrega + 2 anos)
        self.data_final = self.data_entrega + timedelta(days=365*2)
        super(Controlekit, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.usuario} - {self.modelo}'
    

class ControleFones(models.Model):
    matricula = models.CharField(max_length=100)  # Campo 'matricula' para armazenar o código do usuário
    usuario = models.CharField(max_length=100)  # O nome do usuário será salvo aqui
    data_entrega = models.DateField()
    modelo = models.CharField(max_length=100)
    estabelecimento = models.CharField(max_length=100)
    centro_custo = models.CharField(max_length=100)
    serie = models.CharField(max_length=50, blank=True, null=True)
    data_final = models.DateField()

    def save(self, *args, **kwargs):
        # Calcular data final automaticamente (data_entrega + 2 anos)
        self.data_final = self.data_entrega + timedelta(days=365*2)
        super(ControleFones, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.usuario} - {self.modelo}'
    

    # -----------------------------
# Tabelas relacionadas a Monitores
# -----------------------------
class Monitor(models.Model):
    numero_serie = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    patrimonio = models.CharField(max_length=100)
    estabelecimento = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)  
    localizacao = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.modelo} ({self.numero_serie})'

class ProntuarioMonitor(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    data = models.DateField()
    motivo_ocorrencia = models.TextField()
    acao = models.ForeignKey(AcoesProntuario, on_delete=models.PROTECT)  
    unidade_destino = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    localizacao_destino = models.CharField(max_length=100)

    def __str__(self):
        return f'Prontuário de {self.monitor.modelo} - {self.data}'
    




class Computador(models.Model):
    patrimonio = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    processador = models.CharField(max_length=100)
    memoria = models.CharField(max_length=100)
    hd = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    centro_custo = models.CharField(max_length=100)
    estabelecimento = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    numero_nota_fiscal = models.CharField(max_length=100)
    fornecedor = models.CharField(max_length=100)
    sistema_operacional = models.CharField(max_length=100)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    hardware = models.ForeignKey('Hardware', on_delete=models.CASCADE)
    arquivo_computador = models.FileField(upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return f'{self.hostname} ({self.patrimonio})'

    def save(self, *args, **kwargs):
        print("Save method called")
        temp_arquivo = self.arquivo_computador
        if self.pk:
            previous = Computador.objects.get(pk=self.pk)
            if not self.arquivo_computador:
                # Mantém o arquivo existente se nenhum novo for carregado
                self.arquivo_computador = previous.arquivo_computador

        # Sempre salvar, independentemente do arquivo
        super().save(*args, **kwargs)  # Movido para garantir que sempre seja chamado

    # Atualizar o caminho do arquivo após obter o ID
        if temp_arquivo:
            temp_arquivo.name = os.path.join(f'computador/{self.pk}', f'arquivo{os.path.splitext(temp_arquivo.name)[1]}')
            self.arquivo_computador = temp_arquivo
        
    def delete(self, *args, **kwargs):
        if self.arquivo_computador:
            file_path = Path(self.arquivo_computador.path)
            if file_path.exists():
                file_path.unlink()  # Deletar o arquivo ao excluir a instância
        super().delete(*args, **kwargs)



class ProntuarioComputador(models.Model):
    computador = models.ForeignKey(Computador, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    data = models.DateField()
    motivo_ocorrencia = models.TextField()
    acao = models.ForeignKey(AcoesProntuario, on_delete=models.PROTECT)  
    unidade_destino = models.CharField(max_length=100)
    local = models.CharField(max_length=100)

    def __str__(self):
        return f'Prontuário de {self.computador.hostname} - {self.data}'