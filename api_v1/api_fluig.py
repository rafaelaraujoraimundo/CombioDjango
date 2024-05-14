from django.http import JsonResponse
from ninja import Router
from typing import List, Any
from administration.models import User, ServidorFluig
from api_v1.schema import DatasetSchema
from combio.settings import DATABASE_ROUTERS
from .schema import ApiResponseFluig, DatasetSchema
from ninja_jwt.authentication import JWTAuth
from django.utils import timezone
import datetime
import pytz
from requests_oauthlib import OAuth1Session
from .models import (FluigDatabaseInfo, FluigDatabaseSize, 
                     FluigRuntime, FluigOperationSystem, Dataset)
import json

from django.shortcuts import get_object_or_404

routerFLuig = Router()



@routerFLuig.get("/monitor", response=Any)
def get_FluigServer(request):
    servidoresFluig = ServidorFluig.objects.all()
    for servidorFluig in servidoresFluig:
        CLIENT_KEY = servidorFluig.client_key
        CONSUMER_SECRET = servidorFluig.consumer_secret
        ACCESS_TOKEN = servidorFluig.access_token
        ACCESS_SECRET = servidorFluig.access_secret
        body_json = None
        url = servidorFluig.url + '/monitoring/api/v1/statistics/report/'
        print(url)
        print(servidorFluig)
        oauth = OAuth1Session(CLIENT_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=ACCESS_TOKEN, resource_owner_secret=ACCESS_SECRET)
        response = oauth.get(url, data=body_json, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            response_data = response.json()
            api_response = ApiResponseFluig(**response_data)
            now =  datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))

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
            
    
  



        else:
            print('Erro na requisição:', response.status_code)
            print('Erro na requisição:', response)
            """for i in range(1, 21):  # 10 tentativas no máximo
            print('Tentativa', i)
            time.sleep(30)  # Aguarda 10 minutos (600 segundos)
            response = oauth.post(url, data=body_json, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                return response"""
        
            return 'Não foi possível obter uma resposta adequada após 10 tentativas.' 
    return api_response


@routerFLuig.get("/datasets", response=Any)
def get_datasets(request):
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
        now =  datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
        if response.status_code == 200:
            response_data = response.json()
            datasets = response_data.get("items", [])  # Assume que a chave dos datasets é "items"
            for dataset_data in datasets:
                if dataset_data.get("serverOffline") == True:# Aqui, você adaptaria os campos conforme definido no seu modelo `Dataset`
                    Dataset.objects.create(
                        servidor_fluig = servidorFluig,
                        datasetid = dataset_data["datasetId"],
                        datasetdescription = dataset_data.get("datasetDescription", ""),
                        datasetimpl = dataset_data.get("datasetimpl", ""),
                        datasetbuilder = dataset_data["datasetBuilder"],
                        active = dataset_data["active"],
                        draft = dataset_data["draft"],
                        serveroffline = dataset_data["serverOffline"],
                        mobilecache = dataset_data["mobileCache"],
                        internal = dataset_data["internal"],
                        custom = dataset_data["custom"],
                        generated = dataset_data["generated"],
                        offlinemobilecache = dataset_data["offlineMobileCache"],
                        mobileofflinesummary = dataset_data["mobileOfflineSummary"],
                        updateinterval = dataset_data["updateInterval"],
                        lastreset = dataset_data["lastReset"],
                        lastremotesync = dataset_data["lastRemoteSync"],
                        joblastexecution = dataset_data.get("jobLastExecution", ""),
                        jobnextexecution = dataset_data.get("jobNextExecution", ""),
                        type = dataset_data["type"],
                        journalingadherencefull = dataset_data["journalingAdherenceFull"],
                        journalingadherencehalf = dataset_data["journalingAdherenceHalf"],
                        journalingadherencenone = dataset_data["journalingAdherenceNone"],
                        syncstatussuccess = dataset_data["syncStatusSuccess"],
                        syncstatuswarning = dataset_data["syncStatusWarning"],
                        syncstatuserror = dataset_data["syncStatusError"],
                        syncdetails = dataset_data.get("syncDetails", ""),
                        created_at = now
                    )
                    # Aqui, cada dataset_data já é um dicionário, então podemos passá-lo diretamente
                    # validated_data = DatasetSchema(**dataset_data)
                    all_datasets.append(dataset_data)
        else:
            print('Erro na requisição:', response.status_code)
            # Tratamento de erro adequado aqui
    
    # A função agora retorna uma lista de datasets validados
    return all_datasets