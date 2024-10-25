from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .models import (Celular, Computador, Estoque, Hardware, Monitor, ProntuarioCelular,
    ProntuarioMonitor, Status, TipoItem)
from .schema import (BiEstabelecimentoCcustoSchema, BiEstabelecimentoSchema, CelularSchema,
    ComputadorCreateSchema, ComputadorSchema, EstoqueCreateSchema, EstoqueSchema,
    HardwareDetailSchema, HardwareSchema, MonitorOutSchema, MonitorSchema,
    ProntuarioCelularCreateSchema, ProntuarioCelularSchema, ProntuarioMonitorCreateSchema,
    ProntuarioMonitorSchema, StatusSchema, TipoItemSchema, EsCentroCustoSchema)
from datetime import datetime
from dashboard.models import BiEstabelecimento, BiCentroCusto

# Inicializando o Router
routerHardware = Router()
routerMonitor = Router()
routerTipoItem = Router()
routerEstoque = Router()
routerComputador = Router()
routerStatus = Router()
routerCentroCusto = Router()
routerEstabelecimento = Router()

# Endpoint para buscar todos os hardwares e suas tabelas relacionadas
@routerHardware.get("/hardwareDetails", response=List[HardwareDetailSchema])
def get_all_hardware(request):
    # Obtém todos os hardwares com os relacionamentos
    hardwares = Hardware.objects.prefetch_related(
        'bios', 'cpus', 'memories', 'software', 'storages', 'accountinfo'
    ).all()

    # Itera sobre cada hardware e formata os campos datetime
    for hardware in hardwares:
        # Converter datetime para string no hardware
        if hardware.last_come:
            hardware.last_come = hardware.last_come.strftime('%Y-%m-%d %H:%M:%S')
        if hardware.last_date:
            hardware.last_date = hardware.last_date.strftime('%Y-%m-%d %H:%M:%S')

        # Converter datas no software
        for software in hardware.software.all():
            if software.install_date:
                software.install_date = software.install_date.strftime('%Y-%m-%d %H:%M:%S')

    return hardwares

# Endpoint para buscar detalhes de um hardware específico com base no ID


# Endpoint para buscar detalhes de um hardware específico com base no ID
@routerHardware.get("/hardware/{hardware_id}", response=HardwareDetailSchema)
def get_hardware_by_id(request, hardware_id: int):
    # Obtém o hardware e suas relações relacionadas
    hardware = get_object_or_404(
        Hardware.objects.prefetch_related(
            'bios', 'cpus', 'memories', 'software', 'storages', 'accountinfo'
        ), id=hardware_id
    )

    # Converter datetime para string no hardware
    if hardware.last_come:
        hardware.last_come = hardware.last_come.strftime('%Y-%m-%d %H:%M:%S')
    if hardware.last_date:
        hardware.last_date = hardware.last_date.strftime('%Y-%m-%d %H:%M:%S')

    # Converter datas no software
    for software in hardware.software.all():
        if software.install_date:
            software.install_date = software.install_date.strftime('%Y-%m-%d %H:%M:%S')

    return hardware


@routerHardware.get("/hardware", response=List[HardwareSchema])
def get_hardware_main(request):
    # Obtém todos os hardwares sem as tabelas relacionadas
    hardwares = Hardware.objects.all()

    # Iterar sobre os hardwares e formatar os campos de data para string
    for hardware in hardwares:
        if hardware.last_come:
            hardware.last_come = hardware.last_come.strftime('%Y-%m-%d %H:%M:%S')
        if hardware.last_date:
            hardware.last_date = hardware.last_date.strftime('%Y-%m-%d %H:%M:%S')

    return hardwares


# API MONITOR
@routerMonitor.get("/monitors", response=List[MonitorOutSchema])
def get_all_monitors(request):
    return Monitor.objects.all()

# GET: Buscar um Monitor pelo ID
@routerMonitor.get("/monitors/{monitor_id}", response=MonitorOutSchema)
def get_monitor_by_id(request, monitor_id: int):
    monitor = get_object_or_404(Monitor, id=monitor_id)
    return monitor

# POST: Criar um novo Monitor
@routerMonitor.post("/monitors", response=MonitorOutSchema)
def create_monitor(request, monitor_data: MonitorSchema):
    monitor = Monitor.objects.create(**monitor_data.dict())
    return monitor

# PUT: Atualizar um Monitor existente pelo ID
@routerMonitor.put("/monitors/{monitor_id}", response=MonitorOutSchema)
def update_monitor(request, monitor_id: int, monitor_data: MonitorSchema):
    monitor = get_object_or_404(Monitor, id=monitor_id)
    for attr, value in monitor_data.dict().items():
        setattr(monitor, attr, value)
    monitor.save()
    return monitor

# DELETE: Deletar um Monitor pelo ID
@routerMonitor.delete("/monitors/{monitor_id}")
def delete_monitor(request, monitor_id: int):
    monitor = get_object_or_404(Monitor, id=monitor_id)
    monitor.delete()
    return {"success": True, "message": f"Monitor com ID {monitor_id} foi deletado com sucesso."}


# POST criar um novo prontuário
@routerMonitor.post("/monitorprontuarios", response=ProntuarioMonitorSchema)
def create_prontuario(request, payload: ProntuarioMonitorCreateSchema):
    # Buscar a instância de Monitor com base no ID fornecido
    monitor = get_object_or_404(Monitor, id=payload.monitor)
    
    # Criar o prontuário utilizando a instância de Monitor
    prontuario = ProntuarioMonitor.objects.create(
        monitor=monitor,
        usuario=payload.usuario,
        data=payload.data,
        motivo_ocorrencia=payload.motivo_ocorrencia,
        unidade_destino=payload.unidade_destino,
        local_destino=payload.local_destino,
        status=payload.status,
        observacao=payload.observacao
    )
    
    # Ao retornar o prontuário, devolver o ID do monitor em vez da instância completa
    prontuario_dict = prontuario.__dict__
    prontuario_dict["monitor"] = prontuario.monitor.id
    
    return prontuario_dict

# PUT atualizar um prontuário existente
@routerMonitor.put("/monitorsprontuarios/{prontuario_id}", response=ProntuarioMonitorSchema)
def update_prontuario(request, prontuario_id: int, payload: ProntuarioMonitorCreateSchema):
    # Busca o prontuário existente pelo ID
    prontuario = get_object_or_404(ProntuarioMonitor, id=prontuario_id)

    # Atualiza os campos do prontuário, tratando o campo 'monitor' separadamente
    for attr, value in payload.dict().items():
        if attr == 'monitor':
            # Se o campo for 'monitor', buscamos a instância do Monitor
            monitor = get_object_or_404(Monitor, id=value)
            setattr(prontuario, attr, monitor)  # Atribuímos a instância de Monitor
        else:
            setattr(prontuario, attr, value)  # Para os demais campos, fazemos a atribuição normal

    # Salva as mudanças no banco de dados
    prontuario.save()

    # Retorna o prontuário atualizado com o ID do monitor no formato correto
    prontuario_dict = prontuario.__dict__
    prontuario_dict["monitor"] = prontuario.monitor.id  # Garante que o monitor seja um ID na resposta

    return prontuario_dict

# DELETE remover um prontuário
@routerMonitor.delete("/monitorsprontuarios/{prontuario_id}")
def delete_prontuario(request, prontuario_id: int):
    prontuario = get_object_or_404(ProntuarioMonitor, id=prontuario_id)
    prontuario.delete()
    return {"success": True, "message": f"Prontuário com ID {prontuario_id} foi deletado com sucesso."}


@routerMonitor.get("/monitorsprontuarios", response=List[ProntuarioMonitorSchema])
def get_all_prontuarios(request):
    print("Chamando todos os prontuários")
    return ProntuarioMonitor.objects.all()

@routerMonitor.get("/monitorsprontuarios/{prontuario_id}", response=ProntuarioMonitorSchema)
def get_prontuario_by_id(request, prontuario_id: int):
    prontuario = get_object_or_404(ProntuarioMonitor, id=prontuario_id)
    return prontuario

@routerMonitor.get("/monitors/{monitor_id}/prontuarios", response=List[ProntuarioMonitorSchema])
def get_prontuarios_by_monitor(request, monitor_id: int):
    # Busca os prontuários relacionados ao monitor com base no monitor_id
    prontuarios = ProntuarioMonitor.objects.filter(monitor__id=monitor_id)

    # Itera sobre os prontuários e garante que o campo monitor contenha o ID do monitor
    prontuario_list = []
    for prontuario in prontuarios:
        prontuario_dict = prontuario.__dict__.copy()  # Copia o dicionário de atributos
        prontuario_dict['monitor'] = prontuario.monitor.id  # Atribui o ID do monitor
        prontuario_list.append(prontuario_dict)  # Adiciona à lista de retorno

    return prontuario_list

routerCelular = Router()

# GET: Buscar todos os prontuários de celulares
@routerCelular.get("/celularesprontuarios", response=List[ProntuarioCelularSchema])
def get_all_prontuarios_celular(request):
    print("Chamando todos os prontuários de celulares")
    return ProntuarioCelular.objects.all()

# GET: Buscar um prontuário de celular pelo ID
@routerCelular.get("/celularesprontuarios/{prontuario_id}", response=ProntuarioCelularSchema)
def get_prontuario_celular_by_id(request, prontuario_id: int):
    prontuario = get_object_or_404(ProntuarioCelular, id=prontuario_id)
    return prontuario

# GET: Buscar prontuários de um celular específico (relacionado pelo ID)
@routerCelular.get("/celulares/{celular_id}/prontuarios", response=List[ProntuarioCelularSchema])
def get_prontuarios_by_celular(request, celular_id: int):
    prontuarios = ProntuarioCelular.objects.filter(celular__id=celular_id)

    prontuario_list = []
    for prontuario in prontuarios:
        prontuario_dict = prontuario.__dict__.copy()
        prontuario_dict['celular'] = prontuario.celular.id
        prontuario_list.append(prontuario_dict)

    return prontuario_list

# POST: Criar um novo prontuário para celular
@routerCelular.post("/celularesprontuarios", response=ProntuarioCelularSchema)
def create_prontuario_celular(request, payload: ProntuarioCelularCreateSchema):
    celular = get_object_or_404(Celular, id=payload.celular)
    prontuario = ProntuarioCelular.objects.create(
        celular=celular,
        usuario=payload.usuario,
        data=payload.data,
        motivo_ocorrencia=payload.motivo_ocorrencia,
        status=payload.status,
        unidade_destino=payload.unidade_destino,
        local=payload.local
    )
    prontuario_dict = prontuario.__dict__
    prontuario_dict["celular"] = prontuario.celular.id
    return prontuario_dict

# PUT: Atualizar um prontuário de celular existente
@routerCelular.put("/celularesprontuarios/{prontuario_id}", response=ProntuarioCelularSchema)
def update_prontuario_celular(request, prontuario_id: int, payload: ProntuarioCelularCreateSchema):
    prontuario = get_object_or_404(ProntuarioCelular, id=prontuario_id)
    for attr, value in payload.dict().items():
        if attr == 'celular':
            celular = get_object_or_404(Celular, id=value)
            setattr(prontuario, attr, celular)
        else:
            setattr(prontuario, attr, value)
    prontuario.save()
    prontuario_dict = prontuario.__dict__
    prontuario_dict["celular"] = prontuario.celular.id
    return prontuario_dict

# DELETE: Deletar um prontuário de celular pelo ID
@routerCelular.delete("/celularesprontuarios/{prontuario_id}")
def delete_prontuario_celular(request, prontuario_id: int):
    prontuario = get_object_or_404(ProntuarioCelular, id=prontuario_id)
    prontuario.delete()
    return {"success": True, "message": f"Prontuário com ID {prontuario_id} foi deletado com sucesso."}


@routerCelular.get("/celulares", response=List[CelularSchema])
def get_all_celulares(request):
    return Celular.objects.all()

# GET: Buscar um Celular pelo ID
@routerCelular.get("/celulares/{celular_id}", response=CelularSchema)
def get_celular_by_id(request, celular_id: int):
    celular = get_object_or_404(Celular, id=celular_id)
    return CelularSchema.from_orm(celular)

# POST: Criar um novo Celular
@routerCelular.post("/celulares", response=CelularSchema)
def create_celular(request, payload: CelularSchema):
    celular = Celular.objects.create(**payload.dict())
    return CelularSchema.from_orm(celular)

# PUT: Atualizar um Celular existente pelo ID
@routerCelular.put("/celulares/{celular_id}", response=CelularSchema)
def update_celular(request, celular_id: int, payload: CelularSchema):
    celular = get_object_or_404(Celular, id=celular_id)
    for attr, value in payload.dict().items():
        setattr(celular, attr, value)
    celular.save()
    return CelularSchema.from_orm(celular)

# DELETE: Deletar um Celular pelo ID
@routerCelular.delete("/celulares/{celular_id}")
def delete_celular(request, celular_id: int):
    celular = get_object_or_404(Celular, id=celular_id)
    celular.delete()
    return {"success": True, "message": f"Celular com ID {celular_id} foi deletado com sucesso."}





# GET: Buscar todos os tipos de item
@routerTipoItem.get("/tipo_items", response=List[TipoItemSchema])
def get_all_tipo_items(request):
    return TipoItem.objects.all()

# GET: Buscar um TipoItem pelo ID
@routerTipoItem.get("/tipo_items/{tipo_item_id}", response=TipoItemSchema)
def get_tipo_item_by_id(request, tipo_item_id: int):
    tipo_item = get_object_or_404(TipoItem, id=tipo_item_id)
    return TipoItemSchema.from_orm(tipo_item)

# POST: Criar um novo TipoItem
@routerTipoItem.post("/tipo_items", response=TipoItemSchema)
def create_tipo_item(request, payload: TipoItemSchema):
    tipo_item = TipoItem.objects.create(**payload.dict())
    return TipoItemSchema.from_orm(tipo_item)

# PUT: Atualizar um TipoItem existente pelo ID
@routerTipoItem.put("/tipo_items/{tipo_item_id}", response=TipoItemSchema)
def update_tipo_item(request, tipo_item_id: int, payload: TipoItemSchema):
    # Obtém o objeto existente com base no ID
    tipo_item = get_object_or_404(TipoItem, id=tipo_item_id)

    # Verifica se o nome fornecido já existe em outro registro
    if TipoItem.objects.exclude(id=tipo_item_id).filter(nome=payload.nome).exists():
        return {"error": "Já existe um item com esse nome."}

    # Atualiza apenas os atributos da instância existente, exceto o ID
    for attr, value in payload.dict().items():
        if attr != 'id':  # Ignora o campo 'id'
            setattr(tipo_item, attr, value)

    # Salva as mudanças
    tipo_item.save()

    # Retorna o objeto atualizado
    return TipoItemSchema.from_orm(tipo_item)

# DELETE: Deletar um TipoItem pelo ID
@routerTipoItem.delete("/tipo_items/{tipo_item_id}")
def delete_tipo_item(request, tipo_item_id: int):
    tipo_item = get_object_or_404(TipoItem, id=tipo_item_id)
    tipo_item.delete()
    return {"success": True, "message": f"Tipo de Item com ID {tipo_item_id} foi deletado com sucesso."}



@routerEstoque.post("/estoques", response=EstoqueSchema)
def create_estoque(request, payload: EstoqueCreateSchema):
    # Buscar as instâncias de TipoItem e Status com base nos IDs fornecidos
    tipo_item = get_object_or_404(TipoItem, id=payload.tipo_item)
    status = get_object_or_404(Status, id=payload.status)

    # Criar o registro de estoque utilizando as instâncias de TipoItem e Status
    estoque = Estoque.objects.create(
        tipo_item=tipo_item,
        modelo=payload.modelo,
        fabricante=payload.fabricante,
        status=status,
        observacao=payload.observacao,
        local=payload.local
    )
    
    # Retornar o objeto estoque criado
    return EstoqueSchema.from_orm(estoque)


@routerEstoque.put("/estoques/{estoque_id}", response=EstoqueSchema)
def update_estoque(request, estoque_id: int, payload: EstoqueCreateSchema):
    # Buscar a instância de Estoque com base no ID fornecido
    estoque = get_object_or_404(Estoque, id=estoque_id)

    # Atualizar os campos do Estoque, incluindo a instância de Status
    tipo_item = get_object_or_404(TipoItem, id=payload.tipo_item)
    status = get_object_or_404(Status, id=payload.status)
    
    estoque.tipo_item = tipo_item
    estoque.modelo = payload.modelo
    estoque.fabricante = payload.fabricante
    estoque.status = status
    estoque.observacao = payload.observacao
    estoque.local = payload.local

    # Salvar as mudanças no banco de dados
    estoque.save()

    # Retornar o objeto estoque atualizado
    return EstoqueSchema.from_orm(estoque)
    
@routerEstoque.get("/estoques", response=List[EstoqueSchema])
def get_all_estoques(request):
    # Retorna todos os registros de Estoque
    estoques = Estoque.objects.all()
    return estoques

@routerEstoque.get("/estoques/{estoque_id}", response=EstoqueSchema)
def get_estoque_by_id(request, estoque_id: int):
    # Busca o Estoque com o ID fornecido
    estoque = get_object_or_404(Estoque, id=estoque_id)
    return estoque


@routerEstoque.delete("/estoques/{estoque_id}")
def delete_estoque(request, estoque_id: int):
    # Buscar a instância de Estoque com base no ID fornecido
    estoque = get_object_or_404(Estoque, id=estoque_id)
    
    # Deletar a instância de Estoque
    estoque.delete()
    
    # Retornar uma mensagem de sucesso
    return {"success": True, "message": f"Estoque com ID {estoque_id} foi deletado com sucesso."}



@routerComputador.get("/computadores", response=List[ComputadorSchema])
def get_all_computadores(request):
    computadores = Computador.objects.all()

    # Itera sobre cada computador e garante que o campo hardware contenha o ID do hardware
    computador_list = []
    for computador in computadores:
        computador_dict = computador.__dict__.copy()  # Copia o dicionário de atributos
        computador_dict['hardware'] = computador.hardware.id  # Atribui o ID do hardware
        computador_list.append(computador_dict)  # Adiciona à lista de retorno

    return computador_list



@routerComputador.get("/computadores/{computador_id}", response=ComputadorSchema)
def get_computador_by_id(request, computador_id: int):
    computador = get_object_or_404(Computador, id=computador_id)

    # Garante que o campo hardware contenha o ID do hardware
    computador_dict = computador.__dict__.copy()  # Copia o dicionário de atributos
    computador_dict['hardware'] = computador.hardware.id  # Atribui o ID do hardware

    return computador_dict



@routerComputador.post("/computadores", response=ComputadorSchema)
def create_computador(request, payload: ComputadorCreateSchema):
    # Buscar a instância de Hardware com base no ID fornecido
    hardware = get_object_or_404(Hardware, id=payload.hardware)
    
    # Criar o computador utilizando a instância de Hardware
    computador = Computador.objects.create(
        patrimonio=payload.patrimonio,
        hostname=payload.hostname,
        numero_serie=payload.numero_serie,
        fabricante=payload.fabricante,
        modelo=payload.modelo,
        processador=payload.processador,
        memoria=payload.memoria,
        hd=payload.hd,
        usuario=payload.usuario,
        departamento=payload.departamento,
        unidade=payload.unidade,
        cargo=payload.cargo,
        numero_nota_fiscal=payload.numero_nota_fiscal,
        fornecedor=payload.fornecedor,
        sistema_operacional=payload.sistema_operacional,
        status=payload.status,
        hardware=hardware  # Usando a instância de hardware
    )
    
    # Após criar o computador, retornamos o ID do hardware em vez da instância completa
    computador_dict = computador.__dict__.copy()
    computador_dict["hardware"] = computador.hardware.id  # Substitui o objeto pelo ID

    return computador_dict  # Retornamos o dicionário atualizado com o ID de hardware


@routerComputador.put("/computadores/{computador_id}", response=ComputadorSchema)
def update_computador(request, computador_id: int, payload: ComputadorCreateSchema):
    # Buscar o computador existente pelo ID
    computador = get_object_or_404(Computador, id=computador_id)

    # Atualizar os campos do computador, tratando o campo 'hardware' separadamente
    for attr, value in payload.dict().items():
        if attr == 'hardware':
            # Se o campo for 'hardware', buscamos a instância do Hardware
            hardware = get_object_or_404(Hardware, id=value)
            setattr(computador, attr, hardware)  # Atribuímos a instância de Hardware
        else:
            setattr(computador, attr, value)  # Para os demais campos, fazemos a atribuição normal

    # Salvar as mudanças no banco de dados
    computador.save()

    # Retornar o computador atualizado com o ID de hardware no formato correto
    computador_dict = computador.__dict__.copy()
    computador_dict["hardware"] = computador.hardware.id  # Garante que o hardware seja um ID na resposta

    return computador_dict



@routerComputador.delete("/computadores/{computador_id}")
def delete_computador(request, computador_id: int):
    computador = get_object_or_404(Computador, id=computador_id)
    computador.delete()
    return {"success": True, "message": f"Computador com ID {computador_id} foi deletado com sucesso."}


# GET: Buscar todos os status
@routerStatus.get("/status", response=List[StatusSchema])
def get_all_status(request):
    return Status.objects.all()

# GET: Buscar um status pelo ID
@routerStatus.get("/status/{status_id}", response=StatusSchema)
def get_status_by_id(request, status_id: int):
    status = get_object_or_404(Status, id=status_id)
    return StatusSchema.from_orm(status)

# POST: Criar um novo status
@routerStatus.post("/status", response=StatusSchema)
def create_status(request, payload: StatusSchema):
    status = Status.objects.create(**payload.dict())
    return StatusSchema.from_orm(status)

# PUT: Atualizar um status existente pelo ID
@routerStatus.put("/status/{status_id}", response=StatusSchema)
def update_status(request, status_id: int, payload: StatusSchema):
    # Buscar a instância do Status com base no ID fornecido
    status = get_object_or_404(Status, id=status_id)
    
    # Iterar sobre os campos do payload e atualizar apenas os que não são 'id'
    for attr, value in payload.dict().items():
        if attr != 'id':  # Ignorar o campo 'id' para evitar a substituição
            setattr(status, attr, value)
    
    # Salvar as mudanças
    status.save()
    
    return StatusSchema.from_orm(status)

# DELETE: Deletar um status pelo ID
@routerStatus.delete("/status/{status_id}")
def delete_status(request, status_id: int):
    status = get_object_or_404(Status, id=status_id)
    status.delete()
    return {"success": True, "message": f"Status com ID {status_id} foi deletado com sucesso."}


@routerEstabelecimento.get("/estabelecimentos", response=List[BiEstabelecimentoSchema])
def get_all_estabelecimentos(request):
    estabelecimentos = BiEstabelecimento.objects.values(
        'estabelecimento', 'sigla_unidade', 'nome_unidade', 'endereco', 'bairro', 'cidade', 
        'estado', 'pais', 'regional', 'ie', 'nome_fantasia', 'cnpj'
    )
    return list(estabelecimentos)

@routerCentroCusto.get("/centro_custos", response=List[EsCentroCustoSchema])
def get_all_centro_custos(request):
    centro_custos = BiCentroCusto.objects.values('centrocusto', 'descricaocusto')
    return list(centro_custos)