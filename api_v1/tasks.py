from datetime import timezone
from requests_oauthlib import OAuth1Session
from administration.models import ServidorFluig, User
from api_v1.schema import DatasetSchema
from .models import (FluigDatabaseInfo, FluigDatabaseSize, 
                     FluigRuntime, FluigOperationSystem, Dataset)
from celery import shared_task

@shared_task(name='api_v1.tasks.get_FluigServer')
def get_FluigServer():
    servidoresFluig = ServidorFluig.objects.all()
    for servidorFluig in servidoresFluig:
        CLIENT_KEY = servidorFluig.client_key
        CONSUMER_SECRET = servidorFluig.consumer_secret
        ACCESS_TOKEN = servidorFluig.access_token
        ACCESS_SECRET = servidorFluig.access_secret
        body_json = None
        url = servidorFluig.url + '/monitoring/api/v1/statistics/report/'
        oauth = OAuth1Session(CLIENT_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=ACCESS_TOKEN, resource_owner_secret=ACCESS_SECRET)
        response = oauth.get(url, data=body_json, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            response_data = response.json()
            now = timezone.now()

            # Salvar DatabaseInfo
            db_info = response_data.get("DATABASE_INFO", {})
            FluigDatabaseInfo.objects.create(
                servidor_fluig=servidorFluig,
                database_name=db_info.get("databaseName", ""),
                database_version=db_info.get("databaseVersion", ""),
                driver_name=db_info.get("driverName", ""),
                driver_version=db_info.get("driverVersion", ""),
                created_at=now
            )

            # Salvar DatabaseSize
            db_size = response_data.get("DATABASE_SIZE", {})
            FluigDatabaseSize.objects.create(
                servidor_fluig=servidorFluig,
                size=db_size.get("size", 0),
                created_at=now
            )

            # Salvar Runtime
            runtime_data = response_data.get("RUNTIME", {})
            FluigRuntime.objects.create(
                servidor_fluig=servidorFluig,
                start_time=runtime_data.get("startTime", 0),
                uptime=runtime_data.get("uptime", 0),
                created_at=now
            )

            # Salvar OperationSystem
            op_system = response_data.get("OPERATION_SYSTEM", {})
            FluigOperationSystem.objects.create(
                servidor_fluig=servidorFluig,
                server_memory_size=op_system.get("server-memory-size", 0),
                server_memory_free=op_system.get("server-memory-free", 0),
                server_hd_space=op_system.get("server-hd-space", ""),
                server_hd_space_free=op_system.get("server-hd-space-free", ""),
                server_core_system=op_system.get("server-core-system", 0),
                server_arch_system=op_system.get("server-arch_system", ""),
                server_temp_size=op_system.get("server-temp-size", 0),
                server_log_size=op_system.get("server-log-size", 0),
                heap_max_size=op_system.get("heap-max-size", 0),
                heap_size=op_system.get("heap-size", 0),
                system_uptime=op_system.get("system-uptime", 0),
                created_at=now
            )
            print(f"Executado Dados do servidor: {now}")
            
@shared_task(name='api_v1.tasks.get_datasets')
def get_datasets():
    servidoresFluig = ServidorFluig.objects.all()
    all_datasets = []  # Esta lista armazenará todos os datasets validados
    for servidorFluig in servidoresFluig:
        CLIENT_KEY = servidorFluig.client_key
        CONSUMER_SECRET = servidorFluig.consumer_secret
        ACCESS_TOKEN = servidorFluig.access_token
        ACCESS_SECRET = servidorFluig.access_secret
        url = servidorFluig.url + '/dataset/api/v2/datasets'
        oauth = OAuth1Session(CLIENT_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=ACCESS_TOKEN, resource_owner_secret=ACCESS_SECRET)
        response = oauth.get(url, headers={'Content-Type': 'application/json'})
        now = timezone.now()
        if response.status_code == 200:
            response_data = response.json()
            datasets = response_data.get("items", [])  # Assume que a chave dos datasets é "items"
            for dataset_data in datasets:
                if dataset_data.get("serverOffline") == True:# Aqui, você adaptaria os campos conforme definido no seu modelo `Dataset`
                    Dataset.objects.create(
                        servidor_fluig=servidorFluig,
                        datasetId=dataset_data["datasetId"],
                        datasetDescription=dataset_data.get("datasetDescription", ""),
                        datasetImpl=dataset_data.get("datasetImpl", ""),
                        datasetBuilder=dataset_data["datasetBuilder"],
                        active=dataset_data["active"],
                        draft=dataset_data["draft"],
                        serverOffline=dataset_data["serverOffline"],
                        mobileCache=dataset_data["mobileCache"],
                        internal=dataset_data["internal"],
                        custom=dataset_data["custom"],
                        generated=dataset_data["generated"],
                        offlineMobileCache=dataset_data["offlineMobileCache"],
                        mobileOfflineSummary=dataset_data["mobileOfflineSummary"],
                        updateInterval=dataset_data["updateInterval"],
                        lastReset=dataset_data["lastReset"],
                        lastRemoteSync=dataset_data["lastRemoteSync"],
                        jobLastExecution=dataset_data.get("jobLastExecution", ""),
                        jobNextExecution=dataset_data.get("jobNextExecution", ""),
                        type=dataset_data["type"],
                        journalingAdherenceFull=dataset_data["journalingAdherenceFull"],
                        journalingAdherenceHalf=dataset_data["journalingAdherenceHalf"],
                        journalingAdherenceNone=dataset_data["journalingAdherenceNone"],
                        syncStatusSuccess=dataset_data["syncStatusSuccess"],
                        syncStatusWarning=dataset_data["syncStatusWarning"],
                        syncStatusError=dataset_data["syncStatusError"],
                        syncDetails=dataset_data.get("syncDetails", ""),
                        created_at=now
                    )
            print(f"Executado Dataset: {now}")
        else:
            print('Erro na requisição:', response.status_code)
