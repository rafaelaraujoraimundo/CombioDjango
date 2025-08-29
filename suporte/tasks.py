import django.conf
from django.contrib import messages
import django.db
from django.utils import timezone
from celery import shared_task
import requests
from requests.auth import HTTPBasicAuth
import logging
from django.db import transaction
from administration.views import User
from requests_oauthlib import OAuth1Session
from .models import UsuarioDesligamento, UsuarioFluig, MS365Tenant, UsuarioM365
from administration.models import ServidorFluig
from decouple import config
from django.core.mail import send_mail
from django.conf import settings
import json
from django.db.models import Q
from .m365_service import MS365ApiService

logger = logging.getLogger(__name__)

@shared_task
def verificar_bloqueios_pendentes():
    # Algum campo = False -> entra no relatório
    registros_pendentes = UsuarioDesligamento.objects.filter(
        Q(bloqueio_email=False) |
        Q(bloqueio_fluig=False) |
        Q(bloqueio_datasul=False) |
        Q(bloqueio_monday=False) |
        Q(bloqueio_portal_chamados=False) |
        Q(bloqueio_usuario_impressora=False) |
        Q(backup_email=False) |
        Q(backup_onedrive=False) |
        Q(backup_desktop=False) |
        Q(backup_desktop_C=False) |
        Q(backup_desktop_documentos=False) |
        Q(backup_desktop_download=False) |
        Q(backup_keepit=False) |
        Q(devolucao_computador=False) |
        Q(devolucao_celular=False) |
        Q(devolucao_periferico=False)
    )

    if not registros_pendentes.exists():
        return  # nada a enviar

    # Monta linhas apenas com: Usuário, Data Limite, Usuário Inclusão e Pendências
    rows_html = []
    for r in registros_pendentes:
        faltantes = []
        if not r.bloqueio_email:              faltantes.append("Email")
        if not r.bloqueio_fluig:              faltantes.append("Fluig")
        if not r.bloqueio_datasul:            faltantes.append("Datasul")
        if not r.bloqueio_monday:             faltantes.append("Monday")
        if not r.bloqueio_portal_chamados:    faltantes.append("Portal Chamados")
        if not r.bloqueio_usuario_impressora: faltantes.append("Impressora")
        if not r.backup_email:                 faltantes.append("Backup Email")
        if not r.backup_onedrive:              faltantes.append("Backup OneDrive")
        if not r.backup_desktop:               faltantes.append("Backup Área de Trabalho")
        if not r.backup_desktop_C:             faltantes.append("Backup Disco C")
        if not r.backup_desktop_documentos:    faltantes.append("Backup Documentos")
        if not r.backup_desktop_download:      faltantes.append("Backup Downloads")
        if not r.backup_keepit:                faltantes.append("Backup Keepit")
        if not r.devolucao_computador:         faltantes.append("Devolução Computador")
        if not r.devolucao_celular:            faltantes.append("Devolução Celular")
        if not r.devolucao_periferico:         faltantes.append("Devolução Periféricos")

        pendencias_html = (
            '<span style="color:#2e7d32;font-weight:700;">Bloqueio Completo</span>'
            if not faltantes else '<br>'.join(faltantes)
        )
        data_limite = r.data_limite.strftime('%d/%m/%Y') if r.data_limite else 'Não definida'
        usuario_inclusao = getattr(r, 'usuario_cadastro', '') or ''

        rows_html.append(f"""
            <tr>
                <td>{r.usuario}</td>
                <td>{data_limite}</td>
                <td>{usuario_inclusao}</td>
                <td>{pendencias_html}</td>
            </tr>
        """)

    mensagem_html = f"""
        <p>Os seguintes usuários possuem pendências nos sistemas e processos:</p>
        <table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:13px;">
            <thead>
                <tr style="background:#f2f2f2;">
                    <th>Usuário</th>
                    <th>Data Limite</th>
                    <th>Usuário Inclusão</th>
                    <th>Pendências</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows_html)}
            </tbody>
        </table>
    """

    # *** manter exatamente este trecho ***
    usuarios = User.objects.filter(enviar_email_desligados=True).only("email")
    emails = [u.email for u in usuarios if u.email]

    if emails:
        send_mail(
            subject="Alerta: Bloqueios e Processos Pendentes de Usuários",
            message="Pendências detectadas. Veja o HTML.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            html_message=mensagem_html
        )

@shared_task
def update_usuario_fluig():
    try:
        print("Iniciando atualização de usuários Fluig")
        servidor_fluig = ServidorFluig.objects.get(id=1)
        oauth = OAuth1Session(
            servidor_fluig.client_key,
            client_secret=servidor_fluig.consumer_secret,
            resource_owner_key=servidor_fluig.access_token,
            resource_owner_secret=servidor_fluig.access_secret
        )

        url = servidor_fluig.url + "/api/public/2.0/users/listAll?limit=800"
        response = oauth.get(url, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            data = response.json().get('content', [])
            with transaction.atomic():
                for user in data:
                    login = user.get("login")
                    email = user.get("email", "")
                    code = user.get("code", "")
                    full_name = user.get("fullName", "")
                    is_active = user.get("isActive", False)

                    # Update or create UsuarioFluig entry
                    UsuarioFluig.objects.update_or_create(
                        login=login,
                        defaults={
                            "email": email,
                            "code": code,
                            "full_name": full_name,
                            "is_active": is_active,
                        },
                    )
            print("Finalizando atualização de usuários Fluig")
        else:
            print(f"Falha ao buscar dados de usuários: {response.status_code} - {response.text}")
    except ServidorFluig.DoesNotExist:
        print("Servidor Fluig não configurado corretamente.")


@shared_task
def substituir_usuario_fluig(json_data):
    try:
        logger.info("Iniciando substituição de usuário no Fluig")
        
        # Obter credenciais do servidor Fluig
        servidor_fluig = ServidorFluig.objects.get(id=1)
        oauth = OAuth1Session(
            servidor_fluig.client_key,
            client_secret=servidor_fluig.consumer_secret,
            resource_owner_key=servidor_fluig.access_token,
            resource_owner_secret=servidor_fluig.access_secret
        )

        # URL para substituição de usuário
        url = servidor_fluig.url + "/api/public/bpm/substituteUser/create"
        headers = {'Content-Type': 'application/json'}

        # Executar a requisição POST para substituir usuário
        response = oauth.post(url, headers=headers, json=json_data)

        # Verificar resposta
        if response.status_code == 200:
            logger.info("Substituição de usuário realizada com sucesso.")
        else:
            logger.error(f"Falha na substituição de usuário: {response.status_code} - {response.text}")
            # Possível retorno de falha para tratamento na view ou log detalhado
            return {"status": "error", "message": f"Falha na substituição de usuário: {response.status_code} - {response.text}"}

    except ObjectDoesNotExist:
        logger.error("Servidor Fluig não configurado corretamente.")
        return {"status": "error", "message": "Servidor Fluig não configurado corretamente."}

    except Exception as e:
        logger.error(f"Ocorreu um erro ao tentar substituir o usuário: {e}")
        return {"status": "error", "message": f"Ocorreu um erro ao tentar substituir o usuário: {e}"}

    return {"status": "success", "message": "Substituição de usuário realizada com sucesso."}


@shared_task
def atualizar_usuarios_m365():
    tenants = MS365Tenant.objects.all()
    logger.info('Iniciando atualizando do M365')
    print('Iniciando atualizando do M365')
    for tenant in tenants:
        service = MS365ApiService(tenant)
        usuarios, erro = service.list_users()

        if erro:
            logger.error(f"Erro ao listar usuários do tenant {tenant.nome}: {erro}")
            print(f"Erro ao listar usuários do tenant {tenant.nome}: {erro}")
            continue
        logger.info('Iniciando Tenant: ' + tenant.nome_empresa )
        print('Iniciando Tenant: ' + tenant.nome_empresa )
        print('Apagando todos os dados')
        total = UsuarioM365.objects.filter(tenant=tenant).count()
        print('total de usuarios apagados: ' + total )
        UsuarioM365.objects.all().delete()
        print('Todos os dados apagados')
        for user in usuarios:
            email = user.get('mail') or user.get('userPrincipalName')
            if not email:
                continue

            defaults = {
                'display_name': user.get('displayName', ''),
                'given_name': user.get('givenName', ''),
                'surname': user.get('surname', ''),
                'job_title': user.get('jobTitle', ''),
                'department': user.get('department', ''),
                'office_location': user.get('officeLocation', ''),
                'mobile_phone': user.get('mobilePhone', ''),
                'business_phones': ", ".join(user.get('businessPhones', [])),
                'user_type': user.get('userType', ''),
                'account_enabled': user.get('accountEnabled', False),
                'created_at': user.get('createdDateTime'),
                'language': user.get('preferredLanguage', ''),
                'manager_name': user.get('managerDisplayName', ''),
                'manager_email': user.get('managerMail', ''),
                'manager_title': user.get('managerJobTitle', ''),
                'tenant': tenant
            }

            UsuarioM365.objects.update_or_create(email=email, defaults=defaults)
        logger.info('Termino Tenant' + tenant.nome_empresa )
        print('Termino Tenant' + tenant.nome_empresa )
    logger.info('termino da Atualização do M365')
    print('termino da Atualização do M365')