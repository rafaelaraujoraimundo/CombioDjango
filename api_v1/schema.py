from pydantic import BaseModel, Field
from ninja import ModelSchema
from administration.models import ServidorFluig
from typing import List, Dict

# Create your models here.
class UserSchema(BaseModel):
    email: str
    usuario_datasul: str
    usuario_fluig: str
    is_active: bool
    is_staff: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class ServidorFluigSchema(ModelSchema):
    class Config:
        model = ServidorFluig
        model_fields = ['servidor', 'nome_servidor', 'client_key', 'consumer_secret', 'access_token', 'access_secret', 'url']




class DataSource(BaseModel):
    max_pool_size: int = Field(..., alias='max-pool-size')
    min_pool_size: int = Field(..., alias='min-pool-size')
    active_count: int = Field(..., alias='active-count')
    created_count: int = Field(..., alias='created-count')
    max_used_count: int = Field(..., alias='max-used-count')
    available_count: int = Field(..., alias='available-count')

class DatabaseInfo(BaseModel):
    databaseName: str
    databaseVersion: str
    driverName: str
    driverVersion: str

class ConnectedUsers(BaseModel):
    connectedUsers: int

class Memory(BaseModel):
    heap_memory_usage: int = Field(..., alias='heap-memory-usage')
    non_heap_memory_usage: int = Field(..., alias='non-heap-memory-usage')

class DatabaseTraffic(BaseModel):
    received: int
    sent: int

class DatabaseSize(BaseModel):
    size: int

class ArtifactApp(BaseModel):
    name: str
    md5: str

class DetailedMemoryUsage(BaseModel):
    init: int
    used: int
    committed: int
    max: int

class DetailedMemoryType(BaseModel):
    type: str
    usage: DetailedMemoryUsage
    peakUsage: DetailedMemoryUsage

class Runtime(BaseModel):
    startTime: int
    uptime: int

class Threading(BaseModel):
    count: int
    peakCount: int
    deamonCount: int
    totalStartedCount: int

class OperationSystem(BaseModel):
    server_memory_size: int = Field(..., alias='server-memory-size')
    server_memory_free: int = Field(..., alias='server-memory-free')
    server_hd_space: str = Field(..., alias='server-hd-space')
    server_hd_space_free: str = Field(..., alias='server-hd-space-free')
    server_core_system: int = Field(..., alias='server-core-system')
    server_arch_system: str = Field(..., alias='server-arch-system')
    server_temp_size: int = Field(..., alias='server-temp-size')
    server_log_size: int = Field(..., alias='server-log-size')
    heap_max_size: int = Field(..., alias='heap-max-size')
    heap_size: int = Field(..., alias='heap-size')
    system_uptime: int = Field(..., alias='system-uptime')

class ApiResponseFluig(BaseModel):
    DATA_SOURCE_FLUIGDS: DataSource
    DATA_SOURCE_FLUIGDSRO: DataSource
    DATABASE_INFO: DatabaseInfo
    CONNECTED_USERS: ConnectedUsers
    MEMORY: Memory
    DATABASE_TRAFFIC: DatabaseTraffic
    DATABASE_SIZE: DatabaseSize
    ARTIFACTS_APPS_DIR: List[ArtifactApp]
    ARTIFACTS_CORE_DIR: List[ArtifactApp]
    ARTIFACTS_SYSTEM_DIR: List[ArtifactApp]
    LOG_DIR_SIZE_MONITOR: Dict[str, str]
    TEMPLATE_DIR_SIZE: Dict[str, str]
    VOLUME_DIR_SIZE: Dict[str, str]
    TEMPORARY_DIR_SIZE: Dict[str, str]
    EXTERNAL_CONVERTER: Dict[str, bool]
    RUNTIME: Runtime
    THREADING: Threading
    DETAILED_MEMORY: Dict[str, DetailedMemoryType]
    OPERATION_SYSTEM: OperationSystem


class DatasetSchema(BaseModel):
    datasetId: str
    datasetDescription: str = None
    datasetImpl: str = None
    datasetBuilder: str
    active: bool
    draft: bool
    serverOffline: bool
    mobileCache: bool
    internal: bool
    custom: bool
    generated: bool
    offlineMobileCache: bool
    mobileOfflineSummary: str
    updateInterval: int
    lastReset: int
    lastRemoteSync: int
    jobLastExecution: str = None
    jobNextExecution: str = None
    type: str
    journalingAdherenceFull: bool
    journalingAdherenceHalf: bool
    journalingAdherenceNone: bool
    syncStatusSuccess: bool
    syncStatusWarning: bool
    syncStatusError: bool
    syncDetails: str = None