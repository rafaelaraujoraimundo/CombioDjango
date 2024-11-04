import django.conf
from django.utils import timezone
from celery import shared_task
import requests
from requests.auth import HTTPBasicAuth
import logging
from .models import AccountInfo, BIOS, CPU, Hardware, Memory, Software, Storage, UsuarioDesligamento
from decouple import config
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def populate_hardware_data():
    url = "http://172.16.0.15/ocsapi/v1/computers?start=0&limit=1000"
    username = config("OCS_USER")
    password = config("OCS_PASSWORD")

    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        
        if response.status_code == 200:
            response_data = response.json()
            
            # Iterar pelos computadores (ID é a chave)
            for computer_id, computer_data in response_data.items():
                print(f"Processando hardware ID: {computer_id}")
                
                # Criar ou atualizar hardware
                hardware, created = Hardware.objects.update_or_create(
                    id=computer_data["hardware"].get("ID"),  # Assumindo que a chave principal seja ID
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
                        "last_come": computer_data["hardware"].get("LASTCOME"),
                        "last_date": computer_data["hardware"].get("LASTDATE"),
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
                    Software.objects.create(
                        hardware=hardware,
                        architecture=software_data.get("ARCHITECTURE"),
                        bitswidth=software_data.get("BITSWIDTH"),
                        comments=software_data.get("COMMENTS"),
                        filename=software_data.get("FILENAME"),
                        filesize=software_data.get("FILESIZE"),
                        folder=software_data.get("FOLDER"),
                        guid=software_data.get("GUID"),
                        install_date=software_data.get("INSTALLDATE"),
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

            logger.info("Dados de hardware e componentes atualizados com sucesso!")
        else:
            logger.error(f"Erro na requisição à API: {response.status_code}")
    
    except Exception as e:
        logger.error(f"Erro ao processar os dados da API: {str(e)}")


def verificar_bloqueios_pendentes():
    # Busca todos os registros que têm qualquer bloqueio como False
    registros_pendentes = UsuarioDesligamento.objects.filter(
        bloqueio_email=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_fluig=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_datasul=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_monday=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_qualiteam=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_portal_chamados=False
    ) | UsuarioDesligamento.objects.filter(
        bloqueio_usuario_impressora=False
    )

    if registros_pendentes.exists():
        # Cria a tabela HTML com estilização de cores
        mensagem_html = """
        <p>Os seguintes usuários possuem sistemas pendentes de bloqueio:</p>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
            <tr>
                <th>Usuário</th>
                <th>Email</th>
                <th>Fluig</th>
                <th>Datasul</th>
                <th>Monday</th>
                <th>Qualiteam</th>
                <th>Portal de Chamados</th>
                <th>Usuário da Impressora (Matriz)</th>
            </tr>
        """
        
        for registro in registros_pendentes:
            mensagem_html += f"""
                <tr>
                    <td>{registro.usuario}</td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_email else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_email else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_fluig else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_fluig else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_datasul else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_datasul else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_monday else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_monday else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_qualiteam else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_qualiteam else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_portal_chamados else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_portal_chamados else 'Bloqueado'}
                    </td>
                    <td style="background-color: {'#ffcccc' if not registro.bloqueio_usuario_impressora else '#ccffcc'};">
                        {'Pendente' if not registro.bloqueio_usuario_impressora else 'Bloqueado'}
                    </td>
                </tr>
            """
        
        mensagem_html += "</table>"

        # Envia o e-mail usando send_mail com o corpo em HTML
        send_mail(
            subject="Alerta: Bloqueios Pendentes de Usuários",
            message="Os seguintes usuários possuem sistemas pendentes de bloqueio. Confira o conteúdo em HTML para mais detalhes.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['rafael.araujo@combioenergia.com.br'],
            html_message=mensagem_html  # Define o corpo do e-mail em HTML
        )