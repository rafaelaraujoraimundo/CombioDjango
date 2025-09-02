import django.conf
from django.db.models import Sum
from django.utils import timezone
from celery import shared_task
import requests
from requests.auth import HTTPBasicAuth
import logging
from administration.views import User
from .models import AccountInfo, BIOS, CPU, Hardware, Memory, Software, Storage, Computador
from decouple import config
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
import json
import time
import socket
from io import BytesIO
import MySQLdb




logger = logging.getLogger(__name__)
@shared_task
def populate_hardware_data():
    # Configurações de conexão do banco OCS
    db_config = {
        'host': '172.16.0.15',
        'port': 3308,
        'db': 'ocsweb',  # mysqlclient usa 'db' ao invés de 'database'
        'user': 'ocsuser',
        'passwd': 'ocspass',  # mysqlclient usa 'passwd' ao invés de 'password'
        'charset': 'utf8mb4',
        'use_unicode': True,
        'autocommit': True
    }
    
    connection = None
    
    try:
        print("Inicio do populate_hardware_data - Conexão direta ao banco")
        
        # Conectar ao banco OCS usando mysqlclient
        connection = MySQLdb.connect(**db_config)
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)  # Para retornar dicionários
        
        print("Conexão com banco OCS estabelecida")
        
        # 1. Buscar todos os computadores (equivalente à consulta principal da API)
        hardware_query = """
            SELECT 
                ID, NAME, ARCH, CHECKSUM, DEFAULTGATEWAY, DESCRIPTION, 
                DEVICEID, DNS, FIDELITY, IPADDR, IPSRC, LASTCOME, LASTDATE,
                MEMORY, OSNAME, OSVERSION, PROCESSORN, PROCESSORS, PROCESSORT,
                QUALITY, SWAP, UUID, WINOWNER, WINPRODID, WINPRODKEY, WORKGROUP
            FROM hardware 
            WHERE DEVICEID <> '_SYSTEMGROUP_' 
                AND NAME NOT LIKE '%LG%' 
                AND NAME NOT LIKE '%MONITOR%' 
                AND NAME NOT LIKE '%Monitor%' 
                AND NAME NOT LIKE '%22MK400H%'
                AND NAME NOT LIKE '%AOC%'
                AND NAME NOT LIKE '%AOC%'
                AND NAME NOT LIKE '%Samsung%'
            ORDER BY ID 
            LIMIT 1000 OFFSET 0
        """
        
        cursor.execute(hardware_query)
        hardware_data = cursor.fetchall()
        
        quantidade = len(hardware_data)
        print(f"Quantidade de computadores encontrados: {quantidade}")
        
        # Processar cada computador
        for computer in hardware_data:
            computer_id = computer['ID']
            
            print(f"Processando computador ID: {computer_id} - {computer.get('NAME', 'N/A')}")
            
            # Função para converter datas
            def convert_to_aware(date_value):
                if date_value and isinstance(date_value, datetime):
                    return timezone.make_aware(date_value) if timezone.is_naive(date_value) else date_value
                elif date_value and isinstance(date_value, str):
                    try:
                        dt = datetime.strptime(date_value, "%Y-%m-%d %H:%M:%S")
                        return timezone.make_aware(dt)
                    except (ValueError, TypeError):
                        return None
                return None

            # Simular estrutura da API: computer_data["hardware"]
            # Na API, os dados vêm como: computer_data["hardware"].get("CAMPO")
            # Aqui criamos a mesma estrutura
            computer_data = {
                "hardware": computer  # Usar os dados do hardware diretamente
            }

            # Converter datas
            last_come = convert_to_aware(computer_data["hardware"].get("LASTCOME"))
            last_date = convert_to_aware(computer_data["hardware"].get("LASTDATE"))
            
            # Criar/atualizar hardware
            hardware, created = Hardware.objects.update_or_create(
                name=computer.get("NAME"),
                defaults={
                    "arch": computer.get("ARCH"),
                    "checksum": computer.get("CHECKSUM"),
                    "default_gateway": computer.get("DEFAULTGATEWAY"),
                    "description": computer.get("DESCRIPTION"),
                    "device_id": computer.get("DEVICEID"),
                    "dns": computer.get("DNS"),
                    "fidelity": computer.get("FIDELITY"),
                    "ipaddr": computer.get("IPADDR"),
                    "ipsrc": computer.get("IPSRC"),
                    "last_come": last_come,
                    "last_date": last_date,
                    "memory": computer.get("MEMORY"),
                    "name": computer.get("NAME"),
                    "os_name": computer.get("OSNAME"),
                    "os_version": computer.get("OSVERSION"),
                    "processor_n": computer.get("PROCESSORN"),
                    "processors": computer.get("PROCESSORS"),
                    "processor_t": computer.get("PROCESSORT"),
                    "quality": computer.get("QUALITY"),
                    "swap": computer.get("SWAP"),
                    "uuid": computer.get("UUID"),
                    "win_owner": computer.get("WINOWNER"),
                    "win_prod_id": computer.get("WINPRODID"),
                    "win_prod_key": computer.get("WINPRODKEY"),
                    "workgroup": computer.get("WORKGROUP")
                }
            )


            # Buscar todos os dados relacionados e organizar como a API
            computer_data["bios"] = []
            computer_data["cpus"] = []  
            computer_data["memories"] = []
            computer_data["software"] = []
            computer_data["storages"] = []
            computer_data["accountinfo"] = []

            # 2. BUSCAR DADOS DE BIOS
            bios_query = """
                SELECT 
                    ASSETTAG, BDATE, BMANUFACTURER, BVERSION, MMANUFACTURER,
                    MMODEL, MSN, SMANUFACTURER, SMODEL, SSN, TYPE
                FROM bios 
                WHERE HARDWARE_ID = %s
            """
            cursor.execute(bios_query, (computer_id,))
            computer_data["bios"] = cursor.fetchall()

            # 3. BUSCAR DADOS DE CPUs
            cpu_query = """
                SELECT 
                    CORES, CPUARCH, CURRENT_ADDRESS_WIDTH, CURRENT_SPEED,
                    DATA_WIDTH, L2CACHESIZE, LOGICAL_CPUS, MANUFACTURER,
                    SERIALNUMBER, SOCKET, SPEED, TYPE, VOLTAGE
                FROM cpus 
                WHERE HARDWARE_ID = %s
            """
            cursor.execute(cpu_query, (computer_id,))
            computer_data["cpus"] = cursor.fetchall()

            # 4. BUSCAR DADOS DE MEMÓRIAS
            memory_query = """
                SELECT 
                    CAPACITY, CAPTION, DESCRIPTION, NUMSLOTS, PURPOSE,
                    SERIALNUMBER, SPEED, TYPE
                FROM memories 
                WHERE HARDWARE_ID = %s
            """
            cursor.execute(memory_query, (computer_id,))
            computer_data["memories"] = cursor.fetchall()

            # 5. BUSCAR DADOS DE SOFTWARE (exatamente como a API retorna)
            software_query = """
                SELECT 
                    s.ID, s.HARDWARE_ID, s.ARCHITECTURE, s.BITSWIDTH, s.COMMENTS,
                    s.FILENAME, s.FILESIZE, s.FOLDER, s.GUID, s.LANGUAGE, 
                    s.INSTALLDATE, s.SOURCE, s.NAME_ID, s.PUBLISHER_ID, s.VERSION_ID
                FROM software s
                WHERE s.HARDWARE_ID = %s
            """
            cursor.execute(software_query, (computer_id,))
            computer_data["software"] = cursor.fetchall()

            # 6. BUSCAR DADOS DE STORAGE
            storage_query = """
                SELECT 
                    DESCRIPTION, DISKSIZE, FIRMWARE, MANUFACTURER,
                    MODEL, NAME, SERIALNUMBER, TYPE
                FROM storages 
                WHERE HARDWARE_ID = %s
            """
            cursor.execute(storage_query, (computer_id,))
            computer_data["storages"] = cursor.fetchall()

            # 7. BUSCAR DADOS DE ACCOUNTINFO
            accountinfo_query = """
                SELECT 
                    TAG, fields_14, fields_3, fields_4, fields_5,
                    fields_7, fields_8, fields_9
                FROM accountinfo 
                WHERE HARDWARE_ID = %s
            """
            cursor.execute(accountinfo_query, (computer_id,))
            computer_data["accountinfo"] = cursor.fetchall()

            # Agora processa exatamente como a função original da API
            # Remover dados antigos das tabelas relacionadas antes de inserir novos
            hardware.bios.all().delete()
            hardware.cpus.all().delete()
            hardware.memories.all().delete()
            hardware.software.all().delete()
            hardware.storages.all().delete()
            hardware.accountinfo.all().delete()

            # Inserir novos dados para BIOS
            for bios_data in computer_data.get("bios", []):
                BIOS.objects.create(
                    hardware=hardware,
                    asset_tag=bios_data.get("ASSETTAG"),
                    bdate=bios_data.get("BDATE"),
                    bmanufacturer=bios_data.get("BMANUFACTURER"),
                    bversion=bios_data.get("BVERSION"),
                    mmanufacturer=bios_data.get("MMANUFACTURER"),
                    mmodel=bios_data.get("MMODEL"),
                    msn=bios_data.get("MSN"),
                    smanufacturer=bios_data.get("SMANUFACTURER"),
                    smodel=bios_data.get("SMODEL"),
                    ssn=bios_data.get("SSN"),
                    type=bios_data.get("TYPE")
                )

            # Inserir novos dados para CPUs
            for cpu_data in computer_data.get("cpus", []):
                CPU.objects.create(
                    hardware=hardware,
                    cores=cpu_data.get("CORES"),
                    cpu_arch=cpu_data.get("CPUARCH"),
                    current_address_width=cpu_data.get("CURRENT_ADDRESS_WIDTH"),
                    current_speed=cpu_data.get("CURRENT_SPEED"),
                    data_width=cpu_data.get("DATA_WIDTH"),
                    l2_cache_size=cpu_data.get("L2CACHESIZE"),
                    logical_cpus=cpu_data.get("LOGICAL_CPUS"),
                    manufacturer=cpu_data.get("MANUFACTURER"),
                    serial_number=cpu_data.get("SERIALNUMBER"),
                    socket=cpu_data.get("SOCKET"),
                    speed=cpu_data.get("SPEED"),
                    type=cpu_data.get("TYPE"),
                    voltage=cpu_data.get("VOLTAGE")
                )

            # Inserir novos dados para Memórias
            for memory_data in computer_data.get("memories", []):
                Memory.objects.create(
                    hardware=hardware,
                    capacity=memory_data.get("CAPACITY"),
                    caption=memory_data.get("CAPTION"),
                    description=memory_data.get("DESCRIPTION"),
                    num_slots=memory_data.get("NUMSLOTS"),
                    purpose=memory_data.get("PURPOSE"),
                    serial_number=memory_data.get("SERIALNUMBER"),
                    speed=memory_data.get("SPEED"),
                    type=memory_data.get("TYPE")
                )

            # Inserir novos dados para Software
            for software_data in computer_data.get("software", []):
                install_date = convert_to_aware(software_data.get("INSTALLDATE"))
                Software.objects.create(
                    hardware=hardware,
                    architecture=software_data.get("ARCHITECTURE"),
                    bitswidth=software_data.get("BITSWIDTH"),
                    comments=software_data.get("COMMENTS"),
                    filename=software_data.get("FILENAME"),
                    filesize=software_data.get("FILESIZE"),
                    folder=software_data.get("FOLDER"),
                    guid=software_data.get("GUID"),
                    install_date=install_date,
                    language=software_data.get("LANGUAGE"),
                    name_id=software_data.get("NAME_ID"),
                    publisher_id=software_data.get("PUBLISHER_ID"),
                    source=software_data.get("SOURCE"),
                    version_id=software_data.get("VERSION_ID")
                )

            # Inserir novos dados para Armazenamento (Storages)
            for storage_data in computer_data.get("storages", []):
                Storage.objects.create(
                    hardware=hardware,
                    description=storage_data.get("DESCRIPTION"),
                    disk_size=storage_data.get("DISKSIZE"),
                    firmware=storage_data.get("FIRMWARE"),
                    manufacturer=storage_data.get("MANUFACTURER"),
                    model=storage_data.get("MODEL"),
                    name=storage_data.get("NAME"),
                    serial_number=storage_data.get("SERIALNUMBER"),
                    type=storage_data.get("TYPE")
                )

            # Inserir novos dados para AccountInfo
            for accountinfo_data in computer_data.get("accountinfo", []):
                AccountInfo.objects.create(
                    hardware=hardware,
                    tag=accountinfo_data.get("TAG"),
                    fields_14=accountinfo_data.get("fields_14"),
                    fields_3=accountinfo_data.get("fields_3"),
                    fields_4=accountinfo_data.get("fields_4"),
                    fields_5=accountinfo_data.get("fields_5"),
                    fields_7=accountinfo_data.get("fields_7"),
                    fields_8=accountinfo_data.get("fields_8"),
                    fields_9=accountinfo_data.get("fields_9")
                )
            comp = Computador.objects.filter(hardware=hardware).first()
            if comp:
                # BIOS principal (assumindo 1 registro relevante)
                bios = hardware.bios.first()  # related_name="bios" no model
                # Soma do tamanho dos discos (MB) — igual ao que você usa na view
                total_hd_mb = hardware.storages.aggregate(total=Sum('disk_size'))['total'] or 0

                comp.hostname = hardware.name or comp.hostname
                comp.fabricante = (bios.mmanufacturer if bios and bios.mmanufacturer else comp.fabricante)
                comp.modelo = (
                    " ".join(filter(None, [
                        bios.mmodel if bios else None,
                        bios.smodel if bios else None
                    ])).strip() or comp.modelo
                )
                comp.numero_serie = (bios.ssn if bios and bios.ssn else comp.numero_serie)
                comp.processador = hardware.processor_t or comp.processador
                comp.memoria = str(hardware.memory) if hardware.memory not in (None, "") else comp.memoria
                comp.hd = str(total_hd_mb) if total_hd_mb else comp.hd  # mantém em MB, como na tela
                comp.sistema_operacional = hardware.os_name or comp.sistema_operacional

                comp.save()

            print(f"Computador {computer.get('NAME')} processado com sucesso")
        
        print("Fim do populate_hardware_data")
        logger.info("Fim do populate_hardware_data")
        logger.info("Dados de hardware e componentes atualizados com sucesso via conexão direta!")
        
    except MySQLdb.Error as db_error:
        logger.error(f"Erro de banco de dados MySQLdb: {str(db_error)}")
        raise
        
    except Exception as e:
        logger.error(f"Erro ao processar os dados do banco: {str(e)}")
        logger.exception("Exceção completa:")
        raise
        
    finally:
        # Fechar conexão
        if connection:
            try:
                cursor.close()
                connection.close()
                print("Conexão com banco OCS fechada")
            except:
                pass


@shared_task
def populate_hardware_data_api():
    url = "http://172.16.0.15/ocsapi/v1/computers?start=&limit=1000"
    username = config("OCS_USER")
    password = config("OCS_PASSWORD")

    try:
        print("Inicio do populate_hardware_data")
        
        # Estratégia 1: Configuração de socket customizada
        original_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(1800)  # 30 minutos
        
        # Configurar adaptador customizado para arquivos grandes
        session = requests.Session()
        
        # Headers específicos para evitar problemas
        headers = {
            'User-Agent': 'OCS-API-Client/1.0',
            'Accept': 'application/json',
            'Accept-Encoding': 'identity',  # Sem compressão
            'Connection': 'close',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        response_data = None
        
        # Estratégia 1: Usando urllib diretamente (mais baixo nível)
        try:
            print("Tentativa 1: urllib direto")
            import urllib.request
            import urllib.parse
            import base64
            
            # Preparar autenticação
            credentials = f"{username}:{password}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            # Criar request
            req = urllib.request.Request(url)
            req.add_header('Authorization', f'Basic {encoded_credentials}')
            req.add_header('Accept', 'application/json')
            req.add_header('Accept-Encoding', 'identity')
            req.add_header('Connection', 'close')
            
            # Fazer a requisição
            with urllib.request.urlopen(req, timeout=1800) as response:
                # Ler em chunks pequenos
                data = BytesIO()
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    data.write(chunk)
                
                response_data = json.loads(data.getvalue().decode('utf-8'))
                print("Sucesso com urllib!")
                
        except Exception as e:
            print(f"Falha urllib: {e}")
            
            # Estratégia 2: requests com configuração TCP personalizada
            try:
                print("Tentativa 2: requests com TCP customizado")
                
                # Configurar TCP keepalive
                import urllib3
                
                # Desabilitar warnings de SSL
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                
                # Configurar pool manager customizado
                http = urllib3.PoolManager(
                    num_pools=1,
                    maxsize=1,
                    block=True,
                    timeout=urllib3.Timeout(connect=30, read=1800),
                    retries=urllib3.Retry(
                        total=3,
                        connect=2,
                        read=3,
                        backoff_factor=2,
                        status_forcelist=[500, 502, 503, 504]
                    )
                )
                
                # Preparar headers com autenticação
                auth_string = base64.b64encode(f"{username}:{password}".encode()).decode()
                headers_with_auth = {
                    'Authorization': f'Basic {auth_string}',
                    'Accept': 'application/json',
                    'Accept-Encoding': 'identity',
                    'Connection': 'close',
                    'User-Agent': 'urllib3-client'
                }
                
                # Fazer requisição
                response = http.request('GET', url, headers=headers_with_auth)
                
                if response.status == 200:
                    response_data = json.loads(response.data.decode('utf-8'))
                    print("Sucesso com urllib3!")
                else:
                    print(f"Status HTTP: {response.status}")
                    
            except Exception as e2:
                print(f"Falha urllib3: {e2}")
                
                # Estratégia 3: httpx (alternativa ao requests)
                try:
                    print("Tentativa 3: httpx")
                    import httpx
                    
                    with httpx.Client(
                        timeout=httpx.Timeout(30.0, read=1800.0),
                        limits=httpx.Limits(max_connections=1, max_keepalive_connections=0),
                        headers={'Connection': 'close'}
                    ) as client:
                        response = client.get(
                            url,
                            auth=(username, password),
                            headers={
                                'Accept': 'application/json',
                                'Accept-Encoding': 'identity'
                            }
                        )
                        
                        if response.status_code == 200:
                            response_data = response.json()
                            print("Sucesso com httpx!")
                            
                except ImportError:
                    print("httpx não disponível")
                except Exception as e3:
                    print(f"Falha httpx: {e3}")
                    
                    # Estratégia 4: requests com stream e buffer manual
                    try:
                        print("Tentativa 4: requests com buffer manual")
                        
                        # Configurar sessão com parâmetros específicos
                        adapter = requests.adapters.HTTPAdapter(
                            pool_connections=1,
                            pool_maxsize=1,
                            max_retries=0  # Sem retry automático
                        )
                        
                        session.mount('http://', adapter)
                        session.mount('https://', adapter)
                        
                        # Configurar keep-alive
                        session.headers.update({'Connection': 'close'})
                        
                        response = session.get(
                            url,
                            auth=HTTPBasicAuth(username, password),
                            headers=headers,
                            stream=True,
                            timeout=(60, None)  # Sem timeout de read
                        )
                        
                        if response.status_code == 200:
                            # Buffer manual com controle de erro
                            content_buffer = BytesIO()
                            total_read = 0
                            chunk_size = 4096
                            
                            try:
                                for chunk in response.iter_content(chunk_size=chunk_size, decode_unicode=False):
                                    if chunk:
                                        content_buffer.write(chunk)
                                        total_read += len(chunk)
                                        
                                        # Log do progresso a cada 1MB
                                        if total_read % (1024 * 1024) == 0:
                                            print(f"Lidos: {total_read / (1024*1024):.1f} MB")
                                
                                # Processar JSON
                                content_buffer.seek(0)
                                response_data = json.loads(content_buffer.read().decode('utf-8'))
                                print(f"Sucesso! Total lido: {total_read / (1024*1024):.1f} MB")
                                
                            except Exception as chunk_error:
                                print(f"Erro durante leitura: {chunk_error}")
                                # Tentar usar o que já foi lido
                                if total_read > 1024 * 1024:  # Se leu mais de 1MB
                                    try:
                                        content_buffer.seek(0)
                                        partial_data = content_buffer.read().decode('utf-8')
                                        # Tentar encontrar JSON válido
                                        if partial_data.endswith('}'):
                                            response_data = json.loads(partial_data)
                                            print("Recuperado JSON parcial!")
                                    except:
                                        pass
                                        
                    except Exception as e4:
                        print(f"Falha requests manual: {e4}")
                        
                        # Estratégia 5: Baixar para arquivo temporário
                        try:
                            print("Tentativa 5: download para arquivo temporário")
                            import tempfile
                            import os
                            
                            with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
                                temp_filename = temp_file.name
                                
                                # Usar wget ou curl se disponível
                                import subprocess
                                
                                # Tentar curl primeiro
                                try:
                                    curl_cmd = [
                                        'curl',
                                        '-u', f"{username}:{password}",
                                        '-H', 'Accept: application/json',
                                        '-H', 'Accept-Encoding: identity',
                                        '-H', 'Connection: close',
                                        '--max-time', '1800',
                                        '--retry', '3',
                                        '--retry-delay', '5',
                                        '-o', temp_filename,
                                        url
                                    ]
                                    
                                    result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=1800)
                                    
                                    if result.returncode == 0:
                                        with open(temp_filename, 'r', encoding='utf-8') as f:
                                            response_data = json.load(f)
                                        print("Sucesso com curl!")
                                    else:
                                        print(f"Curl falhou: {result.stderr}")
                                        
                                except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError) as curl_error:
                                    print(f"Curl não disponível ou falhou: {curl_error}")
                                
                                # Cleanup
                                try:
                                    os.unlink(temp_filename)
                                except:
                                    pass
                                    
                        except Exception as e5:
                            print(f"Falha download temporário: {e5}")
                            raise Exception("Todas as estratégias falharam")
        
        # Verificar se conseguimos dados
        if response_data is None:
            raise Exception("Não foi possível obter dados da API")
        
        print("Retorno da API - OK")
        quantidade = len(response_data)
        print(f"Quantidade de computadores: {quantidade}")

        # Processar os dados (mantém o código original)
        for computer_id, computer_data in response_data.items():
            
            # Converte campos de data para timezone-aware
            def convert_to_aware(date_str):
                if date_str:
                    try:
                        return timezone.make_aware(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"))
                    except (ValueError, TypeError):
                        return None
                return None

            # Converte os campos datetime para timezone-aware
            last_come = convert_to_aware(computer_data["hardware"].get("LASTCOME"))
            last_date = convert_to_aware(computer_data["hardware"].get("LASTDATE"))
            
            hardware, created = Hardware.objects.update_or_create(
                name=computer_data["hardware"].get("NAME"),
                defaults={
                    "arch": computer_data["hardware"].get("ARCH"),
                    "checksum": computer_data["hardware"].get("CHECKSUM"),
                    "default_gateway": computer_data["hardware"].get("DEFAULTGATEWAY"),
                    "description": computer_data["hardware"].get("DESCRIPTION"),
                    "device_id": computer_data["hardware"].get("DEVICEID"),
                    "dns": computer_data["hardware"].get("DNS"),
                    "fidelity": computer_data["hardware"].get("FIDELITY"),
                    "ipaddr": computer_data["hardware"].get("IPADDR"),
                    "ipsrc": computer_data["hardware"].get("IPSRC"),
                    "last_come": last_come,
                    "last_date": last_date,
                    "memory": computer_data["hardware"].get("MEMORY"),
                    "name": computer_data["hardware"].get("NAME"),
                    "os_name": computer_data["hardware"].get("OSNAME"),
                    "os_version": computer_data["hardware"].get("OSVERSION"),
                    "processor_n": computer_data["hardware"].get("PROCESSORN"),
                    "processors": computer_data["hardware"].get("PROCESSORS"),
                    "processor_t": computer_data["hardware"].get("PROCESSORT"),
                    "quality": computer_data["hardware"].get("QUALITY"),
                    "swap": computer_data["hardware"].get("SWAP"),
                    "uuid": computer_data["hardware"].get("UUID"),
                    "win_owner": computer_data["hardware"].get("WINOWNER"),
                    "win_prod_id": computer_data["hardware"].get("WINPRODID"),
                    "win_prod_key": computer_data["hardware"].get("WINPRODKEY"),
                    "workgroup": computer_data["hardware"].get("WORKGROUP")
                }
            )


            # Remover dados antigos das tabelas relacionadas antes de inserir novos
            hardware.bios.all().delete()
            hardware.cpus.all().delete()
            hardware.memories.all().delete()
            hardware.software.all().delete()
            hardware.storages.all().delete()
            hardware.accountinfo.all().delete()

            # Inserir novos dados para BIOS
            for bios_data in computer_data.get("bios", []):
                BIOS.objects.create(
                    hardware=hardware,
                    asset_tag=bios_data.get("ASSETTAG"),
                    bdate=bios_data.get("BDATE"),
                    bmanufacturer=bios_data.get("BMANUFACTURER"),
                    bversion=bios_data.get("BVERSION"),
                    mmanufacturer=bios_data.get("MMANUFACTURER"),
                    mmodel=bios_data.get("MMODEL"),
                    msn=bios_data.get("MSN"),
                    smanufacturer=bios_data.get("SMANUFACTURER"),
                    smodel=bios_data.get("SMODEL"),
                    ssn=bios_data.get("SSN"),
                    type=bios_data.get("TYPE")
                )

            # Inserir novos dados para CPUs
            for cpu_data in computer_data.get("cpus", []):
                CPU.objects.create(
                    hardware=hardware,
                    cores=cpu_data.get("CORES"),
                    cpu_arch=cpu_data.get("CPUARCH"),
                    current_address_width=cpu_data.get("CURRENT_ADDRESS_WIDTH"),
                    current_speed=cpu_data.get("CURRENT_SPEED"),
                    data_width=cpu_data.get("DATA_WIDTH"),
                    l2_cache_size=cpu_data.get("L2CACHESIZE"),
                    logical_cpus=cpu_data.get("LOGICAL_CPUS"),
                    manufacturer=cpu_data.get("MANUFACTURER"),
                    serial_number=cpu_data.get("SERIALNUMBER"),
                    socket=cpu_data.get("SOCKET"),
                    speed=cpu_data.get("SPEED"),
                    type=cpu_data.get("TYPE"),
                    voltage=cpu_data.get("VOLTAGE")
                )

            # Inserir novos dados para Memórias
            for memory_data in computer_data.get("memories", []):
                Memory.objects.create(
                    hardware=hardware,
                    capacity=memory_data.get("CAPACITY"),
                    caption=memory_data.get("CAPTION"),
                    description=memory_data.get("DESCRIPTION"),
                    num_slots=memory_data.get("NUMSLOTS"),
                    purpose=memory_data.get("PURPOSE"),
                    serial_number=memory_data.get("SERIALNUMBER"),
                    speed=memory_data.get("SPEED"),
                    type=memory_data.get("TYPE")
                )

            # Inserir novos dados para Software
            for software_data in computer_data.get("software", []):
                install_date = convert_to_aware(software_data.get("INSTALLDATE"))
                Software.objects.create(
                    hardware=hardware,
                    architecture=software_data.get("ARCHITECTURE"),
                    bitswidth=software_data.get("BITSWIDTH"),
                    comments=software_data.get("COMMENTS"),
                    filename=software_data.get("FILENAME"),
                    filesize=software_data.get("FILESIZE"),
                    folder=software_data.get("FOLDER"),
                    guid=software_data.get("GUID"),
                    install_date=install_date,
                    language=software_data.get("LANGUAGE"),
                    name_id=software_data.get("NAME_ID"),
                    publisher_id=software_data.get("PUBLISHER_ID"),
                    source=software_data.get("SOURCE"),
                    version_id=software_data.get("VERSION_ID")
                )

            # Inserir novos dados para Armazenamento (Storages)
            for storage_data in computer_data.get("storages", []):
                Storage.objects.create(
                    hardware=hardware,
                    description=storage_data.get("DESCRIPTION"),
                    disk_size=storage_data.get("DISKSIZE"),
                    firmware=storage_data.get("FIRMWARE"),
                    manufacturer=storage_data.get("MANUFACTURER"),
                    model=storage_data.get("MODEL"),
                    name=storage_data.get("NAME"),
                    serial_number=storage_data.get("SERIALNUMBER"),
                    type=storage_data.get("TYPE")
                )

            # Inserir novos dados para AccountInfo
            for accountinfo_data in computer_data.get("accountinfo", []):
                AccountInfo.objects.create(
                    hardware=hardware,
                    tag=accountinfo_data.get("TAG"),
                    fields_14=accountinfo_data.get("fields_14"),
                    fields_3=accountinfo_data.get("fields_3"),
                    fields_4=accountinfo_data.get("fields_4"),
                    fields_5=accountinfo_data.get("fields_5"),
                    fields_7=accountinfo_data.get("fields_7"),
                    fields_8=accountinfo_data.get("fields_8"),
                    fields_9=accountinfo_data.get("fields_9")
                )
            comp = Computador.objects.filter(hardware=hardware).first()
            if comp:
                   # BIOS principal (assumindo 1 registro relevante)
                   bios = hardware.bios.first()  # related_name="bios" no model
                   # Soma do tamanho dos discos (MB) — igual ao que você usa na view
                   total_hd_mb = hardware.storages.aggregate(total=Sum('disk_size'))['total'] or 0
                   #comp.hostname = hardware.name or comp.hostname
                   comp.fabricante = (bios.mmanufacturer if bios and bios.mmanufacturer else comp.fabricante)
                   comp.modelo = (
                       " ".join(filter(None, [
                           bios.mmodel if bios else None,
                           bios.smodel if bios else None
                       ])).strip() or comp.modelo
                   )
                   comp.numero_serie = (bios.ssn if bios and bios.ssn else comp.numero_serie)
                   comp.processador = hardware.processor_t or comp.processador
                   comp.memoria = str(hardware.memory) if hardware.memory not in (None, "") else comp.memoria
                   comp.hd = str(total_hd_mb) if total_hd_mb else comp.hd
                   sistema_anterior =  comp.sistema_operacional # mantém em MB, como na tela
                   comp.sistema_operacional = hardware.os_name or comp.sistema_operacional
                   #print(f" comp: {comp.hostname} - Sistema Anterior: {sistema_anterior} - Sistema Atual: {hardware.os_name}")
                   comp.save()

        print("Fim do populate_hardware_data")
        logger.info("Fim do populate_hardware_data")
        logger.info("Dados de hardware e componentes atualizados com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro ao processar os dados da API: {str(e)}")
        logger.exception("Exceção completa:")
        raise
        
    finally:
        # Restaurar timeout original
        if 'original_timeout' in locals():
            socket.setdefaulttimeout(original_timeout)
        
        # Fechar sessão se existir
        if 'session' in locals():
            session.close()