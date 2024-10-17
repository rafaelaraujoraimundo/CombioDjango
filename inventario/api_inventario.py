from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .models import Hardware, Monitor, ProntuarioMonitor
from .schema import HardwareDetailSchema, HardwareSchema, MonitorSchema, MonitorOutSchema, ProntuarioMonitorSchema, ProntuarioMonitorCreateSchema
from datetime import datetime
# Inicializando o Router
routerHardware = Router()
routerMonitor = Router()

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
    return {"success": True}


# POST criar um novo prontuário
@routerMonitor.post("/monitors/prontuarios", response=ProntuarioMonitorSchema)
def create_prontuario(request, payload: ProntuarioMonitorCreateSchema):
    prontuario = ProntuarioMonitor.objects.create(**payload.dict())
    return prontuario

# PUT atualizar um prontuário existente
@routerMonitor.put("/monitors/prontuarios/{prontuario_id}", response=ProntuarioMonitorSchema)
def update_prontuario(request, prontuario_id: int, payload: ProntuarioMonitorCreateSchema):
    prontuario = get_object_or_404(ProntuarioMonitor, id=prontuario_id)
    for attr, value in payload.dict().items():
        setattr(prontuario, attr, value)
    prontuario.save()
    return prontuario

# DELETE remover um prontuário
@routerMonitor.delete("/monitors/prontuarios/{prontuario_id}")
def delete_prontuario(request, prontuario_id: int):
    prontuario = get_object_or_404(ProntuarioMonitor, id=prontuario_id)
    prontuario.delete()
    return {"success": True}


@routerMonitor.get("/monitors/prontuarios", response=List[ProntuarioMonitorSchema])
def get_all_prontuarios(request):
    print("Chamando todos os prontuários")
    return ProntuarioMonitor.objects.all()

@routerMonitor.get("/monitors/prontuarios/{prontuario_id}", response=ProntuarioMonitorSchema)
def get_prontuario_by_id(request, prontuario_id: int):
    prontuario = get_object_or_404(ProntuarioMonitor, id=prontuario_id)
    return prontuario

@routerMonitor.get("/monitors/{monitor_id}/prontuarios", response=List[ProntuarioMonitorSchema])
def get_prontuarios_by_monitor(request, monitor_id: int):
    prontuarios = ProntuarioMonitor.objects.filter(monitor__id=monitor_id)
    return prontuarios