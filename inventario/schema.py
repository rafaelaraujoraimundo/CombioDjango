from ninja import Schema
from typing import List, Optional
from datetime import datetime
from datetime import date
# Schemas para os dados relacionados
class AccountInfoSchema(Schema):
    tag: Optional[str]
    fields_14: Optional[str]
    fields_3: Optional[str]
    fields_4: Optional[str]
    fields_5: Optional[str]
    fields_7: Optional[str]
    fields_8: Optional[str]
    fields_9: Optional[str]

class BiosSchema(Schema):
    asset_tag: Optional[str]
    bdate: Optional[str]
    bmanufacturer: Optional[str]
    bversion: Optional[str]
    mmanufacturer: Optional[str]
    mmodel: Optional[str]
    msn: Optional[str]
    smanufacturer: Optional[str]
    smodel: Optional[str]
    ssn: Optional[str]
    type: Optional[str]

class CPUSchema(Schema):
    cores: Optional[int]
    cpu_arch: Optional[str]
    current_address_width: Optional[int]
    current_speed: Optional[str]
    data_width: Optional[int]
    l2_cache_size: Optional[str]
    logical_cpus: Optional[int]
    manufacturer: Optional[str]
    serial_number: Optional[str]
    socket: Optional[str]
    speed: Optional[str]
    type: Optional[str]
    voltage: Optional[str]

class MemorySchema(Schema):
    capacity: Optional[int]
    caption: Optional[str]
    description: Optional[str]
    num_slots: Optional[int]
    purpose: Optional[str]
    serial_number: Optional[str]
    speed: Optional[str]
    type: Optional[str]

class SoftwareSchema(Schema):
    architecture: Optional[str]
    bitswidth: Optional[int]
    comments: Optional[str]
    filename: Optional[str]
    filesize: Optional[int]
    folder: Optional[str]
    guid: Optional[str]
    install_date: Optional[str]  # Vamos garantir que a data esteja como string
    language: Optional[str]
    name_id: Optional[int]
    publisher_id: Optional[int]
    source: Optional[int]
    version_id: Optional[int]

class StorageSchema(Schema):
    description: Optional[str]
    disk_size: Optional[int]
    firmware: Optional[str]
    manufacturer: Optional[str]
    model: Optional[str]
    name: Optional[str]
    serial_number: Optional[str]
    type: Optional[str]

# Schema para o Hardware completo
class HardwareDetailSchema(Schema):
    arch: Optional[str]
    archive: Optional[str]
    category_id: Optional[int]
    checksum: Optional[int]
    default_gateway: Optional[str]
    description: Optional[str]
    device_id: Optional[str]
    dns: Optional[str]
    etime: Optional[str]
    fidelity: Optional[int]
    ipaddr: Optional[str]
    ipsrc: Optional[str]
    last_come: Optional[str]  # Certifique-se de que as datas sejam strings
    last_date: Optional[str]
    memory: Optional[int]
    name: Optional[str]
    os_comments: Optional[str]
    os_name: Optional[str]
    os_version: Optional[str]
    processor_n: Optional[int]
    processors: Optional[int]
    processor_t: Optional[str]
    quality: Optional[str]
    sstate: Optional[int]
    swap: Optional[int]
    type: Optional[int]
    user_agent: Optional[str]
    user_domain: Optional[str]
    user_id: Optional[str]
    uuid: Optional[str]
    win_company: Optional[str]
    win_owner: Optional[str]
    win_prod_id: Optional[str]
    win_prod_key: Optional[str]
    workgroup: Optional[str]
    bios: List[BiosSchema]
    cpus: List[CPUSchema]
    memories: List[MemorySchema]
    software: List[SoftwareSchema]
    storages: List[StorageSchema]
    accountinfo: List[AccountInfoSchema]


class HardwareSchema(Schema):
    id: int
    arch: Optional[str] = None
    archive: Optional[str] = None
    category_id: Optional[int] = None
    checksum: Optional[int] = None
    default_gateway: Optional[str] = None
    description: Optional[str] = None
    device_id: Optional[str] = None
    dns: Optional[str] = None
    etime: Optional[str] = None
    fidelity: Optional[int] = None
    ipaddr: Optional[str] = None
    ipsrc: Optional[str] = None
    last_come: Optional[str] = None  # A data será tratada como string, convertida se necessária
    last_date: Optional[str] = None
    memory: Optional[int] = None
    name: Optional[str] = None
    os_comments: Optional[str] = None
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    processor_n: Optional[int] = None
    processors: Optional[int] = None
    processor_t: Optional[str] = None
    quality: Optional[str] = None
    sstate: Optional[int] = None
    swap: Optional[int] = None
    type: Optional[int] = None
    user_agent: Optional[str] = None
    user_domain: Optional[str] = None
    user_id: Optional[str] = None
    uuid: Optional[str] = None
    win_company: Optional[str] = None
    win_owner: Optional[str] = None
    win_prod_id: Optional[str] = None
    win_prod_key: Optional[str] = None
    workgroup: Optional[str] = None



    # Schema Monitor
class MonitorSchema(Schema):
    numero_serie: str
    fabricante: str
    modelo: str
    patrimonio: str
    unidade: str
    local: str
    status: str

# Schema para buscar Monitor (incluindo o ID)
class MonitorOutSchema(MonitorSchema):
    id: int


class ProntuarioMonitorSchema(Schema):
    id: int
    monitor: int
    usuario: str
    data: date
    motivo_ocorrencia: str
    unidade_destino: str
    local_destino: str
    status: str
    observacao: str = None

class ProntuarioMonitorCreateSchema(Schema):
    monitor: int
    usuario: str
    data: date
    motivo_ocorrencia: str
    unidade_destino: str
    local_destino: str
    status: str
    observacao: str = None